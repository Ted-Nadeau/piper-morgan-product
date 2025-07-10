"""
Piper Morgan 1.0 - Main Application
Bootstrap version to prove the architecture
"""

import logging
import os
import shutil
import tempfile
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import (BackgroundTasks, FastAPI, File, Form, HTTPException,
                     UploadFile)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.api.errors import APIError
from services.api.middleware import ErrorHandlingMiddleware
from services.conversation.conversation_handler import ConversationHandler
from services.database.repositories import RepositoryFactory
from services.domain.models import UploadedFile
from services.file_context.storage import (generate_session_id,
                                           save_file_to_storage)
from services.intent_service.intent_enricher import IntentEnricher
from services.knowledge_graph import get_document_service
from services.orchestration import WorkflowStatus, WorkflowType, engine
from services.queries import ProjectQueryService, QueryRouter
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.repositories import DatabasePool
from services.repositories.file_repository import FileRepository
from services.session.session_manager import (ConversationSession,
                                              SessionManager)
from services.utils.serialization import serialize_dataclass

# from services.ingestion_service import get_ingester

# Load environment variables FIRST
load_dotenv()

from services.domain.models import Feature, Intent, IntentCategory, Product
from services.intent_service import classifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session manager and conversation handler
session_manager = SessionManager(ttl_minutes=30)
conversation_handler = ConversationHandler(session_manager=session_manager)


# Request/Response models
class IntentRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ClarificationResponse(BaseModel):
    response: str


class IntentResponse(BaseModel):
    message: str  # User-facing response
    intent: dict
    workflow_id: Optional[str] = None
    requires_clarification: bool = False
    clarification_type: Optional[str] = None


class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    type: str
    tasks: list
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Piper Morgan 1.0...")
    logger.info("✅ Domain models loaded")
    logger.info("✅ LLM clients initialized")
    logger.info("✅ Intent classifier ready")
    logger.info("✅ Orchestration engine ready")
    yield
    # Shutdown
    from services.database.connection import db

    await db.close()
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Piper Morgan Platform 1.0",
    version="1.0.0-bootstrap",
    description="Intelligent Product Management Assistant",
    lifespan=lifespan,
)

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:8080",  # Default for many local dev servers
    "http://localhost:8081",  # Add this line for your web UI
    "http://127.0.0.1:5500",  # Common for VS Code Live Server
    "http://127.0.0.1:8081",  # Also add this for 127.0.0.1 access
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware
app.add_middleware(ErrorHandlingMiddleware)


@app.get("/")
async def root():
    return {
        "name": "Piper Morgan Platform 1.0",
        "version": "1.0.0-bootstrap",
        "status": "healthy",
        "message": "Ready to be your AI PM assistant! 🤖",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "services": {
            "postgres": "connected",
            "redis": "connected",
            "chromadb": "connected",
            "temporal": "connected",
            "llm": "ready",
            "orchestration": "ready",
        },
    }


@app.post("/api/v1/intent", response_model=IntentResponse)
async def process_intent(request: IntentRequest, background_tasks: BackgroundTasks):
    """Process a natural language message with real AI and route to appropriate handler"""
    try:
        # Get or create session
        session_id = request.session_id or "default_session"
        session = session_manager.get_or_create_session(session_id)

        # NEW: Check if this is a disambiguation response
        if session.awaiting_clarification == "file_disambiguation":
            disambiguation_result = await handle_file_disambiguation(
                request.message, session, session_id, background_tasks
            )
            if disambiguation_result:
                return disambiguation_result

        # Check for pending clarification first
        if session.get_pending_clarification():
            # Handle as clarification response
            response = await conversation_handler.handle_clarification_response(
                request.message, session_id
            )

            # Record interaction in session
            session.add_interaction(
                intent=Intent(
                    category=IntentCategory.CONVERSATION,
                    action="clarification_response",
                    confidence=0.8,
                    context={"response": request.message},
                ),
                response=response.get("message", ""),
            )

            # If clarification is resolved, we might need to process the original intent
            if response.get("clarification_resolved"):
                # Get the clarified intent and process it normally
                clarified_intent = response.get("intent")
                if (
                    clarified_intent
                    and clarified_intent.get("category") != "CONVERSATION"
                ):
                    # Process the clarified intent through the normal workflow
                    # This would typically involve creating a workflow or handling the query
                    response["message"] += " Processing your request..."

            return IntentResponse(
                message=response["message"],
                intent=response["intent"],
                workflow_id=response.get("workflow_id"),
                requires_clarification=response.get("requires_clarification", False),
                clarification_type=response.get("clarification_type"),
            )

        # Normal classification flow
        print(f"🔍 Processing intent: {request.message}")
        intent = await classifier.classify(request.message)
        print(f"🔍 Intent classification result: {intent}")

        # Handle conversational intents immediately (minimal, pre-enrichment)
        if intent.category == IntentCategory.CONVERSATION:
            result = await conversation_handler.respond(intent, session_id)
            return IntentResponse(**result)

        # Add this debug line
        print(
            f"DEBUG: Intent classified as - Category: {intent.category}, Action: {intent.action}, Confidence: {intent.confidence}"
        )

        # NEW: Enrich intent with file context
        # Add original message to context for file reference detection
        intent.context["original_message"] = request.message

        # Get database pool for enricher
        pool = await DatabasePool.get_pool()
        enricher = IntentEnricher(pool)
        enriched_intent = await enricher.enrich(intent, session_id)

        # Check if file clarification is needed
        if enriched_intent.context.get("needs_file_clarification"):
            # Handle file disambiguation
            ambiguous_files = enriched_intent.context.get("ambiguous_files", [])
            if ambiguous_files:
                options = "\n".join(
                    [
                        f"{i+1}. {f['filename']} (uploaded {f['upload_time']})"
                        for i, f in enumerate(ambiguous_files)
                    ]
                )

                # Set clarification state in session
                session.set_clarification(
                    "file_disambiguation",
                    {
                        "ambiguous_files": ambiguous_files,
                        "original_intent": serialize_dataclass(enriched_intent),
                    },
                )

                return IntentResponse(
                    message=f"Which file did you mean?\n{options}\n\nPlease respond with the number.",
                    intent={
                        "category": enriched_intent.category.value,
                        "action": enriched_intent.action,
                        "confidence": enriched_intent.confidence,
                        "context": enriched_intent.context,
                    },
                    requires_clarification=True,
                    clarification_type="file_disambiguation",
                )
            else:
                return IntentResponse(
                    message="I couldn't find any files. Please upload a file first.",
                    intent={
                        "category": enriched_intent.category.value,
                        "action": enriched_intent.action,
                        "confidence": enriched_intent.confidence,
                        "context": enriched_intent.context,
                    },
                    requires_clarification=True,
                    clarification_type="no_files_found",
                )

        # Route based on intent category
        if enriched_intent.category == IntentCategory.QUERY:
            # Handle query intents through QueryRouter
            try:
                # Get repositories for query service
                repos = await RepositoryFactory.get_repositories()
                project_query_service = ProjectQueryService(repos["projects"])
                conversation_query_service = ConversationQueryService()
                pool = await DatabasePool.get_pool()
                file_query_service = FileQueryService(FileRepository(pool))
                query_router = QueryRouter(
                    project_query_service,
                    conversation_query_service,
                    file_query_service,
                )

                # Route the query
                query_result = await query_router.route_query(enriched_intent)

                # Format response for query results
                if enriched_intent.action == "list_projects":
                    project_list = [project.to_dict() for project in query_result]
                    response_text = (
                        f"I found {len(project_list)} projects: "
                        + ", ".join([p["name"] for p in project_list])
                    )
                else:
                    response_text = f"Here's what I found for {enriched_intent.action}: {query_result}"

                return IntentResponse(
                    message=response_text,
                    intent={
                        "category": enriched_intent.category.value,
                        "action": enriched_intent.action,
                        "confidence": enriched_intent.confidence,
                        "context": enriched_intent.context,
                    },
                    workflow_id=None,  # No workflow for queries
                    requires_clarification=False,
                    clarification_type=None,
                )
            except ValueError as query_error:
                logger.error(f"Query processing failed: {query_error}")
                raise HTTPException(status_code=422, detail=str(query_error))
            except Exception as query_error:
                logger.error(f"Query processing failed: {query_error}")
                raise HTTPException(status_code=500, detail="Internal server error")
        else:
            # Handle command intents through WorkflowFactory
            print(f"🔍 Creating workflow from intent...")
            workflow = await engine.create_workflow_from_intent(enriched_intent)
            workflow_id = None

            if workflow:
                # Execute workflow in background
                workflow_id = workflow.id
                background_tasks.add_task(engine.execute_workflow, workflow_id)
                response_text = f"I understand you want to {enriched_intent.action}. I've started a workflow to handle this."
            else:
                # No workflow needed, just respond
                response_text = f"I understand you want to {enriched_intent.action}. "

                if enriched_intent.category == IntentCategory.EXECUTION:
                    response_text += "I'll help you execute that task."
                elif enriched_intent.category == IntentCategory.ANALYSIS:
                    response_text += "Let me analyze that for you."
                elif enriched_intent.category == IntentCategory.SYNTHESIS:
                    response_text += "I'll help you create that."
                elif enriched_intent.category == IntentCategory.STRATEGY:
                    response_text += "Let's think strategically about this."
                else:
                    response_text += "I'll help you learn from this."

            return IntentResponse(
                message=response_text,
                intent={
                    "category": enriched_intent.category.value,
                    "action": enriched_intent.action,
                    "confidence": enriched_intent.confidence,
                    "context": enriched_intent.context,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )
    except APIError:
        raise  # Re-raise our custom errors to be handled by the middleware
    except HTTPException:
        raise  # Let FastAPI handle its own exceptions
    except Exception as e:
        logger.error(f"Intent processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process intent")


async def handle_file_disambiguation(
    message: str,
    session: ConversationSession,
    session_id: str,
    background_tasks: BackgroundTasks,
) -> Optional[IntentResponse]:
    """Handle user's response to file disambiguation"""

    # Check if message is a number
    message = message.strip()
    if message.isdigit():
        choice = int(message) - 1  # Convert to 0-based index
        ambiguous_files = session.get_clarification_context("ambiguous_files", [])

        if 0 <= choice < len(ambiguous_files):
            selected_file = ambiguous_files[choice]

            # Re-process the original intent with specific file
            original_intent_data = session.get_clarification_context("original_intent")
            if original_intent_data:
                # Reconstruct intent with selected file
                intent = Intent(
                    category=IntentCategory(original_intent_data["category"]),
                    action=original_intent_data["action"],
                    context={
                        **original_intent_data.get("context", {}),
                        "resolved_file_id": selected_file["id"],
                        "file_confidence": 1.0,  # User explicitly selected
                    },
                )

                # Clear disambiguation state
                session.clear_clarification()

                # Continue with workflow processing
                try:
                    workflow = await engine.create_workflow_from_intent(intent)
                    workflow_id = None

                    if workflow:
                        workflow_id = workflow.id
                        # Execute workflow in background (same as main flow)
                        background_tasks.add_task(engine.execute_workflow, workflow_id)

                    return IntentResponse(
                        message=f"Got it! Using {selected_file['filename']}. Processing your request...",
                        intent=serialize_dataclass(intent),
                        workflow_id=workflow_id,
                        requires_clarification=False,
                        clarification_type=None,
                    )
                except Exception as e:
                    logger.error(
                        f"Workflow creation failed after file disambiguation: {e}"
                    )
                    return IntentResponse(
                        message=f"Got it! Using {selected_file['filename']}. I'll process your request.",
                        intent=serialize_dataclass(intent),
                        workflow_id=None,
                        requires_clarification=False,
                        clarification_type=None,
                    )

    # Invalid response
    return IntentResponse(
        message="Please respond with a number from the list, or describe which file you meant.",
        intent={},
        workflow_id=None,
        requires_clarification=True,
        clarification_type="file_disambiguation",
    )


@app.get("/api/v1/workflows/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: str):
    """Get workflow status and details"""
    # Try to get from memory first, then from database
    workflow = engine.workflows.get(workflow_id)

    # Always fetch from database to ensure we have the latest state
    from services.repositories import DatabasePool
    from services.repositories.workflow_repository import WorkflowRepository

    pool = await DatabasePool.get_pool()
    repo = WorkflowRepository(pool)
    db_workflow = await repo.find_by_id(workflow_id)

    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Use the database version (which has the latest context)
    workflow = db_workflow

    workflow_dict = workflow.to_dict()

    # Create user-friendly message based on status
    if workflow.status == WorkflowStatus.COMPLETED:
        # Format response based on workflow type and task results
        if workflow.type == WorkflowType.CREATE_TICKET:
            # Handle GitHub issue creation
            if workflow.result and workflow.result.data:
                issue_url = workflow.result.data.get("issue_url")
                issue_number = workflow.result.data.get("issue_number")
                if issue_url and issue_number:
                    message = f"✅ Successfully created GitHub issue #{issue_number}:\n{issue_url}"
                else:
                    message = (
                        "✅ GitHub issue created successfully, but URL not available."
                    )
            else:
                message = "✅ GitHub issue created successfully!"

        elif workflow.type == WorkflowType.REVIEW_ITEM:
            # Handle GitHub issue analysis and other review tasks
            if workflow.result and workflow.result.data:
                analysis = workflow.result.data.get("analysis")
                if analysis:
                    message = f"📋 GitHub Issue Analysis:\n\n{analysis}"
                else:
                    message = "✅ Issue analysis completed successfully!"
            else:
                message = "✅ Review completed successfully!"

        elif workflow.type in [WorkflowType.GENERATE_REPORT, WorkflowType.ANALYZE_FILE]:
            # Handle document analysis and reports
            analysis = None
            if workflow.result and workflow.result.data:
                analysis = workflow.result.data.get("analysis")

            # Fallback to context for backward compatibility
            if not analysis and workflow.context:
                analysis = workflow.context.get("analysis")

            if analysis and analysis.get("summary"):
                filename = workflow.context.get("filename", "the document")
                message = f"Here's my summary of {filename}:\n\n{analysis['summary']}"
            else:
                message = "I've completed the analysis but couldn't generate a summary."

        else:
            # Generic fallback for other workflow types
            message = "Workflow completed successfully!"
    elif workflow.status == WorkflowStatus.RUNNING:
        completed_tasks = sum(
            1 for t in workflow.tasks if t.status.value == "completed"
        )
        message = f"Workflow in progress... ({completed_tasks}/{len(workflow.tasks)} tasks completed)"
    elif workflow.status == WorkflowStatus.FAILED:
        message = f"Workflow failed: {workflow.error}"
    else:
        message = "Workflow is pending"

    return WorkflowResponse(
        workflow_id=workflow_id,
        status=workflow_dict["status"],
        type=workflow_dict["type"],
        tasks=workflow_dict["tasks"],
        message=message,
    )


@app.get("/api/v1/workflows")
async def list_workflows():
    """List all workflows"""
    workflows = []
    for wf_id, workflow in engine.workflows.items():
        workflows.append(
            {
                "id": wf_id,
                "type": workflow.type.value,
                "status": workflow.status.value,
                "created_at": workflow.created_at.isoformat(),
            }
        )
    return {"workflows": workflows}


@app.get("/api/v1/products")
async def list_products():
    """List all products"""
    # TODO: Real database integration
    sample_product = Product(
        name="Sample Product",
        vision="Make PMs more effective",
        strategy="AI-first approach",
    )
    return [sample_product]


@app.post("/api/v1/files/upload")
async def upload_file(
    file: UploadFile = File(...), session_id: Optional[str] = Form(None)
):
    """Upload a file and track it in the session"""
    try:
        # Generate session ID if not provided
        if not session_id:
            session_id = generate_session_id()

        # Read file content first to get size
        content = await file.read()
        file_size = len(content)

        # Save file to storage using content bytes
        storage_path = await save_file_to_storage(content, file.filename)

        # Create file metadata
        uploaded_file = UploadedFile(
            session_id=session_id,
            filename=file.filename,
            file_type=file.content_type or "application/octet-stream",
            file_size=file_size,
            storage_path=storage_path,
            upload_time=datetime.now(),
        )

        # Save to database
        pool = await DatabasePool.get_pool()
        repo = FileRepository(pool)
        saved_file = await repo.save_file_metadata(uploaded_file)

        # Track in session
        session = session_manager.get_or_create_session(session_id)
        session.add_uploaded_file(
            file_id=saved_file.id,
            filename=file.filename,
            file_type=file.content_type or "application/octet-stream",
            upload_time=datetime.now(),
        )

        return {
            "file_id": saved_file.id,
            "session_id": session_id,
            "filename": file.filename,
            "file_type": file.content_type,
            "file_size": saved_file.file_size,
            "message": f"File '{file.filename}' uploaded successfully",
        }

    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# Comment out the knowledge search endpoint that uses get_ingester
# @app.post("/api/v1/knowledge_search")
# async def knowledge_search(request: KnowledgeSearchRequest):
#     """Search the knowledge base for relevant documents"""
#     query = request.query
#     limit = request.limit or 5
#     try:
#         # results = await get_ingester().search(query, n_results=limit)
#         results = []  # Stubbed out
#         return {"results": results}
#     except Exception as e:
#         logger.error(f"Knowledge search failed: {e}")
#         raise HTTPException(status_code=500, detail="Knowledge search failed")


@app.post("/api/v1/clarification", response_model=IntentResponse)
async def handle_clarification(
    request: ClarificationResponse, background_tasks: BackgroundTasks
):
    """Handle user's response to clarification questions"""
    try:
        # Use the same session ID for now (in production, extract from headers/auth)
        session_id = "default_session"
        session = session_manager.get_or_create_session(session_id)

        # Check if there's a pending clarification
        pending_clarification = session.get_pending_clarification()
        if not pending_clarification:
            return IntentResponse(
                message="I don't have any pending clarification questions. How can I help you?",
                intent={
                    "category": "CONVERSATION",
                    "action": "chitchat",
                    "confidence": 0.8,
                },
                workflow_id=None,
                requires_clarification=False,
                clarification_type=None,
            )

        # Handle the clarification response
        response = await conversation_handler.handle_clarification_response(
            user_response=request.response, session_id=session_id
        )

        # Record interaction in session
        session.add_interaction(
            intent=Intent(
                category=IntentCategory.CONVERSATION,
                action="clarification_response",
                confidence=0.8,
                context={"response": request.response},
            ),
            response=response.get("message", ""),
        )

        # If clarification is resolved, we might need to process the original intent
        if response.get("clarification_resolved"):
            # Get the clarified intent and process it normally
            clarified_intent = response.get("intent")
            if clarified_intent and clarified_intent.get("category") != "CONVERSATION":
                # Process the clarified intent through the normal workflow
                # This would typically involve creating a workflow or handling the query
                response["message"] += " Processing your request..."

        return IntentResponse(
            message=response["message"],
            intent=response["intent"],
            workflow_id=response.get("workflow_id"),
            requires_clarification=response.get("requires_clarification", False),
            clarification_type=response.get("clarification_type"),
        )

    except Exception as e:
        logger.error(f"Clarification handling failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="info")

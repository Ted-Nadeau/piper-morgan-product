"""
Piper Morgan Web Interface
Simple FastAPI app for interacting with the main Piper Morgan Platform API
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import structlog
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add project root to path for imports (same as CLI)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Standup API moved to backend - only config loader needed for legacy compatibility
from services.configuration.piper_config_loader import piper_config_loader

# Configuration service import - eliminates hardcoded values
from services.configuration.port_configuration_service import get_port_configuration

# Import personality integration
from web.personality_integration import (
    PersonalityResponseEnhancer,
    PiperConfigParser,
    WebPersonalityConfig,
)

# Startup phase management (Phase 2 of Issue #385 - INFR-MAINT-REFACTOR)
from web.startup import lifespan

# Import error response utilities (Pattern 034: Error Handling Standards)
from web.utils.error_responses import internal_error, not_found_error, validation_error

# Server Configuration - now using centralized configuration service
port_config = get_port_configuration()
DEFAULT_PORT = port_config.web_port
API_BASE_URL = port_config.get_api_base_url()

# Initialize logger
logger = structlog.get_logger()


# Pattern-007: Graceful degradation helper functions
def _extract_degradation_message(error: Exception) -> str:
    """
    Extract user-friendly degradation message from exception.

    Maps technical exceptions to actionable user guidance following Pattern-007.
    Never exposes technical details, always provides recovery guidance.

    Args:
        error: The exception that occurred

    Returns:
        User-friendly degradation message with recovery guidance
    """
    error_msg = str(error).lower()

    # Database connection failures
    if "database" in error_msg or "connection" in error_msg or "psycopg" in error_msg:
        return "Database temporarily unavailable. Please ensure Docker is running and try again."

    # File service failures
    if "file" in error_msg and ("service" in error_msg or "unavailable" in error_msg):
        return "File service temporarily unavailable. Please try again in a few moments."

    # Circuit breaker failures
    if "circuit breaker" in error_msg or "circuit" in error_msg:
        return "Service temporarily overloaded. Please try again in a few moments."

    # Conversation service failures
    if "conversation" in error_msg and ("service" in error_msg or "unavailable" in error_msg):
        return "Conversation service temporarily unavailable. Please try again shortly."

    # Generic degradation message
    return "Service temporarily unavailable. Please try again in a few moments."


def _create_degradation_response(message: str, degradation_msg: str) -> dict:
    """
    Create structured IntentResponse for graceful degradation.

    Implements Pattern-007 requirement: maintain consistent response structure
    even when services fail. Returns 200 OK with user-friendly message.

    Args:
        message: Original user message
        degradation_msg: User-friendly degradation message

    Returns:
        Structured IntentResponse dict with degradation message
    """
    # Try to infer basic intent from message for better UX
    message_lower = message.lower()
    action = "unknown"
    category = "query"

    # Simple intent inference for common patterns
    if "list" in message_lower and "project" in message_lower:
        action = "list_projects"
    elif (
        any(word in message_lower for word in ["count", "how many", "number of"])
        and "project" in message_lower
    ):
        action = "count_projects"
    elif "default project" in message_lower:
        action = "get_default_project"
    elif "show" in message_lower and "project" in message_lower:
        action = "get_default_project"
    elif "read" in message_lower and "file" in message_lower:
        action = "read_file_contents"
    elif any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
        action = "greeting"
        category = "conversation"

    return {
        "message": degradation_msg,
        "intent": {
            "action": action,
            "category": category,
            "confidence": 0.0,  # Low confidence due to degradation
            "context": {},
        },
        "workflow_id": None,
        "requires_clarification": False,
        "clarification_type": None,
        "suggestions": [],
    }


def _extract_user_context(request: Request) -> dict:
    """
    Extract user context from request state for template injection.

    Retrieves authenticated user information from request.state (set by auth middleware)
    and returns it as a dict for passing to templates. The navigation component uses this
    to populate the user dropdown menu with the actual username instead of the default
    "user" placeholder.

    Args:
        request: FastAPI Request object with user_claims/user_id in state

    Returns:
        dict with 'user_id', 'username', and 'is_admin' keys for template context
    """
    user_id = getattr(request.state, "user_id", "user")

    # Try to get username from user_claims if available
    username = user_id  # Default to user_id
    user_claims = getattr(request.state, "user_claims", None)
    if user_claims and hasattr(user_claims, "username"):
        username = user_claims.username
    elif user_claims and isinstance(user_claims, dict) and "username" in user_claims:
        username = user_claims["username"]

    # Extract is_admin flag from user claims (SEC-RBAC Phase 3)
    is_admin = False
    if user_claims:
        is_admin = getattr(user_claims, "is_admin", False) or (
            isinstance(user_claims, dict) and user_claims.get("is_admin", False)
        )

    return {"user_id": user_id, "username": username, "is_admin": is_admin}


# Create FastAPI app with lifespan
app = FastAPI(
    title="Piper Morgan UI",
    description="Web Interface for the Piper Morgan Platform",
    lifespan=lifespan,
)

# Issue #283: Enhanced error handling with user-friendly messages
# Mount BEFORE other middleware so it catches exceptions from all handlers
try:
    from web.middleware.enhanced_error_middleware import EnhancedErrorMiddleware

    app.add_middleware(EnhancedErrorMiddleware)
    logger.info("✅ EnhancedErrorMiddleware registered (Issue #283 - CORE-ALPHA-ERROR-MESSAGES)")
except Exception as e:
    logger.error(f"⚠️ Failed to mount EnhancedErrorMiddleware: {e}")

# Issue #283: Custom HTTPException handler for friendly error messages
# This catches FastAPI's built-in HTTPException errors (401, 404, etc) which bypass middleware
try:
    from fastapi import HTTPException, Request
    from fastapi.responses import JSONResponse

    from services.ui_messages.user_friendly_errors import UserFriendlyErrorService

    error_service = UserFriendlyErrorService()

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """
        Convert FastAPI HTTPException to user-friendly messages.

        This handler intercepts FastAPI's built-in error responses (401, 404, etc)
        that bypass normal middleware exception handling, and converts them using
        UserFriendlyErrorService for consistent user-friendly messaging.
        """
        # Get friendly message based on status code and exception detail
        friendly_message = None

        if exc.status_code == 401:
            # Authentication errors
            friendly_message = "Let's try logging in again. Your session may have expired."
        elif exc.status_code == 403:
            # Permission errors
            friendly_message = "You don't have permission to access that. Please contact your administrator if you think this is incorrect."
        elif exc.status_code == 404:
            # Not found errors
            friendly_message = "I couldn't find that. It may have been moved or deleted."
        elif exc.status_code == 422:
            # Validation errors
            friendly_message = f"I couldn't process that request: {str(exc.detail)}"
        elif exc.status_code >= 500:
            # Server errors
            friendly_message = (
                "Something went wrong on my end. I've logged the details for debugging."
            )
        else:
            # Fallback to original detail
            friendly_message = str(exc.detail)

        # CRITICAL: Log technical details server-side for debugging
        logger.error(
            "http_exception",
            status_code=exc.status_code,
            detail=str(exc.detail),
            path=request.url.path,
            method=request.method,
        )

        # Return friendly message to user
        return JSONResponse(status_code=exc.status_code, content={"message": friendly_message})

    logger.info(
        "✅ HTTPException handler registered (Issue #283 - catches 401, 404, 403, 422 errors)"
    )
except Exception as e:
    logger.error(f"⚠️ Failed to register HTTPException handler: {e}")

# Issue #283: APIError exception handler for dependency-level errors
# Dependencies execute BEFORE middleware, so exceptions raised in Depends() need
# this handler to be caught and converted to friendly messages
try:
    from services.api.errors import APIError

    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        """
        Handle APIError exceptions with user-friendly messages.

        This catches APIError raised anywhere in the application,
        including from FastAPI dependencies like get_current_user.

        Since dependencies execute before middleware, this exception
        handler is the appropriate layer to convert APIError to
        friendly messages for users.
        """
        # Get friendly message based on error code and status code
        friendly_message = None

        if exc.status_code == 401:
            # Authentication errors
            friendly_message = "Let's try logging in again. Your session may have expired."
        elif exc.status_code == 403:
            # Permission errors
            friendly_message = (
                "You don't have permission to access that. Please contact your administrator."
            )
        elif exc.status_code == 404:
            # Not found errors
            friendly_message = "I couldn't find that. It may have been moved or deleted."
        elif exc.status_code == 422:
            # Validation errors
            friendly_message = (
                "I couldn't process that request. Please check your input and try again."
            )
        elif exc.status_code >= 500:
            # Server errors
            friendly_message = (
                "Something went wrong on my end. I've logged the details for debugging."
            )
        else:
            # Fallback
            friendly_message = "An error occurred. Please try again."

        # CRITICAL: Log technical details for debugging
        logger.error(
            "api_error",
            error_code=exc.error_code,
            status_code=exc.status_code,
            details=exc.details,
            path=request.url.path,
            method=request.method,
        )

        # Return friendly message to user
        return JSONResponse(status_code=exc.status_code, content={"message": friendly_message})

    logger.info(
        "✅ APIError exception handler registered (Issue #283 - catches dependency-level errors)"
    )
except Exception as e:
    logger.error(f"⚠️ Failed to register APIError handler: {e}")

# GREAT-4B: Intent Enforcement Middleware
from web.middleware.intent_enforcement import IntentEnforcementMiddleware

app.add_middleware(IntentEnforcementMiddleware)
logger.info("✅ IntentEnforcementMiddleware registered (GREAT-4B)")

# Phase 1: Mount remaining API routers using factory pattern (Issue #385 - INFR-MAINT-REFACTOR)
# Previously: ~90 lines of duplicate try/catch boilerplate
# Now: Consolidated calls to RouterInitializer factory for consistency
from web.router_initializer import RouterInitializer

RouterInitializer.mount_router(app, "web.api.routes.auth", "router", "Auth API")
RouterInitializer.mount_router(app, "web.api.routes.files", "router", "Files API")
RouterInitializer.mount_router(app, "web.api.routes.documents", "router", "Documents API")
RouterInitializer.mount_router(
    app, "services.api.todo_management", "todo_management_router", "Todos API"
)
RouterInitializer.mount_router(app, "web.api.routes.lists", "router", "Lists API")
RouterInitializer.mount_router(app, "web.api.routes.todos", "router", "Todos SEC-RBAC API")
RouterInitializer.mount_router(app, "web.api.routes.projects", "router", "Projects API")
RouterInitializer.mount_router(app, "web.api.routes.feedback", "router", "Feedback API")
RouterInitializer.mount_router(
    app, "web.api.routes.knowledge_graph", "router", "Knowledge Graph API"
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=str(project_root / "templates"))

# Initialize personality components
config_parser = PiperConfigParser()
personality_enhancer = PersonalityResponseEnhancer()


@app.get("/debug-markdown", response_class=HTMLResponse)
async def debug_markdown(request: Request):
    return HTMLResponse(
        content="""<!DOCTYPE html>
<html>
<head>
    <title>Markdown Debug Test</title>
    <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { border: 1px solid #ccc; margin: 10px 0; padding: 10px; }
        .raw { background: #f0f0f0; padding: 10px; margin: 5px 0; }
        .rendered { background: #e8f4f8; padding: 10px; margin: 5px 0; }
        h1 { color: #2c3e50; border-bottom: 1px solid #ecf0f1; }
        h2 { color: #34495e; }
        strong { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>Markdown Renderer Debug Test</h1>

    <div class="test-section">
        <h3>Test 1: Check if renderMarkdown function exists</h3>
        <div class="rendered" id="test1"></div>
    </div>

    <div class="test-section">
        <h3>Test 2: Simple Header</h3>
        <div class="raw">Input: "# Header 1"</div>
        <div class="rendered" id="test2"></div>
    </div>

    <div class="test-section">
        <h3>Test 3: Your Failing Example</h3>
        <div class="raw">Input: "Here's my summary... # Header ## Subheader"</div>
        <div class="rendered" id="test3"></div>
    </div>

    <script src="/assets/markdown-renderer.js?v=2"></script>
    <script>
        // Test if the function is loaded
        if (typeof renderMarkdown === 'function') {
            document.getElementById('test1').innerHTML = '✅ renderMarkdown function loaded successfully';

            // Test 2: Simple header
            document.getElementById('test2').innerHTML = renderMarkdown('# Header 1');

            // Test 3: Your failing example
            const failingText = `Here's my summary: # Piper Morgan Summary ## File Type This appears to be documentation.`;
            document.getElementById('test3').innerHTML = renderMarkdown(failingText);

        } else {
            document.getElementById('test1').innerHTML = '❌ renderMarkdown function not loaded - check console for errors';
            console.error('renderMarkdown function not found');
        }
    </script>
</body>
</html>"""
    )


@app.get("/")
async def home(request: Request):
    """Render home page"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("home.html", {"request": request, "user": user_context})


# GREAT-1B: Bug #166 Fix - Add missing workflow status endpoint
# Phase 2: REST-compliant error handling (Pattern 034)
@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str, request: Request):
    """Get workflow status to prevent UI polling hang (Bug #166 fix)"""
    try:
        # Validate workflow_id
        if not workflow_id or not workflow_id.strip():
            return validation_error(
                "Workflow ID required", {"field": "workflow_id", "issue": "Cannot be empty"}
            )

        # Get OrchestrationEngine from app state
        orchestration_engine = getattr(request.app.state, "orchestration_engine", None)

        if orchestration_engine is None:
            # Service unavailable - return 500
            logger.error("OrchestrationEngine not available for workflow status check")
            return internal_error("OrchestrationEngine not available")

        # For GREAT-1B, return a simple status response
        # This prevents the infinite polling that causes UI hangs
        # Bug #xpv: Changed message to not claim completion when status unknown
        return {
            "workflow_id": workflow_id,
            "status": "processing",  # Neutral status (not "completed" - may need clarification)
            "message": "",  # No message - avoids misleading "completed" claim
            "tasks": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

    except ValueError as e:
        # Known validation errors
        return validation_error(str(e))
    except Exception as e:
        # Unexpected errors - log and return 500
        logger.error(f"Error getting workflow {workflow_id}: {e}", exc_info=True)
        return internal_error()


# Version Endpoint - Single source of truth from pyproject.toml
@app.get("/api/v1/version")
async def get_version():
    """
    Get application version information

    Returns version from pyproject.toml (single source of truth)
    plus environment and deployment metadata.
    """
    from services.version import get_version_info

    try:
        return get_version_info()
    except Exception as e:
        logger.error(f"Error getting version info: {e}", exc_info=True)
        return internal_error("Unable to retrieve version information")


# Personality Configuration Endpoints
# Phase 2: REST-compliant error handling (Pattern 034)
@app.get("/api/personality/profile/{user_id}")
async def get_personality_profile(user_id: str = "default"):
    """Get user's personality preferences"""
    try:
        config = config_parser.load_personality_config(user_id)
        return {"status": "success", "data": config.to_dict(), "user_id": user_id}
    except FileNotFoundError:
        # Profile not found - return 404
        return not_found_error(
            f"Personality profile not found for user: {user_id}",
            {"resource": "personality_profile", "user_id": user_id},
        )
    except Exception as e:
        # Load failure - return 500
        logger.error(f"Failed to load personality profile for {user_id}: {e}", exc_info=True)
        return internal_error("Failed to load personality profile")


@app.put("/api/personality/profile/{user_id}")
async def update_personality_profile(user_id: str, request: Request):
    """Update user's personality preferences"""
    try:
        data = await request.json()
        config = WebPersonalityConfig.from_dict(data)

        success = config_parser.save_personality_config(config, user_id)

        if success:
            return {
                "status": "success",
                "data": config.to_dict(),
                "user_id": user_id,
                "message": "Personality preferences updated successfully",
            }
        else:
            # Save failed - return 500
            logger.error(f"Failed to save personality config for {user_id}")
            return internal_error("Failed to save personality configuration")
    except (ValueError, KeyError, TypeError) as e:
        # Invalid data - return 422
        return validation_error(
            f"Invalid personality configuration data: {str(e)}",
            {"user_id": user_id, "error": str(e)},
        )
    except Exception as e:
        # Unexpected error - return 500
        logger.error(f"Error updating personality profile for {user_id}: {e}", exc_info=True)
        return internal_error("Failed to update personality profile")


@app.post("/api/personality/enhance")
async def enhance_response(request: Request):
    """Enhance a response with personality"""
    try:
        data = await request.json()
        content = data.get("content", "")
        user_id = data.get("user_id", "default")
        confidence = data.get("confidence", 0.5)

        # Validate required fields
        if not content or not isinstance(content, str):
            return validation_error(
                "Content is required and must be a string",
                {"field": "content", "issue": "Required field missing or invalid type"},
            )

        # Load personality config
        config = config_parser.load_personality_config(user_id)

        # Enhance response
        enhanced_content = personality_enhancer.enhance_response(content, config, confidence)

        return {
            "status": "success",
            "data": {
                "original_content": content,
                "enhanced_content": enhanced_content,
                "personality_config": config.to_dict(),
                "confidence": confidence,
            },
        }
    except (ValueError, TypeError) as e:
        # Validation errors - return 422
        return validation_error(f"Invalid enhancement request: {str(e)}", {"error": str(e)})
    except Exception as e:
        # Processing errors - return 500
        logger.error(f"Error enhancing response: {e}", exc_info=True)
        return internal_error("Failed to enhance response")


@app.get("/api/standup")
async def standup_proxy(
    format: str = Query("raw", description="Response format: 'raw' or 'human-readable'"),
    personality: bool = Query(False, description="Apply personality enhancement"),
):
    """Proxy standup requests to backend API"""
    import httpx

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/api/v1/standup/generate",
                params={"format": format, "personality": personality},
            )
            return response.json()
    except httpx.ConnectError as e:
        # Backend service unavailable - return 500
        logger.error(f"Backend API connection failed: {e}")
        return internal_error("Backend API unavailable")
    except Exception as e:
        # Unexpected error - return 500
        logger.error(f"Standup proxy error: {e}", exc_info=True)
        return internal_error("Failed to proxy standup request")


@app.post("/api/v1/intent")
async def process_intent(request: Request):
    """
    Phase 2B: Thin HTTP adapter for intent processing

    Delegates all business logic to IntentService.
    Route only handles HTTP concerns (request parsing, response formatting, status codes).

    Implements Pattern-007 (Async Error Handling) graceful degradation:
    - Returns 200 OK with structured response even when services unavailable
    - Provides user-friendly degradation messages
    - Maintains consistent IntentResponse structure

    Business logic: services/intent/intent_service.py
    """
    try:
        # Parse HTTP request
        request_data = await request.json()
        message = request_data.get("message", "")
        session_id = request_data.get("session_id", "default_session")

        # Get IntentService from app state (dependency injection)
        intent_service = getattr(request.app.state, "intent_service", None)

        if intent_service is None:
            # Pattern-007: Graceful degradation - return 200 with user-friendly message
            logger.warning("IntentService not available - returning degradation response")
            return _create_degradation_response(
                message,
                "Database temporarily unavailable. Please ensure Docker is running and try again.",
            )

        # Delegate to service (all business logic)
        result = await intent_service.process_intent(message=message, session_id=session_id)

        # Format HTTP response from service result
        response = {
            "message": result.message,
            "intent": result.intent_data,
            "workflow_id": result.workflow_id,
            "requires_clarification": result.requires_clarification,
            "clarification_type": result.clarification_type,
            "suggestions": result.suggestions,  # Phase 3: Pattern suggestions
            "preferences": result.preferences,  # Issue #248: Preference detection results
        }

        # Add error fields if present (semantic/validation errors from service)
        if result.error:
            return validation_error(
                result.error, {"error_type": result.error_type} if result.error_type else None
            )

        return response

    except Exception as e:
        # Pattern-007: Graceful degradation - return 200 with user-friendly message
        logger.error(f"Intent route error: {str(e)}", exc_info=True)

        # Extract user-friendly degradation message from exception
        degradation_msg = _extract_degradation_message(e)

        # Return structured IntentResponse instead of 500 error
        return _create_degradation_response(
            request_data.get("message", "") if "request_data" in locals() else "", degradation_msg
        )


@app.get("/standup")
async def standup_ui(request: Request):
    """Render standup UI"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("standup.html", {"request": request, "user": user_context})


@app.get("/personality-preferences")
async def personality_preferences_ui(request: Request):
    """Serve the personality preferences interface"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "personality-preferences.html", {"request": request, "user": user_context}
    )


@app.get("/learning")
async def learning_dashboard_ui(request: Request):
    """Serve the learning dashboard interface"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "learning-dashboard.html", {"request": request, "user": user_context}
    )


@app.get("/settings")
async def settings_index_ui(request: Request):
    """Serve the settings index page (G2: Settings Index Page)"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings-index.html", {"request": request, "user": user_context}
    )


@app.get("/account")
async def account_settings_ui(request: Request):
    """Serve the account settings page (Coming Soon)"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("account.html", {"request": request, "user": user_context})


@app.get("/files")
async def files_ui(request: Request):
    """Serve the files page (Coming Soon)"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("files.html", {"request": request, "user": user_context})


@app.get("/settings/integrations")
async def integrations_page(request: Request):
    """Integrations management page - Coming soon"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "integrations.html", {"request": request, "user": user_context}
    )


@app.get("/lists", response_class=HTMLResponse)
async def lists_ui(request: Request):
    """Lists management page with permission-aware UI (Issue #376)"""
    user_context = _extract_user_context(request)
    lists_data = []
    return templates.TemplateResponse(
        "lists.html", {"request": request, "user": user_context, "lists": lists_data}
    )


@app.post("/api/v1/lists", response_model=dict)
async def create_list(request: Request):
    """Create a new list owned by current user (Issue #379)"""
    user_id = request.state.user_id
    is_admin = getattr(request.state, "is_admin", False)

    try:
        # Parse JSON body
        body = await request.json()
        name = body.get("name", "").strip()
        description = body.get("description", "").strip()

        if not name:
            raise HTTPException(status_code=400, detail="List name is required")

        # Import domain model and repository
        import services.domain.models as domain
        from services.database.connection import db
        from services.repositories.universal_list_repository import UniversalListRepository

        # Get database session
        if not db._initialized:
            await db.initialize()

        async with await db.get_session() as session:
            # Create list with owner_id and empty shared_with
            list_obj = domain.List(
                name=name,
                description=description,
                owner_id=user_id,
                item_type="todo",  # Default item type
                shared_with=[],  # Start with no shares
            )

            # Create list in database
            list_repo = UniversalListRepository(session)
            created_list = await list_repo.create_list(list_obj)
            await session.commit()

        # Return created list data
        return {
            "id": str(created_list.id),
            "name": created_list.name,
            "description": created_list.description,
            "owner_id": created_list.owner_id,
            "created_at": created_list.created_at.isoformat() if created_list.created_at else None,
            "shared_with": [],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating list: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create list: {str(e)}")


@app.get("/todos", response_class=HTMLResponse)
async def todos_ui(request: Request):
    """Todos management page with permission-aware UI (Issue #376)"""
    user_context = _extract_user_context(request)
    todos_data = []
    return templates.TemplateResponse(
        "todos.html", {"request": request, "user": user_context, "todos": todos_data}
    )


@app.post("/api/v1/todos", response_model=dict)
async def create_todo(request: Request):
    """Create a new todo owned by current user (Issue #379)"""
    user_id = request.state.user_id
    is_admin = getattr(request.state, "is_admin", False)

    try:
        # Parse JSON body
        body = await request.json()
        text = body.get("text", "").strip()
        due_date = body.get("due_date", "")

        if not text:
            raise HTTPException(status_code=400, detail="Todo text is required")

        # Import domain model and repository
        import services.domain.models as domain
        from services.database.connection import db
        from services.repositories.universal_list_repository import UniversalListRepository

        # Get database session
        if not db._initialized:
            await db.initialize()

        async with await db.get_session() as session:
            # Create todo with owner_id and empty shared_with
            todo_obj = domain.List(
                name=text,  # Store text as name for lists-based todos
                description=due_date,  # Store due_date as description
                owner_id=user_id,
                item_type="todo",
                shared_with=[],  # Start with no shares
            )

            # Create todo in database
            repo = UniversalListRepository(session)
            created_todo = await repo.create_list(todo_obj)
            await session.commit()

        # Return created todo data
        return {
            "id": str(created_todo.id),
            "text": created_todo.name,
            "due_date": created_todo.description,
            "owner_id": created_todo.owner_id,
            "status": "pending",
            "created_at": created_todo.created_at.isoformat() if created_todo.created_at else None,
            "shared_with": [],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create todo: {str(e)}")


@app.get("/projects", response_class=HTMLResponse)
async def projects_ui(request: Request):
    """Projects management page with permission-aware UI (Issue #376)"""
    user_context = _extract_user_context(request)
    projects_data = []
    return templates.TemplateResponse(
        "projects.html", {"request": request, "user": user_context, "projects": projects_data}
    )


@app.get("/settings/privacy")
async def privacy_settings_ui(request: Request):
    """Serve the privacy & data settings page (Coming Soon)"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "privacy-settings.html", {"request": request, "user": user_context}
    )


@app.get("/settings/advanced")
async def advanced_settings_ui(request: Request):
    """Serve the advanced settings page (Coming Soon)"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "advanced-settings.html", {"request": request, "user": user_context}
    )


@app.get("/health/config")
async def health_config():
    """
    Configuration health check endpoint.

    Returns validation status for all service configurations.
    CORE-GREAT-2D: Configuration Validation
    """
    from services.infrastructure.config.config_validator import ConfigValidator

    validator = ConfigValidator()
    summary = validator.get_summary()

    # Return 200 with summary (even if some services invalid)
    # This is a health check endpoint, not a gate
    return {
        "status": "healthy" if summary["all_valid"] else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "validation": summary,
    }


@app.get("/api/admin/intent-monitoring")
async def intent_monitoring():
    """
    Intent enforcement monitoring endpoint.

    Returns current middleware configuration and monitoring status.
    CORE-GREAT-4B: Intent Enforcement
    """
    return IntentEnforcementMiddleware.get_monitoring_status()


@app.get("/api/admin/intent-cache-metrics")
async def intent_cache_metrics(request: Request):
    """
    Intent cache performance metrics endpoint.

    Returns cache hit rate, size, and performance statistics.
    CORE-GREAT-4B Phase 3: Intent Caching
    """
    # Get IntentService from app state
    intent_service = getattr(request.app.state, "intent_service", None)

    # GREAT-5 Phase 1.5: Fix attribute name (intent_classifier not classifier)
    if intent_service and hasattr(intent_service.intent_classifier, "cache"):
        metrics = intent_service.intent_classifier.cache.get_metrics()
        return {"cache_enabled": True, "metrics": metrics, "status": "operational"}
    else:
        return {"cache_enabled": False, "status": "not_configured"}


@app.post("/api/admin/intent-cache-clear")
async def clear_intent_cache(request: Request):
    """
    Clear the intent cache (admin only).

    Removes all cached intent classifications and resets metrics.
    CORE-GREAT-4B Phase 3: Intent Caching
    """
    # Get IntentService from app state
    intent_service = getattr(request.app.state, "intent_service", None)

    # GREAT-5 Phase 1.5: Fix attribute name (intent_classifier not classifier)
    if intent_service and hasattr(intent_service.intent_classifier, "cache"):
        intent_service.intent_classifier.cache.clear()
        return {"status": "cache_cleared", "message": "Intent cache cleared successfully"}
    else:
        return {"status": "cache_not_configured", "message": "Intent cache not available"}


@app.get("/api/admin/piper-config-cache-metrics")
async def piper_config_cache_metrics():
    """
    PIPER.md config cache performance metrics endpoint.

    Returns cache hit rate, age, and performance statistics for PIPER configuration caching.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.configuration.piper_config_loader import piper_config_loader

    metrics = piper_config_loader.get_cache_metrics()
    return {"cache_enabled": True, "metrics": metrics, "status": "operational"}


@app.post("/api/admin/piper-config-cache-clear")
async def clear_piper_config_cache():
    """
    Clear the PIPER.md config cache (admin only).

    Forces next PIPER.md load to read from disk.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.configuration.piper_config_loader import piper_config_loader

    piper_config_loader.clear_cache()
    return {"status": "cache_cleared", "message": "PIPER config cache cleared successfully"}


@app.get("/api/admin/user-context-cache-metrics")
async def user_context_cache_metrics():
    """
    User context cache performance metrics endpoint.

    Returns cache hit rate and session-level cache statistics.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    metrics = user_context_service.get_cache_metrics()
    return {"cache_enabled": True, "metrics": metrics, "status": "operational"}


@app.post("/api/admin/user-context-cache-clear")
async def clear_user_context_cache():
    """
    Clear the user context cache (admin only).

    Removes all cached user contexts. Next request will reload from PIPER.md.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    user_context_service.invalidate_cache()  # No session_id = clear all
    return {"status": "cache_cleared", "message": "User context cache cleared successfully"}


@app.get("/health")
async def health():
    """
    Health check endpoint - exempt from intent enforcement.

    Returns basic service status for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "message": "Piper Morgan web service is running",
        "timestamp": datetime.now().isoformat(),
        "services": {"web": "healthy", "intent_enforcement": "active"},
    }


@app.post("/api/admin/user-context-cache-invalidate/{session_id}")
async def invalidate_user_context(session_id: str):
    """
    Invalidate specific user's cached context (admin only).

    Args:
        session_id: Session identifier to invalidate

    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    user_context_service.invalidate_cache(session_id)
    return {
        "status": "invalidated",
        "session_id": session_id,
        "message": f"User context for session {session_id} invalidated",
    }


# Mount static files (MUST be last - after all routes)
# FastAPI/Starlette routing: routes are checked first, mounts last
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "assets")),
    name="assets",
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)


if __name__ == "__main__":
    import uvicorn

    print(f"🚀 Starting Piper Morgan Web Interface on {port_config.get_web_url()}")
    print(f"📊 Standup API: {port_config.get_web_url()}/api/standup")
    print(f"🌅 Standup UI: {port_config.get_web_url()}/standup")
    print(f"📖 API Docs: {port_config.get_web_url()}/docs")
    print(f"🔗 Backend API: {port_config.get_backend_url()}")
    print(
        f"\n🔧 Server Command: PYTHONPATH=. python -m uvicorn web.app:app --host {port_config.web_host} --port {port_config.web_port}"
    )
    uvicorn.run(app, host=port_config.web_host, port=port_config.web_port)

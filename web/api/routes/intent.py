"""
Intent Processing & Workflow Management API Routes

Provides endpoints for intent processing (Phase 2B: Thin HTTP adapter)
and workflow status tracking (Bug #166 fix).

Routes:
- POST /api/v1/intent - Process user intent message
- GET /api/v1/workflows/{workflow_id} - Get workflow status

Pattern-007: Implements graceful degradation (async error handling)
- Returns 200 OK with structured response even when services unavailable
- Provides user-friendly degradation messages
- Maintains consistent IntentResponse structure

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 419-658)
Now: Extracted to separate router module
"""

from datetime import datetime

import structlog
from fastapi import APIRouter, Request

from web.utils.error_responses import internal_error, validation_error

logger = structlog.get_logger()

# Router configuration
router = APIRouter(prefix="/api/v1", tags=["intent", "workflows"])


# Helper functions for graceful degradation (Pattern-007)
def _extract_degradation_message(error: Exception) -> str:
    """Extract a user-friendly message from an exception.

    Converts technical exceptions into user-understandable messages
    for graceful degradation (Pattern-007).

    Args:
        error: The exception to extract message from

    Returns:
        User-friendly degradation message string
    """
    error_str = str(error).lower()

    # Database/Connection errors
    if "database" in error_str or "connection" in error_str or "timeout" in error_str:
        return "Database service is temporarily unavailable. Please ensure Docker containers are running and try again."

    # LLM/API errors
    if "llm" in error_str or "api" in error_str or "openai" in error_str:
        return "AI service is temporarily unavailable. Please try again in a few moments."

    # File system errors
    if "file" in error_str or "path" in error_str:
        return "File system error. Please check your configuration and try again."

    # Config errors
    if "config" in error_str:
        return "Configuration error. Please verify your setup and try again."

    # Default message for unknown errors
    return "An unexpected error occurred. Please try again later."


def _create_degradation_response(message: str, degradation_msg: str) -> dict:
    """Create a structured IntentResponse with degradation message.

    Returns a properly formatted response even when services fail,
    following Pattern-007 (graceful degradation).

    Args:
        message: Original user message that failed to process
        degradation_msg: User-friendly error message

    Returns:
        Structured IntentResponse dict with degradation values
    """
    return {
        "message": message,
        "intent": {
            "type": "unknown",
            "confidence": 0,
            "action": "clarify",
        },
        "workflow_id": None,
        "requires_clarification": True,
        "clarification_type": "service_unavailable",
        "suggestions": [
            f"Unable to process your request right now ({degradation_msg})",
            "Please try again in a moment",
        ],
        "preferences": {},
        "error": degradation_msg,
        "error_type": "service_unavailable",
    }


@router.get("/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str, request: Request):
    """Get workflow status to prevent UI polling hang (Bug #166 fix)"""
    try:
        # Validate workflow_id
        if not workflow_id or not workflow_id.strip():
            return validation_error(
                "Workflow ID required",
                {"field": "workflow_id", "issue": "Cannot be empty"},
            )

        # Get OrchestrationEngine from app state
        orchestration_engine = getattr(
            request.app.state, "orchestration_engine", None
        )

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


@router.post("/intent")
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
        result = await intent_service.process_intent(
            message=message, session_id=session_id
        )

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
                result.error,
                {"error_type": result.error_type} if result.error_type else None,
            )

        return response

    except Exception as e:
        # Pattern-007: Graceful degradation - return 200 with user-friendly message
        logger.error(f"Intent route error: {str(e)}", exc_info=True)

        # Extract user-friendly degradation message from exception
        degradation_msg = _extract_degradation_message(e)

        # Return structured IntentResponse instead of 500 error
        return _create_degradation_response(
            request_data.get("message", "")
            if "request_data" in locals()
            else "",
            degradation_msg,
        )

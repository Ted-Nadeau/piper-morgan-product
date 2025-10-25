"""
Enhanced error middleware with user-friendly error messages.

Integrates with UserFriendlyErrorService to provide conversational error messages
while maintaining technical logging for debugging.

Issue #255 CORE-UX-ERROR-MESSAGING
"""

import logging
import traceback
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from services.api.errors import ERROR_MESSAGES, APIError
from services.infrastructure.logging.config import get_logger
from services.ui_messages.user_friendly_errors import ErrorSeverity, UserFriendlyErrorService

logger = get_logger(__name__)


class EnhancedErrorMiddleware(BaseHTTPMiddleware):
    """
    Enhanced error handling middleware with user-friendly messages.

    Features:
    - Converts technical errors to conversational messages
    - Provides recovery suggestions
    - Maintains technical logging for debugging
    - Handles both APIError and generic exceptions
    - Preserves correlation IDs for tracing
    """

    def __init__(self, app, include_technical_details: bool = False):
        super().__init__(app)
        self.error_service = UserFriendlyErrorService()
        self.include_technical_details = include_technical_details

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except APIError as exc:
            return await self._handle_api_error(request, exc)
        except Exception as exc:
            return await self._handle_generic_error(request, exc)

    async def _handle_api_error(self, request: Request, exc: APIError) -> JSONResponse:
        """Handle structured API errors with user-friendly messages"""

        # Get correlation context
        correlation_data = getattr(request.state, "correlation", {})
        request_id = correlation_data.get("request_id")
        session_id = correlation_data.get("session_id")

        # Get user-friendly message
        user_message = ERROR_MESSAGES.get(exc.error_code, "An unexpected error occurred.")

        # Format the message with details from the exception
        try:
            formatted_message = user_message.format(**exc.details)
        except (KeyError, TypeError):
            # Fallback if formatting fails
            formatted_message = user_message

        # Enhance with user-friendly error service for better recovery suggestions
        context = self._extract_context_from_request(request)
        user_action = self._extract_user_action_from_request(request)

        enhanced_error = self.error_service.make_user_friendly(
            exc, context=context, user_action=user_action
        )

        # Log the error with full technical details
        logger.error(
            "api_error_handled",
            event_type="api_error",
            error_code=exc.error_code,
            user_message=formatted_message,
            enhanced_message=enhanced_error["message"],
            recovery_suggestion=enhanced_error["recovery"],
            severity=enhanced_error["severity"],
            category=enhanced_error["category"],
            details=exc.details,
            session_id=session_id,
            request_id=request_id,
            url=str(request.url),
            method=request.method,
        )

        # Create response body
        response_body = {
            "status": "error",
            "message": enhanced_error["message"],
            "recovery_suggestion": enhanced_error["recovery"],
            "severity": enhanced_error["severity"],
            "category": enhanced_error["category"],
            "error_code": exc.error_code,
        }

        # Add technical details if enabled (for development)
        if self.include_technical_details:
            response_body["technical_details"] = {
                "original_message": str(exc),
                "error_type": type(exc).__name__,
                "details": exc.details,
            }

        # Add correlation ID for support
        if request_id:
            response_body["request_id"] = request_id

        return JSONResponse(status_code=exc.status_code, content=response_body)

    async def _handle_generic_error(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions with user-friendly messages"""

        # Get correlation context
        correlation_data = getattr(request.state, "correlation", {})
        request_id = correlation_data.get("request_id")
        session_id = correlation_data.get("session_id")

        # Extract context for better error messages
        context = self._extract_context_from_request(request)
        user_action = self._extract_user_action_from_request(request)

        # Get user-friendly error message
        enhanced_error = self.error_service.make_user_friendly(
            exc, context=context, user_action=user_action
        )

        # Log the full technical error for debugging
        logger.error(
            "unexpected_error_handled",
            event_type="unexpected_error",
            error_message=str(exc),
            error_type=type(exc).__name__,
            enhanced_message=enhanced_error["message"],
            recovery_suggestion=enhanced_error["recovery"],
            severity=enhanced_error["severity"],
            category=enhanced_error["category"],
            context=context,
            user_action=user_action,
            session_id=session_id,
            request_id=request_id,
            url=str(request.url),
            method=request.method,
            traceback=traceback.format_exc(),
            exc_info=True,
        )

        # Determine appropriate HTTP status code based on error type
        status_code = self._determine_status_code(exc, enhanced_error)

        # Create response body
        response_body = {
            "status": "error",
            "message": enhanced_error["message"],
            "recovery_suggestion": enhanced_error["recovery"],
            "severity": enhanced_error["severity"],
            "category": enhanced_error["category"],
        }

        # Add technical details if enabled (for development)
        if self.include_technical_details:
            response_body["technical_details"] = {
                "error_message": str(exc),
                "error_type": type(exc).__name__,
                "traceback": traceback.format_exc(),
            }

        # Add correlation ID for support
        if request_id:
            response_body["request_id"] = request_id

        return JSONResponse(status_code=status_code, content=response_body)

    def _extract_context_from_request(self, request: Request) -> str:
        """Extract context about what the user was trying to do"""

        # Extract from URL path
        path = request.url.path

        if "/api/v1/intent" in path:
            return "processing your request"
        elif "/api/v1/github" in path:
            return "accessing GitHub"
        elif "/api/v1/slack" in path:
            return "connecting to Slack"
        elif "/api/v1/knowledge" in path:
            return "searching the knowledge base"
        elif "/api/v1/workflow" in path:
            return "running a workflow"
        elif "/api/v1/learning" in path:
            return "learning from your patterns"
        elif "/api/v1/auth" in path:
            return "handling authentication"
        elif "/api/v1/users" in path:
            return "managing user data"
        else:
            return "processing your request"

    def _extract_user_action_from_request(self, request: Request) -> str:
        """Extract the user action from the request"""

        method = request.method.lower()
        path = request.url.path

        # Map HTTP methods to user actions
        if method == "get":
            if "list" in path or "search" in path:
                return "search"
            else:
                return "list"
        elif method == "post":
            return "create"
        elif method == "put" or method == "patch":
            return "update"
        elif method == "delete":
            return "delete"
        else:
            return "process"

    def _determine_status_code(self, exc: Exception, enhanced_error: dict) -> int:
        """Determine appropriate HTTP status code for generic exceptions"""

        # Map exception types to status codes (order matters for inheritance)
        if isinstance(exc, (FileNotFoundError, KeyError)):
            return 404
        elif isinstance(exc, TimeoutError):
            return 504
        elif isinstance(exc, PermissionError):
            return 403
        elif isinstance(exc, OSError):
            return 403
        elif isinstance(exc, (ValueError, TypeError)):
            return 422
        elif enhanced_error["category"] == "auth":
            return 401
        elif enhanced_error["category"] == "validation":
            return 422
        elif enhanced_error["category"] == "rate_limit":
            return 429
        else:
            return 500

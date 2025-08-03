import logging

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from services.infrastructure.logging.config import generate_request_id, get_logger

from .errors import ERROR_MESSAGES, APIError

# Configure structured logger
logger = get_logger(__name__)


class CorrelationMiddleware(BaseHTTPMiddleware):
    """Middleware to add correlation IDs to all requests"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Generate correlation IDs
        request_id = generate_request_id()
        session_id = request.headers.get("X-Session-ID")

        # Add correlation data to request state
        request.state.correlation = {"request_id": request_id, "session_id": session_id}

        # Create structured logger with correlation context
        correlation_logger = get_logger(name=__name__, session_id=session_id, request_id=request_id)

        # Log request start
        correlation_logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            user_agent=request.headers.get("user-agent"),
            event_type="request_start",
        )

        try:
            response = await call_next(request)

            # Log successful request
            correlation_logger.info(
                "request_completed", status_code=response.status_code, event_type="request_complete"
            )

            return response

        except Exception as e:
            # Log request error
            correlation_logger.error("request_error", error=str(e), event_type="request_error")
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except APIError as exc:
            # Handle our custom, structured API errors
            user_message = ERROR_MESSAGES.get(exc.error_code, "An unexpected error occurred.")

            # Format the message with details from the exception
            try:
                formatted_message = user_message.format(**exc.details)
            except KeyError:
                # Handle cases where a placeholder is in the message but not in the details
                formatted_message = user_message

            # Get correlation data from request state
            correlation_data = getattr(request.state, "correlation", {})
            request_id = correlation_data.get("request_id")
            session_id = correlation_data.get("session_id")

            # Create structured logger with correlation context
            correlation_logger = get_logger(
                name=__name__, session_id=session_id, request_id=request_id
            )

            correlation_logger.warning(
                "api_error_handled",
                error_code=exc.error_code,
                status_code=exc.status_code,
                details=exc.details,
                event_type="api_error",
            )

            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "code": exc.error_code,
                        "message": formatted_message,
                        "details": exc.details,
                    }
                },
            )
        except Exception as exc:
            # Handle unexpected Python exceptions
            # Get correlation data from request state
            correlation_data = getattr(request.state, "correlation", {})
            request_id = correlation_data.get("request_id")
            session_id = correlation_data.get("session_id")

            # Create structured logger with correlation context
            correlation_logger = get_logger(
                name=__name__, session_id=session_id, request_id=request_id
            )

            correlation_logger.error(
                "unexpected_internal_error", error=str(exc), event_type="internal_error"
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected internal error occurred. The technical team has been notified.",
                    }
                },
            )

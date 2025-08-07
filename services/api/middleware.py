"""
API Middleware for Piper Morgan
Handles request/response processing, error handling, and ethics boundary enforcement
"""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from services.api.errors import ERROR_MESSAGES, APIError
from services.ethics.boundary_enforcer import boundary_enforcer
from services.infrastructure.logging.config import generate_request_id, get_logger

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

        # Create correlation logger
        correlation_logger = get_logger(__name__, session_id=session_id, request_id=request_id)

        # Log request start
        correlation_logger.info(
            "request_start",
            event_type="request_start",
            method=request.method,
            url=str(request.url),
            session_id=session_id,
            request_id=request_id,
        )

        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)

            # Calculate response time
            response_time = (time.time() - start_time) * 1000

            # Log request complete
            correlation_logger.info(
                "request_complete",
                event_type="request_complete",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                response_time_ms=response_time,
                session_id=session_id,
                request_id=request_id,
            )

            return response

        except Exception as e:
            # Calculate response time
            response_time = (time.time() - start_time) * 1000

            # Log request error
            correlation_logger.error(
                "request_error",
                error=str(e),
                event_type="request_error",
                method=request.method,
                url=str(request.url),
                response_time_ms=response_time,
                session_id=session_id,
                request_id=request_id,
            )
            raise


class EthicsBoundaryMiddleware(BaseHTTPMiddleware):
    """Middleware for ethics boundary enforcement"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Skip ethics check for health endpoints and static files
        if request.url.path.startswith(("/health", "/static", "/docs", "/openapi")):
            return await call_next(request)

        try:
            # Perform ethics boundary check
            boundary_decision = await boundary_enforcer.enforce_boundaries(request)

            # If violation detected, return appropriate response
            if boundary_decision.violation_detected:
                logger.warning(
                    "boundary_violation_detected",
                    event_type="boundary_violation",
                    boundary_type=boundary_decision.boundary_type,
                    explanation=boundary_decision.explanation,
                    session_id=boundary_decision.session_id,
                    url=str(request.url),
                )

                # Return 403 Forbidden with explanation
                return Response(
                    status_code=403,
                    content=f"Boundary violation detected: {boundary_decision.explanation}",
                    media_type="text/plain",
                )

            # Continue with normal request processing
            return await call_next(request)

        except Exception as e:
            # Log ethics check error but don't block the request
            logger.error(
                "ethics_check_error",
                event_type="ethics_check_error",
                error=str(e),
                session_id=request.headers.get("X-Session-ID"),
                url=str(request.url),
            )

            # Continue with request processing even if ethics check fails
            return await call_next(request)


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
            except (KeyError, TypeError):
                # Fallback if formatting fails
                formatted_message = user_message

            # Log the error with correlation context
            correlation_data = getattr(request.state, "correlation", {})
            logger.error(
                "api_error",
                event_type="api_error",
                error_code=exc.error_code,
                details=exc.details,
                session_id=correlation_data.get("session_id"),
                request_id=correlation_data.get("request_id"),
            )

            return Response(
                status_code=exc.status_code,
                content=formatted_message,
                media_type="text/plain",
            )
        except Exception as e:
            # Handle unexpected errors
            correlation_data = getattr(request.state, "correlation", {})
            logger.error(
                "unexpected_error",
                event_type="unexpected_error",
                error=str(e),
                session_id=correlation_data.get("session_id"),
                request_id=correlation_data.get("request_id"),
            )

            return Response(
                status_code=500,
                content="An unexpected error occurred.",
                media_type="text/plain",
            )

import logging

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

from .errors import ERROR_MESSAGES, APIError

# Configure logger
logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except APIError as exc:
            # Handle our custom, structured API errors
            user_message = ERROR_MESSAGES.get(
                exc.error_code, "An unexpected error occurred."
            )

            # Format the message with details from the exception
            try:
                formatted_message = user_message.format(**exc.details)
            except KeyError:
                # Handle cases where a placeholder is in the message but not in the details
                formatted_message = user_message

            logger.warning(
                f"API Error Handled: {exc.error_code} - Status: {exc.status_code} - Details: {exc.details}",
                exc_info=True,
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
            logger.error(
                f"Unexpected Internal Server Error: {exc}",
                exc_info=True,
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

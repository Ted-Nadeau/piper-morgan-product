import logging
from typing import Any, Optional


class MCPErrorHandler:
    """Comprehensive error handling for MCP operations"""

    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        self.logger = logging.getLogger("MCPErrorHandler")

    def handle_extraction_failure(self, file_path: str, error: Exception) -> dict:
        self.logger.error(f"Extraction failed for {file_path}: {error}")
        return {
            "message": f"Failed to extract content from {file_path}.",
            "suggestion": "Check if the file is corrupted or unsupported. Try re-uploading or using a different file.",
            "error": str(error),
        }

    def handle_connection_timeout(self, operation: str, retry_count: int = 0) -> dict:
        self.logger.warning(
            f"Connection timeout during {operation}. Retry {retry_count}/{self.max_retries}"
        )
        if retry_count < self.max_retries:
            return {
                "message": f"Connection timed out during {operation}. Retrying...",
                "retry": True,
                "retry_count": retry_count + 1,
            }
        else:
            return {
                "message": f"Connection timed out during {operation} after {self.max_retries} retries.",
                "suggestion": "Check network connectivity or try again later.",
                "retry": False,
            }

    def handle_configuration_error(self, config_key: str, error: Exception) -> dict:
        self.logger.error(f"Configuration error: {config_key}: {error}")
        return {
            "message": f"Configuration error for '{config_key}'.",
            "suggestion": f"Verify the configuration value for '{config_key}'.",
            "error": str(error),
        }

    def handle_performance_degradation(self, metric: str, value: Any, threshold: Any) -> dict:
        self.logger.warning(f"Performance degradation: {metric}={value} (threshold={threshold})")
        return {
            "message": f"Performance issue detected: {metric} is {value}, expected < {threshold}.",
            "suggestion": "Consider scaling resources or optimizing the operation.",
        }

    def user_friendly_message(self, error: Exception) -> str:
        # Map known errors to user-friendly messages
        if hasattr(error, "message"):
            return str(error.message)
        return str(error)

    def recovery_suggestion(self, error: Exception) -> str:
        # Provide suggestions based on error type
        if isinstance(error, TimeoutError):
            return "Try again later or check your network connection."
        if isinstance(error, FileNotFoundError):
            return "Verify the file path and try again."
        return "Contact support if the issue persists."

    def automatic_retry(self, func, *args, **kwargs):
        # Retry a function up to max_retries on failure
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.warning(f"Retry {attempt+1}/{self.max_retries} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise

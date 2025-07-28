from typing import Any, Dict


class APIError(Exception):
    """Base class for all application-specific API errors."""

    def __init__(self, status_code: int, error_code: str, details: Dict[str, Any] = None):
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(f"API Error [{error_code}]")


# --- Intent Errors ---


class IntentClassificationFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(500, "INTENT_CLASSIFICATION_FAILED", details)


class LowConfidenceIntentError(APIError):
    def __init__(self, suggestions: str = "clarify your request", details: Dict[str, Any] = None):
        details = details or {}
        details["suggestions"] = suggestions
        super().__init__(422, "LOW_CONFIDENCE_INTENT", details)


# --- Workflow Errors ---


class WorkflowTimeoutError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(504, "WORKFLOW_TIMEOUT", details)


class TaskFailedError(APIError):
    def __init__(
        self,
        task_description: str = "a task",
        recovery_suggestion: str = "please try again",
        details: Dict[str, Any] = None,
    ):
        details = details or {}
        details["task_description"] = task_description
        details["recovery_suggestion"] = recovery_suggestion
        super().__init__(500, "TASK_FAILED", details)


# --- Integration Errors ---


class GitHubRateLimitError(APIError):
    def __init__(self, retry_after: int = 1, details: Dict[str, Any] = None):
        details = details or {}
        details["retry_after"] = retry_after
        super().__init__(429, "GITHUB_RATE_LIMIT", details)


class GitHubAuthFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(502, "GITHUB_AUTH_FAILED", details)


class SlackAuthFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(502, "SLACK_AUTH_FAILED", details)


# --- Knowledge Base Errors ---


class NoRelevantKnowledgeError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(404, "NO_RELEVANT_KNOWLEDGE", details)


class DocumentProcessingError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(500, "DOCUMENT_PROCESSING_FAILED", details)


# --- Centralized Error Messages ---

ERROR_MESSAGES = {
    # Intent errors
    "INTENT_CLASSIFICATION_FAILED": "I couldn't understand that request. Could you rephrase it?",
    "LOW_CONFIDENCE_INTENT": "I'm not so sure what you're asking for. Did you mean to '{suggestions}'?",
    # Workflow errors
    "WORKFLOW_TIMEOUT": "This is taking longer than expected. I'll keep working on it and notify you when done.",
    "TASK_FAILED": "I encountered an issue with {task_description}. As a suggestion, {recovery_suggestion}.",
    "CONTEXT_VALIDATION_FAILED": "{user_message}",
    # Integration errors
    "GITHUB_RATE_LIMIT": "GitHub is limiting our requests. Please try again in {retry_after} minutes.",
    "GITHUB_AUTH_FAILED": "I couldn't authenticate with GitHub. Please check your access token.",
    "SLACK_AUTH_FAILED": "I couldn't authenticate with Slack. Please check your access token.",
    # Knowledge base errors
    "NO_RELEVANT_KNOWLEDGE": "I don't have enough context about that. Could you provide more details?",
    "DOCUMENT_PROCESSING_FAILED": "I couldn't process that document. Please check the file format and try again.",
}

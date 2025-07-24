"""Orchestration and workflow exceptions"""

from typing import Any, Dict, List, Optional


class OrchestrationError(Exception):
    """Base exception for orchestration errors"""

    pass


class WorkflowValidationError(OrchestrationError):
    """Base exception for workflow validation errors"""

    def __init__(self, workflow_type: str, message: str):
        super().__init__(f"Workflow validation failed for {workflow_type}: {message}")
        self.workflow_type = workflow_type


class ContextValidationError(WorkflowValidationError):
    """Raised when workflow context validation fails"""

    def __init__(
        self,
        workflow_type: str,
        missing_fields: List[str] = None,
        invalid_fields: Dict[str, str] = None,
        message: Optional[str] = None,
    ):
        self.missing_fields = missing_fields or []
        self.invalid_fields = invalid_fields or {}

        if message:
            error_message = message
        else:
            parts = []
            if self.missing_fields:
                parts.append(f"Missing required fields: {', '.join(self.missing_fields)}")
            if self.invalid_fields:
                invalid_details = [
                    f"{field}: {error}" for field, error in self.invalid_fields.items()
                ]
                parts.append(f"Invalid fields: {'; '.join(invalid_details)}")
            error_message = "; ".join(parts) if parts else "Context validation failed"

        super().__init__(workflow_type, error_message)


class InsufficientContextError(ContextValidationError):
    """Raised when workflow has insufficient context to execute"""

    def __init__(self, workflow_type: str, required_fields: List[str]):
        super().__init__(
            workflow_type,
            missing_fields=required_fields,
            message=f"Insufficient context. Required fields: {', '.join(required_fields)}",
        )


class InvalidContextError(ContextValidationError):
    """Raised when workflow context contains invalid data"""

    def __init__(self, workflow_type: str, field_errors: Dict[str, str]):
        super().__init__(
            workflow_type, invalid_fields=field_errors, message=f"Invalid context data found"
        )

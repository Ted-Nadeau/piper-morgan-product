"""
Workflow Context Validation Service
Implements PM-057: Validation Rules & User Experience

Provides pre-execution validation for workflow context with user-friendly error messages.
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union

from services.api.errors import APIError
from services.shared_types import WorkflowType


class ContextValidationError(APIError):
    """Raised when workflow context validation fails"""

    def __init__(
        self,
        workflow_type: Union[WorkflowType, str],
        missing_fields: List[str],
        suggestions: List[str],
        details: Dict[str, Any] = None,
    ):
        details = details or {}
        # Handle both enum and string workflow types
        details["workflow_type"] = (
            workflow_type.value if hasattr(workflow_type, "value") else workflow_type
        )
        details["missing_fields"] = missing_fields
        details["suggestions"] = suggestions

        # Create user-friendly error message
        error_message = self._create_user_message(workflow_type, missing_fields, suggestions)

        super().__init__(422, "CONTEXT_VALIDATION_FAILED", details)
        self.user_message = error_message

    def _create_user_message(
        self,
        workflow_type: Union[WorkflowType, str],
        missing_fields: List[str],
        suggestions: List[str],
    ) -> str:
        """Create user-friendly error message with helpful suggestions"""

        workflow_names = {
            WorkflowType.CREATE_TICKET: "create a ticket",
            WorkflowType.LIST_PROJECTS: "list projects",
            WorkflowType.ANALYZE_FILE: "analyze a file",
            WorkflowType.GENERATE_REPORT: "generate a report",
            WorkflowType.REVIEW_ITEM: "review an item",
            WorkflowType.PLAN_STRATEGY: "plan strategy",
        }

        workflow_name = workflow_names.get(workflow_type, "complete this task")

        if "original_message" in missing_fields:
            return (
                f"To {workflow_name}, I need to know what you want me to do. "
                f"Please provide more details about your request."
            )

        if "project_id" in missing_fields and workflow_type == WorkflowType.CREATE_TICKET:
            return (
                f"To {workflow_name}, I need to know which project. "
                f"Try: 'create ticket for project [project name]' or "
                f"'create issue in [repository name]'"
            )

        if "file_id" in missing_fields and workflow_type == WorkflowType.ANALYZE_FILE:
            return (
                f"To {workflow_name}, I need to know which file to analyze. "
                f"Try: 'analyze the uploaded [filename]' or "
                f"'analyze [filename] from the session'"
            )

        if "github_url" in missing_fields and workflow_type == WorkflowType.REVIEW_ITEM:
            return (
                f"To {workflow_name}, I need a GitHub URL. "
                f"Try: 'review this issue: https://github.com/...' or "
                f"'analyze this pull request: [URL]'"
            )

        # Generic message with suggestions
        suggestion_text = " ".join(suggestions)
        return f"To {workflow_name}, I need more information. {suggestion_text}"


class WorkflowContextValidator:
    """
    Validates workflow context before execution with user-friendly error messages.

    Implements PM-057: Validation Rules & User Experience
    """

    def __init__(self):
        self.validation_rules = self._define_validation_rules()

    def _define_validation_rules(self) -> Dict[WorkflowType, Dict[str, Any]]:
        """Define validation rules for each workflow type"""
        return {
            WorkflowType.CREATE_TICKET: {
                "required_fields": ["original_message"],
                "conditional_fields": {
                    "project_id": "project context for repository resolution",
                    "repository": "GitHub repository information",
                },
                "suggestions": [
                    "Specify a project: 'create ticket for project [name]'",
                    "Provide repository: 'create issue in [repo]'",
                    "Use default repository if configured",
                ],
            },
            WorkflowType.LIST_PROJECTS: {
                "required_fields": ["original_message"],
                "conditional_fields": {},
                "suggestions": ["Try: 'list all projects' or 'show my projects'"],
            },
            WorkflowType.ANALYZE_FILE: {
                "required_fields": ["original_message"],
                "conditional_fields": {
                    "file_id": "file reference for analysis",
                    "resolved_file_id": "resolved file reference",
                },
                "suggestions": [
                    "Specify a file: 'analyze the uploaded [filename]'",
                    "Reference session file: 'analyze [filename] from this session'",
                    "Upload a file first if needed",
                ],
            },
            WorkflowType.GENERATE_REPORT: {
                "required_fields": ["original_message"],
                "conditional_fields": {
                    "file_id": "file reference for report generation",
                    "project_id": "project context for enhanced reports",
                },
                "suggestions": [
                    "Specify what to report on: 'generate report on [topic]'",
                    "Include file reference: 'generate report from [filename]'",
                    "Add project context for better results",
                ],
            },
            WorkflowType.REVIEW_ITEM: {
                "required_fields": ["original_message"],
                "conditional_fields": {"github_url": "GitHub URL for issue/PR review"},
                "suggestions": [
                    "Provide GitHub URL: 'review this issue: [URL]'",
                    "Include issue number: 'review issue #123 in [repo]'",
                    "Specify pull request: 'review PR #456'",
                ],
            },
            WorkflowType.PLAN_STRATEGY: {
                "required_fields": ["original_message"],
                "conditional_fields": {"project_id": "project context for strategy planning"},
                "suggestions": [
                    "Specify strategy scope: 'plan strategy for [project/area]'",
                    "Include project context for better planning",
                    "Provide specific objectives or goals",
                ],
            },
        }

    def validate_workflow_context(
        self, workflow_type: WorkflowType, context: Dict[str, Any]
    ) -> None:
        """
        Validate workflow context and raise user-friendly error if validation fails.

        Args:
            workflow_type: Type of workflow to validate
            context: Workflow context dictionary

        Raises:
            ContextValidationError: If validation fails with user-friendly message
        """
        if workflow_type not in self.validation_rules:
            # Unknown workflow type - allow it to proceed
            return

        rules = self.validation_rules[workflow_type]
        missing_fields = []
        suggestions = []

        # Check required fields
        for field in rules.get("required_fields", []):
            if not self._field_exists_and_valid(context, field):
                missing_fields.append(field)

        # Check conditional fields (provide suggestions if missing)
        for field, description in rules.get("conditional_fields", {}).items():
            if not self._field_exists_and_valid(context, field):
                suggestions.append(f"Consider providing {description}")

        # Add workflow-specific suggestions
        suggestions.extend(rules.get("suggestions", []))

        # Raise error if required fields are missing
        if missing_fields:
            raise ContextValidationError(
                workflow_type=workflow_type,
                missing_fields=missing_fields,
                suggestions=suggestions,
                details={
                    "context_keys": list(context.keys()),
                    "workflow_type": workflow_type.value,
                },
            )

    def _field_exists_and_valid(self, context: Dict[str, Any], field: str) -> bool:
        """Check if a field exists and has a valid value"""
        if field not in context:
            return False

        value = context[field]

        # Check for empty strings, None, empty lists, etc.
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, list) and len(value) == 0:
            return False
        if isinstance(value, dict) and len(value) == 0:
            return False

        return True

    def validate_github_url(self, url: str) -> bool:
        """Validate GitHub URL format"""
        if not url:
            return False

        # Basic GitHub URL pattern
        github_pattern = r"https?://github\.com/[^/]+/[^/]+(/issues/\d+|/pull/\d+)?"
        return bool(re.match(github_pattern, url))

    def get_validation_summary(
        self, workflow_type: WorkflowType, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get validation summary without raising exceptions"""
        try:
            self.validate_workflow_context(workflow_type, context)
            return {"valid": True, "missing_fields": [], "suggestions": []}
        except ContextValidationError as e:
            return {
                "valid": False,
                "missing_fields": e.details.get("missing_fields", []),
                "suggestions": e.details.get("suggestions", []),
                "user_message": e.user_message,
            }


# Global validator instance
workflow_validator = WorkflowContextValidator()

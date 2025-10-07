"""
Workflow Factory - Creates workflows from intents
PM-002 Implementation
PM-008 Github integration
PM-057 Context Validation Framework
GREAT-4F: QUERY fallback for mis-classified intents
"""

import logging
from datetime import datetime

# 2025-06-14: Fixed imports and task creation to use correct enums and types
from typing import Any, Dict, List, Optional
from uuid import uuid4

from services.domain.models import Intent, Task, Workflow
from services.orchestration.validation import ContextValidationError, workflow_validator
from services.shared_types import IntentCategory, TaskStatus, TaskType, WorkflowStatus, WorkflowType

logger = logging.getLogger(__name__)


class WorkflowFactory:
    """Factory for creating workflows from intents"""

    def __init__(self):
        self.workflow_registry = {}
        self._register_default_workflows()

        # PM-057: Validation registry for workflow requirements
        self.validation_registry = self._register_validation_requirements()

    def _register_default_workflows(self):
        """Register default workflow mappings"""
        self.workflow_registry = {
            # Existing mappings
            "create_github_issue": WorkflowType.CREATE_TICKET,
            "create_ticket": WorkflowType.CREATE_TICKET,
            "create_issue": WorkflowType.CREATE_TICKET,
            "generate_report": WorkflowType.GENERATE_REPORT,
            "review_issue": WorkflowType.REVIEW_ITEM,
            # PM-008: GitHub Issue Analysis mappings (only for actual GitHub URLs)
            "analyze_github_issue": WorkflowType.REVIEW_ITEM,
            "review_github_issue": WorkflowType.REVIEW_ITEM,
            "check_github_issue": WorkflowType.REVIEW_ITEM,
            # Analysis mappings - separate GitHub from general analysis
            "analyze_data": WorkflowType.ANALYZE_FILE,  # For file/data analysis
            "analyze_file": WorkflowType.ANALYZE_FILE,
            "performance_analysis": WorkflowType.GENERATE_REPORT,  # For performance analysis
            "user_feedback_analysis": WorkflowType.GENERATE_REPORT,  # For user feedback analysis
            "system_analysis": WorkflowType.GENERATE_REPORT,  # For system analysis
            # PM-021: Project listing workflow mapping
            "list_projects": WorkflowType.LIST_PROJECTS,
            "list_all_projects": WorkflowType.LIST_PROJECTS,
            "show_projects": WorkflowType.LIST_PROJECTS,
            # PM-062: Missing workflow type mappings identified in reality check
            "create_feature": WorkflowType.CREATE_FEATURE,
            "analyze_metrics": WorkflowType.ANALYZE_METRICS,
            "create_task": WorkflowType.CREATE_TASK,
            "plan_strategy": WorkflowType.PLAN_STRATEGY,
            "learn_pattern": WorkflowType.LEARN_PATTERN,
            "analyze_feedback": WorkflowType.ANALYZE_FEEDBACK,
            "confirm_project": WorkflowType.CONFIRM_PROJECT,
            "select_project": WorkflowType.SELECT_PROJECT,
        }

    def _register_validation_requirements(self) -> Dict[WorkflowType, Dict[str, Any]]:
        """
        PM-057: Register validation requirements for each workflow type.
        Complements the validation service with factory-level context requirements.
        """
        return {
            WorkflowType.CREATE_TICKET: {
                "context_requirements": {
                    "critical": ["original_message"],  # Always required
                    "important": ["project_id", "repository"],  # Needed for context
                    "optional": ["labels", "priority", "assignee"],  # Nice to have
                },
                "performance_threshold_ms": 50,  # Max validation time
                "pre_execution_checks": ["project_resolution", "repository_access"],
            },
            WorkflowType.LIST_PROJECTS: {
                "context_requirements": {
                    "critical": ["original_message"],
                    "important": [],
                    "optional": ["filter_criteria", "sort_order"],
                },
                "performance_threshold_ms": 30,
                "pre_execution_checks": ["database_access"],
            },
            WorkflowType.ANALYZE_FILE: {
                "context_requirements": {
                    "critical": ["original_message"],
                    "important": ["file_id", "resolved_file_id"],
                    "optional": ["analysis_type", "depth_level"],
                },
                "performance_threshold_ms": 75,
                "pre_execution_checks": ["file_existence", "file_accessibility"],
            },
            WorkflowType.GENERATE_REPORT: {
                "context_requirements": {
                    "critical": ["original_message"],
                    "important": ["data_source"],  # Could be file_id or project_id
                    "optional": ["report_format", "include_charts"],
                },
                "performance_threshold_ms": 60,
                "pre_execution_checks": ["data_source_validation"],
            },
            WorkflowType.REVIEW_ITEM: {
                "context_requirements": {
                    "critical": ["original_message"],
                    "important": ["github_url", "item_type"],
                    "optional": ["focus_areas", "review_depth"],
                },
                "performance_threshold_ms": 40,
                "pre_execution_checks": ["github_accessibility", "url_validation"],
            },
            WorkflowType.PLAN_STRATEGY: {
                "context_requirements": {
                    "critical": ["original_message"],
                    "important": ["scope", "objectives"],
                    "optional": ["timeline", "resources", "constraints"],
                },
                "performance_threshold_ms": 45,
                "pre_execution_checks": ["context_sufficiency"],
            },
        }

    def get_validation_requirements(self, workflow_type: WorkflowType) -> Optional[Dict[str, Any]]:
        """Get validation requirements for a specific workflow type"""
        return self.validation_registry.get(workflow_type)

    def get_performance_threshold(self, workflow_type: WorkflowType) -> int:
        """Get performance threshold for validation in milliseconds"""
        requirements = self.get_validation_requirements(workflow_type)
        return requirements.get("performance_threshold_ms", 100) if requirements else 100

    async def create_from_intent(
        self, intent: Intent, project_context: Optional[Dict[str, Any]] = None
    ) -> Optional[Workflow]:
        """
        Create workflow from intent with PM-057 context validation

        Validates context before workflow creation to prevent execution failures.
        Raises ContextValidationError with user-friendly messages on validation failure.
        """
        """Create workflow from intent with context mapping"""

        print(f"🔍 WorkflowFactory.create_from_intent called")
        print(f"🔍 Intent: action='{intent.action}', category={intent.category}")
        print(f"🔍 Intent context: {intent.context}")

        # Determine workflow type from intent action FIRST (Bug fix: PM-090)
        workflow_type = self.workflow_registry.get(intent.action.lower())
        print(f"🔍 Action '{intent.action.lower()}' mapped to workflow_type: {workflow_type}")

        # PM-057: Pre-execution context validation (Now workflow_type is defined)
        try:
            self._validate_workflow_context(workflow_type, intent, project_context)
            print(f"  ✅ Context validation passed")
        except ContextValidationError as e:
            print(f"  ❌ Context validation failed: {e.user_message}")
            raise e

        if not workflow_type:
            # Default mapping based on intent category
            if intent.category == IntentCategory.EXECUTION:
                workflow_type = WorkflowType.CREATE_TICKET
            elif intent.category == IntentCategory.ANALYSIS:
                # Check if it's GitHub-related analysis
                message = (intent.context or {}).get("original_message", "").lower()
                if "github.com" in message or "github issue" in message:
                    workflow_type = WorkflowType.REVIEW_ITEM  # For GitHub issues
                else:
                    workflow_type = WorkflowType.GENERATE_REPORT  # For general analysis
            elif intent.category == IntentCategory.SYNTHESIS:
                workflow_type = WorkflowType.GENERATE_REPORT
            elif intent.category == IntentCategory.STRATEGY:
                workflow_type = WorkflowType.PLAN_STRATEGY
            elif intent.category == IntentCategory.CONVERSATION:
                # Spatial integration: Conversational intents from Slack monitoring
                # Map to report generation for context-aware responses
                workflow_type = WorkflowType.GENERATE_REPORT
            elif intent.category == IntentCategory.LEARNING:
                # Spatial integration: Learning intents from Slack channel monitoring
                # Map to report generation for pattern analysis and insights
                workflow_type = WorkflowType.GENERATE_REPORT
            elif intent.category == IntentCategory.QUERY:
                # GREAT-4F: Smart fallback for likely mis-classified canonical intents
                text_lower = (intent.context or {}).get("original_message", intent.action).lower()

                # TEMPORAL patterns: calendar, schedule, time-related
                temporal_patterns = [
                    "calendar",
                    "schedule",
                    "meeting",
                    "appointment",
                    "today",
                    "tomorrow",
                    "yesterday",
                    "next week",
                    "this week",
                    "what time",
                    "when is",
                    "what day",
                    "what date",
                ]

                # STATUS patterns: work status, standup, current tasks
                status_patterns = [
                    "status",
                    "standup",
                    "working on",
                    "current",
                    "progress",
                    "what am i",
                    "what's my",
                    "my work",
                ]

                # PRIORITY patterns: importance, focus, priorities
                priority_patterns = [
                    "priority",
                    "priorities",
                    "important",
                    "focus",
                    "urgent",
                    "critical",
                    "top",
                    "most important",
                ]

                # Check for canonical patterns
                if any(pattern in text_lower for pattern in temporal_patterns):
                    # Likely mis-classified TEMPORAL
                    logger.warning(
                        f"QUERY intent likely mis-classified TEMPORAL: {text_lower[:50]}",
                        extra={"intent_id": intent.id, "category": "QUERY", "likely": "TEMPORAL"},
                    )
                    # Route to GENERATE_REPORT for temporal queries (canonical handlers handle this via intent service)
                    workflow_type = WorkflowType.GENERATE_REPORT

                elif any(pattern in text_lower for pattern in status_patterns):
                    # Likely mis-classified STATUS
                    logger.warning(
                        f"QUERY intent likely mis-classified STATUS: {text_lower[:50]}",
                        extra={"intent_id": intent.id, "category": "QUERY", "likely": "STATUS"},
                    )
                    workflow_type = WorkflowType.GENERATE_REPORT

                elif any(pattern in text_lower for pattern in priority_patterns):
                    # Likely mis-classified PRIORITY
                    logger.warning(
                        f"QUERY intent likely mis-classified PRIORITY: {text_lower[:50]}",
                        extra={"intent_id": intent.id, "category": "QUERY", "likely": "PRIORITY"},
                    )
                    workflow_type = WorkflowType.GENERATE_REPORT

                else:
                    # True generic query - use GENERATE_REPORT workflow
                    logger.info(
                        f"QUERY intent routed to GENERATE_REPORT: {text_lower[:50]}",
                        extra={"intent_id": intent.id, "category": "QUERY"},
                    )
                    workflow_type = WorkflowType.GENERATE_REPORT
            else:
                print(f"❌ No workflow type found for intent category: {intent.category}")
                return None
            print(f"🔍 Category {intent.category} mapped to workflow_type: {workflow_type}")

        # Merge intent context and project_context if provided
        context = dict(intent.context or {})
        if project_context:
            context.update(project_context)

        # Add intent category and action for message templating
        context["intent_category"] = intent.category.value
        context["intent_action"] = intent.action

        # Map resolved_file_id to file_id for workflow compatibility
        if "resolved_file_id" in context and "file_id" not in context:
            context["file_id"] = context["resolved_file_id"]

        print(f"🔍 Final context for workflow: {context}")

        # Create workflow with merged context
        workflow = Workflow(
            type=workflow_type,
            status=WorkflowStatus.PENDING,
            context=context,
            intent_id=intent.id,
        )

        # Add appropriate tasks based on workflow type
        if workflow_type == WorkflowType.CREATE_TICKET:
            # Three-step process: Extract work item → Generate enhanced content → Create GitHub issue
            extract_task = Task(
                name="Extract Work Item",
                type=TaskType.EXTRACT_WORK_ITEM,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(extract_task)

            # NEW: Generate professional GitHub issue content using LLM
            content_task = Task(
                name="Generate Issue Content",
                type=TaskType.GENERATE_GITHUB_ISSUE_CONTENT,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(content_task)

            create_task = Task(
                name="Create GitHub Issue",
                type=TaskType.GITHUB_CREATE_ISSUE,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(create_task)
        elif workflow_type == WorkflowType.REVIEW_ITEM:
            # PM-008: Add GitHub Issue Analysis task
            task = Task(
                name="Analyze GitHub Issue",
                type=TaskType.ANALYZE_GITHUB_ISSUE,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.ANALYZE_FILE:
            # Add File Analysis task
            task = Task(
                name="Analyze File",
                type=TaskType.ANALYZE_FILE,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.GENERATE_REPORT:
            # Determine appropriate task type based on context
            if "file_id" in context or context.get("resolved_file_id"):
                # File-based analysis
                task_type = TaskType.ANALYZE_FILE
                task_name = "Analyze File"
            else:
                # General analysis/summarization
                task_type = TaskType.SUMMARIZE
                task_name = "Generate Analysis"

            workflow.tasks.append(
                Task(
                    id=str(uuid4()),
                    name=task_name,
                    type=task_type,
                    status=TaskStatus.PENDING,
                    created_at=datetime.now(),
                )
            )
        elif workflow_type == WorkflowType.LIST_PROJECTS:
            # PM-021: Add project listing task
            task = Task(
                name="List Projects",
                type=TaskType.LIST_PROJECTS,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.CREATE_FEATURE:
            # Feature creation workflow
            task = Task(
                name="Create Feature",
                type=TaskType.CREATE_WORK_ITEM,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.ANALYZE_METRICS:
            # Metrics analysis workflow
            task = Task(
                name="Analyze Metrics",
                type=TaskType.ANALYZE_REQUEST,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.CREATE_TASK:
            # Task creation workflow
            task = Task(
                name="Create Task",
                type=TaskType.CREATE_WORK_ITEM,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.PLAN_STRATEGY:
            # Strategy planning workflow
            task = Task(
                name="Plan Strategy",
                type=TaskType.SUMMARIZE,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.LEARN_PATTERN:
            # Pattern learning workflow
            task = Task(
                name="Learn Pattern",
                type=TaskType.ANALYZE_REQUEST,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.ANALYZE_FEEDBACK:
            # Feedback analysis workflow
            task = Task(
                name="Analyze Feedback",
                type=TaskType.ANALYZE_REQUEST,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.CONFIRM_PROJECT:
            # Project confirmation workflow
            task = Task(
                name="Confirm Project",
                type=TaskType.ANALYZE_REQUEST,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        elif workflow_type == WorkflowType.SELECT_PROJECT:
            # Project selection workflow
            task = Task(
                name="Select Project",
                type=TaskType.ANALYZE_REQUEST,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)
        else:
            # Default fallback for any unhandled workflow types
            task = Task(
                name=f"Handle {workflow_type.value}",
                type=TaskType.ANALYZE_REQUEST,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(task)

        return workflow

    def _validate_workflow_context(
        self,
        workflow_type: WorkflowType,
        intent: Intent,
        project_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        PM-057: Validate workflow context before execution

        Performs pre-execution validation to prevent workflow failures.
        Raises ContextValidationError with user-friendly messages.
        """
        if not workflow_type:
            return  # Skip validation if no workflow type determined

        # Get validation requirements for this workflow type
        requirements = self.get_validation_requirements(workflow_type)
        if not requirements:
            return  # No validation requirements defined

        # Merge context
        context = dict(intent.context or {})
        if project_context:
            context.update(project_context)

        # Validate critical fields
        critical_fields = requirements.get("context_requirements", {}).get("critical", [])
        missing_critical = []

        for field in critical_fields:
            if not self._field_exists_and_valid(context, field):
                missing_critical.append(field)

        # Validate important fields (warn but don't fail)
        important_fields = requirements.get("context_requirements", {}).get("important", [])
        missing_important = []

        for field in important_fields:
            if not self._field_exists_and_valid(context, field):
                missing_important.append(field)

        # Create suggestions for missing fields
        suggestions = self._generate_field_suggestions(
            workflow_type, missing_critical + missing_important
        )

        # Raise error if critical fields are missing
        if missing_critical:
            raise ContextValidationError(
                workflow_type=workflow_type,
                missing_fields=missing_critical,
                suggestions=suggestions,
                details={
                    "missing_important": missing_important,
                    "available_context": list(context.keys()),
                    "intent_action": intent.action,
                    "intent_category": intent.category.value,
                },
            )

        # Log warnings for missing important fields
        if missing_important:
            print(f"  ⚠️  Missing important fields for {workflow_type.value}: {missing_important}")

    def _field_exists_and_valid(self, context: Dict[str, Any], field: str) -> bool:
        """Check if a field exists and has a valid value"""
        if field not in context:
            return False

        value = context[field]

        # Check for empty values
        if value is None:
            return False

        if isinstance(value, str) and not value.strip():
            return False

        if isinstance(value, (list, dict)) and not value:
            return False

        return True

    def _generate_field_suggestions(
        self, workflow_type: WorkflowType, missing_fields: List[str]
    ) -> List[str]:
        """Generate helpful suggestions for missing fields"""
        suggestions = []

        for field in missing_fields:
            if field == "original_message":
                suggestions.append("Please provide more details about what you want me to do.")
            elif field == "project_id":
                suggestions.append("Please specify which project you're working with.")
            elif field == "file_id":
                suggestions.append("Please specify which file you want me to analyze.")
            elif field == "repository":
                suggestions.append("Please provide the repository name or URL.")
            elif field == "github_url":
                suggestions.append("Please provide a GitHub issue or pull request URL.")
            else:
                suggestions.append(f"Please provide the {field} information.")

        return suggestions

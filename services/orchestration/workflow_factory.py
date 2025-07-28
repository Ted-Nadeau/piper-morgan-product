"""
Workflow Factory - Creates workflows from intents
PM-002 Implementation
PM-008 Github integration
PM-057 Context Validation Framework
"""

from datetime import datetime

# 2025-06-14: Fixed imports and task creation to use correct enums and types
from typing import Any, Dict, Optional
from uuid import uuid4

from services.domain.models import Intent, Task, Workflow
from services.orchestration.validation import workflow_validator
from services.shared_types import IntentCategory, TaskStatus, TaskType, WorkflowStatus, WorkflowType


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
        """Create workflow from intent with context mapping"""

        print(f"🔍 WorkflowFactory.create_from_intent called")
        print(f"🔍 Intent: action='{intent.action}', category={intent.category}")
        print(f"🔍 Intent context: {intent.context}")

        # Determine workflow type from intent action
        workflow_type = self.workflow_registry.get(intent.action.lower())
        print(f"🔍 Action '{intent.action.lower()}' mapped to workflow_type: {workflow_type}")

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

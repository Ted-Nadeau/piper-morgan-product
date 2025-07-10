"""
Workflow Factory - Creates workflows from intents
PM-002 Implementation
PM-008 Github integration
"""

from datetime import datetime
# 2025-06-14: Fixed imports and task creation to use correct enums and types
from typing import Any, Dict, Optional
from uuid import uuid4

from services.domain.models import Intent, Task, Workflow
from services.shared_types import (IntentCategory, TaskStatus, TaskType,
                                   WorkflowStatus, WorkflowType)


class WorkflowFactory:
    """Factory for creating workflows from intents"""

    def __init__(self):
        self.workflow_registry = {}
        self._register_default_workflows()

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
        }

    async def create_from_intent(
        self, intent: Intent, project_context: Optional[Dict[str, Any]] = None
    ) -> Optional[Workflow]:
        """Create workflow from intent with context mapping"""

        print(f"🔍 WorkflowFactory.create_from_intent called")
        print(f"🔍 Intent: action='{intent.action}', category={intent.category}")
        print(f"🔍 Intent context: {intent.context}")

        # Determine workflow type from intent action
        workflow_type = self.workflow_registry.get(intent.action.lower())
        print(
            f"🔍 Action '{intent.action.lower()}' mapped to workflow_type: {workflow_type}"
        )

        if not workflow_type:
            # Default mapping based on intent category
            if intent.category == IntentCategory.EXECUTION:
                workflow_type = WorkflowType.CREATE_TICKET
            elif intent.category == IntentCategory.ANALYSIS:
                # Check if it's GitHub-related analysis
                message = intent.context.get("original_message", "").lower()
                if "github.com" in message or "github issue" in message:
                    workflow_type = WorkflowType.REVIEW_ITEM  # For GitHub issues
                else:
                    workflow_type = WorkflowType.GENERATE_REPORT  # For general analysis
            elif intent.category == IntentCategory.SYNTHESIS:
                workflow_type = WorkflowType.GENERATE_REPORT
            elif intent.category == IntentCategory.STRATEGY:
                workflow_type = WorkflowType.PLAN_STRATEGY
            else:
                print(
                    f"❌ No workflow type found for intent category: {intent.category}"
                )
                return None
            print(
                f"🔍 Category {intent.category} mapped to workflow_type: {workflow_type}"
            )

        # Merge intent context and project_context if provided
        context = dict(intent.context)
        if project_context:
            context.update(project_context)

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
            # Extract work item first, then create GitHub issue
            extract_task = Task(
                name="Extract Work Item",
                type=TaskType.EXTRACT_WORK_ITEM,
                status=TaskStatus.PENDING,
            )
            workflow.tasks.append(extract_task)

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

        return workflow

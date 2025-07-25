"""
Orchestration Engine
Coordinates multi-step workflows for PM tasks
PM-008 Github integration
"""

# 2025-06-14: Fixed to use domain-first design - domain models instead of orchestration-specific classes
import asyncio
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from services.analysis.file_type_detector import FileTypeDetector
from services.api.errors import TaskFailedError, WorkflowTimeoutError
from services.database.repositories import TaskRepository, WorkflowRepository
from services.database.session_factory import AsyncSessionFactory

# Domain-first imports - use domain models consistently
from services.domain.models import Intent, IntentCategory, Task, Workflow
from services.integrations.github.config_service import GitHubConfigService
from services.integrations.github.content_generator import GitHubIssueContentGenerator
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.issue_analyzer import GitHubIssueAnalyzer
from services.integrations.github.production_client import (
    GitHubClientConfig,
    ProductionGitHubClient,
)
from services.llm.clients import llm_client
from services.orchestration.validation import ContextValidationError, workflow_validator
from services.shared_types import TaskStatus, TaskType, WorkflowStatus, WorkflowType

logger = structlog.get_logger()


@dataclass
class TaskResult:
    """Result from executing a task - simple dataclass for task handlers"""

    success: bool
    output_data: Dict[str, Any] = None
    error: Optional[str] = None


class OrchestrationEngine:
    def __init__(self, test_mode=False):
        self.workflows = {}
        self.test_mode = test_mode  # PM-062: Enable in-memory testing without database
        from .workflow_factory import WorkflowFactory

        self.factory = WorkflowFactory()
        self.github_analyzer = GitHubIssueAnalyzer()

        # Initialize GitHub clients with ADR-010 configuration patterns
        self.github_config_service = GitHubConfigService()

        try:
            # Use production client with ConfigService if feature is enabled
            if self.github_config_service.is_feature_enabled("production_client"):
                self.github_client = ProductionGitHubClient(
                    config_service=self.github_config_service
                )
                logger.info("✅ Using ProductionGitHubClient for GitHub operations")
            else:
                logger.info("📎 Production client disabled, using GitHubAgent")
                self.github_client = GitHubAgent(
                    token=self.github_config_service.get_authentication_token()
                )
        except Exception as e:
            # Fall back to original agent for backward compatibility
            logger.warning(f"ProductionGitHubClient unavailable: {e}")
            logger.info("📎 Falling back to GitHubAgent")
            try:
                self.github_client = GitHubAgent(
                    token=self.github_config_service.get_authentication_token()
                )
            except Exception as fallback_error:
                logger.error(f"Both GitHub clients failed: {fallback_error}")
                self.github_client = GitHubAgent()  # Final fallback without token

        self.github_content_generator = GitHubIssueContentGenerator(llm_client)
        self.llm_client = llm_client

        self.task_handlers = {
            TaskType.ANALYZE_REQUEST: self._analyze_request,
            TaskType.EXTRACT_REQUIREMENTS: self._extract_requirements,
            TaskType.IDENTIFY_DEPENDENCIES: self._identify_dependencies,
            TaskType.CREATE_WORK_ITEM: self._create_work_item,
            TaskType.UPDATE_WORK_ITEM: self._update_work_item,
            TaskType.NOTIFY_STAKEHOLDERS: self._notify_stakeholders,
            # PM-008: GitHub Issue Analysis handler
            TaskType.ANALYZE_GITHUB_ISSUE: self._analyze_github_issue,
            # File Analysis handler
            TaskType.ANALYZE_FILE: self._analyze_file,
            # Summarization handler
            TaskType.SUMMARIZE: self._summarize,
            # Work Item Extraction handler
            TaskType.EXTRACT_WORK_ITEM: self._extract_work_item,
            # GitHub integration handlers
            TaskType.GITHUB_CREATE_ISSUE: self._create_github_issue,
            TaskType.GENERATE_GITHUB_ISSUE_CONTENT: self._generate_github_issue_content,
            # PM-021: Project listing handler
            TaskType.LIST_PROJECTS: self._list_projects,
            # PM-062: Missing task handlers implementation
            TaskType.GENERATE_DOCUMENT: self._generate_document,
            TaskType.CREATE_SUMMARY: self._create_summary,
            TaskType.PROCESS_USER_FEEDBACK: self._process_user_feedback,
            # Integration handlers (placeholder for now)
            TaskType.JIRA_CREATE_TICKET: self._placeholder_handler,
            TaskType.SLACK_SEND_MESSAGE: self._placeholder_handler,
        }

    async def create_workflow_from_intent(self, intent: Intent) -> Optional[Workflow]:
        """Create appropriate workflow based on intent with database persistence"""
        workflow = await self.factory.create_from_intent(intent)

        # PM-057: Validate workflow context before execution
        if workflow:
            try:
                workflow_validator.validate_workflow_context(workflow.type, workflow.context)
                logger.info(f"✅ Workflow context validation passed for {workflow.type}")
            except ContextValidationError as e:
                logger.warning(f"❌ Workflow context validation failed: {e.user_message}")
                # Store validation error in workflow context for user feedback
                workflow.context["validation_error"] = {
                    "user_message": e.user_message,
                    "missing_fields": e.details.get("missing_fields", []),
                    "suggestions": e.details.get("suggestions", []),
                }
                # Don't fail the workflow creation - let it proceed with validation info

        # Enrich CREATE_TICKET workflows with repository from project (skip in test mode)
        if workflow and workflow.type == WorkflowType.CREATE_TICKET and not self.test_mode:
            project_id = intent.context.get("project_id")
            if project_id:
                try:
                    async with AsyncSessionFactory.session_scope() as session:
                        from services.database.repositories import ProjectRepository

                        project_repo = ProjectRepository(session)
                        project = await project_repo.get_by_id(project_id)
                        if project:
                            repository = project.get_github_repository()
                            if repository:
                                workflow.context["repository"] = repository
                                logger.info(
                                    f"Enriched CREATE_TICKET workflow with repository: {repository}"
                                )
                            else:
                                logger.warning(
                                    f"Project {project_id} has no GitHub repository configured"
                                )
                        else:
                            logger.warning(f"Project {project_id} not found")
                except Exception as e:
                    logger.error(f"Failed to enrich workflow with repository: {str(e)}")
                    # Continue without repository - handler will provide appropriate error
            else:
                # No project context - use default repository
                default_repo = os.getenv("GITHUB_DEFAULT_REPO")
                logger.info(f"🔍 No project context, checking GITHUB_DEFAULT_REPO: {default_repo}")
                if default_repo:
                    workflow.context["repository"] = default_repo
                    logger.info(
                        f"✅ Using default repository for CREATE_TICKET workflow: {default_repo}"
                    )
                else:
                    logger.warning("❌ No project context and no GITHUB_DEFAULT_REPO configured")
        if workflow:
            # Store in memory for execution
            self.workflows[workflow.id] = workflow

            # Persist to database using repository pattern (skip in test mode)
            if not self.test_mode:
                try:
                    await self._persist_workflow_to_database(workflow)
                except Exception as e:
                    logger.warning(
                        f"Database persistence failed, continuing with in-memory execution: {e}"
                    )
            else:
                logger.info(f"Test mode: Skipping database persistence for workflow {workflow.id}")
        return workflow

    async def _persist_workflow_to_database(self, workflow: Workflow):
        """Persist domain workflow to database using repository pattern"""
        async with AsyncSessionFactory.session_scope() as session:
            async with session.begin():
                workflow_repo = WorkflowRepository(session)
                task_repo = TaskRepository(session)

                # Create database workflow from domain workflow
                db_workflow = await workflow_repo.create_from_domain(workflow)

                # Create database tasks for each domain task
                for task in workflow.tasks:
                    await task_repo.create_from_domain(db_workflow.id, task)

                # All operations within single transaction - automatic commit
                logger.info("Workflow persisted to database", workflow_id=workflow.id)

    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Execute a workflow asynchronously using domain objects
        """
        print(f"🔍 execute_workflow called for workflow ID: {workflow_id}")
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            # In a real system, you might load it from the DB here
            raise ValueError(f"Workflow {workflow_id} not found")

        print(f"🔍 Workflow type: {workflow.type}")
        print(f"🔍 Workflow context: {workflow.context}")
        print(f"🔍 Found {len(workflow.tasks)} tasks to execute")
        workflow.status = WorkflowStatus.RUNNING

        # Update status in database and execute tasks
        try:
            # Skip database updates in test mode
            if not self.test_mode:
                try:
                    async with AsyncSessionFactory.session_scope() as session:
                        workflow_repo = WorkflowRepository(session)
                        await workflow_repo.update_status(workflow_id, WorkflowStatus.RUNNING)
                except Exception as e:
                    logger.warning(
                        f"Database status update failed, continuing with in-memory execution: {e}"
                    )

            # Execute tasks with a timeout
            try:
                # Execute tasks with timeout (Python 3.9 compatible)
                async def execute_all_tasks():
                    while task := workflow.get_next_task():
                        print(f"🔍 Executing task: {task.type}")
                        print(f"🔍 Task handler: {self.task_handlers.get(task.type)}")
                        await self._execute_task(workflow, task)
                        # Persist task results after each execution (skip in test mode)
                        if not self.test_mode:
                            try:
                                await self._persist_task_update(workflow_id, task)
                            except Exception as e:
                                logger.warning(f"Task persistence failed, continuing: {e}")
                        if workflow.status == WorkflowStatus.FAILED:
                            break

                await asyncio.wait_for(execute_all_tasks(), timeout=300)  # 5-minute timeout
            except TimeoutError:
                logger.error("Workflow timed out", workflow_id=workflow_id)
                raise WorkflowTimeoutError(details={"workflow_id": workflow_id})

            if workflow.is_complete():
                workflow.status = WorkflowStatus.COMPLETED

                # Aggregate task results into workflow result for CREATE_TICKET workflows
                if workflow.type == WorkflowType.CREATE_TICKET:
                    # Find the GitHub issue creation task result
                    for task in workflow.tasks:
                        if task.type == TaskType.GITHUB_CREATE_ISSUE and task.result:
                            from services.domain.models import WorkflowResult

                            workflow.result = WorkflowResult(
                                success=True,
                                data={
                                    "issue_url": task.result.get("issue_url"),
                                    "issue_number": task.result.get("issue_number"),
                                },
                            )
                            break

                # Update final workflow status (skip in test mode)
                if not self.test_mode:
                    try:
                        async with AsyncSessionFactory.session_scope() as session:
                            workflow_repo = WorkflowRepository(session)
                            await workflow_repo.update_status(
                                workflow_id,
                                WorkflowStatus.COMPLETED,
                                output_data={
                                    "success": True,
                                    "data": workflow.context,
                                    "error": None,
                                },
                            )
                    except Exception as e:
                        logger.warning(f"Final status update failed, continuing: {e}")

                logger.info("Workflow completed", workflow_id=workflow_id)

        except (TaskFailedError, WorkflowTimeoutError) as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.error = e.error_code

            # Update failure status (skip in test mode)
            if not self.test_mode:
                try:
                    async with AsyncSessionFactory.session_scope() as session:
                        workflow_repo = WorkflowRepository(session)
                        await workflow_repo.update_status(
                            workflow_id,
                            WorkflowStatus.FAILED,
                            error=e.error_code,
                            output_data=e.details,
                        )
                except Exception as db_e:
                    logger.warning(f"Failure status update failed, continuing: {db_e}")

            logger.error(
                "Workflow failed with controlled error",
                workflow_id=workflow_id,
                error_code=e.error_code,
            )
            raise  # Re-raise for the middleware to catch
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.error = str(e)

            # Update failure status (skip in test mode)
            if not self.test_mode:
                try:
                    async with AsyncSessionFactory.session_scope() as session:
                        workflow_repo = WorkflowRepository(session)
                        await workflow_repo.update_status(
                            workflow_id, WorkflowStatus.FAILED, error=str(e)
                        )
                except Exception as db_e:
                    logger.warning(f"Exception status update failed, continuing: {db_e}")

            logger.error(
                "Workflow failed with unexpected error",
                workflow_id=workflow_id,
                error=str(e),
                exc_info=True,
            )
            # Wrap unexpected errors in a standard TaskFailedError
            raise TaskFailedError(
                task_description="workflow execution",
                recovery_suggestion="check logs for details",
                details={"original_error": str(e)},
            ) from e

        return workflow.to_dict()

    async def _persist_task_update(self, workflow_id: str, task: Task):
        """Persist task updates to database using repository pattern"""
        async with AsyncSessionFactory.session_scope() as session:
            task_repo = TaskRepository(session)

            # Update database task from domain task
            await task_repo.update(
                task.id, status=task.status, output_data=task.result, error=task.error
            )
            # Automatic commit/rollback and session cleanup via context manager

    async def _execute_task(self, workflow: Workflow, task: Task):
        """Execute a single task using domain objects"""

        # PM-057: Check for validation errors and provide user feedback
        validation_error = workflow.context.get("validation_error")
        if validation_error:
            task.status = TaskStatus.FAILED
            task.error = validation_error["user_message"]
            workflow.status = WorkflowStatus.FAILED
            logger.warning(
                "Task failed due to context validation error",
                workflow_id=workflow.id,
                task_id=task.id,
                validation_error=validation_error,
            )
            raise TaskFailedError(
                task_description=task.type.value,
                recovery_suggestion=validation_error["user_message"],
                details={
                    "task_id": task.id,
                    "validation_error": validation_error,
                    "reason": "context_validation_failed",
                },
            )

        task.status = TaskStatus.RUNNING

        try:
            handler = self.task_handlers.get(task.type)
            if not handler:
                raise ValueError(f"No handler for task type {task.type}")

            # Execute task with a timeout
            result = await asyncio.wait_for(
                handler(workflow, task), timeout=120  # 2-minute timeout per task
            )

            # Update domain task with results
            if result.success:
                task.status = TaskStatus.COMPLETED
                task.result = result.output_data

                # Update workflow context
                if result.output_data:
                    workflow.context.update(result.output_data)
            else:
                task.status = TaskStatus.FAILED
                task.error = result.error or "Task execution failed"
                workflow.status = WorkflowStatus.FAILED
                # Raise a specific error instead of just setting status
                raise TaskFailedError(
                    task_description=task.type.value,
                    recovery_suggestion="review the task details and logs",
                    details={"task_id": task.id, "error": task.error},
                )

            logger.info(
                "Task completed",
                workflow_id=workflow.id,
                task_id=task.id,
                task_type=task.type.value if task.type else "unknown",
                success=result.success,
            )

        except TimeoutError as e:
            task.status = TaskStatus.FAILED
            task.error = "Task timed out after 120 seconds"
            workflow.status = WorkflowStatus.FAILED
            logger.error(
                "Task timed out",
                workflow_id=workflow.id,
                task_id=task.id,
                task_type=task.type.value,
            )
            raise TaskFailedError(
                task_description=task.type.value,
                recovery_suggestion="the system may be under heavy load, please try again later",
                details={"task_id": task.id, "reason": "timeout"},
            ) from e
        except TaskFailedError:
            # Re-raise TaskFailedError without re-wrapping
            raise
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            workflow.status = WorkflowStatus.FAILED
            logger.error(
                "Task failed with unexpected error",
                workflow_id=workflow.id,
                task_id=task.id,
                error=str(e),
                exc_info=True,
            )
            # Wrap the unexpected error
            raise TaskFailedError(
                task_description=task.type.value,
                recovery_suggestion="an unexpected error occurred, check system logs",
                details={"task_id": task.id, "original_error": str(e)},
            ) from e

    # Task handler implementations
    async def _analyze_request(self, workflow: Workflow, task: Task) -> TaskResult:
        """Analyze the original request using LLM"""
        original_message = workflow.context.get("original_message", "")

        prompt = f"""Analyze this product management request and extract key information:

Request: {original_message}

Extract:
1. Main objective
2. Success criteria
3. Potential risks
4. Required resources

Format as JSON."""

        response = await self.llm_client.complete(task_type="analysis", prompt=prompt)

        return TaskResult(success=True, output_data={"analysis": response})

    async def _extract_requirements(self, workflow: Workflow, task: Task) -> TaskResult:
        """Extract detailed requirements"""
        analysis = workflow.context.get("analysis", "")

        prompt = f"""Based on this analysis, extract specific requirements:

Analysis: {analysis}

List concrete requirements, acceptance criteria, and technical specifications."""

        response = await self.llm_client.complete(task_type="analysis", prompt=prompt)

        return TaskResult(success=True, output_data={"requirements": response})

    async def _identify_dependencies(self, workflow: Workflow, task: Task) -> TaskResult:
        """Identify dependencies and blockers"""
        # Placeholder - would analyze existing features, teams, etc
        return TaskResult(success=True, output_data={"dependencies": []})

    async def _create_work_item(self, workflow: Workflow, task: Task) -> TaskResult:
        """Create internal work item representation"""
        # Create work item in database (or simulate in test mode)
        try:
            if self.test_mode:
                # Simulate work item creation for testing
                import uuid

                mock_work_item_id = str(uuid.uuid4())
                title = workflow.context.get("original_message", "")[:100]
                logger.info(f"Test mode: Simulated work item creation - {title}")
                return TaskResult(
                    success=True,
                    output_data={"work_item_id": mock_work_item_id, "title": title},
                )
            else:
                async with AsyncSessionFactory.session_scope() as session:
                    from services.database.repositories import WorkItemRepository

                    work_item_repo = WorkItemRepository(session)
                    work_item = await work_item_repo.create(
                        title=workflow.context.get("original_message", "")[:100],
                        description=workflow.context.get("requirements", ""),
                        status="open",
                        external_refs={},
                    )

                    return TaskResult(
                        success=True,
                        output_data={"work_item_id": work_item.id, "title": work_item.title},
                    )
        except Exception as e:
            logger.error(f"Failed to create work item: {str(e)}")
            return TaskResult(success=False, error=f"Work item creation failed: {str(e)}")

    async def _notify_stakeholders(self, workflow: Workflow, task: Task) -> TaskResult:
        """Notify relevant stakeholders"""
        # Placeholder - would send actual notifications
        logger.info("Would notify stakeholders", workflow_id=workflow.id)
        return TaskResult(success=True, output_data={"notified": True})

    async def _analyze_github_issue(self, workflow: Workflow, task: Task) -> TaskResult:
        """
        PM-008: Analyze GitHub issue using GitHubIssueAnalyzer

        Expects workflow context to contain either:
        - 'github_url': Direct GitHub issue URL
        - 'original_message': Message containing GitHub URL
        """
        try:
            # Extract GitHub URL from workflow context
            github_url = workflow.context.get("github_url")

            if not github_url:
                # Try to extract URL from original message
                original_message = workflow.context.get("original_message", "")
                github_url = self._extract_github_url_from_message(original_message)

            if not github_url:
                return TaskResult(
                    success=False,
                    error="No GitHub URL found in request. Please provide a GitHub issue URL.",
                )

            # Perform issue analysis using PM-008
            logger.info(f"Analyzing GitHub issue: {github_url}")
            analysis_result = await self.github_analyzer.analyze_issue_by_url(github_url)

            if not analysis_result["success"]:
                return TaskResult(
                    success=False,
                    error=f"Issue analysis failed: {analysis_result['error']}",
                )

            # Extract analysis data
            analysis = analysis_result["analysis"]
            issue_info = analysis_result["issue"]

            # Format results for user
            formatted_response = self._format_issue_analysis_response(analysis, issue_info)

            return TaskResult(
                success=True,
                output_data={
                    "analysis_complete": True,
                    "github_url": github_url,
                    "issue_number": issue_info["number"],
                    "issue_title": issue_info["title"],
                    "repository": issue_info["repository"],
                    "analysis_summary": analysis.summary,
                    "draft_comment": analysis.draft_comment,
                    "draft_rewrite": analysis.draft_rewrite,
                    "confidence": analysis.confidence,
                    "formatted_response": formatted_response,
                    "raw_analysis": analysis_result,
                },
            )

        except Exception as e:
            logger.error(f"GitHub issue analysis failed: {e}")
            return TaskResult(success=False, error=f"Analysis error: {str(e)}")

    def _extract_github_url_from_message(self, message: str) -> Optional[str]:
        """Extract GitHub URL from natural language message"""
        import re

        # Look for GitHub URLs in the message
        github_url_pattern = r"https?://github\.com/[^/]+/[^/]+/(?:issues|pull)/\d+"
        matches = re.findall(github_url_pattern, message)

        if matches:
            return matches[0]  # Return first match

        return None

    def _format_issue_analysis_response(self, analysis, issue_info) -> str:
        """Format analysis results for user presentation"""

        response_parts = [
            f"📋 **Issue Analysis Complete**",
            f"**Issue**: #{issue_info['number']} - {issue_info['title']}",
            f"**Repository**: {issue_info['repository']}",
            f"**Confidence**: {analysis.confidence:.1f}/1.0",
            "",
            "**📝 Analysis Summary:**",
        ]

        # Add summary bullets
        for i, bullet in enumerate(analysis.summary, 1):
            response_parts.append(f"{i}. {bullet}")

        response_parts.extend(
            [
                "",
                "**💬 Suggested Comment:**",
                f"```{analysis.draft_comment[:200]}{'...' if len(analysis.draft_comment) > 200 else ''}```",
                "",
                "**📄 Suggested Rewrite:**",
                f"```{analysis.draft_rewrite[:200]}{'...' if len(analysis.draft_rewrite) > 200 else ''}```",
            ]
        )

        if analysis.knowledge_context:
            response_parts.extend(
                [
                    "",
                    "**🧠 Used Knowledge:**",
                    f"- {len(analysis.knowledge_context)} relevant PM practices found",
                ]
            )

        return "\n".join(response_parts)

    async def _analyze_file(self, workflow: Workflow, task: Task) -> TaskResult:
        """Execute file analysis task using FileAnalyzer"""
        try:
            # Extract file ID from context
            file_id = (
                workflow.context.get("file_id")
                or workflow.context.get("resolved_file_id")
                or workflow.context.get("probable_file_id")
            )
            if not file_id:
                return TaskResult(success=False, error="No file ID found in workflow context")
            # Convert file_id to string (database expects string type)
            file_id = str(file_id)

            # Get file repository using AsyncSessionFactory
            async with AsyncSessionFactory.session_scope() as session:
                from services.repositories.file_repository import FileRepository

                file_repo = FileRepository(session)
                file_metadata = await file_repo.get_file_by_id(file_id)
                if not file_metadata:
                    return TaskResult(success=False, error=f"File not found: {file_id}")

                # Create FileAnalyzer with dependencies
                from unittest.mock import Mock

                from services.analysis.analyzer_factory import AnalyzerFactory
                from services.analysis.file_analyzer import FileAnalyzer

                mock_security = Mock()
                mock_security.validate.return_value = Mock(is_valid=True)

                type_detector = FileTypeDetector()

                mock_sampler = Mock()

                analyzer_factory = AnalyzerFactory(llm_client=self.llm_client)
                file_analyzer = FileAnalyzer(
                    security_validator=mock_security,
                    type_detector=type_detector,
                    content_sampler=mock_sampler,
                    analyzer_factory=analyzer_factory,
                    llm_client=self.llm_client,
                )

                # Perform analysis
                logger.info(
                    f"DEBUG: Analyzing file {file_metadata.filename} at path {file_metadata.storage_path}"
                )

                # Debug: Read first 500 chars of file to verify content
                try:
                    with open(file_metadata.storage_path, "r") as f:
                        file_content_preview = f.read(500)
                        logger.info(f"DEBUG: File content preview: {file_content_preview}")
                except Exception as e:
                    logger.error(f"DEBUG: Could not read file content: {e}")

                analysis_result = await file_analyzer.analyze_file(
                    str(file_metadata.storage_path), {"filename": file_metadata.filename}
                )

                # Convert AnalysisResult to dict
                analysis_dict = analysis_result.__dict__.copy()
                analysis_dict["generated_at"] = analysis_result.generated_at.isoformat()
                analysis_dict["analysis_type"] = analysis_result.analysis_type.value

                return TaskResult(
                    success=True,
                    output_data={
                        "analysis": analysis_dict,
                        "file_id": file_id,
                        "filename": file_metadata.filename,
                    },
                )

        except Exception as e:
            logger.error(f"File analysis failed: {e}")
            return TaskResult(success=False, error=f"Analysis error: {str(e)}")

    async def _create_github_issue(self, workflow: Workflow, task: Task) -> TaskResult:
        """Create a GitHub issue from workflow context."""
        try:
            logger.info(f"🔍 _create_github_issue called with workflow ID: {workflow.id}")
            logger.info(f"🔍 Workflow context: {workflow.context}")

            # Get repository from context
            repository = workflow.context.get("repository")

            # If not directly specified, try to extract from project integrations
            if not repository and "integrations" in workflow.context:
                for integration in workflow.context["integrations"]:
                    if integration.get("type") == "github" and "config" in integration:
                        repository = integration["config"].get("repository")
                        if repository:
                            break

            if not repository:
                logger.error("❌ Repository not specified in workflow context")
                return TaskResult(
                    success=False, error="Repository not specified in workflow context"
                )

            # Look for work item from previous extraction task
            work_item = None

            # First, check for enhanced content from the new content generation task
            enhanced_content = None
            work_item = None

            for completed_task in workflow.tasks:
                # Check for enhanced content first (highest priority)
                if (
                    completed_task.type == TaskType.GENERATE_GITHUB_ISSUE_CONTENT
                    and completed_task.status == TaskStatus.COMPLETED
                    and completed_task.result
                ):
                    enhanced_content = completed_task.result.get("enhanced_content")
                    logger.info(
                        f"🎯 Using enhanced content: {enhanced_content.get('title') if enhanced_content else 'None'}"
                    )
                    break
                # Fallback to work item from extraction task
                elif (
                    completed_task.type == TaskType.EXTRACT_WORK_ITEM
                    and completed_task.status == TaskStatus.COMPLETED
                    and completed_task.result
                ):
                    work_item = completed_task.result.get("work_item")

            if enhanced_content:
                # Use the LLM-generated enhanced content (preferred method)
                logger.info(
                    f"✨ Creating issue with enhanced content: '{enhanced_content.get('title')}'"
                )

                # Use the unified GitHub client interface
                if hasattr(self.github_client, "create_issue") and asyncio.iscoroutinefunction(
                    self.github_client.create_issue
                ):
                    # Production client (async)
                    issue_data = await self.github_client.create_issue(
                        repo_name=repository,
                        title=enhanced_content.get("title", "New Issue"),
                        body=enhanced_content.get("body", ""),
                        labels=enhanced_content.get("labels", []),
                    )
                else:
                    # Legacy agent (sync, wrapped in async)
                    issue_data = await self.github_client.create_issue(
                        repo_name=repository,
                        title=enhanced_content.get("title", "New Issue"),
                        body=enhanced_content.get("body", ""),
                        labels=enhanced_content.get("labels", []),
                    )
            elif work_item:
                # Use the extracted work item (fallback)
                logger.info(f"🔍 Using extracted work item: {work_item.get('title')}")

                # Check if we have the legacy agent with create_issue_from_work_item method
                if hasattr(self.github_client, "create_issue_from_work_item"):
                    issue_data = await self.github_client.create_issue_from_work_item(
                        repo_name=repository, work_item=work_item
                    )
                else:
                    # Convert work item to standard create_issue parameters
                    issue_data = await self.github_client.create_issue(
                        repo_name=repository,
                        title=work_item.get("title", "New Issue"),
                        body=work_item.get("description", ""),
                        labels=work_item.get("labels", []),
                    )
            else:
                # Final fallback to old method for backward compatibility
                logger.info("🔍 No enhanced content or work item found, using fallback method")
                title = workflow.context.get("title", "New Issue")
                body = workflow.context.get("body", "")
                labels = workflow.context.get("labels", [])

                issue_data = await self.github_client.create_issue(
                    repo_name=repository, title=title, body=body, labels=labels
                )

            return TaskResult(
                success=True,
                output_data={
                    "issue_number": issue_data.get("number"),
                    "issue_url": issue_data.get("url"),
                    "issue_data": issue_data,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create GitHub issue: {str(e)}")
            return TaskResult(success=False, error=f"GitHub API error: {str(e)}")

    async def _generate_github_issue_content(self, workflow: Workflow, task: Task) -> TaskResult:
        """Generate professional GitHub issue content from natural language using LLM"""
        try:
            logger.info(f"🎯 Generating GitHub issue content for workflow ID: {workflow.id}")

            # Get the original message from workflow context
            original_message = workflow.context.get("original_message", "")
            if not original_message:
                return TaskResult(
                    success=False, error="No original message found in workflow context"
                )

            # Get project context if available
            project_context = None
            project_id = workflow.context.get("project_id")
            if project_id:
                try:
                    async with AsyncSessionFactory.session_scope() as session:
                        from services.database.repositories import ProjectRepository

                        project_repo = ProjectRepository(session)
                        project = await project_repo.get_by_id(project_id)
                        if project:
                            from services.domain.models import ProjectContext

                            project_context = ProjectContext(
                                name=project.name,
                                description=project.description,
                                technologies=[],  # TODO: Add technologies field to Project model if needed
                            )
                except Exception as e:
                    logger.warning(f"Failed to load project context: {e}")

            # Generate enhanced issue content
            content = await self.github_content_generator.generate_issue_content(
                user_request=original_message,
                project_context=project_context,
                template_preferences=workflow.context.get("template_preferences"),
            )

            logger.info(f"✅ Generated issue content: '{content.get('title', 'Unknown')}'")

            return TaskResult(
                success=True,
                output_data={
                    "enhanced_content": content,
                    "title": content.get("title"),
                    "body": content.get("body"),
                    "labels": content.get("labels", []),
                    "priority": content.get("priority", "medium"),
                    "issue_type": content.get("issue_type", "question"),
                },
            )

        except Exception as e:
            logger.error(f"Failed to generate GitHub issue content: {str(e)}")
            return TaskResult(success=False, error=f"Content generation error: {str(e)}")

    async def _extract_work_item(self, workflow: Workflow, task: Task) -> TaskResult:
        """Extract work item details from natural language"""
        try:
            # Get the original message from workflow context
            original_message = workflow.context.get("original_message", "")

            if not original_message:
                return TaskResult(
                    success=False, error="No original message found in workflow context"
                )

            # Create WorkItemExtractor and extract work item
            from services.domain.work_item_extractor import WorkItemExtractor

            extractor = WorkItemExtractor(self.llm_client)

            # Get project context if available
            project_context = None
            project_id = workflow.context.get("project_id")
            if project_id:
                try:
                    async with AsyncSessionFactory.session_scope() as session:
                        from services.database.repositories import ProjectRepository

                        project_repo = ProjectRepository(session)
                        project = await project_repo.get_by_id(project_id)
                        if project:
                            project_context = project.to_dict()
                except Exception as e:
                    logger.warning(f"Failed to get project context: {str(e)}")

            # Extract work item
            work_item = await extractor.extract_from_prompt(original_message, project_context)

            return TaskResult(
                success=True,
                output_data={
                    "work_item": work_item.to_dict(),
                    "extraction_success": True,
                },
            )

        except Exception as e:
            logger.error(f"Work item extraction failed: {str(e)}")
            return TaskResult(success=False, error=f"Extraction error: {str(e)}")

    async def _summarize(self, workflow: Workflow, task: Task) -> TaskResult:
        """Handle general analysis/summarization tasks without files"""
        try:
            if not self.llm_client:
                return TaskResult(success=False, error="LLM client not available for summarization")

            # Get the original message/query from workflow context
            original_message = workflow.context.get("original_message", "")

            if not original_message:
                return TaskResult(success=False, error="No message content found for analysis")

            # Use the SUMMARIZE task type for general analysis
            prompt = f"""Please analyze the following user request and provide a helpful response:

{original_message}

Focus on:
- Understanding what the user is asking for
- Providing actionable insights or recommendations
- Offering specific steps or solutions where applicable
"""

            response = await self.llm_client.complete(
                task_type=TaskType.SUMMARIZE.value, prompt=prompt
            )

            return TaskResult(
                success=True,
                output_data={
                    "analysis": {
                        "summary": response,
                        "analysis_type": "general_analysis",
                        "original_request": original_message,
                    }
                },
            )

        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return TaskResult(success=False, error=f"Analysis failed: {str(e)}")

    async def _list_projects(self, workflow: Workflow, task: Task) -> TaskResult:
        """List projects from the database."""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                from services.database.repositories import ProjectRepository

                project_repo = ProjectRepository(session)
                projects = await project_repo.list_active_projects()

                if not projects:
                    return TaskResult(success=True, output_data={"projects": []})

                project_list = [p.to_dict() for p in projects]
                return TaskResult(success=True, output_data={"projects": project_list})
        except Exception as e:
            logger.error(f"Failed to list projects: {str(e)}")
            return TaskResult(success=False, error=f"Project listing error: {str(e)}")

    async def _update_work_item(self, workflow: Workflow, task: Task) -> TaskResult:
        """Update an existing work item (task, issue, etc.)"""
        try:
            original_message = workflow.context.get("original_message", "")
            work_item_id = workflow.context.get("work_item_id")

            if not work_item_id:
                return TaskResult(success=False, error="No work item ID provided for update")

            # Extract update information from the message
            prompt = f"""Please analyze this update request and extract the key changes needed:

{original_message}

Work Item ID: {work_item_id}

Extract:
- What fields need to be updated
- New values for those fields
- Priority level of the update
- Any additional context
"""

            if self.llm_client:
                response = await self.llm_client.complete(
                    task_type=TaskType.UPDATE_WORK_ITEM.value, prompt=prompt
                )
            else:
                response = "Update analysis completed"

            return TaskResult(
                success=True,
                output_data={
                    "work_item_id": work_item_id,
                    "update_analysis": response,
                    "update_type": "work_item_update",
                },
            )

        except Exception as e:
            logger.error(f"Work item update failed: {str(e)}")
            return TaskResult(success=False, error=f"Update failed: {str(e)}")

    async def _generate_document(self, workflow: Workflow, task: Task) -> TaskResult:
        """Generate a document based on workflow context"""
        try:
            original_message = workflow.context.get("original_message", "")
            document_type = workflow.context.get("document_type", "general")

            if not original_message:
                return TaskResult(
                    success=False, error="No content provided for document generation"
                )

            # Generate document content using LLM
            prompt = f"""Please generate a professional document based on this request:

{original_message}

Document Type: {document_type}

Requirements:
- Professional tone and formatting
- Clear structure and organization
- Actionable content where applicable
- Appropriate for the specified document type
"""

            if self.llm_client:
                document_content = await self.llm_client.complete(
                    task_type=TaskType.GENERATE_DOCUMENT.value, prompt=prompt
                )
            else:
                document_content = (
                    f"Document content for {document_type} based on: {original_message}"
                )

            return TaskResult(
                success=True,
                output_data={
                    "document_type": document_type,
                    "content": document_content,
                    "generation_success": True,
                },
            )

        except Exception as e:
            logger.error(f"Document generation failed: {str(e)}")
            return TaskResult(success=False, error=f"Document generation failed: {str(e)}")

    async def _create_summary(self, workflow: Workflow, task: Task) -> TaskResult:
        """Create a summary of information or data"""
        try:
            original_message = workflow.context.get("original_message", "")
            summary_type = workflow.context.get("summary_type", "general")

            if not original_message:
                return TaskResult(success=False, error="No content provided for summarization")

            # Create summary using LLM
            prompt = f"""Please create a comprehensive summary of the following:

{original_message}

Summary Type: {summary_type}

Requirements:
- Concise but comprehensive
- Key points and insights
- Actionable takeaways where applicable
- Appropriate for the specified summary type
"""

            if self.llm_client:
                summary_content = await self.llm_client.complete(
                    task_type=TaskType.CREATE_SUMMARY.value, prompt=prompt
                )
            else:
                summary_content = f"Summary of {summary_type}: {original_message[:200]}..."

            return TaskResult(
                success=True,
                output_data={
                    "summary_type": summary_type,
                    "content": summary_content,
                    "summary_success": True,
                },
            )

        except Exception as e:
            logger.error(f"Summary creation failed: {str(e)}")
            return TaskResult(success=False, error=f"Summary creation failed: {str(e)}")

    async def _process_user_feedback(self, workflow: Workflow, task: Task) -> TaskResult:
        """Process and analyze user feedback"""
        try:
            original_message = workflow.context.get("original_message", "")
            feedback_type = workflow.context.get("feedback_type", "general")

            if not original_message:
                return TaskResult(success=False, error="No feedback content provided")

            # Process feedback using LLM
            prompt = f"""Please analyze this user feedback and provide insights:

{original_message}

Feedback Type: {feedback_type}

Analysis Requirements:
- Identify key themes and patterns
- Assess sentiment and tone
- Extract actionable insights
- Suggest improvements or responses
- Categorize feedback type (bug, feature, general, etc.)
"""

            if self.llm_client:
                feedback_analysis = await self.llm_client.complete(
                    task_type=TaskType.PROCESS_USER_FEEDBACK.value, prompt=prompt
                )
            else:
                feedback_analysis = (
                    f"Feedback analysis for {feedback_type}: {original_message[:200]}..."
                )

            return TaskResult(
                success=True,
                output_data={
                    "feedback_type": feedback_type,
                    "analysis": feedback_analysis,
                    "processing_success": True,
                },
            )

        except Exception as e:
            logger.error(f"Feedback processing failed: {str(e)}")
            return TaskResult(success=False, error=f"Feedback processing failed: {str(e)}")

    async def _placeholder_handler(self, workflow: Workflow, task: Task) -> TaskResult:
        """Placeholder for unimplemented handlers"""
        logger.info(f"Placeholder handler for {task.type.value if task.type else 'unknown'}")
        return TaskResult(success=True, output_data={"placeholder": True})


def get_github_analyzer():
    # Import only when needed
    from services.integrations.github.issue_analyzer import GitHubIssueAnalyzer

    return GitHubIssueAnalyzer()


# Global engine instance
engine = OrchestrationEngine()


# PM-062: Test utility for in-memory workflow testing


def create_test_engine():
    """Create an OrchestrationEngine instance for testing without database dependencies"""
    return OrchestrationEngine(test_mode=True)

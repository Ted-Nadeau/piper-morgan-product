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
from typing import Any, Dict, List, Optional, Union

import structlog

from services.analysis.file_type_detector import FileTypeDetector
from services.api.errors import TaskFailedError, WorkflowTimeoutError
from services.database.repositories import TaskRepository, WorkflowRepository
from services.database.session_factory import AsyncSessionFactory

# Domain-first imports - use domain models consistently
from services.domain.models import Intent, IntentCategory, Task, Workflow
from services.integrations.github.config_service import GitHubConfigService
from services.integrations.github.content_generator import GitHubIssueContentGenerator
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.issue_analyzer import GitHubIssueAnalyzer
from services.integrations.github.production_client import (
    GitHubClientConfig,
    ProductionGitHubClient,
)
from services.intent_service.intent_enricher import IntentEnricher
from services.llm.clients import LLMClient
from services.queries.query_router import QueryRouter
from services.shared_types import TaskStatus, TaskType, WorkflowStatus, WorkflowType

# Multi-Agent Coordinator Integration
from .integration import PerformanceMonitor, SessionIntegration, WorkflowIntegration

logger = structlog.get_logger()


@dataclass
class TaskResult:
    """Represents the result of executing a task"""

    task_id: str
    status: TaskStatus
    output_data: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time_seconds: Optional[float] = None


@dataclass
class WorkflowResult:
    """Represents the result of executing a complete workflow"""

    workflow_id: str
    status: WorkflowStatus
    task_results: List[TaskResult]
    total_execution_time_seconds: float
    error_message: Optional[str] = None


class OrchestrationEngine:
    """
    Orchestrates the execution of complex workflows
    Handles parallel task execution and error recovery
    """

    def __init__(self, llm_client: Optional[LLMClient] = None):
        # Use ServiceContainer if none provided
        if llm_client is None:
            from services.container import ServiceContainer

            container = ServiceContainer()
            llm_client = container.get_service("llm")

        self.llm_client = llm_client

        # PM-039 Factory Pattern: Initialize WorkflowFactory and registry
        from .workflow_factory import WorkflowFactory

        self.factory = WorkflowFactory()
        self.workflows = {}

        # QueryRouter will be initialized on-demand using async session pattern
        # Following the AsyncSessionFactory pattern from lines 135-138
        self.query_router = None

        self.intent_enricher = IntentEnricher(llm_client)
        self.logger = structlog.get_logger()

        # Initialize Multi-Agent integration
        self.workflow_integration = WorkflowIntegration()
        self.session_integration = SessionIntegration()
        self.performance_monitor = PerformanceMonitor()

        # Initialize Learning System (Issue #221 - CORE-LEARN-A)
        from services.learning.query_learning_loop import QueryLearningLoop

        self.learning_loop = QueryLearningLoop()
        self.logger.info("Learning system initialized in OrchestrationEngine")

    async def get_query_router(self) -> QueryRouter:
        """Get QueryRouter, initializing on-demand with session-aware wrappers"""
        if self.query_router is None:
            from services.queries.conversation_queries import ConversationQueryService
            from services.queries.session_aware_wrappers import (
                SessionAwareFileQueryService,
                SessionAwareProjectQueryService,
            )

            # Initialize QueryRouter with session-aware services
            # These services handle their own session management per-operation
            self.query_router = QueryRouter(
                project_query_service=SessionAwareProjectQueryService(),
                conversation_query_service=ConversationQueryService(),
                file_query_service=SessionAwareFileQueryService(),
            )
            self.logger.info("QueryRouter initialized with session-aware wrappers")

        return self.query_router

    async def handle_query_intent(self, intent: Intent) -> Dict[str, Any]:
        """Handle QUERY intents using QueryRouter integration (GREAT-1B bridge method)"""
        try:
            # Get QueryRouter with session-aware wrappers
            query_router = await self.get_query_router()

            # Route the query based on action
            result = None
            if intent.action in ["search_projects", "list_projects", "find_projects"]:
                # Use project query service through QueryRouter
                projects = await query_router.project_queries.list_active_projects()
                result = {
                    "message": f"Found {len(projects)} active projects",
                    "data": [
                        {"id": p.id, "name": p.name, "description": p.description} for p in projects
                    ],
                    "intent_handled": True,
                }

            elif intent.action in ["search_files", "find_files", "list_files"]:
                # Use file query service through QueryRouter
                files = await query_router.file_queries.list_recent_files(limit=10)
                result = {
                    "message": f"Found {len(files)} recent files",
                    "data": files,
                    "intent_handled": True,
                }

            elif intent.action in ["get_greeting", "hello", "help"]:
                # Use conversation query service through QueryRouter
                greeting = await query_router.conversation_queries.get_greeting()
                result = {"message": greeting, "data": {}, "intent_handled": True}

            else:
                result = {
                    "message": f"Query action '{intent.action}' not yet supported by QueryRouter",
                    "data": {},
                    "intent_handled": False,
                }

            # Learning System Integration (Issue #221 - CORE-LEARN-A)
            # Record successful patterns for future optimization
            if result and result.get("intent_handled"):
                try:
                    from services.learning.query_learning_loop import PatternType

                    await self.learning_loop.learn_pattern(
                        pattern_type=PatternType.QUERY_PATTERN,
                        source_feature=f"orchestration_{intent.category}",
                        pattern_data={
                            "query": intent.original_message or intent.action,
                            "action": intent.action,
                            "entity": intent.context.get("entity"),
                            "category": str(intent.category),
                        },
                        initial_confidence=intent.confidence if intent.confidence else 0.8,
                        metadata={
                            "timestamp": datetime.now().isoformat(),
                            "success": True,
                        },
                    )
                except Exception as learning_error:
                    # Learning failures should not impact query handling
                    self.logger.debug(f"Learning pattern recording failed: {learning_error}")

            return result

        except Exception as e:
            self.logger.error(f"QueryRouter error: {e}")
            return {
                "message": f"Failed to process query: {str(e)}",
                "data": {},
                "intent_handled": False,
                "error": str(e),
            }

    async def create_workflow_from_intent(self, intent: Intent) -> Optional[Workflow]:
        """
        Create appropriate workflow based on intent with database persistence

        PM-039 Restoration: Authentic implementation using WorkflowFactory
        Follows established DDD patterns with proper context validation and enrichment
        """
        try:
            workflow = await self.factory.create_from_intent(intent)

            # PM-039 Pattern: Enrich CREATE_TICKET workflows with repository from project
            if workflow and workflow.type == WorkflowType.CREATE_TICKET:
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
                                    self.logger.info(
                                        f"Enriched CREATE_TICKET workflow with repository: {repository}"
                                    )
                                else:
                                    self.logger.warning(
                                        f"Project {project_id} has no GitHub repository configured"
                                    )
                            else:
                                self.logger.warning(f"Project {project_id} not found")
                    except Exception as e:
                        self.logger.error(f"Failed to enrich workflow with repository: {str(e)}")

            # PM-039 Pattern: Store workflow in registry for tracking
            if workflow:
                self.workflows[workflow.id] = workflow
                self.logger.info(f"Created workflow {workflow.id} for intent {intent.action}")

            return workflow

        except Exception as e:
            self.logger.error(f"Failed to create workflow from intent: {str(e)}")
            return None

    async def execute_workflow(self, workflow: Union[str, Workflow]) -> WorkflowResult:
        """
        Execute a complete workflow, handling task dependencies and error recovery

        Args:
            workflow: Either a Workflow object or workflow ID string to look up

        Returns:
            WorkflowResult with execution details

        Raises:
            ValueError: If workflow ID is provided but not found in registry
        """
        # Support both workflow objects and IDs
        if isinstance(workflow, str):
            workflow_id = workflow
            if workflow_id not in self.workflows:
                raise ValueError(f"Workflow {workflow_id} not found")
            workflow = self.workflows[workflow_id]

        start_time = datetime.now()
        task_results = []

        try:
            # Update workflow status
            workflow.status = WorkflowStatus.RUNNING

            # Execute tasks in dependency order
            for task in workflow.tasks:
                task_result = await self._execute_task(task, workflow)
                task_results.append(task_result)

                # Stop execution if a critical task fails
                if task_result.status == TaskStatus.FAILED and task.type in [
                    TaskType.ANALYZE_REQUEST,
                    TaskType.EXTRACT_REQUIREMENTS,
                ]:
                    workflow.status = WorkflowStatus.FAILED
                    return WorkflowResult(
                        workflow_id=workflow.id,
                        status=WorkflowStatus.FAILED,
                        task_results=task_results,
                        total_execution_time_seconds=(datetime.now() - start_time).total_seconds(),
                        error_message=f"Critical task {task.id} failed",
                    )

            # Mark workflow as completed if all tasks succeeded
            workflow.status = WorkflowStatus.COMPLETED
            return WorkflowResult(
                workflow_id=workflow.id,
                status=WorkflowStatus.COMPLETED,
                task_results=task_results,
                total_execution_time_seconds=(datetime.now() - start_time).total_seconds(),
            )

        except Exception as e:
            self.logger.error("Workflow execution failed", error=str(e), workflow_id=workflow.id)
            workflow.status = WorkflowStatus.FAILED
            workflow.error = str(e)
            return WorkflowResult(
                workflow_id=workflow.id,
                status=WorkflowStatus.FAILED,
                task_results=task_results,
                total_execution_time_seconds=(datetime.now() - start_time).total_seconds(),
                error_message=str(e),
            )

    async def _execute_task(self, task: Task, workflow: Workflow) -> TaskResult:
        """Execute a single task within a workflow context"""
        start_time = datetime.now()

        try:
            task.status = TaskStatus.RUNNING

            if task.type == TaskType.ANALYZE_REQUEST:
                output_data = await self._analyze_request_task(task, workflow)
            elif task.type == TaskType.EXTRACT_REQUIREMENTS:
                output_data = await self._extract_requirements_task(task, workflow)
            elif task.type == TaskType.IDENTIFY_DEPENDENCIES:
                output_data = await self._identify_dependencies_task(task, workflow)
            elif task.type == TaskType.GENERATE_DOCUMENTATION:
                output_data = await self._generate_documentation_task(task, workflow)
            elif task.type == TaskType.EXECUTE_GITHUB_ACTION:
                output_data = await self._execute_github_action_task(task, workflow)
            else:
                raise ValueError(f"Unknown task type: {task.type}")

            task.status = TaskStatus.COMPLETED
            execution_time = (datetime.now() - start_time).total_seconds()

            return TaskResult(
                task_id=task.id,
                status=TaskStatus.COMPLETED,
                output_data=output_data,
                execution_time_seconds=execution_time,
            )

        except Exception as e:
            task.status = TaskStatus.FAILED
            execution_time = (datetime.now() - start_time).total_seconds()

            self.logger.error(
                "Task execution failed",
                task_id=task.id,
                error=str(e),
                execution_time=execution_time,
            )

            return TaskResult(
                task_id=task.id,
                status=TaskStatus.FAILED,
                output_data={},
                error_message=str(e),
                execution_time_seconds=execution_time,
            )

    async def _analyze_request_task(self, task: Task, workflow: Workflow) -> Dict[str, Any]:
        """Analyze the user's request to understand requirements"""

        intent_context = workflow.context.get("intent", {})

        # Use intent enricher for deeper analysis
        analysis = await self.intent_enricher.enrich_intent(
            message=intent_context.get("original_message", ""),
            category=intent_context.get("category", IntentCategory.UNKNOWN),
            context=workflow.context,
        )

        return {
            "analysis": analysis,
            "requirements": analysis.get("requirements", []),
            "complexity": analysis.get("complexity", "unknown"),
            "estimated_effort": analysis.get("estimated_effort", "unknown"),
        }

    async def _extract_requirements_task(self, task: Task, workflow: Workflow) -> Dict[str, Any]:
        """Extract detailed requirements from the analysis"""

        # Get analysis from previous task
        analysis_task = next(
            (t for t in workflow.tasks if t.type == TaskType.ANALYZE_REQUEST), None
        )
        if not analysis_task or analysis_task.status != TaskStatus.COMPLETED:
            raise TaskFailedError("Cannot extract requirements without completed analysis")

        # Extract requirements using LLM
        prompt = f"""
        Based on this analysis: {analysis_task.output_data}

        Extract detailed technical requirements including:
        1. Functional requirements
        2. Non-functional requirements
        3. Technical constraints
        4. Success criteria

        Return as structured data.
        """

        response = await self.llm_client.generate_response(prompt)

        return {
            "functional_requirements": response.get("functional_requirements", []),
            "non_functional_requirements": response.get("non_functional_requirements", []),
            "technical_constraints": response.get("technical_constraints", []),
            "success_criteria": response.get("success_criteria", []),
        }

    async def _identify_dependencies_task(self, task: Task, workflow: Workflow) -> Dict[str, Any]:
        """Identify dependencies and prerequisites"""

        requirements_task = next(
            (t for t in workflow.tasks if t.type == TaskType.EXTRACT_REQUIREMENTS), None
        )
        if not requirements_task or requirements_task.status != TaskStatus.COMPLETED:
            raise TaskFailedError("Cannot identify dependencies without completed requirements")

        # Analyze dependencies
        dependencies = {
            "file_dependencies": [],
            "service_dependencies": [],
            "external_dependencies": [],
            "prerequisite_tasks": [],
        }

        # Add logic to identify dependencies based on requirements
        requirements = requirements_task.output_data

        return dependencies

    async def _generate_documentation_task(self, task: Task, workflow: Workflow) -> Dict[str, Any]:
        """Generate documentation for the solution"""

        # Gather context from previous tasks
        context = {}
        for prev_task in workflow.tasks:
            if prev_task.status == TaskStatus.COMPLETED:
                context[prev_task.type.value] = prev_task.output_data

        # Generate documentation using LLM
        prompt = f"""
        Generate comprehensive documentation for this implementation:
        Context: {context}

        Include:
        1. Overview
        2. Technical specifications
        3. Implementation guide
        4. Testing strategy
        """

        response = await self.llm_client.generate_response(prompt)

        return {"documentation": response, "generated_at": datetime.now().isoformat()}

    async def _execute_github_action_task(self, task: Task, workflow: Workflow) -> Dict[str, Any]:
        """Execute GitHub-related actions"""

        github_config = GitHubConfigService()
        github_client = ProductionGitHubClient(
            GitHubClientConfig(
                token=github_config.get_github_token(),
                owner=github_config.get_github_owner(),
                repo=github_config.get_github_repo(),
            )
        )

        github_agent = GitHubIntegrationRouter()

        # Execute the GitHub action based on task input
        action_type = task.input_data.get("action_type", "create_issue")

        if action_type == "create_issue":
            result = await github_agent.create_issue(
                title=task.input_data.get("title", "Generated Issue"),
                body=task.input_data.get("body", "Generated from workflow"),
                labels=task.input_data.get("labels", []),
            )
        else:
            raise ValueError(f"Unknown GitHub action type: {action_type}")

        return {
            "github_result": result,
            "action_type": action_type,
            "executed_at": datetime.now().isoformat(),
        }


# Global engine instance - will be initialized in main.py
engine: Optional[OrchestrationEngine] = None


def set_global_engine(engine_instance: OrchestrationEngine) -> None:
    """
    Set the global orchestration engine instance
    Phase 3A: DDD-compliant dependency injection support
    """
    global engine
    engine = engine_instance

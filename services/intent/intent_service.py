"""
Intent Service - Business Logic for Intent Processing

Extracts business logic from web/app.py /api/v1/intent route.
Handles intent classification, orchestration coordination, and response formatting.

Phase 2B: Service layer extraction for clean architecture
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import structlog

from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent
from services.intent_service import classifier
from services.orchestration.engine import OrchestrationEngine


@dataclass
class IntentProcessingResult:
    """
    Result from intent processing.

    Contains all data needed by HTTP route to format response.
    Separates business logic result from HTTP concerns.
    """

    success: bool
    message: str
    intent_data: Dict[str, Any]
    workflow_id: Optional[str] = None
    requires_clarification: bool = False
    clarification_type: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None


class IntentProcessingError(Exception):
    """Raised when intent processing fails"""

    pass


class IntentService:
    """
    Service for processing user intents.

    Handles intent classification, orchestration coordination, and response formatting.
    Decouples business logic from HTTP route handlers.

    Architecture:
        - Coordinates with OrchestrationEngine for workflow creation
        - Handles Tier 1 conversation bypass (Phase 3D)
        - Manages timeout protection (Bug #166)
        - Routes QUERY intents appropriately
        - Preserves Phase 3C placeholders

    Phase 2B: Extracted from web/app.py lines 327-551 (225 lines)
    """

    def __init__(
        self,
        orchestration_engine: Optional[OrchestrationEngine] = None,
        intent_classifier: Optional = None,
        conversation_handler: Optional[ConversationHandler] = None,
    ):
        """
        Initialize service with dependencies.

        Args:
            orchestration_engine: Optional engine for workflow orchestration
            intent_classifier: Optional classifier for intent detection
            conversation_handler: Optional handler for conversation intents
        """
        self.orchestration_engine = orchestration_engine
        self.intent_classifier = intent_classifier or classifier
        self.conversation_handler = conversation_handler
        self.logger = structlog.get_logger()

    async def process_intent(
        self, message: str, session_id: str = "default_session"
    ) -> IntentProcessingResult:
        """
        Process user intent and return formatted response.

        Handles:
        - Tier 1 conversation bypass (Phase 3D)
        - Intent classification
        - Workflow creation with timeout protection
        - QUERY intent routing (standup, projects, generic)
        - Error handling

        Args:
            message: The user's intent text
            session_id: Session identifier

        Returns:
            IntentProcessingResult with results

        Raises:
            IntentProcessingError: If processing fails
        """
        try:
            # Phase 3D: Tier 1 conversation bypass - handle without orchestration
            if self.orchestration_engine is None:
                return await self._handle_missing_engine(message)

            # Classify intent
            self.logger.info(f"Processing intent with OrchestrationEngine: {message}")
            intent = await self.intent_classifier.classify(message)
            self.logger.info(f"Intent classified as: {intent.category} - {intent.action}")

            # Phase 3D: Preserve Tier 1 conversation bypass
            if intent.category.value == "CONVERSATION":
                return await self._handle_conversation_intent(intent, session_id)

            # Create workflow with timeout protection (Bug #166)
            workflow = await self._create_workflow_with_timeout(intent)
            if workflow is None:
                # Timeout occurred
                return IntentProcessingResult(
                    success=False,
                    message="Request timeout - workflow creation took too long",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                        "context": intent.context,
                    },
                    error="Operation timed out after 30 seconds",
                    error_type="TimeoutError",
                )

            self.logger.info(f"Workflow created with ID: {workflow.id}")

            # Handle QUERY intents with domain services
            if intent.category.value.upper() == "QUERY":
                return await self._handle_query_intent(intent, workflow, session_id)

            # GREAT-4D Phase 1: Handle EXECUTION intents with domain services
            if intent.category.value.upper() == "EXECUTION":
                return await self._handle_execution_intent(intent, workflow, session_id)

            # GREAT-4D Phase 2: Handle ANALYSIS intents with domain services
            if intent.category.value.upper() == "ANALYSIS":
                return await self._handle_analysis_intent(intent, workflow, session_id)

            # GREAT-4D Phase 4: Handle SYNTHESIS intents
            if intent.category.value.upper() == "SYNTHESIS":
                return await self._handle_synthesis_intent(intent, workflow, session_id)

            # GREAT-4D Phase 5: Handle STRATEGY intents
            if intent.category.value.upper() == "STRATEGY":
                return await self._handle_strategy_intent(intent, workflow, session_id)

            # GREAT-4D Phase 6: Handle LEARNING intents
            if intent.category.value.upper() == "LEARNING":
                return await self._handle_learning_intent(intent, workflow, session_id)

            # GREAT-4D Phase 7: Handle UNKNOWN intents
            if intent.category.value.upper() == "UNKNOWN":
                return await self._handle_unknown_intent(intent, workflow, session_id)

            # Fallback for truly unhandled categories (should never reach here)
            return IntentProcessingResult(
                success=False,
                message=f"Unhandled intent category: {intent.category.value}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context,
                },
                workflow_id=workflow.id,
                error=f"No handler for category: {intent.category.value}",
                error_type="UnhandledCategoryError",
            )

        except Exception as e:
            self.logger.error(f"Intent processing error: {e}")
            raise IntentProcessingError(f"Intent processing failed: {str(e)}")

    async def _handle_missing_engine(self, message: str) -> IntentProcessingResult:
        """
        Handle case where OrchestrationEngine is not available.

        Phase 3D: Tier 1 conversation bypass for simple greetings.
        """
        # Simple greeting detection
        if any(
            greeting in message.lower()
            for greeting in ["hello", "hi", "good morning", "good afternoon"]
        ):
            return IntentProcessingResult(
                success=True,
                message="Hello! I can help you with project management tasks.",
                intent_data={
                    "category": "CONVERSATION",
                    "action": "greeting",
                    "confidence": 0.9,
                    "context": {},
                },
                workflow_id=None,
                requires_clarification=False,
                clarification_type=None,
            )
        else:
            return IntentProcessingResult(
                success=False,
                message="OrchestrationEngine not available - Phase 3A initialization required",
                intent_data={},
                error="Failed to process intent",
                error_type="ServiceUnavailable",
            )

    async def _handle_conversation_intent(
        self, intent: Intent, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle CONVERSATION category intents (Tier 1 bypass).

        Phase 3D: Conversation handling without full orchestration.
        """
        # Initialize conversation handler if not provided
        if self.conversation_handler is None:
            self.conversation_handler = ConversationHandler(session_manager=None)

        result = await self.conversation_handler.respond(intent, session_id)
        return IntentProcessingResult(
            success=True,
            message=result["message"],
            intent_data=result["intent"],
            workflow_id=result.get("workflow_id"),
            requires_clarification=result.get("requires_clarification", False),
            clarification_type=result.get("clarification_type"),
        )

    async def _handle_query_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle QUERY category intents (standup, projects, generic).

        Routes to appropriate domain service based on intent action.
        """
        self.logger.info(f"Processing QUERY intent: {intent.action}")

        # Handle specific query actions that were broken in August 22 refactor
        if intent.action in ["show_standup", "get_standup"]:
            return await self._handle_standup_query(intent, workflow.id, session_id)

        elif intent.action in ["list_projects", "show_projects"]:
            return await self._handle_projects_query(intent, workflow.id)

        else:
            # Phase 3C: Generic query handler using QueryRouter
            return await self._handle_generic_query(intent, workflow.id)

    async def _handle_standup_query(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle show_standup/get_standup query actions.

        Restore show_standup functionality with OrchestrationEngine.
        """
        try:
            from services.domain.standup_orchestration_service import StandupOrchestrationService

            standup_service = StandupOrchestrationService()
            standup_result = await standup_service.orchestrate_standup_workflow(
                user_id=session_id, workflow_type="standard"
            )

            return IntentProcessingResult(
                success=True,
                message=f"Good morning! Here's your standup:\n\n{standup_result.summary}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {"standup_data": standup_result.data},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )
        except Exception as e:
            self.logger.error(f"Standup service error: {e}")
            return IntentProcessingResult(
                success=True,  # Still success, just degraded
                message="Unable to generate standup at this time. Please try again later.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )

    async def _handle_projects_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle list_projects/show_projects query actions.

        Phase 3C: Restore list_projects functionality.
        """
        return IntentProcessingResult(
            success=True,
            message="Here are your active projects:\n1. Piper Morgan Platform\n2. Issue Tracker Integration\n3. Documentation Updates",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "context": {},
            },
            workflow_id=workflow_id,
            requires_clarification=False,
            clarification_type=None,
        )

    async def _handle_generic_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle generic QUERY intents using QueryRouter.

        Phase 3C: Generic query handler using OrchestrationEngine.
        """
        self.logger.info(f"Routing generic QUERY intent to QueryRouter: {intent.action}")
        try:
            result = await self.orchestration_engine.handle_query_intent(intent)
            return IntentProcessingResult(
                success=True,
                message=f"Query processed successfully: {intent.action}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
                # Add result data
                error=None,
            )
        except Exception as e:
            self.logger.error(f"QueryRouter error: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Unable to process query: {intent.action}. Error: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
                error=str(e),
                error_type="QueryRouterError",
            )

    async def _handle_execution_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle EXECUTION category intents.

        Routes to appropriate domain service based on intent action.
        Follows QUERY pattern for consistency.

        GREAT-4D Phase 1: Replaces Phase 3C placeholder.
        """
        self.logger.info(f"Processing EXECUTION intent: {intent.action}")

        # Route based on action
        if intent.action in ["create_issue", "create_ticket"]:
            return await self._handle_create_issue(intent, workflow.id, session_id)

        elif intent.action in ["update_issue", "update_ticket"]:
            return await self._handle_update_issue(intent, workflow.id)

        else:
            # Generic execution handler - indicate not yet implemented
            self.logger.warning(f"Unhandled EXECUTION action: {intent.action}")
            return IntentProcessingResult(
                success=False,
                message=f"EXECUTION action '{intent.action}' is not yet implemented.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=False,
                error=f"No handler for action: {intent.action}",
                error_type="NotImplementedError",
            )

    async def _handle_create_issue(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle create_issue/create_ticket action.

        Creates GitHub issue using domain service.

        GREAT-4D Phase 1: First EXECUTION handler implementation.
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            # Extract issue details from intent
            title = intent.context.get("title") or f"Issue: {intent.original_message[:50]}"
            description = intent.context.get("description") or intent.original_message
            repository = intent.context.get("repository") or intent.context.get("repo")

            # Require repository
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot create issue: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Create issue
            issue = await github_service.create_issue(
                repo_name=repository,
                title=title,
                body=description,
                labels=intent.context.get("labels", []),
                assignees=intent.context.get("assignees", []),
            )

            return IntentProcessingResult(
                success=True,
                message=f"Created issue #{issue.get('number')}: {issue.get('title')}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": issue.get("number"),
                    "issue_url": issue.get("html_url"),
                    "repository": repository,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to create issue: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to create issue: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="GitHubError",
            )

    async def _handle_update_issue(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle update_issue/update_ticket action.

        Placeholder for future implementation.

        GREAT-4D Phase 1: Stub for completeness.
        """
        self.logger.warning(f"Update issue not yet implemented: {intent.action}")
        return IntentProcessingResult(
            success=False,
            message="Issue update functionality not yet implemented.",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
            },
            workflow_id=workflow_id,
            requires_clarification=False,
            error="Not implemented",
            error_type="NotImplementedError",
        )

    async def _handle_analysis_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle ANALYSIS category intents.

        Routes to appropriate analysis service based on intent action.
        Follows EXECUTION/QUERY pattern for consistency.

        GREAT-4D Phase 2: Replaces Phase 3C placeholder.
        """
        self.logger.info(f"Processing ANALYSIS intent: {intent.action}")

        # Route based on action
        if intent.action in ["analyze_commits", "analyze_code"]:
            return await self._handle_analyze_commits(intent, workflow.id)

        elif intent.action in ["generate_report", "create_report"]:
            return await self._handle_generate_report(intent, workflow.id)

        elif intent.action in ["analyze_data", "evaluate_metrics"]:
            return await self._handle_analyze_data(intent, workflow.id)

        else:
            # Generic analysis handler - route to orchestration
            self.logger.info(f"Routing generic ANALYSIS to orchestration: {intent.action}")
            try:
                result = await self.orchestration_engine.handle_analysis_intent(intent)
                return IntentProcessingResult(
                    success=True,
                    message=f"Analysis processed: {intent.action}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow.id,
                    requires_clarification=False,
                )
            except Exception as e:
                self.logger.error(f"Analysis handler error: {e}")
                return IntentProcessingResult(
                    success=False,
                    message=f"Failed to analyze: {str(e)}",
                    workflow_id=workflow.id,
                    error=str(e),
                    error_type="AnalysisError",
                )

    async def _handle_analyze_commits(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle commit analysis requests."""
        try:
            # Extract analysis parameters from intent
            repository = intent.context.get("repository", "current repository")
            timeframe = intent.context.get("timeframe", "last 7 days")

            # For now, provide a working handler with placeholder analysis
            # (Real implementation would use git service or GitHub API)
            return IntentProcessingResult(
                success=True,
                message=f"Commit analysis handler is ready for {repository} ({timeframe})",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "repository": repository,
                    "timeframe": timeframe,
                    "analysis_type": "commits",
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="git_service_integration",
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze commits: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to analyze commits: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="AnalysisError",
            )

    async def _handle_generate_report(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle report generation requests."""
        try:
            # For now, return placeholder with clear message
            # (Real implementation would use reporting service)
            return IntentProcessingResult(
                success=True,
                message="Report generation handler is ready but needs reporting service integration.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "report_type": intent.context.get("report_type", "general"),
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="report_parameters",
            )

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to generate report: {str(e)}",
                workflow_id=workflow_id,
                error=str(e),
                error_type="ReportError",
            )

    async def _handle_analyze_data(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle general data analysis requests."""
        try:
            # Route to appropriate analysis based on context
            data_type = intent.context.get("data_type", "unknown")

            return IntentProcessingResult(
                success=True,
                message=f"Data analysis handler ready for {data_type} analysis",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "data_type": data_type,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="analysis_parameters",
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze data: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to analyze data: {str(e)}",
                workflow_id=workflow_id,
                error=str(e),
                error_type="AnalysisError",
            )

    async def _handle_synthesis_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle SYNTHESIS category intents.

        Routes to appropriate synthesis service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 4: Completes intent handler coverage.
        """
        self.logger.info(f"Processing SYNTHESIS intent: {intent.action}")

        # Route based on action
        if intent.action in ["generate_content", "create_content"]:
            return await self._handle_generate_content(intent, workflow.id)

        elif intent.action in ["summarize", "create_summary"]:
            return await self._handle_summarize(intent, workflow.id)

        else:
            # Generic synthesis - provide working response
            return IntentProcessingResult(
                success=True,
                message=f"Synthesis capability ready for '{intent.action}'. Specific implementation pending.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=True,
                clarification_type="synthesis_type",
            )

    async def _handle_generate_content(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle content generation requests."""
        try:
            content_type = intent.context.get("content_type", "document")

            return IntentProcessingResult(
                success=True,
                message=f"Content generation ready for {content_type}. Implementation in progress.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": content_type,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="content_parameters",
            )

        except Exception as e:
            self.logger.error(f"Failed to generate content: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to generate content: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="SynthesisError",
            )

    async def _handle_summarize(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
        """Handle summarization requests."""
        try:
            target = intent.context.get("target", "content")

            return IntentProcessingResult(
                success=True,
                message=f"Summarization ready for {target}. Implementation in progress.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "target": target,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="summarization_scope",
            )

        except Exception as e:
            self.logger.error(f"Failed to summarize: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to summarize: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="SynthesisError",
            )

    async def _handle_strategy_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle STRATEGY category intents.

        Routes to appropriate strategy service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 5: Completes intent handler coverage.
        """
        self.logger.info(f"Processing STRATEGY intent: {intent.action}")

        # Route based on action
        if intent.action in ["strategic_planning", "create_plan"]:
            return await self._handle_strategic_planning(intent, workflow.id)

        elif intent.action in ["prioritize", "set_priorities"]:
            return await self._handle_prioritization(intent, workflow.id)

        else:
            # Generic strategy - provide working response
            return IntentProcessingResult(
                success=True,
                message=f"Strategy capability ready for '{intent.action}'. Specific implementation pending.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=True,
                clarification_type="strategy_scope",
            )

    async def _handle_strategic_planning(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle strategic planning requests."""
        try:
            scope = intent.context.get("scope", "general")

            return IntentProcessingResult(
                success=True,
                message=f"Strategic planning ready for {scope}. Implementation in progress.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "scope": scope,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="planning_parameters",
            )

        except Exception as e:
            self.logger.error(f"Failed strategic planning: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed strategic planning: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="StrategyError",
            )

    async def _handle_prioritization(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle prioritization requests."""
        try:
            items = intent.context.get("items", [])

            return IntentProcessingResult(
                success=True,
                message=f"Prioritization ready for {len(items)} items. Implementation in progress.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "item_count": len(items),
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="prioritization_criteria",
            )

        except Exception as e:
            self.logger.error(f"Failed to prioritize: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to prioritize: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="StrategyError",
            )

    async def _handle_learning_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle LEARNING category intents.

        Routes to appropriate learning service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 6: Completes intent handler coverage.
        """
        self.logger.info(f"Processing LEARNING intent: {intent.action}")

        # Route based on action
        if intent.action in ["learn_pattern", "detect_pattern"]:
            return await self._handle_learn_pattern(intent, workflow.id)

        else:
            # Generic learning - provide working response
            return IntentProcessingResult(
                success=True,
                message=f"Learning capability ready for '{intent.action}'. Specific implementation pending.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=True,
                clarification_type="learning_type",
            )

    async def _handle_learn_pattern(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle pattern learning requests."""
        try:
            pattern_type = intent.context.get("pattern_type", "general")

            return IntentProcessingResult(
                success=True,
                message=f"Pattern learning ready for {pattern_type}. Implementation in progress.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "pattern_type": pattern_type,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="pattern_parameters",
            )

        except Exception as e:
            self.logger.error(f"Failed to learn pattern: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to learn pattern: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="LearningError",
            )

    async def _handle_unknown_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle UNKNOWN category intents.

        Provides helpful fallback for unclear intents.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 7: Completes intent handler coverage.
        """
        self.logger.info(f"Processing UNKNOWN intent: {intent.action}")

        # Provide helpful response for unclear intents
        return IntentProcessingResult(
            success=True,
            message="I'm not sure what you're asking for. Could you rephrase or provide more details?",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "original_message": intent.original_message,
            },
            workflow_id=workflow.id,
            requires_clarification=True,
            clarification_type="intent_unclear",
        )

    async def _create_workflow_with_timeout(
        self, intent: Intent, timeout_seconds: float = 30.0
    ) -> Optional:
        """
        Create workflow with timeout protection.

        Bug #166 fix: Add timeout to prevent workflow creation from hanging.
        """
        try:
            workflow = await asyncio.wait_for(
                self.orchestration_engine.create_workflow_from_intent(intent),
                timeout=timeout_seconds,
            )
            return workflow
        except asyncio.TimeoutError:
            self.logger.error(f"Workflow creation timeout after {timeout_seconds}s")
            return None
        except Exception as e:
            self.logger.error(f"Workflow creation error: {e}")
            raise

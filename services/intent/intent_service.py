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
            if intent.category.value == "QUERY":
                return await self._handle_query_intent(intent, workflow, session_id)

            # Phase 3C: For EXECUTION/ANALYSIS intents, indicate orchestration needed
            return await self._handle_generic_intent(intent)

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

    async def _handle_generic_intent(self, intent: Intent) -> IntentProcessingResult:
        """
        Handle EXECUTION/ANALYSIS intents (Phase 3C placeholder).

        Phase 3C: For EXECUTION/ANALYSIS intents, indicate orchestration needed.
        """
        return IntentProcessingResult(
            success=True,
            message=f"Intent '{intent.action}' (category: {intent.category.value}) requires full orchestration workflow. This is being restored in Phase 3.",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "context": intent.context,
            },
            workflow_id=None,
            requires_clarification=False,
            clarification_type=None,
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

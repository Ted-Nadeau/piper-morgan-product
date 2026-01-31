"""
Adapters for existing process managers to implement GuidedProcess protocol.

These adapters wrap the existing PortfolioOnboardingManager and
StandupConversationManager to work with the ProcessRegistry.

ADR-049: Two-Tier Intent Architecture
Issue #427: MUX-IMPLEMENT-CONVERSE-MODEL
"""

from typing import Any, Dict, Optional

import structlog

from services.process.registry import GuidedProcess, ProcessCheckResult, ProcessType
from services.shared_types import IntentCategory

logger = structlog.get_logger(__name__)


class OnboardingProcessAdapter:
    """
    Adapter wrapping PortfolioOnboardingManager for ProcessRegistry.

    Implements GuidedProcess protocol by delegating to the existing
    singleton manager and handler.
    """

    def __init__(self):
        self._manager = None
        self._handler = None

    def _get_components(self):
        """Lazy-load components to avoid circular imports."""
        if self._manager is None:
            from services.conversation.conversation_handler import _get_onboarding_components

            self._manager, self._handler = _get_onboarding_components()
        return self._manager, self._handler

    @property
    def process_type(self) -> ProcessType:
        return ProcessType.ONBOARDING

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """Check if there's an active onboarding session."""
        from services.shared_types import PortfolioOnboardingState

        manager, _ = self._get_components()

        # Issue #490 INVESTIGATION: Verify singleton manager ID matches creation
        print(
            f"[OnboardingProcessAdapter] check_active: manager id={id(manager)}, sessions={len(manager._sessions)}"
        )

        # Try user_id first (preferred), then session_id (fallback)
        session = None
        if user_id:
            session = manager.get_session_by_user(user_id)
        if not session and session_id:
            session = manager.get_session_by_session_id(session_id)

        if not session:
            return False

        # Check if terminal state
        if session.state in (
            PortfolioOnboardingState.COMPLETE,
            PortfolioOnboardingState.DECLINED,
        ):
            return False

        return True

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """Handle a message in active onboarding session."""
        from services.shared_types import PortfolioOnboardingState

        manager, handler = self._get_components()

        # Get the session (we know it exists from check_active)
        session = None
        if user_id:
            session = manager.get_session_by_user(user_id)
        if not session and session_id:
            session = manager.get_session_by_session_id(session_id)

        if not session:
            return ProcessCheckResult.not_handled()

        # Handle the turn
        response = handler.handle_turn(session.id, message)

        # Issue #728: Include captured_projects in context for persistence
        # IntentService._check_active_guided_process() looks for this
        # to persist projects when onboarding completes
        context = {
            "onboarding_id": session.id,
            "state": response.state.value,
            "bypassed_classification": True,
            "guided_process": ProcessType.ONBOARDING.value,
        }

        # Add captured_projects when onboarding completes
        if response.is_complete and response.captured_projects:
            context["captured_projects"] = response.captured_projects

        intent_data = {
            "category": IntentCategory.GUIDANCE.value,
            "action": "portfolio_onboarding",
            "confidence": 1.0,
            "context": context,
        }

        return ProcessCheckResult.handled_by(
            process_type=ProcessType.ONBOARDING,
            response_message=response.message,
            intent_data=intent_data,
        )


class StandupProcessAdapter:
    """
    Adapter wrapping StandupConversationManager for ProcessRegistry.

    Implements GuidedProcess protocol by delegating to the existing
    singleton manager and handler.
    """

    def __init__(self):
        self._manager = None
        self._handler = None

    def _get_components(self):
        """Lazy-load components to avoid circular imports."""
        if self._manager is None:
            from services.conversation.conversation_handler import _get_standup_components

            self._manager, self._handler = _get_standup_components()
        return self._manager, self._handler

    @property
    def process_type(self) -> ProcessType:
        return ProcessType.STANDUP

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """Check if there's an active standup conversation."""
        from services.shared_types import StandupConversationState

        manager, _ = self._get_components()

        # Standup uses session_id for lookup
        conversation = None
        if session_id:
            conversation = manager.get_conversation_by_session(session_id)

        if not conversation:
            return False

        # Check if terminal state
        if conversation.state in (
            StandupConversationState.COMPLETE,
            StandupConversationState.ABANDONED,
        ):
            return False

        return True

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """Handle a message in active standup conversation."""
        from services.shared_types import StandupConversationState

        manager, handler = self._get_components()

        # Get the conversation
        conversation = None
        if session_id:
            conversation = manager.get_conversation_by_session(session_id)

        if not conversation:
            return ProcessCheckResult.not_handled()

        # Handle the turn (standup handler is async)
        response = await handler.handle_turn(conversation, message)

        intent_data = {
            "category": IntentCategory.EXECUTION.value,
            "action": "standup_conversation_turn",
            "confidence": 1.0,
            "context": {
                "conversation_id": conversation.id,
                "state": response.state.value,
                "bypassed_classification": True,
                "guided_process": ProcessType.STANDUP.value,
            },
        }

        return ProcessCheckResult.handled_by(
            process_type=ProcessType.STANDUP,
            response_message=response.message,
            intent_data=intent_data,
        )


def register_default_processes() -> None:
    """
    Register the default guided process adapters.

    Called during application startup to register onboarding and
    standup processes with the registry.
    """
    from services.process.registry import get_process_registry

    registry = get_process_registry()

    # Register adapters for existing process managers
    registry.register(OnboardingProcessAdapter())
    registry.register(StandupProcessAdapter())

    logger.info(
        "Registered default guided processes",
        types=[t.value for t in registry.registered_types],
    )

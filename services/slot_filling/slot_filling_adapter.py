"""
ProcessRegistry adapter for slot-filling.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation

Implements GuidedProcess protocol to integrate slot-filling
with the ProcessRegistry (Tier 1 handler per ADR-049).
"""

from typing import Any, Dict, Optional

from services.domain.models import IntentCategory
from services.process.registry import ProcessCheckResult, ProcessType, SuspendedInfo
from services.slot_filling.slot_filling_manager import SlotFillingManager


class SlotFillingProcessAdapter:
    """
    Adapter wrapping SlotFillingManager for ProcessRegistry.

    Implements GuidedProcess protocol by delegating to the
    SlotFillingManager for session management and turn handling.
    """

    def __init__(self, manager: Optional[SlotFillingManager] = None):
        self._manager = manager or SlotFillingManager()

    @property
    def manager(self) -> SlotFillingManager:
        return self._manager

    @property
    def process_type(self) -> ProcessType:
        return ProcessType.SLOT_FILLING

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """Check if there's an active slot-filling session."""
        return self._manager.has_active_session(user_id, session_id)

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """Handle a message in an active slot-filling session."""
        response = await self._manager.handle_turn(user_id, session_id, message)

        if response.is_cancelled:
            # Cancelled — don't intercept further messages
            return ProcessCheckResult.handled_by(
                process_type=ProcessType.SLOT_FILLING,
                response_message=response.message,
                intent_data=self._build_intent_data(response, "slot_filling_cancelled"),
            )

        return ProcessCheckResult.handled_by(
            process_type=ProcessType.SLOT_FILLING,
            response_message=response.message,
            intent_data=self._build_intent_data(response, "slot_filling"),
        )

    async def suspend(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """
        Suspend (cancel) the active slot-filling session.

        Issue #888: Slot-filling sessions are short-lived, so suspend
        simply cancels the session. No resume is offered for slot-filling.
        """
        session = self._manager._find_session(user_id, session_id)
        if session:
            self._manager._cancel_session(session)

    async def has_suspended_session(
        self,
        user_id: Optional[str],
    ) -> Optional[SuspendedInfo]:
        """
        Check if this user has a suspended slot-filling session.

        Slot-filling sessions are not resumable — they are simply
        cancelled on escape. Always returns None.
        """
        return None

    def _build_intent_data(self, response, action: str) -> Dict[str, Any]:
        """Build intent data dict for ProcessCheckResult."""
        return {
            "category": IntentCategory.GUIDANCE.value,
            "action": action,
            "confidence": 1.0,
            "context": {
                "state": response.state.value,
                "bypassed_classification": True,
                "guided_process": ProcessType.SLOT_FILLING.value,
                "template_name": response.template_name,
                "filled_slots": response.filled_slots,
                "is_complete": response.is_complete,
                "is_cancelled": response.is_cancelled,
            },
        }

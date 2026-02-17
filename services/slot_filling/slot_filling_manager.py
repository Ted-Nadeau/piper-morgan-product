"""
Slot-filling state machine manager.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation

Manages multi-turn slot-filling conversations:
- Session storage (in-memory, keyed by session_id)
- State machine: EXTRACTING → PROMPTING → CONFIRMING → COMPLETE/CANCELLED
- Cancel/decline detection
- Slot update detection
"""

import re
from dataclasses import dataclass, field
from typing import Any, Optional

import structlog

from services.shared_types import SlotFillingState
from services.slot_filling.slot_extractor import (
    extract_slots,
    get_missing_required,
    get_next_prompt_group,
    update_slot_state,
)
from services.slot_filling.slot_prompts import (
    format_confirmation_with_prompt,
    format_final_confirmation,
)
from services.slot_filling.slot_template import SlotState, SlotTemplate

logger = structlog.get_logger()

# Patterns for cancel/decline detection (reusable from onboarding)
CANCEL_PATTERNS = [
    r"\b(cancel|never\s?mind|nevermind|forget\s?it|stop|quit|abort)\b",
    r"\bnot?\s?(now|anymore|interested)\b",
    r"\bno\s?thanks\b",
]

# Patterns for confirmation
CONFIRM_PATTERNS = [
    r"\b(yes|yeah|yep|sure|correct|right|looks\s?good|perfect|great|go\s?ahead|do\s?it)\b",
    r"\bthat'?s?\s?(correct|right|good|fine)\b",
    r"\bproceed\b",
]


@dataclass
class SlotFillingResponse:
    """Response from the slot-filling manager."""

    message: str
    state: SlotFillingState
    is_complete: bool = False
    is_cancelled: bool = False
    filled_slots: dict[str, Any] = field(default_factory=dict)
    template_name: str = ""


@dataclass
class SlotFillingSession:
    """In-memory session for an active slot-filling conversation."""

    session_id: str
    user_id: Optional[str]
    template: SlotTemplate
    slot_state: SlotState
    filling_state: SlotFillingState = SlotFillingState.EXTRACTING


class SlotFillingManager:
    """
    Manages slot-filling sessions and state transitions.

    In-memory session storage (same pattern as PortfolioOnboardingManager).
    Sessions are ephemeral — cleared on completion or cancel.
    """

    def __init__(self, llm_service=None):
        self._sessions: dict[str, SlotFillingSession] = {}
        self._llm_service = llm_service

    @property
    def llm_service(self):
        return self._llm_service

    @llm_service.setter
    def llm_service(self, value):
        self._llm_service = value

    def get_session(self, session_id: str) -> Optional[SlotFillingSession]:
        """Get session by session_id."""
        return self._sessions.get(session_id)

    def get_session_by_user(self, user_id: str) -> Optional[SlotFillingSession]:
        """Get active session by user_id."""
        for session in self._sessions.values():
            if session.user_id == user_id:
                return session
        return None

    def has_active_session(self, user_id: Optional[str], session_id: Optional[str]) -> bool:
        """Check if there's an active (non-terminal) slot-filling session."""
        session = self._find_session(user_id, session_id)
        if not session:
            return False
        return session.filling_state not in (
            SlotFillingState.COMPLETE,
            SlotFillingState.CANCELLED,
        )

    async def start_filling(
        self,
        user_id: Optional[str],
        session_id: str,
        template: SlotTemplate,
        initial_message: str,
    ) -> SlotFillingResponse:
        """
        Start a new slot-filling session.

        Extracts slots from the initial message and determines next step.
        """
        slot_state = SlotState(template=template)
        session = SlotFillingSession(
            session_id=session_id,
            user_id=user_id,
            template=template,
            slot_state=slot_state,
            filling_state=SlotFillingState.EXTRACTING,
        )
        self._sessions[session_id] = session

        logger.info(
            "slot_filling_started",
            session_id=session_id,
            template=template.name,
        )

        # Extract slots from initial message
        extracted = {}
        if self._llm_service and initial_message.strip():
            extracted = await extract_slots(initial_message, template, self._llm_service)
            update_slot_state(slot_state, extracted)

        return self._determine_next_step(session)

    async def handle_turn(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> SlotFillingResponse:
        """
        Handle a turn in an active slot-filling session.

        Processes the message based on current state.
        """
        session = self._find_session(user_id, session_id)
        if not session:
            return SlotFillingResponse(
                message="I lost track of what we were setting up. Could you start again?",
                state=SlotFillingState.CANCELLED,
                is_cancelled=True,
            )

        message_lower = message.lower().strip()

        # Cancel detection (any state)
        if _matches_patterns(message_lower, CANCEL_PATTERNS):
            return self._cancel_session(session)

        # Route based on state
        if session.filling_state == SlotFillingState.EXTRACTING:
            return await self._handle_extracting(session, message)
        elif session.filling_state == SlotFillingState.PROMPTING:
            return await self._handle_prompting(session, message)
        elif session.filling_state == SlotFillingState.CONFIRMING:
            return self._handle_confirming(session, message)
        else:
            # Terminal state
            return SlotFillingResponse(
                message="This slot-filling session has already ended.",
                state=session.filling_state,
                is_complete=session.filling_state == SlotFillingState.COMPLETE,
                is_cancelled=session.filling_state == SlotFillingState.CANCELLED,
            )

    async def _handle_extracting(
        self, session: SlotFillingSession, message: str
    ) -> SlotFillingResponse:
        """Handle message in EXTRACTING state."""
        extracted = {}
        if self._llm_service:
            extracted = await extract_slots(
                message,
                session.template,
                self._llm_service,
                existing_values=session.slot_state.filled_slots,
            )
            update_slot_state(session.slot_state, extracted)

        return self._determine_next_step(session)

    async def _handle_prompting(
        self, session: SlotFillingSession, message: str
    ) -> SlotFillingResponse:
        """Handle message in PROMPTING state (collecting missing slots)."""
        # Extract new slots from response
        extracted = {}
        if self._llm_service:
            extracted = await extract_slots(
                message,
                session.template,
                self._llm_service,
                existing_values=session.slot_state.filled_slots,
            )
            update_slot_state(session.slot_state, extracted)

        return self._determine_next_step(session)

    def _handle_confirming(self, session: SlotFillingSession, message: str) -> SlotFillingResponse:
        """Handle message in CONFIRMING state."""
        message_lower = message.lower().strip()

        if _matches_patterns(message_lower, CONFIRM_PATTERNS):
            return self._complete_session(session)

        # User might be updating a slot during confirmation
        # For now, re-prompt for confirmation
        msg = format_final_confirmation(session.slot_state)
        return SlotFillingResponse(
            message=msg,
            state=SlotFillingState.CONFIRMING,
            filled_slots=dict(session.slot_state.filled_slots),
            template_name=session.template.name,
        )

    def _determine_next_step(self, session: SlotFillingSession) -> SlotFillingResponse:
        """Determine the next state and response based on current slot state."""
        missing = get_missing_required(session.slot_state)

        if not missing:
            # All required slots filled → confirm
            session.filling_state = SlotFillingState.CONFIRMING
            msg = format_final_confirmation(session.slot_state)
            return SlotFillingResponse(
                message=msg,
                state=SlotFillingState.CONFIRMING,
                filled_slots=dict(session.slot_state.filled_slots),
                template_name=session.template.name,
            )

        # Still have missing required slots → prompt
        session.filling_state = SlotFillingState.PROMPTING
        next_group = get_next_prompt_group(session.slot_state)
        msg = format_confirmation_with_prompt(session.slot_state, next_group)

        return SlotFillingResponse(
            message=msg,
            state=SlotFillingState.PROMPTING,
            filled_slots=dict(session.slot_state.filled_slots),
            template_name=session.template.name,
        )

    def _cancel_session(self, session: SlotFillingSession) -> SlotFillingResponse:
        """Cancel a slot-filling session."""
        session.filling_state = SlotFillingState.CANCELLED
        session.slot_state.clear_all()
        # Clean up session
        self._sessions.pop(session.session_id, None)

        logger.info("slot_filling_cancelled", session_id=session.session_id)

        return SlotFillingResponse(
            message="No problem, cancelled.",
            state=SlotFillingState.CANCELLED,
            is_cancelled=True,
            template_name=session.template.name,
        )

    def _complete_session(self, session: SlotFillingSession) -> SlotFillingResponse:
        """Complete a slot-filling session."""
        session.filling_state = SlotFillingState.COMPLETE
        filled = dict(session.slot_state.filled_slots)
        template_name = session.template.name

        # Clean up session
        self._sessions.pop(session.session_id, None)

        logger.info(
            "slot_filling_complete",
            session_id=session.session_id,
            template=template_name,
            slots_filled=len(filled),
        )

        return SlotFillingResponse(
            message="Done!",
            state=SlotFillingState.COMPLETE,
            is_complete=True,
            filled_slots=filled,
            template_name=template_name,
        )

    def _find_session(
        self, user_id: Optional[str], session_id: Optional[str]
    ) -> Optional[SlotFillingSession]:
        """Find session by user_id (preferred) or session_id (fallback)."""
        session = None
        if user_id:
            session = self.get_session_by_user(user_id)
        if not session and session_id:
            session = self.get_session(session_id)
        return session


def _matches_patterns(text: str, patterns: list[str]) -> bool:
    """Check if text matches any of the given regex patterns."""
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

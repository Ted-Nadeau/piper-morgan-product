"""
Tests for SlotFillingManager state machine.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Phase 3: SlotFillingManager + ProcessRegistry Integration

Tests cover:
- Full happy path (all slots in first message)
- Partial path (2+ turns)
- Cancel mid-flow
- Slot update mid-flow
- Session isolation
- State transitions
"""

from unittest.mock import AsyncMock

import pytest

from services.shared_types import SlotFillingState
from services.slot_filling.slot_filling_manager import SlotFillingManager
from services.slot_filling.slot_template import MEETING_TEMPLATE


@pytest.fixture
def mock_llm():
    """Mock LLM service."""
    llm = AsyncMock()
    llm.complete = AsyncMock(return_value="{}")
    return llm


@pytest.fixture
def manager(mock_llm):
    """SlotFillingManager with mock LLM."""
    return SlotFillingManager(llm_service=mock_llm)


class TestStartFilling:
    @pytest.mark.asyncio
    async def test_full_extraction_on_start(self, manager, mock_llm):
        """All slots extracted from initial message → CONFIRMING."""
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3 planning"}'
        )
        response = await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Set up a meeting with Sarah Tuesday at 2pm about Q3 planning",
        )
        assert response.state == SlotFillingState.CONFIRMING
        assert response.filled_slots["attendee"] == "Sarah"
        assert response.filled_slots["topic"] == "Q3 planning"
        assert not response.is_complete  # Not yet confirmed

    @pytest.mark.asyncio
    async def test_partial_extraction_on_start(self, manager, mock_llm):
        """Some slots extracted → PROMPTING for rest."""
        mock_llm.complete.return_value = '{"attendee": "Sarah"}'
        response = await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule something with Sarah",
        )
        assert response.state == SlotFillingState.PROMPTING
        assert response.filled_slots["attendee"] == "Sarah"
        assert "Sarah" in response.message  # Confirmation of what we have

    @pytest.mark.asyncio
    async def test_no_extraction_on_start(self, manager, mock_llm):
        """No slots extracted → PROMPTING for all."""
        mock_llm.complete.return_value = "{}"
        response = await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )
        assert response.state == SlotFillingState.PROMPTING
        assert len(response.filled_slots) == 0

    @pytest.mark.asyncio
    async def test_session_created(self, manager, mock_llm):
        """Session is stored after start_filling."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )
        assert manager.has_active_session("user1", "sess1")

    @pytest.mark.asyncio
    async def test_no_llm_service(self):
        """Manager works without LLM (no extraction, just prompting)."""
        manager = SlotFillingManager(llm_service=None)
        response = await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah Tuesday at 2pm",
        )
        # Without LLM, can't extract → prompts for everything
        assert response.state == SlotFillingState.PROMPTING
        assert len(response.filled_slots) == 0


class TestHandleTurn:
    @pytest.mark.asyncio
    async def test_two_turn_flow(self, manager, mock_llm):
        """Partial start → fill remaining → CONFIRMING."""
        # Turn 1: partial extraction
        mock_llm.complete.return_value = '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm"}'
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah Tuesday at 2pm",
        )

        # Turn 2: fill remaining
        mock_llm.complete.return_value = '{"topic": "Q3 planning"}'
        response = await manager.handle_turn("user1", "sess1", "Q3 planning")
        assert response.state == SlotFillingState.CONFIRMING
        assert response.filled_slots["topic"] == "Q3 planning"
        assert response.filled_slots["attendee"] == "Sarah"

    @pytest.mark.asyncio
    async def test_three_turn_flow(self, manager, mock_llm):
        """Minimal start → partial fill → complete fill → CONFIRMING."""
        # Turn 1: no slots
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )

        # Turn 2: some slots
        mock_llm.complete.return_value = '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm"}'
        response2 = await manager.handle_turn("user1", "sess1", "Sarah and Jake, Tuesday at 2pm")
        assert response2.state == SlotFillingState.PROMPTING

        # Turn 3: remaining slot
        mock_llm.complete.return_value = '{"topic": "Sprint review"}'
        response3 = await manager.handle_turn("user1", "sess1", "Sprint review")
        assert response3.state == SlotFillingState.CONFIRMING

    @pytest.mark.asyncio
    async def test_confirmation_yes(self, manager, mock_llm):
        """User confirms → COMPLETE."""
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3"}'
        )
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah Tuesday at 2pm about Q3",
        )

        response = await manager.handle_turn("user1", "sess1", "Yes")
        assert response.state == SlotFillingState.COMPLETE
        assert response.is_complete
        assert response.filled_slots["attendee"] == "Sarah"

    @pytest.mark.asyncio
    async def test_confirmation_reask(self, manager, mock_llm):
        """Unclear response during CONFIRMING → re-prompt."""
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3"}'
        )
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah Tuesday at 2pm about Q3",
        )

        response = await manager.handle_turn("user1", "sess1", "Hmm, let me think")
        assert response.state == SlotFillingState.CONFIRMING
        assert not response.is_complete


class TestCancelFlow:
    @pytest.mark.asyncio
    async def test_cancel_during_prompting(self, manager, mock_llm):
        """Cancel during PROMPTING → CANCELLED."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )

        response = await manager.handle_turn("user1", "sess1", "Never mind")
        assert response.state == SlotFillingState.CANCELLED
        assert response.is_cancelled
        assert not manager.has_active_session("user1", "sess1")

    @pytest.mark.asyncio
    async def test_cancel_during_confirming(self, manager, mock_llm):
        """Cancel during CONFIRMING → CANCELLED."""
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3"}'
        )
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah Tuesday at 2pm about Q3",
        )

        response = await manager.handle_turn("user1", "sess1", "cancel")
        assert response.state == SlotFillingState.CANCELLED
        assert response.is_cancelled

    @pytest.mark.asyncio
    async def test_cancel_clears_session(self, manager, mock_llm):
        """Cancel removes session from manager."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )
        assert manager.has_active_session("user1", "sess1")

        await manager.handle_turn("user1", "sess1", "forget it")
        assert not manager.has_active_session("user1", "sess1")


class TestSlotUpdate:
    @pytest.mark.asyncio
    async def test_slot_update_during_prompting(self, manager, mock_llm):
        """Slot update mid-flow replaces old value."""
        # Start with time=3pm
        mock_llm.complete.return_value = '{"attendee": "Sarah", "day": "Tuesday", "time": "3pm"}'
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah Tuesday at 3pm",
        )

        # Update time to 4pm
        mock_llm.complete.return_value = '{"time": "4pm"}'
        response = await manager.handle_turn("user1", "sess1", "Actually make it 4pm")
        assert response.filled_slots["time"] == "4pm"
        assert response.filled_slots["attendee"] == "Sarah"  # Preserved


class TestSessionIsolation:
    @pytest.mark.asyncio
    async def test_two_users_independent(self, manager, mock_llm):
        """Two users have independent sessions."""
        mock_llm.complete.return_value = '{"attendee": "Sarah"}'
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah",
        )

        mock_llm.complete.return_value = '{"attendee": "Jake"}'
        await manager.start_filling(
            user_id="user2",
            session_id="sess2",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Jake",
        )

        sess1 = manager.get_session("sess1")
        sess2 = manager.get_session("sess2")
        assert sess1.slot_state.get_value("attendee") == "Sarah"
        assert sess2.slot_state.get_value("attendee") == "Jake"

    @pytest.mark.asyncio
    async def test_session_not_found(self, manager):
        """Handle turn for nonexistent session returns cancelled."""
        response = await manager.handle_turn("nobody", "nosess", "Hello")
        assert response.is_cancelled

    @pytest.mark.asyncio
    async def test_completed_session_cleaned_up(self, manager, mock_llm):
        """Completed session is removed from storage."""
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3"}'
        )
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah Tuesday at 2pm about Q3",
        )

        await manager.handle_turn("user1", "sess1", "Yes")
        assert not manager.has_active_session("user1", "sess1")


class TestHasActiveSession:
    @pytest.mark.asyncio
    async def test_no_session(self, manager):
        assert not manager.has_active_session("user1", "sess1")

    @pytest.mark.asyncio
    async def test_active_session_by_user(self, manager, mock_llm):
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting",
        )
        assert manager.has_active_session("user1", None)

    @pytest.mark.asyncio
    async def test_active_session_by_session_id(self, manager, mock_llm):
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Meeting",
        )
        assert manager.has_active_session(None, "sess1")

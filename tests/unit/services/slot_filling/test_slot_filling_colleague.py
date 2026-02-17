"""
Colleague Test for slot-filling framework.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Phase 4: Colleague Test + Regression

The Colleague Test: "Would a competent colleague respond this way?"

Tests verify the system behaves like a helpful human colleague, not a robot:
- Scenario 1: All slots in one message → immediate confirmation
- Scenario 2: Partial slots → prompt only for missing
- Scenario 3: Slot update → accept change, re-confirm
- Scenario 4: Cancel mid-flow → graceful exit
- Scenario 5: Empty first message → grouped prompt for essentials
- Scenario 6: Two-slot message → one follow-up for remaining
"""

from unittest.mock import AsyncMock

import pytest

from services.shared_types import SlotFillingState
from services.slot_filling.slot_filling_manager import SlotFillingManager
from services.slot_filling.slot_template import MEETING_TEMPLATE


@pytest.fixture
def mock_llm():
    llm = AsyncMock()
    llm.complete = AsyncMock(return_value="{}")
    return llm


@pytest.fixture
def manager(mock_llm):
    return SlotFillingManager(llm_service=mock_llm)


class TestColleagueScenarios:
    """
    Each scenario simulates a realistic user conversation.
    The key question: would a competent colleague respond this way?
    """

    @pytest.mark.asyncio
    async def test_scenario_1_all_slots_one_message(self, manager, mock_llm):
        """
        User: "Set up a meeting with Sarah Tuesday at 2pm about Q3 planning"
        Colleague: "Done — Sarah, Tuesday, 2pm, Q3 planning. Want me to proceed?"

        NOT: "What's the meeting about?" (already said!)
        NOT: "When should it be?" (already said!)
        """
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3 planning"}'
        )
        response = await manager.start_filling(
            user_id="user1",
            session_id="s1",
            template=MEETING_TEMPLATE,
            initial_message="Set up a meeting with Sarah Tuesday at 2pm about Q3 planning",
        )

        # Should go straight to confirmation — no extra questions
        assert response.state == SlotFillingState.CONFIRMING
        assert "Sarah" in response.message
        assert "Q3 planning" in response.message or "Q3" in response.message
        # Should NOT be asking for more info
        assert "What's" not in response.message

    @pytest.mark.asyncio
    async def test_scenario_2_partial_slots_prompt_missing_only(self, manager, mock_llm):
        """
        User: "Set up a meeting with Sarah Tuesday at 2pm"
        Colleague: "Got it — Sarah, Tuesday, 2pm. What's the topic?"

        NOT: "Who should attend?" (already said Sarah!)
        NOT: "When should it be?" (already said Tuesday at 2pm!)
        """
        mock_llm.complete.return_value = '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm"}'
        response = await manager.start_filling(
            user_id="user1",
            session_id="s2",
            template=MEETING_TEMPLATE,
            initial_message="Set up a meeting with Sarah Tuesday at 2pm",
        )

        assert response.state == SlotFillingState.PROMPTING
        # Should confirm what we have
        assert "Sarah" in response.message
        # Should ask for what's missing (topic)
        assert "topic" in response.message.lower()
        # Should NOT re-ask for provided info
        assert response.filled_slots["attendee"] == "Sarah"
        assert response.filled_slots["day"] == "Tuesday"
        assert response.filled_slots["time"] == "2pm"

    @pytest.mark.asyncio
    async def test_scenario_3_slot_update_accepted(self, manager, mock_llm):
        """
        User: "Meeting with Sarah at 3pm"
        Colleague: "Got it — Sarah, 3pm. What day and topic?"
        User: "Actually make it 4pm"
        Colleague: "Updated to 4pm. What day and topic?"

        NOT: "I already have a time" (should accept the update!)
        """
        # Turn 1: initial info
        mock_llm.complete.return_value = '{"attendee": "Sarah", "time": "3pm"}'
        await manager.start_filling(
            user_id="user1",
            session_id="s3",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah at 3pm",
        )

        # Turn 2: slot update
        mock_llm.complete.return_value = '{"time": "4pm"}'
        response = await manager.handle_turn("user1", "s3", "Actually make it 4pm")

        # Should accept the update
        assert response.filled_slots["time"] == "4pm"
        # Should preserve other slots
        assert response.filled_slots["attendee"] == "Sarah"

    @pytest.mark.asyncio
    async def test_scenario_4_cancel_graceful(self, manager, mock_llm):
        """
        User: "Schedule a meeting"
        Colleague: "Sure! Who should attend, and when works?"
        User: "Never mind"
        Colleague: "No problem, cancelled."

        NOT: "Are you sure?" (respect the decision!)
        NOT: silence (acknowledge the cancel!)
        """
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="s4",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )

        response = await manager.handle_turn("user1", "s4", "Never mind")
        assert response.state == SlotFillingState.CANCELLED
        assert response.is_cancelled
        # Should acknowledge gracefully
        assert response.message  # Not empty
        # Session should be cleaned up
        assert not manager.has_active_session("user1", "s4")

    @pytest.mark.asyncio
    async def test_scenario_5_empty_first_message_grouped_prompt(self, manager, mock_llm):
        """
        User: "Schedule a meeting"
        Colleague: "Sure! Who should attend, what day, and what time?"

        NOT: "What's the attendee?" then "What's the day?" then "What's the time?"
        (That's interrogation! Group related questions.)
        """
        mock_llm.complete.return_value = "{}"
        response = await manager.start_filling(
            user_id="user1",
            session_id="s5",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )

        assert response.state == SlotFillingState.PROMPTING
        # Should prompt for multiple related slots at once (grouped)
        msg_lower = response.message.lower()
        # Group 0 has attendee, day, time — should mention multiple
        # (The exact wording depends on formatting, but shouldn't be a single slot)
        has_multi = sum(
            [
                "attend" in msg_lower or "who" in msg_lower,
                "day" in msg_lower or "when" in msg_lower,
                "time" in msg_lower,
            ]
        )
        assert has_multi >= 2, f"Expected grouped prompt, got: {response.message}"

    @pytest.mark.asyncio
    async def test_scenario_6_two_slot_message_one_followup(self, manager, mock_llm):
        """
        User: "Meeting with Sarah and Jake"
        Colleague: "Got it — Sarah and Jake. What day, what time?"
        User: "Thursday morning"
        Colleague: "Got it — Thursday, morning. What's the topic?"

        NOT: 4 separate follow-up questions (one per missing slot)
        """
        # Turn 1: attendee only
        mock_llm.complete.return_value = '{"attendee": "Sarah and Jake"}'
        resp1 = await manager.start_filling(
            user_id="user1",
            session_id="s6",
            template=MEETING_TEMPLATE,
            initial_message="Meeting with Sarah and Jake",
        )
        assert resp1.state == SlotFillingState.PROMPTING
        assert resp1.filled_slots["attendee"] == "Sarah and Jake"

        # Turn 2: day + time
        mock_llm.complete.return_value = '{"day": "Thursday", "time": "morning"}'
        resp2 = await manager.handle_turn("user1", "s6", "Thursday morning")

        # Should need just one more: topic
        assert resp2.state == SlotFillingState.PROMPTING
        assert "topic" in resp2.message.lower()
        assert resp2.filled_slots["day"] == "Thursday"
        assert resp2.filled_slots["time"] == "morning"

        # Turn 3: final slot
        mock_llm.complete.return_value = '{"topic": "Sprint review"}'
        resp3 = await manager.handle_turn("user1", "s6", "Sprint review")
        assert resp3.state == SlotFillingState.CONFIRMING
        assert resp3.filled_slots["topic"] == "Sprint review"

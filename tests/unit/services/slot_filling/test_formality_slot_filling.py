"""
Tests for formality-aware slot-filling messages.

Issue #838: Make SlotFillingManager formality-aware.

Tests cover:
- _slot_message helper with warm/balanced/professional baselines
- _slot_message default (None) returns balanced text
- start_filling passes formality_baseline through to session
- Cancel messages vary by formality
- Complete messages vary by formality
"""

from unittest.mock import AsyncMock

import pytest

from services.shared_types import SlotFillingState
from services.slot_filling.slot_filling_manager import SlotFillingManager, _slot_message
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


class TestSlotMessageHelper:
    """Tests for _slot_message formality helper."""

    def test_warm_baseline_returns_warm_text(self):
        """Warm formality (>=0.67) returns warm variant."""
        msg = _slot_message("cancelled", formality_baseline=0.8)
        assert msg == "No problem at all, cancelled! Let me know if you need anything else."

    def test_professional_baseline_returns_professional_text(self):
        """Professional formality (<0.33) returns professional variant."""
        msg = _slot_message("cancelled", formality_baseline=0.1)
        assert msg == "Cancelled."

    def test_none_baseline_returns_balanced_text(self):
        """None formality (default) returns balanced variant."""
        msg = _slot_message("cancelled", formality_baseline=None)
        assert msg == "No problem, cancelled."

    def test_balanced_baseline_returns_balanced_text(self):
        """Mid-range formality (0.33-0.67) returns balanced variant."""
        msg = _slot_message("cancelled", formality_baseline=0.5)
        assert msg == "No problem, cancelled."

    def test_session_expired_warm(self):
        """Session expired message in warm tone."""
        msg = _slot_message("session_expired", formality_baseline=0.9)
        assert "still here to help" in msg

    def test_session_expired_professional(self):
        """Session expired message in professional tone."""
        msg = _slot_message("session_expired", formality_baseline=0.1)
        assert msg == "Session expired. Please restart the setup."

    def test_session_expired_balanced(self):
        """Session expired message matches original hardcoded text."""
        msg = _slot_message("session_expired", formality_baseline=None)
        assert msg == "I lost track of what we were setting up. Could you start again?"

    def test_session_ended_warm(self):
        """Session ended message in warm tone."""
        msg = _slot_message("session_ended", formality_baseline=0.8)
        assert "wrapped up" in msg

    def test_session_ended_professional(self):
        """Session ended message in professional tone."""
        msg = _slot_message("session_ended", formality_baseline=0.1)
        assert msg == "Session completed. Start a new one if needed."

    def test_done_warm(self):
        """Done message in warm tone."""
        msg = _slot_message("done", formality_baseline=0.8)
        assert "All done" in msg

    def test_done_professional(self):
        """Done message in professional tone."""
        msg = _slot_message("done", formality_baseline=0.1)
        assert msg == "Complete."

    def test_done_balanced_matches_original(self):
        """Done balanced message matches original hardcoded text."""
        msg = _slot_message("done", formality_baseline=None)
        assert msg == "Done!"


class TestFormalityPassthrough:
    """Tests that formality_baseline is stored on session and flows through."""

    @pytest.mark.asyncio
    async def test_start_filling_stores_formality_on_session(self, manager, mock_llm):
        """start_filling stores formality_baseline on the session."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
            formality_baseline=0.8,
        )

        session = manager.get_session("sess1")
        assert session is not None
        assert session.formality_baseline == 0.8

    @pytest.mark.asyncio
    async def test_start_filling_default_formality_is_none(self, manager, mock_llm):
        """start_filling without formality_baseline defaults to None."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )

        session = manager.get_session("sess1")
        assert session is not None
        assert session.formality_baseline is None


class TestCancelFormality:
    """Tests that cancel messages vary by formality."""

    @pytest.mark.asyncio
    async def test_cancel_warm_message(self, manager, mock_llm):
        """Cancel with warm formality returns warm message."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
            formality_baseline=0.8,
        )

        response = await manager.handle_turn("user1", "sess1", "Never mind")
        assert response.is_cancelled
        assert "Let me know if you need anything else" in response.message

    @pytest.mark.asyncio
    async def test_cancel_professional_message(self, manager, mock_llm):
        """Cancel with professional formality returns terse message."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
            formality_baseline=0.1,
        )

        response = await manager.handle_turn("user1", "sess1", "cancel")
        assert response.is_cancelled
        assert response.message == "Cancelled."

    @pytest.mark.asyncio
    async def test_cancel_default_message_unchanged(self, manager, mock_llm):
        """Cancel without formality returns original balanced message."""
        mock_llm.complete.return_value = "{}"
        await manager.start_filling(
            user_id="user1",
            session_id="sess1",
            template=MEETING_TEMPLATE,
            initial_message="Schedule a meeting",
        )

        response = await manager.handle_turn("user1", "sess1", "Never mind")
        assert response.is_cancelled
        assert response.message == "No problem, cancelled."

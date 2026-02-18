"""
Tests for soft offer accept/decline cycle.

Issue #824: Close the offer accept/decline loop — detect_offer_response
is now called when a pending offer exists, routing to acceptance or
decline handling before normal intent classification.

Tests verify:
- Accepting a pending offer returns workflow start message
- Declining a pending offer returns graceful acknowledgment
- Non-accept/decline message with pending offer continues normal processing
- No pending offer → normal processing (no interference)
- Pending offer clears after any response (accept, decline, or ignore)
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.shared_types import IntentCategory


def _make_intent(category: IntentCategory, action: str) -> Intent:
    return Intent(category=category, action=action, confidence=1.0)


@pytest.fixture
def mock_engine():
    return MagicMock()


@pytest.fixture
def mock_classifier():
    classifier = MagicMock()
    classifier.classify_multiple = AsyncMock()
    classifier.classify = AsyncMock()
    return classifier


@pytest.fixture
def mock_canonical_handlers():
    handlers = MagicMock()
    handlers.can_handle = MagicMock(return_value=True)
    handlers.handle = AsyncMock(
        return_value={
            "message": "Default response.",
            "intent": {"category": "query", "action": "test"},
            "requires_clarification": False,
        }
    )
    return handlers


@pytest.fixture
def intent_service(mock_engine, mock_classifier, mock_canonical_handlers):
    service = IntentService(
        orchestration_engine=mock_engine,
        intent_classifier=mock_classifier,
    )
    service.canonical_handlers = mock_canonical_handlers
    service.intent_orchestrator = IntentOrchestrator(canonical_handlers=mock_canonical_handlers)
    return service


class TestOfferAcceptance:
    """User accepts a pending soft offer."""

    @pytest.mark.asyncio
    async def test_yes_accepts_meeting_offer(self, intent_service, mock_classifier):
        """'Yes please' with pending meeting offer → acceptance message."""
        # Simulate a pending offer from previous turn
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_accept",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "decline_message": "No worries, just let me know if you change your mind.",
            },
        )

        result = await intent_service.process_intent(
            message="Yes please",
            session_id="sess_accept",
            user_id=None,
        )

        assert result.success
        assert "set that up" in result.message.lower() or "help" in result.message.lower()
        assert result.intent_data["category"] == "soft_offer_accepted"
        assert result.intent_data["action"] == "meeting"

    @pytest.mark.asyncio
    async def test_sure_accepts_status_offer(self, intent_service, mock_classifier):
        """'Sure!' with pending status offer → acceptance message."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_accept2",
            {
                "workflow_type": "status_check",
                "offer_message": "Want me to pull up the status?",
                "decline_message": "No worries.",
            },
        )

        result = await intent_service.process_intent(
            message="Sure!",
            session_id="sess_accept2",
            user_id=None,
        )

        assert result.success
        assert result.intent_data["category"] == "soft_offer_accepted"
        assert result.intent_data["action"] == "status_check"

    @pytest.mark.asyncio
    async def test_go_ahead_accepts(self, intent_service, mock_classifier):
        """'Go ahead' with pending offer → acceptance."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_go",
            {
                "workflow_type": "priority_check",
                "offer_message": "Want me to check priorities?",
                "decline_message": "No worries.",
            },
        )

        result = await intent_service.process_intent(
            message="Go ahead",
            session_id="sess_go",
            user_id=None,
        )

        assert result.success
        assert result.intent_data["category"] == "soft_offer_accepted"

    @pytest.mark.asyncio
    async def test_classifier_not_called_on_accept(self, intent_service, mock_classifier):
        """Accepting an offer should NOT trigger classification."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_no_classify",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        await intent_service.process_intent(
            message="Yes",
            session_id="sess_no_classify",
            user_id=None,
        )

        # Classifier should never be called
        mock_classifier.classify_multiple.assert_not_awaited()


class TestOfferDecline:
    """User declines a pending soft offer."""

    @pytest.mark.asyncio
    async def test_no_thanks_declines(self, intent_service, mock_classifier):
        """'No thanks' with pending offer → decline message."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_decline",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries, just let me know if you change your mind.",
            },
        )

        result = await intent_service.process_intent(
            message="No thanks",
            session_id="sess_decline",
            user_id=None,
        )

        assert result.success
        assert "no worries" in result.message.lower()
        assert result.intent_data["category"] == "soft_offer_declined"

    @pytest.mark.asyncio
    async def test_not_now_declines(self, intent_service, mock_classifier):
        """'Not now' with pending offer → decline."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_later",
            {
                "workflow_type": "status_check",
                "offer_message": "Want me to check?",
                "decline_message": "No problem, I'll be here if you need me.",
            },
        )

        result = await intent_service.process_intent(
            message="Not now",
            session_id="sess_later",
            user_id=None,
        )

        assert result.success
        assert result.intent_data["category"] == "soft_offer_declined"

    @pytest.mark.asyncio
    async def test_classifier_not_called_on_decline(self, intent_service, mock_classifier):
        """Declining an offer should NOT trigger classification."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_no_classify2",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        await intent_service.process_intent(
            message="Maybe later",
            session_id="sess_no_classify2",
            user_id=None,
        )

        mock_classifier.classify_multiple.assert_not_awaited()


class TestOfferIgnored:
    """User says something unrelated to the pending offer."""

    @pytest.mark.asyncio
    async def test_new_topic_continues_normally(self, intent_service, mock_classifier):
        """New topic with pending offer → normal processing, offer cleared."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_ignore",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        intent = _make_intent(IntentCategory.STATUS, "get_project_status")
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="What's the project status?",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Your project is on track.",
            "intent": {"category": "status", "action": "get_project_status"},
        }

        result = await intent_service.process_intent(
            message="What's the project status?",
            session_id="sess_ignore",
            user_id=None,
        )

        # Should proceed with normal processing
        assert result.success
        assert "project" in result.message.lower()
        # Classifier WAS called (normal flow)
        mock_classifier.classify_multiple.assert_awaited_once()


class TestNoPendingOffer:
    """No pending offer → normal processing unaffected."""

    @pytest.mark.asyncio
    async def test_yes_without_pending_offer_is_normal(self, intent_service, mock_classifier):
        """'Yes' without a pending offer → normal classification."""
        intent = _make_intent(IntentCategory.CONVERSATION, "affirmation")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Yes",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Great!",
            "intent": {"category": "conversation", "action": "affirmation"},
        }

        result = await intent_service.process_intent(
            message="Yes",
            session_id="sess_no_offer",
            user_id=None,
        )

        # Normal processing — classifier was called
        assert result.success
        mock_classifier.classify_multiple.assert_awaited_once()


class TestPendingOfferClearing:
    """Pending offer clears after any response type."""

    @pytest.mark.asyncio
    async def test_offer_clears_after_accept(self, intent_service, mock_classifier):
        """After acceptance, no pending offer remains."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_clear",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        await intent_service.process_intent(
            message="Yes",
            session_id="sess_clear",
            user_id=None,
        )

        # Offer should be cleared
        assert (
            intent_service.workflow_offer_service.get_and_clear_pending_offer("sess_clear") is None
        )

    @pytest.mark.asyncio
    async def test_offer_clears_after_ignore(self, intent_service, mock_classifier):
        """After ignoring, no pending offer remains."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_clear2",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        intent = _make_intent(IntentCategory.STATUS, "get_project_status")
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Check status",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Status report.",
            "intent": {"category": "status", "action": "get_project_status"},
        }

        await intent_service.process_intent(
            message="Check status",
            session_id="sess_clear2",
            user_id=None,
        )

        # Offer should be cleared (get_and_clear was already called)
        assert (
            intent_service.workflow_offer_service.get_and_clear_pending_offer("sess_clear2") is None
        )

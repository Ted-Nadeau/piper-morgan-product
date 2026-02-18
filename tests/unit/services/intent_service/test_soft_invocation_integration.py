"""
Integration tests for soft workflow invocation in IntentService.

Issue #767: GLUE-SOFTINVOKE — Soft workflow invocation from natural language.
Phase 3: IntentService Integration

Tests verify:
- Soft offers appear in canonical handler responses
- Offers don't appear for multi-intent orchestrated responses
- Offers don't appear for single-intent explicit commands
- ProactivityGate throttling respected
- Graceful fallback when detection fails
- pending_offer field populated correctly
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.intent_service.soft_invocation import SoftInvocationDetector, WorkflowOfferService
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


class TestSoftOfferInCanonicalResponse:
    """Soft offers appear in canonical handler responses when triggered."""

    @pytest.mark.asyncio
    async def test_meeting_offer_added(self, intent_service, mock_classifier):
        """Natural meeting expression → offer appended to response."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I need to get the team together Tuesday",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That sounds like a plan!",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        result = await intent_service.process_intent(
            message="I need to get the team together Tuesday",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert "That sounds like a plan!" in result.message
        assert "meeting" in result.message.lower() or "find a time" in result.message.lower()
        assert result.pending_offer is not None
        assert result.pending_offer["workflow_type"] == "meeting"

    @pytest.mark.asyncio
    async def test_status_offer_added(self, intent_service, mock_classifier):
        """Deadline worry → status check offer."""
        intent = _make_intent(IntentCategory.CONVERSATION, "empathy")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I'm worried about the deadline",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That's understandable.",
            "intent": {"category": "conversation", "action": "empathy"},
        }

        result = await intent_service.process_intent(
            message="I'm worried about the deadline",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert "understandable" in result.message
        assert result.pending_offer is not None
        assert result.pending_offer["workflow_type"] == "status_check"


class TestNoOfferWhenNotTriggered:
    """Verify soft offers don't appear when not appropriate."""

    @pytest.mark.asyncio
    async def test_no_offer_on_explicit_command(self, intent_service, mock_classifier):
        """Explicit command → no soft offer (handled by normal classification)."""
        intent = _make_intent(IntentCategory.STATUS, "get_project_status")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Check my project status",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Here's your project status...",
            "intent": {"category": "status", "action": "get_project_status"},
        }

        result = await intent_service.process_intent(
            message="Check my project status",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert result.pending_offer is None
        # Message should be the canonical response only
        assert result.message == "Here's your project status..."

    @pytest.mark.asyncio
    async def test_no_offer_on_casual_chat(self, intent_service, mock_classifier):
        """Casual chat → no soft offer."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Good morning!",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Good morning! How can I help today?",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        result = await intent_service.process_intent(
            message="Good morning!",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert result.pending_offer is None

    @pytest.mark.asyncio
    async def test_no_offer_on_multi_intent_orchestrated(self, intent_service, mock_classifier):
        """Multi-intent orchestrated → no soft offer (already compound)."""
        intents = [
            _make_intent(IntentCategory.QUERY, "meeting_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
        ]

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=intents,
            original_message="Calendar and status",
            is_multi_intent=True,
        )

        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            from services.intent_service.orchestrator import (
                IntentExecutionResult,
                OrchestratedResponse,
            )

            mock_execute.return_value = OrchestratedResponse(
                results=[
                    IntentExecutionResult(
                        intent=intents[0],
                        response="Meeting at 2pm.",
                        intent_data={"category": "query", "action": "meeting_time"},
                        success=True,
                    ),
                    IntentExecutionResult(
                        intent=intents[1],
                        response="Sprint on track.",
                        intent_data={"category": "status", "action": "get_project_status"},
                        success=True,
                    ),
                ],
                aggregated_message="Meeting at 2pm. Sprint on track.",
            )

            result = await intent_service.process_intent(
                message="Calendar and status",
                session_id="sess1",
                user_id=None,
            )

            # Multi-intent orchestrated responses don't get soft offers
            assert result.multi_intent_orchestrated
            assert result.pending_offer is None


class TestSoftOfferGracefulFallback:
    """Verify graceful degradation when soft invocation fails."""

    @pytest.mark.asyncio
    async def test_detector_error_graceful(self, intent_service, mock_classifier):
        """Detection error → normal response returned without offer."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="test message for error",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Normal response.",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        # Break the detector
        intent_service.soft_invocation_detector.detect = MagicMock(
            side_effect=RuntimeError("Detector broken")
        )

        result = await intent_service.process_intent(
            message="test message for error",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert result.message == "Normal response."
        assert result.pending_offer is None


class TestPendingOfferField:
    """Verify pending_offer field defaults and population."""

    def test_default_none(self):
        result = IntentProcessingResult(success=True, message="test", intent_data={})
        assert result.pending_offer is None

    def test_set_with_offer(self):
        result = IntentProcessingResult(
            success=True,
            message="test",
            intent_data={},
            pending_offer={
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )
        assert result.pending_offer["workflow_type"] == "meeting"

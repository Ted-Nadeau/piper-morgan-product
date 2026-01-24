"""
Unit tests for ExplanationHandler service.

Tests verify:
1. Correct routing to explainer methods
2. Proper result structure
3. Fallback behavior on errors
4. Integration with detector and explainer
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.shared_types import TrustStage
from services.trust.explanation_detector import ExplanationQueryType
from services.trust.explanation_handler import ExplanationHandler, ExplanationHandlerResult


@pytest.fixture
def mock_trust_service():
    """Create mock trust service."""
    service = MagicMock()
    service.get_trust_stage = AsyncMock(return_value=TrustStage.NEW)
    service.explain_trust_state = AsyncMock(return_value="We're still getting to know each other.")
    return service


@pytest.fixture
def handler(mock_trust_service):
    """Create ExplanationHandler with mock service."""
    return ExplanationHandler(mock_trust_service)


@pytest.fixture
def user_id():
    """Generate test user ID."""
    return uuid4()


class TestExplanationHandlerInit:
    """Tests for ExplanationHandler initialization."""

    def test_creates_detector_and_explainer(self, mock_trust_service):
        """Should create detector and explainer on init."""
        handler = ExplanationHandler(mock_trust_service)

        assert handler._detector is not None
        assert handler._explainer is not None


class TestTryHandle:
    """Tests for try_handle method."""

    @pytest.mark.asyncio
    async def test_returns_not_handled_for_normal_message(self, handler, user_id):
        """Normal messages should return handled=False."""
        result = await handler.try_handle(user_id, "Hello, how are you?")

        assert result.handled is False
        assert result.response is None

    @pytest.mark.asyncio
    async def test_handles_why_action_query(self, handler, user_id):
        """Should handle 'why did you do that' queries."""
        result = await handler.try_handle(
            user_id, "Why did you do that?", recent_action="sent an email"
        )

        assert result.handled is True
        assert result.query_type == ExplanationQueryType.WHY_ACTION
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_handles_why_no_action_query(self, handler, user_id):
        """Should handle 'why don't you' queries."""
        result = await handler.try_handle(user_id, "Why don't you just do things?")

        assert result.handled is True
        assert result.query_type == ExplanationQueryType.WHY_NO_ACTION
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_handles_trust_level_query(self, handler, user_id):
        """Should handle trust level queries."""
        result = await handler.try_handle(user_id, "How do we work together?")

        assert result.handled is True
        assert result.query_type == ExplanationQueryType.TRUST_LEVEL
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_handles_behavior_question(self, handler, user_id):
        """Should handle general behavior questions."""
        result = await handler.try_handle(user_id, "Why do you always do that?")

        assert result.handled is True
        assert result.query_type == ExplanationQueryType.BEHAVIOR_QUESTION
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_includes_followup_offer(self, handler, user_id):
        """Should include follow-up offer in result."""
        result = await handler.try_handle(user_id, "Why are you so cautious?")

        assert result.followup_offer is not None
        assert len(result.followup_offer) > 0

    @pytest.mark.asyncio
    async def test_recent_action_used_for_why_action(self, handler, mock_trust_service, user_id):
        """Recent action should be included in explanation."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.TRUSTED

        result = await handler.try_handle(
            user_id, "Why did you do that?", recent_action="rescheduled your meeting"
        )

        assert "rescheduled your meeting" in result.response


class TestErrorHandling:
    """Tests for error handling."""

    @pytest.mark.asyncio
    async def test_returns_fallback_on_explainer_error(self, mock_trust_service, user_id):
        """Should return fallback response on explainer error."""
        mock_trust_service.explain_trust_state = AsyncMock(side_effect=Exception("Database error"))
        handler = ExplanationHandler(mock_trust_service)

        result = await handler.try_handle(user_id, "How do we work together?")

        assert result.handled is True
        assert result.response is not None
        # Should be fallback, not empty

    @pytest.mark.asyncio
    async def test_fallback_responses_exist_for_all_types(self, handler, user_id):
        """All query types should have fallback responses."""
        # This tests the _get_fallback_response method indirectly
        for query_type in ExplanationQueryType:
            if query_type != ExplanationQueryType.NOT_EXPLANATION_QUERY:
                fallback = handler._get_fallback_response(query_type)
                assert fallback is not None
                assert len(fallback) > 0


class TestResultProperties:
    """Tests for ExplanationHandlerResult properties."""

    def test_full_response_with_followup(self):
        """full_response should combine response and followup."""
        result = ExplanationHandlerResult(
            handled=True,
            response="Main explanation.",
            followup_offer="Would you like me to adjust?",
        )

        assert "Main explanation." in result.full_response
        assert "Would you like me to adjust?" in result.full_response

    def test_full_response_without_followup(self):
        """full_response should work without followup."""
        result = ExplanationHandlerResult(
            handled=True,
            response="Just the explanation.",
        )

        assert result.full_response == "Just the explanation."

    def test_full_response_none_when_no_response(self):
        """full_response should be None when no response."""
        result = ExplanationHandlerResult(handled=False)

        assert result.full_response is None


class TestConvenienceMethods:
    """Tests for convenience methods."""

    @pytest.mark.asyncio
    async def test_is_explanation_query_true(self, handler):
        """is_explanation_query should return True for explanation queries."""
        result = await handler.is_explanation_query("Why did you do that?")
        assert result is True

    @pytest.mark.asyncio
    async def test_is_explanation_query_false(self, handler):
        """is_explanation_query should return False for normal messages."""
        result = await handler.is_explanation_query("Hello there")
        assert result is False

    @pytest.mark.asyncio
    async def test_get_query_type_returns_type(self, handler):
        """get_query_type should return correct type."""
        result = await handler.get_query_type("Why are you so cautious?")
        assert result == ExplanationQueryType.WHY_NO_ACTION

    @pytest.mark.asyncio
    async def test_get_query_type_returns_none_for_normal(self, handler):
        """get_query_type should return None for normal messages."""
        result = await handler.get_query_type("What's on my calendar?")
        assert result is None


class TestHandleWithContext:
    """Tests for handle_with_context method."""

    @pytest.mark.asyncio
    async def test_uses_stage_change_for_behavior_question(self, handler, user_id):
        """Should explain stage change for behavior questions."""
        result = await handler.handle_with_context(
            user_id,
            "Why did you start doing that?",
            old_stage=TrustStage.BUILDING,
            new_stage=TrustStage.ESTABLISHED,
        )

        assert result.handled is True
        # Should mention progression/proactive
        assert "proactive" in result.response.lower()

    @pytest.mark.asyncio
    async def test_falls_back_to_standard_without_context(self, handler, user_id):
        """Should use standard handling without stage context."""
        result = await handler.handle_with_context(
            user_id,
            "Why did you start doing that?",
        )

        assert result.handled is True
        # Should still provide an explanation

    @pytest.mark.asyncio
    async def test_not_handled_for_normal_message(self, handler, user_id):
        """Should return not handled for normal messages."""
        result = await handler.handle_with_context(
            user_id,
            "Hello there",
            old_stage=TrustStage.NEW,
            new_stage=TrustStage.BUILDING,
        )

        assert result.handled is False


class TestIntegrationFlow:
    """Tests for full integration flow."""

    @pytest.mark.asyncio
    async def test_full_flow_why_action(self, mock_trust_service, user_id):
        """Test complete flow for WHY_ACTION query."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.ESTABLISHED
        handler = ExplanationHandler(mock_trust_service)

        result = await handler.try_handle(
            user_id,
            "I didn't ask you to cancel that meeting!",
            recent_action="cancelled the meeting",
        )

        assert result.handled is True
        assert result.query_type == ExplanationQueryType.WHY_ACTION
        assert "cancelled the meeting" in result.response
        assert result.followup_offer is not None

    @pytest.mark.asyncio
    async def test_full_flow_why_no_action(self, mock_trust_service, user_id):
        """Test complete flow for WHY_NO_ACTION query."""
        mock_trust_service.get_trust_stage.return_value = TrustStage.NEW
        handler = ExplanationHandler(mock_trust_service)

        result = await handler.try_handle(user_id, "Why do you always have to ask me first?")

        assert result.handled is True
        assert result.query_type == ExplanationQueryType.WHY_NO_ACTION
        # New stage should mention getting to know
        assert "getting to know" in result.response.lower() or "still" in result.response.lower()

"""
Tests for grammar-conscious intent classification.

Issue #619: GRAMMAR-TRANSFORM: Intent Classification
Phase 6: Integration
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent_service.classifier import IntentClassifier
from services.intent_service.intent_types import IntentUnderstanding
from services.shared_types import IntentCategory, InteractionSpace, PerceptionMode


class TestClassifyConscious:
    """Test classify_conscious method."""

    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.complete = AsyncMock(
            return_value='{"category": "execution", "action": "create_item", "confidence": 0.9, "reasoning": "test"}'
        )
        return llm

    @pytest.fixture
    def classifier(self, mock_llm):
        return IntentClassifier(llm_service=mock_llm)

    # --- Basic Integration Tests ---

    @pytest.mark.asyncio
    async def test_returns_intent_understanding(self, classifier):
        """classify_conscious returns IntentUnderstanding."""
        result = await classifier.classify_conscious(
            message="add a todo",
            context={"user_id": "test-user"},
        )
        assert isinstance(result, IntentUnderstanding)
        assert result.intent is not None
        assert result.understanding_narrative is not None

    @pytest.mark.asyncio
    async def test_preserves_intent_access(self, classifier):
        """Can still access underlying Intent."""
        result = await classifier.classify_conscious(
            message="create a new task",
            context={"user_id": "test-user"},
        )
        # Proxy properties work
        assert result.category is not None
        assert result.action is not None
        assert result.confidence is not None
        # Direct access works
        assert result.intent.category is not None

    # --- Place Awareness Tests ---

    @pytest.mark.asyncio
    async def test_detects_slack_dm(self, classifier):
        """Detects Slack DM context."""
        result = await classifier.classify_conscious(
            message="hi there",
            spatial_context={"room_id": "D123", "is_dm": True},
        )
        # DM should produce understanding
        assert result is not None
        assert result.understanding_narrative is not None

    @pytest.mark.asyncio
    async def test_detects_cli(self, classifier):
        """Detects CLI context."""
        result = await classifier.classify_conscious(
            message="list todos",
            spatial_context={"source": "cli"},
        )
        # Should still work, just with different tone
        assert result is not None

    # --- Experience Tests ---

    @pytest.mark.asyncio
    async def test_experience_test_noticing_language(self, classifier):
        """Uses experiential language."""
        result = await classifier.classify_conscious(
            message="find documents about the project",
            context={"user_id": "test-user"},
        )
        narrative = result.understanding_narrative.lower()
        # Should use first person
        assert "i" in narrative.split()  # "I" as a word
        # Should NOT be mechanical
        assert "query" not in narrative
        assert "returned" not in narrative
        assert "processed" not in narrative

    @pytest.mark.asyncio
    async def test_experience_test_confidence_human(self, classifier, mock_llm):
        """Confidence expressed in human terms."""
        mock_llm.complete = AsyncMock(
            return_value='{"category": "query", "action": "search_files", "confidence": 0.95, "reasoning": "clear request"}'
        )
        result = await classifier.classify_conscious(
            message="find all documents",
            context={"user_id": "test-user"},
        )
        # Should have confidence expression
        assert result.confidence_expression is not None
        # Should be human, not numeric
        assert "0.95" not in result.confidence_expression

    # --- Failure Handling Tests ---

    @pytest.mark.asyncio
    async def test_low_confidence_handled_gracefully(self, classifier, mock_llm):
        """Low confidence gets special handling."""
        mock_llm.complete = AsyncMock(
            return_value='{"category": "query", "action": "search_files", "confidence": 0.3, "reasoning": "uncertain"}'
        )
        result = await classifier.classify_conscious(
            message="do something with files maybe",
            context={"user_id": "test-user"},
        )
        # Should express uncertainty
        narrative = result.understanding_narrative.lower()
        assert (
            "think" in narrative
            or "might" in narrative
            or "sure" in narrative
            or "uncertain" in narrative
        )

    @pytest.mark.asyncio
    async def test_error_returns_understanding_not_exception(self, classifier, mock_llm):
        """Errors return IntentUnderstanding, not raise."""
        mock_llm.complete = AsyncMock(side_effect=ValueError("LLM broke"))

        # Should NOT raise
        result = await classifier.classify_conscious(
            message="test message",
            context={"user_id": "test-user"},
        )

        # Should return graceful failure
        assert isinstance(result, IntentUnderstanding)
        assert result.intent.action == "clarification_needed"

    # --- Backward Compatibility Tests ---

    @pytest.mark.asyncio
    async def test_classify_still_returns_intent(self, classifier):
        """Original classify() still returns Intent."""
        result = await classifier.classify(
            message="add a todo",
            context={"user_id": "test-user"},
        )
        assert isinstance(result, Intent)
        assert not isinstance(result, IntentUnderstanding)


class TestContractorTest:
    """Verify integration passes the Contractor Test."""

    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.complete = AsyncMock(
            return_value='{"category": "execution", "action": "create_item", "confidence": 0.9, "reasoning": "test"}'
        )
        return llm

    @pytest.fixture
    def classifier(self, mock_llm):
        return IntentClassifier(llm_service=mock_llm)

    @pytest.mark.asyncio
    async def test_professional_tone(self, classifier):
        """Responses have professional tone."""
        result = await classifier.classify_conscious(
            message="help me with this task",
            spatial_context={"channel": "general"},  # Public channel
        )

        narrative = result.understanding_narrative

        # Should NOT be over-enthusiastic
        assert "!" not in narrative or narrative.count("!") <= 1
        assert "awesome" not in narrative.lower()
        assert "amazing" not in narrative.lower()

        # Should NOT be robotic
        assert "Query:" not in narrative
        assert "Result:" not in narrative


class TestComponentsInitialized:
    """Verify all grammar-conscious components are initialized."""

    @pytest.fixture
    def mock_llm(self):
        return MagicMock()

    @pytest.fixture
    def classifier(self, mock_llm):
        return IntentClassifier(llm_service=mock_llm)

    def test_place_detector_initialized(self, classifier):
        """PlaceDetector is initialized."""
        assert hasattr(classifier, "place_detector")
        assert classifier.place_detector is not None

    def test_personality_bridge_initialized(self, classifier):
        """PersonalityBridge is initialized."""
        assert hasattr(classifier, "personality_bridge")
        assert classifier.personality_bridge is not None

    def test_warmth_calibrator_initialized(self, classifier):
        """WarmthCalibrator is initialized."""
        assert hasattr(classifier, "warmth_calibrator")
        assert classifier.warmth_calibrator is not None

    def test_failure_handler_initialized(self, classifier):
        """HonestFailureHandler is initialized."""
        assert hasattr(classifier, "failure_handler")
        assert classifier.failure_handler is not None

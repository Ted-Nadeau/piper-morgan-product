"""
Tests for RecognitionTrigger.

Part of #411 MUX-INTERACT-RECOGNITION.

Tests cover:
- Threshold-based triggering
- Recognition generation
- Integration with orientation
- Edge cases
"""

from unittest.mock import MagicMock, Mock

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.intent_types import IntentClassificationContext, IntentUnderstanding
from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    OrientationPillarType,
    OrientationState,
    RecognitionOption,
    RecognitionOptions,
)
from services.mux.recognition_trigger import (
    RECOGNITION_THRESHOLD_HIGH,
    RECOGNITION_THRESHOLD_LOW,
    RecognitionTrigger,
    RecognitionTriggerResult,
    create_recognition_understanding,
)
from services.shared_types import PerceptionMode

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def trigger() -> RecognitionTrigger:
    """Standard recognition trigger."""
    return RecognitionTrigger()


@pytest.fixture
def mock_orientation() -> OrientationState:
    """Mock orientation state for testing."""
    return OrientationState.gather(place=None)


@pytest.fixture
def context_with_orientation(mock_orientation) -> IntentClassificationContext:
    """Classification context with orientation."""
    ctx = IntentClassificationContext(
        message="check on things",
    )
    ctx.orientation = mock_orientation
    return ctx


@pytest.fixture
def context_without_orientation() -> IntentClassificationContext:
    """Classification context without orientation."""
    return IntentClassificationContext(
        message="check on things",
    )


@pytest.fixture
def high_confidence_intent() -> Intent:
    """Intent with high confidence."""
    return Intent(
        category=IntentCategory.QUERY,
        action="list_todos",
        confidence=0.9,
    )


@pytest.fixture
def moderate_confidence_intent() -> Intent:
    """Intent with moderate confidence (in recognition zone)."""
    return Intent(
        category=IntentCategory.QUERY,
        action="check_status",
        confidence=0.5,  # Between 0.35 and 0.7
    )


@pytest.fixture
def low_confidence_intent() -> Intent:
    """Intent with low confidence (below recognition zone)."""
    return Intent(
        category=IntentCategory.QUERY,
        action="unknown",
        confidence=0.2,  # Below 0.35
    )


@pytest.fixture
def sample_recognition_options() -> RecognitionOptions:
    """Sample recognition options for testing."""
    return RecognitionOptions(
        options=[
            RecognitionOption(
                label="Check standup status",
                description="meeting in 30 min",
                intent_hint="standup_status",
                relevance=0.9,
                pillar_source=OrientationPillarType.TEMPORAL,
            ),
            RecognitionOption(
                label="Review pending PRs",
                description="3 waiting",
                intent_hint="review_prs",
                relevance=0.8,
                pillar_source=OrientationPillarType.AGENCY,
            ),
        ],
        narrative_frame="I can help with a few things:",
        escape_hatch="Or something else?",
        call_to_action="Which would help?",
    )


# =============================================================================
# Test: Threshold Logic
# =============================================================================


class TestShouldTrigger:
    """Tests for should_trigger threshold logic."""

    def test_high_confidence_does_not_trigger(
        self, trigger: RecognitionTrigger, context_with_orientation
    ):
        """High confidence (above threshold) should not trigger."""
        result = trigger.should_trigger(0.9, context_with_orientation)
        assert result is False

    def test_moderate_confidence_triggers(
        self, trigger: RecognitionTrigger, context_with_orientation
    ):
        """Moderate confidence (in zone) should trigger."""
        result = trigger.should_trigger(0.5, context_with_orientation)
        assert result is True

    def test_low_confidence_does_not_trigger(
        self, trigger: RecognitionTrigger, context_with_orientation
    ):
        """Low confidence (below threshold) should not trigger."""
        result = trigger.should_trigger(0.2, context_with_orientation)
        assert result is False

    def test_no_orientation_does_not_trigger(
        self, trigger: RecognitionTrigger, context_without_orientation
    ):
        """Missing orientation should not trigger."""
        result = trigger.should_trigger(0.5, context_without_orientation)
        assert result is False

    def test_boundary_high_threshold(self, trigger: RecognitionTrigger, context_with_orientation):
        """Confidence exactly at high threshold should not trigger."""
        result = trigger.should_trigger(RECOGNITION_THRESHOLD_HIGH, context_with_orientation)
        assert result is False

    def test_boundary_low_threshold(self, trigger: RecognitionTrigger, context_with_orientation):
        """Confidence exactly at low threshold should trigger."""
        result = trigger.should_trigger(RECOGNITION_THRESHOLD_LOW, context_with_orientation)
        assert result is True

    def test_just_above_low_threshold(self, trigger: RecognitionTrigger, context_with_orientation):
        """Confidence just above low threshold should trigger."""
        result = trigger.should_trigger(0.36, context_with_orientation)
        assert result is True

    def test_just_below_high_threshold(self, trigger: RecognitionTrigger, context_with_orientation):
        """Confidence just below high threshold should trigger."""
        result = trigger.should_trigger(0.69, context_with_orientation)
        assert result is True


class TestCustomThresholds:
    """Tests for custom threshold configuration."""

    def test_custom_high_threshold(self, context_with_orientation):
        """Custom high threshold should be respected."""
        trigger = RecognitionTrigger(high_threshold=0.8)
        # 0.75 should now trigger (default would not)
        result = trigger.should_trigger(0.75, context_with_orientation)
        assert result is True

    def test_custom_low_threshold(self, context_with_orientation):
        """Custom low threshold should be respected."""
        trigger = RecognitionTrigger(low_threshold=0.5)
        # 0.4 should not trigger (default would)
        result = trigger.should_trigger(0.4, context_with_orientation)
        assert result is False


# =============================================================================
# Test: Evaluate Method
# =============================================================================


class TestEvaluate:
    """Tests for the evaluate() method."""

    def test_evaluate_returns_result(
        self,
        trigger: RecognitionTrigger,
        moderate_confidence_intent: Intent,
        context_with_orientation,
    ):
        """Evaluate should return a RecognitionTriggerResult."""
        result = trigger.evaluate(
            intent=moderate_confidence_intent,
            context=context_with_orientation,
        )
        assert isinstance(result, RecognitionTriggerResult)

    def test_evaluate_high_confidence_no_trigger(
        self,
        trigger: RecognitionTrigger,
        high_confidence_intent: Intent,
        context_with_orientation,
    ):
        """High confidence should return should_trigger=False."""
        result = trigger.evaluate(
            intent=high_confidence_intent,
            context=context_with_orientation,
        )
        assert result.should_trigger is False
        assert "too high" in result.reason.lower() or "act on intent" in result.reason.lower()

    def test_evaluate_low_confidence_no_trigger(
        self,
        trigger: RecognitionTrigger,
        low_confidence_intent: Intent,
        context_with_orientation,
    ):
        """Low confidence should return should_trigger=False."""
        result = trigger.evaluate(
            intent=low_confidence_intent,
            context=context_with_orientation,
        )
        assert result.should_trigger is False
        assert "too low" in result.reason.lower() or "honest failure" in result.reason.lower()

    def test_evaluate_includes_channel_and_trust(
        self,
        trigger: RecognitionTrigger,
        moderate_confidence_intent: Intent,
        context_with_orientation,
    ):
        """Evaluate should use provided channel and trust stage."""
        result = trigger.evaluate(
            intent=moderate_confidence_intent,
            context=context_with_orientation,
            channel=ChannelType.SLACK,
            trust_stage=3,
        )
        # Should not error - channel/trust are used internally
        assert isinstance(result, RecognitionTriggerResult)

    def test_evaluate_none_intent(
        self,
        trigger: RecognitionTrigger,
        context_with_orientation,
    ):
        """None intent should not trigger (confidence = 0)."""
        result = trigger.evaluate(
            intent=None,
            context=context_with_orientation,
        )
        assert result.should_trigger is False


# =============================================================================
# Test: Create Recognition Understanding
# =============================================================================


class TestCreateRecognitionUnderstanding:
    """Tests for create_recognition_understanding helper."""

    def test_creates_understanding(
        self,
        moderate_confidence_intent: Intent,
        context_with_orientation,
        sample_recognition_options,
    ):
        """Should create valid IntentUnderstanding."""
        understanding = create_recognition_understanding(
            intent=moderate_confidence_intent,
            context=context_with_orientation,
            recognition_options=sample_recognition_options,
            formatted_response="I can help...",
        )
        assert isinstance(understanding, IntentUnderstanding)
        assert understanding.intent == moderate_confidence_intent

    def test_understanding_narrative_is_formatted_response(
        self,
        moderate_confidence_intent: Intent,
        context_with_orientation,
        sample_recognition_options,
    ):
        """Understanding narrative should be the formatted response."""
        formatted = "I can help with several things:\n• Option 1\n• Option 2"
        understanding = create_recognition_understanding(
            intent=moderate_confidence_intent,
            context=context_with_orientation,
            recognition_options=sample_recognition_options,
            formatted_response=formatted,
        )
        assert understanding.understanding_narrative == formatted

    def test_understanding_perception_mode_is_noticing(
        self,
        moderate_confidence_intent: Intent,
        context_with_orientation,
        sample_recognition_options,
    ):
        """Recognition understanding should use NOTICING mode."""
        understanding = create_recognition_understanding(
            intent=moderate_confidence_intent,
            context=context_with_orientation,
            recognition_options=sample_recognition_options,
            formatted_response="...",
        )
        assert understanding.perception_mode == PerceptionMode.NOTICING

    def test_understanding_has_metadata(
        self,
        moderate_confidence_intent: Intent,
        context_with_orientation,
        sample_recognition_options,
    ):
        """Recognition understanding should have metadata."""
        understanding = create_recognition_understanding(
            intent=moderate_confidence_intent,
            context=context_with_orientation,
            recognition_options=sample_recognition_options,
            formatted_response="...",
        )
        assert understanding.metadata is not None
        assert understanding.metadata.get("recognition_offered") is True
        assert understanding.metadata.get("recognition_options_count") == 2


# =============================================================================
# Test: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Edge case tests."""

    def test_zero_confidence(self, trigger: RecognitionTrigger, context_with_orientation):
        """Zero confidence should not trigger (below low threshold)."""
        result = trigger.should_trigger(0.0, context_with_orientation)
        assert result is False

    def test_one_confidence(self, trigger: RecognitionTrigger, context_with_orientation):
        """1.0 confidence should not trigger (above high threshold)."""
        result = trigger.should_trigger(1.0, context_with_orientation)
        assert result is False

    def test_negative_confidence(self, trigger: RecognitionTrigger, context_with_orientation):
        """Negative confidence should not trigger."""
        result = trigger.should_trigger(-0.5, context_with_orientation)
        assert result is False

    def test_empty_orientation(self, trigger: RecognitionTrigger):
        """Empty/default orientation should still work."""
        ctx = IntentClassificationContext(
            message="test",
        )
        ctx.orientation = OrientationState.gather(place=None)
        result = trigger.should_trigger(0.5, ctx)
        assert result is True  # Orientation exists, even if sparse


# =============================================================================
# Test: Threshold Constants
# =============================================================================


class TestThresholdConstants:
    """Tests for threshold constant values."""

    def test_high_threshold_reasonable(self):
        """High threshold should be reasonable (0.6-0.8)."""
        assert 0.6 <= RECOGNITION_THRESHOLD_HIGH <= 0.8

    def test_low_threshold_reasonable(self):
        """Low threshold should be reasonable (0.2-0.5)."""
        assert 0.2 <= RECOGNITION_THRESHOLD_LOW <= 0.5

    def test_thresholds_leave_meaningful_gap(self):
        """Gap between thresholds should be meaningful."""
        gap = RECOGNITION_THRESHOLD_HIGH - RECOGNITION_THRESHOLD_LOW
        assert gap >= 0.2  # At least 20% gap

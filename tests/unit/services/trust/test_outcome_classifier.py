"""
Unit tests for OutcomeClassifier.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

Tests outcome classification rules for trust computation.
"""

import pytest

from services.trust.outcome_classifier import (
    NEGATIVE_PATTERNS,
    NEUTRAL_PATTERNS,
    SUCCESSFUL_PATTERNS,
    OutcomeClassification,
    OutcomeClassifier,
    OutcomeType,
)


class TestOutcomeTypeEnum:
    """Test OutcomeType enum."""

    def test_has_required_values(self):
        """OutcomeType has all required values."""
        assert OutcomeType.SUCCESSFUL.value == "successful"
        assert OutcomeType.NEUTRAL.value == "neutral"
        assert OutcomeType.NEGATIVE.value == "negative"

    def test_string_conversion(self):
        """OutcomeType value converts to string properly."""
        assert OutcomeType.SUCCESSFUL.value == "successful"


class TestOutcomeClassificationDataclass:
    """Test OutcomeClassification dataclass."""

    def test_has_required_fields(self):
        """OutcomeClassification has all required fields."""
        result = OutcomeClassification(
            outcome=OutcomeType.SUCCESSFUL,
            confidence=0.8,
            signals_detected=["gratitude"],
            reasoning="User said thanks",
        )
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert result.confidence == 0.8
        assert result.signals_detected == ["gratitude"]
        assert result.reasoning == "User said thanks"


class TestPatternDefinitions:
    """Test pattern constant definitions."""

    def test_successful_patterns_exist(self):
        """SUCCESSFUL_PATTERNS is not empty."""
        assert len(SUCCESSFUL_PATTERNS) > 0
        # Each should be (pattern, signal_name) tuple
        for pattern, signal in SUCCESSFUL_PATTERNS:
            assert isinstance(pattern, str)
            assert isinstance(signal, str)

    def test_negative_patterns_exist(self):
        """NEGATIVE_PATTERNS is not empty."""
        assert len(NEGATIVE_PATTERNS) > 0

    def test_neutral_patterns_exist(self):
        """NEUTRAL_PATTERNS is not empty."""
        assert len(NEUTRAL_PATTERNS) > 0


class TestClassifyGratitude:
    """Test classification of gratitude expressions."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    @pytest.mark.parametrize(
        "message",
        [
            "thanks",
            "Thank you!",
            "Thanks so much",
            "thx",
            "ty",
            "that was helpful",
            "I really appreciated that",
        ],
    )
    def test_gratitude_is_successful(self, classifier, message):
        """Gratitude expressions classify as successful."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert "gratitude" in result.signals_detected

    @pytest.mark.parametrize(
        "message",
        [
            "perfect!",
            "great job",
            "excellent",
            "awesome",
            "nice work",
            "Good job!",
            "well done",
        ],
    )
    def test_acknowledgment_is_successful(self, classifier, message):
        """Acknowledgment expressions classify as successful."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert "acknowledgment" in result.signals_detected


class TestClassifyFollowUp:
    """Test classification of follow-up engagement."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    @pytest.mark.parametrize(
        "message",
        [
            "can you also help with...",
            "what about the other file?",
            "how about we also...",
            "and another thing",
            "one more thing",
            "another question",
        ],
    )
    def test_followup_is_successful(self, classifier, message):
        """Follow-up engagement classifies as successful."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert "follow_up" in result.signals_detected


class TestClassifyConfirmation:
    """Test classification of explicit confirmation."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    @pytest.mark.parametrize(
        "message",
        [
            "yes",
            "yep",
            "yeah",
            "yup",
            "correct",
            "right",
            "got it",
            "understood",
            "makes sense",
        ],
    )
    def test_confirmation_is_successful(self, classifier, message):
        """Confirmation expressions classify as successful."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert "confirmation" in result.signals_detected


class TestClassifyRejection:
    """Test classification of rejection/negative feedback."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    @pytest.mark.parametrize(
        "message",
        [
            "not what I wanted",
            "that's not what I asked for",
            "wrong",
            "incorrect",
            "no that's not it",
            "that's not right",
            "that's not correct",
        ],
    )
    def test_rejection_is_negative(self, classifier, message):
        """Rejection expressions classify as negative."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.NEGATIVE
        assert "rejection" in result.signals_detected


class TestClassifyFrustration:
    """Test classification of frustration expressions."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    @pytest.mark.parametrize(
        "message",
        [
            "ugh, not again",
            "argh this is annoying",
            "sigh...",
            "this is so frustrating",
            "why can't you understand",
            "why won't you do it right",
        ],
    )
    def test_frustration_is_negative(self, classifier, message):
        """Frustration expressions classify as negative."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.NEGATIVE
        assert "frustration" in result.signals_detected


class TestClassifyComplaints:
    """Test classification of complaints."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    @pytest.mark.parametrize(
        "message",
        [
            "stop doing that",
            "don't do that again",
            "I didn't ask for that",
            "I didn't want that",
            "that's wrong",
            "that's terrible",
        ],
    )
    def test_complaint_is_negative(self, classifier, message):
        """Complaints classify as negative."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.NEGATIVE


class TestClassifyNeutral:
    """Test classification of neutral responses."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    @pytest.mark.parametrize(
        "message",
        [
            "anyway, let's move on",
            "different topic",
            "never mind",
            "forget it",
            "whatever",
        ],
    )
    def test_topic_change_is_neutral(self, classifier, message):
        """Topic changes classify as neutral."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.NEUTRAL

    @pytest.mark.parametrize(
        "message",
        [
            "ok",
            "okay",
            "sure",
            "fine",
            "alright",
            "i see",
            "i guess",
            "maybe",
        ],
    )
    def test_noncommittal_is_neutral(self, classifier, message):
        """Non-committal responses classify as neutral."""
        result = classifier.classify(message)
        assert result.outcome == OutcomeType.NEUTRAL


class TestClassifyEdgeCases:
    """Test edge cases and ambiguous inputs."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    def test_empty_message_is_neutral(self, classifier):
        """Empty message classifies as neutral."""
        result = classifier.classify("")
        assert result.outcome == OutcomeType.NEUTRAL
        assert "empty_message" in result.signals_detected

    def test_whitespace_only_is_neutral(self, classifier):
        """Whitespace-only message classifies as neutral."""
        result = classifier.classify("   \n\t  ")
        assert result.outcome == OutcomeType.NEUTRAL

    def test_no_signals_is_neutral(self, classifier):
        """Message with no recognized signals is neutral."""
        result = classifier.classify("The sky is blue")
        assert result.outcome == OutcomeType.NEUTRAL
        assert result.signals_detected == []
        assert "defaulting to neutral" in result.reasoning.lower()

    def test_mixed_signals_negative_wins(self, classifier):
        """When signals conflict, negative wins (user effort to complain)."""
        # "Thanks but that's wrong" has both gratitude and rejection
        result = classifier.classify("thanks but that's wrong")
        assert result.outcome == OutcomeType.NEGATIVE

    def test_case_insensitive(self, classifier):
        """Classification is case-insensitive."""
        result1 = classifier.classify("THANKS")
        result2 = classifier.classify("thanks")
        result3 = classifier.classify("ThAnKs")
        assert result1.outcome == result2.outcome == result3.outcome == OutcomeType.SUCCESSFUL


class TestClassifyWithContext:
    """Test context-based classification."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    def test_error_context_is_negative(self, classifier):
        """Error context classifies as negative regardless of message."""
        result = classifier.classify("ok", context={"error_occurred": True})
        assert result.outcome == OutcomeType.NEGATIVE
        assert "error_occurred" in result.signals_detected

    def test_user_corrected_is_negative(self, classifier):
        """User correction context is negative."""
        result = classifier.classify("no, I meant...", context={"user_corrected": True})
        assert result.outcome == OutcomeType.NEGATIVE
        assert "user_corrected" in result.signals_detected

    def test_task_completed_is_successful(self, classifier):
        """Task completed context is successful."""
        result = classifier.classify("", context={"task_completed": True})
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert "task_completed" in result.signals_detected


class TestClassifyTaskCompletion:
    """Test task completion classification method."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    def test_task_success_no_reaction(self, classifier):
        """Task success with no user reaction is successful."""
        result = classifier.classify_task_completion(task_succeeded=True)
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert "task_completed" in result.signals_detected

    def test_task_failure_no_reaction(self, classifier):
        """Task failure with no user reaction is negative."""
        result = classifier.classify_task_completion(task_succeeded=False)
        assert result.outcome == OutcomeType.NEGATIVE
        assert "task_failed" in result.signals_detected

    def test_task_success_with_thanks(self, classifier):
        """Task success with thanks is successful."""
        result = classifier.classify_task_completion(task_succeeded=True, user_reaction="thanks!")
        assert result.outcome == OutcomeType.SUCCESSFUL
        assert "gratitude" in result.signals_detected

    def test_task_failure_overrides_thanks(self, classifier):
        """Task failure overrides positive user reaction."""
        # User might say "thanks anyway" when task fails
        result = classifier.classify_task_completion(
            task_succeeded=False, user_reaction="thanks for trying"
        )
        assert result.outcome == OutcomeType.NEGATIVE
        assert "task_failed" in result.signals_detected


class TestClassifierConfidence:
    """Test confidence scoring."""

    @pytest.fixture
    def classifier(self):
        """Create OutcomeClassifier instance."""
        return OutcomeClassifier()

    def test_multiple_signals_higher_confidence(self, classifier):
        """Multiple matching signals increase confidence."""
        single = classifier.classify("thanks")
        multiple = classifier.classify("thanks, that was perfect and helpful!")

        assert multiple.confidence >= single.confidence

    def test_confidence_capped(self, classifier):
        """Confidence is capped at 0.9."""
        result = classifier.classify("thanks thanks thanks perfect excellent great awesome")
        assert result.confidence <= 0.9

    def test_no_signals_low_confidence(self, classifier):
        """No signals results in low confidence."""
        result = classifier.classify("The sky is blue today")
        assert result.confidence < 0.5


class TestClassifierStateless:
    """Test that classifier is stateless."""

    def test_multiple_calls_independent(self):
        """Multiple classify calls are independent."""
        classifier = OutcomeClassifier()

        # First call with negative
        result1 = classifier.classify("that's wrong")
        assert result1.outcome == OutcomeType.NEGATIVE

        # Second call with positive
        result2 = classifier.classify("thanks")
        assert result2.outcome == OutcomeType.SUCCESSFUL

        # Third call should still work correctly
        result3 = classifier.classify("ok")
        assert result3.outcome == OutcomeType.NEUTRAL

    def test_multiple_instances_same_behavior(self):
        """Multiple classifier instances behave identically."""
        c1 = OutcomeClassifier()
        c2 = OutcomeClassifier()

        messages = ["thanks", "wrong", "ok", "whatever", "perfect"]
        for msg in messages:
            r1 = c1.classify(msg)
            r2 = c2.classify(msg)
            assert r1.outcome == r2.outcome
            assert r1.signals_detected == r2.signals_detected

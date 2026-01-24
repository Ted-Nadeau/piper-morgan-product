"""
Unit tests for SignalDetector.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

Tests detection of escalation and complaint signals.
"""

import pytest

from services.trust.signal_detector import (
    COMPLAINT_PATTERNS,
    ESCALATION_PATTERNS,
    SignalDetectionResult,
    SignalDetector,
    SignalType,
)


class TestSignalTypeEnum:
    """Test SignalType enum."""

    def test_has_required_values(self):
        """SignalType has all required values."""
        assert SignalType.ESCALATION.value == "escalation"
        assert SignalType.COMPLAINT.value == "complaint"
        assert SignalType.NONE.value == "none"


class TestSignalDetectionResultDataclass:
    """Test SignalDetectionResult dataclass."""

    def test_has_required_fields(self):
        """SignalDetectionResult has all required fields."""
        result = SignalDetectionResult(
            signal_type=SignalType.ESCALATION,
            confidence=0.85,
            phrases_matched=["just handle it"],
            patterns_matched=["autonomy_grant"],
            reasoning="User wants autonomous behavior",
        )
        assert result.signal_type == SignalType.ESCALATION
        assert result.confidence == 0.85
        assert result.phrases_matched == ["just handle it"]
        assert result.patterns_matched == ["autonomy_grant"]
        assert result.reasoning == "User wants autonomous behavior"


class TestPatternDefinitions:
    """Test pattern constant definitions."""

    def test_escalation_patterns_exist(self):
        """ESCALATION_PATTERNS is not empty."""
        assert len(ESCALATION_PATTERNS) > 0
        # Each should be (pattern, signal_name, confidence) tuple
        for pattern, name, confidence in ESCALATION_PATTERNS:
            assert isinstance(pattern, str)
            assert isinstance(name, str)
            assert isinstance(confidence, float)
            assert 0 <= confidence <= 1

    def test_complaint_patterns_exist(self):
        """COMPLAINT_PATTERNS is not empty."""
        assert len(COMPLAINT_PATTERNS) > 0


class TestDetectEscalation:
    """Test detection of escalation signals."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    @pytest.mark.parametrize(
        "message",
        [
            "I trust you to handle that",
            "I trust that you'll do the right thing",
            "You can handle this without asking",
            "You know what to do",
        ],
    )
    def test_explicit_trust_statements(self, detector, message):
        """Explicit trust statements trigger escalation."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.ESCALATION

    @pytest.mark.parametrize(
        "message",
        [
            "Just handle it",
            "Just do it",
            "Just take care of it",
        ],
    )
    def test_autonomy_grants(self, detector, message):
        """Autonomy grant phrases trigger escalation."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.ESCALATION
        assert "autonomy_grant" in result.patterns_matched

    @pytest.mark.parametrize(
        "message",
        [
            "Do that automatically",
            "Do it automatically from now on",
            "Go ahead automatically",
        ],
    )
    def test_auto_requests(self, detector, message):
        """Automatic behavior requests trigger escalation."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.ESCALATION

    @pytest.mark.parametrize(
        "message",
        [
            "Don't ask me first",
            "No need to ask",
            "You don't need to ask",
            "You don't have to confirm",
            "You don't need to check with me",
        ],
    )
    def test_skip_confirmation(self, detector, message):
        """Skip confirmation phrases trigger escalation."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.ESCALATION
        assert "skip_confirmation" in result.patterns_matched

    @pytest.mark.parametrize(
        "message",
        [
            "Take care of it for me",
            "Handle this for me",
            "Leave it to you",
        ],
    )
    def test_delegation(self, detector, message):
        """Delegation phrases trigger escalation."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.ESCALATION

    @pytest.mark.parametrize(
        "message",
        [
            "From now on, just do it",
            "Going forward, always handle that",
            "Whenever this happens, just go ahead",
            "Every time that happens, go ahead and fix it",
        ],
    )
    def test_future_autonomy(self, detector, message):
        """Future autonomy phrases trigger escalation."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.ESCALATION


class TestDetectComplaint:
    """Test detection of complaint signals."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    @pytest.mark.parametrize(
        "message",
        [
            "Stop doing that",
            "Stop it",
            "Stop that please",
        ],
    )
    def test_stop_commands(self, detector, message):
        """Stop commands trigger complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT
        assert "stop_command" in result.patterns_matched

    @pytest.mark.parametrize(
        "message",
        [
            "Don't do that",
            "Don't do that again",
            "Do not say that",
            "Don't say it",
        ],
    )
    def test_prohibition(self, detector, message):
        """Prohibition phrases trigger complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT

    @pytest.mark.parametrize(
        "message",
        [
            "I didn't ask for that",
            "I didn't ask you to do that",
            "I didn't want that",
            "I didn't need you to",
            "I don't want this",
        ],
    )
    def test_rejection_of_offer(self, detector, message):
        """Rejection of offers triggers complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT
        assert "rejection_of_offer" in result.patterns_matched

    @pytest.mark.parametrize(
        "message",
        [
            "That's annoying",
            "This is frustrating",
            "That's irritating",
        ],
    )
    def test_frustration_expressions(self, detector, message):
        """Frustration expressions trigger complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT
        assert "frustration" in result.patterns_matched

    @pytest.mark.parametrize(
        "message",
        [
            "You're being too proactive",
            "You're being too pushy",
            "This is overly aggressive",
        ],
    )
    def test_over_proactive_complaint(self, detector, message):
        """Over-proactive complaints trigger complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT
        assert "over_proactive_complaint" in result.patterns_matched

    @pytest.mark.parametrize(
        "message",
        [
            "Stop suggesting things",
            "Stop offering alternatives",
            "Stop asking me questions",
        ],
    )
    def test_suggestion_complaints(self, detector, message):
        """Suggestion complaints trigger complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT

    @pytest.mark.parametrize(
        "message",
        [
            "I told you not to do that",
            "I asked you to stop",
        ],
    )
    def test_repeated_violation(self, detector, message):
        """Repeated violation complaints have high confidence."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT
        assert "repeated_violation" in result.patterns_matched
        assert result.confidence > 0.8

    @pytest.mark.parametrize(
        "message",
        [
            "Absolutely not",
            "Definitely not",
            "No way",
        ],
    )
    def test_strong_rejection(self, detector, message):
        """Strong rejections trigger complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.COMPLAINT
        assert "strong_rejection" in result.patterns_matched


class TestDetectNone:
    """Test that normal messages don't trigger signals."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    @pytest.mark.parametrize(
        "message",
        [
            "What's the weather like?",
            "Can you help me with my calendar?",
            "Thanks for the help",
            "That looks good",
            "Let me think about it",
            "Maybe tomorrow",
            "I need to check something first",
        ],
    )
    def test_normal_messages_no_signal(self, detector, message):
        """Normal messages don't trigger escalation or complaint."""
        result = detector.detect(message)
        assert result.signal_type == SignalType.NONE

    def test_empty_message(self, detector):
        """Empty message returns NONE."""
        result = detector.detect("")
        assert result.signal_type == SignalType.NONE

    def test_whitespace_message(self, detector):
        """Whitespace-only message returns NONE."""
        result = detector.detect("   \n\t  ")
        assert result.signal_type == SignalType.NONE


class TestContextBoost:
    """Test context-based confidence boosting."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    def test_complaint_boosted_after_proactive(self, detector):
        """Complaints in response to proactive behavior have higher confidence."""
        # Same message with and without proactive context
        message = "No, I don't want that"

        result_normal = detector.detect(message)
        result_proactive = detector.detect(message, context={"in_response_to_proactive": True})

        # Both should be complaints
        assert result_normal.signal_type == SignalType.COMPLAINT
        assert result_proactive.signal_type == SignalType.COMPLAINT

        # Proactive context should boost confidence
        assert result_proactive.confidence >= result_normal.confidence


class TestConvenienceMethods:
    """Test convenience detection methods."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    def test_detect_escalation_returns_result(self, detector):
        """detect_escalation returns result when escalation found."""
        result = detector.detect_escalation("Just handle it")
        assert result is not None
        assert result.signal_type == SignalType.ESCALATION

    def test_detect_escalation_returns_none(self, detector):
        """detect_escalation returns None when no escalation."""
        result = detector.detect_escalation("Thanks for helping")
        assert result is None

    def test_detect_complaint_returns_result(self, detector):
        """detect_complaint returns result when complaint found."""
        result = detector.detect_complaint("Stop doing that")
        assert result is not None
        assert result.signal_type == SignalType.COMPLAINT

    def test_detect_complaint_returns_none(self, detector):
        """detect_complaint returns None when no complaint."""
        result = detector.detect_complaint("That looks great")
        assert result is None

    def test_detect_complaint_with_proactive_flag(self, detector):
        """detect_complaint accepts proactive flag."""
        result = detector.detect_complaint("No thanks", in_response_to_proactive=True)
        # This might or might not be a complaint depending on patterns
        # but the method should work without error
        assert result is None or result.signal_type == SignalType.COMPLAINT


class TestExampleMethods:
    """Test example generation methods."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    def test_escalation_examples_are_detected(self, detector):
        """Example escalation phrases are actually detected."""
        examples = detector.get_escalation_examples()
        assert len(examples) > 0
        for example in examples:
            result = detector.detect(example)
            assert result.signal_type == SignalType.ESCALATION, f"Example not detected: {example}"

    def test_complaint_examples_are_detected(self, detector):
        """Example complaint phrases are actually detected."""
        examples = detector.get_complaint_examples()
        assert len(examples) > 0
        for example in examples:
            result = detector.detect(example)
            assert result.signal_type == SignalType.COMPLAINT, f"Example not detected: {example}"


class TestSignalPrecedence:
    """Test signal precedence when multiple signals present."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    def test_complaint_takes_precedence(self, detector):
        """Complaints take precedence over escalation (negative signals more important)."""
        # This message has both escalation and complaint signals
        # "stop doing that" is complaint, "I trust you" is escalation
        message = "I trust you but stop doing that"
        result = detector.detect(message)
        # The complaint should win because negative signals are more important
        assert result.signal_type == SignalType.COMPLAINT


class TestConfidenceScoring:
    """Test confidence scoring logic."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    def test_multiple_patterns_higher_confidence(self, detector):
        """Multiple matching patterns increase confidence."""
        single = detector.detect("Just handle it")
        multiple = detector.detect("I trust you, just handle it, you don't need to ask")

        # Both should be escalation
        assert single.signal_type == SignalType.ESCALATION
        assert multiple.signal_type == SignalType.ESCALATION

        # Multiple should have higher confidence
        assert multiple.confidence >= single.confidence

    def test_confidence_capped(self, detector):
        """Confidence is capped at 0.95."""
        result = detector.detect(
            "I trust you, just handle it, don't ask, do it automatically, leave it to you"
        )
        assert result.confidence <= 0.95


class TestCaseInsensitivity:
    """Test that detection is case-insensitive."""

    @pytest.fixture
    def detector(self):
        """Create SignalDetector instance."""
        return SignalDetector()

    def test_escalation_case_insensitive(self, detector):
        """Escalation detection is case-insensitive."""
        assert detector.detect("JUST HANDLE IT").signal_type == SignalType.ESCALATION
        assert detector.detect("Just Handle It").signal_type == SignalType.ESCALATION
        assert detector.detect("just handle it").signal_type == SignalType.ESCALATION

    def test_complaint_case_insensitive(self, detector):
        """Complaint detection is case-insensitive."""
        assert detector.detect("STOP DOING THAT").signal_type == SignalType.COMPLAINT
        assert detector.detect("Stop Doing That").signal_type == SignalType.COMPLAINT
        assert detector.detect("stop doing that").signal_type == SignalType.COMPLAINT


class TestDetectorStateless:
    """Test that detector is stateless."""

    def test_multiple_calls_independent(self):
        """Multiple detect calls are independent."""
        detector = SignalDetector()

        # Call with different signals
        r1 = detector.detect("Just handle it")
        r2 = detector.detect("Stop that")
        r3 = detector.detect("Hello there")

        assert r1.signal_type == SignalType.ESCALATION
        assert r2.signal_type == SignalType.COMPLAINT
        assert r3.signal_type == SignalType.NONE

    def test_multiple_instances_same_behavior(self):
        """Multiple detector instances behave identically."""
        d1 = SignalDetector()
        d2 = SignalDetector()

        messages = ["Just handle it", "Stop that", "Hello there"]
        for msg in messages:
            r1 = d1.detect(msg)
            r2 = d2.detect(msg)
            assert r1.signal_type == r2.signal_type
            assert r1.patterns_matched == r2.patterns_matched

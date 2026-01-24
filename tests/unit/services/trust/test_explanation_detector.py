"""
Unit tests for ExplanationDetector service.

Tests verify:
1. Correct detection of each query type
2. No false positives on normal conversation
3. Appropriate confidence levels
4. Edge cases and variations
"""

import pytest

from services.trust.explanation_detector import (
    ExplanationDetectionResult,
    ExplanationDetector,
    ExplanationQueryType,
)


@pytest.fixture
def detector():
    """Create ExplanationDetector instance."""
    return ExplanationDetector()


class TestExplanationDetectorInit:
    """Tests for ExplanationDetector initialization."""

    def test_creates_compiled_patterns(self, detector):
        """Should compile patterns on init."""
        assert len(detector._why_action) > 0
        assert len(detector._why_no_action) > 0
        assert len(detector._trust_level) > 0
        assert len(detector._behavior) > 0


class TestWhyActionDetection:
    """Tests for WHY_ACTION query type detection."""

    @pytest.mark.parametrize(
        "message",
        [
            "Why did you do that?",
            "Why did you just send that email?",
            "Why'd you reschedule my meeting?",
            "I didn't ask you to do that",
            "I didn't tell you to send that",
            "I never asked you to cancel the meeting",
            "Who told you to do that?",
            "What made you decide to move the deadline?",
            "Why would you assume that's okay?",
        ],
    )
    def test_detects_why_action_queries(self, detector, message):
        """Should detect various 'why did you' phrasings."""
        result = detector.detect(message)

        assert result.query_type == ExplanationQueryType.WHY_ACTION
        assert result.confidence >= detector.CONFIDENCE_THRESHOLD
        assert result.is_explanation_query

    def test_why_did_you_do_that(self, detector):
        """Classic 'why did you do that' detection."""
        result = detector.detect("Why did you do that?")

        assert result.query_type == ExplanationQueryType.WHY_ACTION
        assert result.confidence >= 0.85

    def test_i_didnt_ask_you(self, detector):
        """Complaint about uninstructed action."""
        result = detector.detect("I didn't ask you to send that email")

        assert result.query_type == ExplanationQueryType.WHY_ACTION
        assert result.matched_phrase is not None


class TestWhyNoActionDetection:
    """Tests for WHY_NO_ACTION query type detection."""

    @pytest.mark.parametrize(
        "message",
        [
            "Why don't you just do things?",
            "Why won't you just handle it?",
            "Why are you being so cautious?",
            "Why are you so careful about everything?",
            "Why do you always ask me first?",
            "Why do I have to tell you everything?",
            "Can't you just take care of it?",
            "Why not just do it?",
        ],
    )
    def test_detects_why_no_action_queries(self, detector, message):
        """Should detect various 'why don't you' phrasings."""
        result = detector.detect(message)

        assert result.query_type == ExplanationQueryType.WHY_NO_ACTION
        assert result.confidence >= detector.CONFIDENCE_THRESHOLD
        assert result.is_explanation_query

    def test_why_so_cautious(self, detector):
        """User asking about cautiousness."""
        result = detector.detect("Why are you being so cautious?")

        assert result.query_type == ExplanationQueryType.WHY_NO_ACTION
        assert result.confidence >= 0.85

    def test_why_always_ask(self, detector):
        """User frustrated with confirmations."""
        result = detector.detect("Why do you always have to ask?")

        assert result.query_type == ExplanationQueryType.WHY_NO_ACTION


class TestTrustLevelDetection:
    """Tests for TRUST_LEVEL query type detection."""

    @pytest.mark.parametrize(
        "message",
        [
            "How much do you trust me?",
            "How much do I trust you?",
            "What's our relationship?",
            "What is our working relationship like?",
            "How do we work together?",
            "How well do you know me?",
        ],
    )
    def test_detects_trust_level_queries(self, detector, message):
        """Should detect trust/relationship questions."""
        result = detector.detect(message)

        assert result.query_type == ExplanationQueryType.TRUST_LEVEL
        assert result.confidence >= detector.CONFIDENCE_THRESHOLD
        assert result.is_explanation_query

    def test_relationship_question(self, detector):
        """User asking about relationship."""
        result = detector.detect("What's our working relationship?")

        assert result.query_type == ExplanationQueryType.TRUST_LEVEL


class TestBehaviorQuestionDetection:
    """Tests for BEHAVIOR_QUESTION query type detection."""

    @pytest.mark.parametrize(
        "message",
        [
            "Why do you always do that?",
            "Why do you keep asking about meetings?",
            "Why did you start being more proactive?",
            "Why did you stop asking me about emails?",
            "Why are you acting like this?",
            "You used to ask me about everything",
        ],
    )
    def test_detects_behavior_questions(self, detector, message):
        """Should detect general behavior questions."""
        result = detector.detect(message)

        assert result.query_type == ExplanationQueryType.BEHAVIOR_QUESTION
        assert result.confidence >= detector.CONFIDENCE_THRESHOLD
        assert result.is_explanation_query

    def test_why_did_you_change(self, detector):
        """User noticing behavior change."""
        result = detector.detect("Why did you start doing that?")

        assert result.query_type == ExplanationQueryType.BEHAVIOR_QUESTION


class TestNoFalsePositives:
    """Tests to ensure normal messages aren't flagged."""

    @pytest.mark.parametrize(
        "message",
        [
            "Hello, how are you?",
            "What's on my calendar today?",
            "Can you help me with this task?",
            "Add a meeting for tomorrow",
            "I need to finish the report",
            "Thanks for your help",
            "Let me know when you're done",
            "That sounds good",
            "Sure, go ahead",
            "Please schedule a meeting with John",
            "What do you think about this idea?",
            "Can you summarize this document?",
        ],
    )
    def test_normal_messages_not_flagged(self, detector, message):
        """Normal messages should not be detected as explanation queries."""
        result = detector.detect(message)

        assert result.query_type == ExplanationQueryType.NOT_EXPLANATION_QUERY
        assert not result.is_explanation_query

    def test_questions_about_tasks_not_flagged(self, detector):
        """Questions about work tasks shouldn't trigger."""
        result = detector.detect("Why didn't the meeting get scheduled?")

        # This is about a task, not about Piper's behavior
        # It might match some patterns with low confidence
        # but should be below threshold or different category
        assert (
            result.query_type == ExplanationQueryType.NOT_EXPLANATION_QUERY
            or result.confidence < detector.CONFIDENCE_THRESHOLD
        )


class TestConfidenceLevels:
    """Tests for confidence level behavior."""

    def test_high_confidence_exact_phrases(self, detector):
        """Exact phrases should have high confidence."""
        result = detector.detect("Why did you do that?")
        assert result.confidence >= 0.85

    def test_lower_confidence_variations(self, detector):
        """Variations might have lower (but still valid) confidence."""
        result = detector.detect("Why would you assume that?")
        assert detector.CONFIDENCE_THRESHOLD <= result.confidence < 0.9

    def test_below_threshold_returns_not_query(self, detector):
        """Messages below threshold should return NOT_EXPLANATION_QUERY."""
        # This message is vague and shouldn't match with high confidence
        result = detector.detect("What's up?")

        # Even if it matches something, confidence should be low
        if result.query_type != ExplanationQueryType.NOT_EXPLANATION_QUERY:
            assert result.confidence < detector.CONFIDENCE_THRESHOLD


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_message(self, detector):
        """Should handle empty message."""
        result = detector.detect("")

        assert result.query_type == ExplanationQueryType.NOT_EXPLANATION_QUERY
        assert result.confidence == 0.0

    def test_none_message(self, detector):
        """Should handle None message."""
        result = detector.detect(None)

        assert result.query_type == ExplanationQueryType.NOT_EXPLANATION_QUERY
        assert result.confidence == 0.0

    def test_whitespace_only(self, detector):
        """Should handle whitespace-only message."""
        result = detector.detect("   ")

        assert result.query_type == ExplanationQueryType.NOT_EXPLANATION_QUERY

    def test_case_insensitive(self, detector):
        """Should match regardless of case."""
        lower = detector.detect("why did you do that?")
        upper = detector.detect("WHY DID YOU DO THAT?")
        mixed = detector.detect("Why Did You Do That?")

        assert lower.query_type == ExplanationQueryType.WHY_ACTION
        assert upper.query_type == ExplanationQueryType.WHY_ACTION
        assert mixed.query_type == ExplanationQueryType.WHY_ACTION

    def test_with_surrounding_text(self, detector):
        """Should detect queries within longer messages."""
        result = detector.detect("Hey, I was wondering, why did you do that earlier?")

        assert result.query_type == ExplanationQueryType.WHY_ACTION


class TestConvenienceMethods:
    """Tests for convenience methods."""

    def test_detect_why_action_returns_result_for_match(self, detector):
        """detect_why_action returns result when matched."""
        result = detector.detect_why_action("Why did you do that?")

        assert result is not None
        assert result.query_type == ExplanationQueryType.WHY_ACTION

    def test_detect_why_action_returns_none_for_no_match(self, detector):
        """detect_why_action returns None when not matched."""
        result = detector.detect_why_action("Hello there")

        assert result is None

    def test_detect_why_no_action_returns_result_for_match(self, detector):
        """detect_why_no_action returns result when matched."""
        result = detector.detect_why_no_action("Why are you so cautious?")

        assert result is not None
        assert result.query_type == ExplanationQueryType.WHY_NO_ACTION

    def test_detect_why_no_action_returns_none_for_no_match(self, detector):
        """detect_why_no_action returns None when not matched."""
        result = detector.detect_why_no_action("Hello there")

        assert result is None


class TestGetExampleQueries:
    """Tests for get_example_queries method."""

    def test_returns_examples_for_why_action(self, detector):
        """Should return examples for WHY_ACTION."""
        examples = detector.get_example_queries(ExplanationQueryType.WHY_ACTION)

        assert len(examples) > 0
        assert all(isinstance(e, str) for e in examples)

    def test_returns_examples_for_all_types(self, detector):
        """Should return examples for all query types."""
        for query_type in ExplanationQueryType:
            if query_type != ExplanationQueryType.NOT_EXPLANATION_QUERY:
                examples = detector.get_example_queries(query_type)
                assert len(examples) > 0

    def test_examples_are_actually_detected(self, detector):
        """Example queries should actually be detected as their type."""
        for query_type in ExplanationQueryType:
            if query_type == ExplanationQueryType.NOT_EXPLANATION_QUERY:
                continue

            examples = detector.get_example_queries(query_type)
            for example in examples:
                result = detector.detect(example)
                assert (
                    result.query_type == query_type
                ), f"Example '{example}' detected as {result.query_type} instead of {query_type}"


class TestDetectionResultProperties:
    """Tests for ExplanationDetectionResult properties."""

    def test_is_explanation_query_true_for_match(self, detector):
        """is_explanation_query should be True for matches."""
        result = detector.detect("Why did you do that?")
        assert result.is_explanation_query is True

    def test_is_explanation_query_false_for_no_match(self, detector):
        """is_explanation_query should be False for non-matches."""
        result = detector.detect("Hello there")
        assert result.is_explanation_query is False

    def test_matched_phrase_populated(self, detector):
        """matched_phrase should contain the matched text."""
        result = detector.detect("Why did you do that?")

        assert result.matched_phrase is not None
        assert "why did you" in result.matched_phrase.lower()

    def test_reasoning_populated(self, detector):
        """reasoning should explain the match."""
        result = detector.detect("Why did you do that?")

        assert result.reasoning is not None
        assert "pattern" in result.reasoning.lower()

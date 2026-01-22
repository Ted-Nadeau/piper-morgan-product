"""
Tests for FeedbackNarrativeBridge.

Issue #623: GRAMMAR-TRANSFORM: Feedback System
Phase 2: Narrative Bridge Tests
"""

import pytest

from services.feedback.narrative_bridge import FeedbackNarrativeBridge
from services.feedback.response_context import FeedbackResponseContext


class TestAcknowledgeFeedback:
    """Test basic feedback acknowledgment (non-first-time, non-repeat context)."""

    def test_bug_report(self):
        """Bug report acknowledgment."""
        bridge = FeedbackNarrativeBridge()
        # is_first_feedback=False but feedback_count=1 (not repeat contributor)
        ctx = FeedbackResponseContext(
            feedback_type="bug", is_first_feedback=False, feedback_count=1
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "flagging" in result
        assert "attention" in result

    def test_feature_request(self):
        """Feature request acknowledgment."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="feature", is_first_feedback=False, feedback_count=1
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "suggestion" in result.lower() or "noted" in result.lower()

    def test_ux_feedback(self):
        """UX feedback acknowledgment."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(feedback_type="ux", is_first_feedback=False, feedback_count=1)
        result = bridge.acknowledge_feedback(ctx)

        assert "experience" in result

    def test_general_feedback(self):
        """General feedback acknowledgment."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general", is_first_feedback=False, feedback_count=1
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "feedback" in result.lower()

    def test_unavailable(self):
        """Unavailable feedback system."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(feedback_available=False)
        result = bridge.acknowledge_feedback(ctx)

        assert "appreciate" in result.lower()


class TestFirstTimeContributor:
    """Test first-time contributor acknowledgments."""

    def test_first_bug_report(self):
        """First-time bug reporter."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="bug",
            is_first_feedback=True,
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "taking the time" in result

    def test_first_feature_request(self):
        """First-time feature suggester."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="feature",
            is_first_feedback=True,
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "first" in result.lower()

    def test_first_general_feedback(self):
        """First-time general feedback."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            is_first_feedback=True,
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "great to hear" in result.lower()


class TestRepeatContributor:
    """Test repeat contributor acknowledgments."""

    def test_repeat_bug_reporter(self):
        """Repeat bug reporter."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="bug",
            is_first_feedback=False,
            feedback_count=5,
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "again" in result.lower()

    def test_repeat_feature_suggester(self):
        """Repeat feature suggester."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="feature",
            is_first_feedback=False,
            feedback_count=3,
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "continuing" in result.lower() or "another" in result.lower()

    def test_repeat_general(self):
        """Repeat general feedback."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            is_first_feedback=False,
            feedback_count=10,
        )
        result = bridge.acknowledge_feedback(ctx)

        assert "valued" in result.lower() or "touch" in result.lower()


class TestAcknowledgeWithSentiment:
    """Test sentiment-aware acknowledgments."""

    def test_positive_sentiment(self):
        """Positive sentiment addition."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            sentiment="positive",
        )
        result = bridge.acknowledge_with_sentiment(ctx)

        assert "glad" in result.lower()

    def test_negative_sentiment(self):
        """Negative sentiment addition."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="bug",
            sentiment="negative",
        )
        result = bridge.acknowledge_with_sentiment(ctx)

        assert "frustration" in result.lower()

    def test_neutral_sentiment(self):
        """Neutral sentiment - no addition."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            sentiment="neutral",
        )
        result = bridge.acknowledge_with_sentiment(ctx)

        # Should just be base acknowledgment, no extra phrase
        assert "frustration" not in result.lower()
        assert result == bridge.acknowledge_feedback(ctx)


class TestAcknowledgeWithRating:
    """Test rating-aware acknowledgments."""

    def test_five_star(self):
        """5-star rating response."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            has_rating=True,
            rating_value=5,
        )
        result = bridge.acknowledge_with_rating(ctx)

        assert "glad" in result.lower()

    def test_four_star(self):
        """4-star rating response."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            has_rating=True,
            rating_value=4,
        )
        result = bridge.acknowledge_with_rating(ctx)

        assert "positive" in result.lower()

    def test_three_star(self):
        """3-star rating response."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            has_rating=True,
            rating_value=3,
        )
        result = bridge.acknowledge_with_rating(ctx)

        assert "honest" in result.lower()

    def test_two_star(self):
        """2-star rating response."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="ux",
            has_rating=True,
            rating_value=2,
        )
        result = bridge.acknowledge_with_rating(ctx)

        assert "improve" in result.lower()

    def test_one_star(self):
        """1-star rating response."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="ux",
            has_rating=True,
            rating_value=1,
        )
        result = bridge.acknowledge_with_rating(ctx)

        assert "sorry" in result.lower()

    def test_no_rating(self):
        """No rating - just base acknowledgment."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="general",
            has_rating=False,
        )
        result = bridge.acknowledge_with_rating(ctx)

        # Should just be base acknowledgment
        assert result == bridge.acknowledge_feedback(ctx)


class TestNarrateFeedbackType:
    """Test feedback type narration."""

    def test_bug(self):
        """Bug type narration."""
        bridge = FeedbackNarrativeBridge()
        result = bridge.narrate_feedback_type("bug")

        assert result == "bug report"

    def test_feature(self):
        """Feature type narration."""
        bridge = FeedbackNarrativeBridge()
        result = bridge.narrate_feedback_type("feature")

        assert result == "feature suggestion"

    def test_ux(self):
        """UX type narration."""
        bridge = FeedbackNarrativeBridge()
        result = bridge.narrate_feedback_type("ux")

        assert result == "experience feedback"

    def test_general(self):
        """General type narration."""
        bridge = FeedbackNarrativeBridge()
        result = bridge.narrate_feedback_type("general")

        assert result == "feedback"

    def test_unknown(self):
        """Unknown type defaults to feedback."""
        bridge = FeedbackNarrativeBridge()
        result = bridge.narrate_feedback_type("unknown")

        assert result == "feedback"


class TestNarrateContributorStatus:
    """Test contributor status narration."""

    def test_first_time(self):
        """First-time contributor."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(is_first_feedback=True)
        result = bridge.narrate_contributor_status(ctx)

        assert "first time" in result.lower()

    def test_repeat_with_count(self):
        """Repeat contributor with count."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            is_first_feedback=False,
            feedback_count=5,
        )
        result = bridge.narrate_contributor_status(ctx)

        assert "5" in result


class TestNarrateDetailedResponse:
    """Test detailed response generation."""

    def test_bug_with_sentiment(self):
        """Detailed bug report response with negative sentiment."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="bug",
            sentiment="negative",
        )
        result = bridge.narrate_detailed_response(ctx)

        assert "bug report" in result.lower()
        assert "attention" in result.lower()
        assert "frustration" in result.lower()

    def test_feature_positive(self):
        """Detailed feature request with positive sentiment."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="feature",
            sentiment="positive",
        )
        result = bridge.narrate_detailed_response(ctx)

        assert "feature suggestion" in result.lower()
        assert "glad" in result.lower()

    def test_without_type(self):
        """Detailed response without type mention."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(feedback_type="general")
        result = bridge.narrate_detailed_response(ctx, include_type=False)

        assert "Thanks!" in result
        assert "general" not in result.lower()

    def test_without_sentiment(self):
        """Detailed response without sentiment."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="bug",
            sentiment="negative",
        )
        result = bridge.narrate_detailed_response(ctx, include_sentiment=False)

        assert "frustration" not in result.lower()

    def test_unavailable(self):
        """Detailed response when unavailable."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(feedback_available=False)
        result = bridge.narrate_detailed_response(ctx)

        assert "appreciate" in result.lower()


class TestContractorTest:
    """Verify narratives pass the Contractor Test."""

    def test_no_raw_data_terms(self):
        """Narratives don't use raw data terms."""
        bridge = FeedbackNarrativeBridge()
        ctx = FeedbackResponseContext(
            feedback_type="bug",
            sentiment="negative",
            has_rating=True,
            rating_value=2,
        )

        result = bridge.acknowledge_with_sentiment(ctx)

        # Should NOT contain these data-y terms
        assert "feedback_type" not in result
        assert "sentiment" not in result
        assert "rating_value" not in result

    def test_natural_language(self):
        """Narratives use natural language."""
        bridge = FeedbackNarrativeBridge()

        # Each narrative should read naturally
        bug_ack = bridge.acknowledge_feedback(FeedbackResponseContext(feedback_type="bug"))
        assert bug_ack[0].isupper()  # Proper capitalization
        assert "!!!" not in bug_ack  # Not over-excited

    def test_professional_warmth(self):
        """Narratives balance professionalism and warmth."""
        bridge = FeedbackNarrativeBridge()

        # Bug reports are professional
        bug = bridge.acknowledge_feedback(
            FeedbackResponseContext(feedback_type="bug", sentiment="negative")
        )
        assert "Thanks" in bug  # Appreciative

        # Positive feedback is warm
        positive = bridge.acknowledge_with_sentiment(FeedbackResponseContext(sentiment="positive"))
        assert "glad" in positive.lower()

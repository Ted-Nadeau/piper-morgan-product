"""
Tests for Feedback narrative helpers.

Issue #623: GRAMMAR-TRANSFORM: Feedback System
Phase 3: Helper Integration Tests
"""

import pytest

from services.feedback.models import Feedback
from services.feedback.narrative_helpers import (
    acknowledge_feedback,
    acknowledge_feedback_with_rating,
    acknowledge_feedback_with_sentiment,
    get_feedback_formality,
    is_detailed_feedback,
    is_negative_feedback,
    narrate_feedback_type,
)


class TestAcknowledgeFeedback:
    """Test acknowledge_feedback helper."""

    def test_with_feedback_model(self):
        """Acknowledge from Feedback model."""
        feedback = Feedback(
            session_id="test",
            feedback_type="bug",
            comment="Something broken",
        )
        result = acknowledge_feedback(feedback=feedback)

        assert "Thanks" in result

    def test_with_dict(self):
        """Acknowledge from dictionary."""
        data = {"feedback_type": "feature", "comment": "Add dark mode"}
        result = acknowledge_feedback(feedback_data=data)

        assert "Thanks" in result

    def test_with_nothing(self):
        """Acknowledge with no data."""
        result = acknowledge_feedback()

        assert "appreciate" in result.lower()

    def test_with_user_count(self):
        """Acknowledge with user feedback count."""
        feedback = Feedback(
            session_id="test",
            feedback_type="general",
            comment="Nice!",
        )
        result = acknowledge_feedback(feedback=feedback, user_feedback_count=5)

        # Should use repeat contributor message
        assert "Thanks" in result


class TestAcknowledgeWithSentiment:
    """Test acknowledge_feedback_with_sentiment helper."""

    def test_positive_sentiment(self):
        """Positive sentiment response."""
        feedback = Feedback(
            session_id="test",
            feedback_type="general",
            comment="Love it!",
            sentiment_score=0.9,
        )
        result = acknowledge_feedback_with_sentiment(feedback=feedback)

        assert "glad" in result.lower()

    def test_negative_sentiment(self):
        """Negative sentiment response."""
        data = {"feedback_type": "bug", "comment": "Broken", "sentiment_score": -0.8}
        result = acknowledge_feedback_with_sentiment(feedback_data=data)

        assert "frustration" in result.lower()


class TestAcknowledgeWithRating:
    """Test acknowledge_feedback_with_rating helper."""

    def test_high_rating(self):
        """High rating response."""
        feedback = Feedback(
            session_id="test",
            feedback_type="general",
            comment="Great!",
            rating=5,
        )
        result = acknowledge_feedback_with_rating(feedback=feedback)

        assert "glad" in result.lower()

    def test_low_rating(self):
        """Low rating response."""
        data = {"feedback_type": "ux", "comment": "Bad", "rating": 1}
        result = acknowledge_feedback_with_rating(feedback_data=data)

        assert "sorry" in result.lower()


class TestNarrateFeedbackType:
    """Test narrate_feedback_type helper."""

    def test_bug(self):
        """Bug type."""
        result = narrate_feedback_type("bug")
        assert result == "bug report"

    def test_feature(self):
        """Feature type."""
        result = narrate_feedback_type("feature")
        assert result == "feature suggestion"

    def test_ux(self):
        """UX type."""
        result = narrate_feedback_type("ux")
        assert result == "experience feedback"


class TestGetFeedbackFormality:
    """Test get_feedback_formality helper."""

    def test_bug_professional(self):
        """Bug report -> professional."""
        feedback = Feedback(
            session_id="test",
            feedback_type="bug",
            comment="Error",
        )
        result = get_feedback_formality(feedback=feedback)

        assert result == "professional"

    def test_negative_professional(self):
        """Negative sentiment -> professional."""
        data = {"feedback_type": "general", "sentiment_score": -0.5}
        result = get_feedback_formality(feedback_data=data)

        assert result == "professional"

    def test_positive_warm(self):
        """Positive sentiment -> warm."""
        data = {"feedback_type": "general", "sentiment_score": 0.8}
        result = get_feedback_formality(feedback_data=data)

        assert result == "warm"

    def test_neutral_conversational(self):
        """Neutral -> conversational."""
        feedback = Feedback(
            session_id="test",
            feedback_type="general",
            comment="Okay",
        )
        result = get_feedback_formality(feedback=feedback)

        assert result == "conversational"

    def test_no_data_conversational(self):
        """No data -> conversational default."""
        result = get_feedback_formality()

        assert result == "conversational"


class TestIsNegativeFeedback:
    """Test is_negative_feedback helper."""

    def test_negative(self):
        """Negative feedback."""
        feedback = Feedback(
            session_id="test",
            feedback_type="bug",
            comment="Terrible",
            sentiment_score=-0.7,
        )
        assert is_negative_feedback(feedback=feedback) is True

    def test_not_negative(self):
        """Not negative feedback."""
        data = {"feedback_type": "general", "sentiment_score": 0.5}
        assert is_negative_feedback(feedback_data=data) is False

    def test_no_data(self):
        """No data -> False."""
        assert is_negative_feedback() is False


class TestIsDetailedFeedback:
    """Test is_detailed_feedback helper."""

    def test_has_rating(self):
        """Detailed if has rating."""
        feedback = Feedback(
            session_id="test",
            feedback_type="general",
            comment="Good",
            rating=4,
        )
        assert is_detailed_feedback(feedback=feedback) is True

    def test_long_comment(self):
        """Detailed if long comment."""
        data = {
            "feedback_type": "feature",
            "comment": "This is a detailed suggestion with many words explaining the feature",
        }
        assert is_detailed_feedback(feedback_data=data) is True

    def test_short_no_rating(self):
        """Not detailed if short and no rating."""
        feedback = Feedback(
            session_id="test",
            feedback_type="general",
            comment="Ok",
        )
        assert is_detailed_feedback(feedback=feedback) is False


class TestContractorTest:
    """Verify helpers pass Contractor Test."""

    def test_no_raw_data_in_output(self):
        """Helpers don't expose raw data."""
        feedback = Feedback(
            session_id="test-session-id",
            feedback_type="bug",
            comment="Error occurred",
            rating=2,
            sentiment_score=-0.5,
        )

        result = acknowledge_feedback_with_sentiment(feedback=feedback)

        # No raw data terms
        assert "feedback_type" not in result
        assert "sentiment_score" not in result
        assert "test-session-id" not in result

    def test_professional_language(self):
        """Helpers use professional language."""
        feedback = Feedback(
            session_id="test",
            feedback_type="general",
            comment="Test",
        )

        result = acknowledge_feedback(feedback=feedback)

        assert result[0].isupper()  # Proper capitalization
        assert "!!!" not in result  # Not overly excited

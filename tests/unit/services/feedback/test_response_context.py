"""
Tests for FeedbackResponseContext.

Issue #623: GRAMMAR-TRANSFORM: Feedback System
Phase 1: Response Context Tests
"""

from uuid import uuid4

import pytest

from services.feedback.models import Feedback
from services.feedback.response_context import FeedbackResponseContext


class TestFromFeedback:
    """Test building context from Feedback domain model."""

    def test_basic_feedback(self):
        """Build from basic feedback."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="general",
            comment="Good job!",
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.feedback_type == "general"
        assert ctx.feedback_available is True

    def test_bug_report(self):
        """Build from bug report."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="bug",
            comment="The button doesn't work",
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.feedback_type == "bug"
        assert ctx.is_bug_report() is True

    def test_feature_request(self):
        """Build from feature request."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="feature",
            comment="Would be nice to have dark mode",
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.feedback_type == "feature"
        assert ctx.is_feature_request() is True

    def test_with_rating(self):
        """Build with rating provided."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="general",
            comment="Great!",
            rating=5,
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.has_rating is True
        assert ctx.rating_value == 5

    def test_positive_sentiment(self):
        """Build with positive sentiment."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="general",
            comment="Love it!",
            sentiment_score=0.8,
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.sentiment == "positive"
        assert ctx.is_positive() is True

    def test_negative_sentiment(self):
        """Build with negative sentiment."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="bug",
            comment="This is frustrating",
            sentiment_score=-0.6,
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.sentiment == "negative"
        assert ctx.is_negative() is True

    def test_neutral_sentiment(self):
        """Build with neutral sentiment."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="general",
            comment="It works",
            sentiment_score=0.1,
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.sentiment == "neutral"
        assert ctx.is_positive() is False
        assert ctx.is_negative() is False

    def test_detailed_comment(self):
        """Build with detailed comment."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="feature",
            comment="I really think this would help productivity significantly",
        )
        ctx = FeedbackResponseContext.from_feedback(feedback)

        assert ctx.has_detailed_comment is True
        assert ctx.is_detailed() is True

    def test_first_feedback(self):
        """Build for first-time feedback."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="general",
            comment="Hello!",
        )
        ctx = FeedbackResponseContext.from_feedback(feedback, user_feedback_count=1)

        assert ctx.is_first_feedback is True
        assert ctx.is_repeat_contributor() is False

    def test_repeat_contributor(self):
        """Build for repeat feedback contributor."""
        feedback = Feedback(
            session_id="test-session",
            feedback_type="general",
            comment="Another suggestion",
        )
        ctx = FeedbackResponseContext.from_feedback(feedback, user_feedback_count=5)

        assert ctx.is_first_feedback is False
        assert ctx.feedback_count == 5
        assert ctx.is_repeat_contributor() is True


class TestFromDict:
    """Test building context from dictionary."""

    def test_empty_dict(self):
        """Empty dict returns unavailable."""
        ctx = FeedbackResponseContext.from_dict({})

        assert ctx.feedback_available is False

    def test_none_returns_unavailable(self):
        """None returns unavailable."""
        ctx = FeedbackResponseContext.from_dict(None)

        assert ctx.feedback_available is False

    def test_basic_dict(self):
        """Build from basic dict."""
        data = {
            "feedback_type": "ux",
            "comment": "Navigation is confusing",
        }
        ctx = FeedbackResponseContext.from_dict(data)

        assert ctx.feedback_type == "ux"
        assert ctx.feedback_available is True

    def test_dict_with_sentiment(self):
        """Build from dict with sentiment score."""
        data = {
            "feedback_type": "general",
            "comment": "Great!",
            "sentiment_score": 0.9,
        }
        ctx = FeedbackResponseContext.from_dict(data)

        assert ctx.sentiment == "positive"

    def test_dict_with_rating(self):
        """Build from dict with rating."""
        data = {
            "feedback_type": "general",
            "comment": "Okay",
            "rating": 3,
        }
        ctx = FeedbackResponseContext.from_dict(data)

        assert ctx.has_rating is True
        assert ctx.rating_value == 3


class TestUnavailable:
    """Test unavailable factory."""

    def test_unavailable(self):
        """Create unavailable context."""
        ctx = FeedbackResponseContext.unavailable()

        assert ctx.feedback_available is False


class TestFormality:
    """Test formality detection."""

    def test_bug_report_professional(self):
        """Bug reports get professional tone."""
        ctx = FeedbackResponseContext(feedback_type="bug")

        assert ctx.get_formality() == "professional"

    def test_negative_professional(self):
        """Negative sentiment gets professional tone."""
        ctx = FeedbackResponseContext(sentiment="negative")

        assert ctx.get_formality() == "professional"

    def test_positive_warm(self):
        """Positive sentiment gets warm tone."""
        ctx = FeedbackResponseContext(sentiment="positive")

        assert ctx.get_formality() == "warm"

    def test_neutral_conversational(self):
        """Neutral sentiment gets conversational tone."""
        ctx = FeedbackResponseContext(sentiment="neutral", feedback_type="general")

        assert ctx.get_formality() == "conversational"

    def test_feature_request_conversational(self):
        """Feature requests get conversational tone."""
        ctx = FeedbackResponseContext(feedback_type="feature", sentiment="neutral")

        assert ctx.get_formality() == "conversational"


class TestHelperMethods:
    """Test helper methods."""

    def test_is_detailed_with_rating(self):
        """Detailed if has rating."""
        ctx = FeedbackResponseContext(has_rating=True)

        assert ctx.is_detailed() is True

    def test_is_detailed_with_comment(self):
        """Detailed if has detailed comment."""
        ctx = FeedbackResponseContext(has_detailed_comment=True)

        assert ctx.is_detailed() is True

    def test_not_detailed(self):
        """Not detailed without rating or long comment."""
        ctx = FeedbackResponseContext()

        assert ctx.is_detailed() is False

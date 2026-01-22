"""
Feedback Response Context - Rich context for grammar-conscious feedback responses.

This module provides the context bridge between raw feedback data
and grammar-conscious narrative generation.

Issue #623: GRAMMAR-TRANSFORM: Feedback System
Phase 1: Response Context
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from services.feedback.models import Feedback


@dataclass
class FeedbackResponseContext:
    """Rich context for grammar-conscious feedback responses.

    In MUX grammar: captures the Moment of a user sharing feedback.
    This is a connection moment - user trusting Piper with input.

    Attributes:
        feedback_type: Type of feedback (bug, feature, ux, general)
        sentiment: Detected sentiment (positive, negative, neutral)
        has_rating: Whether user provided a rating
        rating_value: The actual rating (1-5) if provided
        is_first_feedback: Whether this is user's first feedback
        feedback_count: Total feedback from this user
        feedback_available: Whether feedback data is available
    """

    # Feedback classification
    feedback_type: str = "general"  # "bug", "feature", "ux", "general"
    sentiment: str = "neutral"  # "positive", "negative", "neutral"

    # User engagement
    has_rating: bool = False
    rating_value: Optional[int] = None  # 1-5
    has_detailed_comment: bool = False

    # User relationship
    is_first_feedback: bool = True
    feedback_count: int = 0

    # System state
    feedback_available: bool = True

    @classmethod
    def from_feedback(
        cls,
        feedback: Feedback,
        user_feedback_count: int = 0,
    ) -> "FeedbackResponseContext":
        """Build context from Feedback domain model.

        Args:
            feedback: Feedback domain model
            user_feedback_count: Total feedback count for this user

        Returns:
            FeedbackResponseContext with populated fields
        """
        # Determine sentiment from score or default
        sentiment = "neutral"
        if feedback.sentiment_score is not None:
            if feedback.sentiment_score > 0.2:
                sentiment = "positive"
            elif feedback.sentiment_score < -0.2:
                sentiment = "negative"

        # Check for detailed comment (more than 20 chars)
        has_detailed = len(feedback.comment) > 20 if feedback.comment else False

        return cls(
            feedback_type=feedback.feedback_type,
            sentiment=sentiment,
            has_rating=feedback.rating is not None,
            rating_value=feedback.rating,
            has_detailed_comment=has_detailed,
            is_first_feedback=user_feedback_count <= 1,
            feedback_count=user_feedback_count,
            feedback_available=True,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FeedbackResponseContext":
        """Build context from dictionary data.

        Args:
            data: Dictionary with feedback data

        Returns:
            FeedbackResponseContext with populated fields
        """
        if not data:
            return cls(feedback_available=False)

        # Extract sentiment
        sentiment = "neutral"
        sentiment_score = data.get("sentiment_score")
        if sentiment_score is not None:
            if sentiment_score > 0.2:
                sentiment = "positive"
            elif sentiment_score < -0.2:
                sentiment = "negative"

        # Extract rating
        rating = data.get("rating")
        has_rating = rating is not None

        # Check comment detail
        comment = data.get("comment", "")
        has_detailed = len(comment) > 20 if comment else False

        return cls(
            feedback_type=data.get("feedback_type", "general"),
            sentiment=sentiment,
            has_rating=has_rating,
            rating_value=rating,
            has_detailed_comment=has_detailed,
            is_first_feedback=data.get("is_first_feedback", True),
            feedback_count=data.get("feedback_count", 0),
            feedback_available=True,
        )

    @classmethod
    def unavailable(cls) -> "FeedbackResponseContext":
        """Create context for unavailable feedback system."""
        return cls(feedback_available=False)

    def is_positive(self) -> bool:
        """Check if feedback sentiment is positive."""
        return self.sentiment == "positive"

    def is_negative(self) -> bool:
        """Check if feedback sentiment is negative."""
        return self.sentiment == "negative"

    def is_detailed(self) -> bool:
        """Check if user provided detailed feedback."""
        return self.has_detailed_comment or self.has_rating

    def is_bug_report(self) -> bool:
        """Check if this is a bug report."""
        return self.feedback_type == "bug"

    def is_feature_request(self) -> bool:
        """Check if this is a feature request."""
        return self.feedback_type == "feature"

    def is_repeat_contributor(self) -> bool:
        """Check if user has given feedback before."""
        return not self.is_first_feedback and self.feedback_count > 1

    def get_formality(self) -> str:
        """Get appropriate formality based on feedback context.

        Bug reports -> professional (user frustrated)
        Feature requests -> conversational (user engaged)
        Negative sentiment -> professional (address concerns)
        Positive sentiment -> warm (celebrate connection)

        Returns:
            "professional", "conversational", or "warm"
        """
        if self.is_bug_report() or self.is_negative():
            return "professional"
        elif self.is_positive():
            return "warm"
        else:
            return "conversational"

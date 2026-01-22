"""
Feedback Narrative Helpers for Canonical Handlers.

This module provides helper functions to transform raw feedback data
into grammar-conscious narratives within canonical handlers.

Issue #623: GRAMMAR-TRANSFORM: Feedback System
Phase 3: Helper Integration
"""

from typing import Any, Dict, Optional

from services.feedback.models import Feedback
from services.feedback.narrative_bridge import FeedbackNarrativeBridge
from services.feedback.response_context import FeedbackResponseContext

# Singleton bridge instance
_narrative_bridge = FeedbackNarrativeBridge()


def acknowledge_feedback(
    feedback: Optional[Feedback] = None,
    feedback_data: Optional[Dict[str, Any]] = None,
    user_feedback_count: int = 0,
) -> str:
    """Generate warm acknowledgment for submitted feedback.

    Args:
        feedback: Feedback domain model (preferred)
        feedback_data: Dictionary with feedback data (alternative)
        user_feedback_count: Total feedback from this user

    Returns:
        Human-readable acknowledgment string

    Example:
        Input: Feedback(feedback_type="bug", comment="Button broken")
        Output: "Thanks for flagging that - I'll make sure this gets attention"
    """
    if feedback:
        ctx = FeedbackResponseContext.from_feedback(feedback, user_feedback_count)
    elif feedback_data:
        ctx = FeedbackResponseContext.from_dict(feedback_data)
    else:
        ctx = FeedbackResponseContext.unavailable()

    return _narrative_bridge.acknowledge_feedback(ctx)


def acknowledge_feedback_with_sentiment(
    feedback: Optional[Feedback] = None,
    feedback_data: Optional[Dict[str, Any]] = None,
    user_feedback_count: int = 0,
) -> str:
    """Generate acknowledgment with sentiment-aware addition.

    Args:
        feedback: Feedback domain model (preferred)
        feedback_data: Dictionary with feedback data (alternative)
        user_feedback_count: Total feedback from this user

    Returns:
        Human-readable acknowledgment with sentiment response

    Example:
        Input: Feedback with negative sentiment
        Output: "Thanks for flagging that. I hear your frustration - we'll look into this."
    """
    if feedback:
        ctx = FeedbackResponseContext.from_feedback(feedback, user_feedback_count)
    elif feedback_data:
        ctx = FeedbackResponseContext.from_dict(feedback_data)
    else:
        ctx = FeedbackResponseContext.unavailable()

    return _narrative_bridge.acknowledge_with_sentiment(ctx)


def acknowledge_feedback_with_rating(
    feedback: Optional[Feedback] = None,
    feedback_data: Optional[Dict[str, Any]] = None,
    user_feedback_count: int = 0,
) -> str:
    """Generate acknowledgment with rating-specific response.

    Args:
        feedback: Feedback domain model (preferred)
        feedback_data: Dictionary with feedback data (alternative)
        user_feedback_count: Total feedback from this user

    Returns:
        Human-readable acknowledgment with rating response

    Example:
        Input: Feedback with 5-star rating
        Output: "Thanks! I'm glad you're enjoying the experience!"
    """
    if feedback:
        ctx = FeedbackResponseContext.from_feedback(feedback, user_feedback_count)
    elif feedback_data:
        ctx = FeedbackResponseContext.from_dict(feedback_data)
    else:
        ctx = FeedbackResponseContext.unavailable()

    return _narrative_bridge.acknowledge_with_rating(ctx)


def narrate_feedback_type(feedback_type: str) -> str:
    """Describe feedback type in human terms.

    Args:
        feedback_type: Type string (bug, feature, ux, general)

    Returns:
        Human-readable type description

    Example:
        Input: "bug"
        Output: "bug report"
    """
    return _narrative_bridge.narrate_feedback_type(feedback_type)


def get_feedback_formality(
    feedback: Optional[Feedback] = None,
    feedback_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Get appropriate formality based on feedback context.

    Bug reports / negative -> professional
    Feature requests / neutral -> conversational
    Positive feedback -> warm

    Args:
        feedback: Feedback domain model (preferred)
        feedback_data: Dictionary with feedback data (alternative)

    Returns:
        "professional", "conversational", or "warm"
    """
    if feedback:
        ctx = FeedbackResponseContext.from_feedback(feedback)
    elif feedback_data:
        ctx = FeedbackResponseContext.from_dict(feedback_data)
    else:
        return "conversational"

    return ctx.get_formality()


def is_negative_feedback(
    feedback: Optional[Feedback] = None,
    feedback_data: Optional[Dict[str, Any]] = None,
) -> bool:
    """Check if feedback has negative sentiment.

    Args:
        feedback: Feedback domain model (preferred)
        feedback_data: Dictionary with feedback data (alternative)

    Returns:
        True if negative sentiment
    """
    if feedback:
        ctx = FeedbackResponseContext.from_feedback(feedback)
    elif feedback_data:
        ctx = FeedbackResponseContext.from_dict(feedback_data)
    else:
        return False

    return ctx.is_negative()


def is_detailed_feedback(
    feedback: Optional[Feedback] = None,
    feedback_data: Optional[Dict[str, Any]] = None,
) -> bool:
    """Check if user provided detailed feedback.

    Detailed = has rating OR has long comment (>20 chars)

    Args:
        feedback: Feedback domain model (preferred)
        feedback_data: Dictionary with feedback data (alternative)

    Returns:
        True if detailed feedback
    """
    if feedback:
        ctx = FeedbackResponseContext.from_feedback(feedback)
    elif feedback_data:
        ctx = FeedbackResponseContext.from_dict(feedback_data)
    else:
        return False

    return ctx.is_detailed()

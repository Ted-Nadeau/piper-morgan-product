"""
Feedback Service
Captures and processes user corrections for learning
"""

from .capture import FeedbackCapture
from .narrative_bridge import FeedbackNarrativeBridge
from .narrative_helpers import (
    acknowledge_feedback,
    acknowledge_feedback_with_rating,
    acknowledge_feedback_with_sentiment,
    get_feedback_formality,
    is_detailed_feedback,
    is_negative_feedback,
    narrate_feedback_type,
)

# Issue #623: Grammar-conscious response components
from .response_context import FeedbackResponseContext

# Note: We'll create the global instance in main.py after Redis is initialized
# since FeedbackCapture requires a Redis connection

__all__ = [
    # Capture
    "FeedbackCapture",
    # Response context
    "FeedbackResponseContext",
    "FeedbackNarrativeBridge",
    # Narrative helpers
    "acknowledge_feedback",
    "acknowledge_feedback_with_sentiment",
    "acknowledge_feedback_with_rating",
    "narrate_feedback_type",
    "get_feedback_formality",
    "is_negative_feedback",
    "is_detailed_feedback",
]

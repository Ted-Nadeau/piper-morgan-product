"""
Recognition Feedback Recording.

Records user selections from recognition options for future analysis.
Part of #412 MUX-INTERACT-INTENT-BRIDGE.

This module captures valuable training signals:
- Which intents are commonly confused
- Which recognition options users select
- Patterns that indicate specific intent types

Storage: Structured logging (MVP approach).
Future: Could be extended to database storage for querying.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class FeedbackContext:
    """
    Context for feedback recording, captured at recognition trigger time.

    This is created when recognition triggers and passed through to the
    handler so we can record what the original situation was.
    """

    original_message: str
    confidence_at_trigger: float
    user_id: Optional[str] = None


@dataclass
class RecognitionFeedback:
    """
    Record of user recognition selection.

    Captures what options were offered and what the user selected,
    along with context about the original recognition trigger.
    """

    # What triggered recognition
    original_message: str
    confidence_at_trigger: float

    # What was offered
    offered_options: List[str]  # intent_hints that were offered

    # What user did
    selected_option: str  # intent_hint selected, or "none_of_these"/"unrelated_input"
    selection_type: str  # "matched" | "none_of_these" | "no_match"

    # Context
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# Selection type constants
SELECTION_MATCHED = "matched"
SELECTION_NONE_OF_THESE = "none_of_these"
SELECTION_NO_MATCH = "no_match"

# Sentinel values for selected_option when not a real option
SELECTED_NONE_OF_THESE = "none_of_these"
SELECTED_UNRELATED_INPUT = "unrelated_input"


def record_recognition_feedback(feedback: RecognitionFeedback) -> None:
    """
    Record recognition feedback via structured logging.

    This creates a structured log entry that can be:
    - Grepped from logs for analysis
    - Piped to analytics systems
    - Queried if logs are stored in a searchable system

    Args:
        feedback: The feedback record to log
    """
    logger.info(
        "recognition_feedback",
        original_message=feedback.original_message,
        confidence_at_trigger=feedback.confidence_at_trigger,
        offered_options=feedback.offered_options,
        selected_option=feedback.selected_option,
        selection_type=feedback.selection_type,
        user_id=feedback.user_id,
        timestamp=feedback.timestamp.isoformat() if feedback.timestamp else None,
    )


def create_feedback_from_match(
    context: FeedbackContext,
    offered_options: List[str],
    selected_intent_hint: str,
) -> RecognitionFeedback:
    """
    Create feedback record for a successful match.

    Args:
        context: The feedback context from recognition trigger
        offered_options: List of intent_hints that were offered
        selected_intent_hint: The intent_hint the user selected

    Returns:
        RecognitionFeedback ready to record
    """
    return RecognitionFeedback(
        original_message=context.original_message,
        confidence_at_trigger=context.confidence_at_trigger,
        offered_options=offered_options,
        selected_option=selected_intent_hint,
        selection_type=SELECTION_MATCHED,
        user_id=context.user_id,
    )


def create_feedback_from_none_of_these(
    context: FeedbackContext,
    offered_options: List[str],
) -> RecognitionFeedback:
    """
    Create feedback record for "none of these" selection.

    Args:
        context: The feedback context from recognition trigger
        offered_options: List of intent_hints that were offered

    Returns:
        RecognitionFeedback ready to record
    """
    return RecognitionFeedback(
        original_message=context.original_message,
        confidence_at_trigger=context.confidence_at_trigger,
        offered_options=offered_options,
        selected_option=SELECTED_NONE_OF_THESE,
        selection_type=SELECTION_NONE_OF_THESE,
        user_id=context.user_id,
    )


def create_feedback_from_no_match(
    context: FeedbackContext,
    offered_options: List[str],
) -> RecognitionFeedback:
    """
    Create feedback record for unrelated input (no match).

    This is when the user says something that doesn't match any option
    and isn't "none of these" - they're asking about something else entirely.

    Args:
        context: The feedback context from recognition trigger
        offered_options: List of intent_hints that were offered

    Returns:
        RecognitionFeedback ready to record
    """
    return RecognitionFeedback(
        original_message=context.original_message,
        confidence_at_trigger=context.confidence_at_trigger,
        offered_options=offered_options,
        selected_option=SELECTED_UNRELATED_INPUT,
        selection_type=SELECTION_NO_MATCH,
        user_id=context.user_id,
    )

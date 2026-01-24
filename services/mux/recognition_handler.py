"""
Recognition Selection Handler.

Handles user responses to recognition options.
Part of #411 MUX-INTERACT-RECOGNITION.
Feedback recording added in #412.

This module processes the second turn of a recognition conversation:
Turn 1: Piper offers recognition options
Turn 2: User selects an option (or "none of these")
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import structlog

from services.domain.models import Intent, IntentCategory
from services.mux.orientation import ArticulationConfig, ChannelType, RecognitionOptions
from services.mux.recognition_feedback import (
    FeedbackContext,
    create_feedback_from_match,
    create_feedback_from_no_match,
    create_feedback_from_none_of_these,
    record_recognition_feedback,
)
from services.mux.recognition_response import (
    RecognitionResponseService,
    SelectionMatch,
    SelectionResult,
)

logger = structlog.get_logger(__name__)


class RecognitionState(Enum):
    """State of recognition conversation."""

    NORMAL = "normal"  # No recognition active
    RECOGNITION_OFFERED = "offered"  # Options were shown, waiting for selection
    CLARIFYING = "clarifying"  # User said "none", asking for clarification


@dataclass
class RecognitionHandlerResult:
    """Result of handling a recognition selection."""

    # What happened
    state_transition: str  # "OFFERED → NORMAL" etc.
    selection_result: SelectionResult

    # What to do next
    should_route_to_handler: bool
    intent_hint: Optional[str] = None  # Intent to route to if should_route_to_handler

    # Response to show user
    response_text: Optional[str] = None

    # Trust implications
    trust_penalty: bool = False  # Never penalize for clarification


class RecognitionHandler:
    """
    Handles user selection from recognition options.

    This is called when:
    1. Recognition was offered (state = RECOGNITION_OFFERED)
    2. User sends a follow-up message

    The handler matches the message to offered options and either:
    - Routes to the selected intent handler
    - Prompts for clarification if "none of these"
    - Re-shows options if input is empty/unclear
    """

    def __init__(self):
        """Initialize handler."""
        self.response_service = RecognitionResponseService

    def handle_selection(
        self,
        user_message: str,
        offered_options: RecognitionOptions,
        config: Optional[ArticulationConfig] = None,
        feedback_context: Optional[FeedbackContext] = None,
    ) -> RecognitionHandlerResult:
        """
        Handle user's selection from recognition options.

        Args:
            user_message: User's response to the options
            offered_options: The RecognitionOptions that were offered
            config: Articulation config for response formatting
            feedback_context: Optional context for recording feedback (#412).
                              When provided, selection feedback is logged.

        Returns:
            RecognitionHandlerResult with routing decision
        """
        if config is None:
            config = ArticulationConfig()

        # Extract intent hints for feedback recording
        option_hints = [opt.intent_hint for opt in offered_options.options]

        # Try to match the selection
        match = self.response_service.handle_selection(
            selection=user_message,
            options=offered_options,
        )

        logger.debug(
            "recognition_selection_match",
            user_message=user_message,
            result=match.result.value,
            matched_option=match.matched_option.label if match.matched_option else None,
        )

        # Handle based on match result
        if match.result == SelectionResult.MATCHED:
            return self._handle_matched_selection(match, config, feedback_context, option_hints)

        elif match.result == SelectionResult.NONE_OF_THESE:
            return self._handle_none_of_these(config, feedback_context, option_hints)

        elif match.result == SelectionResult.NO_MATCH:
            return self._handle_no_match(
                user_message, offered_options, config, feedback_context, option_hints
            )

        elif match.result == SelectionResult.NUMERIC_OUT_OF_RANGE:
            return self._handle_out_of_range(offered_options, config)

        else:
            # Shouldn't happen, but handle gracefully
            return self._handle_no_match(
                user_message, offered_options, config, feedback_context, option_hints
            )

    def _handle_matched_selection(
        self,
        match: SelectionMatch,
        config: ArticulationConfig,
        feedback_context: Optional[FeedbackContext],
        option_hints: List[str],
    ) -> RecognitionHandlerResult:
        """Handle successful option selection."""
        # Record feedback if context provided (#412)
        if feedback_context:
            feedback = create_feedback_from_match(
                context=feedback_context,
                offered_options=option_hints,
                selected_intent_hint=match.intent_hint,
            )
            record_recognition_feedback(feedback)

        # Get acknowledgment
        ack = self.response_service.get_selection_acknowledgment(
            matched_option=match.matched_option,
            config=config,
        )

        return RecognitionHandlerResult(
            state_transition="RECOGNITION_OFFERED → NORMAL",
            selection_result=SelectionResult.MATCHED,
            should_route_to_handler=True,
            intent_hint=match.intent_hint,
            response_text=ack,
            trust_penalty=False,
        )

    def _handle_none_of_these(
        self,
        config: ArticulationConfig,
        feedback_context: Optional[FeedbackContext],
        option_hints: List[str],
    ) -> RecognitionHandlerResult:
        """Handle "none of these" selection."""
        # Record feedback if context provided (#412)
        if feedback_context:
            feedback = create_feedback_from_none_of_these(
                context=feedback_context,
                offered_options=option_hints,
            )
            record_recognition_feedback(feedback)

        # Get clarification prompt
        response = self.response_service.handle_none_of_these(config)

        return RecognitionHandlerResult(
            state_transition="RECOGNITION_OFFERED → CLARIFYING",
            selection_result=SelectionResult.NONE_OF_THESE,
            should_route_to_handler=False,
            response_text=response,
            trust_penalty=False,  # Never penalize clarification
        )

    def _handle_no_match(
        self,
        user_message: str,
        offered_options: RecognitionOptions,
        config: ArticulationConfig,
        feedback_context: Optional[FeedbackContext],
        option_hints: List[str],
    ) -> RecognitionHandlerResult:
        """
        Handle when selection doesn't match any option.

        This could mean:
        1. Empty input → re-show options (no feedback recorded)
        2. Unrelated query → treat as new input (re-classify, record feedback)
        """
        # Empty or whitespace-only input - don't record feedback for empty input
        if not user_message.strip():
            response = self.response_service.format_reshow_options(
                recognition=offered_options,
                config=config,
            )
            return RecognitionHandlerResult(
                state_transition="RECOGNITION_OFFERED → RECOGNITION_OFFERED",
                selection_result=SelectionResult.NO_MATCH,
                should_route_to_handler=False,
                response_text=response,
                trust_penalty=False,
            )

        # Record feedback for unrelated input (#412)
        if feedback_context:
            feedback = create_feedback_from_no_match(
                context=feedback_context,
                offered_options=option_hints,
            )
            record_recognition_feedback(feedback)

        # Treat as new input - re-classify
        # This is returned to the caller to handle
        return RecognitionHandlerResult(
            state_transition="RECOGNITION_OFFERED → NORMAL (re-classify)",
            selection_result=SelectionResult.NO_MATCH,
            should_route_to_handler=True,  # But with no intent_hint - caller should re-classify
            intent_hint=None,  # Signals re-classification needed
            response_text=None,
            trust_penalty=False,
        )

    def _handle_out_of_range(
        self,
        offered_options: RecognitionOptions,
        config: ArticulationConfig,
    ) -> RecognitionHandlerResult:
        """Handle numeric selection out of range."""
        count = len(offered_options.options)
        response = f"I only offered {count} options. Which one would help? (1-{count})"

        return RecognitionHandlerResult(
            state_transition="RECOGNITION_OFFERED → RECOGNITION_OFFERED",
            selection_result=SelectionResult.NUMERIC_OUT_OF_RANGE,
            should_route_to_handler=False,
            response_text=response,
            trust_penalty=False,
        )


def create_intent_from_hint(intent_hint: str) -> Intent:
    """
    Create an Intent from a recognition option's intent_hint.

    Args:
        intent_hint: The intent_hint from RecognitionOption

    Returns:
        Intent configured to route to the hinted handler
    """
    # Map common intent hints to categories
    # This is a simplified mapping - real implementation would
    # use the full intent classification system
    category_hints = {
        "standup": IntentCategory.QUERY,
        "status": IntentCategory.QUERY,
        "todos": IntentCategory.QUERY,
        "list": IntentCategory.QUERY,
        "calendar": IntentCategory.QUERY,
        "review": IntentCategory.EXECUTION,
        "create": IntentCategory.EXECUTION,
        "add": IntentCategory.EXECUTION,
    }

    # Determine category from hint
    category = IntentCategory.QUERY  # Default
    for key, cat in category_hints.items():
        if key in intent_hint.lower():
            category = cat
            break

    return Intent(
        category=category,
        action=intent_hint,
        confidence=1.0,  # User explicitly selected this
        context={"source": "recognition_selection"},
    )

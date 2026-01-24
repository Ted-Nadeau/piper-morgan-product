"""
Recognition Trigger Service.

Determines when to offer recognition options instead of acting on uncertain intent.
Part of #411 MUX-INTERACT-RECOGNITION.

Recognition > Recall: ~50% of users struggle to articulate precise queries.
When confidence is moderate (not high enough to act, not low enough to fail),
we offer contextual options to help users recognize what they need.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

import structlog

# Import Intent from domain models directly to avoid circular import
from services.domain.models import Intent

# Import types that don't cause circular imports
from services.mux.orientation import (
    ArticulationConfig,
    ChannelType,
    OrientationState,
    RecognitionGenerator,
    RecognitionOptions,
)
from services.mux.recognition_response import RecognitionResponseService
from services.shared_types import PerceptionMode

# These are only needed for type hints - use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from services.intent_service.intent_types import (
        IntentClassificationContext,
        IntentUnderstanding,
    )


logger = structlog.get_logger(__name__)


# Confidence thresholds for recognition
RECOGNITION_THRESHOLD_HIGH = 0.7  # Above this: confident enough to act
RECOGNITION_THRESHOLD_LOW = 0.35  # Below this: too uncertain, use honest failure


@dataclass
class RecognitionTriggerResult:
    """Result of recognition trigger evaluation."""

    should_trigger: bool
    reason: str
    recognition_options: Optional[RecognitionOptions] = None
    formatted_response: Optional[str] = None


class RecognitionTrigger:
    """
    Determines when and how to offer recognition options.

    Recognition fills the gap between:
    - High confidence (act on intent)
    - Low confidence (ask for clarification)

    When confidence is "moderate", we offer contextual options
    based on orientation rather than just asking "what do you mean?"
    """

    def __init__(
        self,
        high_threshold: float = RECOGNITION_THRESHOLD_HIGH,
        low_threshold: float = RECOGNITION_THRESHOLD_LOW,
    ):
        """
        Initialize recognition trigger with thresholds.

        Args:
            high_threshold: Above this confidence, don't trigger recognition
            low_threshold: Below this confidence, use honest failure instead
        """
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold

    def should_trigger(
        self,
        confidence: float,
        context: "IntentClassificationContext",
    ) -> bool:
        """
        Determine if recognition should trigger based on confidence.

        Recognition triggers when:
        - Confidence is in the "moderate" zone (low_threshold < conf < high_threshold)
        - Orientation is available to generate meaningful options

        Args:
            confidence: Classification confidence (0.0-1.0)
            context: Classification context with orientation

        Returns:
            True if recognition should trigger
        """
        # Check confidence range
        if confidence >= self.high_threshold:
            logger.debug(
                "Recognition not triggered: confidence too high",
                confidence=confidence,
                threshold=self.high_threshold,
            )
            return False

        if confidence < self.low_threshold:
            logger.debug(
                "Recognition not triggered: confidence too low",
                confidence=confidence,
                threshold=self.low_threshold,
            )
            return False

        # Check if we have orientation to generate options
        if not context.orientation:
            logger.debug("Recognition not triggered: no orientation available")
            return False

        # Confidence is in the recognition zone and we have orientation
        logger.debug(
            "Recognition triggered",
            confidence=confidence,
            low_threshold=self.low_threshold,
            high_threshold=self.high_threshold,
        )
        return True

    def evaluate(
        self,
        intent: Intent,
        context: "IntentClassificationContext",
        channel: ChannelType = ChannelType.WEB,
        trust_stage: int = 1,
    ) -> RecognitionTriggerResult:
        """
        Evaluate whether to trigger recognition and generate options.

        This is the main entry point - it checks conditions and generates
        recognition options if appropriate.

        Args:
            intent: The classified intent (possibly low confidence)
            context: Classification context with orientation
            channel: Channel type for formatting
            trust_stage: User's trust stage for language adaptation

        Returns:
            RecognitionTriggerResult with trigger decision and options
        """
        confidence = intent.confidence if intent else 0.0

        # Check if we should trigger
        if not self.should_trigger(confidence, context):
            reason = self._get_non_trigger_reason(confidence, context)
            return RecognitionTriggerResult(
                should_trigger=False,
                reason=reason,
            )

        # Generate recognition options from orientation
        try:
            config = ArticulationConfig(
                channel=channel,
                trust_stage=trust_stage,
            )

            recognition_options = self.generate_recognition(context, config)

            if not recognition_options or not recognition_options.options:
                return RecognitionTriggerResult(
                    should_trigger=False,
                    reason="No recognition options could be generated",
                )

            # Format the response
            formatted = RecognitionResponseService.format_for_channel(
                recognition_options,
                config,
            )

            return RecognitionTriggerResult(
                should_trigger=True,
                reason=f"Moderate confidence ({confidence:.2f}) with {len(recognition_options.options)} options",
                recognition_options=recognition_options,
                formatted_response=formatted,
            )

        except Exception as e:
            logger.warning(f"Failed to generate recognition: {e}")
            return RecognitionTriggerResult(
                should_trigger=False,
                reason=f"Recognition generation failed: {e}",
            )

    def generate_recognition(
        self,
        context: "IntentClassificationContext",
        config: ArticulationConfig,
    ) -> Optional[RecognitionOptions]:
        """
        Generate recognition options from orientation.

        Args:
            context: Classification context with orientation
            config: Articulation config for language adaptation

        Returns:
            RecognitionOptions or None if generation fails
        """
        if not context.orientation:
            return None

        return RecognitionGenerator.generate(
            orientation=context.orientation,
            config=config,
        )

    def _get_non_trigger_reason(
        self,
        confidence: float,
        context: "IntentClassificationContext",
    ) -> str:
        """Get reason why recognition didn't trigger."""
        if confidence >= self.high_threshold:
            return f"Confidence {confidence:.2f} >= {self.high_threshold} (act on intent)"
        if confidence < self.low_threshold:
            return f"Confidence {confidence:.2f} < {self.low_threshold} (use honest failure)"
        if not context.orientation:
            return "No orientation available"
        return "Unknown reason"


def create_recognition_understanding(
    intent: Intent,
    context: Any,  # IntentClassificationContext - use Any to avoid import
    recognition_options: RecognitionOptions,
    formatted_response: str,
) -> Any:  # IntentUnderstanding - use Any to avoid import
    """
    Create IntentUnderstanding for a recognition response.

    This is returned when recognition triggers, asking the user
    to select from options rather than acting on uncertain intent.

    Args:
        intent: The original (low confidence) intent
        context: Classification context
        recognition_options: Generated options
        formatted_response: Pre-formatted response string

    Returns:
        IntentUnderstanding with recognition response
    """
    # Late import to avoid circular dependency
    from services.intent_service.intent_types import IntentUnderstanding

    return IntentUnderstanding(
        intent=intent,
        understanding_narrative=formatted_response,
        confidence_expression="",  # Confidence is expressed through the options themselves
        place_awareness="",  # Place context is in the options
        perception_mode=PerceptionMode.NOTICING,  # Piper is noticing what might help
        follow_up_suggestion="",  # Options are the follow-up
        # Mark that this is a recognition response for downstream handling
        metadata={
            "recognition_offered": True,
            "recognition_options_count": len(recognition_options.options),
            "recognition_has_escape_hatch": recognition_options.has_escape_hatch,
        },
    )

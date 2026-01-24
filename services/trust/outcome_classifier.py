"""
OutcomeClassifier - Classifies interaction outcomes for trust computation.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

Maps user responses to trust outcomes (successful, neutral, negative):
- successful: User expressed thanks, follow-up questions, command execution
- neutral: Topic change without acknowledgment, ambiguous responses
- negative: "Not what I wanted", explicit rejection, complaints
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class OutcomeType(str, Enum):
    """Trust interaction outcome types."""

    SUCCESSFUL = "successful"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class OutcomeClassification:
    """Result of outcome classification."""

    outcome: OutcomeType
    confidence: float  # 0.0 to 1.0
    signals_detected: List[str]  # Which patterns matched
    reasoning: str  # Human-readable explanation


# Pattern definitions per ADR-053
# Note: Patterns are case-insensitive
SUCCESSFUL_PATTERNS = [
    # Gratitude
    (r"\b(thanks|thank you|thx|ty|appreciated|helpful)\b", "gratitude"),
    # Acknowledgment
    (r"\b(perfect|great|excellent|awesome|nice|good job|well done)\b", "acknowledgment"),
    (r"\b(that'?s? (exactly |just )?(what|it))\b", "acknowledgment"),
    (r"\b(exactly|precisely)\b", "acknowledgment"),
    # Follow-up engagement
    (r"\b(can you also|what about|how about|and|also)\b", "follow_up"),
    (r"\b(one more thing|another question)\b", "follow_up"),
    # Explicit confirmation
    (r"\b(yes|yep|yeah|yup|correct|right)\b", "confirmation"),
    (r"\b(got it|understood|makes sense)\b", "confirmation"),
]

NEGATIVE_PATTERNS = [
    # Explicit rejection
    (r"\b(not what i (wanted|asked|meant))\b", "rejection"),
    (r"\b(wrong|incorrect|no|nope)\b", "rejection"),
    (r"\b(that'?s? not (right|correct|it))\b", "rejection"),
    # Frustration
    (r"\b(ugh|argh|sigh|frustrat(ed|ing)|annoying)\b", "frustration"),
    (r"\b(why (can'?t|won'?t|don'?t) you)\b", "frustration"),
    # Complaints
    (r"\b(stop|don'?t|quit|enough)\b", "complaint"),
    (r"\b(i didn'?t (ask|want|need))\b", "complaint"),
    (r"\b(that'?s? (wrong|bad|terrible|awful))\b", "complaint"),
    # Confusion indicating failure
    (r"\b(confused|don'?t understand|what\?)\b", "confusion"),
    (r"\b(huh|what do you mean)\b", "confusion"),
]

NEUTRAL_PATTERNS = [
    # Topic change
    (r"\b(anyway|moving on|let'?s talk about|different topic)\b", "topic_change"),
    (r"\b(never ?mind|forget it|whatever)\b", "dismissal"),
    # Non-committal
    (r"\b(ok|okay|sure|fine|alright)\b", "non_committal"),
    (r"\b(i see|i guess|maybe)\b", "non_committal"),
]


class OutcomeClassifier:
    """
    Classifies user responses into trust outcomes.

    Uses pattern matching on user messages following Piper's responses
    to determine if the interaction was successful, neutral, or negative.

    Note: This is a heuristic classifier for MVP. Future versions may use
    LLM-based classification for better accuracy.

    Usage:
        classifier = OutcomeClassifier()

        # After Piper responds and user replies
        outcome = classifier.classify(user_reply)
        trust_service.record_interaction(user_id, outcome.outcome.value, context)
    """

    def __init__(self):
        """Initialize with compiled patterns for efficiency."""
        self._successful = [
            (re.compile(pattern, re.IGNORECASE), signal) for pattern, signal in SUCCESSFUL_PATTERNS
        ]
        self._negative = [
            (re.compile(pattern, re.IGNORECASE), signal) for pattern, signal in NEGATIVE_PATTERNS
        ]
        self._neutral = [
            (re.compile(pattern, re.IGNORECASE), signal) for pattern, signal in NEUTRAL_PATTERNS
        ]

    def classify(
        self,
        user_message: str,
        assistant_message: Optional[str] = None,
        context: Optional[dict] = None,
    ) -> OutcomeClassification:
        """
        Classify a user response as successful, neutral, or negative.

        Args:
            user_message: The user's reply after Piper's response
            assistant_message: Optional previous assistant message for context
            context: Optional additional context (e.g., task completion status)

        Returns:
            OutcomeClassification with outcome type, confidence, and reasoning
        """
        # Check for context-based classification first (overrides message analysis)
        if context:
            context_outcome = self._classify_from_context(context)
            if context_outcome:
                return context_outcome

        if not user_message or not user_message.strip():
            return OutcomeClassification(
                outcome=OutcomeType.NEUTRAL,
                confidence=0.5,
                signals_detected=["empty_message"],
                reasoning="Empty or whitespace-only message treated as neutral",
            )

        message = user_message.strip().lower()

        # Pattern-based classification
        successful_signals = self._match_patterns(message, self._successful)
        negative_signals = self._match_patterns(message, self._negative)
        neutral_signals = self._match_patterns(message, self._neutral)

        # Scoring: negative patterns are stronger signals (user effort to complain)
        successful_score = len(successful_signals) * 1.0
        negative_score = len(negative_signals) * 1.5  # Weight negative higher
        neutral_score = len(neutral_signals) * 0.5

        # Decision logic
        if negative_score > 0 and negative_score >= successful_score:
            return OutcomeClassification(
                outcome=OutcomeType.NEGATIVE,
                confidence=min(0.9, 0.5 + (negative_score * 0.1)),
                signals_detected=negative_signals,
                reasoning=f"Negative signals detected: {', '.join(negative_signals)}",
            )

        if successful_score > neutral_score and successful_score > 0:
            return OutcomeClassification(
                outcome=OutcomeType.SUCCESSFUL,
                confidence=min(0.9, 0.5 + (successful_score * 0.1)),
                signals_detected=successful_signals,
                reasoning=f"Success signals detected: {', '.join(successful_signals)}",
            )

        if neutral_signals:
            return OutcomeClassification(
                outcome=OutcomeType.NEUTRAL,
                confidence=min(0.8, 0.5 + (neutral_score * 0.1)),
                signals_detected=neutral_signals,
                reasoning=f"Neutral signals detected: {', '.join(neutral_signals)}",
            )

        # Default: no clear signals, treat as neutral
        return OutcomeClassification(
            outcome=OutcomeType.NEUTRAL,
            confidence=0.3,
            signals_detected=[],
            reasoning="No clear outcome signals detected, defaulting to neutral",
        )

    def classify_task_completion(
        self,
        task_succeeded: bool,
        user_reaction: Optional[str] = None,
    ) -> OutcomeClassification:
        """
        Classify outcome based on task completion status.

        For explicit task requests (create todo, schedule meeting, etc.),
        we can use task success/failure as a strong signal.

        Args:
            task_succeeded: Whether the requested task completed successfully
            user_reaction: Optional user response after task completion

        Returns:
            OutcomeClassification
        """
        if user_reaction:
            # If we have user reaction, let that inform the outcome
            reaction_outcome = self.classify(user_reaction)
            # But task failure should override positive reactions
            if not task_succeeded and reaction_outcome.outcome == OutcomeType.SUCCESSFUL:
                return OutcomeClassification(
                    outcome=OutcomeType.NEGATIVE,
                    confidence=0.7,
                    signals_detected=["task_failed"],
                    reasoning="Task failed despite positive user language",
                )
            return reaction_outcome

        # No user reaction, use task status directly
        if task_succeeded:
            return OutcomeClassification(
                outcome=OutcomeType.SUCCESSFUL,
                confidence=0.7,
                signals_detected=["task_completed"],
                reasoning="Task completed successfully",
            )
        else:
            return OutcomeClassification(
                outcome=OutcomeType.NEGATIVE,
                confidence=0.7,
                signals_detected=["task_failed"],
                reasoning="Task failed to complete",
            )

    def _match_patterns(
        self,
        message: str,
        patterns: List[Tuple[re.Pattern, str]],
    ) -> List[str]:
        """Match message against pattern list, return matched signal names."""
        signals = []
        for pattern, signal in patterns:
            if pattern.search(message):
                signals.append(signal)
        return signals

    def _classify_from_context(
        self,
        context: dict,
    ) -> Optional[OutcomeClassification]:
        """
        Classify based on context if strong signals present.

        Context can include:
        - task_completed: bool
        - error_occurred: bool
        - user_corrected: bool (user had to correct Piper)
        """
        if context.get("error_occurred"):
            return OutcomeClassification(
                outcome=OutcomeType.NEGATIVE,
                confidence=0.8,
                signals_detected=["error_occurred"],
                reasoning="An error occurred during processing",
            )

        if context.get("user_corrected"):
            return OutcomeClassification(
                outcome=OutcomeType.NEGATIVE,
                confidence=0.7,
                signals_detected=["user_corrected"],
                reasoning="User had to correct Piper's understanding",
            )

        if context.get("task_completed"):
            return OutcomeClassification(
                outcome=OutcomeType.SUCCESSFUL,
                confidence=0.6,  # Lower than explicit user thanks
                signals_detected=["task_completed"],
                reasoning="Requested task completed successfully",
            )

        return None

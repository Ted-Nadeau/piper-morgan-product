"""
SignalDetector - Detects conversational signals for trust escalation and regression.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

Detects two types of signals:
1. Trust escalation phrases (Stage 3→4): "just handle it", "I trust you to...", etc.
2. Complaint patterns (trigger regression): "stop doing that", "I didn't ask for...", etc.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class SignalType(str, Enum):
    """Types of trust signals detected."""

    ESCALATION = "escalation"  # User wants to progress to TRUSTED stage
    COMPLAINT = "complaint"  # User is dissatisfied, triggers immediate Stage 2 regression
    SOFT_REGRESSION = "soft_regression"  # User wants less proactivity, drops one stage
    NONE = "none"  # No signal detected


@dataclass
class SignalDetectionResult:
    """Result of signal detection."""

    signal_type: SignalType
    confidence: float  # 0.0 to 1.0
    phrases_matched: List[str]  # Actual text that matched
    patterns_matched: List[str]  # Pattern names that matched
    reasoning: str  # Human-readable explanation


# Trust escalation patterns per ADR-053
# These indicate user wants Piper to act more autonomously
ESCALATION_PATTERNS = [
    # Explicit trust statements
    (r"\b(i trust you|i trust that you)\b", "explicit_trust", 0.9),
    (r"\b(you can handle|you know what to do)\b", "confidence_expression", 0.8),
    # Autonomy grants
    (r"\bjust (handle|do|take care of) it\b", "autonomy_grant", 0.9),
    (r"\b(do that|do it|go ahead) automatically\b", "auto_request", 0.85),
    (r"\b(don'?t|no need to) ask( me)?( first)?\b", "skip_confirmation", 0.8),
    (r"\byou (don'?t need to|don'?t have to) (ask|check|confirm)\b", "skip_confirmation", 0.8),
    # Delegation
    (r"\b(take care of (it|this|that))\b", "delegation", 0.75),
    (r"\b(handle (it|this|that) (for|from) me)\b", "delegation", 0.75),
    (r"\b(leave (it|this|that) to you)\b", "delegation", 0.8),
    # Implicit trust through pattern
    (r"\b(from now on|going forward),? (just|always)\b", "future_autonomy", 0.85),
    (
        r"\b(whenever|every time) (this|that|it) happens,? (just|go ahead)\b",
        "conditional_autonomy",
        0.85,
    ),
]

# Complaint patterns per ADR-053
# These indicate dissatisfaction and may trigger stage regression
COMPLAINT_PATTERNS = [
    # Stop commands
    (r"\bstop (doing|that|it|this)\b", "stop_command", 0.85),
    (r"\b(don'?t|do not) (do|say) (that|it|this)( again)?\b", "prohibition", 0.8),
    (r"\b(quit|stop|enough)\b", "stop_command", 0.7),
    # Rejection of offers
    (r"\bi didn'?t (ask|want|need)( (you )?to)?\b", "rejection_of_offer", 0.85),
    (r"\bi (didn'?t|don'?t) (ask|want) (that|this|it)\b", "rejection_of_offer", 0.85),
    (r"\bno,? (i|we) (didn'?t|don'?t)\b", "explicit_no", 0.75),
    # Explicit complaints
    (r"\b(that'?s?|this is) (annoying|frustrating|irritating)\b", "frustration", 0.8),
    (
        r"\b(you'?re being|this is) (too|overly) (proactive|pushy|aggressive)\b",
        "over_proactive_complaint",
        0.9,
    ),
    (r"\bstop (suggesting|offering|asking)\b", "suggestion_complaint", 0.85),
    # Preference violations
    (r"\bi (told|asked) you (not to|to stop)\b", "repeated_violation", 0.9),
    (r"\b(why (do|are) you keep(ing)?|you keep)\b", "repeated_behavior", 0.75),
    # Strong rejection
    (r"\b(absolutely not|definitely not|no way)\b", "strong_rejection", 0.85),
]

# Soft regression patterns per PPM guidance (2026-01-23)
# These indicate user wants less proactivity but hasn't complained
# Results in one-stage regression (not immediate Stage 2 floor)
# NOTE: "ask me first" must NOT match when preceded by "don't" or "no need to"
# (those are escalation signals meaning user DOESN'T want to be asked)
SOFT_REGRESSION_PATTERNS = [
    # Ask first requests - exclude when preceded by negation
    (r"(?<![''`]t )(?<!need to )\b(actually,? )?ask me first( next time)?\b", "ask_first", 0.85),
    (r"\bcheck with me (first|before)\b", "check_first", 0.85),
    (r"\bi'?d prefer (you|if you) ask\b", "prefer_ask", 0.8),
    (r"\bplease ask (me )?(first|before)\b", "please_ask", 0.8),
    # Let me decide
    (r"\blet me (decide|choose|pick)\b", "let_me_decide", 0.75),
    (r"\bi'?ll (decide|choose|handle) (that|this|it)\b", "self_decide", 0.7),
    (r"\bi want to (decide|approve|confirm)\b", "want_to_decide", 0.8),
    # Softer pushback (not quite complaint)
    (r"\bmaybe (ask|check) (first|next time)\b", "soft_pushback", 0.7),
    (r"\bnext time,? (ask|check|confirm)\b", "next_time_ask", 0.8),
    (r"\bhold off (on|until)\b", "hold_off", 0.7),
]


class SignalDetector:
    """
    Detects conversational signals for trust stage transitions.

    This service scans user messages for:
    1. Escalation signals: Phrases indicating user wants more autonomous behavior
    2. Complaint signals: Phrases indicating dissatisfaction with current behavior

    Usage:
        detector = SignalDetector()
        result = detector.detect(user_message)

        if result.signal_type == SignalType.ESCALATION:
            # User wants Stage 3→4 progression
            await trust_service.progress_to_trusted(user_id, result.reasoning)

        if result.signal_type == SignalType.COMPLAINT:
            # User is dissatisfied, consider regression
            await trust_service.record_interaction(user_id, "negative", result.reasoning)
    """

    def __init__(self):
        """Initialize with compiled patterns for efficiency."""
        self._escalation = [
            (re.compile(pattern, re.IGNORECASE), name, confidence)
            for pattern, name, confidence in ESCALATION_PATTERNS
        ]
        self._complaint = [
            (re.compile(pattern, re.IGNORECASE), name, confidence)
            for pattern, name, confidence in COMPLAINT_PATTERNS
        ]
        self._soft_regression = [
            (re.compile(pattern, re.IGNORECASE), name, confidence)
            for pattern, name, confidence in SOFT_REGRESSION_PATTERNS
        ]

    def detect(
        self,
        message: str,
        context: Optional[dict] = None,
    ) -> SignalDetectionResult:
        """
        Detect trust signals in a user message.

        Args:
            message: User's message text
            context: Optional context (e.g., was this in response to a proactive offer?)

        Returns:
            SignalDetectionResult with signal type, confidence, and details
        """
        if not message or not message.strip():
            return SignalDetectionResult(
                signal_type=SignalType.NONE,
                confidence=1.0,
                phrases_matched=[],
                patterns_matched=[],
                reasoning="Empty message",
            )

        # Detect all signal types
        escalation_matches = self._match_patterns(message, self._escalation)
        complaint_matches = self._match_patterns(message, self._complaint)
        soft_regression_matches = self._match_patterns(message, self._soft_regression)

        # Context boost: complaints/soft regression in response to proactive offers are stronger
        proactive_boost = 0.0
        if context and context.get("in_response_to_proactive"):
            proactive_boost = 0.1

        # Calculate aggregate confidence
        escalation_confidence = self._aggregate_confidence(escalation_matches)
        complaint_confidence = self._aggregate_confidence(complaint_matches) + proactive_boost
        soft_regression_confidence = (
            self._aggregate_confidence(soft_regression_matches) + proactive_boost
        )

        # Decision logic - priority order:
        # 1. Complaints (most severe, immediate Stage 2)
        # 2. Soft regression (gentler, one stage drop)
        # 3. Escalation (positive, stage increase)
        if complaint_confidence > 0.5 and complaint_confidence >= max(
            escalation_confidence, soft_regression_confidence
        ):
            phrases, patterns = zip(*complaint_matches) if complaint_matches else ([], [])
            return SignalDetectionResult(
                signal_type=SignalType.COMPLAINT,
                confidence=min(0.95, complaint_confidence),
                phrases_matched=list(phrases),
                patterns_matched=list(patterns),
                reasoning=f"Complaint signals detected: {', '.join(patterns)}",
            )

        if soft_regression_confidence > 0.5 and soft_regression_confidence >= escalation_confidence:
            phrases, patterns = (
                zip(*soft_regression_matches) if soft_regression_matches else ([], [])
            )
            return SignalDetectionResult(
                signal_type=SignalType.SOFT_REGRESSION,
                confidence=min(0.95, soft_regression_confidence),
                phrases_matched=list(phrases),
                patterns_matched=list(patterns),
                reasoning=f"Soft regression signals detected: {', '.join(patterns)}",
            )

        if escalation_confidence > 0.5:
            phrases, patterns = zip(*escalation_matches) if escalation_matches else ([], [])
            return SignalDetectionResult(
                signal_type=SignalType.ESCALATION,
                confidence=min(0.95, escalation_confidence),
                phrases_matched=list(phrases),
                patterns_matched=list(patterns),
                reasoning=f"Escalation signals detected: {', '.join(patterns)}",
            )

        return SignalDetectionResult(
            signal_type=SignalType.NONE,
            confidence=1.0
            - max(escalation_confidence, complaint_confidence, soft_regression_confidence, 0.0),
            phrases_matched=[],
            patterns_matched=[],
            reasoning="No significant trust signals detected",
        )

    def detect_escalation(self, message: str) -> Optional[SignalDetectionResult]:
        """
        Check specifically for escalation signals.

        Convenience method when you only care about Stage 3→4 progression.

        Args:
            message: User's message text

        Returns:
            SignalDetectionResult if escalation detected, None otherwise
        """
        result = self.detect(message)
        if result.signal_type == SignalType.ESCALATION:
            return result
        return None

    def detect_complaint(
        self,
        message: str,
        in_response_to_proactive: bool = False,
    ) -> Optional[SignalDetectionResult]:
        """
        Check specifically for complaint signals.

        Convenience method for regression detection.

        Args:
            message: User's message text
            in_response_to_proactive: Whether this is a response to proactive behavior

        Returns:
            SignalDetectionResult if complaint detected, None otherwise
        """
        context = {"in_response_to_proactive": in_response_to_proactive}
        result = self.detect(message, context)
        if result.signal_type == SignalType.COMPLAINT:
            return result
        return None

    def detect_soft_regression(
        self,
        message: str,
        in_response_to_proactive: bool = False,
    ) -> Optional[SignalDetectionResult]:
        """
        Check specifically for soft regression signals.

        Soft regression means user wants less proactivity but hasn't complained.
        Results in one-stage drop (not immediate Stage 2 floor).

        Args:
            message: User's message text
            in_response_to_proactive: Whether this is a response to proactive behavior

        Returns:
            SignalDetectionResult if soft regression detected, None otherwise
        """
        context = {"in_response_to_proactive": in_response_to_proactive}
        result = self.detect(message, context)
        if result.signal_type == SignalType.SOFT_REGRESSION:
            return result
        return None

    def _match_patterns(
        self,
        message: str,
        patterns: List[Tuple[re.Pattern, str, float]],
    ) -> List[Tuple[str, str]]:
        """
        Match message against patterns.

        Returns list of (matched_text, pattern_name) tuples.
        """
        matches = []
        for pattern, name, _ in patterns:
            match = pattern.search(message)
            if match:
                matches.append((match.group(0), name))
        return matches

    def _aggregate_confidence(
        self,
        matches: List[Tuple[str, str]],
    ) -> float:
        """
        Aggregate confidence from multiple pattern matches.

        Multiple matches increase confidence but with diminishing returns.
        """
        if not matches:
            return 0.0

        # Get confidence values for matched patterns
        all_patterns = ESCALATION_PATTERNS + COMPLAINT_PATTERNS + SOFT_REGRESSION_PATTERNS
        confidences = []
        for _, pattern_name in matches:
            for _, name, confidence in all_patterns:
                if name == pattern_name:
                    confidences.append(confidence)
                    break

        if not confidences:
            return 0.0

        # Use max confidence as base, add diminishing bonus for additional matches
        base = max(confidences)
        bonus = sum(c * 0.1 for c in confidences[1:]) if len(confidences) > 1 else 0
        return min(0.95, base + bonus)

    def get_escalation_examples(self) -> List[str]:
        """
        Return example phrases that would trigger escalation detection.

        Useful for documentation and testing.
        """
        return [
            "I trust you to handle that",
            "Just handle it from now on",
            "You don't need to ask me first",
            "Do that automatically going forward",
            "Leave it to you",
            "Take care of this for me",
            "Whenever this happens, just go ahead",
        ]

    def get_complaint_examples(self) -> List[str]:
        """
        Return example phrases that would trigger complaint detection.

        Useful for documentation and testing.
        """
        return [
            "Stop doing that",
            "I didn't ask for that",
            "Stop suggesting things",
            "You're being too proactive",
            "No, I don't want that",
            "Don't do that again",
            "I told you not to do that",
        ]

    def get_soft_regression_examples(self) -> List[str]:
        """
        Return example phrases that would trigger soft regression detection.

        These are softer than complaints - user wants less proactivity
        but hasn't complained. Results in one-stage drop, not Stage 2 floor.

        Useful for documentation and testing.
        """
        return [
            "Actually, ask me first next time",
            "Check with me before doing that",
            "I'd prefer you ask",
            "Please ask me first",
            "Let me decide on that",
            "I'll decide that myself",
            "Next time, check with me",
            "Maybe ask first next time",
        ]

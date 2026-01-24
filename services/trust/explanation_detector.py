"""
ExplanationDetector service for identifying trust explanation queries.

This service detects when users are asking questions about Piper's behavior
that should be routed to the TrustExplainer service.

Query types detected:
- WHY_ACTION: "Why did you do that?"
- WHY_NO_ACTION: "Why don't you just do things?"
- TRUST_LEVEL: "How do we work together?"
- BEHAVIOR_QUESTION: "Why do you always ask?"

Pattern design follows SignalDetector architecture for consistency.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class ExplanationQueryType(str, Enum):
    """Types of explanation queries users might ask."""

    WHY_ACTION = "why_action"  # "Why did you do that?"
    WHY_NO_ACTION = "why_no_action"  # "Why don't you just...?"
    TRUST_LEVEL = "trust_level"  # "How much do you trust me?"
    BEHAVIOR_QUESTION = "behavior_question"  # "Why do you always ask?"
    NOT_EXPLANATION_QUERY = "not_explanation_query"  # Normal message


@dataclass
class ExplanationDetectionResult:
    """Result of explanation query detection."""

    query_type: ExplanationQueryType
    confidence: float
    matched_phrase: Optional[str] = None
    reasoning: Optional[str] = None

    @property
    def is_explanation_query(self) -> bool:
        """Check if this is an explanation query (not normal message)."""
        return self.query_type != ExplanationQueryType.NOT_EXPLANATION_QUERY


# Pattern format: (regex_pattern, pattern_name, confidence)
# Patterns are case-insensitive

WHY_ACTION_PATTERNS: List[Tuple[str, str, float]] = [
    # Direct "why did you" questions
    (r"\bwhy did you (do|just|go ahead|decide to)\b", "why_did_you", 0.9),
    (r"\bwhy'?d you\b", "why_did_you_contraction", 0.85),
    # Complaints about uninstructed action
    (r"\bi didn'?t (ask|tell) you to\b", "didnt_ask", 0.85),
    (r"\bi (didn'?t|never) (ask|want|asked) (you to|that)\b", "didnt_want", 0.85),
    (r"\bi never asked you to\b", "never_asked", 0.85),
    (r"\bwho (told|asked) you to\b", "who_asked", 0.8),
    # Questioning specific actions
    (r"\bwhy would you\b", "why_would_you", 0.75),
    (r"\bwhat made you (do|decide|think)\b", "what_made_you", 0.8),
]

WHY_NO_ACTION_PATTERNS: List[Tuple[str, str, float]] = [
    # Direct "why don't you" questions
    (r"\bwhy (don'?t|won'?t|can'?t) you (just|simply)?\b", "why_dont_you", 0.85),
    (
        r"\bwhy (are|do) you (so|being so|always) (cautious|careful|conservative)\b",
        "why_cautious",
        0.9,
    ),
    # Requests for more autonomy framed as questions
    (r"\bwhy do you (always )?(have to )?(ask|check|confirm)\b", "why_always_ask", 0.9),
    (r"\bwhy (do you )?always have to (ask|check|confirm)\b", "why_always_have_to", 0.9),
    (r"\bcan'?t you just (do|handle|take care of)\b", "cant_you_just", 0.8),
    (r"\bwhy (not|can'?t you) (just )?(do|handle) (it|things)\b", "why_not_just", 0.85),
    # Frustration with lack of proactivity
    (r"\bwhy (do i|must i) (always )?have to (ask|tell) you\b", "why_must_i_ask", 0.85),
]

TRUST_LEVEL_PATTERNS: List[Tuple[str, str, float]] = [
    # Direct trust questions
    (r"\bhow (much )?do (you trust me|i trust you)\b", "trust_question", 0.9),
    (
        r"\b(what'?s|what is) our (relationship|working relationship)\b",
        "relationship_question",
        0.85,
    ),
    (r"\bhow do (we|you and i) work together\b", "how_work_together", 0.85),
    # Trust level inquiry
    (r"\b(where|what level) (are we|am i) (at|on)\b", "level_inquiry", 0.7),
    (r"\bhow (well )?do you know me\b", "how_know_me", 0.8),
]

BEHAVIOR_QUESTION_PATTERNS: List[Tuple[str, str, float]] = [
    # General behavior questions
    (r"\bwhy do you (always|keep|usually)\b", "why_always", 0.75),
    (r"\bwhy (are|do) you (being|acting) (like|this way)\b", "why_acting", 0.8),
    (r"\bwhat'?s (up )?with you\b", "whats_with_you", 0.6),  # Lower confidence - could be greeting
    # Change in behavior
    (r"\bwhy did you (start|stop|change)\b", "why_change", 0.85),
    (r"\byou (used to|didn'?t use to)\b", "used_to", 0.75),
]


class ExplanationDetector:
    """
    Detects user queries about Piper's trust-based behavior.

    This service identifies when users are asking questions that should
    be routed to the TrustExplainer service rather than normal intent
    processing.

    Usage:
        detector = ExplanationDetector()
        result = detector.detect(user_message)

        if result.is_explanation_query:
            # Route to TrustExplainer based on query_type
            if result.query_type == ExplanationQueryType.WHY_ACTION:
                explanation = await explainer.explain_proactive_action(user_id, action)

    Design note: Pattern matching follows SignalDetector architecture.
    Confidence threshold is 0.7 - below this, treat as normal message.
    """

    # Minimum confidence to consider it an explanation query
    CONFIDENCE_THRESHOLD = 0.7

    def __init__(self):
        """Initialize with compiled patterns for efficiency."""
        self._why_action = self._compile_patterns(WHY_ACTION_PATTERNS)
        self._why_no_action = self._compile_patterns(WHY_NO_ACTION_PATTERNS)
        self._trust_level = self._compile_patterns(TRUST_LEVEL_PATTERNS)
        self._behavior = self._compile_patterns(BEHAVIOR_QUESTION_PATTERNS)

    def _compile_patterns(
        self,
        patterns: List[Tuple[str, str, float]],
    ) -> List[Tuple[re.Pattern, str, float]]:
        """Compile regex patterns for efficient matching."""
        return [
            (re.compile(pattern, re.IGNORECASE), name, confidence)
            for pattern, name, confidence in patterns
        ]

    def detect(self, message: str) -> ExplanationDetectionResult:
        """
        Detect if message is an explanation query.

        Args:
            message: User message to analyze

        Returns:
            ExplanationDetectionResult with query type and confidence
        """
        if not message or not message.strip():
            return ExplanationDetectionResult(
                query_type=ExplanationQueryType.NOT_EXPLANATION_QUERY,
                confidence=0.0,
            )

        # Check each category in priority order
        # WHY_ACTION has highest priority (user questioning specific action)
        results = [
            (ExplanationQueryType.WHY_ACTION, self._match_patterns(message, self._why_action)),
            (
                ExplanationQueryType.WHY_NO_ACTION,
                self._match_patterns(message, self._why_no_action),
            ),
            (ExplanationQueryType.TRUST_LEVEL, self._match_patterns(message, self._trust_level)),
            (ExplanationQueryType.BEHAVIOR_QUESTION, self._match_patterns(message, self._behavior)),
        ]

        # Find best match above threshold
        best_match = None
        best_confidence = 0.0
        best_phrase = None
        best_name = None

        for query_type, matches in results:
            for phrase, name, confidence in matches:
                if confidence > best_confidence:
                    best_match = query_type
                    best_confidence = confidence
                    best_phrase = phrase
                    best_name = name

        if best_confidence >= self.CONFIDENCE_THRESHOLD:
            return ExplanationDetectionResult(
                query_type=best_match,
                confidence=best_confidence,
                matched_phrase=best_phrase,
                reasoning=f"Matched pattern: {best_name}",
            )

        return ExplanationDetectionResult(
            query_type=ExplanationQueryType.NOT_EXPLANATION_QUERY,
            confidence=best_confidence,
        )

    def _match_patterns(
        self,
        message: str,
        patterns: List[Tuple[re.Pattern, str, float]],
    ) -> List[Tuple[str, str, float]]:
        """
        Match message against a list of patterns.

        Args:
            message: Message to check
            patterns: List of (compiled_pattern, name, confidence)

        Returns:
            List of (matched_text, pattern_name, confidence) for all matches
        """
        matches = []
        for pattern, name, confidence in patterns:
            match = pattern.search(message)
            if match:
                matches.append((match.group(), name, confidence))
        return matches

    def detect_why_action(self, message: str) -> Optional[ExplanationDetectionResult]:
        """
        Specifically detect "why did you do that" queries.

        Convenience method for explicit query type checking.
        """
        result = self.detect(message)
        if result.query_type == ExplanationQueryType.WHY_ACTION:
            return result
        return None

    def detect_why_no_action(self, message: str) -> Optional[ExplanationDetectionResult]:
        """
        Specifically detect "why don't you just" queries.

        Convenience method for explicit query type checking.
        """
        result = self.detect(message)
        if result.query_type == ExplanationQueryType.WHY_NO_ACTION:
            return result
        return None

    def get_example_queries(self, query_type: ExplanationQueryType) -> List[str]:
        """
        Get example queries for a given type.

        Useful for testing and documentation.
        """
        examples = {
            ExplanationQueryType.WHY_ACTION: [
                "Why did you do that?",
                "I didn't ask you to reschedule my meeting",
                "What made you decide to send that email?",
            ],
            ExplanationQueryType.WHY_NO_ACTION: [
                "Why don't you just handle things?",
                "Why are you being so cautious?",
                "Why do you always ask me first?",
            ],
            ExplanationQueryType.TRUST_LEVEL: [
                "How do we work together?",
                "What's our working relationship like?",
                "How well do you know me?",
            ],
            ExplanationQueryType.BEHAVIOR_QUESTION: [
                "Why do you always do that?",
                "Why did you start being more proactive?",
                "You used to ask me about everything",
            ],
        }
        return examples.get(query_type, [])

"""
Conversation Analyzer - Detects user preferences from conversation patterns

ConversationAnalyzer: Core service that analyzes user messages and responses
to detect preference signals (warmth level, confidence style, action orientation,
technical depth preferences).
"""

import logging
import re
from typing import Any, Dict, List, Optional
from uuid import uuid4

from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    TechnicalPreference,
)
from services.personality.preference_detection import (
    ConfidenceLevel,
    DetectionMethod,
    PreferenceDetectionResult,
    PreferenceDimension,
    PreferenceHint,
)

logger = logging.getLogger(__name__)


class ConversationAnalyzer:
    """
    Analyzes conversation to detect user personality preferences.

    Detects signals for 4 personality dimensions:
    1. warmth_level - How warm/friendly vs professional user prefers
    2. confidence_style - How confidence should be displayed
    3. action_orientation - How action-oriented responses should be
    4. technical_depth - Level of technical detail preferred

    Methods:
    - analyze_message: Detect preferences from user's message
    - analyze_response: Detect preferences from system's response patterns
    - analyze_feedback: Detect preferences from explicit user feedback
    """

    # Language patterns for warmth detection
    WARM_WORDS = {
        "love",
        "great",
        "awesome",
        "wonderful",
        "fantastic",
        "beautiful",
        "appreciate",
        "thanks",
        "thank you",
        "grateful",
        "friendly",
        "chat",
        "hang out",
        "casual",
        "informal",
    }

    PROFESSIONAL_WORDS = {
        "efficient",
        "concise",
        "brief",
        "professional",
        "formal",
        "structured",
        "precise",
        "exact",
        "accurate",
        "rigorous",
        "minimal",
        "brief",
    }

    # Language patterns for action orientation
    ACTION_WORDS = {
        "let's",
        "let's go",
        "next step",
        "action",
        "do",
        "implement",
        "build",
        "execute",
        "right now",
        "immediately",
        "asap",
        "should we",
        "can we",
    }

    EXPLORATORY_WORDS = {
        "explore",
        "consider",
        "maybe",
        "perhaps",
        "think about",
        "could",
        "possibilities",
        "options",
        "interesting",
        "curious",
    }

    # Language patterns for confidence preference
    NUMERIC_WORDS = {
        "percent",
        "%",
        "probability",
        "odds",
        "score",
        "rate",
        "number",
        "metrics",
        "data",
        "statistics",
        "precise",
    }

    CONTEXTUAL_WORDS = {
        "based on",
        "because",
        "reason",
        "evidence",
        "research",
        "studies",
        "shows",
        "indicates",
        "pattern",
        "trend",
        "experience",
    }

    # Language patterns for technical depth
    TECHNICAL_WORDS = {
        "algorithm",
        "architecture",
        "database",
        "api",
        "protocol",
        "framework",
        "implementation",
        "code",
        "system",
        "performance",
        "optimization",
    }

    SIMPLIFIED_WORDS = {
        "simple",
        "easy",
        "straightforward",
        "basic",
        "beginner",
        "jargon",
        "explain",
        "plain english",
        "in other words",
        "translation",
    }

    def __init__(self):
        """Initialize analyzer with pattern matchers"""
        self.hint_counter = 0

    def analyze_message(
        self, user_id: str, message: str, current_profile: Any
    ) -> PreferenceDetectionResult:
        """
        Analyze user's message for preference signals.

        Args:
            user_id: User ID
            message: User's message text
            current_profile: Current PersonalityProfile (to detect changes)

        Returns:
            PreferenceDetectionResult with detected hints
        """
        result = PreferenceDetectionResult()

        # Analyze each dimension
        warmth_hint = self._detect_warmth_preference(user_id, message, current_profile)
        if warmth_hint:
            result.hints.append(warmth_hint)
            result.confidence_summary[PreferenceDimension.WARMTH] = warmth_hint.confidence_score

        action_hint = self._detect_action_preference(user_id, message, current_profile)
        if action_hint:
            result.hints.append(action_hint)
            result.confidence_summary[PreferenceDimension.ACTION] = action_hint.confidence_score

        confidence_hint = self._detect_confidence_preference(user_id, message, current_profile)
        if confidence_hint:
            result.hints.append(confidence_hint)
            result.confidence_summary[PreferenceDimension.CONFIDENCE] = (
                confidence_hint.confidence_score
            )

        technical_hint = self._detect_technical_preference(user_id, message, current_profile)
        if technical_hint:
            result.hints.append(technical_hint)
            result.confidence_summary[PreferenceDimension.TECHNICAL] = (
                technical_hint.confidence_score
            )

        # Categorize hints into suggestion and auto-apply groups
        result.suggested_hints = [h for h in result.hints if h.is_ready_for_suggestion()]
        result.auto_apply_hints = [h for h in result.hints if h.is_ready_for_auto_apply()]

        # Generate summary
        if result.hints:
            result.analysis_summary = self._generate_analysis_summary(result.hints)
        else:
            result.analysis_summary = "No preference signals detected in message"

        logger.info(
            f"Analyzed message for {user_id}: {len(result.hints)} hints detected, "
            f"{len(result.suggested_hints)} ready for suggestion"
        )

        return result

    def analyze_response(
        self, user_id: str, user_message: str, system_response: str, current_profile: Any
    ) -> PreferenceDetectionResult:
        """
        Analyze system response and user reaction for preference signals.

        Called after system provides response to user's message.

        Args:
            user_id: User ID
            user_message: Original user message
            system_response: System's response
            current_profile: Current PersonalityProfile

        Returns:
            PreferenceDetectionResult with hints based on interaction
        """
        result = PreferenceDetectionResult()

        # Analyze response length vs user preference for detail
        response_length = len(system_response.split())
        if "too long" in user_message.lower() or "tldr" in user_message.lower():
            # User prefers shorter responses - indicates simplified/medium technical depth
            technical_hint = PreferenceHint(
                id=self._next_hint_id(),
                user_id=user_id,
                dimension=PreferenceDimension.TECHNICAL,
                detected_value=TechnicalPreference.SIMPLIFIED,
                current_value=current_profile.technical_depth,
                detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
                confidence_score=0.85,
                source_text=f"User indicated response was too long",
                evidence={"response_length": response_length},
            )
            result.hints.append(technical_hint)

        if "more detail" in user_message.lower() or "explain more" in user_message.lower():
            # User wants more detail
            technical_hint = PreferenceHint(
                id=self._next_hint_id(),
                user_id=user_id,
                dimension=PreferenceDimension.TECHNICAL,
                detected_value=TechnicalPreference.DETAILED,
                current_value=current_profile.technical_depth,
                detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
                confidence_score=0.9,
                source_text=f"User asked for more detail",
                evidence={"request_type": "explicit_detail_request"},
            )
            result.hints.append(technical_hint)

        # Categorize hints
        result.suggested_hints = [h for h in result.hints if h.is_ready_for_suggestion()]
        result.auto_apply_hints = [h for h in result.hints if h.is_ready_for_auto_apply()]

        if result.hints:
            result.analysis_summary = self._generate_analysis_summary(result.hints)

        return result

    def analyze_feedback(
        self, user_id: str, feedback_text: str, current_profile: Any
    ) -> PreferenceDetectionResult:
        """
        Analyze explicit user feedback (e.g., settings changes, profile updates).

        Args:
            user_id: User ID
            feedback_text: User's explicit feedback
            current_profile: Current PersonalityProfile

        Returns:
            PreferenceDetectionResult with hints from feedback
        """
        result = PreferenceDetectionResult()

        # Parse feedback for explicit preference statements
        if any(
            word in feedback_text.lower()
            for word in ["more warm", "friendlier", "casual", "relaxed"]
        ):
            warmth_hint = PreferenceHint(
                id=self._next_hint_id(),
                user_id=user_id,
                dimension=PreferenceDimension.WARMTH,
                detected_value=0.8,
                current_value=current_profile.warmth_level,
                detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
                confidence_score=0.95,
                source_text=feedback_text,
                evidence={"feedback_type": "explicit_warmth_request"},
            )
            result.hints.append(warmth_hint)

        if any(
            word in feedback_text.lower()
            for word in ["more action", "next steps", "always tell me what to do"]
        ):
            action_hint = PreferenceHint(
                id=self._next_hint_id(),
                user_id=user_id,
                dimension=PreferenceDimension.ACTION,
                detected_value=ActionLevel.HIGH,
                current_value=current_profile.action_orientation,
                detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
                confidence_score=0.95,
                source_text=feedback_text,
                evidence={"feedback_type": "explicit_action_request"},
            )
            result.hints.append(action_hint)

        # Categorize hints
        result.suggested_hints = [h for h in result.hints if h.is_ready_for_suggestion()]
        result.auto_apply_hints = [h for h in result.hints if h.is_ready_for_auto_apply()]

        if result.hints:
            result.analysis_summary = self._generate_analysis_summary(result.hints)

        return result

    # Private detection methods for each dimension

    def _detect_warmth_preference(
        self, user_id: str, message: str, current_profile: Any
    ) -> Optional[PreferenceHint]:
        """Detect warmth/friendliness preference from message"""
        message_lower = message.lower()
        words = set(message_lower.split())

        warm_score = len(words & self.WARM_WORDS) / (len(words) + 1)
        prof_score = len(words & self.PROFESSIONAL_WORDS) / (len(words) + 1)

        # Detect if user shows preference different from current
        if warm_score > prof_score and warm_score > 0.05:
            # User showing warm signals
            if current_profile.warmth_level < 0.7:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.WARMTH,
                    detected_value=0.8,
                    current_value=current_profile.warmth_level,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.7, warm_score * 2),
                    source_text=message,
                    evidence={"warm_word_ratio": warm_score, "professional_word_ratio": prof_score},
                )

        elif prof_score > warm_score and prof_score > 0.05:
            # User showing professional signals
            if current_profile.warmth_level > 0.3:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.WARMTH,
                    detected_value=0.3,
                    current_value=current_profile.warmth_level,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.7, prof_score * 2),
                    source_text=message,
                    evidence={"warm_word_ratio": warm_score, "professional_word_ratio": prof_score},
                )

        return None

    def _detect_action_preference(
        self, user_id: str, message: str, current_profile: Any
    ) -> Optional[PreferenceHint]:
        """Detect action orientation preference from message"""
        message_lower = message.lower()
        words = set(message_lower.split())

        action_score = len(words & self.ACTION_WORDS) / (len(words) + 1)
        exploratory_score = len(words & self.EXPLORATORY_WORDS) / (len(words) + 1)

        if action_score > exploratory_score and action_score > 0.05:
            # User showing action-oriented signals
            if current_profile.action_orientation != ActionLevel.HIGH:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.ACTION,
                    detected_value=ActionLevel.HIGH,
                    current_value=current_profile.action_orientation,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.6, action_score * 2),
                    source_text=message,
                    evidence={
                        "action_word_ratio": action_score,
                        "exploratory_word_ratio": exploratory_score,
                    },
                )

        elif exploratory_score > action_score and exploratory_score > 0.05:
            # User showing exploratory signals
            if current_profile.action_orientation != ActionLevel.LOW:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.ACTION,
                    detected_value=ActionLevel.LOW,
                    current_value=current_profile.action_orientation,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.6, exploratory_score * 2),
                    source_text=message,
                    evidence={
                        "action_word_ratio": action_score,
                        "exploratory_word_ratio": exploratory_score,
                    },
                )

        return None

    def _detect_confidence_preference(
        self, user_id: str, message: str, current_profile: Any
    ) -> Optional[PreferenceHint]:
        """Detect confidence display preference from message"""
        message_lower = message.lower()
        words = set(message_lower.split())

        numeric_score = len(words & self.NUMERIC_WORDS) / (len(words) + 1)
        contextual_score = len(words & self.CONTEXTUAL_WORDS) / (len(words) + 1)

        if numeric_score > contextual_score and numeric_score > 0.05:
            # User shows preference for numeric confidence
            if current_profile.confidence_style != ConfidenceDisplayStyle.NUMERIC:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.CONFIDENCE,
                    detected_value=ConfidenceDisplayStyle.NUMERIC,
                    current_value=current_profile.confidence_style,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.55, numeric_score * 2),
                    source_text=message,
                    evidence={
                        "numeric_word_ratio": numeric_score,
                        "contextual_word_ratio": contextual_score,
                    },
                )

        elif contextual_score > numeric_score and contextual_score > 0.05:
            # User shows preference for contextual confidence
            if current_profile.confidence_style != ConfidenceDisplayStyle.CONTEXTUAL:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.CONFIDENCE,
                    detected_value=ConfidenceDisplayStyle.CONTEXTUAL,
                    current_value=current_profile.confidence_style,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.55, contextual_score * 2),
                    source_text=message,
                    evidence={
                        "numeric_word_ratio": numeric_score,
                        "contextual_word_ratio": contextual_score,
                    },
                )

        return None

    def _detect_technical_preference(
        self, user_id: str, message: str, current_profile: Any
    ) -> Optional[PreferenceHint]:
        """Detect technical depth preference from message"""
        message_lower = message.lower()
        words = set(message_lower.split())

        technical_score = len(words & self.TECHNICAL_WORDS) / (len(words) + 1)
        simplified_score = len(words & self.SIMPLIFIED_WORDS) / (len(words) + 1)

        if technical_score > simplified_score and technical_score > 0.05:
            # User shows preference for technical detail
            if current_profile.technical_depth != TechnicalPreference.DETAILED:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.TECHNICAL,
                    detected_value=TechnicalPreference.DETAILED,
                    current_value=current_profile.technical_depth,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.65, technical_score * 2),
                    source_text=message,
                    evidence={
                        "technical_word_ratio": technical_score,
                        "simplified_word_ratio": simplified_score,
                    },
                )

        elif simplified_score > technical_score and simplified_score > 0.05:
            # User shows preference for simplified language
            if current_profile.technical_depth != TechnicalPreference.SIMPLIFIED:
                return PreferenceHint(
                    id=self._next_hint_id(),
                    user_id=user_id,
                    dimension=PreferenceDimension.TECHNICAL,
                    detected_value=TechnicalPreference.SIMPLIFIED,
                    current_value=current_profile.technical_depth,
                    detection_method=DetectionMethod.LANGUAGE_PATTERNS,
                    confidence_score=min(0.65, simplified_score * 2),
                    source_text=message,
                    evidence={
                        "technical_word_ratio": technical_score,
                        "simplified_word_ratio": simplified_score,
                    },
                )

        return None

    def _generate_analysis_summary(self, hints: List[PreferenceHint]) -> str:
        """Generate human-readable summary of detected preferences"""
        if not hints:
            return "No preferences detected"

        summaries = []
        for hint in hints:
            confidence_level = hint.confidence_level()
            summaries.append(
                f"Detected {hint.dimension.value.replace('_', ' ')} preference: "
                f"{hint.detected_value} ({confidence_level.value} confidence)"
            )

        return "; ".join(summaries)

    def _next_hint_id(self) -> str:
        """Generate next hint ID"""
        self.hint_counter += 1
        return f"hint_{self.hint_counter}_{uuid4().hex[:8]}"

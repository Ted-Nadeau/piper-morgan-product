"""
Warmth calibration for grammar-conscious responses.

Warmth isn't about adding personality everywhere - it's about
removing coldness where it creates distance. The goal is Piper
feeling like a colleague, not Piper being chatty.

The Contractor Test: Would this tone feel appropriate from a
contractor you hired last month?

See: #619 GRAMMAR-TRANSFORM: Intent Classification
Pattern: Pattern-053 (Warmth Calibration)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from services.personality.formality import formality_label as _formality_label
from services.shared_types import InteractionSpace


class WarmthLevel(str, Enum):
    """How warm/cold the response should be."""

    COOL = "cool"  # Terse, minimal warmth (CLI, errors)
    NEUTRAL = "neutral"  # Professional, balanced
    WARM = "warm"  # Friendly, encouraging
    SUPPORTIVE = "supportive"  # Extra care (confusion, frustration)


@dataclass
class WarmthCalibration:
    """Calibration result for response warmth."""

    level: WarmthLevel
    formality: str
    can_use_encouragement: bool
    can_acknowledge_effort: bool
    error_gentleness: float  # 0.0 = direct, 1.0 = very gentle
    formality_baseline: Optional[float] = None  # warmth 0.0-1.0 from PersonalityProfile

    @property
    def formality_label(self) -> str:
        """Presentation label derived from formality_baseline or formality string.

        Returns:
            "warm", "balanced", or "professional"
        """
        if self.formality_baseline is not None:
            return _formality_label(self.formality_baseline)
        # Fallback: map legacy formality strings to labels
        _legacy_map = {
            "warm": "warm",
            "casual": "warm",
            "professional": "balanced",
            "terse": "professional",
        }
        return _legacy_map.get(self.formality, "balanced")


class WarmthCalibrator:
    """
    Calibrates response warmth based on context.

    The calibrator considers:
    - Confidence level (lower confidence → more supportive)
    - Place (Slack DM → warmer than public channel)
    - Apparent user state (confusion → more supportive)
    """

    def calibrate(
        self,
        confidence: float,
        place: InteractionSpace,
        place_settings: Dict[str, Any],
        is_error: bool = False,
        seems_frustrated: bool = False,
        formality_baseline: Optional[float] = None,
    ) -> WarmthCalibration:
        """
        Calibrate warmth for a response.

        Args:
            confidence: Classification confidence (0.0-1.0)
            place: Where the conversation is happening
            place_settings: Settings from PlaceDetector
            is_error: Whether this is an error response
            seems_frustrated: Whether user seems frustrated
            formality_baseline: Optional warmth level from PersonalityProfile
                (0.0 = professional, 1.0 = warm). When provided, context
                modulates around this baseline (±1 WarmthLevel shift max).

        Returns:
            WarmthCalibration with appropriate settings
        """
        formality = place_settings.get("formality", "professional")

        # Determine base warmth level
        level = self._determine_warmth_level(
            confidence,
            place,
            formality,
            is_error,
            seems_frustrated,
            formality_baseline=formality_baseline,
        )

        # Determine what warmth behaviors are appropriate
        can_encourage = self._can_use_encouragement(level, formality)
        can_acknowledge = self._can_acknowledge_effort(level, place)
        error_gentleness = self._calculate_error_gentleness(level, is_error, seems_frustrated)

        return WarmthCalibration(
            level=level,
            formality=formality,
            can_use_encouragement=can_encourage,
            can_acknowledge_effort=can_acknowledge,
            error_gentleness=error_gentleness,
            formality_baseline=formality_baseline,
        )

    # Ordered warmth levels for shift arithmetic
    _WARMTH_ORDER: List[WarmthLevel] = [
        WarmthLevel.COOL,
        WarmthLevel.NEUTRAL,
        WarmthLevel.WARM,
        WarmthLevel.SUPPORTIVE,
    ]

    @classmethod
    def _warmth_level_from_baseline(cls, baseline: float) -> WarmthLevel:
        """Convert a warmth float (0.0-1.0) to a WarmthLevel.

        Mapping (per #838 specification):
            warmth >= 0.75 → WARM (SUPPORTIVE reserved for context triggers)
            warmth >= 0.5  → WARM
            warmth >= 0.25 → NEUTRAL
            warmth <  0.25 → COOL
        """
        if baseline >= 0.5:
            return WarmthLevel.WARM
        elif baseline >= 0.25:
            return WarmthLevel.NEUTRAL
        else:
            return WarmthLevel.COOL

    @classmethod
    def _shift_warmth(cls, level: WarmthLevel, shift: int) -> WarmthLevel:
        """Shift a WarmthLevel by *shift* positions (clamped to valid range).

        Positive shift = warmer, negative = cooler.
        """
        idx = cls._WARMTH_ORDER.index(level)
        new_idx = max(0, min(len(cls._WARMTH_ORDER) - 1, idx + shift))
        return cls._WARMTH_ORDER[new_idx]

    def _determine_warmth_level(
        self,
        confidence: float,
        place: InteractionSpace,
        formality: str,
        is_error: bool,
        seems_frustrated: bool,
        formality_baseline: Optional[float] = None,
    ) -> WarmthLevel:
        """Determine the appropriate warmth level.

        When *formality_baseline* is provided the baseline sets the starting
        WarmthLevel and context signals (frustration, errors, low confidence)
        can shift it up by at most **one** level.  This prevents a professional
        user from suddenly getting SUPPORTIVE language on every error.

        When *formality_baseline* is ``None`` the legacy behaviour is preserved.
        """
        if formality_baseline is not None:
            return self._determine_warmth_level_from_baseline(
                formality_baseline,
                confidence,
                place,
                is_error,
                seems_frustrated,
            )

        # --- Legacy path (no baseline) ---

        # Frustrated users need support
        if seems_frustrated:
            return WarmthLevel.SUPPORTIVE

        # Errors need care (but not on CLI)
        if is_error and place != InteractionSpace.CLI:
            return WarmthLevel.SUPPORTIVE

        # Low confidence means Piper is uncertain - be warmer
        if confidence < 0.5:
            return WarmthLevel.WARM

        # Place-based defaults
        if place == InteractionSpace.CLI:
            return WarmthLevel.COOL
        if place == InteractionSpace.SLACK_DM:
            return WarmthLevel.WARM
        if place == InteractionSpace.WEB_CHAT:
            return WarmthLevel.WARM

        # Default based on formality
        formality_warmth = {
            "terse": WarmthLevel.COOL,
            "professional": WarmthLevel.NEUTRAL,
            "casual": WarmthLevel.WARM,
            "warm": WarmthLevel.WARM,
        }
        return formality_warmth.get(formality, WarmthLevel.NEUTRAL)

    def _determine_warmth_level_from_baseline(
        self,
        baseline: float,
        confidence: float,
        place: InteractionSpace,
        is_error: bool,
        seems_frustrated: bool,
    ) -> WarmthLevel:
        """Baseline-aware warmth: modulate around user preference.

        Context signals (frustrated, error, low confidence) shift the
        baseline up by at most one WarmthLevel position.
        """
        base_level = self._warmth_level_from_baseline(baseline)

        # Determine if context warrants a +1 shift
        needs_extra_warmth = (
            seems_frustrated or (is_error and place != InteractionSpace.CLI) or confidence < 0.5
        )

        if needs_extra_warmth:
            return self._shift_warmth(base_level, +1)

        return base_level

    def _can_use_encouragement(self, level: WarmthLevel, formality: str) -> bool:
        """Can we add encouraging language?"""
        # CLI and terse contexts: no encouragement
        if formality == "terse":
            return False
        # Only warm and supportive levels use encouragement
        return level in (WarmthLevel.WARM, WarmthLevel.SUPPORTIVE)

    def _can_acknowledge_effort(self, level: WarmthLevel, place: InteractionSpace) -> bool:
        """Can we acknowledge user's effort/difficulty?"""
        # Public channels: don't call out difficulty publicly
        if place == InteractionSpace.SLACK_CHANNEL:
            return False
        # Only warm and supportive levels acknowledge effort
        return level in (WarmthLevel.WARM, WarmthLevel.SUPPORTIVE)

    def _calculate_error_gentleness(
        self,
        level: WarmthLevel,
        is_error: bool,
        seems_frustrated: bool,
    ) -> float:
        """
        Calculate how gentle to be with errors (0.0-1.0).

        Higher values mean softer error language:
        - 0.0: "Invalid input"
        - 0.5: "I couldn't understand that"
        - 1.0: "I want to help, but I'm not quite following"
        """
        if not is_error:
            return 0.0  # Not relevant

        base_gentleness = {
            WarmthLevel.COOL: 0.2,
            WarmthLevel.NEUTRAL: 0.4,
            WarmthLevel.WARM: 0.7,
            WarmthLevel.SUPPORTIVE: 1.0,
        }
        gentleness = base_gentleness.get(level, 0.4)

        # Extra gentleness for frustrated users
        if seems_frustrated:
            gentleness = min(1.0, gentleness + 0.3)

        return gentleness

    def get_error_phrase(
        self,
        calibration: WarmthCalibration,
        error_type: str = "general",
        formality_baseline: Optional[float] = None,
    ) -> str:
        """
        Get appropriately calibrated error phrase.

        Args:
            calibration: WarmthCalibration result
            error_type: Type of error (general, not_found, invalid, confused)
            formality_baseline: Optional warmth baseline (for future use)

        Returns:
            Appropriately warm error phrase
        """
        gentleness = calibration.error_gentleness

        error_phrases = {
            "general": {
                0.0: "Error occurred.",
                0.3: "Something went wrong.",
                0.5: "I ran into a problem.",
                0.7: "I'm having trouble with that.",
                1.0: "I want to help, but something's not working right.",
            },
            "not_found": {
                0.0: "Not found.",
                0.3: "I couldn't find that.",
                0.5: "I wasn't able to locate that.",
                0.7: "I looked but couldn't find what you're looking for.",
                1.0: "I searched but came up empty—could you give me more details?",
            },
            "invalid": {
                0.0: "Invalid input.",
                0.3: "That doesn't look right.",
                0.5: "I couldn't process that.",
                0.7: "I'm having trouble understanding that format.",
                1.0: "I want to help, but I'm not quite sure how to read that.",
            },
            "confused": {
                0.0: "Unable to interpret.",
                0.3: "I don't understand.",
                0.5: "I'm not sure what you mean.",
                0.7: "I'm a bit confused by that.",
                1.0: "I want to make sure I help you right—could you rephrase that?",
            },
        }

        phrases = error_phrases.get(error_type, error_phrases["general"])

        # Find the closest gentleness level
        levels = sorted(phrases.keys())
        selected_level = min(levels, key=lambda x: abs(x - gentleness))

        return phrases[selected_level]

    def get_encouragement(
        self,
        calibration: WarmthCalibration,
        context: str = "success",
        formality_baseline: Optional[float] = None,
    ) -> Optional[str]:
        """
        Get encouragement phrase if appropriate.

        Args:
            calibration: WarmthCalibration result
            context: Context for encouragement (success, progress, trying)
            formality_baseline: Optional warmth baseline (for future use)

        Returns:
            Encouragement phrase or None if not appropriate
        """
        if not calibration.can_use_encouragement:
            return None

        encouragements = {
            "success": {
                WarmthLevel.WARM: "Nice!",
                WarmthLevel.SUPPORTIVE: "Great job!",
            },
            "progress": {
                WarmthLevel.WARM: "Getting there.",
                WarmthLevel.SUPPORTIVE: "You're making progress!",
            },
            "trying": {
                WarmthLevel.WARM: "Good thinking.",
                WarmthLevel.SUPPORTIVE: "I appreciate you working through this.",
            },
        }

        context_phrases = encouragements.get(context, encouragements["success"])
        return context_phrases.get(calibration.level)

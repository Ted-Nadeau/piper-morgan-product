# Agent Prompt: Phase 4 - Warmth Calibration (#619)

**Issue**: #619 GRAMMAR-TRANSFORM: Intent Classification
**Phase**: 4 of 6 (can run parallel with 2, 3 after Phase 1)
**Estimated Time**: 1 hour
**Pattern**: Pattern-053 (Warmth Calibration)
**Prerequisite**: Phase 1 complete (PerceptionMode, PlaceType exist)

---

## Objective

Create a warmth calibration module that determines the appropriate tone for responses based on confidence level, Place, and context. This is a support module for the personality bridge.

---

## Task 1: Create Warmth Calibration Module

**File**: `services/intent_service/warmth_calibration.py`

```python
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
from typing import Any, Dict, Optional

from services.shared_types import PlaceType


class WarmthLevel(str, Enum):
    """How warm/cold the response should be."""
    COOL = "cool"           # Terse, minimal warmth (CLI, errors)
    NEUTRAL = "neutral"     # Professional, balanced
    WARM = "warm"           # Friendly, encouraging
    SUPPORTIVE = "supportive"  # Extra care (confusion, frustration)


@dataclass
class WarmthCalibration:
    """Calibration result for response warmth."""
    level: WarmthLevel
    formality: str
    can_use_encouragement: bool
    can_acknowledge_effort: bool
    error_gentleness: float  # 0.0 = direct, 1.0 = very gentle


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
        place: PlaceType,
        place_settings: Dict[str, Any],
        is_error: bool = False,
        seems_frustrated: bool = False,
    ) -> WarmthCalibration:
        """
        Calibrate warmth for a response.

        Args:
            confidence: Classification confidence (0.0-1.0)
            place: Where the conversation is happening
            place_settings: Settings from PlaceDetector
            is_error: Whether this is an error response
            seems_frustrated: Whether user seems frustrated

        Returns:
            WarmthCalibration with appropriate settings
        """
        formality = place_settings.get("formality", "professional")

        # Determine base warmth level
        level = self._determine_warmth_level(
            confidence, place, formality, is_error, seems_frustrated
        )

        # Determine what warmth behaviors are appropriate
        can_encourage = self._can_use_encouragement(level, formality)
        can_acknowledge = self._can_acknowledge_effort(level, place)
        error_gentleness = self._calculate_error_gentleness(
            level, is_error, seems_frustrated
        )

        return WarmthCalibration(
            level=level,
            formality=formality,
            can_use_encouragement=can_encourage,
            can_acknowledge_effort=can_acknowledge,
            error_gentleness=error_gentleness,
        )

    def _determine_warmth_level(
        self,
        confidence: float,
        place: PlaceType,
        formality: str,
        is_error: bool,
        seems_frustrated: bool,
    ) -> WarmthLevel:
        """Determine the appropriate warmth level."""
        # Frustrated users need support
        if seems_frustrated:
            return WarmthLevel.SUPPORTIVE

        # Errors need care (but not on CLI)
        if is_error and place != PlaceType.CLI:
            return WarmthLevel.SUPPORTIVE

        # Low confidence means Piper is uncertain - be warmer
        if confidence < 0.5:
            return WarmthLevel.WARM

        # Place-based defaults
        if place == PlaceType.CLI:
            return WarmthLevel.COOL
        if place == PlaceType.SLACK_DM:
            return WarmthLevel.WARM
        if place == PlaceType.WEB_CHAT:
            return WarmthLevel.WARM

        # Default based on formality
        formality_warmth = {
            "terse": WarmthLevel.COOL,
            "professional": WarmthLevel.NEUTRAL,
            "casual": WarmthLevel.WARM,
            "warm": WarmthLevel.WARM,
        }
        return formality_warmth.get(formality, WarmthLevel.NEUTRAL)

    def _can_use_encouragement(
        self, level: WarmthLevel, formality: str
    ) -> bool:
        """Can we add encouraging language?"""
        # CLI and terse contexts: no encouragement
        if formality == "terse":
            return False
        # Only warm and supportive levels use encouragement
        return level in (WarmthLevel.WARM, WarmthLevel.SUPPORTIVE)

    def _can_acknowledge_effort(
        self, level: WarmthLevel, place: PlaceType
    ) -> bool:
        """Can we acknowledge user's effort/difficulty?"""
        # Public channels: don't call out difficulty publicly
        if place == PlaceType.SLACK_CHANNEL:
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
        self, calibration: WarmthCalibration, error_type: str = "general"
    ) -> str:
        """
        Get appropriately calibrated error phrase.

        Args:
            calibration: WarmthCalibration result
            error_type: Type of error (general, not_found, invalid, confused)

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
        self, calibration: WarmthCalibration, context: str = "success"
    ) -> Optional[str]:
        """
        Get encouragement phrase if appropriate.

        Args:
            calibration: WarmthCalibration result
            context: Context for encouragement (success, progress, trying)

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
```

---

## Task 2: Create Unit Tests

**File**: `tests/unit/services/intent_service/test_warmth_calibration.py`

```python
"""Tests for WarmthCalibrator."""

import pytest

from services.shared_types import PlaceType
from services.intent_service.warmth_calibration import (
    WarmthCalibrator,
    WarmthCalibration,
    WarmthLevel,
)


class TestWarmthCalibrator:
    """Test WarmthCalibrator calibration logic."""

    @pytest.fixture
    def calibrator(self):
        return WarmthCalibrator()

    @pytest.fixture
    def casual_settings(self):
        return {"formality": "casual", "verbosity": "medium"}

    @pytest.fixture
    def professional_settings(self):
        return {"formality": "professional", "verbosity": "concise"}

    @pytest.fixture
    def terse_settings(self):
        return {"formality": "terse", "verbosity": "minimal"}

    # --- Warmth Level Tests ---

    def test_cli_is_cool(self, calibrator, terse_settings):
        """CLI context produces COOL warmth."""
        calibration = calibrator.calibrate(
            confidence=0.9,
            place=PlaceType.CLI,
            place_settings=terse_settings,
        )
        assert calibration.level == WarmthLevel.COOL

    def test_slack_dm_is_warm(self, calibrator, casual_settings):
        """Slack DM produces WARM warmth."""
        calibration = calibrator.calibrate(
            confidence=0.9,
            place=PlaceType.SLACK_DM,
            place_settings=casual_settings,
        )
        assert calibration.level == WarmthLevel.WARM

    def test_frustrated_user_gets_support(self, calibrator, professional_settings):
        """Frustrated users get SUPPORTIVE warmth."""
        calibration = calibrator.calibrate(
            confidence=0.9,
            place=PlaceType.SLACK_CHANNEL,
            place_settings=professional_settings,
            seems_frustrated=True,
        )
        assert calibration.level == WarmthLevel.SUPPORTIVE

    def test_low_confidence_increases_warmth(self, calibrator, professional_settings):
        """Low confidence increases warmth level."""
        calibration = calibrator.calibrate(
            confidence=0.3,
            place=PlaceType.SLACK_CHANNEL,
            place_settings=professional_settings,
        )
        assert calibration.level == WarmthLevel.WARM

    def test_error_triggers_support(self, calibrator, casual_settings):
        """Errors trigger SUPPORTIVE (except CLI)."""
        calibration = calibrator.calibrate(
            confidence=0.9,
            place=PlaceType.WEB_CHAT,
            place_settings=casual_settings,
            is_error=True,
        )
        assert calibration.level == WarmthLevel.SUPPORTIVE

    # --- Encouragement Tests ---

    def test_warm_can_encourage(self, calibrator, casual_settings):
        """WARM level can use encouragement."""
        calibration = calibrator.calibrate(
            confidence=0.9,
            place=PlaceType.SLACK_DM,
            place_settings=casual_settings,
        )
        assert calibration.can_use_encouragement is True

    def test_terse_no_encouragement(self, calibrator, terse_settings):
        """Terse formality disables encouragement."""
        calibration = calibrator.calibrate(
            confidence=0.9,
            place=PlaceType.CLI,
            place_settings=terse_settings,
        )
        assert calibration.can_use_encouragement is False

    # --- Error Gentleness Tests ---

    def test_error_gentleness_scales_with_warmth(self, calibrator, casual_settings):
        """Error gentleness increases with warmth level."""
        cool_cal = WarmthCalibration(
            level=WarmthLevel.COOL,
            formality="terse",
            can_use_encouragement=False,
            can_acknowledge_effort=False,
            error_gentleness=0.2,
        )
        warm_cal = WarmthCalibration(
            level=WarmthLevel.WARM,
            formality="casual",
            can_use_encouragement=True,
            can_acknowledge_effort=True,
            error_gentleness=0.7,
        )
        assert cool_cal.error_gentleness < warm_cal.error_gentleness

    # --- Error Phrase Tests ---

    def test_gentle_error_phrase(self, calibrator):
        """High gentleness produces soft error phrases."""
        calibration = WarmthCalibration(
            level=WarmthLevel.SUPPORTIVE,
            formality="warm",
            can_use_encouragement=True,
            can_acknowledge_effort=True,
            error_gentleness=1.0,
        )
        phrase = calibrator.get_error_phrase(calibration, "confused")
        assert "help" in phrase.lower()
        assert "rephrase" in phrase.lower()

    def test_terse_error_phrase(self, calibrator):
        """Low gentleness produces direct error phrases."""
        calibration = WarmthCalibration(
            level=WarmthLevel.COOL,
            formality="terse",
            can_use_encouragement=False,
            can_acknowledge_effort=False,
            error_gentleness=0.0,
        )
        phrase = calibrator.get_error_phrase(calibration, "not_found")
        assert phrase == "Not found."

    # --- Encouragement Phrase Tests ---

    def test_encouragement_when_allowed(self, calibrator):
        """Gets encouragement phrase when allowed."""
        calibration = WarmthCalibration(
            level=WarmthLevel.WARM,
            formality="casual",
            can_use_encouragement=True,
            can_acknowledge_effort=True,
            error_gentleness=0.7,
        )
        phrase = calibrator.get_encouragement(calibration, "success")
        assert phrase is not None
        assert "!" in phrase  # Encouraging punctuation

    def test_no_encouragement_when_disallowed(self, calibrator):
        """No encouragement when not allowed."""
        calibration = WarmthCalibration(
            level=WarmthLevel.COOL,
            formality="terse",
            can_use_encouragement=False,
            can_acknowledge_effort=False,
            error_gentleness=0.2,
        )
        phrase = calibrator.get_encouragement(calibration, "success")
        assert phrase is None


class TestContractorTest:
    """Verify warmth passes the 'Contractor Test'."""

    def test_warmth_not_excessive(self):
        """Warmth shouldn't feel over-the-top."""
        calibrator = WarmthCalibrator()

        # Even at max warmth, phrases should feel professional
        calibration = WarmthCalibration(
            level=WarmthLevel.SUPPORTIVE,
            formality="warm",
            can_use_encouragement=True,
            can_acknowledge_effort=True,
            error_gentleness=1.0,
        )

        phrase = calibrator.get_error_phrase(calibration, "confused")

        # Should NOT contain
        assert "!" not in phrase  # No exclamation in errors
        assert "awesome" not in phrase.lower()
        assert "amazing" not in phrase.lower()
        assert "super" not in phrase.lower()

        # SHOULD be helpful
        assert "help" in phrase.lower() or "sure" in phrase.lower()
```

---

## Acceptance Criteria

- [ ] WarmthCalibrator class created
- [ ] WarmthLevel enum (COOL, NEUTRAL, WARM, SUPPORTIVE)
- [ ] calibrate() considers confidence, place, errors, frustration
- [ ] Error gentleness scales appropriately
- [ ] Error phrases calibrated by gentleness level
- [ ] Encouragement only when appropriate
- [ ] Contractor Test passes (warmth isn't excessive)
- [ ] All unit tests pass: `pytest tests/unit/services/intent_service/test_warmth_calibration.py -v`

---

## Verification Commands

```bash
# Run the new tests
pytest tests/unit/services/intent_service/test_warmth_calibration.py -v

# Verify import works
python -c "from services.intent_service.warmth_calibration import WarmthCalibrator, WarmthLevel; print('WarmthCalibrator OK')"

# Quick manual test
python -c "
from services.intent_service.warmth_calibration import WarmthCalibrator
from services.shared_types import PlaceType

cal = WarmthCalibrator()

# Test different scenarios
print('CLI high confidence:', cal.calibrate(0.9, PlaceType.CLI, {'formality': 'terse'}).level)
print('DM low confidence:', cal.calibrate(0.3, PlaceType.SLACK_DM, {'formality': 'casual'}).level)
print('Error:', cal.calibrate(0.9, PlaceType.WEB_CHAT, {'formality': 'warm'}, is_error=True).level)
"
```

---

## Notes

- This phase does NOT modify classifier.py
- WarmthCalibrator is a support module for PersonalityBridge
- Error phrases follow the "Contractor Test" principle
- Encouragement is conservative - only when clearly appropriate

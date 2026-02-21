"""Tests for formality_baseline integration in WarmthCalibrator (#838).

Validates that WarmthCalibrator correctly accepts a formality_baseline
from PersonalityProfile and modulates around it with at most one
WarmthLevel shift for context signals.
"""

import pytest

from services.intent_service.warmth_calibration import (
    WarmthCalibration,
    WarmthCalibrator,
    WarmthLevel,
)
from services.shared_types import InteractionSpace


@pytest.fixture
def calibrator():
    return WarmthCalibrator()


@pytest.fixture
def default_settings():
    """Neutral place settings so the baseline drives the outcome."""
    return {"formality": "professional", "verbosity": "medium"}


class TestBaselineHappyPath:
    """formality_baseline → WarmthLevel mapping (no context modifiers)."""

    def test_baseline_0_8_produces_warm(self, calibrator, default_settings):
        """Warm user preference (0.8) → WARM level."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            formality_baseline=0.8,
        )
        assert cal.level == WarmthLevel.WARM

    def test_baseline_0_2_produces_cool(self, calibrator, default_settings):
        """Professional user preference (0.2) → COOL level."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            formality_baseline=0.2,
        )
        assert cal.level == WarmthLevel.COOL

    def test_baseline_0_5_produces_warm(self, calibrator, default_settings):
        """Balanced user preference (0.5) → WARM level (>= 0.5 threshold)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            formality_baseline=0.5,
        )
        assert cal.level == WarmthLevel.WARM

    def test_baseline_0_3_produces_neutral(self, calibrator, default_settings):
        """Mid-low preference (0.3) → NEUTRAL level."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            formality_baseline=0.3,
        )
        assert cal.level == WarmthLevel.NEUTRAL

    def test_baseline_0_1_produces_cool(self, calibrator, default_settings):
        """Very professional preference (0.1) → COOL level."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            formality_baseline=0.1,
        )
        assert cal.level == WarmthLevel.COOL


class TestBaselineWithContextModulation:
    """Context signals (frustrated, error, low confidence) shift baseline +1."""

    def test_warm_baseline_frustrated_becomes_supportive(self, calibrator, default_settings):
        """baseline=0.8 + frustrated → SUPPORTIVE (WARM +1)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            seems_frustrated=True,
            formality_baseline=0.8,
        )
        assert cal.level == WarmthLevel.SUPPORTIVE

    def test_cool_baseline_frustrated_becomes_neutral(self, calibrator, default_settings):
        """baseline=0.2 + frustrated → NEUTRAL (COOL +1)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            seems_frustrated=True,
            formality_baseline=0.2,
        )
        assert cal.level == WarmthLevel.NEUTRAL

    def test_cool_baseline_error_becomes_neutral(self, calibrator, default_settings):
        """baseline=0.2 + error → NEUTRAL (COOL +1), NOT SUPPORTIVE."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.WEB_CHAT,
            place_settings=default_settings,
            is_error=True,
            formality_baseline=0.2,
        )
        assert cal.level == WarmthLevel.NEUTRAL

    def test_neutral_baseline_error_becomes_warm(self, calibrator, default_settings):
        """baseline=0.3 + error → WARM (NEUTRAL +1)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.WEB_CHAT,
            place_settings=default_settings,
            is_error=True,
            formality_baseline=0.3,
        )
        assert cal.level == WarmthLevel.WARM

    def test_low_confidence_shifts_up_one(self, calibrator, default_settings):
        """baseline=0.2 + low confidence → NEUTRAL (COOL +1)."""
        cal = calibrator.calibrate(
            confidence=0.3,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            formality_baseline=0.2,
        )
        assert cal.level == WarmthLevel.NEUTRAL

    def test_supportive_already_max_stays_supportive(self, calibrator, default_settings):
        """baseline=0.8 (WARM) + frustrated → SUPPORTIVE (capped at max)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            seems_frustrated=True,
            formality_baseline=0.8,
        )
        assert cal.level == WarmthLevel.SUPPORTIVE


class TestBaselineNoneFallsBackToLegacy:
    """When formality_baseline is None, existing behavior is preserved."""

    def test_none_baseline_frustrated_goes_supportive(self, calibrator, default_settings):
        """Legacy: frustrated → SUPPORTIVE (unchanged)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            seems_frustrated=True,
            formality_baseline=None,
        )
        assert cal.level == WarmthLevel.SUPPORTIVE

    def test_none_baseline_cli_is_cool(self, calibrator):
        """Legacy: CLI → COOL (unchanged)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.CLI,
            place_settings={"formality": "terse"},
            formality_baseline=None,
        )
        assert cal.level == WarmthLevel.COOL

    def test_none_baseline_slack_dm_is_warm(self, calibrator):
        """Legacy: Slack DM → WARM (unchanged)."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_DM,
            place_settings={"formality": "casual"},
            formality_baseline=None,
        )
        assert cal.level == WarmthLevel.WARM

    def test_omitted_baseline_same_as_none(self, calibrator, default_settings):
        """Omitting formality_baseline entirely works like None."""
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
        )
        # With professional formality and no context triggers, legacy gives NEUTRAL
        assert cal.level == WarmthLevel.NEUTRAL


class TestConflictResolution:
    """Baseline limits how far context can push warmth."""

    def test_professional_baseline_error_caps_at_neutral(self, calibrator, default_settings):
        """baseline=0.2 (COOL) + error → NEUTRAL, NOT SUPPORTIVE.

        This is the key conflict resolution test: a professional user who hits
        an error should get slightly warmer, not full supportive mode.
        """
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.WEB_CHAT,
            place_settings=default_settings,
            is_error=True,
            formality_baseline=0.2,
        )
        assert cal.level == WarmthLevel.NEUTRAL
        assert cal.level != WarmthLevel.SUPPORTIVE

    def test_professional_baseline_all_triggers_still_caps(self, calibrator, default_settings):
        """baseline=0.2 + frustrated + error + low confidence → still just NEUTRAL.

        Multiple context triggers don't stack — max shift is always +1.
        """
        cal = calibrator.calibrate(
            confidence=0.3,
            place=InteractionSpace.WEB_CHAT,
            place_settings=default_settings,
            is_error=True,
            seems_frustrated=True,
            formality_baseline=0.2,
        )
        assert cal.level == WarmthLevel.NEUTRAL


class TestFormalityBaselineStored:
    """The formality_baseline value is stored on the calibration result."""

    def test_baseline_stored_on_result(self, calibrator, default_settings):
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
            formality_baseline=0.8,
        )
        assert cal.formality_baseline == 0.8

    def test_none_baseline_stored_as_none(self, calibrator, default_settings):
        cal = calibrator.calibrate(
            confidence=0.9,
            place=InteractionSpace.SLACK_CHANNEL,
            place_settings=default_settings,
        )
        assert cal.formality_baseline is None


class TestFormalityLabel:
    """WarmthCalibration.formality_label property."""

    def test_label_warm_from_baseline(self):
        cal = WarmthCalibration(
            level=WarmthLevel.WARM,
            formality="professional",
            can_use_encouragement=True,
            can_acknowledge_effort=True,
            error_gentleness=0.7,
            formality_baseline=0.8,
        )
        assert cal.formality_label == "warm"

    def test_label_balanced_from_baseline(self):
        cal = WarmthCalibration(
            level=WarmthLevel.NEUTRAL,
            formality="professional",
            can_use_encouragement=False,
            can_acknowledge_effort=False,
            error_gentleness=0.4,
            formality_baseline=0.5,
        )
        assert cal.formality_label == "balanced"

    def test_label_professional_from_baseline(self):
        cal = WarmthCalibration(
            level=WarmthLevel.COOL,
            formality="professional",
            can_use_encouragement=False,
            can_acknowledge_effort=False,
            error_gentleness=0.2,
            formality_baseline=0.1,
        )
        assert cal.formality_label == "professional"

    def test_label_falls_back_to_formality_string_when_no_baseline(self):
        cal = WarmthCalibration(
            level=WarmthLevel.NEUTRAL,
            formality="professional",
            can_use_encouragement=False,
            can_acknowledge_effort=False,
            error_gentleness=0.4,
        )
        assert cal.formality_label == "balanced"

    def test_label_terse_formality_maps_to_professional(self):
        cal = WarmthCalibration(
            level=WarmthLevel.COOL,
            formality="terse",
            can_use_encouragement=False,
            can_acknowledge_effort=False,
            error_gentleness=0.2,
        )
        assert cal.formality_label == "professional"

    def test_label_casual_formality_maps_to_warm(self):
        cal = WarmthCalibration(
            level=WarmthLevel.WARM,
            formality="casual",
            can_use_encouragement=True,
            can_acknowledge_effort=True,
            error_gentleness=0.7,
        )
        assert cal.formality_label == "warm"


class TestHelperMethods:
    """Internal helper correctness."""

    def test_warmth_level_from_baseline_boundaries(self):
        """Verify boundary values in the mapping."""
        assert WarmthCalibrator._warmth_level_from_baseline(0.0) == WarmthLevel.COOL
        assert WarmthCalibrator._warmth_level_from_baseline(0.24) == WarmthLevel.COOL
        assert WarmthCalibrator._warmth_level_from_baseline(0.25) == WarmthLevel.NEUTRAL
        assert WarmthCalibrator._warmth_level_from_baseline(0.49) == WarmthLevel.NEUTRAL
        assert WarmthCalibrator._warmth_level_from_baseline(0.5) == WarmthLevel.WARM
        assert WarmthCalibrator._warmth_level_from_baseline(0.75) == WarmthLevel.WARM
        assert WarmthCalibrator._warmth_level_from_baseline(1.0) == WarmthLevel.WARM

    def test_shift_warmth_up(self):
        assert WarmthCalibrator._shift_warmth(WarmthLevel.COOL, +1) == WarmthLevel.NEUTRAL
        assert WarmthCalibrator._shift_warmth(WarmthLevel.NEUTRAL, +1) == WarmthLevel.WARM
        assert WarmthCalibrator._shift_warmth(WarmthLevel.WARM, +1) == WarmthLevel.SUPPORTIVE

    def test_shift_warmth_clamped_at_max(self):
        assert WarmthCalibrator._shift_warmth(WarmthLevel.SUPPORTIVE, +1) == WarmthLevel.SUPPORTIVE

    def test_shift_warmth_down(self):
        assert WarmthCalibrator._shift_warmth(WarmthLevel.WARM, -1) == WarmthLevel.NEUTRAL
        assert WarmthCalibrator._shift_warmth(WarmthLevel.COOL, -1) == WarmthLevel.COOL

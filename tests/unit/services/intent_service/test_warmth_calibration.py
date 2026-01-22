"""Tests for WarmthCalibrator."""

import pytest

from services.intent_service.warmth_calibration import (
    WarmthCalibration,
    WarmthCalibrator,
    WarmthLevel,
)
from services.shared_types import PlaceType


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

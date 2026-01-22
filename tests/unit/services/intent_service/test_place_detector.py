"""Tests for PlaceDetector."""

import pytest

from services.intent_service.place_detector import PlaceDetector
from services.shared_types import PlaceType


class TestPlaceDetector:
    """Test PlaceDetector detection logic."""

    @pytest.fixture
    def detector(self):
        return PlaceDetector()

    # --- Detection Tests ---

    def test_no_context_returns_unknown(self, detector):
        """Missing context defaults to UNKNOWN."""
        assert detector.detect(None) == PlaceType.UNKNOWN
        assert detector.detect({}) == PlaceType.UNKNOWN

    def test_explicit_source_cli(self, detector):
        """Explicit CLI source detected."""
        assert detector.detect({"source": "cli"}) == PlaceType.CLI
        assert detector.detect({"source": "CLI"}) == PlaceType.CLI

    def test_explicit_source_api(self, detector):
        """Explicit API source detected."""
        assert detector.detect({"source": "api"}) == PlaceType.API

    def test_explicit_source_web(self, detector):
        """Explicit web source detected."""
        assert detector.detect({"source": "web"}) == PlaceType.WEB_CHAT
        assert detector.detect({"source": "web_chat"}) == PlaceType.WEB_CHAT

    def test_slack_dm_detection(self, detector):
        """Slack DM detected from is_dm flag."""
        context = {"room_id": "D123ABC", "is_dm": True}
        assert detector.detect(context) == PlaceType.SLACK_DM

    def test_slack_channel_detection(self, detector):
        """Slack channel detected from channel without is_dm."""
        context = {"channel": "C123ABC", "is_dm": False}
        assert detector.detect(context) == PlaceType.SLACK_CHANNEL

        # Also works with room_id
        context2 = {"room_id": "C456DEF"}
        assert detector.detect(context2) == PlaceType.SLACK_CHANNEL

    def test_slack_indicators(self, detector):
        """Various Slack indicators trigger Slack detection."""
        # workspace_id alone suggests Slack channel
        assert detector.detect({"workspace_id": "T123"}) == PlaceType.SLACK_CHANNEL

        # thread_ts suggests Slack
        assert detector.detect({"thread_ts": "123.456"}) == PlaceType.SLACK_CHANNEL

    def test_web_from_browser_indicator(self, detector):
        """Browser indicator suggests web chat."""
        assert detector.detect({"browser": "chrome"}) == PlaceType.WEB_CHAT
        assert detector.detect({"web_session": "abc123"}) == PlaceType.WEB_CHAT

    # --- Settings Tests ---

    def test_slack_dm_settings_casual(self, detector):
        """Slack DM settings are casual."""
        settings = detector.get_place_settings(PlaceType.SLACK_DM)
        assert settings["formality"] == "casual"
        assert settings["can_use_emoji"] is True

    def test_slack_channel_settings_professional(self, detector):
        """Slack channel settings are professional."""
        settings = detector.get_place_settings(PlaceType.SLACK_CHANNEL)
        assert settings["formality"] == "professional"
        assert settings["verbosity"] == "concise"
        assert settings["can_use_emoji"] is False

    def test_cli_settings_terse(self, detector):
        """CLI settings are terse."""
        settings = detector.get_place_settings(PlaceType.CLI)
        assert settings["formality"] == "terse"
        assert settings["verbosity"] == "minimal"

    def test_web_settings_warm(self, detector):
        """Web chat settings are warm."""
        settings = detector.get_place_settings(PlaceType.WEB_CHAT)
        assert settings["formality"] == "warm"
        assert settings["verbosity"] == "full"

    def test_unknown_defaults_professional(self, detector):
        """Unknown Place defaults to professional."""
        settings = detector.get_place_settings(PlaceType.UNKNOWN)
        assert settings["formality"] == "professional"

    # --- Convenience Method Tests ---

    def test_detect_with_settings(self, detector):
        """Convenience method returns both Place and settings."""
        context = {"source": "cli"}
        place, settings = detector.detect_with_settings(context)

        assert place == PlaceType.CLI
        assert settings["formality"] == "terse"


class TestPlaceSettingsCompleteness:
    """Ensure all PlaceTypes have settings."""

    def test_all_place_types_have_settings(self):
        """Every PlaceType has corresponding settings."""
        detector = PlaceDetector()
        for place_type in PlaceType:
            settings = detector.get_place_settings(place_type)
            assert "formality" in settings
            assert "verbosity" in settings
            assert "can_use_emoji" in settings

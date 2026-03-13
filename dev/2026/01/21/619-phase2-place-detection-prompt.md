# Agent Prompt: Phase 2 - Place Detection (#619)

**Issue**: #619 GRAMMAR-TRANSFORM: Intent Classification
**Phase**: 2 of 6 (can run parallel with 3, 4 after Phase 1)
**Estimated Time**: 2 hours
**Pattern**: Pattern-051 (Parallel Place Gathering)
**Prerequisite**: Phase 1 complete (PlaceType enum exists)

---

## Objective

Create a PlaceDetector that determines where a conversation is happening (Slack DM, channel, web, CLI, etc.) and provides Place-appropriate settings.

---

## Task 1: Create PlaceDetector

**File**: `services/intent_service/place_detector.py`

```python
"""
Place detection for grammar-conscious intent classification.

The Place in MUX grammar represents WHERE the interaction happens.
Different Places call for different communication styles:
- Slack DM: casual, can be personal
- Slack channel: professional, concise (others watching)
- Web chat: warm, full explanations
- CLI: terse, no fluff

See: #619 GRAMMAR-TRANSFORM: Intent Classification
"""

from typing import Any, Dict, Optional

from services.shared_types import PlaceType


class PlaceDetector:
    """
    Detects the Place where a conversation is happening.

    Place awareness lets Piper adjust her communication style
    appropriately - more casual in DMs, more professional in
    public channels, more terse on CLI.
    """

    # Place-specific communication settings
    PLACE_SETTINGS: Dict[PlaceType, Dict[str, Any]] = {
        PlaceType.SLACK_DM: {
            "formality": "casual",
            "verbosity": "medium",
            "can_use_emoji": True,
            "max_response_lines": 20,
        },
        PlaceType.SLACK_CHANNEL: {
            "formality": "professional",
            "verbosity": "concise",
            "can_use_emoji": False,
            "max_response_lines": 10,
        },
        PlaceType.WEB_CHAT: {
            "formality": "warm",
            "verbosity": "full",
            "can_use_emoji": True,
            "max_response_lines": 50,
        },
        PlaceType.CLI: {
            "formality": "terse",
            "verbosity": "minimal",
            "can_use_emoji": False,
            "max_response_lines": 5,
        },
        PlaceType.API: {
            "formality": "neutral",
            "verbosity": "structured",
            "can_use_emoji": False,
            "max_response_lines": 100,
        },
        PlaceType.UNKNOWN: {
            "formality": "professional",
            "verbosity": "medium",
            "can_use_emoji": False,
            "max_response_lines": 15,
        },
    }

    def detect(self, spatial_context: Optional[Dict[str, Any]]) -> PlaceType:
        """
        Determine PlaceType from spatial context.

        Args:
            spatial_context: Dictionary with location hints from the request.
                Common keys: room_id, channel, is_dm, source, workspace_id

        Returns:
            PlaceType indicating where this conversation is happening.
        """
        if not spatial_context:
            return PlaceType.UNKNOWN

        # Check for explicit source indicator (highest priority)
        source = spatial_context.get("source", "").lower()
        if source == "cli":
            return PlaceType.CLI
        if source == "api":
            return PlaceType.API
        if source in ("web", "web_chat"):
            return PlaceType.WEB_CHAT

        # Check for Slack indicators
        if self._is_slack_context(spatial_context):
            if spatial_context.get("is_dm", False):
                return PlaceType.SLACK_DM
            # Has channel but not DM = public channel
            if spatial_context.get("channel") or spatial_context.get("room_id"):
                return PlaceType.SLACK_CHANNEL

        # Check for web indicators
        if spatial_context.get("browser") or spatial_context.get("web_session"):
            return PlaceType.WEB_CHAT

        return PlaceType.UNKNOWN

    def _is_slack_context(self, spatial_context: Dict[str, Any]) -> bool:
        """Check if this looks like a Slack context."""
        slack_indicators = [
            "room_id",
            "channel",
            "workspace_id",
            "thread_ts",
            "team_id",
            "slack_user_id",
        ]
        return any(key in spatial_context for key in slack_indicators)

    def get_place_settings(self, place: PlaceType) -> Dict[str, Any]:
        """
        Get communication settings appropriate for this Place.

        Args:
            place: The PlaceType to get settings for.

        Returns:
            Dictionary with formality, verbosity, emoji, and line limit settings.
        """
        return self.PLACE_SETTINGS.get(place, self.PLACE_SETTINGS[PlaceType.UNKNOWN])

    def detect_with_settings(
        self, spatial_context: Optional[Dict[str, Any]]
    ) -> tuple[PlaceType, Dict[str, Any]]:
        """
        Convenience method to detect Place and get settings in one call.

        Args:
            spatial_context: Location context dictionary.

        Returns:
            Tuple of (PlaceType, settings dictionary).
        """
        place = self.detect(spatial_context)
        settings = self.get_place_settings(place)
        return place, settings
```

---

## Task 2: Create Unit Tests

**File**: `tests/unit/services/intent_service/test_place_detector.py`

```python
"""Tests for PlaceDetector."""

import pytest

from services.shared_types import PlaceType
from services.intent_service.place_detector import PlaceDetector


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
```

---

## Task 3: Add __init__.py Export

**File**: `services/intent_service/__init__.py`

Add to exports (if file exists, extend; if not, create):

```python
from services.intent_service.place_detector import PlaceDetector

__all__ = [
    # ... existing exports ...
    "PlaceDetector",
]
```

---

## Acceptance Criteria

- [ ] PlaceDetector class created with detect() method
- [ ] Detection handles: Slack DM, Slack channel, web, CLI, API, unknown
- [ ] PLACE_SETTINGS defined for all PlaceTypes
- [ ] get_place_settings() returns appropriate settings
- [ ] detect_with_settings() convenience method works
- [ ] All unit tests pass: `pytest tests/unit/services/intent_service/test_place_detector.py -v`

---

## Verification Commands

```bash
# Run the new tests
pytest tests/unit/services/intent_service/test_place_detector.py -v

# Verify import works
python -c "from services.intent_service.place_detector import PlaceDetector; print('PlaceDetector OK')"

# Quick manual test
python -c "
from services.intent_service.place_detector import PlaceDetector
d = PlaceDetector()
print('CLI:', d.detect({'source': 'cli'}))
print('Slack DM:', d.detect({'room_id': 'D123', 'is_dm': True}))
print('Slack Channel:', d.detect({'channel': 'C123'}))
print('Unknown:', d.detect({}))
"
```

---

## Notes

- This phase does NOT modify classifier.py
- PlaceDetector will be integrated in Phase 6
- Settings can be extended later (these are starting values)
- Consider caching Place detection per session for performance (future optimization)

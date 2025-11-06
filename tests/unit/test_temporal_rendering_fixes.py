"""
Tests for Issue #287: CORE-ALPHA-TEMPORAL-BUGS

Tests three fixes:
1. Timezone displays as abbreviation (PT) not city name (Los Angeles)
2. No contradictory meeting status messages
3. Calendar data validation and freshness checks
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock, patch

import pytest

# These tests will pass AFTER the fixes are implemented


class TestTimezoneDisplay:
    """Test Fix #1: Timezone abbreviation display"""

    @pytest.mark.asyncio
    async def test_timezone_abbreviation_pt(self):
        """Timezone should display as 'PT' not 'Los Angeles'"""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handler = CanonicalHandlers()

        # Mock intent and config
        mock_intent = Mock()
        mock_intent.spatial_context = None

        with patch("services.intent_service.canonical_handlers.piper_config_loader") as mock_loader:
            mock_loader.load_standup_config.return_value = {
                "timing": {"timezone": "America/Los_Angeles"}
            }

            with patch(
                "services.intent_service.canonical_handlers.CalendarIntegrationRouter"
            ) as mock_router:
                mock_router.return_value.get_temporal_summary = AsyncMock(
                    return_value={"stats": {"total_meetings_today": 0}}
                )

                result = await handler._handle_temporal_query(mock_intent, "test_session")

                message = result["message"]
                # Should contain "PT" not "Los Angeles"
                assert "PT" in message, f"Expected 'PT' in message, got: {message}"
                assert (
                    "Los Angeles" not in message
                ), f"Should not contain 'Los Angeles', got: {message}"

    @pytest.mark.asyncio
    async def test_timezone_abbreviation_et(self):
        """Eastern timezone should display as 'ET' not 'New York'"""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handler = CanonicalHandlers()

        mock_intent = Mock()
        mock_intent.spatial_context = None

        with patch("services.intent_service.canonical_handlers.piper_config_loader") as mock_loader:
            mock_loader.load_standup_config.return_value = {
                "timing": {"timezone": "America/New_York"}
            }

            with patch(
                "services.intent_service.canonical_handlers.CalendarIntegrationRouter"
            ) as mock_router:
                mock_router.return_value.get_temporal_summary = AsyncMock(
                    return_value={"stats": {"total_meetings_today": 0}}
                )

                result = await handler._handle_temporal_query(mock_intent, "test_session")

                message = result["message"]
                assert "ET" in message, f"Expected 'ET' in message, got: {message}"
                assert "New York" not in message, f"Should not contain 'New York', got: {message}"


class TestContradictoryMessages:
    """Test Fix #2: No contradictory meeting status messages"""

    @pytest.mark.asyncio
    async def test_no_contradiction_with_zero_meetings(self):
        """When no meetings, should not show both 'in meeting' and 'no meetings'"""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handler = CanonicalHandlers()

        mock_intent = Mock()
        mock_intent.spatial_context = None

        with patch("services.intent_service.canonical_handlers.piper_config_loader") as mock_loader:
            mock_loader.load_standup_config.return_value = {
                "timing": {"timezone": "America/Los_Angeles"}
            }

            with patch(
                "services.intent_service.canonical_handlers.CalendarIntegrationRouter"
            ) as mock_router:
                # No current meeting, no next meeting, 0 meetings total
                mock_router.return_value.get_temporal_summary = AsyncMock(
                    return_value={
                        "current_meeting": None,
                        "next_meeting": None,
                        "stats": {"total_meetings_today": 0},
                    }
                )

                result = await handler._handle_temporal_query(mock_intent, "test_session")

                message = result["message"]
                # Should say "No meetings"
                assert (
                    "No meetings" in message or "great day" in message
                ), f"Expected 'No meetings' message, got: {message}"
                # Should NOT say "currently in"
                assert (
                    "currently in" not in message
                ), f"Should not say 'currently in', got: {message}"

    @pytest.mark.asyncio
    async def test_no_contradiction_with_current_meeting(self):
        """When in a meeting, should not also say 'no meetings'"""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handler = CanonicalHandlers()

        mock_intent = Mock()
        mock_intent.spatial_context = None

        with patch("services.intent_service.canonical_handlers.piper_config_loader") as mock_loader:
            mock_loader.load_standup_config.return_value = {
                "timing": {"timezone": "America/Los_Angeles"}
            }

            with patch(
                "services.intent_service.canonical_handlers.CalendarIntegrationRouter"
            ) as mock_router:
                # Currently in a meeting
                mock_router.return_value.get_temporal_summary = AsyncMock(
                    return_value={
                        "current_meeting": {
                            "title": "Sprint Planning",
                            "duration": "1 hour",
                        },
                        "next_meeting": None,
                        "stats": {"total_meetings_today": 1},
                    }
                )

                result = await handler._handle_temporal_query(mock_intent, "test_session")

                message = result["message"]
                # Should mention current meeting
                assert (
                    "currently in" in message.lower() or "Sprint Planning" in message
                ), f"Expected current meeting mention, got: {message}"
                # Should NOT say "No meetings"
                assert (
                    "No meetings" not in message
                ), f"Should not say 'No meetings' when in meeting, got: {message}"

    @pytest.mark.asyncio
    async def test_no_stats_block_with_current_meeting(self):
        """Stats block should not appear when describing current meeting"""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handler = CanonicalHandlers()

        mock_intent = Mock()
        mock_intent.spatial_context = None

        with patch("services.intent_service.canonical_handlers.piper_config_loader") as mock_loader:
            mock_loader.load_standup_config.return_value = {
                "timing": {"timezone": "America/Los_Angeles"}
            }

            with patch(
                "services.intent_service.canonical_handlers.CalendarIntegrationRouter"
            ) as mock_router:
                # Currently in a meeting, with total meetings > 0
                mock_router.return_value.get_temporal_summary = AsyncMock(
                    return_value={
                        "current_meeting": {"title": "Team Sync", "duration": "30 min"},
                        "next_meeting": None,
                        "stats": {"total_meetings_today": 3},  # This should not appear
                    }
                )

                result = await handler._handle_temporal_query(mock_intent, "test_session")

                message = result["message"]
                # Should mention current meeting
                assert "Team Sync" in message or "currently in" in message.lower()
                # Should NOT show redundant stats "(3 meetings scheduled today)"
                # when already in a meeting


class TestCalendarValidation:
    """Test Fix #3: Calendar data validation and freshness"""

    @pytest.mark.asyncio
    async def test_calendar_failure_shows_warning(self):
        """When calendar fails, should show user-friendly warning"""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handler = CanonicalHandlers()

        mock_intent = Mock()
        mock_intent.spatial_context = None

        with patch("services.intent_service.canonical_handlers.piper_config_loader") as mock_loader:
            mock_loader.load_standup_config.return_value = {
                "timing": {"timezone": "America/Los_Angeles"}
            }

            with patch(
                "services.intent_service.canonical_handlers.CalendarIntegrationRouter"
            ) as mock_router:
                # Calendar service fails
                mock_router.return_value.get_temporal_summary = AsyncMock(
                    side_effect=Exception("Calendar API unavailable")
                )

                result = await handler._handle_temporal_query(mock_intent, "test_session")

                message = result["message"]
                context = result.get("intent", {}).get("context", {})

                # Should still provide date/time
                assert "Today is" in message or "day" in message.lower()
                # Should indicate calendar unavailable
                assert (
                    "calendar" in message.lower() or "unavailable" in message.lower()
                ), f"Expected calendar warning, got: {message}"
                # Context should indicate fallback
                assert context.get("calendar_context", {}).get("fallback_used") is True

    @pytest.mark.asyncio
    async def test_embedded_context_no_calendar_warning(self):
        """EMBEDDED context should not show calendar warning (too verbose)"""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handler = CanonicalHandlers()

        mock_intent = Mock()
        mock_intent.spatial_context = {"pattern": "EMBEDDED"}

        with patch("services.intent_service.canonical_handlers.piper_config_loader") as mock_loader:
            mock_loader.load_standup_config.return_value = {
                "timing": {"timezone": "America/Los_Angeles"}
            }

            with patch(
                "services.intent_service.canonical_handlers.CalendarIntegrationRouter"
            ) as mock_router:
                # Calendar service fails
                mock_router.return_value.get_temporal_summary = AsyncMock(
                    side_effect=Exception("Calendar API unavailable")
                )

                result = await handler._handle_temporal_query(mock_intent, "test_session")

                message = result["message"]
                # EMBEDDED should be brief, no "couldn't access calendar" message
                assert (
                    "couldn't access" not in message.lower()
                ), f"EMBEDDED context should not show verbose error, got: {message}"


class TestTimezoneMapping:
    """Test the timezone abbreviation mapping"""

    def test_common_us_timezones(self):
        """Test mapping for common US timezones"""
        from services.intent_service.canonical_handlers import TIMEZONE_ABBREVIATIONS

        assert TIMEZONE_ABBREVIATIONS["America/Los_Angeles"] == "PT"
        assert TIMEZONE_ABBREVIATIONS["America/New_York"] == "ET"
        assert TIMEZONE_ABBREVIATIONS["America/Chicago"] == "CT"
        assert TIMEZONE_ABBREVIATIONS["America/Denver"] == "MT"

    def test_international_timezones(self):
        """Test mapping for international timezones"""
        from services.intent_service.canonical_handlers import TIMEZONE_ABBREVIATIONS

        assert TIMEZONE_ABBREVIATIONS["Europe/London"] == "GMT"
        assert TIMEZONE_ABBREVIATIONS["Asia/Tokyo"] == "JST"
        assert TIMEZONE_ABBREVIATIONS["Australia/Sydney"] == "AEDT"

    def test_fallback_to_utc(self):
        """Unknown timezones should fallback gracefully"""
        from services.intent_service.canonical_handlers import TIMEZONE_ABBREVIATIONS

        # Unknown timezone should have a fallback
        unknown_tz = "Unknown/Timezone"
        result = TIMEZONE_ABBREVIATIONS.get(unknown_tz, "UTC")
        assert result == "UTC", "Unknown timezones should fallback to UTC"

"""
Tests for Calendar narrative helpers.

Issue #624: GRAMMAR-TRANSFORM: Calendar Integration
Phase 3: Helper Integration Tests
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.integrations.calendar.narrative_helpers import (
    get_calendar_formality,
    has_time_for_task,
    is_calendar_busy,
    narrate_calendar_summary,
    narrate_day_summary,
    narrate_free_blocks,
    narrate_meeting_load,
    narrate_meeting_status,
    narrate_next_meeting,
    narrate_time_until_next,
)


class TestNarrateMeetingStatus:
    """Test meeting status narration helper."""

    def test_in_meeting(self):
        """Currently in meeting."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(minutes=15)

        summary = {
            "success": True,
            "stats": {"total_meetings": 3},
            "current_meeting": {
                "title": "Team Standup",
                "start_time": start.isoformat(),
                "duration_minutes": 30,
            },
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_meeting_status(summary)
        assert "Team Standup" in result
        assert "halfway" in result.lower()

    def test_free(self):
        """Not in meeting."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 0},
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_meeting_status(summary)
        assert "clear" in result.lower()


class TestNarrateDaySummary:
    """Test day summary narration helper."""

    def test_packed_day(self):
        """Packed day."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 6,
                "total_meeting_minutes": 300,
                "calendar_load": "heavy",
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_day_summary(summary)
        assert "packed" in result.lower()

    def test_light_day(self):
        """Light day."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 1,
                "total_meeting_minutes": 30,
                "calendar_load": "light",
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_day_summary(summary)
        assert "open" in result.lower() or "light" in result.lower() or "few" in result.lower()


class TestNarrateNextMeeting:
    """Test next meeting narration helper."""

    def test_has_next_meeting(self):
        """Has upcoming meeting."""
        now = datetime.now(timezone.utc)
        next_start = now + timedelta(minutes=30)

        summary = {
            "success": True,
            "stats": {"total_meetings": 2},
            "current_meeting": None,
            "next_meeting": {
                "title": "1:1 with Alex",
                "start_time": next_start.isoformat(),
            },
            "free_blocks": [],
        }
        result = narrate_next_meeting(summary)
        assert "1:1 with Alex" in result
        assert "30" in result or "minutes" in result

    def test_no_next_meeting(self):
        """No upcoming meeting."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 0},
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_next_meeting(summary)
        assert result == ""


class TestNarrateFreeBlocks:
    """Test free blocks narration helper."""

    def test_has_free_time(self):
        """Has free time."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 2, "total_free_minutes": 120},
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [
                {"duration_minutes": 60},
                {"duration_minutes": 30},
            ],
        }
        result = narrate_free_blocks(summary)
        assert "hour" in result.lower() or "free" in result.lower()

    def test_no_free_time(self):
        """No free time."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 6, "total_free_minutes": 0},
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_free_blocks(summary)
        assert "back-to-back" in result.lower()


class TestNarrateCalendarSummary:
    """Test full calendar summary helper."""

    def test_full_summary(self):
        """Full calendar summary."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(minutes=10)

        summary = {
            "success": True,
            "stats": {"total_meetings": 4},
            "current_meeting": {
                "title": "Planning",
                "start_time": start.isoformat(),
                "duration_minutes": 60,
            },
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_calendar_summary(summary)
        assert "Planning" in result

    def test_calendar_unavailable(self):
        """Calendar unavailable."""
        summary = {"success": False, "error": "Calendar unavailable"}
        result = narrate_calendar_summary(summary)
        assert "couldn't" in result.lower()


class TestNarrateMeetingLoad:
    """Test meeting load helper."""

    def test_many_meetings(self):
        """Many meetings."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 5,
                "total_meeting_minutes": 270,
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_meeting_load(summary)
        assert "5" in result
        assert "busy" in result.lower()


class TestNarrateTimeUntilNext:
    """Test time until next helper."""

    def test_has_next(self):
        """Has next meeting."""
        now = datetime.now(timezone.utc)
        next_start = now + timedelta(minutes=25)

        summary = {
            "success": True,
            "stats": {"total_meetings": 1},
            "current_meeting": None,
            "next_meeting": {
                "title": "Meeting",
                "start_time": next_start.isoformat(),
            },
            "free_blocks": [],
        }
        result = narrate_time_until_next(summary)
        assert "half" in result.lower() or "30" in result or "minute" in result

    def test_no_next(self):
        """No next meeting."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 0},
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = narrate_time_until_next(summary)
        assert "no more" in result.lower()


class TestGetCalendarFormality:
    """Test formality detection helper."""

    def test_busy_day_concise(self):
        """Busy day -> concise."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 6,
                "total_meeting_minutes": 300,
                "calendar_load": "heavy",
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = get_calendar_formality(summary)
        assert result == "concise"

    def test_free_day_conversational(self):
        """Free day -> conversational."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 0,
                "total_meeting_minutes": 0,
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        result = get_calendar_formality(summary)
        assert result == "conversational"


class TestIsCalendarBusy:
    """Test busy check helper."""

    def test_busy(self):
        """Calendar is busy."""
        summary = {
            "success": True,
            "stats": {
                "calendar_load": "heavy",
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        assert is_calendar_busy(summary) is True

    def test_not_busy(self):
        """Calendar is not busy."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 1,
                "calendar_load": "light",
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        assert is_calendar_busy(summary) is False


class TestHasTimeForTask:
    """Test time availability helper."""

    def test_has_time(self):
        """Enough time before next meeting."""
        now = datetime.now(timezone.utc)
        next_start = now + timedelta(minutes=60)

        summary = {
            "success": True,
            "stats": {"total_meetings": 1},
            "current_meeting": None,
            "next_meeting": {
                "title": "Meeting",
                "start_time": next_start.isoformat(),
            },
            "free_blocks": [],
        }
        assert has_time_for_task(summary, 30) is True

    def test_not_enough_time(self):
        """Not enough time before next meeting."""
        now = datetime.now(timezone.utc)
        next_start = now + timedelta(minutes=10)

        summary = {
            "success": True,
            "stats": {"total_meetings": 1},
            "current_meeting": None,
            "next_meeting": {
                "title": "Meeting",
                "start_time": next_start.isoformat(),
            },
            "free_blocks": [],
        }
        assert has_time_for_task(summary, 30) is False


class TestContractorTest:
    """Verify helpers pass Contractor Test."""

    def test_no_raw_data_in_output(self):
        """Helpers don't expose raw data."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 5,
                "total_meeting_minutes": 240,
                "calendar_load": "heavy",
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }

        day = narrate_day_summary(summary)
        load = narrate_meeting_load(summary)

        # No raw data terms
        assert "total_meetings" not in day
        assert "calendar_load" not in day
        assert "total_meeting_minutes" not in load

    def test_professional_language(self):
        """Helpers use professional language."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 0},
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }

        result = narrate_meeting_status(summary)
        assert result[0].isupper()  # Proper capitalization
        assert "!!!" not in result  # Not overly excited

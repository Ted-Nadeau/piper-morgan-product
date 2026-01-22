"""
Tests for CalendarResponseContext.

Issue #624: GRAMMAR-TRANSFORM: Calendar Integration
Phase 1: CalendarResponseContext dataclass
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.integrations.calendar.response_context import (
    CalendarResponseContext,
    _determine_day_atmosphere,
    _determine_time_pressure,
)


class TestCalendarResponseContext:
    """Test CalendarResponseContext dataclass."""

    def test_basic_creation(self):
        """Can create with defaults."""
        ctx = CalendarResponseContext()
        assert ctx.current_status == "free"
        assert ctx.calendar_available is True
        assert ctx.meeting_count == 0

    def test_full_creation(self):
        """Can create with all fields."""
        ctx = CalendarResponseContext(
            day_atmosphere="packed",
            meeting_count=5,
            meeting_hours=4.0,
            free_hours=2.0,
            current_status="in_meeting",
            current_meeting_title="Team Standup",
            current_meeting_progress=0.5,
            next_meeting_title="1:1 with Alex",
            minutes_until_next=30,
            time_pressure="comfortable",
            longest_free_block=60,
            free_blocks_count=2,
        )
        assert ctx.day_atmosphere == "packed"
        assert ctx.meeting_count == 5
        assert ctx.current_meeting_title == "Team Standup"
        assert ctx.current_meeting_progress == 0.5


class TestFromTemporalSummary:
    """Test from_temporal_summary factory method."""

    def test_empty_calendar(self):
        """Creates context from empty calendar."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 0,
                "total_meeting_minutes": 0,
                "total_free_minutes": 480,
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
        }
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.meeting_count == 0
        assert ctx.current_status == "free"
        assert ctx.day_atmosphere == "focused"

    def test_busy_day(self):
        """Creates context from busy calendar."""
        summary = {
            "success": True,
            "stats": {
                "total_meetings": 6,
                "total_meeting_minutes": 300,
                "total_free_minutes": 60,
                "calendar_load": "heavy",
            },
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [{"duration_minutes": 30}],
        }
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.meeting_count == 6
        assert ctx.meeting_hours == 5.0
        assert ctx.day_atmosphere == "packed"
        assert ctx.calendar_load == "heavy"

    def test_current_meeting(self):
        """Extracts current meeting info."""
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
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.current_status == "in_meeting"
        assert ctx.current_meeting_title == "Team Standup"
        assert 0.4 <= ctx.current_meeting_progress <= 0.6  # ~50%

    def test_next_meeting_soon(self):
        """Extracts next meeting with time pressure."""
        now = datetime.now(timezone.utc)
        next_start = now + timedelta(minutes=10)

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
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.next_meeting_title == "1:1 with Alex"
        assert 8 <= ctx.minutes_until_next <= 12  # ~10 minutes
        assert ctx.time_pressure == "tight"
        assert ctx.current_status == "between_meetings"

    def test_next_meeting_far(self):
        """Next meeting far away = plenty of time."""
        now = datetime.now(timezone.utc)
        next_start = now + timedelta(hours=2)

        summary = {
            "success": True,
            "stats": {"total_meetings": 1},
            "current_meeting": None,
            "next_meeting": {
                "title": "Afternoon Review",
                "start_time": next_start.isoformat(),
            },
            "free_blocks": [],
        }
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.time_pressure == "plenty"

    def test_free_blocks(self):
        """Extracts free block info."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 2, "total_free_minutes": 120},
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [
                {"duration_minutes": 30},
                {"duration_minutes": 60},
                {"duration_minutes": 30},
            ],
        }
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.longest_free_block == 60
        assert ctx.free_blocks_count == 3
        assert ctx.total_free_minutes == 120

    def test_calendar_unavailable(self):
        """Handles calendar failure."""
        summary = {
            "success": False,
            "error": "Calendar unavailable",
        }
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.calendar_available is False
        assert ctx.current_status == "unknown"

    def test_summary_field_variants(self):
        """Handles both 'summary' and 'title' fields."""
        summary = {
            "success": True,
            "stats": {"total_meetings": 1},
            "current_meeting": {
                "summary": "Meeting via summary field",
                "duration_minutes": 30,
            },
            "next_meeting": None,
            "free_blocks": [],
        }
        ctx = CalendarResponseContext.from_temporal_summary(summary)

        assert ctx.current_meeting_title == "Meeting via summary field"


class TestHelperMethods:
    """Test helper methods."""

    def test_is_busy_packed(self):
        """Packed day is busy."""
        ctx = CalendarResponseContext(day_atmosphere="packed")
        assert ctx.is_busy() is True

    def test_is_busy_heavy_load(self):
        """Heavy load is busy."""
        ctx = CalendarResponseContext(calendar_load="heavy")
        assert ctx.is_busy() is True

    def test_not_busy(self):
        """Light day is not busy."""
        ctx = CalendarResponseContext(day_atmosphere="light")
        assert ctx.is_busy() is False

    def test_is_free(self):
        """No meetings and free status."""
        ctx = CalendarResponseContext(
            current_status="free",
            meeting_count=0,
        )
        assert ctx.is_free() is True

    def test_not_free_in_meeting(self):
        """In meeting is not free."""
        ctx = CalendarResponseContext(
            current_status="in_meeting",
            meeting_count=1,
        )
        assert ctx.is_free() is False

    def test_has_time_before_next_yes(self):
        """Has time when meeting is far."""
        ctx = CalendarResponseContext(minutes_until_next=60)
        assert ctx.has_time_before_next(30) is True

    def test_has_time_before_next_no(self):
        """No time when meeting is soon."""
        ctx = CalendarResponseContext(minutes_until_next=10)
        assert ctx.has_time_before_next(30) is False

    def test_has_time_no_next_meeting(self):
        """Has time when no next meeting."""
        ctx = CalendarResponseContext(minutes_until_next=None)
        assert ctx.has_time_before_next(30) is True

    def test_formality_busy(self):
        """Busy day -> concise."""
        ctx = CalendarResponseContext(day_atmosphere="packed")
        assert ctx.get_formality() == "concise"

    def test_formality_rushing(self):
        """Time pressure -> concise."""
        ctx = CalendarResponseContext(time_pressure="rushing")
        assert ctx.get_formality() == "concise"

    def test_formality_free(self):
        """Free day -> conversational."""
        ctx = CalendarResponseContext(
            current_status="free",
            meeting_count=0,
        )
        assert ctx.get_formality() == "conversational"

    def test_formality_normal(self):
        """Normal day -> professional."""
        ctx = CalendarResponseContext(
            day_atmosphere="normal",
            meeting_count=2,
        )
        assert ctx.get_formality() == "professional"


class TestDayAtmosphereHelper:
    """Test _determine_day_atmosphere helper."""

    def test_packed_heavy_load(self):
        """Heavy load -> packed."""
        assert _determine_day_atmosphere(4, 4.0, "heavy") == "packed"

    def test_packed_many_hours(self):
        """Many meeting hours -> packed."""
        assert _determine_day_atmosphere(3, 5.5, "normal") == "packed"

    def test_focused_no_meetings(self):
        """No meetings -> focused."""
        assert _determine_day_atmosphere(0, 0, "light") == "focused"

    def test_light_few_meetings(self):
        """Few short meetings -> light."""
        assert _determine_day_atmosphere(2, 1.5, "light") == "light"

    def test_scattered_many_meetings(self):
        """Many meetings spread out -> scattered."""
        assert _determine_day_atmosphere(5, 3.0, "normal") == "scattered"

    def test_normal_moderate(self):
        """Moderate meetings -> normal."""
        assert _determine_day_atmosphere(3, 3.0, "normal") == "normal"


class TestTimePressureHelper:
    """Test _determine_time_pressure helper."""

    def test_rushing(self):
        """5 min or less -> rushing."""
        assert _determine_time_pressure(5) == "rushing"
        assert _determine_time_pressure(2) == "rushing"

    def test_tight(self):
        """6-15 min -> tight."""
        assert _determine_time_pressure(10) == "tight"
        assert _determine_time_pressure(15) == "tight"

    def test_comfortable(self):
        """16-60 min -> comfortable."""
        assert _determine_time_pressure(30) == "comfortable"
        assert _determine_time_pressure(60) == "comfortable"

    def test_plenty(self):
        """60+ min -> plenty."""
        assert _determine_time_pressure(61) == "plenty"
        assert _determine_time_pressure(120) == "plenty"

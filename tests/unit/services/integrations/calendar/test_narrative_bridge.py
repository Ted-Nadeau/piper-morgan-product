"""
Tests for CalendarNarrativeBridge.

Issue #624: GRAMMAR-TRANSFORM: Calendar Integration
Phase 2: Narrative Bridge Tests
"""

import pytest

from services.integrations.calendar.narrative_bridge import CalendarNarrativeBridge
from services.integrations.calendar.response_context import CalendarResponseContext


class TestNarrateCurrentStatus:
    """Test current status narration."""

    def test_in_meeting_halfway(self):
        """In meeting halfway through."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="in_meeting",
            current_meeting_title="Team Standup",
            current_meeting_progress=0.5,
        )
        result = bridge.narrate_current_status(ctx)
        assert "halfway through" in result
        assert "Team Standup" in result

    def test_in_meeting_starting(self):
        """Just started meeting."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="in_meeting",
            current_meeting_title="Planning",
            current_meeting_progress=0.1,
        )
        result = bridge.narrate_current_status(ctx)
        assert "getting started" in result

    def test_in_meeting_ending(self):
        """Wrapping up meeting."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="in_meeting",
            current_meeting_title="Review",
            current_meeting_progress=0.9,
        )
        result = bridge.narrate_current_status(ctx)
        assert "almost done" in result

    def test_between_meetings(self):
        """Between meetings with time info."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="between_meetings",
            next_meeting_title="1:1 with Alex",
            minutes_until_next=15,
        )
        result = bridge.narrate_current_status(ctx)
        assert "before" in result
        assert "1:1 with Alex" in result

    def test_free_no_meetings(self):
        """Free with no meetings."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="free",
            meeting_count=0,
        )
        result = bridge.narrate_current_status(ctx)
        assert "clear today" in result

    def test_calendar_unavailable(self):
        """Calendar not available."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(calendar_available=False)
        result = bridge.narrate_current_status(ctx)
        assert "couldn't check" in result


class TestNarrateDayAtmosphere:
    """Test day atmosphere narration."""

    def test_packed(self):
        """Packed day."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(day_atmosphere="packed")
        result = bridge.narrate_day_atmosphere(ctx)
        assert "packed" in result

    def test_light(self):
        """Light day."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(day_atmosphere="light")
        result = bridge.narrate_day_atmosphere(ctx)
        assert "open" in result or "focus" in result

    def test_focused(self):
        """Focused day (no meetings)."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(day_atmosphere="focused")
        result = bridge.narrate_day_atmosphere(ctx)
        assert "No meetings" in result or "deep work" in result

    def test_scattered(self):
        """Scattered meetings."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(day_atmosphere="scattered")
        result = bridge.narrate_day_atmosphere(ctx)
        assert "scattered" in result


class TestNarrateMeetingLoad:
    """Test meeting load narration."""

    def test_no_meetings(self):
        """No meetings returns empty."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(meeting_count=0)
        result = bridge.narrate_meeting_load(ctx)
        assert result == ""

    def test_one_short_meeting(self):
        """One short meeting."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(meeting_count=1, meeting_hours=0.5)
        result = bridge.narrate_meeting_load(ctx)
        assert "one" in result.lower()
        assert "short" in result.lower()

    def test_couple_meetings(self):
        """Two meetings."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(meeting_count=2, meeting_hours=1.5)
        result = bridge.narrate_meeting_load(ctx)
        assert "couple" in result.lower()

    def test_many_meetings(self):
        """Many meetings."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(meeting_count=5, meeting_hours=4.5)
        result = bridge.narrate_meeting_load(ctx)
        assert "5" in result
        assert "busy" in result.lower()

    def test_all_day_meetings(self):
        """Meetings all day."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(meeting_count=6, meeting_hours=6.5)
        result = bridge.narrate_meeting_load(ctx)
        assert "most of the day" in result


class TestNarrateFreeTime:
    """Test free time narration."""

    def test_no_meetings(self):
        """No meetings = whole day open."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(meeting_count=0)
        result = bridge.narrate_free_time(ctx)
        assert "whole day" in result.lower()

    def test_hours_free(self):
        """Multiple hours free."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            meeting_count=2,
            longest_free_block=150,
        )
        result = bridge.narrate_free_time(ctx)
        assert "hours" in result or "2" in result

    def test_hour_free(self):
        """One hour free."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            meeting_count=3,
            longest_free_block=60,
        )
        result = bridge.narrate_free_time(ctx)
        assert "hour free" in result

    def test_45_minutes(self):
        """45 minutes free."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            meeting_count=4,
            longest_free_block=45,
        )
        result = bridge.narrate_free_time(ctx)
        assert "45" in result

    def test_30_minutes(self):
        """30 minute window."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            meeting_count=4,
            longest_free_block=30,
        )
        result = bridge.narrate_free_time(ctx)
        assert "30" in result

    def test_quick_breaks(self):
        """Just quick breaks."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            meeting_count=5,
            longest_free_block=15,
        )
        result = bridge.narrate_free_time(ctx)
        assert "quick breaks" in result

    def test_back_to_back(self):
        """No free time."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            meeting_count=6,
            longest_free_block=0,
        )
        result = bridge.narrate_free_time(ctx)
        assert "back-to-back" in result.lower()


class TestNarrateTimeUntilNext:
    """Test time until next meeting narration."""

    def test_no_more_meetings(self):
        """No more meetings."""
        bridge = CalendarNarrativeBridge()
        result = bridge.narrate_time_until_next(None)
        assert "No more meetings" in result

    def test_starting_soon(self):
        """5 minutes or less."""
        bridge = CalendarNarrativeBridge()
        result = bridge.narrate_time_until_next(3)
        assert "starting soon" in result

    def test_few_minutes(self):
        """About 10 minutes."""
        bridge = CalendarNarrativeBridge()
        result = bridge.narrate_time_until_next(8)
        assert "few minutes" in result

    def test_15_minutes(self):
        """About 15 minutes."""
        bridge = CalendarNarrativeBridge()
        result = bridge.narrate_time_until_next(15)
        assert "15" in result

    def test_half_hour(self):
        """About 30 minutes."""
        bridge = CalendarNarrativeBridge()
        result = bridge.narrate_time_until_next(28)
        assert "half an hour" in result.lower()

    def test_about_hour(self):
        """About an hour."""
        bridge = CalendarNarrativeBridge()
        result = bridge.narrate_time_until_next(55)
        assert "hour" in result

    def test_hours_away(self):
        """Multiple hours away."""
        bridge = CalendarNarrativeBridge()
        result = bridge.narrate_time_until_next(150)
        assert "while away" in result or "hours" in result


class TestNarrateNextMeeting:
    """Test next meeting narration."""

    def test_no_next_meeting(self):
        """No next meeting."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(next_meeting_title=None)
        result = bridge.narrate_next_meeting(ctx)
        assert result == ""

    def test_starting_soon(self):
        """Next meeting starting soon."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            next_meeting_title="Team Standup",
            minutes_until_next=3,
        )
        result = bridge.narrate_next_meeting(ctx)
        assert "Team Standup" in result
        assert "soon" in result

    def test_in_minutes(self):
        """Next meeting in X minutes."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            next_meeting_title="1:1 with Alex",
            minutes_until_next=30,
        )
        result = bridge.narrate_next_meeting(ctx)
        assert "1:1 with Alex" in result
        assert "30" in result

    def test_in_hours(self):
        """Next meeting in hours."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            next_meeting_title="Review",
            minutes_until_next=120,
        )
        result = bridge.narrate_next_meeting(ctx)
        assert "Review" in result
        assert "hour" in result


class TestNarrateCalendarSummary:
    """Test full calendar summary narration."""

    def test_calendar_unavailable(self):
        """Calendar not available."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(calendar_available=False)
        result = bridge.narrate_calendar_summary(ctx)
        assert "couldn't access" in result

    def test_clear_calendar(self):
        """Clear calendar."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="free",
            meeting_count=0,
            day_atmosphere="focused",
        )
        result = bridge.narrate_calendar_summary(ctx)
        assert "clear" in result.lower()

    def test_in_meeting(self):
        """Currently in meeting."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="in_meeting",
            current_meeting_title="Planning",
            current_meeting_progress=0.5,
        )
        result = bridge.narrate_calendar_summary(ctx)
        assert "Planning" in result
        assert "halfway" in result

    def test_between_meetings_with_next(self):
        """Between meetings with next meeting info."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            current_status="between_meetings",
            next_meeting_title="Review",
            minutes_until_next=20,
            day_atmosphere="scattered",
        )
        result = bridge.narrate_calendar_summary(ctx)
        assert "Review" in result


class TestProgressPhrase:
    """Test meeting progress phrases."""

    def test_starting(self):
        """0-15% -> starting."""
        bridge = CalendarNarrativeBridge()
        assert "started" in bridge._get_progress_phrase(0.1)

    def test_early(self):
        """15-35% -> early."""
        bridge = CalendarNarrativeBridge()
        assert "early" in bridge._get_progress_phrase(0.25)

    def test_halfway(self):
        """35-65% -> halfway."""
        bridge = CalendarNarrativeBridge()
        assert "halfway" in bridge._get_progress_phrase(0.5)

    def test_late(self):
        """65-85% -> late."""
        bridge = CalendarNarrativeBridge()
        assert "end" in bridge._get_progress_phrase(0.75)

    def test_ending(self):
        """85-100% -> ending."""
        bridge = CalendarNarrativeBridge()
        assert "done" in bridge._get_progress_phrase(0.95)


class TestContractorTest:
    """Verify narratives pass the Contractor Test."""

    def test_no_raw_data_terms(self):
        """Narratives don't use raw data terms."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            day_atmosphere="packed",
            meeting_count=5,
            meeting_hours=4.5,
            current_status="between_meetings",
            minutes_until_next=15,
        )
        result = bridge.narrate_calendar_summary(ctx)

        # Should NOT contain these data-y terms
        assert "meeting_count" not in result
        assert "meeting_hours" not in result
        assert "total_" not in result
        assert "calendar_load" not in result

    def test_natural_language(self):
        """Narratives use natural language."""
        bridge = CalendarNarrativeBridge()

        # Each narrative should read naturally
        assert "packed" in bridge.narrate_day_atmosphere(
            CalendarResponseContext(day_atmosphere="packed")
        )
        assert "focus work" in bridge.narrate_day_atmosphere(
            CalendarResponseContext(day_atmosphere="light")
        )

    def test_professional_tone(self):
        """Narratives maintain professional tone."""
        bridge = CalendarNarrativeBridge()
        ctx = CalendarResponseContext(
            day_atmosphere="packed",
            meeting_count=6,
            meeting_hours=5.0,
        )
        result = bridge.narrate_day_atmosphere(ctx)

        # Professional but not robotic
        assert "!!!" not in result
        assert result[0].isupper()  # Proper capitalization

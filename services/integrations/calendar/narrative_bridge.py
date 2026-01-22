"""
Calendar Narrative Bridge - Transform data to experiential narratives.

This module transforms calendar data structures into human-readable
narratives that pass the Contractor Test. Instead of "5 meetings (4.0 hours)",
Piper says "Your day is packed with meetings."

Issue #624: GRAMMAR-TRANSFORM: Calendar Integration
Phase 2: Narrative Bridge
"""

from dataclasses import dataclass
from typing import Optional

from services.integrations.calendar.response_context import CalendarResponseContext


@dataclass
class CalendarNarrativeBridge:
    """Transform calendar data into experiential narratives.

    In MUX grammar: this bridges Situation data to human expression.
    The goal is responses that sound like a colleague, not a database.
    """

    # Day atmosphere narratives
    DAY_ATMOSPHERE_NARRATIVES = {
        "packed": "Your day is packed with meetings",
        "light": "Pretty open day - good for focus work",
        "scattered": "Meetings scattered throughout the day",
        "focused": "No meetings today - great for deep work",
        "normal": "A few meetings on your calendar",
    }

    # Meeting progress narratives
    MEETING_PROGRESS_NARRATIVES = {
        "starting": "just getting started with",
        "early": "still early in",
        "halfway": "about halfway through",
        "late": "getting toward the end of",
        "ending": "almost done with",
    }

    # Time pressure narratives
    TIME_PRESSURE_NARRATIVES = {
        "rushing": "Your next meeting is starting soon",
        "tight": "You've got a few minutes before your next",
        "comfortable": "Some time before your next meeting",
        "plenty": "Plenty of time until your next meeting",
    }

    def narrate_current_status(self, ctx: CalendarResponseContext) -> str:
        """Describe current meeting status.

        Examples:
            In meeting 50% -> "You're about halfway through Team Standup"
            Between meetings -> "You've got 15 minutes before your next"
            Free -> "Your calendar is clear right now"
        """
        if not ctx.calendar_available:
            return "I couldn't check your calendar right now"

        if ctx.current_status == "in_meeting" and ctx.current_meeting_title:
            progress_phrase = self._get_progress_phrase(ctx.current_meeting_progress)
            return f"You're {progress_phrase} {ctx.current_meeting_title}"

        elif ctx.current_status == "between_meetings":
            if ctx.minutes_until_next is not None and ctx.next_meeting_title:
                time_phrase = self._narrate_minutes(ctx.minutes_until_next)
                return f"You've got {time_phrase} before {ctx.next_meeting_title}"
            return "You're between meetings"

        else:  # free
            if ctx.meeting_count == 0:
                return "Your calendar is clear today"
            return "You're not in a meeting right now"

    def narrate_day_atmosphere(self, ctx: CalendarResponseContext) -> str:
        """Describe overall day feel.

        Examples:
            packed -> "Your day is packed with meetings"
            light -> "Pretty open day - good for focus work"
        """
        if not ctx.calendar_available:
            return ""

        return self.DAY_ATMOSPHERE_NARRATIVES.get(ctx.day_atmosphere, "")

    def narrate_meeting_load(self, ctx: CalendarResponseContext) -> str:
        """Describe meeting load in human terms.

        Examples:
            5 meetings, 4 hours -> "5 meetings taking up most of the day"
            2 meetings, 1 hour -> "Just a couple meetings today"
        """
        if not ctx.calendar_available or ctx.meeting_count == 0:
            return ""

        if ctx.meeting_count == 1:
            if ctx.meeting_hours < 1:
                return "Just one short meeting today"
            return "One meeting today"

        if ctx.meeting_hours >= 6:
            return f"{ctx.meeting_count} meetings taking up most of the day"
        elif ctx.meeting_hours >= 4:
            return f"{ctx.meeting_count} meetings - a busy one"
        elif ctx.meeting_count <= 2:
            return f"Just a couple meetings today"
        else:
            return f"{ctx.meeting_count} meetings on the calendar"

    def narrate_free_time(self, ctx: CalendarResponseContext) -> str:
        """Describe available free time.

        Examples:
            60+ min block -> "You've got an hour free later"
            30 min -> "A 30-minute window available"
            No blocks -> "Back-to-back meetings today"
        """
        if not ctx.calendar_available:
            return ""

        if ctx.meeting_count == 0:
            return "The whole day is open"

        if ctx.longest_free_block >= 120:
            hours = ctx.longest_free_block // 60
            return f"You've got {hours} hours of free time"
        elif ctx.longest_free_block >= 60:
            return "You've got an hour free later"
        elif ctx.longest_free_block >= 45:
            return "About 45 minutes free between meetings"
        elif ctx.longest_free_block >= 30:
            return "A 30-minute window available"
        elif ctx.longest_free_block > 0:
            return "Just quick breaks between meetings"
        else:
            return "Back-to-back meetings today"

    def narrate_time_until_next(self, minutes: Optional[int]) -> str:
        """Describe time until next meeting.

        Examples:
            5 min -> "Your next meeting is starting soon"
            30 min -> "Half an hour until your next meeting"
            120 min -> "Next meeting isn't for a while"
        """
        if minutes is None:
            return "No more meetings today"

        if minutes <= 5:
            return "Your next meeting is starting soon"
        elif minutes <= 10:
            return "Just a few minutes until your next meeting"
        elif minutes <= 15:
            return "About 15 minutes until your next"
        elif minutes <= 30:
            return "Half an hour until your next meeting"
        elif minutes <= 45:
            return "About 45 minutes until your next"
        elif minutes <= 60:
            return "About an hour until your next meeting"
        elif minutes <= 120:
            hours = minutes // 60
            return f"Next meeting isn't for {hours}+ hours"
        else:
            return "Your next meeting is a while away"

    def narrate_next_meeting(self, ctx: CalendarResponseContext) -> str:
        """Describe next meeting with context.

        Examples:
            "1:1 with Alex in 30 minutes"
            "Team Standup coming up soon"
        """
        if not ctx.next_meeting_title:
            return ""

        if ctx.minutes_until_next is None:
            return f"{ctx.next_meeting_title} coming up"

        if ctx.minutes_until_next <= 5:
            return f"{ctx.next_meeting_title} starting soon"
        elif ctx.minutes_until_next <= 15:
            return f"{ctx.next_meeting_title} in a few minutes"
        elif ctx.minutes_until_next <= 60:
            return f"{ctx.next_meeting_title} in {ctx.minutes_until_next} minutes"
        else:
            hours = ctx.minutes_until_next // 60
            return f"{ctx.next_meeting_title} in about {hours} hour{'s' if hours > 1 else ''}"

    def narrate_calendar_summary(
        self,
        ctx: CalendarResponseContext,
        include_current: bool = True,
        include_atmosphere: bool = True,
        include_next: bool = True,
    ) -> str:
        """Create full narrative summary of calendar.

        Combines relevant aspects into natural prose.
        """
        if not ctx.calendar_available:
            return "I couldn't access your calendar right now"

        parts = []

        # Current status
        if include_current:
            current = self.narrate_current_status(ctx)
            if current:
                parts.append(current)

        # Day atmosphere (only if not in meeting or if it adds value)
        if include_atmosphere and ctx.current_status != "in_meeting":
            atmosphere = self.narrate_day_atmosphere(ctx)
            if atmosphere and atmosphere not in str(parts):
                parts.append(atmosphere)

        # Next meeting
        if include_next and ctx.next_meeting_title and ctx.current_status != "in_meeting":
            next_meeting = self.narrate_next_meeting(ctx)
            if next_meeting:
                parts.append(next_meeting)

        if not parts:
            return "Your calendar looks clear"

        # Join naturally
        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 2:
            return f"{parts[0]}. {parts[1]}."
        else:
            return ". ".join(parts) + "."

    def _get_progress_phrase(self, progress: float) -> str:
        """Convert progress (0.0-1.0) to narrative phrase."""
        if progress < 0.15:
            return self.MEETING_PROGRESS_NARRATIVES["starting"]
        elif progress < 0.35:
            return self.MEETING_PROGRESS_NARRATIVES["early"]
        elif progress < 0.65:
            return self.MEETING_PROGRESS_NARRATIVES["halfway"]
        elif progress < 0.85:
            return self.MEETING_PROGRESS_NARRATIVES["late"]
        else:
            return self.MEETING_PROGRESS_NARRATIVES["ending"]

    def _narrate_minutes(self, minutes: int) -> str:
        """Convert minutes to casual time phrase."""
        if minutes <= 5:
            return "just a few minutes"
        elif minutes <= 10:
            return "about 10 minutes"
        elif minutes <= 15:
            return "about 15 minutes"
        elif minutes <= 20:
            return "about 20 minutes"
        elif minutes <= 30:
            return "half an hour"
        elif minutes <= 45:
            return "about 45 minutes"
        elif minutes <= 60:
            return "about an hour"
        else:
            hours = minutes // 60
            return f"about {hours} hour{'s' if hours > 1 else ''}"

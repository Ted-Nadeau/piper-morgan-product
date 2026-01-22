"""
Grammar-conscious Calendar response context.

This module provides rich context for generating grammar-conscious
calendar responses. It captures day atmosphere, meeting status,
and time pressure needed to make Piper's calendar responses feel
experiential rather than data-driven.

Issue #624: GRAMMAR-TRANSFORM: Calendar Integration
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class CalendarResponseContext:
    """
    Rich context for grammar-conscious calendar responses.

    This captures everything Piper knows when discussing calendar:
    - Day atmosphere (packed, light, scattered, focused)
    - Current status (in meeting, between meetings, free)
    - Time pressure (rushing, comfortable, plenty)
    - Available free time

    In MUX grammar: this is the Situation for calendar responses.
    """

    # Day atmosphere
    day_atmosphere: str = "normal"  # "packed", "light", "scattered", "focused", "normal"
    meeting_count: int = 0
    meeting_hours: float = 0.0
    free_hours: float = 0.0

    # Current moment
    current_status: str = "free"  # "in_meeting", "between_meetings", "free"
    current_meeting_title: Optional[str] = None
    current_meeting_progress: float = 0.0  # 0.0 to 1.0 (how far through meeting)
    current_meeting_minutes_elapsed: int = 0
    current_meeting_minutes_remaining: int = 0

    # Next meeting
    next_meeting_title: Optional[str] = None
    minutes_until_next: Optional[int] = None
    time_pressure: str = "comfortable"  # "rushing", "tight", "comfortable", "plenty"

    # Free time blocks
    longest_free_block: int = 0  # minutes
    free_blocks_count: int = 0
    total_free_minutes: int = 0

    # Calendar status
    calendar_available: bool = True
    calendar_load: str = "normal"  # "heavy", "light", "normal"

    # Timestamp
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_temporal_summary(
        cls,
        summary: Dict[str, Any],
    ) -> "CalendarResponseContext":
        """
        Build response context from TemporalSummaryResult dict.

        Args:
            summary: Temporal summary from CalendarIntegrationRouter

        Returns:
            CalendarResponseContext for grammar-conscious responses
        """
        # Check if calendar query succeeded
        if not summary.get("success", True):
            return cls(
                calendar_available=False,
                current_status="unknown",
            )

        # Extract stats
        stats = summary.get("stats", {})
        meeting_count = stats.get("total_meetings", stats.get("total_meetings_today", 0))
        meeting_minutes = stats.get(
            "total_meeting_minutes", stats.get("total_meeting_time_minutes", 0)
        )
        free_minutes = stats.get("total_free_minutes", 0)
        calendar_load = stats.get("calendar_load", "normal")

        meeting_hours = meeting_minutes / 60 if meeting_minutes else 0.0
        free_hours = free_minutes / 60 if free_minutes else 0.0

        # Determine day atmosphere
        day_atmosphere = _determine_day_atmosphere(meeting_count, meeting_hours, calendar_load)

        # Current meeting status
        current_status = "free"
        current_meeting_title = None
        current_meeting_progress = 0.0
        current_meeting_minutes_elapsed = 0
        current_meeting_minutes_remaining = 0

        current_meeting = summary.get("current_meeting")
        if current_meeting:
            current_status = "in_meeting"
            current_meeting_title = current_meeting.get(
                "title", current_meeting.get("summary", "Meeting")
            )
            duration = current_meeting.get("duration_minutes", 60)

            # Calculate progress if we have start time
            if current_meeting.get("start_time"):
                try:
                    start = datetime.fromisoformat(
                        current_meeting["start_time"].replace("Z", "+00:00")
                    )
                    now = datetime.now(start.tzinfo) if start.tzinfo else datetime.now()
                    elapsed = (now - start).total_seconds() / 60
                    current_meeting_minutes_elapsed = int(max(0, elapsed))
                    current_meeting_minutes_remaining = int(max(0, duration - elapsed))
                    current_meeting_progress = (
                        min(1.0, max(0.0, elapsed / duration)) if duration > 0 else 0.0
                    )
                except (ValueError, TypeError):
                    pass

        # Next meeting
        next_meeting_title = None
        minutes_until_next = None
        time_pressure = "comfortable"

        next_meeting = summary.get("next_meeting")
        if next_meeting:
            next_meeting_title = next_meeting.get("title", next_meeting.get("summary", "Meeting"))

            if next_meeting.get("start_time"):
                try:
                    start = datetime.fromisoformat(
                        next_meeting["start_time"].replace("Z", "+00:00")
                    )
                    now = datetime.now(start.tzinfo) if start.tzinfo else datetime.now()
                    delta = (start - now).total_seconds() / 60
                    minutes_until_next = int(max(0, delta))
                    time_pressure = _determine_time_pressure(minutes_until_next)

                    # Update current status if not in meeting
                    if current_status == "free" and minutes_until_next < 60:
                        current_status = "between_meetings"
                except (ValueError, TypeError):
                    pass

        # Free blocks
        free_blocks = summary.get("free_blocks", [])
        longest_free_block = 0
        if free_blocks:
            longest_free_block = max(b.get("duration_minutes", 0) for b in free_blocks)

        return cls(
            day_atmosphere=day_atmosphere,
            meeting_count=meeting_count,
            meeting_hours=meeting_hours,
            free_hours=free_hours,
            current_status=current_status,
            current_meeting_title=current_meeting_title,
            current_meeting_progress=current_meeting_progress,
            current_meeting_minutes_elapsed=current_meeting_minutes_elapsed,
            current_meeting_minutes_remaining=current_meeting_minutes_remaining,
            next_meeting_title=next_meeting_title,
            minutes_until_next=minutes_until_next,
            time_pressure=time_pressure,
            longest_free_block=longest_free_block,
            free_blocks_count=len(free_blocks),
            total_free_minutes=free_minutes,
            calendar_available=True,
            calendar_load=calendar_load,
        )

    def is_busy(self) -> bool:
        """Check if day is busy."""
        return self.day_atmosphere == "packed" or self.calendar_load == "heavy"

    def is_free(self) -> bool:
        """Check if calendar is clear."""
        return self.current_status == "free" and self.meeting_count == 0

    def has_time_before_next(self, minutes: int = 30) -> bool:
        """Check if there's enough time before next meeting."""
        if self.minutes_until_next is None:
            return True
        return self.minutes_until_next >= minutes

    def get_formality(self) -> str:
        """Get appropriate formality based on calendar context.

        Busy day -> more concise
        Light day -> can be more conversational
        """
        if self.is_busy() or self.time_pressure in ("rushing", "tight"):
            return "concise"
        elif self.is_free():
            return "conversational"
        return "professional"


def _determine_day_atmosphere(
    meeting_count: int,
    meeting_hours: float,
    calendar_load: str,
) -> str:
    """Determine day atmosphere from meeting data."""
    if calendar_load == "heavy" or meeting_hours >= 5:
        return "packed"
    elif meeting_count == 0:
        return "focused"  # No meetings = focus day
    elif meeting_count <= 2 and meeting_hours <= 2:
        return "light"
    elif meeting_count >= 4:
        return "scattered"
    return "normal"


def _determine_time_pressure(minutes_until_next: int) -> str:
    """Determine time pressure from minutes until next meeting."""
    if minutes_until_next <= 5:
        return "rushing"
    elif minutes_until_next <= 15:
        return "tight"
    elif minutes_until_next <= 60:
        return "comfortable"
    return "plenty"

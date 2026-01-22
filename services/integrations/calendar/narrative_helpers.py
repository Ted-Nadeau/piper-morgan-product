"""
Calendar Narrative Helpers for Canonical Handlers.

This module provides helper functions to transform raw calendar data
into grammar-conscious narratives within canonical handlers.

Issue #624: GRAMMAR-TRANSFORM: Calendar Integration
Phase 3: Helper Integration
"""

from typing import Any, Dict, Optional

from services.integrations.calendar.narrative_bridge import CalendarNarrativeBridge
from services.integrations.calendar.response_context import CalendarResponseContext

# Singleton bridge instance
_narrative_bridge = CalendarNarrativeBridge()


def narrate_meeting_status(temporal_summary: Dict[str, Any]) -> str:
    """Narrate current meeting status for display.

    Args:
        temporal_summary: TemporalSummaryResult dict from calendar adapter

    Returns:
        Human-readable meeting status string

    Example:
        Input: {"current_meeting": {"title": "Standup", "progress": 0.5}}
        Output: "You're about halfway through Standup"
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return _narrative_bridge.narrate_current_status(ctx)


def narrate_day_summary(temporal_summary: Dict[str, Any]) -> str:
    """Narrate overall day for display.

    Args:
        temporal_summary: TemporalSummaryResult dict

    Returns:
        Human-readable day summary

    Example:
        Input: {"stats": {"total_meetings": 5, "calendar_load": "heavy"}}
        Output: "Your day is packed with meetings"
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return _narrative_bridge.narrate_day_atmosphere(ctx)


def narrate_next_meeting(temporal_summary: Dict[str, Any]) -> str:
    """Narrate next meeting for display.

    Args:
        temporal_summary: TemporalSummaryResult dict

    Returns:
        Human-readable next meeting description

    Example:
        Input: {"next_meeting": {"title": "1:1", "start_time": "..."}}
        Output: "1:1 with Alex in 30 minutes"
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return _narrative_bridge.narrate_next_meeting(ctx)


def narrate_free_blocks(temporal_summary: Dict[str, Any]) -> str:
    """Narrate available free time.

    Args:
        temporal_summary: TemporalSummaryResult dict

    Returns:
        Human-readable free time description

    Example:
        Input: {"free_blocks": [{"duration_minutes": 60}]}
        Output: "You've got an hour free later"
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return _narrative_bridge.narrate_free_time(ctx)


def narrate_calendar_summary(
    temporal_summary: Dict[str, Any],
    include_current: bool = True,
    include_atmosphere: bool = True,
    include_next: bool = True,
) -> str:
    """Narrate full calendar summary.

    Args:
        temporal_summary: TemporalSummaryResult dict
        include_current: Include current meeting status
        include_atmosphere: Include day atmosphere
        include_next: Include next meeting info

    Returns:
        Human-readable calendar summary

    Example:
        Output: "You're about halfway through Standup. Pretty open day - good for focus work."
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return _narrative_bridge.narrate_calendar_summary(
        ctx,
        include_current=include_current,
        include_atmosphere=include_atmosphere,
        include_next=include_next,
    )


def narrate_meeting_load(temporal_summary: Dict[str, Any]) -> str:
    """Narrate meeting load in human terms.

    Args:
        temporal_summary: TemporalSummaryResult dict

    Returns:
        Human-readable meeting load description

    Example:
        Input: {"stats": {"total_meetings": 5, "total_meeting_minutes": 270}}
        Output: "5 meetings - a busy one"
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return _narrative_bridge.narrate_meeting_load(ctx)


def narrate_time_until_next(temporal_summary: Dict[str, Any]) -> str:
    """Narrate time until next meeting.

    Args:
        temporal_summary: TemporalSummaryResult dict

    Returns:
        Human-readable time description

    Example:
        Output: "Half an hour until your next meeting"
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return _narrative_bridge.narrate_time_until_next(ctx.minutes_until_next)


def get_calendar_formality(temporal_summary: Dict[str, Any]) -> str:
    """Get appropriate formality based on calendar context.

    Busy day -> more concise
    Light day -> can be more conversational

    Args:
        temporal_summary: TemporalSummaryResult dict

    Returns:
        "concise", "professional", or "conversational"
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return ctx.get_formality()


def is_calendar_busy(temporal_summary: Dict[str, Any]) -> bool:
    """Check if calendar indicates a busy day.

    Args:
        temporal_summary: TemporalSummaryResult dict

    Returns:
        True if day is busy
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return ctx.is_busy()


def has_time_for_task(temporal_summary: Dict[str, Any], minutes_needed: int = 30) -> bool:
    """Check if there's enough time before next meeting for a task.

    Args:
        temporal_summary: TemporalSummaryResult dict
        minutes_needed: Minimum minutes needed

    Returns:
        True if enough time available
    """
    ctx = CalendarResponseContext.from_temporal_summary(temporal_summary)
    return ctx.has_time_before_next(minutes_needed)

"""
Temporal extraction utilities for calendar queries.

Issue #588: Pragmatic approach to parsing relative date modifiers
(today, tomorrow, this week, next week) without over-engineering.

Future: MUX LLM integration will handle complex natural language dates.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple


def parse_relative_date(
    message: str, user_timezone: Optional[str] = None
) -> Tuple[datetime, datetime, str]:
    """
    Extract date range from message with temporal modifiers.

    Supports: today, tomorrow, this week, next week
    Default: today (if no modifier found)

    Args:
        message: User message to parse
        user_timezone: Optional timezone string (e.g., "America/Los_Angeles")
                      If not provided, uses local system time

    Returns:
        Tuple of (start_date, end_date, label)
        - start_date: Beginning of date range (midnight local time, converted to UTC)
        - end_date: End of date range (midnight next day, converted to UTC)
        - label: Human-readable label ("today", "tomorrow", etc.)
    """
    message_lower = message.lower()

    # Get current time in user's timezone (or local if not specified)
    # Issue #588: Use local time for "today" calculation, then convert to UTC for API
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Check for "tomorrow" first (more specific than "today")
    if "tomorrow" in message_lower:
        start = today_start + timedelta(days=1)
        end = start + timedelta(days=1)
        return (start, end, "tomorrow")

    # "next week" - Monday to Sunday of next week
    if "next week" in message_lower:
        days_until_monday = (7 - today_start.weekday()) % 7 or 7
        start = today_start + timedelta(days=days_until_monday)
        end = start + timedelta(days=7)
        return (start, end, "next week")

    # "this week" - Monday to Sunday of current week
    if "this week" in message_lower:
        start = today_start - timedelta(days=today_start.weekday())
        end = start + timedelta(days=7)
        return (start, end, "this week")

    # Default: today
    return (today_start, today_start + timedelta(days=1), "today")

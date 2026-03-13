# Gameplan: Issue #588 - Tomorrow Calendar Intent

**Issue**: [#588](https://github.com/mediajunkie/piper-morgan-product/issues/588)
**Type**: Bug Fix (P2)
**Template Version**: v9.3 (abbreviated - small fix)

---

## Root Cause (Investigation Complete)

**Problem**: "tomorrow" patterns are in `TEMPORAL_PATTERNS` (returns today's date/time) instead of `CALENDAR_QUERY_PATTERNS` (queries calendar).

**Location**: `services/intent_service/pre_classifier.py`
- Lines 104, 111, 122, 123 have "tomorrow" patterns in `TEMPORAL_PATTERNS`
- `CALENDAR_QUERY_PATTERNS` (lines 220-250) only has "today" patterns

**Infrastructure exists**: `calendar_router.get_events_in_range(start, end)` can query any date range.

---

## Approach: Pragmatic Middle Ground

Instead of adding singleton patterns for every temporal modifier, add a small `parse_relative_date()` utility that handles common cases. Not over-engineered, but extensible.

**Scope**:
- Support: "today", "tomorrow", "this week", "next week"
- Future-proof: Easy to add "next Monday", "January 20", etc.
- Defer to MUX for complex natural language parsing

---

## Implementation

### Part 1: Add temporal extraction utility

**File**: `services/intent_service/temporal_utils.py` (new)

```python
"""Temporal extraction utilities for calendar queries."""
from datetime import datetime, timedelta
from typing import Optional, Tuple

def parse_relative_date(message: str) -> Tuple[datetime, datetime, str]:
    """
    Extract date range from message with temporal modifiers.

    Returns:
        (start_date, end_date, label) - label is "today", "tomorrow", etc.
    """
    message_lower = message.lower()
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if "tomorrow" in message_lower:
        start = today_start + timedelta(days=1)
        end = start + timedelta(days=1)
        return (start, end, "tomorrow")

    if "next week" in message_lower:
        # Start from next Monday
        days_until_monday = (7 - today_start.weekday()) % 7 or 7
        start = today_start + timedelta(days=days_until_monday)
        end = start + timedelta(days=7)
        return (start, end, "next week")

    if "this week" in message_lower:
        # Monday of current week to Sunday
        start = today_start - timedelta(days=today_start.weekday())
        end = start + timedelta(days=7)
        return (start, end, "this week")

    # Default: today
    return (today_start, today_start + timedelta(days=1), "today")
```

### Part 2: Add "tomorrow" to CALENDAR_QUERY_PATTERNS

**File**: `services/intent_service/pre_classifier.py`

Add to `CALENDAR_QUERY_PATTERNS` (before line 235):
```python
# Issue #588: Tomorrow calendar queries
r"\bcalendar.*tomorrow\b",
r"\btomorrow'?s calendar\b",
r"\bmeetings.*tomorrow\b",
r"\bschedule.*tomorrow\b",
r"\btomorrow'?s schedule\b",
r"\bwhat'?s on my calendar.*tomorrow\b",
r"\bwhat'?s.*tomorrow\b",
```

### Part 3: Update calendar handler to use date range

**File**: `services/intent/intent_service.py`

In `_handle_meeting_time_query()`, use `parse_relative_date()` to determine which dates to query, then call `get_events_in_range()` instead of `get_todays_events()`.

---

## Files to Modify

| File | Change |
|------|--------|
| `services/intent_service/temporal_utils.py` | NEW - Date parsing utility |
| `services/intent_service/pre_classifier.py` | Add tomorrow patterns |
| `services/intent/intent_service.py` | Use date range in handler |

---

## Testing

- [ ] "what's on my calendar tomorrow?" → tomorrow's events
- [ ] "what's on my calendar today?" → today's events (regression)
- [ ] "meetings tomorrow" → tomorrow's events
- [ ] Response indicates correct date label

---

## Acceptance Criteria (from #588)

- [ ] "what's on my calendar tomorrow?" returns tomorrow's events
- [ ] "what is my schedule like tomorrow?" returns tomorrow's events
- [ ] "tomorrow" temporal modifier correctly parsed
- [ ] Today's calendar queries still work (regression)
- [ ] Response clearly indicates it's showing tomorrow's schedule

---

## Future Work (file as separate issue)

- [ ] Support "next Monday", "January 20", specific dates
- [ ] MUX integration will supersede pattern-based approach
- [ ] Consider `dateparser` library for robust NLP date parsing

---

## Estimate

~30-40 minutes for full implementation with tests.

---

*Gameplan created: 2026-01-14 10:20 PM*

---

## Implementation Complete

**Status**: ✅ Complete
**Commit**: Pending PM verification

### Evidence

```
$ python -m pytest tests/unit/services/intent_service/test_calendar_query_handlers.py -v
======================== 27 passed, 1 warning in 1.21s =========================
```

### Files Modified

| File | Lines Changed |
|------|---------------|
| `services/intent_service/temporal_utils.py` | +54 (new) |
| `services/intent_service/pre_classifier.py` | +16 |
| `services/intent/intent_service.py` | +18/-2 |
| `tests/unit/services/intent_service/test_calendar_query_handlers.py` | +15/-13 |

*Implementation completed: 2026-01-14 11:30 PM*

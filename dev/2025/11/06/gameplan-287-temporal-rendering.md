# Gameplan: Issue #287 - Temporal/Response Rendering Fixes

**Date**: November 6, 2025
**Issue**: #287 - CORE-ALPHA-TEMPORAL-BUGS
**Priority**: P2 - Important (UX)
**Estimated Effort**: 2 hours
**Agent**: Cursor (focused UX fixes)

---

## Context

Response rendering has three UX issues:
1. Shows "Los Angeles" instead of "PT" for timezone
2. Displays contradictory meeting status messages
3. Doesn't validate calendar data freshness

These affect user trust and clarity in time-sensitive responses.

---

## Phase -1: Investigation (20 minutes)

### Find Affected Files

```bash
# Find timezone display logic
grep -r "Los Angeles" . --include="*.py"
grep -r "America/Los_Angeles" . --include="*.py"

# Find meeting status rendering
grep -r "no meetings" . --include="*.py"
grep -r "meetings today" . --include="*.py"

# Find calendar integration points
find . -name "*calendar*.py" -type f
grep -r "get_calendar" . --include="*.py"
```

### Expected Locations
- `services/ui_messages/response_formatter.py`
- `services/integrations/calendar_service.py`
- `services/analysis/temporal_analyzer.py`

### Document Current Behavior

Take screenshots or copy example outputs showing:
- Timezone display issue
- Contradictory messages
- Stale calendar data

---

## Phase 0: Setup (10 minutes)

### Create Branch

```bash
git checkout main
git pull
git checkout -b fix/287-temporal-rendering-bugs
```

### Create Test Cases First

```python
# tests/ui_messages/test_timezone_display.py

def test_timezone_abbreviation_display():
    """Verify timezones show as abbreviations"""

    # Test data
    test_cases = [
        ("America/Los_Angeles", "PT"),
        ("America/New_York", "ET"),
        ("America/Chicago", "CT"),
        ("America/Denver", "MT"),
        ("UTC", "UTC"),
        ("Europe/London", "GMT"),
    ]

    for tz_name, expected_abbr in test_cases:
        result = format_timezone(tz_name)
        assert result == expected_abbr

def test_contradictory_messages_prevented():
    """Verify no contradictory meeting messages"""

    # Scenario: No meetings
    context = {"meetings": [], "meeting_count": 0}
    response = format_meeting_status(context)

    assert "no meetings" in response.lower()
    assert "you have meetings" not in response.lower()
    assert "meetings found" not in response.lower()
```

---

## Phase 1: Fix Timezone Display (30 minutes)

### Step 1: Create Timezone Mapping

```python
# services/ui_messages/timezone_formatter.py (new file)

TIMEZONE_ABBREVIATIONS = {
    # US Timezones
    "America/Los_Angeles": "PT",
    "America/Vancouver": "PT",
    "America/Phoenix": "MST",  # No DST
    "America/Denver": "MT",
    "America/Chicago": "CT",
    "America/New_York": "ET",

    # International
    "Europe/London": "GMT",
    "Europe/Paris": "CET",
    "Asia/Tokyo": "JST",
    "Australia/Sydney": "AEDT",

    # Special
    "UTC": "UTC",
    "GMT": "GMT",
}

def format_timezone(tz_name: str, include_offset: bool = False) -> str:
    """
    Convert timezone name to user-friendly abbreviation.

    Args:
        tz_name: Full timezone name (e.g., "America/Los_Angeles")
        include_offset: Whether to include UTC offset (e.g., "PT (UTC-8)")

    Returns:
        Abbreviated timezone (e.g., "PT")
    """
    # Get abbreviation or fallback to last part of name
    abbr = TIMEZONE_ABBREVIATIONS.get(tz_name, tz_name.split("/")[-1])

    if include_offset:
        # Add UTC offset calculation here if needed
        pass

    return abbr
```

### Step 2: Update Display Logic

Find and update all timezone display points:

```python
# Before:
response = f"Meeting at 2pm Los Angeles time"

# After:
from services.ui_messages.timezone_formatter import format_timezone

tz_abbr = format_timezone("America/Los_Angeles")
response = f"Meeting at 2pm {tz_abbr}"  # "Meeting at 2pm PT"
```

---

## Phase 2: Fix Contradictory Messages (40 minutes)

### Step 1: Identify the Bug

The issue is likely a structure like:
```python
# BUGGY CODE:
if no_meetings:
    response += "You have no meetings today."

# Later in same function (BUG!)
response += f"Found {len(meetings)} meetings."  # Shows even when 0!
```

### Step 2: Fix Logic Flow

```python
# services/ui_messages/meeting_formatter.py

def format_meeting_status(context: dict) -> str:
    """Format meeting status without contradictions."""

    meetings = context.get("meetings", [])
    meeting_count = len(meetings)

    if meeting_count == 0:
        # NO meetings path
        return "You have no meetings scheduled today."

    elif meeting_count == 1:
        # Single meeting path
        meeting = meetings[0]
        return f"You have one meeting today: {meeting.title} at {meeting.time}"

    else:
        # Multiple meetings path
        return f"You have {meeting_count} meetings today."

    # No code after if/elif/else - prevents contradictions!
```

### Step 3: Add Assertion Guards

```python
def format_meeting_response(meetings, stats):
    """Ensure no contradictory messages."""

    response_parts = []

    if not meetings:
        response_parts.append("No meetings today.")
        # GUARD: Don't add stats if no meetings
        assert stats is None or stats.get('count') == 0, \
            "Stats provided for empty meetings!"
    else:
        response_parts.append(f"{len(meetings)} meetings today.")
        # Only add stats in this branch
        if stats:
            response_parts.append(format_meeting_stats(stats))

    return " ".join(response_parts)
```

---

## Phase 3: Add Calendar Validation (30 minutes)

### Step 1: Add Freshness Check

```python
# services/integrations/calendar_validator.py

from datetime import datetime, timedelta

class CalendarDataValidator:
    """Validate calendar data freshness and reliability."""

    STALE_THRESHOLD_MINUTES = 15

    @classmethod
    def validate_calendar_data(cls, calendar_data: dict) -> dict:
        """
        Validate and annotate calendar data.

        Returns:
            dict with 'data', 'is_fresh', 'confidence', 'warnings'
        """
        result = {
            "data": calendar_data,
            "is_fresh": True,
            "confidence": "high",
            "warnings": []
        }

        # Check data age
        if "fetched_at" in calendar_data:
            fetched = datetime.fromisoformat(calendar_data["fetched_at"])
            age_minutes = (datetime.now() - fetched).seconds / 60

            if age_minutes > cls.STALE_THRESHOLD_MINUTES:
                result["is_fresh"] = False
                result["confidence"] = "low"
                result["warnings"].append(
                    f"Calendar data is {age_minutes:.0f} minutes old"
                )

        # Check for null/missing data
        if not calendar_data.get("meetings"):
            result["warnings"].append("No meeting data available")

        return result
```

### Step 2: Show Confidence in UI

```python
def format_calendar_response(calendar_data):
    """Format response with confidence indicators."""

    validation = CalendarDataValidator.validate_calendar_data(calendar_data)

    response = []

    # Add warnings if any
    if validation["warnings"]:
        response.append("⚠️ " + ", ".join(validation["warnings"]))

    # Add confidence indicator
    if validation["confidence"] == "low":
        response.append("(Calendar data may be outdated)")

    # Format meetings
    meetings = validation["data"].get("meetings", [])
    response.append(format_meetings(meetings))

    return "\n".join(response)
```

### Step 3: Add Retry Logic

```python
async def get_fresh_calendar_data(max_retries=2):
    """Get fresh calendar data with retries."""

    for attempt in range(max_retries):
        try:
            data = await fetch_calendar_data()
            validation = CalendarDataValidator.validate_calendar_data(data)

            if validation["is_fresh"]:
                return data

            # Data is stale, try refresh
            if attempt < max_retries - 1:
                await asyncio.sleep(1)  # Brief delay before retry
                continue

        except Exception as e:
            logger.warning(f"Calendar fetch attempt {attempt + 1} failed: {e}")

    # Return what we have with warnings
    return data
```

---

## Phase 4: Integration Testing (20 minutes)

### Test All Fixes Together

```python
# tests/integration/test_temporal_rendering_fixes.py

async def test_complete_temporal_fix():
    """Verify all temporal rendering fixes work together."""

    # Mock calendar with edge cases
    mock_calendar = {
        "fetched_at": datetime.now().isoformat(),
        "meetings": [],
        "timezone": "America/Los_Angeles"
    }

    response = await format_temporal_response(mock_calendar)

    # Verify timezone abbreviation
    assert "PT" in response
    assert "Los Angeles" not in response

    # Verify no contradictions
    assert response.count("no meetings") <= 1
    assert "you have meetings" not in response

    # Verify freshness indicated
    assert "⚠️" not in response  # Fresh data, no warning
```

### Manual Testing Checklist

- [ ] Check timezone displays as "PT" not "Los Angeles"
- [ ] Verify no contradictory messages with 0 meetings
- [ ] Verify no contradictory messages with multiple meetings
- [ ] Test stale data shows warning
- [ ] Test fresh data shows no warning

---

## Phase Z: Polish & PR (10 minutes)

### Final Checklist

- [ ] All timezone displays use abbreviations
- [ ] No contradictory meeting messages possible
- [ ] Calendar validation implemented
- [ ] All tests pass
- [ ] No regressions in existing functionality

### Create PR

```bash
git add -A
git commit -m "fix(#287): Fix temporal and response rendering issues

- Display timezone abbreviations (PT) instead of full names
- Prevent contradictory meeting status messages
- Add calendar data validation and freshness checks
- Show confidence indicators for stale data

Fixes #287"

git push origin fix/287-temporal-rendering-bugs
```

---

## Success Criteria

- ✅ Timezones show as abbreviations (PT, ET, etc.)
- ✅ No contradictory messages about meetings
- ✅ Calendar data freshness validated
- ✅ Users see confidence indicators
- ✅ All tests pass
- ✅ Better UX for time-sensitive information

---

## Risk Assessment

**Low-Medium Risk**
- UI changes visible to users
- Multiple touchpoints affected
- Calendar integration complexity

**Mitigation**:
- Comprehensive test coverage
- Fallback for unknown timezones
- Graceful handling of stale data
- Clear warning messages

---

*Estimated: 2 hours*
*Actual: _____ (fill in after completion)*

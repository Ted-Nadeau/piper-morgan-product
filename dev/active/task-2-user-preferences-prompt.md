# Task 2: User Preference Extension - Reminder Settings

**Agent**: Claude Code (Programmer)
**Issue**: #161 (CORE-STAND-SLACK-REMIND)
**Task**: 2 of 4 - User Preference Extension
**Sprint**: A4 "Standup Epic"
**Date**: October 20, 2025, 8:06 AM
**Estimated Effort**: 30 minutes (likely faster!)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

Extend the existing UserPreferenceManager to support reminder preferences. Add 4 new preference keys with validation, helper methods, and integration with the StandupReminderJob from Task 1.

**Scope**:
- Add 4 reminder preference keys to UserPreferenceManager
- Add validation for time format and timezone
- Create helper methods for reminder preferences
- Update StandupReminderJob to use real preferences (remove placeholders)
- Test preference storage and retrieval

**NOT in scope**:
- Message formatting (Task 3)
- API endpoints (optional - only if needed)
- Full integration testing (Task 4)

---

## Context from Task 1

**EXCELLENT PROGRESS**: Task 1 completed in 13 minutes! 🎉

**What was built**:
- ✅ StandupReminderJob (312 lines) - Using placeholder preferences
- ✅ ReminderScheduler (243 lines) - Timer loop working
- ✅ Tests passing - System functional

**What Task 2 does**:
- Replace placeholder preferences with real UserPreferenceManager integration
- Add 4 preference keys for reminder configuration
- Validation to ensure valid times and timezones

---

## Architecture Document

**YOU HAVE**: `phase-3-discovery-architecture.md` uploaded by PM

**Key sections**:
- "User Preferences System" - What exists (UserPreferenceManager)
- "Task 2: User Preference Extension" - Your specific work
- "Design Decisions" - Preference storage strategy

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Cannot find UserPreferenceManager** - Should be at `services/domain/user_preference_manager.py`
2. **UserPreferenceManager API different from discovery** - Verify set_preference/get_preference methods
3. **Need to modify core preference storage** - Should only extend, not change
4. **Time/timezone validation too complex** - Use standard library validation
5. **Cannot connect to Task 1 code** - Need to update StandupReminderJob placeholders
6. **Preference keys conflict with existing ones** - Check for naming conflicts
7. **Need database migration** - Discovery said JSON storage, no migration needed
8. **Can't provide verification evidence** - Must show preference storage working

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Preferences stored"** → Show code setting preferences
- **"Preferences retrieved"** → Show code getting preferences
- **"Validation works"** → Show invalid input rejected
- **"Integration with Task 1"** → Show StandupReminderJob using real preferences
- **"Tests pass"** → Show test output

### Working Files Location:

- ✅ dev/active/ - For test scripts, evidence
- ✅ services/domain/ - For UserPreferenceManager modifications
- ✅ services/scheduler/ - For StandupReminderJob updates

---

## Task Requirements

### 1. Review UserPreferenceManager

**FIRST**: Understand the existing preference system

```bash
# Read the UserPreferenceManager
cat services/domain/user_preference_manager.py

# Check existing preference keys
grep -n "def set_preference" services/domain/user_preference_manager.py
grep -n "def get_preference" services/domain/user_preference_manager.py

# Look for examples of preference usage
grep -r "set_preference\|get_preference" services/ --include="*.py" | head -20
```

**Understand**:
- How preferences are stored (JSON, hierarchical)
- set_preference() method signature
- get_preference() method signature
- Validation patterns used
- Scope handling (global, user, session)

---

### 2. Define Reminder Preference Keys

**Add 4 new preference keys** for reminders:

```python
# Preference keys (add to UserPreferenceManager or constants file)

STANDUP_REMINDER_ENABLED = "standup_reminder_enabled"
# Type: bool
# Default: True
# Description: Whether daily standup reminders are enabled for this user

STANDUP_REMINDER_TIME = "standup_reminder_time"
# Type: str (HH:MM format, e.g., "06:00")
# Default: "06:00"
# Description: Time of day to send reminder (24-hour format)
# Validation: Must match HH:MM format, hour 00-23, minute 00-59

STANDUP_REMINDER_TIMEZONE = "standup_reminder_timezone"
# Type: str (IANA timezone name, e.g., "America/Los_Angeles")
# Default: "America/Los_Angeles"
# Description: Timezone for reminder time
# Validation: Must be valid IANA timezone (use zoneinfo.available_timezones())

STANDUP_REMINDER_DAYS = "standup_reminder_days"
# Type: List[int] (weekday numbers: 0=Monday, 6=Sunday)
# Default: [0, 1, 2, 3, 4] (Monday-Friday)
# Description: Days of week to send reminders
# Validation: List of integers 0-6, no duplicates
```

---

### 3. Add Validation Methods

**Create validation helpers** in UserPreferenceManager:

```python
from datetime import time
from zoneinfo import ZoneInfo, available_timezones
from typing import List

def _validate_reminder_time(self, time_str: str) -> bool:
    """
    Validate reminder time format (HH:MM).

    Args:
        time_str: Time string in HH:MM format

    Returns:
        True if valid, raises ValueError if invalid

    Raises:
        ValueError: If format is invalid
    """
    try:
        # Parse HH:MM format
        parts = time_str.split(":")
        if len(parts) != 2:
            raise ValueError("Time must be in HH:MM format")

        hour = int(parts[0])
        minute = int(parts[1])

        # Validate ranges
        if hour < 0 or hour > 23:
            raise ValueError("Hour must be 0-23")
        if minute < 0 or minute > 59:
            raise ValueError("Minute must be 0-59")

        return True

    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid time format: {time_str}") from e


def _validate_timezone(self, tz_str: str) -> bool:
    """
    Validate timezone string (IANA timezone name).

    Args:
        tz_str: Timezone string (e.g., "America/Los_Angeles")

    Returns:
        True if valid, raises ValueError if invalid

    Raises:
        ValueError: If timezone is invalid
    """
    try:
        # Check if timezone is valid
        if tz_str not in available_timezones():
            raise ValueError(f"Invalid timezone: {tz_str}")

        # Try to create ZoneInfo to ensure it works
        ZoneInfo(tz_str)

        return True

    except Exception as e:
        raise ValueError(f"Invalid timezone: {tz_str}") from e


def _validate_reminder_days(self, days: List[int]) -> bool:
    """
    Validate reminder days list.

    Args:
        days: List of weekday integers (0=Monday, 6=Sunday)

    Returns:
        True if valid, raises ValueError if invalid

    Raises:
        ValueError: If days list is invalid
    """
    if not isinstance(days, list):
        raise ValueError("Reminder days must be a list")

    if not days:
        raise ValueError("Reminder days list cannot be empty")

    # Check all values are integers 0-6
    for day in days:
        if not isinstance(day, int):
            raise ValueError("Reminder days must be integers")
        if day < 0 or day > 6:
            raise ValueError("Reminder days must be 0-6 (0=Monday, 6=Sunday)")

    # Check for duplicates
    if len(days) != len(set(days)):
        raise ValueError("Reminder days list contains duplicates")

    return True
```

---

### 4. Add Helper Methods

**Create convenience methods** for reminder preferences:

```python
async def get_reminder_enabled(self, user_id: str) -> bool:
    """Get whether reminders are enabled for user."""
    return await self.get_preference(
        user_id,
        STANDUP_REMINDER_ENABLED,
        default=True
    )


async def set_reminder_enabled(self, user_id: str, enabled: bool):
    """Set whether reminders are enabled for user."""
    await self.set_preference(
        user_id,
        STANDUP_REMINDER_ENABLED,
        enabled
    )


async def get_reminder_time(self, user_id: str) -> str:
    """Get reminder time for user (HH:MM format)."""
    return await self.get_preference(
        user_id,
        STANDUP_REMINDER_TIME,
        default="06:00"
    )


async def set_reminder_time(self, user_id: str, time_str: str):
    """
    Set reminder time for user.

    Args:
        user_id: User ID
        time_str: Time in HH:MM format

    Raises:
        ValueError: If time format is invalid
    """
    # Validate time format
    self._validate_reminder_time(time_str)

    await self.set_preference(
        user_id,
        STANDUP_REMINDER_TIME,
        time_str
    )


async def get_reminder_timezone(self, user_id: str) -> str:
    """Get reminder timezone for user."""
    return await self.get_preference(
        user_id,
        STANDUP_REMINDER_TIMEZONE,
        default="America/Los_Angeles"
    )


async def set_reminder_timezone(self, user_id: str, timezone: str):
    """
    Set reminder timezone for user.

    Args:
        user_id: User ID
        timezone: IANA timezone name

    Raises:
        ValueError: If timezone is invalid
    """
    # Validate timezone
    self._validate_timezone(timezone)

    await self.set_preference(
        user_id,
        STANDUP_REMINDER_TIMEZONE,
        timezone
    )


async def get_reminder_days(self, user_id: str) -> List[int]:
    """Get reminder days for user."""
    return await self.get_preference(
        user_id,
        STANDUP_REMINDER_DAYS,
        default=[0, 1, 2, 3, 4]  # Monday-Friday
    )


async def set_reminder_days(self, user_id: str, days: List[int]):
    """
    Set reminder days for user.

    Args:
        user_id: User ID
        days: List of weekday integers (0=Monday, 6=Sunday)

    Raises:
        ValueError: If days list is invalid
    """
    # Validate days list
    self._validate_reminder_days(days)

    await self.set_preference(
        user_id,
        STANDUP_REMINDER_DAYS,
        days
    )


async def get_reminder_preferences(self, user_id: str) -> dict:
    """
    Get all reminder preferences for user.

    Returns:
        Dict with keys: enabled, time, timezone, days
    """
    return {
        "enabled": await self.get_reminder_enabled(user_id),
        "time": await self.get_reminder_time(user_id),
        "timezone": await self.get_reminder_timezone(user_id),
        "days": await self.get_reminder_days(user_id)
    }
```

---

### 5. Update StandupReminderJob

**Replace placeholder preferences** in Task 1 code:

**File**: `services/scheduler/standup_reminder_job.py`

**Find and replace the placeholder methods**:

```python
# OLD (placeholder from Task 1)
async def _get_enabled_users(self) -> List[str]:
    """Get list of user IDs with reminders enabled."""
    # TODO: Query actual UserPreferenceManager
    return []  # Placeholder


async def _should_send_reminder(self, user_id: str) -> bool:
    """Check if reminder should be sent for user based on time/timezone."""
    # TODO: Use actual user preferences
    return False  # Placeholder


# NEW (using real preferences)
async def _get_enabled_users(self) -> List[str]:
    """Get list of user IDs with reminders enabled."""
    # In production, this would query all users
    # For now, we'll need a way to get all user IDs
    # This might require a new method in UserPreferenceManager
    # or querying from a user service

    # For Task 2, document this as TODO for production
    # Test with a known user ID
    return []  # Will be populated in production


async def _should_send_reminder(self, user_id: str) -> bool:
    """Check if reminder should be sent for user based on time/timezone."""
    try:
        # Get user's reminder preferences
        prefs = await self.preference_manager.get_reminder_preferences(user_id)

        # Check if reminders are enabled
        if not prefs["enabled"]:
            return False

        # Get current time in user's timezone
        user_tz = ZoneInfo(prefs["timezone"])
        user_now = datetime.now(user_tz)

        # Parse reminder time
        reminder_time_parts = prefs["time"].split(":")
        reminder_hour = int(reminder_time_parts[0])
        reminder_minute = int(reminder_time_parts[1])

        # Check if current time matches reminder time (within same hour)
        if user_now.hour != reminder_hour:
            return False

        # Check if current minute is close to reminder minute (within 5 minutes)
        # This accounts for hourly checks that might not be exactly on the minute
        minute_diff = abs(user_now.minute - reminder_minute)
        if minute_diff > 5:
            return False

        # Check if today is a reminder day
        if user_now.weekday() not in prefs["days"]:
            return False

        return True

    except Exception as e:
        logger.error(
            "Error checking reminder time for user",
            user_id=user_id,
            error=str(e)
        )
        return False
```

---

### 6. Create Test Script

**File**: `dev/active/test_user_preferences.py`

```python
"""
Test script for reminder user preferences.

Verifies:
- Preference storage and retrieval
- Validation of time/timezone/days
- Integration with StandupReminderJob
"""

import asyncio
from services.domain.user_preference_manager import UserPreferenceManager


async def test_reminder_preferences():
    """Test reminder preference functionality."""
    print("Testing Reminder Preferences\n")

    # Create preference manager
    pref_manager = UserPreferenceManager()

    test_user_id = "test_user_123"

    # Test 1: Set and get reminder enabled
    print("Test 1: Reminder enabled")
    await pref_manager.set_reminder_enabled(test_user_id, True)
    enabled = await pref_manager.get_reminder_enabled(test_user_id)
    print(f"  ✅ Reminder enabled: {enabled}")
    assert enabled is True

    # Test 2: Set and get reminder time
    print("\nTest 2: Reminder time")
    await pref_manager.set_reminder_time(test_user_id, "08:30")
    time_str = await pref_manager.get_reminder_time(test_user_id)
    print(f"  ✅ Reminder time: {time_str}")
    assert time_str == "08:30"

    # Test 3: Validate invalid time format
    print("\nTest 3: Invalid time validation")
    try:
        await pref_manager.set_reminder_time(test_user_id, "25:00")
        print("  ❌ Should have raised ValueError")
    except ValueError as e:
        print(f"  ✅ Validation caught invalid time: {e}")

    # Test 4: Set and get timezone
    print("\nTest 4: Reminder timezone")
    await pref_manager.set_reminder_timezone(test_user_id, "America/New_York")
    tz = await pref_manager.get_reminder_timezone(test_user_id)
    print(f"  ✅ Reminder timezone: {tz}")
    assert tz == "America/New_York"

    # Test 5: Validate invalid timezone
    print("\nTest 5: Invalid timezone validation")
    try:
        await pref_manager.set_reminder_timezone(test_user_id, "Invalid/Timezone")
        print("  ❌ Should have raised ValueError")
    except ValueError as e:
        print(f"  ✅ Validation caught invalid timezone: {e}")

    # Test 6: Set and get reminder days
    print("\nTest 6: Reminder days")
    await pref_manager.set_reminder_days(test_user_id, [0, 2, 4])  # Mon, Wed, Fri
    days = await pref_manager.get_reminder_days(test_user_id)
    print(f"  ✅ Reminder days: {days}")
    assert days == [0, 2, 4]

    # Test 7: Validate invalid days
    print("\nTest 7: Invalid days validation")
    try:
        await pref_manager.set_reminder_days(test_user_id, [0, 7, 8])
        print("  ❌ Should have raised ValueError")
    except ValueError as e:
        print(f"  ✅ Validation caught invalid days: {e}")

    # Test 8: Get all reminder preferences
    print("\nTest 8: Get all preferences")
    prefs = await pref_manager.get_reminder_preferences(test_user_id)
    print(f"  ✅ All preferences: {prefs}")
    assert "enabled" in prefs
    assert "time" in prefs
    assert "timezone" in prefs
    assert "days" in prefs

    print("\n✅ All preference tests passed!")


if __name__ == "__main__":
    asyncio.run(test_reminder_preferences())
```

---

## Verification Steps

### Step 1: Verify UserPreferenceManager Extension

```bash
# Check that new methods exist
grep -n "get_reminder_enabled\|set_reminder_enabled" services/domain/user_preference_manager.py
grep -n "_validate_reminder_time" services/domain/user_preference_manager.py

# Count new lines added
wc -l services/domain/user_preference_manager.py
```

**Expected**: New methods present, ~100-150 lines added

---

### Step 2: Run Preference Tests

```bash
# Run test script
python3 dev/active/test_user_preferences.py

# Expected output:
# Testing Reminder Preferences
#
# Test 1: Reminder enabled
#   ✅ Reminder enabled: True
# ...
# ✅ All preference tests passed!
```

---

### Step 3: Verify Task 1 Integration

```bash
# Check that StandupReminderJob uses real preferences
grep -n "preference_manager.get_reminder_preferences" services/scheduler/standup_reminder_job.py

# Should see the updated _should_send_reminder method
```

---

## Success Criteria

Task 2 is complete when:

- [ ] UserPreferenceManager extended with 4 preference keys
- [ ] Validation methods implemented (_validate_reminder_time, etc.)
- [ ] Helper methods implemented (get/set for each preference)
- [ ] get_reminder_preferences() method created
- [ ] StandupReminderJob updated to use real preferences
- [ ] Test script created and passing
- [ ] All validation tests pass (invalid inputs rejected)
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Files to Modify/Create

### Modify

- `services/domain/user_preference_manager.py` - Add ~100-150 lines
- `services/scheduler/standup_reminder_job.py` - Update placeholder methods

### Create

- `dev/active/test_user_preferences.py` - Test script (~150 lines)

### Session Log

- `dev/2025/10/20/HHMM-prog-code-log.md` - Continue from Task 1

---

## Expected Timeline

**Estimated**: 30 minutes
**Likely**: 15-20 minutes (based on Task 1 speed!)

**Breakdown**:
- 5 min: Review UserPreferenceManager
- 10 min: Add validation + helper methods
- 5 min: Update StandupReminderJob
- 5 min: Create and run tests

---

## Remember

**This is simpler than Task 1**:
- UserPreferenceManager already exists
- Just adding 4 keys + validation
- Clear patterns to follow
- Straightforward integration

**Keep it simple**:
- Standard library validation (zoneinfo, datetime)
- Follow existing UserPreferenceManager patterns
- No database changes needed

---

**Ready to extend preferences!** 🎯

*Template Version: 10.0*
*Based on Task 1 success*
*Building on completed work*
*Ready for deployment*

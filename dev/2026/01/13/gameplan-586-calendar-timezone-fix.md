# Gameplan: Calendar Timezone Fix (#586)

**Issue**: #586 - Calendar integration always shows "no events" due to timezone mismatch
**Author**: Lead Developer (Claude Code)
**Date**: 2026-01-13
**Approach**: Option B - Fix calendar adapter, create follow-up for systematic audit

---

## Problem Statement

Calendar queries return "no events" because:
1. Query range uses UTC day boundaries instead of user's local timezone
2. Event status comparison mixes naive and timezone-aware datetimes
3. Uses deprecated `datetime.utcnow()`

---

## Scope

### In Scope (This Issue)
- Fix timezone handling in `services/mcp/consumer/google_calendar_adapter.py`
- Add unit tests for timezone scenarios
- Manual verification with real calendar

### Out of Scope (Follow-up Issue)
- Systematic audit of 490 datetime calls across codebase
- ADR for datetime standards
- Other integrations with potential timezone issues

---

## Implementation Plan

### Phase 1: Understand User Timezone Source

**Goal**: Determine where user timezone is configured/stored

**Tasks**:
1. Check if user timezone is stored in database (User model)
2. Check if timezone is in `PIPER.user.md` config
3. Check if timezone is in environment variables
4. Determine fallback (UTC if not configured)

**Files to Check**:
- `services/database/models.py` - User model
- `config/PIPER.user.md` - User preferences
- `services/config.py` - Config loader

### Phase 2: Fix `get_todays_events()` Query Range

**Goal**: Query correct day in user's timezone

**Location**: `services/mcp/consumer/google_calendar_adapter.py`, lines 228-236

**Current Code**:
```python
now = datetime.utcnow()  # WRONG: UTC, naive
start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
```

**Fixed Code**:
```python
from datetime import datetime, timezone, timedelta
import zoneinfo

# Get user timezone (with UTC fallback)
user_tz = zoneinfo.ZoneInfo(self._get_user_timezone() or "UTC")

# Get current time in user's timezone
now = datetime.now(user_tz)

# Get start/end of day in user's timezone
start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = start_of_day + timedelta(days=1)

# Convert to UTC for Google API (requires RFC3339 format)
time_min = start_of_day.astimezone(timezone.utc).isoformat()
time_max = end_of_day.astimezone(timezone.utc).isoformat()
```

**Dependency**: Need helper method `_get_user_timezone()` to retrieve from config/preferences.

### Phase 3: Fix `_process_event()` Status Comparison

**Goal**: Use timezone-aware comparison for event status

**Location**: `services/mcp/consumer/google_calendar_adapter.py`, lines 310-316

**Current Code**:
```python
now = datetime.now()  # WRONG: naive local time
if now < start_time:  # Comparing naive to aware!
```

**Fixed Code**:
```python
# Use UTC for comparison (both sides timezone-aware)
now = datetime.now(timezone.utc)
if now < start_time:  # Both are timezone-aware
```

### Phase 4: Add Unit Tests

**Goal**: Verify timezone handling works correctly

**Test File**: `tests/unit/services/mcp/consumer/test_google_calendar_adapter.py`

**Test Cases**:
1. User in Pacific Time, events exist today → returns events
2. User in UTC, events exist today → returns events
3. Event spanning timezone boundary → correct status
4. All-day event handling
5. No user timezone configured → falls back to UTC

### Phase 5: Manual Verification

**Goal**: Confirm fix works with real calendar

**Steps**:
1. Ensure calendar is connected (OAuth valid)
2. Have at least one event today
3. Ask "What's on my calendar today?"
4. Verify events appear
5. Check event status (upcoming/current/completed) is correct

---

## Completion Matrix

| Task | Status | Evidence Required |
|------|--------|------------------|
| Phase 1: Understand timezone source | ⬜ | Document where tz comes from |
| Phase 2: Fix query range | ⬜ | Code change + test |
| Phase 3: Fix status comparison | ⬜ | Code change + test |
| Phase 4: Add unit tests | ⬜ | Test file + all passing |
| Phase 5: Manual verification | ⬜ | Screenshot or terminal output |
| Create follow-up issue for systematic audit | ⬜ | Issue number |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| User timezone not available | Medium | High | Use UTC fallback, add warning |
| Google API format mismatch | Low | High | Test with real API |
| Test coverage gaps | Medium | Medium | Multiple timezone scenarios |
| Regression in other calendar features | Low | Medium | Run existing calendar tests |

---

## Dependencies

- `zoneinfo` module (Python 3.9+ standard library)
- User timezone configuration (may need to add if missing)

---

## Follow-up Work

**Create Issue**: "TECH-DEBT: Systematic datetime audit (490 inconsistent datetime calls)"
- Reference this fix as exemplar
- Catalog all `datetime.utcnow()` and `datetime.now()` usage
- Propose ADR for datetime standards
- Phase remediation by component priority

---

## Definition of Done

- [ ] Calendar returns events when events exist
- [ ] Events show correct status (upcoming/current/completed)
- [ ] Works for users in non-UTC timezones
- [ ] Unit tests pass
- [ ] No regressions in existing calendar tests
- [ ] Follow-up issue created for systematic audit
- [ ] Issue #586 closed with evidence

---

_Gameplan created: 2026-01-13_
_Audited: 2026-01-13_

---

## Audit Findings

**Audit Date**: 2026-01-13
**Auditor**: Claude Code (Lead Developer)
**Status**: REVISED PLAN REQUIRED

### Finding 1: Phase 1 Already Solved ✅

User timezone **already exists** in the codebase:

```python
# services/domain/user_preference_manager.py:590-593
async def get_reminder_timezone(self, user_id: UUID) -> str:
    """Get reminder timezone for user."""
    return await self.get_preference(
        STANDUP_REMINDER_TIMEZONE, user_id=user_id, default="America/Los_Angeles"
    )
```

**Correction**: Phase 1 becomes "Verify integration" rather than "Understand source"
**Default is `America/Los_Angeles`**, not UTC as gameplan assumed.

### Finding 2: Architecture Gap - User Context Not Threaded ⚠️

The gameplan assumes `self._get_user_timezone()` can be called from the adapter, but:

1. **Calendar handlers don't receive user_id**:
   ```python
   # services/intent/intent_service.py:1025
   return await self._handle_meeting_time_query(intent, workflow.id)
   # ❌ No user_id passed!
   ```

2. **CalendarIntegrationRouter created without context**:
   ```python
   # services/intent/intent_service.py:2436
   calendar_router = CalendarIntegrationRouter()
   # ❌ No user context!
   ```

3. **GoogleCalendarMCPAdapter.get_todays_events() has no user parameter**:
   ```python
   # services/mcp/consumer/google_calendar_adapter.py:216
   async def get_todays_events(self) -> List[Dict[str, Any]]:
   # ❌ No user_id to lookup timezone!
   ```

**Correction**: Phase 2 scope expanded - must thread user context through:
- `IntentService._handle_*_query()` methods
- `CalendarIntegrationRouter` constructor and methods
- `GoogleCalendarMCPAdapter.get_todays_events()`

### Finding 3: Code Snippets Assume Non-Existent Method ⚠️

Gameplan assumes `self._get_user_timezone()` exists in the adapter. It doesn't.

**Correction**: Must create helper that:
1. Accepts `user_id` parameter
2. Uses `UserPreferenceManager.get_reminder_timezone(user_id)`
3. Has fallback for when user_id is None (use UTC or system default)

### Finding 4: Two Fix Approaches Available

**Option A (Simple but Limited)**:
- Use hardcoded timezone (e.g., from environment variable)
- Quick fix, but not multi-user ready
- Appropriate if only one user (alpha testing)

**Option B (Proper but More Work)**:
- Thread user_id through call chain
- Use existing UserPreferenceManager
- Multi-user ready, correct architecture

**Recommendation**: Given this is alpha testing with one user, **Option A for immediate fix**, with documented tech debt for Option B.

---

## Revised Implementation Plan

### Phase 1: Verify Existing Timezone Infrastructure (Simplified)
- ✅ Confirm `UserPreferenceManager.get_reminder_timezone()` works
- Decide: Hardcoded timezone vs threading user context

### Phase 2a: Quick Fix (Option A - Alpha Only)
Add environment variable or config fallback:
```python
# In get_todays_events()
user_tz_str = os.environ.get("PIPER_USER_TIMEZONE", "America/Los_Angeles")
user_tz = zoneinfo.ZoneInfo(user_tz_str)
```

### Phase 2b: Proper Fix (Option B - Future)
Thread user context through:
1. Add `user_id` parameter to `_handle_*_calendar_query()` methods
2. Pass to `CalendarIntegrationRouter(user_id=user_id)`
3. Pass to `GoogleCalendarMCPAdapter.get_todays_events(user_id)`
4. Lookup via `UserPreferenceManager`

### Phase 3: Fix Status Comparison (Unchanged)
```python
now = datetime.now(timezone.utc)  # Timezone-aware UTC
```

### Phase 4: Unit Tests (Adjusted)
- Mock timezone configuration
- Test with various timezone offsets
- Test fallback behavior

### Phase 5: Manual Verification (Unchanged)

---

## Revised Completion Matrix

| Task | Status | Evidence Required |
|------|--------|------------------|
| Phase 1: Verify timezone infrastructure | ⬜ | Confirm method exists |
| Phase 2a: Quick fix with config timezone | ⬜ | Code change + test |
| Phase 3: Fix status comparison | ⬜ | Code change + test |
| Phase 4: Add unit tests | ⬜ | Test file + all passing |
| Phase 5: Manual verification | ⬜ | Terminal output |
| Create follow-up for user context threading | ⬜ | Issue number |
| Create follow-up for systematic datetime audit | ⬜ | Issue number |

---

## PM Decision Required

Before proceeding, need decision on:

1. **Option A (Quick Fix)**: Use environment variable `PIPER_USER_TIMEZONE`
   - Pros: Fast, minimal changes
   - Cons: Not multi-user ready

2. **Option B (Proper Fix)**: Thread user_id through call chain
   - Pros: Correct architecture, multi-user ready
   - Cons: More files changed, higher risk

**Recommendation**: Option A for alpha, Option B as follow-up issue.

---

_Audit complete: Ready for PM review_

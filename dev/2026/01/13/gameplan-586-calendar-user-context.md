# Gameplan: Calendar Timezone-Aware Queries with User Context (#586)

**Issue**: #586 - Calendar timezone-aware queries with user context
**Author**: Lead Developer (Claude Code)
**Date**: 2026-01-13
**Type**: Feature (Architecture Change)
**Approach**: Option B - Thread user context through call chain

---

## Problem Statement

Calendar queries return "no events" because:
1. Query range uses UTC day boundaries instead of user's local timezone
2. User context (user_id) is not threaded to calendar layer
3. `UserPreferenceManager.get_reminder_timezone()` exists but can't be called

This requires architectural changes to thread user identity through the calendar call chain.

---

## Architecture Overview

### Current State (Broken)
```
process_intent(message, session_id, user_id, ctx)
    └── _handle_query_intent(intent, workflow, session_id)  # user_id lost!
        └── _handle_meeting_time_query(intent, workflow_id)  # no user context
            └── CalendarIntegrationRouter()  # stateless
                └── get_todays_events()  # UTC hardcoded
```

### Target State (Fixed)
```
process_intent(message, session_id, user_id, ctx)
    └── _handle_query_intent(intent, workflow, session_id, user_id)
        └── _handle_meeting_time_query(intent, workflow_id, user_id)
            └── CalendarIntegrationRouter(user_id)
                └── get_todays_events(user_id)
                    └── _get_user_timezone(user_id)  # UserPreferenceManager
```

---

## Implementation Phases

### Phase 1: Thread user_id to calendar intent handlers

**Goal**: Pass user_id from `_handle_query_intent()` to calendar handler methods

**Files**: `services/intent/intent_service.py`

**Changes**:
1. Update `_handle_query_intent()` signature to accept `user_id` parameter
2. Update `_handle_meeting_time_query()` signature: add `user_id: Optional[str] = None`
3. Update `_handle_recurring_meetings_query()` signature: add `user_id: Optional[str] = None`
4. Update `_handle_week_calendar_query()` signature: add `user_id: Optional[str] = None`
5. Pass user_id at call sites in `_handle_query_intent()`

**Evidence Required**:
- [ ] All 3 calendar handler methods have user_id parameter
- [ ] `_handle_query_intent()` passes user_id to calendar handlers
- [ ] Grep shows no calendar handler calls without user_id

### Phase 2: Update CalendarIntegrationRouter

**Goal**: Accept and propagate user context through router

**Files**: `services/integrations/calendar/calendar_integration_router.py`

**Changes**:
1. Add `user_id: Optional[str] = None` to `__init__()`
2. Store as `self._user_id`
3. Add `user_id: Optional[str] = None` to `get_todays_events()`
4. Pass user_id to underlying `GoogleCalendarMCPAdapter.get_todays_events()`

**Evidence Required**:
- [ ] Router constructor accepts user_id
- [ ] `get_todays_events()` accepts and passes user_id
- [ ] No hardcoded timezone in router

### Phase 3: Fix GoogleCalendarMCPAdapter timezone handling

**Goal**: Use user's timezone for query range and event status

**Files**: `services/mcp/consumer/google_calendar_adapter.py`

**Changes**:
1. Add `user_id: Optional[str] = None` to `get_todays_events()` signature
2. Create `async def _get_user_timezone(self, user_id: Optional[str]) -> str` helper:
   - If user_id provided: use `UserPreferenceManager.get_reminder_timezone(user_id)`
   - Fallback: `"America/Los_Angeles"` (matches existing default)
3. Update `_get_events()` inner function:
   - Replace `datetime.utcnow()` with timezone-aware datetime
   - Use `zoneinfo.ZoneInfo(user_timezone)` for day boundaries
   - Convert to UTC for Google API
4. Fix `_process_event()`:
   - Replace `datetime.now()` with `datetime.now(timezone.utc)`
   - Ensure both sides of comparison are timezone-aware

**Evidence Required**:
- [ ] `_get_user_timezone()` helper exists and uses UserPreferenceManager
- [ ] `get_todays_events()` uses user's timezone for query range
- [ ] `_process_event()` uses timezone-aware comparison
- [ ] No `datetime.utcnow()` or naive `datetime.now()` in adapter

### Phase 4: Unit tests

**Goal**: Verify timezone handling with comprehensive tests

**Files**: `tests/unit/services/mcp/consumer/test_google_calendar_adapter.py`

**Test Cases**:
1. `test_get_todays_events_pacific_timezone` - User in PT, events exist → returns events
2. `test_get_todays_events_utc_timezone` - User in UTC, events exist → returns events
3. `test_get_todays_events_timezone_boundary` - Event near midnight → correct day
4. `test_get_todays_events_no_user_id_fallback` - No user_id → uses default timezone
5. `test_process_event_status_timezone_aware` - Status comparison is timezone-aware
6. `test_get_user_timezone_from_preferences` - Preference lookup works

**Evidence Required**:
- [ ] All 6 test cases exist
- [ ] All tests pass
- [ ] Tests mock UserPreferenceManager correctly

### Phase 5: Manual verification

**Goal**: Confirm fix works with real calendar

**Steps**:
1. Ensure calendar OAuth is valid
2. Have at least one event today
3. Ask "What's on my calendar today?"
4. Verify events appear with correct details
5. Verify event status (upcoming/current/completed) matches reality

**Evidence Required**:
- [ ] Terminal output showing events returned
- [ ] Event count matches actual calendar

---

## Subagent Deployment Strategy

This feature warrants adversarial rigor with multiple subagents:

### Subagent 1: Implementation Agent
**Task**: Implement Phases 1-3 (code changes)
**Scope**:
- `services/intent/intent_service.py`
- `services/integrations/calendar/calendar_integration_router.py`
- `services/mcp/consumer/google_calendar_adapter.py`

### Subagent 2: Test Agent
**Task**: Implement Phase 4 (tests)
**Scope**:
- `tests/unit/services/mcp/consumer/test_google_calendar_adapter.py`
- Run tests, verify coverage

### Subagent 3: Verification Agent
**Task**: Audit implementation for correctness
**Scope**:
- Review all changes for timezone correctness
- Check for edge cases (DST transitions, timezone boundary)
- Verify no regression in existing calendar functionality
- Run full test suite

### Coordination
- Subagent 1 completes first
- Subagent 2 can work in parallel on test structure
- Subagent 3 runs after both complete
- Lead reviews all evidence before closing issue

---

## Completion Matrix

| Phase | Task | Status | Evidence |
|-------|------|--------|----------|
| 1 | Thread user_id to `_handle_query_intent()` | ✅ | Line 984, 540 |
| 1 | Add user_id to `_handle_meeting_time_query()` | ✅ | Line 2415 |
| 1 | Add user_id to `_handle_recurring_meetings_query()` | ✅ | Line 2530 |
| 1 | Add user_id to `_handle_week_calendar_query()` | ✅ | Line 2627 |
| 2 | CalendarIntegrationRouter accepts user_id | ✅ | Line 44 |
| 2 | Router passes user_id to adapter | ✅ | Line 142 |
| 3 | Create `_get_user_timezone()` helper | ✅ | Line 216 |
| 3 | Fix `get_todays_events()` query range | ✅ | Line 240 |
| 3 | Fix `_process_event()` comparison | ✅ | Line 357 |
| 3 | Remove deprecated datetime calls | ✅ | Verified via grep |
| 4 | Test: Pacific timezone | ✅ | 15 tests passing |
| 4 | Test: UTC timezone | ✅ | 15 tests passing |
| 4 | Test: Timezone boundary | ✅ | 15 tests passing |
| 4 | Test: No user_id fallback | ✅ | 15 tests passing |
| 4 | Test: Status timezone-aware | ✅ | 15 tests passing |
| 4 | Test: Preference lookup | ✅ | 15 tests passing |
| 5 | Manual verification | ⏳ | Pending PM test |
| - | Full test suite passes | ✅ | 1720 passed |
| - | Create datetime audit follow-up issue | ⬜ | Issue number |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing calendar functionality | Medium | High | Run all calendar tests before/after |
| Other callers of handlers broken | Medium | Medium | Grep for all call sites |
| UserPreferenceManager async issues | Low | Medium | Match existing patterns |
| DST edge cases | Low | Low | Use proper timezone library |

---

## Dependencies

- `zoneinfo` module (Python 3.9+ stdlib) - already available
- `UserPreferenceManager` - already exists at `services/domain/user_preference_manager.py`
- User timezone preferences - already populated (standup reminders use them)

---

## Definition of Done

- [ ] User context flows from intent handler to calendar adapter
- [ ] Calendar queries use user's configured timezone
- [ ] Event status uses timezone-aware comparison
- [ ] All new unit tests pass
- [ ] Full test suite passes (1705+ tests)
- [ ] Manual verification shows events correctly
- [ ] Follow-up issue created for systematic datetime audit
- [ ] Issue #586 closed with evidence

---

## Follow-up Issues Required

1. **TECH-DEBT: Systematic datetime audit** - 490 datetime calls with inconsistent handling
2. **ADR-055: Datetime Standards** - Codify timezone handling patterns

---

_Gameplan created: 2026-01-13_
_Type: Feature with subagent deployment_
_Audited: 2026-01-13_

---

## Audit Findings

**Audit Date**: 2026-01-13
**Auditor**: Claude Code (Lead Developer)
**Status**: ✅ GAMEPLAN VERIFIED WITH EXPANDED SCOPE

### Finding 1: user_id Available in Calling Context ✅

Confirmed `user_id` is available in `_process_intent_internal()` but not passed to `_handle_query_intent()`:

```python
# Line 539: user_id available but not passed
result = await self._handle_query_intent(intent, workflow, session_id)
# Should be:
result = await self._handle_query_intent(intent, workflow, session_id, user_id)
```

The pattern already exists at line 508 where canonical handlers receive user_id:
```python
canonical_result = await self.canonical_handlers.handle(intent, session_id, user_id)
```

### Finding 2: More Call Sites Than Expected ⚠️

Grep found **12 call sites** for `CalendarIntegrationRouter()`:

| File | Line | Context |
|------|------|---------|
| `services/intent/intent_service.py` | 2436, 2549, 2644, 3240 | Calendar handlers |
| `services/conversation/conversation_handler.py` | 119 | Greeting calendar |
| `services/intent_service/canonical_handlers.py` | 723, 1687 | Temporal handlers |
| `services/features/morning_standup.py` | 425, 568 | Standup feature |
| `services/integrations/calendar/calendar_plugin.py` | 29 | Plugin constructor |
| `services/integrations/calendar/calendar_integration_router.py` | 31, 452 | Examples/factory |

**Scope Decision**: Phase 1-3 focus on intent_service.py call sites (the direct calendar query handlers). Other call sites use `get_temporal_summary()` which calls `get_todays_events()` internally, so they'll benefit from the adapter fix automatically.

### Finding 3: RouterFactory May Need Update

Line 452 shows a factory function:
```python
return CalendarIntegrationRouter()
```

If other code uses this factory, we need to determine if it should accept user context.

### Finding 4: Architecture Validated ✅

The proposed architecture is correct:
1. `user_id` exists in `_process_intent_internal`
2. Just needs threading through `_handle_query_intent` → handlers → router → adapter
3. `UserPreferenceManager.get_reminder_timezone(user_id)` is the right source

### Scope Clarification

**Primary Scope (This Issue)**:
- Fix 4 call sites in `intent_service.py` (calendar query handlers)
- Update `CalendarIntegrationRouter` to accept optional `user_id`
- Fix `GoogleCalendarMCPAdapter.get_todays_events()` timezone handling

**Secondary Benefit** (automatic):
- All other call sites (standup, conversation, canonical) will work correctly
- They use `get_temporal_summary()` which internally calls `get_todays_events()`

**Out of Scope** (future):
- Threading user_id through standup/conversation handlers
- Other integrations with timezone issues
- Systematic datetime audit

---

_Audit complete: Gameplan verified, scope confirmed_
_Ready for execution with subagents_

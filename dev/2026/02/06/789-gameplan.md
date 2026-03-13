# Gameplan: #789 - Calendar False Positive Fix

**Issue**: BUG: Piper claims 'no meetings' without calendar connected
**Date**: 2026-02-06
**Author**: Lead Developer (Claude Code Opus)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Database: PostgreSQL (port 5433)
- [x] Testing framework: pytest
- [x] Calendar integration: `services/mcp/consumer/google_calendar_adapter.py`
- [x] Greeting handler: `services/intent/intent_service.py` or `canonical_handlers.py`

**My understanding of the task**:
- I need to: Distinguish "no calendar connected" from "calendar connected with no events"
- This involves: Adding `calendar_connected` field to temporal summary response
- Current state: Both scenarios return empty list, treated identically as "no meetings"

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits

**Assessment**: ☐ **SKIP WORKTREE** - Single agent, ~30 min fix, 2-3 files

### Part B: PM Verification Required

**PM, please confirm**:
1. Files to modify are correct?
2. Any other places that check calendar connection status?
3. Should we suggest connecting calendar when not connected?

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - PM confirmed
- [ ] **REVISE** - Needs different approach
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending

### GitHub Issue Verification

Already verified - #789 audited and enriched.

### Codebase Investigation

```bash
# Find calendar temporal summary
grep -rn "get_temporal_summary\|temporal_summary" services/

# Find where greeting mentions calendar
grep -rn "calendar\|meetings\|clear day" services/intent/

# Check GoogleCalendarMCPAdapter
grep -n "authenticate\|get_todays_events" services/mcp/consumer/google_calendar_adapter.py
```

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - This is a backend-only change. No API contract changes.

---

## Phase 0.6: Data Flow & Integration Verification

### Data Flow

| Layer | Component | Current Behavior | Needed Change |
|-------|-----------|------------------|---------------|
| Adapter | `GoogleCalendarMCPAdapter.get_todays_events()` | Returns `[]` on auth failure | Return `{"connected": false}` or raise |
| Router | `CalendarIntegrationRouter.get_temporal_summary()` | Passes through empty list | Add `calendar_connected` field |
| Handler | Greeting/check-in handler | Interprets `[]` as "no meetings" | Check `calendar_connected` first |

### Integration Points

| Caller | Callee | Verified? |
|--------|--------|-----------|
| intent_service | CalendarIntegrationRouter | [ ] |
| CalendarIntegrationRouter | GoogleCalendarMCPAdapter | [ ] |

---

## Phase 0.7: Conversation Design

**N/A** - This is not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

None - this is a bug fix, not a state change.

### Downstream Behavior Changes

| Feature | Before Fix | After Fix |
|---------|------------|-----------|
| Greeting (no calendar) | "No meetings - great day!" | No calendar mention OR "Connect calendar for..." |
| Greeting (calendar, no events) | "No meetings - great day!" | "No meetings - great day!" (unchanged) |
| Greeting (calendar, has events) | Shows events | Shows events (unchanged) |

---

## Phase 1: Implementation

### Step 1.1: Modify GoogleCalendarMCPAdapter

**File**: `services/mcp/consumer/google_calendar_adapter.py`

Add authentication state to response or use sentinel value:

```python
# Option A: Return dict with connected state
async def get_todays_events(self) -> dict:
    if not await self.authenticate():
        return {"connected": False, "events": []}
    # ... existing logic
    return {"connected": True, "events": events}

# Option B: Raise specific exception (less preferred)
```

### Step 1.2: Update CalendarIntegrationRouter

**File**: `services/integrations/calendar_integration_router.py` (or similar)

Propagate `connected` state in temporal summary:

```python
async def get_temporal_summary(self) -> dict:
    result = await self.adapter.get_todays_events()
    if not result.get("connected", True):
        return {
            "success": True,
            "calendar_connected": False,
            "timestamp": datetime.now().isoformat()
        }
    # ... existing logic with calendar_connected: True
```

### Step 1.3: Update Greeting Handler

**File**: `services/intent/intent_service.py` or greeting handler

Check connection before mentioning calendar:

```python
temporal_summary = await calendar_router.get_temporal_summary()

if not temporal_summary.get("calendar_connected", True):
    # Don't mention calendar, or suggest connecting
    pass
elif temporal_summary.get("stats", {}).get("total_meetings_today", 0) == 0:
    message += " (No meetings - great day for deep work!)"
else:
    # Show meeting info
```

---

## Phase 2: Testing

### Unit Tests

- [ ] `test_adapter_returns_connected_false_when_no_credentials`
- [ ] `test_adapter_returns_connected_true_when_authenticated`
- [ ] `test_router_propagates_connected_state`
- [ ] `test_greeting_skips_calendar_when_not_connected`

### Integration Test

- [ ] Full flow: unauthenticated user → greeting → no calendar mention

---

## Phase Z: Final Bookending

### Acceptance Criteria

- [ ] User without calendar: greeting does NOT mention calendar or meetings
- [ ] User with calendar, no events: greeting says "No meetings"
- [ ] User with calendar, has events: greeting shows events
- [ ] No regressions in existing calendar functionality
- [ ] Tests passing

### Evidence Required

- Terminal output showing greeting without calendar mention
- Test output showing all scenarios pass

---

## Estimate

| Phase | Time |
|-------|------|
| Investigation | 10 min |
| Implementation | 20 min |
| Testing | 15 min |
| **Total** | **~45 min** |

---

## STOP Conditions

Stop immediately and escalate if:
- `GoogleCalendarMCPAdapter` doesn't have `authenticate()` method
- Calendar is checked in more than 3 places (scope creep)
- Router doesn't exist or has different interface than expected
- Changes break existing calendar tests

---

## Risk Assessment

**Low risk**:
- Isolated change to calendar integration
- Clear fix approach
- No database changes
- No API contract changes

**Potential issues**:
- May need to find all places that check calendar data
- May need to update multiple handlers if calendar is checked in multiple places

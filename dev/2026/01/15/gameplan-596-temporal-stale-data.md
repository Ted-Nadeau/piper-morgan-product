# Gameplan: Issue #596 - TEMPORAL Handler Stale Calendar Data

**Issue**: [#596](https://github.com/mediajunkie/piper-morgan-product/issues/596)
**Type**: Bug Fix (P2)
**Template Version**: v9.3

---

## Phase -1: Pre-Implementation Verification

### Infrastructure Check
- [ ] Verify `canonical_handlers.py` exists at expected location
- [ ] Verify `get_temporal_summary()` method exists in CalendarIntegrationRouter
- [ ] Verify `get_todays_events()` exists in GoogleCalendarMCPAdapter
- [ ] Confirm #588 timezone fix is in `get_events_in_range()` (compare code paths)

### STOP Conditions
- Infrastructure doesn't match assumptions → STOP, report
- `get_todays_events()` already has timezone fix → investigate other root cause
- Method signatures changed → update gameplan

---

## Root Cause Analysis

**Problem**: TEMPORAL handler shows "No meetings" when user has 6 meetings.

**Hypothesis**: Two potential issues:

1. **Missing user_id propagation**: `CalendarIntegrationRouter()` created without user_id
2. **Timezone bug in get_todays_events()**: Same issue we fixed in `get_events_in_range()` - naive datetime treated as UTC instead of local

**Code Path Comparison**:

| Handler | Method Chain | Timezone Handling |
|---------|--------------|-------------------|
| QUERY (meeting_time) | `get_events_in_range()` | ✅ Fixed in #588 - local→UTC conversion |
| TEMPORAL | `get_temporal_summary()` → `get_todays_events()` | ❓ May have same bug |

---

## Phase 0.6: Data Flow & Integration

### User Context Propagation (Current vs Required)

| Layer | Component | user_id Source | Current Status |
|-------|-----------|----------------|----------------|
| Route | `intent.py` | `request.state.user` | ✅ Available |
| Service | `IntentService._handle_temporal_intent()` | `context.get("user_id")` | ✅ Available |
| Handler | `canonical_handlers.py` TEMPORAL | Should receive from service | ❓ Verify |
| Router | `CalendarIntegrationRouter.get_temporal_summary()` | Method param | ❌ Missing param |
| Adapter | `GoogleCalendarMCPAdapter.get_temporal_summary()` | Method param | ❌ Missing param |
| Adapter | `GoogleCalendarMCPAdapter.get_todays_events()` | Method param | ✅ Has param |

### Data Flow Diagram

```
User Request ("How about today?")
    │
    ▼
[intent.py route] ────────────────────────────► user_id from request.state
    │
    ▼
[IntentService._handle_temporal_intent()] ────► user_id in context dict
    │
    ▼
[canonical_handlers.TEMPORAL] ────────────────► ❓ Extract user_id from context
    │
    ▼
[CalendarIntegrationRouter.get_temporal_summary()] ──► ❌ MISSING: user_id param
    │
    ▼
[GoogleCalendarMCPAdapter.get_temporal_summary()] ──► ❌ MISSING: user_id param
    │
    ▼
[GoogleCalendarMCPAdapter.get_todays_events(user_id)] ──► ✅ HAS param, never receives it
    │
    ▼
[Google Calendar API] ────────────────────────► Needs user OAuth tokens
```

### Integration Points Checklist

- [ ] Verify `_handle_temporal_intent()` passes user_id to handler context
- [ ] Verify canonical handler can extract user_id from context dict
- [ ] Add user_id param to `CalendarIntegrationRouter.get_temporal_summary()`
- [ ] Add user_id param to `GoogleCalendarMCPAdapter.get_temporal_summary()`
- [ ] Propagate user_id to existing `get_todays_events(user_id)` call

### Pattern Adaptation (from #588)

The #588 fix for QUERY handler followed same pattern:
1. QUERY handler extracts user_id from `context.get("user_id")`
2. Passes to `CalendarIntegrationRouter` method
3. Router passes to adapter method
4. Adapter uses for OAuth token lookup

**Reuse pattern**: Copy user_id extraction from `_handle_meeting_time_query()` to TEMPORAL handler.

---

## Implementation

### Part 1: Verify get_todays_events() timezone handling

**File**: `services/mcp/consumer/google_calendar_adapter.py`

Check if `get_todays_events()` has the same timezone issue we fixed in `get_events_in_range()`.

From #588 investigation, `get_todays_events()` (lines 240-300) already has timezone handling via:
- `user_timezone = await self._get_user_timezone(user_id)`
- `ZoneInfo(user_timezone)` for local time calculation

**But**: `get_temporal_summary()` calls `get_todays_events()` WITHOUT passing user_id:
```python
all_events = await self.get_todays_events()  # No user_id!
```

### Part 2: Fix get_temporal_summary() to pass user_id

**File**: `services/mcp/consumer/google_calendar_adapter.py`

Update `get_temporal_summary()` to accept and propagate user_id:

```python
async def get_temporal_summary(self, user_id: Optional[str] = None) -> Dict[str, Any]:
    # ... existing code ...
    all_events = await self.get_todays_events(user_id=user_id)
```

### Part 3: Update CalendarIntegrationRouter.get_temporal_summary()

**File**: `services/integrations/calendar/calendar_integration_router.py`

Update router to accept and propagate user_id:

```python
async def get_temporal_summary(self, user_id: Optional[str] = None) -> Dict[str, Any]:
    integration, is_legacy = self._get_preferred_integration("get_temporal_summary")
    # ... existing code ...
    return await integration.get_temporal_summary(user_id=user_id)
```

### Part 4: Update TEMPORAL handler to pass user_id

**File**: `services/intent_service/canonical_handlers.py`

Update the TEMPORAL handler to pass user_id when creating router:

```python
calendar_adapter = CalendarIntegrationRouter(user_id=user_id)
temporal_summary = await calendar_adapter.get_temporal_summary(user_id=user_id)
```

**Note**: Need to verify how user_id is available in the handler context.

---

## Files to Modify

| File | Change |
|------|--------|
| `services/mcp/consumer/google_calendar_adapter.py` | Add user_id param to get_temporal_summary() |
| `services/integrations/calendar/calendar_integration_router.py` | Propagate user_id through router |
| `services/intent_service/canonical_handlers.py` | Pass user_id to calendar calls |

---

## Testing

### Unit Tests
- [ ] Existing calendar tests still pass
- [ ] TEMPORAL handler returns correct meeting count

### Manual Testing
- [ ] "How about today?" (TEMPORAL) shows same meeting count as "What's on my calendar?" (QUERY)
- [ ] "No meetings" message only appears when truly no meetings

---

## Acceptance Criteria (from #596)

- [ ] TEMPORAL handler shows correct meeting count for today
- [ ] "No meetings - great day for deep work!" only appears when user truly has no meetings
- [ ] Calendar data in TEMPORAL response matches calendar QUERY response
- [ ] Today's calendar queries still work (regression check)

---

## Routing Integration Test

Per Pattern #521 learning, verify full routing path:

```python
# TEMPORAL phrases should show calendar data
test_phrases = ["what time is it", "what day is it", "How about today?"]
# Verify calendar data is populated in response
```

---

## Estimate

~20-30 minutes - straightforward parameter propagation fix.

---

*Gameplan created: 2026-01-15 10:18 AM*

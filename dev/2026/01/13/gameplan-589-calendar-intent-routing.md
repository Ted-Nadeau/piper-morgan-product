# Gameplan: Calendar Intent Routing Fix (#589)

**Issue**: #589 - Intent classifier routes calendar queries to TEMPORAL instead of QUERY
**Author**: Lead Developer (Claude Code)
**Date**: 2026-01-13
**Type**: Bug Fix (Intent Classification)
**Blocks**: #586 user verification

---

## Phase -1: Infrastructure Verification (MANDATORY)

### Part A: Current Understanding

Based on investigation, I believe:

**Infrastructure Status**:
- [x] File exists: `services/queries/query_router.py`
- [x] Method exists: `_rule_based_classification()` at line 319
- [x] Temporal patterns at: lines 354-375
- [x] IntentCategory enum available from `services/shared_types.py`
- [x] QUERY handlers exist in `services/intent/intent_service.py`

**My understanding of the task**:
- Add calendar patterns to rule-based classifier
- Patterns must be checked BEFORE temporal patterns
- Return Intent with category=QUERY, action="meeting_time"

### Part B: Verification Commands

```bash
# Verify file exists
ls -la services/queries/query_router.py

# Verify method exists at expected location
grep -n "_rule_based_classification" services/queries/query_router.py

# Verify temporal patterns location
grep -n "what day is it" services/queries/query_router.py

# Verify QUERY action exists
grep -n "meeting_time" services/intent/intent_service.py | head -5
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Infrastructure verified via earlier investigation
- [ ] **REVISE** - N/A
- [ ] **CLARIFY** - N/A

---

## Problem Statement

Calendar queries like "What's on my calendar today?" return "no meetings" despite:
1. Calendar OAuth working
2. Calendar adapter returning 7 real events (verified via direct test)
3. Timezone fix (#586) implemented and working

**Root Cause**: The intent classifier routes calendar queries to `TEMPORAL` category, which invokes `CanonicalHandlers.handle_temporal()` instead of `IntentService._handle_meeting_time_query()`.

---

## Architecture Analysis

### Current Flow (Broken)
```
User: "What's on my calendar today?"
    │
    ├── Pre-classifier checks rule-based patterns (query_router.py:354-375)
    │   └── Doesn't match "what day/time is it" → falls through
    │
    ├── LLM Classifier OR Fallback
    │   └── Classifies as TEMPORAL (why? unclear)
    │
    └── IntentService._process_intent_internal (line 506)
        └── canonical_handlers.can_handle() → True (TEMPORAL is canonical)
            └── canonical_handlers.handle_temporal() (line 678)
                └── CalendarIntegrationRouter() # NO user_id!
                    └── get_temporal_summary() # Different method!
                        └── Returns "No meetings" (doesn't use fixed adapter)
```

### Target Flow (Fixed)
```
User: "What's on my calendar today?"
    │
    ├── Pre-classifier checks rule-based patterns
    │   └── NEW: Matches calendar pattern → QUERY/meeting_time
    │
    └── IntentService._process_intent_internal (line 539)
        └── intent.category == "QUERY"
            └── _handle_query_intent() (line 540)
                └── _handle_meeting_time_query(user_id) (line 1028)
                    └── CalendarIntegrationRouter(user_id=user_id)
                        └── get_todays_events() # Fixed method!
                            └── Returns actual events ✓
```

---

## Root Cause Deep Dive

### Finding 1: No Calendar Patterns in Rule-Based Classifier

`services/queries/query_router.py` lines 354-375 only match pure temporal queries:
```python
# Temporal queries (line 354-375)
elif any(phrase in message_lower for phrase in [
    "what day is it",
    "what time is it",
    "current date",
    "current time",
    "today's date",
]):
    return Intent(category=IntentCategory.TEMPORAL, ...)
```

**Missing**: Calendar patterns like "what's on my calendar", "meetings today", "schedule"

### Finding 2: LLM Classifier Routes to TEMPORAL

When rule-based doesn't match, LLM classifier (or fallback) classifies "What's on my calendar today?" as TEMPORAL because:
- Contains "today" (temporal keyword)
- Asks about schedule (time-related)

### Finding 3: Canonical Handler Bypass

Once classified as TEMPORAL, `canonical_handlers.can_handle()` returns True (line 114-124), and `handle_temporal()` is called instead of the QUERY handlers.

### Finding 4: Different Calendar Code Path

`canonical_handlers.handle_temporal()` (line 723) calls:
```python
calendar_adapter = CalendarIntegrationRouter()  # No user_id!
temporal_summary = await calendar_adapter.get_temporal_summary()
```

This is a DIFFERENT code path from `_handle_meeting_time_query()` which uses:
```python
calendar_router = CalendarIntegrationRouter(user_id=user_id)
events = await calendar_router.get_todays_events()
```

---

## Implementation Options

### Option A: Add Calendar Patterns to Pre-Classifier (RECOMMENDED)

**Pros**:
- Fast, rule-based routing
- No LLM latency
- Specific patterns prevent over-matching

**Cons**:
- Pattern maintenance
- May miss creative phrasings

**Location**: `services/queries/query_router.py`, `_rule_based_classification()` method

**Code Change**:
```python
# Calendar queries (NEW - before temporal patterns)
elif any(phrase in message_lower for phrase in [
    "what's on my calendar",
    "what is on my calendar",
    "my calendar today",
    "meetings today",
    "do i have any meetings",
    "what meetings",
    "my schedule today",
]):
    return Intent(
        category=IntentCategory.QUERY,
        action="meeting_time",
        confidence=0.95,
        original_message=message,
        context={"rule_based": True, "calendar_query": True},
    )
```

### Option B: Fix Canonical TEMPORAL Handler

**Pros**:
- Keeps existing classification
- Single code path for calendar

**Cons**:
- TEMPORAL handler becomes complex
- Doesn't use the QUERY handlers we fixed

**Change**: Update `handle_temporal()` to pass user_id to CalendarIntegrationRouter

### Option C: Re-route in IntentService

**Pros**:
- Central routing logic
- Can intercept before canonical handlers

**Cons**:
- More complex flow
- Adds conditional logic

---

## Selected Approach: Option A

Add calendar patterns to the rule-based pre-classifier in `query_router.py`. This:
1. Routes calendar queries to QUERY category
2. Invokes the fixed `_handle_meeting_time_query()` with user_id
3. Uses the timezone-aware calendar adapter (#586)
4. Fast, deterministic, testable

---

## Implementation Plan

### Phase 1: Add Calendar Patterns to Pre-Classifier

**File**: `services/queries/query_router.py`
**Method**: `_rule_based_classification()` (starts line 319)
**Location**: Insert BEFORE temporal patterns (line 354)

**Patterns to Add**:
```python
CALENDAR_PATTERNS = [
    "what's on my calendar",
    "what is on my calendar",
    "whats on my calendar",
    "my calendar today",
    "calendar today",
    "meetings today",
    "do i have any meetings",
    "do i have meetings",
    "what meetings do i have",
    "my schedule today",
    "today's schedule",
    "todays schedule",
    "schedule for today",
]
```

**Evidence Required**:
- [ ] Pattern block added before temporal patterns
- [ ] Returns `Intent(category=QUERY, action="meeting_time")`
- [ ] grep shows no "calendar" in temporal patterns

### Phase 2: Unit Tests for Calendar Routing

**File**: `tests/unit/services/queries/test_query_router_calendar.py` (new)

**Test Cases**:
1. `test_whats_on_my_calendar_routes_to_query`
2. `test_meetings_today_routes_to_query`
3. `test_do_i_have_meetings_routes_to_query`
4. `test_what_time_is_it_still_routes_to_temporal` (regression)
5. `test_what_day_is_it_still_routes_to_temporal` (regression)

**Evidence Required**:
- [ ] 5 test cases exist
- [ ] All tests pass
- [ ] Regression tests confirm TEMPORAL still works

### Phase 3: Routing Integration Test (Issue #521 Learning)

**CRITICAL**: Per gameplan template v9.3, unit tests that mock routing are NOT sufficient.
We MUST include routing integration tests that verify the full path.

**File**: `tests/integration/services/intent/test_calendar_intent_routing.py` (new)

**Why This Matters**: Issue #521 had 17 passing unit tests but queries failed in production
because the pre-classifier intercepted them. Routing integration tests catch this.

**Test Cases**:

```python
# GOOD: Tests full routing path (pre-classifier → intent service → handler)
async def test_calendar_query_routes_to_query_handler():
    """Issue #589: Routing integration test - calendar queries reach QUERY handler"""
    from services.queries.query_router import QueryRouter

    router = QueryRouter()
    intent = router._rule_based_classification(
        "What's on my calendar today?",
        user_context=None,
        session_id="test"
    )

    # Verify routing reaches correct category and action
    assert intent.category == IntentCategory.QUERY
    assert intent.action == "meeting_time"  # ✅ Proves routing works

async def test_calendar_query_returns_events():
    """Issue #589: Full flow test - calendar queries return actual events"""
    # Send message through intent service (not mocked)
    result = await intent_service.process_intent(
        message="What's on my calendar today?",
        session_id="test",
        user_id="test-user-id"
    )
    # Verify we got calendar data (not "no meetings" from TEMPORAL)
    assert "no meetings" not in result.message.lower() or actual_no_meetings
```

**Evidence Required**:
- [ ] Routing integration test exists (tests classification, not handler)
- [ ] Full flow test exists (tests end-to-end)
- [ ] Both tests pass

### Phase 4: Manual Verification

**Steps**:
1. Restart server after code changes
2. Ask Piper: "What's on my calendar today?"
3. Verify events appear (not "no meetings")
4. Test variations: "Do I have any meetings?", "My schedule today"

**Evidence Required**:
- [ ] Terminal output showing events returned
- [ ] Multiple phrasings work

---

## Completion Matrix

| Phase | Task | Status | Evidence |
|-------|------|--------|----------|
| -1 | Infrastructure verification | ⬜ | Verification command output |
| 1 | Add calendar patterns to pre-classifier | ⬜ | Line numbers |
| 1 | Patterns return QUERY/meeting_time | ⬜ | Code snippet |
| 2 | Unit test: calendar → QUERY | ⬜ | Test output |
| 2 | Unit test: time/date → TEMPORAL (regression) | ⬜ | Test output |
| 3 | **Routing integration test** (Issue #521 learning) | ⬜ | Test output |
| 3 | Full flow integration test | ⬜ | Test output |
| 4 | Manual: "What's on my calendar" works | ⬜ | Terminal output |
| 4 | Manual: "Do I have meetings" works | ⬜ | Terminal output |
| - | Full test suite passes (1720+) | ⬜ | pytest output |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking TEMPORAL queries | Medium | High | Regression tests for "what time/day is it" |
| Over-matching (false positives) | Low | Medium | Specific patterns, not broad matching |
| Pattern gaps (false negatives) | Medium | Low | Can add patterns incrementally |
| LLM classifier disagreement | Low | Low | Rule-based takes priority |

---

## Files Modified

| File | Change Type |
|------|-------------|
| `services/queries/query_router.py` | Add calendar patterns |
| `tests/unit/services/queries/test_query_router_calendar.py` | New test file |
| `tests/integration/services/intent/test_calendar_intent_routing.py` | New test file |

---

## Out of Scope

- #588 "Tomorrow" queries (separate temporal modifier issue)
- Canonical TEMPORAL handler refactoring
- LLM classifier retraining

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] `_rule_based_classification()` method doesn't exist or has different signature
- [ ] Temporal patterns not at expected location (line ~354)
- [ ] `IntentCategory.QUERY` not available
- [ ] `meeting_time` action not handled in `_handle_query_intent()`
- [ ] Any existing tests fail after changes
- [ ] Calendar queries still route to TEMPORAL after fix
- [ ] TEMPORAL queries ("what time is it") break (regression)

---

## Definition of Done

- [ ] "What's on my calendar today?" returns actual events
- [ ] "Do I have any meetings?" returns actual events
- [ ] "What time is it?" still works (regression)
- [ ] Unit tests pass
- [ ] Integration test passes
- [ ] Full test suite passes (1720+ tests)
- [ ] PM manual verification
- [ ] Issue #589 closed with evidence

---

## Subagent Deployment

This is a focused fix - single agent sufficient.

**Agent**: Code Agent
**Scope**: Phases 1-4
**Handoff**: PM verification

---

_Gameplan created: 2026-01-13_
_Type: Bug Fix_
_Estimated effort: Small-Medium (1-2 hours)_

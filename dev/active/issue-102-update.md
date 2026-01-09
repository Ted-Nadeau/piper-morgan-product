# CONV-UX-GREET: Calendar Scanning on Greeting

**Priority**: P1 - High Value
**Labels**: `priority: high`, `component: integration`, `component: ai`, `size: medium`
**Milestone**: Sprint B1
**Epic**: FTUX (First-Time User Experience)
**Related**: #491 (FTUX-CONCIERGE), UX-001.6 (Temporal Context)

---

## Problem Statement

### Current State
Current system is reactive rather than proactive:
- No automatic calendar awareness on conversation start
- Missing proactive identification of schedule conflicts and important meetings
- Lacks proactive surfacing of time-sensitive dependencies and blockers
- No contextual greeting enhancement with schedule intelligence

### Impact
- **Blocks**: Users must explicitly ask about their calendar; no proactive awareness
- **User Impact**: Alpha testers miss time-sensitive information; Piper feels "dumb" compared to expectation
- **Technical Debt**: Greeting responses remain static while calendar infrastructure already exists

### Strategic Context
Part of FTUX sprint making Piper feel intelligent from first interaction. Calendar integration already exists; this leverages existing infrastructure to demonstrate proactive value immediately on greeting.

---

## Goal

**Primary Objective**: When user greets Piper, automatically scan calendar and include relevant schedule context in the greeting response.

**Example User Experience**:
```
User: "Good morning"

Before: "Hello! I'm ready to help with your PM tasks. What would you like to work on today?"

After: "Good morning! Here's your day at a glance:
📅 **Next**: Sprint Planning at 10:00 AM
⏰ **Free time**: 9:00-10:00, 2:00-3:30
📋 3 meetings today

What would you like to focus on?"
```

**Not In Scope** (explicitly):
- ❌ Meeting importance scoring (P1 - defer to future sprint)
- ❌ Conflict detection between meetings (P1 - defer)
- ❌ Dependency surfacing between meetings and projects (P1 - defer)
- ❌ CalendarGreetingService class (issue over-specifies; use existing handlers)
- ❌ MeetingAnalyzer, ScheduleConflict, MeetingDependency classes (P1 - defer)
- ❌ Caching optimization (P2 - defer)

---

## What Already Exists

### Infrastructure ✅
- **GREETING_PATTERNS**: `services/intent_service/pre_classifier.py` - detects "hello", "hi", "good morning", etc.
- **ConversationHandler**: `services/conversation/conversation_handler.py` - handles "greeting" action with static responses
- **CalendarIntegrationRouter**: `services/integrations/calendar/calendar_integration_router.py` - has `get_temporal_summary()`, `get_todays_events()`, `get_next_meeting()`, `get_free_time_blocks()`
- **PluginRegistry**: Can check if calendar is configured via `get_status("calendar")`

### What's Missing ❌
- Calendar-aware greeting response in ConversationHandler
- Graceful fallback when calendar not configured
- Time-of-day awareness in greeting (morning vs afternoon vs evening)

---

## Requirements

### Phase 0: Infrastructure Verification
- [x] GREETING_PATTERNS exist in pre_classifier.py
- [x] ConversationHandler.respond() handles "greeting" action
- [x] CalendarIntegrationRouter.get_temporal_summary() available
- [x] PluginRegistry.get_status() can check calendar configuration

### Phase 1: Calendar-Aware Greeting
**Objective**: Enhance ConversationHandler to fetch calendar data on greeting

**Tasks**:
- [ ] Add `_get_calendar_summary()` method to ConversationHandler
- [ ] Add `_respond_to_greeting()` method for calendar-aware response
- [ ] Add `_format_calendar_greeting()` for response formatting
- [ ] Add `_get_time_of_day_greeting()` helper (morning/afternoon/evening)

**Deliverables**:
- Modified `services/conversation/conversation_handler.py`

### Phase 2: Tests
**Objective**: Verify greeting behavior with and without calendar

**Tasks**:
- [ ] Test greeting with calendar available (shows summary)
- [ ] Test greeting without calendar (graceful fallback)
- [ ] Test greeting with empty calendar
- [ ] Test time-of-day greeting logic

**Deliverables**:
- New/updated tests in `tests/unit/services/conversation/`

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] GitHub issue updated with evidence
- [ ] Session log completed

---

## Acceptance Criteria

### Functionality
- [ ] Detect greeting patterns in user messages (already exists - verify)
- [ ] Automatically trigger calendar scan on greeting detection
- [ ] Surface calendar summary in greeting response (next meeting, free blocks, meeting count)
- [ ] Time-of-day appropriate greeting (Good morning/afternoon/evening)
- [ ] Graceful handling if calendar unavailable (fallback to static response)

### Testing
- [ ] Unit tests for `_respond_to_greeting()` with mocked calendar
- [ ] Unit tests for fallback when calendar unavailable
- [ ] Unit tests for `_get_time_of_day_greeting()` logic

### Quality
- [ ] No regressions in existing greeting behavior
- [ ] Performance: Response < 1 second (calendar fetch + format)
- [ ] Error handling: Calendar errors don't crash greeting

### Documentation
- [ ] Code comments reference Issue #102
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| `_get_calendar_summary()` | ❌ | |
| `_respond_to_greeting()` | ❌ | |
| `_format_calendar_greeting()` | ❌ | |
| `_get_time_of_day_greeting()` | ❌ | |
| Unit tests | ❌ | |
| Fallback behavior | ❌ | |

---

## Testing Strategy

### Unit Tests
- Greeting with calendar returns enhanced response with schedule info
- Greeting without calendar falls back to static response
- Empty calendar shows "Clear calendar today!" message
- Time-of-day: 8am → "Good morning", 2pm → "Good afternoon", 7pm → "Good evening"

### Manual Testing Checklist
**Scenario 1**: Calendar configured
1. [ ] Say "Good morning" → Response includes calendar summary
2. [ ] Response shows next meeting if any
3. [ ] Response shows free time blocks

**Scenario 2**: Calendar not configured
1. [ ] Say "Hello" → Response is standard greeting (no error)

---

## STOP Conditions

**STOP immediately and escalate if**:
- CalendarIntegrationRouter API has changed from expected
- get_temporal_summary() returns unexpected structure
- Calendar plugin not properly registered
- Tests fail for any reason
- Performance exceeds 1 second for greeting response
- Existing greeting tests break

---

## Effort Estimate

**Overall Size**: Small (1 point)

**Breakdown by Phase**:
- Phase 0: Already verified ✅
- Phase 1: 1 hour (4 methods in 1 file)
- Phase 2: 30 min (unit tests)
- Phase Z: 15 min (documentation)

---

## Dependencies

### Required (Must be complete first)
- [x] Calendar integration operational (exists)
- [x] GREETING_PATTERNS in pre_classifier (exists)

### Optional (Nice to have)
- [ ] #491 FTUX-CONCIERGE (complete - provides pattern)

---

## Related Documentation

- **Architecture**: ADR-039 (Canonical Handlers)
- **Pattern**: pattern-007-intent-response-cycle
- **Related Issues**: #491 (FTUX-CONCIERGE), #242 (Interactive Standup)

---

## Evidence Section

[To be filled during implementation]

---

## Notes for Implementation

**Scope Reduction from Original Issue**: The original issue specified extensive functionality including MeetingImportance scoring, ScheduleConflict detection, MeetingDependency analysis, and a CalendarGreetingService class. Per PM scoping, P0 is limited to:

1. Calendar summary in greeting (next meeting, free blocks, count)
2. Time-of-day greeting
3. Graceful fallback

All other functionality is P1/P2 and deferred to future sprints.

---

_Issue updated: 2026-01-07_

# Grammar Audit: Calendar Integration (#624)

**Issue**: #624 GRAMMAR-TRANSFORM: Calendar Integration (Partial → Conscious)
**Auditor**: Lead Developer (Claude Code / Opus)
**Date**: 2026-01-21
**Files Audited**:
- `services/integrations/calendar/calendar_integration_router.py` (~350 lines)
- `services/mcp/consumer/google_calendar_adapter.py` (~870 lines)
- `services/intent_service/canonical_handlers.py` (calendar sections)

---

## Executive Summary

Calendar integration has **good temporal awareness** with `TemporalSummaryResult`, `CalendarStats`, and recommendation generation. The gap is in **presentation layer** - data is displayed mechanically rather than experientially.

**Key insight**: Calendar already provides context like "heavy meeting load" and "free blocks" - but when presenting, it says "**Meeting Load**: 5 meetings (4.0 hours)" instead of "You've got a packed day with back-to-back meetings."

---

## Grammar Element Analysis

### Entity ✅ (Good)
**What exists**: User tracked, meeting participants counted.

**Evidence**:
```python
# google_calendar_adapter.py:466
"attendees": len(event.get("attendees", [])),
```

**Assessment**: Entity preserved. No transformation needed.

### Moment ⚠️ (Needs Work)
**What exists**: Meetings as data objects with timestamps.

**Evidence**:
```python
# canonical_handlers.py:759
message += f"\n\n**Current Meeting**: {current_meeting.get('title', 'Meeting')}"
message += f"\n- Duration: {current_meeting.get('duration', 'Unknown')}"
```

**Gap**: Meetings as data ("Duration: 60") not as experienced moments ("You're an hour into this one").

**Experience Test**:
- Current: `"**Current Meeting**: Team Standup\n- Duration: 30 minutes"`
- Conscious: "You're in Team Standup right now - about halfway through."

### Place ⚠️ (Partial)
**What exists**: Calendar recognized as a planning space.

**Evidence**:
```python
# canonical_handlers.py:1689
return "Collaboration time - good for meetings and team coordination."
```

**Gap**: Calendar Place atmosphere is minimal. No sense of whether the day is "packed", "relaxed", or "scattered".

### Lenses ⚠️ (Present but raw)
**What exists**: Excellent temporal analysis:
- `calendar_load`: "heavy" or "light"
- `total_meetings`, `total_meeting_minutes`, `total_free_minutes`
- `status`: "current", "upcoming", "completed"

**Evidence**:
```python
# google_calendar_adapter.py:621
calendar_load="heavy" if total_meeting_time > 240 else "light",
```

**Gap**: These lenses inform data but not narratives. "heavy" should become "Your day is packed."

### Situation ⚠️ (Functional but mechanical)
**What exists**: Recommendations generated with some context.

**Evidence**:
```python
# google_calendar_adapter.py:867
recommendations.append("📅 Calendar is clear for deep work")
```

**Assessment**: Some situational awareness exists, but presentation is template-based, not fluid.

---

## Response Generation Analysis

Calendar data flows through:
1. `GoogleCalendarMCPAdapter.get_temporal_summary()` → Returns `TemporalSummaryResult`
2. `CalendarIntegrationRouter` → Passes through
3. `canonical_handlers.py._handle_time_query()` → Formats for display

### Current Format Examples

```
**Current Meeting**: Team Standup
- Duration: 30 minutes

**Meeting Load**: 5 meetings (4.0 hours)
```

### Grammar-Conscious Format Examples

```
"You're in Team Standup - about halfway through."

"Your day is pretty packed - 5 meetings taking up most of the afternoon.
You've got a 45-minute window at 2pm if you need focus time."
```

---

## Transformation Opportunities

### 1. CalendarResponseContext
Create context dataclass capturing:
- Day atmosphere (packed, relaxed, scattered, focused)
- Current moment (in meeting, between meetings, free)
- Time pressure (rushing, comfortable, plenty of time)

### 2. Calendar Narrative Bridge
Transform calendar data into experiential narratives:
- Meeting duration → "halfway through" / "just started" / "wrapping up"
- Meeting load → "packed day" / "light day" / "good mix"
- Free blocks → "you've got a window" / "clear afternoon"
- Time until next → "plenty of time" / "a few minutes" / "right after this"

### 3. Canonical Handler Integration
Update calendar presentation in `canonical_handlers.py` to use narrative bridge.

---

## Recommended Transformation Phases

### Phase 1: CalendarResponseContext (1h)
Create dataclass capturing calendar-specific context for grammar-conscious responses.

### Phase 2: Calendar Narrative Bridge (1.5h)
Create transformation functions for common calendar patterns:
- `narrate_meeting_status()`
- `narrate_day_atmosphere()`
- `narrate_free_time()`
- `narrate_time_pressure()`

### Phase 3: Helper Integration (1h)
Create helper functions for use in canonical handlers.

### Phase 4: Testing (1h)
Test narrative transformations pass Contractor Test.

**Total**: ~4.5 hours

---

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `services/integrations/calendar/response_context.py` | Create | CalendarResponseContext dataclass |
| `services/integrations/calendar/narrative_bridge.py` | Create | Narrative transformation functions |
| `services/integrations/calendar/__init__.py` | Modify | Export new components |

---

## Patterns to Apply

| Pattern | Application |
|---------|-------------|
| Pattern-050 | CalendarResponseContext (Context Dataclass) |
| Pattern-052 | Narrative Bridge transforms data to experience |
| Pattern-053 | Warmth calibration for busy/stressful days |
| Pattern-054 | Honest failure when calendar unreachable |

---

## Success Criteria

1. **No raw data in responses** - Users see "packed day" not "5 meetings (4.0 hours)"
2. **Temporal awareness expressed** - "halfway through" not "duration: 30 minutes"
3. **Day atmosphere conveyed** - "good day for deep work" not "calendar_load: light"
4. **Contractor Test passes** - Professional tone, not robotic

---

## Experience Test Examples

| Data | Grammar-Conscious |
|------|-------------------|
| `total_meetings: 5, total_meeting_time: 240` | "Your day is packed with meetings" |
| `status: "current", duration: 30, elapsed: 15` | "You're about halfway through" |
| `free_blocks: [{duration: 60}]` | "You've got an hour free later" |
| `next_meeting: 5 minutes` | "You've got a few minutes before your next" |
| `calendar_load: "light"` | "Pretty open day - good for focus work" |

---

## Risk Assessment

**Low Risk**: We're adding a narrative layer, not changing calendar data retrieval.

**Scope Note**: The transformation focuses on response presentation, not the `GoogleCalendarMCPAdapter` analysis layer (which is working well).

---

*Ready for gameplan creation*

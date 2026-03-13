# Gameplan: Calendar Integration Grammar Transformation (#624)

**Issue**: #624 GRAMMAR-TRANSFORM: Calendar Integration (Partial → Conscious)
**Author**: Lead Developer (Claude Code / Opus)
**Date**: 2026-01-21
**Prerequisites**: #619, #620, #621 complete (reusing patterns)

---

## Strategic Insight

Calendar already has good temporal analysis (`CalendarStats`, `TemporalSummaryResult`). The gap is purely in **presentation**: raw stats need to become human narratives about your day.

**Focus**: Narrative bridge layer, not data layer changes.

---

## Phase Overview

| Phase | Focus | Effort | Parallelizable |
|-------|-------|--------|----------------|
| 1 | CalendarResponseContext | 1h | No (foundation) |
| 2 | Calendar Narrative Bridge | 1.5h | After Phase 1 |
| 3 | Helper Integration | 1h | After Phase 2 |
| 4 | Testing | 1h | After Phase 3 |
| **Total** | | **4.5h** | |

---

## Phase 1: CalendarResponseContext

### Objective
Create a context dataclass for calendar-specific grammar-conscious responses.

### Deliverables

**File**: `services/integrations/calendar/response_context.py`

```python
@dataclass
class CalendarResponseContext:
    """Rich context for grammar-conscious calendar responses."""

    # Day atmosphere
    day_atmosphere: str  # "packed", "light", "scattered", "focused"
    meeting_count: int
    meeting_hours: float
    free_hours: float

    # Current moment
    current_status: str  # "in_meeting", "between_meetings", "free"
    current_meeting_title: Optional[str] = None
    current_meeting_progress: float = 0.0  # 0.0 to 1.0

    # Time pressure
    minutes_until_next: Optional[int] = None
    time_pressure: str = "comfortable"  # "rushing", "comfortable", "plenty"

    # Free time
    longest_free_block: int = 0  # minutes
    free_blocks_count: int = 0

    @classmethod
    def from_temporal_summary(cls, summary: Dict) -> "CalendarResponseContext":
        """Build from TemporalSummaryResult dict."""
        ...

    def get_formality(self) -> str:
        """Get appropriate formality based on context."""
        # Busy day -> more concise
        # Light day -> can be more conversational
        ...
```

### Tests
- `tests/unit/services/integrations/calendar/test_response_context.py`
- Test from_temporal_summary() factory
- Test atmosphere detection
- Test time pressure calculation

### Acceptance Criteria
- [ ] CalendarResponseContext dataclass created
- [ ] from_temporal_summary() works with real calendar data shape
- [ ] All tests pass

---

## Phase 2: Calendar Narrative Bridge

### Objective
Create transformation functions that turn calendar data into experiential narratives.

### Deliverables

**File**: `services/integrations/calendar/narrative_bridge.py`

```python
class CalendarNarrativeBridge:
    """Transform calendar data into experiential narratives."""

    DAY_ATMOSPHERE_NARRATIVES = {
        "packed": "Your day is packed with meetings",
        "light": "Pretty open day - good for focus work",
        "scattered": "Meetings scattered throughout the day",
        "focused": "A few focused blocks today",
    }

    MEETING_PROGRESS_NARRATIVES = {
        "starting": "just started",
        "early": "still early in",
        "halfway": "about halfway through",
        "late": "wrapping up",
        "ending": "almost done with",
    }

    TIME_PRESSURE_NARRATIVES = {
        "rushing": "just a few minutes",
        "comfortable": "some time",
        "plenty": "plenty of time",
    }

    def narrate_current_status(self, ctx: CalendarResponseContext) -> str:
        """Describe current meeting status."""
        if ctx.current_status == "in_meeting":
            progress = self._get_progress_phrase(ctx.current_meeting_progress)
            return f"You're {progress} {ctx.current_meeting_title}"
        elif ctx.current_status == "between_meetings":
            return self._narrate_between_meetings(ctx)
        else:
            return "Your calendar is clear right now"

    def narrate_day_atmosphere(self, ctx: CalendarResponseContext) -> str:
        """Describe overall day feel."""
        return self.DAY_ATMOSPHERE_NARRATIVES.get(ctx.day_atmosphere, "")

    def narrate_free_time(self, ctx: CalendarResponseContext) -> str:
        """Describe available free time."""
        if ctx.longest_free_block >= 60:
            hours = ctx.longest_free_block // 60
            return f"You've got {hours} hour{'s' if hours > 1 else ''} free later"
        elif ctx.longest_free_block >= 30:
            return f"You've got a {ctx.longest_free_block}-minute window"
        elif ctx.longest_free_block > 0:
            return "Just quick breaks between meetings"
        else:
            return "Back-to-back meetings today"

    def narrate_time_until_next(self, minutes: int) -> str:
        """Describe time until next meeting."""
        if minutes <= 5:
            return "Your next meeting is starting soon"
        elif minutes <= 15:
            return "You've got a few minutes before your next"
        elif minutes <= 30:
            return "Half an hour until your next meeting"
        elif minutes <= 60:
            return "About an hour until your next meeting"
        else:
            return f"Next meeting isn't for a while ({minutes // 60}+ hours)"
```

### Tests
- Test each narrate_* function
- Test progress phrases (0%, 25%, 50%, 75%, 100%)
- Test edge cases (0 meetings, all-day events)
- Contractor Test: no technical jargon

### Acceptance Criteria
- [ ] CalendarNarrativeBridge class created
- [ ] All narrate_* functions implemented
- [ ] Tests verify human-readable output
- [ ] No raw data in narratives

---

## Phase 3: Helper Integration

### Objective
Create helper functions for use in canonical handlers.

### Deliverables

**File**: `services/integrations/calendar/narrative_helpers.py`

```python
def narrate_meeting_status(temporal_summary: Dict) -> str:
    """Narrate current meeting status for display."""
    ...

def narrate_day_summary(temporal_summary: Dict) -> str:
    """Narrate overall day for display."""
    ...

def narrate_next_meeting(temporal_summary: Dict) -> str:
    """Narrate next meeting for display."""
    ...

def narrate_free_blocks(temporal_summary: Dict) -> str:
    """Narrate available free time."""
    ...
```

### Tests
- Test helpers with realistic temporal_summary data
- Test edge cases (no meetings, calendar error)

### Acceptance Criteria
- [ ] Helper functions created
- [ ] Can be called from canonical handlers
- [ ] Exports added to __init__.py

---

## Phase 4: Testing

### Test Scenarios

1. **Day Atmosphere**
   - 5+ meetings → "packed day"
   - 1-2 meetings → "light day"
   - Meetings spread out → "scattered"

2. **Meeting Progress**
   - 0% → "just started"
   - 50% → "halfway through"
   - 90% → "wrapping up"

3. **Time Pressure**
   - 5 min → "starting soon"
   - 15 min → "few minutes"
   - 60+ min → "plenty of time"

4. **Free Time**
   - 60+ min block → "hour free"
   - 30 min → "30-minute window"
   - No blocks → "back-to-back"

### Contractor Test
- No "total_meetings", "duration_minutes", etc. in output
- Professional language
- Not overly verbose

---

## Completion Matrix

| Phase | Component | Tests | Evidence |
|-------|-----------|-------|----------|
| 1 | CalendarResponseContext | ⬜ | Dataclass works |
| 2 | CalendarNarrativeBridge | ⬜ | Narratives human-readable |
| 3 | Helper Integration | ⬜ | Helpers callable |
| 4 | Testing | ⬜ | All tests green |

---

## Files to Create/Modify

| File | Action | Phase |
|------|--------|-------|
| `services/integrations/calendar/response_context.py` | Create | 1 |
| `services/integrations/calendar/narrative_bridge.py` | Create | 2 |
| `services/integrations/calendar/narrative_helpers.py` | Create | 3 |
| `services/integrations/calendar/__init__.py` | Modify | 3 |
| `tests/unit/services/integrations/calendar/test_response_context.py` | Create | 1 |
| `tests/unit/services/integrations/calendar/test_narrative_bridge.py` | Create | 2 |
| `tests/unit/services/integrations/calendar/test_narrative_helpers.py` | Create | 3 |

---

## Experience Test Validation

After implementation, verify these transformations:

| Input | Output (should be) |
|-------|-------------------|
| `{total_meetings: 5, total_meeting_time: 240}` | "Your day is packed with meetings" |
| `{status: "current", progress: 0.5}` | "You're about halfway through" |
| `{longest_free_block: 60}` | "You've got an hour free later" |
| `{minutes_until_next: 10}` | "You've got a few minutes before your next" |
| `{calendar_load: "light"}` | "Pretty open day - good for focus work" |

---

*Ready for implementation*

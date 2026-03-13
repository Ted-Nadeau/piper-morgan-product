# MUX-TECH-PHASE1-GRAMMAR: Implement Core Object Model Grammar

## Updated Description (Jan 21, 2026)

**Track**: MUX (Embodied UX)
**Epic**: TECH (Technical Implementation)
**Type**: Implementation
**Priority**: Critical
**Dependencies**: ✅ VISION-OBJECT-MODEL (#399), ✅ ADR-045
**Original Estimate**: 16 hours
**Revised Estimate**: 4 hours (remaining work only)

---

## Context

This issue was written in December 2025. Since then, **#399 MUX-VISION-OBJECT-MODEL** implemented the core grammar infrastructure on Jan 19-20, 2026.

**What was requested** (original spec):
1. Create Moment model with theatrical unity
2. Create Situation model as container
3. Implement 8-stage Lifecycle enum
4. Add lifecycle to existing models

**What was implemented** (in #399):
- ✅ `MomentProtocol` in `services/mux/protocols.py`
- ✅ `Situation` context manager in `services/mux/situation.py`
- ✅ `LifecycleState` enum with all 8 stages in `services/mux/lifecycle.py`
- ✅ `LifecycleManager` and `CompostingExtractor`
- ✅ `HasLifecycle` protocol for integration
- ✅ 302 tests covering all functionality

**What remains**:
- ⚠️ Integration with existing domain models (`services/domain/models.py`)

---

## Implementation Status

### 1. Moment Model ✅ COMPLETE

```python
# services/mux/protocols.py
@runtime_checkable
class MomentProtocol(Protocol):
    id: str
    timestamp: datetime
    def captures(self) -> Dict[str, Any]: ...
```

**Evidence**: Protocol exists with timestamp, captures() method for policy/process/people/outcomes.

### 2. Situation Model ✅ COMPLETE

```python
# services/mux/situation.py
@dataclass
class Situation:
    description: str
    dramatic_tension: str
    goals: List[str]
    moments: List[Any]
    outcomes: List[str]
    # Async context manager support
    async def __aenter__(self) -> "Situation": ...
    async def __aexit__(self, ...): ...
    def extract_learning(self) -> SituationLearning: ...
```

**Evidence**: Full implementation with learning extraction, duration tracking, active state.

### 3. Lifecycle Enum ✅ COMPLETE

```python
# services/mux/lifecycle.py
class LifecycleState(Enum):
    EMERGENT = "emergent"
    DERIVED = "derived"
    NOTICED = "noticed"      # ← Consciousness language as specified
    PROPOSED = "proposed"
    RATIFIED = "ratified"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    COMPOSTED = "composted"  # ← Terminal state with composting
```

**Evidence**: All 8 stages, meanings, experience phrases, valid transitions, composting extractor.

### 4. Domain Model Integration ⚠️ REMAINING

The `HasLifecycle` protocol exists but is not yet integrated with:
- `services/domain/models.py` - WorkItem, Task, Feature, etc.

**Remaining work**: Add optional `lifecycle_state` and `lifecycle_history` to relevant domain models.

---

## Revised Acceptance Criteria

### Already Met ✅

- [x] Moment model expresses bounded occurrences, not tasks
- [x] Situation containers organize Moments narratively
- [x] Lifecycle includes composting that feeds back to Emergent
- [x] "Noticed" appears in lifecycle (consciousness language)
- [x] Models include consciousness attributes (awareness, attention, emotion via Perception)
- [x] Tests verify the theatrical unity constraints (302 tests)

### Remaining ⚠️

- [ ] Morning Standup can be expressed using these models (needs integration test)
- [ ] WorkItem/Task/Feature have optional lifecycle_state field
- [ ] Domain model integration documented

---

## Revised Deliverables

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| MomentProtocol | ✅ Done | `services/mux/protocols.py` |
| Situation class | ✅ Done | `services/mux/situation.py` |
| LifecycleState enum | ✅ Done | `services/mux/lifecycle.py` |
| LifecycleManager | ✅ Done | `services/mux/lifecycle.py` |
| CompostingExtractor | ✅ Done | `services/mux/lifecycle.py` |
| HasLifecycle protocol | ✅ Done | `services/mux/lifecycle.py` |
| Domain model integration | ⚠️ Remaining | `services/domain/models.py` |
| Integration test | ⚠️ Remaining | Morning Standup expression |

---

## Remaining Work (~4 hours)

### Phase 1: Domain Model Integration (3h)

Add to `services/domain/models.py`:

```python
from services.mux.lifecycle import LifecycleState, LifecycleTransition

@dataclass
class WorkItem:
    # ... existing fields ...
    lifecycle_state: Optional[LifecycleState] = None
    lifecycle_history: List[LifecycleTransition] = field(default_factory=list)
```

Apply to: WorkItem, Task, Feature, Decision (objects with natural lifecycles)

### Phase 2: Integration Test (1h)

Create test demonstrating Morning Standup expressed as:
- Entity (Team) experiences Moment (Standup) in Place (Channel)
- Situation wraps the standup with goals/outcomes/learning

---

## Verification

### Consciousness Test ✅ (Already Verified)

Can express "Piper notices user seems frustrated during sprint planning" as a Moment:
- Entity: User (experiencing frustration)
- Place: Sprint planning meeting
- Moment: Bounded scene of recognition
- Perception with mode=NOTICING

### Anti-Flattening Test ✅ (Already Verified)

- Moments are bounded scenes (via Situation.add_moment)
- Situations contain narrative (dramatic_tension, goals, learning)
- Lifecycle includes transformation (composting → emergent feedback)

---

## References

- ADR-045: Object Model specification ✅
- ADR-055: Object Model Implementation ✅
- #399: MUX-VISION-OBJECT-MODEL (implementation) ✅
- Morning Standup: Reference implementation patterns

---

*Updated: 2026-01-21*
*Original estimate: 16h → Revised: 4h (90% complete)*

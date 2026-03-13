# MUX-399-P3 - Lifecycle State Machine with Composting

**Priority**: P1
**Labels**: `MUX`, `architecture`, `DDD`, `state-machine`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-055, #614 (P2)

---

## Problem Statement

### Current State
Objects in the system have implicit lifecycles but no formal state machine:
- Things are "active" or "deleted" with nothing in between
- No concept of deprecation, archiving, or composting
- Deletion destroys without extracting value
- No lifecycle history tracking

### Impact
- **Blocks**: Proper handling of object retirement with learning extraction
- **User Impact**: Lost institutional knowledge when things are deleted
- **Technical Debt**: Ad-hoc status fields across models with inconsistent semantics

### Strategic Context
"Nothing disappears, it transforms." The shadow side of PM work is ending things - but ending should feed new beginnings. Composting closes the loop: archived knowledge becomes fertilizer for future decisions.

---

## Goal

**Primary Objective**: Implement the 8-stage lifecycle state machine with composting feedback to the learning system.

**Example User Experience**:
```
Before: Task deleted → gone forever
After: Task composted → "What did we learn from this task?" extracted and fed to learning system
```

**Not In Scope** (explicitly):
- ❌ Migrating all existing models to lifecycle (future work)
- ❌ Automatic lifecycle transitions based on rules
- ❌ UI for lifecycle state management
- ❌ Lifecycle-based permissions

---

## Requirements

### Phase 1: Lifecycle State Definitions ✅
- [x] Create `services/mux/lifecycle.py`
- [x] Define `LifecycleState` enum with 8 states
- [x] Document each state with meaning, experience phrase, typical objects
- [x] Write tests for enum behavior

### Phase 2: Transition Rules ✅
- [x] Create VALID_TRANSITIONS map
- [x] Define `LifecycleTransition` dataclass
- [x] Implement is_valid() method
- [x] Create `InvalidTransitionError`
- [x] Write tests for transition validation

### Phase 3: HasLifecycle Protocol ✅
- [x] Define `HasLifecycle` protocol with @runtime_checkable
- [x] Include lifecycle_state and lifecycle_history properties
- [x] Write compliance tests

### Phase 4: LifecycleManager ✅
- [x] Create `LifecycleManager` class
- [x] Implement transition() method with validation
- [x] Track history on objects
- [x] Emit events on transitions
- [x] Write comprehensive tests

### Phase 5: Composting Integration ✅
- [x] Define `CompostResult` dataclass
- [x] Create `CompostingExtractor` class
- [x] Extract object summary, journey, lessons
- [x] Write tests for composting extraction

### Phase Z: Completion & Handoff ✅
- [x] All acceptance criteria met
- [x] Evidence provided for each criterion
- [x] All tests passing (69 tests)
- [x] Documentation updated (ADR-055 Appendix B)
- [x] GitHub issue fully updated

---

## Acceptance Criteria

### Functionality
- [x] `LifecycleState` enum defined with 8 states (PM validated)
- [x] Each state has meaning, experience_phrase, typical_objects (PM validated)
- [x] Valid transition map enforced (PM validated)
- [x] `HasLifecycle` protocol defined and `@runtime_checkable` (PM validated)
- [x] `LifecycleManager` validates transitions (PM validated)
- [x] Transition history tracked on objects (PM validated)
- [x] `CompostingExtractor` extracts learning (PM validated)

### Testing
- [x] Unit tests for `LifecycleState` enum (PM validated)
- [x] Unit tests for transition validation (PM validated)
- [x] Unit tests for `HasLifecycle` protocol compliance (PM validated)
- [x] Unit tests for `LifecycleManager` operations (PM validated)
- [x] Unit tests for composting extraction (PM validated)

### Quality
- [x] No regressions in existing functionality (PM validated)
- [x] Type hints throughout (PM validated)
- [x] Docstrings with examples and metaphors (PM validated)
- [x] Follows existing code patterns in services/ (PM validated)

### Documentation
- [x] ADR-055 Appendix B with lifecycle diagram (PM validated)
- [x] Code documentation complete (PM validated)

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| LifecycleState enum (8 states) | ✅ | `services/mux/lifecycle.py:21-106` |
| Transition rules + LifecycleTransition | ✅ | `services/mux/lifecycle.py:108-177` |
| HasLifecycle protocol | ✅ | `services/mux/lifecycle.py:180-209` |
| LifecycleManager | ✅ | `services/mux/lifecycle.py:212-321` |
| CompostingExtractor | ✅ | `services/mux/lifecycle.py:324-430` |
| CompostResult dataclass | ✅ | `services/mux/lifecycle.py:433-460` |
| ADR-055 Appendix B | ✅ | `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md` |
| Unit Tests (69) | ✅ | `tests/unit/services/mux/test_lifecycle.py` |

**TOTAL: 8/8 = 100%**

---

## Evidence Section

### Implementation Evidence

**Test Results (69 tests passing):**
```
============================== 69 passed in 0.21s ==============================
```

**Combined P1+P2+P3 Tests (195 passing):**
```
============================= 195 passed in 0.28s ==============================
```

**Unit Test Regression Check (1958 passing):**
```
=============== 1958 passed, 26 skipped, 260 warnings in 21.83s ================
```

**Files Created:**
```
services/mux/lifecycle.py (16,011 bytes, +496 lines)
tests/unit/services/mux/test_lifecycle.py (+636 lines)
docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md (Appendix B added)
```

**Key Components Implemented:**

1. **LifecycleState Enum** with 8 stages and consciousness metaphors:
   - EMERGENT = "This is just appearing..."
   - DERIVED = "This follows from..."
   - NOTICED = "I see this now..."
   - PROPOSED = "I suggest we..."
   - RATIFIED = "We've committed to..."
   - DEPRECATED = "We're moving away from..."
   - ARCHIVED = "This is preserved but inactive..."
   - COMPOSTED = "This has become learning..."

2. **Transition Rules** (VALID_TRANSITIONS):
   ```
   EMERGENT → {DERIVED, NOTICED}
   DERIVED → {NOTICED, DEPRECATED}
   NOTICED → {PROPOSED, DEPRECATED}
   PROPOSED → {RATIFIED, DEPRECATED}
   RATIFIED → {DEPRECATED}
   DEPRECATED → {ARCHIVED}
   ARCHIVED → {COMPOSTED}
   COMPOSTED → {} (terminal)
   ```

3. **HasLifecycle Protocol** (@runtime_checkable):
   - lifecycle_state property
   - lifecycle_history property

4. **LifecycleManager** with:
   - transition() method
   - Validation of transition rules
   - History tracking
   - Event emission

5. **CompostingExtractor** with:
   - extract() method
   - object_summary extraction
   - journey preservation
   - lessons extraction

---

## Completion Checklist

- [x] All acceptance criteria met ✅
- [x] Completion matrix 100% ✅
- [x] Evidence provided for each criterion ✅
- [x] Tests passing with output ✅
- [x] Documentation updated ✅
- [x] No regressions confirmed ✅
- [x] STOP conditions all clear ✅

**Status**: ✅ COMPLETE - Ready for PM Closure

---

_Issue created: 2026-01-19_
_Completed: 2026-01-19_

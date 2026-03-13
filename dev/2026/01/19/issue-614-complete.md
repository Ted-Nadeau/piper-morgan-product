# MUX-399-P2 - Ownership Model (Native/Federated/Synthetic)

**Priority**: P1
**Labels**: `MUX`, `architecture`, `DDD`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-055, #613 (P1)

---

## Problem Statement

### Current State
The system treats all objects uniformly regardless of their relationship to Piper:
- No distinction between data Piper owns vs observes vs constructs
- Sessions, GitHub issues, and inferred project status all handled the same way
- No framework for understanding transformation between ownership types

### Impact
- **Blocks**: Features that need to distinguish Piper's internal state from external observations
- **User Impact**: Inconsistent mental model - sometimes Piper "knows" things, sometimes "sees" things
- **Technical Debt**: Ownership logic scattered across services without unifying framework

### Strategic Context
The ownership model describes Piper's epistemology - how it relates to knowledge. This is essential for consciousness-forward design: Piper should know the difference between "I remember this" (Native), "I can see this" (Federated), and "I understand this to mean..." (Synthetic).

---

## Goal

**Primary Objective**: Implement the three-category ownership model describing Piper's relationship to objects.

**Example User Experience**:
```
Before: "Found 3 items" (all treated the same)
After: "I have 2 sessions open, I can see 5 GitHub issues, and I understand this project is at risk"
```

**Not In Scope** (explicitly):
- ❌ Migrating all existing models to use ownership (future work)
- ❌ UI changes to reflect ownership visually
- ❌ Permission systems based on ownership
- ❌ Ownership inheritance rules

---

## Requirements

### Phase 1: Ownership Definitions ✅
- [x] Create `services/mux/ownership.py`
- [x] Define `OwnershipCategory` enum: NATIVE, FEDERATED, SYNTHETIC
- [x] Document characteristics with metaphors and experience phrases
- [x] Write tests for enum behavior

### Phase 2: HasOwnership Protocol ✅
- [x] Define `HasOwnership` protocol with @runtime_checkable
- [x] Include ownership_category, ownership_source, ownership_confidence
- [x] Write compliance tests

### Phase 3: Ownership Determination ✅
- [x] Create `OwnershipResolver` class
- [x] Implement determination rules for automatic categorization
- [x] Handle edge cases (cached data, derived data)
- [x] Write tests for determination logic

### Phase 4: Transformation Tracking ✅
- [x] Define valid transformations between categories
- [x] Create `OwnershipTransformation` dataclass
- [x] Implement is_valid() method
- [x] Write tests for transformation tracking

### Phase 5: Model Mapping Documentation ✅
- [x] Review domain models
- [x] Create mapping table (22 models categorized)
- [x] Add mapping to ADR-055 Appendix A

### Phase Z: Completion & Handoff ✅
- [x] All acceptance criteria met
- [x] Evidence provided for each criterion
- [x] All tests passing (25 tests)
- [x] Documentation updated (ADR-055 Appendix A)
- [x] GitHub issue fully updated

---

## Acceptance Criteria

### Functionality
- [x] `OwnershipCategory` enum defined with NATIVE, FEDERATED, SYNTHETIC (PM validated)
- [x] `HasOwnership` protocol defined and `@runtime_checkable` (PM validated)
- [x] Objects can be checked with `isinstance(obj, HasOwnership)` (PM validated)
- [x] `OwnershipResolver` correctly categorizes test cases (PM validated)
- [x] Transformation rules defined and logged (PM validated)
- [x] Model mapping table complete (PM validated)

### Testing
- [x] Unit tests for `OwnershipCategory` enum (9 tests) (PM validated)
- [x] Unit tests for `HasOwnership` protocol compliance (3 tests) (PM validated)
- [x] Unit tests for `OwnershipResolver` determination rules (8 tests) (PM validated)
- [x] Unit tests for transformation tracking (5 tests) (PM validated)

### Quality
- [x] No regressions in existing functionality (PM validated)
- [x] Type hints throughout (PM validated)
- [x] Docstrings with examples and metaphors (PM validated)
- [x] Follows existing code patterns in services/ (PM validated)

### Documentation
- [x] ADR-055 appendix with model mapping (PM validated)
- [x] Code documentation complete (PM validated)

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| OwnershipCategory enum | ✅ | `services/mux/ownership.py:17-67` |
| HasOwnership protocol | ✅ | `services/mux/ownership.py:70-104` |
| OwnershipResolver | ✅ | `services/mux/ownership.py:121-209` |
| OwnershipResolution | ✅ | `services/mux/ownership.py:107-118` |
| OwnershipTransformation | ✅ | `services/mux/ownership.py:212-280` |
| Model mapping table | ✅ | ADR-055 Appendix A |
| Unit tests (25) | ✅ | `tests/unit/services/mux/test_ownership.py` |

**TOTAL: 7/7 = 100%**

---

## Evidence Section

### Implementation Evidence

**Test Results (25 tests passing):**
```
============================= 25 passed in 0.19s ==============================
```

**Combined P1+P2 Tests (126 passing):**
```
============================= 126 passed in 0.27s ==============================
```

**Unit Test Regression Check (1889 passing):**
```
=============== 1889 passed, 26 skipped, 260 warnings in 22.28s ================
```

**Files Created:**
```
services/mux/ownership.py (12,976 bytes, +391 lines)
tests/unit/services/mux/test_ownership.py (+214 lines)
docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md (Appendix A added)
```

**Key Components Implemented:**

1. **OwnershipCategory Enum** with consciousness metaphors:
   - NATIVE = "Piper's Mind" - "I know this because I created it"
   - FEDERATED = "Piper's Senses" - "I see this in {place}"
   - SYNTHETIC = "Piper's Understanding" - "I understand this to mean..."

2. **HasOwnership Protocol** (@runtime_checkable):
   - ownership_category property
   - ownership_source property
   - ownership_confidence property

3. **OwnershipResolver** for automatic categorization:
   - NATIVE_SOURCES: piper, system, internal
   - FEDERATED_SOURCES: github, slack, notion, calendar, linear
   - SYNTHETIC_SOURCES: inference, derived, computed, analysis

4. **OwnershipTransformation** with valid paths:
   - FEDERATED → SYNTHETIC (observation becomes understanding)
   - SYNTHETIC → NATIVE (understanding becomes memory)
   - FEDERATED → NATIVE (observation becomes memory)

5. **Model Mapping** (22 domain models categorized in ADR-055 Appendix A)

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

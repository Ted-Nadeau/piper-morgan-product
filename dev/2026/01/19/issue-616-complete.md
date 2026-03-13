# MUX-399-P4 - Metadata Schema & Journal Extensions

**Priority**: P1
**Labels**: `MUX`, `architecture`, `DDD`, `metadata`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-055, #613 (P1), #614 (P2), #615 (P3)

---

## Problem Statement

### Current State
Objects have no standardized way to track metadata about themselves:
- No structured provenance (where data came from)
- No relevance scoring (how important something is)
- No attention tracking (who has noticed)
- No confidence tracking (how certain we are)
- No typed relationships between objects
- No unified journal/history system

### Impact
- **Blocks**: Intelligent filtering and prioritization
- **User Impact**: No way for Piper to express certainty or importance
- **Technical Debt**: Ad-hoc metadata fields scattered across models

### Strategic Context
"Metadata is what Piper knows about what it perceives." The 6 universal dimensions provide vocabulary for describing knowledge about knowledge.

---

## Goal

**Primary Objective**: Implement the 6 universal metadata dimensions with utilities and journal infrastructure.

**Example User Experience**:
```
Before: Task has no provenance or confidence
After: Task has metadata.provenance.source="github", metadata.confidence.score=0.9
```

**Not In Scope** (explicitly):
- ❌ Migrating existing models to use metadata
- ❌ ML-based inference of metadata values
- ❌ UI for metadata display
- ❌ Metadata-based filtering

---

## Requirements

### Phase 1: Metadata Dimension Definitions ✅
- [x] Create `services/mux/metadata.py`
- [x] Define Provenance dataclass with freshness decay
- [x] Define Relevance dataclass with factors and decay
- [x] Define AttentionState dataclass with levels
- [x] Define Confidence dataclass with basis tracking
- [x] Define RelationType enum and Relation dataclass
- [x] Define Journal with SessionJournalEntry and InsightJournalEntry
- [x] Write tests for all dimensions

### Phase 2: HasMetadata Protocol ✅
- [x] Create @runtime_checkable HasMetadata protocol
- [x] All dimensions Optional
- [x] Write compliance tests

### Phase 3: Trackers and Calculators ✅
- [x] Create ProvenanceTracker utility
- [x] Create ConfidenceCalculator utility
- [x] Write tests for both utilities

### Phase 4: Relations Registry ✅
- [x] Create RelationRegistry class
- [x] Support bidirectional relations
- [x] Write tests for registry operations

### Phase 5: Journal Manager ✅
- [x] Create JournalManager class
- [x] Two-layer journal (Session + Insight)
- [x] Write tests for journal operations

### Phase Z: Completion & Handoff ✅
- [x] All acceptance criteria met
- [x] Evidence provided for each criterion
- [x] All tests passing (67 tests)
- [x] Documentation updated (ADR-055 Appendix C)
- [x] GitHub issue fully updated

---

## Acceptance Criteria

### Functionality
- [x] 6 metadata dimensions defined (PM validated)
- [x] HasMetadata @runtime_checkable protocol (PM validated)
- [x] ProvenanceTracker utility (PM validated)
- [x] ConfidenceCalculator utility (PM validated)
- [x] RelationRegistry with bidirectional support (PM validated)
- [x] JournalManager with two-layer journal (PM validated)

### Testing
- [x] Unit tests for all dimensions (PM validated)
- [x] Unit tests for HasMetadata protocol compliance (PM validated)
- [x] Unit tests for trackers/calculators (PM validated)
- [x] Unit tests for RelationRegistry (PM validated)
- [x] Unit tests for JournalManager (PM validated)

### Quality
- [x] No regressions in existing functionality (PM validated)
- [x] Type hints throughout (PM validated)
- [x] Docstrings with examples and metaphors (PM validated)
- [x] Follows existing code patterns in services/ (PM validated)

### Documentation
- [x] ADR-055 Appendix C with metadata diagram (PM validated)
- [x] Code documentation complete (PM validated)

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Provenance dimension | ✅ | `services/mux/metadata.py:47-67` |
| Relevance dimension | ✅ | `services/mux/metadata.py:74-93` |
| AttentionState dimension | ✅ | `services/mux/metadata.py:100-117` |
| Confidence dimension | ✅ | `services/mux/metadata.py:124-142` |
| Relation + RelationType | ✅ | `services/mux/metadata.py:149-188` |
| Journal (Session + Insight) | ✅ | `services/mux/metadata.py:195-264` |
| HasMetadata protocol | ✅ | `services/mux/metadata.py:271-305` |
| ProvenanceTracker | ✅ | `services/mux/metadata.py:312-370` |
| ConfidenceCalculator | ✅ | `services/mux/metadata.py:377-414` |
| RelationRegistry | ✅ | `services/mux/metadata.py:421-478` |
| JournalManager | ✅ | `services/mux/metadata.py:485-544` |
| ADR-055 Appendix C | ✅ | `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md` |
| Unit Tests (67) | ✅ | `tests/unit/services/mux/test_metadata.py` |

**TOTAL: 13/13 = 100%**

---

## Evidence Section

### Implementation Evidence

**Test Results (67 tests passing):**
```
======================= 67 passed, 43 warnings in 0.21s ========================
```

**Combined P1+P2+P3+P4 Tests (262 passing):**
```
======================= 262 passed, 43 warnings in 0.32s =======================
```

**Unit Test Regression Check (2025 passing):**
```
=============== 2025 passed, 26 skipped, 303 warnings in 21.71s ================
```

**Files Created:**
```
services/mux/metadata.py (544 lines)
tests/unit/services/mux/test_metadata.py (624 lines)
docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md (Appendix C added)
```

**Key Components Implemented:**

1. **6 Metadata Dimensions** with experience framing:
   - **Provenance**: "I received this from {source} {freshness} ago"
   - **Relevance**: "This matters because {factors}"
   - **AttentionState**: "This has {level} attention from {noticed_by}"
   - **Confidence**: "I am {score}% confident based on {basis}"
   - **Relations**: "This {relation_type} {target}"
   - **Journal**: "The story of this object is..."

2. **RelationType Enum**:
   - REFERENCES, BLOCKS, CONTAINS, DERIVES_FROM
   - RELATED_TO, PARENT_OF, CHILD_OF

3. **Two-Layer Journal**:
   - Session: Audit trail (event_type, trigger, actor)
   - Insight: Meaning extraction (learning, connected_insights)

4. **HasMetadata Protocol** (@runtime_checkable):
   - All 6 dimensions as Optional properties
   - Duck typing compatible with isinstance()

5. **Utilities**:
   - ProvenanceTracker (from_integration, from_user_input, from_inference)
   - ConfidenceCalculator (from_observation, from_source_reliability)
   - RelationRegistry (add, remove, get_relations, bidirectional support)
   - JournalManager (log_session_event, extract_insight, get_journal)

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

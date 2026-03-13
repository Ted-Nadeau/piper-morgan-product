# MUX-399-P4 - Metadata Schema & Journal Extensions

**Priority**: P1
**Labels**: `MUX`, `architecture`, `DDD`, `metadata`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-055, ADR-050

---

## Problem Statement

### Current State
Metadata about objects is scattered and inconsistent:
- Some objects have `created_at`, some don't
- Confidence/certainty not tracked
- No systematic provenance tracking
- Session logs and insights stored separately without linking
- Relations between objects are implicit, not explicit

### Impact
- **Blocks**: Rich contextual awareness across objects
- **User Impact**: Piper can't express "how sure" it is or "where this came from"
- **Technical Debt**: Each service invents its own metadata patterns

### Strategic Context
Metadata is "what Piper knows about what it perceives." Without structured metadata, perception is shallow. The six dimensions provide a universal vocabulary for describing knowledge about knowledge.

---

## Goal

**Primary Objective**: Implement the 6 universal metadata dimensions and extend journal infrastructure.

**Example User Experience**:
```
Before: "Here are 3 items" (no context)
After: "Here are 3 items from GitHub (high confidence, fetched 5 min ago, related to Project X)"
```

**Not In Scope** (explicitly):
- ❌ Migrating all existing models to use metadata (future work)
- ❌ UI for displaying metadata
- ❌ Metadata-based filtering/search
- ❌ Automatic metadata inference (ML-based)

---

## What Already Exists

### Infrastructure ✅
- ADR-045: Object Model with metadata concepts
- ADR-050: Conversation-as-Graph (some journal patterns)
- Existing session logging infrastructure
- Learning service with some insight tracking
- `created_at`/`updated_at` on some database models

### What's Missing ❌
- Unified metadata dimension definitions
- `HasMetadata` protocol
- Provenance tracking type
- Relevance scoring type
- Attention state tracking
- Confidence scoring type
- Relations tracking type
- Two-layer journal (Session + Insight)

---

## Requirements

### Phase 1: Metadata Dimension Definitions
**Objective**: Define the 6 universal metadata dimensions

**Tasks**:
- [ ] Create `services/mux/metadata.py` (or appropriate location)
- [ ] Define dimension types:

  **1. Provenance** (where did this come from?):
  - `source`: Integration/service that provided it
  - `confidence`: How certain is the source (0-1)
  - `fetched_at`: When was this retrieved
  - `freshness`: How stale is this data

  **2. Relevance** (how important is this?):
  - `score`: Relevance score (0-1)
  - `factors`: What contributed to the score
  - `decay_rate`: How quickly relevance fades
  - `context`: What context is this relevant to

  **3. Attention State** (who has noticed this?):
  - `noticed_by`: List of entities that noticed
  - `noticed_at`: When first noticed
  - `attention_level`: Current attention priority

  **4. Confidence** (how sure are we?):
  - `score`: Confidence score (0-1)
  - `basis`: What is confidence based on
  - `last_validated`: When was this last verified

  **5. Relations** (how does this connect?):
  - `links`: List of typed relations to other objects
  - `relation_type`: Type of relationship
  - `strength`: Relationship strength (0-1)

  **6. Journal** (what's the history?):
  - `session_entries`: Audit trail (what happened)
  - `insight_entries`: Meaning extraction (what it meant)

- [ ] Write tests for each dimension type

**Deliverables**:
- 6 metadata dimension types
- Unit tests for dimension types

### Phase 2: HasMetadata Protocol
**Objective**: Create protocol for metadata-aware objects

**Tasks**:
- [ ] Define `HasMetadata` protocol with:
  - `provenance` property (optional)
  - `relevance` property (optional)
  - `attention_state` property (optional)
  - `confidence` property (optional)
  - `relations` property (optional)
  - `journal` property (optional)
- [ ] Make dimensions optional (not all objects need all metadata)
- [ ] Make protocol `@runtime_checkable`
- [ ] Write compliance tests

**Deliverables**:
- `HasMetadata` protocol definition
- Protocol compliance tests

### Phase 3: Provenance & Confidence Tracking
**Objective**: Implement source tracking and certainty

**Tasks**:
- [ ] Create `ProvenanceTracker` for recording sources
- [ ] Create `ConfidenceCalculator` with configurable basis
- [ ] Integrate with existing integration fetchers (design only, not migration)
- [ ] Write tests for tracking and calculation

**Deliverables**:
- `ProvenanceTracker` implementation
- `ConfidenceCalculator` implementation
- Unit tests

### Phase 4: Relations Tracking
**Objective**: Implement typed relationships between objects

**Tasks**:
- [ ] Define `Relation` type with:
  - `target_id`: ID of related object
  - `relation_type`: Type of relationship (REFERENCES, BLOCKS, CONTAINS, etc.)
  - `strength`: Relationship strength
  - `bidirectional`: Whether relation goes both ways
- [ ] Create `RelationRegistry` for managing relations
- [ ] Write tests for relation management

**Deliverables**:
- `Relation` type definition
- `RelationRegistry` implementation
- Relation tests

### Phase 5: Two-Layer Journal
**Objective**: Extend journal infrastructure with session + insight layers

**Tasks**:
- [ ] Document existing session logging infrastructure
- [ ] Define `SessionJournalEntry` (audit trail):
  - What happened
  - When it happened
  - What triggered it
- [ ] Define `InsightJournalEntry` (meaning extraction):
  - What it meant
  - Learning extracted
  - Connected insights
- [ ] Create `JournalManager` that coordinates both layers
- [ ] Integrate with existing learning service for insights
- [ ] Write tests for journaling

**Deliverables**:
- Session and Insight journal types
- `JournalManager` implementation
- Journal tests

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] All tests passing
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] Session log completed
- [ ] **Experience Checkpoint**: One paragraph on how metadata honors the grammar

---

## Acceptance Criteria

### Functionality
- [ ] All 6 metadata dimensions defined as types
- [ ] `HasMetadata` protocol defined and `@runtime_checkable`
- [ ] Dimensions are optional (objects can have subset)
- [ ] `ProvenanceTracker` records source information
- [ ] `ConfidenceCalculator` produces scores with basis
- [ ] `RelationRegistry` manages typed relationships
- [ ] Session journal captures audit trail
- [ ] Insight journal captures meaning extraction
- [ ] `JournalManager` coordinates both layers

### Testing
- [ ] Unit tests for each metadata dimension type
- [ ] Unit tests for `HasMetadata` protocol compliance
- [ ] Unit tests for `ProvenanceTracker`
- [ ] Unit tests for `ConfidenceCalculator`
- [ ] Unit tests for `RelationRegistry`
- [ ] Unit tests for journal entries and manager
- [ ] Integration test: Object with full metadata profile

### Quality
- [ ] No regressions in existing functionality
- [ ] Type hints throughout
- [ ] Docstrings with examples
- [ ] Follows existing code patterns in services/

### Documentation
- [ ] Metadata schema diagram in ADR-055
- [ ] Code documentation complete
- [ ] Experience checkpoint written
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Provenance dimension | ❌ | |
| Relevance dimension | ❌ | |
| Attention State dimension | ❌ | |
| Confidence dimension | ❌ | |
| Relations dimension | ❌ | |
| Journal dimension | ❌ | |
| HasMetadata protocol | ❌ | |
| ProvenanceTracker | ❌ | |
| ConfidenceCalculator | ❌ | |
| RelationRegistry | ❌ | |
| JournalManager | ❌ | |
| Experience checkpoint | ❌ | |

---

## Testing Strategy

### Unit Tests
```python
# Dimension type tests
def test_provenance_type_fields():
    """Test Provenance has required fields"""

def test_relevance_decay_calculation():
    """Test relevance decay over time"""

def test_confidence_basis_tracking():
    """Test that confidence records its basis"""

def test_relation_type_values():
    """Test relation types are well-defined"""

# Protocol tests
def test_has_metadata_with_all_dimensions():
    """Test object with full metadata"""

def test_has_metadata_with_partial_dimensions():
    """Test object with only some metadata dimensions"""

# Tracker tests
def test_provenance_tracker_records_source():
    """Test source recording"""

def test_confidence_calculator_produces_score():
    """Test confidence calculation"""

# Journal tests
def test_session_journal_entry():
    """Test session journal captures audit info"""

def test_insight_journal_entry():
    """Test insight journal captures meaning"""

def test_journal_manager_coordinates_layers():
    """Test both journal layers work together"""
```

### Integration Tests
```python
async def test_full_metadata_profile():
    """
    Verify an object can have complete metadata:
    - Provenance from GitHub
    - Relevance to current project
    - Attention from user
    - Confidence based on source
    - Relations to other objects
    - Journal entries (session + insight)
    """
```

### Manual Testing Checklist
**Scenario 1**: Metadata Assignment
1. [ ] Create object with provenance → verify source tracked
2. [ ] Add confidence → verify score and basis
3. [ ] Add relation → verify bidirectional if applicable

**Scenario 2**: Journal Entries
1. [ ] Log session event → verify audit trail
2. [ ] Extract insight → verify insight journal
3. [ ] Verify both accessible via JournalManager

---

## Success Metrics

### Quantitative
- 6 metadata dimension types defined
- 1 protocol definition
- 4+ utility classes (trackers, calculators, registries, managers)
- >40 tests passing
- 0 regressions

### Qualitative
- Metadata feels like "knowledge about knowledge"
- Journal tells the story of an object's life
- Relations create meaningful graph structure

---

## STOP Conditions

**STOP immediately and escalate if**:
- Metadata dimensions conflict with existing patterns
- Journal integration breaks existing logging
- Relations create circular dependency issues
- Performance concerns with metadata storage
- Scope creep into UI/migration territory

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (Dimension Definitions): 1.5 hours
- Phase 2 (Protocol): 0.5 hours
- Phase 3 (Provenance & Confidence): 0.5 hours
- Phase 4 (Relations): 0.5 hours
- Phase 5 (Two-Layer Journal): 1 hour
- Testing: Included in each phase

**Total**: 4 hours

**Complexity Notes**:
- Six dimensions means more types to define
- Journal integration needs careful coordination with existing systems

---

## Dependencies

### Required (Must be complete first)
- [ ] #[P1-issue-number] - Core Grammar & Lens Infrastructure (Protocols defined)

### Optional (Nice to have)
- Existing session logging documentation
- Learning service interface documentation
- P2 Ownership (metadata includes ownership context)
- P3 Lifecycle (journal tracks lifecycle transitions)

---

## Related Documentation

- **Architecture**: ADR-045 (metadata concepts), ADR-050 (graph model), ADR-055 (implementation)
- **Methodology**: TDD, DDD
- **Strategic**: "Metadata is what Piper knows about what it perceives"

---

## Evidence Section

[To be filled during implementation]

### Implementation Evidence
```bash
[Test output showing all tests passing]
[Commit hashes]
```

### Cross-Validation (if applicable)
**Verified By**: [TBD - separate verification agent]
**Date**:
**Report**:

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] Documentation updated ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅
- [ ] Cross-validation complete (if multi-agent) ✅

**Status**: Not Started

---

## Notes for Implementation

**From Chief Architect Memo**:
- Metadata should be optional per dimension
- Don't force all objects to have all metadata
- Consider lazy loading for expensive metadata

**Six Dimensions Summary**:
| Dimension | Question | Example |
|-----------|----------|---------|
| Provenance | Where from? | "Fetched from GitHub 5 min ago" |
| Relevance | How important? | "High relevance to Project X" |
| Attention | Who noticed? | "User noticed at 10:30 AM" |
| Confidence | How sure? | "85% confident based on direct observation" |
| Relations | Connections? | "Blocks Issue #123, Contains Task A" |
| Journal | What history? | "Created → Modified → Archived" |

**Two-Layer Journal**:
- **Session Journal**: The audit trail - what happened (objective, factual)
- **Insight Journal**: The meaning - what it meant (subjective, interpretive)

Example:
```
Session: "Task completed at 3:00 PM by user"
Insight: "Completing this task unblocked the release; user seems more confident with the workflow now"
```

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_

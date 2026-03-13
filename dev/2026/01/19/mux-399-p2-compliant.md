# MUX-399-P2 - Ownership Model (Native/Federated/Synthetic)

**Priority**: P1
**Labels**: `MUX`, `architecture`, `DDD`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-055

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

## What Already Exists

### Infrastructure ✅
- ADR-045: Object Model with ownership concepts mentioned
- P1 Protocol definitions (EntityProtocol, MomentProtocol, PlaceProtocol)
- Existing domain models that implicitly have ownership (sessions are Native, GitHub issues are Federated)

### What's Missing ❌
- `OwnershipCategory` enum definition
- `HasOwnership` protocol/mixin
- Ownership determination rules
- Transformation tracking between categories
- Documentation mapping existing models to categories

---

## Requirements

### Phase 1: Ownership Definitions
**Objective**: Define the three ownership categories and their characteristics

**Tasks**:
- [ ] Create `services/mux/ownership.py` (or appropriate location)
- [ ] Define `OwnershipCategory` enum: NATIVE, FEDERATED, SYNTHETIC
- [ ] Document characteristics of each category:
  - Native: Piper's Mind (sessions, memories, trust states, learning)
  - Federated: Piper's Senses (GitHub issues, Slack messages, calendar events)
  - Synthetic: Piper's Understanding (inferred status, assembled risk, pattern recognition)
- [ ] Write tests for enum behavior

**Deliverables**:
- `OwnershipCategory` enum with docstrings explaining each category
- Unit tests for ownership category definitions

### Phase 2: HasOwnership Protocol
**Objective**: Create protocol for objects with ownership awareness

**Tasks**:
- [ ] Define `HasOwnership` protocol with:
  - `ownership_category` property
  - `ownership_source` property (where it came from)
  - `ownership_confidence` property (how certain)
- [ ] Make protocol `@runtime_checkable`
- [ ] Write compliance tests

**Deliverables**:
- `HasOwnership` protocol definition
- Protocol compliance tests

### Phase 3: Ownership Determination
**Objective**: Implement rules for determining ownership category

**Tasks**:
- [ ] Create `OwnershipResolver` class
- [ ] Implement rules for automatic category determination:
  - If created by Piper → NATIVE
  - If fetched from integration → FEDERATED
  - If derived/computed → SYNTHETIC
- [ ] Handle edge cases (cached federated data, etc.)
- [ ] Write tests for determination logic

**Deliverables**:
- `OwnershipResolver` with determination rules
- Unit tests for each determination path

### Phase 4: Transformation Tracking
**Objective**: Track when objects transform between categories

**Tasks**:
- [ ] Define valid transformations:
  - FEDERATED → SYNTHETIC (observation becomes understanding)
  - SYNTHETIC → NATIVE (understanding becomes memory)
  - NATIVE → FEDERATED (publishing internal state)
- [ ] Create `OwnershipTransformation` record type
- [ ] Implement transformation logging
- [ ] Write tests for transformation tracking

**Deliverables**:
- Transformation definitions and logging
- Transformation tests

### Phase 5: Model Mapping Documentation
**Objective**: Document how existing models map to ownership categories

**Tasks**:
- [ ] Review `services/domain/models.py`
- [ ] Create mapping table for all major models
- [ ] Document any ambiguous cases
- [ ] Add mapping to ADR-055

**Deliverables**:
- Model-to-ownership mapping table in ADR-055 appendix

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] All tests passing
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] Session log completed
- [ ] **Experience Checkpoint**: One paragraph on how ownership model honors the grammar

---

## Acceptance Criteria

### Functionality
- [ ] `OwnershipCategory` enum defined with NATIVE, FEDERATED, SYNTHETIC
- [ ] `HasOwnership` protocol defined and `@runtime_checkable`
- [ ] Objects can be checked with `isinstance(obj, HasOwnership)`
- [ ] `OwnershipResolver` correctly categorizes test cases
- [ ] Transformation rules defined and logged
- [ ] Model mapping table complete

### Testing
- [ ] Unit tests for `OwnershipCategory` enum
- [ ] Unit tests for `HasOwnership` protocol compliance
- [ ] Unit tests for `OwnershipResolver` determination rules
- [ ] Unit tests for transformation tracking
- [ ] Integration test: Demonstrate ownership across a user flow

### Quality
- [ ] No regressions in existing functionality
- [ ] Type hints throughout
- [ ] Docstrings with examples and metaphors
- [ ] Follows existing code patterns in services/

### Documentation
- [ ] ADR-055 appendix with model mapping
- [ ] Code documentation complete
- [ ] Experience checkpoint written
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| OwnershipCategory enum | ❌ | |
| HasOwnership protocol | ❌ | |
| OwnershipResolver | ❌ | |
| Transformation tracking | ❌ | |
| Model mapping table | ❌ | |
| Experience checkpoint | ❌ | |

---

## Testing Strategy

### Unit Tests
```python
# Enum tests
def test_ownership_category_values():
    """Test that all three categories exist"""

def test_ownership_category_descriptions():
    """Test that categories have meaningful descriptions"""

# Protocol tests
def test_has_ownership_protocol_compliance():
    """Test that a class can satisfy HasOwnership"""

# Resolver tests
def test_native_ownership_determination():
    """Test that Piper-created objects are NATIVE"""

def test_federated_ownership_determination():
    """Test that integration-fetched objects are FEDERATED"""

def test_synthetic_ownership_determination():
    """Test that derived objects are SYNTHETIC"""

# Transformation tests
def test_federated_to_synthetic_transformation():
    """Test observation → understanding transformation"""
```

### Integration Tests
```python
async def test_ownership_in_user_flow():
    """
    Verify ownership tracking across a realistic flow:
    1. Fetch GitHub issues (FEDERATED)
    2. Compute project health (SYNTHETIC)
    3. Store insight as memory (NATIVE)
    """
```

### Manual Testing Checklist
**Scenario 1**: Ownership Assignment
1. [ ] Create a session → verify NATIVE
2. [ ] Fetch a GitHub issue → verify FEDERATED
3. [ ] Compute derived insight → verify SYNTHETIC

**Scenario 2**: Transformation
1. [ ] Start with federated calendar event
2. [ ] Derive scheduling insight
3. [ ] Verify transformation logged

---

## Success Metrics

### Quantitative
- 3 ownership categories defined
- 1 protocol definition
- 1 resolver implementation
- >20 tests passing
- 0 regressions

### Qualitative
- Code reads with metaphors ("Piper's Mind", "Piper's Senses", "Piper's Understanding")
- Ownership distinctions feel natural, not forced
- Mapping table clarifies, not confuses

---

## STOP Conditions

**STOP immediately and escalate if**:
- Ownership categories don't map cleanly to existing models
- Transformation rules create circular dependencies
- Protocol pattern conflicts with P1 implementation
- Performance concerns with runtime checking
- Existing code assumes uniform object treatment in incompatible way

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (Definitions): 1 hour
- Phase 2 (Protocol): 1 hour
- Phase 3 (Resolver): 1 hour
- Phase 4 (Transformation): 0.5 hours
- Phase 5 (Documentation): 0.5 hours
- Testing: Included in each phase

**Total**: 4 hours

**Complexity Notes**:
- Conceptually clear but needs careful edge case handling
- Model mapping may reveal inconsistencies requiring discussion

---

## Dependencies

### Required (Must be complete first)
- [ ] #[P1-issue-number] - Core Grammar & Lens Infrastructure (Protocols defined)

### Optional (Nice to have)
- P0 investigation findings for reference

---

## Related Documentation

- **Architecture**: ADR-045 (ownership concepts), ADR-055 (implementation)
- **Methodology**: TDD, DDD
- **Strategic**: CXO design principles (Native/Federated/Synthetic definitions)
- **Memos**: CXO design principles one-pager

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

**From CXO Design Principles Memo**:
- Native = "Piper's Mind" (sessions, memories, trust states)
- Federated = "Piper's Senses" (GitHub issues, Slack messages, calendar events)
- Synthetic = "Piper's Understanding" (inferred project status, assembled risk picture)

**From Chief Architect Memo**:
- Ownership should compose with Protocols (an Entity can have ownership)
- Consider transformation as journey, not category reassignment

**Experience Framing**:
- NATIVE: "I know this because I created it"
- FEDERATED: "I see this in [Place]"
- SYNTHETIC: "I understand this to mean..."

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_

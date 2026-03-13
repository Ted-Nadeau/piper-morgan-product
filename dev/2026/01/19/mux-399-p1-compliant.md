# MUX-399-P1 - Core Grammar Implementation & Lens Infrastructure

**Priority**: P1
**Labels**: `MUX`, `architecture`, `foundation`, `DDD`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-038, #[P0-issue-number]

---

## Problem Statement

### Current State
ADR-045 defined the grammar "Entities experience Moments in Places" conceptually, but no implementation exists:
- No Protocol definitions for Entity, Moment, Place
- No Situation context manager
- No Lens infrastructure (8D dimensions exist only as methods within integration classes)
- No unified way to perceive through lenses

### Impact
- **Blocks**: All subsequent MUX phases (P2-P4, PZ) depend on these core abstractions
- **User Impact**: Without this, features remain disconnected rather than expressing coherent grammar
- **Technical Debt**: Continuing to build without foundational grammar perpetuates "flattening"

### Strategic Context
This is the cathedral foundation. Every future feature will express this grammar. Time Lord philosophy: take the time it needs to be right.

---

## Goal

**Primary Objective**: Implement the core grammar with Protocol definitions, Situation context manager, and Lens infrastructure.

**Example User Experience**:
```
Before: Code describes "fetching 3 calendar events"
After: Code describes "Piper perceiving Moments in Calendar Place through Temporal lens"
```

**Not In Scope** (explicitly):
- ❌ Ownership model (P2)
- ❌ Lifecycle state machine (P3)
- ❌ Metadata schema (P4)
- ❌ Canonical query tagging (P4.5)
- ❌ Refactoring existing features to use grammar (future work)

---

## What Already Exists

### Infrastructure ✅
- ADR-045: Object Model conceptual framework
- ADR-038: Spatial Intelligence Patterns (3 patterns documented)
- `NotionSpatialIntelligence.dimensions` dict pattern (8 methods)
- Slack `spatial_*.py` granular pattern
- Per-integration spatial adapters in `services/integrations/spatial/`

### What's Missing ❌
- `EntityProtocol`, `MomentProtocol`, `PlaceProtocol` definitions
- `Situation` context manager
- `Lens` base class and 8 implementations
- `LensSet` for compound perception
- `Perception` result type
- ADR-055 (Implementation Specification)

---

## Requirements

### Phase 1: Protocol Definitions
**Objective**: Define the three substrate Protocols

**Tasks**:
- [ ] Create `services/mux/protocols.py` (or appropriate location per P0 findings)
- [ ] Define `EntityProtocol` with identity, agency, `experiences()` method
- [ ] Define `MomentProtocol` with theatrical unities, `captures()` method
- [ ] Define `PlaceProtocol` with atmosphere, modality, `contains()` method
- [ ] Use `@runtime_checkable` for grammatical role fluidity
- [ ] Write comprehensive tests for protocol compliance

**Deliverables**:
- Protocol definitions file
- Protocol tests file
- Documentation of how existing models could satisfy protocols

### Phase 2: Situation Context Manager
**Objective**: Implement Situation as frame (not substrate)

**Tasks**:
- [ ] Create `Situation` context manager
- [ ] Support dramatic tension description
- [ ] Capture moments during situation
- [ ] Extract learning on exit (goals vs outcomes delta)
- [ ] Write tests for context manager behavior

**Deliverables**:
- `services/mux/situation.py`
- Situation tests
- Usage examples in docstrings

### Phase 3: Lens Infrastructure
**Objective**: Create lens abstraction layer over spatial dimensions

**Tasks**:
- [ ] Define `PerceptionMode` enum (NOTICING, REMEMBERING, ANTICIPATING)
- [ ] Define `Perception` result type with experience framing
- [ ] Create `Lens` abstract base class
- [ ] Implement 8 lens classes (Temporal, Hierarchy, Priority, Collaborative, Flow, Quantitative, Causal, Contextual)
- [ ] Create `LensSet` for compound perception
- [ ] Each lens wraps/unifies existing dimension implementations
- [ ] Write tests for each lens and compound perception

**Deliverables**:
- `services/mux/lenses/` module with base and 8 implementations
- `services/mux/perception.py` for Perception type
- Lens tests (unit tests per lens + integration tests for LensSet)

### Phase 4: Visual Diagram
**Objective**: Create visual representation of the model

**Tasks**:
- [ ] Create mermaid diagram showing substrate relationships
- [ ] Show lens application flow
- [ ] Document in ADR-055

**Deliverables**:
- Mermaid diagram in ADR-055 or separate file

### Phase 5: ADR-055 Draft
**Objective**: Document implementation specification

**Tasks**:
- [ ] Create ADR-055 draft building on ADR-045
- [ ] Document all technical decisions made
- [ ] Include Protocol definitions
- [ ] Include Lens architecture
- [ ] Reference existing infrastructure being built upon

**Deliverables**:
- `dev/active/adr-055-object-model-implementation.md` (draft)

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] All tests passing
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] Session log completed
- [ ] **Experience Checkpoint**: One paragraph on how implementation honors the grammar

---

## Acceptance Criteria

### Functionality
- [ ] `EntityProtocol` defined and usable with `isinstance()` checks
- [ ] `MomentProtocol` defined and usable with `isinstance()` checks
- [ ] `PlaceProtocol` defined and usable with `isinstance()` checks
- [ ] Protocols support role fluidity (same object can satisfy multiple)
- [ ] `Situation` context manager works with `async with`
- [ ] Situation captures moments and extracts learning on exit
- [ ] All 8 lenses implemented with NOTICING mode working
- [ ] REMEMBERING and ANTICIPATING modes at least stubbed
- [ ] `LensSet` can apply multiple lenses for compound perception
- [ ] `Perception` objects have experience-framed observations (not raw data)

### Testing
- [ ] Unit tests for each Protocol (compliance tests)
- [ ] Unit tests for Situation context manager
- [ ] Unit tests for each of 8 Lenses
- [ ] Unit tests for LensSet compound perception
- [ ] Integration test: Express Morning Standup using new constructs

### Quality
- [ ] No regressions in existing spatial functionality
- [ ] Type hints throughout
- [ ] Docstrings with examples
- [ ] Follows existing code patterns in services/

### Documentation
- [ ] ADR-055 draft complete
- [ ] Code documentation complete
- [ ] Experience checkpoint written
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| EntityProtocol | ❌ | |
| MomentProtocol | ❌ | |
| PlaceProtocol | ❌ | |
| Situation context manager | ❌ | |
| Lens base class | ❌ | |
| TemporalLens | ❌ | |
| HierarchyLens | ❌ | |
| PriorityLens | ❌ | |
| CollaborativeLens | ❌ | |
| FlowLens | ❌ | |
| QuantitativeLens | ❌ | |
| CausalLens | ❌ | |
| ContextualLens | ❌ | |
| LensSet | ❌ | |
| Perception type | ❌ | |
| Visual diagram | ❌ | |
| ADR-055 draft | ❌ | |
| Experience checkpoint | ❌ | |

---

## Testing Strategy

### Unit Tests
```python
# Protocol tests
def test_entity_protocol_compliance():
    """Test that a class satisfies EntityProtocol"""

def test_role_fluidity():
    """Test that one object can satisfy multiple protocols"""

# Situation tests
async def test_situation_captures_moments():
    """Test moment capture during situation"""

async def test_situation_extracts_learning_on_exit():
    """Test learning extraction when situation closes"""

# Lens tests (for each lens)
def test_temporal_lens_noticing_mode():
    """Test temporal perception in noticing mode"""

def test_lens_set_compound_perception():
    """Test multiple lenses applied together"""
```

### Integration Tests
```python
async def test_morning_standup_expressible():
    """
    Verify Morning Standup can be expressed using grammar:
    - User (Entity) experiences Standup (Moment) in Calendar+GitHub (Places)
    - Perceived through Temporal, Priority, Collaborative lenses
    """
```

### Manual Testing Checklist
**Scenario 1**: Protocol Fluidity
1. [ ] Create a Project object
2. [ ] Verify it satisfies EntityProtocol when acting
3. [ ] Verify it satisfies PlaceProtocol when containing

**Scenario 2**: Compound Perception
1. [ ] Apply Temporal + Priority lenses to a set of items
2. [ ] Verify compound Perception has coherent observation

---

## Success Metrics

### Quantitative
- 3 Protocols defined
- 1 Situation context manager
- 8 Lens implementations
- 1 LensSet implementation
- \>50 tests passing
- 0 regressions

### Qualitative
- Code reads as grammar ("entity experiences moment in place")
- Perception observations sound conscious, not mechanical
- Existing Morning Standup patterns visible in new constructs

---

## STOP Conditions

**STOP immediately and escalate if**:
- P0 findings significantly change the approach
- Protocol pattern doesn't work for role fluidity
- Can't wrap existing spatial infrastructure cleanly
- Performance concerns with runtime_checkable
- Architectural conflict with existing patterns
- Any "flattening" detected (feeling like database design)

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Large

**Breakdown by Phase**:
- Phase 1 (Protocols): 2 hours
- Phase 2 (Situation): 2 hours
- Phase 3 (Lenses): 5-6 hours
- Phase 4 (Diagram): 0.5 hours
- Phase 5 (ADR-055): 1 hour
- Testing: Included in each phase
- Documentation: 0.5 hours

**Total**: 10-12 hours

**Complexity Notes**:
- Lens infrastructure is new creation, not wrapping (larger than initially assumed)
- Need to unify disparate integration patterns
- TDD approach adds time but ensures quality

---

## Dependencies

### Required (Must be complete first)
- [ ] #[P0-issue-number] - Investigation & Pattern Discovery

### Optional (Nice to have)
- Morning Standup as reference during implementation

---

## Related Documentation

- **Architecture**: ADR-045 (builds on), ADR-038 (spatial patterns), ADR-055 (creates)
- **Methodology**: TDD, DDD, Pattern-020
- **Strategic**: MUX super-epic, CXO design principles memo
- **Memos**: Chief Architect (Protocols over inheritance, wrap spatial dimensions)

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
- Use `@runtime_checkable` Protocols, not inheritance
- Lens wraps spatial dimension with consciousness framing
- `_frame_as_experience()` transforms data → experience language
- Situation is context manager (frame), not data model (substrate)

**From PPM Memo**:
- "Done" means conceptually sound, not just code committed
- Write "experience" paragraph at checkpoint
- If grammar feels forced, STOP and discuss

**TDD Approach**:
1. Write test for expected behavior
2. Implement to pass test
3. Verify experience framing (not just data correctness)

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_

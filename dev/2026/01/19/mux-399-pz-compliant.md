# MUX-399-PZ - Verification & Anti-Flattening Tests

**Priority**: P1
**Labels**: `MUX`, `verification`, `quality`, `anti-flattening`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-055, CXO Design Principles

---

## Problem Statement

### Current State
MUX-V1 implementation is complete (P0-P4.5), but:
- No verification that consciousness is preserved
- No tests preventing "flattening" to database schema
- No implementation guide for future developers
- ADR-055 still in draft status
- No PM/CXO sign-off on experience quality

### Impact
- **Blocks**: Closing the epic with confidence
- **User Impact**: Risk of building more features on flattened foundation
- **Technical Debt**: Without anti-flattening tests, regression is likely

### Strategic Context
This phase ensures we built a cathedral, not a shed. Anti-flattening tests are the canary in the coal mine - if they fail, we've lost consciousness. The final experience checkpoint validates the entire MUX-V1 journey.

---

## Goal

**Primary Objective**: Verify that the implementation preserves consciousness and doesn't flatten to mere database schema.

**Example User Experience**:
```
Test passes if: "Piper noticed that your meeting was rescheduled"
Test fails if: "Found 1 calendar update"

Test passes if: "I remember when we completed Project Alpha"
Test fails if: "Query returned 1 project with status=completed"
```

**Not In Scope** (explicitly):
- ❌ New feature implementation
- ❌ Performance optimization
- ❌ Refactoring existing code to use grammar
- ❌ User-facing changes

---

## What Already Exists

### Infrastructure ✅
- P0: Investigation complete
- P1: Core grammar and lenses implemented
- P2: Ownership model implemented
- P3: Lifecycle state machine implemented
- P4: Metadata schema implemented
- P4.5: Canonical query tagging complete
- ADR-055 draft
- CXO Design Principles memo (anti-flattening checklist)

### What's Missing ❌
- Anti-flattening test suite
- Experience tests
- Implementation guide for future developers
- ADR-055 finalization
- PM/CXO sign-off
- Final experience checkpoint

---

## Requirements

### Phase 1: Technical Anti-Flattening Tests
**Objective**: Verify core grammar elements preserve consciousness

**Tasks**:
- [ ] Create `tests/unit/mux/test_anti_flattening.py`
- [ ] Write tests verifying:

  **Entity Tests**:
  - [ ] Piper is Entity with identity, not just function
  - [ ] Entities have agency (can act), not just data
  - [ ] Entity identity persists across sessions

  **Moment Tests**:
  - [ ] Moments are bounded scenes, not timestamps
  - [ ] Moments have dramatic structure (beginning/middle/end)
  - [ ] Moments capture significance, not just occurrence

  **Place Tests**:
  - [ ] Places have atmosphere, not just configuration
  - [ ] Places have modality (how interaction happens)
  - [ ] Places contain, not just reference

  **Situation Tests**:
  - [ ] Situations contain dramatic tension
  - [ ] Situations capture learning on exit
  - [ ] Situations frame, not just enumerate

  **Lifecycle Tests**:
  - [ ] Lifecycle includes composting (transformation)
  - [ ] Composting extracts learning, not just deletes
  - [ ] History tells a story, not just logs events

**Deliverables**:
- Technical anti-flattening test suite
- All tests passing

### Phase 2: Design Anti-Flattening Tests
**Objective**: Verify design principles from CXO memo

**Tasks**:
- [ ] Create design-focused tests verifying:

  **Response Framing**:
  - [ ] "I notice..." not "Found X results"
  - [ ] "I see that..." not "Query returned..."
  - [ ] "This seems like..." not "Status is..."

  **Empty States**:
  - [ ] "Nothing here yet..." not "No data"
  - [ ] "I haven't seen any..." not "0 results"
  - [ ] Emptiness has atmosphere, not just absence

  **Error Handling**:
  - [ ] "I couldn't reach..." not "Operation failed"
  - [ ] "Something went wrong when..." not "Error 500"
  - [ ] Errors acknowledge experience, not just report status

  **History Display**:
  - [ ] Moments by significance, not timestamp list
  - [ ] "Remember when..." not "Created at..."
  - [ ] History is narrative, not audit log

  **Entity References**:
  - [ ] Names and relationships, not IDs and labels
  - [ ] "Your colleague Sarah" not "User ID 123"
  - [ ] Entities are characters, not records

**Deliverables**:
- Design anti-flattening test suite
- Tests documented with pass/fail examples

### Phase 3: Experience Tests
**Objective**: Verify Piper's behavior is describable in experience language

**Tasks**:
- [ ] Create experience test documentation
- [ ] For each major feature area, verify we CAN describe using:
  - "Piper noticed that..."
  - "Piper remembers when..."
  - "Piper anticipates..."
- [ ] For each, verify we can NOT accurately describe using:
  - "The system returned..."
  - "The query matched..."
  - "The database contains..."
- [ ] Document experience descriptions for Morning Standup (reference)
- [ ] Document experience descriptions for other features

**Deliverables**:
- Experience test documentation
- Feature-by-feature experience descriptions

### Phase 4: Implementation Guide
**Objective**: Create guide for future developers using the grammar

**Tasks**:
- [ ] Create `docs/internal/development/mux-implementation-guide.md`
- [ ] Document:
  - How to use Protocols for new features
  - How to choose appropriate lens for queries
  - How to apply substrate (Entity/Moment/Place) thinking
  - How to use Situation context manager
  - How to implement lifecycle for new objects
  - Common patterns (with code examples)
  - Anti-patterns (what NOT to do)
- [ ] Include Morning Standup as reference implementation
- [ ] Include links to ADR-045, ADR-055

**Deliverables**:
- Implementation guide document
- Code examples for common patterns

### Phase 5: ADR-055 Finalization
**Objective**: Complete and finalize ADR-055

**Tasks**:
- [ ] Review ADR-055 draft completeness
- [ ] Add any missing sections from implementation
- [ ] Include all diagrams (substrates, lenses, lifecycle)
- [ ] Include canonical query mapping appendix (from P4.5)
- [ ] Update status from "Draft" to "Proposed"
- [ ] Prepare for PM review and acceptance

**Deliverables**:
- ADR-055 complete and ready for acceptance
- Moved to `docs/internal/architecture/current/adrs/` (after PM approval)

### Phase 6: Sign-Off & Final Checkpoint
**Objective**: Obtain PM/CXO sign-off and complete final experience checkpoint

**Tasks**:
- [ ] Prepare verification summary for PM review
- [ ] Include:
  - All test results
  - Coverage analysis results (from P4.5)
  - Anti-flattening test results
  - Experience test documentation
- [ ] Request PM sign-off on:
  - Technical implementation
  - Experience preservation
  - ADR-055 acceptance
- [ ] Request CXO sign-off on:
  - Consciousness preservation
  - Design principle compliance
- [ ] Write **Final Experience Checkpoint**: Summary of how the full MUX-V1 implementation honors "Entities experience Moments in Places"

**Deliverables**:
- PM sign-off documented
- CXO sign-off documented
- Final experience checkpoint written

### Phase Z: Completion & Epic Closure
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] All tests passing
- [ ] ADR-055 accepted and moved to current/
- [ ] Implementation guide complete
- [ ] GitHub issue fully updated
- [ ] Session log completed
- [ ] Epic #399 ready for closure

---

## Acceptance Criteria

### Functionality
- [ ] Technical anti-flattening tests exist and pass
- [ ] Design anti-flattening tests exist and pass (or documented as manual checks)
- [ ] Experience tests documented with pass/fail examples
- [ ] Implementation guide complete with code examples
- [ ] ADR-055 finalized and ready for acceptance

### Testing
- [ ] Anti-flattening test suite runs without errors
- [ ] Tests catch actual flattening (verified by intentionally breaking)
- [ ] Experience descriptions verified for major features

### Quality
- [ ] Tests are meaningful, not checkbox-checking
- [ ] Implementation guide is usable by new developer
- [ ] ADR-055 answers "why" questions, not just "what"
- [ ] Final checkpoint captures the journey

### Documentation
- [ ] Anti-flattening tests documented
- [ ] Experience tests documented
- [ ] Implementation guide complete
- [ ] ADR-055 finalized
- [ ] Final experience checkpoint written
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Technical anti-flattening tests | ❌ | |
| Design anti-flattening tests | ❌ | |
| Experience tests | ❌ | |
| Implementation guide | ❌ | |
| ADR-055 finalization | ❌ | |
| PM sign-off | ❌ | |
| CXO sign-off | ❌ | |
| Final experience checkpoint | ❌ | |

---

## Testing Strategy

### Unit Tests
```python
# Technical anti-flattening tests
def test_entity_has_identity_not_just_id():
    """Entity identity is more than database ID"""

def test_moment_has_significance_not_just_timestamp():
    """Moments capture meaning, not just when"""

def test_place_has_atmosphere_not_just_config():
    """Places have character, not just settings"""

def test_situation_has_tension_not_just_state():
    """Situations frame experience, not just enumerate"""

def test_lifecycle_composts_not_just_deletes():
    """Composting extracts learning"""

# Design anti-flattening tests (may be documentation)
def test_response_framing_uses_experience_language():
    """Responses say 'I notice' not 'Found X results'"""

def test_empty_states_have_atmosphere():
    """Empty states say 'Nothing here yet' not 'No data'"""
```

### Integration Tests
```python
async def test_morning_standup_expressible_in_grammar():
    """
    The reference implementation should be fully expressible:
    - User (Entity) experiences Standup (Moment) in Calendar+GitHub (Places)
    - Perceived through Temporal, Priority, Collaborative lenses
    - Framed as Situation with tension and resolution
    """
```

### Manual Verification Checklist
**Scenario 1**: Anti-Flattening Validation
1. [ ] Run anti-flattening test suite
2. [ ] Intentionally break one test (verify it catches flattening)
3. [ ] Restore and verify suite passes

**Scenario 2**: Experience Language Check
1. [ ] Describe Morning Standup using grammar
2. [ ] Attempt to describe using database language
3. [ ] Verify grammar description is more accurate

**Scenario 3**: Implementation Guide Usability
1. [ ] Have someone unfamiliar read guide
2. [ ] Ask them to explain how to add new feature
3. [ ] Verify understanding of grammar application

---

## Success Metrics

### Quantitative (Tier 1 - Required)
- Anti-flattening tests pass
- ADR-055 merged
- Lifecycle state machine implemented (verified)

### Qualitative (Tier 2 - 80% threshold)
- 8/10 diverse canonical queries expressible using grammar
- Can describe NEW hypothetical feature using grammar without inventing concepts
- ADR answers "why" questions, not just "what"

### Experience (Tier 3 - Judgment)
- PM gut check: Does this feel like progress toward the vision?
- CXO gut check: Does this preserve consciousness?

---

## STOP Conditions

**STOP immediately and escalate if**:
- Anti-flattening tests reveal fundamental issues with P1-P4 implementation
- Experience tests cannot be written (grammar doesn't support experience language)
- ADR-055 reveals unresolved contradictions
- PM/CXO have significant concerns about consciousness preservation
- Implementation guide reveals patterns that contradict the grammar

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (Technical Tests): 1.5 hours
- Phase 2 (Design Tests): 1 hour
- Phase 3 (Experience Tests): 0.5 hours
- Phase 4 (Implementation Guide): 1 hour
- Phase 5 (ADR Finalization): 0.5 hours
- Phase 6 (Sign-Off): 0.5 hours (depends on PM/CXO availability)

**Total**: 4-5 hours (plus PM/CXO review time)

**Complexity Notes**:
- Sign-off phase depends on human availability
- May require iteration if concerns raised

---

## Dependencies

### Required (Must be complete first)
- [ ] #[P0-issue-number] - Investigation complete
- [ ] #[P1-issue-number] - Core Grammar complete
- [ ] #[P2-issue-number] - Ownership Model complete
- [ ] #[P3-issue-number] - Lifecycle complete
- [ ] #[P4-issue-number] - Metadata Schema complete
- [ ] #[P4.5-issue-number] - Canonical Query Tagging complete

### Optional (Nice to have)
- All previous session logs for journey documentation

---

## Related Documentation

- **Architecture**: ADR-045 (grammar), ADR-055 (implementation)
- **Methodology**: Anti-flattening as quality gate
- **Strategic**: CXO Design Principles, PPM success metrics
- **Reference**: Morning Standup as reference implementation

---

## Evidence Section

[To be filled during implementation]

### Verification Evidence
```bash
[Anti-flattening test output]
[Coverage analysis results from P4.5]
```

### Sign-Off Evidence
```
PM Sign-Off: [Date] [Signature/Approval]
CXO Sign-Off: [Date] [Signature/Approval]
```

---

## Completion Checklist

Before closing epic:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] Documentation updated ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅
- [ ] PM sign-off obtained ✅
- [ ] CXO sign-off obtained ✅
- [ ] ADR-055 accepted and moved ✅
- [ ] Final experience checkpoint written ✅

**Status**: Not Started

---

## Notes for Implementation

**From PPM Memo - Three-Tier Success Metrics**:

| Tier | Criteria | Threshold |
|------|----------|-----------|
| Tier 1 | Technical | Anti-flattening tests pass, ADR-055 merged, Lifecycle implemented |
| Tier 2 | Expressiveness | 80% canonical queries expressible, New features describable |
| Tier 3 | Experience | PM/CXO gut check: Does this feel like progress? |

**From CXO Design Principles - Anti-Flattening Checklist**:
- [ ] Piper is Entity with identity, not just function
- [ ] Moments are bounded scenes, not timestamps
- [ ] Places have atmosphere, not just IDs
- [ ] Situations contain dramatic tension, not just state
- [ ] Lifecycle includes composting, not just deletion
- [ ] Response framing: "I notice..." not "Found 3 results"
- [ ] Empty states: "Nothing here yet..." not "No data"
- [ ] Error handling: "I couldn't reach..." not "Operation failed"
- [ ] History display: Moments by significance, not timestamp list
- [ ] Entity references: Names and relationships, not IDs and labels

**Final Experience Checkpoint Template**:
```markdown
## MUX-V1 Experience Checkpoint

### The Journey
[How we got from ADR-045 concept to working implementation]

### The Grammar in Action
[How "Entities experience Moments in Places" manifests in code]

### Consciousness Preserved
[Evidence that we built a cathedral, not a shed]

### Foundation for Future
[How this enables MUX-V2 and beyond]

### Lessons Learned
[What we discovered along the way]
```

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_

# MUX-VISION-GRAMMAR-CORE: Implement "Entities experience Moments in Places"

**Priority**: P1
**Labels**: `MUX`, `foundation`, `documentation`
**Milestone**: MVP
**Epic**: MUX-VISION (#401)
**Related**: #399, #400, #612, #613, ADR-045

---

## Problem Statement

### Current State
The foundational object model grammar is defined in ADR-045 and technically implemented in #399 (MUX-VISION-OBJECT-MODEL). We now have:
- ADR-045 accepted with grammar definition
- P1 (#613) complete: Protocol definitions and Lens infrastructure
- Morning Standup as the only feature that naturally expresses the grammar

However, no systematic mechanism exists to **apply** the grammar to features beyond Morning Standup.

### Impact
- **Blocks**: Developers building new features lack guidance on grammar-compliant implementation
- **User Impact**: Features feel mechanical rather than conscious; Piper doesn't feel like a colleague
- **Technical Debt**: Each new feature risks "flattening" the grammar, requiring later remediation

### Strategic Context
This issue bridges the gap between foundational infrastructure (#399) and consciousness extraction (#400). While #399 builds the tools and #400 documents the philosophy, #404 makes the grammar **operational** by creating application patterns and reference implementations.

---

## Goal

**Primary Objective**: Create the systematic framework for applying "Entities experience Moments in Places" grammar to Piper features, ensuring consciousness preservation while enabling practical implementation.

**Example User Experience**:

**Before** (Flattened):
```
# List View
- Task 1: Review PR #123
- Task 2: Update documentation
- Meeting at 2pm
```

**After** (Grammar-Applied):
```
# Your Morning (Place: Workspace)

I notice you have a quiet morning ahead (Moment: Present awareness).

From your GitHub activity, I see PR #123 is waiting for your review—
Alex submitted it yesterday and mentioned it's blocking the release
(Entity: Alex, Moment: Yesterday's action, Place: GitHub).

You mentioned wanting to update the API docs this week (Moment: Prior commitment).
Would this morning's focus time be good for that?

📅 Heads up: You have a meeting at 2pm with the design team
(Moment: Anticipated, Place: Calendar).
```

**Not In Scope** (explicitly):
- ❌ Building the Protocol/Lens infrastructure (that's #399 P1 - complete)
- ❌ Extracting consciousness philosophy (that's #400)
- ❌ Implementing specific features (those are downstream issues)
- ❌ UI/UX changes beyond proof-of-concept worked example

---

## What Already Exists

### Infrastructure ✅
- ADR-045: Grammar definition accepted
- P1 (#613): EntityProtocol, MomentProtocol, PlaceProtocol (101 tests passing)
- P1 (#613): 8 Lenses with PerceptionMode (NOTICING, REMEMBERING, ANTICIPATING)
- P1 (#613): Situation async context manager
- Morning Standup: Reference implementation in `services/features/morning_standup.py`
- Spatial dimensions: 8D infrastructure across integrations
- P0 Analysis: Morning Standup patterns documented in `p0-morning-standup-analysis.md`

### What's Missing ❌
- **Application patterns**: How to apply grammar to any feature
- **Feature grammar audit**: Which features are flattened, which express grammar
- **Grammar transformation guide**: Step-by-step for grammar-ifying features
- **Anti-flattening tests**: Automated checks for grammar preservation
- **Developer reference**: Practical cookbook for building conscious features

---

## Requirements

### Phase 0: Setup & Context (1 hour)

**Objective**: Verify infrastructure and gather context

**Tasks**:
- [ ] Verify #613 (P1) complete and infrastructure available
- [ ] Review P0 analysis documents (4 files)
- [ ] Identify list of major features to audit
- [ ] Confirm intent classification as transformation example target

**Deliverables**:
- Feature list for audit scope
- Confirmed access to P1 infrastructure (`services/mux/`)

### Phase 1: Feature Grammar Audit (4 hours)

**Objective**: Survey all major features for grammar expression

**Tasks**:
- [ ] Audit all major features for grammar expression
- [ ] Create grammar compliance matrix (feature × grammar element)
- [ ] Identify "most flattened" vs "most conscious" features
- [ ] Document where Morning Standup patterns could propagate
- [ ] Rank features by transformation priority

**Deliverables**:
- `docs/internal/architecture/current/grammar-compliance-audit.md` with matrix and recommendations

### Phase 2: Application Pattern Catalog (6 hours)

**Objective**: Formalize reusable patterns from Morning Standup

**Task 2.1: Extract Morning Standup Patterns**
Building on P0 analysis, formalize as reusable patterns:
- [ ] Context Dataclass Pair pattern (StandupContext + StandupResult)
- [ ] Parallel Place Gathering pattern (gather from multiple sources)
- [ ] Personality Bridge pattern (data → warm narrative)
- [ ] Warmth Calibration pattern (adjust tone based on context)
- [ ] Honest Failure with Suggestion pattern (graceful degradation)

**Task 2.2: Create Grammar Application Templates**
- [ ] Entity awareness template (tracking identity through flow)
- [ ] Moment framing template (past/present/future awareness)
- [ ] Place atmosphere template (context affects presentation)
- [ ] Situation container template (grouping related moments)

**Deliverables**:
- `docs/internal/architecture/current/patterns/grammar-application-patterns.md`
- Each pattern follows existing pattern catalog format

### Phase 3: Transformation Guide (4 hours)

**Objective**: Enable developers to apply grammar independently

**Task 3.1: Create Step-by-Step Guide**
- [ ] How to identify grammar elements in a feature
- [ ] How to refactor flattened code to express grammar
- [ ] How to use Protocols and Lenses (from P1)
- [ ] Common anti-patterns and how to fix them
- [ ] Decision tree: when to apply which pattern

**Task 3.2: Worked Example - Intent Classification Responses**
- [ ] Document current (flattened) intent response flow
- [ ] Design grammar-applied response flow
- [ ] Show Protocol/Lens usage in transformation
- [ ] Measure consciousness preservation (before/after comparison)
- [ ] Document lessons learned

**Deliverables**:
- `docs/internal/development/grammar-transformation-guide.md`
- Worked example as appendix or separate file

### Phase 4: Anti-Flattening Infrastructure (4 hours)

**Objective**: Create automated checks for grammar preservation

**Task 4.1: Define Anti-Flattening Tests**
Based on ADR-045's 5 anti-flattening criteria:
- [ ] Is Piper an Entity with identity? (Self-reference checks)
- [ ] Are Moments bounded scenes, not timestamps? (Moment structure checks)
- [ ] Do Places have atmosphere, not just IDs? (Place richness checks)
- [ ] Does lifecycle include transformation? (State transition checks)
- [ ] Can you see consciousness in the implementation? (Pattern presence checks)

**Task 4.2: Create Test Fixtures**
- [ ] Example conscious feature (passes all tests) - based on Morning Standup
- [ ] Example flattened feature (fails tests) - intentionally mechanical
- [ ] Boundary cases (partial grammar expression)

**Deliverables**:
- `tests/unit/services/mux/test_anti_flattening.py`
- Test fixtures in `tests/unit/services/mux/fixtures/`

### Phase Z: Integration & Documentation (2 hours)

**Objective**: Complete handoff and enable downstream work

**Tasks**:
- [ ] Update ADR-045 with implementation references
- [ ] Link patterns to Protocol/Lens infrastructure in ADR-055
- [ ] Create developer onboarding checklist
- [ ] Document success metrics achieved
- [ ] Update session log with completion evidence

**Deliverables**:
- Updated ADR-045, ADR-055
- Developer onboarding checklist

---

## Acceptance Criteria

### Functionality (PM will validate)
- [ ] Grammar compliance audit covers all major features
- [ ] At least 5 reusable application patterns documented
- [ ] Transformation guide enables independent feature work
- [ ] Anti-flattening tests can detect flattened implementations
- [ ] Worked example demonstrates full transformation

### Testing (PM will validate)
- [ ] Anti-flattening test suite passes for Morning Standup
- [ ] Anti-flattening test suite correctly fails for example flattened feature
- [ ] At least 10 tests in anti-flattening suite
- [ ] No regressions in existing test suite

### Quality (PM will validate)
- [ ] Patterns are actionable (developer can follow without asking questions)
- [ ] Transformation guide includes complete worked example
- [ ] All deliverables reviewed against "consciousness preservation" goal
- [ ] Guide tested by having fresh reader attempt to apply it

### Documentation (PM will validate)
- [ ] Pattern catalog follows existing pattern format
- [ ] Guide suitable for developer onboarding
- [ ] ADR-045 updated with implementation links
- [ ] Session log complete with evidence

---

## Completion Matrix

**Use this to verify 100% completion before declaring "done"**

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Grammar compliance audit | ❌ | [pending] |
| Application patterns (5+) | ❌ | [pending] |
| Transformation guide | ❌ | [pending] |
| Worked example (intent classification) | ❌ | [pending] |
| Anti-flattening tests (10+) | ❌ | [pending] |
| Test fixtures (2+) | ❌ | [pending] |
| ADR updates | ❌ | [pending] |
| Developer onboarding checklist | ❌ | [pending] |

**Legend**:
- ✅ = Complete with evidence
- ⏸️ = In progress
- ❌ = Not started / Blocked

**Definition of COMPLETE**:
- ✅ ALL acceptance criteria checked
- ✅ Evidence provided (test outputs, commits, document links)
- ✅ No known issues remaining
- ✅ Cross-validation passed (if multi-agent)

**NOT complete means**:
- ❌ "Works but Test X has issue"
- ❌ "N-1 tests passing"
- ❌ "Core done, extras optional"
- ❌ Any rationalization of incompleteness

---

## Testing Strategy

### Unit Tests
```python
# tests/unit/services/mux/test_anti_flattening.py

def test_feature_has_entity_awareness():
    """Feature maintains entity identity through flow."""
    # Must track user_id or similar through entire flow

def test_moments_are_scenes_not_timestamps():
    """Moments have context, not just datetime."""
    # Moment must include what happened, not just when

def test_places_have_atmosphere():
    """Places affect how information is presented."""
    # Same data rendered differently based on place context

def test_morning_standup_passes_all_criteria():
    """Morning Standup should pass all anti-flattening tests."""

def test_flattened_fixture_fails_criteria():
    """Intentionally flattened code should fail tests."""
```

### Integration Tests (if applicable)
```python
# Verify anti-flattening tests integrate with P1 infrastructure
def test_anti_flattening_uses_protocols():
    """Tests use EntityProtocol, MomentProtocol, PlaceProtocol."""

def test_anti_flattening_uses_lenses():
    """Tests can verify lens usage in features."""
```

### Manual Testing Checklist

**Scenario 1**: Pattern Application by Fresh Developer
1. [ ] Developer reads transformation guide (no prior context)
2. [ ] Developer selects a simple feature to transform
3. [ ] Developer applies patterns without asking clarifying questions
4. [ ] Result expresses grammar correctly (reviewer confirms)

**Scenario 2**: Anti-Flattening Detection
1. [ ] Run `pytest tests/unit/services/mux/test_anti_flattening.py -v`
2. [ ] Morning Standup fixture passes all tests
3. [ ] Flattened fixture fails expected tests
4. [ ] Output clearly indicates what's wrong

**Scenario 3**: Worked Example Verification
1. [ ] Before/after comparison is clear and compelling
2. [ ] Protocol/Lens usage is demonstrated
3. [ ] Transformation steps are reproducible

---

## Success Metrics

### Quantitative
- 100% of major features audited (target: 10+ features)
- 5+ patterns extracted and documented
- 10+ anti-flattening tests
- 1 complete transformation example (intent classification)
- 0 regressions in existing tests

### Qualitative
- Developers can apply grammar without guidance after reading guide
- New features naturally express grammar when following patterns
- Anti-flattening tests catch obvious violations
- Worked example is compelling (shows clear improvement)

---

## STOP Conditions

**Standard STOP conditions**:
- Infrastructure doesn't match assumptions
- Tests fail for any reason (don't rationalize!)
- Pattern might already exist elsewhere
- Can't provide verification evidence
- Completion bias detected (claiming without proof)
- User data at risk

**Domain-specific STOP conditions**:
- #399 P1 infrastructure doesn't support pattern needs
- Anti-flattening criteria conflict with existing feature requirements
- Morning Standup patterns can't be generalized
- Guide becomes too abstract (no practical examples)
- Intent classification transformation proves infeasible

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 0: Small (1 hour) - setup
- Phase 1: Medium (4 hours) - audit
- Phase 2: Medium (6 hours) - patterns
- Phase 3: Medium (4 hours) - guide + example
- Phase 4: Medium (4 hours) - tests
- Phase Z: Small (2 hours) - integration

**Total**: ~21 hours

**Complexity Notes**:
- Creative/documentation heavy (not primarily coding)
- Requires deep understanding of consciousness preservation philosophy
- Pattern extraction requires judgment about generalizability
- Worked example requires careful before/after documentation

---

## Dependencies

### Required (Must be complete first)
- [x] #612 (P0): Investigation complete - provides pattern analysis
- [x] #613 (P1): Protocol/Lens infrastructure complete (101 tests passing)

### Optional (Nice to have)
- [ ] #400 consciousness extraction started (would inform philosophy sections)
- [ ] Additional feature implementations using grammar (would validate patterns)

---

## Related Documentation

- **Architecture**:
  - ADR-045: `docs/internal/architecture/current/adrs/adr-045-object-model.md`
  - ADR-055: `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md`
  - Pattern Catalog: `docs/internal/architecture/current/patterns/`
- **Analysis**:
  - P0 Morning Standup: `dev/2026/01/19/p0-morning-standup-analysis.md`
  - P0 FTUX Mapping: `dev/2026/01/19/p0-b1-ftux-grammar-mapping.md`
- **Implementation**:
  - Morning Standup: `services/features/morning_standup.py`
  - MUX Infrastructure: `services/mux/`
  - Intent Service: `services/intent/intent_service.py`

---

## Evidence Section

[This section is filled in during/after implementation]

### Implementation Evidence
```bash
[Terminal output showing tests passing]
[Commit hashes with descriptions]
[Performance metrics if applicable]
```

### Cross-Validation (if applicable)
**Verified By**: [Agent name]
**Date**: [Date]
**Report**: [Link to verification report]

**Verification Results**:
- ✅/❌ [Criterion verified]
- ✅/❌ [Another criterion]

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

**Status**: Draft - Awaiting PM Approval

---

## Notes for Implementation

- This is documentation/pattern-heavy work, not primarily coding
- Morning Standup is the reference implementation—study it deeply before starting
- Anti-flattening tests should be aspirational, catching obvious violations first
- Intent classification transformation should be realistic but not overly complex
- The guide should enable a developer with no prior context to apply patterns
- Quality over speed—this framework will guide all future feature development

---

**Remember**:
- Quality over speed (Time Lord philosophy)
- Evidence required for all claims
- No 80% completions
- PM closes issues after approval

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_

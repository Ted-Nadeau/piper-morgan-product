# MUX-399-P4.5 - Canonical Query Lens/Substrate Tagging

**Priority**: P1
**Labels**: `MUX`, `validation`, `grammar`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-045, ADR-055, Canonical Query Test Matrix

---

## Problem Statement

### Current State
The canonical query test matrix exists with 50+ queries, but:
- No mapping to the new lens/substrate grammar
- No validation that the grammar can express existing functionality
- No way to know if we've over-complicated or under-specified the model
- Grammar could be beautiful theory that doesn't work in practice

### Impact
- **Blocks**: Confidence that the grammar is practically useful
- **User Impact**: Risk of grammar that sounds nice but doesn't help
- **Technical Debt**: Could build on grammar that needs revision later

### Strategic Context
"If we can't express what we already do, we've over-complicated." This phase validates the grammar against real queries. 80% coverage (40/50 queries expressible) is the Tier 2 success threshold from PPM.

---

## Goal

**Primary Objective**: Map existing canonical queries to lenses and substrates, validating the grammar's expressiveness.

**Example User Experience**:
```
Query: "What's on my agenda today?"
Mapping: Temporal lens → Moment substrate (Calendar Place)
Feature: Morning Standup

Query: "Show me stale PRs"
Mapping: Flow lens + Temporal lens → Moment substrate (GitHub Place)
Feature: Backlog Review
```

**Not In Scope** (explicitly):
- ❌ Implementing new query handling based on mapping
- ❌ Changing existing canonical query behavior
- ❌ Automated lens/substrate selection
- ❌ Grammar revisions (only documenting gaps)

---

## What Already Exists

### Infrastructure ✅
- Canonical query test matrix (`docs/internal/testing/canonical-query-test-matrix-v2.md`)
- P1 Lens infrastructure (8 lenses defined)
- P1 Substrate protocols (Entity, Moment, Place)
- Morning Standup as reference implementation
- ADR-045 grammar definition

### What's Missing ❌
- Query-to-lens mapping table
- Query-to-substrate mapping table
- Coverage analysis
- Gap documentation
- ADR-055 appendix with mappings

---

## Requirements

### Phase 1: Query Inventory
**Objective**: Compile complete list of canonical queries

**Tasks**:
- [ ] Read canonical query test matrix
- [ ] Extract all 50+ query patterns
- [ ] Group by functional area (calendar, GitHub, todos, etc.)
- [ ] Identify any queries not in matrix but in actual use

**Deliverables**:
- Complete query inventory list
- Grouping by functional area

### Phase 2: Lens Mapping
**Objective**: Map each query to primary and secondary lenses

**Tasks**:
- [ ] For each query, identify primary lens:
  - Temporal: Time-based queries
  - Hierarchy: Structure/containment queries
  - Priority: Urgency/importance queries
  - Collaborative: People/team queries
  - Flow: Progress/state queries
  - Quantitative: Metrics/counts queries
  - Causal: Cause/effect queries
  - Contextual: Background/setting queries
- [ ] Identify secondary lenses where applicable
- [ ] Document rationale for each mapping
- [ ] Flag queries that don't map cleanly

**Deliverables**:
- Query-to-lens mapping table
- Rationale documentation
- Unclear mappings flagged

### Phase 3: Substrate Mapping
**Objective**: Map each query to primary substrate

**Tasks**:
- [ ] For each query, identify substrate:
  - Entity: About actors/agents
  - Moment: About bounded occurrences
  - Place: About contexts/locations
  - Situation: About frames combining multiple elements
- [ ] Identify Place type where applicable (Calendar, GitHub, Slack, Notion, etc.)
- [ ] Document rationale for each mapping
- [ ] Flag queries that don't map cleanly

**Deliverables**:
- Query-to-substrate mapping table
- Place type annotations
- Unclear mappings flagged

### Phase 4: Coverage Analysis
**Objective**: Calculate and document coverage metrics

**Tasks**:
- [ ] Count total queries analyzed
- [ ] Count queries that map cleanly (both lens and substrate)
- [ ] Count queries that map with caveats
- [ ] Count queries that don't map (gaps)
- [ ] Calculate coverage percentage
- [ ] Assess against 80% threshold (PPM Tier 2 requirement)

**Coverage Categories**:
- **Clean**: Maps directly to grammar without forcing
- **Caveat**: Maps but requires explanation/judgment
- **Gap**: Doesn't map - requires grammar concept that doesn't exist

**Deliverables**:
- Coverage statistics
- Assessment against 80% threshold
- List of gaps

### Phase 5: Gap Analysis & Recommendations
**Objective**: Document gaps and provide recommendations

**Tasks**:
- [ ] For each gap, analyze why grammar doesn't express it
- [ ] Categorize gaps:
  - Missing lens type?
  - Missing substrate type?
  - Grammar too restrictive?
  - Query actually ambiguous?
- [ ] Provide recommendations:
  - Grammar refinement suggestions (if needed)
  - Query clarification suggestions (if query is the issue)
  - "Leave as-is" with rationale
- [ ] Do NOT make changes - only document

**Deliverables**:
- Gap analysis document
- Recommendations (documented, not implemented)

### Phase 6: ADR-055 Appendix
**Objective**: Create appendix with full mapping table

**Tasks**:
- [ ] Create appendix section in ADR-055
- [ ] Include complete mapping table:
  | Query | Primary Lens | Secondary Lens(es) | Substrate | Place Type | Coverage | Notes |
- [ ] Include coverage statistics
- [ ] Include gap summary
- [ ] Include recommendations section

**Deliverables**:
- ADR-055 appendix complete

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] All documentation complete
- [ ] GitHub issue fully updated
- [ ] Session log completed
- [ ] **Experience Checkpoint**: One paragraph on how tagging validates the grammar

---

## Acceptance Criteria

### Functionality
- [ ] All 50+ canonical queries inventoried
- [ ] Each query mapped to primary lens (or flagged as gap)
- [ ] Each query mapped to substrate (or flagged as gap)
- [ ] Coverage percentage calculated
- [ ] Coverage meets or documented why below 80% threshold
- [ ] Gaps analyzed with recommendations

### Testing
- [ ] N/A - This is analysis/documentation, not implementation

### Quality
- [ ] Mappings are justified, not arbitrary
- [ ] Gaps are genuine (not forcing unmappable queries)
- [ ] Recommendations are actionable
- [ ] Analysis is reproducible (another person could verify)

### Documentation
- [ ] Complete mapping table in ADR-055 appendix
- [ ] Coverage statistics documented
- [ ] Gap analysis documented
- [ ] Experience checkpoint written
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Query inventory | ❌ | |
| Lens mapping table | ❌ | |
| Substrate mapping table | ❌ | |
| Coverage analysis | ❌ | |
| Gap analysis | ❌ | |
| ADR-055 appendix | ❌ | |
| Experience checkpoint | ❌ | |

---

## Testing Strategy

### Unit Tests
N/A - This is analysis/documentation work, not implementation.

### Integration Tests
N/A

### Manual Verification Checklist
**Scenario 1**: Mapping Verification
1. [ ] Select 10 random queries from mapping
2. [ ] Verify lens assignment makes sense
3. [ ] Verify substrate assignment makes sense
4. [ ] Verify rationale is documented

**Scenario 2**: Coverage Verification
1. [ ] Recount total queries
2. [ ] Recount clean mappings
3. [ ] Verify percentage calculation
4. [ ] Verify against 80% threshold assessment

**Scenario 3**: Gap Verification
1. [ ] For each gap, verify it's a genuine grammar limitation
2. [ ] Verify recommendations are actionable
3. [ ] Verify no "clean" mappings miscategorized as gaps

---

## Success Metrics

### Quantitative
- 50+ queries analyzed
- 80%+ coverage target (PPM Tier 2)
- All gaps documented with recommendations
- ADR-055 appendix complete

### Qualitative
- Mappings feel natural, not forced
- Gaps reveal genuine grammar limitations (not analysis errors)
- Recommendations are useful for future grammar evolution

---

## STOP Conditions

**STOP immediately and escalate if**:
- Coverage below 60% (grammar fundamentally broken)
- Major feature areas completely unmapped (e.g., all GitHub queries are gaps)
- Lens or substrate concepts appear fundamentally wrong
- Analysis reveals P1 implementation needs revision
- Significant scope creep into implementation territory

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (Query Inventory): 0.5 hours
- Phase 2 (Lens Mapping): 1 hour
- Phase 3 (Substrate Mapping): 0.5 hours
- Phase 4 (Coverage Analysis): 0.5 hours
- Phase 5 (Gap Analysis): 0.5 hours
- Phase 6 (ADR Appendix): 0.5 hours

**Total**: 3 hours

**Complexity Notes**:
- Mostly analytical work, not coding
- May require subjective judgment calls on ambiguous queries
- Coverage percentage is key deliverable

---

## Dependencies

### Required (Must be complete first)
- [ ] #[P1-issue-number] - Core Grammar & Lens Infrastructure (Lenses and Protocols defined)

### Optional (Nice to have)
- Canonical query test matrix up to date
- Access to actual query usage data (not just test matrix)

---

## Related Documentation

- **Architecture**: ADR-045 (grammar), ADR-055 (implementation)
- **Testing**: Canonical query test matrix v2
- **Methodology**: Validation through expressiveness
- **Strategic**: PPM memo (80% coverage = Tier 2 success)

---

## Evidence Section

[To be filled during implementation]

### Analysis Evidence
```
Query Inventory: X queries
Coverage: Y% (Z/X queries mapped cleanly)
Gaps: N queries not expressible

Top gap categories:
1. [category]: X queries
2. [category]: Y queries
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
- [ ] Documentation updated ✅
- [ ] No regressions confirmed ✅ (N/A - no code)
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅

**Status**: Not Started

---

## Notes for Implementation

**From PPM Memo**:
- 80% coverage (40/50 queries) is Tier 2 success threshold
- "If we can't express what we already do, we've over-complicated"
- This is validation, not implementation

**Mapping Table Format**:
| Query | Primary Lens | Secondary Lens(es) | Substrate | Place Type | Coverage | Notes |
|-------|-------------|-------------------|-----------|------------|----------|-------|
| "What's on my agenda today?" | Temporal | Contextual | Moment | Calendar | Clean | Morning standup reference |
| "Show me stale PRs" | Flow | Temporal, Priority | Moment | GitHub | Clean | Backlog review pattern |
| "What needs attention?" | Priority | Collaborative, Temporal | Situation | — | Caveat | Requires Situation frame |

**Coverage Categories**:
- **Clean**: Direct, obvious mapping
- **Caveat**: Maps with explanation/judgment needed
- **Gap**: Doesn't map without grammar changes

**Expected Lens Distribution** (rough):
- Temporal: ~30% of queries (time is central to PM work)
- Priority: ~20% (urgency/importance common)
- Flow: ~15% (progress tracking)
- Collaborative: ~15% (team coordination)
- Others: ~20% combined

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_

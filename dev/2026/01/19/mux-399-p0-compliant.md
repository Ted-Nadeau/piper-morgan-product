# MUX-399-P0 - Investigation & Pattern Discovery

**Priority**: P1
**Labels**: `MUX`, `investigation`, `foundation`
**Milestone**: MUX-V1
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Related**: ADR-038, ADR-045, ADR-050, Pattern-020

---

## Problem Statement

### Current State
The object model grammar "Entities experience Moments in Places" was discovered and documented in ADR-045 (November 2025), but implementation requires understanding:
1. How Morning Standup already embodies the grammar (reference implementation)
2. What spatial infrastructure exists vs what the memos assumed exists
3. How B1 FTUX specs implicitly use Entity/Moment/Place thinking
4. Connections between existing ADRs and the grammar

### Impact
- **Blocks**: All other MUX-399 phases depend on this investigation
- **User Impact**: None directly (this is foundational research)
- **Technical Debt**: Implementing without understanding risks "flattening" the model to mere database schema

### Strategic Context
MUX-V1 is the first phase of the MUX super-epic. This investigation ensures we build on solid understanding rather than assumptions. Cathedral Context: understanding what we're building before laying bricks.

---

## Goal

**Primary Objective**: Complete investigation that enables informed implementation of the object model grammar.

**Example User Experience**: N/A (internal investigation)

**Not In Scope** (explicitly):
- ❌ Writing any implementation code
- ❌ Creating new infrastructure
- ❌ Modifying existing code
- ❌ Making architectural decisions (only documenting findings)

---

## What Already Exists

### Infrastructure ✅
- ADR-045: Object Model (Accepted, Nov 2025)
- ADR-038: Spatial Intelligence Patterns
- ADR-050: Conversation-as-Graph Model
- Morning Standup implementation
- B1 FTUX specs in `docs/internal/design/specs/`
- Spatial implementations: `services/intelligence/spatial/`, `services/integrations/spatial/`

### What's Missing ❌
- Analysis of how Morning Standup embodies the grammar
- Audit of actual spatial infrastructure vs assumed infrastructure
- Mapping of B1 specs to Entity/Moment/Place concepts
- Clear documentation of what exists to build on

---

## Requirements

### Phase 1: Morning Standup Analysis
**Objective**: Extract consciousness patterns from the reference implementation

**Tasks**:
- [ ] Read Morning Standup implementation completely
- [ ] Document how it embodies "Entities experience Moments in Places"
- [ ] Identify what makes it feel "present" vs mechanical
- [ ] Extract patterns that should be replicated elsewhere

**Deliverables**:
- Morning Standup analysis document (1-2 pages)
- List of extractable consciousness patterns

### Phase 2: Spatial Infrastructure Audit
**Objective**: Document what actually exists vs what was assumed

**Tasks**:
- [ ] Audit `services/intelligence/spatial/` (Notion pattern)
- [ ] Audit `services/integrations/spatial/` (per-integration pattern)
- [ ] Audit `services/integrations/slack/spatial_*.py` (granular pattern)
- [ ] Document how 8D dimensions are currently implemented (methods, not classes)
- [ ] Identify common interfaces vs integration-specific implementations
- [ ] Compare actual infrastructure to `8d-spatial-to-lens-mapping.md` assumptions

**Deliverables**:
- Spatial infrastructure audit document with file paths and patterns
- Gap analysis: assumed vs actual

### Phase 3: B1 FTUX Spec Review
**Objective**: Document how existing specs implicitly use the grammar

**Tasks**:
- [ ] Review `empty-state-voice-guide-v1.md`
- [ ] Review cross-session greeting specs
- [ ] Review `contextual-hint-ux-spec-v1.md`
- [ ] Document Entity/Moment/Place thinking in each

**Deliverables**:
- B1 FTUX implicit grammar mapping table

### Phase 4: ADR Connection Mapping
**Objective**: Understand how existing ADRs connect to the object model

**Tasks**:
- [ ] Review ADR-038 (Spatial Intelligence)
- [ ] Review ADR-045 (Object Model original)
- [ ] Review ADR-050 (Conversation-as-Graph)
- [ ] Document connections, overlaps, and gaps

**Deliverables**:
- ADR connection map document

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] Investigation findings documented in session log
- [ ] GitHub issue fully updated
- [ ] Recommendations for P1 scope adjustments (if any)

---

## Acceptance Criteria

### Functionality
- [ ] Morning Standup analysis complete with consciousness pattern extraction
- [ ] Spatial infrastructure audit complete with accurate file paths
- [ ] B1 FTUX specs reviewed and mapped to grammar
- [ ] ADR connections documented

### Testing
- [ ] N/A - This is investigation, not implementation

### Quality
- [ ] All findings verified against actual code (not assumptions)
- [ ] No speculation - only documented observations
- [ ] Clear distinction between "exists" and "was assumed to exist"

### Documentation
- [ ] Investigation findings in session log
- [ ] Separate analysis documents for each area
- [ ] **Experience Checkpoint**: One paragraph explaining how this investigation honors "Entities experience Moments in Places"

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Morning Standup analysis | ❌ | |
| Spatial infrastructure audit | ❌ | |
| B1 FTUX spec review | ❌ | |
| ADR connection map | ❌ | |
| Experience checkpoint | ❌ | |

---

## Testing Strategy

### Unit Tests
N/A - Investigation phase, no code written

### Integration Tests
N/A

### Manual Testing Checklist
**Scenario 1**: Verify findings accuracy
1. [ ] Each file path in audit actually exists
2. [ ] Each pattern described matches actual code
3. [ ] Each ADR reference is accurate

---

## Success Metrics

### Quantitative
- 4 analysis documents produced
- 100% of referenced files verified to exist
- 0 assumptions carried forward unverified

### Qualitative
- Findings are actionable for P1 implementation
- No "we thought X existed but it doesn't" surprises in later phases

---

## STOP Conditions

**STOP immediately and escalate if**:
- Morning Standup implementation is significantly different than documented
- Core assumptions from memos are fundamentally wrong
- ADR-045 conflicts with implementation plans
- Scope of P1 needs significant revision based on findings

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (Standup analysis): 1.5 hours
- Phase 2 (Spatial audit): 1.5 hours
- Phase 3 (B1 FTUX review): 1 hour
- Phase 4 (ADR mapping): 0.5 hours
- Documentation: 0.5 hours

**Total**: 5 hours

**Complexity Notes**: Depends on codebase familiarity. May surface findings that require PM discussion.

---

## Dependencies

### Required (Must be complete first)
- None - this is the starting point

### Optional (Nice to have)
- Access to original hand sketches from Nov 27 discovery session

---

## Related Documentation

- **Architecture**: ADR-038, ADR-045, ADR-050
- **Methodology**: Pattern-020 (Spatial Metaphor Integration)
- **Strategic**: MUX super-epic planning docs
- **Memos**: PPM guidance, Chief Architect guidance, CXO design principles

---

## Evidence Section

[To be filled during implementation]

### Implementation Evidence
```bash
[Links to analysis documents]
[Session log entries]
```

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
- Morning Standup is the PRIMARY source material
- "When uncertain, ask 'how does standup do this?'"
- Take the full time - do not rush investigation

**From Chief Architect Memo**:
- Morning Standup already: perceives through lenses, experiences entities, has awareness of places, generates moments
- Extract patterns from what works before inventing new ones

**Cathedral Context**: This investigation is understanding the cathedral we're building before picking up any tools.

---

_Issue created: 2026-01-19_
_Last updated: 2026-01-19_

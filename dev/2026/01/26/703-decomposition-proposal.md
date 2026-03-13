# #703 Mini-Epic Decomposition Proposal

**Date**: 2026-01-26
**Author**: Lead Developer
**Status**: Proposal for PM Review

---

## Overview

Based on Serena-informed analysis of the actual codebase, #703 should be decomposed into a phased mini-epic with clear MVP cutoff.

### Key Finding

The feature-object-model-map.md was stale. Actual lifecycle wiring status:

| Model | Has lifecycle_state | to_dict() wired | UI Ready |
|-------|---------------------|-----------------|----------|
| WorkItem | ✅ Yes | ✅ Yes (#685) | Ready for integration |
| Feature | ✅ Yes | ❌ No | Needs to_dict() wiring |
| Insight | ❌ No | N/A | Needs model work |
| SurfaceableInsight | ❌ No | Has to_dict() | Needs lifecycle field |

---

## Proposed Issue Decomposition

### Issue 1: #703-A - Morning Standup Integration (MVP)

**Parent**: #703
**Priority**: P2 (MVP)
**Effort**: Small-Medium

**Scope**:
- Integrate lifecycle_indicator into standup.html
- WorkItem already has lifecycle_state wired to to_dict()
- Reference implementation - establishes pattern for other views

**Why First**:
- Morning Standup is the "Conscious" reference implementation
- Backend fully ready (WorkItem.to_dict() returns lifecycle_state)
- Lowest risk, highest readiness
- Establishes integration pattern

**Acceptance Criteria**:
- [ ] lifecycle_indicator.html included in standup.html
- [ ] JavaScript renders indicator when WorkItem has lifecycle_state
- [ ] Experience phrases display (not technical labels)
- [ ] Tests verify indicator rendering
- [ ] Integration pattern documented

---

### Issue 2: #703-B - Feature Model to_dict() Wiring (MVP)

**Parent**: #703
**Priority**: P2 (MVP)
**Effort**: Small

**Scope**:
- Wire Feature.to_dict() to include lifecycle_state (like WorkItem)
- Add tests for Feature serialization
- Enables Feature-based views for lifecycle display

**Why Second**:
- Feature already has lifecycle_state field
- Just needs to_dict() serialization (same pattern as WorkItem)
- Quick win that expands coverage

**Acceptance Criteria**:
- [ ] Feature.to_dict() includes lifecycle_state when present
- [ ] Unit tests verify serialization
- [ ] Follows WorkItem pattern exactly

---

### Issue 3: #703-C - Insight Model Lifecycle Wiring (Post-MVP)

**Parent**: #703
**Priority**: P3 (Post-MVP)
**Effort**: Medium

**Scope**:
- Add lifecycle_state to Insight model
- Add lifecycle_state to SurfaceableInsight model
- Wire to_dict() methods
- Update InsightJournal to handle lifecycle

**Why Later**:
- Requires model changes, not just UI work
- Insights are semantically "composted" - need to decide if they START as COMPOSTED or track their own journey
- More architectural consideration needed

**Open Questions**:
- Should Insight have lifecycle, or is "insight" itself the END of lifecycle (composting output)?
- If insights have lifecycle, what are valid states for an insight?

**Acceptance Criteria**:
- [ ] Design decision documented on insight lifecycle semantics
- [ ] Insight/SurfaceableInsight models updated
- [ ] to_dict() wiring complete
- [ ] Tests verify serialization

---

### Issue 4: #703-D - Insights Page Integration (Post-MVP)

**Parent**: #703
**Priority**: P3 (Post-MVP)
**Effort**: Small-Medium
**Blocked By**: #703-C

**Scope**:
- Integrate lifecycle_indicator into insights.html
- Depends on #703-C completing model work
- Similar pattern to Morning Standup integration

**Acceptance Criteria**:
- [ ] lifecycle_indicator.html included in insights.html
- [ ] JavaScript renders indicator when SurfaceableInsight has lifecycle_state
- [ ] Experience phrases display
- [ ] Tests verify indicator rendering

---

### Long Tail (Backlog - Future)

These should be documented but deferred beyond MVP:

| View | Model | Status | Priority |
|------|-------|--------|----------|
| Todos | (needs investigation) | Unknown model | Backlog |
| Projects | Project | No lifecycle yet | Backlog |
| Documents | Document | No lifecycle yet | Backlog |

---

## MVP Cutoff Recommendation

**MVP Includes**:
- ✅ #703-A: Morning Standup integration
- ✅ #703-B: Feature.to_dict() wiring

**Post-MVP**:
- ⏳ #703-C: Insight model lifecycle wiring
- ⏳ #703-D: Insights page integration
- ⏳ Long tail views

**Rationale**:
- Morning Standup + Feature wiring gives users visible lifecycle in at least one view
- Proves the integration pattern works
- Insight model work requires architectural decisions
- Long tail can be addressed incrementally

---

## Updated feature-object-model-map.md

Added "Lifecycle Model Wiring Status" section documenting actual state from Serena analysis. This section should be maintained as lifecycle wiring progresses.

---

## Questions for PM

1. Does this decomposition make sense?
2. Is the MVP cutoff appropriate (standup + Feature wiring)?
3. For #703-C: Should insights have their own lifecycle, or are they inherently "composted"?
4. Should we create these as child issues now, or keep #703 as the tracker and work phases within it?

---

*Proposal ready for PM review*

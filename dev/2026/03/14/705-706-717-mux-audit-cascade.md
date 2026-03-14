# Audit Cascade: MUX Issues #705, #706, #717 — Issue → Execution Gate

**Date**: 2026-03-14
**Auditor**: Lead Developer (Claude Code Opus)
**Template**: `.github/ISSUE_TEMPLATE/feature.md`

---

## Issue #705: MUX-LIFECYCLE-UI-B — Feature.to_dict() lifecycle wiring

### Audit Matrix: #705 against feature.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label | ✅ | `MUX-LIFECYCLE-UI-B: Feature.to_dict() lifecycle wiring` |
| Priority | ✅ | P2 |
| Labels | ✅ | `enhancement` |
| Milestone | ✅ | MVP |
| Problem Statement | ✅ | Clear: Feature model has lifecycle_state field but no to_dict() method |
| Impact | ✅ | Blocks Feature-based UI views from displaying lifecycle indicators |
| Strategic Context | ✅ | Follows WorkItem.to_dict() pattern from #685 |
| Goal | ✅ | Primary objective clearly stated |
| Not In Scope | ✅ | UI integration, lifecycle init, status sync excluded |
| What Already Exists | ✅ | Infrastructure and gaps documented |
| Requirements/Phases | ✅ | Phase 1 (impl), Phase 2 (testing), Phase Z (completion) |
| Acceptance Criteria | ✅ | Functionality, Testing, Quality, Documentation sections |
| Completion Matrix | ✅ | Present with 3 components |
| Testing Strategy | ✅ | Unit test code examples provided |
| Success Metrics | ❌ | Not present (Quantitative/Qualitative) |
| STOP Conditions | ✅ | Present |
| Effort Estimate | ✅ | Small, with breakdown |
| Dependencies | ✅ | #685 marked complete |
| Evidence Section | ✅ | Template present (unfilled) |
| Completion Checklist | ✅ | Present |

### Critical Finding: ALREADY IMPLEMENTED

**Feature.to_dict()** exists at `services/domain/models.py:224-244` with lifecycle wiring.
**5 tests** exist at `tests/unit/services/domain/test_feature_lifecycle.py` — ALL PASSING.

This issue was implemented but never closed. The issue body's completion matrix still shows ❌ for all items.

### Action Items

1. **Update issue**: Mark completion matrix items as ✅ with evidence
2. **Close issue**: With test output evidence (5/5 passing)
3. **No code work needed** — already complete

### Risk Assessment: NONE (already done)

---

## Issue #706: MUX-OBJECTS-VIEWS — Objects & Views Discovery Epic

### Audit Matrix: #706 against feature.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label | ✅ | `MUX-OBJECTS-VIEWS: Objects & Views Discovery Epic` |
| Priority | ✅ | P3 |
| Labels | ✅ | `enhancement`, `architecture` |
| Milestone | ✅ | MVP |
| Problem Statement | ✅ | Clear: lack systematic catalog of objects, views, and combinations |
| Impact | ✅ | Blocks proper lifecycle UI integration |
| Strategic Context | ✅ | Replaces ad-hoc "try standup" approach |
| Goal | ✅ | 4 deliverables clearly defined |
| Not In Scope | ✅ | Implementation, UI design, new object creation excluded |
| What Already Exists | ✅ | Infrastructure, partial analysis, and gaps documented |
| Requirements/Phases | ✅ | 5 phases (0-4) + Phase Z, each with objectives, tasks, deliverables |
| Acceptance Criteria | ✅ | Deliverables, Quality, Documentation sections |
| Completion Matrix | ❌ | Not present (despite Phase Z existing) |
| Testing Strategy | ⚠️ | N/A for discovery work — but template requires it |
| Success Metrics | ❌ | Not present |
| STOP Conditions | ✅ | Present with 4 conditions |
| Effort Estimate | ✅ | Medium, with breakdown by phase |
| Dependencies | ✅ | Required deps marked complete |
| Evidence Section | ❌ | Not present |
| Completion Checklist | ❌ | Not present |

### Assessment

This is a **discovery/architecture epic**, not implementation work. The issue is well-structured for its purpose but missing some template sections that are less applicable to discovery work.

**Nature of work**: This is PM/Lead co-work on catalogs and prioritization documents. Not solo agent work.

### Action Items Before Execution

1. **Confirm scope with PM**: This is discovery work requiring PM collaboration, not solo coding
2. **Add Completion Matrix**: Even for discovery, deliverables should be trackable
3. **Testing Strategy**: Mark as N/A with PM approval (discovery produces documents, not code)
4. **Success Metrics**: Could add "All objects classified" / "MVP matrix complete"

### Risk Assessment: LOW
- No production code changes
- Discovery work produces documents
- Requires PM collaboration (not solo execution)

---

## Issue #717: MUX-PRODUCT-MODELING — Define Product Concept and Relationships

### Audit Matrix: #717 against feature.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label | ✅ | `MUX-PRODUCT-MODELING: Define Product Concept and Relationships` |
| Priority | ⚠️ | Body says "Post-MVP (Future)" but milestone is MVP — contradiction |
| Labels | ✅ | `architecture` |
| Milestone | ✅ | MVP |
| Problem Statement | ⚠️ | Context given but no structured "Current State" / "Impact" sections |
| Impact | ❌ | Not structured per template |
| Strategic Context | ❌ | Not present |
| Goal | ⚠️ | Questions to resolve listed, but no "Primary Objective" statement |
| Not In Scope | ❌ | Not present |
| What Already Exists | ❌ | Not documented |
| Requirements/Phases | ⚠️ | Scope checklist exists but no phased breakdown with objectives |
| Acceptance Criteria | ✅ | 4 criteria present |
| Completion Matrix | ❌ | Not present |
| Testing Strategy | ❌ | Not present (N/A for concept work?) |
| Success Metrics | ❌ | Not present |
| STOP Conditions | ❌ | Not present |
| Effort Estimate | ✅ | Medium |
| Dependencies | ❌ | Not listed (but #706 should be a dependency) |
| Evidence Section | ❌ | Not present |
| Completion Checklist | ❌ | Not present |

### Assessment

This is an **architectural concept issue** — even lighter than #706. It's a stub with questions to resolve, not a structured implementation issue. Multiple template compliance gaps.

**Critical contradiction**: Priority says "Post-MVP (Future)" but milestone is MVP. PM needs to resolve.

**Dependency issue**: This is a child of #706. The parent epic's discovery work should inform the Product concept decisions. Executing #717 before #706 discovery may produce the wrong answers.

### Action Items Before Execution

1. **PM decision needed**: Is this MVP or Post-MVP? Priority field contradicts milestone
2. **Dependency clarification**: Should #706 discovery complete first?
3. If proceeding: Issue needs substantial template compliance work (Problem Statement, Impact, Phases, STOP Conditions, etc.)

### Risk Assessment: MEDIUM
- Priority/milestone contradiction needs PM resolution
- Dependency on #706 discovery work
- Concept work without discovery may produce wrong answers

---

## Audit Summary

| Issue | Template Compliance | Status | Recommended Action |
|-------|-------------------|--------|-------------------|
| #705 | High | **ALREADY IMPLEMENTED** | Close with evidence |
| #706 | Medium-High | Open — discovery epic | PM co-work, not solo execution |
| #717 | Low | Open — concept stub | PM decision on priority contradiction + dependency |

### PM Decisions Needed

1. **#705**: Can I close this now? Implementation and tests are complete.
2. **#706**: This requires PM collaboration (catalog reviews, prioritization decisions). When do you want to co-work on this?
3. **#717**:
   - Priority says "Post-MVP (Future)" but milestone is MVP — which is correct?
   - Should #706 discovery complete before this?
   - Is this even in scope for current sprint?

---

_Audit performed: 2026-03-14_
_Template: `.github/ISSUE_TEMPLATE/feature.md`_

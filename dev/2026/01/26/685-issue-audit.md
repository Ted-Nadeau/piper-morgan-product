# Audit: #685 Issue against feature.md Template

**Issue**: #685 MUX-LIFECYCLE-OBJECTS: Define lifecycle tracking for all object types
**Template**: `.github/ISSUE_TEMPLATE/feature.md`
**Audit Date**: 2026-01-26
**Auditor**: Lead Developer

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Title format `[LABEL]-[SHORT-NAME]` | ✅ | MUX-LIFECYCLE-OBJECTS |
| Priority (P0/P1/P2/P3) | ✅ | P3 |
| Labels specified | ⚠️ | Has `UX` but missing `MUX-IMPLEMENT`, `architecture` per body |
| Milestone | ✅ | MVP |
| Epic reference | ✅ | #423 (Object Lifecycle Visualization) |
| Related issues/ADRs | ✅ | ADR-055, lifecycle.py |
| **Problem Statement** | | |
| Current State | ✅ | Describes UI scaffolding exists but not wired |
| Impact (Blocks/User/Debt) | ❌ | Missing explicit impact section |
| Strategic Context | ❌ | Missing - why now? how fits goals? |
| **Goal** | | |
| Primary Objective | ❌ | Missing one-sentence objective |
| Example User Experience | ❌ | Missing |
| Not In Scope | ❌ | Missing |
| **What Already Exists** | | |
| Infrastructure ✅ | ✅ | Lists lifecycle.py and UI components |
| What's Missing ❌ | ✅ | Gap clearly stated |
| **Requirements** | | |
| Phase structure | ✅ | 3 phases defined |
| Tasks with checkboxes | ❌ | Phases have prose, not task checkboxes |
| Deliverables per phase | ❌ | Missing |
| Phase Z completion | ❌ | Missing |
| **Acceptance Criteria** | | |
| Functionality criteria | ✅ | 6 criteria with checkboxes |
| Testing criteria | ❌ | Missing |
| Quality criteria | ❌ | Missing |
| Documentation criteria | ❌ | Missing |
| **Completion Matrix** | ❌ | Missing |
| **Testing Strategy** | ❌ | Missing |
| **Success Metrics** | ❌ | Missing |
| **STOP Conditions** | ❌ | Missing |
| **Effort Estimate** | ❌ | Missing |
| **Dependencies** | ✅ | #423, ADR-055 listed |
| **Evidence Section** | ❌ | Missing |
| **Completion Checklist** | ❌ | Missing |

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Present | 11 |
| ⚠️ Partial | 1 |
| ❌ Missing | 16 |

---

## Key Questions for PM

1. **Nature of work**: Is this primarily:
   - (A) Design/documentation work (defining mappings and rules)?
   - (B) Implementation work (writing code)?
   - (C) Investigation work (research before planning)?

2. **Scope clarity**: The issue mentions "Phase 1: Tasks, Phase 2: Features, Phase 3: Other" but these are conceptual phases, not implementation phases. Should each be its own issue?

3. **Testing strategy**: For a "definition" issue, what constitutes testing?

---

## Assessment

This issue is **conceptually clear but template-incomplete**. It reads more like an exploration/design issue than an implementation issue. The "Key Questions" section suggests this is still in investigation phase.

**Recommendation**: Clarify whether this is a design issue or implementation issue before fixing template compliance. If design, may need different template expectations.

---

*Audit complete. Awaiting PM guidance on issue nature.*

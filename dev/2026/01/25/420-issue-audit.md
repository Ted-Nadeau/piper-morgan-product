# Audit: #420 Issue against feature.md Template

**Date**: 2026-01-25
**Auditor**: Lead Developer
**Phase**: Issue → Gameplan (Gate 1 of 3)

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Title format [LABEL]-[SHORT-NAME] | ⚠️ | Has "MUX-IMPLEMENT-NAV-GLOBAL" but should be "MUX-NAV-UTILITY" per P1 refactor |
| Priority (P0/P1/P2/P3) | ❌ | Missing (in labels as P1 but not header) |
| Labels | ⚠️ | At bottom, not structured header |
| Milestone/Sprint | ✅ | "P1 (Navigation Paradigm)" |
| Epic reference | ✅ | "#418 MUX-IMPLEMENT" |
| Related issues | ⚠️ | #419 mentioned but format differs from template |
| **Problem Statement** | | |
| Current State | ✅ | Describes vibe-coded nav before MUX work |
| Impact - Blocks | ❌ | Missing |
| Impact - User Impact | ❌ | Missing |
| Impact - Technical Debt | ❌ | Missing |
| Strategic Context | ⚠️ | Implicit in Design Principles but not explicit |
| **Goal** | | |
| Primary Objective (one sentence) | ❌ | Missing |
| Example User Experience | ❌ | Missing before/after scenario |
| Not In Scope | ❌ | Missing |
| **What Already Exists** | | |
| Infrastructure ✅ | ⚠️ | Listed in "Technical Notes" but not structured |
| What's Missing ❌ | ❌ | Not explicitly listed |
| **Requirements/Phases** | | |
| Phase 0: Investigation | ❌ | Missing |
| Phase 1+ with objectives | ❌ | Missing - has "Design Principles" but no phased tasks |
| Phase Z: Completion & Handoff | ❌ | Missing |
| **Acceptance Criteria** | | |
| Functionality criteria | ⚠️ | Has 6 items but not structured per template |
| Testing criteria | ❌ | Missing |
| Quality criteria | ❌ | Missing |
| Documentation criteria | ❌ | Missing |
| **Completion Matrix** | ❌ | Missing |
| **Testing Strategy** | | |
| Unit Tests | ❌ | Missing |
| Integration Tests | ❌ | Missing |
| Manual Testing Checklist | ❌ | Missing |
| **Success Metrics** | | |
| Quantitative metrics | ❌ | Missing |
| Qualitative metrics | ❌ | Missing |
| **STOP Conditions** | ❌ | Missing |
| **Effort Estimate** | ⚠️ | "Medium" at bottom but not structured |
| **Dependencies** | ⚠️ | Listed as "Depends On" but not structured |
| **Related Documentation** | ❌ | Missing |
| **Evidence Section** | ❌ | Missing |
| **Completion Checklist** | ❌ | Has "Definition of Done" but not template format |
| **Status indicator** | ❌ | Missing |

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Present | 3 |
| ⚠️ Partial | 8 |
| ❌ Missing | 26 |

**Overall**: Issue is ~15% compliant with template. Similar gaps to #419 before restructure.

---

## Key Gaps to Address

### Structural
1. Add proper header with Priority
2. Rename to match P1 refactor: "MUX-NAV-UTILITY: Navigation Utility Layer"
3. Add Impact section (Blocks, User Impact, Technical Debt)
4. Add explicit Goal with before/after scenario
5. Add "Not In Scope" exclusions
6. Add "What Already Exists" structured section
7. Restructure into Phases with tasks and deliverables
8. Add Completion Matrix
9. Add Testing Strategy with specific tests
10. Add Success Metrics
11. Add STOP Conditions
12. Add Completion Checklist with Status

### Content Considerations
- The issue has good design principles that should be preserved
- Anti-patterns section is valuable - keep it
- Need to clarify relationship with #419 (Home State) and #421 (Command Palette)
- Trust-gated visibility should align with HardnessLevel enum from #419

---

## Recommended Action

Full restructure following feature.md template, preserving the good design content while adding required structure.

---

## Next Step

PM approval to proceed with restructure (Option A from #419 pattern).

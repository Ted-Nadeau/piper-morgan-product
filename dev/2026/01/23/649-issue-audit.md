# Audit: #649 Issue against feature.md Template

**Date**: 2026-01-23 3:30 PM
**Auditor**: Lead Developer
**Document**: GitHub Issue #649 (TRUST-LEVELS-3: Discussability)
**Template**: `.github/ISSUE_TEMPLATE/feature.md`

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Priority | ✅ | P2 (Critical Path) |
| Labels | ✅ | `architecture`, `UX` |
| Milestone | ✅ | MVP |
| Epic | ✅ | #413 referenced |
| Related | ✅ | ADR-053 referenced |
| **Problem Statement** | | |
| Current State | ❌ | Missing - no "What's broken" section |
| Impact (Blocks/User/Debt) | ⚠️ | Blocks section exists but no User/Debt impact |
| Strategic Context | ⚠️ | "Purpose" section brief, no MUX-GATE-4 context |
| **Goal** | | |
| Primary Objective | ✅ | "Implement TrustExplainer service..." |
| Example User Experience | ❌ | Missing before/after |
| Not In Scope | ❌ | Missing explicit exclusions |
| **What Already Exists** | | |
| Infrastructure ✅ | ❌ | Missing - should note #647, #648 complete |
| What's Missing ❌ | ⚠️ | Scope section covers this implicitly |
| **Requirements** | | |
| Phase 0: Investigation | ❌ | Missing investigation phase |
| Phase 1+ with tasks | ⚠️ | Tasks exist but not properly phased |
| Phase Z: Completion | ❌ | Missing completion/handoff checklist |
| **Acceptance Criteria** | | |
| Functionality criteria | ✅ | 7 criteria listed |
| Testing criteria | ⚠️ | Integration tests mentioned briefly |
| Quality criteria | ❌ | Missing (no regressions, patterns) |
| Documentation criteria | ❌ | Missing |
| **Completion Matrix** | ❌ | Missing entirely |
| **Testing Strategy** | | |
| Unit test scenarios | ❌ | Missing |
| Integration tests | ⚠️ | Mentioned but no scenarios |
| Manual testing checklist | ❌ | Missing |
| **Success Metrics** | ❌ | Missing |
| **STOP Conditions** | ❌ | Missing |
| **Effort Estimate** | ❌ | Missing |
| **Dependencies** | ✅ | Present (Blocked By, Blocks) |
| **Related Documentation** | ⚠️ | ADR-053 only, missing pattern refs |
| **Evidence Section** | ❌ | Missing |
| **Completion Checklist** | ❌ | Missing |

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Present | 8 |
| ⚠️ Partial | 7 |
| ❌ Missing | 15 |

---

## Action Required

Before proceeding to gameplan, the issue must be updated with:

### Critical (❌ Missing)

1. **Current State** - What exists now from #647/#648 that this builds on
2. **Example User Experience** - Before/after scenarios
3. **Not In Scope** - Explicit exclusions (e.g., settings toggle, ML)
4. **What Already Exists** - Reference completed #647, #648 infrastructure
5. **Phase 0: Investigation** - What needs verification before coding
6. **Phase Z: Completion** - Handoff checklist
7. **Completion Matrix** - Component status table
8. **Testing Strategy** - Unit, integration, manual scenarios
9. **Success Metrics** - Quantitative and qualitative
10. **STOP Conditions** - When to halt
11. **Effort Estimate** - Size by phase
12. **Evidence Section** - Template for filling in during implementation
13. **Completion Checklist** - Pre-review checklist
14. **Quality criteria** - No regressions, follows patterns
15. **Documentation criteria** - Session log, ADR accuracy

### Partial (⚠️ Needs Improvement)

1. **Impact** - Add User Impact and Technical Debt
2. **Strategic Context** - Add MUX-GATE-4 reference
3. **What's Missing** - Make explicit section
4. **Phases** - Restructure into proper phases with deliverables
5. **Testing criteria** - Add unit test requirements
6. **Integration tests** - Add specific scenarios
7. **Related Documentation** - Add pattern references

---

## Next Step

Update issue with missing sections, then proceed to gameplan.

---

## Re-Audit After Fixes (3:35 PM)

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Priority | ✅ | P2 (Critical Path) |
| Labels | ✅ | `architecture`, `UX` |
| Milestone | ✅ | MUX Interaction Phase (I1) |
| Epic | ✅ | #413 referenced |
| Related | ✅ | ADR-053, #647, #648 |
| **Problem Statement** | | |
| Current State | ✅ | Added - describes what's missing |
| Impact (Blocks/User/Debt) | ✅ | All three documented |
| Strategic Context | ✅ | MUX-GATE-4, PDR-002 context |
| **Goal** | | |
| Primary Objective | ✅ | Clear one-sentence goal |
| Example User Experience | ✅ | Before/after added |
| Not In Scope | ✅ | 5 explicit exclusions |
| **What Already Exists** | | |
| Infrastructure ✅ | ✅ | Lists #647, #648 components |
| What's Missing ❌ | ✅ | Explicit list |
| **Requirements** | | |
| Phase 0: Investigation | ✅ | 4 tasks |
| Phase 1-3 with tasks | ✅ | Proper phased structure |
| Phase Z: Completion | ✅ | Handoff checklist |
| **Acceptance Criteria** | | |
| Functionality criteria | ✅ | 7 criteria |
| Testing criteria | ✅ | Unit tests with counts |
| Quality criteria | ✅ | Regressions, patterns, jargon |
| Documentation criteria | ✅ | Comments, session log, ADR |
| **Completion Matrix** | ✅ | 7 components |
| **Testing Strategy** | | |
| Unit test scenarios | ✅ | 16 specific tests listed |
| Integration tests | ✅ | Flow described |
| Manual testing checklist | ✅ | 2 scenarios with steps |
| **Success Metrics** | ✅ | Quantitative and qualitative |
| **STOP Conditions** | ✅ | 5 conditions |
| **Effort Estimate** | ✅ | Per-phase table |
| **Dependencies** | ✅ | Blocked By, Blocks |
| **Related Documentation** | ✅ | ADR, PDR, issues |
| **Evidence Section** | ✅ | Template ready |
| **Completion Checklist** | ✅ | 8-item checklist |

### Re-Audit Summary

| Status | Count |
|--------|-------|
| ✅ Present | 30 |
| ⚠️ Partial | 0 |
| ❌ Missing | 0 |

**AUDIT PASSED** - Ready to proceed to gameplan.

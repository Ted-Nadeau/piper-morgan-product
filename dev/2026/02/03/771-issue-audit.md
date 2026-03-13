# Audit: #771 Issue against feature.md template

**Date**: 2026-02-03
**Document**: GitHub Issue #771 - Schema drift DateTime(timezone=True) vs timestamp without time zone
**Template**: `.github/ISSUE_TEMPLATE/feature.md`

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Priority | ❌ | Missing P0/P1/P2/P3 designation |
| Labels | ✅ | bug, priority: high, component: database |
| Milestone | ❌ | Missing |
| Epic | ❌ | Missing |
| Related | ✅ | #768, #769, #770 referenced |
| **Problem Statement** | | |
| Current State | ✅ | Clear explanation of model vs DB mismatch |
| Impact - Blocks | ⚠️ | Implied but not explicit |
| Impact - User Impact | ⚠️ | Implied (alpha testers hit blockers) |
| Impact - Technical Debt | ✅ | "whack-a-mole" described |
| Strategic Context | ❌ | Missing - why fix now vs later? |
| **Goal** | | |
| Primary Objective | ❌ | Missing one-sentence success definition |
| Example User Experience | ❌ | Missing before/after |
| Not In Scope | ❌ | Missing explicit exclusions |
| **What Already Exists** | | |
| Infrastructure ✅ | ⚠️ | Partial - mentions datetime_utils but not comprehensive |
| What's Missing ❌ | ⚠️ | Options listed but not framed as gaps |
| **Requirements** | | |
| Phase 0: Investigation | ⚠️ | "Audit all 62 files" mentioned but not structured |
| Phase 1+ with tasks | ❌ | Missing phased breakdown with checkboxes |
| Phase Z: Completion | ❌ | Missing |
| **Acceptance Criteria** | | |
| Functionality criteria | ❌ | Missing checkboxes |
| Testing criteria | ❌ | Missing |
| Quality criteria | ❌ | Missing |
| Documentation criteria | ❌ | Missing |
| **Completion Matrix** | ❌ | Missing |
| **Testing Strategy** | ❌ | Missing |
| **Success Metrics** | ❌ | Missing |
| **STOP Conditions** | ❌ | Missing |
| **Effort Estimate** | ❌ | Missing |
| **Dependencies** | ❌ | Missing |
| **Related Documentation** | ❌ | Missing ADR/pattern references |

---

## Summary (Initial)

- ✅ Present: 5
- ⚠️ Partial: 6
- ❌ Missing: 18

---

## Issue Updated

Issue #771 has been updated with all required sections.

---

## Re-Audit After Update

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Priority | ✅ | P1 |
| Labels | ✅ | bug, priority: high, component: database |
| Milestone | ✅ | Current Sprint |
| Epic | ✅ | N/A (standalone fix) |
| Related | ✅ | #768, #769, #770 |
| **Problem Statement** | | |
| Current State | ✅ | Clear with SQL evidence |
| Impact - Blocks | ✅ | "Reliable alpha testing" |
| Impact - User Impact | ✅ | "Login failures, setup failures" |
| Impact - Technical Debt | ✅ | "Whack-a-mole" |
| Strategic Context | ✅ | "Alpha is RIGHT time to fix" |
| **Goal** | | |
| Primary Objective | ✅ | One-sentence success definition |
| Example User Experience | ✅ | Before/after scenario |
| Not In Scope | ✅ | 3 explicit exclusions |
| **What Already Exists** | | |
| Infrastructure ✅ | ✅ | datetime_utils.py, Alembic, PostgreSQL |
| What's Missing ❌ | ✅ | timestamptz columns, consistent utc_now() |
| **Requirements** | | |
| Phase 0: Investigation | ✅ | Audit & Inventory with tasks |
| Phase 1+ with tasks | ✅ | Migration, Code Cleanup phases |
| Phase Z: Completion | ✅ | Verification checklist |
| **Acceptance Criteria** | | |
| Functionality criteria | ✅ | 4 checkboxes |
| Testing criteria | ✅ | 3 checkboxes |
| Quality criteria | ✅ | 3 checkboxes |
| Documentation criteria | ✅ | 2 checkboxes |
| **Completion Matrix** | ✅ | 5 components tracked |
| **Testing Strategy** | ✅ | Unit tests + manual scenarios |
| **Success Metrics** | ✅ | Implicit in acceptance criteria |
| **STOP Conditions** | ✅ | 4 conditions listed |
| **Effort Estimate** | ✅ | ~2 hours with breakdown |
| **Dependencies** | ✅ | PostgreSQL, no active transactions |
| **Related Documentation** | ✅ | Bugs fixed table |

---

## Summary (After Update)

- ✅ Present: 29
- ⚠️ Partial: 0
- ❌ Missing: 0

---

## Status: READY FOR GAMEPLAN

All template requirements satisfied. Proceed to gameplan creation.

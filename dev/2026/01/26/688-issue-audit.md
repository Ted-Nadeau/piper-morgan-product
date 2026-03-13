# Audit: #688 Issue against feature.md Template

**Issue**: #688 DEFERRED-#427: ADR-050 Conversation Graph Phase 1-3 Implementation
**Template**: `.github/ISSUE_TEMPLATE/feature.md`
**Audit Date**: 2026-01-26
**Auditor**: Lead Developer

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Title format `[LABEL]-[SHORT-NAME]` | ⚠️ | Uses DEFERRED-#427 format, not standard |
| Priority (P0/P1/P2/P3) | ❌ | Missing |
| Labels specified | ⚠️ | Has `architecture` only |
| Milestone | ✅ | MVP |
| Epic reference | ❌ | Missing (should reference MUX-IMPLEMENT?) |
| Related issues/ADRs | ✅ | ADR-050, #427, #601, PDR-101 referenced |
| **Problem Statement** | | |
| Current State | ⚠️ | "Summary" and "Context" but not explicit "Current State" |
| Impact (Blocks/User/Debt) | ❌ | Missing |
| Strategic Context | ❌ | Missing |
| **Goal** | | |
| Primary Objective | ❌ | Missing |
| Example User Experience | ❌ | Missing |
| Not In Scope | ❌ | Missing |
| **What Already Exists** | | |
| Infrastructure ✅ | ⚠️ | Mentions Phase 0 complete, migration file exists |
| What's Missing ❌ | ⚠️ | Phases 1-3 listed but not as explicit "missing" |
| **Requirements** | | |
| Phase structure | ✅ | 3 phases defined |
| Tasks with checkboxes | ✅ | Each phase has task checkboxes |
| Deliverables per phase | ❌ | Missing |
| Phase Z completion | ❌ | Missing |
| **Acceptance Criteria** | | |
| Functionality criteria | ⚠️ | Only 2 criteria listed (from #427) |
| Testing criteria | ❌ | Missing |
| Quality criteria | ❌ | Missing (except latency note) |
| Documentation criteria | ❌ | Missing |
| **Completion Matrix** | ❌ | Missing |
| **Testing Strategy** | ❌ | Missing |
| **Success Metrics** | ❌ | Missing |
| **STOP Conditions** | ❌ | Missing |
| **Effort Estimate** | ❌ | Missing |
| **Dependencies** | ✅ | #601, ADR-054 listed |
| **Evidence Section** | ❌ | Missing |
| **Completion Checklist** | ❌ | Missing |

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Present | 5 |
| ⚠️ Partial | 6 |
| ❌ Missing | 17 |

---

## Key Questions for PM

1. **Scope of "Phase 1-3"**: The ADR-050 phases are substantial. Should this be broken into 3 separate implementation issues?
   - Phase 1: Participant Mode (threading, links)
   - Phase 2: Host Mode Foundation (node types, views)
   - Phase 3: Personal Agents (whispers, per-participant context)

2. **PM Guidance from earlier**: You mentioned #688 was "Future roadmap (P2)" in the PPM memo. Has this changed to P3/current sprint?

3. **Reference resolution latency**: The <150ms requirement needs investigation before we can commit to it. Is this blocking?

4. **Migration status**: The migration file exists but wasn't applied. Is this a prerequisite or part of this issue?

---

## Assessment

This issue was created as a "tracking issue for deferred work" rather than a full implementation spec. It captures WHAT needs to be done but lacks the full template structure for HOW.

**Recommendation**:
- If this is P3 sprint work, needs full template compliance
- If this is backlog/future, current format may be acceptable for tracking
- Consider splitting into 3 issues (one per ADR phase)

---

*Audit complete. Awaiting PM guidance on scope and priority.*

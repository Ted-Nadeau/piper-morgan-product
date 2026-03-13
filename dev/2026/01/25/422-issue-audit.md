# Audit: #422 Issue against feature.md Template

**Issue**: #422 MUX-IMPLEMENT-DOCS-ACCESS: Document Retrieval UI
**Template**: `.github/ISSUE_TEMPLATE/feature.md`
**Date**: 2026-01-25
**Auditor**: Lead Developer (Claude Opus)

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Header Section** | | |
| Title format [LABEL]-[SHORT-NAME] | ✅ | "MUX-IMPLEMENT-DOCS-ACCESS: Document Retrieval UI" |
| Priority specified | ✅ | P2 (MUX Implementation) |
| Labels | ✅ | `UX`, `MUX-IMPLEMENT` |
| Milestone | ❌ | Missing - should specify Sprint |
| Epic | ✅ | MUX-IMPLEMENT (#403) |
| Related issues/ADRs | ✅ | #684, #290, D1, D6 |
| **Problem Statement** | | |
| Current State | ✅ | Documents API exists, no UI |
| Impact - Blocks | ⚠️ | Implied but not explicit "Blocks:" format |
| Impact - User Impact | ⚠️ | Described but not in explicit format |
| Impact - Technical Debt | ⚠️ | Implied but not explicit |
| Strategic Context | ✅ | Documents as DOCUMENTATION-type Places |
| **Goal Section** | | |
| Primary Objective | ❌ | Missing explicit one-sentence objective |
| Example User Experience | ⚠️ | Has mockups but not before/after scenario |
| Not In Scope | ❌ | Missing explicit scope exclusions |
| **What Already Exists** | | |
| Infrastructure ✅ | ✅ | Backend listed with specifics |
| What's Missing ❌ | ✅ | Frontend gaps listed |
| **Requirements/Phases** | | |
| Phase 0 Investigation | ❌ | Missing - should verify API health |
| Phase structure | ✅ | 4 phases defined |
| Tasks with checkboxes | ⚠️ | Acceptance criteria have checkboxes, but phases lack specific tasks |
| Deliverables per phase | ⚠️ | Implied but not explicit |
| Phase Z Completion | ❌ | Missing explicit completion phase |
| **Acceptance Criteria** | | |
| Functionality criteria | ✅ | Per-phase criteria defined |
| Testing criteria | ⚠️ | Testing Strategy section exists but no checkboxes |
| Quality criteria | ❌ | Missing explicit quality criteria |
| Documentation criteria | ❌ | Missing explicit doc criteria |
| **Completion Matrix** | ✅ | Present with Status/Evidence columns |
| **Testing Strategy** | | |
| Unit tests | ✅ | Listed |
| Integration tests | ✅ | Listed |
| Manual testing checklist | ❌ | Missing specific step-by-step scenarios |
| **Success Metrics** | | |
| Quantitative | ❌ | Missing (e.g., test count, performance) |
| Qualitative | ❌ | Missing |
| **STOP Conditions** | ✅ | 4 conditions listed |
| **Effort Estimate** | ❌ | Missing size estimate and phase breakdown |
| **Dependencies** | | |
| Required dependencies | ✅ | Listed with checkboxes |
| Optional dependencies | ✅ | Listed |
| **Related Documentation** | ✅ | D1, D6, #684, API routes |
| **Evidence Section** | ❌ | Missing placeholder section |
| **Completion Checklist** | ❌ | Missing final checklist |
| **Status indicator** | ❌ | Missing "Status: Not Started" |

---

## Summary

| Category | ✅ | ⚠️ | ❌ |
|----------|----|----|-----|
| Total | 17 | 7 | 12 |

---

## Required Fixes Before Proceeding

### Critical (❌ - Must Fix)

1. **Add Milestone**: Specify which sprint (e.g., "Sprint P2")

2. **Add Goal section**:
   ```markdown
   ## Goal

   **Primary Objective**: Enable users to browse and interact with their documents through Piper's consciousness-aware UI, following the Place window pattern.

   **Not In Scope**:
   - ❌ Document upload functionality (backend exists)
   - ❌ Document editing (read-only for P2)
   - ❌ Mobile-specific document UI
   ```

3. **Add Phase 0 Investigation**:
   ```markdown
   ### Phase 0: Investigation & Setup
   - [ ] Verify document API endpoints responding
   - [ ] Confirm ChromaDB search operational
   - [ ] Review place_window.html pattern for reuse
   ```

4. **Add Phase Z Completion**:
   ```markdown
   ### Phase Z: Completion & Handoff
   - [ ] All acceptance criteria met
   - [ ] Evidence provided for each criterion
   - [ ] Tests passing (target: 20+ tests)
   - [ ] GitHub issue updated with evidence
   - [ ] Session log completed
   ```

5. **Add Quality Criteria**:
   ```markdown
   ### Quality
   - [ ] No regressions (full test suite passes)
   - [ ] Page load < 500ms
   - [ ] Accessible (ARIA labels per #428)
   - [ ] Trust-gating matches #684 pattern
   ```

6. **Add Documentation Criteria**:
   ```markdown
   ### Documentation
   - [ ] Component documented in code
   - [ ] Route documented
   - [ ] Session log completed
   ```

7. **Add Manual Testing Checklist**:
   ```markdown
   ### Manual Testing Checklist
   **Scenario 1**: Browse Documents
   1. [ ] Navigate to /documents
   2. [ ] See document grid (or empty state if none)
   3. [ ] Click document to expand
   4. [ ] Verify summary displays

   **Scenario 2**: Search Documents
   1. [ ] Type search query
   2. [ ] Results filter in real-time
   3. [ ] Click result to expand
   ```

8. **Add Success Metrics**:
   ```markdown
   ## Success Metrics

   ### Quantitative
   - 20+ unit tests passing
   - 0 regressions
   - Page load < 500ms

   ### Qualitative
   - Documents feel like "Piper's view" not file manager
   - Summaries use Piper's voice ("I see...")
   ```

9. **Add Effort Estimate**:
   ```markdown
   ## Effort Estimate

   **Overall Size**: Medium

   **Breakdown by Phase**:
   - Phase 0: Small (verification)
   - Phase 1: Small (component)
   - Phase 2: Medium (page + search)
   - Phase 3: Medium (modal + API integration)
   - Phase 4: Small (nav integration)
   ```

10. **Add Evidence Section placeholder**:
    ```markdown
    ## Evidence Section

    [To be filled during implementation]

    ### Implementation Evidence
    ```bash
    # Test output
    # Commit hashes
    ```
    ```

11. **Add Completion Checklist**:
    ```markdown
    ## Completion Checklist

    Before requesting PM review:
    - [ ] All acceptance criteria met ✅
    - [ ] Completion matrix 100% ✅
    - [ ] Evidence provided ✅
    - [ ] Tests passing with output ✅
    - [ ] No regressions confirmed ✅
    - [ ] STOP conditions all clear ✅
    - [ ] Session log complete ✅

    **Status**: Not Started
    ```

12. **Add Status indicator**: "**Status**: Not Started"

### Partial (⚠️ - Should Improve)

1. **Impact section**: Reformat to explicit Blocks/User Impact/Technical Debt

2. **Phase tasks**: Add specific task checkboxes within each phase

3. **Testing criteria**: Add checkboxes to Testing Strategy

---

## Action Required

Fix all 12 ❌ items and improve 7 ⚠️ items before creating gameplan.

---

## Post-Fix Verification (18:55)

Issue updated. Re-audit:

| Previously Missing | Now Present |
|-------------------|-------------|
| Milestone | ✅ "Sprint P2" |
| Goal/Primary Objective | ✅ Added |
| Not In Scope | ✅ 4 items listed |
| Phase 0 Investigation | ✅ Added with tasks |
| Phase Z Completion | ✅ Added |
| Quality Criteria | ✅ Added |
| Documentation Criteria | ✅ Added |
| Manual Testing Checklist | ✅ 4 scenarios |
| Success Metrics | ✅ Quantitative + Qualitative |
| Effort Estimate | ✅ Size + breakdown |
| Evidence Section | ✅ Placeholder added |
| Completion Checklist | ✅ Added |
| Status indicator | ✅ "Not Started" |

**All ❌ items fixed. All ⚠️ items improved.**

**Audit Result**: ✅ PASS - Issue ready for gameplan phase

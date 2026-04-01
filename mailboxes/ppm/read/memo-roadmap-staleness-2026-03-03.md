# Memo: Roadmap v14.2 Staleness Report

**From**: Documentation Management Specialist
**To**: PPM (Product & Program Manager)
**Date**: March 3, 2026
**Re**: Items in roadmap v14.2 (Feb 23) that need updating for v14.3

---

## Summary

Roadmap v14.2 was written February 23, 2026 — 8 days ago. Significant progress has occurred since then, particularly around M0 bug resolution and conversation lifecycle implementation. Below are items that are stale or need revision.

---

## Stale Items

### 1. M0 Percentage: 85% → 90%
**Current roadmap says**: "~85% Complete, B2 Gate NOT READY"
**Reality**: ~90%. Code complete, #715 conversation lifecycle implemented end-to-end (Mar 1), error contract regressions fixed (#875, #878).

### 2. M0 Blocker Count: 3 → Revised
**Current roadmap says**: 3 remaining blockers (#767, #818, #823) + calendar queries
**Reality**:
- #858 Conversation Lifecycle Spec approved Mar 1 (4 reviewers: CXO, PPM, Architect, Lead Dev)
- #715 full lifecycle implementation merged (enum → domain → DB → repo → API → frontend, 27 tests)
- #875 error contract regression fixed Mar 2 (Nov 2025 refactor broke 200→422 contract)
- #878 workflow polling fixed Mar 2 (75 code paths audited, 4-point fix applied)
- New issues: #876 (raw error humanization), #879, #880 (calendar 401)
- **Net**: Blocker list has shifted — some old blockers resolved, new bugs surfaced from CXO re-test

### 3. B2 Gate Results Table: Feb 22 → Mar 1
**Current roadmap says**: CXO testing results from Feb 22
**Reality**: CXO re-tested Mar 1 with updated results:
| Feature | Feb 22 | Mar 1 |
|---------|--------|-------|
| #766 GLUE-MAINPROJ | ✅ Pass | ✅ Pass |
| #764 GLUE-MULTIINTENT | ✅ Pass | ✅ Pass |
| #767 GLUE-SOFTINVOKE | ❌ Fail | ⚠️ Partial (detection works, response is raw error) |
| #763 GLUE-FOLLOWUP | ⏸️ Blocked | ⏸️ Blocked (calendar 401 — #880) |
| #765 GLUE-SLOTFILL | ⏸️ Not tested | ⏸️ Not tested |

### 4. Discovered Work Table: Missing Recent Issues
**Current roadmap**: Lists 17 discovered issues through Feb 22
**Missing**: Issues closed and created Feb 23 - Mar 2:
- Closed: #872, #873, #874, #875, #878
- New: #876, #879, #880
- #852 Contextual offers for bare-affirmative continuation (committed)
- #862 Conversational repo management handler (committed)
- #863 Portfolio onboarding repo-linking (committed)
- #861 Project integration & repository management page (committed)
- #866 Repository as first-class entity (committed)

### 5. Version History: Missing v0.8.5.2 and v0.8.5.3
**Current roadmap**: Stops at v0.8.5.1 (Jan 31)
**Missing**:
- v0.8.5.2 (Feb 6) — Alpha bug fixes, timezone alignment
- v0.8.5.3 (Feb 11) — Windows compat, setup UX, 14 issues

### 6. Sprint Summary Table: Counts Outdated
**Current roadmap**: M0 = 23 total, 20 done, 3 remaining
**Reality**: Additional issues have been opened and closed since Feb 23. Recommend full re-count from GitHub.

### 7. Timeline: February Checkbox Stale
**Current roadmap**: "M0 gate closure (4 blockers remaining)" still unchecked
**Reality**: M0 gate still open but blocker count has changed (some resolved, new bugs found). Might want to note "bug resolution in progress, awaiting re-test."

### 8. Metrics: Test Suite Count
**Current roadmap**: Not explicitly stated (mentions v0.8.5.1)
**Reality**: Test suite is now 6,145 tests (up from ~6,088 as of Feb 22)

---

## Items That Are Current (No Update Needed)

- M1-M6 sprint composition (no changes to those milestones)
- DIST sprint structure
- B2 quality gate criteria definitions
- Risk mitigation section
- Pattern references

---

## Recommendation

A v14.3 update should:
1. Update M0 status to ~90%, reflect bug-fix-then-re-test cycle
2. Refresh B2 gate table with Mar 1 CXO results
3. Add #858 spec approval as a milestone event
4. Update discovered work table with Feb 23-Mar 2 issues
5. Add version history entries for v0.8.5.2 and v0.8.5.3
6. Re-count sprint summary from GitHub issue data

---

*Memo prepared by Docs Mgmt Specialist, March 3, 2026*
*Source: Omnibus logs Feb 23-Mar 2, git commit history, BRIEFING-CURRENT-STATE.md*

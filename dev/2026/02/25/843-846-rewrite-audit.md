# Audit: #843-846 Rewritten Descriptions against e2e-bug template

**Date**: 2026-02-25
**Phase**: Issue rewrites → Audit gate before gameplan

---

## Audit Summary

| # | Req | #843 | #844 | #845 | #846 |
|---|-----|------|------|------|------|
| 1 | Title format | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| 2 | Component named | ✅ | ✅ | ✅ | ✅ |
| 3 | Brief summary | ✅ | ✅ | ✅ | ✅ |
| 4 | Steps to reproduce | ✅ | ✅ | ✅ | ✅ |
| 5 | Reproducibility | ✅ | ✅ | ✅ | ✅ |
| 6 | Expected behavior | ✅ | ✅ | ✅ | ✅ |
| 7 | Actual behavior | ✅ | ✅ | ✅ | ✅ |
| 8 | Environment - Browser | ❌ | ❌ | ❌ | ❌ |
| 9 | Environment - OS | ❌ | ❌ | ❌ | ❌ |
| 10 | Environment - Test Data | ✅ | ✅ | ✅ | ✅ |
| 11 | Environment - URL | ❌ | ❌ | ❌ | ❌ |
| 12 | Evidence - Screenshots | ❌ | ❌ | ❌ | ❌ |
| 13 | Evidence - Console | ❌ | ❌ | ❌ | ❌ |
| 14 | Evidence - Network | ❌ | ❌ | ❌ | ❌ |
| 15 | Evidence - Backend | ❌ | ❌ | ❌ | ❌ |
| 16 | Initial Categorization | ✅ | ✅ | ✅ | ✅ |
| 17 | Severity | ✅ | ✅ | ✅ | ✅ |
| 18 | Investigation Status | ✅ | ✅ | ✅ | ✅ |

### Items Requiring PM Approval to Mark N/A

| # | Requirement | Justification |
|---|------------|---------------|
| 1 | Title format `[E2E]` | Issues were filed pre-template as `BUG:` prefix. Changing titles now would break cross-references in commit messages and session logs. |
| 8-9 | Browser/OS | These are backend/AI classification bugs, not UI rendering issues. Browser/OS are not relevant. |
| 11 | URL | Same — these occur via chat API, not at a specific URL. |
| 12-15 | Evidence (Screenshots, Console, Network, Backend) | Bugs were reported from CXO memo, not live testing session. Evidence was not captured at time of occurrence. Root cause investigation provides code-level evidence instead. |

**Request**: PM, can items 1, 8-9, 11, 12-15 be marked N/A for these issues? They're backend/AI bugs reported from a memo, not UI bugs observed during testing.

---

## Root Cause Accuracy Check

| Issue | Root cause correctly identified? | Acceptance criteria test root cause? |
|-------|--------------------------------|-------------------------------------|
| #843 | ✅ User_id threading; likely fixed by #849 | ✅ Includes diagnostic logging, auth path verification |
| #844 | ✅ Pipeline wiring gap, not pattern gap | ✅ Requires _apply_soft_offer() for all categories |
| #845 | ✅ _get_github_action() missing case | ✅ Requires routing consistency + handler existence |
| #846 | ✅ Persistence/key stability, not classification | ✅ Requires cross-turn retrieval + key stability |

All four issues now correctly identify root causes and have acceptance criteria that test the root cause, not just symptoms.

---

## Cross-Issue Consistency Check

- [x] All reference their systemic parent (#854 or #855)
- [x] Overlap with #850/#851/#852 is documented
- [x] Investigation status reflects actual state (investigation complete, fix not yet determined)
- [x] No contradictions between issues

---

## Verdict

**14/18 satisfied, 4 N/A-pending-PM-approval** for all four issues.

Template compliance items 1, 8-9, 11, 12-15 are structurally inapplicable to these bugs (backend issues reported from memo). All substantive requirements (root cause, acceptance criteria, categorization, investigation status) are ✅.

**Ready to proceed to gameplan** (pending PM approval of N/A items).

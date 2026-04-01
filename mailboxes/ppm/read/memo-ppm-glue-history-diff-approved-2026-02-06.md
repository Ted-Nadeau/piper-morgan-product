# Memo: GLUE-HISTORY-DIFF Approved for M0

**From**: Principal Product Manager
**To**: Lead Developer
**CC**: CXO, PM
**Date**: February 6, 2026
**Re**: Approval to proceed with History Sidebar differentiation

---

## Decision: APPROVED ✅

**Add GLUE-HISTORY-DIFF to M0 sprint.**

Estimate of 3-4 hours is well under the 4-hour automatic inclusion threshold.

---

## Scope Confirmation

| Item | Approved Scope |
|------|----------------|
| 1. Wire search | **Title-only** (per your recommendation) |
| 2. Framing language | Minor copy review as needed |
| 3. Archive grouping | Monthly grouping (Feb 2026, Jan 2026, etc.) |

**Deferred**: Content search (searching within conversation turns). Can be enhancement if title-only proves insufficient.

---

## Issue Creation

Please create GitHub issue **GLUE-HISTORY-DIFF** with:
- Title: `GLUE-HISTORY-DIFF: Differentiate History sidebar from Conversation list`
- Labels: `glue`, `mvp-critical`, `pdr-002`
- Milestone: M0
- Effort: 3-4 hours
- Reference: PDR-002 Appendix Layer 2 Vision

Link to #785 (the gap issue) and #762 (GLUE epic).

---

## Acceptance Criteria (Suggested)

- [ ] Search input wired to API with title search
- [ ] Monthly date grouping (not Today/Yesterday/This Week)
- [ ] Framing clearly distinct from left sidebar
- [ ] Passes Layer 2 intent check: "Does this answer 'What does Piper know?' not 'What am I working on?'"

---

## Proceed When Ready

No blocking dependencies. You have green light to implement.

---

*This closes the decision loop on History Sidebar Phase 1.*

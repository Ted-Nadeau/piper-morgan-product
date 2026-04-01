# CANONICAL-GITHUB-CLOSE: Close and Reopen GitHub Issues

**Labels**: `enhancement`, `M1`, `canonical-queries`
**Priority**: P3 — Completes GitHub issue lifecycle symmetry
**Discovered**: #884 Run 4, 2026-03-12
**Source**: CXO failure gap analysis

---

## Problem

Piper can create GitHub issues (Q16) and update them (Q58), but cannot close them (Q45). Users who manage their workflow through Piper will expect issue lifecycle symmetry — if you can open it, you should be able to close it.

## Affected Queries

| Query # | Input | Current Status |
|---------|-------|---------------|
| Q16 | "Create a GitHub issue about testing" | ✅ PASS (when API configured) |
| Q58 | "Update issue #123" | ✅ PASS |
| Q45 | "Close completed issues" | ❌ NOT_IMPL (graceful fallback) |

## Scope

**Single-issue close:**
- "Close issue #123" → Closes via GitHub API
- "Close the testing issue" → Fuzzy match to recent issues, confirm before closing
- Piper confirms: "Closed issue #123: Fix authentication bug"

**Batch close (Q45 as written):**
- "Close completed issues" → Piper identifies issues marked as done/resolved, presents list, user confirms
- This is more complex and may warrant a separate issue or M5 scope

## Acceptance Criteria

- [ ] User can close a specific issue by number ("close #123")
- [ ] User can close by description with confirmation ("close the auth bug" → "Do you mean #123: Fix authentication bug?")
- [ ] Piper confirms closure with issue title
- [ ] Reopen also supported ("reopen #123") for symmetry

## Implementation Notes

The GitHub API `PATCH /repos/{owner}/{repo}/issues/{number}` with `{"state": "closed"}` is all that's needed for the API layer. The work is in the intent routing (recognizing "close" as a GitHub execution action) and the confirmation UX (don't close without confirming, especially for fuzzy matches).

## Sprint Placement

M1 — Single API endpoint + routing fix. GitHub create/update infrastructure already exists. No M3 dependencies.

---

*Drafted by CXO, 2026-03-13*

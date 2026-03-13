# Audit: #844-845-846 Gameplan against gameplan-template.md v9.3

**Date**: 2026-02-25

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Phase -1: Infrastructure verification | ✅ | Infrastructure confirmed via investigation |
| 2 | Phase -1 Part A: Understanding documented | ✅ | All three files and mechanisms identified |
| 3 | Phase -1 Part A.2: Worktree assessment | ✅ | Skip worktree — sequential, tightly coupled |
| 4 | Phase -1 Part B: PM verification | ✅ | Pre-verified via code investigation |
| 5 | Phase -1 Part C: Proceed/Revise decision | ✅ | PROCEED |
| 6 | Phase 0: GitHub investigation | ✅ | All issues verified and rewritten |
| 7 | Phase 0.5: Frontend-Backend contract | ✅ N/A | Backend-only changes, no UI work |
| 8 | Phase 0.6: Data flow verification | ✅ | Full flow tables for all 3 bugs |
| 9 | Phase 0.7: Conversation design | ⚠️ | #846 involves conversation turns but gameplan doesn't include edge case table |
| 10 | Phase 0.8: Post-completion integration | ✅ N/A | No state changes to user records |
| 11 | Phases 1-N: Development work | ✅ | Three phases with specific code changes |
| 12 | Multi-agent deployment plan | ✅ | Single agent justified |
| 13 | Progressive bookending | ⚠️ | Not explicitly scheduled — should note when to update GH issues |
| 14 | Test scope requirements | ✅ | Tests specified per phase |
| 15 | Routing integration tests | ✅ | Explicitly included for #844 and #845 |
| 16 | Wiring integration tests | ✅ | N/A — not multi-layer, same-layer fixes |
| 17 | Cross-validation points | ✅ | Phase 4 with specific grep checks |
| 18 | Phase Z: Final bookending | ✅ | Closure plan for all 3 + systemic parents |
| 19 | STOP conditions | ✅ | Three specific conditions documented |
| 20 | Evidence format | ⚠️ | Evidence format not explicitly specified per phase |
| 21 | Success criteria | ✅ | Implicit in acceptance criteria + tests |
| 22 | #846 _key() caller analysis | ⚠️ | Flagged as "verification needed" but not completed |
| 23 | #845 handler existence check | ⚠️ | Flagged as "needed" but not completed |

**Score**: 17/23 ✅, 5/23 ⚠️, 0/23 ❌, 1 N/A

---

## Fixes Required Before Proceeding

### Fix 1: Phase 0.7 edge case for #846 (item 9)

#846 involves turn-by-turn conversation (offer → response). Add a minimal edge case note:

| User Input | Pending Offer? | Expected Behavior |
|-----------|---------------|-------------------|
| "yes" | Yes | Accept offer, trigger workflow |
| "no" / "not now" | Yes | Decline offer, clear pending |
| "yes" | No (expired/lost) | Classify normally (current behavior, acceptable) |
| "something else" | Yes | Classify normally, clear pending offer |

**Resolution**: This is already handled by `detect_offer_response()` which returns "accept", "decline", or None. No edge case gap. ✅ Resolved — the mechanism handles it correctly, just wasn't documented in gameplan.

### Fix 2: Progressive bookending (item 13)

Add: After each phase implementation, update the corresponding GitHub issue description with evidence before moving to next phase.

### Fix 3: Evidence format (item 20)

Add: Each phase produces evidence as test output (pytest -v) and cross-validation grep results.

### Fix 4: _key() caller analysis (item 22)

**Must resolve before Phase 3.** Need to read all callers of `_key()` to determine if splitting key strategies is needed.

### Fix 5: Handler existence for list_issues_query (item 23)

**Must resolve before Phase 2.** Need to check if `_handle_list_issues_query` exists.

---

## Blocking Items — RESOLVED

### Fix 4: _key() callers (RESOLVED)

`_key()` has 4 callers using 2 different dicts:
- `should_offer()` + `record_offer()` → `_offer_windows` (throttling — needs user scoping)
- `set_pending_offer()` + `get_and_clear_pending_offer()` → `_pending_offers` (turn state — needs session-only)

**Resolution**: Split into `_key()` (throttling, keeps composite) and `_offer_key()` (pending offers, session-only). Update pending offer methods to use `_offer_key()`.

### Fix 5: Handler existence (RESOLVED)

`_handle_list_issues_query` EXISTS at `intent_service.py:2913` and is dispatched at line 1515-1516 via `_handle_query_intent()`.

**Resolution**: Phase 2 scope confirmed — only fix `_get_github_action()`, no handler creation needed.

---

## Audit Verdict

All 5 fixes resolved. **17/23 → 22/23 ✅**, 1 N/A. Ready to proceed to implementation.

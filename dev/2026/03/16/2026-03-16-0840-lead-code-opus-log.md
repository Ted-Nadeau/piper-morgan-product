# Session Log: 2026-03-16-0840-lead-code-opus

**Role**: Lead Developer
**Model**: Claude Code (Opus)
**Date**: Monday, March 16, 2026
**Start Time**: 8:40 AM

**Active pattern families this session**: Completion Theater (045/046/047/049), Investigation (006/041-043/060)

## Standing Rule
**Before every report-in to PM**: merge to main + push to origin. PM reads from local main, not the worktree.

## Session Objectives

1. Assess M1 issues #905, #906, #902, #898, #899 for shovel-readiness
2. Rank by effort low→high, work through the list
3. Run audit cascade on each, fix what's clear
4. Save questions for PM to review later today
5. PM will resume testing later — do not block on PM

## Work Log

### 8:40 AM - Session Start
- Created session log
- Mailbox: empty
- PM is heads down on other work, will resume testing later
- Assessing M1 issues for independent work

### 8:45 AM - Issue Assessment Complete
Ranked 5 issues by effort:
1. **#906** (XS) — Health endpoint auth → Already fixed! Closed with evidence.
2. **#905** (S) — Starlette version drift → Pins already in place. Initially closed prematurely (completion bias — PM caught it). Reopened. Added `make lock` and `make check-deps` targets. Found 25 drifted transitive deps. Left open pending PM decision on sync strategy.
3. **#902** (M) — Close/reopen GitHub issues → Close already worked (QUERY path)! Added reopen handler, fixed misleading "can't close" fallback, 18 new tests. Fuzzy close-by-description deferred.
4. **#899** (M-L) — Off-topic detection → Assessed as feasible, 4-5 days. Needs PM input on aggressiveness, UX, scope. Questions prepared.
5. **#898** (L) — 9 classifier misroutes → 5 of 9 already fixed (pattern ordering fix in commit 23f5946e). Q2 is actually correct (test needs updating). Q23/24/25 need LLM prompt tuning (defer until after #911 floor inversion).

### 9:30 AM - Stale Test Cleanup
- Fixed `test_contextual_fallbacks_886`: "can't close issues yet" → "I can close issues" (stale after #902)
- Fixed `test_conversational_floor` (2 tests): assert "action" → assert "capabilities" (stale after floor prompt rewrite)
- Full suite: 1171 passed, 0 failed

### 9:45 AM - All Merged and Pushed
Everything on main. PM questions saved to `dev/active/pm-questions-899-898.md`.

### 10:15 AM - #902 Fuzzy Close Complete
- Implemented fuzzy close/reopen by description (word overlap matching)
- Single match → confirmation prompt, multiple → list options, none → ask for number
- 34 total tests for close/reopen feature (16 new for fuzzy)
- Fixed stale test in test_github_query_handlers.py
- Full suite: 1187 passed, 0 failed
- Merged and pushed to main

### Work Complete — Waiting for PM

**Completed today:**
| Issue | Status | Notes |
|-------|--------|-------|
| #906 | Closed | Already fixed, closed with evidence |
| #905 | Reopened, infrastructure added | `make lock` + `make check-deps`. 25 drifted transitive deps found. Needs PM decision on sync strategy. |
| #902 | Implementation complete | Reopen handler, fuzzy matching, fixed fallback. 34 tests. All acceptance criteria met except PM testing. |
| #898 | 5 of 9 already fixed | Q2 test expectation wrong. Q23/24/25 need prompt tuning (defer to post-#911). |
| #899 | Assessed | Feasible (~4-5 days). Questions prepared for PM. |

**Stale tests fixed:** 4 total (from #902 fallback change and floor prompt rewrite)

### Discovered Work
- #905 needs PM decision: sync requirements.txt to installed versions, or force-reinstall to match pins?
- #898 Q23/24/25 prompt tuning should wait for #911 floor inversion
- Stale tests from recent changes (found and fixed 4)

### Questions Saved for PM
See `dev/active/pm-questions-899-898.md`

---

## Session Resumed (after compaction)

### #913 Phase 2 Audit Fixes — All Complete

Completed remaining 5 audit fix items:

1. **✅ Core IDENTITY rewrite** — Done before compaction
2. **✅ Continuation rate logging** — Added `last_response_was_floor` / `last_floor_category` to `ConversationContext`. All 3 floor paths (action gate, unknown, guidance) set the flag. `process_intent()` checks on next request and logs `floor_continuation_detected`. 3 new tests.
3. **✅ Q2 test expectation** — Updated `test_concierge.py` from IDENTITY → DISCOVERY for "what can you do?" queries.
4. **✅ Q16 investigation** — Confirmed test env artifact (missing GITHUB_TOKEN). No code fix needed.
5. **✅ Quality verification queries** — 10 queries from addendum documented in `913-phase2-audit.md`.

**Test results**: 1235 passed, 0 failed (intent service suite)

**Committed**: `feat(#913): Phase 2 Action Gate, Context Assembler, and audit fixes` + style fixup
**Merged to main and pushed**: ✅

### Audit Status
All 21 requirements from synthesis memo + addendum now fully met. Audit document updated with all green checkmarks.

### Remaining for PM
- **#902 PM testing**: Close/reopen features await verification
- **#899 implementation**: PM approved all 4 decisions; ready to start

---

## PM QA Testing — 3:31 PM

PM tested Q33, Q43, Q62 from the verification queries. All three failed. Five-whys investigation launched for each plus a calendar credential concern.

### Issues Filed

| Issue | Query | Root Cause | Classification |
|-------|-------|-----------|----------------|
| #914 | Q16: GitHub integration test needs GITHUB_TOKEN | Test env missing credentials | Test infra |
| #915 | Q33: "Find time for a 1:1" → raw data dump | QUERY not floor-routed + missing action sub-pattern from #901 | Incomplete wiring |
| #916 | Q43: "What's blocking the milestone?" → bare stub label | analyze_blockers has no handler, two layers of placeholder | Unfinished implementation |
| #917 | Calendar credential leak (alfamux sees other user's meetings) | Legacy keychain fallback reads global token when no per-user key exists | Security — incomplete fix from #734/#843 |
| #918 | Q62: "Check my calendar for conflicts" → success + apology | Multi-intent false positive from pattern overlap, orchestrator can't handle QUERY | Pattern overlap + architectural gap |

### Meta-Analysis: Why the Audit Cascade Missed These

PM raised a valid process question. Root causes of the process gap:

1. **Verification queries tested un-migrated categories**: Q33/Q43/Q62 test QUERY, ANALYSIS, and TEMPORAL — categories scheduled for Phase 3+. The audit correctly marked Phase 2 requirements as met, but the verification queries assumed those categories would also improve. The audit should have flagged: "these queries will still hit old handlers."

2. **No adversarial validation against live system**: All 48 tests were unit tests with mocked dependencies. No e2e test sent actual queries to a running server. The excellence flywheel calls for adversarial validation — we didn't do it.

3. **The 75% pattern on #734/#843**: Calendar multi-tenancy was "fixed" but the legacy fallback was left in. No credential isolation test exists.

4. **Pattern additions without handler wiring (#901)**: Pre-classifier patterns were added for `analyze_blockers` and scheduling queries, but no corresponding handlers or action sub-routes were built.

### Systemic Re-Audit — 4:24 PM

PM asked the right question: "Did our five whys include wondering if they represent a category or pattern?"

**Shared structural root cause: "Extend without verifying"**

All five bugs follow the same meta-pattern:
1. New capability added at one layer (classification patterns, user-scoped auth)
2. Downstream layer not updated to match (handler implementation, legacy auth removal)
3. Silent fallback absorbs the gap (stub responses, global keychain key)
4. No contract or test exists to detect the mismatch
5. System appears to work until a human sends a real query

**Two structural failures:**
1. **No contract between classification and handling** — pre-classifier emits action strings, handler chain matches with if/elif. No registry, no verification. 3+ actions fall to stubs today.
2. **Tests verify routing, not response quality** — zero tests assert on what the user sees. All four bugs pass the existing test suite.

**Scale (from codebase audit):**
- 3 pre-classifier actions fall to generic stubs (`analyze_blockers`, `contextual_query`, `get_feature_info`)
- 8+ pattern overlaps between CALENDAR_QUERY and TEMPORAL in multi-intent detection
- Multiple legacy fallback patterns in security-sensitive paths

**Methodological note written**: `dev/active/methodological-note-classification-handling-contract.md`
For discussion with Chief Architect and CIO. Covers: action registry, response quality smoke tests, fail-loud stubs, legacy removal discipline, multi-intent deduplication.

**PM decisions pending**: How to address the systemic issues before fixing individual bugs.

### Systemic Fix Implementation — 4:41 PM

PM approved Option A (route stub actions to floor). Implemented three workstreams:

**1. Action Registry** (`services/intent_service/action_registry.py`):
- All 34 (category, action) pairs from pre-classifier cataloged
- `ActionDisposition` enum: CANONICAL, FLOOR, HANDLER, WORKFLOW
- `validate_registry_coverage()` — startup check that fails fast on missing entries
- Example messages per action for smoke test generation
- Previously-stubbed actions (`get_feature_info`, `analyze_blockers`) marked FLOOR

**2. Stub-to-Floor Routing**:
- `_handle_generic_query` → now routes to conversational floor (was: "Query processed successfully: {action}")
- `_handle_analysis_intent` else → now routes to conversational floor (was: "Analysis processed: {action}")
- Fixes #915, #916 directly

**3. Multi-intent Subsumption Filter** (`pre_classifier.py`):
- `_apply_subsumption_filter()` removes phantom intents from pattern overlap
- CALENDAR_QUERY subsumes TEMPORAL, PRIORITY subsumes GUIDANCE, DISCOVERY subsumes GUIDANCE
- Fixes #919 directly

**Tests**: 21 new (registry coverage 4, disposition 5, stub routing 4, subsumption 8). 1256 total passing.
**Committed and pushed to main**: ✅

**CIO cover note**: Delivered to `mailboxes/cio/inbox/`

### #899 — Already Complete
PM directed "Proceed with #899 now" at 4:48 PM. Investigation found it was already fully implemented:
- `services/process/off_topic.py` — detection module with all 3 process types
- Registry integration wired in `services/process/registry.py`
- 63 tests passing in `tests/unit/services/process/test_off_topic.py`
- Already on main (commit `3eb500ed`)
- Added implementation evidence comment to GitHub issue #899
- Hit STOP condition #3 ("Pattern/class/function already exists")

---

## Session Resumed (after 2nd compaction)

### Status: Waiting for PM Retest
All systemic fixes merged to main. PM will retest Q33, Q43, Q62 on restarted server.

### 4:56 PM — #914 GitHub Integration Tests — Complete

PM directed: proceed to #914, then #917, then regroup.

**Changes:**
- Conftest loads `GITHUB_TOKEN` from keychain (matching OpenAI/Anthropic pattern)
- Fallback to `gh auth token` CLI when keychain has no token stored
- `@pytest.mark.github` marker registered in pytest.ini + pyproject.toml
- Auto-skip github-marked tests when no token available
- 5 integration tests: auth, scopes, repo access, issue listing, token format
- All 5 pass (gh CLI token authenticated as mediajunkie)

**Discovered work filed**: #920 — 3 pre-existing httpx `AsyncClient(app=)` failures

**Tests**: 1261 passed (1256 existing + 5 new)
**Merged and pushed to main**: ✅

### 5:05 PM — #917 Calendar Credential Leak — Fixed

**Root cause confirmed**: Line 272 of `google_calendar_adapter.py` fell back to global `google_calendar` keychain key when no user-scoped key existed. Line 1317 of `setup.py` stored to global key when `user_id` was None.

**Fixes:**
1. Removed legacy fallback in adapter — now returns `calendar_connected=False` when no user-scoped key exists
2. OAuth callback now rejects token storage when `user_id` is missing (returns error redirect instead of storing to global key)
3. Deleted global `google_calendar` keychain entry (contained real refresh token starting with `1//01HFj7F...`)
4. Added 5 credential isolation tests (adapter: 3, OAuth callback: 2)
5. Fixed 2 stale tests that expected the old global key pattern

**Tests**: 1302 passed (including 5 new isolation tests)
**Merged and pushed to main**: ✅

---

## 6:29 PM — Session End: Issue Closure Sweep

PM wrapping up for the day, asked to verify all issues closed properly.

### Issues closed with full evidence:
| Issue | Title | Status |
|-------|-------|--------|
| #913 | FLOOR-INVERSION-P2: Action Gate + Context Assembler | ✅ Closed |
| #899 | Off-topic detection (Layer C) | ✅ Closed |
| #914 | GitHub integration tests with token | ✅ Closed |
| #915 | Calendar raw data dumps | ✅ Closed (partial fix, full in Phase 3) |
| #916 | analyze_blockers stub label | ✅ Closed |
| #917 | Calendar credential leak | ✅ Closed |
| #918 | Multi-intent false positive | ✅ Closed |
| #919 | Phantom multi-intent (dup of #918) | ✅ Closed |

### Still open:
- **#902** — Close/reopen GitHub issues: awaiting PM verification

### Pending for PM (2026-03-17)
- Retest verification queries (Q33, Q43, Q62) with new fixes
- #902 close/reopen PM verification

---

## 9:33 PM — #920 httpx Pin Fix

PM asked to look at #920 before wrapping up. Investigated and presented 3 options (pin httpx, upgrade full stack, hybrid). PM approved Option A (pin).

- Pinned `httpx>=0.27.0,<0.28` in requirements.txt
- All 3 failing tests now pass: `test_expired_token_returns_401`, `test_no_auth_on_conversations_endpoint`, `test_create_list_accepts_json_body`
- Filed #921 for the proper long-term fix (fastapi/starlette/httpx full upgrade)
- Closed #920 with evidence
- Merged and pushed to main (commit `646c33f4`)

---

## Day Summary

**Massive day.** Started at 8:40 AM, ending ~9:40 PM. Key accomplishments:
1. **#913 Phase 2** — Action Gate, Context Assembler, category migration (complete)
2. **#899** — Off-topic detection verified complete (already existed)
3. **Five Whys investigations** — Q33, Q43, Q62 bugs root-caused → #915, #916, #918, #919
4. **#917** — Calendar credential leak found and fixed
5. **#914** — GitHub integration test infrastructure
6. **Systemic analysis** — "Extend without verifying" meta-pattern documented
7. **Action registry** — 34 (category, action) pairs mapped
8. **Stub-to-floor routing** — Dev stubs eliminated
9. **Multi-intent subsumption** — Phantom intent deduplication
10. **#920** — httpx version pin for test compatibility
11. **9 issues closed** with full evidence, 1 new filed (#921)

**Discovered work filed**: #914, #915, #916, #917, #918, #919, #920, #921 (8 issues)

**Open items for next session**:
- PM retest of Q33, Q43, Q62
- #902 PM verification
- #921 framework upgrade (low priority, when sprint allows)

# Gameplan: #849 SEC-KEYCHAIN — Non-Scoped Keychain Key Audit & Fix

**Issue**: #849
**Author**: Lead Developer
**Date**: 2026-02-25

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL on port 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] KeychainService: Supports `username` parameter for user-scoped keys (confirmed)
- [x] Existing user-scoped patterns: Calendar OAuth, Slack OAuth, user API keys all use `username=user_id` (confirmed)
- [x] Missing: GitHub token storage, connection test endpoints, deletion operations (confirmed via audit)

**My understanding of the task**:
- I need to fix 13 non-scoped keychain sites across 4 categories
- The critical bug is Category B: GitHub token stored globally but retrieved per-user (silent failure)
- Categories C and D are wrong/legacy key names in connection tests and deletion
- Category A requires threading user_id through calendar-related method signatures

### Part A.2: Work Characteristics Assessment

Worktrees ADD value when:
- [x] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes — possibly, but changes are focused

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [x] Tightly coupled files requiring atomic commits

**Assessment:**
- [x] **SKIP WORKTREE** — Overhead criteria dominate. Changes are in 3 files (settings_integrations.py, integrations.py, service handlers). Most fixes are 1-3 line changes. Subagents can work on isolated categories without worktrees since files don't overlap much.

### Part B: PM Verification Required

**Already verified by Lead Developer (investigation completed 2026-02-24)**:
- Full inventory of 13 sites completed via codebase audit
- Each site confirmed with exact line numbers and current vs. correct key patterns
- #734 root cause analysis complete — gaps are in runtime paths, not infrastructure
- No prior work on these specific sites (they were missed by #734)

**PM context**: PM was present during the 2026-02-24 systemic analysis session where all 13 sites were identified. PM reviewed the findings and directed the issue filing. Explicit re-verification of infrastructure understanding is not required — PM can validate during execution.

### Part C: Proceed/Revise Decision

- [x] **PROCEED** — Understanding is verified by exhaustive codebase audit

---

## Phase 0: Investigation (COMPLETE)

Investigation was completed during 2026-02-24 systemic analysis session. Results documented in:
- Issue #849 body (full inventory with line numbers)
- `dev/2026/02/24/2026-02-24-1743-lead-code-opus-log.md` (session log)
- Exploration subagent report (comprehensive keychain call inventory)

No additional investigation needed — all 13 sites are confirmed with exact file/line/key information.

---

## Phase 0.5: Frontend-Backend Contract Verification

**Not applicable** — this is backend-only work. No new endpoints or frontend changes.

---

## Phase 0.6: Data Flow & Integration Verification (CRITICAL)

This phase is the CORE of why #734 missed these sites. We trace each integration's data flow end-to-end.

### Part A: Data Flow Requirements — Per Integration

#### GitHub Token Flow
| Layer | Needs user_id? | Has user_id? | Source |
|-------|----------------|--------------|--------|
| Settings route (store) | YES | YES — `current_user.sub` available | JWT middleware |
| Settings route (retrieve) | YES | YES — `current_user.sub` available | JWT middleware |
| Settings route (delete) | YES | YES — `current_user.sub` available | JWT middleware |
| Connection test `_test_github()` | YES | NO — function takes no params | **GAP** — must add user_id param |
| Config service retrieval | YES | YES — uses `username=user_id` | Method parameter |
| Intent handler | YES | YES — `user_id` in method params | Process context |

**GitHub Store/Retrieve Mismatch**:
- STORE: `settings_integrations.py:1650` → `store_api_key("github_token", token)` — NO username
- RETRIEVE: `github/config_service.py:167` → `get_api_key("github_token", username=user_id)` — HAS username
- Result: **silent failure** — stored globally, retrieved per-user, never found

#### Slack Token Flow
| Layer | Needs user_id? | Has user_id? | Source |
|-------|----------------|--------------|--------|
| OAuth handler (store) | YES | YES — `f"slack_bot_{user_id}"` | OAuth callback |
| Config service (retrieve) | YES | YES — `username=user_id` | Method parameter |
| Connection test `_test_slack()` | YES | NO — retrieves `"slack"` | **GAP** — wrong key name AND no user_id |
| Settings route (delete) | YES | NO — deletes `"slack_bot_token"` | **GAP** — wrong key name AND no user_id |

**Slack Key Name Chaos**:
- STORE: `"slack_bot_{user_id}"` via OAuth handler
- RETRIEVE (config service): `"slack_bot"` + `username=user_id` (different format but KeychainService may handle this)
- RETRIEVE (connection test): `"slack"` (totally wrong key name)
- DELETE: `"slack_bot_token"` (yet another wrong key name)

**STOP CONDITION TRIGGERED** (Phase 1 finding): KeychainService `_get_key_name` verified:

```python
# _get_key_name(provider, username):
#   with username: f"{username}_{provider}_api_key"
#   without:       f"{provider}_api_key"

# Slack OAuth STORES:  store_api_key(f"slack_bot_{user_id}", token)
#   → keyring: "slack_bot_{user_id}_api_key"

# Slack config RETRIEVES: get_api_key("slack_bot", username=user_id)
#   → keyring: "{user_id}_slack_bot_api_key"

# THESE ARE DIFFERENT KEYS. Slack is ALSO silently broken.
```

**Resolution**: Standardize on the `username` parameter approach (ADR-058 design). Fix Slack OAuth handler to use `store_api_key("slack_bot", token, username=user_id)` instead of f-string in provider name. This adds the Slack OAuth handler to the fix scope (Category E below).

**NEW Category E: OAuth Handler Store Using Wrong Key Pattern (2 sites)**

| # | File | Line | Current | Correct |
|---|------|------|---------|---------|
| E1 | `services/integrations/slack/oauth_handler.py` | 535 | `store_api_key(f"slack_bot_{user_id}", bot_token)` | `store_api_key("slack_bot", bot_token, username=user_id)` |
| E2 | `services/integrations/slack/oauth_handler.py` | 550 | `store_api_key(f"slack_user_{user_id}", user_token)` | `store_api_key("slack_user", user_token, username=user_id)` |

**Updated total: 15 sites** (13 original + 2 OAuth handler fixes)

#### Notion Token Flow
| Layer | Needs user_id? | Has user_id? | Source |
|-------|----------------|--------------|--------|
| Settings route (store) | YES | Unclear — need to check | JWT middleware |
| Config service (retrieve) | YES | YES — `username=user_id` | Method parameter |
| Connection test | YES | NO — retrieves `"notion"` without username | **GAP** |
| Settings route (delete) | YES | NO — deletes `"notion"` without username | **GAP** |

#### Calendar Token Flow
| Layer | Needs user_id? | Has user_id? | Source |
|-------|----------------|--------------|--------|
| OAuth storage | YES | YES — `f"google_calendar_{user_id}"` | OAuth callback |
| Adapter retrieval | YES | YES — user-scoped + legacy fallback (#843) | Constructor param |
| Router calls in handlers | YES | 4 YES, 5 NO | **GAPs** = Category A sites |

### Part B: Integration Points Checklist

For Category A (calendar router calls), each call site must be verified:

| Caller | CalendarIntegrationRouter() | user_id Available Upstream? | Threading Difficulty |
|--------|---------------------------|----------------------------|---------------------|
| `canonical_handlers._get_calendar_context()` | Line 1907 | YES — `_handle_temporal_query` has user_id | Low — add param |
| `conversation_handler._get_calendar_summary()` | Line 131 | PARTIAL — handler has session but not explicit user_id | Medium — need to source from session |
| `intent_service._handle_attention_query()` | Line 3824 | YES — `process_message` has user_id, but `_handle_attention_query` doesn't | Low-Medium — thread from parent |
| `CalendarPlugin.__init__` | Line 29 | NO — plugin instantiated at startup | Document as system-context |
| `create_calendar_integration()` | Line 482 | NO — factory function | Add optional param |

### Part C: Pattern Adaptation Notes

**This issue follows the #734 pattern but with a critical difference:**

| Aspect | #734 Approach | This Implementation | Why Different? |
|--------|--------------|---------------------|----------------|
| Audit scope | By layer (routes → services → repos) | By user flow (end-to-end per integration) | Catches seam bugs |
| Test strategy | Infrastructure isolation tests | Flow-level tests + CI guard | Prevents regression |
| Fix approach | Comprehensive architecture redesign | Targeted fixes to 13 specific sites | Infrastructure already exists |

**Potential Pitfalls from Differences:**
- [ ] Slack key name resolution: Need to verify `"slack_bot"` + username vs `f"slack_bot_{user_id}"` are equivalent
- [ ] Connection test functions are called from routes — need to ensure user_id is available at the call site
- [ ] CalendarPlugin is initialized at startup without user context — may need different approach

### STOP Condition from Phase 0.6

**MUST VERIFY BEFORE PHASE 1**: How does KeychainService resolve `store_api_key("slack_bot", token, username="user123")` vs `store_api_key("slack_bot_user123", token)`? If these store to different underlying keys, we have a deeper architectural issue in Slack token storage.

---

## Phase 0.7: Conversation Design

**Not applicable** — no multi-turn conversation changes.

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects Checklist

| Side Effect | Scope | Verified? |
|-------------|-------|-----------|
| GitHub tokens stored per-user | settings_integrations.py | [ ] |
| GitHub connection test works per-user | integrations.py | [ ] |
| Slack connection test works per-user | integrations.py | [ ] |
| Notion connection test works per-user | settings_integrations.py | [ ] |
| Slack disconnect removes correct key | settings_integrations.py | [ ] |
| Notion disconnect removes correct key | settings_integrations.py | [ ] |
| Calendar handlers pass user_id | 5 service files | [ ] |
| CI guard prevents regression | scripts/ + CI | [ ] |

### Downstream Behavior Changes

| Feature | Before Fix | After Fix |
|---------|-----------|-----------|
| GitHub "show my issues" | Silent failure (token not found) | Works for connected users, "not connected" for others |
| Slack connection test | Tests wrong key ("slack") | Tests correct user-scoped key |
| GitHub connection test | Tests wrong key ("github") | Tests correct user-scoped key |
| Notion connection test | Tests global key | Tests user-scoped key |
| Slack disconnect | Deletes wrong key ("slack_bot_token") | Deletes correct user-scoped key |
| Calendar in greeting | Uses global token | Uses user-scoped token (with fallback) |

---

## Phase 1: KeychainService Resolution Verification (BLOCKING)

**Objective**: Verify how KeychainService maps key name + username to storage, to resolve the Slack key name question from Phase 0.6.

**Tasks**:
- [ ] Read KeychainService `store_api_key` and `get_api_key` implementations
- [ ] Determine: does `store_api_key("slack_bot", token, username="user123")` store the same key as `store_api_key("slack_bot_user123", token)`?
- [ ] If NO: document the mismatch and determine which pattern is canonical
- [ ] If YES: proceed with confidence

**Deliverables**:
- Finding documented in session log
- Decision on canonical key naming pattern

**STOP Condition**: If KeychainService uses incompatible naming between f-string and username approaches, STOP and escalate — this is a deeper architectural bug.

---

## Phase 2: GitHub Token Fixes (Category B — CRITICAL)

**Objective**: Fix the silent auth failure. This is the highest-priority fix.

**Tasks**:
- [ ] `settings_integrations.py:1650`: Add `username=current_user.sub` to `store_api_key`
- [ ] `settings_integrations.py:1736`: Add `username=current_user.sub` to `get_api_key`
- [ ] `settings_integrations.py:1686`: Add `username=current_user.sub` to `delete_api_key`
- [ ] Write unit test: GitHub token lifecycle with user isolation
- [ ] Run existing GitHub settings tests — verify no regressions

**Deliverables**:
- Modified `web/api/routes/settings_integrations.py`
- Tests in `tests/unit/web/api/routes/test_settings_github.py`

**Bookend**: `gh issue comment 849 -b "Phase 2 complete: GitHub store/retrieve/delete fixed. [test output]"`

---

## Phase 3: Connection Test + Deletion Fixes (Categories C + D)

**Objective**: Fix connection tests and disconnect operations.

**Tasks**:
- [ ] C1: Update `_test_slack()` in `integrations.py:478` — add user_id param, use correct key
- [ ] C2: Update `_test_github()` in `integrations.py:516` — add user_id param, use correct key
- [ ] C3: Update Notion check in `settings_integrations.py:1261` — add `username=current_user.sub`
- [ ] D1: Update Slack disconnect in `settings_integrations.py:440` — correct key + username
- [ ] D2: Update Notion disconnect in `settings_integrations.py:1365` — add `username=current_user.sub`
- [ ] Update callers of `_test_slack()` and `_test_github()` to pass user_id
- [ ] Write tests for connection test key correctness
- [ ] Write tests for disconnect key correctness

**Deliverables**:
- Modified `web/api/routes/integrations.py`
- Modified `web/api/routes/settings_integrations.py`
- Tests

**Bookend**: `gh issue comment 849 -b "Phase 3 complete: Connection tests + deletions fixed. [test output]"`

---

## Phase 4: Calendar Router user_id Threading (Category A)

**Objective**: All CalendarIntegrationRouter instantiations pass user_id where available.

**Tasks**:
- [ ] A1: Add `user_id` param to `_get_calendar_context()` in canonical_handlers, update callers
- [ ] A2: Add `user_id` to `_get_calendar_summary()` in conversation_handler — source from session or request context
- [ ] A3: Thread `user_id` to `_handle_attention_query()` in intent_service from its caller
- [ ] A4: Document `CalendarPlugin.__init__` as system-context with TODO comment
- [ ] A5: Add optional `user_id` param to `create_calendar_integration()` factory
- [ ] Write tests verifying user_id reaches CalendarIntegrationRouter for each call site

**Deliverables**:
- Modified `services/intent_service/canonical_handlers.py`
- Modified `services/conversation/conversation_handler.py`
- Modified `services/intent/intent_service.py`
- Modified `services/integrations/calendar/calendar_plugin.py` (comment only)
- Modified `services/integrations/calendar/calendar_integration_router.py`
- Tests

**Bookend**: `gh issue comment 849 -b "Phase 4 complete: All 5 calendar router calls pass user_id. [test output]"`

---

## Phase 5: CI Grep Guard

**Objective**: Prevent regression with automated detection.

**Tasks**:
- [ ] Create `scripts/check-keychain-scoping.sh`
- [ ] Include allowlist for legitimate global keys (LLM providers, app credentials, legacy fallback)
- [ ] Add to CI workflow or pre-commit
- [ ] Verify it catches all 13 original non-scoped patterns
- [ ] Verify it passes on the fixed codebase

**Deliverables**:
- `scripts/check-keychain-scoping.sh`
- CI integration

---

## Phase 6: Flow-Level Isolation Tests

**Objective**: Test end-to-end user flows, not just infrastructure.

**Tasks**:
- [ ] GitHub flow: User A connects → queries → gets results; User B queries → "not connected"
- [ ] Slack flow: Connection test with User A token → works; Connection test without → fails
- [ ] Notion flow: Connection test with User A key → works; Connection test without → fails
- [ ] Calendar flow: User A authenticated → calendar query → correct token used
- [ ] Disconnect flow: User A disconnects → User A's key gone → User B's key intact

**Deliverables**:
- `tests/security/test_integration_flow_isolation.py`

---

## Phase Z: Final Bookending & Handoff

- [ ] All 13 sites remediated (verified by grep)
- [ ] CI guard passing
- [ ] All tests passing (new + existing)
- [ ] Session log complete with evidence
- [ ] GitHub issue #849 updated with completion matrix
- [ ] PM approval requested

---

## Multi-Agent Deployment Plan

### Assessment

Given PM's instruction for exhaustive handling with subagent logging:

**Categories B+C+D** (Phases 2-3): Route-level fixes in `settings_integrations.py` and `integrations.py`. These are focused changes to a small number of files. Best handled by a single **Programmer subagent** with its own session log.

**Category A** (Phase 4): Service-level changes across 5 files, requiring method signature changes and caller updates. More complex. Best handled by a second **Programmer subagent** with its own session log.

**Phase 1** (KeychainService verification): Quick investigation. Lead does this first — it's a blocking question.

**Phases 5-6** (CI guard + flow tests): Lead handles after subagents complete, since these verify the subagents' work.

### Agent Deployment Map

| Phase | Agent | Scope | Log Required? | Evidence Required |
|-------|-------|-------|---------------|-------------------|
| 1 | Lead Developer | KeychainService verification | In lead log | Finding documented |
| 2-3 | Programmer Subagent A | GitHub/Slack/Notion route fixes (B+C+D) | YES — own session log | Modified files list, test output (full pytest -v), any blockers |
| 4 | Programmer Subagent B | Calendar router user_id threading (A) | YES — own session log | Modified files list, test output (full pytest -v), any blockers |
| 5 | Lead Developer | CI grep guard | In lead log | Script + CI passing |
| 6 | Lead Developer | Flow-level isolation tests | In lead log | Test file + output |
| Z | Lead Developer | Verification + handoff | In lead log | Full completion matrix |

### Subagent Handoff Quality Checklist

Before accepting handoff from either subagent:
- [ ] All acceptance criteria for their category addressed
- [ ] Test output provided (full `pytest -v` output, not just "tests pass")
- [ ] Files modified list included (exact paths)
- [ ] Session log created at `dev/2026/02/25/` with timestamped entries
- [ ] Blockers explicitly stated (if any)
- [ ] No existing tests broken (full test suite output for changed areas)

### Verification Gates

- [ ] Phase 1: KeychainService naming resolution confirmed
- [ ] Phases 2-3: All Category B+C+D sites fixed, tests passing
- [ ] Phase 4: All Category A sites fixed, tests passing
- [ ] Phase 5: CI grep guard catches non-scoped patterns
- [ ] Phase 6: Flow-level tests all passing
- [ ] Phase Z: Full test suite passing, no regressions

---

## STOP Conditions

- KeychainService `username` parameter uses incompatible naming with f-string approach
- Any existing test fails after changes
- `current_user` not available at a call site where user_id is needed
- Connection test functions are called from contexts without user_id
- Uncertainty about canonical key name for any integration

---

_Gameplan written: 2026-02-25 by Lead Developer_

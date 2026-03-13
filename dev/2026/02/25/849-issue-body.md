# SEC-KEYCHAIN: Comprehensive Non-Scoped Keychain Key Audit & Fix

**Priority**: P1 (High)
**Labels**: `bug`, `component: integration`, `P1`
**Milestone**: Alpha Testing
**Epic**: Security & Data Isolation
**Related**: #734 (SEC-MULTITENANCY, completed but gaps remain), #843 (calendar auth fix), #839 (user-scoped keys)

---

## Problem Statement

### Current State

Issue #734 (SEC-MULTITENANCY) was a 7-phase, 94-test multi-tenancy isolation effort completed 2026-01-30. It was marked COMPLETE with all acceptance criteria checked. However, CXO testing on 2026-02-22 revealed that calendar authentication still used non-scoped keys (#843), which was fixed. Systemic analysis on 2026-02-24 revealed **additional non-scoped sites across Slack, GitHub, and Notion integrations**, plus a critical store/retrieve key mismatch for GitHub.

### Impact

- **Blocks**: Multi-user alpha testing — User B may silently see User A's integration data, or integrations silently fail because tokens stored globally can't be found by user-scoped retrieval
- **User Impact**: GitHub integration is likely broken for any user whose token was stored after #734's config service changes (stored globally at `"github_token"`, retrieved per-user with `username=user_id` — silent miss). Slack/Notion have similar inconsistencies.
- **Technical Debt**: Every new integration will inherit the broken pattern unless we add a regression gate

### Strategic Context

We have attempted multi-tenant prep three times now (#734 original, #839 cookie fix, #843 calendar fix) and keep missing sites. The structural reason: **#734 audited by architectural layer** (routes, config services, repositories) **but not by user flow** (user asks question — handler — service — adapter — keychain). Multi-tenancy bugs live in the seams between layers, not within them.

This issue takes a different methodology: **audit by user flow, then add a CI grep guard so we can't regress.**

---

## Goal

**Primary Objective**: Every integration token retrieval and storage path uses user-scoped keys, with a CI guard preventing regression.

**Example User Experience**:
```
BEFORE (current broken state for GitHub):
1. User A connects GitHub via settings page
2. Token stored as keychain key "github_token" (global)
3. User A asks "show my open issues"
4. GitHubConfigService.get_github_token() calls get_api_key("github_token", username=user_id)
5. Keychain looks for USER-SCOPED key - not found (was stored globally)
6. GitHub query fails silently

AFTER:
1. User A connects GitHub via settings page
2. Token stored as keychain key "github_token" with username=user_a_id (user-scoped)
3. User A asks "show my open issues"
4. GitHubConfigService.get_github_token() calls get_api_key("github_token", username=user_id)
5. Keychain finds user-scoped key - returns User A's token
6. GitHub query succeeds
7. User B asks "show my open issues" - gets "GitHub not connected"
```

**Not In Scope** (explicitly):
- LLM provider keys (openai, anthropic) — these are app-level, correctly global
- OAuth app credentials (client_id/client_secret for all integrations) — these are app-level, correctly global
- Workspace-level isolation (future enterprise feature)
- Migration of existing global tokens — alpha users can re-authenticate

---

## What Already Exists

### Infrastructure that works

1. **KeychainService** (`services/infrastructure/keychain_service.py`) — supports `username` parameter for user-scoped keys
2. **UserAPIKeyService** (`services/security/user_api_key_service.py`) — correctly implements user-scoped LLM key storage with audit logging
3. **Slack OAuth handler** (`services/integrations/slack/oauth_handler.py:529-550`) — correctly stores as `f"slack_bot_{user_id}"` / `f"slack_user_{user_id}"`
4. **Calendar OAuth storage** (`web/api/routes/setup.py:1172`, `settings_integrations.py:963`) — correctly stores as `f"google_calendar_{user_id}"`
5. **Calendar adapter authentication** (`google_calendar_adapter.py:268`) — correctly retrieves with user-scoped key first (fixed in #843)
6. **GitHub config service retrieval** (`github/config_service.py:167`) — correctly uses `username=user_id`
7. **Notion config service retrieval** (`notion/config_service.py:192`) — correctly uses `username=user_id`
8. **Slack config service retrieval** (`slack/config_service.py:215`) — correctly uses `username=user_id`
9. **CLI tokens** — fully user-scoped, no issues
10. **ADR-058** — documents the multi-tenancy isolation architecture

### What's Missing

1. **GitHub token STORAGE is global** — stored as `"github_token"` without username, but retrieved with username — **silent auth failure**
2. **GitHub token deletion is global** — deletes `"github_token"` without username
3. **GitHub token retrieval in settings page is global** — `settings_integrations.py:1736` uses `get_api_key("github_token")` without username
4. **Slack connection test uses wrong key** — `integrations.py:478` retrieves `"slack"` (not `"slack_bot"` or user-scoped)
5. **Slack deletion uses wrong key** — `settings_integrations.py:440` deletes `"slack_bot_token"` (not `"slack_bot"` + user-scoped)
6. **GitHub connection test uses wrong key** — `integrations.py:516` retrieves `"github"` (not `"github_token"` or user-scoped)
7. **Notion connection test is global** — `settings_integrations.py:1261` retrieves `"notion"` without username
8. **Notion deletion is global** — `settings_integrations.py:1365` deletes `"notion"` without username
9. **5 CalendarIntegrationRouter() calls without user_id** — in services layer, falling back to legacy global key
10. **No CI grep guard** — nothing prevents new code from introducing non-scoped patterns

---

## Complete Inventory of Non-Scoped Sites

### Category A: CalendarIntegrationRouter Without user_id (5 sites)

Default to `user_id="system"` — adapter falls back to legacy non-scoped `google_calendar` key.

| # | File | Line | Method | user_id Available? |
|---|------|------|--------|--------------------|
| A1 | `services/intent_service/canonical_handlers.py` | 1907 | `_get_calendar_context()` | No — no user_id param |
| A2 | `services/conversation/conversation_handler.py` | 131 | `_get_calendar_summary()` | No — greeting path |
| A3 | `services/intent/intent_service.py` | 3824 | `_handle_attention_query()` | No — method lacks it |
| A4 | `services/integrations/calendar/calendar_plugin.py` | 29 | `CalendarPlugin.__init__` | No — plugin init |
| A5 | `services/integrations/calendar/calendar_integration_router.py` | 482 | `create_calendar_integration()` | No — factory |

### Category B: GitHub Token Store/Retrieve/Delete Mismatch (3 sites)

Config service retrieves per-user, but settings routes store/retrieve/delete globally — **silent auth failure**.

| # | File | Line | Operation | Key Used | Should Be |
|---|------|------|-----------|----------|-----------|
| B1 | `web/api/routes/settings_integrations.py` | 1650 | `store_api_key` | `"github_token"` (global) | `"github_token"` + `username=user_id` |
| B2 | `web/api/routes/settings_integrations.py` | 1736 | `get_api_key` | `"github_token"` (global) | `"github_token"` + `username=user_id` |
| B3 | `web/api/routes/settings_integrations.py` | 1686 | `delete_api_key` | `"github_token"` (global) | `"github_token"` + `username=user_id` |

### Category C: Integration Connection Tests Using Wrong/Legacy Keys (3 sites)

Test functions use hardcoded key names that don't match stored key patterns.

| # | File | Line | Key Used | Correct Key Pattern |
|---|------|------|----------|---------------------|
| C1 | `web/api/routes/integrations.py` | 478 | `"slack"` | `"slack_bot"` + `username=user_id` |
| C2 | `web/api/routes/integrations.py` | 516 | `"github"` | `"github_token"` + `username=user_id` |
| C3 | `web/api/routes/settings_integrations.py` | 1261 | `"notion"` (no username) | `"notion"` + `username=user_id` |

### Category D: Slack/Notion Deletion Using Wrong/Global Keys (2 sites)

| # | File | Line | Operation | Key Used | Correct Key Pattern |
|---|------|------|-----------|----------|---------------------|
| D1 | `web/api/routes/settings_integrations.py` | 440 | `delete_api_key` | `"slack_bot_token"` | `"slack_bot"` + `username=user_id` |
| D2 | `web/api/routes/settings_integrations.py` | 1365 | `delete_api_key` | `"notion"` (no username) | `"notion"` + `username=user_id` |

### NOT in scope (correctly global):
- `openai`, `anthropic`, `gemini`, `perplexity` — LLM provider keys, app-level
- `google_calendar_client_id/secret`, `slack_client_id/secret`, `github_client_id/secret` — OAuth app credentials
- `google_calendar` at `google_calendar_adapter.py:272` — intentional legacy fallback from #843 fix

**Total sites requiring remediation: 13** (5 calendar router + 3 GitHub + 3 connection tests + 2 deletions)

---

## Requirements

### Phase 1: Fix GitHub Token Store/Retrieve/Delete (Category B - CRITICAL)

**Objective**: Eliminate the silent auth failure where GitHub tokens are stored globally but retrieved per-user.

**Tasks**:
- [ ] Update `settings_integrations.py:1650` to `store_api_key("github_token", token, username=current_user.sub)`
- [ ] Update `settings_integrations.py:1736` to `get_api_key("github_token", username=current_user.sub)`
- [ ] Update `settings_integrations.py:1686` to `delete_api_key("github_token", username=current_user.sub)`
- [ ] Verify `github/config_service.py:167` retrieval pattern matches new storage pattern
- [ ] Write test: store as User A — retrieve as User A succeeds — retrieve as User B fails

**Deliverables**:
- Modified `web/api/routes/settings_integrations.py`
- Test in `tests/unit/web/api/routes/test_settings_github.py`

### Phase 2: Fix Connection Test Endpoints (Category C)

**Objective**: Connection test functions use correct user-scoped keys.

**Tasks**:
- [ ] Update `_test_slack()` in `integrations.py:478` to accept user_id and use correct scoped key
- [ ] Update `_test_github()` in `integrations.py:516` to accept user_id and use correct scoped key
- [ ] Update Notion status check in `settings_integrations.py:1261` to use `get_api_key("notion", username=current_user.sub)`
- [ ] Update callers of these test functions to pass user_id
- [ ] Write tests verifying connection tests use correct keys

**Deliverables**:
- Modified `web/api/routes/integrations.py`
- Modified `web/api/routes/settings_integrations.py`
- Tests for connection test functions

### Phase 3: Fix Slack/Notion Deletion (Category D)

**Objective**: Disconnect operations remove the correct user-scoped key.

**Tasks**:
- [ ] Update `settings_integrations.py:440` to `delete_api_key("slack_bot", username=current_user.sub)` (and also delete user token key)
- [ ] Update `settings_integrations.py:1365` to `delete_api_key("notion", username=current_user.sub)`
- [ ] Write tests verifying user-scoped deletion

**Deliverables**:
- Modified `web/api/routes/settings_integrations.py`
- Deletion tests

### Phase 4: Thread user_id Through Calendar Router Calls (Category A)

**Objective**: All CalendarIntegrationRouter instantiations pass user_id.

**Tasks**:
- [ ] A1: Add user_id parameter to `_get_calendar_context()` in canonical_handlers and thread through callers
- [ ] A2: Add user_id to `_get_calendar_summary()` in conversation_handler (or source from session)
- [ ] A3: Add user_id to `_handle_attention_query()` in intent_service
- [ ] A4: Document CalendarPlugin as system-context (no user_id expected) with `# TODO(multi-tenant):` comment
- [ ] A5: Update `create_calendar_integration()` factory to accept optional user_id
- [ ] Write test: each call site passes user_id when available

**Deliverables**:
- Modified handler files
- Tests for each call site

### Phase 5: Add CI Grep Guard

**Objective**: Prevent regression — new code can't introduce non-scoped patterns without detection.

**Tasks**:
- [ ] Create `scripts/check-keychain-scoping.sh` that greps for known non-scoped patterns
- [ ] Add to CI workflow (or pre-commit hook)
- [ ] Document allowlist for intentional global keys (LLM providers, app credentials, legacy fallback)

**Deliverables**:
- `scripts/check-keychain-scoping.sh`
- CI integration

### Phase 6: Add Flow-Level Isolation Tests

**Objective**: Test the full user flow, not just infrastructure plumbing.

**Tasks**:
- [ ] Test: "User A connects GitHub — asks about issues — adapter uses User A's token"
- [ ] Test: "User B (not connected) — asks about issues — gets 'not connected'"
- [ ] Same pattern for Slack connection test, Notion connection test, Calendar authentication
- [ ] Test: disconnect as User A — User A's key removed — User B's key still exists

**Deliverables**:
- `tests/security/test_integration_flow_isolation.py`

### Phase Z: Completion and Handoff

- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] All 13 sites remediated
- [ ] CI grep guard passing
- [ ] Session log completed
- [ ] GitHub issue fully updated with evidence

---

## Acceptance Criteria

### Functionality
- [ ] GitHub token stored per-user — retrieved per-user (no silent failure)
- [ ] Slack connection test uses correct user-scoped key
- [ ] GitHub connection test uses correct user-scoped key
- [ ] Notion connection test uses correct user-scoped key
- [ ] Slack/Notion disconnect removes correct user-scoped key
- [ ] All 5 CalendarIntegrationRouter calls pass user_id (or documented as system-context)
- [ ] `grep -rn 'CalendarIntegrationRouter()' services/ --include='*.py'` returns only comments/docstrings

### Testing
- [ ] Unit tests for each Category B, C, D fix
- [ ] Flow-level isolation tests for GitHub, Slack, Notion, Calendar
- [ ] All existing tests still passing (no regressions)

### Quality
- [ ] No regressions introduced
- [ ] CI grep guard script exists and passes
- [ ] Error handling for missing user_id (graceful degradation, not crash)

### Documentation
- [ ] Session log completed with evidence
- [ ] Each fix references this issue number in code comments

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase 1: GitHub store/retrieve/delete | Not started | |
| Phase 2: Connection tests | Not started | |
| Phase 3: Slack/Notion deletion | Not started | |
| Phase 4: Calendar router user_id | Not started | |
| Phase 5: CI grep guard | Not started | |
| Phase 6: Flow-level isolation tests | Not started | |
| All tests passing | Not started | |

---

## Testing Strategy

### Unit Tests
- GitHub token lifecycle: store per-user, retrieve per-user, delete per-user, cross-user isolation
- Connection test functions: verify correct key name and username parameter
- Deletion functions: verify correct key name and username parameter

### Integration Tests
- Full conversation flow: "user connects integration — asks question — correct token used"
- Cross-user isolation: "User A connected, User B not — each sees correct state"

### Manual Testing Checklist
**Scenario 1**: GitHub Isolation
1. [ ] Log in as User A, connect GitHub with PAT
2. [ ] Ask "show my open issues" — issues returned
3. [ ] Log out, log in as User B
4. [ ] Ask "show my open issues" — "GitHub not connected"
5. [ ] Disconnect as User A — User B unaffected

---

## Success Metrics

### Quantitative
- 13/13 non-scoped sites remediated
- 0 non-scoped patterns found by CI grep guard in production code
- All flow-level isolation tests passing

### Qualitative
- No integration works for a user who hasn't connected it themselves
- Disconnect removes only the disconnecting user's credentials

---

## STOP Conditions

**STOP immediately and escalate if**:
- KeychainService `username` parameter doesn't work as expected
- Existing scoped retrieval (github/config_service.py) uses a different key name than what we're storing
- Any test that passed before this work now fails
- Uncertainty about which key name pattern an integration uses (confirm before changing)

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (GitHub): Small — 3 line changes + test
- Phase 2 (Connection tests): Small-Medium — need to thread user_id through test functions
- Phase 3 (Deletions): Small — 2 line changes + test
- Phase 4 (Calendar router): Medium — requires threading user_id through method signatures
- Phase 5 (CI guard): Small — shell script + CI config
- Phase 6 (Flow tests): Medium — new test file with cross-user scenarios

**Complexity Notes**: Phase 4 is the most complex — threading user_id through `_get_calendar_context()` requires updating the method signature and all its callers. The others are straightforward key name corrections.

---

## Dependencies

### Required (Must be complete first)
- [x] #843 — Calendar auth fix (completed 2026-02-24)
- [x] #734 — Multi-tenancy infrastructure (completed 2026-01-30)

### Optional
- [ ] Architect guidance on offer system (separate concern, #846)

---

## Related Documentation

- **Architecture**: ADR-058 (Multi-Tenancy Isolation Architecture)
- **Patterns**: Pattern-049 (Audit Cascade), Pattern-046 (Beads Completion Discipline)
- **Prior work**: #734 issue body documents original 7-phase approach
- **Session logs**: `dev/2026/02/24/2026-02-24-1743-lead-code-opus-log.md` (systemic analysis)

---

## Why #734 Missed These - Root Cause Analysis

Three structural factors caused recurring misses:

1. **Audit-by-layer, not audit-by-flow**: #734 audited each architectural layer independently (routes then services then repositories). Multi-tenancy bugs live in the *seams between layers* — e.g., a route correctly stores a token per-user, but a different route's connection test retrieves it globally.

2. **Tests verify plumbing, not user stories**: 94 tests verified "config service accepts user_id" but none verified "User A's GitHub query uses User A's token end-to-end." Infrastructure isolation does not equal user flow isolation.

3. **No regression gate**: After #734, new code introduced `CalendarIntegrationRouter()` without user_id, and nothing caught it. No CI check exists for non-scoped patterns.

**This time**: We audit by user flow (Phase 6), fix by category (Phases 1-4), and add a regression gate (Phase 5).

---

## Evidence Section

[To be filled during implementation]

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met
- [ ] Completion matrix 100%
- [ ] Evidence provided for each criterion
- [ ] Tests passing with output
- [ ] Documentation updated
- [ ] No regressions confirmed
- [ ] STOP conditions all clear
- [ ] Session log complete

**Status**: Not Started

---

## Notes for Implementation

**Methodology**: Audit by user flow, not by layer. For each integration:
1. Trace the full path from "user asks question" to handler to service to adapter to keychain
2. Verify user_id is threaded at every step (store, retrieve, delete, test)
3. Write a test that exercises the full path with two different user_ids
4. Add a grep guard so new code can't regress

---

_Issue created: 2026-02-24_
_Rewritten: 2026-02-25 (expanded to full template with enriched inventory)_

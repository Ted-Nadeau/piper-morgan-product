# Programmer Subagent A Prompt: #849 Route-Level Keychain Fixes (Categories B+C+D+E)

## Your Identity

You are a Programmer Agent (prog-A) working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims. You report back to the Lead Developer.

## Session Log

Create a session log at: `dev/2026/02/25/2026-02-25-prog-a-code-opus-log.md`
Update it throughout your work with timestamped entries.

## GitHub Issue

**Issue**: #849 — SEC-KEYCHAIN: Comprehensive audit and fix of all non-scoped keychain retrieval paths

## Mission

Fix all route-level and OAuth handler keychain key mismatches across GitHub, Slack, and Notion integrations. This covers Categories B, C, D, and E from the issue.

**Scope**: ONLY route-level fixes + Slack OAuth handler fix. Do NOT touch calendar-related code or service-layer method signatures.

## Critical Context: KeychainService Key Naming

The root cause of these bugs is a key naming mismatch. KeychainService builds keyring entry names via `_get_key_name()`:

```python
def _get_key_name(self, provider: str, username: Optional[str] = None) -> str:
    if username:
        return f"{username}_{provider}_api_key"
    return f"{provider}_api_key"
```

This means:
- `store_api_key("github_token", token)` → keyring entry: `github_token_api_key` (global)
- `store_api_key("github_token", token, username="user123")` → keyring entry: `user123_github_token_api_key` (user-scoped)
- `store_api_key(f"slack_bot_user123", token)` → keyring entry: `slack_bot_user123_api_key` (WRONG — f-string in provider name)
- `store_api_key("slack_bot", token, username="user123")` → keyring entry: `user123_slack_bot_api_key` (CORRECT — username param)

**The canonical pattern is: use the `username` parameter, NOT f-strings in the provider name.** All config services already use this pattern for retrieval.

## Multi-Agent Coordination

Subagent B is working in parallel on Category A (calendar router threading in service-layer files).
Your scope is B+C+D+E. Do NOT modify any files in:
- `services/integrations/calendar/` (any file)
- `services/conversation/conversation_handler.py`
- `services/intent/intent_service.py` (except if needed for C1/C2 connection test callers in `integrations.py`)
- `services/intent_service/canonical_handlers.py`

## Pre-Flight Verification (MANDATORY FIRST ACTION)

Before making any changes:
1. Confirm each file listed below exists at the expected path
2. Confirm the line numbers are approximately correct (code may have shifted)
3. Confirm `current_user` is available in each route handler where specified
4. Run existing tests BEFORE changes to establish a baseline: `pytest tests/unit/web/api/routes/ -v -k "slack or github or notion" 2>&1 | tail -30`

If reality doesn't match this prompt, STOP and report the mismatch.

## Exact Changes Required

### Category B: GitHub Token Store/Retrieve/Delete (3 sites in settings_integrations.py)

**File**: `web/api/routes/settings_integrations.py`

**B1 — Line ~1650**: GitHub token storage
- Current: `keychain.store_api_key("github_token", token)`
- Fix: `keychain.store_api_key("github_token", token, username=current_user.sub)`
- Note: `current_user` is available in this route handler (it's a dependency-injected FastAPI parameter)

**B2 — Line ~1736**: GitHub token retrieval
- Current: `token = keychain.get_api_key("github_token")`
- Fix: `token = keychain.get_api_key("github_token", username=current_user.sub)`
- Note: You need to verify `current_user` is available in this endpoint's function signature. If not, check how the route gets user context.

**B3 — Line ~1686**: GitHub token deletion
- Current: `keychain.delete_api_key("github_token")`
- Fix: `keychain.delete_api_key("github_token", username=current_user.sub)`

**Add comment**: `# Issue #849: User-scoped key for multi-tenancy isolation`

### Category C: Connection Test Endpoints (3 sites)

**C1 — File `web/api/routes/integrations.py`, line ~478**: Slack connection test
- Function: `_test_slack()`
- Current: `token = keychain.get_api_key("slack")`
- Fix: Add `user_id: Optional[str] = None` parameter to `_test_slack()`. Then: `token = keychain.get_api_key("slack_bot", username=user_id) if user_id else keychain.get_api_key("slack_bot")`
- Also update the caller of `_test_slack()` to pass `user_id`. Search for where `_test_slack()` is called — it should be from a route handler that has access to user_id.

**C2 — File `web/api/routes/integrations.py`, line ~516**: GitHub connection test
- Function: `_test_github()`
- Current: `token = keychain.get_api_key("github")`
- Fix: Add `user_id: Optional[str] = None` parameter. Then: `token = keychain.get_api_key("github_token", username=user_id) if user_id else keychain.get_api_key("github_token")`
- Also update the caller to pass `user_id`.

**C3 — File `web/api/routes/settings_integrations.py`, line ~1261**: Notion connection test
- Current: `api_key = keychain.get_api_key("notion")`
- Fix: `api_key = keychain.get_api_key("notion", username=current_user.sub)`

### Category D: Disconnection Using Wrong Keys (2 sites)

**D1 — File `web/api/routes/settings_integrations.py`, line ~440**: Slack disconnect
- Current: `keychain.delete_api_key("slack_bot_token")`
- Fix: `keychain.delete_api_key("slack_bot", username=current_user.sub)` AND also `keychain.delete_api_key("slack_user", username=current_user.sub)`
- Note: Both bot and user tokens should be removed on disconnect.

**D2 — File `web/api/routes/settings_integrations.py`, line ~1365**: Notion disconnect
- Current: `keychain.delete_api_key("notion")`
- Fix: `keychain.delete_api_key("notion", username=current_user.sub)`

### Category E: Slack OAuth Handler Store Mismatch (2 sites)

**File**: `services/integrations/slack/oauth_handler.py`

**E1 — Line ~529-535**: Bot token key name
- Current: `bot_key = f"slack_bot_{user_id}" if user_id else "slack_bot"` then `keychain.store_api_key(bot_key, bot_token)`
- Fix: Change to use `username` parameter:
  ```python
  keychain.store_api_key("slack_bot", bot_token, username=user_id)
  ```
  If `user_id` is None, `store_api_key("slack_bot", bot_token, username=None)` will store as global (fallback).

**E2 — Line ~548-550**: User token key name
- Current: `user_key = f"slack_user_{user_id}" if user_id else "slack_user"` then `keychain.store_api_key(user_key, user_token)`
- Fix: `keychain.store_api_key("slack_user", user_token, username=user_id)`

**Add comment**: `# Issue #849: Use username param (not f-string) for consistent key naming with config service retrieval`

## Testing Requirements

### Unit Tests to Write

1. **GitHub token lifecycle test**: Store with username → retrieve with same username → succeeds. Retrieve with different username → returns None.
2. **Slack OAuth store/config retrieve consistency**: Store via OAuth pattern → retrieve via config pattern → same token returned.
3. **Connection test key correctness**: Verify `_test_slack()` and `_test_github()` use correct key names + username.
4. **Disconnect key correctness**: Verify Slack disconnect removes `"slack_bot"` with username, not `"slack_bot_token"`.

### Run Existing Tests

After all changes, run:
```bash
pytest tests/unit/web/api/routes/test_settings_github.py -v
pytest tests/unit/web/api/routes/ -v -k "slack or github or notion or integration"
pytest tests/unit/services/integrations/ -v
```

Report ALL test output, not just "tests pass."

## STOP Conditions

- If `current_user` is not available in a route handler where you need it → STOP and report
- If you can't find the caller of `_test_slack()` or `_test_github()` → STOP and report
- If any existing test fails after your changes → STOP and report (do NOT decide if it's critical — the Lead Developer decides)
- If you find additional non-scoped sites not listed above → note them and continue with your assigned scope

**When tests fail**: STOP immediately. Report the exact error output. Do NOT decide if the failure is "critical" or "pre-existing" — the Lead Developer decides. Report: which tests fail, exact error messages, and whether the failure existed in your baseline run.

## Self-Check Before Claiming Complete

- [ ] Every site listed in my scope (B1-B3, C1-C3, D1-D2, E1-E2) has been modified
- [ ] Every modified method's callers have been verified (no broken call sites)
- [ ] Tests run and FULL output captured (not "tests pass" but actual output)
- [ ] Session log updated with all changes
- [ ] No changes outside my assigned scope (no calendar/service-layer files)
- [ ] STOP conditions checked — none triggered

## Evidence Requirements

Before reporting back, you MUST provide:
1. List of all files modified with exact paths
2. Full `pytest -v` output for all test runs (not just pass counts)
3. Any tests that were failing BEFORE your changes (baseline run output)
4. Your session log location
5. **Cross-validation markers**: For each change, the before/after grep pattern so Lead can verify:
   - Example: `grep -n "get_api_key(\"github_token\")" web/api/routes/settings_integrations.py` should return 0 matches after fix
   - Example: `grep -n "username=current_user.sub" web/api/routes/settings_integrations.py` should show the new pattern

## Handoff Format

```
## Issue #849 Subagent A Completion Report
**Status**: Complete/Partial/Blocked

**Categories Fixed**:
- B (GitHub store/retrieve/delete): [status]
- C (Connection tests): [status]
- D (Disconnections): [status]
- E (Slack OAuth handler): [status]

**Tests**:
- X tests added in [location]
- `pytest [path] -v` output: [paste actual output]

**Files Modified**:
- [file1.py] (lines changed)
- [file2.py] (lines changed)

**Session Log**: dev/2026/02/25/2026-02-25-prog-a-code-opus-log.md

**Blockers** (if any):
- [description]
```

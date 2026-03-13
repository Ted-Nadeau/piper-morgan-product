# Multi-Tenancy Isolation Audit Report

**Issue**: #734 - CRITICAL: Calendar and integration tokens leak between users
**Date**: 2026-01-30
**Auditor**: Lead Developer (Opus)
**Status**: Investigation Complete - Awaiting Architectural Decision

---

## Executive Summary

A comprehensive audit reveals **severe and systemic multi-tenancy isolation failures** across the Piper Morgan codebase. The original issue (#734 - calendar token leakage) is a symptom of a much larger architectural gap: **user context is not consistently propagated through the application**.

**Scope**: This is not a bug fix - it's a **missing architectural layer**.

---

## Critical Findings

### 1. OAuth Flows - ALL Leak User Tokens

| Integration | State Contains user_id? | Callback Has Auth? | Token Storage | Status |
|-------------|------------------------|-------------------|---------------|--------|
| Google Calendar | ❌ NO | ❌ NO | Global key | 🔴 CRITICAL |
| Slack | ❌ NO | ❌ NO | Global key | 🔴 CRITICAL |
| GitHub | N/A (PAT flow) | ❌ NO | Global key | 🔴 CRITICAL |
| Notion | N/A | ❌ NO | Hardcoded "system" | 🔴 CRITICAL |

**Root Cause**: OAuth state is pure CSRF token. Callbacks have no way to identify which user initiated the flow.

### 2. Credential Storage - Mixed Patterns

| Storage Location | User-Scoped? | Notes |
|-----------------|--------------|-------|
| `UserAPIKeyService` | ✅ YES | Correct implementation exists |
| Direct `KeychainService` calls | ❌ NO | 38+ locations bypass proper service |
| Config services | ❌ NO | Return global credentials |
| LLMConfigService | ❌ NO | Server-wide LLM keys |

**Root Cause**: `UserAPIKeyService` exists but routes/services bypass it and call `KeychainService` directly without `username` parameter.

### 3. Service Layer - Optional User Context

| Pattern | Status | Risk |
|---------|--------|------|
| `RequestContext` (ADR-051) | Defined, optional | Medium |
| Repository `owner_id` filtering | Optional parameter | High |
| Integration adapters | No user context | High |
| Background tasks | Context lost | High |

**Root Cause**: ADR-051 RequestContext migration incomplete. Services accept `user_id` as optional, defaulting to single-user assumptions.

### 4. Global Singleton State

| Component | Scope | Risk |
|-----------|-------|------|
| `PortfolioOnboardingManager._sessions` | Global dict | High |
| `StandupConversationManager` | Global singleton | High |
| `SlackConfigService._config` | Cached singleton | High |

**Root Cause**: Managers use in-memory dicts keyed by `session_id` (ephemeral) not `user_id` (persistent).

---

## Affected Components (Full Inventory)

### Routes with Direct Keychain Access (Should Use UserAPIKeyService)

```
web/api/routes/setup.py:
  - Line 519: keychain.get_api_key(provider)           # check-keychain
  - Line 564: keychain.get_api_key(req.provider)       # use-keychain
  - Line 742: keychain.store_api_key("openai", ...)    # complete setup
  - Line 749: keychain.store_api_key("anthropic", ...) # complete setup
  - Line 1060: keychain.store_api_key("google_calendar", ...) # OAuth callback
  - Line 1100: keychain.get_api_key("google_calendar") # calendar status

web/api/routes/settings_integrations.py:
  - Line 613-614: keychain.store_api_key("slack_*", ...) # Slack creds
  - Line 702-703: keychain.store_api_key("google_calendar_*", ...) # Calendar app creds
  - Line 738-739: keychain.get_api_key("google_calendar_*") # Get app creds
  - Line 783: keychain.get_api_key("google_calendar") # Get token
  - Line 926: keychain.store_api_key("google_calendar", ...) # OAuth callback
  - Line 1006: keychain.get_api_key("google_calendar") # Calendar settings
  - Line 1186: keychain.get_api_key("google_calendar") # Calendar list
  - Line 1215: keychain.get_api_key("notion") # Notion settings
  - Line 1602: keychain.store_api_key("github_token", ...) # GitHub save
  - Line 1688: keychain.get_api_key("github_token") # GitHub status

web/api/routes/integrations.py:
  - Line 391: keychain.get_api_key("google_calendar")
  - Line 472: keychain.get_api_key("slack")
  - Line 510: keychain.get_api_key("github")
  - Line 549: keychain.get_api_key("google_calendar")
```

### Services with Global Credential Access

```
services/integrations/slack/config_service.py:
  - Line 187-189: keychain.get_api_key("slack_*") # No user_id

services/integrations/slack/oauth_handler.py:
  - Line 382: keychain.store_api_key("slack_bot", ...) # Global
  - Line 393: keychain.store_api_key("slack_user", ...) # Global

services/integrations/github/config_service.py:
  - Line 145: keychain.get_api_key("github_token") # No user_id

services/integrations/notion/config_service.py:
  - Line 173: keychain.get_api_key("notion", username="system") # Hardcoded

services/integrations/calendar/oauth_handler.py:
  - Line 70-72: keychain.get_api_key("google_calendar_*") # App creds

services/config/llm_config_service.py:
  - Line 199: keychain.get_api_key(provider) # No user_id

services/mcp/consumer/google_calendar_adapter.py:
  - Line 245: keychain.get_api_key("google_calendar") # No user_id
```

### OAuth State Management (Needs User ID)

```
services/integrations/calendar/oauth_handler.py:
  - Line 92: state = secrets.token_urlsafe(32) # No user_id encoded
  - _PENDING_STATES[state] = time.time() # Only timestamp, no user

services/integrations/slack/oauth_handler.py:
  - Line 73: state = secrets.token_urlsafe(32) # No user_id encoded
  - self._oauth_states[state] = {...} # No user_id
```

---

## Architectural Options

### Option A: Incremental Fix (Narrow Scope)

**Scope**: Fix only the routes that have `current_user` available

**Changes**:
- Update settings_integrations.py endpoints to pass `username=current_user.sub` to keychain
- Update integrations.py to use UserAPIKeyService
- Leave OAuth callbacks and setup wizard unchanged (deferred to separate issue)

**Pros**: Faster, lower risk, partial improvement
**Cons**: Doesn't fix OAuth flows, setup wizard still global, incomplete solution

**Estimated Effort**: 1-2 days

### Option B: Full Credential Isolation (Medium Scope)

**Scope**: Fix all credential storage/retrieval to be user-scoped

**Changes**:
- All keychain calls include `username=user_id`
- OAuth handlers embed user_id in state
- Config services accept user context
- Setup wizard stores per-user keys

**Additional Complexity**:
- OAuth callbacks need session/cookie to recover user_id
- LLM keys need decision: per-user or server-wide?
- Migration for existing global keys

**Pros**: Complete credential isolation
**Cons**: Significant refactoring, OAuth flow redesign, migration needed

**Estimated Effort**: 1-2 weeks

### Option C: Domain-Driven Refactor (Full Scope)

**Scope**: Implement proper multi-tenancy layer per ADR-051

**Changes**:
- Complete RequestContext migration (make it required, not optional)
- Add workspace_id to all queries (currently defined but unused)
- Refactor singleton managers to be per-user/workspace
- Add tenant isolation layer to repositories
- Integration adapters receive and use RequestContext

**Pros**: Proper architectural foundation, enables true multi-tenant
**Cons**: Largest scope, touches most of codebase, needs careful design

**Estimated Effort**: 2-4 weeks with architect guidance

---

## Design Questions Requiring Decision

1. **LLM Keys**: Should they be per-user or server-wide?
   - Per-user: Users bring their own keys
   - Server-wide: Single org-level keys (current assumption)
   - Hybrid: Admin keys as default, user keys as override

2. **OAuth App Credentials** (client_id, client_secret):
   - These are legitimately app-level (not per-user)
   - But user **tokens** from OAuth must be per-user
   - Need clear separation of app creds vs user tokens

3. **Workspace Model**:
   - RequestContext has `workspace_id` but it's never used
   - Is multi-workspace a future requirement?
   - Should this fix include workspace isolation groundwork?

4. **Migration Strategy**:
   - Existing global keys will become inaccessible after fix
   - Require users to re-authenticate integrations?
   - Migration script to re-key existing tokens (needs user mapping)?

---

## Recommendation

Given that:
- This is alpha (few users, limited testing)
- The gap is systemic (not a simple bug)
- Correct fix requires architectural decisions

**I recommend**: Request Chief Architect guidance before implementation.

**Questions for Architect**:
1. Is Option C (full RequestContext migration) the right approach?
2. Should workspace_id be activated as part of this?
3. What's the LLM key ownership model?
4. Should we create a formal ADR for multi-tenancy isolation?

---

## Evidence Files

- `dev/2026/01/30/734-issue-audit.md` - Original issue audit
- `dev/2026/01/30/734-gameplan.md` - Original (narrow) gameplan
- `dev/2026/01/30/734-gameplan-audit.md` - Gameplan audit
- This file - Full multi-tenancy audit

---

## Next Steps

1. PM reviews this audit
2. Decision: Fix incrementally (Option A/B) or architect properly (Option C)
3. If Option C: Draft architecture guidance request
4. Create revised gameplan based on decision

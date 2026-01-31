# Architecture Guidance Request: Multi-Tenancy Isolation Layer

**From**: Lead Developer (Opus)
**To**: Chief Architect
**Date**: 2026-01-30
**Priority**: High
**Response-Requested**: Yes
**Related Issue**: #734

---

## Context

During investigation of issue #734 (calendar tokens leaking between users), we discovered **systemic multi-tenancy isolation failures** across the codebase. This is not a bug - it's a missing architectural layer.

PM has decided: **Do the domain-driven refactor properly.** Timeline is not a constraint; correctness is.

## Decisions Already Made (PM Input)

1. **LLM keys**: Per-user in current model (may change for enterprise/teams later)
2. **workspace_id**: Activate now (currently in RequestContext but unused)
3. **Migration**: Not a concern (few alpha users, can require re-auth)
4. **Approach**: Option C - Full domain-driven refactor

## Guidance Requested

### 1. OAuth Credential Separation Pattern

**Problem**: OAuth flows involve two types of credentials:
- **App credentials** (client_id, client_secret) - legitimately shared across all users
- **User tokens** (access_token, refresh_token) - must be per-user

**Current State**: Both stored the same way (global keychain keys)

**Question**: What's the correct architectural pattern for separating these?

Options I see:
- A) Different storage mechanisms (app creds in env/config, user tokens in keychain with user_id)
- B) Different key prefixes (e.g., `app_google_calendar_client_id` vs `{user_id}_google_calendar_token`)
- C) Different services entirely (AppCredentialService vs UserTokenService)

### 2. RequestContext Activation Strategy

**Problem**: ADR-051 defined RequestContext but migration is incomplete:
- Many services accept `ctx: Optional[RequestContext] = None`
- Many routes don't create RequestContext
- `workspace_id` is defined but never used

**Question**: What's the safest migration path to make RequestContext required?

Options I see:
- A) Big bang: Make ctx required everywhere, fix all call sites at once
- B) Gradual: Add deprecation warnings for None, then enforce later
- C) Boundary enforcement: Require at route level, optional deeper (services decide)

### 3. Integration Adapter User Context

**Problem**: Integration adapters (Slack, Calendar, GitHub) need user context but:
- Config services are singletons (no user state)
- Background tasks lose RequestContext
- OAuth callbacks can't use `current_user` dependency (GET redirects from external provider)

**Question**: How should integration adapters receive and use user context?

Specific sub-questions:
- Should config services be instantiated per-request with user context?
- How do OAuth callbacks identify the initiating user? (embed in state? session cookie?)
- How do background tasks (webhooks) maintain user context?

### 4. Singleton Manager Refactor

**Problem**: `PortfolioOnboardingManager` and `StandupConversationManager` are global singletons with in-memory state keyed by `session_id` (ephemeral).

**Question**: Should these be:
- A) Refactored to key by `user_id` instead of `session_id`
- B) Moved to database-backed state (survives restarts)
- C) Made per-user instances (instantiated per request)

### 5. Repository Isolation Pattern

**Problem**: Repositories have optional `owner_id` filtering:
```python
async def get_by_id(self, id: str, owner_id: Optional[str] = None):
    if owner_id:  # Only filters if provided
        filters.append(Model.owner_id == owner_id)
```

**Question**: Should we:
- A) Make `owner_id` required (breaking change, catches missing context)
- B) Add `workspace_id` filtering alongside `owner_id`
- C) Create isolated repository instances per-user (can't accidentally cross-query)

### 6. Sequencing Recommendation

Given the scope (38+ locations, multiple patterns), what's the recommended implementation order?

My initial thought:
1. RequestContext enforcement (foundation)
2. OAuth state redesign (user identification)
3. Credential storage (UserAPIKeyService for all)
4. Config service refactor (per-user context)
5. Repository isolation (workspace activation)

But you may see dependencies or risks I'm missing.

---

## Supporting Documentation

- **Full Audit Report**: `dev/2026/01/30/734-multi-tenancy-audit-report.md`
- **Issue Audit**: `dev/2026/01/30/734-issue-audit.md`
- **Original Gameplan** (now superseded): `dev/2026/01/30/734-gameplan.md`

---

## Requested Output

1. Answers/guidance on the 6 questions above
2. Any additional architectural considerations I've missed
3. Recommended ADR if this warrants formal documentation
4. Green light to proceed with revised gameplan

---

Thank you for your guidance on this. Getting the foundation right now will pay dividends as we scale.

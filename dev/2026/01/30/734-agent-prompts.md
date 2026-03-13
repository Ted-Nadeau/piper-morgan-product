# Agent Prompts: Issue #734 - Multi-Tenancy Isolation Architecture

**Issue**: #734 - SEC-MULTITENANCY: Multi-Tenancy Isolation Architecture Implementation
**Date**: 2026-01-30
**Author**: Lead Developer (Opus)
**Gameplan**: `dev/2026/01/30/734-gameplan-v2.md`

---

## Overview

This document contains agent prompts for subagent phases of Issue #734. Lead Developer executes Phases 1, 2, 3, 8, 9 directly. Subagents handle Phases 4, 5, 6, 7.

**Parallel Work Opportunities**:
- Phase 4 + Phase 5 (can run simultaneously)
- Phase 6 + Phase 7 (can run simultaneously after 4+5 complete)

---

## Agent Prompt: Phase 4 - Repository Isolation

### Your Identity

You are a Coding Agent working on the Piper Morgan project. You follow TDD methodology and provide evidence for all claims.

### Mission

**Make `owner_id` REQUIRED (not optional) in all repository methods** - this creates a "forcing function" that makes any code path without user context fail at compile time.

**GitHub Issue**: #734 - SEC-MULTITENANCY: Multi-Tenancy Isolation Architecture Implementation

### Context

- **Current State**: Repository methods accept `owner_id: Optional[str] = None`. When None, queries return ALL records regardless of owner.
- **Target State**: Repository methods require `owner_id: str`. Any call without owner_id fails with ValueError.
- **Dependencies**: Phase 3 (RequestContext enforcement) must be complete - routes now have user context available.
- **Risk**: This will break call sites that don't pass owner_id. That's intentional - we want them to fail loudly.

### Acceptance Criteria

- [ ] Write failing cross-user isolation tests FIRST (TDD)
- [ ] Change `owner_id: Optional[str]` → `owner_id: str` in all repository methods
- [ ] Add validation: raise `ValueError("owner_id is required")` if None
- [ ] Fix ALL call sites that now fail type checks
- [ ] All new tests pass showing isolation works
- [ ] All existing tests still pass (no regressions)
- [ ] Grep confirms no `owner_id: Optional` remains in repositories

### TDD Tests First (Write These Before Implementation)

Create `tests/security/test_cross_user_isolation.py`:

```python
"""Cross-user isolation tests for repository layer.

These tests verify that User A's data is NEVER visible to User B.
This is the wiring test for multi-tenancy isolation.
"""
import pytest
from services.repositories.universal_list_repository import UniversalListRepository
from services.repositories.todo_repository import TodoRepository
from services.repositories.project_repository import ProjectRepository

class TestCrossUserIsolation:
    """Verify data isolation between users."""

    async def test_user_a_lists_not_visible_to_user_b(self, db_session):
        """User A's lists should not be returned when querying as User B."""
        repo = UniversalListRepository(db_session)

        # User A creates a list
        list_a = await repo.create(owner_id="user_a", name="User A's List")

        # User B queries lists
        lists_b = await repo.get_all(owner_id="user_b")

        # User A's list should NOT be in User B's results
        assert list_a.id not in [l.id for l in lists_b]

    async def test_user_a_todos_not_visible_to_user_b(self, db_session):
        """User A's todos should not be returned when querying as User B."""
        repo = TodoRepository(db_session)

        # User A creates a todo
        todo_a = await repo.create(owner_id="user_a", title="User A's Todo")

        # User B queries todos
        todos_b = await repo.get_all(owner_id="user_b")

        # User A's todo should NOT be in User B's results
        assert todo_a.id not in [t.id for t in todos_b]

    async def test_repository_rejects_none_owner_id(self, db_session):
        """Repository methods must reject None owner_id."""
        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.get_all(owner_id=None)

    async def test_repository_rejects_empty_owner_id(self, db_session):
        """Repository methods must reject empty string owner_id."""
        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.get_all(owner_id="")
```

### Files to Modify

1. **Repositories** (change signatures):
   - `services/repositories/universal_list_repository.py`
   - `services/repositories/todo_repository.py`
   - `services/repositories/project_repository.py`
   - `services/repositories/file_repository.py`

2. **Callers** (fix to pass owner_id):
   - `services/list_management/list_service.py`
   - `services/todo_management/todo_service.py`
   - `services/project_management/project_service.py`
   - `services/file_management/file_service.py`
   - `web/api/routes/lists.py`
   - `web/api/routes/todos.py`
   - `web/api/routes/projects.py`

### Implementation Steps

1. **Write tests first** - Create test file, run to verify they fail
2. **Update repository signatures** - Change Optional[str] to str
3. **Add validation** - Raise ValueError at method entry if owner_id is None or empty
4. **Find broken callers** - Run tests, note failures
5. **Fix callers** - Update each caller to pass owner_id from RequestContext
6. **Verify** - All tests pass

### Evidence Required

Provide in your handoff:

```markdown
## Phase 4 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in tests/security/test_cross_user_isolation.py
- `pytest tests/security/test_cross_user_isolation.py -v` output: [paste]

**Verification**:
```bash
# Confirm no Optional owner_id in repositories
grep -r "owner_id: Optional" services/repositories/
# Should return NOTHING
```

**Files Modified**:
- services/repositories/universal_list_repository.py (+X/-Y lines)
- [list all files with line counts]

**Regression Check**:
```bash
pytest tests/unit/ -v
# All passing
```
```

### User Testing Steps

1. Start server: `python main.py`
2. Log in as User A, create a list via API or UI
3. Log out, log in as User B
4. Query lists as User B via API
5. Verify User A's list is NOT visible to User B

### Anti-80% Check

Before claiming complete, verify:
- ALL repository methods updated (not just some)
- ALL call sites fixed (grep to confirm zero type errors remain)
- Method enumeration: X/X repository methods = 100%

### STOP Conditions

Stop and report if:
- Tests fail after changes
- Can't find owner_id source for a caller
- Breaking change affects >10 files unexpectedly
- Existing tests break and fix is non-obvious

---

## Agent Prompt: Phase 5 - OAuth State Redesign

### Your Identity

You are a Coding Agent working on the Piper Morgan project. You follow TDD methodology and provide evidence for all claims.

### Mission

**Embed user_id in OAuth state** so that when OAuth providers (Google, Slack) redirect back to our callback, we can identify which user initiated the flow.

**GitHub Issue**: #734 - SEC-MULTITENANCY: Multi-Tenancy Isolation Architecture Implementation

### Context

- **Current State**: OAuth state contains only CSRF nonce. Callbacks can't identify initiating user. Tokens stored globally.
- **Target State**: OAuth state = JSON with `{user_id, nonce, return_url}`, base64 encoded. Callbacks extract user_id and store tokens per-user.
- **Dependencies**: None - can run in parallel with Phase 4.
- **Risk**: Breaking OAuth flows means users can't connect integrations. Test carefully.

### Acceptance Criteria

- [ ] Write failing tests for state encoding/decoding FIRST (TDD)
- [ ] Update `generate_authorization_url()` to accept user_id and embed in state
- [ ] Update `_verify_state()` to extract and return user_id
- [ ] OAuth initiation endpoints require authentication (get user from JWT)
- [ ] Callback handlers extract user_id from state, store tokens per-user
- [ ] All new tests pass
- [ ] Manual test: OAuth flow completes with user-scoped storage

### TDD Tests First (Write These Before Implementation)

Create `tests/integrations/test_oauth_state.py`:

```python
"""OAuth state encoding/decoding tests.

These tests verify that user_id is correctly embedded in OAuth state
and can be extracted on callback.
"""
import pytest
import json
import base64
from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

class TestOAuthState:
    """Verify OAuth state contains user identity."""

    def test_oauth_state_encodes_user_id(self):
        """OAuth state should contain user_id."""
        handler = GoogleCalendarOAuthHandler()

        # Generate auth URL with user_id
        auth_url, state = handler.generate_authorization_url(
            user_id="test-user-123",
            return_url="/settings/integrations"
        )

        # Decode state and verify user_id present
        decoded = json.loads(base64.urlsafe_b64decode(state + "=="))
        assert decoded["user_id"] == "test-user-123"
        assert "nonce" in decoded  # CSRF protection still present

    def test_oauth_state_decodes_user_id(self):
        """Callback should extract user_id from state."""
        handler = GoogleCalendarOAuthHandler()

        # Generate state with user_id
        _, state = handler.generate_authorization_url(
            user_id="test-user-456",
            return_url="/settings"
        )

        # Verify extraction works
        user_id = handler.extract_user_id_from_state(state)
        assert user_id == "test-user-456"

    def test_oauth_state_validates_nonce(self):
        """State validation should still check CSRF nonce."""
        handler = GoogleCalendarOAuthHandler()

        # Generate valid state
        _, state = handler.generate_authorization_url(
            user_id="test-user",
            return_url="/settings"
        )

        # Tampered state should fail validation
        tampered = base64.urlsafe_b64encode(
            json.dumps({"user_id": "hacker", "nonce": "fake"}).encode()
        ).decode().rstrip("=")

        with pytest.raises(ValueError, match="Invalid state"):
            handler.verify_state(tampered)

    def test_oauth_state_rejects_missing_user_id(self):
        """State without user_id should be rejected."""
        handler = GoogleCalendarOAuthHandler()

        # Old-style state (no user_id) should fail
        old_state = base64.urlsafe_b64encode(
            json.dumps({"nonce": "some-nonce"}).encode()
        ).decode().rstrip("=")

        with pytest.raises(ValueError, match="user_id"):
            handler.extract_user_id_from_state(old_state)
```

### Files to Modify

1. **OAuth Handlers** (update state encoding):
   - `services/integrations/calendar/oauth_handler.py`
   - `services/integrations/slack/oauth_handler.py`

2. **Route Files** (require auth, pass user_id):
   - `web/api/routes/setup.py` - OAuth initiation endpoints
   - `web/api/routes/settings_integrations.py` - OAuth initiation endpoints

### Implementation Steps

1. **Write tests first** - Create test file, run to verify they fail
2. **Update state encoding** - Change from simple nonce to JSON with user_id
3. **Update state validation** - Extract user_id when verifying
4. **Update initiation routes** - Require authentication, pass current_user.sub
5. **Update callback handlers** - Extract user_id, use for token storage
6. **Manual test** - Complete OAuth flow, verify token stored with user scope

### State Format

**Before** (broken):
```python
state = secrets.token_urlsafe(32)  # Just CSRF nonce
```

**After** (secure):
```python
state_data = {
    "user_id": user_id,
    "nonce": secrets.token_urlsafe(16),
    "return_url": return_url
}
state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode().rstrip("=")
```

### Evidence Required

Provide in your handoff:

```markdown
## Phase 5 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in tests/integrations/test_oauth_state.py
- `pytest tests/integrations/test_oauth_state.py -v` output: [paste]

**Verification**:
```bash
# Show state encoding includes user_id
python -c "
from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler
import json, base64
h = GoogleCalendarOAuthHandler()
url, state = h.generate_authorization_url(user_id='test', return_url='/')
decoded = json.loads(base64.urlsafe_b64decode(state + '=='))
print('user_id in state:', 'user_id' in decoded)
"
# Output: user_id in state: True
```

**Files Modified**:
- services/integrations/calendar/oauth_handler.py (+X/-Y lines)
- [list all files]

**Manual Test**:
1. Started server: python main.py
2. Logged in as test user
3. Clicked "Connect Calendar"
4. Completed OAuth flow
5. Verified token stored with user scope:
   ```bash
   # Check keychain for user-scoped token
   python -c "from services.infrastructure.keychain_service import KeychainService; ks = KeychainService(); print(ks.get_api_key('google_calendar', username='USER_ID'))"
   ```
```

### STOP Conditions

Stop and report if:
- Tests fail after changes
- OAuth flow breaks (can't complete authorization)
- State encoding/decoding produces errors
- Existing OAuth tokens become inaccessible

---

## Agent Prompt: Phase 6 - Credential Storage Separation

### Your Identity

You are a Coding Agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

### Mission

**Separate app credentials from user tokens** - Create `IntegrationConfigService` for app credentials (client_id, client_secret) and ensure all user tokens go through `UserAPIKeyService`.

**GitHub Issue**: #734 - SEC-MULTITENANCY: Multi-Tenancy Isolation Architecture Implementation

### Context

- **Current State**: Routes directly call KeychainService for both app credentials AND user tokens. 38+ locations identified.
- **Target State**:
  - `IntegrationConfigService` handles app credentials (read-only, no user_id needed)
  - `UserAPIKeyService` handles user tokens (requires user_id)
  - No direct KeychainService imports in routes
- **Dependencies**: Phases 4 and 5 should be complete (repositories require owner_id, OAuth embeds user_id)
- **Risk**: Breaking credential retrieval means integrations stop working.

### Acceptance Criteria

- [ ] Create `IntegrationConfigService` for app credentials (client_id, client_secret)
- [ ] Ensure `UserAPIKeyService` used for ALL user token operations
- [ ] Update all 38+ direct keychain calls to use appropriate service
- [ ] Remove direct `KeychainService` imports from route files
- [ ] Tests for credential separation
- [ ] Grep confirms no keychain calls in routes

### Files to Create

**NEW: `services/integrations/integration_config_service.py`**

```python
"""Service for retrieving integration app credentials.

App credentials (client_id, client_secret) are server-wide configuration,
NOT per-user. This service provides read-only access to these credentials.

For user tokens (access_token, refresh_token), use UserAPIKeyService instead.
"""
from services.infrastructure.keychain_service import KeychainService

class IntegrationConfigService:
    """Provides app credentials for OAuth integrations."""

    def __init__(self, keychain: KeychainService = None):
        self._keychain = keychain or KeychainService()

    def get_google_client_id(self) -> str | None:
        """Get Google OAuth client ID (app credential)."""
        return self._keychain.get_api_key("google_client_id")

    def get_google_client_secret(self) -> str | None:
        """Get Google OAuth client secret (app credential)."""
        return self._keychain.get_api_key("google_client_secret")

    def get_slack_client_id(self) -> str | None:
        """Get Slack OAuth client ID (app credential)."""
        return self._keychain.get_api_key("slack_client_id")

    def get_slack_client_secret(self) -> str | None:
        """Get Slack OAuth client secret (app credential)."""
        return self._keychain.get_api_key("slack_client_secret")

    def get_github_client_id(self) -> str | None:
        """Get GitHub OAuth client ID (app credential)."""
        return self._keychain.get_api_key("github_client_id")

    def get_github_client_secret(self) -> str | None:
        """Get GitHub OAuth client secret (app credential)."""
        return self._keychain.get_api_key("github_client_secret")

    # Add other integrations as needed...
```

### Files to Modify

1. **Route files** (replace direct keychain with services):
   - `web/api/routes/setup.py` - 6 locations
   - `web/api/routes/settings_integrations.py` - 13 locations
   - `web/api/routes/integrations.py` - 4 locations

2. **OAuth handlers** (use services):
   - `services/integrations/calendar/oauth_handler.py`
   - `services/integrations/slack/oauth_handler.py`

### Implementation Steps

1. **Create IntegrationConfigService** - New file with app credential methods
2. **Audit existing calls** - Categorize each as "app credential" or "user token"
3. **Update routes** - Replace keychain imports with service imports
4. **Update OAuth handlers** - Use services for credential retrieval
5. **Remove imports** - Ensure no direct KeychainService in routes
6. **Verify** - Grep confirms separation complete

### Categorization Guide

| Key Pattern | Type | Service to Use |
|-------------|------|----------------|
| `*_client_id` | App credential | IntegrationConfigService |
| `*_client_secret` | App credential | IntegrationConfigService |
| `*_access_token` | User token | UserAPIKeyService |
| `*_refresh_token` | User token | UserAPIKeyService |
| `*_api_key` (user's) | User token | UserAPIKeyService |
| `*_bot_token` | User token | UserAPIKeyService |

### Evidence Required

Provide in your handoff:

```markdown
## Phase 6 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in tests/integrations/test_credential_separation.py
- `pytest tests/integrations/test_credential_separation.py -v` output: [paste]

**Verification**:
```bash
# Confirm no direct keychain in routes
grep -r "from services.infrastructure.keychain_service import" web/api/routes/
# Should return NOTHING

grep -r "keychain\.(store|get)_api_key" web/api/routes/
# Should return NOTHING
```

**Files Modified**:
- NEW: services/integrations/integration_config_service.py (+X lines)
- web/api/routes/setup.py (+X/-Y lines)
- [list all files]

**Credential Categorization**:
| Location | Key | Category | Now Uses |
|----------|-----|----------|----------|
| setup.py:45 | google_client_id | App | IntegrationConfigService |
| setup.py:67 | google_access_token | User | UserAPIKeyService |
| [complete table] |
```

### STOP Conditions

Stop and report if:
- Can't categorize a credential (app vs user unclear)
- Service injection pattern unclear for a route
- Breaking change affects OAuth flows
- Tests fail after changes

---

## Agent Prompt: Phase 7 - Config Service Method Signatures

### Your Identity

You are a Coding Agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

### Mission

**Update config service methods to accept user_id** so they return user-scoped credentials, not global credentials.

**GitHub Issue**: #734 - SEC-MULTITENANCY: Multi-Tenancy Isolation Architecture Implementation

### Context

- **Current State**: Config services like `SlackConfigService.get_bot_token()` return global credentials with no user context.
- **Target State**: Config services accept `user_id: str` parameter and return that user's credentials.
- **Dependencies**: Phase 6 should be complete (credential separation established).
- **Risk**: Breaking config services affects all integrations.

### Acceptance Criteria

- [ ] Update `SlackConfigService` methods to accept `user_id: str`
- [ ] Update `GitHubConfigService` methods to accept `user_id: str`
- [ ] Update `NotionConfigService` methods to accept `user_id: str`
- [ ] Update `CalendarConfigService` methods to accept `user_id: str`
- [ ] Update ALL callers to pass user_id
- [ ] Tests showing different users get different configs
- [ ] Grep confirms all config methods accept user_id

### Files to Modify

1. **Config Services** (update signatures):
   - `services/integrations/slack/config_service.py`
   - `services/integrations/github/config_service.py`
   - `services/integrations/notion/config_service.py`
   - `services/integrations/calendar/config_service.py`

2. **Callers** (update to pass user_id):
   - `services/integrations/slack/slack_plugin.py`
   - `services/integrations/github/github_plugin.py`
   - `services/integrations/notion/notion_plugin.py`
   - `services/integrations/calendar/calendar_plugin.py`
   - Route files that call config services

### Example Transformation

**Before**:
```python
class SlackConfigService:
    def get_bot_token(self) -> str | None:
        return self._keychain.get_api_key("slack_bot_token")
```

**After**:
```python
class SlackConfigService:
    def get_bot_token(self, user_id: str) -> str | None:
        if not user_id:
            raise ValueError("user_id is required")
        return self._user_api_key_service.get_user_key(
            user_id=user_id,
            provider="slack_bot_token"
        )
```

### TDD Tests

Create `tests/integrations/test_config_service_isolation.py`:

```python
"""Config service user isolation tests."""
import pytest

class TestConfigServiceIsolation:
    """Verify config services return user-scoped credentials."""

    async def test_slack_token_isolated_by_user(self):
        """User A's Slack token != User B's Slack token."""
        # Store different tokens for different users
        await user_api_key_service.store_user_key(
            user_id="user_a", provider="slack_bot_token", key="token_a"
        )
        await user_api_key_service.store_user_key(
            user_id="user_b", provider="slack_bot_token", key="token_b"
        )

        config = SlackConfigService()

        # Each user gets their own token
        assert config.get_bot_token(user_id="user_a") == "token_a"
        assert config.get_bot_token(user_id="user_b") == "token_b"

    async def test_config_service_requires_user_id(self):
        """Config methods must require user_id."""
        config = SlackConfigService()

        with pytest.raises((ValueError, TypeError)):
            config.get_bot_token()  # No user_id = error
```

### Evidence Required

Provide in your handoff:

```markdown
## Phase 7 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in tests/integrations/test_config_service_isolation.py
- `pytest tests/integrations/test_config_service_isolation.py -v` output: [paste]

**Verification**:
```bash
# Confirm all config methods accept user_id
grep -r "def get_.*token\|def get_.*key" services/integrations/*/config_service.py
# All should show user_id parameter
```

**Files Modified**:
- services/integrations/slack/config_service.py (+X/-Y lines)
- [list all files]

**Method Signature Updates**:
| Service | Method | Before | After |
|---------|--------|--------|-------|
| SlackConfigService | get_bot_token | () | (user_id: str) |
| SlackConfigService | get_user_token | () | (user_id: str) |
| [complete table] |
```

### STOP Conditions

Stop and report if:
- Can't determine correct signature for a method
- Caller doesn't have user_id available
- Breaking change cascades unexpectedly
- Tests fail after changes

---

## Coordination Notes

### Parallel Execution

| Wave | Agents | Prerequisite |
|------|--------|--------------|
| Wave 1 | Phase 4 + Phase 5 | Phase 3 complete |
| Wave 2 | Phase 6 + Phase 7 | Wave 1 complete |

### Handoff Protocol

1. Each agent completes their phase with evidence
2. Lead Dev reviews handoff report
3. Lead Dev runs verification commands
4. If passing, Lead Dev approves and moves to next wave
5. If failing, agent addresses issues before proceeding

### Evidence Compilation

All evidence should be collected in the session log at:
`dev/2026/01/30/2026-01-30-1018-lead-code-opus-log.md`

### GitHub Updates

After each phase completion:
```bash
gh issue comment 734 -b "✓ Phase [X] complete
Evidence: [test output / grep / commit]"
```

---

_Prompts created: 2026-01-30_
_Based on: Gameplan v2, Agent Prompt Template v10.2_

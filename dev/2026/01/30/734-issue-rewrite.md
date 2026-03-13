# SEC-MULTITENANCY - Multi-Tenancy Isolation Architecture Implementation

**Priority**: P0
**Labels**: `security`, `architecture`, `refactor`, `alpha-blocker`
**Milestone**: Alpha Testing
**Epic**: Security & Data Isolation
**Related**: #724 (LLM keys), #736 (Projects constraint), ADR-051 (RequestContext), ADR-058 (to be created)

---

## Problem Statement

### Current State

User data leaks between users because multi-tenancy isolation was never fully implemented. Investigation revealed this is not a bug but a **missing architectural layer**.

**Specific Failures**:
1. **OAuth tokens stored globally** - All users share same calendar/Slack/GitHub tokens
2. **OAuth state lacks user identity** - Callbacks can't identify initiating user
3. **RequestContext migration incomplete** - user_id often optional, not enforced
4. **Repository filtering optional** - owner_id parameter defaults to None (no filtering)
5. **Singleton managers use wrong key** - Keyed by session_id (ephemeral) not user_id (persistent)
6. **Config services are user-agnostic** - Return global credentials for all users

**Evidence**: Full audit in `dev/2026/01/30/734-multi-tenancy-audit-report.md`

### Impact

- **Blocks**: Multi-user alpha testing impossible - users see each other's data
- **User Impact**: Critical privacy violation - User A's calendar visible to User B
- **Technical Debt**: Every new integration inherits the broken pattern

### Strategic Context

Alpha testing requires multiple users. This foundational fix enables proper multi-tenant operation and prepares architecture for future workspace/team features.

---

## Goal

**Primary Objective**: Implement complete user isolation so User A's data is never accessible to User B.

**Example User Experience**:
```
BEFORE:
- User A connects Google Calendar
- User B logs in (never connected calendar)
- User B sees User A's calendar events ❌

AFTER:
- User A connects Google Calendar
- User B logs in (never connected calendar)
- User B sees "Calendar not connected" ✅
- User B connects their own calendar
- User B sees only their own events ✅
- User A still sees only their own events ✅
```

**Not In Scope** (explicitly):
- ❌ Workspace/team sharing (future enterprise feature)
- ❌ Admin impersonation capabilities
- ❌ Cross-user data sharing features
- ❌ Migration of existing global tokens (users will re-authenticate)

---

## What Already Exists

### Infrastructure ✅

1. **UserAPIKeyService** (`services/security/user_api_key_service.py`)
   - Correctly implements user-scoped credential storage
   - Uses `username=user_id` parameter
   - Has audit logging

2. **KeychainService** (`services/infrastructure/keychain_service.py`)
   - Supports optional `username` parameter
   - When provided, keys are scoped to user

3. **RequestContext** (`services/domain/models.py`)
   - Defined per ADR-051
   - Has `user_id`, `workspace_id`, `conversation_id`
   - Factory method `from_jwt_and_request()` exists

4. **Repository owner_id parameters**
   - Repositories accept `owner_id` for filtering
   - Pattern exists, just not enforced

### What's Missing ❌

1. **Consistent credential storage** - 38+ locations bypass UserAPIKeyService
2. **OAuth user identification** - State contains only CSRF, not user_id
3. **RequestContext enforcement** - Optional everywhere, not required
4. **Repository isolation** - owner_id optional, defaults to "return all"
5. **Config service user context** - Methods don't accept user_id
6. **Singleton manager scoping** - Keyed by session_id not user_id

---

## Requirements

### Phase -1: OAuth State Infrastructure Investigation

**Objective**: Audit existing OAuth infrastructure before redesigning (PM-requested)

**Tasks**:
- [ ] Document current state generation code (Calendar, Slack)
- [ ] Document current state validation code
- [ ] Document state storage mechanism and expiration
- [ ] Identify what changes are needed for user_id embedding
- [ ] Document findings in investigation report

**Deliverables**:
- `dev/2026/01/30/734-oauth-investigation.md`

### Phase 1: RequestContext Enforcement

**Objective**: Make RequestContext the foundation - required at route boundary

**Tasks**:
- [ ] Create `require_request_context` dependency for authenticated routes
- [ ] Update all authenticated routes to use dependency
- [ ] Services receiving user context: change parameter from Optional to Required
- [ ] Add tests verifying routes without context are rejected

**Deliverables**:
- Modified `services/auth/auth_middleware.py` or new context module
- Updated route files
- Unit tests for context enforcement

### Phase 2: Repository Isolation (owner_id Required)

**Objective**: Make owner_id required - "forcing function" that breaks any code path without user context

**Tasks**:
- [ ] Write failing cross-user isolation tests FIRST (TDD)
- [ ] Change repository methods: owner_id Optional → Required
- [ ] Fix all call sites that now fail
- [ ] Tests pass showing isolation works

**Deliverables**:
- `tests/security/test_cross_user_isolation.py`
- Modified repository files
- All tests green

### Phase 3: OAuth State Redesign

**Objective**: Embed user_id in OAuth state so callbacks can identify user

**Tasks**:
- [ ] Update `generate_authorization_url()` to accept and embed user_id
- [ ] Update `_verify_state()` to extract and return user_id
- [ ] Update OAuth initiation routes to pass current_user.sub
- [ ] Update callback handlers to use extracted user_id for token storage
- [ ] Add tests for state encoding/decoding

**Deliverables**:
- Modified OAuth handlers (Calendar, Slack)
- Modified route files
- Integration tests for OAuth flow with user isolation

### Phase 4: Credential Storage Separation

**Objective**: Separate app credentials from user tokens (per Architect guidance)

**Tasks**:
- [ ] Create `IntegrationConfigService` for app credentials (client_id, client_secret)
- [ ] Ensure `UserAPIKeyService` used for all user tokens
- [ ] Update all 38+ direct keychain calls to use appropriate service
- [ ] Remove direct KeychainService imports from routes

**Deliverables**:
- New `services/integrations/integration_config_service.py`
- Modified route files (setup.py, settings_integrations.py, integrations.py)
- Modified service files

### Phase 5: Config Service Method Signatures

**Objective**: Config services accept user context and return user-scoped data

**Tasks**:
- [ ] Update SlackConfigService methods to accept user_id
- [ ] Update GitHubConfigService methods to accept user_id
- [ ] Update NotionConfigService methods to accept user_id
- [ ] Update CalendarConfigService methods to accept user_id
- [ ] Update all callers to pass user_id

**Deliverables**:
- Modified config service files
- Modified caller files

### Phase 6: Singleton Manager Refactor

**Objective**: Key managers by user_id instead of session_id

**Tasks**:
- [ ] Update PortfolioOnboardingManager to key by user_id
- [ ] Update StandupConversationManager to key by user_id
- [ ] Update ProcessRegistry adapters
- [ ] Add tests verifying user isolation in managers

**Deliverables**:
- Modified manager files
- Modified adapter files
- Isolation tests

### Phase 7: workspace_id Activation

**Objective**: Activate workspace_id field for future multi-tenant support

**Tasks**:
- [ ] Add workspace_id to repository queries (with default value)
- [ ] Add workspace_id to RequestContext creation
- [ ] Document workspace isolation pattern for future use

**Deliverables**:
- Modified repository files
- Updated RequestContext factory
- Documentation

### Phase Z: Completion & Handoff

- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] ADR-058 created and complete
- [ ] GitHub issue fully updated
- [ ] Session log completed

---

## Acceptance Criteria

### Functionality

- [ ] User A's calendar tokens not accessible to User B
- [ ] User A's GitHub token not accessible to User B
- [ ] User A's Slack tokens not accessible to User B
- [ ] User A's LLM keys not accessible to User B
- [ ] User A's onboarding state not visible to User B
- [ ] OAuth callbacks correctly identify initiating user
- [ ] RequestContext required for all authenticated routes

### Testing

- [ ] Cross-user isolation tests written and passing
- [ ] OAuth state encoding/decoding tests passing
- [ ] Repository isolation tests passing
- [ ] All existing tests still passing (no regressions)

### Quality

- [ ] No direct KeychainService calls in routes (all via services)
- [ ] No Optional[user_id] in service method signatures (required)
- [ ] No session_id keying in managers (use user_id)

### Documentation

- [ ] ADR-058: Multi-Tenancy Isolation Architecture created
- [ ] Session log complete with evidence
- [ ] Code documentation updated

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase -1: OAuth Investigation | ❌ | |
| Phase 1: RequestContext Enforcement | ❌ | |
| Phase 2: Repository Isolation | ❌ | |
| Phase 3: OAuth State Redesign | ❌ | |
| Phase 4: Credential Storage | ❌ | |
| Phase 5: Config Services | ❌ | |
| Phase 6: Singleton Managers | ❌ | |
| Phase 7: workspace_id | ❌ | |
| ADR-058 | ❌ | |
| Cross-user isolation tests | ❌ | |

---

## Testing Strategy

### Unit Tests

- RequestContext dependency rejects unauthenticated requests
- OAuth state correctly encodes/decodes user_id
- UserAPIKeyService stores with user scope
- UserAPIKeyService retrieves only user's keys

### Integration Tests

```python
# test_cross_user_isolation.py
async def test_user_a_calendar_not_visible_to_user_b():
    # User A stores calendar token
    await store_token(user_id="user_a", provider="google_calendar", token="token_a")

    # User B retrieves calendar token
    token = await get_token(user_id="user_b", provider="google_calendar")

    # Should be None, not user_a's token
    assert token is None

async def test_user_a_data_isolated_from_user_b():
    # User A creates a list
    list_a = await create_list(owner_id="user_a", name="User A List")

    # User B queries lists
    lists = await get_lists(owner_id="user_b")

    # Should not contain User A's list
    assert list_a.id not in [l.id for l in lists]
```

### Manual Testing Checklist

**Scenario 1**: Calendar Isolation
1. [ ] Log in as User A, connect Google Calendar
2. [ ] Verify User A sees their calendar events
3. [ ] Log out, log in as User B (fresh user)
4. [ ] Verify User B sees "Calendar not connected"
5. [ ] User B connects their calendar
6. [ ] Verify User B sees only their own events

**Scenario 2**: Onboarding Isolation
1. [ ] User A starts onboarding, adds projects
2. [ ] User B logs in, starts onboarding
3. [ ] Verify User B doesn't see User A's captured projects

---

## Success Metrics

### Quantitative
- 0 cross-user data leaks in isolation tests
- 100% of repository methods require owner_id
- 0 direct KeychainService calls in route files

### Qualitative
- Fresh user sees no data from other users
- OAuth flow works seamlessly with user scoping
- Code review shows clear separation of app vs user credentials

---

## STOP Conditions

**STOP immediately and escalate if**:
- Tests fail for any reason
- Cross-user data visible after a phase completes
- OAuth flow breaks (can't connect integrations)
- Existing user data becomes inaccessible unexpectedly
- Performance degrades significantly
- Security concern discovered

---

## Effort Estimate

**Overall Size**: Large (2-4 weeks)

**Breakdown by Phase**:
- Phase -1: Small (investigation)
- Phase 1: Medium (RequestContext)
- Phase 2: Medium (Repositories)
- Phase 3: Medium (OAuth)
- Phase 4: Large (38+ call sites)
- Phase 5: Medium (Config services)
- Phase 6: Small (Managers)
- Phase 7: Small (workspace_id)
- ADR + Documentation: Small

---

## Dependencies

### Required (Must be complete first)

- [x] Chief Architect guidance received
- [ ] ADR-058 created (Phase 0)

### Optional

- [ ] #724 can be closed as duplicate (same root cause)

---

## Related Documentation

- **Architecture**: ADR-051 (RequestContext), ADR-058 (to be created)
- **Patterns**: Pattern-046 (Beads Completion Discipline)
- **Investigation**: `dev/2026/01/30/734-multi-tenancy-audit-report.md`
- **Architect Memo**: `mailboxes/lead/read/memo-arch-to-lead-multitenancy-guidance-2026-01-30.md`

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] Documentation updated ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅

---

## Notes for Implementation

**From Chief Architect**:
- "Break loudly now" over gradual migration - alpha phase favors forcing functions
- Repository owner_id required early creates forcing function
- OAuth state: embed user_id as JSON, base64 encode
- Config services: keep singletons, pass user_id to methods
- Consider JobContext for background tasks

**From PM**:
- LLM keys are per-user in current model
- workspace_id should be activated now
- No migration needed - few alpha users can re-authenticate
- Do it right, timeline is not a constraint

---

**Status**: Ready for Implementation

---

_Issue created: 2026-01-29_
_Rewritten: 2026-01-30 (scope expanded from bug to architectural refactor)_

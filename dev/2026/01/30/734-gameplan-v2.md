# Gameplan: Issue #734 - Multi-Tenancy Isolation Architecture

**Issue**: #734 - SEC-MULTITENANCY: Multi-Tenancy Isolation Architecture Implementation
**Date**: 2026-01-30
**Author**: Lead Developer (Opus)
**Version**: 2.0 (Complete rewrite after scope discovery)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] CLI structure: Click
- [x] Database: PostgreSQL on port 5433
- [x] Testing framework: pytest
- [x] Existing endpoints: OAuth callbacks, settings integrations, setup wizard
- [x] Missing features: User-scoped credential storage, RequestContext enforcement

**My understanding of the task**:
- I believe we need to: Implement complete user isolation across all data access and credential storage
- I think this involves: 7 phases touching auth, repositories, OAuth, config services, and managers
- I assume the current state is: Thoroughly investigated - 38+ direct keychain calls, no user scoping

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [x] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance)
- [x] Multi-component work (routes + services + repositories)
- [x] Exploratory/risky changes where easy rollback is valuable

**Assessment:**
- [x] **USE WORKTREE** - 4 parallel criteria checked

### Part B: PM Verification

**PM confirmed** (2026-01-30):
1. LLM keys are per-user in current model
2. workspace_id should be activated now
3. No migration needed - few alpha users can re-authenticate
4. Do it right, timeline is not a constraint

**Chief Architect guidance received** (2026-01-30):
- Memo in `mailboxes/lead/read/memo-arch-to-lead-multitenancy-guidance-2026-01-30.md`
- Sequencing approved with modifications
- ADR-058 required

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - PM and Architect approved, full investigation complete

---

## Phase 0: Initial Bookending - GitHub Investigation

### Completed Actions

1. **GitHub Issue Verification** ✅
   - Issue #734 exists and rewritten with full scope
   - Related: #724 (duplicate - same root cause), #736

2. **Codebase Investigation** ✅
   - Full audit in `dev/2026/01/30/734-multi-tenancy-audit-report.md`
   - 38+ direct keychain calls identified
   - OAuth state lacks user_id
   - RequestContext optional everywhere

3. **GitHub Issue Updated** ✅
   - Rewritten with feature.md template
   - 7 phases defined with acceptance criteria

### STOP Conditions Check
- [x] Issue exists ✓
- [x] Root cause identified ✓
- [x] Approach determined (Architect-approved) ✓

---

## Phase 0.5: Frontend-Backend Contract Verification

**Applicability**: ❌ N/A - No UI work, backend/service refactor only

---

## Phase 0.6: Data Flow & Integration Verification

### Part A: Data Flow Requirements

**User Context Propagation** (target state after refactor):

| Layer | Needs user_id? | Source of value |
|-------|----------------|-----------------|
| Route handler | Yes | `get_current_user` → RequestContext |
| Service method | Yes | RequestContext parameter (REQUIRED) |
| Repository | Yes | owner_id parameter (REQUIRED) |
| Config service | Yes | user_id parameter to methods |
| OAuth handler | Yes | Embedded in OAuth state |

**State Persistence**:
- [x] Credentials stored in: Keychain with `username=user_id`
- [x] Key for lookup: `user_id` (not session_id)
- [x] State retrieved via: UserAPIKeyService with user_id
- [x] If lookup fails: Return None (not global fallback)

### Part B: Integration Points

| Caller | Callee | Current Status | Target Status |
|--------|--------|----------------|---------------|
| Routes | KeychainService | Direct calls, no user_id | Via UserAPIKeyService |
| Routes | OAuth handlers | No user_id in state | user_id embedded |
| Config services | KeychainService | Global keys | User-scoped keys |
| Managers | Session storage | Keyed by session_id | Keyed by user_id |

### Part C: Pattern Notes

**Breaking change from current pattern:**

| Aspect | Current | Target | Migration |
|--------|---------|--------|-----------|
| Credential lookup | Global | Per-user | Users re-authenticate |
| Repository queries | Optional owner_id | Required owner_id | Fix all call sites |
| OAuth state | CSRF only | CSRF + user_id | Update handlers |

---

## Phase 0.7: Conversation Design

**Applicability**: ❌ N/A - Not a conversational feature

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

| Side Effect | Table/Field | Value | Verified? |
|-------------|-------------|-------|-----------|
| Old global tokens inaccessible | Keychain | N/A | Users re-auth |
| User tokens isolated | Keychain | `{user_id}_{provider}` | [ ] |
| Repository queries filtered | All repos | `owner_id` required | [ ] |
| workspace_id active | RequestContext | Default value set | [ ] |

### Downstream Behavior Changes

| Feature | Before Completion | After Completion |
|---------|-------------------|------------------|
| User A calendar | Visible to all | Visible only to A |
| New user integrations | Sees previous user's data | Sees "Not connected" |
| OAuth connect | Stores globally | Stores per-user |

---

## Development Phases

### TDD Approach (All Phases)

Each phase follows TDD:
1. Write failing tests showing current (broken) isolation
2. Implement fix
3. Tests pass showing isolation works
4. Verify no regressions

---

## Phase 1: ADR-058 Creation

**Objective**: Document architectural decisions before implementation

**Executor**: Lead Developer (direct)

**Tasks**:
- [ ] Create ADR-058 at `docs/internal/architecture/current/adrs/adr-058-multi-tenancy-isolation.md`
- [ ] Document: credential separation, RequestContext enforcement, OAuth state design
- [ ] Reference Chief Architect memo for decisions
- [ ] Link to issue #734

**Deliverables**:
- `docs/internal/architecture/current/adrs/adr-058-multi-tenancy-isolation.md`

**Evidence Required**:
- ADR file exists with all decisions documented

---

## Phase 2: OAuth State Infrastructure Investigation

**Objective**: Audit existing OAuth infrastructure before redesigning (PM-requested Phase -1)

**Executor**: Lead Developer (direct) or Subagent (Explore)

**Tasks**:
- [ ] Document Calendar OAuth state generation (`services/integrations/calendar/oauth_handler.py`)
- [ ] Document Slack OAuth state generation (`services/integrations/slack/oauth_handler.py`)
- [ ] Document state storage mechanism (in-memory dict, expiration)
- [ ] Document state validation logic
- [ ] Identify changes needed for user_id embedding
- [ ] Write investigation report

**Deliverables**:
- `dev/2026/01/30/734-oauth-investigation.md`

**Evidence Required**:
- Code snippets of current state handling
- Diagram or table of proposed changes

---

## Phase 3: RequestContext Enforcement

**Objective**: Make RequestContext the foundation - required at route boundary

**Executor**: Lead Developer (direct) - foundational work

**TDD Tests First**:
```python
# tests/security/test_request_context_enforcement.py
async def test_authenticated_route_requires_context():
    """Route without RequestContext should fail"""
    # Call route without proper auth
    # Assert 401 or context error

async def test_context_contains_user_id():
    """RequestContext must have user_id populated"""
    # Create context from JWT
    # Assert user_id is not None
```

**Tasks**:
- [ ] Write failing tests for context enforcement
- [ ] Create `require_request_context` dependency in `services/auth/`
- [ ] Update `get_current_user` to return RequestContext (not just JWTClaims)
- [ ] Services: change `ctx: Optional[RequestContext]` → `ctx: RequestContext`
- [ ] Tests pass

**Files to Modify**:
- `services/auth/auth_middleware.py`
- `services/domain/models.py` (RequestContext if needed)
- `services/intent/intent_service.py`
- `services/conversation/conversation_handler.py`

**Deliverables**:
- `tests/security/test_request_context_enforcement.py`
- Modified auth middleware
- Updated service signatures

**Evidence Required**:
- Test output showing context enforcement
- Grep showing no more `Optional[RequestContext]` in services

---

## Phase 4: Repository Isolation (owner_id Required)

**Objective**: Make owner_id required - "forcing function" for user context

**Executor**: Subagent (Code Agent) - parallel with Phase 5

**TDD Tests First** (including wiring tests):
```python
# tests/security/test_cross_user_isolation.py
async def test_user_a_data_not_visible_to_user_b():
    """User A's lists should not be returned when querying as User B"""
    # Create list as User A
    list_a = await repo.create(owner_id="user_a", name="A's List")

    # Query as User B
    lists = await repo.get_all(owner_id="user_b")

    # User A's list should NOT be in User B's results
    assert list_a.id not in [l.id for l in lists]

async def test_repository_rejects_none_owner_id():
    """Repository methods must reject None owner_id"""
    with pytest.raises(ValueError):
        await repo.get_all(owner_id=None)
```

**Tasks**:
- [ ] Write failing cross-user isolation tests
- [ ] Change repository method signatures: `owner_id: Optional[str]` → `owner_id: str`
- [ ] Add validation: raise ValueError if owner_id is None
- [ ] Fix all call sites that now fail type checks
- [ ] All tests pass

**Files to Modify**:
- `services/repositories/universal_list_repository.py`
- `services/repositories/todo_repository.py`
- `services/repositories/project_repository.py`
- `services/repositories/file_repository.py`
- All callers of these repositories

**Deliverables**:
- `tests/security/test_cross_user_isolation.py`
- Modified repository files
- Modified caller files

**Evidence Required**:
- Test output showing isolation works
- Grep showing no `owner_id: Optional` in repositories

---

## Phase 5: OAuth State Redesign

**Objective**: Embed user_id in OAuth state so callbacks identify user

**Executor**: Subagent (Code Agent) - can parallel with Phase 4

**TDD Tests First**:
```python
# tests/integrations/test_oauth_state.py
def test_oauth_state_encodes_user_id():
    """OAuth state should contain user_id"""
    handler = GoogleCalendarOAuthHandler()
    auth_url, state = handler.generate_authorization_url(user_id="test-user-123")

    # Decode state and verify user_id
    decoded = handler._decode_state(state)
    assert decoded["user_id"] == "test-user-123"

def test_oauth_callback_extracts_user_id():
    """Callback should extract user_id from state"""
    # Generate state with user_id
    state = handler._encode_state(user_id="test-user-123")

    # Verify extraction
    user_id = handler._extract_user_id_from_state(state)
    assert user_id == "test-user-123"
```

**Tasks**:
- [ ] Write failing tests for state encoding/decoding
- [ ] Update `generate_authorization_url()` to accept and embed user_id
- [ ] Update `_verify_state()` to extract and return user_id
- [ ] Update OAuth initiation routes to require auth and pass current_user.sub
- [ ] Update callback handlers to use extracted user_id for token storage
- [ ] All tests pass

**Files to Modify**:
- `services/integrations/calendar/oauth_handler.py`
- `services/integrations/slack/oauth_handler.py`
- `web/api/routes/setup.py` (OAuth endpoints)
- `web/api/routes/settings_integrations.py` (OAuth endpoints)

**Deliverables**:
- `tests/integrations/test_oauth_state.py`
- Modified OAuth handlers
- Modified route files

**Evidence Required**:
- Test output showing state encoding/decoding
- Manual test: OAuth flow completes with user-scoped token storage

---

## Phase 6: Credential Storage Separation

**Objective**: Separate app credentials from user tokens per Architect guidance

**Executor**: Subagent (Code Agent)

**Tasks**:
- [ ] Create `IntegrationConfigService` for app credentials (client_id, client_secret)
- [ ] Ensure all user tokens go through `UserAPIKeyService`
- [ ] Update all 38+ direct keychain calls to use appropriate service
- [ ] Remove direct `KeychainService` imports from route files

**Files to Modify**:
- NEW: `services/integrations/integration_config_service.py`
- `web/api/routes/setup.py`
- `web/api/routes/settings_integrations.py`
- `web/api/routes/integrations.py`
- `services/integrations/slack/oauth_handler.py`
- `services/integrations/calendar/oauth_handler.py`

**Deliverables**:
- New IntegrationConfigService
- All routes using services instead of direct keychain

**Evidence Required**:
- Grep showing no `keychain.store_api_key` or `keychain.get_api_key` in routes
- Test showing app creds retrieved separately from user tokens

---

## Phase 7: Config Service Method Signatures

**Objective**: Config services accept user context and return user-scoped data

**Executor**: Subagent (Code Agent) - can parallel with Phase 6

**Tasks**:
- [ ] Update `SlackConfigService.get_bot_token(user_id: str)`
- [ ] Update `GitHubConfigService.get_token(user_id: str)`
- [ ] Update `NotionConfigService.get_api_key(user_id: str)`
- [ ] Update `CalendarConfigService` methods with user_id
- [ ] Update all callers to pass user_id

**Files to Modify**:
- `services/integrations/slack/config_service.py`
- `services/integrations/github/config_service.py`
- `services/integrations/notion/config_service.py`
- `services/integrations/calendar/config_service.py`
- All callers

**Deliverables**:
- Modified config service files
- Modified caller files

**Evidence Required**:
- Grep showing all config service methods accept user_id
- Test showing different users get different configs

---

## Phase 8: Singleton Manager Refactor

**Objective**: Key managers by user_id instead of session_id

**Executor**: Lead Developer (direct) - touches foundational code

**TDD Tests First**:
```python
# tests/security/test_manager_isolation.py
async def test_onboarding_isolated_by_user():
    """User A's onboarding state not visible to User B"""
    manager = PortfolioOnboardingManager()

    # Start onboarding for User A
    session_a = manager.start_session(user_id="user_a")
    session_a.add_project("A's Project")

    # Get session for User B
    session_b = manager.get_session(user_id="user_b")

    # User B should have no session or empty session
    assert session_b is None or len(session_b.projects) == 0
```

**Tasks**:
- [ ] Write failing tests for manager isolation
- [ ] Update `PortfolioOnboardingManager` to key by user_id
- [ ] Update `StandupConversationManager` to key by user_id
- [ ] Update `ProcessRegistry` adapters to pass user_id
- [ ] All tests pass

**Files to Modify**:
- `services/onboarding/portfolio_manager.py`
- `services/standup/standup_manager.py`
- `services/process/adapters.py`

**Deliverables**:
- `tests/security/test_manager_isolation.py`
- Modified manager files

**Evidence Required**:
- Test output showing manager isolation
- Code showing `user_id` as dict key instead of `session_id`

---

## Phase 9: workspace_id Activation

**Objective**: Activate workspace_id for future multi-tenant support

**Executor**: Lead Developer (direct)

**Tasks**:
- [ ] Add workspace_id to repository queries (with default "default")
- [ ] Ensure RequestContext.workspace_id populated (default if not provided)
- [ ] Document workspace isolation pattern

**Files to Modify**:
- `services/domain/models.py` (RequestContext)
- Repository files (add workspace_id filter)

**Deliverables**:
- Updated RequestContext
- Updated repositories
- Documentation note in ADR-058

**Evidence Required**:
- Code showing workspace_id in queries
- Test showing default workspace works

---

## Progressive Bookending (All Phases)

After each phase completion:
```bash
gh issue comment 734 -b "✓ Phase [X] complete
Evidence: [test output / grep / commit]"
```

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**
   - Update issue #734 completion matrix
   - All acceptance criteria checked with evidence

2. **Documentation Updates**
   - [x] ADR-058 created (Phase 1)
   - [ ] Update CURRENT-STATE.md
   - [ ] Session log complete

3. **Evidence Compilation**
   - [ ] All test outputs in session log
   - [ ] Cross-user isolation verified
   - [ ] No regressions (full test suite)

4. **PM Approval Request**
   ```
   @PM - Issue #734 complete:
   - All 7 phases complete ✓
   - Cross-user isolation tests passing ✓
   - ADR-058 documented ✓
   - No direct keychain calls in routes ✓

   Please review and close if satisfied.
   ```

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Executor | Can Parallel With | Evidence Required |
|-------|----------|-------------------|-------------------|
| 1 (ADR) | Lead Dev | - | ADR file exists |
| 2 (OAuth Investigation) | Lead Dev or Explore Agent | - | Investigation report |
| 3 (RequestContext) | Lead Dev | - | Test output, grep |
| 4 (Repositories) | Code Agent A | Phase 5 | Test output, grep |
| 5 (OAuth State) | Code Agent B | Phase 4 | Test output, manual verify |
| 6 (Credential Storage) | Code Agent A | Phase 7 | Grep, test |
| 7 (Config Services) | Code Agent B | Phase 6 | Grep, test |
| 8 (Managers) | Lead Dev | - | Test output |
| 9 (workspace_id) | Lead Dev | - | Code review |

### Verification Gates

- [ ] Phase 3 complete: RequestContext required everywhere
- [ ] Phase 4 complete: Repositories require owner_id
- [ ] Phase 5 complete: OAuth embeds user_id
- [ ] Phase 6 complete: No direct keychain in routes
- [ ] Phase 8 complete: Managers keyed by user_id
- [ ] All tests pass: `pytest tests/security/`

### Handoff Quality Checklist

Before accepting handoff from any agent:
- [ ] All tests passing with output provided
- [ ] Files modified list included
- [ ] No regressions (existing tests pass)
- [ ] Evidence matches acceptance criteria

---

## STOP Conditions

Stop immediately and escalate if:
- Tests fail after any phase
- Cross-user data visible after fix
- OAuth flow breaks (can't connect)
- Performance degrades significantly
- Existing user data inaccessible unexpectedly

---

## Evidence Requirements

✅ Terminal output showing test results
✅ Grep output showing pattern removal
✅ Before/after code snippets
✅ Manual test of OAuth flow

❌ "Tests pass" without output
❌ "Fixed" without proof

---

## Success Criteria

| Criterion | How to Verify |
|-----------|--------------|
| No direct keychain calls in routes | `grep -r "keychain\.(store\|get)_api_key" web/api/routes/` returns empty |
| Repositories require owner_id | `grep -r "owner_id: Optional" services/repositories/` returns empty |
| OAuth state has user_id | Tests pass + manual OAuth flow test |
| Managers keyed by user_id | Code inspection + isolation tests |
| Cross-user isolation | `tests/security/test_cross_user_isolation.py` all pass |

---

_Gameplan created: 2026-01-30_
_Based on: Chief Architect memo, PM guidance, full codebase audit_

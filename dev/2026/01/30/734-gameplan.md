# Gameplan: Issue #734 - Multi-Tenancy Token Isolation

**Issue**: #734 - CRITICAL: Calendar and integration tokens leak between users
**Date**: 2026-01-30
**Author**: Lead Developer (Opus)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] CLI structure: Click
- [x] Database: PostgreSQL on port 5433
- [x] Testing framework: pytest
- [x] Existing endpoints: `/api/v1/intent`, `/settings/integrations/*`, `/setup/*`
- [x] Missing features: User-scoped token storage/retrieval

**My understanding of the task**:
- I believe we need to: Add `user_id` parameter to all keychain store/retrieve calls for integration tokens
- I think this involves: Modifying routes, services, and adapters to thread `user_id` through
- I assume the current state is: Tokens stored globally, causing cross-user data leaks

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [x] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance)
- [x] Multi-component work (routes + services + adapters)
- [ ] Exploratory/risky changes where easy rollback is valuable

**Assessment:**
- [x] **USE WORKTREE** - 3 parallel criteria checked

### Part B: PM Verification Required

**PM, please confirm**:

1. **Actual task needed?**
   - [x] Fix broken functionality (multi-tenancy violation)

2. **Critical context**:
   - `UserAPIKeyService` already exists with correct pattern
   - Routes bypass it and call keychain directly
   - Need to route all calls through `UserAPIKeyService`

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - PM approved 2026-01-30
- [ ] **REVISE** - If assumptions wrong
- [ ] **CLARIFY** - If more context needed

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification** ✅
   - Issue #734 exists and is OPEN
   - Root cause documented with code evidence
   - Related to #724 (LLM keys) and #736 (Projects constraint - now fixed)

2. **Codebase Investigation**

   **Storage locations needing fix** (6 total):
   | File | Line | Current | Fix |
   |------|------|---------|-----|
   | `web/api/routes/setup.py` | 742 | `keychain.store_api_key("openai", key)` | Use UserAPIKeyService |
   | `web/api/routes/setup.py` | 749 | `keychain.store_api_key("anthropic", key)` | Use UserAPIKeyService |
   | `web/api/routes/setup.py` | 1060 | `keychain.store_api_key("google_calendar", token)` | Use UserAPIKeyService |
   | `web/api/routes/settings_integrations.py` | 926 | `keychain.store_api_key("google_calendar", token)` | Use UserAPIKeyService |
   | `web/api/routes/settings_integrations.py` | 1602 | `keychain.store_api_key("github_token", token)` | Use UserAPIKeyService |
   | `web/api/routes/settings_integrations.py` | 613-614 | `keychain.store_api_key("slack_*", ...)` | Use UserAPIKeyService |

   **Retrieval locations needing fix** (3+ total):
   | File | Line | Current | Fix |
   |------|------|---------|-----|
   | `services/mcp/consumer/google_calendar_adapter.py` | 245 | `keychain.get_api_key("google_calendar")` | Add user_id param |
   | `services/config/llm_config_service.py` | 199 | `keychain.get_api_key(provider)` | Add user_id param |
   | `services/integrations/github/config_service.py` | 145 | `keychain.get_api_key("github_token")` | Add user_id param |

3. **Correct Pattern Already Exists**:
   ```python
   # services/security/user_api_key_service.py
   # Line 148 (CORRECT - store)
   self._keychain.store_api_key(provider, api_key, username=user_id)

   # Line 254 (CORRECT - retrieve)
   api_key = self._keychain.get_api_key(provider, username=user_id)
   ```

### STOP Conditions Check
- [x] Issue exists ✓
- [x] Root cause identified ✓
- [x] Correct pattern exists (UserAPIKeyService) ✓

---

## Phase 0.5: Frontend-Backend Contract Verification

**Applicability**: ❌ N/A - Backend-only changes (no UI work)

---

## Phase 0.6: Data Flow & Integration Verification

### Part A: Data Flow Requirements

**User Context Propagation**:

| Layer | Needs user_id? | Source of value |
|-------|----------------|-----------------|
| Route handler | Yes | `get_current_user` dependency → `current_user.sub` |
| UserAPIKeyService | Yes | Parameter from route |
| KeychainService | Yes | `username` parameter |

### Part B: Integration Points

| Caller | Callee | Import Path | Parameters |
|--------|--------|-------------|------------|
| setup.py routes | UserAPIKeyService | `services.security.user_api_key_service` | `user_id`, `provider`, `key` |
| settings_integrations.py | UserAPIKeyService | Same | Same |
| google_calendar_adapter.py | UserAPIKeyService | Same | `user_id`, `provider` |
| llm_config_service.py | UserAPIKeyService | Same | `user_id`, `provider` |
| github/config_service.py | UserAPIKeyService | Same | `user_id`, `provider` |

### Part C: Pattern Notes

**Current (broken)**:
```
Route → KeychainService.store_api_key(provider, key)  # No user_id!
```

**Target (correct)**:
```
Route → UserAPIKeyService.store_user_key(user_id, provider, key)
      → KeychainService.store_api_key(provider, key, username=user_id)
```

---

## Phase 0.7: Conversation Design

**Applicability**: ❌ N/A - Not a conversational feature

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

When fix is complete:

| Side Effect | Verification |
|-------------|--------------|
| Tokens stored with user prefix | `security find-generic-password -s "piper-morgan" -a "{user_id}_google_calendar"` |
| Old tokens no longer accessible | New users see "not connected" |
| Each user's tokens isolated | User A's calendar not visible to User B |

### Migration Consideration

**Existing tokens** stored without user prefix will become inaccessible. Options:
1. Require users to re-connect integrations (simplest)
2. Migration script to re-key existing tokens (requires knowing owner)

**Recommendation**: Option 1 for alpha - require re-connect. Document in release notes.

---

## Phase 1: Fix Storage Layer (Routes)

### 1.1 Update setup.py

**Files**: `web/api/routes/setup.py`

**Changes**:
1. Import `UserAPIKeyService`
2. Get `user_id` from `current_user.sub`
3. Replace direct keychain calls with UserAPIKeyService calls

**Acceptance Criteria**:
- [ ] Line 742: `keychain.store_api_key("openai", ...)` → `user_api_key_service.store_user_key(user_id, "openai", ...)`
- [ ] Line 749: Same for anthropic
- [ ] Line 1060: Same for google_calendar
- [ ] Tests pass

### 1.2 Update settings_integrations.py

**Files**: `web/api/routes/settings_integrations.py`

**Changes**:
1. Import `UserAPIKeyService`
2. Replace direct keychain calls

**Acceptance Criteria**:
- [ ] Line 926: google_calendar storage uses user_id
- [ ] Line 1602: github_token storage uses user_id
- [ ] Lines 613-614: slack credentials use user_id
- [ ] Tests pass

---

## Phase 2: Fix Retrieval Layer (Services/Adapters)

### 2.1 Update google_calendar_adapter.py

**Files**: `services/mcp/consumer/google_calendar_adapter.py`

**Changes**:
1. Add `user_id` parameter to `_authenticate_from_keychain()` method
2. Thread `user_id` from caller through to keychain call
3. Update all callers to pass `user_id`

**Acceptance Criteria**:
- [ ] `_authenticate_from_keychain(user_id)` accepts user_id
- [ ] Keychain call uses `username=user_id`
- [ ] All callers updated
- [ ] Tests pass

### 2.2 Update llm_config_service.py

**Files**: `services/config/llm_config_service.py`

**Changes**:
1. Add `user_id` parameter to `get_api_key()` method
2. Pass through to keychain
3. Update all callers

**Acceptance Criteria**:
- [ ] `get_api_key(provider, user_id)` signature updated
- [ ] All callers pass user_id
- [ ] Tests pass

### 2.3 Update github/config_service.py

**Files**: `services/integrations/github/config_service.py`

**Changes**:
1. Add `user_id` to retrieval methods
2. Update callers

**Acceptance Criteria**:
- [ ] Token retrieval uses user_id
- [ ] Tests pass

---

## Phase 3: Thread user_id Through Call Chains

### 3.1 Identify All Callers

Callers that need user_id added:
- `CalendarIntegrationRouter` → `GoogleCalendarMCPAdapter`
- `IntentService` → `LLMConfigService`
- `CanonicalHandlers` → various integrations

### 3.2 Update Each Call Chain

**Acceptance Criteria**:
- [ ] All paths from route to keychain have user_id
- [ ] No keychain calls without user scoping remain
- [ ] Integration tests verify isolation

---

## Phase 4: Verification & Testing

### 4.1 Unit Tests

- [ ] Test UserAPIKeyService stores with user prefix
- [ ] Test UserAPIKeyService retrieves only user's keys
- [ ] Test different users get different keys
- [ ] **Wiring tests**: Verify UserAPIKeyService.store_user_key() and .get_user_key() are called with correct user_id from routes through to keychain

### 4.2 Integration Tests

- [ ] User A connects calendar → only User A sees events
- [ ] User B (no calendar) → sees "not connected"
- [ ] User A's LLM keys not used by User B

### 4.3 Manual Verification

```bash
# Check keychain entries have user prefix
security find-generic-password -s "piper-morgan" -a "{user_id}_google_calendar"
```

---

## Phase Z: Final Bookending

### Evidence Required

- [ ] All storage calls use UserAPIKeyService
- [ ] All retrieval calls include user_id
- [ ] No cross-user data visible
- [ ] Tests passing with output
- [ ] GitHub issue updated with evidence

### Documentation Updates

- [ ] ADR if architectural decision made
- [ ] Release notes: "Users must re-connect integrations after update"

---

## Success Criteria

1. User A's calendar tokens not accessible to User B
2. User A's LLM keys not used by User B
3. User A's GitHub integration not visible to User B
4. All existing tests pass
5. New isolation tests pass

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Existing tokens become inaccessible | Document in release notes, require re-connect |
| Missing a call site | Grep for all `keychain.store_api_key` and `keychain.get_api_key` |
| Breaking existing functionality | Run full test suite after each phase |

---

## Estimated Effort

| Phase | Estimate |
|-------|----------|
| Phase 1 (Storage) | 1-2 hours |
| Phase 2 (Retrieval) | 1-2 hours |
| Phase 3 (Call chains) | 2-3 hours |
| Phase 4 (Testing) | 1-2 hours |
| **Total** | 5-9 hours |

---

## Agent Deployment

| Phase | Agent | Task |
|-------|-------|------|
| 1 | Code Agent A | Fix setup.py storage |
| 1 | Code Agent B | Fix settings_integrations.py storage |
| 2 | Code Agent A | Fix calendar adapter |
| 2 | Code Agent B | Fix LLM config service |
| 3 | Lead Dev | Thread user_id through call chains |
| 4 | Lead Dev | Integration testing |

# Gameplan: #746 - Auth Context Injection for Hardcoded user_id Values

**Issue**: #746 - [TECH-DEBT] Auth context injection for hardcoded user_id values
**Date**: 2026-02-01
**Estimated Effort**: Small-Medium

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Authentication: JWT via `get_current_user` dependency
- [x] Database: PostgreSQL (user_id is UUID, FK to users table)
- [x] Testing framework: pytest
- [x] Existing endpoints: `/api/v1/todos/{id}` (PATCH, DELETE) already exist
- [x] Reference implementation: #745 fixed intent service path

**My understanding of the task**:
- 5 endpoints have hardcoded `user_id` values that bypass authentication
- Need to inject real authenticated user via FastAPI dependency injection
- Pattern exists from #745 fix - this is applying same pattern to REST API paths

### Part A.2: Work Characteristics Assessment

**Worktree Assessment:**
- [ ] Multiple agents will work in parallel - NO
- [ ] Task duration >30 minutes - MAYBE (depends on testing depth)
- [ ] Multi-component work - NO (same pattern repeated)
- [ ] Exploratory/risky changes - NO (well-defined pattern)

**Assessment:** ✅ **SKIP WORKTREE** - Single agent, repetitive pattern, reference implementation exists

### Part B: PM Verification

**What exists:**
- `get_current_user` dependency in `services/auth/auth_middleware.py`
- 4 todo endpoints in `services/api/todo_management.py`
- 1 Notion key endpoint in `web/api/routes/settings_integrations.py`
- Reference fix in `services/intent/intent_service.py` (#745)

### Part C: Proceed/Revise Decision
- [x] **PROCEED** - Understanding is correct, pattern is established

---

## Phase 0: Initial Bookending - Investigation

### Required Verification

```bash
# Verify get_current_user dependency exists and works
grep -n "get_current_user" services/auth/auth_middleware.py web/api/routes/*.py

# Verify affected endpoints
grep -n "user_id=\"default" services/api/todo_management.py web/api/routes/settings_integrations.py

# Check how other endpoints use get_current_user
grep -n "current_user.*Depends" web/api/routes/*.py | head -10
```

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - These are backend-only changes. No frontend modifications needed.

---

## Phase 0.6: Data Flow Verification

### User Context Propagation

| Layer | Needs user_id? | Source |
|-------|----------------|--------|
| FastAPI Route | ✅ Yes | `current_user: User = Depends(get_current_user)` |
| Service Method | ✅ Yes | `current_user.id` passed as parameter |

**Verification**: This is simpler than #745 - direct route → service call, no multi-layer propagation.

---

## Phase 0.7: Conversation Design

**N/A** - Not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

**N/A** - No new user state changes. Existing functionality, just with proper auth.

---

## Phase 1: Fix todo_management.py (4 instances)

**Objective**: REST API todo endpoints use authenticated user

### Tasks

1. **Add auth dependency to update_todo endpoint**
   - Import `get_current_user` if not already imported
   - Add `current_user: User = Depends(get_current_user)` parameter
   - Replace `user_id="default-user"` with `current_user.id`

2. **Add auth dependency to delete_todo endpoint**
   - Same pattern as above

3. **Update OpenAPI metadata**
   - Endpoints should show authentication required

### Evidence Required

```bash
# After fix, verify no hardcoded user_id remains
grep "default-user" services/api/todo_management.py
# Should return nothing

# Test endpoint works with auth
curl -X PATCH http://localhost:8001/api/v1/todos/{id} \
  -H "Cookie: auth_token=..." \
  -d '{"status": "completed"}'
```

---

## Phase 2: Fix settings_integrations.py (1 instance)

**Objective**: Notion API key stored per-user

### Tasks

1. **Add auth dependency to Notion key storage**
   - Add `current_user` parameter
   - Replace `user_id="system"` with `current_user.id`

2. **Consider data migration**
   - Check if existing keys stored under "system" need migration
   - Document if manual migration required

### Evidence Required

```bash
# Verify no hardcoded user_id
grep "user_id=\"system\"" web/api/routes/settings_integrations.py
# Should return nothing
```

---

## Phase Z: Final Bookending & Handoff

### Success Criteria

- [ ] No hardcoded user_id values in affected files (grep verification)
- [ ] All endpoints return 401 for unauthenticated requests
- [ ] User isolation works (User A can't modify User B's data)
- [ ] All existing tests still pass
- [ ] New security tests added

### STOP Conditions

- `get_current_user` not available in affected route files
- Existing tests break (may indicate hidden dependencies on "default-user")
- Notion keys migration complexity exceeds scope

---

## Multi-Agent Coordination

**Not Required** - Single agent, sequential fixes.

---

## Evidence Requirements

| What | How |
|------|-----|
| No hardcoded values | `grep` output showing 0 matches |
| Auth working | curl/test output showing 401 for unauth |
| User isolation | Test output showing cross-user access blocked |
| No regressions | pytest output |

---

*Gameplan version: 1.0*
*Based on gameplan-template.md v9.3*

# Gameplan: Fix Cookie Authentication Mismatch (Issue #393)

**Date**: 2025-11-27 12:45 PM
**Agent**: Claude Code (Programmer)
**Issue**: #393 - [UX-AUTH] No login UI - users cannot authenticate despite complete backend
**Type**: Bug Fix - Critical Blocker

---

## Problem Statement

**Critical Bug Found**: Cookie name mismatch prevents authentication from working.

- **Backend sets cookie**: `auth_token` ([web/api/routes/auth.py:195](web/api/routes/auth.py#L195))
- **Middleware expects**: `access_token` ([services/auth/auth_middleware.py:206](services/auth/auth_middleware.py#L206))
- **Result**: Users appear unauthenticated despite having valid token

**Impact**: Login UI completely non-functional. Alpha users cannot authenticate via web UI.

---

## Root Cause Analysis

Investigation by haiku agent revealed:

1. Login endpoint creates JWT and sets cookie with key `auth_token`
2. On subsequent requests, middleware's `_extract_token()` looks for `access_token` cookie
3. Cookie mismatch means token is never found
4. User remains unauthenticated despite successful login

**Evidence**:
```python
# web/api/routes/auth.py:195
response.set_cookie(
    key="auth_token",  # ← Sets this name
    ...
)

# services/auth/auth_middleware.py:206
token = request.cookies.get("access_token")  # ← Expects this name
```

---

## Solution Design

**Option A**: Rename `auth_token` → `access_token` in auth.py (RECOMMENDED)
- **Pro**: `access_token` is more standard OAuth 2.0 naming
- **Pro**: Matches middleware expectations (fewer changes)
- **Pro**: Consistent with Authorization header pattern
- **Con**: None

**Option B**: Rename `access_token` → `auth_token` in middleware
- **Pro**: Matches current cookie name
- **Con**: Non-standard naming
- **Con**: Confusing (header uses `access_token`, cookie uses `auth_token`)

**Decision**: Option A - Use `access_token` everywhere for consistency.

---

## Implementation Plan

### Phase 1: Fix Cookie Name (5 minutes)

**File**: `web/api/routes/auth.py`

**Change**: Line 195
```python
# Before
response.set_cookie(
    key="auth_token",
    ...
)

# After
response.set_cookie(
    key="access_token",
    ...
)
```

### Phase 2: Update Logout Endpoint (5 minutes)

**File**: `web/api/routes/auth.py`

**Review**: Logout endpoint (lines 236-250) to ensure it clears the correct cookie name.

**Expected**: Should already reference `auth_token` - update to `access_token` if found.

### Phase 3: Verification (10 minutes)

**Automated Tests**:
```bash
# Run auth tests
pytest tests/unit/services/auth/ -xvs
pytest tests/integration/auth/ -xvs -k "login"
```

**Code Verification**:
```bash
# Search for remaining auth_token references
grep -r "auth_token" web/ services/ --include="*.py"
# Should only find historical comments or unrelated uses
```

---

## Completion Matrix

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Cookie name changed to `access_token` | ⬜ | Commit shows line 195 updated |
| Logout endpoint uses correct cookie name | ⬜ | Code review confirms |
| No remaining `auth_token` cookie references | ⬜ | grep search returns clean |
| Auth middleware finds cookie | ⬜ | Code inspection confirms match |
| Tests pass | ⬜ | pytest output shows all green |
| No regressions in auth flow | ⬜ | Test suite validates |

**Definition of Done**: All 6 criteria checked ✅

---

## Stop Conditions

**STOP if**:
1. Tests fail after cookie rename
2. Additional cookie references found that break compatibility
3. Logout endpoint has complex dependencies on cookie name
4. Any auth-related code shows unexpected behavior

**Escalate to PM if**: Cookie name has other dependencies not visible in grep search.

---

## Manual Testing Required (Post-Fix)

For xian when he returns:

1. **Login Flow** (5 minutes):
   - Navigate to `http://localhost:8001/login`
   - Enter valid credentials
   - Should redirect to `/` with user menu showing

2. **Cookie Persistence** (2 minutes):
   - After login, refresh page
   - User menu should still show (cookie persisted)

3. **Logout** (2 minutes):
   - Click logout button
   - Should clear cookie and return to login page

4. **Unauthenticated Access** (2 minutes):
   - Open incognito window
   - Visit `/`
   - Should show "Login" link, not user menu

**Total manual testing**: ~11 minutes

---

## Risk Assessment

**Risk Level**: LOW

**Risks**:
- Cookie name might be referenced in frontend JavaScript → Mitigated: auth.js uses `credentials: 'include'` (browser handles cookies automatically)
- Existing sessions might break → Expected: Users will need to re-login (acceptable for alpha)
- Logout might not clear cookie → Will verify during Phase 2

**Mitigation**: Thorough grep search + test suite validation

---

## Dependencies

**None** - This is a simple rename operation.

---

## Estimated Effort

- **Phase 1**: 5 minutes (cookie rename)
- **Phase 2**: 5 minutes (logout verification)
- **Phase 3**: 10 minutes (testing & verification)
- **Total**: 20 minutes

---

## Success Criteria

**Code Complete**:
- ✅ Cookie name is `access_token` throughout codebase
- ✅ All auth tests pass
- ✅ No grep results for `auth_token` cookie usage

**Manual Testing** (by PM):
- ✅ Login redirects to home with user menu
- ✅ Page refresh maintains authentication
- ✅ Logout clears session
- ✅ Unauthenticated users see login link

---

## Notes

- This fixes a **critical alpha blocker** - login UI non-functional without it
- Investigation credit: haiku agent found the mismatch during #393 review
- Frontend code doesn't need changes (uses browser's automatic cookie handling)
- Standard OAuth 2.0 naming: `access_token` for both header and cookie

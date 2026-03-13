# Session Log: Logout Bug Fix (piper-morgan-fb9)

**Date**: 2026-01-09
**Time**: 21:00
**Agent**: Code (Claude Code Opus 4.5)
**Bead**: piper-morgan-fb9
**Issue**: Logout returns 403 'Not authenticated' - auth/logout endpoint broken

## Investigation Summary

### Problem
The `/auth/logout` endpoint returns 403 "Not authenticated" when users try to log out.

### Root Cause Analysis

The issue has **two contributing factors**:

#### Factor 1: AuthMiddleware blocks invalid tokens before route executes
- `/auth/logout` is NOT in the middleware's `exclude_paths` list
- If token is invalid/expired/revoked, middleware returns 401 immediately
- Route handler never gets a chance to execute

**Location**: `services/auth/auth_middleware.py` line 36-82 (`__init__`)

#### Factor 2: HTTPBearer dependency returns 403 when no auth header present
- The logout route uses `credentials: HTTPAuthorizationCredentials = Depends(security)`
- FastAPI's `HTTPBearer()` returns **403** "Not authenticated" when no Authorization header is present
- This is a [known FastAPI issue](https://github.com/fastapi/fastapi/issues/2026)

**Location**: `web/api/routes/auth.py` line 33 (`security = HTTPBearer()`)

### The User Experience Problem

Users trying to logout face these issues:
1. If their token is invalid/expired - middleware blocks with 401
2. If they don't send Authorization header - HTTPBearer blocks with 403
3. Even if their token is already revoked - they can't "log out" (though they're already logged out)

### Solution Design

The fix requires:

1. **Add `/auth/logout` to middleware `exclude_paths`**
   - Let requests through to the route handler regardless of token state
   - The route handler will manage authentication itself

2. **Modify logout route to handle tokens gracefully**
   - Make `credentials` optional using `auto_error=False` on HTTPBearer
   - Handle case where token is missing, invalid, or already revoked
   - Return success in all cases (user ends up logged out either way)

## Implementation

### Change 1: Add /auth/logout to exclude_paths

File: `services/auth/auth_middleware.py`

Added `/auth/logout` to `exclude_paths` with comment explaining why.

### Change 2: Make HTTPBearer optional and handle gracefully

File: `web/api/routes/auth.py`

- Changed `security = HTTPBearer()` to `security = HTTPBearer(auto_error=False)`
- Modified logout route to handle `None` credentials gracefully
- Return success message when token is missing (user is already logged out)

## Testing

```bash
# Relevant logout test - PASSED
python -m pytest tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_logout_clears_cookie -v

# Token blacklist tests - ALL 17 PASSED
python -m pytest tests/unit/services/auth/test_token_blacklist.py -v
```

### Test Results

- `test_logout_clears_cookie` - PASSED
- All 17 token blacklist tests - PASSED
- Pre-existing failures in login tests (unrelated to this fix) - form/JSON data mismatch in tests

## Files Modified

1. `services/auth/auth_middleware.py` (line 65) - Added `/auth/logout` to exclude_paths
2. `web/api/routes/auth.py`:
   - Line 33-34: Changed `security = HTTPBearer()` to `security = HTTPBearer(auto_error=False)`
   - Lines 238-305: Rewrote `logout()` function to handle optional credentials gracefully
   - Line 396: Updated `change_password()` to use `Optional[HTTPAuthorizationCredentials]`
   - Lines 465-470: Added credentials None check in `change_password()`

## Key Changes in Logout Function

The new logout function:
1. Extracts token from Authorization header OR auth_token cookie
2. If no token: returns success (user is already logged out)
3. If token found: tries to validate it for logging purposes (but doesn't fail if invalid)
4. Revokes the token via blacklist
5. Returns success regardless of revocation result (user ends up logged out either way)

## References

- [FastAPI HTTPBearer 403 issue](https://github.com/fastapi/fastapi/issues/2026)
- Related: Issue #490 (same middleware-route contract violation pattern)

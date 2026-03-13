# Issue #14 Investigation: Login/Logout UI Broken

**Date**: November 23, 2025
**Investigator**: Code Agent
**Duration**: 12 minutes
**Status**: Complete

---

## Summary

Login/Logout UI is partially broken, but for a different reason than Issues #6/#7. The **frontend UI buttons exist and are fully wired** - both logout and login/account navigation are present in the navigation component. The **backend auth endpoints exist and are fully implemented** (`POST /auth/login`, `POST /auth/logout`, `GET /auth/me`). However, there's a **critical mismatch between frontend and backend**:

- Frontend logout handler calls `POST /api/v1/auth/logout` (incorrect path prefix)
- Backend route is mounted at `/auth/logout` (not `/api/v1/auth/logout`)

This is **Type A: Quick Fix** (5-10 minutes) - just change the endpoint path.

Additionally, there's no dedicated login page/route (`GET /login`) - users must be logged in to see the app. This may be intentional alpha design, but it's worth noting.

---

## Frontend Analysis

**User Menu Location**: `templates/components/navigation.html:320-350`

```html
<!-- User Menu -->
<div class="nav-user">
  <button class="user-button" aria-haspopup="true" aria-expanded="false" id="user-menu-button">
    <span class="user-avatar" id="user-avatar">U</span>
    <span class="user-name" id="user-name">User</span>
    <svg class="user-chevron" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M4 6l4 4 4-4"/>
    </svg>
  </button>

  <div class="user-dropdown" hidden id="user-dropdown">
    <a href="/settings" class="dropdown-item" id="dropdown-settings">
      <svg><!-- settings icon --></svg>
      Settings
    </a>
    <a href="/account" class="dropdown-item" id="dropdown-account">
      <svg><!-- account icon --></svg>
      Account
    </a>
    <hr class="dropdown-divider">
    <a href="#" class="dropdown-item dropdown-item-danger" id="dropdown-logout" onclick="handleLogout(event)">
      <svg><!-- logout icon --></svg>
      Logout
    </a>
  </div>
</div>
```

**Status**: ✅ User menu fully implemented with logout button

**JavaScript Handler**: `templates/components/navigation.html:477-501`

**Function Name**: `handleLogout(event)`

**Status**: ✅ Exists and wired correctly - but **WRONG ENDPOINT**

### Logout Handler Code

```javascript
// G8: Handle logout - POST to /api/v1/auth/logout
async function handleLogout(event) {
  event.preventDefault();

  try {
    const response = await fetch('/api/v1/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include' // Include authentication cookies
    });

    if (response.ok) {
      // Redirect to login or home page
      window.location.href = '/';
    } else {
      const data = await response.json();
      alert('Logout failed: ' + (data.detail || 'Unknown error'));
    }
  } catch (error) {
    console.error('Logout error:', error);
    alert('Logout failed: ' + error.message);
  }
}
```

**Problem**: Line 482 calls `POST /api/v1/auth/logout` but the backend endpoint is actually at `POST /auth/logout` (missing `/v1` prefix).

**Additional Features**:
- User dropdown menu renders correctly (lines 330-350)
- Settings and Account links exist (navigation to existing pages)
- Mobile menu handling implemented (hamburger menu for <480px)
- User avatar and name populated from window.currentUser (lines 470-472)

---

## Backend Analysis

**Auth Router**: `web/api/routes/auth.py` - Mount point at `/auth` (not `/api/v1/auth`)

**Routes that EXIST**:
- ✅ `POST /auth/login` (lines 70-221) - Full implementation
- ✅ `POST /auth/logout` (lines 224-290) - Full implementation with token blacklist
- ✅ `GET /auth/me` (lines 293-344) - Get current user
- ✅ `POST /auth/change-password` (lines 347-487) - Change password

**Router Mount**: `web/app.py:595-598`

```python
from web.api.routes.auth import router as auth_router
app.include_router(auth_router)
logger.info("✅ Auth API router mounted at /auth (login, logout endpoints)")
```

**Status**: ✅ Auth endpoints are fully implemented and mounted correctly

### Logout Endpoint Details

```python
@router.post("/logout")
async def logout(
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Logout user by revoking their access token.
    Token will be added to blacklist and no longer valid.
    """
    token = credentials.credentials
    try:
        # ... token revocation via blacklist ...
        return {"message": "Logged out successfully", "user_id": current_user.user_id}
    except Exception as e:
        raise HTTPException(...)
```

**Security Features**:
- ✅ Requires authentication (depends on `get_current_user`)
- ✅ Revokes token via blacklist (doesn't just remove cookie)
- ✅ Even expired tokens won't work after logout
- ✅ Audit logging with user_id

---

## Root Cause Analysis

**Classification**: **Type A (Quick Fix)**

**The Issue**:
The frontend `handleLogout()` function calls the wrong endpoint path:
- Frontend calls: `POST /api/v1/auth/logout` ❌
- Backend provides: `POST /auth/logout` ✅

This causes a 404 error when users try to logout.

**Why This Happened**:
Inconsistency in endpoint naming conventions. The codebase has mixed naming:
- Most API routes use `/api/v1/` prefix (e.g., `/api/v1/lists`, `/api/v1/todos`)
- Auth router was mounted at `/auth` without the `/api/v1/` prefix
- Frontend developer assumed the convention applied to auth routes too

**Impact**:
- Logout button appears and clicks, but fails with 404
- User sees "Logout failed: Unknown error"
- Token is not revoked, remains active
- User can still access page by refreshing

---

## Secondary Findings: Login Page Gap

**Finding**: There is NO `GET /login` route in web/app.py
- Frontend calls `POST /auth/login` ✅ (endpoint exists)
- But there's no login page (`GET /login`)
- No login form for unauthenticated users

**Current Flow**:
1. User arrives at `/` (home page)
2. `_extract_user_context()` is called but doesn't redirect
3. If unauthenticated, `window.currentUser` is null (line 71 in navigation.html)
4. Navigation component shows "User" as default name (line 324)

**Status**: This appears to be **intentional alpha design**:
- No login page built yet (Type D - Known Gap)
- Users are expected to exist in database already
- Token management is API-first (curl commands for testing)
- This is consistent with "alpha" state mentioned in gameplan

**Recommendation**: Not blocking - this is intentional for alpha testing phase.

---

## Fix Estimate

**Effort**: 5-10 minutes (Type A)

**What Needs to Happen**:

1. **Frontend Fix (2 minutes)**:
   - Update `handleLogout()` function in templates/components/navigation.html:482
   - Change `/api/v1/auth/logout` → `/auth/logout`

2. **Testing (3 minutes)**:
   - Click logout button, verify no error
   - Verify token is revoked
   - Verify page redirects to home

**Note**: Could also standardize to `/api/v1/auth/logout` by adding a route alias in web/app.py, but path fix is simpler.

---

## Recommendation

**Action**: **Fix This Issue** (Type A - Quick fix, 5-10 minutes)

**Reasoning**:
1. Endpoint path mismatch is simple one-line fix
2. Blocks logout functionality (can't test multi-user scenarios)
3. Security implication: tokens aren't revoked on logout
4. Quick win that unblocks alpha testing
5. No architectural changes needed

**Implementation**:
1. Change line 482 in templates/components/navigation.html from:
   ```javascript
   const response = await fetch('/api/v1/auth/logout', {
   ```
   to:
   ```javascript
   const response = await fetch('/auth/logout', {
   ```
2. Test logout button works

**Alternative**: If we want to follow RESTful `/api/v1/` convention everywhere:
- Add route alias in web/app.py: `app.include_router(auth_router, prefix="/api/v1")`
- But current backend structure doesn't support this without breaking cookie-based auth

---

## Evidence

**Frontend Button**: templates/components/navigation.html:344
**Function Code**: templates/components/navigation.html:477-501
**Wrong Endpoint Called**: templates/components/navigation.html:482 (calls `/api/v1/auth/logout`)
**Backend Route Location**: web/api/routes/auth.py:224
**Mount Point**: web/app.py:595-598 (mounted at `/auth`, not `/api/v1/auth`)
**Auth Router Config**: web/api/routes/auth.py:32 (prefix="/auth")

---

## Session Timeout Modal

**Additional Finding**: There's also a session timeout modal at `templates/components/session-timeout-modal.html`:
- Line 48: `onclick="SessionTimeout.logout()"`
- This also needs to be checked for correct endpoint

**Status**: Not yet investigated - recommend verifying SessionTimeout.logout() uses correct path after fixing handleLogout()

---

## Next Steps

1. Fix endpoint path (2 minutes)
2. Test logout button (3 minutes)
3. Check SessionTimeout.logout() for same issue (2 minutes)
4. Verify token blacklist works correctly

**Priority**: FIX NOW - blocks core functionality and security (token revocation)

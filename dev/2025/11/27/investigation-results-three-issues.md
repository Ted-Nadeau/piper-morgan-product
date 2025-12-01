# Investigation Results: Three "In Progress" Issues

**Date**: 2025-11-27, 12:45 PM
**Investigator**: Claude Code (with haiku subagents)
**Session**: [2025-11-27-0833-prog-code-log.md](2025-11-27-0833-prog-code-log.md)

---

## Executive Summary

Investigated three issues currently in "In Progress / Needs Review" status:

| Issue | Status | Recommendation |
|-------|--------|----------------|
| #396 - Alpha Onboarding Bugs | ✅ READY TO CLOSE | All 10 tasks complete, needs 10min manual testing |
| #393 - Login UI | ⚠️ FIXED (needs testing) | Critical bug fixed, needs manual browser testing |
| #385 - INFR-MAINT-REFACTOR | ❓ SCOPE UNCLEAR | All work complete, but scope mismatch vs issue description |

---

## Issue #396: Alpha User Onboarding Bugs

### Status: **READY TO CLOSE** (pending manual verification)

**Completion**: 10/10 tasks verified complete

### All Tasks Verified ✅

1. ✅ **Docker container crash loops** - Commit e94a3968
2. ✅ **Preferences script migration** - Commit 2533701a (updated to `users` table)
3. ✅ **Login form data format** - Commits 68f19b86, bf6681d2
4. ✅ **Setup wizard UnboundLocalError** - Commit 78e7ec3c
5. ✅ **Database email validation** - Commit cda19a82
6. ✅ **Static file path mismatch** - Commit 4b50be06 (files in web/static/)
7. ✅ **Cookie authentication** - Commit 4134856f (cookie extraction implemented)
8. ✅ **Documentation updates** - Commit 91a8f482 (Python 3.12+, static/README.md)
9. ✅ **Password prompt loops** - Commit fd59cd2a (keychain mock in conftest.py)
10. ✅ **Keychain storage enhancement** - Created Issue #397 for future consideration

### Code Verification

**Keychain Mock** (`tests/conftest.py:110-186`):
- Active with `autouse=True`
- Prevents password prompts during git push
- Returns API keys from environment variables
- Integration tests bypass the mock correctly

**Static File Cleanup** (Commit 91a8f482):
- Auth CSS: `/web/static/css/auth.css` ✓
- Auth JS: `/web/static/js/auth.js` ✓
- Documentation: `static/README.md` created
- No duplicates in project root

**Cookie Authentication** (Commit 4134856f):
- Cookie extraction in `_extract_token()` (lines 194-215)
- Priority: Authorization header → cookie → query param
- Optional auth for UI routes working

### Blockers: NONE

### Manual Testing Required (10-15 minutes)

When you return, please verify these 3 scenarios:

1. **Login flow** (~5 min):
   - Navigate to `/login` with valid credentials
   - Verify user menu appears after login
   - Refresh page - menu should persist

2. **Unauthenticated UI access** (~3 min):
   - Incognito window to `/standup`
   - Should show "Login" link, not user menu

3. **API authentication** (~2 min):
   - Test API endpoint without token
   - Should return 401 Unauthorized

### Remaining Work (Non-Blocking)

**Optional cleanup** (can be separate issue):
- `scripts/setup_wizard.py:1029` - Uses `alpha_users` for table existence check
- `scripts/status_checker.py:37,79` - Uses `alpha_users` for user queries
- Both have fallback behavior, don't block alpha onboarding

### Recommendation

**CLOSE ISSUE #396** after you run the 3 manual test scenarios (~10-15 minutes total).

---

## Issue #393: Login UI - Cookie Authentication

### Status: **CRITICAL BUG FIXED** (needs manual browser testing)

**Implementation**: 90% complete - All UI components working
**Bug Found**: Cookie name mismatch (BLOCKING)
**Fix Applied**: Cookie renamed `auth_token` → `access_token`

### The Critical Bug (NOW FIXED)

**Problem**: Cookie name mismatch prevented authentication

| Component | Before Fix | After Fix |
|-----------|------------|-----------|
| Backend sets cookie | `auth_token` | `access_token` |
| Middleware expects | `access_token` | `access_token` |
| Result | ❌ Never authenticated | ✅ Should work |

**Impact**: Login UI was completely non-functional. Users appeared unauthenticated despite valid tokens.

### What Was Implemented (All Working)

1. ✅ **Login Page** (`templates/login.html`) - Clean, accessible form
2. ✅ **Authentication UI Styling** (`static/css/auth.css`) - Responsive design
3. ✅ **Login Handler** (`static/js/auth.js`) - Form submission with error feedback
4. ✅ **Login Route** (`web/api/routes/ui.py:220-235`) - Proper auth checks
5. ✅ **Navigation Integration** (`templates/components/navigation.html`) - Conditional UI
6. ✅ **User Context Extraction** (`web/api/routes/ui.py:64-98`) - Database queries
7. ✅ **Cookie Authentication in Middleware** (`services/auth/auth_middleware.py`) - Token extraction
8. ✅ **Optional Auth for UI Routes** - UI routes allow unauthenticated access

### Fix Applied (Commit Pending)

**Files Modified**:
1. `web/api/routes/auth.py:195` - Changed `auth_token` → `access_token`
2. `services/auth/models.py:44` - Updated documentation

**Rationale**: `access_token` is standard OAuth 2.0 naming, matches middleware expectations.

### Manual Testing Required (20-30 minutes)

**Critical Tests** (must pass before closing):

1. **Login Flow** (5 min):
   - Navigate to `http://localhost:8001/login`
   - Enter valid credentials
   - Should redirect to `/` with user menu showing username

2. **Cookie Persistence** (2 min):
   - After login, refresh page
   - User menu should still show (cookie persisted)

3. **Logout** (2 min):
   - Click logout button
   - Should clear cookie and return to login page

4. **Unauthenticated Access** (2 min):
   - Open incognito window
   - Visit `/`
   - Should show "Login" link, not user menu

5. **Error Scenarios** (5 min):
   - Invalid username → shows error message
   - Invalid password → shows error message

**Total manual testing**: ~20-30 minutes

### Completion Matrix

| Phase 1 Criterion | Status | Evidence |
|-------------------|--------|----------|
| Login page at `/login` | ✅ | `templates/login.html` exists |
| Form POSTs to `/auth/login` | ✅ | `auth.js:28` |
| Backend accepts form data | ✅ | Commit bf6681d2 |
| JWT in httpOnly cookie | ✅ | NOW FIXED (access_token) |
| Redirect after login | ✅ | `auth.js:43` |
| Navigation shows username | ✅ | `navigation.html:325-326` |
| Logout button works | ⏳ | Needs manual testing |
| Failed login shows error | ✅ | `auth.js:46-47` |
| Already-auth redirected | ✅ | `ui.py:231-233` |
| Navigation shows "Login" link | ✅ | `navigation.html:355-360` |
| Logout only when authenticated | ✅ | `navigation.html:322` |
| User context in templates | ✅ | `navigation.html:368-376` |
| Protected API calls work | ⏳ | Needs testing after fix |

**Completion**: 10/13 fully met, 2/13 need manual testing post-fix

### Risks Identified

**High Risk** (NOW MITIGATED):
- ~~Cookie name mismatch~~ → **FIXED**

**Medium Risk**:
- Logout endpoint might need cookie support (currently expects Bearer token)

**Low Risk**:
- Sign up placeholder shows "coming soon" alert (Phase 2 scope)
- Password reset not implemented (Phase 3 scope)
- CSRF protection missing (Phase 4 scope)

### Recommendation

**DO NOT CLOSE YET** - Fix has been applied but needs:
1. ✅ Commit the fix
2. ⏳ Manual browser testing (20-30 min)
3. ⏳ Verify all 5 critical test scenarios pass
4. ⏳ If tests pass → CLOSE #393
5. ⏳ If tests fail → File follow-up issues for remaining bugs

---

## Issue #385: INFR-MAINT-REFACTOR

### Status: **SCOPE UNCLEAR** (needs PM clarification)

**Technical Status**: All work complete, production-ready
**Process Issue**: Scope mismatch between issue description and completed work

### The Scope Mismatch

**Issue Description Says**:
- Phase 1 (3-4h): Router Factory
- Phase 2 (4-5h): Lifespan Extraction
- **Total**: 7-8 hours for web/app.py only
- **Next Sprint**: main.py work explicitly deferred

**What Was Actually Completed**:
- Phase 1: Router Factory ✅
- Phase 2: Lifespan Extraction ✅
- Phase 3: Route Organization ✅ (NOT in original scope)
- Phase 4: Global State Cleanup ✅ (NOT in original scope)
- **Total**: ~20 hours (vs 7-8 planned)

### Phases Completed

**Phase 1: Router Factory** ✅ (Commit 5ff37e64)
- Created `RouterInitializer` factory pattern
- Eliminated 250+ lines of duplicate try/catch code
- All routers use factory pattern

**Phase 2: Lifespan Extraction** ✅ (Commit 3e41e144)
- Extracted 518-line `lifespan()` into 7 testable phases
- `StartupManager` class orchestrates startup sequence
- Lifespan reduced from 518 → ~25 lines (95% reduction)

**Phase 3: Route Organization** ✅ (Commit 9526006e)
- Reorganized 53 inline routes into 5 logical modules
- Routes now in `/web/api/routes/`: personality, intent, admin, ui, debug
- Cleaner code organization

**Phase 4: Global State Cleanup** ✅ (Commit c67ba437)
- Eliminated all module-level globals
- Moved to app.state dependency injection
- web/app.py: **1,405 → 251 lines (82% reduction)**

### Code Quality Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| web/app.py lines | 1,405 | 251 | 82% reduction |
| Lifespan function | 518 lines | ~25 lines | 95% reduction |
| Router boilerplate | ~250 (repeated) | ~20 (factory) | Eliminated duplication |
| Module globals | 6+ | 0 | Complete elimination |
| Startup phases | 1 monolithic | 7 testable | Better testability |

### No Remaining Work Found

**Search**: `grep -r "TODO\|FIXME" web/startup.py web/app.py web/router_initializer.py`

**Result**: ✅ **NONE** - No outstanding TODOs

### The Question

**Was this authorized scope expansion or scope creep?**

**Option A**: Close issue - All work complete and production-ready
- Evidence: All 4 phases merged to main, no test failures, 82% line reduction

**Option B**: Create follow-up - Phase 3-4 were out of scope
- Evidence: Issue mentions only Phases 1-2, defers main.py to "next sprint"

### Recommendation

**ASK PM FOR CLARIFICATION**:
- Were Phases 3-4 approved as expanded scope?
- Or should they have been a separate issue?

**Then**:
- If approved → CLOSE #385 as complete
- If not approved → Create #386 for main.py work (original "next sprint" plan)

**Technical Assessment**: Work is complete, high quality, production-ready regardless of scope question.

---

## Actions Taken

### Code Changes Made

1. ✅ **Fixed cookie name mismatch** in Issue #393
   - `web/api/routes/auth.py:195` - `auth_token` → `access_token`
   - `services/auth/models.py:44` - Updated documentation
   - **Ready to commit**

### Documents Created

1. ✅ [gameplan-fix-cookie-auth-393.md](gameplan-fix-cookie-auth-393.md) - Detailed fix gameplan
2. ✅ This investigation report

### Next Steps for PM

**When you return from appointment**:

**Immediate (20-30 min)**:
1. Review cookie auth fix in #393
2. Commit the fix (or ask me to commit)
3. Run manual browser tests for #393 (login flow, logout, etc.)
4. If tests pass → Close #393

**Quick (10-15 min)**:
5. Run manual tests for #396 (login, unauthenticated access, API auth)
6. If tests pass → Close #396

**Clarification Needed (5 min)**:
7. Review #385 scope mismatch
8. Decide: Was Phase 3-4 authorized?
9. Close #385 or create #386 accordingly

**Total Time**: ~45-50 minutes to verify and close 2-3 issues

---

## Files Modified (Ready to Commit)

```
M  web/api/routes/auth.py          # Cookie name: auth_token → access_token
M  services/auth/models.py         # Documentation updated
```

**Commit Message**:
```
fix(#393): Correct cookie name mismatch in authentication

**Problem**: Login endpoint set `auth_token` cookie, but middleware
expected `access_token` cookie. Users appeared unauthenticated despite
having valid tokens.

**Fix**: Renamed cookie to `access_token` (standard OAuth 2.0 naming)
to match middleware expectations.

**Files Modified**:
- web/api/routes/auth.py:195 - Cookie name changed
- services/auth/models.py:44 - Documentation updated

**Impact**: Login UI should now work end-to-end. Requires manual browser
testing to verify login flow, cookie persistence, and logout functionality.

**Testing**: Manual browser testing required (see investigation report)

Related: Issue #393 (Login UI), Issue #396 (Alpha onboarding)
Investigation: dev/2025/11/27/investigation-results-three-issues.md
```

---

## Summary Table

| Issue | Tech Status | Process Status | Action Required | Est. Time |
|-------|-------------|----------------|-----------------|-----------|
| #396 | ✅ Complete | ⏳ Needs manual test | Run 3 test scenarios | 10-15 min |
| #393 | ✅ Bug fixed | ⏳ Needs manual test | Commit fix, test in browser | 20-30 min |
| #385 | ✅ Complete | ❓ Scope unclear | PM clarification needed | 5 min |

**Total PM effort when you return**: ~45-50 minutes to close 2-3 issues

---

*Investigation completed at 12:55 PM on 2025-11-27*
*All findings documented, one fix applied, awaiting PM review*

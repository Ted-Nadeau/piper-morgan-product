# GitHub Issue: Missing Authentication UI

## Issue Number
#[TBD] - Authentication UI Missing (Login/Logout Flow)

## Title
**[UX-AUTH] No login UI - users cannot authenticate despite complete backend**

## Labels
- `priority: critical`
- `type: bug`
- `area: authentication`
- `area: ui`
- `severity: blocker`
- `status: alpha-blocker`
- `sprint: MVP`

## Description

### Problem Statement
Alpha users cannot log in to Piper Morgan despite having a fully functional JWT authentication backend. The authentication system is architecturally complete but missing all user-facing UI components, making the application effectively unusable for features requiring authentication.

### Impact
**Alpha Blocker**: This issue prevents users from:
- ❌ Logging in with their credentials
- ❌ Creating lists (requires auth)
- ❌ Creating todos (requires auth)
- ❌ Creating projects (requires auth)
- ❌ Uploading files (requires auth)
- ❌ Viewing their username in navigation
- ❌ Logging out (button exists but no session to end)

**Discovered During**: Alpha testing session on 2025-11-24
**Related Issues**:
- UI Issues CSV ([dev/active/UI-issues.csv](../active/UI-issues.csv)) - Issues #6, #7, #14
- Investigation report: [dev/2025/11/24/ui-issues-triage-report.md](ui-issues-triage-report.md)

### Current State

#### ✅ What EXISTS (Backend Complete)
- JWT authentication service with token generation/validation
- Token blacklist for secure logout
- Password hashing with bcrypt
- Auth middleware (`get_current_user`)
- Database: User table with full schema
- API endpoints:
  - `POST /auth/login` - Authenticates and issues JWT
  - `POST /auth/logout` - Revokes tokens
  - `GET /auth/me` - Returns user profile
  - `POST /auth/change-password` - Changes password

#### ❌ What's MISSING (UI Gaps)
- No login page template
- No `/login` route to serve UI
- No registration/signup page
- No user context injection into templates
- No "Login" link in navigation
- Logout button visible but non-functional
- No password reset flow
- No error messages when auth fails

### Root Cause
Classic 75% pattern - backend was built and works perfectly, but UI integration was never completed. Authentication system is production-ready architecturally (ADR-012) but inaccessible to users.

### Expected Behavior
1. User visits homepage
2. Sees "Login" link in navigation
3. Clicks login, sees login form
4. Enters credentials, submits
5. Backend validates, issues JWT token
6. User redirected to homepage
7. Navigation shows username and logout button
8. User can now access protected features
9. Click logout, session ends, redirect to login

### Actual Behavior
1. User visits homepage
2. No login option visible
3. User menu shows hardcoded "User"
4. Logout button visible but does nothing
5. All "Create" buttons fail with 401 errors
6. No way to authenticate

## Acceptance Criteria

### Phase 1: MVP Login Flow (P0 - Alpha Blocker)
- [ ] Login page created at `/login` with username/password form
- [ ] Login form POSTs to `/auth/login` backend endpoint
- [ ] Successful login:
  - [ ] Sets JWT token in httpOnly cookie
  - [ ] Redirects to homepage
  - [ ] Navigation shows actual username
  - [ ] Logout button works
- [ ] Failed login shows error message to user
- [ ] Already-authenticated users redirected from `/login` to `/`
- [ ] Navigation shows "Login" link when not authenticated
- [ ] Navigation shows "Logout" button only when authenticated
- [ ] User context (`window.currentUser`) properly set in all templates
- [ ] Protected API calls (Lists, Todos, Projects) now work

### Phase 2: Registration Flow (P1 - MVP)
- [ ] Registration page created at `/register`
- [ ] Backend route `POST /auth/register` implemented
- [ ] Username uniqueness validation
- [ ] Email format validation
- [ ] Password complexity validation
- [ ] Successful registration logs user in automatically
- [ ] Navigation includes "Sign Up" link

### Phase 3: Password Management (P2 - Post-MVP)
- [ ] "Forgot Password" link on login page
- [ ] Email-based password reset flow
- [ ] Temporary reset token generation
- [ ] Password change UI in `/account` settings

### Phase 4: Security & Polish (P2 - Post-MVP)
- [ ] CSRF protection on login/register forms
- [ ] Rate limiting on login attempts
- [ ] Account lockout after failed attempts
- [ ] Session timeout warnings
- [ ] "Remember me" checkbox
- [ ] Password strength indicator
- [ ] "Show password" toggle

## Technical Approach

### Files to Create
1. `templates/login.html` - Login page template
2. `templates/register.html` - Registration page (Phase 2)
3. `static/css/auth.css` - Authentication page styling
4. `static/js/auth.js` - Login form handling

### Files to Modify
1. `web/api/routes/ui.py` - Add `/login` and `/register` routes
2. `templates/components/navigation.html` - Add login link, conditional logout
3. `web/api/routes/auth.py` - Add `/auth/register` endpoint (Phase 2)
4. `templates/*.html` - Ensure user context properly passed

### Integration Points
- JWT tokens stored in httpOnly cookies (already works)
- Auth middleware validates tokens on protected routes (already works)
- User context must be injected into Jinja2 template context
- Navigation component reads `window.currentUser` from template variable

## Complexity Estimate

### Phase 1 (MVP - P0): **4 hours**
- Login page template: 1 hour
- Route integration: 30 mins
- Navigation updates: 30 mins
- User context injection: 1 hour
- End-to-end testing: 1 hour

### Phase 2 (Registration - P1): **5 hours**
- Registration template: 1 hour
- Backend route: 2 hours
- Validation: 1 hour
- Testing: 1 hour

### Phase 3 (Password Reset - P2): **6 hours**
- Email integration: 2 hours
- Reset flow: 2 hours
- UI pages: 1 hour
- Testing: 1 hour

### Phase 4 (Security - P2): **6 hours**
- Security features: 3 hours
- UX polish: 2 hours
- Testing: 1 hour

**Total: 21 hours for complete system**

## Dependencies
- None (backend complete)
- Optional: Email service for password reset (Phase 3)

## Architecture References
- **ADR-012**: Protocol-Ready JWT Authentication (ACCEPTED)
  - Backend fully implements this ADR
  - UI integration pending

## Testing Strategy

### Manual Testing (Phase 1)
1. Visit `/login` - see login form
2. Enter invalid credentials - see error
3. Enter valid credentials - redirect to home
4. Check navigation shows username
5. Click logout - return to login
6. Try creating list/todo - should work now

### Automated Testing (Future)
- E2E tests for login flow
- E2E tests for logout flow
- Integration tests for protected routes
- Unit tests for form validation

## Related Work
- **Triage Report**: [dev/2025/11/24/ui-issues-triage-report.md](ui-issues-triage-report.md)
- **Investigation**: [dev/2025/11/24/auth-investigation-report.md](auth-investigation-report.md)
- **Setup Scripts**:
  - `scripts/setup_alpha_passwords.py` - Sets alpha user passwords
  - `scripts/setup_wizard.py` - CLI user creation

## Risk Assessment
**LOW** - Backend is production-ready and tested. This is purely UI work with clear integration points.

## Notes
- Backend authentication is **production-quality** per ADR-012
- Security best practices already implemented (httpOnly cookies, bcrypt, token blacklist)
- Architecture supports future OAuth/federation
- Missing error messaging is a separate issue to track

---

**Created**: 2025-11-24 11:05 AM
**By**: Claude Code (Programmer)
**Session**: 2025-11-24-0516-prog-code-log.md

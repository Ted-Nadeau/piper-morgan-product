# Gameplan: Authentication UI - Phase 1 (MVP Login Flow)

**Issue**: #[TBD] - Authentication UI Missing
**Phase**: Phase 1 - MVP Login Flow (P0 Alpha Blocker)
**Estimated Time**: 4 hours
**Complexity**: Medium
**Agent Assignment**: Code Agent (Programmer)

---

## Context & Problem Statement

### What We're Solving
Alpha users cannot log in to Piper Morgan despite having a complete JWT authentication backend. All authentication infrastructure exists and works perfectly, but there's no UI to access it. This blocks all authenticated features (Lists, Todos, Projects, Files).

### Why This Happened
Classic 75% pattern - backend was built completely but UI integration was never finished. The authentication system is production-ready (ADR-012) but inaccessible to users.

### Success Criteria
After this phase, users can:
1. Navigate to `/login` and see a login form
2. Enter credentials and authenticate
3. See their username in the navigation
4. Successfully create lists, todos, and other authenticated resources
5. Log out and return to login page

---

## Infrastructure Verification

### ✅ What EXISTS (No Work Needed)
- `POST /auth/login` endpoint - validates credentials, issues JWT
- `POST /auth/logout` endpoint - revokes tokens via blacklist
- `GET /auth/me` endpoint - returns user profile
- JWT service with token generation/validation
- Auth middleware (`get_current_user`) - protects routes
- User database table with all fields
- Token blacklist for secure logout
- Password hashing with bcrypt
- Navigation component with logout button
- User context variables in navigation JavaScript

### ❌ What's MISSING (Our Work)
- Login page template (`templates/login.html`)
- Login route to serve the page (`/login` in ui.py)
- Auth CSS styling (`static/css/auth.css`)
- Auth JavaScript (`static/js/auth.js`)
- User context injection in templates
- Login link in navigation (when not authenticated)
- Conditional logout button (only when authenticated)

---

## Phase 1 Implementation Plan

### Step 1: Create Login Page Template (60 min)

**Create**: `templates/login.html`

**Requirements**:
- Clean, professional login form
- Username and password fields
- Submit button
- Error message display area
- Link to registration (future - show "Coming Soon")
- Consistent with existing Piper Morgan UI style
- Responsive design
- Accessibility (ARIA labels, keyboard navigation)

**Design Pattern**: Follow personality-preferences.html for styling consistency

**Implementation Details**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login - Piper Morgan</title>
    <link rel="icon" type="image/x-icon" href="/assets/favicon.ico" />
    <link rel="stylesheet" href="/static/css/auth.css" />
    <style>
        /* Inline critical CSS for faster load */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="auth-header">
            <div class="auth-logo">PM</div>
            <h1>Welcome Back</h1>
            <p>Log in to continue to Piper Morgan</p>
        </div>

        <form id="login-form" class="auth-form">
            <div class="form-group">
                <label for="username">Username</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    required
                    autocomplete="username"
                    autofocus
                    placeholder="Enter your username"
                />
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    required
                    autocomplete="current-password"
                    placeholder="Enter your password"
                />
            </div>

            <div id="error-message" class="error-message" style="display: none;"></div>

            <button type="submit" class="auth-button" id="login-button">
                Log In
            </button>
        </form>

        <div class="auth-footer">
            <p>
                Don't have an account?
                <a href="#" onclick="alert('Registration coming soon!'); return false;">Sign up</a>
            </p>
        </div>
    </div>

    <script src="/static/js/auth.js"></script>
</body>
</html>
```

**Validation**:
- Form has required fields
- Error message area exists
- Styling is consistent with app
- Accessibility: labels, autocomplete, focus management

---

### Step 2: Create Auth CSS (30 min)

**Create**: `static/css/auth.css`

**Requirements**:
- Match Piper Morgan design system
- Responsive layout (mobile, tablet, desktop)
- Clean, professional appearance
- Accessible (sufficient contrast, focus states)
- Loading states for submit button
- Error message styling

**Design Tokens** (from existing pages):
- Primary color: `#3498db`
- Text color: `#2c3e50`
- Background: `#f5f5f5`
- Card background: `white`
- Border color: `#ecf0f1`
- Error color: `#e74c3c`
- Success color: `#27ae60`

**Implementation**:
```css
.auth-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 48px;
    width: 100%;
    max-width: 420px;
}

.auth-header {
    text-align: center;
    margin-bottom: 32px;
}

.auth-logo {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #3498db, #2980b9);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 32px;
    font-weight: 700;
    margin: 0 auto 16px;
}

.auth-header h1 {
    font-size: 28px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0 0 8px 0;
}

.auth-header p {
    font-size: 15px;
    color: #7f8c8d;
    margin: 0;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    font-size: 14px;
    font-weight: 500;
    color: #2c3e50;
    margin-bottom: 8px;
}

.form-group input {
    width: 100%;
    padding: 12px 16px;
    font-size: 15px;
    border: 1px solid #ecf0f1;
    border-radius: 8px;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-sizing: border-box;
}

.form-group input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.error-message {
    background: #fee;
    border: 1px solid #e74c3c;
    border-radius: 8px;
    padding: 12px 16px;
    color: #c0392b;
    font-size: 14px;
    margin-bottom: 20px;
}

.auth-button {
    width: 100%;
    padding: 12px 16px;
    font-size: 16px;
    font-weight: 600;
    color: white;
    background: #3498db;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
}

.auth-button:hover {
    background: #2980b9;
}

.auth-button:active {
    transform: scale(0.98);
}

.auth-button:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
}

.auth-button.loading::after {
    content: '...';
    animation: loading 1s infinite;
}

@keyframes loading {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}

.auth-footer {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #ecf0f1;
}

.auth-footer p {
    font-size: 14px;
    color: #7f8c8d;
    margin: 0;
}

.auth-footer a {
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
}

.auth-footer a:hover {
    text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
    .auth-container {
        padding: 32px 24px;
        margin: 16px;
    }
}
```

---

### Step 3: Create Auth JavaScript (30 min)

**Create**: `static/js/auth.js`

**Requirements**:
- Handle login form submission
- POST to `/auth/login` endpoint
- Show loading state during request
- Display errors from backend
- Redirect on success
- Handle network failures gracefully

**Implementation**:
```javascript
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const loginButton = document.getElementById('login-button');
    const errorMessage = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Get form data
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            // Validate
            if (!username || !password) {
                showError('Please enter both username and password');
                return;
            }

            // Show loading state
            loginButton.disabled = true;
            loginButton.classList.add('loading');
            loginButton.textContent = 'Logging in';
            hideError();

            try {
                // POST to login endpoint
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        username: username,
                        password: password
                    }),
                    credentials: 'include' // Include cookies
                });

                if (response.ok) {
                    // Success - redirect to home
                    const data = await response.json();
                    window.location.href = '/';
                } else {
                    // Login failed
                    const error = await response.json();
                    showError(error.detail || 'Invalid username or password');
                }
            } catch (error) {
                console.error('Login error:', error);
                showError('Network error. Please check your connection and try again.');
            } finally {
                // Reset button state
                loginButton.disabled = false;
                loginButton.classList.remove('loading');
                loginButton.textContent = 'Log In';
            }
        });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }
});
```

---

### Step 4: Add Login Route (15 min)

**Modify**: `web/api/routes/ui.py`

**Add route at line ~80 (after existing routes)**:
```python
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Serve login page

    If user is already authenticated, redirect to homepage.
    Otherwise, show login form.
    """
    templates = _get_templates(request)
    user_context = _extract_user_context(request)

    # If already logged in, redirect to home
    if user_context.get("user"):
        return RedirectResponse(url="/", status_code=302)

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            **user_context
        }
    )
```

**Import required**:
```python
from fastapi.responses import RedirectResponse
```

**Validation**:
- Route returns login template
- Already-authenticated users redirected
- User context properly passed

---

### Step 5: Update Navigation (30 min)

**Modify**: `templates/components/navigation.html`

**Changes Required**:
1. Add "Login" link (visible when NOT authenticated)
2. Make logout button conditional (visible only when authenticated)
3. Update user context reading logic

**Implementation** (around line 318):
```html
<!-- Main Navigation -->
<ul class="nav-menu" id="nav-menu">
  <li><a href="/" class="nav-link" id="nav-home">Home</a></li>
  <li><a href="/standup" class="nav-link" id="nav-standup">Standup</a></li>
  <li><a href="/lists" class="nav-link" id="nav-lists">Lists</a></li>
  <li><a href="/todos" class="nav-link" id="nav-todos">Todos</a></li>
  <li><a href="/projects" class="nav-link" id="nav-projects">Projects</a></li>
  <li><a href="/files" class="nav-link" id="nav-files">Files</a></li>
  <li><a href="/learning" class="nav-link" id="nav-learning">Learning</a></li>
  <li><a href="/settings" class="nav-link" id="nav-settings">Settings</a></li>
</ul>

<!-- User Menu (if authenticated) or Login link (if not) -->
<div class="nav-user">
  {% if user %}
  <!-- Authenticated: Show user menu with logout -->
  <button class="user-button" aria-haspopup="true" aria-expanded="false" id="user-menu-button">
    <span class="user-avatar" id="user-avatar">{{ user.username[0]|upper }}</span>
    <span class="user-name" id="user-name">{{ user.username }}</span>
    <svg class="user-chevron" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M4 6l4 4 4-4"/>
    </svg>
  </button>

  <div class="user-dropdown" hidden id="user-dropdown">
    <a href="/settings" class="dropdown-item" id="dropdown-settings">
      <svg viewBox="0 0 16 16" fill="currentColor">
        <path d="M9.405 1.05c-.413-1.238-2.397-1.238-2.81 0l-.1.34a1.464 1.464 0 01-2.105.872l-.31-.17c-1.088-.601-2.187.529-1.586 1.617l.17.31c.463.836.023 1.917-.856 2.105l-.34.1c-1.238.413-1.238 2.397 0 2.81l.34.1c.883.188 1.319 1.269.856 2.105l-.17.31c-.601 1.088.529 2.187 1.617 1.586l.31-.17a1.464 1.464 0 012.105.872l.1.34c.413 1.238 2.397 1.238 2.81 0l.1-.34a1.464 1.464 0 012.105-.872l.31.17c1.088.601 2.187-.529 1.586-1.617l-.17-.31c-.463-.836-.023-1.917.856-2.105l.34-.1c1.238-.413 1.238-2.397 0-2.81l-.34-.1c-.883-.188-1.319-1.269-.856-2.105l.17-.31c.601-1.088-.529-2.187-1.617-1.586l-.31.17a1.464 1.464 0 01-2.105-.872l-.1-.34z"/>
      </svg>
      Settings
    </a>
    <a href="/account" class="dropdown-item" id="dropdown-account">
      <svg viewBox="0 0 16 16" fill="currentColor">
        <path d="M8 8a3 3 0 100-6 3 3 0 000 6zm.5-9H8c4.418 0 8 1.79 8 4v2c0 2.21-3.582 4-8 4s-8-1.79-8-4V3c0-2.21 3.582-4 8-4z"/>
      </svg>
      Account
    </a>
    <hr class="dropdown-divider">
    <a href="#" class="dropdown-item dropdown-item-danger" id="dropdown-logout" onclick="handleLogout(event)">
      <svg viewBox="0 0 16 16" fill="currentColor">
        <path d="M5.338 1.59a61.44 61.44 0 00-2.837.856.481.481 0 00-.328.39c-.554 4.157.726 7.213 2.363 9.337a3.494 3.494 0 00.636.643l.049-.04a.658.658 0 00.015-.691A2.89 2.89 0 005.1 9.5c0-.822.503-4.76 1.102-6.402a.413.413 0 00-.078-.465 3.2 3.2 0 00-.6-.756zm2.768.885a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm4.048 .895a.75.75 0 11-1.5 0 .75.75 0 011.5 0z"/>
      </svg>
      Logout
    </a>
  </div>
  {% else %}
  <!-- Not authenticated: Show login link -->
  <a href="/login" class="user-button" style="text-decoration: none;">
    <svg viewBox="0 0 16 16" fill="currentColor" style="width: 20px; height: 20px;">
      <path d="M8 8a3 3 0 100-6 3 3 0 000 6zm.5-9H8c4.418 0 8 1.79 8 4v2c0 2.21-3.582 4-8 4s-8-1.79-8-4V3c0-2.21 3.582-4 8-4z"/>
    </svg>
    <span class="user-name">Log In</span>
  </a>
  {% endif %}
</div>
```

**Update JavaScript** (around line 466):
```javascript
// Set user context from server (now comes from Jinja2 template)
{% if user %}
window.currentUser = {
    username: "{{ user.username }}",
    user_id: "{{ user.user_id }}",
    is_admin: {{ 'true' if user.is_admin else 'false' }}
};
{% else %}
window.currentUser = null;
{% endif %}
```

**Validation**:
- Login link visible when `user` is null
- User menu visible when `user` exists
- Avatar shows first letter of username
- Logout button only shows when authenticated

---

### Step 6: User Context Injection (60 min)

**Problem**: Templates expect `{% if user %}` but user is never set

**Solution**: Extract user from request state and inject into all template contexts

**Modify**: `web/api/routes/ui.py`

**Update `_extract_user_context` function** (around line 50):
```python
def _extract_user_context(request: Request) -> dict:
    """
    Extract user context from request state for template rendering.

    After successful authentication, the auth middleware sets request.state.user_id.
    This function converts that into template-friendly user context.

    Returns:
        dict: {"user": {...}} if authenticated, {"user": None} if not
    """
    user_context = {"user": None}

    # Check if user_id is in request state (set by auth middleware)
    if hasattr(request.state, "user_id") and request.state.user_id:
        try:
            # Get user from database
            from services.database.models import UserDB
            from services.database import get_db_session

            session = next(get_db_session())
            user_db = session.query(UserDB).filter(UserDB.user_id == request.state.user_id).first()

            if user_db:
                user_context["user"] = {
                    "user_id": str(user_db.user_id),
                    "username": user_db.username,
                    "email": user_db.email,
                    "is_admin": user_db.is_admin,
                    "is_alpha": user_db.is_alpha
                }
        except Exception as e:
            logger.error("Failed to extract user context", error=str(e))

    return user_context
```

**Validation**:
- Authenticated requests have `request.state.user_id` set
- User context properly extracted from database
- Template receives complete user object
- Unauthenticated requests get `{"user": None}`

---

### Step 7: Test End-to-End Flow (60 min)

**Manual Testing Checklist**:

1. **Test Unauthenticated State**:
   - [ ] Visit homepage - see "Login" link in navigation
   - [ ] Click "Login" - navigate to `/login`
   - [ ] Login form displays correctly
   - [ ] No user menu visible (only login link)

2. **Test Login Flow**:
   - [ ] Enter invalid credentials - see error message
   - [ ] Error message is clear and helpful
   - [ ] Enter valid credentials (use setup script if needed)
   - [ ] Submit form - button shows "Logging in..." loading state
   - [ ] Successful login redirects to homepage
   - [ ] Navigation now shows username and avatar
   - [ ] Logout button is visible

3. **Test Authenticated State**:
   - [ ] Create a new list - button works (no 401 error)
   - [ ] Create a new todo - button works
   - [ ] User menu dropdown works
   - [ ] Settings link works
   - [ ] Account link works

4. **Test Logout Flow**:
   - [ ] Click logout button
   - [ ] Confirm redirect to `/login` (or homepage)
   - [ ] Navigation shows "Login" link again
   - [ ] No user menu visible
   - [ ] Cannot access protected routes (get redirected/error)

5. **Test Edge Cases**:
   - [ ] Visit `/login` while already logged in - redirect to homepage
   - [ ] Clear cookies, try to create list - get proper error
   - [ ] Network error during login - see helpful error message
   - [ ] XSS attempt in username field - properly escaped

**Setup Test User** (if needed):
```bash
# Use existing setup script
python scripts/setup_alpha_passwords.py
# Creates alpha users with passwords from config
```

**Browser Console Checks**:
- No JavaScript errors
- `window.currentUser` is set correctly when logged in
- `window.currentUser` is null when logged out
- Fetch requests include credentials

---

## Completion Matrix

### Code Complete
- [ ] `templates/login.html` created with all required fields
- [ ] `static/css/auth.css` created with responsive design
- [ ] `static/js/auth.js` created with error handling
- [ ] `/login` route added to `ui.py`
- [ ] `_extract_user_context()` implemented correctly
- [ ] Navigation updated with conditional login/logout
- [ ] User context properly passed to all templates

### Functionality Complete
- [ ] Users can navigate to `/login`
- [ ] Login form submits to `/auth/login`
- [ ] Successful login redirects to homepage
- [ ] Failed login shows error message
- [ ] Already-authenticated users redirected from `/login`
- [ ] Navigation shows username when authenticated
- [ ] Navigation shows "Login" when not authenticated
- [ ] Logout button works correctly
- [ ] Protected routes (Lists/Todos) now accessible

### Quality Complete
- [ ] All manual tests pass
- [ ] No console errors
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Accessibility: keyboard navigation works
- [ ] Accessibility: screen readers supported
- [ ] Error messages are user-friendly
- [ ] Loading states provide feedback
- [ ] Code follows existing patterns

### Documentation Complete
- [ ] Code comments explain non-obvious logic
- [ ] User context injection documented
- [ ] Auth flow documented in ADR (if needed)
- [ ] Testing steps documented

---

## Risk Mitigation

### Risk 1: Auth Middleware Not Setting request.state.user_id
**Mitigation**: Test with authenticated request first, verify middleware behavior
**Fallback**: Manually set user_id in request state for testing

### Risk 2: Cookie Not Being Set
**Mitigation**: Verify `/auth/login` returns Set-Cookie header
**Fallback**: Check cookie settings (httpOnly, SameSite, Secure)

### Risk 3: CORS Issues
**Mitigation**: Ensure credentials: 'include' in fetch calls
**Fallback**: Check CORS configuration in web/app.py

### Risk 4: User Context Not Propagating
**Mitigation**: Add logging in `_extract_user_context()`
**Fallback**: Check if user is in database

---

## Definition of Done

Phase 1 is complete when:
1. ✅ All code changes committed to feature branch
2. ✅ All manual tests pass
3. ✅ No regressions (existing features still work)
4. ✅ Login/logout flow works end-to-end
5. ✅ Protected routes (Lists/Todos) now functional
6. ✅ Alpha users can authenticate successfully
7. ✅ Issue #[TBD] updated with "Phase 1 Complete" comment
8. ✅ Ready for PM review and v0.8.1.1 release

---

**Created**: 2025-11-24 11:10 AM
**By**: Claude Code (Programmer)
**For**: Code Agent execution
**Estimated Time**: 4 hours
**Priority**: P0 (Alpha Blocker)

# Gameplan: Bug #605 - Setup Wizard [Continue] Button Non-Functional

**Issue**: #605 BUG-FTUX: Setup wizard final step [Continue] button does nothing
**Priority**: P0 (blocking new user onboarding)
**Type**: Regression
**Created**: 2026-01-17

---

## Five Whys Analysis

### Problem Statement
When clicking the [Continue] button on the final step of the setup wizard, nothing happens. Account is not created or authentication fails.

### Analysis of Recent Changes

**Potentially culpable commits (since last known-good state):**

| Commit | Date | Description | Risk Area |
|--------|------|-------------|-----------|
| `d3554765` | 2026-01-09 | FTUX-PORTFOLIO onboarding | conversation_handler.py +200 lines |
| `db28e885` | 2026-01-09 | Standup Assistant epic | Intent routing changes |
| `1535fa8b` | 2026-01-17 | Temporal/calendar fixes | None (different flow) |
| `39fe6703` | 2026-01-17 | Auto-title conversations | repository changes |

### Five Whys Deep Dive

**Why #1: Why does nothing happen when clicking [Continue]?**

Looking at `templates/setup.html`:
- Step 1: `#next-1` button → `showStep(2)` ✓
- Step 2: `#next-2` button → `showStep(3)` ✓
- Step 3: Form submit → `create-user` API → `completeSetup()` → `showStep(4)`
- Step 4: Static `<a href="/login">` link (NOT a button)

**Clarification needed**: User said "final step [Continue] button" but:
- Step 4 has "Log In" link, not Continue button
- Step 3 has "Create Account" button that triggers account creation + setup completion

**Hypothesis 1**: The bug is actually on Step 3 - "Create Account" button doesn't work.

**Why #2: Why might "Create Account" fail silently?**

Looking at `web/static/js/setup.js` lines 265-317:

```javascript
document.getElementById('account-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    // ... validation ...
    try {
        const response = await fetch('/setup/create-user', {...});
        const data = await response.json();
        if (data.success) {
            userId = data.user_id;
            await completeSetup();  // ← This is the critical path
        } else {
            showError(data.message || 'Failed to create account.');
        }
    } catch (err) {
        // Error handling
    }
});
```

Potential failure points:
1. Form validation fails silently (`FormValidation.validateForm` returns false)
2. `/setup/create-user` returns error but JS doesn't handle it properly
3. `completeSetup()` fails but doesn't show error
4. JavaScript error before event listener runs

**Why #3: Why might completeSetup() fail silently?**

Looking at `completeSetup()` function (lines 319-347):

```javascript
async function completeSetup() {
    try {
        const response = await fetch('/setup/complete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                openai_key: keychainKeys.openai ? null : apiKeys.openai,
                // ... other keys
            })
        });
        const data = await response.json();
        if (data.success) {
            showStep(4);  // ← Success path
        } else {
            showError(data.message || 'Unable to complete setup.');
        }
    } catch (err) {
        // Error toast shown
    }
}
```

The function has proper error handling, so if the backend fails, it should show a toast.

**Why #4: Why might the backend `/setup/complete` fail?**

Looking at `web/api/routes/setup.py` lines 667-778:

The `complete_setup()` endpoint:
1. Stores API keys (with try/except, non-blocking)
2. Updates `users.setup_complete = true`
3. Generates CLI token (non-blocking)
4. Returns `SetupCompleteResponse` with `redirect_url="/login"`

Potential issues:
- `req.user_id` might be None if `create-user` didn't return a valid ID
- Database session issues (uses `session_scope_fresh()`)
- SQL injection of user_id if not validated as UUID

**Why #5: Why might `create-user` not return a valid user_id?**

Looking at `/setup/create-user` endpoint (lines 601-664):

The response model is:
```python
class CreateUserResponse(BaseModel):
    success: bool
    user_id: Optional[str] = None
    message: str
```

On success:
```python
return CreateUserResponse(
    success=True,
    user_id=str(user.id),
    message=f"Account created: {user.username}",
)
```

But if there's an exception, it either:
- Returns 400 for duplicate username
- Returns 500 for other errors

**Neither returns success=True with no user_id** - this path looks clean.

### Hypothesis Summary

Based on Five Whys analysis, most likely causes (in order of probability):

1. **JavaScript execution error** - Some JS error prevents the form submit handler from running
2. **Form validation blocking silently** - `FormValidation.validateForm()` returns false but no visual feedback
3. **Event listener not attached** - If `setup.js` fails to load or has parse error
4. **Backend returns error but JS handling broken** - Response parsing issue

### What to Verify First

1. Check browser console for JavaScript errors
2. Check Network tab for `/setup/create-user` request
3. If request fires: check response status and body
4. If request doesn't fire: check form validation state

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

Based on code review:

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Frontend: Jinja2 templates + vanilla JS
- [x] Database: PostgreSQL on 5433
- [x] Testing: pytest

**My understanding of the bug**:
- User cannot complete setup wizard
- "Final step [Continue] button" likely refers to Step 3's "Create Account" or Step 4's "Log In"
- This is a regression (worked before)
- Could be JS error, form validation, or backend issue

### Part B: PM Verification Required

**PM, please provide:**

1. **Exact step where failure occurs**:
   - [ ] Step 3: "Create Account" button
   - [ ] Step 4: "Log In" link
   - [ ] Other: ____________

2. **Browser console errors?**
   - Any red errors in console when clicking?

3. **Network activity?**
   - Does `/setup/create-user` request appear in Network tab?
   - If yes, what status code?

4. **Form state when clicking?**
   - Are all fields filled in?
   - Any red validation errors visible?

5. **Environment details**:
   - Browser and version: ____________
   - Server running locally or deployed?

---

## Phase 0: Initial Investigation

### 0.1 Reproduce the Bug

```bash
# Start fresh with a clean database (to ensure no existing user)
docker-compose down -v
docker-compose up -d
alembic upgrade head

# Start the server
python main.py

# Navigate to /setup and attempt full flow
```

### 0.2 Check for JavaScript Errors

```bash
# Check if setup.js loads correctly
curl -s http://localhost:8001/static/js/setup.js | head -50

# Check for obvious syntax errors
# (Visual inspection in browser DevTools)
```

### 0.3 Check Form Validation Library

The setup wizard uses `FormValidation` from `/static/js/form-validation.js`. If this script fails to load or has errors, validation might silently block submission.

```bash
# Verify form-validation.js exists and loads
curl -s http://localhost:8001/static/js/form-validation.js | head -30
```

### 0.4 Check Recent Changes to Shared JS

```bash
# Check if any recent commits touched shared JS files
git log --oneline --since="2026-01-08" -- web/static/js/
```

---

## Phase 1: Root Cause Investigation

### 1.1 Scenarios to Test

| Scenario | Test Method | Expected Result |
|----------|-------------|-----------------|
| Fresh user signup | New username | Account created, redirect to login |
| Duplicate username | Existing username | Error message shown |
| Invalid password | <8 chars | Validation error shown |
| Missing email | Empty email | Validation error shown |
| Server down | Stop server | Network error toast shown |

### 1.2 Backend Endpoint Testing

```bash
# Test create-user endpoint directly
curl -X POST http://localhost:8001/setup/create-user \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"password123","password_confirm":"password123"}'

# Expected: {"success":true,"user_id":"<uuid>","message":"Account created: testuser"}
```

```bash
# Test complete endpoint
curl -X POST http://localhost:8001/setup/complete \
  -H "Content-Type: application/json" \
  -d '{"user_id":"<uuid-from-above>","openai_key":"sk-test"}'

# Expected: {"success":true,"message":"Setup complete!...","redirect_url":"/login"}
```

### 1.3 JavaScript Debugging

Add console.log statements temporarily to trace execution:

```javascript
// In setup.js, add at start of form submit handler:
console.log('Form submit handler triggered');

// Before fetch:
console.log('About to call /setup/create-user');

// After fetch response:
console.log('create-user response:', data);
```

---

## Phase 2: Fix Implementation

*To be determined after Phase 0 and Phase 1 investigation*

Possible fixes based on likely causes:

### If FormValidation.validateForm fails silently
- Add visual feedback when validation fails
- Check if `validateForm` is defined before calling

### If JavaScript error
- Fix the specific error identified in browser console

### If backend error
- Fix the specific endpoint error
- Ensure proper error response propagation

---

## Phase Z: Verification

### Acceptance Criteria

- [ ] User can complete setup wizard from start to finish
- [ ] Account is created in database
- [ ] User can log in with created credentials
- [ ] No JavaScript console errors during flow
- [ ] Error cases show appropriate messages
- [ ] All existing tests still pass

### Test Commands

```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Run integration tests for setup
python -m pytest tests/ -k "setup" -v

# Manual E2E test
# 1. Navigate to /setup
# 2. Complete all steps
# 3. Verify login works
```

---

## Audit Against Gameplan Template v9.3

| Section | Present | Notes |
|---------|---------|-------|
| Phase -1: Infrastructure | ✓ | Awaiting PM environment details |
| Phase 0: Initial Bookending | ✓ | Investigation steps defined |
| Phase 0.5: Frontend-Backend Contract | N/A | Bug fix, not new feature |
| Phase 0.6: Data Flow | N/A | Single-request issue |
| Phase 0.7: Conversation Design | N/A | Not conversational |
| Phase 0.8: Post-Completion | ✓ | Verification criteria defined |
| Five Whys Analysis | ✓ | Complete with 5 levels |
| Evidence Requirements | ✓ | Test commands defined |
| STOP Conditions | ✓ | Implicit in investigation |

### Template Compliance

- ✓ Multi-agent deployment: Not needed (single bug fix)
- ✓ Worktree assessment: Not needed (estimated <30 min)
- ✓ Acceptance criteria with checkboxes
- ✓ Evidence format specified
- ✓ STOP conditions understood

---

## Summary

This gameplan provides a structured approach to debug the setup wizard regression. The Five Whys analysis points to JavaScript execution issues as the most likely cause, with form validation and backend errors as secondary suspects.

**Recommended investigation order**:
1. Check browser console for JS errors
2. Check Network tab for request/response
3. Test backend endpoints directly
4. Add console.log tracing if needed

**Blocking questions for PM**:
1. Exact step where failure occurs
2. Any console errors visible
3. Network request behavior

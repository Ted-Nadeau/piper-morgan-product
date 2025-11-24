# Agent Prompt: Authentication UI Implementation (Phase 1)

**Agent Type**: Code Agent (Programmer)
**Model**: Sonnet
**Estimated Time**: 4 hours
**Session Branch**: `feat/auth-ui-login-#[ISSUE_NUM]`

---

## Your Mission

Implement the user-facing login UI for Piper Morgan's authentication system. The backend is **100% complete** - your job is purely UI integration. After your work, alpha users will be able to log in, see their username, and access protected features.

---

## Critical Context

### What EXISTS (Don't Build This)
- ✅ `/auth/login` endpoint - POST credentials, get JWT token
- ✅ `/auth/logout` endpoint - Revoke token via blacklist
- ✅ `/auth/me` endpoint - Get user profile
- ✅ JWT service, auth middleware, token blacklist
- ✅ User database table
- ✅ Password hashing (bcrypt)
- ✅ Navigation component (waiting for user context)

### What You're Building
- ❌ Login page template (`templates/login.html`)
- ❌ Auth CSS (`static/css/auth.css`)
- ❌ Auth JavaScript (`static/js/auth.js`)
- ❌ `/login` route in `ui.py`
- ❌ User context injection
- ❌ Navigation login/logout links

---

## Gameplan Reference

**Full details**: `dev/2025/11/24/gameplan-auth-ui-phase1.md`

Read the gameplan completely before starting. It contains:
- Complete code snippets for all files
- Step-by-step implementation order
- Validation criteria for each step
- Testing checklist
- Completion matrix

---

## Implementation Order (MANDATORY)

Follow this exact order:

1. **Create Login Page** (`templates/login.html`) - 60 min
   - Use code from gameplan Step 1
   - Form with username/password fields
   - Error message display area
   - Link to registration (show "Coming Soon")

2. **Create Auth CSS** (`static/css/auth.css`) - 30 min
   - Use code from gameplan Step 2
   - Match Piper Morgan design system
   - Responsive layout
   - Loading states

3. **Create Auth JavaScript** (`static/js/auth.js`) - 30 min
   - Use code from gameplan Step 3
   - Handle form submission
   - POST to `/auth/login`
   - Show errors, redirect on success

4. **Add Login Route** (`web/api/routes/ui.py`) - 15 min
   - Use code from gameplan Step 4
   - Serve login template
   - Redirect if already authenticated

5. **Update Navigation** (`templates/components/navigation.html`) - 30 min
   - Use code from gameplan Step 5
   - Add conditional login link
   - Make logout conditional
   - Update user context reading

6. **User Context Injection** (`web/api/routes/ui.py`) - 60 min
   - Use code from gameplan Step 6
   - Implement `_extract_user_context()`
   - Extract user from `request.state.user_id`
   - Query database for user details

7. **Test End-to-End** - 60 min
   - Follow gameplan Step 7 testing checklist
   - Test all scenarios (authenticated, not authenticated, errors)
   - Verify Lists/Todos buttons now work

---

## Critical Requirements

### STOP CONDITIONS

If ANY of these occur, STOP and report to PM:

1. **Backend doesn't exist** - If `/auth/login` endpoint missing
2. **Auth middleware not working** - If `request.state.user_id` never set
3. **Database query fails** - If can't retrieve user from DB
4. **Cookie not being set** - If JWT token not in response
5. **Tests fail** - If any manual test fails

### MUST FOLLOW

1. **Use Exact Code from Gameplan** - Don't improvise, use provided snippets
2. **Test After Each Step** - Verify each file before moving to next
3. **Follow Existing Patterns** - Match personality-preferences.html styling
4. **No Backend Changes** - Only UI files and route additions
5. **Update Completion Matrix** - Mark each item as you complete it

---

## Testing Protocol

### Before Declaring Done

Run through this complete checklist (from gameplan Step 7):

**Unauthenticated State**:
- [ ] Homepage shows "Login" link
- [ ] `/login` page displays correctly
- [ ] Form has username/password fields
- [ ] No user menu visible

**Login Flow**:
- [ ] Invalid credentials show error
- [ ] Valid credentials redirect to homepage
- [ ] Navigation shows username after login
- [ ] Logout button visible after login

**Authenticated State**:
- [ ] Create List button works (no 401)
- [ ] Create Todo button works (no 401)
- [ ] User menu dropdown works
- [ ] Can navigate to Settings/Account

**Logout Flow**:
- [ ] Logout button redirects to login
- [ ] Navigation shows "Login" link after logout
- [ ] Cannot access protected routes after logout

**Edge Cases**:
- [ ] `/login` while logged in redirects to home
- [ ] Clear cookies → protected routes fail appropriately
- [ ] Network error shows helpful message

---

## Definition of Done

Phase 1 is complete ONLY when:

1. ✅ All 4 new files created (login.html, auth.css, auth.js)
2. ✅ All 2 existing files modified (ui.py, navigation.html)
3. ✅ ALL manual tests pass (see checklist above)
4. ✅ No console errors in browser
5. ✅ Lists/Todos buttons now functional
6. ✅ Completion matrix 100% checked off
7. ✅ Code committed to feature branch
8. ✅ Session log documents all changes

---

## Files You'll Touch

### Create (New Files)
```
templates/login.html          (Step 1 - 60 min)
static/css/auth.css           (Step 2 - 30 min)
static/js/auth.js             (Step 3 - 30 min)
```

### Modify (Existing Files)
```
web/api/routes/ui.py          (Step 4 + Step 6 - 75 min)
templates/components/navigation.html  (Step 5 - 30 min)
```

---

## Common Pitfalls to Avoid

1. **Don't modify backend** - Auth routes already work perfectly
2. **Don't skip testing** - Test after EACH step, not just at end
3. **Don't improvise styling** - Use exact CSS from gameplan
4. **Don't guess user context** - Follow gameplan for `_extract_user_context()`
5. **Don't forget imports** - Add `RedirectResponse` import to ui.py
6. **Don't skip error handling** - JavaScript must handle network errors
7. **Don't hardcode URLs** - Use `/auth/login`, not `http://localhost:8001/...`

---

## Success Metrics

After your work:
- ✅ Alpha users can log in via web UI
- ✅ Username displays in navigation
- ✅ Logout button works
- ✅ Protected features (Lists, Todos, Projects) now functional
- ✅ All UI issues #6, #7, #14 from CSV are resolved

---

## Resources

- **Gameplan**: `dev/2025/11/24/gameplan-auth-ui-phase1.md` - READ THIS FIRST
- **Issue**: `dev/2025/11/24/issue-auth-ui-missing.md`
- **Triage Report**: `dev/2025/11/24/ui-issues-triage-report.md`
- **Investigation**: From Plan agent output
- **Reference Template**: `templates/personality-preferences.html` - For styling patterns
- **Reference Component**: `templates/components/navigation.html` - For user context

---

## Session Logging

Create session log: `dev/2025/11/24/YYYY-MM-DD-HHMM-prog-code-log.md`

Document:
- Each step completed
- Any deviations from gameplan (with reason)
- Testing results
- Issues encountered
- Final verification checklist

---

## After Completion

1. **Update GitHub Issue** - Add "Phase 1 Complete" comment with evidence
2. **Update Session Log** - Mark all completion matrix items
3. **Commit Changes** - One logical commit with all Phase 1 work
4. **Report to PM** - Session log + testing evidence + ready for v0.8.1.1

---

**Ready to Start?**

1. Read gameplan completely
2. Create feature branch: `feat/auth-ui-login-#[ISSUE_NUM]`
3. Follow Steps 1-7 in exact order
4. Test thoroughly
5. Report completion

**Estimated Time**: 4 hours
**Priority**: P0 (Alpha Blocker)
**Blockers**: None (all dependencies ready)

---

**Created**: 2025-11-24 11:15 AM
**By**: Claude Code (Lead Developer)
**For**: Code Agent (Programmer)

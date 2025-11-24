# GitHub Issue: Systematic Error Messaging & User Recovery

## Issue Number
#[TBD] - Missing Error Messages and Recovery Guidance

## Title
**[UX] No error messages or recovery guidance when things fail**

## Labels
- `priority: high`
- `type: enhancement`
- `area: ux`
- `area: error-handling`
- `sprint: MVP`
- `category: polish`

## Description

### Problem Statement
Throughout the alpha testing session (2025-11-24), users encountered multiple failures (login issues, create button failures, missing features) but received **no error messages, guidance, or recovery paths**. Buttons fail silently, features hang without feedback, and users are left confused about what went wrong and how to fix it.

### Impact
**User Experience Degradation**: When features fail, users:
- ❌ Don't know **what** went wrong
- ❌ Don't know **why** it failed
- ❌ Don't know **how** to recover
- ❌ Don't know **who** to contact for help
- ❌ Feel frustrated and lose trust in the application

**Discovered During**: Alpha testing session on 2025-11-24
**Related Issues**:
- #[TBD] Authentication UI Missing - Root cause of many errors
- UI Issues CSV - Multiple failures without error messages

### Examples from Alpha Testing

#### Example 1: Create List Button Fails Silently
**What Happens**:
- User clicks "Create New List"
- Dialog appears
- User enters list name, clicks "Create"
- Nothing happens (401 error in console, invisible to user)
- Dialog stays open, no feedback

**What SHOULD Happen**:
- User clicks "Create New List"
- Dialog appears
- User enters list name, clicks "Create"
- **Error message appears**: "Unable to create list. Please log in and try again."
- **Recovery action**: "Log In" button in error message

#### Example 2: Standup Generate Button Hangs
**What Happens**:
- User clicks "Generate Standup"
- Button shows "pending" state
- Request hangs or fails
- No error message
- User doesn't know if still processing or failed

**What SHOULD Happen**:
- User clicks "Generate Standup"
- Button shows "Generating..."
- **If fails**: Error message appears
- **Error explains**: "Unable to generate standup. Your OpenAI API key may not be configured."
- **Recovery action**: "Go to Settings" button

#### Example 3: Logout Button Does Nothing
**What Happens**:
- User clicks "Logout"
- Nothing happens (no auth session to end)
- No feedback
- User confused

**What SHOULD Happen**:
- User clicks "Logout"
- **If not logged in**: Toast message "You are not currently logged in"
- **If logged in**: Success message "Logged out successfully" + redirect

### Current State

#### ❌ Missing Error Handling
- No toast notifications for errors
- No inline error messages in forms
- No graceful degradation when features unavailable
- No loading state timeouts (buttons hang forever)
- No network error handling
- No 401/403 error interceptors
- No user-friendly error messages (show raw API errors)

#### ✅ Some Error Handling Exists
- Login form has error message display area (but not used elsewhere)
- JavaScript console shows errors (not helpful for users)
- Backend returns proper error codes (but frontend doesn't handle them)

## Acceptance Criteria

### Phase 1: Core Error Infrastructure (P1 - MVP)

#### A. Toast Notification System
- [ ] Global toast notification component
- [ ] Success, error, warning, info variants
- [ ] Auto-dismiss after 5 seconds
- [ ] Manual dismiss button
- [ ] Queue multiple toasts
- [ ] Accessible (ARIA live regions)

#### B. Error Interceptor for API Calls
- [ ] Global fetch wrapper that catches errors
- [ ] 401 errors → Show "Please log in" toast + redirect to login
- [ ] 403 errors → Show "You don't have permission"
- [ ] 404 errors → Show "Resource not found"
- [ ] 500 errors → Show "Server error, please try again"
- [ ] Network errors → Show "Check your connection"
- [ ] Timeout errors → Show "Request timed out"

#### C. Loading State Timeouts
- [ ] All buttons with loading states have 30s timeout
- [ ] After timeout, show error: "Request took too long"
- [ ] Provide retry button
- [ ] Log timeout for debugging

### Phase 2: Contextual Error Messages (P2 - Post-MVP)

#### A. Form Validation Messages
- [ ] Inline validation for all forms
- [ ] Show errors next to fields (not just at top)
- [ ] Clear, actionable error text
- [ ] Example: "Password must be at least 8 characters"

#### B. Feature-Specific Error Messages
- [ ] Lists/Todos: "Authentication required" with login link
- [ ] Standup: "API key not configured" with settings link
- [ ] Files: "Upload failed" with specific reason
- [ ] Projects: Permission errors with explanation

#### C. Recovery Actions
- [ ] Every error message has recovery action
- [ ] Example: "Not logged in" → "Log In" button
- [ ] Example: "API key missing" → "Go to Settings" button
- [ ] Example: "Network error" → "Retry" button

### Phase 3: Proactive User Guidance (P3 - Future)

#### A. Empty States
- [ ] "No lists yet" → "Create your first list" call-to-action
- [ ] "Not connected" → "Connect your account" button
- [ ] "No API key" → "Add API key in settings"

#### B. Tooltips and Help Text
- [ ] Contextual help for complex features
- [ ] "What's this?" links to documentation
- [ ] Hover tooltips for icons

#### C. Error Prevention
- [ ] Disable buttons that won't work (e.g., create list when not logged in)
- [ ] Show why disabled: "Log in to create lists"
- [ ] Prevent errors before they happen

## Technical Approach

### Architecture

```
┌─────────────────────────────────────┐
│  User Action (e.g., click button)  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  API Call (fetch with error wrapper)│
└─────────────┬───────────────────────┘
              │
              ├──Success──> Update UI
              │
              └──Error────> Error Handler
                            │
                            ├─> Parse error type
                            ├─> Get user-friendly message
                            ├─> Show toast notification
                            ├─> Provide recovery action
                            └─> Log for debugging
```

### Files to Create

#### Phase 1
1. `static/js/toast.js` - Toast notification system
2. `static/css/toast.css` - Toast styling
3. `static/js/error-handler.js` - Global error handler
4. `static/js/api-wrapper.js` - Fetch wrapper with error handling

#### Phase 2
2. `static/js/validators.js` - Form validation helpers
3. `docs/user-guide/error-messages.md` - Error message catalog

### Files to Modify

#### Phase 1
1. `templates/lists.html` - Use global error handler
2. `templates/todos.html` - Use global error handler
3. `templates/standup.html` - Add timeout handling
4. All templates - Include toast.js and toast.css

## Complexity Estimate

### Phase 1 (Core Infrastructure): **8 hours**
- Toast notification system: 3 hours
- Error interceptor: 2 hours
- Loading state timeouts: 2 hours
- Integration with existing features: 1 hour

### Phase 2 (Contextual Messages): **12 hours**
- Form validation: 4 hours
- Feature-specific errors: 6 hours
- Recovery actions: 2 hours

### Phase 3 (Proactive Guidance): **10 hours**
- Empty states: 4 hours
- Tooltips and help: 3 hours
- Error prevention: 3 hours

**Total: 30 hours**

## Dependencies
- **Phase 1** depends on authentication UI being complete (Issue #[TBD])
- Toast system should be built before other error handling
- Error catalog needs product input for messaging

## Success Metrics

### Quantitative
- **Zero silent failures** - Every error shows user message
- **100% recovery actions** - Every error has "what to do next"
- **<5s feedback time** - Errors show within 5 seconds of failure
- **Error rate tracking** - Log all errors for analysis

### Qualitative
- **User confidence** - Users know what went wrong
- **User autonomy** - Users can self-recover without support
- **Trust** - Application feels reliable and transparent

## Examples of Good Error Messages

### ❌ Bad Error Messages
- "Error 401"
- "Request failed"
- "Something went wrong"
- [No message at all]

### ✅ Good Error Messages
- "You need to log in to create lists. [Log In]"
- "Unable to connect to server. Check your internet connection and try again. [Retry]"
- "Your OpenAI API key is not configured. Add one in settings to use this feature. [Go to Settings]"
- "List name is required. Please enter a name for your list."

## Priority Rationale

**P1 (MVP)**: Phase 1 is critical for alpha testing. Users need basic error feedback to effectively test the application.

**P2 (Post-MVP)**: Phase 2 improves UX but isn't blocking. Can ship MVP with basic error handling.

**P3 (Future)**: Phase 3 is polish and proactive guidance. Nice to have but not essential for launch.

## Related ADRs
- Consider creating ADR for error handling strategy
- Define error message tone and voice guidelines
- Establish error logging and monitoring approach

## Testing Strategy

### Manual Testing
- Trigger each error scenario
- Verify error message appears
- Verify recovery action works
- Test network offline mode
- Test API timeout scenarios

### Automated Testing
- E2E tests for error flows
- Unit tests for error message generation
- Integration tests for error interceptor

## Notes

**Discovered**: This issue was identified during alpha testing when multiple features failed silently without user feedback. It's a **systematic problem** affecting the entire application, not isolated to specific features.

**Philosophy**: Every error is an opportunity to help the user. Error messages should:
1. Explain what went wrong (in user terms)
2. Explain why it happened (if helpful)
3. Tell the user what to do next (recovery)
4. Be empathetic and supportive

**Tone**: Friendly, helpful, never blaming the user.

---

**Created**: 2025-11-24 11:20 AM
**By**: Claude Code (Programmer)
**Session**: 2025-11-24-0516-prog-code-log.md
**Priority**: P1 for Phase 1, P2 for Phase 2-3

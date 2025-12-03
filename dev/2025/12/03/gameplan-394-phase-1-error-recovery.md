# Gameplan: Issue #394 Phase 1 - Error Messaging & Recovery Core

**Issue**: #394 CORE-UX-ERROR-QUAL: No error messages or recovery guidance
**Phase**: 1 of 3 (Core Infrastructure)
**Estimated Effort**: Small-Medium (~5h remaining after toast discovery)
**Date**: 2025-12-03

---

## Phase -1: Infrastructure Verification (COMPLETE)

### Verified Infrastructure

**Web framework**: FastAPI (web/app.py)
**JS Utilities**: Existing in web/static/js/
- `toast.js` - COMPLETE toast notification system (success/error/warning/info)
- `loading.js` - COMPLETE loading state utilities (button/page/overlay)
- `dialog.js`, `form-validation.js`, etc.

**Templates**: 18 HTML templates in templates/
**Error pages**: 404.html, 500.html, network-error.html already exist

### Phase 1 Scope (Remaining Work)

**Phase 1A - Toast System**: ✅ ALREADY COMPLETE
- toast.js has success/error/warning/info with WCAG 2.2 AA accessibility
- Auto-dismiss, keyboard support, aria-live

**Phase 1B - Error Interceptor**: NOT DONE
- Create `api-wrapper.js` - global fetch wrapper
- Intercept failed API responses
- Show toast with error details
- Handle network errors (offline)

**Phase 1C - Loading Timeouts**: NOT DONE
- Extend Loading.button() with timeout parameter
- Show warning after X seconds
- Auto-recover and show error if timeout exceeded

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
```bash
gh issue view 394
```

### Update Issue Description
```markdown
## Status: Phase 1 In Progress

### Phase 1A: Toast System
- [x] WCAG 2.2 AA accessible toast notifications
- [x] Success/error/warning/info variants
- [x] Auto-dismiss with keyboard support
- Evidence: web/static/js/toast.js (164 lines)

### Phase 1B: Error Interceptor (In Progress)
- [ ] Create api-wrapper.js with global fetch wrapper (PM will validate)
- [ ] Intercept 4xx/5xx responses with user-friendly messages
- [ ] Handle network errors with offline detection
- [ ] Integrate with existing toast system

### Phase 1C: Loading Timeouts (Pending)
- [ ] Add timeout parameter to Loading.button() (PM will validate)
- [ ] Show warning after 10s, error after 30s
- [ ] Auto-recover failed actions
```

---

## Phase 1: Development Work

### Subtask 1B: Create API Wrapper with Error Interceptor

**Files to Create**:
- `web/static/js/api-wrapper.js` - New file

**Implementation Details**:
```javascript
// ApiWrapper provides fetch() with automatic error handling
const ApiWrapper = {
  // Default timeout in ms
  defaultTimeout: 30000,

  // Main fetch wrapper
  async fetch(url, options = {}) {
    // Add timeout
    // Intercept response
    // Handle errors with Toast
    // Detect network offline
  },

  // Convenience methods
  async get(url, options = {}),
  async post(url, body, options = {}),
  async put(url, body, options = {}),
  async delete(url, options = {}),

  // Error handling
  handleError(error, response)
};
```

**Acceptance Criteria**:
- [ ] ApiWrapper.fetch() wraps native fetch with timeout (PM will validate)
- [ ] 4xx errors show Toast.warning with user-friendly message (PM will validate)
- [ ] 5xx errors show Toast.error with "Something went wrong" (PM will validate)
- [ ] Network errors show Toast.error with "Connection failed" (PM will validate)
- [ ] Returns response for chaining (PM will validate)
- [ ] WCAG accessible - no flash, appropriate timing (PM will validate)

**Test Scope**:
- Unit tests: ApiWrapper.fetch(), error handling
- Integration tests: Real endpoint error responses
- No performance tests needed (not performance-critical)

### Subtask 1C: Add Loading Timeout to Button States

**Files to Modify**:
- `web/static/js/loading.js` - Add timeout parameter

**Implementation Details**:
```javascript
// Extend Loading.button() signature:
Loading.button(button, isLoading, options = {})
// options: { timeout: 30000, onTimeout: () => {} }

// Add timeout tracking
Loading.buttonWithTimeout(button, timeoutMs = 30000)
// Returns: { stop: () => void, timeoutPromise: Promise }
```

**Acceptance Criteria**:
- [ ] Loading.button() accepts optional timeout parameter (PM will validate)
- [ ] Warning shown after 10s of loading (PM will validate)
- [ ] Error shown after 30s with recovery option (PM will validate)
- [ ] Timeout clears when loading stops (PM will validate)
- [ ] Screen reader announces timeout warning (PM will validate)

**Test Scope**:
- Unit tests: Timeout behavior, cleanup
- Integration tests: Button loading with timeouts
- No performance tests needed

---

## Phase Z: Final Bookending

### Evidence Compilation
- [ ] Show `ls -la web/static/js/api-wrapper.js`
- [ ] Show loading.js diff with timeout changes
- [ ] pytest output for any new tests
- [ ] Manual test: trigger API error, see toast

### Documentation Updates
- [ ] Update issue #394 with Phase 1 complete
- [ ] Note any architecture decisions in session log

### PM Approval Request
```markdown
@PM - Issue #394 Phase 1 complete:
- Phase 1A: Toast system (already existed) ✓
- Phase 1B: API wrapper with error interceptor ✓
- Phase 1C: Loading timeouts ✓
- Evidence provided ✓

Ready for review. Recommend evaluating scope of Phase 2/3 before continuing.
```

---

## Completion Matrix

| Subtask | Status | Evidence |
|---------|--------|----------|
| 1A Toast System | COMPLETE | web/static/js/toast.js exists |
| 1B Error Interceptor | PENDING | api-wrapper.js to create |
| 1C Loading Timeouts | PENDING | loading.js to extend |

---

## STOP Conditions

Stop and escalate if:
- Existing fetch calls would break with wrapper
- Toast system has bugs not previously discovered
- Loading.js architecture prevents timeout extension
- WCAG requirements unclear

---

## Notes

This is a single-agent task (Claude Code or Cursor can execute independently).
No cross-validation needed - straightforward implementation.
Templates reference: gameplan-template-v8.md, agent-prompt-template.md v10.2

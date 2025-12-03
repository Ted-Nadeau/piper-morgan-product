# Gameplan: Issue #394 Phase 2 - Contextual Error Messages

**Issue**: #394 CORE-UX-ERROR-QUAL: No error messages or recovery guidance
**Phase**: 2 of 3 (Contextual Errors)
**Estimated Effort**: Medium (~8h)
**Date**: 2025-12-03
**Dependencies**: Phase 1 Complete (toast.js, api-wrapper.js, loading.js with timeouts)

---

## Phase -1: Infrastructure Verification (COMPLETE)

### Verified Infrastructure from Phase 1

**JS Utilities Created/Verified**:
- `toast.js` - COMPLETE toast notification system (WCAG 2.2 AA)
- `api-wrapper.js` - NEW global fetch wrapper with error interception
- `loading.js` - EXTENDED with `buttonWithTimeout()` for timeout warnings
- `form-validation.js` - COMPLETE form validation (FormValidation + Validators)

**Current Error Handling in setup.js**:
- Uses `showError()` function (div-based, 5s auto-hide)
- Inline validation status divs for API key validation
- No integration with Toast system
- No use of ApiWrapper
- No use of FormValidation

### Phase 2 Scope (Remaining Work)

**Phase 2A - Setup Wizard Error Enhancement**: NOT DONE
- Replace `showError()` with Toast integration
- Use ApiWrapper for all fetch calls
- Add recovery actions to error messages

**Phase 2B - Form Validation Integration**: NOT DONE
- Wire FormValidation into account creation form
- Replace inline password mismatch check with validators
- Add email format validation

**Phase 2C - Contextual Recovery Actions**: NOT DONE
- Add actionable buttons to error messages
- "Retry" for network errors
- "Check Docker" for service errors
- Guide users to resolution

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
```bash
gh issue view 394
```

### Update Issue Description
```markdown
## Status: Phase 2 In Progress

### Phase 1: Complete ✓
- [x] Toast system (pre-existing)
- [x] API wrapper with error interceptor
- [x] Loading timeouts

### Phase 2A: Setup Wizard Enhancement (In Progress)
- [ ] Replace showError() with Toast (PM will validate)
- [ ] Use ApiWrapper for all setup fetch calls (PM will validate)
- [ ] Add recovery actions to error messages (PM will validate)

### Phase 2B: Form Validation Integration (Pending)
- [ ] Wire FormValidation into account form (PM will validate)
- [ ] Add email/password validators (PM will validate)

### Phase 2C: Recovery Actions (Pending)
- [ ] Retry buttons for network errors (PM will validate)
- [ ] Docker guidance for service errors (PM will validate)
```

---

## Phase 1: Development Work

### Subtask 2A: Setup Wizard Error Enhancement

**Files to Modify**:
- `web/static/js/setup.js` - Main setup wizard

**Implementation Details**:

1. **Replace showError() with Toast**:
```javascript
// Before
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => { errorDiv.style.display = 'none'; }, 5000);
}

// After
function showError(message, title = 'Error') {
    if (typeof Toast !== 'undefined') {
        Toast.error(title, message);
    } else {
        // Fallback for when Toast not loaded
        console.error(title, message);
    }
}
```

2. **Use ApiWrapper for fetch calls**:
```javascript
// Before
const response = await fetch('/setup/check-system', { method: 'POST' });

// After (ApiWrapper handles errors automatically)
const response = await ApiWrapper.post('/setup/check-system');
```

3. **Add contextual error titles**:
- System check fails → "System Check Failed"
- API key invalid → "Invalid API Key"
- Account creation fails → "Account Creation Failed"
- Network error → "Connection Failed"

**Acceptance Criteria**:
- [ ] All showError() calls replaced with Toast.error() (PM will validate)
- [ ] All fetch() calls use ApiWrapper methods (PM will validate)
- [ ] Error messages have contextual titles (PM will validate)
- [ ] Error div removed from template (PM will validate)
- [ ] WCAG accessible - proper timing, no flash (PM will validate)

### Subtask 2B: Form Validation Integration

**Files to Modify**:
- `web/static/js/setup.js` - Add FormValidation init

**Implementation Details**:

```javascript
// Add at end of IIFE, before checkSetupStatus()
FormValidation.init('account-form', {
    username: [Validators.required(), Validators.minLength(3)],
    email: [Validators.required(), Validators.email()],
    password: [Validators.required(), Validators.minLength(8)],
    'password-confirm': [
        Validators.required(),
        Validators.custom(
            (value) => value === document.getElementById('password').value,
            'Passwords do not match'
        )
    ]
});
```

**Acceptance Criteria**:
- [ ] FormValidation.init() called for account-form (PM will validate)
- [ ] Real-time validation on blur/input (PM will validate)
- [ ] Password match validation using Validators.custom() (PM will validate)
- [ ] Remove manual password mismatch check from submit handler (PM will validate)
- [ ] aria-invalid and error messages display correctly (PM will validate)

### Subtask 2C: Recovery Actions

**Files to Modify**:
- `web/static/js/setup.js` - Add recovery buttons to errors

**Implementation Details**:

For service check failures, add guidance:
```javascript
if (!data.all_required_ready) {
    Toast.error(
        'Services Not Running',
        'Required services are offline. Start Docker with: docker-compose up -d'
    );
}
```

For network errors, add retry guidance:
```javascript
} catch (err) {
    if (!navigator.onLine) {
        Toast.error('No Connection', 'Check your internet connection and try again.');
    } else {
        Toast.error('Connection Failed', 'Unable to reach server. Please try again.');
    }
}
```

**Acceptance Criteria**:
- [ ] Docker command shown when services not running (PM will validate)
- [ ] Offline detection with appropriate message (PM will validate)
- [ ] Generic retry guidance for other network errors (PM will validate)
- [ ] All error messages guide user to next action (PM will validate)

---

## Phase Z: Final Bookending

### Evidence Compilation
- [ ] Show `git diff web/static/js/setup.js`
- [ ] Manual test: trigger each error type, see toast
- [ ] Verify FormValidation real-time feedback
- [ ] Screen reader test for accessibility

### Documentation Updates
- [ ] Update issue #394 with Phase 2 complete
- [ ] Note integration patterns in session log

### PM Approval Request
```markdown
@PM - Issue #394 Phase 2 complete:
- Phase 2A: Setup wizard uses Toast ✓
- Phase 2B: FormValidation integrated ✓
- Phase 2C: Recovery actions added ✓
- Evidence provided ✓

Ready for review. Recommend evaluating Phase 3 scope before continuing.
```

---

## Completion Matrix

| Subtask | Status | Evidence |
|---------|--------|----------|
| 2A Setup Toast Integration | PENDING | setup.js showError → Toast |
| 2B FormValidation Integration | PENDING | FormValidation.init() added |
| 2C Recovery Actions | PENDING | Contextual error guidance |

---

## STOP Conditions

Stop and escalate if:
- Toast.js has bugs when integrated with setup.js
- ApiWrapper breaks existing setup fetch flow
- FormValidation CSS conflicts with setup form styles
- WCAG requirements unclear for error display timing

---

## Notes

This is a single-agent task (Claude Code can execute independently).
Main risk: CSS styling of error messages may need adjustment.
Templates reference: gameplan-template-v8.md

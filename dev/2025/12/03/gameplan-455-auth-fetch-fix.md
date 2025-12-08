# Gameplan: Issue #455 - Add credentials to fetch calls
*Created: December 3, 2025*
*GitHub Issue: https://github.com/mediajunkie/piper-morgan-product/issues/455*

---

## Summary

All fetch() calls for authenticated endpoints need `credentials: 'include'` to send the auth cookie. Currently, most templates are missing this, causing 401 errors for logged-in users.

## Root Cause

The login sets an `auth_token` cookie, but fetch() doesn't send cookies by default. The `credentials: 'include'` option is required.

## Files to Modify

### Priority 1: Core User Actions

| File | Fetch Calls | Lines | Current Status |
|------|-------------|-------|----------------|
| templates/home.html | intent POST, workflows GET | ~1199, ~1115 | MISSING credentials |
| templates/todos.html | create, shares, delete | ~224, ~284, ~363, ~389 | MISSING credentials |
| templates/lists.html | create, shares, delete | ~226, ~286, ~365, ~391 | MISSING credentials |
| templates/projects.html | shares | ~256, ~335, ~361 | MISSING credentials |

### Already Fixed (Reference)

| File | Lines | Status |
|------|-------|--------|
| templates/home.html | ~1053 (file upload) | HAS credentials: 'include' |
| templates/components/navigation.html | ~480 | HAS credentials: 'include' |

### Lower Priority (May Need Check)

- templates/files.html
- templates/standup.html
- templates/learning-dashboard.html
- templates/account.html
- templates/settings-index.html
- templates/personality-preferences.html

---

## Implementation Approach

**Option A: Add credentials to each fetch call**
- Simple, explicit
- More repetitive but clear
- Lower risk

**Option B: Create/extend a wrapper function**
- api-wrapper.js exists but may not handle credentials
- Would need to migrate all fetch calls
- Higher risk, more work

**Recommendation**: Option A for this fix. Quick, low-risk, unblocks users.

---

## Phase 1: Fix Priority Templates (Unblock Alpha Testing)

### 1.1 templates/home.html

Add `credentials: 'include'` to:
- Line ~1199: intent POST (chat submit)
- Line ~1115: workflows GET (polling)

### 1.2 templates/todos.html

Add `credentials: 'include'` to all fetch calls:
- Line ~224: POST /api/v1/todos (create)
- Line ~284: GET shares
- Line ~363: POST share
- Line ~389: DELETE share

### 1.3 templates/lists.html

Same pattern as todos.html:
- Line ~226: POST /api/v1/lists (create)
- Line ~286: GET shares
- Line ~365: POST share
- Line ~391: DELETE share

### 1.4 templates/projects.html

- Line ~256: GET shares
- Line ~335: POST share
- Line ~361: DELETE share

---

## Phase 2: Audit Remaining Templates

Check and fix if needed:
- files.html
- standup.html
- learning-dashboard.html
- account.html
- settings-index.html
- personality-preferences.html

---

## Completion Matrix

| Task | Status | Evidence |
|------|--------|----------|
| home.html - intent POST | [ ] | Line number |
| home.html - workflows GET | [ ] | Line number |
| todos.html - all fetch calls | [ ] | grep confirmation |
| lists.html - all fetch calls | [ ] | grep confirmation |
| projects.html - all fetch calls | [ ] | grep confirmation |
| Audit remaining templates | [ ] | grep results |
| Test chat submit in browser | [ ] | PM verification |
| Test create todo in browser | [ ] | PM verification |
| Merge to production | [ ] | git log |

---

## Acceptance Criteria

- [ ] Logged-in user can submit chat message
- [ ] Logged-in user can create todo
- [ ] Logged-in user can create list
- [ ] Logged-in user can create project
- [ ] All verified in browser on alpha laptop

---

## Risk Assessment

**Low Risk**: This is an additive change. Adding `credentials: 'include'` to fetch calls doesn't break anything - it just makes them work when cookies exist.

**Edge Case**: If someone is testing without cookies, the requests will still work (backend will reject with 401 as designed).

---

## Post-Fix: Consider Future Prevention

After this fix, consider:
1. Lint rule to require credentials on API fetch calls
2. Update api-wrapper.js to include credentials by default
3. Document the pattern for future template authors

# Gameplan: Issue #394 Phase 3 - Global Error Handling

**Issue**: #394 CORE-UX-ERROR-QUAL: No error messages or recovery guidance
**Phase**: 3 of 3 (Global Error Handling)
**Estimated Effort**: Small (~3h - reduced from 6h after survey)
**Date**: 2025-12-03
**Dependencies**: Phase 1 & 2 Complete

---

## Phase -1: Infrastructure Verification (COMPLETE)

### Survey Results

**Templates already with toast.js** (8 - no work needed):
- files.html, home.html, lists.html, personality-preferences.html
- projects.html, setup.html, standup.html, todos.html

**Templates with fetch() but NO toast.js** (3 - need work):
- account.html
- learning-dashboard.html
- settings-index.html

**Templates without fetch()** (static pages - no JS work needed):
- login.html, integrations.html, privacy-settings.html, advanced-settings.html
- 404.html, 500.html, network-error.html

---

## Phase 3: Development Work

### Subtask 3A: Add Toast/ApiWrapper to account.html
- Add toast.css link
- Add toast.js, api-wrapper.js scripts
- Update fetch() calls to use ApiWrapper or add error handling

### Subtask 3B: Add Toast/ApiWrapper to learning-dashboard.html
- Add toast.css link
- Add toast.js, api-wrapper.js scripts
- Update fetch() calls to use ApiWrapper or add error handling

### Subtask 3C: Add Toast/ApiWrapper to settings-index.html
- Add toast.css link
- Add toast.js, api-wrapper.js scripts
- Update fetch() calls to use ApiWrapper or add error handling

### Acceptance Criteria
- [ ] All templates with fetch() have toast.js loaded (PM will validate)
- [ ] Error handling shows contextual toast messages (PM will validate)
- [ ] Offline detection works across all pages (PM will validate)
- [ ] WCAG accessible error messages (PM will validate)

---

## Completion Matrix

| Template | Has toast.js | Has fetch() | Status |
|----------|-------------|-------------|--------|
| account.html | ❌ | ✅ | PENDING |
| learning-dashboard.html | ❌ | ✅ | PENDING |
| settings-index.html | ❌ | ✅ | PENDING |

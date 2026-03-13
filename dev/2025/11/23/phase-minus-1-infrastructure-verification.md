# Phase -1: Infrastructure Verification Report
**Issue**: #376 FRONTEND-RBAC-AWARENESS
**Date**: November 23, 2025, 9:15 AM
**Lead Developer**: xian (PM)
**Purpose**: Verify infrastructure before proceeding with gameplan

---

## Current Understanding

### Frontend Architecture Discovery

**Framework**: Hybrid architecture
- **Primary**: Jinja2 templates (server-side rendering)
- **Secondary**: Vanilla JavaScript utilities (`web/static/js/`)
- **Tertiary**: React component (1 file: `MultiAgentWorkflowProgress.jsx`)

**Key Findings**:
1. ❌ No `web/templates/` directory found
2. ✅ HTML assets in `web/assets/` directory:
   - `personality-preferences.html`
   - `standup.html`
   - `learning-dashboard.html`
3. ✅ Utility JS modules in `web/static/js/`:
   - `dialog.js`, `focus-manager.js`, `form-validation.js`
   - `loading.js`, `session-timeout.js`, `toast.js`
   - `help-tooltip.js`, `keyboard-shortcuts.js`, `page-transitions.js`
4. ✅ Main app: `web/app.py` (FastAPI + Jinja2Templates)

### User Context / Auth System

**Status**: ⚠️ **NOT FOUND in initial search**

**Searched**:
- ❌ No `window.currentUser` references in HTML files checked
- ❌ No `window.user` references found
- ❌ No obvious JWT token handling in `web/static/js/` utilities

**Possible Locations** (need to investigate):
- Could be in `web/app.py` (FastAPI routes passing user to templates)
- Could be in Issue #307 work (mentioned as "infrastructure working")
- May exist but not in files searched yet

### Component Locations

**Lists/Todos/Projects** components:
- ⚠️ **NOT FOUND** in initial search

**HTML files found**:
- `web/assets/personality-preferences.html` (preferences UI)
- `web/assets/standup.html` (standup feature)
- `web/assets/learning-dashboard.html` (learning dashboard)

**NO evidence of**:
- Lists UI components
- Todos UI components
- Projects UI components

### Known Issues

**From investigation**:
1. No templates directory at expected location
2. No obvious user context setup found
3. No resource (Lists/Todos/Projects) UI components found
4. Unclear where/if resource UI exists

---

## Infrastructure Assessment

### What EXISTS ✅

1. **FastAPI Backend** (`web/app.py`):
   - Jinja2Templates setup
   - StaticFiles mounting
   - Error handling utilities
   - Personality integration

2. **Utility JavaScript Modules**:
   - Dialog system
   - Form validation
   - Loading states
   - Toast notifications
   - Session timeout tracking
   - Keyboard shortcuts
   - Page transitions

3. **HTML Assets** (limited):
   - Personality preferences page
   - Standup page
   - Learning dashboard page

4. **One React Component**:
   - `MultiAgentWorkflowProgress.jsx` (probably not relevant for RBAC)

### What's MISSING ❌

1. **User Context System**:
   - No `window.currentUser` found
   - No JWT token handling visible
   - No role/permission state management

2. **Resource UI Components**:
   - No Lists UI
   - No Todos UI
   - No Projects UI

3. **Permission Infrastructure**:
   - No existing permission checks
   - No role-based component wrappers
   - No sharing UI

---

## Critical Questions for PM

### Question 1: Where are the resource UIs?

**Options**:
A. They exist but I haven't found them yet (where should I look?)
B. They're in a different location than expected
C. They haven't been built yet (this would be a STOP condition)
D. They're part of the main conversation UI (not separate pages)

**Impact**: If resource UIs don't exist, we can't add permission awareness to them.

### Question 2: Where is user context set?

**Possible locations**:
- In `web/app.py` route handlers (passed to Jinja2 templates)
- In a JavaScript file I haven't checked yet
- In Issue #307 work (CONV-UX-NAV - "all route handlers properly extract user context")
- Doesn't exist yet (would be a STOP condition)

**Impact**: If user context isn't available in frontend, we need to create it before Phase 1.

### Question 3: Is this primarily a Jinja2 template project?

**Evidence suggests YES**:
- FastAPI with Jinja2Templates
- HTML files in `web/assets/`
- Minimal JavaScript (utilities only)
- One React component (seems isolated)

**If YES**: Our approach will be:
- Server-side rendering with user context in templates
- Vanilla JavaScript for permission helpers
- No React/Vue framework assumptions

**If NO**: Need to understand actual architecture.

### Question 4: Does Issue #307 have relevant context?

**From session summary**: "#307 infrastructure working - route handlers extract user context"

**Questions**:
- Did #307 already set up user context in templates?
- Is there a pattern we should follow from #307?
- Should I read the #307 completion report?

---

## Recommendations

### Option A: Proceed with Investigation (Phase 0)

**If**:
- Resource UIs exist somewhere I haven't found yet
- User context exists (from #307 or elsewhere)
- PM can point me to correct locations

**Action**:
- Deeper investigation of `web/app.py` routes
- Search for home/dashboard templates
- Check for conversation UI that might include resource management
- Read #307 completion artifacts

### Option B: STOP - Missing Infrastructure

**If**:
- Resource UIs don't exist yet
- User context not set up
- Frontend different than expected (SPA vs SSR)

**Action**:
- Document gap
- Propose alternative approach or creation plan
- Wait for PM decision

### Option C: Pivot - Different Architecture

**If**:
- This is a SPA (single-page application) I haven't identified
- Resources managed via API only (no UI)
- Different framework than Jinja2 + vanilla JS

**Action**:
- Re-investigate with new framework assumptions
- Document actual architecture
- Revise gameplan approach

---

## Immediate Next Steps (Awaiting PM Decision)

**Before proceeding to Phase 0**, I need PM to clarify:

1. **Where are Lists/Todos/Projects UI components?**
   - File paths or directories to check
   - Or confirmation they don't exist yet

2. **Where is user context set up?**
   - Point me to #307 completion work
   - Or tell me it needs to be created in Phase 1

3. **Is Jinja2 + vanilla JS the correct architecture assumption?**
   - Or is there a SPA framework I'm missing?

4. **Should I read any specific prior completion reports?**
   - #307 (CONV-UX-NAV)?
   - #310 (Settings & Startup Quick Wins)?
   - Any others with frontend context?

---

## Phase -1 Checkpoint Decision

**Chief Architect / PM: Please choose ONE**:

- [ ] **PROCEED** - I'll provide the missing context you need (see questions above)
- [ ] **INVESTIGATE** - Go deeper with Phase 0 (Serena queries, file reads, etc.)
- [ ] **REVISE** - Different architecture, need to revise gameplan
- [ ] **STOP** - Missing critical infrastructure, need to build it first

**Notes from PM**:
[Space for PM feedback]

---

**Status**: Awaiting PM decision on Phase -1 checkpoint
**Next Action**: PM answers questions above, then I proceed accordingly

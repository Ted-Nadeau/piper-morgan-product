# Agent Prompt: #554 Phase 4 - Site-Wide Integration

**Issue**: #554 STANDUP-CHAT-WIDGET
**Phase**: 4 of 6
**Model**: Haiku
**Deployed By**: Lead Developer
**Depends On**: Phases 1-3 complete

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 4 of GitHub Issue #554. Your work is part of a multi-agent coordination chain.

### Your Acceptance Criteria
- [ ] Widget visible on all main pages
- [ ] CSS/JS loaded correctly everywhere
- [ ] No layout regressions
- [ ] Session persists across page navigation

**Every checkbox must be addressed in your handoff.**

### Your Handoff Format
Return your work with this structure:
```
## Issue #554 Phase 4 Completion Report
**Status**: Complete/Partial/Blocked

**Approach Chosen**: [A/B/C and why]

**Files Modified**:
- [file1] (+X lines)
- [file2] (+X lines)

**Pages Verified**:
- /home - Widget visible ✓
- /standup - Widget visible ✓
- /todos - Widget visible ✓
- /lists - Widget visible ✓
- /projects - Widget visible ✓
- /files - Widget visible ✓
- /settings/* - Widget visible ✓

**Session Test**:
- Started conversation on /home
- Navigated to /todos
- Conversation history: [preserved/lost]

**Blockers** (if any):
- [Blocker description]
```

---

## Mission

Include the floating chat widget on all pages in the application.

**Scope**: ONLY Phase 4 integration. Assume Phase 3 session persistence is already implemented.

---

## Context

- **GitHub Issue**: #554 STANDUP-CHAT-WIDGET
- **Current State**: Widget works on home.html only
- **Target State**: Widget accessible from every page
- **Dependencies**: Phases 1-3 complete (extraction, floating, session)
- **Risk**: Layout regressions, CSS conflicts on other pages

---

## Pre-Flight Verification

Before starting, verify previous phases are complete:

```bash
# Phase 1-2 files must exist
ls -la web/static/css/chat.css
ls -la web/static/js/chat.js
ls -la templates/components/chat-widget.html

# Phase 3 - check for localStorage code
grep -n "localStorage" web/static/js/chat.js
```

**STOP if files missing or no localStorage code** - previous phases incomplete.

---

## Investigation: Find Best Integration Point

### Option A: Navigation Component

Check if navigation is included on all pages:

```bash
# Find pages that include navigation
grep -l "navigation.html" templates/*.html

# Check navigation component location
ls -la templates/components/navigation.html
```

**If all pages include navigation.html** → Add widget to end of navigation.html

### Option B: Base Template

Check if there's a base template:

```bash
# Find templates that extend a base
grep -l "extends" templates/*.html

# Find base templates
ls -la templates/base*.html templates/layout*.html
```

**If base template exists and is extended** → Add widget to base template

### Option C: Individual Pages

If no common include point:

```bash
# List all main templates
ls templates/*.html
```

**Add widget include to each page individually**.

---

## Implementation Steps

### Step 1: Determine Approach

Run the investigation commands above and choose:

| Approach | When to Use | Effort |
|----------|-------------|--------|
| A: Navigation | All pages include navigation.html | Small (1 file) |
| B: Base Template | All pages extend base | Small (1 file) |
| C: Individual | No common point | Medium (7+ files) |

**Document your choice in the handoff.**

### Step 2: Ensure CSS/JS Loaded

The CSS and JS must be loaded on every page.

**Check current include pattern**:
```bash
# How does home.html include the CSS/JS?
grep -n "chat.css\|chat.js" templates/home.html
```

**Option 1: Add to component HTML**

If `chat-widget.html` doesn't include CSS/JS links, add them:

```html
<!-- At top of chat-widget.html -->
<link rel="stylesheet" href="/static/css/chat.css">
<!-- At bottom of chat-widget.html -->
<script src="/static/js/chat.js"></script>
```

**Option 2: Add to common head/scripts**

If there's a common head include:
```bash
grep -l "head" templates/components/*.html
```

Add CSS link there. Add JS before closing body.

### Step 3: Add Widget Include

Based on your chosen approach:

**Approach A (Navigation)**:
```html
<!-- At end of templates/components/navigation.html -->
{% include 'components/chat-widget.html' %}
```

**Approach B (Base Template)**:
```html
<!-- Before </body> in base.html -->
{% include 'components/chat-widget.html' %}
```

**Approach C (Individual)**:
Add to each template before `</body>`:
- `templates/home.html`
- `templates/standup.html`
- `templates/todos.html`
- `templates/lists.html`
- `templates/projects.html`
- `templates/files.html`
- `templates/settings*.html` (all settings pages)

### Step 4: Verify All Pages

Start server and check each page:

```bash
python main.py
```

**Test each page**:
| Page | URL | Widget Visible? |
|------|-----|-----------------|
| Home | http://localhost:8001/ | |
| Standup | http://localhost:8001/standup | |
| Todos | http://localhost:8001/todos | |
| Lists | http://localhost:8001/lists | |
| Projects | http://localhost:8001/projects | |
| Files | http://localhost:8001/files | |
| Settings | http://localhost:8001/settings | |

### Step 5: Test Session Persistence

1. Open http://localhost:8001/ (home)
2. Click widget toggle to expand
3. Type "hello" and send
4. Navigate to http://localhost:8001/todos
5. Click widget toggle
6. **Verify**: Previous message should appear

If session not preserved, **STOP** - Phase 3 may be incomplete.

### Step 6: Check for Layout Conflicts

On each page, verify:
- [ ] Widget doesn't overlap critical content
- [ ] Widget doesn't break existing layout
- [ ] No CSS conflicts (check browser console for errors)
- [ ] No JavaScript errors in console

---

## STOP Conditions

Stop immediately and report if:
- [ ] Previous phase files don't exist
- [ ] Session not persisting (Phase 3 incomplete)
- [ ] Widget causes layout regression on any page
- [ ] CSS conflicts break page styling
- [ ] JavaScript errors on any page
- [ ] Cannot find common integration point

**When stopped**: Document the issue, provide error details, wait for Lead Dev.

---

## Evidence Requirements

For EVERY claim:
- **"Chose Approach X"** → Explain why (grep output showing pattern)
- **"Widget on all pages"** → List each page tested
- **"Session persists"** → Describe navigation test result
- **"No regressions"** → Confirm no console errors

---

## Files Summary

**Likely Modify** (depends on approach):
- `templates/components/navigation.html` (if Approach A)
- `templates/base.html` (if Approach B)
- `templates/*.html` - 7+ files (if Approach C)
- Possibly `templates/components/chat-widget.html` (add CSS/JS links)

---

## Common Issues

**Issue**: Widget appears but no styling
- **Fix**: Ensure `chat.css` is loaded (check Network tab)

**Issue**: Toggle doesn't work
- **Fix**: Ensure `chat.js` is loaded and runs after DOM ready

**Issue**: Widget visible but behind page content
- **Fix**: Check z-index, may need to increase from 1000

**Issue**: Session not persisting
- **Fix**: This is Phase 3 issue - report as blocker

---

## Remember

- Choose simplest integration approach
- Test EVERY page before claiming complete
- Check for layout regressions
- Session persistence should already work (Phase 3)
- Evidence for all claims

---

*Prompt Version: 1.0*
*Template: agent-prompt-template v10.2*

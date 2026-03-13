# Gameplan: Issue #566 - CONV-PERSIST-4: Home Page Cleanup & Sidebar Integration

**Date**: 2026-01-10
**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/566
**Parent**: #314 (CONV-UX-PERSIST)
**Priority**: P2 (Medium)
**Blocks**: #565 (Sidebar)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Frontend: Jinja2 templates with vanilla JavaScript
- [x] Home page template: `templates/home.html`
- [x] CSS: `web/static/css/` (multiple files)
- [x] Chat components: Already working from #563/#564

**My understanding of the task**:
This is a **frontend visual cleanup** with these goals:
1. Remove/minimize purple hero section
2. Relocate or remove broken/redundant buttons
3. Keep clean greeting area
4. Relocate example prompts to help tooltip
5. Prepare layout for future sidebar (#565)

### Part A.2: Work Characteristics Assessment

**Worktree Assessment:**
- [ ] Multiple agents will work in parallel - NO
- [ ] Task duration >30 minutes - YES
- [x] Frontend-only changes (templates + CSS)
- [x] Visual/audit work first

**Assessment: SKIP WORKTREE** - Single agent, frontend-focused, visual work.

### Part B: PM Verification (Infrastructure Investigation)

**Verification commands** (to run at start of Phase 0):
```bash
ls -la templates/home.html
grep -n "purple\|hero\|btn" templates/home.html | head -20
ls -la web/static/css/
```

**Expected files** (to confirm in Phase 0):
```
templates/home.html           # Main home page template
web/static/css/style.css      # Main styles (likely)
web/static/css/chat.css       # Chat-specific styles
```

**Note**: Actual infrastructure verification happens at start of Phase 0 with audit. If reality differs from expectations, STOP and revise gameplan.

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Infrastructure understood, visual cleanup work

---

## Phase 0.6-0.8: Skipped Phases (Documented)

**Phase 0.6 (Data Flow & Integration)**: SKIP - Frontend-only visual changes, no data flow.

**Phase 0.7 (Conversation Design)**: SKIP - Not a conversational feature.

**Phase 0.8 (Post-Completion Integration)**: SKIP - No database state changes.

---

## Phase 0: Initial Bookending & Audit

### Required Actions

```bash
# 1. Verify issue exists
gh issue view 566

# 2. Update issue status
gh issue comment 566 -b "## Status: Implementation Started
- [ ] Phase 0: Current state audit
- [ ] Phase 1: Remove purple hero
- [ ] Phase 2: Refine greeting area
- [ ] Phase 3: Relocate example prompts
- [ ] Phase 4: Sidebar-ready layout"
```

### Current State Audit

**Goal**: Document what exists before changing it.

**Tasks**:
1. Read `templates/home.html` completely
2. Identify the purple hero section (HTML structure)
3. List all buttons in hero area with their functions
4. List example prompts
5. Identify CSS files involved
6. Note any JavaScript dependencies

**Audit Template**:
```markdown
## Button Inventory

| Button | Location | Works? | Purpose | Decision |
|--------|----------|--------|---------|----------|
| [name] | hero     | Y/N    | [what]  | keep/remove/relocate |

## Example Prompts Found

| Prompt | Location | Decision |
|--------|----------|----------|
| [text] | [where]  | relocate to help |

## Files Involved

| File | Contains |
|------|----------|
| templates/home.html | Hero, greeting, prompts |
| web/static/css/?.css | Styles for hero |
```

---

## Phase 0.5: Frontend-Backend Contract Verification

**Not Applicable** - This is pure visual cleanup, no new endpoints.

---

## Phase 1: Remove Purple Hero

### Approach

1. Identify the hero section in `templates/home.html`
2. For each element in hero:
   - **Working + useful** → relocate (header or help tooltip)
   - **Broken** → remove entirely
   - **Redundant** → remove
3. Remove the purple background/styling
4. Document all changes

### Implementation Steps

**Step 1**: Comment out (don't delete) the hero section first for safety
```html
<!-- Issue #566: Removed purple hero
{% comment %}
<div class="hero-section">
  ...
</div>
{% endcomment %}
-->
```

**Step 2**: Test that page still loads correctly

**Step 3**: If stable, fully remove commented code

**Step 4**: Remove associated CSS (if any dedicated hero styles)

### Acceptance Criteria - Phase 1

- [ ] Purple hero section removed from templates/home.html
- [ ] No broken buttons visible on page
- [ ] Page still loads and functions correctly
- [ ] Change documented

---

## Phase 2: Refine Greeting Area

### Design Target

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Good afternoon, xian!                                 │
│   Friday, January 10, 2026                        [?]   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Implementation Steps

**Step 1**: Locate existing greeting code in home.html

**Step 2**: Ensure greeting structure is:
```html
<div class="greeting-area">
  <h1 class="greeting-text">Good afternoon, {{ user.display_name }}!</h1>
  <p class="greeting-date">{{ current_date }}</p>
  <button class="help-trigger" aria-label="Show help">?</button>
</div>
```

**Step 3**: Add/update CSS for clean, minimal styling:
```css
.greeting-area {
  padding: 20px;
  text-align: center;
  /* or left-aligned if preferred */
}

.greeting-text {
  font-size: 1.5rem;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.greeting-date {
  font-size: 0.9rem;
  color: #7f8c8d;
}
```

### Acceptance Criteria - Phase 2

- [ ] Greeting displays cleanly
- [ ] Date/time visible
- [ ] No unnecessary decorations
- [ ] Help [?] icon positioned

---

## Phase 3: Relocate Example Prompts

### Approach: Help Tooltip/Modal

Move example prompts from permanent display to a help tooltip that appears when clicking [?].

### Implementation Steps

**Step 1**: Extract current example prompts from home.html

**Step 2**: Create help tooltip component:
```html
<div class="help-tooltip" id="help-tooltip" style="display: none;">
  <h3>Try asking Piper:</h3>
  <ul class="example-prompts">
    <li onclick="setExample(this)">What needs my attention today?</li>
    <li onclick="setExample(this)">Summarize my recent standup notes</li>
    <li onclick="setExample(this)">Help me prepare for my meeting with the design team</li>
  </ul>
</div>
```

**Step 3**: Add toggle JavaScript:
```javascript
function toggleHelp() {
  const tooltip = document.getElementById('help-tooltip');
  tooltip.style.display = tooltip.style.display === 'none' ? 'block' : 'none';
}
```

**Step 4**: Style the tooltip:
```css
.help-tooltip {
  position: absolute;
  right: 20px;
  top: 80px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 100;
  max-width: 300px;
}

.example-prompts li {
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
}

.example-prompts li:hover {
  background: #f5f5f5;
}
```

### Acceptance Criteria - Phase 3

- [ ] Example prompts removed from main page area
- [ ] Help [?] icon visible
- [ ] Clicking [?] shows example prompts
- [ ] Prompts can still be clicked to fill chat input

---

## Phase 4: Sidebar-Ready Layout

### Approach

Prepare the CSS layout to accommodate a future sidebar (~250-300px wide).

### Implementation Steps

**Step 1**: Update main layout structure:
```html
<div class="app-layout">
  <aside class="sidebar" id="sidebar" style="display: none;">
    <!-- Placeholder for #565 -->
  </aside>
  <main class="main-content">
    <div class="greeting-area">...</div>
    <div class="chat-container">...</div>
  </main>
</div>
```

**Step 2**: Add flexbox layout CSS:
```css
.app-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 280px;
  flex-shrink: 0;
  background: #f8f9fa;
  border-right: 1px solid #e0e0e0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0; /* Prevents flex overflow */
}
```

**Step 3**: Test with sidebar visible (temporarily):
```javascript
// Dev console test:
document.getElementById('sidebar').style.display = 'block';
```

### Acceptance Criteria - Phase 4

- [ ] Layout uses flexbox for sidebar + main
- [ ] Main content shrinks when sidebar shown
- [ ] No layout breaks at various widths
- [ ] Sidebar placeholder hidden by default

---

## Agent Deployment

**Single Agent Assignment**: Visual cleanup with sequential phases.

| Phase | Agent | Evidence Required |
|-------|-------|-------------------|
| 0 | Claude Code | Audit document |
| 1-4 | Claude Code | Before/after screenshots, code changes |
| Z | Claude Code | Manual verification, PM approval |

---

## Verification Gates

### Test Scope Requirements

- [ ] **Unit tests**: NOT APPLICABLE - Visual/CSS changes only, no testable logic
- [ ] **Integration tests**: NOT APPLICABLE - No backend changes
- [ ] **Wiring tests**: NOT APPLICABLE - No multi-layer data flow
- [ ] **Manual visual testing**: REQUIRED - Primary verification method

**Justification**: This is pure visual cleanup (HTML/CSS). The only testable behavior is the help tooltip toggle, which is simple enough for manual verification. No automated tests required.

### Verification Checkpoints

| Gate | Criteria | Method |
|------|----------|--------|
| Phase 1 complete | Hero removed, page loads | Manual browser check |
| Phase 2 complete | Greeting displays | Visual inspection |
| Phase 3 complete | Help tooltip works | Click test |
| Phase 4 complete | Sidebar layout ready | Dev console test |

---

## Phase Z: Final Verification

### Manual Testing Checklist

- [ ] Purple hero is gone
- [ ] Greeting displays correctly (personalized, date)
- [ ] Help [?] icon works
- [ ] Example prompts appear in tooltip
- [ ] Clicking prompt fills chat input
- [ ] Layout resizes with sidebar placeholder
- [ ] No visual regressions
- [ ] No console errors

### Evidence Required

```bash
# Before screenshot (take in Phase 0)
# After screenshot (take in Phase Z)

# Verify no JS errors
# Open browser console, check for errors
```

### Files Modified/Created

| File | Action |
|------|--------|
| `templates/home.html` | MODIFY (major) |
| `web/static/css/style.css` | MODIFY |
| `web/static/css/home.css` | CREATE (if needed) |

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Current state audit | ❌ | |
| Purple hero removed | ❌ | |
| Greeting area refined | ❌ | |
| Example prompts relocated | ❌ | |
| Sidebar-ready layout | ❌ | |
| Help tooltip working | ❌ | |
| Manual testing | ❌ | |

---

## STOP Conditions

- Removing hero breaks critical functionality
- Can't identify what buttons do → escalate to PM
- Example prompts are critical onboarding → PM decision needed
- Layout changes cause regressions elsewhere
- Existing JavaScript depends on removed elements

---

## Success Criteria (Issue Completion Requires)

- [ ] All acceptance criteria met (Phases 1-4)
- [ ] Evidence provided (before/after screenshots)
- [ ] Manual testing complete
- [ ] No regressions to existing functionality
- [ ] GitHub issue #566 fully updated with evidence
- [ ] PM approval received

---

## PM Approval Request Template

```markdown
@PM - Issue #566 complete and ready for review:
- Purple hero removed ✓
- Greeting area clean ✓
- Example prompts in help tooltip ✓
- Sidebar-ready layout ✓
- Before/after screenshots in issue ✓

Please review and close if satisfied.
```

---

## Notes

- Start with audit - understand before changing
- Take "before" screenshot immediately in Phase 0
- Comment out before deleting (reversible)
- The [?] help could use dialog.js pattern if available
- Sidebar is hidden by default; just need layout ready for #565

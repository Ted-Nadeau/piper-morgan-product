# Gameplan: #550 FTUX-CHAT-BRIDGE - Add 'Ask Piper' button to empty states

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/550
**Created**: 2026-01-07
**Approach**: Option (a) - Simple JavaScript query param handling (PM approved)

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### STOP! Complete This Section WITH PM Before Proceeding

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] CLI structure: N/A (frontend-only work)
- [x] Database: N/A (no persistence needed)
- [x] Testing framework: N/A (manual UI verification)
- [x] Existing endpoints: N/A (no API calls - client-side navigation only)
- [x] Missing features: JavaScript query param handler on home.html

**My understanding of the task**:
- I believe we need to: Add "Ask Piper →" button to empty states that navigates to home with chat focused
- I think this involves: JS handler on home.html + HTML changes to 4 template files
- I assume the current state is: Empty states exist but lack actionable CTA

**Feature-Specific Infrastructure**:
- [x] Templates: Jinja2 server-rendered HTML
- [x] Empty state component: `templates/components/empty-state.html` (already supports CTA)
- [x] Home page chat: `templates/home.html` with `.chat-input` class (line 961)
- [x] Query param pattern: Already used in OAuth flows (URLSearchParams)

**Empty states to update**:
1. `templates/todos.html` - "No todos yet" (line 138)
2. `templates/projects.html` - "No projects set up yet" (line 108)
3. `templates/files.html` - "No documents in your knowledge base yet" (line 203)
4. `templates/lists.html` - "No lists yet" (line 138)

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?** (Check all that apply)

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [ ] **USE WORKTREE** - 2+ parallel criteria checked
- [x] **SKIP WORKTREE** - Overhead criteria dominate
- [ ] **PM DECISION** - Mixed signals, escalate

**Rationale**: Single agent, 5 files, ~30 min estimate - worktree overhead exceeds benefit

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   # Verified:
   ls templates/{home,todos,projects,files,lists}.html  # All exist
   ls templates/components/empty-state.html             # Exists, has CTA support
   ```

2. **Recent work in this area?**
   - Last changes to this feature: #548 FTUX empty states (2026-01-06)
   - Known issues/quirks: None identified
   - Previous attempts: None

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [x] Add to existing application
   - [ ] Fix broken functionality
   - [ ] Refactor existing code
   - [ ] Other: ____________

4. **Critical context I'm missing?**
   - ____________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

---

## Phase 0.5: Frontend-Backend Contract Verification

### Applicability Check
- [ ] Creating new API endpoints + UI that calls them → **NO**
- [ ] Modifying existing API paths → **NO**
- [ ] Adding JavaScript that makes fetch() calls → **NO** (navigation via href, not fetch)
- [x] Frontend-only styling/navigation changes → **YES**

**Decision**: **SKIP** - This is frontend-only work (HTML links + JS focus handler).
No backend routes, no fetch() calls, no API contracts to verify.

---

## Phase 0: Initial Bookending

### GitHub Issue
Already created: #550

### Acceptance Criteria (from issue)
- [ ] Empty states have "Ask Piper →" button
- [ ] Button navigates to home page
- [ ] Chat input receives focus on arrival
- [ ] Works on: Todos, Projects, Files, Lists

---

## Phase 1: Add Focus Handler to Home Page

**Target**: `templates/home.html`

Add JavaScript to check for `?focus=chat` query param and focus the chat input.

```javascript
// Add to DOMContentLoaded handler or create new one
function checkChatFocusParam() {
  const params = new URLSearchParams(window.location.search);
  if (params.get('focus') === 'chat') {
    const chatInput = document.querySelector('.chat-input');
    if (chatInput) {
      chatInput.focus();
      // Clean up URL (remove param without reload)
      window.history.replaceState({}, '', window.location.pathname);
    }
  }
}

// Call on page load
checkChatFocusParam();
```

**Evidence needed**: Navigate to `/?focus=chat` and verify chat input has focus.

---

## Phase 2: Update Empty States

### 2a: Todos Empty State (`templates/todos.html`)

**Current** (line 141):
```html
<p class="empty-state-message">Say "add a todo: [your task]" to create one, or I can suggest some based on your open GitHub issues.</p>
```

**Updated**:
```html
<p class="empty-state-message">Say "add a todo: [your task]" to create one, or I can suggest some based on your open GitHub issues.</p>
<a href="/?focus=chat" class="btn btn-primary empty-state-cta">Ask Piper →</a>
```

### 2b: Projects Empty State (`templates/projects.html`)

**Current** (line 111):
```html
<p class="empty-state-message">Projects help me understand your work context. Say "create a project called..." to get started.</p>
```

**Updated**:
```html
<p class="empty-state-message">Projects help me understand your work context. Say "create a project called..." to get started.</p>
<a href="/?focus=chat" class="btn btn-primary empty-state-cta">Ask Piper →</a>
```

### 2c: Files Empty State (`templates/files.html`)

**Current** (line 206):
```html
<p class="empty-state-message">You can upload files, connect Notion, or just paste content into our chat—I'll remember it for later.</p>
```

**Updated**:
```html
<p class="empty-state-message">You can upload files, connect Notion, or just paste content into our chat—I'll remember it for later.</p>
<a href="/?focus=chat" class="btn btn-primary empty-state-cta">Ask Piper →</a>
```

### 2d: Lists Empty State (`templates/lists.html`)

**Current** (line 141):
```html
<p class="empty-state-message">Say "create a list called..." to get started. Lists help you group and organize related items.</p>
```

**Updated**:
```html
<p class="empty-state-message">Say "create a list called..." to get started. Lists help you group and organize related items.</p>
<a href="/?focus=chat" class="btn btn-primary empty-state-cta">Ask Piper →</a>
```

**Evidence needed**: Screenshot or manual verification of each page showing the button.

---

## Phase 3: Verify Existing CTA Styling

Check that `.btn`, `.btn-primary`, and `.empty-state-cta` classes are styled appropriately. The shared component already uses these classes, so they should exist.

```bash
grep -n "empty-state-cta\|\.btn-primary" templates/components/empty-state.html web/static/css/*.css
```

If styles missing, add minimal CSS to match design system.

---

## Phase Z: Final Bookending & Handoff

### Purpose
Complete final verification, update all documentation, prepare for PM approval

### Required Actions

#### 1. Manual Testing Checklist
- [ ] Navigate to `/?focus=chat` - verify chat input receives focus
- [ ] Navigate to `/todos` with no todos - see "Ask Piper →" button
- [ ] Click button → navigates to home with chat focused
- [ ] Repeat for `/projects`, `/files`, `/lists`
- [ ] Verify button styling matches design system (no broken CSS)
- [ ] Verify URL is cleaned up after focus (no `?focus=chat` remaining)

#### 2. Evidence Compilation
- [ ] Screenshot or description of each empty state with button
- [ ] Verification that focus behavior works
- [ ] List of files modified with line numbers
- [ ] Commit hash

#### 3. GitHub Final Update
```bash
gh issue edit 550 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Manual testing: [evidence]
- [x] No regressions: Navigation and chat still work
- [x] Files modified: [list]

### Ready for PM Review
"
```

#### 4. Documentation Updates
- [ ] N/A - No ADRs needed for simple UI enhancement
- [ ] N/A - No architecture changes

#### 5. PM Approval Request
```markdown
@PM - Issue #550 complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided ✓
- No regressions confirmed ✓

Please review and close if satisfied.
```

### CRITICAL: Agent Does NOT Close Issue
**Only PM closes issues after review and approval**

---

## Files to Modify

1. `templates/home.html` - Add query param handler (~10 lines JS)
2. `templates/todos.html` - Add CTA button (~1 line)
3. `templates/projects.html` - Add CTA button (~1 line)
4. `templates/files.html` - Add CTA button (~1 line)
5. `templates/lists.html` - Add CTA button (~1 line)

**Estimated effort**: ~30 minutes

---

## Risk Assessment

**Low risk**:
- No backend changes needed
- No database changes
- No new dependencies
- Follows existing patterns (URLSearchParams, empty-state component)

**Potential issues**:
- CSS styling may need minor adjustment for button appearance
- URL history management (using replaceState to clean up URL)

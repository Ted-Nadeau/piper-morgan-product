# Gameplan #554: STANDUP-CHAT-WIDGET - Floating Chat Widget Component

**Issue**: #554
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Created**: 2026-01-08
**Author**: Lead Developer (Claude Code Opus)

---

## Phase -1: Infrastructure Verification Checkpoint ✅ COMPLETE

### Part A: Current Understanding (Verified 2026-01-08)

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Templates: Jinja2 with `templates/` directory
- [x] Static files: `web/static/` served at `/static/`
- [x] Testing: pytest (confirmed)
- [x] Existing endpoint: `POST /api/v1/intent` (verified)
- [x] Missing: Modular chat component (inline in home.html)

**Task Understanding**:
- Extract inline chat UI from `templates/home.html` into reusable component
- Add floating widget positioning
- Include on all pages with session persistence
- NO backend changes needed (#552, #553 complete)

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [x] Task duration >30 minutes (est. 1.5-2 days)
- [ ] Multiple agents in parallel on different files - partial (sequential phases)
- [x] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits (extraction must be atomic)

**Assessment**: **SKIP WORKTREE**
- Rationale: Files are tightly coupled (CSS/JS/HTML must stay synchronized during extraction). Atomic commits preferred. Risk mitigation through careful testing, not branching.

### Part B: PM Verification ✅

PM confirmed (2026-01-08 10:16 AM):
1. Path C (floating widget) selected
2. HTTP polling acceptable for MVP
3. WebSockets deferred to #557
4. Visible in corner, no custom pages

### Part C: Proceed Decision

- [x] **PROCEED** - Understanding verified, gameplan appropriate

---

## Phase 0: Initial Bookending ✅ COMPLETE

### GitHub Issue Verification
```bash
gh issue view 554  # Verified, updated with Phase -1 findings
```

### Codebase Investigation (Complete)

| Asset | Location | Lines | Status |
|-------|----------|-------|--------|
| Chat HTML | `templates/home.html:957-966` | 10 | To extract |
| Chat CSS | `templates/home.html:45-106` | 62 | To extract |
| Chat JS | `templates/home.html:1068-1392` | 324 | To extract |
| Bot Renderer | `web/assets/bot-message-renderer.js` | 519 | Already modular ✅ |

### API Endpoint Verification
- `POST /api/v1/intent` - accepts `{message, session_id}`, returns response
- Mount: `/api/v1` prefix in `web/app.py`
- Full path: `/api/v1/intent`

---

## Phase 0.5: Frontend-Backend Contract Verification

### When to Apply
- ✅ Adding JavaScript that makes fetch() calls
- ❌ NOT creating new API endpoints (using existing)

### Contract Verification

| Endpoint | Full Path | Verified |
|----------|-----------|----------|
| Intent | `/api/v1/intent` | ✅ (existing, working) |

### Static File Verification

```bash
# Static files served from web/static/ at /static/
grep -n "StaticFiles" web/app.py
# Verified: web/static → /static/
```

**Files to create**:
- `web/static/css/chat.css` → `/static/css/chat.css`
- `web/static/js/chat.js` → `/static/js/chat.js`
- `templates/components/chat-widget.html` → `{% include 'components/chat-widget.html' %}`

---

## Multi-Agent Deployment Strategy

### Assessment

| Factor | Value | Implication |
|--------|-------|-------------|
| Complexity | Medium | Not trivial, benefits from oversight |
| Parallelization | Limited | Sequential dependencies between phases |
| Risk | Medium | Must not break home.html |
| Model fit | Haiku for extraction | CSS/JS extraction is mechanical |

### Deployment Plan

| Phase | Agent | Model | Rationale |
|-------|-------|-------|-----------|
| 1 | Subagent | Haiku | CSS/JS extraction is straightforward |
| 2 | Subagent | Haiku | Floating positioning is CSS-focused |
| 3 | Lead Dev | Opus | Session persistence has edge cases |
| 4 | Subagent | Haiku | Template includes are mechanical |
| 5 | Lead Dev | Opus | Mobile responsiveness needs judgment |
| 6 | Subagent | Haiku | Test creation follows patterns |
| Z | Lead Dev | Opus | Final verification and handoff |

**Coordination**: Lead Dev (me) deploys subagents via Task tool, collects evidence, maintains oversight. Subagents report back with evidence; Lead Dev validates before proceeding.

**Prompt Revision at Phase Boundaries**: Before deploying each subsequent phase, Lead Dev reviews the previous phase's handoff and updates the next prompt if:
- File names/paths differ from expected
- Function names or APIs changed
- Structure differs from template assumptions
- New dependencies or edge cases discovered

This ensures later prompts always match the actual state of the codebase.

---

## Phase 1: Extract Chat Component

**Deploy**: Haiku Subagent

### Objective
Create modular, reusable chat files from home.html inline code.

### Agent Prompt
```markdown
## Task: Extract Chat Component from home.html

**Issue**: #554 Phase 1
**Goal**: Create standalone chat CSS/JS files and Jinja2 component

### Files to Create

1. **`web/static/css/chat.css`**
   - Extract CSS from `templates/home.html` lines 45-106
   - All `.chat-*` classes
   - All `#chat-window` styles
   - Message styling (`.user-message`, `.bot-message`)

2. **`web/static/js/chat.js`**
   - Extract JS from `templates/home.html` lines 1068-1392
   - Key functions: appendMessage, form submit handler
   - Dependencies: API_BASE_URL, sessionId, marked.js
   - Export as module or IIFE

3. **`templates/components/chat-widget.html`**
   - Extract HTML from `templates/home.html` lines 957-966
   - Make it includable: `{% include 'components/chat-widget.html' %}`
   - Include CSS/JS links

### Verification Required

After extraction:
1. Update `templates/home.html` to use the new component
2. Test that home page still works:
   - Chat form submits
   - Messages appear
   - Responses render with markdown
3. Run: `python main.py` and manually verify

### Evidence to Provide
- List of files created with line counts
- Screenshot or curl output showing home chat works
- Any issues encountered

### STOP Conditions
- If home.html breaks → stop and report
- If extraction unclear → ask before proceeding
```

### Acceptance Criteria (Phase 1)
- [ ] `web/static/css/chat.css` created
- [ ] `web/static/js/chat.js` created
- [ ] `templates/components/chat-widget.html` created
- [ ] `templates/home.html` updated to use component
- [ ] Home page chat still functional (manual verification)

### Evidence Required
- File list with line counts
- Manual test: send message on home page, receive response

### Progressive Bookending
After completion:
```bash
gh issue comment 554 -b "✓ Phase 1 complete: Chat component extracted
Evidence: 3 files created (chat.css, chat.js, chat-widget.html)
Home page verified working
Next: Phase 2 (floating positioning)"
```

### Handoff Quality Checklist
- [ ] Acceptance criteria checkboxes addressed
- [ ] Evidence provided (not just "done")
- [ ] Files modified listed with line counts
- [ ] Manual verification documented
- [ ] Blockers explicitly stated (if any)

---

## Phase 2: Floating Widget Styling

**Deploy**: Haiku Subagent (after Phase 1 complete)

### Objective
Position chat as floating corner widget with expand/collapse.

### Agent Prompt
```markdown
## Task: Add Floating Widget Positioning

**Issue**: #554 Phase 2
**Depends On**: Phase 1 complete

### Changes to Make

1. **Update `web/static/css/chat.css`**
   Add floating widget styles:
   ```css
   .chat-widget-container {
     position: fixed;
     bottom: 20px;
     right: 20px;
     z-index: 1000;
     /* Collapsed state */
   }

   .chat-widget-container.expanded {
     /* Expanded state */
     width: 380px;
     height: 500px;
   }

   .chat-widget-toggle {
     /* Floating button */
   }
   ```

2. **Update `web/static/js/chat.js`**
   Add toggle functionality:
   ```javascript
   function toggleChatWidget() {
     const container = document.querySelector('.chat-widget-container');
     container.classList.toggle('expanded');
   }
   ```

3. **Update `templates/components/chat-widget.html`**
   - Wrap in `.chat-widget-container`
   - Add toggle button
   - Default to collapsed state

### Verification Required
1. Widget appears in bottom-right corner
2. Clicking toggle expands/collapses smoothly
3. Widget floats above page content
4. No visual conflicts with existing modals/toasts

### Evidence to Provide
- CSS changes summary
- Manual test: toggle works, positioning correct
```

### Acceptance Criteria (Phase 2)
- [ ] Widget positioned bottom-right corner
- [ ] Expand/collapse toggle works
- [ ] Smooth animations
- [ ] Z-index handles modals/toasts correctly

### Evidence Required
- Before/after description
- Manual toggle test

### Progressive Bookending
After completion:
```bash
gh issue comment 554 -b "✓ Phase 2 complete: Floating widget positioning
Evidence: Widget in bottom-right, toggle works
Z-index verified against modals
Next: Phase 3 (session persistence)"
```

---

## Phase 3: Session Persistence

**Deploy**: Lead Dev (Opus) - handles edge cases

### Objective
Maintain conversation across page navigation.

### Implementation Approach

1. **Store session_id in localStorage**
   ```javascript
   // In chat.js
   const SESSION_KEY = 'piper_chat_session';

   function getOrCreateSessionId() {
     let sessionId = localStorage.getItem(SESSION_KEY);
     if (!sessionId) {
       sessionId = crypto.randomUUID();
       localStorage.setItem(SESSION_KEY, sessionId);
     }
     return sessionId;
   }
   ```

2. **Optional: Store chat history**
   ```javascript
   const HISTORY_KEY = 'piper_chat_history';

   function saveChatHistory(messages) {
     localStorage.setItem(HISTORY_KEY, JSON.stringify(messages));
   }

   function loadChatHistory() {
     const stored = localStorage.getItem(HISTORY_KEY);
     return stored ? JSON.parse(stored) : [];
   }
   ```

3. **Restore state on page load**
   ```javascript
   document.addEventListener('DOMContentLoaded', () => {
     const history = loadChatHistory();
     history.forEach(msg => appendMessage(msg.html, msg.isUser));
   });
   ```

4. **Handle session expiry**
   - Consider TTL for stored history (24h?)
   - Clear on explicit logout

### Edge Cases to Handle
- localStorage unavailable (private browsing)
- Corrupted storage data
- Conflict with auth session
- Storage quota exceeded

### Acceptance Criteria (Phase 3)
- [ ] Session ID persists in localStorage
- [ ] Chat history restored on page load
- [ ] Works in private browsing (graceful degradation)
- [ ] No conflicts with auth system

### Evidence Required
- Test: Start conversation, navigate away, return - history preserved
- Test: Private browsing mode - no errors

### Progressive Bookending
After completion:
```bash
gh issue comment 554 -b "✓ Phase 3 complete: Session persistence
Evidence: localStorage session verified
Cross-page navigation tested
Private browsing graceful degradation confirmed
Next: Phase 4 (site-wide integration)"
```

---

## Phase 4: Site-Wide Integration

**Deploy**: Haiku Subagent

### Objective
Include widget on all pages.

### Agent Prompt
```markdown
## Task: Include Chat Widget on All Pages

**Issue**: #554 Phase 4
**Depends On**: Phases 1-3 complete

### Approach Options

**Option A: Add to navigation component**
If `templates/components/navigation.html` is included on all pages:
- Add widget include at end of navigation.html

**Option B: Add to base template**
If there's a base template all pages extend:
- Add widget include to base

**Option C: Add to each page individually**
If no common base:
- Add to: home.html, standup.html, todos.html, lists.html, projects.html, files.html, settings pages

### Investigation Required
1. Check which approach is feasible:
   ```bash
   grep -l "navigation.html" templates/*.html
   grep -l "extends" templates/*.html
   ```

2. Verify CSS/JS loaded on all pages
   - Check if there's a common `<head>` include
   - Or add links to each page

### Changes to Make
Based on investigation, implement the cleanest approach.

### Verification Required
Test widget appears on:
- [ ] /home
- [ ] /standup
- [ ] /todos
- [ ] /lists
- [ ] /projects
- [ ] /files
- [ ] /settings (all settings pages)

### Evidence to Provide
- Approach chosen and why
- List of files modified
- Manual verification on 3+ pages
```

### Acceptance Criteria (Phase 4)
- [ ] Widget visible on all main pages
- [ ] CSS/JS loaded correctly everywhere
- [ ] No layout regressions
- [ ] Session persists across page navigation

### Evidence Required
- Approach documented
- Manual test on home, todos, standup pages

### Progressive Bookending
After completion:
```bash
gh issue comment 554 -b "✓ Phase 4 complete: Site-wide integration
Evidence: Widget on all 7 pages
Approach: [navigation.html / base template / individual]
Session persists across navigation
Next: Phase 5 (mobile responsiveness)"
```

---

## Phase 5: Mobile Responsiveness

**Deploy**: Lead Dev (Opus) - judgment calls needed

### Objective
Usable experience on mobile devices.

### Implementation Approach

1. **Full-screen on mobile**
   ```css
   @media (max-width: 768px) {
     .chat-widget-container.expanded {
       position: fixed;
       top: 0;
       left: 0;
       right: 0;
       bottom: 0;
       width: 100%;
       height: 100%;
       border-radius: 0;
     }
   }
   ```

2. **Touch-friendly toggle**
   - Larger touch target (44x44px minimum)
   - Clear close button when expanded

3. **Keyboard handling**
   - Input stays above virtual keyboard
   - Test with `visualViewport` API if needed

### Testing Strategy
- Chrome DevTools mobile emulation
- Real device if available (iOS Safari, Android Chrome)

### Acceptance Criteria (Phase 5)
- [ ] Widget usable on mobile viewport (<768px)
- [ ] Full-screen when expanded on mobile
- [ ] Virtual keyboard doesn't obscure input
- [ ] Close button accessible

### Evidence Required
- Mobile viewport screenshot (DevTools)
- Description of mobile behavior

### Progressive Bookending
After completion:
```bash
gh issue comment 554 -b "✓ Phase 5 complete: Mobile responsiveness
Evidence: DevTools mobile screenshot
Full-screen expand on <768px
Close button accessible
Next: Phase 6 (tests)"
```

---

## Phase 6: Tests

**Deploy**: Haiku Subagent

### Objective
Create unit tests for chat.js functions.

### Agent Prompt
```markdown
## Task: Create Chat Widget Tests

**Issue**: #554 Phase 6

### Tests to Create

**File**: `tests/unit/web/static/test_chat_widget.py`

Or if using JS testing:
**File**: `web/static/js/chat.test.js` (with Jest or similar)

### Test Cases

1. **Session Management**
   - getOrCreateSessionId returns consistent ID
   - New session created if none exists
   - Handles localStorage unavailable

2. **Chat History**
   - saveChatHistory stores correctly
   - loadChatHistory retrieves correctly
   - Handles corrupted data gracefully

3. **Toggle Functionality**
   - toggleChatWidget adds/removes expanded class
   - Widget starts collapsed

4. **Message Handling**
   - appendMessage adds to DOM correctly
   - User messages styled correctly
   - Bot messages styled correctly

### Evidence to Provide
- Test file created with test count
- All tests passing
- Coverage of key functions
```

### Acceptance Criteria (Phase 6)
- [ ] Unit tests for session management
- [ ] Unit tests for toggle functionality
- [ ] All tests passing
- [ ] Test output provided

### Evidence Required
- Test file location
- pytest/test output showing passes

### Progressive Bookending
After completion:
```bash
gh issue comment 554 -b "✓ Phase 6 complete: Tests created
Evidence: X tests in [location]
All tests passing (output below)
Next: Phase Z (final verification)"
```

---

## Phase Z: Final Bookending & Handoff

**Deploy**: Lead Dev (Opus)

### Final Verification Checklist

- [ ] All Phase 1-6 acceptance criteria met
- [ ] Evidence collected for each phase
- [ ] No regressions on home.html
- [ ] Widget works on all pages
- [ ] Mobile experience acceptable
- [ ] Tests passing

### GitHub Issue Update

```bash
gh issue edit 554 --body "[Updated body with evidence]"
gh issue comment 554 -b "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] Phase 1: CSS/JS/HTML extracted - [files list]
- [x] Phase 2: Floating positioning - [verified]
- [x] Phase 3: Session persistence - [tested]
- [x] Phase 4: Site-wide integration - [pages list]
- [x] Phase 5: Mobile responsive - [screenshot]
- [x] Phase 6: Tests passing - [output]

### Verification
- Manual test: Start conversation on /home, navigate to /todos, conversation preserved
- No regressions: home.html chat still works
- Mobile: Tested in Chrome DevTools

### Ready for PM Review
"
```

### Documentation Updates
- [ ] No ADR needed (no architectural decisions)
- [ ] No architecture.md changes (frontend only)
- [ ] Remove/update TODO comments if any added
- [ ] Session log complete

### Evidence Compilation
- [ ] All terminal outputs in session log
- [ ] Before/after behavior documented
- [ ] Screenshots for mobile (Phase 5)
- [ ] Test output pasted (Phase 6)
- [ ] Commit hashes recorded

### Session Log Update
- Document all phase completions
- Note any discoveries or issues
- Update omnibus log if significant

### PM Approval Request
```markdown
@PM - Issue #554 complete and ready for review:
- All 6 phases complete with evidence ✓
- Widget visible on all pages ✓
- Session persistence working ✓
- Mobile responsive ✓
- Tests passing ✓
- No regressions ✓

Please review and close if satisfied.
```

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- [ ] Home.html breaks after extraction
- [ ] `/api/v1/intent` behaves unexpectedly
- [ ] Session conflicts with auth system
- [ ] Mobile layout severely broken
- [ ] Tests fail for any reason
- [ ] Security concern (XSS, injection)

**When stopped**: Document issue, provide options, wait for PM decision.

---

## Verification Gates

| Gate | Requirement | Blocking |
|------|-------------|----------|
| Post-Phase 1 | Home chat still works | Yes |
| Post-Phase 2 | Toggle works, no z-index issues | Yes |
| Post-Phase 3 | Session persists across navigation | Yes |
| Post-Phase 4 | Widget on all pages | Yes |
| Post-Phase 5 | Mobile usable | No (acceptable degradation OK) |
| Post-Phase 6 | Tests pass | Yes |

---

## Success Criteria

### Issue Completion Requires
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Tests passing (with output)
- [ ] No regressions introduced
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Timeline Estimate

| Phase | Effort | Cumulative |
|-------|--------|------------|
| Phase 1 | 3-4 hours | 3-4 hours |
| Phase 2 | 2-3 hours | 5-7 hours |
| Phase 3 | 2-3 hours | 7-10 hours |
| Phase 4 | 1-2 hours | 8-12 hours |
| Phase 5 | 2-3 hours | 10-15 hours |
| Phase 6 | 2 hours | 12-17 hours |
| Phase Z | 30 min | ~1.5-2 days |

---

*Gameplan created: 2026-01-08*
*Template version: v9.2*

# Gameplan: Issue #592 - Markdown Rendering Regression

**Issue**: [#592](https://github.com/mediajunkie/piper-morgan-product/issues/592)
**Type**: Bug Fix (P1)
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Frontend: Server-rendered Jinja2 templates + vanilla JavaScript
- [x] Chat widget: `templates/home.html` with `appendMessage()` function
- [x] Static files: `web/static/js/` and `web/static/css/`
- [x] Testing framework: pytest

**My understanding of the task**:
- I believe we need to: Add markdown rendering to chat message display
- I think this involves: Finding where `appendMessage()` inserts content and adding a markdown→HTML conversion step
- I assume the current state is: Messages are inserted as plain text without markdown processing

**Potential approaches**:
1. Use existing markdown library if already in project
2. Add `marked.js` or similar lightweight markdown renderer
3. Use server-side rendering (return HTML instead of markdown)

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes
- [ ] Multi-component work
- [ ] Exploratory/risky changes

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<15 min estimated)
- [x] Tightly coupled files (just home.html likely)
- [ ] Time-critical work

**Assessment**:
- [x] **SKIP WORKTREE** - Single file fix, focused scope, <30 min estimate

### Part B: PM Verification Required

**PM, please confirm**:

1. **What actually exists?**
   ```bash
   grep -r "marked\|markdown" web/static/js/ templates/
   grep -n "appendMessage" templates/home.html
   ```

2. **Was markdown working before?**
   - Last time markdown rendered correctly: ____________
   - Recent changes that might have broken it: ____________

3. **Preferred approach?**
   - [ ] Client-side rendering (marked.js or similar)
   - [ ] Server-side rendering (return HTML from API)
   - [ ] Other: ____________

4. **Security requirements?**
   - [ ] Must sanitize HTML (XSS prevention)
   - [ ] Specific library preference: ____________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding correct
- [ ] **REVISE** - Need different approach
- [ ] **CLARIFY** - Need more context on: ____________

---

## Phase 0: Investigation

### Purpose
Understand current message rendering flow and identify where markdown conversion should occur.

### Required Actions

1. **Locate message rendering code**
   ```bash
   grep -n "appendMessage\|innerHTML\|textContent" templates/home.html
   ```

2. **Check for existing markdown libraries**
   ```bash
   grep -r "marked\|showdown\|markdown" web/static/ templates/ package.json requirements.txt
   ```

3. **Trace message flow**
   - API returns markdown string
   - JavaScript receives response
   - `appendMessage()` inserts into DOM
   - Identify exact insertion point

4. **Check if regression or never implemented**
   ```bash
   git log --oneline -20 -- templates/home.html
   git log --grep="markdown" --oneline
   ```

### STOP Conditions
- If markdown was never implemented → this is a feature, not a bug fix
- If server should return HTML → different approach needed

---

## Phase 0.5: Frontend-Backend Contract Verification

### Purpose
Verify API response format and frontend expectations align.

### Required Actions

1. **Check API response format**
   ```bash
   curl -s -X POST "http://localhost:8001/api/v1/intent" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is on my calendar today?", "session_id": "test"}' | jq '.message'
   ```
   - Confirm response is markdown string (not HTML)

2. **Verify frontend expectations**
   - Does `appendMessage()` expect plain text, markdown, or HTML?
   - Is there a conversion step that's missing or broken?

---

## Phase 1: Implementation

### Approach
Add client-side markdown rendering using lightweight library.

### Tasks

1. **Add markdown library** (if not present)
   - Option A: CDN link in template
   - Option B: Local copy in `web/static/js/`
   - Recommended: `marked.js` (lightweight, well-maintained)

2. **Modify `appendMessage()` function**
   ```javascript
   // Before (plain text):
   messageEl.textContent = message;

   // After (markdown rendered):
   messageEl.innerHTML = DOMPurify.sanitize(marked.parse(message));
   ```

3. **Add XSS protection**
   - Use DOMPurify or similar to sanitize HTML output
   - Never use `innerHTML` with unsanitized content

4. **Test rendering**
   - Bold: `**text**` → **text**
   - Bullets: `- item` → • item
   - Code: `` `code` `` → `code`
   - Headers: `## heading` → styled heading

### Files to Modify

| File | Change |
|------|--------|
| `templates/home.html` | Add markdown library, modify `appendMessage()` |
| `web/static/js/` | Add marked.js and DOMPurify if using local files |

---

## Phase 2: Testing & Verification

### Unit Tests
- [ ] Markdown library loads without errors
- [ ] `appendMessage()` renders markdown correctly

### Manual Verification
- [ ] "What's on my calendar today?" shows formatted response
- [ ] Bold text appears bold
- [ ] Bullet points display correctly
- [ ] Code blocks render with monospace
- [ ] No XSS vulnerabilities (test with `<script>alert(1)</script>`)

### Regression Tests
- [ ] Plain text messages still display correctly
- [ ] User messages (non-markdown) display correctly
- [ ] Long messages don't break layout

---

## Phase Z: Completion

### Acceptance Criteria (from #592)

- [ ] Markdown responses render as formatted HTML
- [ ] Bold text appears bold
- [ ] Bullet lists display with proper styling
- [ ] Code blocks render with monospace formatting
- [ ] No XSS vulnerabilities from markdown rendering
- [ ] Regression test added to prevent future breaks

### Evidence Required

1. **Screenshot**: Before/after of calendar response
2. **XSS test**: Attempt `<script>` injection, show it's sanitized
3. **Test output**: Any automated tests added

### Documentation Updates
- [ ] Update ALPHA_TESTING_GUIDE.md if needed
- [ ] Note in release notes for next version

---

## STOP Conditions

Stop and escalate if:
- [ ] Markdown was never working (feature, not bug)
- [ ] Server-side rendering preferred (different approach)
- [ ] XSS sanitization library unavailable
- [ ] `appendMessage()` architecture incompatible

---

## Multi-Agent Deployment

**Recommendation**: Single agent sufficient

**Rationale**:
- Focused frontend-only fix
- Single file modification likely
- Clear acceptance criteria
- <30 min estimated duration

---

## Estimated Effort

| Phase | Estimate |
|-------|----------|
| Phase -1 | 5 min (PM verification) |
| Phase 0 | 10 min (investigation) |
| Phase 1 | 15-20 min (implementation) |
| Phase 2 | 10 min (testing) |
| Phase Z | 5 min (documentation) |
| **Total** | **45-50 min** |

---

*Gameplan created: 2026-01-14*
*Template: v9.3*

# Gameplan: Issue #574 - Conversation History Switch Bug

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/574
**Type**: Bug Fix (E2E)
**Template Version**: v9.3
**Created**: 2026-01-12
**Status**: Awaiting PM Verification (Phase -1)

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

Based on available context, I believe:

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Frontend: Server-rendered HTML (Jinja2) with vanilla JavaScript
- [x] Database: PostgreSQL on port 5433
- [x] Testing framework: pytest
- [x] Existing endpoints: `/api/conversation/list`, `/api/conversation/{id}` (likely)
- [x] Conversation sidebar: Implemented in #565

**My understanding of the task**:
- I believe we need to: Fix the click handler for conversation items in the sidebar
- I think this involves: JavaScript event handling and/or API call logic in `templates/index.html`
- I assume the current state is: Sidebar renders conversations but clicking doesn't switch the view

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<15 min expected once root cause found)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [ ] **USE WORKTREE** - 2+ parallel criteria checked
- [x] **SKIP WORKTREE** - Overhead criteria dominate
- [ ] **PM DECISION** - Mixed signals, escalate

**Rationale**: Single agent, likely single file fix (templates/index.html), estimated <1 hour total.

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   ls -la templates/index.html
   grep -n "conversation" templates/index.html | head -20
   grep -n "sidebar" templates/index.html | head -10
   ```

2. **Recent work in this area?**
   - Last changes to this feature: #565 (Conversation History Sidebar)
   - Known issues/quirks: ____________
   - Previous attempts: ____________

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [ ] Add to existing application
   - [x] Fix broken functionality
   - [ ] Refactor existing code
   - [ ] Other: ____________

4. **Critical context I'm missing?**
   - ____________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

**If REVISE or CLARIFY checked, STOP and create new gameplan**

---

## Phase 0: Initial Bookending - GitHub Investigation

### Purpose
Establish context, verify issue exists, reproduce bug, gather evidence

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 574
   ```

2. **Codebase Investigation**
   ```bash
   # Find conversation-related code in templates
   grep -n "conversation" templates/index.html | head -30

   # Find click handlers
   grep -n "onclick\|addEventListener\|click" templates/index.html | head -20

   # Check conversation API routes
   grep -n "conversation" web/api/routes/*.py

   # Check git history for #565
   git log --grep="565" --oneline
   ```

3. **Reproduce the Bug**
   - Start server: `python main.py`
   - Log in at http://localhost:8001
   - Navigate to have 2+ conversations visible
   - Click on different conversation in sidebar
   - Document exact behavior

4. **Update GitHub Issue**
   ```bash
   gh issue edit 574 --body "[Updated with Investigation Started status]"
   ```

### Evidence to Capture
- [ ] Screenshot: Sidebar with multiple conversations
- [ ] Screenshot: Failure behavior when clicking
- [ ] Browser console errors (if any)
- [ ] Network tab: API calls made/not made
- [ ] Backend logs: Errors on load attempt

### STOP Conditions
- Issue doesn't exist or is wrong number
- Feature already fixed
- Different problem than described
- Cannot reproduce bug

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY)

### Purpose
Verify the conversation load endpoint exists and works before debugging frontend

### Required Actions

#### 1. Find Backend Endpoints
```bash
# Get conversation-related endpoints
grep -n "@router\." web/api/routes/conversation.py

# Get the mount prefix
grep -n "include_router\|conversation" web/app.py
```

#### 2. Calculate Full Paths
| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| list | /list | /api/conversation (TBD) | /api/conversation/list |
| load | /{id} | /api/conversation (TBD) | /api/conversation/{id} |

#### 3. Verify Paths Work (Server Running)
```bash
# Test list endpoint (requires auth token)
curl -s -H "Authorization: Bearer [token]" http://localhost:8001/api/conversation/list

# Test load endpoint with a known conversation ID
curl -s -H "Authorization: Bearer [token]" http://localhost:8001/api/conversation/[id]
```

#### 4. Verify Frontend Uses Correct Paths
```bash
# Find fetch calls for conversations
grep -n "fetch.*conversation" templates/index.html
```

### Evidence Required
```markdown
Verified paths:
  /api/conversation/list → HTTP [status]
  /api/conversation/{id} → HTTP [status]
  Frontend fetch path: [path found in code]
  Match: [yes/no]
```

### STOP Conditions
- If ANY endpoint returns 404 → backend bug, not frontend
- If paths don't match → that's the bug
- If mount prefix unclear → verify in app.py

---

## Phase 1: Root Cause Investigation

### 1.1 Click Handler Analysis

Examine the click handler for conversation items:

```bash
# Find where click handler is defined
grep -n -A5 "conversation.*click\|loadConversation\|selectConversation" templates/index.html
```

**Key Questions**:
| Question | Finding |
|----------|---------|
| Is click event firing? | [ ] Yes [ ] No |
| Is correct function called? | [ ] Yes [ ] No |
| Is conversation ID passed? | [ ] Yes [ ] No |
| Is API call made? | [ ] Yes [ ] No |
| Is API returning data? | [ ] Yes [ ] No |
| Is UI update executing? | [ ] Yes [ ] No |

### 1.2 Browser Debugging

Using browser DevTools:
1. Add breakpoint on click handler
2. Click conversation item
3. Step through to find where it fails

### 1.3 Document Root Cause

**Root Cause Hypothesis**: [To be determined]

| Layer | Working? | Evidence |
|-------|----------|----------|
| Click handler attached | ? | |
| Function invoked | ? | |
| API call made | ? | |
| API returns data | ? | |
| UI updates | ? | |

---

## Phase 2: Fix Implementation

_Dependent on Phase 1 findings_

### Possible Fix Scenarios

**Scenario A: Click handler not attached/wrong selector**
- Fix: Correct event binding or selector

**Scenario B: API path mismatch**
- Fix: Align frontend path with backend route

**Scenario C: Conversation ID not passed correctly**
- Fix: Correct parameter extraction/passing

**Scenario D: UI not updating after data received**
- Fix: Correct DOM update logic

**Scenario E: Race condition / async issue**
- Fix: Proper async/await handling

### Progressive Bookending
```bash
gh issue comment 574 -b "✓ Root cause identified: [description]
Evidence: [what was found]
Fix approach: [plan]"
```

---

## Phase 3: Testing

### 3.1 Manual Testing

| Scenario | Steps | Expected | Status |
|----------|-------|----------|--------|
| Switch to older conversation | Click older item in sidebar | Chat shows that conversation's messages | [ ] |
| Switch to newer conversation | Click newer item in sidebar | Chat shows that conversation's messages | [ ] |
| Rapid switching | Click multiple items quickly | Final clicked conversation displayed | [ ] |
| Switch after sending message | Send message, then switch | Previous conversation preserved, new one loads | [ ] |
| Switch back to original | Switch away then back | Original conversation loads correctly | [ ] |

### 3.2 Regression Testing

```bash
# Run existing conversation tests
python -m pytest tests/unit/web/api/routes/test_conversation*.py -v

# Run any sidebar-related tests
python -m pytest tests/ -k "conversation" -v
```

---

## Phase Z: Final Bookending & Handoff

### Required Actions

#### 1. Update Issue with Evidence
```bash
gh issue edit 574 --body "[Full updated body with:
- Root cause documented
- Fix description
- All Investigation Status boxes checked
- Evidence section filled]"
```

#### 2. Commit with Evidence
```bash
git add [files]
git commit -m "fix(#574): [description based on root cause]

- Root cause: [what was wrong]
- Fix: [what was changed]
- Testing: [what was verified]

Closes #574

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

#### 3. Push and Verify
```bash
git push origin main
gh issue view 574  # Verify auto-closed
```

#### 4. Update Session Log
Document fix in session log with timestamp.

---

## Multi-Agent Deployment Map

| Phase | Agent Type | Focus | Evidence Required |
|-------|------------|-------|-------------------|
| 0-1 | Lead Dev | Investigation & root cause | Console/network evidence |
| 2 | Lead Dev | Fix implementation | Code changes |
| 3 | Lead Dev + PM | Testing | Manual test results |
| Z | Lead Dev | Bookending | Commit hash, issue closed |

**Single-agent rationale**: Bug investigation requires sequential debugging; multi-agent would add coordination overhead without benefit.

---

## Verification Gates

- [ ] Phase 0: Bug reproduced with evidence
- [ ] Phase 0.5: Frontend-backend paths verified
- [ ] Phase 1: Root cause identified with evidence
- [ ] Phase 2: Fix implemented
- [ ] Phase 3: All manual test scenarios pass
- [ ] Phase 3: No test regressions
- [ ] Phase Z: Issue closed with full evidence

---

## Completion Matrix

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Bug reproduced and documented | [ ] | Screenshots in issue |
| Root cause identified | [ ] | Phase 1 findings |
| Frontend-backend contract verified | [ ] | Phase 0.5 paths |
| Fix implemented | [ ] | Commit hash |
| Manual testing passed (5 scenarios) | [ ] | All green |
| Regression tests pass | [ ] | pytest output |
| Issue updated with full evidence | [ ] | Issue link |
| Issue closed | [ ] | GitHub confirmation |

---

## STOP Conditions

- Cannot reproduce bug → Escalate to PM for clarification
- Root cause unclear after 30 min investigation → Document findings, ask PM
- Fix requires architectural changes → Escalate before implementing
- Fix breaks other conversation features → Stop and reassess
- Backend endpoint missing/broken → File new bug, escalate

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase -1: Infrastructure Verification | 5 min |
| Phase 0: Investigation & Reproduction | 15-20 min |
| Phase 0.5: Frontend-Backend Contract | 10 min |
| Phase 1: Root Cause | 15-20 min |
| Phase 2: Fix Implementation | 10-20 min (depends on root cause) |
| Phase 3: Testing | 10 min |
| Phase Z: Bookending | 5 min |
| **Total** | 70-90 min |

---

## Files Likely Involved

- `templates/index.html` - Sidebar HTML, click handlers, UI update logic
- `web/api/routes/conversation.py` - Conversation list/load endpoints
- `static/js/*.js` - Any extracted JavaScript (if applicable)
- `web/app.py` - Router mounting (for path verification)

---

_Gameplan created: 2026-01-12 13:21_
_Updated to v9.3 compliance: 2026-01-12 13:35_

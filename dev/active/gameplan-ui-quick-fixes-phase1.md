# Gameplan: UI Quick Fixes - Phase 1 Investigation

**Issue**: UI-QUICK-FIXES
**Date**: November 23, 2025, 2:18 PM
**Phase**: Phase 1 (Investigation & Quick Wins)
**Estimated Duration**: 60-90 minutes
**Target**: Complete by 3:30 PM for evaluation

---

## Mission Statement

Systematically investigate 3 high-priority UI issues using Serena, git history, and documentation. Identify quick wins vs rabbit holes. Fix what's simple, document what's complex, prepare for PM evaluation on next steps.

**Philosophy**: Investigation thoroughness over rushed fixes. We need honest assessment of the 75% completion pattern.

---

## Phase 1 Scope: Three Critical Issues

### Issue #6: Create New List Button Fails
- **Built**: Today (Option B work)
- **Hypothesis**: Missing API endpoint or miswiring
- **Priority**: High (core feature just built)

### Issue #7: Create New Todo Button Fails
- **Built**: Today (Option B work)
- **Hypothesis**: Same as #6 (missing API or miswiring)
- **Priority**: High (core feature just built)

### Issue #14: Login/Logout UI Broken
- **Built**: Partially (user menu exists)
- **Hypothesis**: Known issue - buttons not implemented
- **Priority**: High (can't test multi-user scenarios)

---

## Investigation Protocol (For Each Issue)

### Step 1: Serena Symbolic Investigation (10 min)

**Find the code**:
```bash
# Locate template
mcp__serena__find_file "lists.html" "templates"
mcp__serena__get_symbols_overview "templates/lists.html"

# Find JavaScript handler
mcp__serena__search_for_pattern "createNewList|Create.*List" paths_include_glob="**/*.js"

# Find backend route
mcp__serena__find_symbol "lists" relative_path="web/app.py"
mcp__serena__search_for_pattern "@app\.(get|post).*lists" relative_path="web/app.py"
```

**What to document**:
- Does frontend code exist? (button, handler, API call)
- Does backend route exist? (web/app.py)
- Does backend API exist? (services/api/)
- Where is the gap?

### Step 2: Git History Analysis (5 min)

**Check recent work**:
```bash
# When was this touched?
git log --oneline --all --since="1 week ago" -- templates/lists.html web/static/js/

# What was the last change?
git log -p -1 -- templates/lists.html

# Was it part of today's work?
git log --oneline --since="today" --author="Claude"
```

**What to document**:
- Was this built today or earlier?
- What was the last commit message?
- Is there evidence of incomplete work?

### Step 3: Manual Testing (5 min)

**Test the actual behavior**:
1. Open browser to http://localhost:8001/lists
2. Open DevTools Console (F12)
3. Click "Create New List" button
4. Observe:
   - What happens in console?
   - Any JavaScript errors?
   - Any network requests (Network tab)?
   - Any 404s or 500s?

**What to document**:
- Exact error message (if any)
- Network request URL (if made)
- HTTP status code (if applicable)

### Step 4: Root Cause Assessment (5 min)

**Classify the issue**:
- **Type A: Quick Fix** (5-15 min) - Typo, missing function call, simple wiring
- **Type B: Missing Piece** (30-60 min) - Need to implement API endpoint
- **Type C: Rabbit Hole** (2+ hours) - Architectural issue, requires refactor
- **Type D: Known Gap** (document only) - Intentionally incomplete, needs proper implementation

**What to document**:
- Root cause classification
- Estimated fix effort
- Recommendation (fix now, defer, or document)

---

## Phase 1: Issue #6 Investigation (25 minutes)

### Deploy: Lead Developer (You)

**Your Task**: Investigate "Create New List" button failure

#### Investigation Steps

**1. Frontend Code Investigation** (10 min)

```bash
# Find the lists template
mcp__serena__find_file "lists.html" "templates"

# Get overview of template
mcp__serena__read_file "templates/lists.html"

# Find the JavaScript function
mcp__serena__search_for_pattern "createNewList|Create.*List" paths_include_glob="web/static/**/*.js"

# Check if function exists
mcp__serena__find_symbol "createNewList" relative_path="web/static/js/"
```

**Document**:
- Line number where button is defined
- JavaScript function that's called
- Does the function exist?
- What does the function do?

**2. Backend Route Investigation** (5 min)

```bash
# Check if /lists route exists in web/app.py
mcp__serena__search_for_pattern "@app\.post.*lists" relative_path="web/app.py"

# Check services layer
mcp__serena__search_for_pattern "class.*List.*Repository" relative_path="services"

# Check API routes
mcp__serena__find_file "*list*.py" "services/api"
```

**Document**:
- Does POST /api/v1/lists exist?
- Does the backend service exist?
- Where is the gap?

**3. Manual Testing** (5 min)

```bash
# Test in browser
# 1. Navigate to http://localhost:8001/lists
# 2. Open DevTools Console
# 3. Click "Create New List"
# 4. Observe errors

# Test API directly
curl -X POST http://localhost:8001/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"name": "Test List"}'
```

**Document**:
- Console error (if any)
- Network request details
- API response (if any)

**4. Root Cause Assessment** (5 min)

Answer:
- **What's broken?** (Frontend? Backend? Both?)
- **Why?** (Missing code? Typo? Config issue?)
- **Fix effort?** (Quick win? Medium? Rabbit hole?)
- **Recommendation?** (Fix now? Defer? Document?)

**Deliverable**: Create `dev/2025/11/23/issue-6-investigation-report.md`

---

## Phase 1: Issue #7 Investigation (25 minutes)

### Deploy: Lead Developer (You)

**Your Task**: Investigate "Create New Todo" button failure

**Note**: Likely same pattern as Issue #6. If Issue #6 fix is successful, apply same solution here.

#### Investigation Steps

Same protocol as Issue #6, but for:
- `templates/todos.html`
- POST `/api/v1/todos`
- `TodoRepository` or similar

**Efficiency shortcuts**:
- If #6 was "missing API", check if todos API also missing
- If #6 was "JavaScript error", check same error in todos.html
- If #6 was "typo in function name", check todos for same typo

**Deliverable**: Create `dev/2025/11/23/issue-7-investigation-report.md`

---

## Phase 1: Issue #14 Investigation (20 minutes)

### Deploy: Lead Developer (You)

**Your Task**: Investigate login/logout functionality

**Context**: We already documented this as a known issue earlier today (12:51 PM). This investigation confirms what needs to be built.

#### Investigation Steps

**1. Current State Assessment** (10 min)

```bash
# Find user menu code
mcp__serena__search_for_pattern "logout|login|user.*menu" paths_include_glob="templates/**/*.html"

# Find navigation component
mcp__serena__find_file "navigation.html" "templates/components"

# Check for existing auth routes
mcp__serena__search_for_pattern "@app\.(get|post).*(login|logout)" relative_path="web/app.py"

# Check auth service
mcp__serena__find_symbol "auth" relative_path="services"
```

**Document**:
- Where is user menu rendered?
- Do login/logout buttons exist at all?
- Do auth routes exist in backend?
- What's the current auth flow?

**2. Requirements Clarification** (10 min)

**Questions to answer**:
- How are users currently logging in? (Direct URL? Token?)
- Is there a login page or just API endpoints?
- What should logout do? (Clear JWT? Redirect?)
- Do we need login UI or just logout button?

**Check**:
- Read auth middleware in web/app.py
- Check JWT handling
- Look for existing login templates
- Review Issue #307 completion (user context work)

**Deliverable**: Create `dev/2025/11/23/issue-14-investigation-report.md`

---

## Evaluation Point 1: After All Three Investigations

### Required Before Proceeding

**Create**: `dev/2025/11/23/phase-1-summary.md`

**Contents**:

```markdown
# Phase 1 Investigation Summary
**Date**: November 23, 2025
**Time**: [End time]
**Duration**: [Actual time spent]

## Quick Wins Found
- [ ] Issue #6: [Classification] - Estimated fix: [X minutes]
- [ ] Issue #7: [Classification] - Estimated fix: [X minutes]
- [ ] Issue #14: [Classification] - Estimated fix: [X minutes]

## Root Causes Identified
1. Issue #6: [Exact cause]
2. Issue #7: [Exact cause]
3. Issue #14: [Exact cause]

## Recommended Actions

### Fix Immediately (Type A - Quick Wins)
- [List issues that can be fixed in 15-30 minutes]

### Defer with Messaging (Type C/D - Rabbit Holes)
- [List issues that need more time]

### Remaining High-Priority Issues
Based on Phase 1 findings, should we investigate:
- [ ] Issue #4 (Standup generation)?
- [ ] Issue #8 (Files page)?
- [ ] Issue #13 (Integrations)?

## Time/Capacity Assessment
- Time remaining today: [X hours]
- Capacity for Phase 2: [estimate]
- Recommendation: [Fix specific issues / Add "Coming Soon" messaging / Both]

## PM Decision Required
- [ ] Approve fixes for Type A issues
- [ ] Decide on Phase 2 scope (which issues to tackle)
- [ ] Approve "Coming Soon" messaging for deferred issues
```

### Stop and Wait for PM Decision

**Do NOT proceed to fixes without PM approval**

---

## Success Criteria for Phase 1

**Investigation Complete When**:
- [ ] All 3 issues investigated using Serena + git + manual testing
- [ ] Root causes documented with evidence
- [ ] Fix effort estimated (Quick/Medium/Rabbit hole)
- [ ] Investigation reports created for each issue
- [ ] Phase 1 summary document created
- [ ] PM has clear data for decision-making

**Quality Standards**:
- [ ] Used Serena symbolic queries (not just grep)
- [ ] Checked git history (not assumptions)
- [ ] Tested manually (saw actual error)
- [ ] Honest assessment (no rationalization)
- [ ] Evidence-based estimates (not guesses)

---

## Timeline

| Task | Duration | Start | End |
|------|----------|-------|-----|
| Issue #6 investigation | 25 min | 2:25 PM | 2:50 PM |
| Issue #7 investigation | 25 min | 2:50 PM | 3:15 PM |
| Issue #14 investigation | 20 min | 3:15 PM | 3:35 PM |
| Phase 1 summary | 15 min | 3:35 PM | 3:50 PM |
| **Total** | **85 min** | **2:25 PM** | **3:50 PM** |

**Buffer**: 10 minutes (investigation may find surprises)

---

## Tools to Use

### Serena MCP Tools
```bash
mcp__serena__find_file         # Locate files by name
mcp__serena__find_symbol       # Find functions/classes
mcp__serena__get_symbols_overview  # Get file structure
mcp__serena__search_for_pattern    # Search code patterns
mcp__serena__find_referencing_symbols  # Find usages
```

### Git Commands
```bash
git log --oneline --all --since="1 week ago" -- [path]
git log -p --since="today"
git blame [file]
```

### Testing Commands
```bash
# Browser DevTools Console
# Network tab for requests
# curl for API testing
curl -X POST http://localhost:8001/api/v1/[endpoint]
```

---

## STOP Conditions

**STOP investigation if**:
- Issue is deeply architectural (requires ADR discussion)
- Security vulnerability discovered (escalate immediately)
- Requires breaking changes to working features
- Time exceeds 30 minutes per issue (document and move on)

**When stopped**: Mark as Type C (Rabbit Hole), document findings, recommend deferral

---

## After Phase 1: Possible Outcomes

### Outcome A: All Quick Wins
- 2-3 issues are Type A (quick fixes)
- Fix them in 30-45 minutes
- Evaluate if time for more issues

### Outcome B: Mixed Results
- 1 quick win, 2 rabbit holes
- Fix the quick win
- Add "Coming Soon" messaging for others
- Document for post-alpha

### Outcome C: All Rabbit Holes
- All issues are Type C/D
- Add clear "Coming Soon" messaging
- Create proper issues for post-alpha work
- Focus on alpha docs (Issue #377)

---

**Remember**:
- Investigation thoroughness over speed
- Evidence required for all claims
- Honest assessment of completion patterns
- PM decides on Phase 2 scope

---

*Gameplan prepared by: Lead Developer*
*Date: November 23, 2025, 2:18 PM*
*For: Lead Developer (systematic investigation)*

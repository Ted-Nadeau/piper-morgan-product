# Code Agent Prompt: UI Quick Fixes - Phase 1 Investigation

**Date**: November 23, 2025, 2:25 PM
**Estimated Duration**: 85 minutes
**Phase**: Investigation Only (no fixes without PM approval)

---

## Your Mission

Systematically investigate 3 high-priority UI issues that were discovered during navigation testing. Your job is **investigation and diagnosis**, NOT implementing fixes (yet). Use Serena symbolic tools, git history, and manual testing to identify root causes and classify fix effort.

**Critical**: This is detective work. Be thorough, use all available tools, provide evidence for all claims.

---

## Context: What We Know

### Recent Work (Today)
- ✅ Option B complete: Built `/lists`, `/todos`, `/projects` pages
- ✅ Option C complete: Added conversational permission commands
- ✅ Permission system working (permissions.js, sharing modals)

### Navigation QA Results
PM tested all navigation options and found 14 issues. See `dev/active/UI-issues.csv` for full list.

**Your Focus**: Investigate these 3 issues first:
- **Issue #6**: "Create New List" button fails (High priority)
- **Issue #7**: "Create New Todo" button fails (High priority)
- **Issue #14**: Login/logout UI broken (High priority)

---

## Investigation Protocol (Use for Each Issue)

### Step 1: Serena Symbolic Investigation

**Find the code using MCP Serena tools**:

```bash
# Example for Issue #6 (Lists)

# 1. Find the template file
mcp__serena__find_file("lists.html", "templates")

# 2. Get structure of template
mcp__serena__get_symbols_overview("templates/lists.html")

# 3. Find JavaScript handler
mcp__serena__search_for_pattern(
  substring_pattern="createNewList|Create.*List",
  paths_include_glob="web/static/**/*.js",
  output_mode="content"
)

# 4. Check backend routes
mcp__serena__search_for_pattern(
  substring_pattern="@app\\.(get|post).*lists",
  relative_path="web/app.py",
  output_mode="content"
)

# 5. Check backend API
mcp__serena__search_for_pattern(
  substring_pattern="class.*List.*Repository",
  relative_path="services",
  output_mode="files_with_matches"
)
```

**Document your findings**:
- Does frontend button exist? (template line number)
- Does JavaScript handler exist? (function name, file, line number)
- Does backend route exist? (route path, handler function)
- Does backend API exist? (service class, repository)

### Step 2: Git History Analysis

**Check when this was built**:

```bash
# Find recent changes
git log --oneline --all --since="1 week ago" -- templates/lists.html web/static/js/

# Get last commit details
git log -p -1 -- templates/lists.html

# Check today's work
git log --oneline --since="today" --grep="list"

# Check who built it
git log --oneline --author="Claude" -- templates/lists.html
```

**Document your findings**:
- When was this last modified? (commit hash, date)
- What was the commit message?
- Is there evidence of incomplete work?
- Was this built today or earlier?

### Step 3: Manual Testing

**Test the actual behavior** (use browser and DevTools):

1. Navigate to the page (e.g., http://localhost:8001/lists)
2. Open Browser DevTools Console (F12)
3. Click the button
4. Observe and document:
   - JavaScript errors in console?
   - Network requests made? (check Network tab)
   - HTTP status codes? (200, 404, 500?)
   - Any error messages displayed?

**Also test API directly**:

```bash
# Test if endpoint exists
curl -X POST http://localhost:8001/api/v1/lists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [token]" \
  -d '{"name": "Test List"}'

# Document the response
# - 200 OK? → Frontend issue
# - 404 Not Found? → Endpoint missing
# - 500 Error? → Backend bug
# - 401/403? → Auth issue
```

### Step 4: Root Cause Classification

**Classify the issue type**:

**Type A: Quick Fix** (5-15 minutes)
- Typo in function name
- Missing event listener
- Simple wiring issue
- Frontend calls wrong endpoint

**Type B: Missing Piece** (30-60 minutes)
- Backend API endpoint missing
- Need to implement repository method
- Missing database migration
- Frontend logic incomplete

**Type C: Rabbit Hole** (2+ hours)
- Architectural issue
- Requires refactoring
- Multiple missing pieces
- Breaking change required

**Type D: Known Gap** (document only)
- Intentionally incomplete
- Needs proper design
- Post-alpha feature
- Requires PM discussion

**For your recommendation**:
- Classification: [A/B/C/D]
- Root Cause: [Exact technical issue]
- Estimated Fix Effort: [X minutes]
- Recommendation: [Fix now / Defer / Document]

---

## Issue #6: Create New List Button Investigation

### Your Investigation Checklist

**Frontend Investigation**:
- [ ] Found templates/lists.html
- [ ] Located "Create New List" button (line number: ___)
- [ ] Found JavaScript click handler (function: ___, file: ___)
- [ ] Verified function exists and is wired up
- [ ] Checked what API endpoint it calls

**Backend Investigation**:
- [ ] Checked if POST /api/v1/lists exists in web/app.py
- [ ] Checked if ListRepository exists in services/
- [ ] Verified backend has create_list method
- [ ] Checked if database schema supports lists table

**Manual Testing**:
- [ ] Clicked button in browser
- [ ] Documented JavaScript console errors (if any)
- [ ] Checked Network tab for requests
- [ ] Tested API endpoint with curl
- [ ] Documented exact error/response

**Git History**:
- [ ] Found when lists.html was created
- [ ] Checked commit message
- [ ] Identified if this was today's work or earlier

### Create Investigation Report

Save as: `dev/2025/11/23/issue-6-investigation-report.md`

```markdown
# Issue #6 Investigation: Create New List Button Fails

**Date**: November 23, 2025
**Investigator**: Code Agent
**Duration**: [X minutes]

## Summary
[One sentence: What's broken and why]

## Frontend Analysis

**Button Location**: templates/lists.html:LINE
**JavaScript Handler**: web/static/js/FILE.js:LINE
**Function Name**: `functionName()`
**API Call**: POST /api/v1/lists

**Code Snippet**:
```javascript
// Paste relevant code here
```

**Status**: [Working / Broken / Missing]

## Backend Analysis

**Route**: web/app.py:LINE
**Endpoint**: POST /api/v1/lists
**Handler**: `function_name()`
**Service**: ListRepository / UniversalListRepository

**Code Snippet**:
```python
# Paste relevant code here
```

**Status**: [Exists / Missing / Broken]

## Manual Testing Results

**Browser Console**:
```
[Paste exact error messages]
```

**Network Request**:
- URL: [actual URL called]
- Method: POST
- Status: [200/404/500/etc]
- Response: [paste response]

**API Test**:
```bash
curl -X POST http://localhost:8001/api/v1/lists ...
# Response:
[paste response]
```

## Git History

**Last Modified**: [commit hash] - [date]
**Commit Message**: [message]
**Author**: [name]
**Context**: [Was this today's work? Part of Issue #376?]

## Root Cause

**Classification**: [Type A/B/C/D]

**Exact Issue**:
[Describe the technical gap - be specific]

**Why This Happened**:
[Context - was this 75% complete? Never wired? Broke recently?]

## Fix Estimate

**Effort**: [X minutes]

**What Needs to Happen**:
1. [Specific step 1]
2. [Specific step 2]
3. [Specific step 3]

**Complexity**: [Simple / Medium / Complex]

## Recommendation

**Action**: [Fix now / Defer with messaging / Document as known issue]

**Reasoning**: [Why this recommendation?]

**If deferring**: Suggested "Coming Soon" message:
> [Draft user-facing message]

## Evidence

**Screenshots**: [If helpful - save to dev/active/]
**Console logs**: [Attached above]
**API responses**: [Attached above]
```

---

## Issue #7: Create New Todo Button Investigation

**Same protocol as Issue #6**, but for:
- templates/todos.html
- POST /api/v1/todos
- TodoRepository

**Efficiency Note**: If Issue #6 revealed a pattern (e.g., "all POST endpoints missing"), check if Issue #7 has the same pattern. Don't duplicate investigation unnecessarily.

**Save as**: `dev/2025/11/23/issue-7-investigation-report.md`

---

## Issue #14: Login/Logout UI Investigation

### Your Investigation Checklist

**User Menu Investigation**:
- [ ] Found user menu component (navigation.html?)
- [ ] Located logout button (if exists)
- [ ] Located login button (if exists)
- [ ] Checked JavaScript handlers

**Backend Auth Investigation**:
- [ ] Found auth routes in web/app.py
- [ ] Checked for /login endpoint
- [ ] Checked for /logout endpoint
- [ ] Reviewed JWT handling middleware

**Current Auth Flow**:
- [ ] How do users currently log in? (URL? API?)
- [ ] Where is JWT stored? (localStorage? cookie?)
- [ ] What should logout do? (Clear token? Redirect?)

**Manual Testing**:
- [ ] Tested logout button (if exists)
- [ ] Checked DevTools console for errors
- [ ] Attempted login flow
- [ ] Verified token handling

### Create Investigation Report

**Save as**: `dev/2025/11/23/issue-14-investigation-report.md`

Use same template structure as Issue #6, adapted for auth context.

**Key Questions to Answer**:
1. Do login/logout buttons exist at all?
2. Do backend auth endpoints exist?
3. What's the gap? (Frontend? Backend? Both?)
4. Is this a "never built" or "partially built" situation?

---

## Phase 1 Summary Document

After completing all 3 investigations, create:

**File**: `dev/2025/11/23/phase-1-summary.md`

```markdown
# Phase 1 Investigation Summary
**Date**: November 23, 2025, [time]
**Duration**: [actual time]
**Issues Investigated**: 3 (Issues #6, #7, #14)

## Executive Summary

[2-3 sentences: What did we learn? Are these quick fixes or rabbit holes?]

## Results by Issue

| Issue | Classification | Root Cause | Fix Effort | Recommendation |
|-------|----------------|------------|------------|----------------|
| #6 Lists | [A/B/C/D] | [One sentence] | [X min] | [Fix/Defer] |
| #7 Todos | [A/B/C/D] | [One sentence] | [X min] | [Fix/Defer] |
| #14 Login | [A/B/C/D] | [One sentence] | [X min] | [Fix/Defer] |

## Quick Wins Identified

**Can fix immediately** (Type A issues):
- [ ] [Issue #X: Description - Est. Y minutes]
- [ ] [Issue #X: Description - Est. Y minutes]

**Total quick win time**: [X minutes]

## Rabbit Holes Identified

**Should defer** (Type C/D issues):
- [ ] [Issue #X: Description - Reason to defer]
- [ ] [Issue #X: Description - Reason to defer]

## Common Patterns Found

[Any patterns across multiple issues?]
- All POST endpoints missing?
- All buttons have typo in handler name?
- All built today but API wasn't implemented?
- All pre-existing 75% work?

## Recommendations for Phase 2

### Option A: Fix Quick Wins Only
**Time**: [X minutes]
**Issues**: [List Type A issues]
**Result**: [Core features working]

### Option B: Fix Quick Wins + One Rabbit Hole
**Time**: [X minutes]
**Issues**: [List]
**Result**: [More complete but takes longer]

### Option C: Add "Coming Soon" Messaging Only
**Time**: [X minutes]
**Action**: [No fixes, just clear communication]
**Result**: [Honest alpha state]

## PM Decision Required

Based on investigation findings:
1. Approve fixes for Type A issues? [Yes/No]
2. Which rabbit holes (if any) to tackle today?
3. Approve "Coming Soon" messaging for deferred issues?
4. Should we investigate remaining issues (#4, #8, #13)?

## Time/Capacity Assessment

**Time Spent on Phase 1**: [X minutes]
**Current Time**: [time]
**Remaining Time Today**: [estimate]
**Capacity for Phase 2**: [Conservative estimate]

**Recommendation**: [What's realistic for rest of today?]
```

---

## Validation Before Reporting Complete

**Check your work**:
- [ ] Used Serena MCP tools (not just grep/read)
- [ ] Checked git history (not assumptions)
- [ ] Tested manually in browser (saw actual errors)
- [ ] Tested API with curl (verified endpoints)
- [ ] Created all 4 documents (3 reports + 1 summary)
- [ ] Evidence-based classifications (not guesses)
- [ ] Honest assessments (no rationalization)
- [ ] Clear recommendations with reasoning

---

## STOP Conditions

**STOP and escalate if**:
- Issue requires architectural decision
- Security vulnerability discovered
- Database schema issues found
- Breaking changes to working features
- Investigation exceeds 30 min per issue

**When stopped**: Document findings, mark as Type C/D, move to next issue

---

## Reporting Back

When complete, provide:

1. **Investigation Summary**:
   - Total time spent
   - Issues classified (how many A/B/C/D)
   - Quick wins identified
   - Rabbit holes identified

2. **Evidence**:
   - All 4 markdown documents created
   - Console logs captured
   - API responses documented
   - Git history checked

3. **Recommendations**:
   - What should PM approve for Phase 2?
   - Which issues to fix vs defer?
   - Estimated time for approved fixes

4. **Any Surprises**:
   - Unexpected findings?
   - Common patterns discovered?
   - New issues revealed?

---

**Remember**:
- Investigation thoroughness > speed
- Evidence required for ALL claims
- Honest assessment of 75% pattern
- DO NOT implement fixes without PM approval
- Michelle's alpha experience is tomorrow!

---

*Prompt prepared by: Lead Developer*
*Date: November 23, 2025, 2:25 PM*
*Estimated completion: 3:50 PM*

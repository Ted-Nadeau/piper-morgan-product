# Code Agent Prompt: UI Quick Fixes - Phase 3 Investigation

**Date**: November 23, 2025, 4:16 PM
**Estimated Duration**: 90 minutes
**Phase**: Investigation Only (no fixes without PM approval)

---

## Your Mission

Systematically investigate 3 remaining high-priority UI issues discovered during navigation testing. Your job is **investigation and diagnosis**, NOT implementing fixes (yet). Use Serena symbolic tools, git history, and manual testing to identify root causes and classify fix effort.

**Pattern Recognition**: Phase 2 showed that thorough investigation led to 5-minute fixes for 3 issues. Apply the same systematic approach here.

---

## Context: What We Know

### Phase 2 Success (Completed 4:10 PM - 4:15 PM)
- ✅ Issue #14 (Logout): Type A - 1 line fix (endpoint path)
- ✅ Issue #6 (Lists): Type B - Backend POST endpoint missing
- ✅ Issue #7 (Todos): Type B - Copy/paste from #6
- **Total time**: 5 minutes (vs 60-75 min estimate)
- **Learning**: Systematic investigation identifies quick wins and pattern reuse

### Phase 3 Focus: Investigate These Issues
- **Issue #4**: Standup generation button hangs/does nothing (High priority)
- **Issue #8**: Files page says "coming soon" but feature exists (High priority)
- **Issue #13**: Integrations page broken, causes error (High priority)

---

## Investigation Protocol (Use for Each Issue)

### Step 1: Serena Symbolic Investigation

**Find the code using MCP Serena tools**:

```bash
# Example for Issue #4 (Standup)

# 1. Find the template file
mcp__serena__find_file("standup.html", "templates")

# 2. Get structure of template
mcp__serena__get_symbols_overview("templates/standup.html")

# 3. Find JavaScript handler
mcp__serena__search_for_pattern(
  substring_pattern="generateStandup|Generate.*Standup",
  paths_include_glob="**/*.js",
  context_lines_before=5,
  context_lines_after=5
)

# 4. Check backend routes
mcp__serena__search_for_pattern(
  substring_pattern="@app\\.(get|post).*standup",
  relative_path="web/app.py"
)

# 5. Check backend service
mcp__serena__find_symbol(
  name_path_pattern="StandupService",
  relative_path="services",
  depth=1
)
```

**Document your findings**:
- Does frontend button exist? (template line number)
- Does JavaScript handler exist? (function name, file, line number)
- Does backend route exist? (route path, handler function)
- Does backend service exist? (service class, methods)

### Step 2: Git History Analysis

**Check when this was built**:

```bash
# Find recent changes
git log --oneline --all --since="1 week ago" -- templates/standup.html web/static/js/

# Get last commit details
git log -p -1 -- templates/standup.html

# Check historical work
git log --oneline --grep="standup" --since="2 weeks ago"

# Check author
git log --oneline --author="Claude" -- templates/standup.html
```

**Document your findings**:
- When was this last modified? (commit hash, date)
- What was the commit message?
- Is there evidence of incomplete work?
- Was this recently built or pre-existing?

### Step 3: Manual Testing

**Test the actual behavior** (use browser and DevTools):

1. Navigate to the page (e.g., http://localhost:8001/standup)
2. Open Browser DevTools Console (F12)
3. Click the button
4. Observe and document:
   - JavaScript errors in console?
   - Network requests made? (check Network tab)
   - HTTP status codes? (200, 404, 500?)
   - Any error messages displayed?
   - Does it "hang" (spinner forever) or fail immediately?

**Also test API directly**:

```bash
# Test if endpoint exists
curl -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [token]" \
  -d '{}'

# Document the response
# - 200 OK? → Frontend issue
# - 404 Not Found? → Endpoint missing
# - 500 Error? → Backend bug
# - 401/403? → Auth issue
# - Timeout? → Long-running task issue
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

## Issue #4: Standup Generation Button Investigation

### Your Investigation Checklist

**Frontend Investigation**:
- [ ] Found templates/standup.html
- [ ] Located "Generate Standup" button (line number: ___)
- [ ] Found JavaScript click handler (function: ___, file: ___)
- [ ] Verified function exists and is wired up
- [ ] Checked what API endpoint it calls
- [ ] Observed behavior: Does it hang with spinner? Error? Silent fail?

**Backend Investigation**:
- [ ] Checked if POST /api/v1/standup/generate exists in web/app.py
- [ ] Checked if StandupService exists in services/
- [ ] Verified backend has generate method
- [ ] Checked if endpoint requires async/await handling
- [ ] Checked for timeout issues (long-running AI generation?)

**Manual Testing**:
- [ ] Clicked button in browser
- [ ] Documented JavaScript console errors (if any)
- [ ] Checked Network tab for requests
- [ ] Documented exact behavior (hangs? spinner? error?)
- [ ] Tested API endpoint with curl
- [ ] Documented exact error/response

**Git History**:
- [ ] Found when standup.html was created
- [ ] Checked commit message
- [ ] Identified if this was recent work or pre-existing

### Create Investigation Report

Save as: `dev/2025/11/23/issue-4-investigation-report.md`

```markdown
# Issue #4 Investigation: Standup Generation Button Hangs

**Date**: November 23, 2025
**Investigator**: Code Agent
**Duration**: [X minutes]

## Summary
[One sentence: What's broken and why]

## Frontend Analysis

**Button Location**: templates/standup.html:LINE
**JavaScript Handler**: web/static/js/FILE.js:LINE
**Function Name**: `functionName()`
**API Call**: POST /api/v1/standup/generate

**Code Snippet**:
```javascript
// Paste relevant code here
```

**Status**: [Working / Broken / Missing]

## Backend Analysis

**Route**: web/app.py:LINE
**Endpoint**: POST /api/v1/standup/generate
**Handler**: `function_name()`
**Service**: StandupService

**Code Snippet**:
```python
# Paste relevant code here
```

**Status**: [Exists / Missing / Broken]

## Manual Testing Results

**Browser Behavior**:
- Click button → [exact behavior]
- Spinner shown? [yes/no]
- How long before failure? [X seconds / never completes]

**Browser Console**:
```
[Paste exact error messages]
```

**Network Request**:
- URL: [actual URL called]
- Method: POST
- Status: [200/404/500/timeout/pending forever]
- Response: [paste response]

**API Test**:
```bash
curl -X POST http://localhost:8001/api/v1/standup/generate ...
# Response:
[paste response]
```

## Git History

**Last Modified**: [commit hash] - [date]
**Commit Message**: [message]
**Author**: [name]
**Context**: [Was this recent work? Pre-existing?]

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

## Issue #8: Files Page Investigation

### Your Investigation Checklist

**Frontend Investigation**:
- [ ] Found templates/files.html
- [ ] Checked for "Coming Soon" placeholder text (line number: ___)
- [ ] Looked for commented-out code or disabled features
- [ ] Found any JavaScript handlers (file upload? list display?)

**Backend Investigation**:
- [ ] Checked if GET /files route exists
- [ ] Checked if POST /api/v1/files exists (file upload)
- [ ] Checked if FileRepository exists in services/
- [ ] Verified backend has CRUD methods
- [ ] Checked if file storage is configured

**Manual Testing**:
- [ ] Navigated to /files page
- [ ] Documented what's visible (placeholder vs UI)
- [ ] Checked console for errors
- [ ] Tested if any functionality works

**Git History**:
- [ ] When was files.html created?
- [ ] What commit added "coming soon" message?
- [ ] Is there evidence of feature being built but disabled?

### Create Investigation Report

**Save as**: `dev/2025/11/23/issue-8-investigation-report.md`

Use same template structure as Issue #4, adapted for Files context.

**Key Questions to Answer**:
1. Does the Files feature actually exist in backend?
2. Is frontend showing "coming soon" but backend is ready?
3. What's the gap? (Frontend disabled? Backend missing? Both incomplete?)
4. Why was "coming soon" added if feature exists?

---

## Issue #13: Integrations Page Investigation

### Your Investigation Checklist

**Frontend Investigation**:
- [ ] Found templates/integrations.html (or equivalent)
- [ ] Located "Coming Soon" message
- [ ] Found JavaScript that causes error when clicking
- [ ] Identified what click event triggers the error

**Backend Investigation**:
- [ ] Checked if GET /settings/integrations route exists
- [ ] Checked if integration services exist (slack, github, notion, etc.)
- [ ] Verified which integrations are actually implemented
- [ ] Checked if API endpoints for managing integrations exist

**Manual Testing**:
- [ ] Navigated to integrations page
- [ ] Clicked and documented exact error
- [ ] Checked console for JavaScript errors
- [ ] Checked Network tab for failed requests
- [ ] Tested if any integration functionality works

**Git History**:
- [ ] When was integrations page created?
- [ ] What integrations have been built? (check services/integrations/)
- [ ] Why is page showing "coming soon" if features exist?

**Known Context**:
From earlier investigation, we know these integrations exist:
- services/integrations/slack/
- services/integrations/github/
- services/integrations/notion/
- services/integrations/calendar/
- services/integrations/demo/
- services/integrations/mcp/
- services/integrations/spatial/

So the question is: Why is the UI saying "coming soon"?

### Create Investigation Report

**Save as**: `dev/2025/11/23/issue-13-investigation-report.md`

Use same template structure, but pay special attention to:
- What error occurs when clicking?
- Which integrations are wired vs unwired?
- Is this a display issue (showing wrong message) or functionality issue?

---

## Phase 3 Summary Document

After completing all 3 investigations, create:

**File**: `dev/2025/11/23/phase-3-investigation-summary.md`

```markdown
# Phase 3 Investigation Summary

**Date**: November 23, 2025, [time]
**Duration**: [actual time]
**Issues Investigated**: 3 (Issues #4, #8, #13)

## Executive Summary

[2-3 sentences: What did we learn? Are these quick fixes or rabbit holes?]

## Results by Issue

| Issue | Classification | Root Cause | Fix Effort | Recommendation |
|-------|----------------|------------|------------|----------------|
| #4 Standup | [A/B/C/D] | [One sentence] | [X min] | [Fix/Defer] |
| #8 Files | [A/B/C/D] | [One sentence] | [X min] | [Fix/Defer] |
| #13 Integrations | [A/B/C/D] | [One sentence] | [X min] | [Fix/Defer] |

## Quick Wins Identified

**Can fix immediately** (Type A issues):
- [ ] [Issue #X: Description - Est. Y minutes]

**Total quick win time**: [X minutes]

## Medium Effort (Type B)

**Can fix with pattern reuse**:
- [ ] [Issue #X: Description - Est. Y minutes - Pattern from Issue #X]

## Rabbit Holes Identified

**Should defer** (Type C/D issues):
- [ ] [Issue #X: Description - Reason to defer]

## Common Patterns Found

[Any patterns across multiple issues?]
- All features exist but UI says "coming soon"?
- All clicking causes same error?
- All async/timeout issues?
- All pre-existing 75% work?

## Recommendations for Phase 4

### Option A: Fix Quick Wins Only
**Time**: [X minutes]
**Issues**: [List Type A issues]
**Result**: [Core features working]

### Option B: Fix Quick Wins + Medium Effort
**Time**: [X minutes]
**Issues**: [List]
**Result**: [More complete but takes longer]

### Option C: Add Clear Messaging Only
**Time**: [X minutes]
**Action**: [No fixes, just clear communication]
**Result**: [Honest alpha state]

## PM Decision Required

Based on investigation findings:
1. Approve fixes for Type A issues? [Yes/No]
2. Which Type B issues to tackle today?
3. Approve messaging for deferred issues?
4. Continue to Medium/Low priority issues after this?

## Time/Capacity Assessment

**Time Spent on Phase 3**: [X minutes]
**Current Time**: [time]
**Remaining Time Today**: [estimate]
**Capacity for Phase 4**: [Conservative estimate]

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
   - What should PM approve for Phase 4?
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
- Phase 2 took 5 minutes because investigation was thorough

---

*Prompt prepared by: Lead Developer*
*Date: November 23, 2025, 4:16 PM*
*Based on Phase 2 success pattern*

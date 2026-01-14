# Claude Code Agent Prompt: Issue #548 FTUX-EMPTY-STATES

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #548. Your work is part of a multi-agent coordination chain.

### Your Acceptance Criteria Format
When you receive acceptance criteria, they will look like:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Test requirement]

**Every checkbox must be addressed in your handoff.**

### Evidence You MUST Provide
1. **Test count**: "Added X tests in [file path]"
2. **Test verification**: "All tests passing" with actual output below
3. **Files modified**: Complete list with approximate line counts
4. **How to verify**: Step-by-step instructions for user testing

### Your Handoff Format
Return your work with this structure:
```
## Issue #548 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in [location]
- `pytest [path] -v` output: [paste actual output]

**Verification**:
[Actual command output showing success]

**Files Modified**:
- [file1.html] (+X/-Y lines)
- [file2.py] (+X/-Y lines)

**User Testing Steps**:
1. [Step 1]
2. [Step 2]
3. [Expected result]

**Blockers** (if any):
- [Blocker description and why it prevents completion]
```

### Remember
- You're part of a coordination chain
- Your output enables the next step
- Incomplete handoff = failed task
- Evidence > assertions
- The Lead Developer will verify your work independently

---

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

---

## Essential Context

Read these briefing documents first in `docs/briefing/`:
- `PROJECT.md` - What Piper Morgan is
- `BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

**This is critical**. After compaction, get your bearings first.

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
**Before doing ANYTHING else, verify infrastructure matches gameplan**:

```bash
# What the gameplan assumes exists:
# - templates/todos.html, projects.html, files.html, lists.html
# - templates/components/empty-state.html component
# - dev/active/empty-state-voice-guide-v1.md voice guide
# - Empty states at specific line numbers

# Verify reality:
ls -la templates/todos.html templates/projects.html templates/files.html templates/lists.html
ls -la templates/components/empty-state.html
ls -la dev/active/empty-state-voice-guide-v1.md

# Check current empty state patterns
grep -n "No todos" templates/todos.html | head -3
grep -n "No projects" templates/projects.html | head -3
grep -n "No files" templates/files.html | head -3
grep -n "No lists" templates/lists.html | head -3

# Check component interface
head -30 templates/components/empty-state.html

# Check server state
ps aux | grep python
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## 🎯 ANTI-80% COMPLETION SAFEGUARDS

### For This Task (4 Templates + Voice Guide + Tests)
This task modifies 4 templates with 2 locations each (static + JS). Component completeness check:

1. **Template Completeness Check**:
```
Required Changes         | Implemented | Status
------------------------ | ----------- | ------
Voice guide: Add Lists   | ?           |
todos.html static        | ?           |
todos.html JS render     | ?           |
todos.html "all complete"| ?           |
projects.html static     | ?           |
projects.html JS render  | ?           |
files.html static        | ?           |
files.html JS render     | ?           |
lists.html static        | ?           |
lists.html JS render     | ?           |
Unit tests (5)           | ?           |
TOTAL: ?/11 = ?%
```

2. **ZERO AUTHORIZATION to skip templates**
You have NO permission to:
- Skip any of the 4 templates
- Skip the "all complete" state for todos
- Skip JS render updates
- Skip tests "because copy looks right"
- Rationalize gaps as "minor"

3. **Objective Completion Metric Required**
Before claiming completion:
- Show exact count: "11/11 elements = 100%"
- Not subjective: "looks complete"

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!
```bash
# Check if you already have a log today
ls -la dev/2026/01/06/*-prog-code-*.md
```

**If NO log exists**: Create new log with format:
- `dev/2026/01/06/2026-01-06-HHMM-prog-code-log.md`

**If log EXISTS**: DO NOT create new log!
- Append new session section to existing log
- Use format: `## Session [N]: Issue #548 ([Time])`

---

## MANDATORY FIRST ACTIONS

### 1. Check What Already Exists
**After infrastructure verification**:
```bash
# Check empty-state component interface
cat templates/components/empty-state.html

# Check voice guide current state
cat dev/active/empty-state-voice-guide-v1.md | head -50

# Check if Lists section exists in voice guide
grep -n "Lists" dev/active/empty-state-voice-guide-v1.md

# Check existing empty state patterns
grep -n "empty-state" templates/todos.html | head -5
grep -n "empty-state" templates/projects.html | head -5

# Check server state
ps aux | grep python
```

### 2. Assess System Context
**Is this a LIVE SYSTEM with user data?**
- [ ] Check if user configuration exists
- [ ] This is frontend-only, no user data at risk
- [ ] Voice guide is development documentation (safe to modify)
- [ ] No backup needed for this task

---

## Mission

**Objective**: Replace generic empty state copy in todos, projects, files, and lists views with voice guide templates using the existing `empty-state.html` component. Include "all complete" state for todos.

**Scope Boundaries**:
- This prompt covers ONLY: 4 templates + voice guide update + unit tests
- NOT in scope: Backend changes, new components
- Separate prompts handle: #547 (piper intro), #549 (post-setup orientation)

**PREREQUISITE**: Update voice guide with Lists section BEFORE implementing templates.

---

## Context

- **GitHub Issue**: [#548 - Replace empty state copy with voice guide templates](https://github.com/mediajunkie/piper-morgan-product/issues/548)
- **Gameplan**: `dev/active/gameplan-548-ftux-empty-states.md`
- **Current State**: Templates have generic "No X yet" copy with inline HTML
- **Target State**: Templates use component with voice guide copy
- **Dependencies**: Voice guide must have Lists section first
- **User Data Risk**: None
- **Infrastructure Verified**: Pending (you must verify)

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"Updated todos.html"** → Show `grep -n "No todos yet" templates/todos.html`
- **"Added component include"** → Show `grep -n "include.*empty-state" templates/todos.html`
- **"Updated voice guide"** → Show `grep -n "Lists" dev/active/empty-state-voice-guide-v1.md`
- **"Added all complete state"** → Show `grep -n "All caught up" templates/todos.html`
- **"Tests pass"** → Show full pytest output with pass counts

### Completion Bias Prevention (CRITICAL):
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- **NO assumptions** - only verified facts
- **NO rushing to claim done** - evidence first, claims second

### Git Workflow Discipline:
After ANY code changes:
```bash
./scripts/fix-newlines.sh  # ALWAYS run first
git status
git add [files]
git commit -m "[descriptive message]"
git log --oneline -1  # MANDATORY - show this output
```

---

## Constraints & Requirements

### For ALL Agents (14 Rules)
1. **Infrastructure verified**: Check gameplan assumptions first
2. **100% completion**: No partial implementations
3. **Check existing first**: Never create what already exists
4. **Preserve user data**: Never delete user configuration
5. **Resource Check First**: Consult resource-map.md before starting
6. **GitHub First**: Issue must exist and be assigned
7. **Evidence Required**: Every claim needs terminal output proof
8. **Verification First**: Check existing patterns before implementing
9. **Stop Conditions**: Stop immediately if any trigger occurs
10. **Session Log Format**: Must be .md not .txt
11. **Git Discipline**: Verify all commits with log output
12. **Server Awareness**: Know what's running before changes
13. **Objective metrics**: X/X = 100% for all components
14. **Time agnosticism**: No time estimates, only effort (small/medium/large)

---

## Multi-Agent Coordination

You are likely working alongside other agents on Sprint B1.

### Your Role (Claude Code):
- Focus on #548 implementation
- Update GitHub issue with your progress
- Provide evidence for cross-validation
- Session log: `2026-01-06-HHMM-prog-code-log.md`

### Cross-Validation:
- Your work will be verified by the Lead Developer
- Provide evidence (terminal output, diffs)
- Flag any conflicts or contradictions found

### Coordination Timing:
- Update GitHub issue after completing implementation
- Before claiming complete, run all verification steps
- STOP if you find conflicting implementations

---

## Phase 0: Mandatory Verification (STOP if any fail)

```bash
# -1. INFRASTRUCTURE CHECK (CRITICAL)
ls -la templates/todos.html templates/projects.html templates/files.html templates/lists.html
ls -la templates/components/empty-state.html
ls -la dev/active/empty-state-voice-guide-v1.md

# 0. SERVER STATE CHECK
ps aux | grep python

# 1. Verify GitHub issue exists
gh issue view 548 --repo mediajunkie/piper-morgan-product

# 2. Check voice guide for Lists section (should NOT exist yet)
grep -n "Lists View" dev/active/empty-state-voice-guide-v1.md
# Should return nothing - we need to add it

# 3. Check component interface
grep -n "set icon" templates/components/empty-state.html
grep -n "set title" templates/components/empty-state.html
grep -n "set message" templates/components/empty-state.html

# 4. Check current empty state locations
grep -n "No todos" templates/todos.html
grep -n "No projects" templates/projects.html
grep -n "No files" templates/files.html
grep -n "No lists" templates/lists.html

# 5. Check git status
git status
git log --oneline -3
```

**STOP and report if**:
- [ ] Infrastructure doesn't match gameplan
- [ ] Any template file doesn't exist
- [ ] Component interface differs from expected
- [ ] Voice guide v2 exists (supersedes v1)
- [ ] Issue doesn't exist or isn't assigned
- [ ] Git repository in unexpected state

---

## Implementation Approach

### Step 0: Update Voice Guide with Lists Section (PREREQUISITE)

**File**: `dev/active/empty-state-voice-guide-v1.md`

Add after the Projects section (around line 177):

```markdown
---

### Lists View

**State**: No lists created

```
No lists yet.

Lists help organize related items. Say "create a list called..."
to get started.
```

---
```

- **Expected outcome**: Lists section added to voice guide
- **Validation**: `grep -n "Lists View" dev/active/empty-state-voice-guide-v1.md`
- **Evidence**: Show grep output with line number

### Step 1: Refactor todos.html

**File**: `templates/todos.html`

**Location 1** (static HTML) - Replace empty state with:
```jinja2
{% set icon = '✅' %}
{% set title = 'No todos yet.' %}
{% set message = 'Say "add a todo: [your task]" to create one, or I can suggest some based on your open GitHub issues.' %}
{% include 'components/empty-state.html' %}
```

**Location 2** (JavaScript render) - Update copy to match:
```javascript
container.innerHTML = `
    <div class="empty-state" role="status" aria-label="Empty state">
        <div class="empty-state-icon" aria-hidden="true">✅</div>
        <h2 class="empty-state-title">No todos yet.</h2>
        <p class="empty-state-message">Say "add a todo: [your task]" to create one, or I can suggest some based on your open GitHub issues.</p>
    </div>
`;
```

**Add "All Complete" state** - Find where todos are rendered when list is non-empty but all complete:
```javascript
// When all todos are completed
if (todos.length > 0 && todos.every(t => t.completed)) {
    container.innerHTML = `
        <div class="empty-state" role="status" aria-label="All complete">
            <div class="empty-state-icon" aria-hidden="true">🎯</div>
            <h2 class="empty-state-title">All caught up!</h2>
            <p class="empty-state-message">Your todo list is clear. Nice work.</p>
        </div>
    `;
    return;
}
```

- **Expected outcome**: todos.html updated with 3 changes
- **Validation**:
  - `grep -n "No todos yet" templates/todos.html`
  - `grep -n "All caught up" templates/todos.html`
- **Evidence**: Show grep output

### Step 2: Refactor projects.html

**File**: `templates/projects.html`

**Static HTML**:
```jinja2
{% set icon = '📁' %}
{% set title = 'No projects set up yet.' %}
{% set message = 'Projects help me understand your work context. Say "create a project called..." to get started.' %}
{% include 'components/empty-state.html' %}
```

**JavaScript render** - Update copy to match, keep inline structure.

- **Expected outcome**: projects.html updated with 2 changes
- **Validation**: `grep -n "No projects set up yet" templates/projects.html`
- **Evidence**: Show grep output

### Step 3: Refactor files.html

**File**: `templates/files.html`

**Static HTML**:
```jinja2
{% set icon = '📄' %}
{% set title = 'No documents in your knowledge base yet.' %}
{% set message = 'You can upload files, connect Notion, or just paste content into our chat—I\'ll remember it for later.' %}
{% include 'components/empty-state.html' %}
```

**JavaScript render** - Update copy to match.

- **Expected outcome**: files.html updated with 2 changes
- **Validation**: `grep -n "No documents in your knowledge base" templates/files.html`
- **Evidence**: Show grep output

### Step 4: Refactor lists.html

**File**: `templates/lists.html`

**Static HTML**:
```jinja2
{% set icon = '📋' %}
{% set title = 'No lists yet.' %}
{% set message = 'Lists help organize related items. Say "create a list called..." to get started.' %}
{% include 'components/empty-state.html' %}
```

**JavaScript render** - Update copy to match.

- **Expected outcome**: lists.html updated with 2 changes
- **Validation**: `grep -n "No lists yet" templates/lists.html`
- **Evidence**: Show grep output

### Step 5: Write Unit Tests

**Create**: `tests/unit/templates/test_empty_states.py`

```python
"""Tests for empty state copy in view templates."""
import pytest


class TestEmptyStateCopy:
    """Verify empty states use voice guide copy."""

    def test_empty_state_copy_todos(self, test_client):
        """Todos empty state uses voice guide copy."""
        response = test_client.get("/todos")
        assert response.status_code == 200
        assert "No todos yet" in response.text
        assert 'Say "add a todo' in response.text

    def test_empty_state_copy_projects(self, test_client):
        """Projects empty state uses voice guide copy."""
        response = test_client.get("/projects")
        assert response.status_code == 200
        assert "No projects set up yet" in response.text
        assert "create a project called" in response.text

    def test_empty_state_copy_files(self, test_client):
        """Files empty state uses voice guide copy."""
        response = test_client.get("/files")
        assert response.status_code == 200
        assert "No documents in your knowledge base" in response.text
        assert "upload files" in response.text

    def test_empty_state_copy_lists(self, test_client):
        """Lists empty state uses voice guide copy."""
        response = test_client.get("/lists")
        assert response.status_code == 200
        assert "No lists yet" in response.text
        assert "create a list called" in response.text

    def test_empty_state_demonstrates_piper_grammar(self, test_client):
        """Empty states show how to talk to Piper."""
        response = test_client.get("/todos")
        # Should demonstrate conversational command pattern
        assert 'Say "' in response.text or "say '" in response.text.lower()
```

- **Expected outcome**: 5 unit tests created
- **Validation**: `python -m pytest tests/unit/templates/test_empty_states.py -v`
- **Evidence**: Show full pytest output

### Step 6: Git Commit

```bash
./scripts/fix-newlines.sh
git add dev/active/empty-state-voice-guide-v1.md templates/todos.html templates/projects.html templates/files.html templates/lists.html tests/unit/templates/test_empty_states.py
git commit -m "feat(ftux): Update empty state copy to use voice guide templates (#548)"
git log --oneline -1
```

- **Expected outcome**: Clean commit
- **Validation**: `git log --oneline -1`
- **Evidence**: Show commit hash and message

---

## Architecture Boundaries

This is a **Presentation Layer** change only:
- **Presentation Layer**: Template modifications (allowed)
- **No Domain Layer changes**: Correct
- **No Application Layer changes**: Correct
- **No Infrastructure Layer changes**: Correct

---

## Success Criteria (With Evidence)

- [ ] Infrastructure matches expectations (`ls -la templates/*.html` output)
- [ ] 11/11 elements complete (show completeness table)
- [ ] Voice guide updated with Lists section (show grep)
- [ ] All 4 templates updated (show grep for each)
- [ ] "All complete" state added to todos (show grep)
- [ ] All tests pass (show pytest output: 5 passed)
- [ ] GitHub issue updated (show issue link)
- [ ] Evidence provided for each claim (terminal outputs)
- [ ] Git commit clean (show `git log --oneline -1`)
- [ ] Copy demonstrates Piper grammar (show grep for `Say "`)

---

## Deliverables

1. **Voice Guide Update**: `dev/active/empty-state-voice-guide-v1.md` - Lists section added
2. **Code Changes**: 4 templates modified
3. **Component Completeness**: 11/11 elements table
4. **Test Coverage**: `tests/unit/templates/test_empty_states.py` (5 tests)
5. **Evidence Report**: Terminal output showing success
6. **GitHub Update**: Issue #548 updated with completion
7. **Git Status**: Clean repository with commit

---

## Cross-Validation Preparation

Leave clear markers for verification:
- File paths:
  - `dev/active/empty-state-voice-guide-v1.md`
  - `templates/todos.html`
  - `templates/projects.html`
  - `templates/files.html`
  - `templates/lists.html`
  - `tests/unit/templates/test_empty_states.py`
- Test command: `python -m pytest tests/unit/templates/test_empty_states.py -v`
- Expected test output: 5 passed
- Grep commands to verify:
  - `grep -n "Lists View" dev/active/empty-state-voice-guide-v1.md`
  - `grep -n "No todos yet" templates/todos.html`
  - `grep -n "All caught up" templates/todos.html`
  - `grep -n "No projects set up yet" templates/projects.html`
  - `grep -n "No documents in your knowledge base" templates/files.html`
  - `grep -n "No lists yet" templates/lists.html`

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. **Does infrastructure match what gameplan expected?**
2. **Is my implementation 100% complete (11/11 elements)?**
3. **Did I update the voice guide FIRST (prerequisite)?**
4. **Did I update ALL 4 templates (both static and JS)?**
5. **Did I add the "all complete" state to todos?**
6. **Did I provide terminal evidence for every claim?**
7. **Can another agent verify my work independently?**
8. **Am I claiming work done that I didn't actually do?**
9. **Is there a gap between my claims and reality?**
10. **Did I verify git commits with log output?**
11. **Did I run the tests and show output?**
12. **Does the copy demonstrate Piper grammar ("Say...")?**
13. **Am I rationalizing gaps as "minor" or "optional"?**

### If Uncertain:
- Run verification commands yourself
- Show actual output, not expected output
- Acknowledge what's not done yet
- Ask for help if stuck
- Never guess - always verify!

---

## Example Evidence Format

```bash
# Show voice guide updated
$ grep -n "Lists View" dev/active/empty-state-voice-guide-v1.md
178:### Lists View

# Show todos.html updated
$ grep -n "No todos yet" templates/todos.html
87:{% set title = 'No todos yet.' %}
142:<h2 class="empty-state-title">No todos yet.</h2>

# Show "all complete" state added
$ grep -n "All caught up" templates/todos.html
155:<h2 class="empty-state-title">All caught up!</h2>

# Show projects.html updated
$ grep -n "No projects set up yet" templates/projects.html
56:{% set title = 'No projects set up yet.' %}

# Show files.html updated
$ grep -n "No documents in your knowledge base" templates/files.html
150:{% set title = 'No documents in your knowledge base yet.' %}

# Show lists.html updated
$ grep -n "No lists yet" templates/lists.html
86:{% set title = 'No lists yet.' %}

# Show test results
$ python -m pytest tests/unit/templates/test_empty_states.py -v
===== test session starts =====
tests/unit/templates/test_empty_states.py::TestEmptyStateCopy::test_empty_state_copy_todos PASSED
tests/unit/templates/test_empty_states.py::TestEmptyStateCopy::test_empty_state_copy_projects PASSED
tests/unit/templates/test_empty_states.py::TestEmptyStateCopy::test_empty_state_copy_files PASSED
tests/unit/templates/test_empty_states.py::TestEmptyStateCopy::test_empty_state_copy_lists PASSED
tests/unit/templates/test_empty_states.py::TestEmptyStateCopy::test_empty_state_demonstrates_piper_grammar PASSED
===== 5 passed in 0.67s =====

# Show git commit
$ git log --oneline -1
def5678 feat(ftux): Update empty state copy to use voice guide templates (#548)
```

---

## Related Documentation

- `docs/development/methodology-core/resource-map.md` - Resource locations
- `docs/internal/architecture/current/patterns/` - Pattern catalog
- `dev/active/gameplan-548-ftux-empty-states.md` - Full gameplan
- `dev/active/empty-state-voice-guide-v1.md` - Authoritative copy source

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:
1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. **Completing prerequisite FIRST** (voice guide update)
4. Checking what exists NEXT (no reinventing)
5. Following ALL verification requirements
6. Providing evidence for EVERY claim
7. Creating component completeness table
8. Stopping when assumptions are needed
9. Maintaining architectural integrity
10. Updating GitHub with progress
11. Creating session logs in .md format
12. Verifying git commits with log output
13. Providing grep/terminal proof for UI claims
14. **Never guessing - always verifying first!**
15. **Never rationalizing incompleteness!**

**Infrastructure mismatches and completion bias are session failures. Evidence is mandatory.**

---

## Anti-Pattern Examples

### ❌ WRONG: Skipping JS Render Updates
```
"Updated the static HTML, the JS render still has old copy but it works"
```
**Why wrong**: Both locations must be updated for consistency!

### ✅ RIGHT: Both Locations Updated
```
$ grep -n "No todos yet" templates/todos.html
87:{% set title = 'No todos yet.' %}  # Static
142:<h2 class="empty-state-title">No todos yet.</h2>  # JS render
```

### ❌ WRONG: Skipping Voice Guide Prerequisite
```
"Started implementing templates, will update voice guide later"
```
**Why wrong**: Prerequisite must be done FIRST!

### ✅ RIGHT: Prerequisite First
```
Step 0: Updated voice guide with Lists section
$ grep -n "Lists View" dev/active/empty-state-voice-guide-v1.md
178:### Lists View
Then proceeded to templates...
```

### ❌ WRONG: Forgetting "All Complete" State
```
"Updated all 4 templates, done!"
```
**Why wrong**: Missing the "All caught up!" state for todos!

### ✅ RIGHT: All Elements Included
```
11/11 elements complete:
- Voice guide: Lists added ✓
- todos.html: static ✓, JS ✓, all complete ✓
- projects.html: static ✓, JS ✓
- files.html: static ✓, JS ✓
- lists.html: static ✓, JS ✓
- Tests: 5 passing ✓
```

---

## STOP Conditions (17 Total)

If ANY of these occur, STOP and escalate:
1. Infrastructure doesn't match gameplan
2. Implementation <100% complete (11/11)
3. Any template file missing
4. Tests fail for any reason
5. Component interface differs from expected
6. GitHub issue missing or unassigned
7. Can't provide verification evidence
8. Voice guide v2 supersedes v1
9. Resource not found after searching
10. Completion bias detected (claiming without proof)
11. Rationalizing gaps as "minor" or "optional"
12. GitHub tracking not working
13. Git operations failing
14. Server state unexpected
15. JS render locations can't be identified
16. Copy doesn't match voice guide
17. Prerequisite not completed first

---

## When Tests Fail (CRITICAL - YOU DO NOT DECIDE)

**If ANY test fails**:

1. **STOP immediately** - Do NOT continue
2. **Do NOT decide** if failure is "critical"
3. **Do NOT rationalize** ("core works", "not blocking")

**Instead, report**:
```
⚠️ STOP - Tests Failing

Failing: [X] tests
Passing: [Y] tests

Exact errors:
[paste error output]

Root cause (if known):
[your diagnosis]

Options:
1. [fix approach]
2. [alternative approach]
3. [skip with approval]

Awaiting PM decision.
```

**Remember**: PM decides what's critical, not you. Your job is to report, provide options, and wait.

---

*Agent Prompt v2.0 | Template v10.2 Compliant | January 6, 2026*

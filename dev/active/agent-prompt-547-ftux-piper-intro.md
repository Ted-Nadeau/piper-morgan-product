# Claude Code Agent Prompt: Issue #547 FTUX-PIPER-INTRO

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #547. Your work is part of a multi-agent coordination chain.

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
## Issue #547 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in [location]
- `pytest [path] -v` output: [paste actual output]

**Verification**:
[Actual command output showing success]

**Files Modified**:
- [file1.py] (+X/-Y lines)
- [file2.html] (+X/-Y lines)

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
# - templates/setup.html with .setup-step classes
# - CSS-hidden wizard steps
# - Vanilla JavaScript (no React/Vue)

# Verify reality:
ls -la templates/setup.html
grep -n "setup-step" templates/setup.html | head -5
grep -n "class=\"active\"" templates/setup.html | head -3

# Check for existing intro panel (should NOT exist)
grep -n "piper-intro" templates/setup.html

# Check server state
ps aux | grep python
ps aux | grep piper
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

Example report:
```
"Gameplan assumes vanilla JS wizard, but found:
$ grep -n "React" templates/setup.html
Line 5: <script src='react.min.js'>
Actually need: Different implementation approach"
```

---

## 🎯 ANTI-80% COMPLETION SAFEGUARDS

### For This Task (Frontend-Only)
This task does not implement an interface/adapter, so method enumeration is N/A. However:

1. **Component Completeness Check**:
```
Required Elements    | Implemented | Status
-------------------- | ----------- | ------
HTML panel           | ?           |
CSS styling          | ?           |
JS init function     | ?           |
JS dismiss function  | ?           |
sessionStorage logic | ?           |
Unit tests (2)       | ?           |
TOTAL: ?/6 = ?%
```

2. **ZERO AUTHORIZATION to skip elements**
You have NO permission to:
- Skip mobile responsive CSS
- Skip accessibility attributes
- Skip tests "because UI works"
- Rationalize gaps as "minor"

3. **Objective Completion Metric Required**
Before claiming completion:
- Show exact count: "6/6 elements = 100%"
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
- Use format: `## Session [N]: Issue #547 ([Time])`

---

## MANDATORY FIRST ACTIONS

### 1. Check What Already Exists
**After infrastructure verification**:
```bash
# Check for existing patterns
grep -r "intro" templates/ --include="*.html"
grep -r "greeting" templates/ --include="*.html"

# Check existing CSS patterns in setup.html
grep -n "\.setup-" templates/setup.html | head -10

# Check existing JS patterns
grep -n "function" templates/setup.html | head -10

# Check server state
ps aux | grep python
```

### 2. Assess System Context
**Is this a LIVE SYSTEM with user data?**
- [ ] Check if user configuration exists
- [ ] This is frontend-only, no user data at risk
- [ ] No backup needed for this task

---

## Mission

**Objective**: Add inline Piper greeting panel to setup wizard that appears BEFORE Step 1, introducing users to Piper before they begin the setup process.

**Scope Boundaries**:
- This prompt covers ONLY: `templates/setup.html` modifications + unit tests
- NOT in scope: Backend changes, other templates
- Separate prompts handle: #548 (empty states), #549 (post-setup orientation)

---

## Context

- **GitHub Issue**: [#547 - Add Piper greeting to setup wizard start](https://github.com/mediajunkie/piper-morgan-product/issues/547)
- **Gameplan**: `dev/active/gameplan-547-ftux-piper-intro.md`
- **Current State**: Setup wizard starts directly at Step 1 (System Requirements)
- **Target State**: Inline greeting panel appears before Step 1, dismisses to reveal wizard
- **Dependencies**: None (frontend-only)
- **User Data Risk**: None
- **Infrastructure Verified**: Pending (you must verify)

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"Added HTML panel"** → Show `grep -n "piper-intro" templates/setup.html`
- **"Added CSS"** → Show `grep -n "piper-intro-panel" templates/setup.html`
- **"Added JS functions"** → Show `grep -n "dismissPiperIntro" templates/setup.html`
- **"Tests pass"** → Show full pytest output with pass counts
- **"Mobile responsive"** → Show CSS media query in file
- **"Accessibility"** → Show `role=` and `aria-` attributes in output

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
- Focus on #547 implementation
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
ls -la templates/setup.html
grep -n "setup-step" templates/setup.html | head -5

# 0. SERVER STATE CHECK
ps aux | grep python

# 1. Verify GitHub issue exists
gh issue view 547 --repo mediajunkie/piper-morgan-product

# 2. Check for existing intro patterns
grep -r "intro" templates/setup.html
grep -r "greeting" templates/setup.html

# 3. Check existing JS structure
grep -n "DOMContentLoaded" templates/setup.html

# 4. Check existing CSS structure
grep -n "<style>" templates/setup.html

# 5. Verify no piper-intro already exists
grep -n "piper-intro" templates/setup.html
# Should return nothing

# 6. Check git status
git status
git log --oneline -3
```

**STOP and report if**:
- [ ] Infrastructure doesn't match gameplan
- [ ] `templates/setup.html` doesn't exist
- [ ] Wizard uses React/Vue instead of vanilla JS
- [ ] `piper-intro` already exists
- [ ] Issue doesn't exist or isn't assigned
- [ ] Git repository in unexpected state

---

## Implementation Approach

### Step 1: Add Intro Panel HTML

**File**: `templates/setup.html`

Add BEFORE the first `.setup-step` div:

```html
<!-- Piper Introduction Panel - shown before wizard steps -->
<div id="piper-intro" class="piper-intro-panel" role="region" aria-labelledby="piper-intro-heading">
    <div class="piper-intro-content">
        <h2 id="piper-intro-heading" class="piper-greeting">
            Hi, I'm Piper Morgan, your PM assistant! You can call me Piper. 👋
        </h2>
        <p class="piper-description">
            I'm here to help you with product management work—tracking tasks,
            managing GitHub issues, prepping for standups, and staying on top
            of your calendar.
        </p>
        <p class="piper-setup-intro">
            Let me help you get set up. I'll need to check a few things and
            connect to your tools.
        </p>
        <button id="piper-intro-cta" class="piper-intro-button" onclick="dismissPiperIntro()">
            Let's get started →
        </button>
    </div>
</div>
```

- **Expected outcome**: HTML panel exists in template
- **Validation**: `grep -n "piper-intro" templates/setup.html`
- **Evidence**: Show grep output with line numbers

### Step 2: Add CSS Styling

Add to `<style>` section in `setup.html`:

```css
/* Piper Introduction Panel - Inline before wizard */
.piper-intro-panel {
    text-align: center;
    padding: 40px 30px;
    max-width: 500px;
    margin: 0 auto;
}

.piper-intro-panel.hidden {
    display: none;
}

.piper-greeting {
    font-size: 24px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0 0 20px 0;
}

.piper-description,
.piper-setup-intro {
    font-size: 16px;
    color: #5a6c7d;
    line-height: 1.6;
    margin-bottom: 16px;
}

.piper-intro-button {
    background: #3498db;
    color: white;
    border: none;
    padding: 14px 28px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 20px;
    transition: background 0.2s;
}

.piper-intro-button:hover {
    background: #2980b9;
}

.piper-intro-button:focus {
    outline: 2px solid #2980b9;
    outline-offset: 2px;
}

/* Mobile responsiveness */
@media (max-width: 480px) {
    .piper-intro-panel {
        padding: 30px 20px;
    }

    .piper-greeting {
        font-size: 20px;
    }

    .piper-description,
    .piper-setup-intro {
        font-size: 15px;
    }
}
```

- **Expected outcome**: CSS classes defined with mobile responsiveness
- **Validation**: `grep -n "piper-intro-panel" templates/setup.html`
- **Evidence**: Show grep output showing CSS block

### Step 3: Add JavaScript Logic

Add to `<script>` section:

```javascript
// Piper Intro Panel Logic
function initPiperIntro() {
    const introSeen = sessionStorage.getItem('piper_intro_seen');
    const introPanel = document.getElementById('piper-intro');
    const progressBar = document.querySelector('.setup-progress');
    const wizardSteps = document.querySelectorAll('.setup-step');

    if (introSeen === 'true') {
        // Skip intro, show wizard
        if (introPanel) introPanel.classList.add('hidden');
        if (progressBar) progressBar.style.display = 'flex';
        // Activate first step
        if (wizardSteps.length > 0) wizardSteps[0].classList.add('active');
    } else {
        // Show intro, hide wizard until dismissed
        if (introPanel) introPanel.classList.remove('hidden');
        if (progressBar) progressBar.style.display = 'none';
        wizardSteps.forEach(step => step.classList.remove('active'));
    }
}

function dismissPiperIntro() {
    sessionStorage.setItem('piper_intro_seen', 'true');

    const introPanel = document.getElementById('piper-intro');
    const progressBar = document.querySelector('.setup-progress');
    const firstStep = document.querySelector('.setup-step');

    if (introPanel) introPanel.classList.add('hidden');
    if (progressBar) progressBar.style.display = 'flex';
    if (firstStep) firstStep.classList.add('active');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initPiperIntro);
```

- **Expected outcome**: JS functions for init and dismiss
- **Validation**: `grep -n "dismissPiperIntro" templates/setup.html`
- **Evidence**: Show grep output with function definitions

### Step 4: Write Unit Tests

**Create**: `tests/unit/templates/test_setup_intro.py`

```python
"""Tests for Piper intro panel in setup wizard."""
import pytest


class TestSetupIntroPanel:
    """Test setup intro panel rendering and behavior."""

    def test_setup_intro_panel_renders(self, test_client):
        """Verify intro panel HTML is present in setup template."""
        response = test_client.get("/setup")
        assert response.status_code == 200
        assert "piper-intro" in response.text
        assert "Hi, I'm Piper Morgan" in response.text
        assert "Let's get started" in response.text

    def test_setup_intro_has_required_elements(self, test_client):
        """Verify all required intro elements exist."""
        response = test_client.get("/setup")
        assert "piper-intro-cta" in response.text  # CTA button
        assert "dismissPiperIntro" in response.text  # JS function
        assert 'role="region"' in response.text  # Accessibility
```

- **Expected outcome**: 2 unit tests created
- **Validation**: `python -m pytest tests/unit/templates/test_setup_intro.py -v`
- **Evidence**: Show full pytest output

### Step 5: Git Commit

```bash
./scripts/fix-newlines.sh
git add templates/setup.html tests/unit/templates/test_setup_intro.py
git commit -m "feat(ftux): Add Piper greeting panel to setup wizard (#547)"
git log --oneline -1
```

- **Expected outcome**: Clean commit
- **Validation**: `git log --oneline -1`
- **Evidence**: Show commit hash and message

---

## Architecture Boundaries

This is a **Presentation Layer** change only:
- **Presentation Layer**: Template modification (allowed)
- **No Domain Layer changes**: Correct
- **No Application Layer changes**: Correct
- **No Infrastructure Layer changes**: Correct

---

## Success Criteria (With Evidence)

- [ ] Infrastructure matches expectations (`ls -la templates/setup.html` output)
- [ ] 6/6 elements complete (show completeness table)
- [ ] All tests pass (show pytest output: 2 passed)
- [ ] GitHub issue updated (show issue link)
- [ ] No architecture violations (frontend-only confirmed)
- [ ] Evidence provided for each claim (terminal outputs)
- [ ] Git commit clean (show `git log --oneline -1`)
- [ ] Accessibility attributes present (show grep for `role=`)
- [ ] Mobile responsive CSS present (show grep for `@media`)

---

## Deliverables

1. **Code Changes**: `templates/setup.html` modified
2. **Component Completeness**: 6/6 elements table
3. **Test Coverage**: `tests/unit/templates/test_setup_intro.py` (2 tests)
4. **Evidence Report**: Terminal output showing success
5. **GitHub Update**: Issue #547 updated with completion
6. **Git Status**: Clean repository with commit
7. **Accessibility**: `role="region"`, `aria-labelledby` present
8. **Mobile**: `@media` query present

---

## Cross-Validation Preparation

Leave clear markers for verification:
- File path: `templates/setup.html`
- Test command: `python -m pytest tests/unit/templates/test_setup_intro.py -v`
- Expected test output: 2 passed
- Grep commands to verify:
  - `grep -n "piper-intro" templates/setup.html`
  - `grep -n "dismissPiperIntro" templates/setup.html`
  - `grep -n "@media" templates/setup.html`

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. **Does infrastructure match what gameplan expected?**
2. **Is my implementation 100% complete (6/6 elements)?**
3. **Did I provide terminal evidence for every claim?**
4. **Can another agent verify my work independently?**
5. **Am I claiming work done that I didn't actually do?**
6. **Is there a gap between my claims and reality?**
7. **Did I verify git commits with log output?**
8. **For UI claims, do I have evidence (grep output)?**
9. **Am I rationalizing gaps as "minor" or "optional"?**
10. **Do I have objective metrics or subjective impressions?**
11. **Did I run the tests and show output?**
12. **Did I check accessibility attributes are present?**
13. **Did I check mobile responsive CSS is present?**

### If Uncertain:
- Run verification commands yourself
- Show actual output, not expected output
- Acknowledge what's not done yet
- Ask for help if stuck
- Never guess - always verify!

---

## Example Evidence Format

```bash
# Show HTML was added
$ grep -n "piper-intro" templates/setup.html
45:<div id="piper-intro" class="piper-intro-panel" role="region"...
67:</div> <!-- end piper-intro -->

# Show CSS was added
$ grep -n "piper-intro-panel" templates/setup.html
112:.piper-intro-panel {
118:.piper-intro-panel.hidden {

# Show JS was added
$ grep -n "dismissPiperIntro" templates/setup.html
185:function dismissPiperIntro() {
59:onclick="dismissPiperIntro()"

# Show accessibility
$ grep -n 'role=' templates/setup.html
45:role="region" aria-labelledby="piper-intro-heading"

# Show mobile responsive
$ grep -n "@media" templates/setup.html
145:@media (max-width: 480px) {

# Show test results
$ python -m pytest tests/unit/templates/test_setup_intro.py -v
===== test session starts =====
tests/unit/templates/test_setup_intro.py::TestSetupIntroPanel::test_setup_intro_panel_renders PASSED
tests/unit/templates/test_setup_intro.py::TestSetupIntroPanel::test_setup_intro_has_required_elements PASSED
===== 2 passed in 0.45s =====

# Show git commit
$ git log --oneline -1
abc1234 feat(ftux): Add Piper greeting panel to setup wizard (#547)
```

---

## Related Documentation

- `docs/development/methodology-core/resource-map.md` - Resource locations
- `docs/internal/architecture/current/patterns/` - Pattern catalog
- `dev/active/gameplan-547-ftux-piper-intro.md` - Full gameplan
- `dev/active/empty-state-voice-guide-v1.md` - Voice/tone reference

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:
1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. Checking what exists NEXT (no reinventing)
4. Following ALL verification requirements
5. Providing evidence for EVERY claim
6. Creating component completeness table
7. Stopping when assumptions are needed
8. Maintaining architectural integrity
9. Updating GitHub with progress
10. Creating session logs in .md format
11. Verifying git commits with log output
12. Providing grep/terminal proof for UI claims
13. **Never guessing - always verifying first!**
14. **Never rationalizing incompleteness!**

**Infrastructure mismatches and completion bias are session failures. Evidence is mandatory.**

---

## Anti-Pattern Examples

### ❌ WRONG: Skipping Tests Because "UI Works"
```
"The panel displays correctly in the browser, so tests aren't necessary"
```
**Why wrong**: Tests are required deliverables, not optional!

### ✅ RIGHT: Tests Are Mandatory
```
Tests added: 2 in tests/unit/templates/test_setup_intro.py
Output: 2 passed in 0.45s
```

### ❌ WRONG: Claiming Done Without Evidence
```
"Added the intro panel with all required elements"
```
**Why wrong**: No grep output, no proof!

### ✅ RIGHT: Evidence for Every Claim
```
$ grep -n "piper-intro" templates/setup.html
45:<div id="piper-intro"...
[full output shown]
```

---

## STOP Conditions (17 Total)

If ANY of these occur, STOP and escalate:
1. Infrastructure doesn't match gameplan
2. Implementation <100% complete
3. Pattern already exists (piper-intro found)
4. Tests fail for any reason
5. Configuration assumptions needed
6. GitHub issue missing or unassigned
7. Can't provide verification evidence
8. Template structure unexpected
9. Resource not found after searching
10. Completion bias detected (claiming without proof)
11. Rationalizing gaps as "minor" or "optional"
12. GitHub tracking not working
13. Git operations failing
14. Server state unexpected
15. UI behavior can't be verified
16. Accessibility attributes missing
17. Mobile CSS missing

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

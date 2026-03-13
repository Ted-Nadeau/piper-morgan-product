# Claude Code Agent Prompt: Issue #549 FTUX-POST-SETUP

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #549. Your work is part of a multi-agent coordination chain.

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
5. **Migration status**: Confirm migration created and applied

### Your Handoff Format
Return your work with this structure:
```
## Issue #549 Completion Report
**Status**: Complete/Partial/Blocked

**Migration**:
- File: alembic/versions/xxx_add_orientation_seen.py
- Applied: `alembic upgrade head` output

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
# - services/database/models.py with User model having setup_complete
# - templates/home.html
# - web/api/routes/ui.py with home route
# - /api/v1/integrations/health endpoint
# - Alembic for migrations

# Verify reality:
grep -n "setup_complete" services/database/models.py
ls -la templates/home.html
grep -n "def home" web/api/routes/ui.py
grep -n "health" web/api/routes/integrations.py
ls -la alembic/

# Check current User model boolean flags pattern
grep -n "Column(Boolean" services/database/models.py | head -10

# Check if orientation_seen already exists (should NOT)
grep -n "orientation_seen" services/database/models.py

# Check server state
ps aux | grep python
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## 🎯 ANTI-80% COMPLETION SAFEGUARDS

### For This Task (Backend + Frontend + Tests)
This task has migration, backend routes, and frontend changes. Component completeness check:

1. **Component Completeness Check**:
```
Required Changes              | Implemented | Status
----------------------------- | ----------- | ------
User model: orientation_seen  | ?           |
Alembic migration             | ?           |
Migration applied             | ?           |
Home route: pass context      | ?           |
Dismiss endpoint              | ?           |
home.html: modal HTML         | ?           |
home.html: CSS styling        | ?           |
home.html: JS logic           | ?           |
home.html: Escape key handler | ?           |
Unit tests (3)                | ?           |
Integration test (1)          | ?           |
TOTAL: ?/11 = ?%
```

2. **ZERO AUTHORIZATION to skip components**
You have NO permission to:
- Skip the migration
- Skip the dismiss endpoint
- Use localStorage instead of database
- Skip keyboard accessibility
- Skip tests "because modal works"
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
- Use format: `## Session [N]: Issue #549 ([Time])`

---

## MANDATORY FIRST ACTIONS

### 1. Check What Already Exists
**After infrastructure verification**:
```bash
# Check User model structure
grep -A 5 "class User" services/database/models.py | head -20

# Check home route current implementation
grep -A 20 "def home" web/api/routes/ui.py

# Check integration health endpoint response format
grep -A 15 "IntegrationHealthResponse" services/domain/models.py

# Check integration health endpoint
grep -A 10 "def.*health" web/api/routes/integrations.py

# Check server state
ps aux | grep python
```

### 2. Assess System Context
**Is this a LIVE SYSTEM with user data?**
- [ ] Check if user configuration exists
- [ ] User model change requires migration
- [ ] Backup database before migration: `pg_dump piper_morgan > backup.sql`
- [ ] Migration adds column with default value (safe)

---

## Mission

**Objective**: Add a post-setup orientation modal that appears on the home page after a user completes setup for the first time. Shows contextual suggestions based on connected integrations. Uses database storage (User model column) for persistence.

**Scope Boundaries**:
- This prompt covers: Migration + User model + routes + home.html + tests
- NOT in scope: Other templates, voice guide changes
- Separate prompts handle: #547 (piper intro), #548 (empty states)

---

## Context

- **GitHub Issue**: [#549 - Add post-setup orientation](https://github.com/mediajunkie/piper-morgan-product/issues/549)
- **Gameplan**: `dev/active/gameplan-549-ftux-post-setup.md`
- **Current State**: No post-setup orientation exists
- **Target State**: Modal appears once after setup, persists dismissal in database
- **Dependencies**: None (but integrations endpoint used for conditional suggestions)
- **User Data Risk**: LOW - adding column with default, no data loss
- **Infrastructure Verified**: Pending (you must verify)

**IMPORTANT ENDPOINT CORRECTION**:
- Use `/api/v1/integrations/health` (NOT `/status`)
- Response format: `{ integrations: [...] }` array (NOT `{ github: {...} }`)

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"Added User model column"** → Show `grep -n "orientation_seen" services/database/models.py`
- **"Created migration"** → Show `ls -la alembic/versions/*orientation*`
- **"Applied migration"** → Show `alembic upgrade head` output
- **"Updated home route"** → Show `grep -n "orientation_seen" web/api/routes/ui.py`
- **"Added dismiss endpoint"** → Show `grep -n "dismiss" web/api/routes/ui.py`
- **"Added modal HTML"** → Show `grep -n "orientation-modal" templates/home.html`
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
- Focus on #549 implementation
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
grep -n "setup_complete" services/database/models.py
ls -la templates/home.html
grep -n "def home" web/api/routes/ui.py
ls -la alembic/

# 0. SERVER STATE CHECK
ps aux | grep python

# 1. Verify GitHub issue exists
gh issue view 549 --repo mediajunkie/piper-morgan-product

# 2. Check if orientation_seen already exists (should NOT)
grep -n "orientation_seen" services/database/models.py
# Should return nothing

# 3. Check User model boolean flag pattern
grep -n "Column(Boolean" services/database/models.py | head -10

# 4. Check integration health endpoint
grep -n "/health" web/api/routes/integrations.py

# 5. Check IntegrationHealthResponse format
grep -A 10 "class IntegrationHealthResponse" services/domain/models.py

# 6. Check git status
git status
git log --oneline -3
```

**STOP and report if**:
- [ ] Infrastructure doesn't match gameplan
- [ ] `setup_complete` doesn't exist on User model
- [ ] `orientation_seen` already exists
- [ ] Home route doesn't exist
- [ ] Integration health endpoint doesn't exist
- [ ] Issue doesn't exist or isn't assigned
- [ ] Git repository in unexpected state

---

## Implementation Approach

### Step 1: Update User Model

**File**: `services/database/models.py`

Add after `setup_completed_at` (around line 86):

```python
orientation_seen = Column(Boolean, default=False, nullable=False)
```

- **Expected outcome**: New column added to User model
- **Validation**: `grep -n "orientation_seen" services/database/models.py`
- **Evidence**: Show grep output with line number

### Step 2: Create Migration

```bash
alembic revision --autogenerate -m "Add orientation_seen to users"
```

Verify the generated migration contains:

```python
def upgrade():
    op.add_column('users', sa.Column('orientation_seen', sa.Boolean(),
                                      nullable=False, server_default='false'))

def downgrade():
    op.drop_column('users', 'orientation_seen')
```

- **Expected outcome**: Migration file created
- **Validation**: `ls -la alembic/versions/*orientation*`
- **Evidence**: Show ls output and migration content

### Step 3: Apply Migration

```bash
alembic upgrade head
```

- **Expected outcome**: Migration applied successfully
- **Validation**: Show alembic output
- **Evidence**: Paste full alembic output

### Step 4: Update Home Route

**File**: `web/api/routes/ui.py`

Find the home route and update to pass additional context:

```python
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Get user from request state (already authenticated)
    user = request.state.user if hasattr(request.state, 'user') else None

    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": user,
        "setup_complete": user.setup_complete if user else False,
        "orientation_seen": user.orientation_seen if user else True,
    })
```

- **Expected outcome**: Home route passes setup_complete and orientation_seen
- **Validation**: `grep -n "orientation_seen" web/api/routes/ui.py`
- **Evidence**: Show grep output

### Step 5: Add Dismiss Endpoint

**File**: `web/api/routes/ui.py`

Add new endpoint:

```python
@router.post("/api/v1/orientation/dismiss")
async def dismiss_orientation(request: Request):
    """Mark orientation as seen for current user."""
    user = request.state.user if hasattr(request.state, 'user') else None
    if user:
        user.orientation_seen = True
        # Commit the change (adjust based on your session handling)
        db = request.state.db
        await db.commit()
    return {"status": "ok"}
```

- **Expected outcome**: Dismiss endpoint created
- **Validation**: `grep -n "dismiss_orientation" web/api/routes/ui.py`
- **Evidence**: Show grep output

### Step 6: Add Modal HTML to home.html

**File**: `templates/home.html`

Add before closing `</body>`:

```html
<!-- Post-Setup Orientation Modal -->
<div id="orientation-modal" class="orientation-modal hidden" role="dialog" aria-modal="true" aria-labelledby="orientation-title">
    <div class="orientation-backdrop" onclick="dismissOrientation()"></div>
    <div class="orientation-content">
        <button class="orientation-close" onclick="dismissOrientation()" aria-label="Close orientation">×</button>

        <h2 id="orientation-title" class="orientation-title">You're all set! 🎉</h2>
        <p class="orientation-subtitle">Here are some things we can do together:</p>

        <div class="orientation-suggestions">
            <!-- GitHub suggestion (conditional) -->
            <div id="suggestion-github" class="orientation-suggestion hidden">
                <span class="suggestion-icon" aria-hidden="true">📋</span>
                <div class="suggestion-content">
                    <strong>"Show me my open issues"</strong>
                    <span>See what needs attention</span>
                </div>
            </div>

            <!-- Calendar suggestion (conditional) -->
            <div id="suggestion-calendar" class="orientation-suggestion hidden">
                <span class="suggestion-icon" aria-hidden="true">📅</span>
                <div class="suggestion-content">
                    <strong>"What's on my calendar today?"</strong>
                    <span>Check your schedule</span>
                </div>
            </div>

            <!-- Always available -->
            <div class="orientation-suggestion">
                <span class="suggestion-icon" aria-hidden="true">✅</span>
                <div class="suggestion-content">
                    <strong>"Add a todo: [task]"</strong>
                    <span>Start tracking work</span>
                </div>
            </div>
        </div>

        <button class="orientation-cta" onclick="dismissOrientation()">
            Get started →
        </button>
    </div>
</div>
```

- **Expected outcome**: Modal HTML added
- **Validation**: `grep -n "orientation-modal" templates/home.html`
- **Evidence**: Show grep output

### Step 7: Add CSS Styling

**File**: `templates/home.html` (in `<style>` section)

```css
/* Orientation Modal */
.orientation-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.orientation-modal.hidden {
    display: none;
}

.orientation-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
}

.orientation-content {
    position: relative;
    background: white;
    border-radius: 16px;
    padding: 40px;
    max-width: 480px;
    width: 90%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    text-align: center;
}

.orientation-close {
    position: absolute;
    top: 16px;
    right: 16px;
    background: none;
    border: none;
    font-size: 24px;
    color: #95a5a6;
    cursor: pointer;
    padding: 4px 8px;
}

.orientation-close:hover {
    color: #7f8c8d;
}

.orientation-close:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}

.orientation-title {
    font-size: 28px;
    font-weight: 600;
    color: #2c3e50;
    margin: 0 0 8px 0;
}

.orientation-subtitle {
    font-size: 16px;
    color: #7f8c8d;
    margin: 0 0 24px 0;
}

.orientation-suggestions {
    text-align: left;
    margin-bottom: 24px;
}

.orientation-suggestion {
    display: flex;
    align-items: flex-start;
    padding: 12px 16px;
    background: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 12px;
}

.orientation-suggestion.hidden {
    display: none;
}

.suggestion-icon {
    font-size: 20px;
    margin-right: 12px;
    flex-shrink: 0;
}

.suggestion-content {
    display: flex;
    flex-direction: column;
}

.suggestion-content strong {
    color: #2c3e50;
    font-size: 15px;
}

.suggestion-content span {
    color: #7f8c8d;
    font-size: 13px;
    margin-top: 2px;
}

.orientation-cta {
    background: #3498db;
    color: white;
    border: none;
    padding: 14px 32px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}

.orientation-cta:hover {
    background: #2980b9;
}

.orientation-cta:focus {
    outline: 2px solid #2980b9;
    outline-offset: 2px;
}

/* Mobile responsiveness */
@media (max-width: 480px) {
    .orientation-content {
        padding: 30px 24px;
    }

    .orientation-title {
        font-size: 24px;
    }
}
```

- **Expected outcome**: CSS classes defined
- **Validation**: `grep -n "orientation-modal" templates/home.html | head -5`
- **Evidence**: Show grep output showing CSS

### Step 8: Add JavaScript Logic

**File**: `templates/home.html` (in `<script>` section)

```javascript
// Post-Setup Orientation Logic
async function initOrientation() {
    // Check if user has completed setup but hasn't seen orientation
    const setupComplete = {{ setup_complete | tojson }};
    const orientationSeen = {{ orientation_seen | tojson }};

    if (setupComplete && !orientationSeen) {
        // Fetch integration status to customize suggestions
        await loadIntegrationSuggestions();
        showOrientationModal();
    }
}

async function loadIntegrationSuggestions() {
    try {
        const response = await fetch('/api/v1/integrations/health');
        if (response.ok) {
            const data = await response.json();

            // Integration health returns { integrations: [...] } array
            const integrations = data.integrations || [];

            // Show GitHub suggestion if connected
            const github = integrations.find(i => i.name === 'github');
            if (github?.status === 'connected') {
                document.getElementById('suggestion-github')?.classList.remove('hidden');
            }

            // Show Calendar suggestion if connected
            const calendar = integrations.find(i => i.name === 'calendar');
            if (calendar?.status === 'connected') {
                document.getElementById('suggestion-calendar')?.classList.remove('hidden');
            }
        }
    } catch (error) {
        console.error('Failed to load integration status:', error);
        // Continue showing modal without conditional suggestions
    }
}

function showOrientationModal() {
    const modal = document.getElementById('orientation-modal');
    if (modal) {
        modal.classList.remove('hidden');
        // Focus the close button for accessibility
        const closeBtn = modal.querySelector('.orientation-close');
        if (closeBtn) closeBtn.focus();
    }
}

async function dismissOrientation() {
    // Persist to database
    try {
        await fetch('/api/v1/orientation/dismiss', {
            method: 'POST',
            credentials: 'same-origin'
        });
    } catch (error) {
        console.error('Failed to save orientation state:', error);
    }

    // Hide modal
    const modal = document.getElementById('orientation-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Keyboard accessibility - close on Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modal = document.getElementById('orientation-modal');
        if (modal && !modal.classList.contains('hidden')) {
            dismissOrientation();
        }
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', initOrientation);
```

- **Expected outcome**: JS functions added including Escape handler
- **Validation**:
  - `grep -n "dismissOrientation" templates/home.html`
  - `grep -n "Escape" templates/home.html`
- **Evidence**: Show grep output

### Step 9: Write Unit Tests

**Create**: `tests/unit/templates/test_orientation.py`

```python
"""Tests for post-setup orientation modal."""
import pytest


class TestOrientationModal:
    """Test orientation modal rendering and behavior."""

    def test_orientation_modal_renders(self, test_client, authenticated_user):
        """Verify orientation modal HTML is present in home template."""
        response = test_client.get("/")
        assert response.status_code == 200
        assert "orientation-modal" in response.text
        assert "You're all set!" in response.text

    def test_orientation_has_required_elements(self, test_client, authenticated_user):
        """Verify all required orientation elements exist."""
        response = test_client.get("/")
        assert "suggestion-github" in response.text
        assert "suggestion-calendar" in response.text
        assert "dismissOrientation" in response.text
        assert 'role="dialog"' in response.text  # Accessibility

    def test_orientation_conditional_suggestions(self, test_client, authenticated_user):
        """Verify suggestions are conditional on integration status."""
        response = test_client.get("/")
        # GitHub and Calendar suggestions should exist (hidden by default)
        assert "suggestion-github" in response.text
        assert "suggestion-calendar" in response.text
        # Always-available todo suggestion should be visible
        assert "Add a todo" in response.text
```

- **Expected outcome**: 3 unit tests created
- **Validation**: `python -m pytest tests/unit/templates/test_orientation.py -v`
- **Evidence**: Show full pytest output

### Step 10: Write Integration Test

**Create**: `tests/integration/test_orientation_flow.py`

```python
"""Integration test for orientation shown-once behavior."""
import pytest


class TestOrientationFlow:
    """Test orientation appears only once."""

    @pytest.mark.integration
    async def test_orientation_dismiss_endpoint(self, test_client, authenticated_user):
        """Dismiss endpoint marks orientation as seen."""
        # Call dismiss endpoint
        response = test_client.post("/api/v1/orientation/dismiss")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
```

- **Expected outcome**: 1 integration test created
- **Validation**: `python -m pytest tests/integration/test_orientation_flow.py -v`
- **Evidence**: Show full pytest output

### Step 11: Git Commit

```bash
./scripts/fix-newlines.sh
git add services/database/models.py alembic/versions/*orientation* web/api/routes/ui.py templates/home.html tests/unit/templates/test_orientation.py tests/integration/test_orientation_flow.py
git commit -m "feat(ftux): Add post-setup orientation modal (#549)"
git log --oneline -1
```

- **Expected outcome**: Clean commit
- **Validation**: `git log --oneline -1`
- **Evidence**: Show commit hash and message

---

## Architecture Boundaries

This task spans multiple layers:
- **Domain Layer**: User model change (orientation_seen column)
- **Infrastructure Layer**: Database migration
- **Presentation Layer**: Template + route changes
- **Application Layer**: Dismiss endpoint

All changes follow existing patterns in each layer.

---

## Success Criteria (With Evidence)

- [ ] Infrastructure matches expectations (grep output)
- [ ] 11/11 elements complete (show completeness table)
- [ ] User model updated (show grep)
- [ ] Migration created and applied (show alembic output)
- [ ] Home route passes context (show grep)
- [ ] Dismiss endpoint works (show grep)
- [ ] Modal HTML added (show grep)
- [ ] Escape key handler added (show grep)
- [ ] All tests pass (show pytest output: 3 unit + 1 integration)
- [ ] GitHub issue updated (show issue link)
- [ ] Git commit clean (show `git log --oneline -1`)

---

## Deliverables

1. **Schema Change**: `services/database/models.py` - orientation_seen column
2. **Migration**: `alembic/versions/xxx_add_orientation_seen.py`
3. **Route Changes**: `web/api/routes/ui.py` - home context + dismiss endpoint
4. **Template Changes**: `templates/home.html` - modal HTML/CSS/JS
5. **Component Completeness**: 11/11 elements table
6. **Test Coverage**: 3 unit tests + 1 integration test
7. **Evidence Report**: Terminal output showing success
8. **GitHub Update**: Issue #549 updated with completion
9. **Git Status**: Clean repository with commit

---

## Cross-Validation Preparation

Leave clear markers for verification:
- File paths:
  - `services/database/models.py`
  - `alembic/versions/*orientation*`
  - `web/api/routes/ui.py`
  - `templates/home.html`
  - `tests/unit/templates/test_orientation.py`
  - `tests/integration/test_orientation_flow.py`
- Test commands:
  - `python -m pytest tests/unit/templates/test_orientation.py -v`
  - `python -m pytest tests/integration/test_orientation_flow.py -v`
- Expected test output: 3 unit passed + 1 integration passed
- Grep commands to verify:
  - `grep -n "orientation_seen" services/database/models.py`
  - `grep -n "dismiss_orientation" web/api/routes/ui.py`
  - `grep -n "orientation-modal" templates/home.html`
  - `grep -n "Escape" templates/home.html`

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. **Does infrastructure match what gameplan expected?**
2. **Is my implementation 100% complete (11/11 elements)?**
3. **Did I create AND apply the migration?**
4. **Did I add the dismiss endpoint?**
5. **Did I add keyboard accessibility (Escape key)?**
6. **Did I use database storage (NOT localStorage)?**
7. **Did I use correct endpoint `/api/v1/integrations/health`?**
8. **Did I parse integrations array correctly?**
9. **Did I provide terminal evidence for every claim?**
10. **Can another agent verify my work independently?**
11. **Am I claiming work done that I didn't actually do?**
12. **Did I verify git commits with log output?**
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
# Show User model updated
$ grep -n "orientation_seen" services/database/models.py
87:    orientation_seen = Column(Boolean, default=False, nullable=False)

# Show migration created
$ ls -la alembic/versions/*orientation*
-rw-r--r--  1 user  group  456 Jan  6 12:00 alembic/versions/abc123_add_orientation_seen.py

# Show migration applied
$ alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade xyz -> abc123, Add orientation_seen to users

# Show home route updated
$ grep -n "orientation_seen" web/api/routes/ui.py
125:        "orientation_seen": user.orientation_seen if user else True,

# Show dismiss endpoint
$ grep -n "dismiss_orientation" web/api/routes/ui.py
135:async def dismiss_orientation(request: Request):

# Show modal HTML
$ grep -n "orientation-modal" templates/home.html
245:<div id="orientation-modal" class="orientation-modal hidden"

# Show Escape handler
$ grep -n "Escape" templates/home.html
312:    if (e.key === 'Escape') {

# Show unit test results
$ python -m pytest tests/unit/templates/test_orientation.py -v
===== test session starts =====
tests/unit/templates/test_orientation.py::TestOrientationModal::test_orientation_modal_renders PASSED
tests/unit/templates/test_orientation.py::TestOrientationModal::test_orientation_has_required_elements PASSED
tests/unit/templates/test_orientation.py::TestOrientationModal::test_orientation_conditional_suggestions PASSED
===== 3 passed in 0.52s =====

# Show integration test results
$ python -m pytest tests/integration/test_orientation_flow.py -v
===== test session starts =====
tests/integration/test_orientation_flow.py::TestOrientationFlow::test_orientation_dismiss_endpoint PASSED
===== 1 passed in 1.23s =====

# Show git commit
$ git log --oneline -1
ghi9012 feat(ftux): Add post-setup orientation modal (#549)
```

---

## Related Documentation

- `docs/development/methodology-core/resource-map.md` - Resource locations
- `docs/internal/architecture/current/patterns/` - Pattern catalog
- `dev/active/gameplan-549-ftux-post-setup.md` - Full gameplan
- `services/database/models.py` - User model pattern reference

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:
1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. Checking what exists NEXT (no reinventing)
4. **Creating AND applying migration**
5. Following ALL verification requirements
6. Providing evidence for EVERY claim
7. Creating component completeness table
8. Stopping when assumptions are needed
9. Maintaining architectural integrity
10. Updating GitHub with progress
11. Creating session logs in .md format
12. Verifying git commits with log output
13. Providing grep/terminal proof for all claims
14. **Never guessing - always verifying first!**
15. **Never rationalizing incompleteness!**

**Infrastructure mismatches and completion bias are session failures. Evidence is mandatory.**

---

## Anti-Pattern Examples

### ❌ WRONG: Using localStorage Instead of Database
```
"Used localStorage for simplicity, works fine"
```
**Why wrong**: PM decided database storage - persists across browsers/devices!

### ✅ RIGHT: Database Storage
```
$ grep -n "orientation_seen" services/database/models.py
87:    orientation_seen = Column(Boolean, default=False, nullable=False)
```

### ❌ WRONG: Wrong Endpoint Path
```
const response = await fetch('/api/v1/integrations/status');
```
**Why wrong**: Endpoint is `/health` not `/status`!

### ✅ RIGHT: Correct Endpoint
```
$ grep -n "integrations/health" templates/home.html
295:        const response = await fetch('/api/v1/integrations/health');
```

### ❌ WRONG: Skipping Migration
```
"Added column to model, will create migration later"
```
**Why wrong**: Migration must be created AND applied!

### ✅ RIGHT: Complete Migration
```
$ alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade xyz -> abc123
```

### ❌ WRONG: Forgetting Keyboard Accessibility
```
"Modal works, user can click X to close"
```
**Why wrong**: Escape key handler is required for accessibility!

### ✅ RIGHT: Keyboard Accessible
```
$ grep -n "Escape" templates/home.html
312:    if (e.key === 'Escape') {
```

---

## STOP Conditions (17 Total)

If ANY of these occur, STOP and escalate:
1. Infrastructure doesn't match gameplan
2. Implementation <100% complete (11/11)
3. `setup_complete` doesn't exist on User model
4. Tests fail for any reason
5. Migration fails to create or apply
6. GitHub issue missing or unassigned
7. Can't provide verification evidence
8. Integration health endpoint missing
9. Resource not found after searching
10. Completion bias detected (claiming without proof)
11. Rationalizing gaps as "minor" or "optional"
12. GitHub tracking not working
13. Git operations failing
14. Server state unexpected
15. Database connection issues
16. Home route can't be modified
17. Keyboard accessibility missing

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

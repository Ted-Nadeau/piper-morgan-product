# Gameplan: Issue #548 FTUX-EMPTY-STATES

**Issue**: [#548](https://github.com/mediajunkie/piper-morgan-product/issues/548)
**Title**: Replace empty state copy with voice guide templates
**Sprint**: B1
**Estimated Effort**: 2-3 hours
**Created**: January 6, 2026
**Updated**: January 6, 2026 (PM decisions applied)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI with Jinja2 templates
- [x] Templates exist: `todos.html`, `projects.html`, `files.html`, `lists.html`
- [x] Empty state component: `templates/components/empty-state.html` exists (965 bytes)
- [x] Component is WCAG 2.2 AA accessible (role="status", aria-label)
- [x] Current empty states: Inline HTML with generic copy

**Current Empty State Patterns Found**:

| Template | Current Copy | Location (line) |
|----------|--------------|-----------------|
| todos.html | "No todos yet" / "Create your first todo" | L85-88, L138-141 |
| projects.html | "No projects yet" | L55-56, L108-109 |
| files.html | "No files yet" | L149-150, L201-202 |
| lists.html | "No lists yet" | L85-86, L138-139 |

**Component Interface** (`templates/components/empty-state.html`):
- `icon` - Emoji icon (optional, default 📭)
- `title` - Headline text
- `message` - Body text
- `cta_text` / `cta_url` - Optional CTA button
- `help_link` - Optional help link

### Part A.2: Work Characteristics Assessment

**Assessment**: **SKIP WORKTREE** - Single agent modifying 4 templates sequentially + component usage.

### Part B: PM Verification ✅ COMPLETE

**PM Decisions (January 6, 2026)**:
1. [x] **Option B: Component refactor** - Do it right the first time
2. [x] Voice guide copy in `dev/active/empty-state-voice-guide-v1.md` is authoritative
3. [x] **Add Lists to voice guide first** before implementing (prerequisite)
4. [x] **Include "all complete" states** (e.g., "All caught up! 🎯" for todos)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - After prerequisite (voice guide update) is complete

---

## Prerequisites

### Prerequisite 1: Update Voice Guide with Lists

Before implementing, the voice guide needs a Lists section.

**File**: `dev/active/empty-state-voice-guide-v1.md`

**Add after Projects section**:

```markdown
### Lists View

**State**: No lists created

```
No lists yet.

Lists help organize related items. Say "create a list called..."
to get started.
```
```

**Assignee**: Can be done by implementing agent or as separate micro-task.

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
```bash
gh issue view 548 --repo mediajunkie/piper-morgan-product
```

### Phase 0.5: Frontend-Backend Contract
**N/A** - This is a frontend-only change. No backend endpoints involved.

### STOP Conditions Check
- [x] All 4 template files exist at expected paths
- [x] Templates use server-rendered + JS-rendered pattern (understood)
- [x] Voice guide v1 is current (Jan 4, 2026)
- [x] Component interface compatible with voice guide
- [ ] Lists added to voice guide (PREREQUISITE)

**Result**: Proceed after prerequisite complete.

---

## Phase 1: Implementation (Component Refactor)

### Agent Deployment Map

| Phase | Agent | Task | Evidence Required |
|-------|-------|------|-------------------|
| 0 | Sonnet | Update voice guide with Lists section | File updated |
| 1 | Sonnet | Refactor todos.html to use component | Template uses component |
| 2 | Sonnet | Refactor projects.html | Template uses component |
| 3 | Sonnet | Refactor files.html | Template uses component |
| 4 | Sonnet | Refactor lists.html | Template uses component |
| 5 | Sonnet | Write unit tests | 5 tests passing |

### 1.0 Update Voice Guide (Prerequisite)

**File**: `dev/active/empty-state-voice-guide-v1.md`

Add Lists section after Projects (line ~177):

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

### 1.1 Refactor todos.html

**File**: `templates/todos.html`

**Location 1** (static HTML, ~L85-88) - Replace with:
```jinja2
{% set icon = '✅' %}
{% set title = 'No todos yet.' %}
{% set message = 'Say "add a todo: [your task]" to create one, or I can suggest some based on your open GitHub issues.' %}
{% include 'components/empty-state.html' %}
```

**Location 2** (JavaScript render, ~L138-141) - Keep inline but update copy:
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

### 1.2 Refactor projects.html

**File**: `templates/projects.html`

**Static HTML**:
```jinja2
{% set icon = '📁' %}
{% set title = 'No projects set up yet.' %}
{% set message = 'Projects help me understand your work context. Say "create a project called..." to get started.' %}
{% include 'components/empty-state.html' %}
```

**JavaScript render** - Update copy to match, keep inline structure.

### 1.3 Refactor files.html

**File**: `templates/files.html`

**Static HTML**:
```jinja2
{% set icon = '📄' %}
{% set title = 'No documents in your knowledge base yet.' %}
{% set message = 'You can upload files, connect Notion, or just paste content into our chat—I\'ll remember it for later.' %}
{% include 'components/empty-state.html' %}
```

**JavaScript render** - Update copy to match.

### 1.4 Refactor lists.html

**File**: `templates/lists.html`

**Static HTML**:
```jinja2
{% set icon = '📋' %}
{% set title = 'No lists yet.' %}
{% set message = 'Lists help organize related items. Say "create a list called..." to get started.' %}
{% include 'components/empty-state.html' %}
```

**JavaScript render** - Update copy to match.

---

## Phase 2: Testing

### 2.1 Unit Tests

**File**: `tests/unit/templates/test_empty_states.py`

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

### 2.2 Manual Verification Checklist

- [ ] Todos view (empty): New copy appears with ✅ icon
- [ ] Todos view (all complete): "All caught up! 🎯" appears
- [ ] Projects view (empty): New copy appears with 📁 icon
- [ ] Files view (empty): New copy appears with 📄 icon
- [ ] Lists view (empty): New copy appears with 📋 icon
- [ ] Tone check: Reads as colleague, not system message
- [ ] Copy demonstrates Piper grammar ("Say '...'")
- [ ] Mobile: All 4 views render correctly on mobile viewport
- [ ] Accessibility: role="status" present on all empty states

---

## Phase Z: Final Bookending & Handoff

### Acceptance Criteria Verification

- [ ] Todos view: Updated per voice guide template
- [ ] Projects view: Updated per voice guide template
- [ ] Files/Documents view: Updated per voice guide template
- [ ] Lists view: Updated per voice guide template
- [ ] Copy demonstrates Piper grammar (e.g., "Say 'add a todo: [task]'")
- [ ] Tone is colleague, not system (no "Click button to...")
- [ ] "All complete" state implemented for todos

### Test Evidence Required

```bash
python -m pytest tests/unit/templates/test_empty_states.py -v
```

### Files Modified

- `dev/active/empty-state-voice-guide-v1.md` - Added Lists section
- `templates/todos.html` - Refactored to use component, added "all complete" state
- `templates/projects.html` - Refactored to use component
- `templates/files.html` - Refactored to use component
- `templates/lists.html` - Refactored to use component
- `tests/unit/templates/test_empty_states.py` - NEW: 5 unit tests

### GitHub Issue Update

Update issue with evidence:
- Screenshots of all 4 empty states (showing new copy + icons)
- Screenshot of "All caught up!" state
- Test output
- Before/after comparison of copy

---

## STOP Conditions

- STOP if any template file doesn't exist at expected path
- STOP if templates use different empty state pattern than expected
- STOP if `empty-state-voice-guide-v1.md` has been superseded by v2
- STOP if component interface doesn't support required variables
- STOP if JS render locations can't be identified

---

*Gameplan Version: 1.1 | Updated: January 6, 2026 | PM decisions applied*

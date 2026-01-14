# Gameplan: Issue #547 FTUX-PIPER-INTRO

**Issue**: [#547](https://github.com/mediajunkie/piper-morgan-product/issues/547)
**Title**: Add Piper greeting to setup wizard start
**Sprint**: B1
**Estimated Effort**: 1-2 hours
**Created**: January 6, 2026
**Updated**: January 6, 2026 (PM decisions applied)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI with Jinja2 templates
- [x] Setup wizard: `templates/setup.html` - single-page wizard with CSS-hidden steps
- [x] Step structure: Uses `.setup-step` class with `.active` toggling via JavaScript
- [x] Storage: sessionStorage available for "intro seen" flag
- [x] No frontend framework (React/Vue) - pure Jinja2 + vanilla JS

**My understanding of the task**:
- Add **inline intro panel** that appears BEFORE Step 1 (System Requirements)
- Panel dismisses on CTA click, stores flag to prevent re-show on refresh
- Copy is provided in issue, follows voice guide tone
- This is a UI-only change, no backend endpoints needed

### Part A.2: Work Characteristics Assessment

**Assessment**: **SKIP WORKTREE** - Single file change, <2 hours, straightforward implementation.

### Part B: PM Verification ✅ COMPLETE

**PM Decisions (January 6, 2026)**:
1. [x] `templates/setup.html` is the correct file
2. [x] sessionStorage is acceptable for "intro seen" flag
3. [x] **Inline panel** (not overlay/modal) before Step 1
4. [x] Intro re-appearing after browser data clear is acceptable

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - All decisions made, understanding confirmed

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
```bash
gh issue view 547 --repo mediajunkie/piper-morgan-product
```

### Phase 0.5: Frontend-Backend Contract
**N/A** - This is a frontend-only change. No backend endpoints involved.

### STOP Conditions Check
- [x] Issue exists and is OPEN
- [x] Template structure matches expectations (wizard with steps)
- [x] Voice guide copy source confirmed
- [x] No frontend framework complications

**Result**: No STOP conditions triggered. Proceed to Phase 1.

---

## Phase 1: Implementation

### Agent Deployment Map

| Phase | Agent | Task | Evidence Required |
|-------|-------|------|-------------------|
| 1 | Sonnet | Implement intro panel HTML/CSS/JS | Template modified, manual test |
| 2 | Sonnet | Write unit tests | 2 tests passing |

### 1.1 Add Intro Panel HTML

**File**: `templates/setup.html`

Add before the first `.setup-step` div (inline panel, not overlay):

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

### 1.2 Add CSS Styling

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

### 1.3 Add JavaScript Logic

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

---

## Phase 2: Testing

### 2.1 Unit Tests

**File**: `tests/unit/templates/test_setup_intro.py`

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

### 2.2 Manual Verification Checklist

- [ ] Fresh browser session: Intro panel appears before Step 1
- [ ] Click "Let's get started": Panel hides, Step 1 appears with progress bar
- [ ] Refresh page: Intro does NOT reappear (sessionStorage works)
- [ ] Clear sessionStorage: Intro reappears
- [ ] Wizard still functions correctly after intro dismissal
- [ ] Desktop Chrome: Layout correct
- [ ] Desktop Safari: Layout correct
- [ ] Mobile viewport (375px): Responsive layout works

---

## Phase Z: Final Bookending & Handoff

### Acceptance Criteria Verification

- [ ] User sees Piper greeting before Step 1 system requirements
- [ ] Greeting follows voice guide tone (colleague, not system)
- [ ] Single "Let's get started" CTA to proceed to Step 1
- [ ] No new navigation step (inline panel, not new wizard step)
- [ ] Mobile responsive

### Test Evidence Required

```bash
python -m pytest tests/unit/templates/test_setup_intro.py -v
```

### Files Modified

- `templates/setup.html` - Added intro panel, CSS, JavaScript
- `tests/unit/templates/test_setup_intro.py` - NEW: 2 unit tests

### GitHub Issue Update

Update issue with evidence:
- Screenshot of intro panel (desktop)
- Screenshot of intro panel (mobile)
- Test output
- sessionStorage behavior confirmation
- Wizard flow still works after dismissal

---

## STOP Conditions

- STOP if `templates/setup.html` structure differs significantly from expected
- STOP if voice guide copy in `empty-state-voice-guide-v1.md` has been updated
- STOP if setup wizard uses frontend framework instead of Jinja templates
- STOP if wizard flow breaks after intro dismissal

---

*Gameplan Version: 1.1 | Updated: January 6, 2026 | PM decisions applied*

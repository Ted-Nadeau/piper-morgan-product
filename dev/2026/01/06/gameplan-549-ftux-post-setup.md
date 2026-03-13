# Gameplan: Issue #549 FTUX-POST-SETUP

**Issue**: [#549](https://github.com/mediajunkie/piper-morgan-product/issues/549)
**Title**: Add post-setup orientation
**Sprint**: B1
**Estimated Effort**: 2-3 hours
**Created**: January 6, 2026
**Updated**: January 6, 2026 (PM decisions applied)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI with Jinja2 templates
- [x] User model: Has `setup_complete` boolean field (verified: `services/database/models.py:85`)
- [x] User model: Has `setup_completed_at` timestamp field
- [x] Home page: `templates/home.html` - main landing after login
- [x] User preferences storage: Use User model column (follows `setup_complete` pattern)
- [x] Integration health: Available via `/api/v1/integrations/health` endpoint

**Database Model Verification**:
```python
# services/database/models.py:78-86 - Existing boolean flag pattern
is_active = Column(Boolean, default=True, nullable=False)
is_verified = Column(Boolean, default=False, nullable=False)
is_alpha = Column(Boolean, default=False, nullable=False)
is_admin = Column(Boolean, default=False, nullable=False)
setup_complete = Column(Boolean, default=False, nullable=False)
setup_completed_at = Column(DateTime, nullable=True)
# Will add: orientation_seen = Column(Boolean, default=False, nullable=False)
```

**Home Route Verification** (`web/api/routes/ui.py:115`):
```python
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Currently passes: request, user
    # Needs to add: setup_complete, orientation_seen
```

**Integration Health Endpoint** (`web/api/routes/integrations.py`):
- Router prefix: `/api/v1/integrations` (line 21)
- Endpoint: `GET /health` (line 162)
- Full path: `/api/v1/integrations/health`
- Returns: `IntegrationHealthResponse` with `integrations[]` array

### Part A.2: Work Characteristics Assessment

**Assessment**: **SKIP WORKTREE** - Single agent, sequential work. Migration is simple (one boolean column).

### Part B: PM Verification ✅ COMPLETE

**PM Decisions (January 6, 2026)**:
1. [x] **Storage**: User model column (follows `setup_complete` pattern)
2. [x] **Implementation**: Overlay modal on home.html
3. [x] **Edge cases**: No expiration needed - shown once, ever
4. [x] Worktree: Not needed

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - All decisions made, infrastructure verified

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
```bash
gh issue view 549 --repo mediajunkie/piper-morgan-product
```

### Phase 0.5: Frontend-Backend Contract

**Backend Changes Required**:

1. **User model**: Add `orientation_seen` column
   - File: `services/database/models.py`
   - Pattern: Follows existing boolean flags (`is_active`, `setup_complete`, etc.)

2. **Migration**: Add Alembic migration
   - Command: `alembic revision --autogenerate -m "Add orientation_seen to users"`

3. **Home route**: Pass additional context to template
   - File: `web/api/routes/ui.py:115`
   - Add: `setup_complete`, `orientation_seen` to template context

4. **New endpoint**: Mark orientation as seen
   - Path: `POST /api/v1/orientation/dismiss`
   - Action: Set `orientation_seen = True` for current user

**Frontend Changes Required**:

1. **Template**: Add modal HTML to `templates/home.html`
2. **CSS**: Add modal styles (inline or separate file)
3. **JavaScript**:
   - Init logic checking `setup_complete` AND NOT `orientation_seen`
   - Fetch `/api/v1/integrations/health` for conditional suggestions
   - Dismiss function calling `POST /api/v1/orientation/dismiss`

### STOP Conditions Check
- [x] `user.setup_complete` flag exists in user model
- [x] User model boolean pattern verified (6 existing fields)
- [x] Home page template compatible with modal overlay
- [x] Integration health endpoint verified (`/api/v1/integrations/health`)

**Result**: Proceed to Phase 1.

---

## Phase 1: Implementation (User Model Column + Overlay Modal)

### Agent Deployment Map

| Phase | Agent | Task | Evidence Required |
|-------|-------|------|-------------------|
| 1 | Sonnet | Add migration + update User model | Migration file, model updated |
| 2 | Sonnet | Update home route to pass context | Route passes setup_complete, orientation_seen |
| 3 | Sonnet | Add dismiss endpoint | POST endpoint returns 200 |
| 4 | Sonnet | Add modal HTML/CSS/JS to home.html | Template renders modal |
| 5 | Sonnet | Write unit tests | 3 unit tests passing |
| 6 | Sonnet | Write integration test | 1 integration test passing |

### 1.1 Add Migration

```bash
alembic revision --autogenerate -m "Add orientation_seen to users"
```

**Migration content**:
```python
def upgrade():
    op.add_column('users', sa.Column('orientation_seen', sa.Boolean(),
                                      nullable=False, server_default='false'))

def downgrade():
    op.drop_column('users', 'orientation_seen')
```

### 1.2 Update User Model

**File**: `services/database/models.py`

Add after `setup_completed_at` (around line 86):
```python
orientation_seen = Column(Boolean, default=False, nullable=False)
```

### 1.3 Update Home Route

**File**: `web/api/routes/ui.py`

```python
@router.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: JWTClaims = Depends(get_current_user)):
    # Get user from database for setup/orientation status
    user = await get_user_by_id(current_user.sub)

    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": user,
        "setup_complete": user.setup_complete if user else False,
        "orientation_seen": user.orientation_seen if user else True,  # Default to True (don't show) if no user
    })
```

### 1.4 Add Dismiss Endpoint

**File**: `web/api/routes/ui.py` (or create `web/api/routes/orientation.py`)

```python
@router.post("/api/v1/orientation/dismiss")
async def dismiss_orientation(
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark orientation as seen for current user."""
    user = await get_user_by_id(current_user.sub, db)
    if user:
        user.orientation_seen = True
        await db.commit()
    return {"status": "ok"}
```

### 1.5 Add Orientation Modal HTML

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

### 1.6 Add CSS Styling

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

### 1.7 Add JavaScript Logic

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

---

## Phase 2: Testing

### 2.1 Unit Tests

**File**: `tests/unit/templates/test_orientation.py`

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

### 2.2 Integration Test

**File**: `tests/integration/test_orientation_flow.py`

```python
"""Integration test for orientation shown-once behavior."""
import pytest


class TestOrientationFlow:
    """Test orientation appears only once."""

    @pytest.mark.integration
    async def test_orientation_dismiss_endpoint(self, test_client, setup_complete_user):
        """Dismiss endpoint marks orientation as seen."""
        # Call dismiss endpoint
        response = test_client.post("/api/v1/orientation/dismiss")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

        # Verify user's orientation_seen is now True
        # (Implementation depends on test fixtures)
```

### 2.3 Manual Verification Checklist

- [ ] User completes setup, logs in: Orientation modal appears
- [ ] Click "Get started": Modal dismisses
- [ ] Refresh page: Modal does NOT reappear
- [ ] New browser/device: Modal does NOT reappear (database persistence)
- [ ] GitHub connected: GitHub suggestion visible
- [ ] GitHub not connected: GitHub suggestion hidden
- [ ] Calendar connected: Calendar suggestion visible
- [ ] Calendar not connected: Calendar suggestion hidden
- [ ] Click X button: Modal dismisses
- [ ] Click backdrop: Modal dismisses
- [ ] Press Escape: Modal dismisses
- [ ] Desktop Chrome: Layout correct
- [ ] Desktop Safari: Layout correct
- [ ] Mobile viewport (375px): Responsive layout works

---

## Phase Z: Final Bookending & Handoff

### Acceptance Criteria Verification

- [ ] User sees orientation after first successful login post-setup
- [ ] Orientation shows 2-3 contextual starting suggestions
- [ ] Suggestions are based on connected integrations
- [ ] Single dismissal takes user to home (not shown again)
- [ ] Persists across browsers/devices (database storage)
- [ ] Can be skipped/dismissed immediately
- [ ] Mobile responsive
- [ ] Keyboard accessible (Escape to close)

### Test Evidence Required

```bash
python -m pytest tests/unit/templates/test_orientation.py -v
python -m pytest tests/integration/test_orientation_flow.py -v
```

### Files Modified

- `services/database/models.py` - Add `orientation_seen` column
- `alembic/versions/xxx_add_orientation_seen.py` - NEW migration
- `web/api/routes/ui.py` - Pass context + add dismiss endpoint
- `templates/home.html` - Added modal HTML, CSS, JavaScript
- `tests/unit/templates/test_orientation.py` - NEW: 3 unit tests
- `tests/integration/test_orientation_flow.py` - NEW: 1 integration test

### GitHub Issue Update

Update issue with evidence:
- Screenshot of orientation modal (desktop)
- Screenshot of orientation modal (mobile)
- Screenshot showing conditional GitHub suggestion
- Test output
- Confirmation of "shown once" behavior across page refresh AND across browsers

---

## STOP Conditions

- STOP if `user.setup_complete` flag doesn't exist in user model
- STOP if home page template structure incompatible with modal overlay
- STOP if `/api/v1/integrations/health` endpoint doesn't exist or returns different format
- STOP if migration fails to apply
- STOP if home route can't be modified to pass additional context

---

*Gameplan Version: 1.1 | Updated: January 6, 2026 | PM decisions applied*

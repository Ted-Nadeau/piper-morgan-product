# Gameplan: Issue #578 - GitHub Personal Access Token Configuration in UI

**Issue**: #578 ENHANCE-GITHUB-PAT-UI
**Created**: 2026-01-11
**Status**: Ready for Implementation
**Estimated Effort**: Small (~1.5 hours total)

---

## Overview

Add UI for configuring GitHub Personal Access Token (PAT) in Settings page, following the pattern established by #576 (Slack) and #577 (Calendar).

**Key Difference from #576/#577**: Single token field vs client_id/secret pair - simpler implementation.

---

## Phase -1: Infrastructure Verification (10 min)

### Objective
Verify all infrastructure assumptions before writing code.

### Verification Checklist

```bash
# 1. Verify KeychainService exists and works
ls -la services/infrastructure/keychain_service.py

# 2. Verify GitHubConfigService exists
ls -la services/integrations/github/

# 3. Verify settings_github.html exists
ls -la templates/settings_github.html

# 4. Verify settings_integrations.py route file
ls -la web/api/routes/settings_integrations.py

# 5. Check existing GitHub endpoints pattern
grep -n "github" web/api/routes/settings_integrations.py
```

### Expected Infrastructure
- `KeychainService` at `services/infrastructure/keychain_service.py` ✓
- GitHub integration at `services/integrations/github/` ✓
- Settings template at `templates/settings_github.html` ✓
- Routes at `web/api/routes/settings_integrations.py` ✓

### Keychain Key
- Key name: `github_token` (following existing pattern)

---

## Phase 0: Investigation (10 min)

### Objective
Understand existing GitHub credential loading before modifying.

### Investigation Tasks

1. **Read GitHubConfigService** (if exists) or find where GitHub token is loaded:
   ```bash
   find services/integrations/github -name "*.py" -exec grep -l "token\|TOKEN" {} \;
   ```

2. **Check existing settings_github.html structure**:
   - What UI elements exist?
   - Is there already a token configuration section?

3. **Review #577 implementation** for pattern consistency:
   - `web/api/routes/settings_integrations.py` - Calendar credential endpoints
   - `templates/settings_calendar.html` - App Configuration card

### Key Questions to Answer
- Where does GitHub currently load its token from?
- What's the credential priority order? (env > config > keychain)
- Does `settings_github.html` have existing structure we can extend?

---

## Phase 0.5: Frontend-Backend Contract (5 min)

### Objective
Confirm API design before implementation.

### API Contract

**Endpoint 1: Save Token**
```
POST /api/v1/settings/integrations/github/token
Content-Type: application/json

Request:
{
  "token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}

Response (200):
{
  "success": true,
  "message": "GitHub token saved securely"
}
```

**Endpoint 2: Check Status**
```
GET /api/v1/settings/integrations/github/token/status

Response (200):
{
  "configured": true  // or false
}
```

### Verification
```bash
# After implementation, verify endpoints exist:
curl -s http://localhost:8001/api/v1/settings/integrations/github/token/status
# Expected: 401 (auth required) or 200 with JSON
```

---

## Phase 1: Backend API (30 min)

### 1.1 Add Pydantic Models

**File**: `web/api/routes/settings_integrations.py`

Add after existing Calendar models (~line 102):

```python
class GitHubTokenRequest(BaseModel):
    """Request body for saving GitHub Personal Access Token."""
    token: str


class GitHubTokenStatusResponse(BaseModel):
    """Response for GitHub token status check (never exposes actual token)."""
    configured: bool
```

### 1.2 Add POST Endpoint

**File**: `web/api/routes/settings_integrations.py`

Add after Calendar endpoints:

```python
@router.post("/github/token")
async def save_github_token(
    request: GitHubTokenRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save GitHub Personal Access Token to keychain.

    Issue #578: ENHANCE-GITHUB-PAT-UI
    """
    from services.infrastructure.keychain_service import KeychainService

    keychain = KeychainService()
    keychain.store_api_key("github_token", request.token.strip())

    logger.info(
        "github_token_saved",
        user_id=current_user.sub,
    )

    return {"success": True, "message": "GitHub token saved securely"}
```

### 1.3 Add GET Status Endpoint

```python
@router.get("/github/token/status", response_model=GitHubTokenStatusResponse)
async def get_github_token_status(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Check if GitHub token is configured.

    Issue #578: ENHANCE-GITHUB-PAT-UI
    Never returns the actual token value.
    Priority: env vars > keychain
    """
    import os
    from services.infrastructure.keychain_service import KeychainService

    # Check env vars first (multiple GitHub token env var names)
    token = os.getenv("GITHUB_TOKEN", "") or os.getenv("GITHUB_API_TOKEN", "") or os.getenv("GH_TOKEN", "")

    # Fallback to keychain
    if not token:
        keychain = KeychainService()
        token = keychain.get_api_key("github_token") or ""

    return GitHubTokenStatusResponse(
        configured=bool(token)
    )
```

### 1.4 Update GitHub Token Loading (if needed)

**File**: Find where GitHub loads its token and add keychain fallback.

Check `services/integrations/github/` for config loading. Add keychain as final fallback:

```python
# Priority: env vars > PIPER.user.md > keychain
if not self.token:
    try:
        from services.infrastructure.keychain_service import KeychainService
        keychain = KeychainService()
        self.token = keychain.get_api_key("github_token") or ""
    except Exception:
        pass
```

---

## Phase 2: Settings Page UI (30 min)

### 2.1 Add CSS (if needed)

**File**: `templates/settings_github.html`

The CSS from Calendar (#577) should work. Add if not present:

```css
/* Token Configuration Card (Issue #578) */
.token-config-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.token-config-card h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.token-config-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}

.token-config-status.configured {
  background: #d4edda;
  color: #155724;
}

.token-config-status.not-configured {
  background: #f8d7da;
  color: #721c24;
}
```

### 2.2 Add HTML Card

**File**: `templates/settings_github.html`

Add Token Configuration card (insert before any existing OAuth card):

```html
<!-- Token Configuration Card (Issue #578) -->
<div class="token-config-card" id="token-config-card">
  <h3>🔑 Access Token Configuration</h3>
  <p class="description">
    Configure your GitHub Personal Access Token for API access.
  </p>
  <a href="https://github.com/settings/tokens" target="_blank" class="help-link">
    📖 Create a token on GitHub Settings → Developer settings → Personal access tokens
  </a>

  <p class="help-text" style="margin: 12px 0; font-size: 13px; color: #7f8c8d;">
    Recommended scopes: <code>repo</code>, <code>read:user</code>
  </p>

  <!-- Status indicator -->
  <div id="token-config-status" class="token-config-status not-configured">
    <span id="token-config-status-icon">❌</span>
    <span id="token-config-status-text">Checking token...</span>
  </div>

  <!-- Configuration form -->
  <div id="token-config-form" style="display: none;">
    <div class="config-form-group">
      <label for="github-token">Personal Access Token</label>
      <input type="password" id="github-token" placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" />
      <p class="help-text">Your token is stored securely and never displayed after saving.</p>
    </div>

    <div class="config-button-group">
      <button class="btn btn-primary" id="save-token-btn" onclick="saveGitHubToken()">
        Save Token
      </button>
      <button class="btn btn-secondary" id="cancel-token-btn" onclick="cancelTokenEdit()" style="display: none;">
        Cancel
      </button>
    </div>
  </div>

  <!-- Configured view -->
  <div id="token-config-configured" style="display: none;">
    <button class="btn btn-secondary" onclick="showTokenForm()">
      Update Token
    </button>
  </div>
</div>
```

### 2.3 Add JavaScript Functions

**File**: `templates/settings_github.html` (in `<script>` section)

```javascript
// ============================================================================
// Token Configuration Functions (Issue #578)
// ============================================================================

let tokenConfigured = false;

async function loadTokenStatus() {
  try {
    const response = await fetch('/api/v1/settings/integrations/github/token/status');
    if (!response.ok) {
      updateTokenConfigUI(false);
      return;
    }

    const data = await response.json();
    tokenConfigured = data.configured;
    updateTokenConfigUI(data.configured);
  } catch (error) {
    console.error('Failed to load token status:', error);
    updateTokenConfigUI(false);
  }
}

function updateTokenConfigUI(configured) {
  const statusEl = document.getElementById('token-config-status');
  const statusIconEl = document.getElementById('token-config-status-icon');
  const statusTextEl = document.getElementById('token-config-status-text');
  const formEl = document.getElementById('token-config-form');
  const configuredEl = document.getElementById('token-config-configured');
  const cancelBtn = document.getElementById('cancel-token-btn');

  if (configured) {
    statusEl.className = 'token-config-status configured';
    statusIconEl.textContent = '✅';
    statusTextEl.textContent = 'GitHub token configured';
    formEl.style.display = 'none';
    configuredEl.style.display = 'block';
  } else {
    statusEl.className = 'token-config-status not-configured';
    statusIconEl.textContent = '❌';
    statusTextEl.textContent = 'GitHub token not configured';
    formEl.style.display = 'block';
    configuredEl.style.display = 'none';
    cancelBtn.style.display = 'none';
  }
}

function showTokenForm() {
  const formEl = document.getElementById('token-config-form');
  const configuredEl = document.getElementById('token-config-configured');
  const cancelBtn = document.getElementById('cancel-token-btn');

  formEl.style.display = 'block';
  configuredEl.style.display = 'none';
  if (tokenConfigured) {
    cancelBtn.style.display = 'block';
  }
  document.getElementById('github-token').value = '';
}

function cancelTokenEdit() {
  const formEl = document.getElementById('token-config-form');
  const configuredEl = document.getElementById('token-config-configured');

  formEl.style.display = 'none';
  configuredEl.style.display = 'block';
  document.getElementById('github-token').value = '';
}

async function saveGitHubToken() {
  const token = document.getElementById('github-token').value.trim();

  if (!token) {
    showToast('error', 'Token is required', 'Validation Error');
    return;
  }

  const saveBtn = document.getElementById('save-token-btn');
  saveBtn.disabled = true;
  saveBtn.textContent = 'Saving...';

  try {
    const response = await fetch('/api/v1/settings/integrations/github/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: token })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to save token');
    }

    const data = await response.json();
    if (data.success) {
      showToast('success', 'GitHub token saved securely', 'Token Saved');
      tokenConfigured = true;
      updateTokenConfigUI(true);
      document.getElementById('github-token').value = '';
    } else {
      throw new Error(data.message || 'Failed to save token');
    }
  } catch (error) {
    console.error('Failed to save token:', error);
    showToast('error', error.message, 'Save Failed');
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = 'Save Token';
  }
}
```

### 2.4 Update DOMContentLoaded

Add to existing `DOMContentLoaded`:

```javascript
document.addEventListener('DOMContentLoaded', function() {
  loadTokenStatus();  // Issue #578
  // ... existing code
});
```

---

## Phase 3: Testing (15 min)

### 3.1 Unit Tests

**File**: `tests/unit/web/api/routes/test_settings_github.py` (create or extend)

```python
"""
Unit tests for GitHub Token Settings API
Issue #578: ENHANCE-GITHUB-PAT-UI
"""

from unittest.mock import MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    GitHubTokenRequest,
    get_github_token_status,
    save_github_token,
)


class TestGitHubToken:
    """Tests for GitHub token endpoints (Issue #578)"""

    @pytest.mark.asyncio
    async def test_save_token_stores_in_keychain(self):
        """Should store token in keychain"""
        mock_keychain = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        request = GitHubTokenRequest(token="ghp_test_token_value")

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await save_github_token(request, mock_user)

            assert result["success"] is True
            mock_keychain.store_api_key.assert_called_once_with(
                "github_token", "ghp_test_token_value"
            )

    @pytest.mark.asyncio
    async def test_save_token_strips_whitespace(self):
        """Should strip whitespace from token"""
        mock_keychain = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        request = GitHubTokenRequest(token="  ghp_token_with_spaces  ")

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            await save_github_token(request, mock_user)

            mock_keychain.store_api_key.assert_called_once_with(
                "github_token", "ghp_token_with_spaces"
            )

    @pytest.mark.asyncio
    async def test_get_status_returns_configured_from_keychain(self):
        """Should return configured=True when token in keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "ghp_stored_token"
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_github_token_status(mock_user)

            assert result.configured is True

    @pytest.mark.asyncio
    async def test_get_status_returns_configured_from_env(self):
        """Should return configured=True when token in env var"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = ""
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_env_token"}),
        ):
            result = await get_github_token_status(mock_user)

            assert result.configured is True

    @pytest.mark.asyncio
    async def test_get_status_returns_not_configured(self):
        """Should return configured=False when no token"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = ""
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_github_token_status(mock_user)

            assert result.configured is False
```

### 3.2 Run Tests

```bash
python -m pytest tests/unit/web/api/routes/test_settings_github.py -xvs
```

---

## Phase Z: Final Bookending (10 min)

### Checklist

- [ ] All tests pass
- [ ] Pre-commit hooks pass (`./scripts/fix-newlines.sh`)
- [ ] Commit with proper message
- [ ] Update GitHub issue with evidence
- [ ] Close issue

### Commit Message Template

```
feat(#578): Add GitHub PAT configuration UI in Settings

Implements UI for configuring GitHub Personal Access Token in Settings page.

Changes:
- Backend: Add /github/token POST and GET status endpoints
- Settings page: Add Token Configuration card with form
- Tests: Add 5 unit tests for GitHub token endpoints

Follows same pattern as Slack (#576) and Calendar (#577) OAuth UI.
Token stored securely in OS keychain.

Issue: #578

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### GitHub Issue Closure Comment Template

```markdown
## Implementation Complete

### Implementation Evidence

**Commits:**
- `XXXXXXXX` - feat(#578): Add GitHub PAT configuration UI in Settings

**Files Modified:**
1. `web/api/routes/settings_integrations.py` - Two new endpoints
2. `templates/settings_github.html` - Token Configuration card
3. `tests/unit/web/api/routes/test_settings_github.py` - 5 new tests

**API Endpoints:**
- `POST /api/v1/settings/integrations/github/token` - Save token
- `GET /api/v1/settings/integrations/github/token/status` - Check status

**Keychain Key:** `github_token`

**Test Results:**
[paste test output]

**User Verification:**
1. Navigate to Settings → GitHub → Token Configuration card visible
2. Enter token → Stored securely in OS keychain
3. Status indicator shows ✅ when configured
```

---

## Files to Modify Summary

| File | Changes |
|------|---------|
| `web/api/routes/settings_integrations.py` | Add models + 2 endpoints |
| `templates/settings_github.html` | Add CSS + HTML card + JavaScript |
| `tests/unit/web/api/routes/test_settings_github.py` | Create with 5 tests |

---

## Risk Assessment

**Low Risk**: This follows established patterns from #576 and #577. Single token is simpler than OAuth credentials.

**Potential Issues**:
- `settings_github.html` may have different structure than Calendar/Slack - adapt as needed
- GitHub may already have some token UI - investigate in Phase 0

---

_Gameplan created: 2026-01-11_
_Template version: 9.2_

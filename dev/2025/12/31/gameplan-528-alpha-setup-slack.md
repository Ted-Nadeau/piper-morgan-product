# Gameplan: #528 ALPHA-SETUP-SLACK

**Issue**: Add Slack OAuth to setup wizard
**Priority**: Alpha Critical
**Created**: 2025-12-31 21:15
**Author**: Claude Code (Opus)

---

## Executive Summary

Add Slack OAuth flow to the setup wizard. Unlike #527 (Notion API key), Slack requires OAuth redirect flow - user clicks "Connect to Slack", gets redirected to Slack authorization, then returned to wizard.

**Key insight from investigation**: Complete OAuth infrastructure already exists in `SlackOAuthHandler` and `SlackWebhookRouter`. The main work is integrating this into the setup wizard flow with proper callback routing back to the wizard.

---

## Phase -1: Investigation Summary

### Existing Infrastructure

**OAuth Handler** (`services/integrations/slack/oauth_handler.py`):
- `SlackOAuthHandler.generate_authorization_url()` - creates OAuth URL with state
- `SlackOAuthHandler.handle_oauth_callback()` - exchanges code for tokens
- State management with 15-minute expiration
- Spatial workspace initialization on success
- Token storage mechanism

**Webhook Router** (`services/integrations/slack/webhook_router.py`):
- `/slack/oauth/authorize` - generates OAuth URL
- `/slack/oauth/callback` - handles callback from Slack
- Already integrated with `SlackOAuthHandler`

**Config Service** (`services/integrations/slack/config_service.py`):
- `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `SLACK_REDIRECT_URI` env vars
- `SlackConfig.redirect_uri` field

### What's Missing

1. **Setup wizard OAuth trigger**: UI button to launch OAuth from wizard
2. **Setup-specific callback**: Callback that returns user to setup wizard (not just `/slack/oauth/callback`)
3. **Setup wizard status**: Show Slack connection status in wizard
4. **Dashboard configure link**: Point to OAuth flow (like Notion points to setup wizard)

---

## Acceptance Criteria (from issue, simplified for MVP)

- [x] OAuth flow launches from wizard (click "Connect to Slack")
- [x] Returns to wizard after OAuth success/failure
- [x] Workspace name displayed after successful auth
- [x] Error messages for: denied, timeout, expired state
- [x] Dashboard "Configure" button points to setup wizard

**Out of Scope for MVP** (tracked in future issue):
- Channel selection UI (use default channel for now)
- Permission display (just show connected status)
- Enterprise Grid support

---

## Phase 0: TDD Test Scaffolding

**File**: `tests/unit/web/api/routes/test_setup_slack.py`

```python
"""
Unit tests for Slack OAuth in setup wizard
Issue #528: ALPHA-SETUP-SLACK
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

pytestmark = pytest.mark.unit


class TestSlackOAuthTrigger:
    """Tests for initiating Slack OAuth from setup wizard"""

    @pytest.mark.asyncio
    async def test_get_slack_oauth_url_returns_authorization_url(self):
        """Should return Slack OAuth URL with state"""
        pass

    @pytest.mark.asyncio
    async def test_oauth_url_includes_required_scopes(self):
        """OAuth URL should include bot scopes"""
        pass


class TestSlackOAuthCallback:
    """Tests for OAuth callback handling in setup context"""

    @pytest.mark.asyncio
    async def test_callback_success_returns_workspace_info(self):
        """Successful callback should return workspace name and ID"""
        pass

    @pytest.mark.asyncio
    async def test_callback_error_returns_error_message(self):
        """OAuth error should return user-friendly error"""
        pass

    @pytest.mark.asyncio
    async def test_callback_invalid_state_returns_error(self):
        """Invalid/expired state should return clear error"""
        pass


class TestSlackSetupStatus:
    """Tests for Slack status in setup wizard"""

    @pytest.mark.asyncio
    async def test_check_slack_configured_with_token(self):
        """Should return configured=True when bot token exists"""
        pass

    @pytest.mark.asyncio
    async def test_check_slack_not_configured(self):
        """Should return configured=False when no token"""
        pass
```

---

## Phase 1: Backend - Setup OAuth Endpoints

### 1.1 Add OAuth Endpoints to Setup Routes

**File**: `web/api/routes/setup.py`

**New endpoints**:

```python
# GET /setup/slack/oauth/start
# Returns: { "auth_url": "https://slack.com/oauth/...", "state": "..." }

@router.get("/slack/oauth/start")
async def start_slack_oauth():
    """
    Generate Slack OAuth URL for setup wizard.

    Issue #528: ALPHA-SETUP-SLACK
    """
    from services.integrations.slack.oauth_handler import SlackOAuthHandler

    handler = SlackOAuthHandler()

    # Use setup-specific redirect URI
    # This returns user to wizard instead of general callback
    redirect_uri = os.getenv("SLACK_SETUP_REDIRECT_URI",
                            os.getenv("SLACK_REDIRECT_URI", ""))

    auth_url, state = handler.generate_authorization_url(
        redirect_uri=redirect_uri
    )

    return {
        "auth_url": auth_url,
        "state": state,
    }


# GET /setup/slack/oauth/callback?code=...&state=...
# Returns: { "success": true, "workspace_name": "..." }

@router.get("/slack/oauth/callback")
async def handle_slack_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Slack OAuth callback for setup wizard.

    Returns user to setup wizard with success/error status.
    Issue #528: ALPHA-SETUP-SLACK
    """
    from services.integrations.slack.oauth_handler import SlackOAuthHandler

    if error:
        return RedirectResponse(
            url=f"/setup?slack_error={error}#step-2",
            status_code=302
        )

    if not code or not state:
        return RedirectResponse(
            url="/setup?slack_error=missing_params#step-2",
            status_code=302
        )

    try:
        handler = SlackOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        workspace_name = result.get("workspace", {}).get("workspace_name", "")

        # Redirect back to setup wizard with success
        return RedirectResponse(
            url=f"/setup?slack_success=true&slack_workspace={workspace_name}#step-2",
            status_code=302
        )
    except Exception as e:
        logger.error(f"Slack OAuth callback error: {e}")
        return RedirectResponse(
            url=f"/setup?slack_error=callback_failed#step-2",
            status_code=302
        )


# GET /setup/slack/status
# Returns: { "configured": true, "workspace_name": "..." }

@router.get("/setup/slack/status")
async def get_slack_status():
    """
    Get Slack configuration status for setup wizard.

    Issue #528: ALPHA-SETUP-SLACK
    """
    from services.integrations.slack.config_service import SlackConfigService

    config = SlackConfigService()
    slack_config = config.get_config()

    if slack_config.bot_token:
        # Could add workspace name lookup here
        return {
            "configured": True,
            "message": "Slack connected",
        }
    else:
        return {
            "configured": False,
            "message": "Not connected",
        }
```

### 1.2 Update Integrations Dashboard Configure URL

**File**: `web/api/routes/integrations.py`

```python
"slack": {
    "display_name": "Slack",
    "icon": "💬",
    "configure_url": "/setup#step-2",  # Changed from /settings/integrations/slack
    ...
}
```

---

## Phase 2: Frontend - Setup Wizard UI

### 2.1 Add Slack OAuth Section to Step 2

**File**: `templates/setup.html`

After Notion section (line ~209), add:

```html
<div class="form-group">
    <label>Slack Integration (optional)</label>
    <div class="slack-oauth-section">
        <div id="slack-not-connected" class="oauth-status">
            <button type="button" id="connect-slack-btn" class="auth-button slack-connect-btn">
                Connect to Slack
            </button>
            <small>Connect your Slack workspace to enable messaging</small>
        </div>
        <div id="slack-connected" class="oauth-status" style="display: none;">
            <div class="connected-status">
                <span class="status-icon">✓</span>
                <span id="slack-workspace-name">Connected</span>
            </div>
            <button type="button" id="disconnect-slack-btn" class="btn-secondary btn-sm">
                Disconnect
            </button>
        </div>
        <div id="slack-error" class="validation-status invalid" style="display: none;"></div>
    </div>
</div>
```

**Add CSS** (inline or in auth.css):

```css
.slack-connect-btn {
    background: #4A154B;  /* Slack purple */
    color: white;
}
.slack-connect-btn:hover {
    background: #3E1041;
}
.connected-status {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px;
    background: #d4edda;
    border-radius: 8px;
    color: #155724;
}
.oauth-status {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
```

### 2.2 Add Slack JavaScript

**File**: `web/static/js/setup.js`

```javascript
// State tracking
let slackConnected = false;

// On page load, check for OAuth callback params
document.addEventListener('DOMContentLoaded', function() {
    checkSlackCallbackParams();
    checkSlackStatus();
});

function checkSlackCallbackParams() {
    const params = new URLSearchParams(window.location.search);

    if (params.get('slack_success') === 'true') {
        const workspace = params.get('slack_workspace') || 'Workspace';
        showSlackConnected(workspace);
        // Clean URL
        window.history.replaceState({}, document.title, '/setup#step-2');
    } else if (params.get('slack_error')) {
        const error = params.get('slack_error');
        showSlackError(getSlackErrorMessage(error));
        window.history.replaceState({}, document.title, '/setup#step-2');
    }
}

async function checkSlackStatus() {
    try {
        const response = await fetch('/setup/slack/status');
        const data = await response.json();

        if (data.configured) {
            showSlackConnected(data.workspace_name || 'Connected');
        }
    } catch (err) {
        console.log('Slack status check failed:', err);
    }
}

async function connectSlack() {
    try {
        const response = await fetch('/setup/slack/oauth/start');
        const data = await response.json();

        if (data.auth_url) {
            // Redirect to Slack OAuth
            window.location.href = data.auth_url;
        } else {
            showSlackError('Failed to start OAuth flow');
        }
    } catch (err) {
        showSlackError('Connection failed. Please try again.');
    }
}

function showSlackConnected(workspace) {
    document.getElementById('slack-not-connected').style.display = 'none';
    document.getElementById('slack-connected').style.display = 'flex';
    document.getElementById('slack-workspace-name').textContent = `Connected to ${workspace}`;
    document.getElementById('slack-error').style.display = 'none';
    slackConnected = true;
}

function showSlackError(message) {
    document.getElementById('slack-error').textContent = message;
    document.getElementById('slack-error').style.display = 'block';
}

function getSlackErrorMessage(error) {
    const messages = {
        'access_denied': 'Authorization was denied. Please try again.',
        'missing_params': 'OAuth callback missing parameters.',
        'callback_failed': 'Failed to complete authorization.',
        'invalid_state': 'Session expired. Please try again.',
    };
    return messages[error] || 'An error occurred. Please try again.';
}

// Event listeners
document.getElementById('connect-slack-btn')?.addEventListener('click', connectSlack);
```

---

## Phase 3: CLI Wizard Extension

**File**: `scripts/setup_wizard.py`

Add Slack OAuth section after Notion:

```python
# Slack (optional) - Issue #528: ALPHA-SETUP-SLACK
print("\n   Slack Integration (optional):")
print("   Note: Slack requires OAuth authorization via web browser.")
print("   Run 'python main.py' and visit /setup to connect Slack,")
print("   or set SLACK_BOT_TOKEN environment variable directly.")

# Check if already configured
if os.environ.get("SLACK_BOT_TOKEN"):
    print("   ✓ Slack already configured (SLACK_BOT_TOKEN found)")
else:
    print("   ℹ️  Slack not configured (connect via web setup wizard)")
```

---

## Phase 4: Integration Testing

### Manual Test Scenarios

| Scenario | Steps | Expected |
|----------|-------|----------|
| Happy path | Click Connect → Authorize in Slack → Return | Shows "Connected to [Workspace]" |
| User denies | Click Connect → Deny in Slack | Shows error, can retry |
| Expired state | Wait 16 min after clicking Connect → Complete in Slack | Shows "session expired" error |
| Already connected | Visit setup with existing token | Shows connected status |

### Integration Test File

**File**: `tests/integration/test_setup_slack.py`

```python
"""
Integration tests for Slack OAuth in setup wizard
Issue #528: ALPHA-SETUP-SLACK
"""
import pytest

pytestmark = pytest.mark.integration


class TestSlackOAuthFlow:
    """Full OAuth flow tests (require mocked Slack responses)"""

    @pytest.mark.asyncio
    async def test_full_oauth_flow_success(self):
        """Complete OAuth flow with mocked Slack"""
        pass

    @pytest.mark.asyncio
    async def test_oauth_callback_redirects_to_setup(self):
        """Callback should redirect back to setup wizard"""
        pass
```

---

## Completion Matrix

| Phase | Deliverable | Verification |
|-------|-------------|--------------|
| 0 | Test scaffolding | `pytest tests/unit/web/api/routes/test_setup_slack.py --collect-only` |
| 1 | Backend endpoints | Tests pass, curl commands work |
| 2 | Frontend integration | Manual test in browser |
| 3 | CLI message | `python main.py setup` shows Slack section |
| 4 | Integration tests | All tests pass |

---

## STOP Conditions

- [ ] If `SlackOAuthHandler` fails with current config → STOP, verify Slack app settings
- [ ] If redirect URI mismatch → STOP, update Slack app OAuth settings
- [ ] If tests fail → STOP, fix before proceeding
- [ ] If callback doesn't redirect to wizard → STOP, verify route registration

---

## Files to Modify

1. `web/api/routes/setup.py` - Add OAuth endpoints
2. `templates/setup.html` - Add Slack UI section
3. `web/static/js/setup.js` - Add Slack OAuth JavaScript
4. `scripts/setup_wizard.py` - Add CLI message
5. `web/api/routes/integrations.py` - Update configure URL

## Files to Create

1. `tests/unit/web/api/routes/test_setup_slack.py` - Unit tests
2. `tests/integration/test_setup_slack.py` - Integration tests

---

## Estimated Effort

| Phase | Time |
|-------|------|
| Phase 0 (Tests) | 20 min |
| Phase 1 (Backend) | 40 min |
| Phase 2 (Frontend) | 45 min |
| Phase 3 (CLI) | 10 min |
| Phase 4 (Integration) | 30 min |
| **Total** | ~2.5 hours |

---

## Environment Requirements

Ensure these are set for OAuth to work:
- `SLACK_CLIENT_ID` - From Slack app settings
- `SLACK_CLIENT_SECRET` - From Slack app settings
- `SLACK_REDIRECT_URI` - Must match Slack app OAuth settings

---

## PM Decisions Needed

1. **Channel selection**: Defer to future issue? (Recommendation: Yes, use default_channel for now)
2. **Permission display**: Show granted scopes? (Recommendation: No, just show "Connected")
3. **Enterprise Grid**: Support multiple workspaces? (Recommendation: Out of scope)

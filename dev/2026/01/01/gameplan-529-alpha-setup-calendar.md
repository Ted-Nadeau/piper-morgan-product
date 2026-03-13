# Gameplan: #529 ALPHA-SETUP-CALENDAR

# Gameplan: #529 ALPHA-SETUP-CALENDAR

**Issue**: Add Google Calendar OAuth to setup wizard
**Priority**: Alpha Critical
**Created**: 2026-01-01 07:26
**Author**: Claude Code (Opus)

---

## Executive Summary

Add Google Calendar OAuth flow to the setup wizard using standard web OAuth 2.0 (redirect flow), matching the pattern established in #528 (Slack). This requires refactoring from the current file-based desktop OAuth to proper web OAuth.

**Key insight**: Google Calendar supports standard web OAuth identical to Slack. The existing `GoogleCalendarMCPAdapter` uses a "desktop application" pattern that we will supplement with web OAuth endpoints.

---

## Phase -1: Investigation Summary

### Existing Infrastructure

**GoogleCalendarMCPAdapter** (`services/mcp/consumer/google_calendar_adapter.py`):

- Uses `google-auth-oauthlib.flow.Flow` with file-based tokens
- Reads `credentials.json` (client secrets) and writes `token.json`
- Redirect URI hardcoded to `http://localhost:8084` (desktop pattern)
- Full calendar operations: `get_todays_events()`, `get_current_meeting()`, etc.

**CalendarConfigService** (`services/integrations/calendar/config_service.py`):

- Reads from env vars → PIPER.user.md → defaults
- Stores `client_secrets_file`, `token_file`, `calendar_id`, `scopes`

### What's Missing

1. **OAuth handler for web flow**: Similar to `SlackOAuthHandler`
2. **Setup wizard endpoints**: `/setup/calendar/oauth/start`, `/callback`, `/status`
3. **Token storage**: Currently file-based, needs DB/keychain support
4. **UI section**: Calendar OAuth button in setup wizard

### Architecture Decision

**Web OAuth Flow** (to implement):

1. User clicks "Connect Calendar" → redirect to Google
2. Google redirects to `/setup/calendar/oauth/callback?code=...`
3. Exchange code for tokens at `https://oauth2.googleapis.com/token`
4. Store refresh token securely (keychain or env var)
5. `GoogleCalendarMCPAdapter` uses stored token

---

## PM Prerequisites (Manual Setup Required)

**STOP CONDITION**: These must be completed before Phase 1 implementation.

### Google Cloud Console Setup

1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID with type **"Web Application"**
3. Set authorized redirect URI: `http://localhost:8001/setup/calendar/oauth/callback`
4. Copy Client ID → set as `GOOGLE_CLIENT_ID` env var
5. Copy Client Secret → set as `GOOGLE_CLIENT_SECRET` env var

### Environment Variables Required

```bash
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_CALENDAR_REDIRECT_URI=http://localhost:8001/setup/calendar/oauth/callback
```

### Verification Command

```bash
# Verify env vars are set
echo $GOOGLE_CLIENT_ID | head -c 20  # Should show partial client ID
```

---

## Acceptance Criteria

- [ ] OAuth flow launches from wizard (click "Connect Calendar")
- [ ] Returns to wizard after OAuth success/failure
- [ ] Calendar name/email displayed after successful auth
- [ ] Error messages for: denied, invalid credentials, expired state
- [ ] Connection test fetches today's events count
- [ ] Dashboard "Configure" button points to setup wizard
- [ ] Existing `GoogleCalendarMCPAdapter` works with new token storage

---

## Phase 0: TDD Test Scaffolding

**File**: `tests/unit/web/api/routes/test_setup_calendar.py`

```python
"""
Unit tests for Google Calendar OAuth in setup wizard
Issue #529: ALPHA-SETUP-CALENDAR

Tests Calendar OAuth flow initiation, callback handling,
and status checking in the setup wizard context.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

pytestmark = pytest.mark.unit


class TestCalendarOAuthTrigger:
    """Tests for initiating Calendar OAuth from setup wizard"""

    @pytest.mark.asyncio
    async def test_get_calendar_oauth_url_returns_authorization_url(self):
        """Should return Google OAuth URL with state"""
        pass

    @pytest.mark.asyncio
    async def test_oauth_url_includes_calendar_scope(self):
        """OAuth URL should include calendar.readonly scope"""
        pass

    @pytest.mark.asyncio
    async def test_oauth_url_requests_offline_access(self):
        """OAuth URL should request offline access for refresh token"""
        pass


class TestCalendarOAuthCallback:
    """Tests for OAuth callback handling in setup context"""

    @pytest.mark.asyncio
    async def test_callback_success_redirects_with_email(self):
        """Successful callback should redirect with calendar email"""
        pass

    @pytest.mark.asyncio
    async def test_callback_error_redirects_with_error(self):
        """OAuth error should redirect with error message"""
        pass

    @pytest.mark.asyncio
    async def test_callback_exchanges_code_for_tokens(self):
        """Callback should exchange code for access/refresh tokens"""
        pass

    @pytest.mark.asyncio
    async def test_callback_stores_refresh_token(self):
        """Callback should store refresh token securely"""
        pass


class TestCalendarSetupStatus:
    """Tests for Calendar status in setup wizard"""

    @pytest.mark.asyncio
    async def test_check_calendar_configured_with_token(self):
        """Should return configured=True when refresh token exists"""
        pass

    @pytest.mark.asyncio
    async def test_check_calendar_not_configured(self):
        """Should return configured=False when no token"""
        pass

    @pytest.mark.asyncio
    async def test_status_includes_calendar_info(self):
        """Should include calendar email when configured"""
        pass


class TestCalendarConnectionTest:
    """Tests for Calendar connection verification"""

    @pytest.mark.asyncio
    async def test_connection_test_fetches_events(self):
        """Connection test should fetch today's events"""
        pass

    @pytest.mark.asyncio
    async def test_connection_test_returns_event_count(self):
        """Should return count of today's events on success"""
        pass
```

**Verification**: `pytest tests/unit/web/api/routes/test_setup_calendar.py --collect-only`

---

## Phase 1: OAuth Handler Service

**File**: `services/integrations/calendar/oauth_handler.py` (NEW)

### 1.1 Create GoogleCalendarOAuthHandler

```python
"""
Google Calendar OAuth Handler for Web Flow

Issue #529: ALPHA-SETUP-CALENDAR
Implements standard OAuth 2.0 web server flow for Google Calendar.
"""
import os
import secrets
import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode

import aiohttp
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class CalendarTokens:
    """OAuth tokens for Google Calendar"""
    access_token: str
    refresh_token: Optional[str]
    expires_at: int  # Unix timestamp
    token_type: str = "Bearer"
    scope: str = ""


class GoogleCalendarOAuthHandler:
    """
    OAuth 2.0 web flow handler for Google Calendar.

    Issue #529: ALPHA-SETUP-CALENDAR
    """

    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    # State tokens expire after 15 minutes
    STATE_EXPIRATION = 900

    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv(
            "GOOGLE_CALENDAR_REDIRECT_URI",
            "http://localhost:8001/setup/calendar/oauth/callback"
        )
        self.scopes = [
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/userinfo.email",
        ]

        # In-memory state storage (production should use Redis/DB)
        self._pending_states: Dict[str, float] = {}

    def generate_authorization_url(self) -> Tuple[str, str]:
        """
        Generate Google OAuth authorization URL with state.

        Returns:
            Tuple of (authorization_url, state_token)
        """
        state = secrets.token_urlsafe(32)
        self._pending_states[state] = time.time()

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": "offline",  # Request refresh token
            "state": state,
            "prompt": "consent",  # Force consent to get refresh token
        }

        auth_url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"
        return auth_url, state

    def _verify_state(self, state: str) -> bool:
        """Verify state token is valid and not expired."""
        if state not in self._pending_states:
            return False

        created_at = self._pending_states[state]
        if time.time() - created_at > self.STATE_EXPIRATION:
            del self._pending_states[state]
            return False

        del self._pending_states[state]
        return True

    async def handle_oauth_callback(
        self, code: str, state: str
    ) -> Dict:
        """
        Handle OAuth callback: verify state, exchange code, get user info.

        Returns:
            Dict with tokens and user info
        """
        if not self._verify_state(state):
            raise ValueError("Invalid or expired state token")

        # Exchange code for tokens
        tokens = await self._exchange_code_for_tokens(code)

        # Get user info (email)
        user_info = await self._get_user_info(tokens.access_token)

        return {
            "tokens": tokens,
            "user": user_info,
        }

    async def _exchange_code_for_tokens(self, code: str) -> CalendarTokens:
        """Exchange authorization code for access/refresh tokens."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri,
                },
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error("token_exchange_failed", status=response.status, error=error_text)
                    raise ValueError(f"Token exchange failed: {error_text}")

                data = await response.json()

                return CalendarTokens(
                    access_token=data["access_token"],
                    refresh_token=data.get("refresh_token"),
                    expires_at=int(time.time()) + data.get("expires_in", 3600),
                    token_type=data.get("token_type", "Bearer"),
                    scope=data.get("scope", ""),
                )

    async def _get_user_info(self, access_token: str) -> Dict:
        """Get user email from Google."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            ) as response:
                if response.status != 200:
                    return {"email": "Unknown"}

                data = await response.json()
                return {
                    "email": data.get("email", "Unknown"),
                    "name": data.get("name", ""),
                }
```

---

## Phase 2: Backend - Setup OAuth Endpoints

**File**: `web/api/routes/setup.py`

### 2.1 Add Calendar OAuth Endpoints

Add after Slack OAuth section:

```python
# ============================================================================
# Google Calendar OAuth Endpoints (Issue #529: ALPHA-SETUP-CALENDAR)
# ============================================================================


@router.get("/calendar/oauth/start")
async def start_calendar_oauth():
    """
    Generate Google Calendar OAuth URL for setup wizard.

    Issue #529: ALPHA-SETUP-CALENDAR
    """
    try:
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Verify credentials are configured
        if not handler.client_id or not handler.client_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google Calendar OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
            )

        auth_url, state = handler.generate_authorization_url()

        logger.info("calendar_oauth_started", state=state[:8] + "...")

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("calendar_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start Calendar OAuth: {str(e)}",
        )


@router.get("/calendar/oauth/callback")
async def handle_calendar_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Google Calendar OAuth callback.

    Issue #529: ALPHA-SETUP-CALENDAR
    """
    from starlette.responses import RedirectResponse
    from urllib.parse import quote

    if error:
        logger.warning("calendar_oauth_denied", error=error)
        return RedirectResponse(
            url=f"/setup?calendar_error={error}#step-2",
            status_code=302
        )

    if not code or not state:
        logger.warning("calendar_oauth_missing_params")
        return RedirectResponse(
            url="/setup?calendar_error=missing_params#step-2",
            status_code=302
        )

    try:
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler
        from services.infrastructure.keychain_service import KeychainService

        handler = GoogleCalendarOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        # Store refresh token securely
        tokens = result["tokens"]
        if tokens.refresh_token:
            keychain = KeychainService()
            keychain.store_api_key("google_calendar", tokens.refresh_token)
            logger.info("calendar_refresh_token_stored")

        # Get user email for display
        user_email = result["user"].get("email", "Calendar")
        email_encoded = quote(user_email)

        logger.info("calendar_oauth_success", email=user_email)

        return RedirectResponse(
            url=f"/setup?calendar_success=true&calendar_email={email_encoded}#step-2",
            status_code=302
        )

    except ValueError as e:
        logger.warning("calendar_oauth_validation_error", error=str(e))
        return RedirectResponse(
            url="/setup?calendar_error=callback_failed#step-2",
            status_code=302
        )
    except Exception as e:
        logger.error("calendar_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(
            url="/setup?calendar_error=callback_failed#step-2",
            status_code=302
        )


@router.get("/calendar/status")
async def get_calendar_status():
    """
    Get Calendar configuration status for setup wizard.

    Issue #529: ALPHA-SETUP-CALENDAR
    """
    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        refresh_token = keychain.get_api_key("google_calendar")

        if refresh_token:
            return {
                "configured": True,
                "message": "Calendar connected",
            }
        else:
            return {
                "configured": False,
                "message": "Not connected",
            }

    except Exception as e:
        logger.error("calendar_status_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "message": "Status check failed",
        }
```

---

## Phase 3: Frontend - Setup Wizard UI

### 3.1 Add Calendar Section to HTML

**File**: `templates/setup.html`

Add after Slack OAuth section:

```html
<!-- Google Calendar OAuth Integration (Issue #529: ALPHA-SETUP-CALENDAR) -->
<div class="form-group">
  <label>Google Calendar (optional)</label>
  <div class="calendar-oauth-section">
    <div id="calendar-not-connected" class="oauth-status">
      <button
        type="button"
        id="connect-calendar-btn"
        class="auth-button calendar-connect-btn"
      >
        Connect Calendar
      </button>
      <small>Connect your Google Calendar for scheduling awareness</small>
    </div>
    <div id="calendar-connected" class="oauth-status" style="display: none;">
      <div class="connected-status">
        <span class="status-icon">✓</span>
        <span id="calendar-email">Connected</span>
      </div>
      <button
        type="button"
        id="disconnect-calendar-btn"
        class="btn-secondary btn-sm"
      >
        Disconnect
      </button>
    </div>
    <div
      id="calendar-error"
      class="validation-status invalid"
      style="display: none;"
    ></div>
  </div>
</div>
```

### 3.2 Add Calendar CSS

```css
/* Google Calendar OAuth styles (Issue #529) */
.calendar-connect-btn {
  background: #4285f4 !important; /* Google blue */
  color: white !important;
}
.calendar-connect-btn:hover {
  background: #3367d6 !important;
}
```

### 3.3 Add Calendar JavaScript

**File**: `web/static/js/setup.js`

```javascript
// =========================================================================
// Google Calendar OAuth Functions (Issue #529: ALPHA-SETUP-CALENDAR)
// =========================================================================

function checkCalendarCallbackParams() {
  const params = new URLSearchParams(window.location.search);

  if (params.get("calendar_success") === "true") {
    const email = params.get("calendar_email") || "Calendar";
    showCalendarConnected(decodeURIComponent(email));
    window.history.replaceState({}, document.title, "/setup#step-2");
  } else if (params.get("calendar_error")) {
    const error = params.get("calendar_error");
    showCalendarError(getCalendarErrorMessage(error));
    window.history.replaceState({}, document.title, "/setup#step-2");
  }
}

async function checkCalendarStatus() {
  try {
    const response = await fetch("/setup/calendar/status");
    const data = await response.json();

    if (data.configured) {
      showCalendarConnected(data.email || "Connected");
    }
  } catch (err) {
    console.log("Calendar status check failed:", err);
  }
}

async function connectCalendar() {
  const btn = document.getElementById("connect-calendar-btn");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "Connecting...";
  }

  try {
    const response = await fetch("/setup/calendar/oauth/start");
    const data = await response.json();

    if (data.auth_url) {
      window.location.href = data.auth_url;
    } else {
      showCalendarError("Failed to start OAuth flow");
      if (btn) {
        btn.disabled = false;
        btn.textContent = "Connect Calendar";
      }
    }
  } catch (err) {
    showCalendarError("Connection failed. Please try again.");
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Connect Calendar";
    }
  }
}

function showCalendarConnected(email) {
  const notConnected = document.getElementById("calendar-not-connected");
  const connected = document.getElementById("calendar-connected");
  const emailSpan = document.getElementById("calendar-email");
  const errorDiv = document.getElementById("calendar-error");

  if (notConnected) notConnected.style.display = "none";
  if (connected) connected.style.display = "flex";
  if (emailSpan) emailSpan.textContent = `Connected: ${email}`;
  if (errorDiv) errorDiv.style.display = "none";
}

function showCalendarError(message) {
  const errorDiv = document.getElementById("calendar-error");
  if (errorDiv) {
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
  }
}

function getCalendarErrorMessage(error) {
  const messages = {
    access_denied: "Authorization was denied. Please try again.",
    missing_params: "OAuth callback missing parameters.",
    callback_failed: "Failed to complete authorization.",
  };
  return messages[error] || "An error occurred. Please try again.";
}

// Event listener
const connectCalendarBtn = document.getElementById("connect-calendar-btn");
if (connectCalendarBtn) {
  connectCalendarBtn.addEventListener("click", connectCalendar);
}

// Initialize on page load
checkCalendarCallbackParams();
checkCalendarStatus();
```

---

## Phase 4: Update Integrations Dashboard

**File**: `web/api/routes/integrations.py`

Update calendar configure_url:

```python
"google_calendar": {
    "display_name": "Google Calendar",
    "icon": "📅",
    "configure_url": "/setup#step-2",  # Issue #529
    ...
}
```

---

## Phase 5: Integration with Existing Adapter

**File**: `services/mcp/consumer/google_calendar_adapter.py`

### 5.1 Add Keychain Token Loading

Modify `authenticate()` to check keychain first:

```python
async def authenticate(self) -> bool:
    """
    Authenticate with Google Calendar API.

    Priority:
    1. Check keychain for refresh token (web OAuth)
    2. Fall back to file-based tokens (legacy)
    """
    try:
        # Try keychain first (web OAuth flow)
        from services.infrastructure.keychain_service import KeychainService
        keychain = KeychainService()
        refresh_token = keychain.get_api_key("google_calendar")

        if refresh_token:
            # Use refresh token to get access token
            credentials = await self._refresh_access_token(refresh_token)
            if credentials:
                self._credentials = credentials
                self._service = build("calendar", "v3", credentials=self._credentials)
                logger.info("Calendar authenticated via keychain")
                return True

        # Fall back to file-based flow (legacy)
        # ... existing file-based code ...
```

---

## Completion Matrix

| Phase | Deliverable         | Verification            |
| ----- | ------------------- | ----------------------- |
| 0     | Test scaffolding    | `pytest --collect-only` |
| 1     | OAuth handler       | Unit tests pass         |
| 2     | Backend endpoints   | curl commands work      |
| 3     | Frontend UI         | Manual browser test     |
| 4     | Dashboard link      | Click "Configure"       |
| 5     | Adapter integration | Calendar queries work   |

---

## STOP Conditions

- [ ] If `GOOGLE_CLIENT_ID` not set → STOP, PM must configure
- [ ] If `GOOGLE_CLIENT_SECRET` not set → STOP, PM must configure
- [ ] If redirect URI mismatch → STOP, update Google Cloud Console
- [ ] If tests fail → STOP, fix before proceeding
- [ ] If token storage fails → STOP, verify keychain access

---

## Files to Create

1. `services/integrations/calendar/oauth_handler.py` - OAuth handler
2. `tests/unit/web/api/routes/test_setup_calendar.py` - Unit tests

## Files to Modify

1. `web/api/routes/setup.py` - Add OAuth endpoints
2. `templates/setup.html` - Add Calendar UI section
3. `web/static/js/setup.js` - Add Calendar JavaScript
4. `web/api/routes/integrations.py` - Update configure_url
5. `services/mcp/consumer/google_calendar_adapter.py` - Add keychain support

---

## Estimated Effort

| Phase                   | Time         |
| ----------------------- | ------------ |
| Phase 0 (Tests)         | 20 min       |
| Phase 1 (OAuth Handler) | 45 min       |
| Phase 2 (Backend)       | 30 min       |
| Phase 3 (Frontend)      | 30 min       |
| Phase 4 (Dashboard)     | 5 min        |
| Phase 5 (Adapter)       | 30 min       |
| **Total**               | ~2.5-3 hours |

---

## Environment Requirements

```bash
# Required (PM must set before implementation)
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_CALENDAR_REDIRECT_URI=http://localhost:8001/setup/calendar/oauth/callback
```

---

## PM Actions Required

1. **Create Google Cloud OAuth credentials** (Web Application type)
2. **Add redirect URI**: `http://localhost:8001/setup/calendar/oauth/callback`
3. **Set environment variables** in `.env` or shell
4. **Confirm ready** for Phase 1 implementation

---

## Risk Mitigation

| Risk                   | Mitigation                                  |
| ---------------------- | ------------------------------------------- |
| Token expiration       | Store refresh token, implement auto-refresh |
| Keychain access denied | Fall back to env var storage                |
| Google API quota       | Existing circuit breaker handles this       |
| Multiple calendars     | MVP uses primary only, future enhancement   |

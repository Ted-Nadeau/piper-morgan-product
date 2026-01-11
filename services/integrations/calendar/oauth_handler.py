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

# Module-level state storage (singleton pattern)
# This ensures state persists across handler instances within the same process.
# Production should use Redis/DB - this works for single-server alpha.
_PENDING_STATES: Dict[str, float] = {}


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

    Implements standard authorization code flow:
    1. Generate authorization URL with state
    2. User authorizes at Google
    3. Handle callback with code exchange
    4. Return tokens and user info

    Issue #529: ALPHA-SETUP-CALENDAR
    """

    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    # State tokens expire after 15 minutes
    STATE_EXPIRATION = 900

    def __init__(self):
        # Issue #577: Load credentials with keychain fallback
        # Priority: env vars > keychain
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")

        # Fallback to keychain if env vars not set
        if not self.client_id or not self.client_secret:
            try:
                from services.infrastructure.keychain_service import KeychainService

                keychain = KeychainService()
                if not self.client_id:
                    self.client_id = keychain.get_api_key("google_calendar_client_id") or ""
                if not self.client_secret:
                    self.client_secret = keychain.get_api_key("google_calendar_client_secret") or ""
            except Exception:
                pass  # Keychain not available, continue with empty values

        self.redirect_uri = os.getenv(
            "GOOGLE_CALENDAR_REDIRECT_URI", "http://localhost:8001/setup/calendar/oauth/callback"
        )
        self.scopes = [
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/userinfo.email",
        ]
        # State storage is now module-level (_PENDING_STATES) to persist across instances

    def generate_authorization_url(self) -> Tuple[str, str]:
        """
        Generate Google OAuth authorization URL with state.

        Returns:
            Tuple of (authorization_url, state_token)
        """
        state = secrets.token_urlsafe(32)
        _PENDING_STATES[state] = time.time()

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

        logger.info(
            "calendar_oauth_url_generated",
            state_prefix=state[:8],
            redirect_uri=self.redirect_uri,
        )

        return auth_url, state

    def _verify_state(self, state: str) -> bool:
        """Verify state token is valid and not expired."""
        if state not in _PENDING_STATES:
            logger.warning(
                "calendar_oauth_state_not_found", state_prefix=state[:8] if state else "none"
            )
            return False

        created_at = _PENDING_STATES[state]
        if time.time() - created_at > self.STATE_EXPIRATION:
            del _PENDING_STATES[state]
            logger.warning("calendar_oauth_state_expired", state_prefix=state[:8])
            return False

        del _PENDING_STATES[state]
        return True

    async def handle_oauth_callback(self, code: str, state: str) -> Dict:
        """
        Handle OAuth callback: verify state, exchange code, get user info.

        Args:
            code: Authorization code from Google
            state: State token for CSRF verification

        Returns:
            Dict with tokens and user info

        Raises:
            ValueError: If state is invalid or expired
        """
        if not self._verify_state(state):
            raise ValueError("Invalid or expired state token")

        # Exchange code for tokens
        tokens = await self._exchange_code_for_tokens(code)

        # Get user info (email)
        user_info = await self._get_user_info(tokens.access_token)

        logger.info(
            "calendar_oauth_callback_success",
            email=user_info.get("email", "unknown"),
            has_refresh_token=bool(tokens.refresh_token),
        )

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
                    logger.error(
                        "calendar_token_exchange_failed",
                        status=response.status,
                        error=error_text,
                    )
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
                    logger.warning(
                        "calendar_userinfo_failed",
                        status=response.status,
                    )
                    return {"email": "Unknown"}

                data = await response.json()
                return {
                    "email": data.get("email", "Unknown"),
                    "name": data.get("name", ""),
                }

    async def refresh_access_token(self, refresh_token: str) -> Optional[CalendarTokens]:
        """
        Refresh an expired access token using refresh token.

        Args:
            refresh_token: The stored refresh token

        Returns:
            New CalendarTokens or None if refresh failed
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(
                        "calendar_token_refresh_failed",
                        status=response.status,
                        error=error_text,
                    )
                    return None

                data = await response.json()

                return CalendarTokens(
                    access_token=data["access_token"],
                    refresh_token=refresh_token,  # Keep the original refresh token
                    expires_at=int(time.time()) + data.get("expires_in", 3600),
                    token_type=data.get("token_type", "Bearer"),
                    scope=data.get("scope", ""),
                )

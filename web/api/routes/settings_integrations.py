"""
Settings Integrations API Routes

Provides OAuth connection management for the Settings page.
Allows users to connect/disconnect OAuth-based integrations
(Slack, Calendar) after initial setup is complete.

Issue #529: ALPHA-SETUP-CALENDAR (Settings integration)
"""

import os
from typing import Optional
from urllib.parse import quote

import structlog
from fastapi import APIRouter, HTTPException, status
from starlette.responses import RedirectResponse

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/settings/integrations", tags=["settings-integrations"])


# ============================================================================
# Slack OAuth for Settings
# ============================================================================


@router.get("/slack/connect")
async def connect_slack():
    """
    Start Slack OAuth flow from Settings page.

    Returns authorization URL for OAuth. After completion,
    redirects back to /settings/integrations with status.
    """
    try:
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        handler = SlackOAuthHandler()

        # Use settings-specific redirect URI
        redirect_uri = os.getenv(
            "SLACK_SETTINGS_REDIRECT_URI",
            os.getenv(
                "SLACK_REDIRECT_URI",
                "http://localhost:8001/api/v1/settings/integrations/slack/callback",
            ),
        )

        auth_url, state = handler.generate_authorization_url(
            redirect_uri=redirect_uri if redirect_uri else None
        )

        logger.info("slack_settings_oauth_started", state=state[:8] + "...")

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except Exception as e:
        logger.error("slack_settings_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start Slack OAuth: {str(e)}",
        )


@router.get("/slack/callback")
async def handle_slack_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Slack OAuth callback for Settings page.

    Redirects back to /settings/integrations with status.
    """
    # Handle OAuth error
    if error:
        logger.warning("slack_settings_oauth_denied", error=error)
        return RedirectResponse(url=f"/settings/integrations?slack_error={error}", status_code=302)

    # Handle missing parameters
    if not code or not state:
        logger.warning(
            "slack_settings_oauth_missing_params", has_code=bool(code), has_state=bool(state)
        )
        return RedirectResponse(
            url="/settings/integrations?slack_error=missing_params", status_code=302
        )

    try:
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        handler = SlackOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        workspace_name = result.get("workspace", {}).get("workspace_name", "Workspace")
        workspace_name_encoded = quote(workspace_name)

        logger.info("slack_settings_oauth_success", workspace=workspace_name)

        return RedirectResponse(
            url=f"/settings/integrations?slack_success=true&slack_workspace={workspace_name_encoded}",
            status_code=302,
        )

    except ValueError as e:
        logger.warning("slack_settings_oauth_validation_error", error=str(e))
        return RedirectResponse(
            url="/settings/integrations?slack_error=callback_failed", status_code=302
        )
    except Exception as e:
        logger.error("slack_settings_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(
            url="/settings/integrations?slack_error=callback_failed", status_code=302
        )


@router.post("/slack/disconnect")
async def disconnect_slack():
    """
    Disconnect Slack integration.

    Removes stored tokens from environment/keychain.
    Note: Does not revoke tokens on Slack's side.
    """
    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()

        # Try to remove from keychain
        try:
            keychain.delete_api_key("slack_bot_token")
        except Exception:
            pass

        # Clear from environment (won't persist after restart)
        if "SLACK_BOT_TOKEN" in os.environ:
            del os.environ["SLACK_BOT_TOKEN"]

        logger.info("slack_disconnected")

        return {
            "success": True,
            "message": "Slack disconnected",
        }

    except Exception as e:
        logger.error("slack_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect Slack: {str(e)}",
        )


# ============================================================================
# Google Calendar OAuth for Settings
# ============================================================================


@router.get("/calendar/connect")
async def connect_calendar():
    """
    Start Google Calendar OAuth flow from Settings page.

    Returns authorization URL for OAuth. After completion,
    redirects back to /settings/integrations with status.
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

        # Override redirect URI for settings flow
        original_redirect = handler.redirect_uri
        handler.redirect_uri = os.getenv(
            "GOOGLE_SETTINGS_REDIRECT_URI",
            "http://localhost:8001/api/v1/settings/integrations/calendar/callback",
        )

        auth_url, state = handler.generate_authorization_url()

        # Restore original
        handler.redirect_uri = original_redirect

        logger.info("calendar_settings_oauth_started", state=state[:8] + "...")

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("calendar_settings_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start Calendar OAuth: {str(e)}",
        )


@router.get("/calendar/callback")
async def handle_calendar_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Google Calendar OAuth callback for Settings page.

    Redirects back to /settings/integrations with status.
    """
    # Handle OAuth error
    if error:
        logger.warning("calendar_settings_oauth_denied", error=error)
        return RedirectResponse(
            url=f"/settings/integrations?calendar_error={error}", status_code=302
        )

    # Handle missing parameters
    if not code or not state:
        logger.warning(
            "calendar_settings_oauth_missing_params", has_code=bool(code), has_state=bool(state)
        )
        return RedirectResponse(
            url="/settings/integrations?calendar_error=missing_params", status_code=302
        )

    try:
        from services.infrastructure.keychain_service import KeychainService
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Override redirect URI to match what was used in authorization
        handler.redirect_uri = os.getenv(
            "GOOGLE_SETTINGS_REDIRECT_URI",
            "http://localhost:8001/api/v1/settings/integrations/calendar/callback",
        )

        result = await handler.handle_oauth_callback(code, state)

        # Store refresh token securely
        tokens = result["tokens"]
        if tokens.refresh_token:
            keychain = KeychainService()
            keychain.store_api_key("google_calendar", tokens.refresh_token)
            logger.info("calendar_refresh_token_stored_settings")

        user_email = result["user"].get("email", "Calendar")
        email_encoded = quote(user_email)

        logger.info("calendar_settings_oauth_success", email=user_email)

        return RedirectResponse(
            url=f"/settings/integrations?calendar_success=true&calendar_email={email_encoded}",
            status_code=302,
        )

    except ValueError as e:
        logger.warning("calendar_settings_oauth_validation_error", error=str(e))
        return RedirectResponse(
            url="/settings/integrations?calendar_error=callback_failed", status_code=302
        )
    except Exception as e:
        logger.error("calendar_settings_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(
            url="/settings/integrations?calendar_error=callback_failed", status_code=302
        )


@router.post("/calendar/disconnect")
async def disconnect_calendar():
    """
    Disconnect Google Calendar integration.

    Removes stored refresh token from keychain.
    Note: Does not revoke tokens on Google's side.
    """
    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()

        # Remove refresh token from keychain
        try:
            keychain.delete_api_key("google_calendar")
        except Exception:
            pass

        logger.info("calendar_disconnected")

        return {
            "success": True,
            "message": "Calendar disconnected",
        }

    except Exception as e:
        logger.error("calendar_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect Calendar: {str(e)}",
        )


# ============================================================================
# Connection Status Endpoints
# ============================================================================


@router.get("/status")
async def get_all_oauth_status():
    """
    Get connection status for all OAuth-based integrations.

    Returns connection status for Slack and Calendar.
    """
    from services.infrastructure.keychain_service import KeychainService

    status_result = {
        "slack": {"connected": False, "info": None},
        "calendar": {"connected": False, "info": None},
    }

    try:
        keychain = KeychainService()

        # Check Slack
        try:
            from services.integrations.slack.config_service import SlackConfigService

            config_service = SlackConfigService()
            slack_config = config_service.get_config()
            if slack_config.bot_token:
                status_result["slack"]["connected"] = True
        except Exception:
            pass

        # Check Calendar
        try:
            refresh_token = keychain.get_api_key("google_calendar")
            if refresh_token:
                status_result["calendar"]["connected"] = True
        except Exception:
            pass

    except Exception as e:
        logger.error("oauth_status_check_failed", error=str(e))

    return status_result

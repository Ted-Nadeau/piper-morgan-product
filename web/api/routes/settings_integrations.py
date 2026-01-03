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
# Google Calendar OAuth for Settings (Issue #537)
# ============================================================================


@router.get("/calendar")
async def get_calendar_settings():
    """
    Get Google Calendar integration status.

    Returns whether Calendar is configured and validates connection if token present.
    Issue #537: ALPHA-SETUP-MANAGE - Integration Management Post-Setup
    """
    try:
        from services.infrastructure.keychain_service import KeychainService
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        keychain = KeychainService()
        refresh_token = keychain.get_api_key("google_calendar")

        if refresh_token:
            # Validate the token by attempting to refresh it
            handler = GoogleCalendarOAuthHandler()
            try:
                tokens = await handler.refresh_access_token(refresh_token)

                if tokens:
                    # Token is valid - try to get user info if possible
                    return {
                        "configured": True,
                        "valid": True,
                        "email": None,  # Would need additional API call to get email
                        "error": None,
                    }
                else:
                    return {
                        "configured": True,
                        "valid": False,
                        "email": None,
                        "error": "Token expired or revoked",
                    }
            except Exception as token_error:
                logger.warning("calendar_token_validation_failed", error=str(token_error))
                return {
                    "configured": True,
                    "valid": False,
                    "email": None,
                    "error": str(token_error),
                }
        else:
            return {
                "configured": False,
                "valid": False,
                "email": None,
                "error": None,
            }

    except Exception as e:
        logger.error("calendar_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "email": None,
            "error": str(e),
        }


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


# ============================================================================
# Notion API Key Management (Issue #540)
# ============================================================================


@router.get("/notion")
async def get_notion_settings():
    """
    Get Notion integration status.

    Returns whether Notion is configured and any workspace info.
    Issue #540: ALPHA-SETUP-NOTION stuck state recovery
    """
    from services.infrastructure.keychain_service import KeychainService

    try:
        keychain = KeychainService()
        api_key = keychain.get_api_key("notion")

        if api_key:
            # Validate the key and get workspace info
            from services.security.user_api_key_service import UserAPIKeyService
            from web.api.routes.setup import validate_notion_key_and_get_workspace

            is_valid, workspace_name, error_msg = await validate_notion_key_and_get_workspace(
                api_key
            )

            return {
                "configured": True,
                "valid": is_valid,
                "workspace": workspace_name if is_valid else None,
                "error": error_msg if not is_valid else None,
            }
        else:
            return {
                "configured": False,
                "valid": False,
                "workspace": None,
                "error": None,
            }

    except Exception as e:
        logger.error("notion_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "workspace": None,
            "error": str(e),
        }


@router.post("/notion/save")
async def save_notion_key(api_key: str):
    """
    Save or update Notion API key.

    Validates the key first, then stores in keychain.
    Issue #540: ALPHA-SETUP-NOTION stuck state recovery
    """
    from services.database.session_factory import AsyncSessionFactory
    from services.security.user_api_key_service import UserAPIKeyService
    from web.api.routes.setup import validate_notion_key_and_get_workspace

    # Validate the key first
    is_valid, workspace_name, error_msg = await validate_notion_key_and_get_workspace(api_key)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg or "Invalid Notion API key",
        )

    # Store in keychain using UserAPIKeyService
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            service = UserAPIKeyService()

            # Get current user from session context (simplified - use system user for now)
            # In production, this should get the authenticated user
            await service.store_user_key(
                session=session,
                user_id="system",  # TODO: Get from auth context
                provider="notion",
                api_key=api_key,
                validate=False,  # Already validated above
            )

        logger.info("notion_key_saved", workspace=workspace_name)

        return {
            "success": True,
            "workspace": workspace_name,
            "message": f"Connected to {workspace_name}",
        }

    except Exception as e:
        logger.error("notion_key_save_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Notion key: {str(e)}",
        )


@router.post("/notion/disconnect")
async def disconnect_notion():
    """
    Disconnect Notion integration.

    Removes API key from keychain.
    Issue #540: ALPHA-SETUP-NOTION stuck state recovery
    """
    from services.infrastructure.keychain_service import KeychainService

    try:
        keychain = KeychainService()

        # Remove from keychain
        try:
            keychain.delete_api_key("notion")
        except Exception:
            pass  # Key might not exist

        logger.info("notion_disconnected")

        return {
            "success": True,
            "message": "Notion disconnected",
        }

    except Exception as e:
        logger.error("notion_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect Notion: {str(e)}",
        )


# ============================================================================
# GitHub Token Management (Issue #541)
# ============================================================================


@router.get("/github")
async def get_github_settings():
    """
    Get GitHub integration status.

    Returns whether GitHub is configured and validates token if present.
    Issue #541: ALPHA-SETUP-GITHUB stuck state recovery
    """
    try:
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()
        token = config_service.get_authentication_token()

        if token:
            # Validate the token by testing connection
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            router_instance = GitHubIntegrationRouter()
            test_result = router_instance.test_connection()

            is_valid = test_result.get("authenticated", False)

            return {
                "configured": True,
                "valid": is_valid,
                "username": test_result.get("username") if is_valid else None,
                "error": test_result.get("error") if not is_valid else None,
            }
        else:
            return {
                "configured": False,
                "valid": False,
                "username": None,
                "error": None,
            }

    except Exception as e:
        logger.error("github_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "username": None,
            "error": str(e),
        }


@router.post("/github/save")
async def save_github_token(token: str):
    """
    Save or update GitHub personal access token.

    Validates the token first, then stores in keychain and environment.
    Issue #541: ALPHA-SETUP-GITHUB stuck state recovery
    """
    from services.infrastructure.keychain_service import KeychainService

    # Validate the token by testing connection
    try:
        # Temporarily set the token for validation
        original_token = os.environ.get("GITHUB_TOKEN")
        os.environ["GITHUB_TOKEN"] = token

        # Clear config cache to pick up new token
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()
        config_service.clear_cache()

        # Test connection
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter

        router_instance = GitHubIntegrationRouter()
        test_result = router_instance.test_connection()

        is_valid = test_result.get("authenticated", False)

        if not is_valid:
            # Restore original token
            if original_token:
                os.environ["GITHUB_TOKEN"] = original_token
            else:
                os.environ.pop("GITHUB_TOKEN", None)
            config_service.clear_cache()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=test_result.get("error", "Invalid GitHub token"),
            )

        # Token is valid - store in keychain for persistence
        keychain = KeychainService()
        keychain.store_api_key("github_token", token)

        username = test_result.get("username", "GitHub User")
        logger.info("github_token_saved", username=username)

        return {
            "success": True,
            "username": username,
            "message": f"Connected as {username}",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("github_token_save_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save GitHub token: {str(e)}",
        )


@router.post("/github/disconnect")
async def disconnect_github():
    """
    Disconnect GitHub integration.

    Removes token from keychain and environment.
    Issue #541: ALPHA-SETUP-GITHUB stuck state recovery
    """
    from services.infrastructure.keychain_service import KeychainService

    try:
        keychain = KeychainService()

        # Remove from keychain
        try:
            keychain.delete_api_key("github_token")
        except Exception:
            pass  # Key might not exist

        # Clear from environment
        os.environ.pop("GITHUB_TOKEN", None)
        os.environ.pop("GITHUB_API_TOKEN", None)
        os.environ.pop("GH_TOKEN", None)

        # Clear config cache
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()
        config_service.clear_cache()

        logger.info("github_disconnected")

        return {
            "success": True,
            "message": "GitHub disconnected",
        }

    except Exception as e:
        logger.error("github_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect GitHub: {str(e)}",
        )


# ============================================================================
# Slack OAuth Management (Issue #528)
# ============================================================================


@router.get("/slack")
async def get_slack_settings():
    """
    Get Slack integration status.

    Returns whether Slack is configured and validates connection if token present.
    Issue #528: ALPHA-SETUP-SLACK - Add Slack OAuth to setup wizard
    """
    try:
        # Check if bot token is configured
        bot_token = os.environ.get("SLACK_BOT_TOKEN")

        if bot_token:
            # Validate the token by testing connection
            from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

            router_instance = SlackIntegrationRouter()
            test_result = await router_instance.test_auth()

            is_valid = test_result.get("ok", False)
            team_name = test_result.get("team")
            bot_id = test_result.get("bot_id")

            return {
                "configured": True,
                "valid": is_valid,
                "workspace": team_name if is_valid else None,
                "bot_id": bot_id if is_valid else None,
                "error": test_result.get("error") if not is_valid else None,
            }
        else:
            return {
                "configured": False,
                "valid": False,
                "workspace": None,
                "bot_id": None,
                "error": None,
            }

    except Exception as e:
        logger.error("slack_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "workspace": None,
            "bot_id": None,
            "error": str(e),
        }


@router.get("/slack/authorize")
async def get_slack_oauth_url():
    """
    Get Slack OAuth authorization URL.

    Generates a secure OAuth URL to initiate Slack workspace connection.
    Issue #528: ALPHA-SETUP-SLACK
    """
    try:
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        config_service = SlackConfigService()
        oauth_handler = SlackOAuthHandler(config_service)

        auth_url, state = oauth_handler.generate_authorization_url()

        return {
            "success": True,
            "authorization_url": auth_url,
            "state": state,
        }

    except Exception as e:
        logger.error("slack_oauth_url_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate Slack OAuth URL: {str(e)}",
        )


@router.post("/slack/disconnect")
async def disconnect_slack():
    """
    Disconnect Slack integration.

    Revokes OAuth access and removes stored tokens.
    Issue #528: ALPHA-SETUP-SLACK
    """
    try:
        # Get workspace ID if available
        workspace_id = os.environ.get("SLACK_TEAM_ID", "default")

        # Try to revoke via OAuth handler
        try:
            from services.integrations.slack.config_service import SlackConfigService
            from services.integrations.slack.oauth_handler import SlackOAuthHandler

            config_service = SlackConfigService()
            oauth_handler = SlackOAuthHandler(config_service)
            await oauth_handler.revoke_workspace_access(workspace_id)
        except Exception as revoke_error:
            logger.warning(
                "slack_revoke_warning",
                error=str(revoke_error),
                message="Could not revoke via API, clearing local config",
            )

        # Clear environment variables (they'll need to be re-set on restart)
        # Note: In production, this would clear from secure storage
        os.environ.pop("SLACK_BOT_TOKEN", None)
        os.environ.pop("SLACK_TEAM_ID", None)
        os.environ.pop("SLACK_APP_TOKEN", None)

        logger.info("slack_disconnected", workspace_id=workspace_id)

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

"""
Unit tests for Slack Settings API
Issue #528: ALPHA-SETUP-SLACK - Add Slack OAuth to setup wizard

Tests the Slack OAuth management endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    disconnect_slack,
    get_slack_oauth_url,
    get_slack_settings,
)


class TestGetSlackSettings:
    """Tests for GET /api/v1/settings/integrations/slack"""

    @pytest.mark.asyncio
    async def test_returns_not_configured_when_no_token(self):
        """Should return configured=False when no bot token is set"""
        with patch.dict("os.environ", {}, clear=True):
            result = await get_slack_settings()

            assert result["configured"] is False
            assert result["valid"] is False
            assert result["workspace"] is None
            assert result["bot_id"] is None
            assert result["error"] is None

    @pytest.mark.asyncio
    async def test_returns_configured_and_valid_when_token_works(self):
        """Should return configured=True, valid=True when token validates"""
        mock_router = MagicMock()
        mock_router.test_auth = AsyncMock(
            return_value={
                "ok": True,
                "team": "Test Workspace",
                "bot_id": "B12345",
            }
        )

        with (
            patch.dict("os.environ", {"SLACK_BOT_TOKEN": "xoxb-test"}, clear=True),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=mock_router,
            ),
        ):
            result = await get_slack_settings()

            assert result["configured"] is True
            assert result["valid"] is True
            assert result["workspace"] == "Test Workspace"
            assert result["bot_id"] == "B12345"
            assert result["error"] is None

    @pytest.mark.asyncio
    async def test_returns_configured_but_invalid_when_token_fails(self):
        """Should return configured=True, valid=False when token is invalid (stuck state)"""
        mock_router = MagicMock()
        mock_router.test_auth = AsyncMock(
            return_value={
                "ok": False,
                "error": "invalid_auth",
            }
        )

        with (
            patch.dict("os.environ", {"SLACK_BOT_TOKEN": "xoxb-expired"}, clear=True),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=mock_router,
            ),
        ):
            result = await get_slack_settings()

            assert result["configured"] is True
            assert result["valid"] is False
            assert result["workspace"] is None
            assert result["error"] == "invalid_auth"


class TestGetSlackOAuthUrl:
    """Tests for GET /api/v1/settings/integrations/slack/authorize"""

    @pytest.mark.asyncio
    async def test_returns_authorization_url(self):
        """Should return OAuth authorization URL and state"""
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.generate_authorization_url.return_value = (
            "https://slack.com/oauth/v2/authorize?client_id=test&scope=chat:write",
            "secure_state_token",
        )

        with (
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            result = await get_slack_oauth_url()

            assert result["success"] is True
            assert "slack.com/oauth" in result["authorization_url"]
            assert result["state"] == "secure_state_token"

    @pytest.mark.asyncio
    async def test_handles_oauth_generation_failure(self):
        """Should raise HTTPException when OAuth URL generation fails"""
        mock_config = MagicMock()
        mock_config.get_config.side_effect = Exception("Missing client_id")

        with patch(
            "services.integrations.slack.config_service.SlackConfigService",
            return_value=mock_config,
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_slack_oauth_url()

            assert exc_info.value.status_code == 500
            assert "Failed to generate" in str(exc_info.value.detail)


class TestDisconnectSlack:
    """Tests for POST /api/v1/settings/integrations/slack/disconnect"""

    @pytest.mark.asyncio
    async def test_disconnects_and_returns_success(self):
        """Should revoke access and return success"""
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.revoke_workspace_access = AsyncMock(return_value=True)

        with (
            patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-test", "SLACK_TEAM_ID": "T12345"},
                clear=True,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            result = await disconnect_slack()

            assert result["success"] is True
            assert result["message"] == "Slack disconnected"
            mock_oauth_handler.revoke_workspace_access.assert_called_once_with("T12345")

    @pytest.mark.asyncio
    async def test_succeeds_even_when_revoke_fails(self):
        """Should still succeed even if API revoke fails (clears local config)"""
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.revoke_workspace_access = AsyncMock(side_effect=Exception("API error"))

        with (
            patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-test"},
                clear=True,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            # Should not raise, just log warning
            result = await disconnect_slack()

            assert result["success"] is True
            assert result["message"] == "Slack disconnected"

    @pytest.mark.asyncio
    async def test_handles_missing_token_gracefully(self):
        """Should succeed even if no token exists to clear"""
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.revoke_workspace_access = AsyncMock(return_value=True)

        with (
            patch.dict("os.environ", {}, clear=True),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            result = await disconnect_slack()

            assert result["success"] is True
            assert result["message"] == "Slack disconnected"


class TestIntegrationRegistrySlackUrl:
    """Tests for Slack configure_url in INTEGRATION_REGISTRY (Issue #528)"""

    def test_slack_configure_url_points_to_settings_page(self):
        """Slack configure_url should point to dedicated settings page"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        slack_config = INTEGRATION_REGISTRY.get("slack")
        assert slack_config is not None
        assert slack_config["configure_url"] == "/settings/integrations/slack"
        # Should NOT be None anymore
        assert slack_config["configure_url"] is not None

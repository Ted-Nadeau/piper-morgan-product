"""
Unit tests for Google Calendar Settings API
Issue #537: ALPHA-SETUP-MANAGE - Integration Management Post-Setup

Tests the Google Calendar OAuth management endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import disconnect_calendar, get_calendar_settings


class TestGetCalendarSettings:
    """Tests for GET /api/v1/settings/integrations/calendar"""

    @pytest.mark.asyncio
    async def test_returns_not_configured_when_no_token(self):
        """Should return configured=False when no refresh token is stored"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await get_calendar_settings()

            assert result["configured"] is False
            assert result["valid"] is False
            assert result["email"] is None
            assert result["error"] is None

    @pytest.mark.asyncio
    async def test_returns_configured_and_valid_when_token_works(self):
        """Should return configured=True, valid=True when token refreshes successfully"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "valid_refresh_token"

        mock_handler = MagicMock()
        mock_handler.refresh_access_token = AsyncMock(
            return_value=MagicMock(access_token="new_access_token")
        )

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=mock_handler,
            ),
        ):
            result = await get_calendar_settings()

            assert result["configured"] is True
            assert result["valid"] is True
            assert result["error"] is None

    @pytest.mark.asyncio
    async def test_returns_configured_but_invalid_when_token_fails(self):
        """Should return configured=True, valid=False when token is expired (stuck state)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "expired_refresh_token"

        mock_handler = MagicMock()
        mock_handler.refresh_access_token = AsyncMock(return_value=None)

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=mock_handler,
            ),
        ):
            result = await get_calendar_settings()

            assert result["configured"] is True
            assert result["valid"] is False
            assert result["error"] == "Token expired or revoked"

    @pytest.mark.asyncio
    async def test_returns_invalid_when_refresh_raises_exception(self):
        """Should return configured=True, valid=False when token refresh throws exception"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "bad_refresh_token"

        mock_handler = MagicMock()
        mock_handler.refresh_access_token = AsyncMock(side_effect=Exception("API error"))

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=mock_handler,
            ),
        ):
            result = await get_calendar_settings()

            assert result["configured"] is True
            assert result["valid"] is False
            assert "API error" in result["error"]


class TestDisconnectCalendar:
    """Tests for POST /api/v1/settings/integrations/calendar/disconnect"""

    @pytest.mark.asyncio
    async def test_disconnects_and_returns_success(self):
        """Should remove token from keychain and return success"""
        mock_keychain = MagicMock()
        mock_keychain.delete_api_key.return_value = True

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await disconnect_calendar()

            assert result["success"] is True
            assert result["message"] == "Calendar disconnected"
            mock_keychain.delete_api_key.assert_called_once_with("google_calendar")

    @pytest.mark.asyncio
    async def test_succeeds_even_when_no_token_exists(self):
        """Should still succeed even if no token exists to clear"""
        mock_keychain = MagicMock()
        mock_keychain.delete_api_key.side_effect = Exception("Key not found")

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await disconnect_calendar()

            assert result["success"] is True
            assert result["message"] == "Calendar disconnected"


class TestIntegrationRegistryCalendarUrl:
    """Tests for Calendar configure_url in INTEGRATION_REGISTRY (Issue #537)"""

    def test_calendar_configure_url_points_to_settings_page(self):
        """Calendar configure_url should point to dedicated settings page"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        calendar_config = INTEGRATION_REGISTRY.get("calendar")
        assert calendar_config is not None
        assert calendar_config["configure_url"] == "/settings/integrations/calendar"
        # Should NOT be None anymore
        assert calendar_config["configure_url"] is not None

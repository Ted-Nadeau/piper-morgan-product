"""
Unit tests for Google Calendar Settings API
Issue #537: ALPHA-SETUP-MANAGE - Integration Management Post-Setup

Tests the Google Calendar OAuth management endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    CalendarAppCredentialsRequest,
    disconnect_calendar,
    get_calendar_app_credentials_status,
    get_calendar_settings,
    save_calendar_app_credentials,
)


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


class TestCalendarAppCredentials:
    """Tests for Calendar app credentials endpoints (Issue #577)"""

    @pytest.mark.asyncio
    async def test_save_credentials_stores_in_keychain(self):
        """Should store client_id and client_secret in keychain"""
        mock_keychain = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        credentials = CalendarAppCredentialsRequest(
            client_id="123456789.apps.googleusercontent.com",
            client_secret="GOCSPX-test_secret_value",
        )

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await save_calendar_app_credentials(credentials, mock_user)

            assert result["success"] is True
            assert "saved" in result["message"].lower()
            # Verify keychain was called with correct keys
            mock_keychain.store_api_key.assert_any_call(
                "google_calendar_client_id", "123456789.apps.googleusercontent.com"
            )
            mock_keychain.store_api_key.assert_any_call(
                "google_calendar_client_secret", "GOCSPX-test_secret_value"
            )

    @pytest.mark.asyncio
    async def test_save_credentials_strips_whitespace(self):
        """Should strip whitespace from credentials before storing"""
        mock_keychain = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        credentials = CalendarAppCredentialsRequest(
            client_id="  123456789.apps.googleusercontent.com  ",
            client_secret="  GOCSPX-secret_with_spaces  ",
        )

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            await save_calendar_app_credentials(credentials, mock_user)

            # Verify whitespace was stripped
            mock_keychain.store_api_key.assert_any_call(
                "google_calendar_client_id", "123456789.apps.googleusercontent.com"
            )
            mock_keychain.store_api_key.assert_any_call(
                "google_calendar_client_secret", "GOCSPX-secret_with_spaces"
            )

    @pytest.mark.asyncio
    async def test_get_status_returns_configured_when_both_present(self):
        """Should return configured=True when both client_id and client_secret exist in keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "google_calendar_client_id": "123456789.apps.googleusercontent.com",
            "google_calendar_client_secret": "GOCSPX-secret_value",
        }.get(key, None)
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is True
            assert result.has_client_id is True
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_returns_not_configured_when_missing_id(self):
        """Should return configured=False when client_id is missing"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "google_calendar_client_id": "",  # Empty
            "google_calendar_client_secret": "GOCSPX-secret_value",
        }.get(key, "")
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is False
            assert result.has_client_id is False
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_returns_not_configured_when_missing_secret(self):
        """Should return configured=False when client_secret is missing"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "google_calendar_client_id": "123456789.apps.googleusercontent.com",
            "google_calendar_client_secret": "",  # Empty
        }.get(key, "")
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is False
            assert result.has_client_id is True
            assert result.has_client_secret is False

    @pytest.mark.asyncio
    async def test_get_status_falls_back_to_env_vars(self):
        """Should check environment variables as fallback when keychain is empty"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = ""  # Keychain returns nothing
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict(
                "os.environ",
                {
                    "GOOGLE_CLIENT_ID": "env_client_id",
                    "GOOGLE_CLIENT_SECRET": "env_client_secret",
                },
            ),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is True
            assert result.has_client_id is True
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_never_exposes_credentials(self):
        """Status response should never contain actual credential values"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "google_calendar_client_id": "secret_client_id_value",
            "google_calendar_client_secret": "super_secret_value",
        }.get(key, "")
        mock_user = MagicMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            # Convert to dict to check all fields
            result_dict = result.model_dump()

            # Should not contain actual credential values
            for value in result_dict.values():
                if isinstance(value, str):
                    assert "secret_client_id_value" not in value
                    assert "super_secret_value" not in value

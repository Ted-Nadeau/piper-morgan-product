"""
Unit tests for GitHub Settings API
Issue #541: ALPHA-SETUP-GITHUB stuck state recovery

Tests the GitHub token management endpoints in settings_integrations.py.
"""

from unittest.mock import MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    disconnect_github,
    get_github_settings,
    save_github_token,
)


class TestGetGitHubSettings:
    """Tests for GET /api/v1/settings/integrations/github"""

    @pytest.mark.asyncio
    async def test_returns_not_configured_when_no_token(self):
        """Should return configured=False when no token is available"""
        mock_config_service = MagicMock()
        mock_config_service.get_authentication_token.return_value = None

        with patch(
            "services.integrations.github.config_service.GitHubConfigService",
            return_value=mock_config_service,
        ):
            result = await get_github_settings()

            assert result["configured"] is False
            assert result["valid"] is False
            assert result["username"] is None
            assert result["error"] is None

    @pytest.mark.asyncio
    async def test_returns_configured_and_valid_when_token_valid(self):
        """Should return configured=True, valid=True when token validates"""
        mock_config_service = MagicMock()
        mock_config_service.get_authentication_token.return_value = "ghp_test_token"

        mock_router = MagicMock()
        mock_router.test_connection.return_value = {
            "authenticated": True,
            "username": "testuser",
        }

        with (
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config_service,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=mock_router,
            ),
        ):
            result = await get_github_settings()

            assert result["configured"] is True
            assert result["valid"] is True
            assert result["username"] == "testuser"
            assert result["error"] is None

    @pytest.mark.asyncio
    async def test_returns_configured_but_invalid_when_token_fails(self):
        """Should return configured=True, valid=False when token is invalid (stuck state)"""
        mock_config_service = MagicMock()
        mock_config_service.get_authentication_token.return_value = "ghp_expired_token"

        mock_router = MagicMock()
        mock_router.test_connection.return_value = {
            "authenticated": False,
            "error": "Token has expired or been revoked",
        }

        with (
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config_service,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=mock_router,
            ),
        ):
            result = await get_github_settings()

            assert result["configured"] is True
            assert result["valid"] is False
            assert result["username"] is None
            assert result["error"] == "Token has expired or been revoked"


class TestSaveGitHubToken:
    """Tests for POST /api/v1/settings/integrations/github/save"""

    @pytest.mark.asyncio
    async def test_rejects_invalid_token(self):
        """Should return 400 when token validation fails"""
        mock_config_service = MagicMock()
        mock_config_service.clear_cache = MagicMock()

        mock_router = MagicMock()
        mock_router.test_connection.return_value = {
            "authenticated": False,
            "error": "Bad credentials",
        }

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config_service,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=mock_router,
            ),
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await save_github_token("ghp_invalid_token")

            assert exc_info.value.status_code == 400
            assert "Bad credentials" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_saves_valid_token_and_returns_success(self):
        """Should store token and return success when validation passes"""
        mock_config_service = MagicMock()
        mock_config_service.clear_cache = MagicMock()

        mock_router = MagicMock()
        mock_router.test_connection.return_value = {
            "authenticated": True,
            "username": "testuser",
        }

        mock_keychain = MagicMock()

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config_service,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=mock_router,
            ),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            result = await save_github_token("ghp_valid_token")

            assert result["success"] is True
            assert result["username"] == "testuser"
            assert "testuser" in result["message"]
            mock_keychain.store_api_key.assert_called_once_with("github_token", "ghp_valid_token")


class TestDisconnectGitHub:
    """Tests for POST /api/v1/settings/integrations/github/disconnect"""

    @pytest.mark.asyncio
    async def test_disconnects_and_returns_success(self):
        """Should remove token from keychain and return success"""
        mock_keychain = MagicMock()
        mock_keychain.delete_api_key.return_value = None

        mock_config_service = MagicMock()
        mock_config_service.clear_cache = MagicMock()

        with (
            patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_test"}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config_service,
            ),
        ):
            result = await disconnect_github()

            assert result["success"] is True
            assert result["message"] == "GitHub disconnected"
            mock_keychain.delete_api_key.assert_called_once_with("github_token")

    @pytest.mark.asyncio
    async def test_handles_missing_token_gracefully(self):
        """Should succeed even if no token exists to delete"""
        mock_keychain = MagicMock()
        mock_keychain.delete_api_key.side_effect = KeyError("github_token")

        mock_config_service = MagicMock()
        mock_config_service.clear_cache = MagicMock()

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config_service,
            ),
        ):
            result = await disconnect_github()

            # Should still succeed - key not existing is fine
            assert result["success"] is True
            assert result["message"] == "GitHub disconnected"


class TestIntegrationRegistryGitHubUrl:
    """Tests for GitHub configure_url in INTEGRATION_REGISTRY (Issue #541)"""

    def test_github_configure_url_points_to_settings_page(self):
        """GitHub configure_url should point to dedicated settings page, not setup wizard"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        github_config = INTEGRATION_REGISTRY.get("github")
        assert github_config is not None
        assert github_config["configure_url"] == "/settings/integrations/github"
        # Should NOT point to setup wizard
        assert github_config["configure_url"] != "/setup#step-3"


class TestGitHubConfigServiceKeychainFallback:
    """Tests for GitHubConfigService keychain fallback (Issue #578)"""

    def test_get_token_returns_env_var_first(self):
        """Should return env var token when available (priority over keychain)"""
        from services.integrations.github.config_service import GitHubConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "ghp_keychain_token"

        with (
            patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_env_token"}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = GitHubConfigService()
            config_service.clear_cache()  # Ensure fresh lookup
            token = config_service.get_authentication_token()

            assert token == "ghp_env_token"
            # Keychain should NOT be called when env var is present
            mock_keychain.get_api_key.assert_not_called()

    def test_get_token_falls_back_to_keychain(self):
        """Should fall back to keychain when no env var is set (Issue #578)"""
        from services.integrations.github.config_service import GitHubConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "ghp_keychain_token"

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = GitHubConfigService()
            config_service.clear_cache()  # Ensure fresh lookup
            token = config_service.get_authentication_token()

            assert token == "ghp_keychain_token"
            mock_keychain.get_api_key.assert_called_once_with("github_token")

    def test_get_token_returns_none_when_nothing_configured(self):
        """Should return None when neither env var nor keychain has token"""
        from services.integrations.github.config_service import GitHubConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = GitHubConfigService()
            config_service.clear_cache()  # Ensure fresh lookup
            token = config_service.get_authentication_token()

            assert token is None

    def test_get_token_handles_keychain_error_gracefully(self):
        """Should return None if keychain throws an error"""
        from services.integrations.github.config_service import GitHubConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = Exception("Keychain unavailable")

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = GitHubConfigService()
            config_service.clear_cache()  # Ensure fresh lookup
            token = config_service.get_authentication_token()

            # Should gracefully return None, not raise
            assert token is None

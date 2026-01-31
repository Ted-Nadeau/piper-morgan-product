"""
Tests for IntegrationConfigService

Issue #734: SEC-MULTITENANCY - Multi-Tenancy Isolation Architecture Implementation

This service handles app credentials (client_id, client_secret) which are
server-wide configuration, NOT per-user. User tokens should use UserAPIKeyService.
"""

from unittest.mock import MagicMock, patch

import pytest

from services.integrations.integration_config_service import IntegrationConfigService


class TestIntegrationConfigService:
    """Tests for IntegrationConfigService app credentials handling"""

    def test_get_google_client_id_returns_from_keychain(self):
        """Should retrieve Google client_id from keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "test-google-client-id"

        service = IntegrationConfigService(keychain=mock_keychain)
        result = service.get_google_client_id()

        assert result == "test-google-client-id"
        mock_keychain.get_api_key.assert_called_once_with("google_calendar_client_id")

    def test_get_google_client_secret_returns_from_keychain(self):
        """Should retrieve Google client_secret from keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "test-google-client-secret"

        service = IntegrationConfigService(keychain=mock_keychain)
        result = service.get_google_client_secret()

        assert result == "test-google-client-secret"
        mock_keychain.get_api_key.assert_called_once_with("google_calendar_client_secret")

    def test_get_slack_client_id_returns_from_keychain(self):
        """Should retrieve Slack client_id from keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "test-slack-client-id"

        service = IntegrationConfigService(keychain=mock_keychain)
        result = service.get_slack_client_id()

        assert result == "test-slack-client-id"
        mock_keychain.get_api_key.assert_called_once_with("slack_client_id")

    def test_get_slack_client_secret_returns_from_keychain(self):
        """Should retrieve Slack client_secret from keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "test-slack-client-secret"

        service = IntegrationConfigService(keychain=mock_keychain)
        result = service.get_slack_client_secret()

        assert result == "test-slack-client-secret"
        mock_keychain.get_api_key.assert_called_once_with("slack_client_secret")

    def test_has_google_credentials_returns_true_when_both_present(self):
        """Should return True when both Google credentials are configured"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "google_calendar_client_id": "client-id",
            "google_calendar_client_secret": "client-secret",
        }.get(key)

        service = IntegrationConfigService(keychain=mock_keychain)
        assert service.has_google_credentials() is True

    def test_has_google_credentials_returns_false_when_missing(self):
        """Should return False when Google credentials are missing"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        service = IntegrationConfigService(keychain=mock_keychain)
        assert service.has_google_credentials() is False

    def test_has_slack_credentials_returns_true_when_both_present(self):
        """Should return True when both Slack credentials are configured"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "slack_client_id": "client-id",
            "slack_client_secret": "client-secret",
        }.get(key)

        service = IntegrationConfigService(keychain=mock_keychain)
        assert service.has_slack_credentials() is True

    def test_has_slack_credentials_returns_false_when_missing(self):
        """Should return False when Slack credentials are missing"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        service = IntegrationConfigService(keychain=mock_keychain)
        assert service.has_slack_credentials() is False

    def test_store_google_credentials_stores_both(self):
        """Should store both Google client_id and client_secret"""
        mock_keychain = MagicMock()

        service = IntegrationConfigService(keychain=mock_keychain)
        service.store_google_credentials("new-client-id", "new-client-secret")

        mock_keychain.store_api_key.assert_any_call("google_calendar_client_id", "new-client-id")
        mock_keychain.store_api_key.assert_any_call(
            "google_calendar_client_secret", "new-client-secret"
        )

    def test_store_google_credentials_raises_on_empty(self):
        """Should raise ValueError if credentials are empty"""
        mock_keychain = MagicMock()
        service = IntegrationConfigService(keychain=mock_keychain)

        with pytest.raises(ValueError, match="Both client_id and client_secret are required"):
            service.store_google_credentials("", "secret")

        with pytest.raises(ValueError, match="Both client_id and client_secret are required"):
            service.store_google_credentials("id", "")

    def test_store_slack_credentials_stores_both(self):
        """Should store both Slack client_id and client_secret"""
        mock_keychain = MagicMock()

        service = IntegrationConfigService(keychain=mock_keychain)
        service.store_slack_credentials("new-client-id", "new-client-secret")

        mock_keychain.store_api_key.assert_any_call("slack_client_id", "new-client-id")
        mock_keychain.store_api_key.assert_any_call("slack_client_secret", "new-client-secret")

    def test_get_client_credentials_google(self):
        """Should return Google credentials via generic method"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "google_calendar_client_id": "google-id",
            "google_calendar_client_secret": "google-secret",
        }.get(key)

        service = IntegrationConfigService(keychain=mock_keychain)
        client_id, client_secret = service.get_client_credentials("google")

        assert client_id == "google-id"
        assert client_secret == "google-secret"

    def test_get_client_credentials_slack(self):
        """Should return Slack credentials via generic method"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "slack_client_id": "slack-id",
            "slack_client_secret": "slack-secret",
        }.get(key)

        service = IntegrationConfigService(keychain=mock_keychain)
        client_id, client_secret = service.get_client_credentials("slack")

        assert client_id == "slack-id"
        assert client_secret == "slack-secret"

    def test_get_client_credentials_unknown_provider_raises(self):
        """Should raise ValueError for unknown provider"""
        mock_keychain = MagicMock()
        service = IntegrationConfigService(keychain=mock_keychain)

        with pytest.raises(ValueError, match="Unknown provider"):
            service.get_client_credentials("unknown_provider")

    def test_has_credentials_generic(self):
        """Should check credentials via generic method"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = lambda key: {
            "google_calendar_client_id": "id",
            "google_calendar_client_secret": "secret",
        }.get(key)

        service = IntegrationConfigService(keychain=mock_keychain)
        assert service.has_credentials("google") is True
        assert service.has_credentials("unknown") is False

"""
Integration Configuration Service

Provides read-only access to integration app credentials (client_id, client_secret).
App credentials are server-wide configuration, NOT per-user.

For user tokens (access_token, refresh_token), use UserAPIKeyService instead.

Issue #734 SEC-MULTITENANCY: Multi-Tenancy Isolation Architecture Implementation
"""

import logging
from typing import Optional

from services.infrastructure.keychain_service import KeychainService

logger = logging.getLogger(__name__)


class IntegrationConfigService:
    """
    Service for retrieving integration app credentials.

    This service provides a clean interface for accessing OAuth client credentials
    (client_id, client_secret) that are configured server-wide for the application.

    Usage:
        config_service = IntegrationConfigService()
        client_id = config_service.get_google_client_id()
        client_secret = config_service.get_google_client_secret()

    For user-specific tokens, use UserAPIKeyService instead.
    """

    def __init__(self, keychain: Optional[KeychainService] = None):
        """
        Initialize the integration config service.

        Args:
            keychain: Optional KeychainService for testing injection
        """
        self._keychain = keychain or KeychainService()
        logger.debug("IntegrationConfigService initialized")

    # -------------------------------------------------------------------------
    # Google Calendar OAuth Credentials
    # -------------------------------------------------------------------------

    def get_google_client_id(self) -> Optional[str]:
        """
        Get Google OAuth client ID (app credential).

        Returns:
            Client ID string or None if not configured
        """
        return self._keychain.get_api_key("google_calendar_client_id")

    def get_google_client_secret(self) -> Optional[str]:
        """
        Get Google OAuth client secret (app credential).

        Returns:
            Client secret string or None if not configured
        """
        return self._keychain.get_api_key("google_calendar_client_secret")

    def has_google_credentials(self) -> bool:
        """
        Check if Google OAuth credentials are configured.

        Returns:
            True if both client_id and client_secret are present
        """
        client_id = self.get_google_client_id()
        client_secret = self.get_google_client_secret()
        return bool(client_id and client_secret)

    # -------------------------------------------------------------------------
    # Slack OAuth Credentials
    # -------------------------------------------------------------------------

    def get_slack_client_id(self) -> Optional[str]:
        """
        Get Slack OAuth client ID (app credential).

        Returns:
            Client ID string or None if not configured
        """
        return self._keychain.get_api_key("slack_client_id")

    def get_slack_client_secret(self) -> Optional[str]:
        """
        Get Slack OAuth client secret (app credential).

        Returns:
            Client secret string or None if not configured
        """
        return self._keychain.get_api_key("slack_client_secret")

    def has_slack_credentials(self) -> bool:
        """
        Check if Slack OAuth credentials are configured.

        Returns:
            True if both client_id and client_secret are present
        """
        client_id = self.get_slack_client_id()
        client_secret = self.get_slack_client_secret()
        return bool(client_id and client_secret)

    # -------------------------------------------------------------------------
    # GitHub OAuth Credentials (if needed in future)
    # -------------------------------------------------------------------------

    def get_github_client_id(self) -> Optional[str]:
        """
        Get GitHub OAuth client ID (app credential).

        Note: GitHub integration currently uses personal access tokens,
        but this is provided for future OAuth app support.

        Returns:
            Client ID string or None if not configured
        """
        return self._keychain.get_api_key("github_client_id")

    def get_github_client_secret(self) -> Optional[str]:
        """
        Get GitHub OAuth client secret (app credential).

        Note: GitHub integration currently uses personal access tokens,
        but this is provided for future OAuth app support.

        Returns:
            Client secret string or None if not configured
        """
        return self._keychain.get_api_key("github_client_secret")

    def has_github_oauth_credentials(self) -> bool:
        """
        Check if GitHub OAuth credentials are configured.

        Returns:
            True if both client_id and client_secret are present
        """
        client_id = self.get_github_client_id()
        client_secret = self.get_github_client_secret()
        return bool(client_id and client_secret)

    # -------------------------------------------------------------------------
    # Generic Credential Access
    # -------------------------------------------------------------------------

    def get_client_credentials(self, provider: str) -> tuple[Optional[str], Optional[str]]:
        """
        Get client credentials for a specific provider.

        Args:
            provider: Provider name (google, slack, github)

        Returns:
            Tuple of (client_id, client_secret)

        Raises:
            ValueError: If provider is not recognized
        """
        provider_lower = provider.lower()

        if provider_lower in ("google", "google_calendar"):
            return self.get_google_client_id(), self.get_google_client_secret()
        elif provider_lower == "slack":
            return self.get_slack_client_id(), self.get_slack_client_secret()
        elif provider_lower == "github":
            return self.get_github_client_id(), self.get_github_client_secret()
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def has_credentials(self, provider: str) -> bool:
        """
        Check if credentials are configured for a provider.

        Args:
            provider: Provider name (google, slack, github)

        Returns:
            True if credentials are configured
        """
        provider_lower = provider.lower()

        if provider_lower in ("google", "google_calendar"):
            return self.has_google_credentials()
        elif provider_lower == "slack":
            return self.has_slack_credentials()
        elif provider_lower == "github":
            return self.has_github_oauth_credentials()
        else:
            return False

    # -------------------------------------------------------------------------
    # Credential Storage (Admin Operations)
    # -------------------------------------------------------------------------

    def store_google_credentials(self, client_id: str, client_secret: str) -> None:
        """
        Store Google OAuth credentials.

        Args:
            client_id: Google OAuth client ID
            client_secret: Google OAuth client secret

        Raises:
            ValueError: If credentials are empty
            RuntimeError: If storage fails
        """
        if not client_id or not client_secret:
            raise ValueError("Both client_id and client_secret are required")

        self._keychain.store_api_key("google_calendar_client_id", client_id.strip())
        self._keychain.store_api_key("google_calendar_client_secret", client_secret.strip())
        logger.info("Google OAuth credentials stored")

    def store_slack_credentials(self, client_id: str, client_secret: str) -> None:
        """
        Store Slack OAuth credentials.

        Args:
            client_id: Slack OAuth client ID
            client_secret: Slack OAuth client secret

        Raises:
            ValueError: If credentials are empty
            RuntimeError: If storage fails
        """
        if not client_id or not client_secret:
            raise ValueError("Both client_id and client_secret are required")

        self._keychain.store_api_key("slack_client_id", client_id.strip())
        self._keychain.store_api_key("slack_client_secret", client_secret.strip())
        logger.info("Slack OAuth credentials stored")

    def store_github_credentials(self, client_id: str, client_secret: str) -> None:
        """
        Store GitHub OAuth credentials.

        Args:
            client_id: GitHub OAuth client ID
            client_secret: GitHub OAuth client secret

        Raises:
            ValueError: If credentials are empty
            RuntimeError: If storage fails
        """
        if not client_id or not client_secret:
            raise ValueError("Both client_id and client_secret are required")

        self._keychain.store_api_key("github_client_id", client_id.strip())
        self._keychain.store_api_key("github_client_secret", client_secret.strip())
        logger.info("GitHub OAuth credentials stored")

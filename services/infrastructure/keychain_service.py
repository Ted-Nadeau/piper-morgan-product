"""
Keychain Service for Secure API Key Storage

Provides abstraction over OS keychain for secure storage of API keys
and other sensitive credentials. Uses Python keyring library with
macOS Keychain backend.

Security Features:
- Encrypted storage via OS keychain
- No plaintext credentials in memory longer than necessary
- Automatic fallback to environment variables during migration
- Comprehensive error handling and logging
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

import keyring
import structlog

logger = structlog.get_logger(__name__)

# Service name for keychain entries
SERVICE_NAME = "piper-morgan"


@dataclass
class KeychainEntry:
    """Represents a keychain entry"""

    key: str
    exists_in_keychain: bool
    exists_in_env: bool


class KeychainService:
    """
    Service for secure API key storage in OS keychain

    Provides high-level interface for storing and retrieving
    API keys securely. Handles migration from environment
    variables to keychain storage.

    Usage:
        keychain = KeychainService()

        # Store API key
        keychain.store_api_key("openai", "sk-...")

        # Retrieve API key
        key = keychain.get_api_key("openai")
    """

    def __init__(self, service_name: str = SERVICE_NAME):
        """
        Initialize keychain service

        Args:
            service_name: Service identifier for keychain entries
        """
        self.service_name = service_name
        self._verify_keyring_backend()

    def _verify_keyring_backend(self) -> None:
        """Verify keyring backend is available"""
        try:
            backend = keyring.get_keyring()
            logger.info(
                "Keychain service initialized",
                backend=backend.__class__.__name__,
                service_name=self.service_name,
            )
        except Exception as e:
            logger.error(f"Failed to initialize keyring: {e}")
            raise RuntimeError(f"Keyring initialization failed: {e}")

    def store_api_key(self, provider: str, api_key: str, username: Optional[str] = None) -> None:
        """
        Store API key securely in keychain

        Args:
            provider: Provider name (e.g., "openai", "anthropic")
            api_key: API key to store
            username: Optional username for multi-user support (uses provider as default)

        Raises:
            ValueError: If provider or api_key is empty
            RuntimeError: If storage fails
        """
        if not provider:
            raise ValueError("Provider name cannot be empty")
        if not api_key:
            raise ValueError("API key cannot be empty")

        try:
            keyring.set_password(self.service_name, self._get_key_name(provider, username), api_key)
            log_identifier = f"{username}/{provider}" if username else provider
            logger.info(f"Stored API key for {log_identifier} in keychain")
        except Exception as e:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.error(f"Failed to store API key for {log_identifier}: {e}")
            raise RuntimeError(f"Failed to store API key: {e}")

    def get_api_key(self, provider: str, username: Optional[str] = None) -> Optional[str]:
        """
        Retrieve API key from keychain

        Args:
            provider: Provider name (e.g., "openai", "anthropic")
            username: Optional username for multi-user support (uses provider as default)

        Returns:
            API key if found, None otherwise
        """
        if not provider:
            return None

        try:
            key = keyring.get_password(self.service_name, self._get_key_name(provider, username))
            if key:
                log_identifier = f"{username}/{provider}" if username else provider
                logger.debug(f"Retrieved API key for {log_identifier} from keychain")
            return key
        except Exception as e:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.error(f"Failed to retrieve API key for {log_identifier}: {e}")
            return None

    def delete_api_key(self, provider: str, username: Optional[str] = None) -> bool:
        """
        Delete API key from keychain

        Args:
            provider: Provider name
            username: Optional username for multi-user support (uses provider as default)

        Returns:
            True if deleted, False if not found or error
        """
        if not provider:
            return False

        try:
            keyring.delete_password(self.service_name, self._get_key_name(provider, username))
            log_identifier = f"{username}/{provider}" if username else provider
            logger.info(f"Deleted API key for {log_identifier} from keychain")
            return True
        except keyring.errors.PasswordDeleteError:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.debug(f"No API key found for {log_identifier} to delete")
            return False
        except Exception as e:
            log_identifier = f"{username}/{provider}" if username else provider
            logger.error(f"Failed to delete API key for {log_identifier}: {e}")
            return False

    def list_stored_keys(self) -> List[str]:
        """
        List all providers with keys stored in keychain

        Note: keyring doesn't provide a list API, so this returns
        known providers that we check for.

        Returns:
            List of provider names with stored keys
        """
        known_providers = ["openai", "anthropic", "gemini", "perplexity"]
        stored = []

        for provider in known_providers:
            if self.get_api_key(provider) is not None:
                stored.append(provider)

        return stored

    def check_migration_status(self, providers: List[str]) -> Dict[str, KeychainEntry]:
        """
        Check migration status for given providers

        Checks both keychain and environment variables to determine
        which keys need to be migrated.

        Args:
            providers: List of provider names to check

        Returns:
            Dict mapping provider to KeychainEntry status
        """
        import os

        status = {}
        for provider in providers:
            keychain_key = self.get_api_key(provider)
            env_key = os.getenv(self._get_env_var_name(provider))

            status[provider] = KeychainEntry(
                key=provider,
                exists_in_keychain=keychain_key is not None,
                exists_in_env=env_key is not None,
            )

        return status

    def _get_key_name(self, provider: str, username: Optional[str] = None) -> str:
        """
        Get keychain entry name for provider

        Args:
            provider: Provider name
            username: Optional username for multi-user support

        Returns:
            Keychain entry name (e.g., "openai_api_key" or "user123_openai_api_key")
        """
        if username:
            return f"{username}_{provider}_api_key"
        return f"{provider}_api_key"

    def _get_env_var_name(self, provider: str) -> str:
        """
        Get environment variable name for provider

        Args:
            provider: Provider name

        Returns:
            Environment variable name
        """
        return f"{provider.upper()}_API_KEY"


# Convenience instance for global access
_keychain_service = None


def get_keychain_service() -> KeychainService:
    """
    Get global keychain service instance

    Returns:
        KeychainService instance
    """
    global _keychain_service
    if _keychain_service is None:
        _keychain_service = KeychainService()
    return _keychain_service

"""
Notion Configuration Service
Implements ADR-010 Configuration Access Patterns for Notion integration components.

Provides centralized configuration management for Notion operations including:
- Authentication and API key management
- API rate limiting and retry configuration
- Feature flags for Notion integrations
- Environment-specific settings

Note: Replaces static config/notion_config.py with service injection pattern
Legacy file preserved for backward compatibility during migration
"""

import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from services.infrastructure.config.feature_flags import FeatureFlags


class NotionEnvironment(Enum):
    """Notion environment types"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class NotionConfig:
    """Notion configuration settings"""

    # Authentication
    api_key: str = ""
    workspace_id: str = ""

    # API Configuration
    api_base_url: str = "https://api.notion.com/v1"
    timeout_seconds: int = 30
    max_retries: int = 3

    # Rate Limiting
    requests_per_minute: int = 30  # Notion's rate limit

    # Feature Flags
    enable_spatial_mapping: bool = True

    # Environment
    environment: NotionEnvironment = NotionEnvironment.DEVELOPMENT

    def get_api_key(self) -> str:
        """Get API key (interface compatibility with legacy config)"""
        return self.api_key

    def get_workspace_id(self) -> str:
        """Get workspace ID (interface compatibility with legacy config)"""
        return self.workspace_id

    def validate(self) -> bool:
        """Validate configuration settings"""
        return bool(self.api_key)


class NotionConfigService:
    """
    Notion configuration service following ADR-010 patterns.

    Issue #734: Updated for multi-tenancy isolation.
    All user-scoped methods now require user_id parameter.
    """

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        # Per-user config cache (keyed by user_id)
        self._config_cache: Dict[str, NotionConfig] = {}

    def get_config(self, user_id: str) -> NotionConfig:
        """
        Get Notion configuration with environment variable loading.

        Implements standard config service interface for plugin architecture.
        Returns NotionConfig object with all settings loaded from environment.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            NotionConfig: Complete Notion configuration with user-scoped API key

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")

        if user_id not in self._config_cache:
            self._config_cache[user_id] = self._load_config(user_id)
        return self._config_cache[user_id]

    def _load_from_user_config(self) -> Dict[str, Any]:
        """
        Load Notion configuration from PIPER.user.md.

        Parses YAML blocks from the markdown file and extracts the notion section.
        Follows the same pattern as Calendar and GitHub config loading.

        Returns:
            Dict with Notion configuration, or empty dict if not found/invalid
        """
        try:
            user_config_path = Path("config/PIPER.user.md")
            if not user_config_path.exists():
                return {}

            # Read the markdown file
            content = user_config_path.read_text()

            # Find the Notion Integration section
            # Look for heading pattern: ## Notion Integration
            notion_section_match = re.search(
                r"##\s+\U0001F4DD\s+Notion Integration(.*?)(?=##\s+|$)", content, re.DOTALL
            )

            if not notion_section_match:
                return {}

            section_content = notion_section_match.group(1)

            # Extract YAML from markdown code blocks
            yaml_match = re.search(r"```yaml.*?```", section_content, re.DOTALL)
            if not yaml_match:
                return {}

            # Extract YAML content by removing markdown markers
            full_yaml_block = yaml_match.group(0)
            yaml_content = full_yaml_block.replace("```yaml", "").replace("```", "").strip()
            config_data = yaml.safe_load(yaml_content)

            if config_data and "notion" in config_data:
                return config_data["notion"]

            return {}

        except Exception as e:
            # Log error but don't crash - graceful fallback
            print(f"Warning: Could not load Notion config from PIPER.user.md: {e}")
            return {}

    def _load_config(self, user_id: str) -> NotionConfig:
        """
        Load Notion configuration with priority: env vars > PIPER.user.md > keychain > defaults.

        Configuration Priority Order:
        1. Environment variables (highest priority - overrides everything)
        2. PIPER.user.md notion section (middle priority)
        3. User-scoped keychain (UI-saved keys via UserAPIKeyService)
        4. Hardcoded defaults (lowest priority - fallback)

        Args:
            user_id: User identifier for scoping credentials

        Returns:
            NotionConfig: Configuration loaded with priority order applied

        Issue #579: Added keychain fallback for UI-configured keys.
        Issue #734: Keychain lookups now scoped by user_id.
        """
        # Load from PIPER.user.md first (base layer)
        user_config = self._load_from_user_config()

        # Get authentication section (with fallback to empty dict)
        auth_config = user_config.get("authentication", {})

        # Get API key with fallback chain: env var > user config > user-scoped keychain
        api_key = os.getenv("NOTION_API_KEY", auth_config.get("api_key", ""))

        # Issue #579/#734: Fallback to user-scoped keychain if not found in env or user config
        if not api_key:
            try:
                from services.infrastructure.keychain_service import KeychainService

                keychain = KeychainService()
                # User-scoped API key lookup (per ADR-058)
                api_key = keychain.get_api_key("notion", username=user_id) or ""
            except Exception:
                pass  # Keychain not available

        # Environment variables override user config for all settings
        return NotionConfig(
            api_key=api_key,
            workspace_id=os.getenv("NOTION_WORKSPACE_ID", auth_config.get("workspace_id", "")),
            api_base_url=os.getenv(
                "NOTION_API_BASE_URL",
                user_config.get("api_base_url", "https://api.notion.com/v1"),
            ),
            timeout_seconds=int(
                os.getenv(
                    "NOTION_TIMEOUT_SECONDS",
                    str(user_config.get("timeout_seconds", 30)),
                )
            ),
            max_retries=int(
                os.getenv(
                    "NOTION_MAX_RETRIES",
                    str(user_config.get("max_retries", 3)),
                )
            ),
            requests_per_minute=int(
                os.getenv(
                    "NOTION_RATE_LIMIT_RPM",
                    str(user_config.get("requests_per_minute", 30)),
                )
            ),
            enable_spatial_mapping=self.feature_flags.is_enabled("notion_spatial_mapping"),
            environment=NotionEnvironment(
                os.getenv("NOTION_ENVIRONMENT", user_config.get("environment", "development"))
            ),
        )

    def is_configured(self, user_id: str) -> bool:
        """
        Check if Notion is properly configured for the given user.

        Implements standard config service interface for plugin architecture.
        Validates that API key exists, which is the minimum requirement for Notion operations.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            bool: True if Notion is properly configured

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")
        config = self.get_config(user_id)
        return config.validate()

    def get_environment(self, user_id: str) -> NotionEnvironment:
        """
        Get current Notion environment.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            NotionEnvironment enum value

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")
        return self.get_config(user_id).environment

    def is_production(self, user_id: str) -> bool:
        """
        Check if running in production environment.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            True if in production environment

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")
        return self.get_environment(user_id) == NotionEnvironment.PRODUCTION

    def clear_cache(self, user_id: Optional[str] = None) -> None:
        """
        Clear configuration cache.

        Args:
            user_id: If provided, clear only that user's cache.
                     If None, clear entire cache.

        Issue #734: Added for multi-tenancy support.
        """
        if user_id:
            self._config_cache.pop(user_id, None)
        else:
            self._config_cache.clear()

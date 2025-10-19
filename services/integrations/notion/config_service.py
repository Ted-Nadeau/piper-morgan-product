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
    """Notion configuration service following ADR-010 patterns"""

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        self._config: Optional[NotionConfig] = None

    def get_config(self) -> NotionConfig:
        """
        Get Notion configuration with environment variable loading.

        Implements standard config service interface for plugin architecture.
        Returns NotionConfig object with all settings loaded from environment.

        Returns:
            NotionConfig: Complete Notion configuration
        """
        if self._config is None:
            self._config = self._load_config()
        return self._config

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
            # Look for heading pattern: ## 📝 Notion Integration
            notion_section_match = re.search(
                r"##\s+📝\s+Notion Integration(.*?)(?=##\s+|$)", content, re.DOTALL
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

    def _load_config(self) -> NotionConfig:
        """
        Load Notion configuration with priority: env vars > PIPER.user.md > defaults.

        Configuration Priority Order:
        1. Environment variables (highest priority - overrides everything)
        2. PIPER.user.md notion section (middle priority)
        3. Hardcoded defaults (lowest priority - fallback)

        Implements standard config service interface for plugin architecture.

        Returns:
            NotionConfig: Configuration loaded with priority order applied
        """
        # Load from PIPER.user.md first (base layer)
        user_config = self._load_from_user_config()

        # Get authentication section (with fallback to empty dict)
        auth_config = user_config.get("authentication", {})

        # Environment variables override user config for all settings
        return NotionConfig(
            api_key=os.getenv("NOTION_API_KEY", auth_config.get("api_key", "")),
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

    def is_configured(self) -> bool:
        """
        Check if Notion is properly configured.

        Implements standard config service interface for plugin architecture.
        Validates that API key exists, which is the minimum requirement for Notion operations.

        Returns:
            bool: True if Notion is properly configured
        """
        config = self.get_config()
        return config.validate()

    def get_environment(self) -> NotionEnvironment:
        """Get current Notion environment"""
        return self.get_config().environment

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.get_environment() == NotionEnvironment.PRODUCTION

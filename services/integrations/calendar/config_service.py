"""
Calendar Configuration Service

Implements ADR-010 Configuration Access Patterns for Calendar integration.
Provides centralized configuration management for Google Calendar operations.
"""

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from services.infrastructure.config.feature_flags import FeatureFlags


@dataclass
class CalendarConfig:
    """Calendar configuration settings"""

    # OAuth 2.0 Configuration
    client_secrets_file: str = "credentials.json"
    token_file: str = "token.json"

    # API Configuration
    calendar_id: str = "primary"
    scopes: List[str] = field(
        default_factory=lambda: ["https://www.googleapis.com/auth/calendar.readonly"]
    )

    # Timeouts
    timeout_seconds: int = 30

    # Circuit Breaker
    circuit_timeout: int = 300  # 5 minutes
    error_threshold: int = 5

    # Feature Flags
    enable_spatial_mapping: bool = True

    def validate(self) -> bool:
        """Validate configuration settings"""
        # Check if credential file exists
        # Token file is created during OAuth flow, so it's optional for validation
        return os.path.exists(self.client_secrets_file)


class CalendarConfigService:
    """
    Calendar configuration service following ADR-010 patterns.

    Implements standard config service interface for plugin architecture:
    - get_config() -> CalendarConfig: Returns complete configuration
    - is_configured() -> bool: Validates required config present
    - _load_config() -> CalendarConfig: Loads config from environment

    Provides centralized configuration management for Google Calendar operations
    including OAuth credentials, API settings, and feature flags.
    """

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        self._config: Optional[CalendarConfig] = None

    def get_config(self) -> CalendarConfig:
        """
        Get Calendar configuration with environment variable loading.

        Implements standard config service interface for plugin architecture.
        Returns CalendarConfig object with all settings loaded from environment.

        Returns:
            CalendarConfig: Complete Calendar configuration
        """
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def _load_from_user_config(self) -> Dict[str, Any]:
        """
        Load calendar configuration from PIPER.user.md.

        Parses YAML blocks from the markdown file and extracts the calendar section.
        Follows the same pattern as GitHub and Standup config loading.

        Returns:
            Dict with calendar configuration, or empty dict if not found/invalid
        """
        try:
            user_config_path = Path("config/PIPER.user.md")
            if not user_config_path.exists():
                return {}

            # Read the markdown file
            content = user_config_path.read_text()

            # Find the Calendar Integration section
            # Look for heading pattern: ## 📅 Calendar Integration
            calendar_section_match = re.search(
                r"##\s+📅\s+Calendar Integration(.*?)(?=##\s+|$)", content, re.DOTALL
            )

            if not calendar_section_match:
                return {}

            section_content = calendar_section_match.group(1)

            # Extract YAML from markdown code blocks (more robust)
            yaml_match = re.search(r"```yaml.*?```", section_content, re.DOTALL)
            if not yaml_match:
                return {}

            # Extract YAML content by removing markdown markers
            full_yaml_block = yaml_match.group(0)
            yaml_content = full_yaml_block.replace("```yaml", "").replace("```", "").strip()
            config_data = yaml.safe_load(yaml_content)

            if config_data and "calendar" in config_data:
                return config_data["calendar"]

            return {}

        except Exception as e:
            # Log error but don't crash - graceful fallback
            print(f"Warning: Could not load calendar config from PIPER.user.md: {e}")
            return {}

    def _load_config(self) -> CalendarConfig:
        """
        Load calendar configuration with priority: env vars > PIPER.user.md > defaults.

        Configuration Priority Order:
        1. Environment variables (highest priority - overrides everything)
        2. PIPER.user.md calendar section (middle priority)
        3. Hardcoded defaults (lowest priority - fallback)

        Implements standard config service interface for plugin architecture.

        Returns:
            CalendarConfig: Configuration loaded with priority order applied
        """
        # Load from PIPER.user.md first (base layer)
        user_config = self._load_from_user_config()

        # Parse scopes with priority order
        if "GOOGLE_CALENDAR_SCOPES" in os.environ:
            # Environment variable present - use it
            scopes_env = os.getenv("GOOGLE_CALENDAR_SCOPES")
            scopes = [s.strip() for s in scopes_env.split(",") if s.strip()]
        elif "scopes" in user_config:
            # Use PIPER.user.md scopes
            scopes = user_config["scopes"]
        else:
            # Use default
            scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

        # Environment variables override user config for all other settings
        return CalendarConfig(
            client_secrets_file=os.getenv(
                "GOOGLE_CLIENT_SECRETS_FILE",
                user_config.get("client_secrets_file", "credentials.json"),
            ),
            token_file=os.getenv("GOOGLE_TOKEN_FILE", user_config.get("token_file", "token.json")),
            calendar_id=os.getenv("GOOGLE_CALENDAR_ID", user_config.get("calendar_id", "primary")),
            scopes=scopes,
            timeout_seconds=int(
                os.getenv("GOOGLE_CALENDAR_TIMEOUT", str(user_config.get("timeout_seconds", 30)))
            ),
            circuit_timeout=int(
                os.getenv(
                    "GOOGLE_CALENDAR_CIRCUIT_TIMEOUT",
                    str(user_config.get("circuit_timeout", 300)),
                )
            ),
            error_threshold=int(
                os.getenv(
                    "GOOGLE_CALENDAR_ERROR_THRESHOLD",
                    str(user_config.get("error_threshold", 5)),
                )
            ),
            enable_spatial_mapping=self.feature_flags.is_enabled("calendar_spatial_mapping"),
        )

    def is_configured(self) -> bool:
        """
        Check if Calendar is properly configured.

        Implements standard config service interface for plugin architecture.
        Validates that OAuth credentials file exists, which is the minimum
        requirement for Google Calendar operations.

        Returns:
            bool: True if Calendar is properly configured
        """
        config = self.get_config()
        return config.validate()

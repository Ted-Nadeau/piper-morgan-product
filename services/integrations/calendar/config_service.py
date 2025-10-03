"""
Calendar Configuration Service

Implements ADR-010 Configuration Access Patterns for Calendar integration.
Provides centralized configuration management for Google Calendar operations.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional

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

    def _load_config(self) -> CalendarConfig:
        """
        Load configuration from environment variables.

        Implements standard config service interface for plugin architecture.
        Reads configuration from environment variables with sensible defaults.

        Returns:
            CalendarConfig: Configuration loaded from environment
        """
        # Parse scopes from comma-separated env var
        scopes_env = os.getenv(
            "GOOGLE_CALENDAR_SCOPES", "https://www.googleapis.com/auth/calendar.readonly"
        )
        scopes = [s.strip() for s in scopes_env.split(",") if s.strip()]

        return CalendarConfig(
            client_secrets_file=os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json"),
            token_file=os.getenv("GOOGLE_TOKEN_FILE", "token.json"),
            calendar_id=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            scopes=scopes,
            timeout_seconds=int(os.getenv("GOOGLE_CALENDAR_TIMEOUT", "30")),
            circuit_timeout=int(os.getenv("GOOGLE_CALENDAR_CIRCUIT_TIMEOUT", "300")),
            error_threshold=int(os.getenv("GOOGLE_CALENDAR_ERROR_THRESHOLD", "5")),
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

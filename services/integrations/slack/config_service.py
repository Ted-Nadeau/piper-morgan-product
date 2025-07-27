"""
Slack Configuration Service
Implements ADR-010 Configuration Access Patterns for Slack integration components.

Provides centralized configuration management for Slack operations including:
- Authentication and token management
- API rate limiting and retry configuration
- Feature flags for Slack integrations
- Environment-specific settings
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from services.infrastructure.config.feature_flags import FeatureFlags


class SlackEnvironment(Enum):
    """Slack environment types"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class SlackConfig:
    """Slack configuration settings"""

    # Authentication
    bot_token: str = ""
    app_token: str = ""
    signing_secret: str = ""

    # API Configuration
    api_base_url: str = "https://slack.com/api"
    timeout_seconds: int = 30
    max_retries: int = 3

    # Rate Limiting
    requests_per_minute: int = 50
    burst_limit: int = 10

    # Feature Flags
    enable_webhooks: bool = True
    enable_socket_mode: bool = False
    enable_spatial_mapping: bool = True

    # Environment
    environment: SlackEnvironment = SlackEnvironment.DEVELOPMENT

    # OAuth Settings
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""

    # Webhook Configuration
    webhook_url: str = ""
    default_channel: str = ""

    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.bot_token:
            return False
        if self.enable_webhooks and not self.webhook_url:
            return False
        return True


class SlackConfigService:
    """Slack configuration service following ADR-010 patterns"""

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        self._config: Optional[SlackConfig] = None

    def get_config(self) -> SlackConfig:
        """Get Slack configuration with environment variable loading"""
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def _load_config(self) -> SlackConfig:
        """Load configuration from environment variables"""
        return SlackConfig(
            bot_token=os.getenv("SLACK_BOT_TOKEN", ""),
            app_token=os.getenv("SLACK_APP_TOKEN", ""),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET", ""),
            api_base_url=os.getenv("SLACK_API_BASE_URL", "https://slack.com/api"),
            timeout_seconds=int(os.getenv("SLACK_TIMEOUT_SECONDS", "30")),
            max_retries=int(os.getenv("SLACK_MAX_RETRIES", "3")),
            requests_per_minute=int(os.getenv("SLACK_RATE_LIMIT_RPM", "50")),
            burst_limit=int(os.getenv("SLACK_BURST_LIMIT", "10")),
            enable_webhooks=self.feature_flags.is_enabled("slack_webhooks"),
            enable_socket_mode=self.feature_flags.is_enabled("slack_socket_mode"),
            enable_spatial_mapping=self.feature_flags.is_enabled("slack_spatial_mapping"),
            environment=SlackEnvironment(os.getenv("SLACK_ENVIRONMENT", "development")),
            client_id=os.getenv("SLACK_CLIENT_ID", ""),
            client_secret=os.getenv("SLACK_CLIENT_SECRET", ""),
            redirect_uri=os.getenv("SLACK_REDIRECT_URI", ""),
            webhook_url=os.getenv("SLACK_WEBHOOK_URL", ""),
            default_channel=os.getenv("SLACK_DEFAULT_CHANNEL", ""),
        )

    def is_configured(self) -> bool:
        """Check if Slack is properly configured"""
        config = self.get_config()
        return config.validate()

    def get_environment(self) -> SlackEnvironment:
        """Get current Slack environment"""
        return self.get_config().environment

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.get_environment() == SlackEnvironment.PRODUCTION

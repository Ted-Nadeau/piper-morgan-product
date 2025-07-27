"""
Slack Integration Module
Implements Slack API integration following established patterns from GitHub integration.

Provides:
- Configuration management (ADR-010 compliant)
- Production client with error handling
- Spatial metaphor architecture (via spatial_mapper)
- Webhook and OAuth support
"""

from .config_service import SlackConfigService
from .slack_client import SlackClient

__all__ = ["SlackConfigService", "SlackClient"]

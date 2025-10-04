"""Configuration service for Demo integration

This is a template showing the standard config service pattern.
Copy and adapt this for your own integrations.
"""

import os
from typing import Optional


class DemoConfigService:
    """Manages configuration for Demo integration

    This service demonstrates the standard pattern:
    - Read from environment variables
    - Provide sensible defaults
    - Include is_configured() check
    """

    def __init__(self):
        # Configuration from environment
        self.api_key = os.getenv("DEMO_API_KEY", "")
        self.api_endpoint = os.getenv("DEMO_API_ENDPOINT", "https://api.example.com")
        self.enabled = os.getenv("DEMO_ENABLED", "true").lower() == "true"

    def is_configured(self) -> bool:
        """Check if integration is properly configured

        Returns:
            bool: True if all required config present
        """
        # For demo purposes, always configured
        # Real integrations should check API keys, etc.
        return self.enabled

    def get_api_key(self) -> Optional[str]:
        """Get API key if configured

        Returns:
            Optional[str]: API key or None
        """
        return self.api_key if self.api_key else None

    def get_endpoint(self) -> str:
        """Get API endpoint

        Returns:
            str: API endpoint URL
        """
        return self.api_endpoint

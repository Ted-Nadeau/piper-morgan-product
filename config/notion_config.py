"""Notion integration configuration."""

import os
from typing import Optional


class NotionConfig:
    """Notion API configuration."""

    @staticmethod
    def get_api_key() -> Optional[str]:
        """Get Notion API key from environment."""
        return os.environ.get("NOTION_API_KEY")

    @staticmethod
    def get_workspace_id() -> Optional[str]:
        """Get default workspace ID."""
        return os.environ.get("NOTION_WORKSPACE_ID")

    @staticmethod
    def validate_config() -> bool:
        """Validate Notion configuration."""
        api_key = NotionConfig.get_api_key()
        if not api_key:
            print("WARNING: NOTION_API_KEY not set")
            return False
        if not api_key.startswith("secret_"):
            print("WARNING: NOTION_API_KEY format may be invalid")
            return False
        return True

    @staticmethod
    def get_config_status() -> dict:
        """Get detailed configuration status."""
        api_key = NotionConfig.get_api_key()
        workspace_id = NotionConfig.get_workspace_id()

        return {
            "api_key_set": bool(api_key),
            "api_key_format_valid": bool(api_key and api_key.startswith("secret_")),
            "workspace_id_set": bool(workspace_id),
            "fully_configured": NotionConfig.validate_config() and bool(workspace_id),
        }

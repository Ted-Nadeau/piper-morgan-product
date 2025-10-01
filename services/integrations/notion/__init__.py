"""
Notion Integration Module

Provides router-based access to Notion integrations with feature flag control.
"""

from .notion_integration_router import NotionIntegrationRouter, create_notion_integration

__all__ = ["NotionIntegrationRouter", "create_notion_integration"]

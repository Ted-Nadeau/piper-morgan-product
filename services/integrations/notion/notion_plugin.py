"""
Notion Integration Plugin

Wraps Notion integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata

from .config_service import NotionConfigService
from .notion_integration_router import NotionIntegrationRouter


class NotionPlugin(PiperPlugin):
    """
    Notion workspace integration plugin.

    Provides Notion integration routes and MCP capabilities through
    the plugin system.
    """

    def __init__(self):
        """Initialize Notion plugin with config service"""
        self.config_service = NotionConfigService()
        self.integration_router = NotionIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return Notion plugin metadata"""
        return PluginMetadata(
            name="notion",
            version="1.0.0",
            description="Notion workspace integration with MCP",
            author="Piper Morgan Team",
            capabilities=["routes", "mcp"],  # Notion uses MCP
            dependencies=[],
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with Notion routes.

        Creates APIRouter wrapper around NotionIntegrationRouter
        for plugin system compatibility.
        """
        if self._api_router is None:
            self._api_router = APIRouter(prefix="/api/v1/integrations/notion", tags=["notion"])

            # Simple status endpoint for plugin
            @self._api_router.get("/status")
            async def notion_status():
                """Get Notion integration status"""
                return {
                    "configured": self.is_configured(),
                    "spatial_enabled": self.integration_router.use_spatial,
                    "legacy_allowed": self.integration_router.allow_legacy,
                }

        return self._api_router

    def is_configured(self) -> bool:
        """Check if Notion is properly configured.

        Note: At plugin startup, there's no user context available.
        This returns False until a user context is established.
        Issue #781: Fixed crash from calling is_configured() without user_id.
        """
        # Without user context, we can't determine configuration
        # The config_service.is_configured() requires user_id (Issue #734)
        return False

    async def initialize(self) -> None:
        """
        Initialize Notion plugin.

        Performs any startup initialization needed for Notion integration.
        """
        if self.is_configured():
            print(
                f"  ✅ Notion plugin initialized (spatial: {self.integration_router.use_spatial})"
            )
        else:
            print(f"  ⚠️  Notion plugin initialized but not configured")

    async def shutdown(self) -> None:
        """
        Cleanup Notion plugin resources.

        Performs any cleanup needed when shutting down.
        """
        # Any cleanup needed
        pass

    def get_status(self) -> Dict[str, Any]:
        """
        Get Notion plugin status.

        Returns detailed status information for monitoring.
        """
        return {
            "configured": self.is_configured(),
            "config_service": "active",
            "router": "active" if self._api_router else "inactive",
            "spatial_enabled": self.integration_router.use_spatial,
            "legacy_allowed": self.integration_router.allow_legacy,
            "integration_router": "active",
        }


# Auto-register plugin when module is imported
from services.plugins import get_plugin_registry

_notion_plugin = NotionPlugin()
get_plugin_registry().register(_notion_plugin)

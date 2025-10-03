"""
Calendar Integration Plugin

Wraps Calendar integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata

from .calendar_integration_router import CalendarIntegrationRouter
from .config_service import CalendarConfigService


class CalendarPlugin(PiperPlugin):
    """
    Google Calendar integration plugin.

    Provides Calendar integration routes and spatial intelligence
    through the plugin system.
    """

    def __init__(self):
        """Initialize Calendar plugin with config service"""
        self.config_service = CalendarConfigService()
        self.integration_router = CalendarIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return Calendar plugin metadata"""
        return PluginMetadata(
            name="calendar",
            version="1.0.0",
            description="Google Calendar integration with spatial intelligence",
            author="Piper Morgan Team",
            capabilities=["routes", "spatial"],  # Calendar has spatial
            dependencies=[],
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with Calendar routes.

        Creates APIRouter wrapper around CalendarIntegrationRouter.
        """
        if self._api_router is None:
            self._api_router = APIRouter(prefix="/api/v1/integrations/calendar", tags=["calendar"])

            @self._api_router.get("/status")
            async def calendar_status():
                """Get Calendar integration status"""
                return {
                    "configured": self.is_configured(),
                    "spatial_enabled": self.integration_router.use_spatial,
                    "legacy_allowed": self.integration_router.allow_legacy,
                }

        return self._api_router

    def is_configured(self) -> bool:
        """Check if Calendar is properly configured"""
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        """Initialize Calendar plugin"""
        if self.is_configured():
            print(
                f"  ✅ Calendar plugin initialized (spatial: {self.integration_router.use_spatial})"
            )
        else:
            print(f"  ⚠️  Calendar plugin initialized but not configured")

    async def shutdown(self) -> None:
        """Cleanup Calendar plugin resources"""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get Calendar plugin status"""
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

_calendar_plugin = CalendarPlugin()
get_plugin_registry().register(_calendar_plugin)

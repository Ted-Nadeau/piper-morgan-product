"""Demo integration plugin wrapper

This demonstrates the standard plugin wrapper pattern.
Plugins are thin adapters that wrap routers to implement the PiperPlugin interface.
"""

from typing import Any, Dict

from fastapi import APIRouter

from services.plugins.plugin_interface import PiperPlugin, PluginMetadata

from .config_service import DemoConfigService
from .demo_integration_router import DemoIntegrationRouter


class DemoPlugin(PiperPlugin):
    """Demo plugin wrapper showing standard patterns

    This is a template showing the minimal plugin wrapper:
    - Implements all 6 PiperPlugin interface methods
    - Wraps an integration router
    - Uses config service for configuration
    - Provides metadata
    - Handles lifecycle (initialize/shutdown)

    Copy this pattern for your own plugins.
    """

    def __init__(self):
        """Initialize plugin with config and router

        Standard pattern:
        1. Create config service
        2. Create router with config
        3. Store both for interface methods
        """
        self.config_service = DemoConfigService()
        self.router_instance = DemoIntegrationRouter(self.config_service)

    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata

        Metadata describes the plugin's capabilities and identity.

        Returns:
            PluginMetadata with name, version, description, etc.
        """
        return PluginMetadata(
            name="demo",
            version="1.0.0",  # Use semantic versioning
            description="Demo integration template for developers",
            author="Piper Morgan Team",
            capabilities=["routes"],  # What this plugin provides
        )

    def get_router(self) -> APIRouter:
        """Return FastAPI router

        The router will be mounted into the main application.

        Returns:
            APIRouter with all integration routes
        """
        return self.router_instance.router

    def is_configured(self) -> bool:
        """Check if plugin is configured

        Delegates to config service to check configuration.

        Returns:
            bool: True if configured and ready to use
        """
        return self.config_service.is_configured()

    async def initialize(self):
        """Initialize plugin on startup

        Called when application starts.
        Use for:
        - Setting up connections
        - Loading resources
        - Validating configuration

        For demo, no initialization needed.
        """
        # Demo plugin needs no initialization
        # Real integrations might connect to APIs here
        pass

    async def shutdown(self):
        """Cleanup on shutdown

        Called when application stops.
        Use for:
        - Closing connections
        - Releasing resources
        - Cleanup tasks

        For demo, no cleanup needed.
        """
        # Demo plugin needs no cleanup
        # Real integrations might close connections here
        pass

    def get_status(self) -> Dict[str, Any]:
        """Return plugin status

        Provides runtime information about the plugin.

        Returns:
            Dict with status information
        """
        return {
            "configured": self.is_configured(),
            "router_prefix": self.router_instance.router.prefix,
            "routes": len(self.router_instance.router.routes),
            "tags": self.router_instance.router.tags,
        }


# Auto-registration
# This code runs when the module is imported, registering the plugin
from services.plugins import get_plugin_registry

_demo_plugin = DemoPlugin()
get_plugin_registry().register(_demo_plugin)

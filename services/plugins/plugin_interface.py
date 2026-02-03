"""
Plugin Interface for Piper Integration Plugins

Defines the abstract base class and types that all integration plugins
must implement to participate in the plugin architecture.

Phase 3A: Foundation for plugin system - interface definition only.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from fastapi import APIRouter


@dataclass
class PluginMetadata:
    """
    Metadata about a plugin.

    Provides information about plugin identity, version, capabilities,
    and dependencies.

    Example:
        metadata = PluginMetadata(
            name="slack",
            version="1.0.0",
            description="Slack integration plugin",
            author="Piper Team",
            capabilities=["routes", "webhooks", "spatial"],
            dependencies=[]
        )
    """

    # Identity
    name: str  # Unique plugin identifier (e.g., "slack", "notion")
    version: str  # Semantic version (e.g., "1.0.0")
    description: str  # Human-readable description
    author: str  # Plugin author/maintainer

    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    # Supported capability types:
    # - "routes": Plugin provides HTTP routes
    # - "webhooks": Plugin handles webhook callbacks
    # - "spatial": Plugin uses spatial intelligence
    # - "mcp": Plugin uses Model Context Protocol
    # - "background": Plugin runs background tasks

    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    # Other plugins this plugin requires (by name)


class PiperPlugin(ABC):
    """
    Abstract base class for Piper integration plugins.

    All integration plugins (Slack, Notion, GitHub, Calendar) must
    implement this interface. The plugin system uses this interface
    to manage plugin lifecycle, routes, and status.

    Minimal Required Methods:
    - get_metadata(): Plugin identity and capabilities
    - get_router(): FastAPI routes (if any)
    - is_configured(): Configuration validation
    - initialize(): Startup initialization
    - shutdown(): Cleanup and resource release
    - get_status(): Health and status reporting

    Example Plugin:
        ```python
        class MyPlugin(PiperPlugin):
            def get_metadata(self) -> PluginMetadata:
                return PluginMetadata(
                    name="my_plugin",
                    version="1.0.0",
                    description="My integration plugin",
                    author="Developer Name",
                    capabilities=["routes"],
                    dependencies=[]
                )

            def get_router(self) -> Optional[APIRouter]:
                router = APIRouter(prefix="/api/v1/my-plugin")

                @router.get("/status")
                async def status():
                    return {"status": "active"}

                return router

            def is_configured(self) -> bool:
                return True  # Check actual configuration

            async def initialize(self) -> None:
                # Setup resources
                pass

            async def shutdown(self) -> None:
                # Cleanup resources
                pass

            def get_status(self) -> Dict[str, Any]:
                return {
                    "configured": self.is_configured(),
                    "active": True
                }
        ```

    Lifecycle:
        1. Plugin instantiated
        2. Plugin registered with registry
        3. initialize() called at app startup
        4. Routes active, status queryable
        5. shutdown() called at app shutdown
    """

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """
        Return plugin metadata.

        Provides information about plugin identity, version,
        capabilities, and dependencies.

        Returns:
            PluginMetadata: Plugin information

        Example:
            return PluginMetadata(
                name="slack",
                version="1.0.0",
                description="Slack integration",
                author="Piper Team",
                capabilities=["routes", "webhooks", "spatial"],
                dependencies=[]
            )
        """
        pass

    @abstractmethod
    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with plugin routes.

        If the plugin provides HTTP routes, return an APIRouter
        with those routes configured. If the plugin has no routes,
        return None.

        The router will be mounted automatically by the plugin system
        during application startup.

        Returns:
            Optional[APIRouter]: Router with plugin routes, or None

        Example:
            router = APIRouter(prefix="/api/v1/slack")

            @router.post("/webhook")
            async def handle_webhook(request: Request):
                return {"status": "received"}

            return router
        """
        pass

    @abstractmethod
    def is_configured(self, user_id: Optional[str] = None) -> bool:
        """
        Check if plugin is properly configured for a user.

        Validates that all required configuration (environment variables,
        credentials, etc.) is present for the plugin to operate.

        Args:
            user_id: User identifier for user-scoped configuration.
                     If None, returns False (can't check user config without user).
                     Issue #759: Added for multi-tenancy support.

        Returns:
            bool: True if configured for the given user, False otherwise

        Example:
            def is_configured(self, user_id: Optional[str] = None) -> bool:
                if user_id is None:
                    return False
                return self.config_service.is_configured(user_id)
        """
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize plugin resources.

        Called during application startup after all plugins are registered.
        Use this to:
        - Initialize connections
        - Allocate resources
        - Start background tasks
        - Validate configuration

        Raises:
            Exception: If initialization fails

        Example:
            async def initialize(self) -> None:
                self.logger.info(f"Initializing {self.get_metadata().name}")
                # Initialize connections
                await self.adapter.authenticate()
                self.logger.info("Plugin initialized successfully")
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """
        Cleanup plugin resources.

        Called during application shutdown. Use this to:
        - Close connections
        - Release resources
        - Stop background tasks
        - Save state

        Should not raise exceptions.

        Example:
            async def shutdown(self) -> None:
                self.logger.info(f"Shutting down {self.get_metadata().name}")
                # Cleanup resources
                await self.adapter.disconnect()
                self.logger.info("Plugin shutdown complete")
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Return plugin health and status information.

        Provides runtime status information for monitoring and debugging.
        Should include:
        - Configuration status
        - Connection status
        - Resource usage
        - Error counts
        - Any plugin-specific metrics

        Returns:
            Dict[str, Any]: Status information

        Example:
            def get_status(self) -> Dict[str, Any]:
                return {
                    "name": self.get_metadata().name,
                    "configured": self.is_configured(),
                    "active": True,
                    "connections": {
                        "api": "connected",
                        "webhooks": "active"
                    },
                    "metrics": {
                        "requests_today": 42,
                        "errors": 0
                    }
                }
        """
        pass

"""
Plugin Registry for Piper Integration Plugins

Manages plugin registration, lifecycle, and discovery.
Singleton pattern ensures global registry instance.
"""

import logging
from typing import Dict, List, Optional

from fastapi import APIRouter

from .plugin_interface import PiperPlugin, PluginMetadata


class PluginRegistry:
    """
    Manages plugin registration, lifecycle, and discovery.

    Singleton registry that all plugins register with at startup.
    Provides plugin lookup, health checks, and lifecycle management.

    Usage:
        registry = get_plugin_registry()
        registry.register(my_plugin)
        await registry.initialize_all()
        routers = registry.get_routers()
    """

    def __init__(self):
        """Initialize empty registry"""
        self._plugins: Dict[str, PiperPlugin] = {}
        self._initialized: bool = False
        self.logger = logging.getLogger(__name__)

    def register(self, plugin: PiperPlugin) -> None:
        """
        Register a plugin with the registry.

        Args:
            plugin: Plugin instance to register

        Raises:
            ValueError: If plugin name already registered
            TypeError: If plugin doesn't implement PiperPlugin
        """
        if not isinstance(plugin, PiperPlugin):
            raise TypeError(f"Plugin must implement PiperPlugin interface")

        metadata = plugin.get_metadata()

        if metadata.name in self._plugins:
            raise ValueError(f"Plugin '{metadata.name}' already registered")

        self._plugins[metadata.name] = plugin
        self.logger.info(
            f"Registered plugin: {metadata.name} v{metadata.version}",
            extra={
                "plugin_name": metadata.name,
                "plugin_version": metadata.version,
                "capabilities": metadata.capabilities,
            },
        )

    def unregister(self, plugin_name: str) -> bool:
        """
        Unregister a plugin by name.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            bool: True if unregistered, False if not found
        """
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
            self.logger.info(f"Unregistered plugin: {plugin_name}")
            return True
        return False

    def get_plugin(self, name: str) -> Optional[PiperPlugin]:
        """
        Get plugin by name.

        Args:
            name: Plugin name

        Returns:
            Optional[PiperPlugin]: Plugin instance or None if not found
        """
        return self._plugins.get(name)

    def list_plugins(self) -> List[str]:
        """
        List all registered plugin names.

        Returns:
            List[str]: List of plugin names
        """
        return list(self._plugins.keys())

    def get_all_plugins(self) -> Dict[str, PiperPlugin]:
        """
        Get all registered plugins.

        Returns:
            Dict[str, PiperPlugin]: Copy of plugins dictionary
        """
        return self._plugins.copy()

    def get_plugin_count(self) -> int:
        """
        Get count of registered plugins.

        Returns:
            int: Number of registered plugins
        """
        return len(self._plugins)

    async def initialize_all(self) -> Dict[str, bool]:
        """
        Initialize all registered plugins.

        Calls initialize() on each plugin. Continues even if some fail.

        Returns:
            Dict[str, bool]: Map of plugin name to success status
        """
        results = {}

        for name, plugin in self._plugins.items():
            try:
                await plugin.initialize()
                self.logger.info(f"Initialized plugin: {name}")
                results[name] = True
            except Exception as e:
                self.logger.error(
                    f"Failed to initialize plugin: {name}",
                    extra={"error": str(e), "plugin_name": name},
                )
                results[name] = False

        self._initialized = True
        return results

    async def shutdown_all(self) -> Dict[str, bool]:
        """
        Shutdown all registered plugins.

        Calls shutdown() on each plugin. Continues even if some fail.

        Returns:
            Dict[str, bool]: Map of plugin name to success status
        """
        results = {}

        for name, plugin in self._plugins.items():
            try:
                await plugin.shutdown()
                self.logger.info(f"Shutdown plugin: {name}")
                results[name] = True
            except Exception as e:
                self.logger.error(
                    f"Failed to shutdown plugin: {name}",
                    extra={"error": str(e), "plugin_name": name},
                )
                results[name] = False

        self._initialized = False
        return results

    def get_routers(self) -> List[APIRouter]:
        """
        Get all plugin routers for mounting.

        Returns:
            List[APIRouter]: List of routers from plugins that provide them
        """
        routers = []

        for name, plugin in self._plugins.items():
            try:
                router = plugin.get_router()
                if router is not None:
                    routers.append(router)
                    self.logger.debug(f"Added router from plugin: {name}")
            except Exception as e:
                self.logger.error(
                    f"Failed to get router from plugin: {name}",
                    extra={"error": str(e), "plugin_name": name},
                )

        return routers

    def get_status_all(self) -> Dict[str, Dict]:
        """
        Get status of all plugins.

        Returns:
            Dict[str, Dict]: Map of plugin name to status dict
        """
        status = {}

        for name, plugin in self._plugins.items():
            try:
                plugin_status = plugin.get_status()
                status[name] = plugin_status
            except Exception as e:
                status[name] = {"error": str(e), "status": "error"}

        return status

    def get_plugins_with_capability(self, capability: str) -> List[PiperPlugin]:
        """
        Get all plugins with a specific capability.

        Args:
            capability: Capability to filter by (e.g., "routes", "webhooks")

        Returns:
            List[PiperPlugin]: Plugins with the specified capability
        """
        plugins = []

        for plugin in self._plugins.values():
            metadata = plugin.get_metadata()
            if capability in metadata.capabilities:
                plugins.append(plugin)

        return plugins

    def is_initialized(self) -> bool:
        """
        Check if registry has been initialized.

        Returns:
            bool: True if initialize_all() has been called
        """
        return self._initialized


# Global registry instance (singleton)
_registry: Optional[PluginRegistry] = None


def get_plugin_registry() -> PluginRegistry:
    """
    Get the global plugin registry (singleton).

    Returns:
        PluginRegistry: Global registry instance
    """
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry


def reset_plugin_registry() -> None:
    """
    Reset the global plugin registry.

    Used primarily for testing. Creates a fresh registry instance.
    """
    global _registry
    _registry = PluginRegistry()

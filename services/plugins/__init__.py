"""
Plugin System for Piper Integration Plugins

Provides the plugin interface and registry for managing
integration plugins (Slack, Notion, GitHub, Calendar, etc.)
"""

from .plugin_interface import PiperPlugin, PluginMetadata
from .plugin_registry import PluginRegistry, get_plugin_registry, reset_plugin_registry

__all__ = [
    "PiperPlugin",
    "PluginMetadata",
    "PluginRegistry",
    "get_plugin_registry",
    "reset_plugin_registry",
]

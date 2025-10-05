"""Contract tests for plugin isolation

Verifies that plugins maintain proper isolation from core system
and don't create unwanted dependencies.
"""

import importlib
import sys

import pytest


@pytest.mark.contract
class TestIsolationContract:
    """Verify plugins maintain proper isolation"""

    def test_plugin_module_structure(self, plugin_instance):
        """Plugin should be in services/integrations/[name]/ structure"""
        metadata = plugin_instance.get_metadata()
        plugin_name = metadata.name

        # Plugin module should exist
        module_name = f"services.integrations.{plugin_name}"
        assert module_name in sys.modules, f"Plugin module {module_name} should be loaded"

    def test_plugin_has_no_circular_imports(self, plugin_instance):
        """Plugin should not create circular import issues"""
        metadata = plugin_instance.get_metadata()
        plugin_name = metadata.name

        # Try to reload plugin module (would fail with circular imports)
        # Note: Re-registration error is expected and acceptable
        try:
            module_name = f"services.integrations.{plugin_name}.{plugin_name}_plugin"
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
        except ImportError as e:
            pytest.fail(f"Plugin has import issues: {e}")
        except ValueError as e:
            # Re-registration error is expected during reload
            if "already registered" not in str(e):
                pytest.fail(f"Unexpected plugin registration error: {e}")

    def test_plugin_auto_registration(self, plugin_instance):
        """Plugin should auto-register via registry pattern"""
        from services.plugins import get_plugin_registry

        metadata = plugin_instance.get_metadata()
        plugin_name = metadata.name

        # Plugin should be in registry
        registry = get_plugin_registry()
        assert (
            plugin_name in registry.list_plugins()
        ), f"Plugin {plugin_name} should be auto-registered"

    def test_plugin_independence(self, plugin_instance):
        """Each plugin should be independently accessible"""
        metadata = plugin_instance.get_metadata()
        plugin_name = metadata.name

        # Should be able to get plugin without loading others
        from services.plugins import get_plugin_registry

        registry = get_plugin_registry()

        plugin = registry.get_plugin(plugin_name)
        assert plugin is not None, f"Plugin {plugin_name} should be independently accessible"

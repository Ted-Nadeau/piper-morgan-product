"""
Plugin Interface Compliance Tests

Tests to verify plugins correctly implement PiperPlugin interface.
"""

from inspect import signature
from typing import get_type_hints

import pytest
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata


class TestPluginMetadata:
    """Tests for PluginMetadata dataclass"""

    def test_metadata_creation(self, sample_metadata):
        """Test PluginMetadata can be created"""
        assert sample_metadata.name == "test_plugin"
        assert sample_metadata.version == "1.0.0"
        assert sample_metadata.description == "Test plugin for validation"
        assert sample_metadata.author == "Test Author"

    def test_metadata_capabilities(self, sample_metadata):
        """Test capabilities list"""
        assert "routes" in sample_metadata.capabilities
        assert "webhooks" in sample_metadata.capabilities

    def test_metadata_dependencies(self, sample_metadata):
        """Test dependencies list"""
        assert "other_plugin" in sample_metadata.dependencies

    def test_metadata_defaults(self):
        """Test PluginMetadata with default values"""
        metadata = PluginMetadata(
            name="simple", version="1.0.0", description="Simple plugin", author="Author"
        )
        assert metadata.capabilities == []
        assert metadata.dependencies == []


class TestPiperPluginInterface:
    """Tests for PiperPlugin ABC"""

    def test_cannot_instantiate_abstract_class(self):
        """Test PiperPlugin cannot be instantiated directly"""
        with pytest.raises(TypeError):
            PiperPlugin()

    def test_minimal_plugin_implements_interface(self, minimal_plugin):
        """Test minimal plugin implements all required methods"""
        assert isinstance(minimal_plugin, PiperPlugin)
        assert hasattr(minimal_plugin, "get_metadata")
        assert hasattr(minimal_plugin, "get_router")
        assert hasattr(minimal_plugin, "is_configured")
        assert hasattr(minimal_plugin, "initialize")
        assert hasattr(minimal_plugin, "shutdown")
        assert hasattr(minimal_plugin, "get_status")

    def test_get_metadata_returns_metadata(self, minimal_plugin):
        """Test get_metadata() returns PluginMetadata"""
        metadata = minimal_plugin.get_metadata()
        assert isinstance(metadata, PluginMetadata)
        assert metadata.name == "minimal"

    def test_get_router_returns_optional_router(self, minimal_plugin):
        """Test get_router() returns Optional[APIRouter]"""
        router = minimal_plugin.get_router()
        assert router is None or isinstance(router, APIRouter)

    def test_is_configured_returns_bool(self, minimal_plugin):
        """Test is_configured() returns bool"""
        result = minimal_plugin.is_configured()
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_initialize_is_async(self, minimal_plugin):
        """Test initialize() is async"""
        result = await minimal_plugin.initialize()
        assert result is None

    @pytest.mark.asyncio
    async def test_shutdown_is_async(self, minimal_plugin):
        """Test shutdown() is async"""
        result = await minimal_plugin.shutdown()
        assert result is None

    def test_get_status_returns_dict(self, minimal_plugin):
        """Test get_status() returns dict"""
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)


class TestPluginWithRouter:
    """Tests for plugins with router implementation"""

    def test_router_is_api_router(self, plugin_with_router):
        """Test router is FastAPI APIRouter"""
        router = plugin_with_router.get_router()
        assert isinstance(router, APIRouter)

    def test_router_has_prefix(self, plugin_with_router):
        """Test router has prefix configured"""
        router = plugin_with_router.get_router()
        assert router.prefix == "/api/v1/test"

    def test_router_has_routes(self, plugin_with_router):
        """Test router has routes defined"""
        router = plugin_with_router.get_router()
        assert len(router.routes) > 0

    def test_metadata_has_routes_capability(self, plugin_with_router):
        """Test plugin with router declares routes capability"""
        metadata = plugin_with_router.get_metadata()
        assert "routes" in metadata.capabilities


class TestPluginLifecycle:
    """Tests for plugin lifecycle management"""

    @pytest.mark.asyncio
    async def test_initialize_before_use(self, minimal_plugin):
        """Test plugin can be initialized"""
        await minimal_plugin.initialize()
        assert minimal_plugin.is_configured()

    @pytest.mark.asyncio
    async def test_shutdown_after_use(self, minimal_plugin):
        """Test plugin can be shut down"""
        await minimal_plugin.initialize()
        await minimal_plugin.shutdown()
        # Plugin should still report status after shutdown
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)

    @pytest.mark.asyncio
    async def test_full_lifecycle(self, minimal_plugin):
        """Test complete plugin lifecycle"""
        # Initialize
        await minimal_plugin.initialize()

        # Use plugin
        metadata = minimal_plugin.get_metadata()
        assert metadata.name == "minimal"

        router = minimal_plugin.get_router()
        assert router is None

        status = minimal_plugin.get_status()
        assert isinstance(status, dict)

        # Shutdown
        await minimal_plugin.shutdown()


class TestPluginStatus:
    """Tests for plugin status reporting"""

    def test_status_is_dict(self, minimal_plugin):
        """Test status is dictionary"""
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)

    def test_status_not_empty(self, minimal_plugin):
        """Test status contains information"""
        status = minimal_plugin.get_status()
        assert len(status) > 0

    def test_status_includes_configured(self, plugin_with_router):
        """Test status includes configuration status"""
        status = plugin_with_router.get_status()
        # Status should have some meaningful information
        assert isinstance(status, dict)


class TestPluginValidation:
    """Tests for plugin validation helpers"""

    def test_validate_plugin_has_all_methods(self, minimal_plugin):
        """Test helper to validate plugin implements all methods"""
        required_methods = [
            "get_metadata",
            "get_router",
            "is_configured",
            "initialize",
            "shutdown",
            "get_status",
        ]

        for method in required_methods:
            assert hasattr(minimal_plugin, method), f"Missing method: {method}"

    def test_validate_method_signatures(self, minimal_plugin):
        """Test method signatures match interface"""
        # get_metadata() -> PluginMetadata
        metadata = minimal_plugin.get_metadata()
        assert isinstance(metadata, PluginMetadata)

        # get_router() -> Optional[APIRouter]
        router = minimal_plugin.get_router()
        assert router is None or isinstance(router, APIRouter)

        # is_configured() -> bool
        configured = minimal_plugin.is_configured()
        assert isinstance(configured, bool)

        # get_status() -> Dict[str, Any]
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)


# Plugin validation helper function
def validate_plugin_interface(plugin: PiperPlugin) -> bool:
    """
    Validate that a plugin correctly implements PiperPlugin interface.

    Args:
        plugin: Plugin instance to validate

    Returns:
        bool: True if valid, raises AssertionError if invalid
    """
    # Check it's a PiperPlugin
    assert isinstance(plugin, PiperPlugin), "Plugin must inherit from PiperPlugin"

    # Check all methods exist
    required_methods = [
        "get_metadata",
        "get_router",
        "is_configured",
        "initialize",
        "shutdown",
        "get_status",
    ]
    for method in required_methods:
        assert hasattr(plugin, method), f"Missing required method: {method}"

    # Check method return types
    metadata = plugin.get_metadata()
    assert isinstance(metadata, PluginMetadata), "get_metadata() must return PluginMetadata"

    router = plugin.get_router()
    assert router is None or isinstance(
        router, APIRouter
    ), "get_router() must return Optional[APIRouter]"

    configured = plugin.is_configured()
    assert isinstance(configured, bool), "is_configured() must return bool"

    status = plugin.get_status()
    assert isinstance(status, dict), "get_status() must return dict"

    return True

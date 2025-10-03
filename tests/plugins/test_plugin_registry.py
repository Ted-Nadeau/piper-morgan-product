"""
Plugin Registry Tests

Tests for PluginRegistry lifecycle and operations.
"""

from typing import Any, Dict, Optional

import pytest
from fastapi import APIRouter

from services.plugins import (
    PiperPlugin,
    PluginMetadata,
    PluginRegistry,
    get_plugin_registry,
    reset_plugin_registry,
)


@pytest.fixture
def fresh_registry():
    """Create fresh registry for each test"""
    reset_plugin_registry()
    return get_plugin_registry()


@pytest.fixture
def sample_plugin():
    """Sample plugin for testing"""

    class SamplePlugin(PiperPlugin):
        def get_metadata(self):
            return PluginMetadata(
                name="sample",
                version="1.0.0",
                description="Sample plugin",
                author="Test",
                capabilities=["routes"],
                dependencies=[],
            )

        def get_router(self):
            return None

        def is_configured(self):
            return True

        async def initialize(self):
            pass

        async def shutdown(self):
            pass

        def get_status(self):
            return {"status": "ok"}

    return SamplePlugin()


class TestPluginRegistry:
    """Tests for PluginRegistry class"""

    def test_registry_creation(self, fresh_registry):
        """Test registry can be created"""
        assert fresh_registry is not None
        assert fresh_registry.get_plugin_count() == 0

    def test_singleton_pattern(self):
        """Test registry is singleton"""
        r1 = get_plugin_registry()
        r2 = get_plugin_registry()
        assert r1 is r2

    def test_register_plugin(self, fresh_registry, sample_plugin):
        """Test plugin registration"""
        fresh_registry.register(sample_plugin)
        assert fresh_registry.get_plugin_count() == 1
        assert "sample" in fresh_registry.list_plugins()

    def test_register_duplicate_fails(self, fresh_registry, sample_plugin):
        """Test duplicate registration fails"""
        fresh_registry.register(sample_plugin)
        with pytest.raises(ValueError, match="already registered"):
            fresh_registry.register(sample_plugin)

    def test_get_plugin(self, fresh_registry, sample_plugin):
        """Test getting plugin by name"""
        fresh_registry.register(sample_plugin)
        plugin = fresh_registry.get_plugin("sample")
        assert plugin is sample_plugin

    def test_get_nonexistent_plugin(self, fresh_registry):
        """Test getting nonexistent plugin returns None"""
        plugin = fresh_registry.get_plugin("nonexistent")
        assert plugin is None

    def test_unregister_plugin(self, fresh_registry, sample_plugin):
        """Test plugin unregistration"""
        fresh_registry.register(sample_plugin)
        result = fresh_registry.unregister("sample")
        assert result is True
        assert fresh_registry.get_plugin_count() == 0

    @pytest.mark.asyncio
    async def test_initialize_all(self, fresh_registry, sample_plugin):
        """Test initializing all plugins"""
        fresh_registry.register(sample_plugin)
        results = await fresh_registry.initialize_all()
        assert results["sample"] is True
        assert fresh_registry.is_initialized()

    @pytest.mark.asyncio
    async def test_shutdown_all(self, fresh_registry, sample_plugin):
        """Test shutting down all plugins"""
        fresh_registry.register(sample_plugin)
        await fresh_registry.initialize_all()
        results = await fresh_registry.shutdown_all()
        assert results["sample"] is True
        assert not fresh_registry.is_initialized()

    def test_get_status_all(self, fresh_registry, sample_plugin):
        """Test getting status of all plugins"""
        fresh_registry.register(sample_plugin)
        status = fresh_registry.get_status_all()
        assert "sample" in status
        assert status["sample"]["status"] == "ok"

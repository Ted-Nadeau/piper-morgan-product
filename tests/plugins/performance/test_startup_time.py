"""Performance tests for plugin system startup

Validates that plugin discovery, loading, and initialization
complete within acceptable time limits.
"""

import time

import pytest

from services.plugins import get_plugin_registry, reset_plugin_registry


@pytest.mark.performance
class TestStartupPerformance:
    """Validate plugin system startup performance"""

    def test_plugin_discovery_time(self, performance_threshold):
        """Plugin discovery should complete quickly"""
        reset_plugin_registry()
        registry = get_plugin_registry()

        start = time.perf_counter()
        available = registry.discover_plugins()
        elapsed = (time.perf_counter() - start) * 1000  # ms

        # Discovery should be < 100ms
        assert elapsed < 100, f"Discovery too slow: {elapsed:.2f}ms (limit: 100ms)"
        assert len(available) >= 4, f"Expected at least 4 plugins, found {len(available)}"

    def test_plugin_loading_time(self, performance_threshold):
        """Plugin loading should complete within limits"""
        reset_plugin_registry()
        registry = get_plugin_registry()
        registry.discover_plugins()

        start = time.perf_counter()
        results = registry.load_enabled_plugins()
        elapsed = (time.perf_counter() - start) * 1000  # ms

        # Loading should be < 500ms
        assert elapsed < 500, f"Loading too slow: {elapsed:.2f}ms (limit: 500ms)"
        assert (
            sum(1 for success in results.values() if success) >= 4
        ), "Expected at least 4 plugins loaded successfully"

    @pytest.mark.asyncio
    async def test_plugin_initialization_time(self, performance_threshold):
        """Plugin initialization should complete within limits"""
        reset_plugin_registry()
        registry = get_plugin_registry()
        registry.discover_plugins()
        registry.load_enabled_plugins()

        start = time.perf_counter()
        await registry.initialize_all()
        elapsed = (time.perf_counter() - start) * 1000  # ms

        # Initialization should be < 1400ms
        assert elapsed < 1400, f"Initialization too slow: {elapsed:.2f}ms (limit: 1400ms)"

    @pytest.mark.asyncio
    async def test_total_startup_time(self, performance_threshold):
        """Total startup time should meet target"""
        reset_plugin_registry()
        registry = get_plugin_registry()

        start = time.perf_counter()

        # Discovery
        registry.discover_plugins()

        # Loading
        registry.load_enabled_plugins()

        # Initialization
        await registry.initialize_all()

        elapsed = (time.perf_counter() - start) * 1000  # ms

        # Total should be < 2000ms
        threshold = performance_threshold["startup_ms"]
        assert (
            elapsed < threshold
        ), f"Total startup too slow: {elapsed:.2f}ms (limit: {threshold}ms)"

"""Performance tests for concurrent plugin operations

Validates that plugins can handle concurrent operations without
performance degradation or conflicts.
"""

import asyncio
import time

import pytest

from services.plugins import get_plugin_registry


@pytest.mark.performance
class TestConcurrency:
    """Validate concurrent plugin operation performance"""

    @pytest.mark.asyncio
    async def test_concurrent_status_checks(self, performance_threshold):
        """All plugins should handle concurrent status checks"""
        registry = get_plugin_registry()
        plugin_names = registry.list_plugins()

        async def check_plugin(name):
            plugin = registry.get_plugin(name)
            return plugin.get_status()

        start = time.perf_counter()
        results = await asyncio.gather(*[check_plugin(name) for name in plugin_names])
        elapsed = (time.perf_counter() - start) * 1000  # ms

        threshold = performance_threshold["concurrency_ms"]
        assert (
            elapsed < threshold
        ), f"Concurrent status checks too slow: {elapsed:.2f}ms (limit: {threshold}ms)"
        assert len(results) == len(plugin_names), "Not all plugins responded"

    @pytest.mark.asyncio
    async def test_concurrent_metadata_retrieval(self, performance_threshold):
        """Concurrent metadata retrieval should be fast"""
        registry = get_plugin_registry()
        plugin_names = registry.list_plugins()

        async def get_metadata(name):
            plugin = registry.get_plugin(name)
            return plugin.get_metadata()

        start = time.perf_counter()
        results = await asyncio.gather(*[get_metadata(name) for name in plugin_names])
        elapsed = (time.perf_counter() - start) * 1000  # ms

        # Should complete very quickly
        assert (
            elapsed < 10
        ), f"Concurrent metadata retrieval too slow: {elapsed:.2f}ms (limit: 10ms)"
        assert len(results) == len(plugin_names), "Not all plugins responded"

    @pytest.mark.asyncio
    async def test_no_resource_conflicts(self, performance_threshold):
        """Plugins should not have resource conflicts under concurrent load"""
        registry = get_plugin_registry()
        plugin_names = registry.list_plugins()

        async def stress_plugin(name, iterations=100):
            plugin = registry.get_plugin(name)
            for _ in range(iterations):
                _ = plugin.get_status()
                _ = plugin.get_metadata()
                _ = plugin.is_configured()

        # Stress all plugins concurrently
        start = time.perf_counter()
        await asyncio.gather(*[stress_plugin(name) for name in plugin_names])
        elapsed = (time.perf_counter() - start) * 1000  # ms

        # Should complete without errors in reasonable time
        # 100 ops × 4 plugins = 400 ops, should be < 1s
        assert elapsed < 1000, f"Concurrent stress test too slow: {elapsed:.2f}ms (limit: 1000ms)"

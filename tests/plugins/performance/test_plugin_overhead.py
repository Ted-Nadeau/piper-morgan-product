"""Performance tests for plugin wrapper overhead

These tests validate that the plugin wrapper pattern does not
introduce significant performance overhead.
"""

import time
from statistics import mean

import pytest

from services.plugins import get_plugin_registry


@pytest.mark.performance
class TestPluginOverhead:
    """Validate plugin wrapper overhead is minimal"""

    def test_get_router_overhead(self, performance_threshold):
        """Getting router through plugin should have minimal overhead"""
        registry = get_plugin_registry()
        # Ensure plugins are loaded
        registry.load_enabled_plugins()
        plugin = registry.get_plugin("github")

        # Measure overhead of get_router() calls
        iterations = 10000
        times = []

        for _ in range(5):  # 5 runs for stability
            start = time.perf_counter()
            for _ in range(iterations):
                _ = plugin.get_router()
            elapsed = time.perf_counter() - start
            times.append(elapsed / iterations * 1000)  # ms per call

        avg_time = mean(times)
        threshold = performance_threshold["overhead_ms"]

        assert (
            avg_time < threshold
        ), f"Router access too slow: {avg_time:.6f}ms (limit: {threshold}ms)"

    def test_get_metadata_overhead(self, performance_threshold):
        """Getting metadata should be fast"""
        registry = get_plugin_registry()
        # Ensure plugins are loaded
        registry.load_enabled_plugins()
        plugin = registry.get_plugin("github")

        # Measure metadata retrieval
        iterations = 10000

        start = time.perf_counter()
        for _ in range(iterations):
            _ = plugin.get_metadata()
        elapsed = time.perf_counter() - start

        avg_time = (elapsed / iterations) * 1000  # ms per call
        threshold = performance_threshold["overhead_ms"]

        assert (
            avg_time < threshold
        ), f"Metadata retrieval too slow: {avg_time:.6f}ms (limit: {threshold}ms)"

    def test_is_configured_overhead(self, performance_threshold):
        """is_configured() should be extremely fast (no I/O)"""
        registry = get_plugin_registry()
        # Ensure plugins are loaded
        registry.load_enabled_plugins()
        plugin = registry.get_plugin("github")

        # Should complete 100,000 calls in < 100ms
        iterations = 100000

        start = time.perf_counter()
        for _ in range(iterations):
            _ = plugin.is_configured()
        elapsed = time.perf_counter() - start

        # Should be < 0.001ms per call
        avg_time = (elapsed / iterations) * 1000

        assert avg_time < 0.001, f"is_configured() too slow: {avg_time:.6f}ms (limit: 0.001ms)"

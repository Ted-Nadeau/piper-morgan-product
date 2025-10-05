"""Performance tests for plugin memory usage

Validates that plugins have reasonable memory footprints.

Note: These tests require psutil. They will be skipped if psutil
is not available.
"""

import os

import pytest

# Check if psutil available
psutil = pytest.importorskip("psutil", reason="psutil required for memory tests")


@pytest.mark.performance
class TestMemoryUsage:
    """Validate plugin memory usage is reasonable"""

    def get_memory_mb(self):
        """Get current process memory in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    def test_plugin_memory_footprint(self, performance_threshold):
        """Each plugin should have reasonable memory footprint"""
        from services.plugins import get_plugin_registry, reset_plugin_registry

        reset_plugin_registry()
        registry = get_plugin_registry()

        # Baseline
        baseline = self.get_memory_mb()

        # Discover
        available = registry.discover_plugins()

        # Load each plugin and measure
        memory_per_plugin = {}

        for plugin_name in sorted(available.keys()):
            before = self.get_memory_mb()
            module_path = available[plugin_name]
            registry.load_plugin(plugin_name, module_path)
            after = self.get_memory_mb()

            delta = after - before
            memory_per_plugin[plugin_name] = delta

        # Check each plugin
        threshold = performance_threshold["memory_mb"]
        failures = []

        for plugin_name, memory_mb in memory_per_plugin.items():
            if memory_mb > threshold:
                failures.append(f"{plugin_name}: {memory_mb:.2f}MB > {threshold}MB")

        assert not failures, f"Plugins exceed memory threshold: {', '.join(failures)}"

    def test_total_memory_footprint(self, performance_threshold):
        """Total plugin memory should be reasonable"""
        from services.plugins import get_plugin_registry, reset_plugin_registry

        reset_plugin_registry()
        registry = get_plugin_registry()

        # Baseline
        baseline = self.get_memory_mb()

        # Load all plugins
        registry.discover_plugins()
        registry.load_enabled_plugins()

        # Measure total
        after_loading = self.get_memory_mb()
        total_overhead = after_loading - baseline

        # Total should be reasonable (< 200MB for all plugins)
        assert (
            total_overhead < 200
        ), f"Total plugin memory too high: {total_overhead:.2f}MB (limit: 200MB)"

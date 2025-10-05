"""Multi-plugin integration tests

Tests that validate multiple plugins working together without conflicts,
proper resource sharing, and graceful degradation when plugins fail.
"""

import asyncio
import time
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from services.plugins import PiperPlugin, get_plugin_registry, reset_plugin_registry


@pytest.mark.integration
class TestMultiPluginOrchestration:
    """Test multiple plugins working together."""

    @pytest.fixture(autouse=True)
    def setup_plugins(self):
        """Ensure all plugins are loaded for each test."""
        reset_plugin_registry()
        registry = get_plugin_registry()
        registry.load_enabled_plugins()
        yield registry
        # Cleanup after each test
        reset_plugin_registry()

    @pytest.mark.asyncio
    async def test_all_plugins_concurrent_status(self, setup_plugins):
        """Test getting status from all plugins concurrently."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        # Ensure we have multiple plugins to test
        assert len(plugin_names) >= 4, f"Expected at least 4 plugins, got {len(plugin_names)}"

        async def get_plugin_status(name: str) -> Dict[str, Any]:
            """Get status from a single plugin."""
            plugin = registry.get_plugin(name)
            return {
                "name": name,
                "status": plugin.get_status(),
                "configured": plugin.is_configured(),
                "metadata": plugin.get_metadata(),
            }

        # Get status from all plugins concurrently
        start_time = time.perf_counter()
        results = await asyncio.gather(*[get_plugin_status(name) for name in plugin_names])
        elapsed_time = time.perf_counter() - start_time

        # Verify all plugins responded
        assert len(results) == len(plugin_names), "Not all plugins responded"

        # Verify no conflicts or race conditions
        plugin_results = {result["name"]: result for result in results}
        for name in plugin_names:
            assert name in plugin_results, f"Plugin {name} missing from results"
            result = plugin_results[name]

            # Verify status structure
            assert isinstance(result["status"], dict), f"Plugin {name} status not dict"
            assert isinstance(result["configured"], bool), f"Plugin {name} configured not bool"
            assert result["metadata"].name == name, f"Plugin {name} metadata mismatch"

        # Performance check - concurrent operations should be fast
        assert elapsed_time < 1.0, f"Concurrent status check too slow: {elapsed_time:.3f}s"

    @pytest.mark.asyncio
    async def test_plugin_isolation(self, setup_plugins):
        """Verify plugins don't interfere with each other."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        # Get baseline status from all plugins
        baseline_status = {}
        for name in plugin_names:
            plugin = registry.get_plugin(name)
            baseline_status[name] = {
                "status": plugin.get_status(),
                "configured": plugin.is_configured(),
                "router": plugin.get_router(),
            }

        # Test that accessing one plugin doesn't affect others
        for target_name in plugin_names:
            target_plugin = registry.get_plugin(target_name)

            # Perform operations on target plugin
            _ = target_plugin.get_metadata()
            _ = target_plugin.get_status()
            _ = target_plugin.get_router()
            _ = target_plugin.is_configured()

            # Verify other plugins unchanged
            for other_name in plugin_names:
                if other_name == target_name:
                    continue

                other_plugin = registry.get_plugin(other_name)
                current_status = other_plugin.get_status()

                # Status should be consistent (allowing for timestamp differences)
                baseline = baseline_status[other_name]["status"]
                assert current_status.get("configured") == baseline.get(
                    "configured"
                ), f"Plugin {other_name} configuration changed after accessing {target_name}"

    @pytest.mark.asyncio
    async def test_concurrent_metadata_retrieval(self, setup_plugins):
        """Test concurrent metadata retrieval from all plugins."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        async def get_metadata_multiple_times(name: str, iterations: int = 10):
            """Get metadata from plugin multiple times."""
            plugin = registry.get_plugin(name)
            results = []
            for _ in range(iterations):
                metadata = plugin.get_metadata()
                results.append(
                    {
                        "name": metadata.name,
                        "version": metadata.version,
                        "capabilities": metadata.capabilities,
                    }
                )
            return results

        # Run concurrent metadata retrieval
        start_time = time.perf_counter()
        all_results = await asyncio.gather(
            *[get_metadata_multiple_times(name) for name in plugin_names]
        )
        elapsed_time = time.perf_counter() - start_time

        # Verify consistency across all calls
        for i, name in enumerate(plugin_names):
            results = all_results[i]
            assert len(results) == 10, f"Plugin {name} didn't return all results"

            # All metadata calls should return identical results
            first_result = results[0]
            for result in results[1:]:
                assert result == first_result, f"Plugin {name} metadata inconsistent"

        # Performance check
        total_calls = len(plugin_names) * 10
        avg_time_per_call = elapsed_time / total_calls
        assert (
            avg_time_per_call < 0.01
        ), f"Metadata retrieval too slow: {avg_time_per_call*1000:.2f}ms per call"

    @pytest.mark.asyncio
    async def test_resource_sharing(self, setup_plugins):
        """Test plugins can share resources appropriately."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        # Test that plugins can be accessed simultaneously without conflicts
        plugins = [registry.get_plugin(name) for name in plugin_names]

        # Simulate concurrent resource access
        async def access_plugin_resources(plugin: PiperPlugin):
            """Access various plugin resources."""
            tasks = []

            # Metadata access
            tasks.append(asyncio.create_task(asyncio.to_thread(plugin.get_metadata)))

            # Status access
            tasks.append(asyncio.create_task(asyncio.to_thread(plugin.get_status)))

            # Router access
            tasks.append(asyncio.create_task(asyncio.to_thread(plugin.get_router)))

            # Configuration check
            tasks.append(asyncio.create_task(asyncio.to_thread(plugin.is_configured)))

            # Wait for all tasks
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Check for exceptions
            exceptions = [r for r in results if isinstance(r, Exception)]
            return len(exceptions) == 0, exceptions

        # Access all plugins concurrently
        access_results = await asyncio.gather(
            *[access_plugin_resources(plugin) for plugin in plugins]
        )

        # Verify no resource conflicts
        for i, (success, exceptions) in enumerate(access_results):
            plugin_name = plugin_names[i]
            assert success, f"Plugin {plugin_name} had resource conflicts: {exceptions}"

    @pytest.mark.asyncio
    async def test_graceful_degradation(self, setup_plugins):
        """Test system continues when plugins fail."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        # Test that registry continues to work when individual plugins have issues
        working_plugins = []

        for name in plugin_names:
            try:
                plugin = registry.get_plugin(name)

                # Test basic operations
                metadata = plugin.get_metadata()
                status = plugin.get_status()
                router = plugin.get_router()
                configured = plugin.is_configured()

                # If all operations succeed, plugin is working
                if (
                    metadata
                    and isinstance(status, dict)
                    and router
                    and isinstance(configured, bool)
                ):
                    working_plugins.append(name)

            except Exception as e:
                # Plugin failure should not crash the test
                print(f"Plugin {name} failed gracefully: {e}")
                continue

        # Verify at least some plugins are working
        assert (
            len(working_plugins) >= 2
        ), f"Too few working plugins: {working_plugins}. Expected at least 2."

        # Verify registry still functions with working plugins
        assert (
            registry.list_plugins() == plugin_names
        ), "Registry plugin list should remain consistent"

        # Verify we can still get working plugins
        for name in working_plugins:
            plugin = registry.get_plugin(name)
            assert plugin is not None, f"Working plugin {name} should be accessible"

    @pytest.mark.asyncio
    async def test_plugin_lifecycle_coordination(self, setup_plugins):
        """Test plugin initialization and shutdown coordination."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        # Test that all plugins can be initialized concurrently
        plugins = [registry.get_plugin(name) for name in plugin_names]

        # Initialize all plugins concurrently
        start_time = time.perf_counter()
        init_results = await asyncio.gather(
            *[plugin.initialize() for plugin in plugins], return_exceptions=True
        )
        init_time = time.perf_counter() - start_time

        # Check for initialization failures
        init_failures = [
            (i, result) for i, result in enumerate(init_results) if isinstance(result, Exception)
        ]

        # Allow some initialization failures (e.g., missing API keys)
        success_rate = (len(plugins) - len(init_failures)) / len(plugins)
        assert (
            success_rate >= 0.5
        ), f"Too many initialization failures: {len(init_failures)}/{len(plugins)}"

        # Test concurrent shutdown
        start_time = time.perf_counter()
        shutdown_results = await asyncio.gather(
            *[plugin.shutdown() for plugin in plugins], return_exceptions=True
        )
        shutdown_time = time.perf_counter() - start_time

        # Shutdown should generally succeed
        shutdown_failures = [
            (i, result)
            for i, result in enumerate(shutdown_results)
            if isinstance(result, Exception)
        ]

        # Shutdown should be more reliable than initialization
        shutdown_success_rate = (len(plugins) - len(shutdown_failures)) / len(plugins)
        assert (
            shutdown_success_rate >= 0.8
        ), f"Too many shutdown failures: {len(shutdown_failures)}/{len(plugins)}"

        # Performance checks
        assert init_time < 5.0, f"Concurrent initialization too slow: {init_time:.2f}s"
        assert shutdown_time < 2.0, f"Concurrent shutdown too slow: {shutdown_time:.2f}s"

    @pytest.mark.asyncio
    async def test_configuration_isolation(self, setup_plugins):
        """Test that plugin configurations don't interfere with each other."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        # Get configuration status for all plugins
        config_states = {}
        for name in plugin_names:
            plugin = registry.get_plugin(name)
            config_states[name] = {
                "is_configured": plugin.is_configured(),
                "status": plugin.get_status(),
                "metadata": plugin.get_metadata(),
            }

        # Verify each plugin has independent configuration
        for name in plugin_names:
            state = config_states[name]

            # Configuration state should be deterministic
            plugin = registry.get_plugin(name)
            current_configured = plugin.is_configured()
            assert (
                current_configured == state["is_configured"]
            ), f"Plugin {name} configuration state changed unexpectedly"

            # Metadata should be consistent
            current_metadata = plugin.get_metadata()
            assert (
                current_metadata.name == state["metadata"].name
            ), f"Plugin {name} metadata name changed"
            assert (
                current_metadata.version == state["metadata"].version
            ), f"Plugin {name} metadata version changed"

    def test_plugin_registry_thread_safety(self, setup_plugins):
        """Test that plugin registry operations are thread-safe."""
        registry = setup_plugins
        plugin_names = registry.list_plugins()

        import queue
        import threading

        results_queue = queue.Queue()
        errors_queue = queue.Queue()

        def worker_thread(thread_id: int, iterations: int = 50):
            """Worker thread that performs plugin operations."""
            try:
                for i in range(iterations):
                    # Perform various registry operations
                    plugins = registry.list_plugins()

                    for name in plugins:
                        plugin = registry.get_plugin(name)
                        if plugin:
                            _ = plugin.get_metadata()
                            _ = plugin.is_configured()

                results_queue.put(f"Thread {thread_id} completed {iterations} iterations")

            except Exception as e:
                errors_queue.put(f"Thread {thread_id} error: {e}")

        # Start multiple worker threads
        threads = []
        num_threads = 4

        for thread_id in range(num_threads):
            thread = threading.Thread(target=worker_thread, args=(thread_id,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=10.0)  # 10 second timeout

        # Check results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        errors = []
        while not errors_queue.empty():
            errors.append(errors_queue.get())

        # Verify thread safety
        assert len(errors) == 0, f"Thread safety errors: {errors}"
        assert (
            len(results) == num_threads
        ), f"Not all threads completed: {len(results)}/{num_threads}"

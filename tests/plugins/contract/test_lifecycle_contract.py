"""Contract tests for plugin lifecycle methods

Verifies that initialize() and shutdown() work correctly and can be
called multiple times safely (idempotency).
"""

import pytest


@pytest.mark.contract
class TestLifecycleContract:
    """Verify plugin lifecycle methods work correctly"""

    @pytest.mark.asyncio
    async def test_initialize_is_async(self, plugin_instance):
        """initialize() must be async method"""
        import inspect

        assert inspect.iscoroutinefunction(
            plugin_instance.initialize
        ), "initialize() must be async method"

    @pytest.mark.asyncio
    async def test_initialize_is_idempotent(self, plugin_instance):
        """initialize() can be called multiple times safely"""
        # First call
        await plugin_instance.initialize()

        # Second call should not raise error
        try:
            await plugin_instance.initialize()
        except Exception as e:
            pytest.fail(f"initialize() should be idempotent, raised: {e}")

    @pytest.mark.asyncio
    async def test_shutdown_is_async(self, plugin_instance):
        """shutdown() must be async method"""
        import inspect

        assert inspect.iscoroutinefunction(
            plugin_instance.shutdown
        ), "shutdown() must be async method"

    @pytest.mark.asyncio
    async def test_shutdown_is_idempotent(self, plugin_instance):
        """shutdown() can be called multiple times safely"""
        # Initialize first
        await plugin_instance.initialize()

        # First shutdown
        await plugin_instance.shutdown()

        # Second shutdown should not raise error
        try:
            await plugin_instance.shutdown()
        except Exception as e:
            pytest.fail(f"shutdown() should be idempotent, raised: {e}")

    @pytest.mark.asyncio
    async def test_lifecycle_order(self, plugin_instance):
        """Plugins must support initialize -> use -> shutdown lifecycle"""
        # Initialize
        await plugin_instance.initialize()

        # Use plugin (get status)
        status = plugin_instance.get_status()
        assert status is not None

        # Shutdown
        await plugin_instance.shutdown()

        # Should still be able to get status after shutdown
        # (plugin object still valid, just resources cleaned up)
        status_after = plugin_instance.get_status()
        assert status_after is not None

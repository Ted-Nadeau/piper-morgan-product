"""Benchmark concurrent plugin operations

Tests that all plugins can handle concurrent requests without conflicts.

Target: All 5 plugins respond < 100ms total
"""

import asyncio
import time

from services.plugins import get_plugin_registry


async def test_concurrent_health_checks():
    """Test concurrent health checks to all plugins"""
    registry = get_plugin_registry()

    # Load plugins if not already loaded
    if not registry.list_plugins():
        registry.discover_plugins()
        registry.load_enabled_plugins()
        await registry.initialize_all()

    # Get all plugins
    plugin_names = registry.list_plugins()

    async def check_plugin(name):
        """Check a single plugin"""
        plugin = registry.get_plugin(name)
        status = plugin.get_status()
        return name, status

    # Run concurrently
    start = time.perf_counter()
    results = await asyncio.gather(*[check_plugin(name) for name in plugin_names])
    elapsed = (time.perf_counter() - start) * 1000  # ms

    return {"time_ms": elapsed, "count": len(results), "results": dict(results)}


async def main():
    """Run concurrency benchmark"""
    print("=" * 60)
    print("Plugin Concurrency Benchmark")
    print("=" * 60)
    print()

    print("Testing concurrent health checks...")
    result = await test_concurrent_health_checks()

    print(f"Plugins tested: {result['count']}")
    print(f"Total time: {result['time_ms']:.2f} ms")
    if result["count"] > 0:
        print(f"Average per plugin: {result['time_ms'] / result['count']:.2f} ms")
    print()

    print("Individual results:")
    for name, status in result["results"].items():
        print(f"  {name:12s}: {status.get('configured', False)}")

    print()

    # Check target
    target = 100  # ms
    passed = result["time_ms"] < target
    print(f"Target: < {target} ms total")
    print(f"{'✅ PASS' if passed else '❌ FAIL'}: {result['time_ms']:.2f} ms")
    print()

    return 0 if passed else 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))

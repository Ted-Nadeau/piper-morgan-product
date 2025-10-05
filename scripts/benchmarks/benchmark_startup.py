"""Benchmark plugin system startup time

Measures time for plugin discovery, loading, and initialization.

Target: < 2s total for all 5 plugins
Breakdown: Discovery <100ms, Loading <500ms, Init <1400ms
"""

import asyncio
import time

from services.plugins import get_plugin_registry, reset_plugin_registry


def benchmark_discovery():
    """Measure plugin discovery time"""
    reset_plugin_registry()
    registry = get_plugin_registry()

    start = time.perf_counter()
    available = registry.discover_plugins()
    elapsed = (time.perf_counter() - start) * 1000  # ms

    return {"time_ms": elapsed, "count": len(available), "plugins": list(available.keys())}


def benchmark_loading():
    """Measure plugin loading time"""
    reset_plugin_registry()
    registry = get_plugin_registry()
    registry.discover_plugins()

    start = time.perf_counter()
    results = registry.load_enabled_plugins()
    elapsed = (time.perf_counter() - start) * 1000  # ms

    return {
        "time_ms": elapsed,
        "count": len(results),
        "success": sum(1 for success in results.values() if success),
    }


async def benchmark_initialization():
    """Measure plugin initialization time"""
    reset_plugin_registry()
    registry = get_plugin_registry()
    registry.discover_plugins()
    registry.load_enabled_plugins()

    start = time.perf_counter()
    await registry.initialize_all()
    elapsed = (time.perf_counter() - start) * 1000  # ms

    return {"time_ms": elapsed, "count": len(registry.list_plugins())}


async def main():
    """Run startup benchmark"""
    print("=" * 60)
    print("Plugin System Startup Benchmark")
    print("=" * 60)
    print()

    # Discovery
    print("Phase 1: Discovery")
    discovery = benchmark_discovery()
    print(f"  Time: {discovery['time_ms']:.2f} ms")
    print(f"  Found: {discovery['count']} plugins")
    print(f"  Target: < 100 ms")
    discovery_pass = discovery["time_ms"] < 100
    print(f"  {'✅ PASS' if discovery_pass else '❌ FAIL'}")
    print()

    # Loading
    print("Phase 2: Loading")
    loading = benchmark_loading()
    print(f"  Time: {loading['time_ms']:.2f} ms")
    print(f"  Loaded: {loading['success']}/{loading['count']} plugins")
    print(f"  Target: < 500 ms")
    loading_pass = loading["time_ms"] < 500
    print(f"  {'✅ PASS' if loading_pass else '❌ FAIL'}")
    print()

    # Initialization
    print("Phase 3: Initialization")
    init = await benchmark_initialization()
    print(f"  Time: {init['time_ms']:.2f} ms")
    print(f"  Initialized: {init['count']} plugins")
    print(f"  Target: < 1400 ms")
    init_pass = init["time_ms"] < 1400
    print(f"  {'✅ PASS' if init_pass else '❌ FAIL'}")
    print()

    # Total
    total = discovery["time_ms"] + loading["time_ms"] + init["time_ms"]
    print("=" * 60)
    print(f"Total Startup Time: {total:.2f} ms")
    print(f"Target: < 2000 ms")
    total_pass = total < 2000
    print(f"{'✅ PASS' if total_pass else '❌ FAIL'}")
    print()

    return 0 if all([discovery_pass, loading_pass, init_pass, total_pass]) else 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))

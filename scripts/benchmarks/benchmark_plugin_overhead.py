"""Benchmark plugin wrapper overhead

Measures the performance overhead of the plugin wrapper pattern
by comparing direct router calls vs plugin-wrapped calls.

Target: < 0.05ms overhead per call
"""

import asyncio
import time
from statistics import mean, stdev

from services.plugins import get_plugin_registry


async def benchmark_direct_router():
    """Benchmark direct router calls (baseline)"""
    from services.integrations.demo.config_service import DemoConfigService
    from services.integrations.demo.demo_integration_router import DemoIntegrationRouter

    config = DemoConfigService()
    router_instance = DemoIntegrationRouter(config)

    # Warm up
    for _ in range(100):
        router_instance.router.routes

    # Benchmark
    iterations = 10000
    times = []

    for _ in range(10):  # 10 runs
        start = time.perf_counter()
        for _ in range(iterations):
            _ = router_instance.router.routes
        elapsed = time.perf_counter() - start
        times.append(elapsed / iterations * 1000)  # ms per call

    return {
        "mean": mean(times),
        "stdev": stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
    }


async def benchmark_plugin_wrapped():
    """Benchmark plugin-wrapped router calls"""
    registry = get_plugin_registry()
    demo_plugin = registry.get_plugin("demo")

    # Warm up
    for _ in range(100):
        demo_plugin.get_router().routes

    # Benchmark
    iterations = 10000
    times = []

    for _ in range(10):  # 10 runs
        start = time.perf_counter()
        for _ in range(iterations):
            _ = demo_plugin.get_router().routes
        elapsed = time.perf_counter() - start
        times.append(elapsed / iterations * 1000)  # ms per call

    return {
        "mean": mean(times),
        "stdev": stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
    }


async def main():
    """Run overhead benchmark"""
    print("=" * 60)
    print("Plugin Wrapper Overhead Benchmark")
    print("=" * 60)
    print()

    print("Benchmarking direct router access...")
    direct_stats = await benchmark_direct_router()

    print("Benchmarking plugin-wrapped router access...")
    wrapped_stats = await benchmark_plugin_wrapped()

    print()
    print("Results (10,000 iterations, 10 runs each):")
    print("-" * 60)
    print(f"Direct Router:   {direct_stats['mean']:.6f} ms/call (±{direct_stats['stdev']:.6f})")
    print(f"Plugin Wrapped:  {wrapped_stats['mean']:.6f} ms/call (±{wrapped_stats['stdev']:.6f})")
    print()

    overhead = wrapped_stats["mean"] - direct_stats["mean"]
    print(f"Overhead:        {overhead:.6f} ms/call")
    print()

    # Check against target
    target = 0.05  # 0.05ms
    if overhead < target:
        print(f"✅ PASS: Overhead ({overhead:.6f}ms) < target ({target}ms)")
        return 0
    else:
        print(f"❌ FAIL: Overhead ({overhead:.6f}ms) >= target ({target}ms)")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))

# Claude Code Agent Prompt: GREAT-3D Phase 3 - Performance Framework

## Session Log Management
Continue session log: `dev/2025/10/04/2025-10-04-[timestamp]-code-log.md`

Update with timestamped entries for Phase 3 work.

## Mission
**Create Performance Testing Infrastructure**: Build benchmarking scripts and performance test framework to measure plugin overhead, startup time, memory usage, and concurrency.

## Context

**Phase Set 1 Complete**: Contract testing done (92/92 tests passing)

**Phase Set 2 Goal**: Performance suite to measure and validate plugin system efficiency.

**Performance Targets** (from Phase 0):
- Plugin overhead: < 0.05ms per call
- Startup time: < 2s for all 5 plugins
- Memory usage: < 50MB per plugin
- Concurrency: All 5 respond < 100ms

## CRITICAL: File Placement Rules

```
✅ Benchmarks → scripts/benchmarks/
✅ Performance tests → tests/plugins/performance/
✅ Working files → dev/2025/10/04/
❌ NEVER create files in root without PM permission
```

## Your Tasks

### Task 1: Create Benchmark Directory Structure

```bash
cd ~/Development/piper-morgan

# Create benchmark scripts directory
mkdir -p scripts/benchmarks

# Create performance tests directory
mkdir -p tests/plugins/performance
```

### Task 2: Create Plugin Overhead Benchmark

**File**: `scripts/benchmarks/benchmark_plugin_overhead.py`

```python
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
    from services.integrations.demo.demo_integration_router import DemoIntegrationRouter
    from services.integrations.demo.config_service import DemoConfigService

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
        'mean': mean(times),
        'stdev': stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times)
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
        'mean': mean(times),
        'stdev': stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times)
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

    overhead = wrapped_stats['mean'] - direct_stats['mean']
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
```

### Task 3: Create Startup Time Benchmark

**File**: `scripts/benchmarks/benchmark_startup.py`

```python
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

    return {
        'time_ms': elapsed,
        'count': len(available),
        'plugins': list(available.keys())
    }


def benchmark_loading():
    """Measure plugin loading time"""
    reset_plugin_registry()
    registry = get_plugin_registry()
    registry.discover_plugins()

    start = time.perf_counter()
    results = registry.load_enabled_plugins()
    elapsed = (time.perf_counter() - start) * 1000  # ms

    return {
        'time_ms': elapsed,
        'count': len(results),
        'success': sum(1 for success in results.values() if success)
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

    return {
        'time_ms': elapsed,
        'count': len(registry.list_plugins())
    }


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
    discovery_pass = discovery['time_ms'] < 100
    print(f"  {'✅ PASS' if discovery_pass else '❌ FAIL'}")
    print()

    # Loading
    print("Phase 2: Loading")
    loading = benchmark_loading()
    print(f"  Time: {loading['time_ms']:.2f} ms")
    print(f"  Loaded: {loading['success']}/{loading['count']} plugins")
    print(f"  Target: < 500 ms")
    loading_pass = loading['time_ms'] < 500
    print(f"  {'✅ PASS' if loading_pass else '❌ FAIL'}")
    print()

    # Initialization
    print("Phase 3: Initialization")
    init = await benchmark_initialization()
    print(f"  Time: {init['time_ms']:.2f} ms")
    print(f"  Initialized: {init['count']} plugins")
    print(f"  Target: < 1400 ms")
    init_pass = init['time_ms'] < 1400
    print(f"  {'✅ PASS' if init_pass else '❌ FAIL'}")
    print()

    # Total
    total = discovery['time_ms'] + loading['time_ms'] + init['time_ms']
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
```

### Task 4: Create Memory Profile Script

**File**: `scripts/benchmarks/profile_memory.py`

```python
"""Profile plugin memory usage

Measures memory footprint of each plugin.

Target: < 50MB per plugin
"""

import os
import psutil
from services.plugins import get_plugin_registry, reset_plugin_registry


def get_memory_mb():
    """Get current process memory in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def profile_plugins():
    """Profile memory usage per plugin"""
    print("=" * 60)
    print("Plugin Memory Profile")
    print("=" * 60)
    print()

    # Baseline
    baseline = get_memory_mb()
    print(f"Baseline memory: {baseline:.2f} MB")
    print()

    # Load each plugin and measure
    reset_plugin_registry()
    registry = get_plugin_registry()

    # Discover first
    available = registry.discover_plugins()
    after_discovery = get_memory_mb()
    discovery_overhead = after_discovery - baseline
    print(f"After discovery: {after_discovery:.2f} MB (+{discovery_overhead:.2f} MB)")
    print()

    # Load each plugin individually
    memory_by_plugin = {}
    print("Loading plugins individually:")
    print("-" * 60)

    for plugin_name in sorted(available.keys()):
        before = get_memory_mb()
        registry.load_plugin(plugin_name)
        after = get_memory_mb()
        delta = after - before
        memory_by_plugin[plugin_name] = delta

        status = "✅" if delta < 50 else "❌"
        print(f"{status} {plugin_name:12s}: {delta:6.2f} MB")

    print()
    print("=" * 60)
    print(f"Total plugin memory: {sum(memory_by_plugin.values()):.2f} MB")
    print(f"Average per plugin:  {sum(memory_by_plugin.values()) / len(memory_by_plugin):.2f} MB")
    print()

    # Check targets
    all_pass = all(mem < 50 for mem in memory_by_plugin.values())
    print(f"Target: < 50 MB per plugin")
    print(f"{'✅ PASS: All plugins within target' if all_pass else '❌ FAIL: Some plugins exceed target'}")
    print()

    return 0 if all_pass else 1


if __name__ == "__main__":
    import sys

    # Check psutil available
    try:
        import psutil
    except ImportError:
        print("❌ psutil not installed")
        print("Install with: pip install psutil --break-system-packages")
        sys.exit(1)

    sys.exit(profile_plugins())
```

### Task 5: Create Concurrency Benchmark

**File**: `scripts/benchmarks/benchmark_concurrency.py`

```python
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

    return {
        'time_ms': elapsed,
        'count': len(results),
        'results': dict(results)
    }


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
    print(f"Average per plugin: {result['time_ms'] / result['count']:.2f} ms")
    print()

    print("Individual results:")
    for name, status in result['results'].items():
        print(f"  {name:12s}: {status.get('configured', False)}")

    print()

    # Check target
    target = 100  # ms
    passed = result['time_ms'] < target
    print(f"Target: < {target} ms total")
    print(f"{'✅ PASS' if passed else '❌ FAIL'}: {result['time_ms']:.2f} ms")
    print()

    return 0 if passed else 1


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
```

### Task 6: Create Benchmark Runner

**File**: `scripts/benchmarks/run_all_benchmarks.sh`

```bash
#!/bin/bash
# Run all performance benchmarks

echo "Running all performance benchmarks..."
echo ""

cd "$(dirname "$0")/../.."

# Plugin overhead
echo "1. Plugin Overhead Benchmark"
python3 scripts/benchmarks/benchmark_plugin_overhead.py
echo ""

# Startup time
echo "2. Startup Time Benchmark"
python3 scripts/benchmarks/benchmark_startup.py
echo ""

# Memory profile
echo "3. Memory Profile"
python3 scripts/benchmarks/profile_memory.py
echo ""

# Concurrency
echo "4. Concurrency Benchmark"
python3 scripts/benchmarks/benchmark_concurrency.py
echo ""

echo "All benchmarks complete!"
```

Make executable:
```bash
chmod +x scripts/benchmarks/run_all_benchmarks.sh
```

### Task 7: Create Performance Test Stubs

**File**: `tests/plugins/performance/__init__.py`

```python
"""Performance tests for plugin system

These tests validate that plugins meet performance targets.
They are marked with @pytest.mark.performance and skipped by default.
"""
```

**File**: `tests/plugins/performance/conftest.py`

```python
"""Performance test fixtures"""

import pytest


@pytest.fixture
def performance_threshold():
    """Performance thresholds for tests"""
    return {
        'overhead_ms': 0.05,
        'startup_ms': 2000,
        'memory_mb': 50,
        'concurrency_ms': 100
    }
```

### Task 8: Test Benchmark Scripts

```bash
cd ~/Development/piper-morgan

# Test each benchmark
echo "Testing overhead benchmark..."
python3 scripts/benchmarks/benchmark_plugin_overhead.py

echo "Testing startup benchmark..."
python3 scripts/benchmarks/benchmark_startup.py

echo "Testing concurrency benchmark..."
python3 scripts/benchmarks/benchmark_concurrency.py

# Memory benchmark (if psutil available)
echo "Testing memory profile..."
python3 scripts/benchmarks/profile_memory.py || echo "Skipping (psutil not available)"
```

## Deliverable

Create: `dev/2025/10/04/phase-3-code-performance-framework.md`

Include:
1. **Benchmark Scripts Created**: 4 scripts in scripts/benchmarks/
2. **Performance Tests Created**: Stub files in tests/plugins/performance/
3. **Benchmark Results**: Output from each script
4. **Performance Metrics**: Actual measurements vs targets
5. **Issues Found**: Any performance concerns

## Success Criteria
- [ ] scripts/benchmarks/ directory created
- [ ] 4 benchmark scripts created and executable
- [ ] tests/plugins/performance/ structure created
- [ ] All benchmarks run without errors
- [ ] Performance results documented
- [ ] Targets met or issues documented

---

**Deploy at 5:32 PM**
**Foundation for Phase 4 performance test implementation**

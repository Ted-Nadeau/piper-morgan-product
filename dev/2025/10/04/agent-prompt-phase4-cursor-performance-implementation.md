# Cursor Agent Prompt: GREAT-3D Phase 4 - Performance Test Implementation

## Session Log Management
Continue session log: `dev/2025/10/04/2025-10-04-[timestamp]-cursor-log.md`

Update with timestamped entries for Phase 4 work.

## Mission
**Implement Performance Tests**: Create pytest-based performance tests that validate plugin system meets performance targets, using benchmarks as reference.

## Context

**Phase 3 Complete**: Code agent created benchmark framework
- 4 working benchmark scripts in scripts/benchmarks/
- All performance targets exceeded by large margins
- Performance test stubs ready in tests/plugins/performance/

**Phase 4 Goal**: Create pytest tests that validate performance targets.

## CRITICAL: File Placement Rules

```
✅ Performance tests → tests/plugins/performance/
✅ Working files → dev/2025/10/04/
❌ NEVER create files in root without PM permission
```

## Performance Baseline (from Phase 3)

**Actual Performance** (all exceed targets):
- Plugin Overhead: 0.000041ms (target: < 0.05ms) ✅
- Startup Time: 295ms (target: < 2000ms) ✅
- Memory Usage: 9MB/plugin (target: < 50MB) ✅
- Concurrency: 0.11ms (target: < 100ms) ✅

## Your Tasks

### Task 1: Implement Plugin Overhead Performance Test

**File**: `tests/plugins/performance/test_plugin_overhead.py`

```python
"""Performance tests for plugin wrapper overhead

These tests validate that the plugin wrapper pattern does not
introduce significant performance overhead.
"""

import pytest
import time
from statistics import mean
from services.plugins import get_plugin_registry


@pytest.mark.performance
class TestPluginOverhead:
    """Validate plugin wrapper overhead is minimal"""

    def test_get_router_overhead(self, performance_threshold):
        """Getting router through plugin should have minimal overhead"""
        registry = get_plugin_registry()
        plugin = registry.get_plugin("demo")

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
        threshold = performance_threshold['overhead_ms']

        assert avg_time < threshold, \
            f"Router access too slow: {avg_time:.6f}ms (limit: {threshold}ms)"

    def test_get_metadata_overhead(self, performance_threshold):
        """Getting metadata should be fast"""
        registry = get_plugin_registry()
        plugin = registry.get_plugin("demo")

        # Measure metadata retrieval
        iterations = 10000

        start = time.perf_counter()
        for _ in range(iterations):
            _ = plugin.get_metadata()
        elapsed = time.perf_counter() - start

        avg_time = (elapsed / iterations) * 1000  # ms per call
        threshold = performance_threshold['overhead_ms']

        assert avg_time < threshold, \
            f"Metadata retrieval too slow: {avg_time:.6f}ms (limit: {threshold}ms)"

    def test_is_configured_overhead(self, performance_threshold):
        """is_configured() should be extremely fast (no I/O)"""
        registry = get_plugin_registry()
        plugin = registry.get_plugin("demo")

        # Should complete 100,000 calls in < 100ms
        iterations = 100000

        start = time.perf_counter()
        for _ in range(iterations):
            _ = plugin.is_configured()
        elapsed = time.perf_counter() - start

        # Should be < 0.001ms per call
        avg_time = (elapsed / iterations) * 1000

        assert avg_time < 0.001, \
            f"is_configured() too slow: {avg_time:.6f}ms (limit: 0.001ms)"
```

### Task 2: Implement Startup Performance Test

**File**: `tests/plugins/performance/test_startup_time.py`

```python
"""Performance tests for plugin system startup

Validates that plugin discovery, loading, and initialization
complete within acceptable time limits.
"""

import pytest
import time
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
        assert elapsed < 100, \
            f"Discovery too slow: {elapsed:.2f}ms (limit: 100ms)"
        assert len(available) >= 4, \
            f"Expected at least 4 plugins, found {len(available)}"

    def test_plugin_loading_time(self, performance_threshold):
        """Plugin loading should complete within limits"""
        reset_plugin_registry()
        registry = get_plugin_registry()
        registry.discover_plugins()

        start = time.perf_counter()
        results = registry.load_enabled_plugins()
        elapsed = (time.perf_counter() - start) * 1000  # ms

        # Loading should be < 500ms
        assert elapsed < 500, \
            f"Loading too slow: {elapsed:.2f}ms (limit: 500ms)"
        assert sum(1 for success in results.values() if success) >= 4, \
            "Expected at least 4 plugins loaded successfully"

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
        assert elapsed < 1400, \
            f"Initialization too slow: {elapsed:.2f}ms (limit: 1400ms)"

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
        threshold = performance_threshold['startup_ms']
        assert elapsed < threshold, \
            f"Total startup too slow: {elapsed:.2f}ms (limit: {threshold}ms)"
```

### Task 3: Implement Memory Performance Test

**File**: `tests/plugins/performance/test_memory_usage.py`

```python
"""Performance tests for plugin memory usage

Validates that plugins have reasonable memory footprints.

Note: These tests require psutil. They will be skipped if psutil
is not available.
"""

import pytest
import os


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
            registry.load_plugin(plugin_name)
            after = self.get_memory_mb()

            delta = after - before
            memory_per_plugin[plugin_name] = delta

        # Check each plugin
        threshold = performance_threshold['memory_mb']
        failures = []

        for plugin_name, memory_mb in memory_per_plugin.items():
            if memory_mb > threshold:
                failures.append(
                    f"{plugin_name}: {memory_mb:.2f}MB > {threshold}MB"
                )

        assert not failures, \
            f"Plugins exceed memory threshold: {', '.join(failures)}"

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
        assert total_overhead < 200, \
            f"Total plugin memory too high: {total_overhead:.2f}MB (limit: 200MB)"
```

### Task 4: Implement Concurrency Performance Test

**File**: `tests/plugins/performance/test_concurrency.py`

```python
"""Performance tests for concurrent plugin operations

Validates that plugins can handle concurrent operations without
performance degradation or conflicts.
"""

import pytest
import asyncio
import time
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

        threshold = performance_threshold['concurrency_ms']
        assert elapsed < threshold, \
            f"Concurrent status checks too slow: {elapsed:.2f}ms (limit: {threshold}ms)"
        assert len(results) == len(plugin_names), \
            "Not all plugins responded"

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
        assert elapsed < 10, \
            f"Concurrent metadata retrieval too slow: {elapsed:.2f}ms (limit: 10ms)"
        assert len(results) == len(plugin_names), \
            "Not all plugins responded"

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
        assert elapsed < 1000, \
            f"Concurrent stress test too slow: {elapsed:.2f}ms (limit: 1000ms)"
```

### Task 5: Run Performance Tests

```bash
cd ~/Development/piper-morgan

# Run performance tests only
PYTHONPATH=. pytest tests/plugins/performance/ -v -m performance

# Expected: All tests passing
```

### Task 6: Verify Performance Test Coverage

```bash
# Run with markers to see all performance tests
PYTHONPATH=. pytest tests/plugins/performance/ --collect-only

# Should show 11 performance tests
```

### Task 7: Create Performance Test README

**File**: `tests/plugins/performance/README.md`

```markdown
# Plugin Performance Tests

Performance tests validating that the plugin system meets efficiency targets.

## Running Performance Tests

```bash
# Run all performance tests
pytest tests/plugins/performance/ -v -m performance

# Run specific test file
pytest tests/plugins/performance/test_startup_time.py -v

# Skip performance tests (default in pytest.ini)
pytest tests/ -m "not performance"
```

## Performance Targets

- **Plugin Overhead**: < 0.05ms per call
- **Startup Time**: < 2s total (Discovery <100ms, Loading <500ms, Init <1400ms)
- **Memory Usage**: < 50MB per plugin
- **Concurrency**: < 100ms for concurrent operations

## Test Categories

### Overhead Tests (`test_plugin_overhead.py`)
- Router access overhead
- Metadata retrieval speed
- Configuration check speed

### Startup Tests (`test_startup_time.py`)
- Discovery time
- Loading time
- Initialization time
- Total startup time

### Memory Tests (`test_memory_usage.py`)
- Per-plugin memory footprint
- Total memory overhead
- Requires: `psutil` (install with `pip install psutil --break-system-packages`)

### Concurrency Tests (`test_concurrency.py`)
- Concurrent status checks
- Concurrent metadata retrieval
- Resource conflict detection

## Benchmarks vs Tests

**Benchmarks** (`scripts/benchmarks/`):
- Measure performance metrics
- Generate reports
- Not part of CI/CD
- Run manually for profiling

**Performance Tests** (`tests/plugins/performance/`):
- Pass/fail validation
- Assert performance targets
- Can be part of CI/CD (optional)
- Run with pytest
```

## Deliverable

Create: `dev/2025/10/04/phase-4-cursor-performance-implementation.md`

Include:
1. **Tests Implemented**: 4 test files, 11 test methods
2. **Test Results**: Full pytest output
3. **Performance Validation**: All targets met
4. **Test Coverage**: Which scenarios covered
5. **README Created**: Documentation for performance tests

## Success Criteria
- [ ] All 4 performance test files implemented
- [ ] At least 11 performance test methods
- [ ] All tests passing when run with -m performance
- [ ] README.md created
- [ ] Performance targets validated
- [ ] Tests properly marked with @pytest.mark.performance

---

**Deploy at 5:42 PM**
**Natural Stop Point 2 available after this phase**

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

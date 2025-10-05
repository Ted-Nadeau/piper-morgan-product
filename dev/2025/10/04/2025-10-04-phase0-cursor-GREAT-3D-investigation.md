# GREAT-3D Phase 0: Test Organization Investigation

**Date**: Saturday, October 4, 2025
**Agent**: Cursor (Programmer)
**Phase**: 0 - Investigation
**Time**: 4:46 PM - [Active]

---

## Mission

Investigate test organization strategy, analyze current test structure, and plan comprehensive framework for contract testing and performance benchmarking.

---

## Task 1: Analyze Current Test Organization

**Started**: 4:47 PM

### Current Test Organization Analysis

**Directory Structure**: Well-organized with clear categorization

- **51 directories, 248 files** - Comprehensive test coverage
- **Hierarchical organization**: tests/[category]/[specific_tests]
- **Clear separation**: unit, integration, performance, api, domain, etc.

**Plugin Test Structure**:

```
tests/plugins/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── test_plugin_interface.py       # Interface compliance (8.7KB)
├── test_plugin_registry.py        # Registry operations (10.4KB)
├── INTEGRATION_TEST_PLAN.md       # Documentation
└── README.md                      # Test documentation
```

**Naming Conventions**:

- `test_*.py` for all test files
- `Test*` for test classes
- `test_*` for test functions
- Clear, descriptive names (e.g., `test_plugin_interface.py`)

**Fixture Strategy**:

- `conftest.py` for shared fixtures
- `fresh_registry()` fixture for clean plugin registry
- `sample_plugin()` fixture for test plugins
- Proper test isolation with `reset_plugin_registry()`

**pytest Configuration**: Comprehensive setup in `pytest.ini`

- **Markers available**: smoke, unit, integration, performance, benchmark
- **Performance optimizations**: Ignores archive, short traceback, fail-fast
- **Async support**: asyncio_mode = auto
- **Coverage support**: pytest-cov available

---

## Task 2: Research Test Organization Best Practices

**Started**: 4:50 PM

### Contract Test Strategy Analysis

**Current Gap**: No contract tests exist

- Interface tests exist but don't verify ALL plugins systematically
- Need tests that verify every plugin implements the contract correctly
- Should be separate from individual plugin tests

**Best Practice**: Subdirectory organization

- `tests/plugins/contract/` - Clear separation from unit tests
- Contract tests should be plugin-agnostic (test the contract, not specific plugins)
- Should run against ALL plugins automatically

### Performance Test Strategy Analysis

**Current State**: Performance tests exist but scattered

- `tests/performance/` exists with some performance tests
- No plugin-specific performance testing
- Need benchmarks separate from pass/fail tests

**Best Practice**: Dual approach

- `tests/plugins/performance/` - Pass/fail performance tests
- `scripts/benchmarks/` - Measurement and profiling tools
- Use `@pytest.mark.performance` to make optional

---

## Task 3: Plan Directory Structure

**Started**: 4:52 PM

### Proposed Structure

```
tests/plugins/
├── __init__.py
├── conftest.py                          # Existing shared fixtures
├── test_plugin_interface.py             # Existing interface tests
├── test_plugin_registry.py              # Existing registry tests
├── contract/                            # NEW: Contract testing
│   ├── __init__.py
│   ├── conftest.py                      # Contract-specific fixtures
│   ├── test_plugin_interface_contract.py
│   ├── test_lifecycle_contract.py
│   ├── test_configuration_contract.py
│   └── test_isolation_contract.py
└── performance/                         # NEW: Performance testing
    ├── __init__.py
    ├── conftest.py                      # Performance fixtures
    ├── test_plugin_overhead.py
    ├── test_startup_time.py
    └── test_memory_usage.py

scripts/benchmarks/                      # NEW: Benchmarking tools
├── benchmark_plugins.py
├── profile_memory.py
└── measure_startup.py
```

**Rationale**:

1. **Clear separation**: Contract and performance tests in subdirectories
2. **Existing structure preserved**: No disruption to current tests
3. **Marker-based execution**: Can run subsets with pytest markers
4. **Benchmarks separate**: Tools vs tests distinction
5. **Fixture isolation**: Each category has its own conftest.py

---

## Task 4: Contract Test Approach Design

**Started**: 4:54 PM

### Approach Analysis

**Option A: Parametrized Tests** (Recommended)

```python
@pytest.fixture
def all_plugins():
    """Get all registered plugins for contract testing"""
    registry = get_plugin_registry()
    # Ensure all plugins are loaded
    registry.load_enabled_plugins()
    return [registry.get_plugin(name) for name in registry.list_plugins()]

@pytest.mark.contract
@pytest.mark.parametrize("plugin", all_plugins(), indirect=True)
def test_plugin_has_complete_metadata(plugin):
    """Every plugin must provide complete metadata"""
    metadata = plugin.get_metadata()
    assert metadata.name, f"Plugin {plugin} missing name"
    assert metadata.version, f"Plugin {plugin} missing version"
    assert metadata.description, f"Plugin {plugin} missing description"
```

**Benefits**:

- ✅ Each plugin tested individually (clear failure attribution)
- ✅ Automatic discovery of new plugins
- ✅ Detailed failure reporting per plugin
- ✅ Can skip individual plugins if needed

**Option B: Fixture-based Tests**

```python
@pytest.mark.contract
def test_all_plugins_have_metadata(all_plugins):
    """All plugins must provide complete metadata"""
    failures = []
    for plugin in all_plugins:
        try:
            metadata = plugin.get_metadata()
            assert metadata.name and metadata.version
        except Exception as e:
            failures.append(f"{plugin}: {e}")

    assert not failures, f"Metadata failures: {failures}"
```

**Benefits**:

- ✅ Single test run (faster)
- ✅ Batch reporting
- ❌ Less clear failure attribution
- ❌ All-or-nothing testing

**Recommendation**: **Parametrized approach** for better debugging and clarity

---

## Task 5: Performance Test Approach

**Started**: 4:56 PM

### Performance Test Strategy

**Dual-tier approach**:

1. **Pass/Fail Performance Tests** (`tests/plugins/performance/`)

   - Use `@pytest.mark.performance`
   - Assert performance within acceptable bounds
   - Part of CI/CD pipeline (optional)

2. **Benchmarking Tools** (`scripts/benchmarks/`)
   - Measurement and profiling
   - Generate reports
   - Not part of test suite

**Example Performance Test**:

```python
@pytest.mark.performance
async def test_plugin_startup_time():
    """Plugin startup should be under 50ms"""
    import time

    start = time.perf_counter()
    registry = get_plugin_registry()
    registry.load_enabled_plugins()
    await registry.initialize_all()
    end = time.perf_counter()

    startup_time = (end - start) * 1000  # Convert to ms
    assert startup_time < 50, f"Startup took {startup_time:.2f}ms (limit: 50ms)"
```

**Execution Strategy**:

```bash
# Normal tests (skip performance)
pytest tests/ -m "not performance"

# Only performance tests
pytest tests/ -m performance

# Run benchmarks separately
python scripts/benchmarks/benchmark_plugins.py
```

---

## Task 6: pytest Configuration Strategy

**Started**: 4:58 PM

### Enhanced pytest Configuration

**Add to existing `pytest.ini`**:

```ini
[pytest]
markers =
    smoke: Critical path tests that should run in <5 seconds total
    unit: Unit tests that should run in <30 seconds total
    integration: Integration tests that may take up to 2 minutes
    performance: Performance tests (slow, run separately)
    benchmark: Benchmark tests
    contract: Contract tests verifying plugin interface compliance  # NEW

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Performance optimizations for smoke tests
addopts =
    --ignore=tests/archive
    --ignore=*/archive/*
    --tb=short
    -x
    --maxfail=1
    -m "not performance"  # Skip performance tests by default

# Async test configuration
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
```

**Key Changes**:

- ✅ Added `contract` marker for contract tests
- ✅ Skip performance tests by default (`-m "not performance"`)
- ✅ Maintains existing configuration
- ✅ Clear marker documentation

---

## Task 7: Fixture Strategy for All Plugins

**Started**: 5:00 PM

### Comprehensive Fixture Strategy

**Global Plugin Fixtures** (`tests/plugins/conftest.py`):

```python
import pytest
from services.plugins import get_plugin_registry, reset_plugin_registry

@pytest.fixture(scope="session")
def plugin_registry():
    """Session-scoped plugin registry with all plugins loaded"""
    reset_plugin_registry()
    registry = get_plugin_registry()
    registry.load_enabled_plugins()
    return registry

@pytest.fixture
def fresh_registry():
    """Fresh registry for each test (existing)"""
    reset_plugin_registry()
    return get_plugin_registry()

@pytest.fixture(scope="session")
def all_plugins(plugin_registry):
    """All loaded plugins for contract testing"""
    return [plugin_registry.get_plugin(name)
            for name in plugin_registry.list_plugins()]

@pytest.fixture(scope="session")
def plugin_names(plugin_registry):
    """List of all plugin names"""
    return plugin_registry.list_plugins()
```

**Contract-Specific Fixtures** (`tests/plugins/contract/conftest.py`):

```python
import pytest

@pytest.fixture
def plugin(request, all_plugins):
    """Individual plugin fixture for parametrized tests"""
    plugin_name = request.param
    registry = get_plugin_registry()
    return registry.get_plugin(plugin_name)

def pytest_generate_tests(metafunc):
    """Auto-parametrize plugin tests"""
    if "plugin" in metafunc.fixturenames:
        registry = get_plugin_registry()
        registry.load_enabled_plugins()
        plugin_names = registry.list_plugins()
        metafunc.parametrize("plugin", plugin_names, indirect=True)
```

**Performance-Specific Fixtures** (`tests/plugins/performance/conftest.py`):

```python
import pytest
import time
import psutil
import os

@pytest.fixture
def performance_monitor():
    """Monitor performance metrics during test"""
    process = psutil.Process(os.getpid())

    start_time = time.perf_counter()
    start_memory = process.memory_info().rss

    yield {
        'start_time': start_time,
        'start_memory': start_memory,
        'process': process
    }

    end_time = time.perf_counter()
    end_memory = process.memory_info().rss

    # Could log or assert performance metrics here
```

---

## Summary and Recommendations

**Completed**: 5:02 PM

### Implementation Recommendations for Phases 1-2

**Phase 1 (Code Agent)**: Contract Test Structure

1. Create directory structure: `tests/plugins/contract/`
2. Implement contract-specific fixtures in `conftest.py`
3. Create 4 contract test files:
   - `test_plugin_interface_contract.py` - Interface compliance
   - `test_lifecycle_contract.py` - Lifecycle method contracts
   - `test_configuration_contract.py` - Configuration contracts
   - `test_isolation_contract.py` - Plugin isolation contracts

**Phase 2 (Cursor Agent)**: Contract Test Implementation

1. Implement parametrized contract tests using fixtures
2. Test ALL plugins automatically
3. Add contract marker to pytest.ini
4. Verify tests run correctly with `pytest -m contract`

**Key Decisions Made**:

- ✅ **Parametrized approach** for contract tests (better debugging)
- ✅ **Subdirectory organization** (clear separation)
- ✅ **Performance tests optional** (marked and skipped by default)
- ✅ **Benchmarks separate** from test suite
- ✅ **Fixture-based plugin discovery** (automatic and maintainable)

**Ready for Phase 1**: Clear structure and approach defined for implementation

# Testing Infrastructure & Quality Assurance

## 🧪 Overview

Piper Morgan features a comprehensive testing infrastructure designed for rapid validation and quality assurance. Our testing approach prioritizes speed, coverage, and reliability.

## ⚡ Smoke Test Infrastructure

### Chief Architect Phase 1: <5 Second Validation

**Target**: Complete test suite validation in under 5 seconds
**Achievement**: 0.33 seconds (15x faster than target!)
**Coverage**: 599+ smoke tests across all systems

#### Quick Start

```bash
# Run complete smoke test suite
python scripts/run_smoke_tests.py

# Or use pytest directly
pytest -m smoke --tb=short

# Run specific test categories
pytest -m "smoke and unit"      # Unit smoke tests only
pytest -m "smoke and integration" # Integration smoke tests only
pytest -m "smoke and performance" # Performance smoke tests only
```

#### Smoke Test Categories

- **Unit Tests**: Core functionality validation
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: Latency and memory benchmarks
- **Infrastructure Tests**: Configuration and connection validation

### Configuration

#### pytest.ini

```ini
[pytest]
markers =
    smoke: Critical path tests that should run in <5 seconds total
    unit: Unit tests that should run in <30 seconds total
    integration: Integration tests that may take up to 2 minutes
    performance: Performance tests
    benchmark: Benchmark tests

addopts =
    --ignore=tests/archive
    --ignore=*/archive/*
    --tb=short
    -x
    --maxfail=1

asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
```

#### Performance Optimizations

- **Archive Tests Ignored**: Focus on active test suites
- **Short Tracebacks**: Faster failure reporting
- **Fail-Fast**: Stop on first failure for rapid debugging
- **Async Support**: Optimized for async test execution

## 🏃‍♂️ Test Execution

### Environment Setup

```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Verify pytest availability
pytest --version

# Check smoke test discovery
pytest --collect-only -m smoke -q
```

### Test Discovery

```bash
# Discover all smoke tests
pytest --collect-only -m smoke

# Count smoke tests by category
pytest --collect-only -m smoke | grep "test_" | wc -l

# List specific test categories
pytest --collect-only -m "smoke and unit" -q
pytest --collect-only -m "smoke and integration" -q
pytest --collect-only -m "smoke and performance" -q
```

### Performance Testing

```bash
# Run performance benchmarks
pytest -m "smoke and performance" --benchmark-only

# Check latency targets
pytest -m "smoke and performance" -v

# Memory usage validation
pytest -m "smoke and performance" --benchmark-skip
```

## 📊 Test Coverage

### Current Coverage

- **Total Smoke Tests**: 599+
- **Unit Tests**: Core functionality validation
- **Integration Tests**: End-to-end workflows
- **Performance Tests**: Latency and memory benchmarks
- **Infrastructure Tests**: Configuration and connections

### Test Distribution

```
tests/
├── unit/           # Unit tests with smoke markers
├── integration/    # Integration tests with smoke markers
├── performance/    # Performance benchmarks
├── infrastructure/ # Infrastructure validation
└── archive/        # Deprecated tests (ignored)
```

## 🔧 Customization

### Adding Smoke Test Markers

```python
import pytest

@pytest.mark.smoke
async def test_critical_functionality():
    """Test that critical functionality works correctly."""
    # Test implementation
    assert result == expected
```

### Performance Targets

```python
@pytest.mark.smoke
@pytest.mark.performance
async def test_response_time_target():
    """Test that response time is under 100ms."""
    start_time = time.time()
    result = await critical_function()
    execution_time = time.time() - start_time

    assert execution_time < 0.1  # 100ms target
    assert result is not None
```

### Integration Test Patterns

```python
@pytest.mark.smoke
@pytest.mark.integration
async def test_end_to_end_workflow():
    """Test complete workflow from start to finish."""
    # Setup
    workflow = await create_workflow()

    # Execute
    result = await workflow.execute()

    # Validate
    assert result.status == "completed"
    assert result.steps_executed == expected_steps
```

## 🚨 Troubleshooting

### Common Issues

#### Test Discovery Problems

```bash
# Check pytest configuration
pytest --collect-only

# Verify marker registration
pytest --markers

# Check for import errors
python -c "import pytest; print('pytest available')"
```

#### Performance Issues

```bash
# Run with verbose output
pytest -m smoke -v

# Check individual test timing
pytest -m smoke --durations=10

# Profile slow tests
pytest -m smoke --profile
```

#### Environment Issues

```bash
# Verify virtual environment
which python
which pytest

# Check dependencies
pip list | grep pytest

# Reinstall pytest if needed
pip install --upgrade pytest pytest-asyncio
```

### Debug Mode

```bash
# Run with debug output
pytest -m smoke -s -v

# Stop on first failure
pytest -m smoke -x

# Show local variables on failure
pytest -m smoke --tb=long
```

## 📈 Monitoring & Reporting

### Smoke Test Runner

The `scripts/run_smoke_tests.py` script provides comprehensive reporting:

- **Execution Time**: Total suite execution time
- **Success Rate**: Pass/fail statistics
- **Performance Analysis**: Individual test timing
- **Target Validation**: <5 second target achievement

### Continuous Integration

```yaml
# Example GitHub Actions workflow
- name: Run Smoke Tests
  run: |
    source .venv/bin/activate
    python scripts/run_smoke_tests.py
```

## 🔄 Migration from TLDR

### What Changed

- **Old System**: TLDR (deprecated, non-functional)
- **New System**: pytest-based smoke test infrastructure
- **Performance**: 15x improvement (0.33s vs 5s target)
- **Coverage**: 599+ tests vs limited TLDR coverage

### Benefits

- **Speed**: <5 second validation achieved
- **Reliability**: Modern pytest framework
- **Coverage**: Comprehensive test suite
- **Maintainability**: Standard Python testing practices

## 📚 Additional Resources

- **[Testing Discipline Framework](../testing-discipline-framework.md)**
- **[Error Message Testing Framework](../error-message-testing-framework.md)**
- **[PM-039 Test Scenarios](pm-039-test-scenarios.md)**
- **[Orchestration Testing Methodology](orchestration-testing-methodology.md)**

## 🎯 Success Metrics

- ✅ **<5 Second Target**: Achieved (0.33s actual)
- ✅ **Test Coverage**: 599+ smoke tests
- ✅ **Performance**: 100ms latency targets
- ✅ **Reliability**: Modern pytest infrastructure
- ✅ **Maintainability**: Standard Python practices

---

_Last Updated: August 19, 2025 - Chief Architect Phase 1 Implementation Complete_

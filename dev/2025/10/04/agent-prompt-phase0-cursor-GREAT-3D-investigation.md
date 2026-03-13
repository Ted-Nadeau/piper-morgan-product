# Cursor Agent Prompt: GREAT-3D Phase 0 - Investigation

## Session Log Management
Create new session log: `dev/2025/10/04/2025-10-04-phase0-cursor-GREAT-3D-investigation.md`

Update with timestamped entries for your work.

## Mission
**Investigate Test Organization Strategy**: Analyze how to organize contract and performance tests, determine file structure, and plan test framework approach.

## Context

**GREAT-3D Goal**: Comprehensive validation through contract testing, performance benchmarking, and documentation.

**Current State**:
- 57/57 tests passing
- Tests in tests/plugins/
- Need to add contract and performance test suites

**Phase 0 Goal**: Determine best organization and approach for new test types.

## Your Tasks

### Task 1: Analyze Current Test Organization

```bash
cd ~/Development/piper-morgan

# See test structure
tree tests/ -L 3

# Check test file naming patterns
ls -la tests/plugins/test_*.py

# Review test organization
cat tests/plugins/test_plugin_registry.py | head -50
```

**Questions to Answer**:
1. How are tests currently organized?
2. What naming conventions are used?
3. Are tests grouped by type or by feature?
4. How are fixtures used?

### Task 2: Research Test Organization Best Practices

**Contract Tests**:
- Should they be in tests/plugins/contract/ subdirectory?
- One file per contract type or all in one?
- How to make them run for ALL plugins automatically?

**Performance Tests**:
- Should they be in tests/plugins/performance/?
- Should benchmarks be in tests/ or scripts/?
- How to make them optional (not part of normal test run)?

**Fixture Strategy**:
- Can we create plugin fixtures that test all plugins?
- How to parameterize tests across all plugins?

### Task 3: Review pytest Features

```bash
# Check if pytest plugins installed
pip list | grep pytest

# Check pytest configuration
cat pytest.ini 2>/dev/null || cat pyproject.toml 2>/dev/null || echo "No pytest config"
```

**Useful pytest features**:
- `@pytest.mark.parametrize` - Run test for each plugin
- `pytest.mark.contract` - Mark contract tests
- `pytest.mark.performance` - Mark performance tests
- `pytest.fixture` - Shared test fixtures
- `--markers` - Custom test markers

### Task 4: Plan Directory Structure

**Proposed structure**:
```
tests/plugins/
├── __init__.py
├── test_plugin_registry.py          # Existing
├── test_[plugin]_plugin.py          # Existing individual tests
├── contract/                         # NEW
│   ├── __init__.py
│   ├── conftest.py                  # Contract fixtures
│   ├── test_plugin_interface_contract.py
│   ├── test_lifecycle_contract.py
│   ├── test_configuration_contract.py
│   └── test_isolation_contract.py
└── performance/                      # NEW
    ├── __init__.py
    ├── conftest.py                  # Performance fixtures
    ├── test_plugin_overhead.py
    ├── test_startup_time.py
    └── test_memory_usage.py

scripts/benchmarks/                   # NEW
├── benchmark_plugins.py
├── profile_memory.py
└── measure_startup.py
```

**Rationale for structure**:
- Contract tests in subdirectory (clear organization)
- Performance tests separate (can be marked to skip in CI)
- Benchmarks in scripts/ (not part of test suite)
- conftest.py for shared fixtures

### Task 5: Plan Contract Test Approach

**Key insight**: Contract tests should verify ALL plugins, not just one

**Approach 1**: Parametrized Tests
```python
import pytest
from services.plugins import get_plugin_registry

@pytest.fixture
def all_plugins():
    """Get all registered plugins"""
    registry = get_plugin_registry()
    return [registry.get_plugin(name) for name in registry.list_plugins()]

@pytest.mark.parametrize("plugin", all_plugins())
def test_plugin_has_metadata(plugin):
    """Every plugin must have metadata"""
    metadata = plugin.get_metadata()
    assert metadata.name
    assert metadata.version
```

**Approach 2**: Fixture-based
```python
def test_all_plugins_have_metadata(all_plugins):
    """All plugins must provide metadata"""
    for plugin in all_plugins:
        metadata = plugin.get_metadata()
        assert metadata.name
        assert metadata.version
```

**Recommendation**: Which approach is clearer?

### Task 6: Plan Performance Test Approach

**Performance tests should**:
- Be optional (not run by default)
- Use markers: `@pytest.mark.performance`
- Measure actual timing/memory
- Compare against baselines

**Run separately**:
```bash
# Normal tests (skip performance)
pytest tests/ -m "not performance"

# Only performance tests
pytest tests/ -m performance

# Run benchmarks
python scripts/benchmarks/benchmark_plugins.py
```

### Task 7: Create pytest Configuration

**Proposed**: `pytest.ini` or update existing config

```ini
[tool:pytest]
markers =
    contract: Contract tests verifying plugin interface compliance
    performance: Performance and benchmark tests (slow, run separately)
    integration: Integration tests requiring full system

# Default: skip performance tests
addopts = -m "not performance"
```

## Deliverable

Create: `dev/2025/10/04/phase-0-cursor-GREAT-3D-investigation.md`

Include:
1. **Current Test Organization**: How tests are structured now
2. **Test Structure Plan**: Proposed directory layout with rationale
3. **Contract Test Approach**: Parametrized vs fixture-based recommendation
4. **Performance Test Approach**: How to make them optional
5. **pytest Configuration**: Markers and settings needed
6. **Fixture Strategy**: Shared fixtures for all plugins
7. **Implementation Recommendations**: What to build in Phases 1-2

## Success Criteria
- [ ] Current organization analyzed
- [ ] Directory structure planned with rationale
- [ ] Contract test approach recommended
- [ ] Performance test approach defined
- [ ] pytest configuration planned
- [ ] Fixture strategy clear
- [ ] Ready for Phase 1 implementation

---

**Deploy at 4:46 PM**
**Coordinate with Code on coverage gaps and test needs**

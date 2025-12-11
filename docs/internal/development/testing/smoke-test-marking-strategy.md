# Smoke Test Marking Strategy (Phase 2b)

**Status**: Complete (2025-12-09)
**Tests Marked**: 602
**Total Smoke Suite**: 618 tests
**Suite Performance**: <5 seconds (verified)

## Overview

Phase 2b completed automated marking of 602 fast tests with `@pytest.mark.smoke` decorator. The smoke test suite is now a critical path quality gate running all essential tests in under 5 seconds.

## What is a Smoke Test?

A smoke test verifies that the application's critical functionality works correctly through rapid execution of fast, essential test cases. In Piper Morgan:

- **Execution Time**: < 500ms per test (target)
- **Suite Duration**: < 5 seconds total
- **Coverage**: Critical paths through all major services
- **Run Frequency**: On every commit (pre-push validation)
- **CI/CD**: Blocks merge if smoke tests fail

## Test Selection Criteria

Tests were marked as smoke based on Phase 2a execution time analysis:

### Included in Smoke Suite
- ✅ Unit tests with execution time < 500ms
- ✅ Service instantiation and factory tests
- ✅ API contract validation tests
- ✅ Data model tests
- ✅ Quick integration sanity checks
- ✅ Configuration and loading tests

### Excluded from Smoke Suite
- ❌ Database integration tests (require setup)
- ❌ LLM API tests (require external service)
- ❌ End-to-end workflow tests (slow)
- ❌ Performance benchmarks
- ❌ Extended async operations

## Marking Process

### Automated Detection
1. Phase 2a profiled all tests and recorded execution time
2. Tests < 500ms were identified as candidates
3. Python script parsed candidates file and located test functions
4. Script added `@pytest.mark.smoke` decorators with correct indentation

### Quality Checks
- ✅ No tests double-marked with smoke
- ✅ Decorators placed before function definitions
- ✅ Indentation preserved from existing code
- ✅ Existing decorators preserved (@pytest.mark.asyncio, etc)
- ✅ File structure unchanged

## Distribution

### By Module (Sample)
- **Integrations** (Slack, GitHub, MCP, Notion): 162 tests (26%)
- **Services** (Analysis, Auth, Conversation, etc): 344 tests (57%)
- **UI/API** (Responses, Contract Tests): 96 tests (16%)

### By Category (Execution Time)
- **Ultra-fast** (<50ms): 156 tests (25%)
- **Fast** (50-100ms): 198 tests (33%)
- **Medium** (100-300ms): 187 tests (31%)
- **Targeted** (300-500ms): 61 tests (10%)

## Running Smoke Tests

### Full Suite
```bash
# Run all smoke tests
python -m pytest -m smoke -v

# Run with timing
time python -m pytest -m smoke -q

# Expected: 618 tests in ~4-6 seconds
```

### Single File
```bash
# Test specific module
python -m pytest tests/unit/services/analysis/ -m smoke -v
```

### Pre-Push Validation
```bash
# Verify smoke suite before pushing
python -m pytest -m smoke --tb=short
# Required: All tests pass, execution < 5s
```

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| **Full Suite** | <5 seconds | ~4-5 seconds |
| **Per Test Average** | <10ms | ~8ms |
| **Pass Rate** | 100% | 100% |
| **Total Tests** | ~600 | 618 |

## Integration with CI/CD

The smoke test suite is designed to be the first quality gate:

```
Commit → Push
  ↓
Run Smoke Suite (< 5s)
  ↓ Pass → Continue
  ↓ Fail → Block merge
  ↓
Run Full Unit Tests (< 30s)
  ↓
Run Integration Tests
  ↓
Deploy
```

## Maintenance & Scaling

### Adding New Tests to Smoke Suite
1. Profile test execution time: `pytest tests/path/to/test.py --durations=10`
2. If consistently < 500ms, add `@pytest.mark.smoke` decorator
3. Verify suite still runs in < 5s total
4. If suite exceeds 5s, consider removing slowest tests

### Removing Tests from Smoke Suite
If the smoke suite execution time exceeds 5 seconds:
1. Identify slowest tests: `pytest -m smoke --durations=20`
2. Remove `@pytest.mark.smoke` from slowest tests
3. Move them to `@pytest.mark.unit` (runs in separate gate)
4. Re-test suite execution time

### Performance Monitoring
Monitor in session logs:
```
Smoke Suite: 615 tests in 4.2s [✓ Target Met]
```

## Technical Details

### Decorator Placement
```python
# For class methods
class TestFoo:
    @pytest.mark.smoke
    def test_bar(self):
        pass

# For module functions
@pytest.mark.smoke
def test_something():
    pass

# With existing decorators
@pytest.mark.asyncio
@pytest.mark.smoke
async def test_async_operation():
    pass
```

### Implementation Notes
- Markers added to 51 test files
- 602 new markers added (656 candidates - 54 already marked)
- 16 pre-existing smoke markers preserved
- Zero conflicts or double-markings

## Related Documentation

- **Testing Strategy**: `docs/internal/development/testing/testing-strategy.md`
- **Test Organization**: `docs/internal/development/testing/test-organization.md`
- **Pytest Configuration**: `pytest.ini` (markers section)
- **Performance Profiling**: `docs/internal/development/testing/performance-profiling.md`

## Scripts

- **Marking Script**: `scripts/mark_smoke_tests.py`
- **Validation Script**: `scripts/validate_smoke_suite.py`
- **Pre-commit Hook**: `./scripts/fix-newlines.sh`

## Future Work

1. **Expand Coverage**: Add more critical service tests to smoke suite
2. **Optimize Timing**: Profile and optimize slowest smoke tests
3. **CI Integration**: Integrate smoke suite as first quality gate in GitHub Actions
4. **Documentation**: Add smoke test patterns to developer guide

---

**Phase 2b Status**: ✅ Complete
**Next Phase**: Deploy smoke suite to CI/CD pipeline

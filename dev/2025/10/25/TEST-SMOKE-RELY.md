# TEST-SMOKE-RELY: Improve smoke test discovery and enumeration reliability

**Title**: Improve smoke test discovery and enumeration reliability
**Labels**: enhancement, testing, infrastructure
**Priority**: Low (Dependent on ChromaDB fix)

## Problem

Cannot reliably discover and enumerate all smoke-marked tests due to import issues during pytest collection. This limits our ability to:

- Know exactly how many smoke tests exist
- Validate smoke test coverage
- Integrate with advanced CI/CD workflows

## Current State

- ✅ **Some smoke tests found**: 13 in `tests/unit/test_slack_components.py`
- ✅ **Documentation claims**: 599+ smoke tests exist project-wide
- ❌ **Discovery broken**: `pytest --collect-only -m smoke` crashes with Bus error
- ❌ **Enumeration impossible**: Can't get reliable count or list

## Root Cause

Dependent on ChromaDB/numpy Bus error issue (#XXX). The import crash prevents pytest from collecting tests that have smoke markers.

## Proposed Solutions

### Option 1: Fix Import Issues (Preferred)

- Resolve ChromaDB/numpy compatibility (see issue #XXX)
- Once imports work, pytest collection should work normally

### Option 2: Alternative Discovery Methods

- **Static analysis**: Parse test files for `@pytest.mark.smoke` markers
- **Import isolation**: Lazy loading or optional imports for problematic dependencies
- **Separate discovery**: Run discovery in isolated environment

### Option 3: Hybrid Approach

- Use working script for execution (`./scripts/run_tests.sh smoke`)
- Use alternative method for discovery/enumeration
- Combine for complete smoke test management

## Implementation Ideas

### Static Analysis Discovery

```python
def find_smoke_tests_static():
    """Find smoke tests by parsing files, not importing"""
    # Parse .py files for @pytest.mark.smoke
    # Return list without importing modules
```

### Import Isolation

```python
def safe_test_discovery():
    """Discover tests with import error handling"""
    # Try pytest collection
    # Fall back to static analysis if imports fail
```

## Success Criteria

- [ ] Reliable count of all smoke tests in project
- [ ] List of all smoke-marked test files and functions
- [ ] Discovery works regardless of import issues
- [ ] Integration with CI for smoke test coverage validation

## Priority

**Low** - This is primarily a "nice to have" for better visibility and management. The core functionality (running smoke tests) already works via `./scripts/run_tests.sh smoke`.

## Dependencies

- **Blocked by**: ChromaDB Bus error issue (#XXX)
- **Alternative**: Can implement static analysis approach independently

## Estimated Effort

- **Option 1** (fix imports): Depends on ChromaDB issue resolution
- **Option 2** (static analysis): 2-4 hours
- **Option 3** (hybrid): 1-2 hours

## Files Involved

- `scripts/run_smoke_tests.py` (current discovery logic)
- `pytest.ini` (smoke marker configuration)
- Test files throughout project with `@pytest.mark.smoke`

## Future Benefits

- Better smoke test coverage reporting
- Automated smoke test validation
- Integration with advanced CI/CD workflows
- Smoke test metrics and trends

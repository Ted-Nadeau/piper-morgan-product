# TEST-SMOKE-BUG-BUS: Smoke test collection fails with ChromaDB/numpy Bus error on macOS

**Title**: Smoke test collection fails with ChromaDB/numpy Bus error on macOS
**Labels**: bug, testing, high-priority
**Priority**: High

## Problem

Pytest collection of smoke tests crashes with a Bus error due to ChromaDB/numpy compatibility issues on macOS.

## Current Behavior

```bash
python -m pytest -m smoke --collect-only
# Results in: Fatal Python error: Bus error
```

The error trace shows:

- numpy/linalg/linalg.py line 561 in inv
- ChromaDB embedding functions import chain
- Affects test discovery and execution

## Impact

- **Blocks 599+ smoke tests**: Cannot discover or run smoke-marked tests
- **Prevents CI integration**: Can't reliably collect tests for automation
- **Manual workaround exists**: `./scripts/run_tests.sh smoke` works (1s execution)

## Investigation Needed

1. **ChromaDB version compatibility**: Check if newer/older versions resolve the issue
2. **numpy version conflicts**: Investigate numpy version requirements
3. **macOS-specific issue**: Test on Linux/Windows environments
4. **Import isolation**: Consider lazy loading or optional imports

## Current Workaround

The smoke test script works fine:

```bash
./scripts/run_tests.sh smoke  # ✅ Works (1s execution)
```

## Expected Outcome

- Pytest collection should work without Bus errors
- All smoke-marked tests should be discoverable
- Enable proper CI integration of smoke tests

## Priority

**High** - This blocks the full smoke test infrastructure and CI integration.

## Files Involved

- `tests/unit/test_slack_components.py` (13 smoke tests found)
- `services/knowledge_graph/ingestion.py` (ChromaDB import)
- `scripts/run_smoke_tests.py` (discovery logic)

## Environment

- macOS (Bus error observed)
- Python 3.9+
- ChromaDB dependency chain
- numpy compatibility issue

# Agent Prompt: Systematic AsyncSessionFactory Import Cleanup

## Mission
Fix ALL incorrect AsyncSessionFactory import paths throughout the entire codebase. This is systematic debt cleanup - we finish what we start.

## Context
**Pattern Discovered**: Multiple incorrect import paths to AsyncSessionFactory from past incomplete refactor
- Phase 1 fixed: `async_session_factory` → `session_factory` (2 files)
- Phase 2 found: `connection.AsyncSessionFactory` → `session_factory.AsyncSessionFactory` (4+ instances)

**The Truth**: AsyncSessionFactory lives in `services/database/session_factory.py`

**PM Directive**: Inchworm Protocol - complete this subbranch before moving on

## Step 1: Comprehensive Codebase Audit

### Search for ALL AsyncSessionFactory Import Variants
```bash
cd /Users/xian/Development/piper-morgan

# Find ALL files importing AsyncSessionFactory (any variant)
grep -r "AsyncSessionFactory" . --include="*.py" | grep -v "__pycache__" | grep -v ".pyc"

# Specific wrong patterns to find:
grep -r "from services.database.async_session_factory" . --include="*.py"
grep -r "from services.database.connection" . --include="*.py" | grep AsyncSessionFactory
grep -r "import.*async_session_factory" . --include="*.py"

# Count total instances
grep -r "AsyncSessionFactory" . --include="*.py" | grep -v "__pycache__" | wc -l
```

### Categorize Findings
For each file found, determine:
- **CORRECT**: `from services.database.session_factory import AsyncSessionFactory` ✅
- **WRONG**: Any other import path ❌
- **File path**: Full path to file needing fix
- **Line number**: Exact line with wrong import

## Step 2: Systematic Fixes

### Fix ALL Wrong Imports
For each wrong import found:

1. **Show before state**:
```bash
grep -n "AsyncSessionFactory" [filepath]
```

2. **Make the fix**:
Replace wrong import with: `from services.database.session_factory import AsyncSessionFactory`

3. **Verify the fix**:
```bash
python -c "from [module.path] import *; print('Import OK')"
```

### Known Files to Fix (Minimum)
1. `test_api_degradation_integration.py` - 4 instances (already identified)
2. Any others found in audit

## Step 3: Verification

### Test Import Fixes
```bash
# Verify each fixed file imports correctly
for file in [list of fixed files]; do
    python -c "import sys; sys.path.insert(0, '.'); import $file" 2>&1 | head -5
done
```

### Run Integration Tests Again
```bash
# Full integration test suite
PYTHONPATH=. python -m pytest tests/integration/ -v

# Should now collect ALL tests without import errors
# Report actual pass/fail counts
```

### Run Performance Tests
```bash
# Verify performance tests still work
PYTHONPATH=. python -m pytest tests/performance/ -v
```

## Evidence Requirements

### Audit Report
```
Total AsyncSessionFactory References: [count]

CORRECT Imports (✅):
- [filepath:line] - from services.database.session_factory import AsyncSessionFactory

WRONG Imports Fixed (❌→✅):
- [filepath:line] - BEFORE: [wrong import]
- [filepath:line] - AFTER: from services.database.session_factory import AsyncSessionFactory
[repeat for all fixes]

Files Modified: [count]
Total Import Fixes: [count]
```

### Test Verification
```
Integration Tests:
Terminal Output:
[paste complete pytest output]

Status: [ALL_PASSING | SOME_FAILING | COLLECTION_ERRORS]
Count: X passed, Y failed, Z errors
Collection: [clean | still has issues]

Performance Tests:
Terminal Output:
[paste complete pytest output]

Status: [ALL_PASSING | SOME_FAILING]
Count: X passed, Y failed
```

## Success Criteria
- ✅ ALL AsyncSessionFactory imports audited
- ✅ ALL wrong imports fixed to use session_factory
- ✅ NO remaining import path errors
- ✅ Integration tests COLLECT without ModuleNotFoundError
- ✅ Tests execute (may fail assertions, but run)

## STOP Conditions
- If AsyncSessionFactory doesn't actually exist in session_factory.py
- If fixing imports reveals deeper architectural inconsistencies
- If "correct" import path is actually wrong

## The Inchworm Principle
We don't leave this subbranch until import debt is cleared. Every instance fixed. Every test collects. No half-measures.

Report complete audit findings and all fixes with terminal evidence.

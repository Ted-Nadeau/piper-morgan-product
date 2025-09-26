# Agent Prompt: Fix Import Path Errors

## Mission
Fix incorrect import paths in 2 files that reference `async_session_factory` when they should reference `session_factory`.

## Context from Phase 0

**The Problem**: Import path typo
- **Wrong**: `from services.database.async_session_factory import AsyncSessionFactory`
- **Right**: `from services.database.session_factory import AsyncSessionFactory`

**Files to Fix**:
1. `services/intent_service/llm_classifier_factory.py`
2. `tests/integration/test_pm034_e2e_validation.py`

**Actual File**: `services/database/session_factory.py` (exists and works correctly)

## Implementation Tasks

### 1. Verify Current State
```bash
# Confirm the wrong imports exist
grep "async_session_factory" services/intent_service/llm_classifier_factory.py
grep "async_session_factory" tests/integration/test_pm034_e2e_validation.py

# Confirm correct file exists
ls -la services/database/session_factory.py
```

### 2. Fix Import in llm_classifier_factory.py
```bash
# Show current import line
grep -n "from services.database" services/intent_service/llm_classifier_factory.py

# Make the fix (change async_session_factory → session_factory)
# Use str_replace or direct edit
```

### 3. Fix Import in test_pm034_e2e_validation.py
```bash
# Show current import line  
grep -n "from services.database" tests/integration/test_pm034_e2e_validation.py

# Make the fix (change async_session_factory → session_factory)
```

### 4. Verify Imports Work
```bash
# Test that fixed imports work
cd /Users/xian/Development/piper-morgan

# Verify llm_classifier_factory imports correctly
python -c "from services.intent_service.llm_classifier_factory import *; print('llm_classifier_factory imports OK')"

# Verify test file imports correctly
python -c "import sys; sys.path.insert(0, '.'); from tests.integration.test_pm034_e2e_validation import *; print('test imports OK')" 2>&1 | grep -v "DeprecationWarning"
```

### 5. Run Affected Tests
```bash
# Run test file to see if it now collects
PYTHONPATH=. python -m pytest tests/integration/test_pm034_e2e_validation.py --collect-only

# Run test to see execution results
PYTHONPATH=. python -m pytest tests/integration/test_pm034_e2e_validation.py -v
```

## Evidence Requirements

### For Each File Fixed

**File**: `services/intent_service/llm_classifier_factory.py`
```
Before:
from services.database.async_session_factory import AsyncSessionFactory

After:
from services.database.session_factory import AsyncSessionFactory

Import Verification:
[paste terminal output of import test]
```

**File**: `tests/integration/test_pm034_e2e_validation.py`
```
Before:
from services.database.async_session_factory import AsyncSessionFactory

After:
from services.database.session_factory import AsyncSessionFactory

Import Verification:
[paste terminal output of import test]

Test Collection:
[paste pytest --collect-only output]

Test Execution:
[paste pytest -v output]
```

## Success Criteria
- ✅ Both import statements corrected
- ✅ Python can import both files without ModuleNotFoundError
- ✅ Test file collects without errors
- ✅ Test executes (may fail assertions, but runs)

## STOP Conditions
- If files use AsyncSessionFactory in complex ways that break after import fix
- If there are other async_session_factory references we missed
- If the fix reveals deeper architectural issues

**Principle**: Surgical fix - change import path only, nothing else.

Report findings with full before/after terminal output.

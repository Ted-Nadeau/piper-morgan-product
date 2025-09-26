# Agent Prompt: Create Missing Mock Infrastructure

## Mission
Create `tests/mocks/mock_agents.py` with MockCoordinatorAgent and create_mock_agent_pool that tests expect but which never existed.

## Context from Phase 0
**Import attempts expecting**:
- `from tests.mocks.mock_agents import MockCoordinatorAgent, create_mock_agent_pool`

**Used in**:
- `tests/ui/test_pm033d_ui_integration.py`
- `tests/integration/test_pm033d_database_integration.py`

**Status**: File never existed (no git history)

## Implementation Tasks

### 1. Examine Test Requirements
```bash
# See how tests try to use these mocks
grep -A 10 "MockCoordinatorAgent" tests/ui/test_pm033d_ui_integration.py
grep -A 10 "create_mock_agent_pool" tests/ui/test_pm033d_ui_integration.py

grep -A 10 "MockCoordinatorAgent" tests/integration/test_pm033d_database_integration.py
grep -A 10 "create_mock_agent_pool" tests/integration/test_pm033d_database_integration.py
```

### 2. Check for Real Implementation Pattern
```bash
# Find actual CoordinatorAgent to understand interface
grep -r "class CoordinatorAgent" services/ --include="*.py"
grep -r "CoordinatorAgent" services/ --include="*.py" | head -20

# Find agent pool patterns
grep -r "agent.*pool" services/ --include="*.py"
grep -r "AgentPool" services/ --include="*.py"
```

### 3. Create Mock Infrastructure

**File**: `tests/mocks/mock_agents.py`

**Requirements**:
- MockCoordinatorAgent class matching actual CoordinatorAgent interface
- create_mock_agent_pool() function returning testable pool
- Minimal but functional mocks (don't over-engineer)

**Standards**:
- Use Python's `unittest.mock` or similar
- Make mocks predictable for testing
- Include docstrings explaining mock behavior

### 4. Create Package Structure
```bash
# Ensure tests/mocks is a proper package
mkdir -p tests/mocks
touch tests/mocks/__init__.py
```

## Verification Steps

After creating mocks:

```bash
# 1. Verify imports work
cd /Users/xian/Development/piper-morgan
python -c "from tests.mocks.mock_agents import MockCoordinatorAgent, create_mock_agent_pool; print('Import successful')"

# 2. Check if tests can now collect
PYTHONPATH=. python -m pytest tests/ui/test_pm033d_ui_integration.py --collect-only
PYTHONPATH=. python -m pytest tests/integration/test_pm033d_database_integration.py --collect-only

# 3. Run the tests (may fail on assertions, but should execute)
PYTHONPATH=. python -m pytest tests/ui/test_pm033d_ui_integration.py -v
PYTHONPATH=. python -m pytest tests/integration/test_pm033d_database_integration.py -v
```

## Evidence Requirements

### Report Format

**Mock Implementation**:
```
Created: tests/mocks/mock_agents.py

Classes:
- MockCoordinatorAgent: [brief description of interface]
- Functions provided: create_mock_agent_pool

Based on: [actual CoordinatorAgent from services/X/Y or inferred from tests]
```

**Import Verification**:
```
Terminal Output:
[paste Python import test result]

Status: [SUCCESS | FAILED]
```

**Test Collection**:
```
Terminal Output:
[paste pytest --collect-only output for both test files]

Status: [COLLECTS | STILL_FAILS]
```

**Test Execution**:
```
Terminal Output:
[paste pytest -v output]

Status: [X passed, Y failed | collection errors]
```

## Success Criteria
- ✅ `tests/mocks/mock_agents.py` exists with required classes
- ✅ Import statement works without errors
- ✅ Tests can collect (no ModuleNotFoundError)
- ✅ Tests execute (may fail assertions, but run)

## STOP Conditions
- If actual CoordinatorAgent interface is too complex to mock simply
- If tests require deep agent coordination logic (beyond mock scope)
- If mock creation requires architectural decisions

**Principle**: Create minimal viable mocks that make tests collectible and executable. Don't build the real implementation.

Report findings with full terminal output.

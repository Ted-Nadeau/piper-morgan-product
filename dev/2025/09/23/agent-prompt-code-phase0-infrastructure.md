# Agent Prompt: Infrastructure Verification for Test Dependencies

## Mission
Discover what `tests.mocks` and `services.database.async_session_factory` actually are (or were), so we can fix them correctly rather than guessing.

## Context
Testing Phase assessment revealed collection errors:
- Integration tests: missing `tests.mocks` module
- Performance tests: missing `services.database.async_session_factory`
- E2E tests: blocked by above dependencies

**Critical**: We need to know if these are deleted files we should restore, or missing implementations we should create.

## Investigation Tasks

### 1. Search for tests.mocks
```bash
# Check if it exists anywhere
find . -name "mocks.py" -o -name "mocks" -type d

# Check git history for deletion
git log --all --full-history -- "**/tests/mocks*"
git log --all --full-history -- "**/mocks.py"

# Check what tests are trying to import
grep -r "from tests.mocks" tests/ --include="*.py"
grep -r "from tests import mocks" tests/ --include="*.py"
grep -r "import tests.mocks" tests/ --include="*.py"
```

### 2. Search for async_session_factory
```bash
# Check if it exists in services/database/
ls -la services/database/
cat services/database/__init__.py 2>/dev/null | grep -i session

# Search for any session factory patterns
grep -r "async_session_factory" . --include="*.py"
grep -r "AsyncSessionFactory" . --include="*.py"
grep -r "session_factory" services/database/ --include="*.py"

# Check what's trying to import it
grep -r "from services.database.async_session_factory" . --include="*.py"
grep -r "from services.database import.*session" . --include="*.py"
```

### 3. Check Test Configuration
```bash
# See what conftest.py sets up
cat tests/conftest.py 2>/dev/null

# Check if there's a test requirements file
cat tests/requirements.txt 2>/dev/null
cat requirements-test.txt 2>/dev/null
```

## Evidence Format

### For tests.mocks
Report:
- **Status**: [EXISTS | DELETED | NEVER_EXISTED]
- **Location**: [path if exists]
- **Git History**: [last commit if deleted, or "no history found"]
- **Import Patterns**: [what tests expect to import]
- **Recommendation**: [restore from git | create new | other]

### For async_session_factory
Report:
- **Status**: [EXISTS | MISSING | WRONG_LOCATION]
- **Current Location**: [path if exists]
- **Import Attempts**: [what's trying to import it]
- **Actual Session Pattern**: [what services/database actually has]
- **Recommendation**: [move file | create | fix imports | other]

## Success Criteria
- Clear answer: Do we restore, create, or fix imports?
- No guessing about what these should contain
- Foundation for next phase (actual fixes)

## STOP Conditions
- If git history is corrupted/unavailable
- If the codebase has conflicting patterns (multiple session factories)
- If dependencies require complex architectural decisions

Report findings and wait for Phase 1 deployment decision.

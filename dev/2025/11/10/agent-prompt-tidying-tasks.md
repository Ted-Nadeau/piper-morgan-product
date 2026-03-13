# Code Agent Prompt: Tidying Tasks - Dead Code Removal & Test Cleanup

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements

---

## Task Overview

**Type**: Cleanup / Technical Debt
**Priority**: Medium (tidying after major work)
**Date**: November 10, 2025, post-Issues #262/#291
**Context**: After successful UUID migration, cleaning up dead code and pre-existing test issues

**Two Tasks**:
1. **Dead Code Removal**: Remove `alpha_migration_service.py` (identified during #262 work)
2. **Test Cleanup**: Fix pre-existing test database cleanup issues

**Goal**: Clean codebase, all tests passing reliably

---

## Task 1: Dead Code Removal

### Background

During Issue #262 (UUID Migration), the file `services/alpha_migration_service.py` was identified as dead code. This file was part of the old `alpha_users` table architecture which has now been merged into the main `users` table.

### File to Remove

**File**: `services/alpha_migration_service.py`

**Why It's Dead Code**:
- alpha_users table has been merged into users (Issue #262)
- AlphaUser model removed
- No references remain in codebase
- Functionality no longer needed

### Verification Steps

**Before Removal**:
```bash
# 1. Verify file exists
ls -l services/alpha_migration_service.py

# 2. Search for any imports or references
grep -r "alpha_migration_service" . --include="*.py" --exclude-dir=".git"
# Expected: 0 or very few references (only in dead code itself)

# 3. Check if imported anywhere
grep -r "from services.alpha_migration_service" . --include="*.py"
grep -r "import alpha_migration_service" . --include="*.py"
# Expected: 0 references (dead code)
```

### Removal Process

**If no references found** (expected):
```bash
# Archive first (don't just delete)
mkdir -p archive/dead-code/2025-11-10
mv services/alpha_migration_service.py archive/dead-code/2025-11-10/

# Document removal
cat > archive/dead-code/2025-11-10/README.md << 'EOF'
# Dead Code Archive - November 10, 2025

## Files Archived

### alpha_migration_service.py
- **Removed**: November 10, 2025
- **Reason**: alpha_users table merged into users (Issue #262)
- **Safe to Delete**: No references in codebase
- **Related Issue**: #262 (UUID Migration)

This service was part of the alpha_users table architecture which has been
superseded by the merged users table with is_alpha flag.
EOF

# Create commit
git add archive/dead-code/
git rm services/alpha_migration_service.py
git commit -m "chore: Archive dead alpha_migration_service.py

File no longer needed after alpha_users merge (Issue #262).
Archived to archive/dead-code/2025-11-10/ for reference.

Related: #262"
```

**If references found** (unexpected):
```bash
# Document findings
echo "Found references to alpha_migration_service:" > dead-code-analysis.txt
grep -r "alpha_migration_service" . --include="*.py" >> dead-code-analysis.txt

# Notify PM
# "⚠️ Found unexpected references to alpha_migration_service. Need PM decision on how to handle."
```

### Success Criteria - Task 1

- [ ] Verified file is dead code (no references)
- [ ] File archived (not just deleted)
- [ ] README documented reason for archival
- [ ] Commit created with proper message
- [ ] Codebase still works (tests pass)

---

## Task 2: Test Cleanup Issues

### Background

During Issue #262/#291 work, some pre-existing test issues were discovered:
1. **Duplicate Key Errors**: Some tests fail due to data from previous runs
2. **Test Database Cleanup**: Tests not cleaning up properly between runs

**These are NOT related to UUID migration** - they existed before.

**Goal**: Fix these so tests run cleanly every time.

### Investigation Phase

**Identify Problem Tests**:
```bash
# Run tests and identify failures
pytest tests/ -v --tb=short 2>&1 | tee test-output.txt

# Look for duplicate key errors
grep -i "duplicate key" test-output.txt
grep -i "IntegrityError" test-output.txt
grep -i "already exists" test-output.txt

# Document findings
```

### Common Test Cleanup Patterns

**Pattern 1: Test Leaves Data Behind**
```python
# Problem: Test creates data but doesn't clean up
def test_create_user():
    user = create_user(username="test_user")
    # ... test logic ...
    # MISSING: cleanup

# Solution: Add cleanup
def test_create_user():
    user = create_user(username="test_user")
    try:
        # ... test logic ...
    finally:
        db.delete(user)
        db.commit()
```

**Pattern 2: Fixture Doesn't Clean Up**
```python
# Problem: Fixture creates data but doesn't clean up
@pytest.fixture
def test_user():
    user = create_user(username="test_user")
    return user
    # MISSING: yield and cleanup

# Solution: Use yield for cleanup
@pytest.fixture
def test_user():
    user = create_user(username="test_user")
    yield user
    db.delete(user)
    db.commit()
```

**Pattern 3: Test Uses Fixed ID/Username**
```python
# Problem: Tests use same username, causing duplicates
def test_user_creation():
    user = create_user(username="test_user")  # Always same name

# Solution: Use unique names or UUID
from uuid import uuid4

def test_user_creation():
    username = f"test_user_{uuid4().hex[:8]}"  # Unique
    user = create_user(username=username)
```

**Pattern 4: Database Not Reset Between Tests**
```python
# Problem: Database state carries over between tests

# Solution: Add database cleanup fixture
@pytest.fixture(scope="function", autouse=True)
def clean_database():
    """Clean database before each test"""
    yield
    # Cleanup after test
    db.rollback()
    # Or: db.query(User).delete()
    # Or: db.execute("TRUNCATE TABLE users CASCADE")
```

### Implementation Steps

**Step 1: Identify Problem Tests** (30 minutes)
```bash
# Run full suite, capture failures
pytest tests/ -v --tb=short > test-failures.txt 2>&1

# Analyze failures
grep -B 5 "IntegrityError\|duplicate key" test-failures.txt > duplicate-errors.txt

# Count affected tests
cat duplicate-errors.txt | grep "FAILED" | wc -l
```

**Step 2: Fix High-Impact Tests** (1-2 hours)

Priority order:
1. Tests in critical paths (auth, database)
2. Tests that block other tests
3. Tests that fail intermittently

**For each failing test**:
```python
# 1. Identify the issue
# - Duplicate key? → Use unique identifiers
# - Data persists? → Add cleanup
# - Fixture issue? → Use yield pattern

# 2. Apply appropriate pattern (see above)

# 3. Verify fix
pytest tests/path/to/test_file.py::test_name -v

# 4. Document change in code comment
# Example:
def test_create_user():
    """Test user creation

    Note: Uses unique username to avoid duplicate key errors
    from multiple test runs.
    """
    username = f"test_user_{uuid4().hex[:8]}"
    ...
```

**Step 3: Add Database Cleanup Fixture** (30 minutes)

**File**: `tests/conftest.py`

```python
import pytest
from services.database.connection import get_db_session

@pytest.fixture(scope="function", autouse=True)
async def clean_database_after_test():
    """Ensure clean database state after each test"""
    yield
    # Cleanup after test completes
    async with get_db_session() as session:
        await session.rollback()
        # Optional: More aggressive cleanup for specific tables
        # await session.execute("DELETE FROM token_blacklist")
        # await session.commit()
```

**Step 4: Run Full Suite** (10 minutes)
```bash
# Verify all tests pass
pytest tests/ -v --tb=short

# Check for remaining issues
pytest tests/ -v 2>&1 | grep -i "duplicate\|IntegrityError"
# Expected: 0 matches
```

**Step 5: Document Changes** (10 minutes)

**Create**: `dev/2025/11/10/test-cleanup-report.md`

```markdown
# Test Cleanup Report - November 10, 2025

## Problem
Pre-existing test cleanup issues causing duplicate key errors and intermittent failures.

## Root Causes Identified
1. Tests using fixed usernames/IDs
2. Fixtures not cleaning up
3. Database state persisting between tests

## Fixes Applied
- [List of test files modified]
- [Number of tests fixed]
- [Cleanup fixtures added]

## Results
- Before: X tests failing
- After: All tests passing
- Success rate: 100%

## Patterns Established
- Use uuid4() for unique test data
- Use yield in fixtures for cleanup
- Add autouse cleanup fixture in conftest.py
```

### Success Criteria - Task 2

- [ ] Problem tests identified (list with counts)
- [ ] High-impact tests fixed (auth, database)
- [ ] Database cleanup fixture added
- [ ] Full test suite passes (100%)
- [ ] No duplicate key errors remain
- [ ] Cleanup report documented
- [ ] Commit created with proper message

---

## Combined Deliverables

**What PM Gets**:
1. ✅ Dead code archived (alpha_migration_service.py)
2. ✅ Test cleanup issues fixed
3. ✅ All tests passing reliably
4. ✅ Documentation for both tasks
5. ✅ Clean, tidy codebase

**Commits**:
```bash
# Commit 1: Dead code removal
git commit -m "chore: Archive dead alpha_migration_service.py

Related: #262"

# Commit 2: Test cleanup
git commit -m "fix: Resolve pre-existing test cleanup issues

- Add database cleanup fixture (autouse)
- Fix duplicate key errors in [X] tests
- Use unique identifiers for test data
- All tests now passing reliably

Fixes: [list of affected test files]"
```

---

## Timeline

**Task 1** (Dead Code): 30 minutes
- Verification: 10 min
- Archival: 10 min
- Commit: 10 min

**Task 2** (Test Cleanup): 2-3 hours
- Investigation: 30 min
- High-impact fixes: 1-2 hours
- Cleanup fixture: 30 min
- Verification: 10 min
- Documentation: 10 min
- Commit: 10 min

**Total**: 2.5-3.5 hours

---

## Safety & Verification

### Before Starting

- [ ] Read current state briefing
- [ ] Confirm PM wants both tasks done
- [ ] Verify git is clean (no uncommitted changes)

### During Work

- [ ] Archive (don't delete) dead code
- [ ] Test each fix individually
- [ ] Document reasoning in code comments
- [ ] Run tests frequently

### Before Completing

- [ ] Full test suite passing (pytest tests/ -v)
- [ ] Git commits have clear messages
- [ ] Documentation complete
- [ ] Session log written

---

## Stop Conditions

**Stop and ask PM if**:
- alpha_migration_service.py has unexpected references
- Test fixes require architectural changes
- Cleanup fixture causes other tests to fail
- More than 10 tests need fixes (scope creep)

---

## Communication

**Progress Updates**:
- After Task 1 complete: "Dead code archived, commit [hash]"
- After investigation: "Found X failing tests, plan to fix [list]"
- After Task 2 complete: "Test cleanup done, all tests passing"

**Final Report**:
```markdown
## Tidying Tasks Complete ✅

**Task 1: Dead Code Removal**
- ✅ alpha_migration_service.py archived
- Commit: [hash]

**Task 2: Test Cleanup**
- ✅ [X] tests fixed
- ✅ Database cleanup fixture added
- ✅ All tests passing (Y/Y)
- Commit: [hash]

**Session Log**: [link]
**Test Report**: [link]
```

---

## Resources

**PM's Request**: "Let's also have one of the agents remove or archive the dead code and let's address the pre-existing test cleanup issues. I am in a tidying mood."

**Context**: Post-Issue #262/#291 cleanup

**Template**: agent-prompt-template.md v10.2

---

**Execute**: Remove dead code, fix test cleanup issues, make codebase tidy! 🧹✨

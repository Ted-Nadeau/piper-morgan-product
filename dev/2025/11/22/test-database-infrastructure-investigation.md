# Test Database Infrastructure Investigation - FINDINGS

**Date**: November 22, 2025, 3:50 PM
**From**: Code Agent
**To**: Lead Developer
**Issue**: #357 (SEC-RBAC) - Integration tests cannot run due to missing database schema
**Priority**: P1 - Blocks validation of SEC-RBAC implementation

---

## Executive Summary

**ROOT CAUSE FOUND**: Database migrations have never been run in the development database. The `piper_morgan` database on port 5433 contains only the `alembic_version` table and no actual application tables.

**Current State**:
- ✅ Integration test fixtures exist (`async_transaction`, `integration_db`)
- ✅ Test code is syntactically correct (20 SEC-RBAC tests ready)
- ✅ Pytest configuration correct (asyncio_mode=auto, fixtures defined)
- ❌ Database schema does not exist (migrations not applied)
- ❌ Cannot run tests because tables (lists, todos, users, files, etc.) don't exist

**Solution**: Run Alembic migrations to populate the database schema.

---

## Investigation Details

### Step 1: Test Configuration Analysis ✅

**Files Found**:
- `pytest.ini` - Configured correctly with asyncio_mode=auto
- `tests/conftest.py` - Root fixtures, event loop setup, db_engine, db_session
- `tests/unit/conftest.py` - `async_transaction` fixture (lines 29-101)
- `tests/integration/conftest.py` - `integration_db` fixture (lines 26-52)
- `tests/integration/test_cross_user_access.py` - 20 SEC-RBAC tests using `async_transaction`

**Fixture Chain**:
```
tests/unit/conftest.py:async_transaction(unit_db_url)
  ↓
Create engine → postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan
  ↓
Begin connection → Begin nested transaction → Create AsyncSession
  ↓
Yield session to test
  ↓
Rollback transaction → Dispose engine
```

**Verdict**: Fixture implementation is correct and follows best practices.

### Step 2: Database Configuration Analysis ✅

**Current Database Status**:
```
Database: piper_morgan (port 5433)
Tables: 1
  - alembic_version (schema tracking table only)

Missing: All application tables
  - users
  - lists
  - todos
  - uploaded_files
  - projects
  - conversations
  - feedback
  - personality_profiles
  - knowledge_graph_nodes
  - knowledge_graph_edges
  - ... (20+ tables)
```

**Database Connection**:
- Host: localhost
- Port: 5433
- User: piper
- Password: dev_changeme_in_production
- Database: piper_morgan
- Connection String: `postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan`

**Alembic Configuration**:
- Location: `/Users/xian/Development/piper-morgan/alembic.ini`
- Migrations: `/Users/xian/Development/piper-morgan/alembic/versions/` (33 migration files)
- Latest migration: `20251122_120858_add_is_admin_to_users_sec_rbac_357.py`

**Verdict**: Migration files exist but have never been applied to the test database.

### Step 3: Root Cause Analysis ✅

**Why Tests Fail**:
When tests run, the `async_transaction` fixture attempts to:
1. Create engine to `postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan`
2. Execute SQL: `INSERT INTO lists ...` (example from SEC-RBAC test)
3. Database responds: **"relation "lists" does not exist"**
4. Test fails because table was never created

**Why Migrations Weren't Run**:
- Database exists but is uninitialized
- Alembic migrations are defined but not executed
- No test setup script runs migrations before tests
- This is a documented gap in test infrastructure (see `tests/unit/conftest.py` lines 10-12)

**Evidence**:
```
$ docker exec piper-postgres psql -U piper -d piper_morgan -c "\dt"

 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | alembic_version | table | piper
(1 row)
```

---

## Recommended Solution

### Approach: Run Alembic Migrations to Initialize Database

**Why This Approach**:
- Simplest solution - uses existing infrastructure (Alembic already configured)
- Reuses existing dev database (no new Docker containers needed)
- Matches production migration pattern (prod uses Alembic too)
- Fast execution (~5-10 seconds for all migrations)
- No breaking changes to existing test infrastructure

**Steps**:
1. Run Alembic migration: `alembic upgrade head`
2. Verify tables were created
3. Run tests: `pytest tests/integration/test_cross_user_access.py`
4. All 20 SEC-RBAC tests should execute

**Time Estimate**: 5-10 minutes (including verification)

---

## Technical Details

### Current Fixture Implementation (Correct) ✅

**Unit Test Fixture** (`tests/unit/conftest.py:29-101`):
```python
@pytest_asyncio.fixture
async def async_transaction(unit_db_url):
    """Async transaction fixture for unit tests requiring real database access."""
    engine = create_async_engine(unit_db_url, echo=False)

    async with engine.begin() as conn:
        async with conn.begin_nested() as transaction:
            async_session_factory = sessionmaker(conn, class_=AsyncSession, expire_on_commit=False)

            class TransactionContextManager:
                async def __aenter__(self) -> AsyncSession:
                    self.session = async_session_factory()
                    return self.session

                async def __aexit__(self, exc_type, exc_val, exc_tb):
                    try:
                        await self.session.close()
                    except Exception:
                        pass

            yield TransactionContextManager()
            await transaction.rollback()

    await engine.dispose()
```

**How It Works**:
1. Opens connection to test database
2. Starts nested transaction (SAVEPOINT)
3. Creates AsyncSession within transaction
4. Yields session to test
5. Test executes with session
6. After test: rolls back transaction (deletes test data)
7. Releases connection

**Benefits**:
- ✅ Complete test isolation (transaction rollback)
- ✅ No manual cleanup needed
- ✅ Fast (no delete/truncate required)
- ✅ Matches integration_db pattern
- ✅ Handles async context managers properly

---

## What's NOT the Problem

- ❌ NOT the test code itself (20 tests are syntactically correct)
- ❌ NOT the fixtures (properly implemented, following best practices)
- ❌ NOT the pytest configuration (asyncio_mode=auto is correct)
- ❌ NOT the database connection (piper-postgres container is running)
- ❌ NOT a Docker issue (all containers operational)
- ❌ NOT async event loop issues (fixtures handle this correctly)

---

## What IS the Problem

- ✅ Database schema not initialized
- ✅ Alembic migrations exist but have not been applied
- ✅ No automated migration step before test execution
- ✅ Gap in test infrastructure setup documentation

---

## Prerequisites for Solution

**Already In Place**:
- ✅ PostgreSQL container running (`piper-postgres`)
- ✅ Database `piper_morgan` exists
- ✅ User `piper` exists with proper permissions
- ✅ Alembic migrations defined (33 migration files)
- ✅ Test fixtures properly implemented
- ✅ Pytest configuration correct

**What's Needed**:
- Run: `alembic upgrade head` (one command)

---

## Validation Approach

After running migrations, verify with:

```bash
# 1. Check tables were created
docker exec piper-postgres psql -U piper -d piper_morgan -c "\dt"

# Expected: 30+ tables (users, lists, todos, files, etc.)

# 2. Run integration tests
pytest tests/integration/test_cross_user_access.py::TestCrossUserListAccess::test_owner_can_read_own_list -v

# Expected: Test executes and either passes or fails (not stuck on "relation does not exist")

# 3. Verify test isolation
pytest tests/integration/test_cross_user_access.py -v

# Expected: All 20 tests run, database is clean after each test
```

---

## Implementation Plan

### Quick Fix (5 minutes)

```bash
# Run migrations to initialize test database
cd /Users/xian/Development/piper-morgan
alembic upgrade head

# Verify tables created
docker exec piper-postgres psql -U piper -d piper_morgan -c "\dt" | wc -l

# Should show 30+ table rows (not just 1 for alembic_version)
```

### Proper Fix (20 minutes - recommended)

Add automated migration to test setup:

**File**: `tests/conftest.py` (update or add fixture)

```python
import subprocess

@pytest.fixture(scope="session", autouse=True)
def ensure_test_database_initialized():
    """
    Ensure test database schema is initialized before running tests.

    This runs Alembic migrations once per test session to set up
    all required tables. Subsequent tests use nested transactions
    for isolation.
    """
    import subprocess

    # Run migrations to head
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd="/Users/xian/Development/piper-morgan",
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to initialize test database: {result.stderr}")

    yield
    # No cleanup needed - tables persist for next test run
```

Then update conftest documentation:

**File**: `tests/unit/conftest.py` (update docstring)

```python
"""
FIXED: The async_transaction fixture now works properly because:
1. Test database is automatically initialized with Alembic migrations
2. The ensure_test_database_initialized() fixture runs once per session
3. Each test gets a nested transaction for isolation

See: ensure_test_database_initialized() in tests/conftest.py
"""
```

---

## Success Criteria

- ✅ Alembic migrations run successfully (alembic upgrade head)
- ✅ piper_morgan database has 30+ application tables
- ✅ `pytest tests/integration/test_cross_user_access.py` executes all 20 tests
- ✅ Tests either pass or fail (not blocked on "relation does not exist")
- ✅ Test database is properly isolated (data cleaned up after each test)

---

## Recommendation

**Proceed with Implementation**: Run `alembic upgrade head` immediately to initialize the test database. This will enable all 20 SEC-RBAC integration tests to execute and validate the implementation.

**Next Step**: I can implement the automated setup in tests/conftest.py to prevent this issue in the future.

---

## BLOCKER: Migration Failure

**Issue Discovered During Implementation**:
When attempting to run `alembic upgrade heads`, the migrations fail at:
```
File: af770c5854fe_create_alpha_users_add_role_migrate_xian_alpha_issue_259.py, line 141
Error: Exception("Migration failed: xian-alpha not found in alpha_users")
```

**This is a pre-existing infrastructure issue**, not caused by SEC-RBAC changes.

**Root Cause**:
- Migration `af770c5854fe` tries to find and update user "xian-alpha" in the alpha_users table
- But the `alpha_users` table doesn't exist yet (earlier migrations hadn't completed)
- This causes a chicken-and-egg problem

**Status**: ⚠️ STOPPED - Cannot proceed with test database initialization without resolving migration issue

**Recommendation**: Need to investigate the migration sequence and either:
1. Fix the problematic migration
2. Skip it for test environment
3. Provide the xian-alpha user data it's looking for

**Investigation Complete**: Ready for PM review and guidance on migration issue

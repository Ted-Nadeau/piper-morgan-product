# Test Database Infrastructure Setup - Investigation & Implementation

**Date**: November 22, 2025, 3:42 PM
**From**: Lead Developer
**To**: Code Agent
**Priority**: P1 (Blocks integration test execution)
**Type**: Infrastructure Side Quest
**Estimated Time**: 60-90 minutes

---

## Mission

Investigate why integration tests cannot run due to missing test database infrastructure, then implement proper test database setup so that all 20 SEC-RBAC integration tests can execute.

**Current Problem**: Integration tests exist but cannot run because test database tables don't exist.

**Goal**: Enable `pytest tests/integration/` to run successfully with proper database setup.

---

## STOP: Track This Work in Beads First

Before starting investigation, create a beads issue to track this work:

```bash
# Create the tracking issue
bd create "TEST-DB: Set up integration test database infrastructure" \
  --type task \
  --priority P1 \
  --estimate "90m"

# Get the issue ID (e.g., piper-morgan-abc123)
# Use that ID in all commits for this work
```

**Commit Pattern**: `fix(TEST-DB #<beads-id>): <description>`

---

## Context

**What We Know**:
- ✅ Integration test code exists: `tests/integration/test_cross_user_access.py`
- ✅ Test fixtures exist: `async_transaction` fixture in conftest.py
- ✅ 20 test cases written and syntactically correct
- ❌ Tests cannot run: "test database infrastructure (tables) doesn't exist"
- ❌ Database schema not initialized in test environment

**Standard Practice**: Integration tests should:
1. Connect to a test database (isolated from dev/prod)
2. Run migrations to create schema
3. Execute tests with clean transactions
4. Rollback after each test

**Our Setup**: Unknown - needs investigation

---

## Phase 1: Investigation (30 minutes)

### Step 1.1: Find Current Test Configuration (10 min)

**Use Serena to locate test infrastructure files**:

```bash
# Find pytest configuration
mcp__serena__find_file("pytest.ini", ".")
mcp__serena__find_file("conftest.py", ".")
mcp__serena__find_file("pyproject.toml", ".")

# Find test fixtures
mcp__serena__search_for_pattern(
  substring_pattern="async_transaction",
  relative_path="tests",
  restrict_search_to_code_files=true
)

# Find database session setup
mcp__serena__search_for_pattern(
  substring_pattern="AsyncSession|SessionLocal|create_async_engine",
  relative_path="tests",
  restrict_search_to_code_files=true
)
```

**Read key files**:
- `pytest.ini` or `pyproject.toml` [tool.pytest.ini_options]
- `tests/conftest.py` (root test fixtures)
- `tests/integration/conftest.py` (if exists)
- Any test database setup scripts

**Document Findings**:
- Where is test database configured?
- What database URL is used for tests?
- Is there a test database fixture?
- Are migrations run before tests?

### Step 1.2: Check Existing Database Setup (10 min)

**Search for test database patterns**:

```bash
# Look for test database URL configuration
mcp__serena__search_for_pattern(
  substring_pattern="TEST_DATABASE_URL|DATABASE_URL.*test|test.*database",
  relative_path=".",
  restrict_search_to_code_files=false
)

# Look for Alembic test configuration
mcp__serena__search_for_pattern(
  substring_pattern="alembic.*upgrade|run_migrations",
  relative_path="tests",
  restrict_search_to_code_files=true
)

# Check for Docker test database
mcp__serena__find_file("docker-compose.test.yml", ".")
mcp__serena__find_file("docker-compose.yml", ".")
```

**Check if test database exists**:
```bash
# Try to connect to test database
docker ps | grep postgres
docker exec -it piper-postgres psql -U piper -l
```

**Document Findings**:
- Does a test database exist?
- Is it the same as dev database or separate?
- What's the connection string?

### Step 1.3: Understand Current async_transaction Fixture (10 min)

**Read the fixture implementation**:
```bash
mcp__serena__find_symbol(
  name_path_pattern="async_transaction",
  relative_path="tests",
  include_body=true
)
```

**Analyze**:
- Does it create database schema?
- Does it run migrations?
- Does it rollback transactions properly?
- What's missing?

**Create Investigation Report**:

File: `dev/2025/11/22/test-database-infrastructure-investigation.md`

Include:
- Current test database configuration (or lack thereof)
- What fixtures exist
- What's missing for tests to run
- Root cause of "tables don't exist" error
- Recommended solution approach

---

## Phase 2: Solution Design (15 minutes)

Based on investigation findings, choose the appropriate solution:

### Option A: Use Existing Dev Database with Test Schema

**When to use**: Dev database exists (piper-postgres on 5433), just need test schema

**Approach**:
1. Create separate test schema in existing database
2. Run migrations in test schema before tests
3. Clean up test schema after tests
4. Update fixtures to use test schema

**Pros**: Simple, reuses existing infrastructure
**Cons**: Test data in same DB as dev data (but different schema)

### Option B: Dedicated Test Database Container

**When to use**: Want complete isolation between test and dev

**Approach**:
1. Create `docker-compose.test.yml` with separate Postgres instance
2. Use different port (e.g., 5434)
3. Run migrations in test database
4. Update fixtures to connect to test database

**Pros**: Complete isolation, production-like
**Cons**: More Docker containers to manage

### Option C: In-Memory SQLite for Fast Tests

**When to use**: Want super-fast tests, no PostgreSQL-specific features needed

**Approach**:
1. Use SQLite in-memory database for tests
2. Update fixtures to use SQLite engine
3. Run migrations against SQLite

**Pros**: Fastest, no Docker needed
**Cons**: Won't test PostgreSQL-specific features (JSONB, GIN indexes)

**STOP: Get PM Approval for Chosen Approach**

Document your recommended approach in the investigation report and wait for PM approval before implementing.

---

## Phase 3: Implementation (30-45 minutes)

### Implementation for Option A (Recommended)

**Step 3.1: Create Test Database Setup Script (15 min)**

File: `tests/setup_test_db.py`

```python
"""
Test database setup utilities.
Handles migration running and schema setup for integration tests.
"""
import asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine
from services.config import settings

async def setup_test_database():
    """Run all Alembic migrations in test database."""
    # Get test database URL (use existing dev DB but different schema)
    test_db_url = settings.database_url.replace("/piper_morgan", "/piper_morgan_test")

    # Create test database if it doesn't exist
    engine = create_async_engine(test_db_url.replace("/piper_morgan_test", "/postgres"))
    async with engine.connect() as conn:
        await conn.execute("CREATE DATABASE piper_morgan_test IF NOT EXISTS")

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url.replace("+asyncpg", ""))
    command.upgrade(alembic_cfg, "head")

    return test_db_url

async def teardown_test_database():
    """Clean up test database (optional)."""
    pass  # Can drop tables or keep for debugging

if __name__ == "__main__":
    asyncio.run(setup_test_database())
```

**Step 3.2: Update conftest.py Fixtures (15 min)**

File: `tests/conftest.py`

Add or update these fixtures:

```python
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from tests.setup_test_db import setup_test_database

# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for entire test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Database setup fixture (runs once per test session)
@pytest.fixture(scope="session")
async def test_database_url(event_loop):
    """Set up test database with migrations."""
    db_url = await setup_test_database()
    yield db_url
    # Teardown happens here if needed

# Engine fixture
@pytest.fixture(scope="session")
async def test_engine(test_database_url):
    """Create async engine for test database."""
    engine = create_async_engine(test_database_url, echo=False)
    yield engine
    await engine.dispose()

# Session factory fixture
@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """Create session factory for tests."""
    return sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

# Transaction fixture (one per test)
@pytest.fixture
async def async_transaction(test_session_factory):
    """
    Provide a transactional database session for each test.
    All changes are rolled back after the test completes.
    """
    async with test_session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()  # Rollback after test
```

**Step 3.3: Update pytest Configuration (5 min)**

File: `pytest.ini` or `pyproject.toml`

Ensure async support is configured:

```ini
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "integration: Integration tests requiring database",
    "unit: Unit tests not requiring database"
]
```

**Step 3.4: Add Test Database Environment Variable (5 min)**

File: `.env.test` (create if doesn't exist)

```bash
# Test database configuration
DATABASE_URL=postgresql+asyncpg://piper:piper_password@localhost:5433/piper_morgan_test
ENVIRONMENT=test
```

Update test setup to load `.env.test` when running tests.

---

## Phase 4: Validation (15 minutes)

### Step 4.1: Run Database Setup Script

```bash
# Create test database and run migrations
python tests/setup_test_db.py

# Verify migrations ran
docker exec -it piper-postgres psql -U piper -d piper_morgan_test -c "\dt"

# Should see all tables (users, lists, todos, files, etc.)
```

### Step 4.2: Run Integration Tests

```bash
# Run all integration tests
pytest tests/integration/test_cross_user_access.py -v

# Expected: 20/20 tests should execute (may have failures, but should run)

# Run specific test class
pytest tests/integration/test_cross_user_access.py::TestCrossUserListAccess -v

# Run with verbose output
pytest tests/integration/ -vv -s
```

### Step 4.3: Verify Test Isolation

```bash
# Run tests twice - second run should have clean state
pytest tests/integration/test_cross_user_access.py -v
pytest tests/integration/test_cross_user_access.py -v

# Both runs should have identical results (tests are isolated)
```

### Step 4.4: Check Test Database State

```bash
# After tests run, check if data was cleaned up
docker exec -it piper-postgres psql -U piper -d piper_morgan_test -c "SELECT COUNT(*) FROM lists;"

# Should be 0 or very small (transactions rolled back)
```

---

## Deliverables

### 1. Investigation Report

File: `dev/2025/11/22/test-database-infrastructure-investigation.md`

**Contents**:
- Current state analysis
- Root cause of test failures
- Recommended solution
- Implementation plan

### 2. Test Database Setup Code

**Files Created/Modified**:
- `tests/setup_test_db.py` (new)
- `tests/conftest.py` (updated)
- `.env.test` (new)
- `pytest.ini` or `pyproject.toml` (updated)

### 3. Documentation

File: `docs/internal/development/testing/integration-test-setup.md`

**Contents**:
- How to set up test database
- How to run integration tests
- How test isolation works
- Troubleshooting common issues

### 4. Validation Report

File: `dev/2025/11/22/test-database-validation-report.md`

**Contents**:
- Test execution results
- How many tests pass/fail
- Evidence that database setup works
- Any remaining issues

---

## Success Criteria

✅ Test database infrastructure exists
✅ Migrations run successfully in test database
✅ Integration tests can execute (not stuck on "tables don't exist")
✅ Test transactions rollback properly (tests are isolated)
✅ All 20 SEC-RBAC integration tests run
✅ Documentation explains how to use test database
✅ Work tracked in beads with issue ID

---

## When to Use Serena or Subagents

### Use Serena for:
- Finding existing test configuration files
- Searching for database setup patterns
- Locating fixture implementations
- Understanding codebase structure

### Use Subagent (general-purpose) for:
- Complex investigation requiring multiple searches
- Comparing different test setup approaches
- If you need to explore multiple conftest.py files in different directories

### Do NOT use subagents for:
- Simple file reads
- Running pytest commands
- Creating new files
- Making straightforward edits

---

## Example Investigation Flow

1. **Use Serena** to find conftest.py files
2. **Read** conftest.py to understand current fixtures
3. **Use Serena** to search for database URL patterns
4. **Document** findings in investigation report
5. **Get PM approval** for solution approach
6. **Implement** solution (write new files, update fixtures)
7. **Test** with pytest commands
8. **Document** how it works
9. **Commit** with beads issue ID
10. **Report** completion with evidence

---

## STOP Conditions

- Investigation reveals breaking changes needed to existing tests → STOP, report to PM
- Test database requires production data migration → STOP, get PM guidance
- Docker setup requires new containers → STOP, get PM approval
- Integration tests reveal bugs in SEC-RBAC code → STOP, file separate bug issue

---

## Commit Strategy

All commits for this work should reference the beads issue ID:

```bash
git commit -m "fix(TEST-DB #<beads-id>): Add test database setup infrastructure"
git commit -m "docs(TEST-DB #<beads-id>): Document integration test database setup"
git commit -m "test(TEST-DB #<beads-id>): Verify integration tests can run"
```

---

## Final Report Format

When complete, provide a summary with:

**Investigation Findings**: What was missing, why tests couldn't run
**Solution Implemented**: Which option chosen and why
**Test Results**: How many tests run/pass/fail
**Evidence**: Terminal output from pytest run
**Next Steps**: Any remaining issues or follow-up work needed

---

**Authorization**: Approved as side quest during SEC-RBAC completion
**Expected Timeline**: 60-90 minutes
**Priority**: P1 (blocks validation of SEC-RBAC implementation)

Good luck! This is important infrastructure work that will benefit all future integration tests.

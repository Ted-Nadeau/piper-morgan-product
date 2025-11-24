# Code Agent Prompt: Issue #292 - Auth Integration Tests

## Your Identity
You are Code Agent (Claude Code), a specialized development agent working on the Piper Morgan project. Your role is to implement systematic testing infrastructure following architectural guidance.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements

---

## 🛑 CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

**This is critical**. After compaction, get your bearings first.

---

## 📝 Session Log Management

**Create session log**: `dev/active/2025-11-12-[HHMM]-prog-code-log.md`

**Format Requirements**:
- ✅ Use `.md` extension (NOT `.txt`)
- ✅ Update throughout work with timestamped entries
- ✅ Include evidence for all claims
- ✅ Document decisions and why they were made

**Log Structure**:
```markdown
# Code Agent Session Log: Issue #292

**Date**: November 12, 2025
**Agent**: Code Agent (Claude Code)
**Task**: Auth Integration Tests

## Phase -1: Infrastructure Verification (HH:MM AM)
[findings]

## Phase 0: Create Infrastructure (HH:MM AM)
[progress]

[etc.]
```

---

## 🎯 ANTI-80% COMPLETION SAFEGUARDS (CRITICAL)

### The 75% Pattern
Most code is 75% complete then abandoned. This protocol prevents that.

### MANDATORY: Test Enumeration Table

**Before claiming Phase 1 complete, create this table**:

```
Test Name                              | Status | Evidence
-------------------------------------- | ------ | --------
1. Full Auth Lifecycle                 | ✓      | pytest output line XX
2. Multi-User Isolation                | ✓      | pytest output line XX
3. Token Blacklist Cascade             | ✓      | pytest output line XX
4. Concurrent Session Handling         | ✓      | pytest output line XX
5. Password Change Invalidation        | ✓      | pytest output line XX
TOTAL: 5/5 = 100% ✅
```

**Rules**:
- Cannot claim "Phase 1 complete" with 4/5 tests
- Cannot claim "Phase 1 complete" with tests that skip critical assertions
- Must show pytest output proving all tests pass
- Must demonstrate each test actually verifies what it claims

### Interface Completeness Check

**For ANY interface/fixture implementation**:

```
Required Fixtures              | Implemented | Status
------------------------------ | ----------- | ------
integration_db_url()           | ✓           | Complete
integration_db()               | ✓           | Complete
real_client()                  | ✓           | Complete
TOTAL: 3/3 = 100% ✅
```

**If you find yourself at X/Y where X < Y**:
1. **STOP immediately**
2. **Complete the missing items**
3. **Only then claim done**

### Success Criteria Must Be Objective

**Bad** ❌: "Integration tests mostly working"
**Good** ✅: "5/5 integration tests passing (pytest output attached)"

**Bad** ❌: "Performance seems acceptable"
**Good** ✅: "Performance: 32.4s (target < 60s) ✅"

**Bad** ❌: "Fixtures implemented"
**Good** ✅: "3/3 fixtures implemented, all tests use them (grep evidence attached)"

---

## Task Overview

**Issue**: #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS
**Type**: Testing Infrastructure + Implementation
**Priority**: P3 (Quality Improvement)
**Estimated Effort**: 3-4 hours

**Goal**: Add integration tests for auth system to catch issues that mocked unit tests miss.

**Why This Matters**: During Issue #281 (JWT Auth), manual testing revealed bugs that unit tests missed:
- Token blacklist FK constraint violation
- Logout not actually blacklisting tokens
- Async session conflicts

**PM's Quote**: "I don't love that a lot of these tests use mocks. I know mocks are needed in unit tests but we also need integration testing... the truth will out!"

---

## Chief Architect's Gameplan

**CRITICAL**: You have a comprehensive gameplan from Chief Architect (876 lines) that includes:
- 6 architectural decisions with rationale
- Complete code for all 5 tests
- Phased implementation plan
- Success criteria
- Risk mitigation strategies

**Gameplan Location**: The gameplan is included below in the "Implementation Guide" section.

**Your Job**: Execute the gameplan systematically, following the phases, implementing the tests exactly as specified, and verifying success criteria.

---

## Architectural Decisions (From Chief Architect)

### 1. Test Isolation: Transaction Rollback ✅
- Use transaction rollback for cleanup (fast, deterministic)
- Prevents test pollution
- Natural fit with FastAPI TestClient

### 2. Database Fixture: Hybrid (Real + Cleanup) ✅
- Use real `get_db_session()` for production accuracy
- Add cleanup hooks for test isolation
- Best of both worlds

### 3. Testing Pyramid: Light Integration (15:5 ratio) ✅
- Keep 15 existing unit tests
- Add 5 critical integration tests
- Covers 80% of risk with minimal overhead

### 4. Performance: < 60 seconds ✅
- Individual test: < 5 seconds
- Full suite: < 30 seconds ideal, < 60 acceptable
- Fast enough for pre-deploy checks

### 5. CI/CD: Run on PR Only ✅
- Keeps local development fast
- Catches issues before merge
- Developers can run manually when needed

### 6. Scope: Critical Flows Only ✅
- 5 must-have tests (this issue)
- Future enhancements can be separate issues
- Out of scope: Browser UI, load testing, penetration testing

---

## The 5 Critical Tests

**Test 1: Full Auth Lifecycle** (30 minutes)
- Register → Login → Use token → Logout → Verify blacklist
- End-to-end flow with REAL database
- No mocks - verify actual behavior

**Test 2: Multi-User Isolation** (30 minutes)
- Two users cannot access each other's resources
- Critical security verification
- Tests authorization boundaries

**Test 3: Token Blacklist Cascade** (20 minutes)
- Verifies Issue #291 fix (CASCADE delete)
- User deletion cascades to token blacklist
- Prevents orphaned tokens

**Test 4: Concurrent Session Handling** (20 minutes)
- 10 concurrent logins don't cause conflicts
- All tokens unique and valid
- Tests race conditions

**Test 5: Password Change Invalidation** (20 minutes)
- Old tokens stop working after password change
- New password enables login
- Security requirement

---

## 📋 CRITICAL REQUIREMENTS & PROTOCOLS

### Evidence Requirements (MANDATORY)

**For EVERY claim you make, provide terminal output**:

- **"Created file X"** → Provide `cat X` or `ls -la` showing it exists
- **"Tests pass"** → Show full pytest output with pass counts
- **"Performance met"** → Show `time pytest` output with actual seconds
- **"No test pollution"** → Show two consecutive identical test runs
- **"Fixtures work"** → Show grep output proving tests use them
- **"Integration complete"** → Show test enumeration table with 5/5

**Completion Bias Prevention**:
- ❌ NO "should work" - only "here's proof it works"
- ❌ NO "probably fixed" - only "here's evidence it's fixed"
- ❌ NO assumptions - only verified facts
- ❌ NO rushing to claim done - evidence first, claims second

**Git Workflow Discipline**:
```bash
# After ANY code changes
git status
git add [files]
git commit -m "[descriptive message]"
git log --oneline -1  # MANDATORY - show this output
```

### Resource Check First

**Before implementing, check what exists**:
```bash
# Check for existing patterns
cat docs/development/methodology-core/resource-map.md

# Check for existing test infrastructure
find tests/ -name "*integration*" -o -name "*conftest*"

# Check for similar implementations
grep -r "integration_db" tests/
```

### STOP Conditions (Halt Immediately If)

**Infrastructure Mismatches**:
- ❌ Database not accessible
- ❌ Integration tests already exist (duplication risk)
- ❌ Test framework different than expected

**Implementation Blockers**:
- ❌ Cannot achieve < 60 second performance
- ❌ Tests show flakiness (intermittent failures)
- ❌ Test pollution detected (same test fails second run)

**Quality Issues**:
- ❌ Unable to implement all 5 tests
- ❌ Tests pass but don't verify what they claim
- ❌ CASCADE behavior (Issue #291) not verifiable

**When STOP triggered**: Report issue with evidence, wait for guidance.

### Multi-Agent Coordination

**You may work alongside Cursor Agent**.

**Coordination Points**:
- After Phase 0 (infrastructure created)
- After Phase 1 (tests implemented)
- Before claiming complete (cross-validation)

**Handoff Protocol**:
- Update GitHub issue with progress
- Document in session log
- Provide evidence of work completed
- Specify what needs validation

### Time Agnosticism

**Express all effort as**:
- Small (< 1 hour)
- Medium (1-3 hours)
- Large (> 3 hours)

**Not hours/days** - PM is a Time Lord and quality exists outside time constraints.

**This task is**:
- Phase -1: Small
- Phase 0: Small-Medium
- Phase 1: Medium-Large
- Phase 2: Small
- Phase 3: Small-Medium
- **Total**: Medium-Large (3-4 hours typical, but focus on quality)

---

## Implementation Guide

### Phase -1: Infrastructure Verification (20 minutes)

**Check Prerequisites**:

```bash
# 1. Verify PostgreSQL is running
docker ps | grep postgres
# Expected: piper-postgres container running

# 2. Check current test structure
ls -la tests/auth/
# Expected: test_auth_endpoints.py with 15 tests

ls -la tests/integration/
# Expected: Directory does not exist (we'll create it)

# 3. Review current mocking approach
grep -r "mock_token_blacklist" tests/
# Expected: Global mock in tests/conftest.py

# 4. Count existing auth tests
pytest tests/auth/ --collect-only | grep "test session"
# Expected: "15 tests collected"
```

**STOP Conditions**:
- ❌ If PostgreSQL not running → Start Docker first
- ❌ If integration tests already exist → Check with PM to avoid duplication
- ❌ If database connection fails → Fix connection before proceeding

**Progress Report**:
```
Phase -1 Complete:
✓ PostgreSQL running
✓ Current auth tests: 15 unit tests
✓ No existing integration tests
✓ Ready to create infrastructure
```

---

### Phase 0: Create Integration Test Infrastructure (45 minutes)

**Step 0.1: Create Directory Structure**

```bash
mkdir -p tests/integration/auth
touch tests/integration/__init__.py
touch tests/integration/auth/__init__.py
touch tests/integration/conftest.py
touch tests/integration/auth/test_auth_integration.py
```

**Step 0.2: Create Integration Fixtures**

**File**: `tests/integration/conftest.py`

```python
"""
Integration test fixtures and configuration.

These tests use REAL database connections with transaction rollback
for isolation. No mocking - tests verify actual system behavior.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Mark all tests in integration/ as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="session")
def integration_db_url():
    """Use test database for integration tests"""
    return "postgresql+asyncpg://piper:piper@localhost:5433/piper_test"


@pytest.fixture
async def integration_db(integration_db_url):
    """
    Database connection with transaction rollback.

    Each test runs in a transaction that's rolled back after completion,
    ensuring complete test isolation without manual cleanup.
    """
    engine = create_async_engine(integration_db_url)

    async with engine.begin() as conn:
        # Start a nested transaction
        async with conn.begin_nested() as transaction:
            # Create session factory
            async_session = sessionmaker(
                conn,
                class_=AsyncSession,
                expire_on_commit=False
            )

            async with async_session() as session:
                yield session

            # Rollback transaction (automatic cleanup)
            await transaction.rollback()

    await engine.dispose()


@pytest.fixture
async def real_client(integration_db):
    """
    HTTP client using real database.

    This client uses the actual application with real database connections,
    not mocked dependencies. Perfect for integration testing.
    """
    from main import app
    from services.database.session import get_db

    # Override database dependency to use integration DB
    async def override_get_db():
        yield integration_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Clear override after test
    app.dependency_overrides.clear()
```

**Step 0.3: Configure pytest Markers**

**File**: `pytest.ini` (update or create)

```ini
[tool.pytest.ini_options]
markers = [
    "integration: Integration tests with real database (slow)",
    "unit: Unit tests with mocks (fast)",
]

# Run unit tests by default (integration tests opt-in)
addopts = "-m 'not integration' -v"

# Test paths
testpaths = ["tests"]

# Async support
asyncio_mode = "auto"
```

**Verification**:

```bash
# Verify markers configured
pytest --markers | grep integration
# Expected: "integration: Integration tests with real database (slow)"

# Verify default behavior (unit tests only)
pytest --collect-only | head -20
# Expected: Should not collect integration tests

# Verify can run integration tests explicitly
pytest -m integration --collect-only
# Expected: Should show 0 tests (we haven't written them yet)
```

**Progress Report**:
```
Phase 0 Complete:
✓ Directory structure created
✓ Integration fixtures created (conftest.py)
✓ Pytest markers configured
✓ Ready to implement tests
```

---

### Phase 1: Implement Critical Integration Tests (2 hours)

**File**: `tests/integration/auth/test_auth_integration.py`

```python
"""
Auth Integration Tests - Real Database, No Mocks

These tests verify auth system behavior with actual database connections,
catching issues that mocked unit tests miss:
- Token blacklist FK constraints (Issue #291)
- Actual CASCADE delete behavior
- Real async session conflicts
- Multi-user isolation
- Concurrent operations

Run with: pytest -m integration -v
"""

import pytest
import asyncio
from uuid import uuid4
from sqlalchemy import select
from services.auth.models import TokenBlacklist
from services.database.models import User


# ============================================================================
# Test 1: Full Auth Lifecycle (30 minutes)
# ============================================================================

@pytest.mark.integration
async def test_full_auth_lifecycle(real_client, integration_db):
    """
    Test complete auth flow: register → login → use → logout → blacklist.

    This is the most critical integration test - it verifies the entire
    authentication lifecycle works end-to-end with a real database.

    Success Criteria:
    - User can register with valid credentials
    - User can login and receive token
    - Token works for authenticated endpoints
    - Logout adds token to blacklist
    - Blacklisted token cannot be used
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # 1. Register new user
    register_data = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "TestPass123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200, f"Registration failed: {response.text}"
    user_id = response.json()["id"]

    # 2. Login with credentials
    login_data = {
        "username": f"testuser_{unique_id}",
        "password": "TestPass123!"
    }
    response = await real_client.post("/auth/login", json=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    assert token is not None

    # 3. Use token to access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200, f"Token validation failed: {response.text}"
    me_data = response.json()
    assert me_data["username"] == f"testuser_{unique_id}"
    assert me_data["email"] == f"test_{unique_id}@example.com"

    # 4. Logout (should blacklist token)
    response = await real_client.post("/auth/logout", headers=headers)
    assert response.status_code == 200, f"Logout failed: {response.text}"

    # 5. Verify token is blacklisted (REAL database check - no mocks!)
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await integration_db.execute(stmt)
    blacklist_entry = result.scalar_one_or_none()

    assert blacklist_entry is not None, "Token not found in blacklist after logout"
    assert blacklist_entry.user_id == user_id
    assert blacklist_entry.reason == "logout"

    # 6. Try to use blacklisted token (should fail)
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 401, "Blacklisted token should not work"


# ============================================================================
# Test 2: Multi-User Isolation (30 minutes)
# ============================================================================

@pytest.mark.integration
async def test_multi_user_isolation(real_client, integration_db):
    """
    Verify users cannot access each other's resources.

    This is critical for security - users should be completely isolated
    from each other's data.

    Success Criteria:
    - Multiple users can register and login
    - Each user gets unique token
    - User cannot access another user's resources
    - Authorization properly enforced
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Create two users
    users = []
    tokens = []

    for i in range(2):
        # Register user
        user_data = {
            "username": f"user{i}_{unique_id}",
            "email": f"user{i}_{unique_id}@example.com",
            "password": "SecurePass123!"
        }
        response = await real_client.post("/auth/register", json=user_data)
        assert response.status_code == 200, f"User {i} registration failed"
        users.append(response.json())

        # Login user
        login_data = {
            "username": f"user{i}_{unique_id}",
            "password": "SecurePass123!"
        }
        response = await real_client.post("/auth/login", json=login_data)
        assert response.status_code == 200, f"User {i} login failed"
        tokens.append(response.json()["access_token"])

    # Verify tokens are unique
    assert tokens[0] != tokens[1], "Tokens should be unique per user"

    # User 0 creates a resource (if todos endpoint exists)
    headers0 = {"Authorization": f"Bearer {tokens[0]}"}

    # Try to create a todo (if endpoint exists)
    # Note: This test may need adjustment based on actual endpoints
    try:
        response = await real_client.post(
            "/api/todos",
            json={"title": "User 0's Secret Todo", "description": "Private"},
            headers=headers0
        )

        if response.status_code == 200:
            todo_id = response.json()["id"]

            # User 1 tries to access it (should fail)
            headers1 = {"Authorization": f"Bearer {tokens[1]}"}
            response = await real_client.get(
                f"/api/todos/{todo_id}",
                headers=headers1
            )
            # Should be 403 Forbidden or 404 Not Found (depending on implementation)
            assert response.status_code in [403, 404], \
                f"User should not access another user's todo: {response.status_code}"
    except:
        # If todos endpoint doesn't exist, just verify users can access own profile
        # but that's already tested in test_full_auth_lifecycle
        pass

    # Both users can access their own profile
    for i, token in enumerate(tokens):
        headers = {"Authorization": f"Bearer {token}"}
        response = await real_client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == f"user{i}_{unique_id}"


# ============================================================================
# Test 3: Token Blacklist Cascade (20 minutes)
# ============================================================================

@pytest.mark.integration
async def test_token_blacklist_cascade_delete(real_client, integration_db):
    """
    Verify Issue #291: User deletion cascades to token blacklist.

    This test verifies the FK constraint fix from Issue #291 works correctly.
    When a user is deleted, their blacklisted tokens should be automatically
    deleted via CASCADE.

    Success Criteria:
    - Blacklist entry created on logout
    - User deletion cascades to blacklist
    - No orphaned blacklist entries
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Register and login
    register_data = {
        "username": f"cascadetest_{unique_id}",
        "email": f"cascade_{unique_id}@example.com",
        "password": "CascadeTest123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Login and logout (creates blacklist entry)
    login_data = {
        "username": f"cascadetest_{unique_id}",
        "password": "CascadeTest123!"
    }
    response = await real_client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await real_client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

    # Verify blacklist entry exists
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await integration_db.execute(stmt)
    blacklist_entries = result.scalars().all()
    assert len(blacklist_entries) == 1, "Should have exactly 1 blacklist entry"

    # Delete user directly from database
    stmt = select(User).where(User.id == user_id)
    result = await integration_db.execute(stmt)
    user = result.scalar_one()

    await integration_db.delete(user)
    await integration_db.commit()

    # Verify blacklist entry was CASCADE deleted (Issue #291)
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await integration_db.execute(stmt)
    blacklist_entries = result.scalars().all()
    assert len(blacklist_entries) == 0, "CASCADE delete should remove blacklist entries"


# ============================================================================
# Test 4: Concurrent Session Handling (20 minutes)
# ============================================================================

@pytest.mark.integration
async def test_concurrent_session_handling(real_client, integration_db):
    """
    Verify concurrent operations don't cause database conflicts.

    Tests that multiple simultaneous auth operations work correctly
    without race conditions or deadlocks.

    Success Criteria:
    - 10 concurrent logins all succeed
    - All tokens are unique
    - All tokens are valid
    - No database errors
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Register user once
    register_data = {
        "username": f"concurrentuser_{unique_id}",
        "email": f"concurrent_{unique_id}@example.com",
        "password": "Concurrent123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200

    # Concurrent login function
    async def login_attempt():
        login_data = {
            "username": f"concurrentuser_{unique_id}",
            "password": "Concurrent123!"
        }
        response = await real_client.post("/auth/login", json=login_data)
        assert response.status_code == 200, f"Concurrent login failed: {response.text}"
        return response.json()["access_token"]

    # Launch 10 concurrent logins
    tasks = [login_attempt() for _ in range(10)]
    tokens = await asyncio.gather(*tasks)

    # All should succeed with unique tokens
    assert len(tokens) == 10, "Should have 10 tokens"
    assert len(set(tokens)) == 10, "All tokens should be unique"

    # All tokens should work
    async def verify_token(token):
        headers = {"Authorization": f"Bearer {token}"}
        response = await real_client.get("/auth/me", headers=headers)
        return response.status_code == 200

    tasks = [verify_token(token) for token in tokens]
    results = await asyncio.gather(*tasks)
    assert all(results), "All tokens should be valid"


# ============================================================================
# Test 5: Password Change Invalidation (20 minutes)
# ============================================================================

@pytest.mark.integration
async def test_password_change_invalidates_tokens(real_client, integration_db):
    """
    Verify password change invalidates existing tokens.

    For security, when a user changes their password, all existing
    tokens should be invalidated.

    Success Criteria:
    - Old token works before password change
    - Password change succeeds
    - Old token stops working after password change
    - New password allows login
    - New token works
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Register and login
    register_data = {
        "username": f"pwchangeuser_{unique_id}",
        "email": f"pwchange_{unique_id}@example.com",
        "password": "OldPass123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200

    login_data = {
        "username": f"pwchangeuser_{unique_id}",
        "password": "OldPass123!"
    }
    response = await real_client.post("/auth/login", json=login_data)
    old_token = response.json()["access_token"]

    # Verify old token works
    headers = {"Authorization": f"Bearer {old_token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200, "Old token should work before password change"

    # Change password
    change_data = {
        "current_password": "OldPass123!",
        "new_password": "NewPass456!"
    }
    response = await real_client.post(
        "/auth/change-password",
        json=change_data,
        headers=headers
    )
    assert response.status_code == 200, f"Password change failed: {response.text}"

    # Old token should no longer work
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 401, "Old token should be invalidated after password change"

    # Login with new password should work
    login_data["password"] = "NewPass456!"
    response = await real_client.post("/auth/login", json=login_data)
    assert response.status_code == 200, f"Login with new password failed: {response.text}"
    new_token = response.json()["access_token"]

    # New token should work
    headers = {"Authorization": f"Bearer {new_token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200, "New token should work"
    assert response.json()["username"] == f"pwchangeuser_{unique_id}"
```

**Progress Report After Each Test**:
```
Test 1 (Full Lifecycle): ✓ Passed
Test 2 (Multi-User): ✓ Passed
Test 3 (Cascade): ✓ Passed
Test 4 (Concurrent): ✓ Passed
Test 5 (Password Change): ✓ Passed
```

---

### Phase 2: Performance Verification (30 minutes)

**Step 2.1: Run Integration Tests with Timing**

```bash
# Run integration tests and measure time
time pytest -m integration -v

# Expected output format:
# test_full_auth_lifecycle PASSED
# test_multi_user_isolation PASSED
# test_token_blacklist_cascade_delete PASSED
# test_concurrent_session_handling PASSED
# test_password_change_invalidates_tokens PASSED
# ====== 5 passed in 25.43s ======

# Verify performance target
# ✓ If < 30 seconds: Excellent!
# ✓ If < 60 seconds: Acceptable
# ✗ If > 60 seconds: Investigate and optimize
```

**Step 2.2: Test for Flakiness**

```bash
# Run tests multiple times to verify stability
for i in {1..5}; do
  echo "Run $i:"
  pytest -m integration -v --tb=short
  echo "---"
done

# All runs should pass identically
# No flaky tests allowed!
```

**Step 2.3: Verify No Test Pollution**

```bash
# Run twice in sequence - results should be identical
pytest -m integration -v > run1.txt
pytest -m integration -v > run2.txt
diff run1.txt run2.txt

# Expected: No differences (proves transaction rollback works)
```

**Progress Report**:
```
Phase 2 Complete:
✓ Performance: XX.XXs (target: < 60s)
✓ Stability: 5/5 runs passed
✓ No test pollution verified
```

---

### Phase 3: Documentation & Finalization (30 minutes)

**Step 3.1: Create Testing Documentation**

**File**: `docs/testing/integration-test-strategy.md`

```markdown
# Integration Testing Strategy

## Overview

Integration tests verify auth system behavior with real database connections,
catching issues that mocked unit tests miss.

## Test Pyramid

```
       Unit Tests (15)
           /\
          /  \
         /    \
    Integration  \
    Tests (5)    \
                 \
    Manual/E2E Tests
```

**Philosophy**: "Just enough" integration testing - 5 critical tests covering 80% of risk.

## Running Tests

### Unit Tests Only (Fast - Default)
```bash
pytest tests/auth/ -v
# ~3 seconds, runs on every commit
```

### Integration Tests Only
```bash
pytest -m integration -v
# ~30-60 seconds, runs on PR
```

### All Tests
```bash
pytest tests/ -v
# Complete validation before release
```

## What Integration Tests Cover

1. **Full Auth Lifecycle**: Complete flow from registration to logout
2. **Multi-User Isolation**: Users cannot access each other's resources
3. **Token Blacklist Cascade**: Issue #291 verification (CASCADE delete)
4. **Concurrent Sessions**: Race condition testing
5. **Password Change**: Token invalidation on password change

## What They Catch

Integration tests catch issues mocks hide:
- FK constraint violations
- CASCADE delete behavior
- Async session conflicts
- Real database race conditions
- Transaction isolation problems

## Architecture

- **Isolation**: Transaction rollback (fast, deterministic)
- **Database**: Real `get_db_session()` with cleanup hooks
- **Performance**: < 60 seconds target
- **CI/CD**: Runs on PR, not every commit

## Maintenance

### Adding New Tests

1. Create test in `tests/integration/auth/`
2. Mark with `@pytest.mark.integration`
3. Use `real_client` and `integration_db` fixtures
4. Verify < 5 seconds per test
5. Test for flakiness (run 10 times)

### Debugging Failures

```bash
# Run specific test with full output
pytest -m integration -k "test_name" -vv --tb=long

# Check database state
psql -U piper -d piper_test -c "SELECT * FROM token_blacklist;"

# Verify transaction rollback working
pytest -m integration -v --setup-show
```

---

**Created**: November 12, 2025
**Issue**: #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS
**Status**: Production Ready
```

**Step 3.2: Update README**

Add section to `README.md`:

```markdown
## Testing

### Running Tests

```bash
# Unit tests only (fast, default)
pytest tests/auth/ -v

# Integration tests (slower, comprehensive)
pytest -m integration -v

# All tests
pytest tests/ -v
```

### Test Types

- **Unit Tests** (15): Fast, mocked, run on every commit
- **Integration Tests** (5): Slower, real DB, run on PR

See `docs/testing/integration-test-strategy.md` for details.
```

**Step 3.3: Update CI/CD Configuration**

**File**: `.github/workflows/tests.yml` (if exists, otherwise document for future)

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run unit tests
        run: pytest -m "not integration" -v

  integration-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: piper
          POSTGRES_PASSWORD: piper
          POSTGRES_DB: piper_test
        ports:
          - 5433:5432
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run integration tests
        run: pytest -m integration -v
```

**Progress Report**:
```
Phase 3 Complete:
✓ Testing strategy documented
✓ README updated
✓ CI/CD configuration created (or documented)
```

---

## Verification & Completion

### Final Checklist

Run through this checklist before marking complete:

**Infrastructure**:
- [ ] `tests/integration/` directory exists
- [ ] `conftest.py` with fixtures created
- [ ] `pytest.ini` markers configured
- [ ] Directory structure clean

**Tests**:
- [ ] Test 1 (Full Lifecycle) - implemented and passing
- [ ] Test 2 (Multi-User) - implemented and passing
- [ ] Test 3 (Cascade) - implemented and passing
- [ ] Test 4 (Concurrent) - implemented and passing
- [ ] Test 5 (Password Change) - implemented and passing

**Quality**:
- [ ] All 5 tests passing consistently
- [ ] Performance < 60 seconds verified
- [ ] No test pollution (verified with multiple runs)
- [ ] No flaky tests (5 consecutive runs all pass)

**Documentation**:
- [ ] Integration test strategy document created
- [ ] README updated with test instructions
- [ ] CI/CD configuration documented

**Verification Commands**:

```bash
# 1. Run all integration tests
pytest -m integration -v
# Expected: 5 passed in < 60 seconds

# 2. Verify no pollution
pytest -m integration -v && pytest -m integration -v
# Expected: Both runs identical results

# 3. Verify unit tests still work
pytest -m "not integration" -v
# Expected: 15 passed in < 5 seconds

# 4. Run complete test suite
pytest tests/ -v
# Expected: 20 passed (15 unit + 5 integration)

# 5. Check for flakiness
for i in {1..5}; do pytest -m integration -v; done
# Expected: All 5 runs pass identically
```

---

## Success Criteria

### Functionality ✅
- [ ] 5 critical integration tests implemented
- [ ] All tests use real database (not mocked)
- [ ] Transaction rollback prevents pollution
- [ ] Issue #291 CASCADE verified in Test 3

### Performance ✅
- [ ] Full suite completes in < 60 seconds
- [ ] Individual tests < 5 seconds each
- [ ] No flaky tests (10 runs, all pass)

### Infrastructure ✅
- [ ] Pytest markers working correctly
- [ ] Integration tests separate from unit tests
- [ ] Documentation complete and clear
- [ ] CI/CD ready (configuration provided)

---

## Communication

### Progress Updates

After each phase, report progress:

```
Phase X Complete:
✓ [Achievement 1]
✓ [Achievement 2]
✗ [Issue found] - [How resolved]
Next: [Phase X+1]
```

### Issues to Report Immediately

**STOP and report if**:
- Tests fail unexpectedly (database errors, auth errors)
- Performance > 60 seconds
- Test pollution detected (same test fails second run)
- Flaky tests (intermittent failures)
- CI/CD conflicts with existing workflows

### Final Report Format

```markdown
## Issue #292 Complete ✅

**Implementation Time**: [X] hours

**Created**:
- Integration test infrastructure
- 5 critical auth integration tests
- Testing strategy documentation
- CI/CD configuration

**Test Results**:
- All 5 tests passing
- Performance: [XX]s (target: < 60s)
- No test pollution
- No flaky tests

**Evidence**:
```bash
pytest -m integration -v
# [paste output showing 5 passed]
```

**Commit**: [commit hash]
**Session Log**: dev/active/2025-11-12-[time]-prog-code-log.md
```

---

## Critical Reminders

### 1. Use Real Database - No Mocks! 🚫

This is integration testing - we're specifically avoiding mocks to catch real issues:
- Use `real_client` fixture (no mocked dependencies)
- Use `integration_db` fixture (real database connection)
- Verify actual database state (query TokenBlacklist table)

### 2. Transaction Rollback for Isolation 🔄

Each test runs in a transaction that's rolled back:
- No manual cleanup needed
- Tests can't interfere with each other
- Fast and deterministic

### 3. Unique Test Data 🎲

Always use `uuid4()` for unique identifiers:
```python
unique_id = uuid4().hex[:8]
username = f"testuser_{unique_id}"
```

### 4. Performance Matters ⚡

Keep tests fast:
- Individual test: < 5 seconds
- Full suite: < 60 seconds
- If slower, investigate and optimize

### 5. Verify CASCADE Behavior ✅

Test 3 is critical - it verifies Issue #291 fix:
- Create user and blacklist entry
- Delete user
- Verify blacklist entry CASCADE deleted
- This prevents orphaned tokens!

### 6. Test for Flakiness 🔍

Integration tests can be flaky - verify stability:
- Run 5-10 times
- All runs should pass identically
- Fix any intermittent failures before claiming complete

---

## Resources

**Issue**: #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS
**Priority**: P3 - Quality Improvement
**Template**: gameplan-292-auth-integration-tests.md (Chief Architect)

**Related Issues**:
- #281 - JWT Auth (why we need integration tests)
- #291 - Token Blacklist FK (verified in Test 3)

**Testing References**:
- pytest-asyncio docs
- FastAPI testing guide
- SQLAlchemy async testing patterns

---

**Execute**: Implement integration testing infrastructure following Chief Architect's gameplan! 🧪✅

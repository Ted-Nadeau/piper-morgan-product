# Gameplan: Issue #292 - Auth Integration Testing Architecture

**Date**: November 12, 2025
**Issue**: #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS
**Priority**: P3 - Quality Improvement
**Estimated Effort**: 3-4 hours
**Agent**: Code (test implementation with architectural guidance)

---

## Architectural Decisions

Based on analysis of Piper Morgan's needs and the excellent weekend UUID migration success, here are my architectural recommendations:

### Decision 1: Test Isolation Strategy

**Selected**: **Option A - Transaction Rollback** ✅

**Rationale**:
- Auth tests don't need to verify commit behavior itself
- Transaction rollback is fast and deterministic
- Prevents test pollution completely
- Matches how FastAPI TestClient works naturally

**Implementation**:
```python
@pytest.fixture
async def integration_db():
    """Database fixture with automatic rollback"""
    async with engine.begin() as conn:
        async with conn.begin_nested() as transaction:
            yield conn
            await transaction.rollback()
```

---

### Decision 2: Database Fixture Design

**Selected**: **Option C - Hybrid (Real sessions with cleanup hooks)** ✅

**Rationale**:
- Uses real `get_db_session()` for production accuracy
- Adds cleanup hooks for test isolation
- Best of both worlds: real behavior + control

**Implementation**:
```python
@pytest.fixture
async def real_db_session():
    """Real session with cleanup tracking"""
    created_ids = []

    async with get_db_session() as session:
        # Track any created entities
        original_add = session.add
        def tracked_add(entity):
            created_ids.append(entity.id)
            return original_add(entity)
        session.add = tracked_add

        yield session

        # Cleanup in reverse order
        for entity_id in reversed(created_ids):
            # Cleanup logic
```

---

### Decision 3: Testing Pyramid Balance

**Selected**: **Option A - Light Integration (15:5 ratio)** ✅

**Rationale**:
- Start with 5 critical flows that cover 80% of risk
- Can expand later if valuable
- Maintains fast feedback loop
- Follows "just enough" principle

**The 5 Critical Integration Tests**:
1. Full auth lifecycle (login → use → logout → blacklist)
2. Multi-user isolation (users can't access others' data)
3. Token blacklist cascade (Issue #291 verification)
4. Concurrent session handling
5. Password change invalidation

---

### Decision 4: Performance Budget

**Selected**: **Option B - < 60 seconds** ✅

**Rationale**:
- Fast enough for pre-deploy checks
- Comprehensive enough to catch real issues
- Reasonable for developer patience
- Can optimize later if needed

**Performance Targets**:
- Individual test: < 5 seconds
- Full suite (5 tests): < 30 seconds ideal, < 60 seconds acceptable
- Database setup/teardown: < 10 seconds total

---

### Decision 5: CI/CD Strategy

**Selected**: **Option B - Run on PR only** ✅

**Rationale**:
- Keeps local development fast
- Catches issues before merge
- Developers can run manually when needed
- Balances speed with safety

**Implementation**:
```yaml
# .github/workflows/tests.yml
on:
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    # ... runs on every commit

  integration-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    # ... runs only on PR
```

---

### Decision 6: Scope Definition

**Selected**: **Critical Flows Only** ✅

**Must Have** (in this issue):
- ✅ Full auth lifecycle
- ✅ Multi-user isolation
- ✅ Token blacklist verification

**Nice to Have** (future issues if valuable):
- Token expiration timing
- Rate limiting (when implemented)
- API key rotation

**Out of Scope**:
- Browser UI testing
- Load testing
- Penetration testing

---

## Implementation Phases

### Phase -1: Infrastructure Verification (20 minutes)

**Check Prerequisites**:

```bash
# Verify test database available
docker ps | grep postgres

# Check current test structure
ls -la tests/auth/
ls -la tests/integration/  # Should not exist yet

# Review current mocking approach
grep -r "mock_token_blacklist" tests/

# Count existing auth tests
pytest tests/auth/ --collect-only | grep "test session"
# Expected: 15 tests
```

**STOP Conditions**:
- If no PostgreSQL available
- If integration tests already exist (avoid duplication)

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

```python
# tests/integration/conftest.py

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
    """Database connection with transaction rollback"""
    engine = create_async_engine(integration_db_url)

    async with engine.begin() as conn:
        # Start a transaction
        async with conn.begin_nested() as transaction:
            # Create session
            async_session = sessionmaker(
                conn, class_=AsyncSession, expire_on_commit=False
            )

            async with async_session() as session:
                yield session

            # Rollback transaction (cleanup)
            await transaction.rollback()

@pytest.fixture
async def real_client(integration_db):
    """HTTP client using real database"""
    from main import app
    from services.database.session import get_db

    # Override dependency to use integration DB
    async def override_get_db():
        yield integration_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Clear override
    app.dependency_overrides.clear()
```

**Step 0.3: Configure pytest markers**

```ini
# pytest.ini (update or create)

[tool.pytest.ini_options]
markers = [
    "integration: Integration tests with real database (slow)",
    "unit: Unit tests with mocks (fast)",
]

# Run unit tests by default
addopts = "-m 'not integration'"
```

---

### Phase 1: Implement Critical Integration Tests (2 hours)

**Test 1: Full Auth Lifecycle** (30 minutes)

```python
# tests/integration/auth/test_auth_integration.py

import pytest
from datetime import datetime
from services.auth.models import TokenBlacklist
from services.database.models import User

@pytest.mark.integration
async def test_full_auth_lifecycle(real_client, integration_db):
    """Test complete auth flow: register → login → use → logout → blacklist"""

    # 1. Register new user
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # 2. Login
    login_data = {
        "username": "testuser",
        "password": "TestPass123!"
    }
    response = await real_client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 3. Use token to access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    # 4. Logout
    response = await real_client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

    # 5. Verify token is blacklisted (REAL database check)
    blacklist_entry = await integration_db.query(TokenBlacklist).filter_by(
        token_id=token
    ).first()
    assert blacklist_entry is not None
    assert blacklist_entry.user_id == user_id

    # 6. Try to use blacklisted token (should fail)
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 401
```

**Test 2: Multi-User Isolation** (30 minutes)

```python
@pytest.mark.integration
async def test_multi_user_isolation(real_client, integration_db):
    """Verify users cannot access each other's resources"""

    # Create two users
    users = []
    tokens = []

    for i in range(2):
        # Register
        user_data = {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "password": "SecurePass123!"
        }
        response = await real_client.post("/auth/register", json=user_data)
        assert response.status_code == 200

        # Login
        login_data = {
            "username": f"user{i}",
            "password": "SecurePass123!"
        }
        response = await real_client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        tokens.append(response.json()["access_token"])

    # User 0 creates a resource
    headers0 = {"Authorization": f"Bearer {tokens[0]}"}
    response = await real_client.post(
        "/todos/create",
        json={"title": "User 0's Secret Todo"},
        headers=headers0
    )
    assert response.status_code == 200
    todo_id = response.json()["id"]

    # User 1 tries to access it (should fail)
    headers1 = {"Authorization": f"Bearer {tokens[1]}"}
    response = await real_client.get(
        f"/todos/{todo_id}",
        headers=headers1
    )
    assert response.status_code in [403, 404]  # Forbidden or Not Found

    # User 1 tries to delete it (should fail)
    response = await real_client.delete(
        f"/todos/{todo_id}",
        headers=headers1
    )
    assert response.status_code in [403, 404]
```

**Test 3: Token Blacklist Cascade** (20 minutes)

```python
@pytest.mark.integration
async def test_token_blacklist_cascade_delete(real_client, integration_db):
    """Verify Issue #291: User deletion cascades to blacklist"""

    # Register and login
    register_data = {
        "username": "cascadetest",
        "email": "cascade@example.com",
        "password": "CascadeTest123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Login and logout (creates blacklist entry)
    login_data = {
        "username": "cascadetest",
        "password": "CascadeTest123!"
    }
    response = await real_client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await real_client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

    # Verify blacklist entry exists
    blacklist_count = await integration_db.query(TokenBlacklist).filter_by(
        user_id=user_id
    ).count()
    assert blacklist_count == 1

    # Delete user directly from database
    user = await integration_db.query(User).filter_by(id=user_id).first()
    await integration_db.delete(user)
    await integration_db.commit()

    # Verify blacklist entry was CASCADE deleted (Issue #291)
    blacklist_count = await integration_db.query(TokenBlacklist).filter_by(
        user_id=user_id
    ).count()
    assert blacklist_count == 0  # CASCADE worked!
```

**Test 4: Concurrent Session Handling** (20 minutes)

```python
import asyncio

@pytest.mark.integration
async def test_concurrent_session_handling(real_client, integration_db):
    """Verify concurrent operations don't cause conflicts"""

    # Register user
    register_data = {
        "username": "concurrentuser",
        "email": "concurrent@example.com",
        "password": "Concurrent123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200

    # Concurrent login attempts
    async def login_attempt():
        login_data = {
            "username": "concurrentuser",
            "password": "Concurrent123!"
        }
        response = await real_client.post("/auth/login", json=login_data)
        return response.json()["access_token"]

    # Launch 10 concurrent logins
    tasks = [login_attempt() for _ in range(10)]
    tokens = await asyncio.gather(*tasks)

    # All should succeed with unique tokens
    assert len(tokens) == 10
    assert len(set(tokens)) == 10  # All unique

    # All tokens should work
    async def verify_token(token):
        headers = {"Authorization": f"Bearer {token}"}
        response = await real_client.get("/auth/me", headers=headers)
        return response.status_code == 200

    tasks = [verify_token(token) for token in tokens]
    results = await asyncio.gather(*tasks)
    assert all(results)  # All tokens valid
```

**Test 5: Password Change Invalidation** (20 minutes)

```python
@pytest.mark.integration
async def test_password_change_invalidates_tokens(real_client, integration_db):
    """Verify password change invalidates existing tokens"""

    # Register and login
    register_data = {
        "username": "pwchangeuser",
        "email": "pwchange@example.com",
        "password": "OldPass123!"
    }
    response = await real_client.post("/auth/register", json=register_data)
    assert response.status_code == 200

    login_data = {
        "username": "pwchangeuser",
        "password": "OldPass123!"
    }
    response = await real_client.post("/auth/login", json=login_data)
    old_token = response.json()["access_token"]

    # Verify old token works
    headers = {"Authorization": f"Bearer {old_token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200

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
    assert response.status_code == 200

    # Old token should no longer work
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 401

    # Login with new password should work
    login_data["password"] = "NewPass456!"
    response = await real_client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    new_token = response.json()["access_token"]

    # New token should work
    headers = {"Authorization": f"Bearer {new_token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200
```

---

### Phase 2: Performance Verification (30 minutes)

**Step 2.1: Add Performance Benchmarks**

```python
# tests/integration/auth/test_auth_performance.py

import time
import pytest

@pytest.mark.integration
@pytest.mark.benchmark
async def test_auth_operation_performance(real_client, integration_db):
    """Verify auth operations meet performance targets"""

    # Setup: Create user
    register_data = {
        "username": "perftest",
        "email": "perf@example.com",
        "password": "PerfTest123!"
    }
    await real_client.post("/auth/register", json=register_data)

    # Benchmark login
    start = time.perf_counter()
    for i in range(10):
        login_data = {
            "username": "perftest",
            "password": "PerfTest123!"
        }
        response = await real_client.post("/auth/login", json=login_data)
        assert response.status_code == 200
    login_time = time.perf_counter() - start

    # Should handle 10 logins in < 5 seconds
    assert login_time < 5.0
    print(f"10 logins: {login_time:.2f}s ({login_time/10:.3f}s per login)")

    # Get a token for validation tests
    response = await real_client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Benchmark token validation
    start = time.perf_counter()
    for i in range(100):
        response = await real_client.get("/auth/me", headers=headers)
        assert response.status_code == 200
    validation_time = time.perf_counter() - start

    # Should validate 100 tokens in < 5 seconds
    assert validation_time < 5.0
    print(f"100 validations: {validation_time:.2f}s ({validation_time*1000/100:.1f}ms per validation)")
```

**Step 2.2: Verify Suite Performance**

```bash
# Run integration tests with timing
time pytest tests/integration/auth/ -v

# Should complete in < 60 seconds
# Ideal: < 30 seconds
```

---

### Phase 3: Documentation & CI/CD Setup (30 minutes)

**Step 3.1: Create Testing Documentation**

```markdown
# docs/testing/integration-test-strategy.md

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
pytest tests/ -v --tb=short
# Complete validation before release
```

## Test Coverage

### Unit Tests (Mocked, Fast)
- Individual component behavior
- Error handling
- Input validation
- Business logic

### Integration Tests (Real DB, Slower)
1. Full auth lifecycle
2. Multi-user isolation
3. Token blacklist cascade
4. Concurrent operations
5. Password change invalidation

### Manual Tests
- UI/UX validation
- Browser compatibility
- Production smoke tests

## Performance Targets

- Individual integration test: < 5 seconds
- Full integration suite: < 60 seconds
- Unit test suite: < 5 seconds

## Database Strategy

Integration tests use transaction rollback for isolation:
- Each test runs in a transaction
- Automatic rollback after test
- No test pollution
- Fast cleanup
```

**Step 3.2: Update CI/CD Configuration**

```yaml
# .github/workflows/tests.yml

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
          pip install pytest pytest-asyncio
      - name: Run unit tests
        run: pytest tests/ -m "not integration" -v

  integration-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: piper
          POSTGRES_USER: piper
          POSTGRES_DB: piper_test
        ports:
          - 5433:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio
      - name: Run integration tests
        run: pytest tests/ -m integration -v
        env:
          DATABASE_URL: postgresql://piper:piper@localhost:5433/piper_test
```

---

### Phase Z: Completion & Verification (15 minutes)

**Final Checklist**:

- [ ] Integration test directory created
- [ ] 5 critical tests implemented and passing
- [ ] Performance < 60 seconds verified
- [ ] pytest markers configured
- [ ] CI/CD configuration updated
- [ ] Documentation created
- [ ] No test pollution (verified with multiple runs)

**Run Final Verification**:

```bash
# Run integration tests twice to verify no pollution
pytest -m integration -v
pytest -m integration -v  # Should pass identically

# Verify performance
time pytest -m integration -v

# Verify unit tests still work
pytest -m "not integration" -v

# Full test suite
pytest tests/ -v
```

**Create PR**:

```bash
git add -A
git commit -m "feat(#292): Add integration tests for auth system

- Create integration test infrastructure with transaction rollback
- Implement 5 critical auth flow tests
- Verify Issue #291 cascade behavior
- Add performance benchmarks
- Configure pytest markers for test separation
- Update CI/CD to run integration tests on PR
- Document testing strategy

Integration tests catch issues mocks miss:
- Token blacklist FK violations
- Concurrent session conflicts
- Cascade delete behavior
- Real database constraints

Performance: Suite runs in < 60 seconds

Fixes #292"

git push origin feature/292-auth-integration-tests
```

---

## Success Criteria

### Functionality ✅
- [ ] 5 critical integration tests passing
- [ ] Tests use real database (not mocked)
- [ ] Transaction rollback prevents pollution
- [ ] Issue #291 cascade verified

### Performance ✅
- [ ] Suite completes in < 60 seconds
- [ ] Individual tests < 5 seconds
- [ ] No flaky tests (10 runs, all pass)

### Infrastructure ✅
- [ ] Pytest markers working
- [ ] CI/CD configured correctly
- [ ] Documentation complete
- [ ] Separate from unit tests

---

## Risk Mitigation

**Test Flakiness**:
- Use explicit waits, not sleep
- Clean transaction boundaries
- Proper async handling

**Performance Issues**:
- Connection pooling configured
- Indexes verified
- Batch operations where possible

**Database Pollution**:
- Transaction rollback strategy
- Unique test data per run
- Cleanup hooks as backup

---

## ADR: Testing Architecture Decision

**Decision**: Hybrid integration testing with transaction rollback

**Status**: Accepted

**Context**: Auth system needs integration tests to catch issues mocks hide

**Decision Details**:
1. Transaction rollback for test isolation (fast, clean)
2. Real database sessions with cleanup hooks (production-like)
3. 5 critical tests covering 80% of risk (just enough)
4. < 60 second performance target (practical)
5. PR-only CI/CD execution (balanced)

**Consequences**:
- ✅ Catches real integration issues
- ✅ Fast enough for regular use
- ✅ Maintains test isolation
- ⚠️ Requires PostgreSQL for testing
- ⚠️ Slightly slower than pure unit tests

**Alternatives Considered**:
- Separate database per test: Too slow
- Truncate tables: Risk of pollution
- Only unit tests: Miss critical bugs

---

*Gameplan complete - Ready for implementation*

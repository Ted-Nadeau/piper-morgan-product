# Solution Guide: Fix Async Test Isolation in Auth Tests

**Problem**: Auth tests pass individually but fail when run together due to pytest-asyncio event loop + SQLAlchemy async connection pool conflicts.

**Goal**: All tests pass when run together: `pytest tests/auth/test_auth_endpoints.py -v`

**Time Estimate**: 1-2 hours

---

## Root Cause Analysis

### The Problem

```python
# Test 1 runs in Event Loop A
async def test_login():
    # Creates DB connection in Loop A
    async with db_session() as db:
        user = await db.execute(...)
    # Test passes ✅

# Test 2 runs in Event Loop B (pytest-asyncio creates new loop)
async def test_get_user():
    # Tries to use DB connection pool from Loop A
    # ERROR: Future attached to different loop ❌
```

**Why it happens**:
- pytest-asyncio creates new event loop per test (or per session)
- SQLAlchemy async connection pool created in one loop
- Subsequent tests try to use pool from different loop
- AsyncIO raises "Future attached to different loop"

---

## Solution Options (Try in Order)

### Option 1: Proper Fixture Scoping (Fastest - Try This First)

**Hypothesis**: Database engine/sessionmaker being reused across event loops.

**Fix**: Create fresh database connection per test.

#### Step 1: Update conftest.py Database Fixture

```python
# tests/conftest.py

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

@pytest_asyncio.fixture(scope="function")  # KEY: function scope, not session
async def db_engine():
    """Create fresh async engine per test"""
    from config import PIPER_CONFIG

    engine = create_async_engine(
        PIPER_CONFIG.database_url,
        echo=False,  # Reduce log noise
        pool_pre_ping=True,  # Verify connections
        pool_recycle=3600,
    )

    yield engine

    # Proper cleanup
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """Create fresh session per test"""
    async_session_factory = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_factory() as session:
        yield session
        # Session cleanup automatic with context manager
```

**Key Changes**:
1. `scope="function"` - New engine per test
2. Proper `await engine.dispose()` cleanup
3. Fresh sessionmaker per test

#### Step 2: Update Test Fixtures to Use db_session

```python
# tests/auth/test_auth_endpoints.py

@pytest_asyncio.fixture
async def test_user(db_session):
    """Create and cleanup test user"""
    from services.database.models import AlphaUser
    from services.auth.password_service import PasswordService

    ps = PasswordService()

    # Cleanup any existing
    result = await db_session.execute(
        select(AlphaUser).where(AlphaUser.email == "logintest@example.com")
    )
    existing = result.scalar_one_or_none()
    if existing:
        await db_session.delete(existing)
        await db_session.commit()

    # Create fresh user
    user = AlphaUser(
        username="login_test_user",
        email="logintest@example.com",
        password_hash=ps.hash_password("Test123!@#"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    yield user

    # Cleanup
    await db_session.delete(user)
    await db_session.commit()


async def test_login_success(async_client, test_user):
    """Test no longer needs manual DB operations"""
    response = await async_client.post(
        "/auth/login",
        json={
            "username": "login_test_user",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 200
    # Test user automatically cleaned up by fixture
```

**Test this**:
```bash
pytest tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_success -v
pytest tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_get_current_user -v
# Then together:
pytest tests/auth/test_auth_endpoints.py -v
```

---

### Option 2: Event Loop Fixture (If Option 1 Fails)

**Hypothesis**: pytest-asyncio event loop policy causing issues.

**Fix**: Explicit event loop per test with proper cleanup.

```python
# tests/conftest.py

import asyncio
import pytest_asyncio

@pytest_asyncio.fixture(scope="function")
async def event_loop():
    """Create fresh event loop per test"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop

    # Proper cleanup
    loop.close()
```

**Configure pytest-asyncio**:
```ini
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # or "strict"
```

---

### Option 3: Database Connection Per Test (If Option 1-2 Fail)

**Hypothesis**: Connection pool itself is the issue.

**Fix**: Don't use connection pooling in tests.

```python
# tests/conftest.py

@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """Create fresh async engine with no pooling"""
    from config import PIPER_CONFIG

    engine = create_async_engine(
        PIPER_CONFIG.database_url,
        echo=False,
        poolclass=NullPool,  # KEY: Disable pooling for tests
    )

    yield engine

    await engine.dispose()
```

---

### Option 4: Monkeypatch get_db_session (Nuclear Option)

**Hypothesis**: Application code database singleton causing issues.

**Fix**: Replace database connection in tests completely.

```python
# tests/conftest.py

@pytest_asyncio.fixture(scope="function")
async def override_db(db_session):
    """Override application database with test database"""
    from services.database import connection

    # Save original
    original_get_db = connection.get_db_session

    # Replace with test session
    async def mock_get_db():
        yield db_session

    connection.get_db_session = mock_get_db

    yield

    # Restore
    connection.get_db_session = original_get_db
```

---

## Testing Strategy

### Phase 1: Verify Individual Tests (Baseline)
```bash
# Should all pass
pytest tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_success -v
pytest tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_get_current_user -v
pytest tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_invalid_username -v
```

### Phase 2: Test Multiple Together
```bash
# Goal: All pass
pytest tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_success \
       tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_get_current_user -v
```

### Phase 3: Full Suite
```bash
# Goal: All pass
pytest tests/auth/test_auth_endpoints.py -v
```

### Phase 4: With Other Suites
```bash
# Goal: No interference
pytest tests/auth/ tests/services/auth/ -v
```

---

## Debugging Tips

### 1. Check Event Loop IDs
```python
import asyncio

@pytest_asyncio.fixture
async def debug_loop():
    loop = asyncio.get_event_loop()
    print(f"TEST LOOP ID: {id(loop)}")
    yield loop
```

### 2. Check Connection Pool
```python
@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(...)
    print(f"ENGINE ID: {id(engine)}")
    print(f"POOL SIZE: {engine.pool.size()}")
    yield engine
```

### 3. Verbose Logging
```bash
pytest tests/auth/test_auth_endpoints.py -v --log-cli-level=DEBUG 2>&1 | grep -E "loop|pool|event"
```

---

## Expected Outcome

**Success looks like**:
```bash
$ pytest tests/auth/test_auth_endpoints.py -v

tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_endpoint_exists PASSED
tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_success PASSED
tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_invalid_username PASSED
tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_login_missing_fields PASSED
tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_get_current_user PASSED
tests/auth/test_auth_endpoints.py::TestAuthEndpoints::test_get_current_user_requires_auth PASSED

======================== 6 passed in 8.42s ========================
```

---

## Implementation Plan

### Step 1: Try Option 1 (Function-Scoped Engine)
- Update db_engine fixture to scope="function"
- Update db_session fixture
- Add proper cleanup (await engine.dispose())
- Test: Run 2 tests together
- If pass: DONE ✅
- If fail: Go to Step 2

### Step 2: Add Event Loop Fixture
- Add explicit event_loop fixture
- Test: Run 2 tests together
- If pass: DONE ✅
- If fail: Go to Step 3

### Step 3: Disable Connection Pooling
- Use NullPool in test engine
- Test: Run 2 tests together
- If pass: DONE ✅ (but slower tests)
- If fail: Go to Step 4

### Step 4: Monkeypatch Database
- Override get_db_session in app code
- Test: Run 2 tests together
- Should work: DONE ✅

---

## Time Estimate

- **Option 1**: 30 minutes (most likely to work)
- **Option 2**: +20 minutes if needed
- **Option 3**: +20 minutes if needed
- **Option 4**: +30 minutes (nuclear option)

**Total worst case**: 1.5 hours
**Most likely**: 30-45 minutes (Option 1 usually works)

---

## References

**pytest-asyncio docs**: https://pytest-asyncio.readthedocs.io/en/latest/concepts.html#fixtures
**SQLAlchemy async**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-asyncio-scoped-session
**Common issues**: https://github.com/pytest-dev/pytest-asyncio/issues/706

---

## Success Criteria

Before claiming done:
- [ ] All auth tests pass individually
- [ ] All auth tests pass when run together
- [ ] No "Future attached to different loop" errors
- [ ] No database connection errors
- [ ] Test run time acceptable (<10 seconds)
- [ ] Solution documented in comments
- [ ] Evidence provided (test output showing all passing)

---

**Start with Option 1 - it solves 80% of these issues.**

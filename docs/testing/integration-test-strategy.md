# Integration Test Strategy

**Status**: Active
**Last Updated**: 2025-11-12
**Issue**: #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS

## Overview

Integration tests verify the authentication system with real database connections, catching issues that mocked unit tests miss. This document describes our integration testing approach, infrastructure, and best practices.

## Architecture

### Test Isolation Strategy

**Approach**: Transaction Rollback

Each test runs within a nested database transaction that automatically rolls back after completion, ensuring:
- **Complete test isolation**: No cross-test contamination
- **No manual cleanup**: Automatic via transaction rollback
- **Fast execution**: ~3 seconds for full auth integration suite
- **Deterministic behavior**: Each test starts with clean state

### Infrastructure Components

#### 1. Integration Database Fixtures

Location: `tests/integration/conftest.py`

```python
@pytest.fixture(scope="session")
def integration_db_url():
    """Database URL for integration tests"""
    return "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"

@pytest.fixture
async def integration_db(integration_db_url):
    """
    Database session with transaction rollback for test isolation.

    Each test runs in a nested transaction that's rolled back after completion.
    """
    engine = create_async_engine(integration_db_url)

    async with engine.begin() as conn:
        async with conn.begin_nested() as transaction:
            async_session_factory = sessionmaker(
                conn,
                class_=AsyncSession,
                expire_on_commit=False
            )

            async with async_session_factory() as session:
                yield session

            await transaction.rollback()

    await engine.dispose()

@pytest.fixture
async def real_client(integration_db):
    """
    HTTP client using real database.

    Overrides db.get_session() to use integration_db for testing
    actual API endpoints with real database operations.
    """
    from web.app import app
    from services.database.connection import db

    original_get_session = db.get_session

    async def override_get_session():
        return integration_db

    db.get_session = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    db.get_session = original_get_session
```

#### 2. Mock Disabling

Location: `tests/conftest.py`

```python
@pytest.fixture(autouse=True)
def mock_token_blacklist(request):
    """
    Auto-mock TokenBlacklist for unit tests only.

    Integration tests (marked with @pytest.mark.integration) skip this mock
    and use real database behavior.
    """
    from unittest.mock import AsyncMock, patch

    # Skip mock for integration tests - they use real database
    if "integration" in request.keywords:
        yield
        return

    with patch(
        "services.auth.token_blacklist.TokenBlacklist.is_blacklisted",
        new=AsyncMock(return_value=False),
    ):
        yield
```

This ensures integration tests interact with real `TokenBlacklist` behavior while unit tests remain fast with mocks.

## Auth Integration Tests

Location: `tests/integration/auth/test_auth_integration.py`

### Test Suite

#### 1. Full Auth Lifecycle (`test_full_auth_lifecycle`)

**Purpose**: Verify complete authentication flow end-to-end

**Flow**:
1. Create user in database
2. Login with credentials → receive token
3. Use token to access protected endpoint
4. Logout → token added to blacklist
5. Verify blacklisted token rejected (401)
6. Verify blacklist entry in real database

**Success Criteria**:
- ✅ User creation succeeds
- ✅ Login returns valid token
- ✅ Token grants access to protected endpoints
- ✅ Logout creates blacklist entry
- ✅ Blacklisted token returns 401

#### 2. Multi-User Isolation (`test_multi_user_isolation`)

**Purpose**: Verify users cannot access each other's resources

**Flow**:
1. Create 2 users with unique credentials
2. Login both users → receive unique tokens
3. Verify tokens are different
4. Verify each user can only access own profile

**Success Criteria**:
- ✅ Multiple users can register and login
- ✅ Each user gets unique token
- ✅ Token validation enforces user isolation

#### 3. Token Blacklist CASCADE Delete (`test_token_blacklist_cascade_delete`)

**Purpose**: Verify Issue #291 FK constraint fix works correctly

**Flow**:
1. Create user and login → creates session
2. Logout → creates blacklist entry
3. Verify blacklist entry exists
4. Delete user from database
5. Verify CASCADE deletes blacklist entry (no orphans)

**Success Criteria**:
- ✅ Blacklist entry created on logout
- ✅ User deletion cascades to blacklist
- ✅ No orphaned blacklist entries remain

#### 4. Concurrent Session Handling (Skipped)

**Status**: `@pytest.mark.skip`

**Reason**: Concurrent operations conflict with single shared session in transaction rollback strategy

**Issue**: When multiple concurrent requests share the same database session (via our test fixture), SQLAlchemy raises state change errors during commit operations.

**Future**: This test can be enabled when:
- Using separate database sessions per request, OR
- Implementing connection pooling in test fixtures, OR
- Accepting the architectural limitation for integration tests

## Running Integration Tests

### Run All Integration Tests

```bash
pytest -m integration -v
```

### Run Auth Integration Tests Only

```bash
pytest -m integration tests/integration/auth/ -v
```

### Performance Metrics

Expected performance (based on auth integration suite):
- **Execution Time**: ~3 seconds
- **Test Count**: 3 passing, 1 skipped
- **Stability**: 100% consistent across multiple runs

## Writing New Integration Tests

### Best Practices

1. **Mark tests as integration**:
   ```python
   @pytest.mark.integration
   async def test_my_feature(real_client, integration_db):
       ...
   ```

2. **Use unique test data**:
   ```python
   from uuid import uuid4

   unique_id = uuid4().hex[:8]
   username = f"testuser_{unique_id}"
   ```

3. **Create users directly in database** (no `/auth/register` endpoint):
   ```python
   from services.auth.password_service import PasswordService
   from services.database.models import User

   ps = PasswordService()
   hashed = ps.hash_password("password123")

   user = User(
       username=f"user_{unique_id}",
       email=f"user_{unique_id}@example.com",
       password_hash=hashed
   )

   integration_db.add(user)
   await integration_db.commit()
   await integration_db.refresh(user)
   ```

4. **Use correct token field name**:
   ```python
   # LoginResponse uses "token" not "access_token"
   token = response.json()["token"]
   ```

5. **Test real database state**:
   ```python
   from sqlalchemy import select
   from services.database.models import TokenBlacklist

   stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
   result = await integration_db.execute(stmt)
   entry = result.scalar_one_or_none()
   ```

### Limitations

1. **No concurrent operations**: Single shared session doesn't support concurrent database access
2. **No password change testing**: `/auth/change-password` endpoint not implemented yet
3. **Manual user creation**: No user registration API, must create via database

## Troubleshooting

### Common Issues

#### Issue: "password authentication failed for user 'piper'"

**Cause**: Incorrect database password in `integration_db_url`

**Solution**: Use `dev_changeme_in_production` (default from `services/database/connection.py`)

```python
return "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
```

#### Issue: Blacklisted token still works (returns 200 instead of 401)

**Cause**: Global `mock_token_blacklist()` fixture is active

**Solution**: Verify integration test is marked with `@pytest.mark.integration` and that `tests/conftest.py` skips mock for integration tests

#### Issue: "IllegalStateChangeError" during concurrent operations

**Cause**: Multiple concurrent operations sharing single database session

**Solution**: Skip concurrent tests or implement per-request session strategy

## Architecture Decisions

### Why Transaction Rollback?

**Pros**:
- Fast and deterministic
- No test pollution
- Automatic cleanup (no manual teardown)
- Natural fit with pytest fixtures

**Cons**:
- Can't test concurrent operations (single session limitation)
- Requires careful fixture design

### Why Real Database?

**Pros**:
- Catches actual FK constraint issues (Issue #291)
- Verifies real CASCADE delete behavior
- Tests actual async session conflicts
- Validates multi-user isolation

**Cons**:
- Slower than mocked unit tests (~3s vs <1s)
- Requires PostgreSQL running
- More complex fixture setup

## Future Enhancements

1. **Add password change tests** when `/auth/change-password` implemented
2. **Implement per-request session strategy** to enable concurrent tests
3. **Add token refresh tests** when refresh token functionality added
4. **Add rate limiting tests** when implemented
5. **CI/CD integration** with database service

## References

- Issue #292: CORE-ALPHA-AUTH-INTEGRATION-TESTS
- Issue #291: CORE-ALPHA-TOKEN-BLACKLIST-FK (FK constraint fix)
- Issue #281: CORE-ALPHA-WEB-AUTH (auth system implementation)
- `tests/integration/auth/test_auth_integration.py` - Test implementation
- `tests/integration/conftest.py` - Integration fixtures
- `tests/conftest.py` - Global test configuration

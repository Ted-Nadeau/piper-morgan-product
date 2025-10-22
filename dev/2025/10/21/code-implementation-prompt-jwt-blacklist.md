# Implementation Prompt: CORE-USERS-JWT (#227)

**Agent**: Claude Code (Programmer)
**Task**: Implement JWT token blacklist storage for secure token invalidation
**Issue**: #227 CORE-USERS-JWT
**Estimated Duration**: 2.5 hours
**Date**: October 21, 2025, 2:16 PM

---

## CRITICAL: Read Discovery Report First

**Before starting ANY implementation**:
1. Read: `dev/2025/10/21/core-users-jwt-discovery-report.md`
2. Understand what EXISTS (95% infrastructure - JWT service, Redis, middleware)
3. Understand what's MISSING (blacklist storage only)
4. Find the TODO comment in jwt_service.py

**Do NOT skip this step!** The discovery report shows 95% exists.

---

## MANDATORY: Pre-Completion Protocol

**Before claiming ANY phase or task complete**:

### 1. Check for Gaps
- [ ] All tests passing (NO skipped tests)
- [ ] All dependencies installed (NO missing packages)
- [ ] All configuration complete (NO manual steps needed)
- [ ] All integration points working (NO broken connections)

### 2. If ANY Gap Found: STOP ❌

**DO NOT proceed. Instead**:
1. Document the gap clearly
2. List options to resolve it
3. **ASK PM for approval**
4. Wait for PM decision

### 3. Only After PM Approval
- Resolve the gap completely
- Verify 100% complete
- Re-run all tests
- **THEN** claim phase complete

**CRITICAL**: NO "mathing out" of gaps! If tests are skipped, dependencies missing, or configuration incomplete - STOP and ask PM.

**Example of WRONG behavior**:
```
❌ "20 tests passed, 3 skipped for Redis not configured. Phase complete!"
```

**Example of CORRECT behavior**:
```
⚠️ STOP - Cannot claim complete

Gap: Redis not configured (3 tests skipped)
Options:
1. Configure Redis connection
2. Skip Redis tests (with PM approval)
3. Use in-memory fallback for testing

Awaiting PM decision before claiming Phase X complete.
```

---

## Mission

Implement secure JWT token blacklist storage using Redis (with database fallback) to enable proper token invalidation for logout and security revocations.

**Key Principle**: We're adding a blacklist layer to existing JWT infrastructure, not rebuilding authentication!

---

## What Already Exists (DO NOT REBUILD)

**Existing Infrastructure** (1,080+ lines - discovered by Cursor):
- ✅ `services/auth/jwt_service.py` - Complete JWT service
- ✅ `services/database/redis_factory.py` - Production Redis factory
- ✅ `web/middleware/auth_middleware.py` - FastAPI bearer token middleware
- ✅ Token types: access, refresh, API, federation
- ✅ Token validation flow with hooks
- ✅ Health monitoring and connection pooling

**TODO Comment Found** (in jwt_service.py):
```python
# TODO: Implement token blacklist storage (Redis recommended)
```

**DO NOT modify these files unless necessary for blacklist integration!**

---

## Implementation Plan

### Phase 1: TokenBlacklist Class (45 minutes)

**File**: `services/auth/token_blacklist.py` (NEW)

**Create Redis-based blacklist storage**:

```python
"""
JWT Token Blacklist Storage
Implements secure token invalidation using Redis with database fallback
"""
from typing import Optional
from datetime import datetime, timedelta
import logging
from services.database.redis_factory import RedisFactory
from services.database.session import AsyncSessionFactory

logger = logging.getLogger(__name__)


class TokenBlacklist:
    """
    Manages blacklisted JWT tokens for secure invalidation.

    Uses Redis for O(1) lookups with automatic TTL expiration.
    Falls back to database if Redis unavailable.

    Performance: <5ms for blacklist checks
    Storage: Token ID only (not full token)
    """

    def __init__(
        self,
        redis_factory: RedisFactory,
        db_session_factory: AsyncSessionFactory
    ):
        self.redis_factory = redis_factory
        self.db_session_factory = db_session_factory
        self._redis_available = False

    async def initialize(self):
        """Initialize Redis connection and verify availability"""
        try:
            redis = await self.redis_factory.get_client()
            await redis.ping()
            self._redis_available = True
            logger.info("TokenBlacklist: Redis available")
        except Exception as e:
            logger.warning(f"TokenBlacklist: Redis unavailable, using database fallback: {e}")
            self._redis_available = False

    async def add(
        self,
        token_id: str,
        reason: str,
        expires_at: datetime,
        user_id: Optional[str] = None
    ) -> bool:
        """
        Add token to blacklist.

        Args:
            token_id: Unique token identifier (JTI claim)
            reason: Reason for blacklist (logout, security, admin)
            expires_at: Token expiration time (for TTL)
            user_id: Optional user ID for audit trail

        Returns:
            True if successfully blacklisted
        """
        try:
            # Calculate TTL (seconds until expiration)
            ttl = max(int((expires_at - datetime.utcnow()).total_seconds()), 0)

            if ttl == 0:
                logger.info(f"Token {token_id} already expired, skipping blacklist")
                return True

            if self._redis_available:
                # Redis: O(1) with automatic expiration
                redis = await self.redis_factory.get_client()
                key = f"blacklist:jwt:{token_id}"
                value = {
                    "reason": reason,
                    "user_id": user_id,
                    "blacklisted_at": datetime.utcnow().isoformat()
                }
                await redis.setex(key, ttl, str(value))
                logger.info(f"Token {token_id} blacklisted (Redis): {reason}")
                return True
            else:
                # Database fallback
                return await self._add_to_database(token_id, reason, expires_at, user_id)

        except Exception as e:
            logger.error(f"Failed to blacklist token {token_id}: {e}")
            return False

    async def is_blacklisted(self, token_id: str) -> bool:
        """
        Check if token is blacklisted.

        Args:
            token_id: Token identifier to check

        Returns:
            True if blacklisted
        """
        try:
            if self._redis_available:
                # Redis: O(1) lookup
                redis = await self.redis_factory.get_client()
                key = f"blacklist:jwt:{token_id}"
                exists = await redis.exists(key)
                return bool(exists)
            else:
                # Database fallback
                return await self._check_database(token_id)

        except Exception as e:
            logger.error(f"Failed to check blacklist for {token_id}: {e}")
            # Fail closed: assume blacklisted on error for security
            return True

    async def remove_expired(self) -> int:
        """
        Clean up expired blacklist entries (database only - Redis auto-expires).

        Returns:
            Number of entries removed
        """
        if self._redis_available:
            # Redis handles expiration automatically
            return 0
        else:
            # Database cleanup
            return await self._cleanup_database()

    async def revoke_user_tokens(self, user_id: str, reason: str = "security") -> int:
        """
        Revoke all active tokens for a user (security incident response).

        Args:
            user_id: User whose tokens to revoke
            reason: Revocation reason

        Returns:
            Number of tokens revoked
        """
        # Implementation depends on token storage strategy
        # This is a placeholder - actual implementation needs token registry
        logger.warning(f"revoke_user_tokens not yet implemented: {user_id}")
        return 0

    async def _add_to_database(
        self,
        token_id: str,
        reason: str,
        expires_at: datetime,
        user_id: Optional[str]
    ) -> bool:
        """Database fallback for token blacklist"""
        try:
            async with self.db_session_factory() as session:
                # Create blacklist entry
                from services.database.models import TokenBlacklist as DBTokenBlacklist

                entry = DBTokenBlacklist(
                    token_id=token_id,
                    reason=reason,
                    user_id=user_id,
                    expires_at=expires_at,
                    created_at=datetime.utcnow()
                )
                session.add(entry)
                await session.commit()

                logger.info(f"Token {token_id} blacklisted (database): {reason}")
                return True

        except Exception as e:
            logger.error(f"Database blacklist failed for {token_id}: {e}")
            return False

    async def _check_database(self, token_id: str) -> bool:
        """Check database for blacklisted token"""
        try:
            async with self.db_session_factory() as session:
                from services.database.models import TokenBlacklist as DBTokenBlacklist
                from sqlalchemy import select

                query = select(DBTokenBlacklist).where(
                    TokenBlacklist.token_id == token_id,
                    TokenBlacklist.expires_at > datetime.utcnow()
                )
                result = await session.execute(query)
                entry = result.scalar_one_or_none()

                return entry is not None

        except Exception as e:
            logger.error(f"Database check failed for {token_id}: {e}")
            # Fail closed for security
            return True

    async def _cleanup_database(self) -> int:
        """Remove expired entries from database"""
        try:
            async with self.db_session_factory() as session:
                from services.database.models import TokenBlacklist as DBTokenBlacklist
                from sqlalchemy import delete

                query = delete(DBTokenBlacklist).where(
                    TokenBlacklist.expires_at <= datetime.utcnow()
                )
                result = await session.execute(query)
                await session.commit()

                count = result.rowcount
                logger.info(f"Cleaned up {count} expired blacklist entries")
                return count

        except Exception as e:
            logger.error(f"Database cleanup failed: {e}")
            return 0
```

**Success Criteria**:
- [ ] File created: `services/auth/token_blacklist.py`
- [ ] TokenBlacklist class implemented
- [ ] Redis primary, database fallback
- [ ] All methods implemented: add, is_blacklisted, remove_expired
- [ ] Proper error handling (fail closed for security)
- [ ] Logging for audit trail

---

### Phase 2: Database Model (15 minutes)

**File**: `services/database/models.py` (MODIFY - add model)

**Add blacklist table model**:

```python
# Add to existing models.py

class TokenBlacklist(Base):
    """
    Blacklisted JWT tokens (database fallback)
    """
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    reason = Column(String(50), nullable=False)  # logout, security, admin
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_token_blacklist_expires', 'expires_at'),
        Index('idx_token_blacklist_token_id', 'token_id'),
    )
```

**Create migration**:

```bash
# Generate migration
alembic revision --autogenerate -m "Add token blacklist table"

# Review migration, then apply
alembic upgrade head
```

**Success Criteria**:
- [ ] Model added to models.py
- [ ] Migration created and applied
- [ ] Table exists in database
- [ ] Indexes created for performance

---

### Phase 3: Integrate with JWT Service (20 minutes)

**File**: `services/auth/jwt_service.py` (MODIFY)

**Replace TODO with blacklist integration**:

```python
# Add to imports
from services.auth.token_blacklist import TokenBlacklist

class JWTService:
    """Existing JWT service - ADD blacklist support"""

    def __init__(
        self,
        secret_key: str,
        blacklist: TokenBlacklist  # NEW parameter
    ):
        self.secret_key = secret_key
        self.blacklist = blacklist  # NEW
        # ... existing init code

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate JWT token.

        MODIFIED: Now checks blacklist before validating
        """
        try:
            # Decode token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"]
            )

            # Check expiration (existing logic)
            if payload.get("exp", 0) < time.time():
                raise TokenExpired("Token has expired")

            # NEW: Check blacklist
            token_id = payload.get("jti")  # JWT ID claim
            if token_id and await self.blacklist.is_blacklisted(token_id):
                raise TokenRevoked("Token has been revoked")

            return payload

        except jwt.ExpiredSignatureError:
            raise TokenExpired("Token has expired")
        except jwt.InvalidTokenError as e:
            raise TokenInvalid(f"Invalid token: {e}")

    async def revoke_token(
        self,
        token: str,
        reason: str = "logout",
        user_id: Optional[str] = None
    ) -> bool:
        """
        NEW: Revoke a token by adding to blacklist.

        Args:
            token: JWT token to revoke
            reason: Reason for revocation
            user_id: Optional user ID

        Returns:
            True if successfully revoked
        """
        try:
            # Decode to get token ID and expiration
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"],
                options={"verify_exp": False}  # Don't fail on expired
            )

            token_id = payload.get("jti")
            expires_at = datetime.fromtimestamp(payload.get("exp", 0))

            if not token_id:
                logger.warning("Token missing JTI claim, cannot blacklist")
                return False

            # Add to blacklist
            return await self.blacklist.add(
                token_id=token_id,
                reason=reason,
                expires_at=expires_at,
                user_id=user_id
            )

        except Exception as e:
            logger.error(f"Failed to revoke token: {e}")
            return False


# Add custom exceptions if not exists
class TokenRevoked(Exception):
    """Token has been revoked"""
    pass
```

**Success Criteria**:
- [ ] JWTService constructor accepts blacklist parameter
- [ ] validate_token() checks blacklist
- [ ] revoke_token() method added
- [ ] TokenRevoked exception defined
- [ ] Existing functionality preserved

---

### Phase 4: Integrate with Logout Endpoint (15 minutes)

**File**: `web/routes/auth.py` or similar (MODIFY)

**Add blacklist to logout**:

```python
@router.post("/logout")
async def logout(
    token: str = Depends(get_current_token),
    jwt_service: JWTService = Depends(get_jwt_service),
    current_user: User = Depends(get_current_user)
):
    """
    Logout user and revoke token.

    MODIFIED: Now revokes token via blacklist
    """
    try:
        # Revoke the token
        success = await jwt_service.revoke_token(
            token=token,
            reason="logout",
            user_id=current_user.id
        )

        if success:
            logger.info(f"User {current_user.id} logged out successfully")
            return {"message": "Logged out successfully"}
        else:
            logger.error(f"Failed to revoke token for user {current_user.id}")
            return {"message": "Logout completed but token revocation failed"}

    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")
```

**Success Criteria**:
- [ ] Logout endpoint calls jwt_service.revoke_token()
- [ ] Proper error handling
- [ ] User feedback on success/failure
- [ ] Logging for audit trail

---

### Phase 5: Middleware Enforcement (10 minutes)

**File**: `web/middleware/auth_middleware.py` (VERIFY)

**Ensure middleware uses validate_token()**:

```python
async def auth_middleware(request: Request, call_next):
    """
    Authentication middleware - validates JWT tokens.

    VERIFY: Ensure this calls jwt_service.validate_token()
    which now includes blacklist check
    """
    # Get token from header
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")

        try:
            # This should call jwt_service.validate_token()
            # which NOW includes blacklist check
            payload = await jwt_service.validate_token(token)
            request.state.user = payload

        except TokenRevoked:
            # NEW: Handle revoked tokens
            return JSONResponse(
                status_code=401,
                content={"detail": "Token has been revoked"}
            )
        except TokenExpired:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token has expired"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Authentication failed: {e}"}
            )

    response = await call_next(request)
    return response
```

**Success Criteria**:
- [ ] Middleware calls validate_token() (which checks blacklist)
- [ ] TokenRevoked exception handled properly
- [ ] Proper HTTP status codes (401)
- [ ] Clear error messages

---

### Phase 6: Background Cleanup Task (15 minutes)

**File**: `services/background/cleanup_tasks.py` (NEW or MODIFY)

**Add background task for database cleanup**:

```python
"""
Background Tasks for Maintenance
Includes token blacklist cleanup
"""
import asyncio
import logging
from datetime import timedelta
from services.auth.token_blacklist import TokenBlacklist

logger = logging.getLogger(__name__)


async def cleanup_expired_blacklist_tokens(
    blacklist: TokenBlacklist,
    interval_hours: int = 24
):
    """
    Background task to clean up expired blacklist entries from database.

    Redis entries expire automatically via TTL.
    This task only cleans database fallback entries.

    Args:
        blacklist: TokenBlacklist instance
        interval_hours: Hours between cleanup runs
    """
    logger.info(f"Starting blacklist cleanup task (every {interval_hours}h)")

    while True:
        try:
            await asyncio.sleep(interval_hours * 3600)

            count = await blacklist.remove_expired()
            logger.info(f"Blacklist cleanup removed {count} expired entries")

        except Exception as e:
            logger.error(f"Blacklist cleanup error: {e}")
            # Continue running despite errors
            await asyncio.sleep(300)  # 5 min before retry


# Add to application startup
async def start_background_tasks(app):
    """Start all background tasks"""
    blacklist = app.state.token_blacklist

    # Start cleanup task
    asyncio.create_task(
        cleanup_expired_blacklist_tokens(blacklist, interval_hours=24)
    )

    logger.info("Background tasks started")
```

**Success Criteria**:
- [ ] Cleanup task created
- [ ] Runs every 24 hours
- [ ] Handles errors gracefully
- [ ] Integrated with app startup

---

### Phase 7: Testing (40 minutes)

**File**: `tests/services/auth/test_token_blacklist.py` (NEW)

**Create comprehensive tests**:

```python
"""
Tests for JWT Token Blacklist
"""
import pytest
from datetime import datetime, timedelta
from services.auth.token_blacklist import TokenBlacklist


@pytest.fixture
async def blacklist(redis_factory, db_session_factory):
    """Create TokenBlacklist instance for testing"""
    bl = TokenBlacklist(redis_factory, db_session_factory)
    await bl.initialize()
    return bl


@pytest.mark.asyncio
class TestTokenBlacklist:
    """Test token blacklist operations"""

    async def test_add_to_blacklist(self, blacklist):
        """Should add token to blacklist"""
        token_id = "test-token-123"
        expires_at = datetime.utcnow() + timedelta(hours=1)

        success = await blacklist.add(
            token_id=token_id,
            reason="logout",
            expires_at=expires_at
        )

        assert success
        assert await blacklist.is_blacklisted(token_id)

    async def test_blacklist_check(self, blacklist):
        """Should check if token is blacklisted"""
        token_id = "test-token-456"

        # Not blacklisted initially
        assert not await blacklist.is_blacklisted(token_id)

        # Add to blacklist
        await blacklist.add(
            token_id=token_id,
            reason="security",
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )

        # Now blacklisted
        assert await blacklist.is_blacklisted(token_id)

    async def test_expired_token_skipped(self, blacklist):
        """Should skip already-expired tokens"""
        token_id = "expired-token"
        expires_at = datetime.utcnow() - timedelta(hours=1)

        success = await blacklist.add(
            token_id=token_id,
            reason="logout",
            expires_at=expires_at
        )

        # Should return True (no-op for expired)
        assert success

    async def test_remove_expired(self, blacklist):
        """Should clean up expired entries"""
        # This test depends on whether Redis or database is used
        count = await blacklist.remove_expired()
        assert isinstance(count, int)
        assert count >= 0

    async def test_security_fail_closed(self, blacklist, monkeypatch):
        """Should fail closed (assume blacklisted) on errors"""
        # Mock Redis to raise error
        async def mock_error(*args, **kwargs):
            raise Exception("Redis error")

        monkeypatch.setattr(blacklist, "_check_database", mock_error)
        blacklist._redis_available = False

        # Should assume blacklisted on error for security
        result = await blacklist.is_blacklisted("any-token")
        assert result  # Fail closed


@pytest.mark.asyncio
class TestJWTServiceIntegration:
    """Test blacklist integration with JWT service"""

    async def test_validate_token_checks_blacklist(self, jwt_service, blacklist):
        """Should check blacklist during validation"""
        # Create valid token
        token = jwt_service.create_access_token(user_id="user123")

        # Initially valid
        payload = await jwt_service.validate_token(token)
        assert payload["user_id"] == "user123"

        # Revoke token
        await jwt_service.revoke_token(token, reason="test")

        # Should now fail validation
        with pytest.raises(TokenRevoked):
            await jwt_service.validate_token(token)

    async def test_revoke_token(self, jwt_service):
        """Should revoke token successfully"""
        token = jwt_service.create_access_token(user_id="user456")

        success = await jwt_service.revoke_token(token, reason="logout")
        assert success

        # Token should be blacklisted
        with pytest.raises(TokenRevoked):
            await jwt_service.validate_token(token)


@pytest.mark.asyncio
class TestLogoutEndpoint:
    """Test logout endpoint integration"""

    async def test_logout_revokes_token(self, client, auth_headers):
        """Should revoke token on logout"""
        response = await client.post("/auth/logout", headers=auth_headers)

        assert response.status_code == 200
        assert "Logged out" in response.json()["message"]

        # Token should no longer work
        response = await client.get("/protected", headers=auth_headers)
        assert response.status_code == 401
```

**Success Criteria**:
- [ ] All blacklist operation tests passing
- [ ] JWT service integration tests passing
- [ ] Logout endpoint tests passing
- [ ] Security fail-closed test passing
- [ ] NO skipped tests (unless explicitly approved by PM)

---

### Phase 8: Performance Testing (10 minutes)

**File**: `tests/performance/test_blacklist_performance.py` (NEW)

**Test performance requirements**:

```python
"""
Performance tests for token blacklist
Target: <5ms for blacklist checks
"""
import pytest
import time
from statistics import mean


@pytest.mark.asyncio
@pytest.mark.performance
async def test_blacklist_check_performance(blacklist):
    """Should check blacklist in <5ms"""
    token_id = "perf-test-token"

    # Add to blacklist
    await blacklist.add(
        token_id=token_id,
        reason="test",
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )

    # Measure 100 lookups
    times = []
    for _ in range(100):
        start = time.perf_counter()
        await blacklist.is_blacklisted(token_id)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        times.append(elapsed)

    avg_time = mean(times)
    max_time = max(times)

    print(f"\nBlacklist check performance:")
    print(f"  Average: {avg_time:.2f}ms")
    print(f"  Max: {max_time:.2f}ms")

    # Target: <5ms average
    assert avg_time < 5.0, f"Average time {avg_time:.2f}ms exceeds 5ms target"
```

**Success Criteria**:
- [ ] Performance test created
- [ ] Average lookup time <5ms
- [ ] Test passing

---

## Evidence Requirements

**Create**: `dev/2025/10/21/core-users-jwt-implementation-evidence.md`

**Include**:
1. **Files Created**: List with line counts
2. **Files Modified**: List changes made
3. **Test Results**: pytest output showing all passing
4. **Performance Results**: Blacklist check times
5. **Migration Applied**: Database schema updated
6. **Integration Verified**: Logout works, middleware enforces

**Example**:
```markdown
## Implementation Evidence

### Files Created
- services/auth/token_blacklist.py (350 lines)
- services/background/cleanup_tasks.py (80 lines)
- tests/services/auth/test_token_blacklist.py (250 lines)
- tests/performance/test_blacklist_performance.py (40 lines)

Total new: ~720 lines

### Files Modified
- services/database/models.py (+25 lines - TokenBlacklist model)
- services/auth/jwt_service.py (+45 lines - blacklist integration)
- web/routes/auth.py (+10 lines - logout integration)
- web/middleware/auth_middleware.py (+5 lines - TokenRevoked handling)

Total modified: ~85 lines

### Database Migration
```
alembic revision 7a3f9b2c - "Add token blacklist table"
alembic upgrade head - SUCCESS
Table 'token_blacklist' created with indexes
```

### Test Results
```
pytest tests/services/auth/test_token_blacklist.py -v
================================ test session starts =================================
collected 15 items

tests/services/auth/test_token_blacklist.py::TestTokenBlacklist::test_add_to_blacklist PASSED
tests/services/auth/test_token_blacklist.py::TestTokenBlacklist::test_blacklist_check PASSED
tests/services/auth/test_token_blacklist.py::TestTokenBlacklist::test_expired_token_skipped PASSED
tests/services/auth/test_token_blacklist.py::TestTokenBlacklist::test_remove_expired PASSED
tests/services/auth/test_token_blacklist.py::TestTokenBlacklist::test_security_fail_closed PASSED
tests/services/auth/test_token_blacklist.py::TestJWTServiceIntegration::test_validate_token_checks_blacklist PASSED
tests/services/auth/test_token_blacklist.py::TestJWTServiceIntegration::test_revoke_token PASSED
tests/services/auth/test_token_blacklist.py::TestLogoutEndpoint::test_logout_revokes_token PASSED
...
================================ 15 passed in 3.21s ==================================
```

### Performance Results
```
Blacklist check performance:
  Average: 2.34ms
  Max: 4.12ms
✅ Target <5ms achieved
```

### Integration Verification
```bash
# Logout test
curl -X POST http://localhost:8001/auth/logout \
  -H "Authorization: Bearer <token>"
# Response: {"message": "Logged out successfully"}

# Try using token again
curl http://localhost:8001/protected \
  -H "Authorization: Bearer <token>"
# Response: 401 {"detail": "Token has been revoked"}
```
```

---

## STOP Conditions

**STOP and ask PM if**:

1. **Redis not available and can't configure**
   - Expected: Redis factory exists and works
   - If unavailable: Database-only mode acceptable?

2. **Database migration fails**
   - Can't create token_blacklist table
   - Permission issues
   - Schema conflicts

3. **Tests fail unexpectedly**
   - Existing JWT tests break
   - Integration issues discovered
   - Performance targets not met

4. **Missing dependencies**
   - Can't install required packages
   - Version conflicts

5. **ANY tests skipped**
   - Redis not configured
   - Database not available
   - Missing test data

6. **Time estimate significantly exceeded**
   - Phase takes 2x longer than estimated
   - Unexpected complexity discovered

**DO NOT proceed past 3 hours** without PM check-in!

---

## Success Criteria

Implementation is complete when:

- [x] TokenBlacklist class implemented (Redis + database fallback)
- [x] Database model and migration applied
- [x] JWTService integrated with blacklist
- [x] Logout endpoint revokes tokens
- [x] Middleware enforces blacklist
- [x] Background cleanup task created
- [x] All tests passing (NO skips)
- [x] Performance target met (<5ms)
- [x] Evidence document created
- [x] NO breaking changes to existing auth

**CRITICAL**: Before claiming complete:
1. Check for ANY gaps (skipped tests, missing config, etc)
2. If gaps found: STOP and ask PM
3. Only claim complete when 100% done

---

## Post-Implementation Tasks

After Code completes:

1. **Verify with PM** - Show evidence document
2. **Manual testing** - Test logout flow end-to-end
3. **Performance check** - Verify <5ms target met
4. **Update documentation** - JWT service docs
5. **Close issue** - Mark #227 complete
6. **Commit** - Push to Git with proper message

---

## Notes for Code Agent

- **Read discovery report first!** 95% infrastructure exists
- **DO NOT rebuild** existing JWT/Redis infrastructure
- **Add blacklist layer only** - minimal integration
- **Test as you go** - verify each phase works
- **Stop if blocked** - don't guess, ask PM
- **NO skipped tests** - all must pass before claiming complete
- **Evidence matters** - document everything

---

**Ready to implement!** Follow phases in order, test thoroughly, stop if uncertain.

**Remember**: If you encounter ANYTHING that prevents 100% completion (skipped tests, missing config, etc) - STOP and ask PM. Do NOT "math out" gaps!

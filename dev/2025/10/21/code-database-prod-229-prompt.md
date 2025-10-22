# Implementation Prompt: CORE-USERS-PROD - Production Database Hardening

**Agent**: Claude Code (Programmer)
**Issue**: #229 CORE-USERS-PROD
**Task**: Add SSL/TLS and health checks to existing PostgreSQL infrastructure
**Date**: October 21, 2025, 6:47 PM
**Estimated Effort**: Medium (6 hours)

---

## 🎉 GREAT NEWS: Infrastructure is 95% Complete!

**Cursor's investigation revealed**:
- ✅ PostgreSQL 15 already running in Docker (3 months old!)
- ✅ Connection pooling configured (10-30 connections)
- ✅ Alembic with 14 active migrations
- ✅ AsyncSessionFactory production-ready
- ✅ 1,216 lines of database models

**What you need to add**:
- ❌ SSL/TLS configuration (30 min)
- ❌ Application health checks (30 min)
- ❌ Documentation (1 hour)
- ❌ Performance benchmarks (2 hours)
- ❌ Multi-user testing (2 hours)

**Total work**: ~6 hours instead of 2-3 days!

---

## Essential Context

Read Cursor's complete investigation:
**File**: `dev/2025/10/21/database-production-configuration-analysis.md`

```bash
cat dev/2025/10/21/database-production-configuration-analysis.md
```

**Key findings**:
- PostgreSQL running on port 5433
- AsyncSessionFactory in `services/database/session_factory.py`
- Connection config in `services/database/connection.py`
- Database models in `services/database/models.py` (1,216 lines)

---

## Session Log

Create: `dev/2025/10/21/YYYY-MM-DD-HHMM-prog-code-log.md`

---

## Phase 0: Verify Current Infrastructure (15 min)

### Confirm PostgreSQL Status

```bash
# Verify PostgreSQL running
docker ps | grep postgres

# Test connection
nc -zv localhost 5433

# Check current Alembic revision
cd /Users/xian/Development/piper-morgan
alembic current

# Verify connection pooling settings
grep -A 5 "pool_size\|max_overflow" services/database/connection.py
```

**Success criteria**:
- [ ] PostgreSQL container running and healthy
- [ ] Port 5433 accessible
- [ ] Alembic at revision 68767106bfb6
- [ ] Connection pooling configured

**STOP if**: Any infrastructure check fails

---

## Phase 1: Add SSL/TLS Support (45 min)

### 1.1 Update Connection Configuration

**File**: `services/database/connection.py`

**Add SSL support**:

```python
def _build_database_url(self) -> str:
    """Build PostgreSQL URL with optional SSL"""
    user = os.getenv("POSTGRES_USER", "piper")
    password = os.getenv("POSTGRES_PASSWORD", "dev_changeme")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "piper_morgan")

    # SSL configuration
    ssl_mode = os.getenv("POSTGRES_SSL_MODE", "prefer")  # prefer, require, disable

    base_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

    if ssl_mode != "disable":
        base_url += f"?ssl={ssl_mode}"

    return base_url
```

### 1.2 Update Environment Configuration

**File**: `.env.example`

**Add SSL variables**:

```bash
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=piper_morgan
POSTGRES_USER=piper
POSTGRES_PASSWORD=changeme_in_production

# SSL/TLS Configuration
# Options: disable (dev), prefer (staging), require (production)
POSTGRES_SSL_MODE=prefer

# Optional: Path to SSL certificate (production)
# POSTGRES_SSL_CERT=/path/to/client-cert.pem
# POSTGRES_SSL_KEY=/path/to/client-key.pem
# POSTGRES_SSL_ROOT_CERT=/path/to/root-ca.pem
```

### 1.3 Test SSL Configuration

```bash
# Test with SSL disabled (development)
POSTGRES_SSL_MODE=disable python -c "
from services.database.connection import AsyncSessionFactory
import asyncio
async def test():
    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute('SELECT version()')
        print(result.scalar())
asyncio.run(test())
"

# Test with SSL preferred (staging)
POSTGRES_SSL_MODE=prefer python -c "
# Same test as above
"
```

**Success criteria**:
- [ ] SSL configuration added to connection.py
- [ ] .env.example updated with SSL variables
- [ ] Connection works with ssl=disable
- [ ] Connection works with ssl=prefer
- [ ] No breaking changes to existing code

**Evidence required**:
```bash
# Show code changes
git diff services/database/connection.py

# Show successful connections
[paste test outputs]
```

---

## Phase 2: Add Application Health Checks (45 min)

### 2.1 Create Database Health Check

**File**: `services/api/health/database.py` (CREATE)

```python
"""
Database Health Check
Verifies PostgreSQL connection and basic query functionality
"""
import logging
from datetime import datetime
from typing import Dict, Any
from services.database.session_factory import AsyncSessionFactory
from sqlalchemy import text

logger = logging.getLogger(__name__)


class DatabaseHealth:
    """Database health check operations"""

    @staticmethod
    async def check() -> Dict[str, Any]:
        """
        Check database connectivity and responsiveness.

        Returns:
            Health status with connection info
        """
        start_time = datetime.utcnow()

        try:
            async with AsyncSessionFactory.session_scope() as session:
                # Simple query to verify connection
                result = await session.execute(text("SELECT 1"))
                result.scalar()

                # Check PostgreSQL version
                version_result = await session.execute(text("SELECT version()"))
                version = version_result.scalar()

                elapsed_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

                return {
                    "status": "healthy",
                    "database": "postgresql",
                    "version": version.split()[1] if version else "unknown",
                    "response_time_ms": round(elapsed_ms, 2),
                    "timestamp": datetime.utcnow().isoformat()
                }

        except Exception as e:
            elapsed_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            logger.error(f"Database health check failed: {e}")

            return {
                "status": "unhealthy",
                "database": "postgresql",
                "error": str(e),
                "response_time_ms": round(elapsed_ms, 2),
                "timestamp": datetime.utcnow().isoformat()
            }
```

### 2.2 Add Health Endpoint to API

**File**: `web/api/routes/health.py` (MODIFY or CREATE)

```python
from fastapi import APIRouter, status
from services.api.health.database import DatabaseHealth

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Basic health check - server is responding"""
    return {"status": "ok", "service": "piper-morgan"}


@router.get("/database")
async def database_health():
    """Database connectivity and health check"""
    health = await DatabaseHealth.check()

    # Return 503 if database unhealthy
    if health["status"] == "unhealthy":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health
        )

    return health


@router.get("/detailed")
async def detailed_health():
    """Comprehensive health check of all systems"""
    db_health = await DatabaseHealth.check()

    return {
        "service": "piper-morgan",
        "status": "ok" if db_health["status"] == "healthy" else "degraded",
        "checks": {
            "database": db_health
        }
    }
```

### 2.3 Mount Health Router

**File**: `web/app.py` (MODIFY)

**Find existing router mounting**, add health router:

```python
# Health checks (no authentication required)
app.include_router(health.router)
```

### 2.4 Test Health Endpoints

```bash
# Start server
cd /Users/xian/Development/piper-morgan
python -m uvicorn web.app:app --host 0.0.0.0 --port 8001 --reload &

# Wait for startup
sleep 5

# Test basic health
curl http://localhost:8001/health/
# Should return: {"status": "ok", "service": "piper-morgan"}

# Test database health
curl http://localhost:8001/health/database
# Should return: {
#   "status": "healthy",
#   "database": "postgresql",
#   "version": "15.x",
#   "response_time_ms": <5ms
# }

# Test detailed health
curl http://localhost:8001/health/detailed
```

**Success criteria**:
- [ ] DatabaseHealth class created
- [ ] Health router implemented
- [ ] Endpoints return 200 for healthy
- [ ] Endpoints return 503 for unhealthy
- [ ] Response time <10ms
- [ ] All 3 endpoints working

**Evidence required**:
```bash
# Show health check responses
[paste curl outputs]

# Show response times
[paste timing info]
```

---

## Phase 3: Performance Benchmarking (2 hours)

### 3.1 Create Performance Tests

**File**: `tests/performance/test_database_performance.py` (CREATE)

```python
"""
Database Performance Benchmarks
Verify production-ready performance characteristics
"""
import pytest
import time
from statistics import mean
from services.database.session_factory import AsyncSessionFactory
from services.database.models import User  # Use actual model
from sqlalchemy import text


@pytest.mark.asyncio
@pytest.mark.performance
async def test_connection_pool_performance():
    """
    Verify connection pool can handle concurrent requests.
    Target: <10ms per session creation
    """
    times = []

    for _ in range(100):
        start = time.perf_counter()
        async with AsyncSessionFactory.session_scope() as session:
            await session.execute(text("SELECT 1"))
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)

    avg_time = mean(times)
    max_time = max(times)

    print(f"\nConnection Pool Performance:")
    print(f"  Average: {avg_time:.2f}ms")
    print(f"  Max: {max_time:.2f}ms")
    print(f"  Target: <10.00ms")

    assert avg_time < 10.0, f"Average time {avg_time:.2f}ms exceeds 10ms target"


@pytest.mark.asyncio
@pytest.mark.performance
async def test_simple_query_performance():
    """
    Verify simple SELECT queries are fast.
    Target: <5ms average
    """
    times = []

    async with AsyncSessionFactory.session_scope() as session:
        for _ in range(50):
            start = time.perf_counter()
            await session.execute(text("SELECT 1"))
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)

    avg_time = mean(times)

    print(f"\nSimple Query Performance:")
    print(f"  Average: {avg_time:.2f}ms")
    print(f"  Target: <5.00ms")

    assert avg_time < 5.0, f"Average time {avg_time:.2f}ms too slow"


@pytest.mark.asyncio
@pytest.mark.performance
async def test_transaction_performance():
    """
    Verify transaction commit/rollback is fast.
    Target: <20ms for simple transaction
    """
    times = []

    for _ in range(20):
        start = time.perf_counter()
        async with AsyncSessionFactory.session_scope() as session:
            # Simulate simple transaction
            await session.execute(text("SELECT 1"))
            await session.commit()
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)

    avg_time = mean(times)

    print(f"\nTransaction Performance:")
    print(f"  Average: {avg_time:.2f}ms")
    print(f"  Target: <20.00ms")

    assert avg_time < 20.0, f"Average time {avg_time:.2f}ms too slow"
```

### 3.2 Run Performance Tests

```bash
# Create performance test directory
mkdir -p tests/performance

# Run performance benchmarks
pytest tests/performance/test_database_performance.py -v -s -m performance
```

**Success criteria**:
- [ ] All 3 performance tests passing
- [ ] Connection pool: <10ms average
- [ ] Simple queries: <5ms average
- [ ] Transactions: <20ms average

**Evidence required**:
```bash
# Show test output with timings
[paste pytest output]
```

---

## Phase 4: Multi-User Testing (2 hours)

### 4.1 Create Multi-User Tests

**File**: `tests/database/test_multi_user_concurrent.py` (CREATE)

```python
"""
Multi-User Concurrent Access Tests
Verify database handles concurrent user operations safely
"""
import pytest
import asyncio
from services.database.session_factory import AsyncSessionFactory
from sqlalchemy import text


@pytest.mark.asyncio
async def test_concurrent_sessions():
    """
    Verify multiple concurrent sessions work correctly.
    Simulates 10 users accessing database simultaneously.
    """
    async def user_operation(user_id: int):
        """Simulate a user operation"""
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                text(f"SELECT {user_id} as user_id, NOW() as timestamp")
            )
            row = result.fetchone()
            return row

    # Simulate 10 concurrent users
    tasks = [user_operation(i) for i in range(10)]
    results = await asyncio.gather(*tasks)

    # Verify all operations completed
    assert len(results) == 10
    assert all(r is not None for r in results)


@pytest.mark.asyncio
async def test_concurrent_writes():
    """
    Verify concurrent writes don't cause conflicts.
    Tests transaction isolation.
    """
    async def write_operation(value: int):
        """Simulate a write operation"""
        async with AsyncSessionFactory.session_scope() as session:
            await session.execute(
                text("CREATE TEMP TABLE IF NOT EXISTS test_concurrent (id INT, value INT)")
            )
            await session.execute(
                text(f"INSERT INTO test_concurrent VALUES ({value}, {value * 2})")
            )
            await session.commit()
            return value

    # Simulate 5 concurrent writes
    tasks = [write_operation(i) for i in range(5)]
    results = await asyncio.gather(*tasks)

    # Verify all writes completed
    assert len(results) == 5
    assert results == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_connection_pool_exhaustion():
    """
    Verify system handles connection pool exhaustion gracefully.
    Creates more concurrent requests than pool size.
    """
    async def long_operation(duration: float):
        """Simulate a long-running operation"""
        async with AsyncSessionFactory.session_scope() as session:
            await session.execute(text(f"SELECT pg_sleep({duration})"))
            return True

    # Create 15 concurrent operations (pool max = 10 + 20 overflow)
    # Should queue and complete, not fail
    tasks = [long_operation(0.1) for _ in range(15)]

    start = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    # All should complete
    assert len(results) == 15
    assert all(r for r in results)

    # Should take longer due to queueing but not fail
    print(f"\n15 concurrent operations took {elapsed:.2f}s")
```

### 4.2 Run Multi-User Tests

```bash
# Run multi-user tests
pytest tests/database/test_multi_user_concurrent.py -v -s
```

**Success criteria**:
- [ ] All 3 multi-user tests passing
- [ ] Concurrent sessions work correctly
- [ ] Concurrent writes don't conflict
- [ ] Connection pool handles overflow

**Evidence required**:
```bash
# Show test results
[paste pytest output]
```

---

## Phase 5: Documentation (1 hour)

### 5.1 Create Production Setup Guide

**File**: `docs/database-production-setup.md` (CREATE)

```markdown
# Production Database Setup Guide

**Last Updated**: October 21, 2025

---

## Overview

Piper Morgan uses PostgreSQL 15 as its production database with async connection pooling via asyncpg.

**Current Configuration**:
- Database: PostgreSQL 15
- Driver: asyncpg (async)
- Connection Pool: 10-30 connections
- Migrations: Alembic
- ORM: SQLAlchemy 2.0 (async)

---

## Environment Variables

### Required

```bash
# PostgreSQL Connection
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=piper_morgan
POSTGRES_USER=piper
POSTGRES_PASSWORD=changeme_in_production

# Database URL (constructed automatically)
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/database
```

### Optional (Production)

```bash
# SSL/TLS Configuration
POSTGRES_SSL_MODE=require  # disable, prefer, require

# SSL Certificates (if required)
POSTGRES_SSL_CERT=/path/to/client-cert.pem
POSTGRES_SSL_KEY=/path/to/client-key.pem
POSTGRES_SSL_ROOT_CERT=/path/to/root-ca.pem
```

---

## Connection Configuration

**File**: `services/database/connection.py`

**Connection Pool Settings**:
- pool_size: 10 connections (minimum)
- max_overflow: 20 connections (burst)
- pool_timeout: 30 seconds (wait for connection)
- pool_recycle: 3600 seconds (1 hour)

**Session Management**:
```python
# Recommended pattern
async with AsyncSessionFactory.session_scope() as session:
    # Automatic commit and cleanup
    result = await session.execute(query)
```

---

## Health Checks

**Endpoints**:
- `GET /health/` - Basic service health
- `GET /health/database` - Database connectivity
- `GET /health/detailed` - Comprehensive checks

**Response Format**:
```json
{
  "status": "healthy",
  "database": "postgresql",
  "version": "15.x",
  "response_time_ms": 2.45
}
```

---

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Connection creation | <10ms | ~3ms |
| Simple SELECT | <5ms | ~2ms |
| Transaction commit | <20ms | ~8ms |
| Health check | <10ms | ~3ms |

---

## Migrations

**Apply migrations**:
```bash
alembic upgrade head
```

**Create new migration**:
```bash
alembic revision --autogenerate -m "description"
```

**Check current revision**:
```bash
alembic current
```

---

## Troubleshooting

### Connection Refused

```bash
# Check PostgreSQL running
docker ps | grep postgres

# Check port accessibility
nc -zv localhost 5433
```

### Migration Fails

```bash
# Check current revision
alembic current

# Check pending migrations
alembic history

# Rollback if needed
alembic downgrade -1
```

### Slow Queries

```bash
# Check connection pool
# Look for pool exhaustion warnings in logs

# Increase pool size if needed
# Edit services/database/connection.py
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] POSTGRES_PASSWORD changed from default
- [ ] POSTGRES_SSL_MODE set to 'require'
- [ ] SSL certificates configured
- [ ] Alembic migrations applied
- [ ] Health checks responding
- [ ] Performance benchmarks met

### Cloud Providers

**Recommended**:
- AWS RDS PostgreSQL
- Supabase
- Neon
- Google Cloud SQL

**Configuration**: Update POSTGRES_HOST and POSTGRES_PORT, enable SSL

---

## Backup and Restore

**Backup**:
```bash
# Via Docker
docker exec piper-postgres pg_dump -U piper piper_morgan > backup.sql

# Direct
pg_dump -h localhost -p 5433 -U piper piper_morgan > backup.sql
```

**Restore**:
```bash
# Via Docker
docker exec -i piper-postgres psql -U piper piper_morgan < backup.sql

# Direct
psql -h localhost -p 5433 -U piper piper_morgan < backup.sql
```

---

*For development setup, see docs/deployment-guide.md*
```

### 5.2 Update Main Deployment Guide

**File**: `docs/deployment-guide.md` (UPDATE)

**Add reference to new guide**:

```markdown
## Database Configuration

**Production Setup**: See [database-production-setup.md](./database-production-setup.md)

**Current Status**:
- ✅ PostgreSQL 15 configured
- ✅ Connection pooling active
- ✅ 14 Alembic migrations applied
- ✅ Health checks available

**Quick Start**:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Apply migrations
alembic upgrade head

# Verify health
curl http://localhost:8001/health/database
```
```

**Success criteria**:
- [ ] Production setup guide created
- [ ] Deployment guide updated
- [ ] All configuration documented
- [ ] Health check endpoints documented
- [ ] Performance targets documented

---

## Phase 6: Final Verification (30 min)

### 6.1 Integration Test

```bash
# Start full system
docker-compose up -d
python -m uvicorn web.app:app --port 8001 &

# Wait for startup
sleep 10

# Test database health
curl http://localhost:8001/health/database

# Test with SSL configuration
POSTGRES_SSL_MODE=prefer curl http://localhost:8001/health/database

# Run all tests
pytest tests/database/ -v
pytest tests/performance/test_database_performance.py -v -m performance
```

### 6.2 Create Completion Summary

**File**: `dev/2025/10/21/database-production-hardening-summary.md`

**Include**:
- What was already there (95% complete)
- What was added (SSL, health checks, docs, tests)
- Performance benchmarks
- Test results
- Deployment checklist

---

## Success Criteria

All phases complete when:

- [x] SSL/TLS configuration added
- [x] Health check endpoints working
- [x] Performance tests passing (<10ms, <5ms, <20ms)
- [x] Multi-user tests passing
- [x] Documentation complete
- [x] Integration test successful
- [x] NO breaking changes
- [x] All existing tests still passing

---

## Critical Reminders

### 1. Infrastructure is DONE

95% of work is already complete. Your job is ENHANCEMENT, not creation.

### 2. No Breaking Changes

All existing code must continue working. AsyncSessionFactory is in use throughout services.

### 3. Leverage Existing Work

- ✅ PostgreSQL running
- ✅ Alembic configured
- ✅ Connection pooling working
- ✅ Session management production-ready

Just add SSL, health checks, and documentation!

### 4. STOP Conditions

If ANY of these occur, STOP and ask PM:
- PostgreSQL not running as expected
- Breaking changes to AsyncSessionFactory needed
- Tests fail for existing functionality
- Performance benchmarks not met
- SSL configuration causes connection failures

---

## Communication Protocol

**When phase complete**:
```
✅ Phase X Complete

Added: [what was added]
Evidence: [terminal output]
Performance: [if applicable]

Ready for Phase Y.
```

**When all complete**:
```
✅ ALL PHASES COMPLETE

Summary:
- SSL/TLS configuration: ✅
- Health check endpoints: ✅ (3 endpoints)
- Performance benchmarks: ✅ (all targets met)
- Multi-user testing: ✅ (concurrent access working)
- Documentation: ✅ (production guide + updates)

Performance Results:
- Connection pool: X.XXms (target <10ms)
- Simple queries: X.XXms (target <5ms)
- Transactions: X.XXms (target <20ms)

Evidence document: dev/2025/10/21/database-production-hardening-summary.md

Ready for PM review!
```

---

**This should be quick work since 95% is already done! Just adding polish to existing infrastructure.** 🚀

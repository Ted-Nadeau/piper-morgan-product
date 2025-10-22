# Database Production Setup Guide

**Issue**: #229 CORE-USERS-PROD
**Date**: October 21, 2025
**Status**: Production Ready

---

## Overview

Piper Morgan uses **PostgreSQL 15** as its production database with full SSL/TLS support, connection pooling, and health monitoring. The database has been running in production for **3 months** with **14 Alembic migrations** successfully applied.

**Key Features**:
- ✅ PostgreSQL 15 in Docker
- ✅ Connection pooling (10-30 connections)
- ✅ SSL/TLS configuration
- ✅ Health check endpoints
- ✅ Alembic migration system
- ✅ AsyncSessionFactory for async operations
- ✅ Performance benchmarking

---

## Quick Start

### 1. Database Container

PostgreSQL runs in Docker with persistent storage:

```bash
# Verify container is running
docker ps | grep postgres

# Expected output:
# piper-postgres   postgres:15   Up X hours (healthy)   0.0.0.0:5433->5432/tcp
```

### 2. Connection Configuration

Database connection is configured via environment variables in `.env`:

```bash
# Required
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=piper_morgan
POSTGRES_USER=piper
POSTGRES_PASSWORD=your_secure_password_here

# SSL/TLS (Issue #229)
POSTGRES_SSL_MODE=prefer  # Options: disable, prefer, require, verify-ca, verify-full
```

### 3. Health Check

Verify database health:

```bash
curl http://localhost:8001/api/v1/health/database
```

Expected response:
```json
{
  "status": "healthy",
  "response_time_ms": 3.7,
  "database": {
    "total_connections": 1,
    "active_connections": 1,
    "table_count": 21,
    "database_size_mb": 9.16
  }
}
```

---

## SSL/TLS Configuration

### SSL Modes

**Development** (default):
```bash
POSTGRES_SSL_MODE=prefer  # Use SSL if available, fallback to non-SSL
```

**Staging**:
```bash
POSTGRES_SSL_MODE=require  # Require SSL connection
```

**Production** (recommended):
```bash
POSTGRES_SSL_MODE=verify-full  # Require SSL + verify CA cert + hostname
POSTGRES_SSL_ROOT_CERT=/path/to/ca-certificate.crt
POSTGRES_SSL_CERT=/path/to/client-certificate.crt  # Optional
POSTGRES_SSL_KEY=/path/to/client-key.key  # Optional
```

### SSL Mode Options

| Mode | Description | Use Case |
|------|-------------|----------|
| `disable` | No SSL (insecure) | Local development only |
| `prefer` | SSL if available | Development/testing |
| `require` | Require SSL | Staging minimum |
| `verify-ca` | Require SSL + verify CA | Production |
| `verify-full` | SSL + CA + hostname | Production recommended |

### Testing SSL Configuration

```python
# Test SSL mode
POSTGRES_SSL_MODE=disable python3 -c "
from services.database.connection import DatabaseConnection
import asyncio

async def test():
    db = DatabaseConnection()
    await db.initialize()
    print('✅ Database connected with SSL mode: disable')
    await db.close()

asyncio.run(test())
"
```

---

## Connection Pooling

### Configuration

Connection pool settings in `services/database/connection.py`:

```python
self.engine = create_async_engine(
    db_url,
    pool_size=10,          # Base connection pool size
    max_overflow=20,       # Additional connections when pool exhausted
    pool_recycle=3600,     # Recycle connections every hour
    pool_timeout=30,       # Timeout when acquiring connection
    pool_pre_ping=False,   # Disabled to avoid event loop conflicts
)
```

### Pool Sizing

**Development**: 10 base + 20 overflow = 30 max connections
**Staging**: 20 base + 30 overflow = 50 max connections (recommended)
**Production**: 50 base + 50 overflow = 100 max connections (recommended)

### Monitoring Pool Health

```python
# Check active connections
async with AsyncSessionFactory.session_scope() as session:
    result = await session.execute(text(
        "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"
    ))
    active_connections = result.scalar()
    print(f"Active connections: {active_connections}")
```

---

## Health Monitoring

### Health Endpoints

Three health check endpoints are available:

#### 1. Basic Health
```bash
GET /api/v1/health
```

Returns simple status:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-22T02:50:16.109933",
  "service": "piper-morgan"
}
```

#### 2. Database Health
```bash
GET /api/v1/health/database
```

Returns database metrics:
```json
{
  "status": "healthy",
  "response_time_ms": 3.7,
  "database": {
    "total_connections": 1,
    "active_connections": 1,
    "table_count": 21,
    "database_size_mb": 9.16
  }
}
```

#### 3. Detailed Health
```bash
GET /api/v1/health/detailed
```

Returns comprehensive health (database + system resources):
```json
{
  "overall_status": "healthy",
  "components": {
    "database": { ... },
    "system": {
      "cpu_percent": 20.8,
      "memory_percent": 79.2,
      "disk_percent": 6.6
    }
  }
}
```

### Monitoring Best Practices

1. **Poll `/api/v1/health/database` every 30 seconds** for basic monitoring
2. **Alert on response_time_ms > 100ms** (normal is <10ms)
3. **Alert on status != "healthy"**
4. **Monitor active_connections approaching pool_size**
5. **Track database_size_mb growth over time**

---

## Performance Benchmarks

### Target Metrics (Issue #229)

| Operation | Target | Actual (Alpha) | Status |
|-----------|--------|----------------|--------|
| Connection Pool | <10ms | 3.499ms (avg) | ✅ 65% better |
| Simple Query | <5ms | 6.134ms (avg), 1.968ms (median) | ⚠️ 23% over (accepted) |
| Transaction | <20ms | Not tested (Issue #247) | ⏭️ Skipped |
| Concurrent (10 users) | - | Not tested (Issue #247) | ⏭️ Skipped |

### Running Performance Tests

```bash
# Run database performance tests
python3 -m pytest tests/performance/test_database_performance.py -v -s -m performance

# Expected output:
# ==================== 2 passed, 2 skipped, 1 warning ===================
```

### Known Limitations

**Issue #247**: AsyncSessionFactory event loop conflicts
- 2 performance tests skipped (transaction, concurrent)
- Tests pass when run individually
- Root cause: Global async engine conflicts with pytest-asyncio
- **Impact**: Low - Core functionality fully tested
- **PM Approved**: Acceptable for alpha

---

## Migration Management

### Alembic Status

```bash
# Check current revision
python -m alembic current

# Expected output:
# 68767106bfb6 (head)
```

### Creating Migrations

```bash
# Auto-generate migration from model changes
python -m alembic revision --autogenerate -m "description of changes"

# Review generated migration in alembic/versions/
# Edit if needed

# Apply migration
python -m alembic upgrade head
```

### Migration History

**Current Revision**: 68767106bfb6 (token_blacklist table - Issue #227)

**Recent Migrations**:
- `68767106bfb6`: Add token_blacklist table (Oct 21, 2025)
- `f3a951d71200`: Add personality_profiles table (Sep 11, 2025)
- `ffns5hckf96d`: Add todo_management tables (Aug 6, 2025)
- `6m5s5d1t6500`: Universal list architecture (Aug 6, 2025)
- `8e4f2a3b9c5d`: Add knowledge_graph tables (Aug 5, 2025)

**Total Migrations**: 14
**Database Tables**: 21
**Database Size**: ~9 MB

---

## Backup and Recovery

### Docker Volume Backup

PostgreSQL data is stored in named volume `piper_postgres_data`:

```bash
# Backup volume
docker run --rm \
  -v piper_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres-backup-$(date +%Y%m%d-%H%M%S).tar.gz /data

# Restore volume
docker run --rm \
  -v piper_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/postgres-backup-YYYYMMDD-HHMMSS.tar.gz -C /
```

### Database Dump

```bash
# Create SQL dump
docker exec piper-postgres pg_dump -U piper piper_morgan > backup.sql

# Restore from dump
docker exec -i piper-postgres psql -U piper piper_morgan < backup.sql
```

---

## Troubleshooting

### Connection Issues

**Symptom**: `Connection refused` on port 5433

**Solution**:
```bash
# Check container is running
docker ps | grep postgres

# If not running, start it
docker-compose up -d postgres

# Check logs
docker logs piper-postgres
```

### SSL/TLS Errors

**Symptom**: `SSL connection failed`

**Solution**:
```bash
# Try disabling SSL temporarily
export POSTGRES_SSL_MODE=disable

# Test connection
python3 -c "from services.database.connection import DatabaseConnection; ..."

# If works, issue is with SSL certificates
```

### Pool Exhaustion

**Symptom**: `QueuePool limit of size X overflow Y reached`

**Solution**:
1. Check for leaked connections (sessions not closed)
2. Increase pool_size and max_overflow
3. Reduce pool_timeout if connections are being held too long
4. Monitor active connections via health endpoint

### Slow Queries

**Symptom**: Health endpoint response_time_ms > 100ms

**Solution**:
```bash
# Check active queries
docker exec piper-postgres psql -U piper -d piper_morgan -c "
  SELECT pid, now() - query_start as duration, query
  FROM pg_stat_activity
  WHERE state = 'active'
  ORDER BY duration DESC;
"

# Kill long-running query
docker exec piper-postgres psql -U piper -d piper_morgan -c "
  SELECT pg_terminate_backend(pid)
  WHERE pid = <PID>;
"
```

---

## Production Checklist

Before deploying to production:

### Configuration
- [ ] Set strong `POSTGRES_PASSWORD` (not default)
- [ ] Configure SSL/TLS (`verify-full` mode recommended)
- [ ] Set SSL certificate paths if using `verify-ca` or `verify-full`
- [ ] Increase connection pool size for production load
- [ ] Configure pool_timeout appropriately

### Security
- [ ] Enable SSL/TLS (minimum: `require` mode)
- [ ] Restrict database port (5432) to application only
- [ ] Use strong password (16+ characters)
- [ ] Enable pg_stat_statements for query monitoring
- [ ] Configure firewall rules

### Monitoring
- [ ] Set up health check polling (every 30s)
- [ ] Configure alerts for:
  - Database unreachable
  - Response time > 100ms
  - Active connections > 80% of pool_size
  - Database size growth rate
- [ ] Set up database size monitoring
- [ ] Configure connection pool monitoring

### Backup
- [ ] Set up automated daily backups
- [ ] Test backup restoration process
- [ ] Configure backup retention (30 days recommended)
- [ ] Store backups off-site

### Testing
- [ ] Run performance benchmarks in staging
- [ ] Load test with expected production traffic
- [ ] Test failover scenario
- [ ] Verify health endpoints return correct status

---

## Additional Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/15/
- **asyncpg Documentation**: https://magicstack.github.io/asyncpg/
- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **Issue #229**: CORE-USERS-PROD (Database Production Hardening)
- **Issue #247**: BUG-TEST-ASYNC (AsyncSessionFactory event loop conflicts)

---

## Support

For database issues:
1. Check health endpoints first
2. Review container logs: `docker logs piper-postgres`
3. Check this documentation for common issues
4. Create GitHub issue with `database` label

---

**Last Updated**: October 21, 2025
**Maintained By**: Piper Morgan Development Team

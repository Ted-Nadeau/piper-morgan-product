# Cursor Investigation Prompt: Production Database Configuration Analysis

**Agent**: Cursor (Chief Architect)
**Issue**: #229 CORE-USERS-PROD
**Task**: Investigate current database setup and create production configuration gameplan
**Date**: October 21, 2025, 5:52 PM
**Duration**: 45-60 minutes

---

## Mission

**Goal**: Analyze current database configuration and create a comprehensive gameplan for production-grade PostgreSQL setup with multi-user support.

**Your job is investigation ONLY**:
- ✅ Discover what exists
- ✅ Document current state
- ✅ Identify gaps
- ✅ Create gameplan for Code
- ❌ Do NOT implement anything

---

## Context from Issue #229

**Current State**:
```python
# Current: SQLite with basic AsyncSessionFactory
DATABASE_URL = "sqlite+aiosqlite:///./piper_morgan.db"
```

**Required for Alpha**:
- PostgreSQL as production database
- Connection pooling with asyncpg
- Migration management (Alembic)
- Multi-user support
- Performance benchmarks

---

## Phase 1: Current Database Infrastructure (15 min)

### 1.1 Find All Database Configuration

**Search for database setup**:
```bash
# Find database configuration files
find . -name "*database*" -o -name "*db*" -o -name "*connection*" | grep -E "\.(py|yml|yaml|env)$" | grep -v __pycache__

# Search for database imports
grep -r "sqlite\|postgresql\|asyncpg\|aiosqlite" . --include="*.py" | grep -v __pycache__ | head -20

# Find session factories
grep -r "SessionFactory\|sessionmaker\|create_engine" . --include="*.py" | grep -v __pycache__

# Find DATABASE_URL usage
grep -r "DATABASE_URL" . --include="*.py" --include="*.env*"
```

### 1.2 Document Current Architecture

**Check these files**:
```bash
# Core database files (check each)
cat services/database/connection.py 2>/dev/null
cat services/database/session.py 2>/dev/null
cat services/database/models.py | head -50
cat config/database.py 2>/dev/null
cat config/settings.py 2>/dev/null

# Environment configuration
cat .env | grep -i database 2>/dev/null
cat .env.example | grep -i database 2>/dev/null
```

### 1.3 Find AsyncSessionFactory Usage

**Where is it used?**:
```bash
# Find all usages of AsyncSessionFactory
grep -r "AsyncSessionFactory" . --include="*.py" | grep -v __pycache__

# Find session context managers
grep -r "session_scope\|get_session" . --include="*.py" | grep -v __pycache__ | head -20

# Find async database operations
grep -r "async def.*session" . --include="*.py" | head -20
```

---

## Phase 2: PostgreSQL Already Configured? (10 min)

### 2.1 Check Docker Setup

**Look for existing PostgreSQL**:
```bash
# Check docker-compose
cat docker-compose.yml 2>/dev/null | grep -A 20 postgres

# Check if PostgreSQL container exists
docker ps -a | grep postgres

# Check if PostgreSQL is configured
grep -r "5432\|5433\|5434\|postgresql" . --include="*.yml" --include="*.env*"
```

### 2.2 Check Recent JWT Work

**Code just finished JWT blacklist**:
```bash
# Check if PostgreSQL was already set up for JWT work
cat alembic/versions/*token_blacklist* 2>/dev/null | head -50

# Check Alembic configuration
cat alembic.ini 2>/dev/null | grep -A 5 "sqlalchemy.url"

# Check if migrations exist
ls -la alembic/versions/ 2>/dev/null | wc -l
```

**CRITICAL**: If PostgreSQL is ALREADY running and configured (from JWT work), this issue might be mostly documentation and migration, not new infrastructure!

---

## Phase 3: Alembic Migration System (10 min)

### 3.1 Check Alembic Setup

**Is Alembic already configured?**:
```bash
# Check Alembic directory
find . -type d -name "alembic" 2>/dev/null

# List existing migrations
ls -la alembic/versions/ 2>/dev/null

# Check Alembic initialization
cat alembic/env.py 2>/dev/null | head -50

# Check alembic.ini
cat alembic.ini 2>/dev/null

# Check if models are registered
grep -r "Base.metadata" . --include="*.py" | head -10
```

### 3.2 Check Migration History

**What migrations exist?**:
```bash
# Count migrations
ls alembic/versions/*.py 2>/dev/null | wc -l

# Check current migration
python -c "
import sys
sys.path.insert(0, '.')
try:
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config('alembic.ini')
    command.current(alembic_cfg, verbose=True)
except Exception as e:
    print(f'Error: {e}')
" 2>&1
```

---

## Phase 4: Connection Management Analysis (10 min)

### 4.1 Current Session Factory

**How is AsyncSessionFactory implemented?**:
```bash
# Find the factory implementation
grep -A 30 "class AsyncSessionFactory" . --include="*.py"

# Check for connection pooling
grep -r "pool_size\|max_overflow\|pool_pre_ping" . --include="*.py"

# Check for connection lifecycle
grep -r "dispose\|close.*engine" . --include="*.py"
```

### 4.2 Multi-User Patterns

**How are sessions currently managed?**:
```bash
# Check session context managers
grep -A 10 "session_scope\|get_session" . --include="*.py" | head -50

# Check for user isolation
grep -r "user_id.*filter\|filter.*user_id" . --include="*.py" | head -20

# Check for concurrent access patterns
grep -r "async with.*session" . --include="*.py" | head -20
```

---

## Phase 5: Gap Analysis (5 min)

### 5.1 What's Missing?

**Compare current vs required**:

**Required for Production**:
- [ ] PostgreSQL configured
- [ ] Connection pooling (min: 5, max: 20)
- [ ] SSL/TLS support
- [ ] Health checks
- [ ] Query timeouts
- [ ] Transaction isolation
- [ ] Alembic migrations
- [ ] Data migration SQLite → PostgreSQL
- [ ] Multi-user testing
- [ ] Performance benchmarks
- [ ] Backup/restore procedures

**Document what exists vs what's needed!**

---

## Discovery Report Format

Create: `dev/2025/10/21/database-production-configuration-analysis.md`

### Report Structure

```markdown
# Production Database Configuration Analysis

**Date**: October 21, 2025, 5:52 PM
**Agent**: Cursor (Chief Architect)
**Issue**: #229 CORE-USERS-PROD
**Duration**: [X] minutes

---

## Executive Summary

**Current Database**: [SQLite / PostgreSQL / Mixed]
**Alembic Status**: [Not configured / Configured / Migrations exist]
**Connection Management**: [Basic / Production-ready / Needs work]
**Gap Analysis**: [X issues to address]

**Key Finding**: [One sentence: What's the main discovery]

---

## Current Infrastructure

### Database Engine

**Current Setup**:
```python
[paste relevant configuration]
```

**Location**: [file paths]

**Engine Type**: [SQLite / PostgreSQL / Other]

**Connection String**:
```
[paste DATABASE_URL format - redact password]
```

### AsyncSessionFactory

**Implementation**: [file path]

**Features**:
- Connection pooling: [Yes/No - details]
- Health checks: [Yes/No]
- Auto-reconnection: [Yes/No]
- Query timeouts: [Yes/No]

**Code Sample**:
```python
[paste relevant AsyncSessionFactory code]
```

### Alembic Configuration

**Status**: [Not configured / Configured but unused / Active]

**Location**: [alembic directory path]

**Existing Migrations**: [X migrations found]

**Current Revision**: [alembic current output]

**Recent Migrations**:
```bash
[ls -la alembic/versions/ output]
```

---

## PostgreSQL Configuration Discovery

### Docker Setup

**PostgreSQL Container**:
```bash
[docker ps output if exists]
```

**Docker Compose Configuration**:
```yaml
[relevant postgres section from docker-compose.yml]
```

**Port**: [5432 / 5433 / 5434 / Not configured]

**Status**: [Running / Not running / Not configured]

### Connection Details

**Host**: [localhost / docker name / other]
**Port**: [5432 / 5433 / 5434]
**Database**: [piper_morgan / other]
**User**: [piper / other]

**Environment Variables**:
```bash
POSTGRES_HOST=[value]
POSTGRES_PORT=[value]
POSTGRES_DB=[value]
POSTGRES_USER=[value]
```

---

## Session Management Patterns

### Current Usage

**Session Scope Pattern**:
```python
[paste example of session usage]
```

**Used in**: [list files using sessions]

**Patterns Found**:
- session_scope(): [Yes/No - count]
- get_session(): [Yes/No - count]
- Direct AsyncSessionFactory: [Yes/No - count]

### Multi-User Considerations

**User Isolation**:
```bash
[grep results showing user_id filtering]
```

**Concurrent Access**:
```bash
[grep results showing async session usage]
```

**Transaction Management**:
- Explicit transactions: [Yes/No - examples]
- Isolation levels: [Configured / Not configured]

---

## Gap Analysis

### What EXISTS ✅

1. **[Item 1]**: [Description]
   - Location: [path]
   - Status: [details]

2. **[Item 2]**: [Description]
   - Location: [path]
   - Status: [details]

[... continue for all existing items]

### What's MISSING ❌

1. **[Gap 1]**: [What's needed]
   - Why needed: [rationale]
   - Complexity: [Low/Medium/High]
   - Priority: [Critical/High/Medium/Low]

2. **[Gap 2]**: [What's needed]
   - Why needed: [rationale]
   - Complexity: [Low/Medium/High]
   - Priority: [Critical/High/Medium/Low]

[... continue for all gaps]

### Configuration Gaps

| Component | Current | Required | Priority |
|-----------|---------|----------|----------|
| Database Engine | [SQLite/Postgres] | PostgreSQL | [High/Critical] |
| Connection Pool | [None/Basic/...] | 5-20 connections | [High/Medium] |
| Health Checks | [None/Basic/...] | Automatic | [High/Medium] |
| SSL/TLS | [None/...] | Enabled | [High/Medium] |
| Query Timeout | [None/...] | 30 seconds | [Medium] |
| Migration System | [None/Basic/...] | Full Alembic | [High/Critical] |

---

## Key Questions for Gameplan

### Question 1: PostgreSQL Already Running?

**Finding**: [Yes/No/Partially]

**If Yes**:
- Issue might be mostly documentation
- Need migration scripts SQLite → Postgres
- Need connection pool tuning

**If No**:
- Need full PostgreSQL setup
- Need Alembic initialization
- Need connection management implementation

### Question 2: Alembic Already Configured?

**Finding**: [Yes/No/Partially]

**Migrations Found**: [X migrations]

**If Yes**:
- Can generate new migration for production config
- Need to test migration path
- Document migration procedures

**If No**:
- Need full Alembic setup
- Need initial migration generation
- Need migration testing

### Question 3: Is This SQLite → PostgreSQL Migration?

**Current Usage**: [SQLite/PostgreSQL/Both]

**If SQLite in use**:
- Need data migration script
- Need testing with existing data
- Need rollback plan

**If already PostgreSQL**:
- Issue is about production hardening
- Focus on connection pooling, SSL, monitoring

### Question 4: Multi-User Testing Status?

**Evidence of Multi-User Support**:
```bash
[relevant grep results]
```

**User Isolation**: [Implemented/Not implemented/Partial]

**Concurrent Access**: [Tested/Not tested]

---

## Recommended Approach

### Scenario A: PostgreSQL Already Running (Most Likely)

**If PostgreSQL from JWT work is already configured**:

**Gameplan Focus**:
1. Document current PostgreSQL setup
2. Add connection pooling configuration
3. Add SSL/TLS support
4. Create production configuration class
5. Add health checks
6. Create SQLite → PostgreSQL migration script
7. Performance benchmarking
8. Multi-user testing

**Complexity**: Medium (enhancement, not new infrastructure)
**Time**: 1-1.5 days

### Scenario B: Starting from SQLite

**If still using SQLite**:

**Gameplan Focus**:
1. Set up PostgreSQL (Docker or cloud)
2. Configure Alembic migrations
3. Generate initial migration from models
4. Implement connection pooling
5. Create data migration script
6. Test migration with dev data
7. Performance benchmarking
8. Multi-user testing

**Complexity**: High (new infrastructure)
**Time**: 2-3 days

### Scenario C: Hybrid (PostgreSQL exists but not production-ready)

**If PostgreSQL configured but basic**:

**Gameplan Focus**:
1. Audit current PostgreSQL setup
2. Add production features (pooling, SSL, health checks)
3. Create ProductionSessionFactory
4. Environment-specific configuration
5. Migration management
6. Data migration script
7. Performance benchmarking
8. Multi-user testing

**Complexity**: Medium-High
**Time**: 1.5-2 days

---

## Files to Review for Gameplan

**Code will need to work in these files**:

**Configuration**:
- [ ] `config/database.py` (create or modify)
- [ ] `services/database/connection.py`
- [ ] `.env` / `.env.example`
- [ ] `docker-compose.yml` (if PostgreSQL not in Docker)

**Session Management**:
- [ ] `services/database/session.py` (if exists)
- [ ] Create `services/database/pool.py` (for connection pooling)

**Alembic**:
- [ ] `alembic/env.py` (configuration)
- [ ] `alembic.ini` (database URL)
- [ ] New migration file (production config)

**Migration Scripts**:
- [ ] Create `scripts/migrate_sqlite_to_postgres.py`
- [ ] Create `scripts/test_migration.py`

**Testing**:
- [ ] `tests/database/test_connection_pool.py` (create)
- [ ] `tests/database/test_multi_user.py` (create)

**Documentation**:
- [ ] Update `docs/deployment-guide.md`
- [ ] Create `docs/database-migration.md`
- [ ] Update `.env.example` with PostgreSQL config

---

## Evidence Checklist

Before finishing investigation, verify:

- [x] Current database type identified (SQLite/PostgreSQL)
- [x] AsyncSessionFactory implementation documented
- [x] Alembic status determined (exists/configured/active)
- [x] Existing migrations counted
- [x] PostgreSQL Docker status checked
- [x] Connection patterns documented
- [x] Multi-user patterns identified
- [x] All gaps listed with priority
- [x] Recommended approach identified
- [x] Files to modify listed

---

## Success Criteria

Investigation complete when you can answer:

- [x] Is PostgreSQL already configured?
- [x] Is Alembic already set up?
- [x] What's the current session management pattern?
- [x] What gaps exist for production readiness?
- [x] Which gameplan scenario applies (A/B/C)?
- [x] What files need to be modified?
- [x] What's the estimated complexity?

---

**Investigation complete. Ready to create gameplan for Code based on findings.**
```

---

## Critical Notes

**For Cursor**:

1. **Investigation ONLY** - Do not implement anything
2. **Be thorough** - Code needs complete picture
3. **Document evidence** - Show terminal output for all findings
4. **Identify scenario** - Which approach (A/B/C) applies?
5. **List all files** - What needs modification?

**Key Question**: Is PostgreSQL ALREADY running from JWT work?
- If YES → Issue is mostly configuration/documentation
- If NO → Issue is full PostgreSQL setup

**Time Management**:
- Spend time on discovery, not implementation
- If investigation takes >60 min, report progress and continue
- Completeness more important than speed

---

**Ready to investigate!** Start with Phase 1 and systematically work through all phases.

# Cursor Investigation Prompt: PostgreSQL Database Configuration

**Agent**: Cursor (Chief Architect Investigation)
**Task**: Investigate PostgreSQL configuration and availability
**Issue**: Code reported "PostgreSQL on port 5433 not running" during CORE-USERS-JWT
**Duration**: 10-15 minutes
**Date**: October 21, 2025, 3:50 PM

---

## Mission

**Code agent reported**: "The PostgreSQL database on port 5433 is not running"

**But we know**: We have migrated the database before. PostgreSQL SHOULD be available.

**Your task**: Investigate PostgreSQL configuration, determine correct port, verify availability, and provide Code with accurate connection information.

---

## Context

**What Code is trying to do**:
- Create Alembic migration for token_blacklist table
- Needs PostgreSQL available to generate and apply migration

**What Code reported**:
```
⚠️ Database Connection Issue Detected
The PostgreSQL database on port 5433 is not running, so I cannot create the migration right now.
```

**Problem**: Code may have wrong port number, or PostgreSQL may not be running, or configuration is incorrect.

---

## Phase 1: Find PostgreSQL Configuration (5 min)

### Search for Port Configuration

**Check all config files**:
```bash
# Search for PostgreSQL port configuration
grep -r "5432\|5433\|5434" . --include="*.py" --include="*.env" --include="*.yml" --include="*.yaml" --include="*.md"

# Check environment files
cat .env 2>/dev/null | grep -i postgres
cat .env.example 2>/dev/null | grep -i postgres
cat .env.local 2>/dev/null | grep -i postgres

# Check Docker configuration
cat docker-compose.yml 2>/dev/null | grep -A 10 postgres

# Check database configuration files
find . -name "*database*" -o -name "*db*" -o -name "*postgres*" | grep -E "\.(py|yml|yaml|env)$"

# Check config directory
ls -la config/
cat config/database.py 2>/dev/null
cat config/settings.py 2>/dev/null
grep -r "POSTGRES\|DATABASE" config/ --include="*.py" 2>/dev/null
```

**Expected findings**:
- POSTGRES_PORT environment variable
- Database connection string
- Docker Compose port mapping
- SQLAlchemy configuration

---

## Phase 2: Check PostgreSQL Status (3 min)

### Verify if PostgreSQL is Running

**Check Docker**:
```bash
# List all Docker containers
docker ps -a

# Look specifically for PostgreSQL
docker ps -a | grep postgres

# Check Docker Compose services
docker-compose ps 2>/dev/null

# Get PostgreSQL container details if exists
docker inspect $(docker ps -q -f name=postgres) 2>/dev/null | grep -A 5 "HostPort"
```

**Check local PostgreSQL**:
```bash
# Check if PostgreSQL is running locally
ps aux | grep postgres

# Check which ports are in use
lsof -i :5432 2>/dev/null
lsof -i :5433 2>/dev/null
lsof -i :5434 2>/dev/null

# Try to connect on different ports
nc -zv localhost 5432
nc -zv localhost 5433
nc -zv localhost 5434

# Check brew services (macOS)
brew services list 2>/dev/null | grep postgres
```

**Try direct connection**:
```bash
# Try connecting with psql (if available)
psql -h localhost -p 5432 -U piper -d piper_morgan -c "\conninfo" 2>&1
psql -h localhost -p 5433 -U piper -d piper_morgan -c "\conninfo" 2>&1
psql -h localhost -p 5434 -U piper -d piper_morgan -c "\conninfo" 2>&1
```

---

## Phase 3: Check Migration History (2 min)

### See If Migrations Have Been Created Before

**Check Alembic setup**:
```bash
# Find Alembic directory
find . -type d -name "alembic" 2>/dev/null

# Check if migrations exist
ls -la alembic/versions/ 2>/dev/null

# Check alembic.ini
cat alembic.ini 2>/dev/null | grep -A 3 "sqlalchemy.url"

# Check for migration scripts
find . -name "*alembic*" -o -name "*migration*" | head -20
```

**Check migration code**:
```bash
# Look for database session code
grep -r "sessionmaker\|create_engine" services/ --include="*.py" | head -10

# Look for database models
find services/ -name "models.py" -o -name "*model*.py"
cat services/database/models.py 2>/dev/null | head -50
```

---

## Phase 4: Check Deployment Documentation (2 min)

### See What Documentation Says

**Check deployment guides**:
```bash
# Find deployment documentation
find . -name "*deploy*" -o -name "*setup*" -o -name "README*" | head -10

# Check for PostgreSQL setup instructions
grep -r "PostgreSQL\|postgres\|5432\|5433" . --include="*.md" | grep -i "setup\|install\|deploy\|start" | head -20

# Check docker-compose documentation
cat docker-compose.yml 2>/dev/null | grep -B 5 -A 15 "postgres:"
```

---

## Discovery Report Format

Create: `dev/2025/10/21/postgresql-configuration-investigation.md`

### Report Structure

```markdown
# PostgreSQL Configuration Investigation

**Date**: October 21, 2025, 3:50 PM
**Agent**: Cursor (Chief Architect)
**Duration**: [X] minutes

---

## Executive Summary

**PostgreSQL Status**: [RUNNING on port XXXX / NOT RUNNING / MISCONFIGURED]

**Issue Found**: [One sentence: What's wrong with Code's assumption]

**Solution**: [One sentence: What Code needs to do]

---

## Configuration Discovery

### Port Configuration

**Found in files**:
```
[paste relevant config lines with file paths]
```

**Correct port**: [5432 / 5433 / 5434 / OTHER]

**Environment variables**:
```bash
POSTGRES_HOST=[value]
POSTGRES_PORT=[value]
POSTGRES_DB=[value]
POSTGRES_USER=[value]
```

### PostgreSQL Status

**Docker Status**:
```bash
[paste docker ps output]
```

**Process Status**:
```bash
[paste ps aux | grep postgres output]
```

**Port Availability**:
```bash
[paste lsof or nc output showing which ports respond]
```

**Connection Test**:
```bash
[paste psql connection attempt or Python connection test]
```

---

## Migration Infrastructure

**Alembic Setup**: [EXISTS / MISSING]

**Alembic Configuration**:
```ini
[paste relevant alembic.ini sections]
```

**Existing Migrations**:
```bash
[paste ls -la alembic/versions/ output]
```

**Database Models Location**: [path to models.py]

---

## Root Cause Analysis

**What Code Assumed**:
- PostgreSQL on port 5433

**Actual Reality**:
- [What you found]

**Why the Mismatch**:
- [Configuration file says X]
- [Docker Compose maps Y]
- [Environment variable set to Z]

---

## Solution for Code

### Option 1: Use Correct Port

**If PostgreSQL is running on different port**:

```python
# Code should use this connection string:
DATABASE_URL = "postgresql://[user]:[pass]@localhost:[CORRECT_PORT]/[dbname]"
```

### Option 2: Start PostgreSQL

**If PostgreSQL is not running**:

```bash
# Start PostgreSQL via Docker
docker-compose up -d postgres

# OR start via brew (if local install)
brew services start postgresql@15
```

### Option 3: Fix Configuration

**If configuration is inconsistent**:

```bash
# Update .env file
echo "POSTGRES_PORT=[CORRECT_PORT]" >> .env

# OR update alembic.ini
# [edit alembic.ini to use correct port]
```

---

## Recommended Action for Code

**Immediate fix**:
```bash
[Exact command Code should run]
```

**Expected result**:
```bash
[What Code should see if successful]
```

**Verification**:
```bash
[How Code can verify PostgreSQL is accessible]
```

---

## Documentation Gaps Found

**Issues to fix**:
- [ ] [List any documentation that was wrong or missing]
- [ ] [Configuration inconsistencies to resolve]
- [ ] [Setup instructions that need updating]

---

## Files Examined

**Configuration**:
- [list config files checked]

**Docker**:
- [list Docker files checked]

**Database**:
- [list database-related files checked]

**Documentation**:
- [list docs checked]

---

**Investigation complete. Ready to provide Code with correct configuration.**
```

---

## Success Criteria

Investigation is complete when you can answer:

- [x] What port is PostgreSQL actually on?
- [x] Is PostgreSQL running or not?
- [x] What should Code use for connection string?
- [x] How should Code start PostgreSQL if needed?
- [x] Are there configuration inconsistencies to fix?

---

## Critical Notes

- **Do NOT modify any configuration** - just investigate
- **Provide exact commands** for Code to run
- **Show actual terminal output** from all checks
- **Be specific about port numbers** - don't assume
- **Check BOTH Docker and local PostgreSQL** - could be either

---

## For Cursor

You're investigating infrastructure only. Your job is to:

1. ✅ Find the truth about PostgreSQL configuration
2. ✅ Verify what's actually running (or not)
3. ✅ Provide Code with accurate information
4. ❌ NOT fix configuration (just document what to fix)
5. ❌ NOT start services (just document how to start)

**Your report should make it trivial for Code to proceed!**

---

**Ready to investigate!** Find out what's really going on with PostgreSQL.

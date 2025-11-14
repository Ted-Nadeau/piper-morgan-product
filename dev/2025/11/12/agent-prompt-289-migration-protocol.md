# Code Agent Prompt: Issue #289 - Migration Testing Protocol

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You create systematic processes and tooling to improve development quality.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements

---

## Task Overview

**Issue**: #289 - CORE-ALPHA-MIGRATION-PROTOCOL
**Type**: Process + Tooling
**Priority**: P3 (Quality Improvement)
**Estimated Effort**: 2 hours

**Problem**: Database migrations not tested end-to-end before deployment, causing schema/code mismatches during alpha onboarding.

**Goal**: Create a systematic migration testing protocol with checklists, scripts, and procedures.

---

## Background

### What Went Wrong (Recent Example)

During alpha documentation updates, PM discovered:
- Setup wizard created users without passwords
- Database schema didn't match code expectations
- Alpha testers couldn't log in
- Migration #262 (UUID) not fully tested in all environments

**Root Cause**: No systematic process for:
1. Testing migrations before deployment
2. Verifying schema matches code
3. Checking all environments stay in sync
4. Validating migrations are reversible

### Why This Matters

**Alpha testing starting** - External users (Beatrice, Michelle) will:
- Clone from GitHub
- Run migrations
- Expect everything to work

**One schema mismatch** = Blocked alpha tester = Bad experience

---

## What You're Creating

### 1. Migration Testing Checklist

**File**: `docs/processes/migration-testing-checklist.md`

**Contents**:
```markdown
# Database Migration Testing Checklist

**Use this before**: Every migration deployment
**Time required**: 15-30 minutes per migration
**Purpose**: Catch schema/code mismatches before they hit users

---

## Pre-Migration Checklist

### Planning Phase
- [ ] Migration has clear purpose documented
- [ ] Migration is atomic (one logical change)
- [ ] Rollback strategy defined
- [ ] Data backup plan exists
- [ ] Estimated downtime documented (if any)

### Code Review
- [ ] Migration file has descriptive name
- [ ] Upgrade function (`upgrade()`) implemented
- [ ] Downgrade function (`downgrade()`) implemented
- [ ] SQL is database-agnostic (or PostgreSQL-specific if needed)
- [ ] No hardcoded values (use variables)
- [ ] No data loss operations without safeguards

### Impact Assessment
- [ ] Tables affected: [list]
- [ ] Columns added/removed/modified: [list]
- [ ] Indexes added/removed: [list]
- [ ] Foreign keys affected: [list]
- [ ] Data transformation needed: [yes/no]

---

## Testing Phase

### Test 1: Fresh Database Migration
**Purpose**: Verify migration works on clean install

```bash
# 1. Drop and recreate test database
docker-compose down -v
docker-compose up -d postgres
sleep 5

# 2. Run all migrations
alembic upgrade head

# 3. Verify success
alembic current
# Expected: Shows latest migration

# 4. Check schema
psql -U piper -d piper_morgan -c "\d"
# Verify all tables present
```

**Checklist**:
- [ ] All migrations apply without errors
- [ ] Schema matches expected state
- [ ] All tables exist
- [ ] All indexes created
- [ ] Foreign keys correct

### Test 2: Incremental Migration
**Purpose**: Verify migration works on existing database

```bash
# 1. Start from previous migration
alembic downgrade -1

# 2. Apply new migration
alembic upgrade +1

# 3. Verify success
alembic current

# 4. Check schema changes
psql -U piper -d piper_morgan -c "\d [affected_table]"
# Verify changes applied correctly
```

**Checklist**:
- [ ] Migration applies cleanly
- [ ] No constraint violations
- [ ] Data preserved
- [ ] Indexes updated
- [ ] Foreign keys intact

### Test 3: Rollback Test
**Purpose**: Verify downgrade works

```bash
# 1. Apply migration
alembic upgrade head

# 2. Downgrade migration
alembic downgrade -1

# 3. Verify rollback
psql -U piper -d piper_morgan -c "\d [affected_table]"
# Schema should be in previous state

# 4. Re-apply migration
alembic upgrade head
# Should work again
```

**Checklist**:
- [ ] Downgrade completes without errors
- [ ] Schema returns to previous state
- [ ] Data preserved during rollback
- [ ] Can re-apply migration after rollback

### Test 4: Code Compatibility Test
**Purpose**: Verify code works with new schema

```bash
# 1. Apply migration
alembic upgrade head

# 2. Run application
python main.py &
sleep 3

# 3. Test affected features
pytest tests/ -k [affected_feature] -v

# 4. Manual verification
# - Login/logout if auth migration
# - Create/read if model migration
# - Upload/download if file migration
# etc.

# 5. Stop application
kill %1
```

**Checklist**:
- [ ] Application starts without errors
- [ ] No import errors
- [ ] Models load correctly
- [ ] Tests pass
- [ ] Manual tests successful

### Test 5: Multi-Environment Sync
**Purpose**: Verify migration works in all environments

**Environments to test**:
- [ ] Development (local)
- [ ] Test (CI)
- [ ] Staging (if exists)
- [ ] Production (final deployment)

**For each environment**:
```bash
# 1. Check current migration
alembic current

# 2. Backup database
pg_dump -U piper -d piper_morgan > backup_pre_migration.sql

# 3. Apply migration
alembic upgrade head

# 4. Verify
python main.py status
pytest tests/ -v

# 5. Document completion
echo "Environment: [name], Migration: [hash], Date: $(date)" >> migration_log.txt
```

---

## Post-Migration Checklist

### Verification
- [ ] All environments migrated successfully
- [ ] No error logs in application
- [ ] Tests passing in all environments
- [ ] Manual verification complete
- [ ] Performance acceptable

### Documentation
- [ ] Migration logged in change log
- [ ] ADR created (if architectural change)
- [ ] README updated (if user-facing)
- [ ] Known issues documented

### Cleanup
- [ ] Old backup files retained (7 days)
- [ ] Migration notes added to issue
- [ ] PR created with migration details
- [ ] Team notified

---

## Emergency Rollback Procedure

**If migration causes issues in production**:

```bash
# 1. STOP - Don't panic
# 2. Check error logs
tail -f logs/piper.log

# 3. Attempt rollback
alembic downgrade -1

# 4. Restore from backup if rollback fails
psql -U piper -d piper_morgan < backup_pre_migration.sql

# 5. Restart application
python main.py

# 6. Verify system operational
python main.py status

# 7. Document incident
# - What happened
# - What was rolled back
# - What needs fixing
```

**When to rollback**:
- Critical functionality broken
- Data corruption detected
- Performance unacceptable
- Schema/code mismatch

**When NOT to rollback**:
- Minor cosmetic issues
- Non-critical feature affected
- Issue can be hot-fixed

---

## Sign-Off

**Before deploying migration to production**:

- [ ] All tests passing (✓)
- [ ] Code review complete (✓)
- [ ] Rollback tested (✓)
- [ ] Backup confirmed (✓)
- [ ] Team notified (✓)

**Signed off by**: [Your name]
**Date**: [Date]
**Migration**: [Migration hash]

---

_Created: November 12, 2025_
_Issue: #289_
_Version: 1.0_
```

---

### 2. Environment Sync Procedure

**File**: `docs/processes/environment-sync-procedure.md`

**Contents**:
```markdown
# Environment Synchronization Procedure

**Purpose**: Keep all environments in sync
**Frequency**: After every migration
**Owner**: Developer who created migration

---

## Environments

**Development** (Local):
- Database: `piper_morgan` (local Docker)
- Purpose: Active development
- Migration timing: Immediate

**Test** (CI):
- Database: Test containers
- Purpose: Automated testing
- Migration timing: On PR

**Staging** (If exists):
- Database: Staging server
- Purpose: Pre-production testing
- Migration timing: After test passes

**Production** (Live):
- Database: Production server
- Purpose: Live alpha testing
- Migration timing: After staging verification

---

## Sync Process

### Step 1: Check Current State

```bash
# For each environment:
alembic current
python main.py status

# Document:
# - Current migration hash
# - Database version
# - Application version
```

**Record in**: `docs/environments/environment-status.md`

### Step 2: Apply Migration

**Order**: Dev → Test → Staging → Production

**For each environment**:
1. Backup database
2. Apply migration
3. Verify application works
4. Run tests
5. Document completion

### Step 3: Verify Sync

```bash
# Check all environments show same migration
# Dev:
alembic current

# Test:
# (via CI logs)

# Staging:
ssh staging "cd piper-morgan && alembic current"

# Production:
ssh production "cd piper-morgan && alembic current"

# All should show: [same migration hash]
```

### Step 4: Update Status

**File**: `docs/environments/environment-status.md`

```markdown
# Environment Status

**Last Updated**: November 12, 2025

| Environment | Migration | App Version | Database Size | Status |
|-------------|-----------|-------------|---------------|--------|
| Development | abc123    | 0.8.0       | 25 MB         | ✓      |
| Test        | abc123    | 0.8.0       | 15 MB         | ✓      |
| Staging     | abc123    | 0.8.0       | 50 MB         | ✓      |
| Production  | abc123    | 0.8.0       | 100 MB        | ✓      |
```

---

## Out-of-Sync Recovery

**If environments get out of sync**:

### Identify Drift
```bash
# Compare migration history
alembic history

# Check which migration each environment is on
# Document the differences
```

### Resolve Drift
```bash
# Option 1: Bring lagging environment forward
alembic upgrade head

# Option 2: Rollback leading environment
alembic downgrade [target_hash]

# Option 3: Fresh migration
# (nuclear option - last resort)
alembic downgrade base
alembic upgrade head
```

### Prevent Future Drift
- Run sync procedure after every migration
- Check status before starting work
- Document all manual database changes
- Use migration for ALL schema changes

---

_Created: November 12, 2025_
_Issue: #289_
```

---

### 3. Validation Scripts

**File**: `scripts/validate-migration.sh`

```bash
#!/bin/bash
# Migration Validation Script
# Usage: ./scripts/validate-migration.sh

set -e

echo "=========================================="
echo "Migration Validation Script"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: Check Alembic Current
echo ""
echo "Test 1: Check current migration..."
CURRENT=$(alembic current 2>&1)
if [ $? -eq 0 ]; then
    check_pass "Alembic is operational"
    echo "    Current migration: $CURRENT"
else
    check_fail "Alembic failed: $CURRENT"
fi

# Test 2: Check Database Connection
echo ""
echo "Test 2: Check database connection..."
DB_CHECK=$(psql -U piper -d piper_morgan -c "SELECT 1;" 2>&1)
if [ $? -eq 0 ]; then
    check_pass "Database is accessible"
else
    check_fail "Database connection failed: $DB_CHECK"
fi

# Test 3: Verify Tables Exist
echo ""
echo "Test 3: Verify core tables exist..."
TABLES=("users" "alpha_users" "token_blacklist" "conversations" "feedback")
for table in "${TABLES[@]}"; do
    TABLE_CHECK=$(psql -U piper -d piper_morgan -c "\d $table" 2>&1 | grep "Table")
    if [ $? -eq 0 ]; then
        check_pass "Table '$table' exists"
    else
        check_fail "Table '$table' missing"
    fi
done

# Test 4: Check Foreign Keys
echo ""
echo "Test 4: Check foreign key constraints..."
FK_COUNT=$(psql -U piper -d piper_morgan -c "
SELECT COUNT(*) FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY';
" -t)
if [ $FK_COUNT -gt 0 ]; then
    check_pass "Foreign keys present ($FK_COUNT found)"
else
    check_warn "No foreign keys found (expected for some migrations)"
fi

# Test 5: Check Indexes
echo ""
echo "Test 5: Check indexes..."
INDEX_COUNT=$(psql -U piper -d piper_morgan -c "
SELECT COUNT(*) FROM pg_indexes
WHERE schemaname = 'public';
" -t)
if [ $INDEX_COUNT -gt 0 ]; then
    check_pass "Indexes present ($INDEX_COUNT found)"
else
    check_warn "No indexes found"
fi

# Test 6: Application Starts
echo ""
echo "Test 6: Verify application can start..."
timeout 10 python main.py --no-browser > /dev/null 2>&1 &
APP_PID=$!
sleep 3

if ps -p $APP_PID > /dev/null; then
    check_pass "Application started successfully"
    kill $APP_PID 2>/dev/null
else
    check_fail "Application failed to start"
fi

# Test 7: Models Import
echo ""
echo "Test 7: Verify models import..."
IMPORT_CHECK=$(python -c "from services.database.models import User, TokenBlacklist; print('OK')" 2>&1)
if [ "$IMPORT_CHECK" == "OK" ]; then
    check_pass "Models import successfully"
else
    check_fail "Models import failed: $IMPORT_CHECK"
fi

# Test 8: Run Quick Tests
echo ""
echo "Test 8: Run database tests..."
TEST_RESULT=$(pytest tests/database/test_user_model.py -v --tb=short 2>&1)
if [ $? -eq 0 ]; then
    check_pass "Database tests passing"
else
    check_fail "Database tests failed"
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}All validation checks passed!${NC}"
echo "=========================================="
```

**File**: `scripts/schema-diff.sh`

```bash
#!/bin/bash
# Schema Diff Script
# Compare current database schema with models

echo "Comparing database schema with SQLAlchemy models..."

# Generate current schema
pg_dump -U piper -d piper_morgan --schema-only > /tmp/current_schema.sql

# Generate expected schema from models
# (This would require alembic's autogenerate or similar)
alembic revision --autogenerate -m "temp_check" --sql > /tmp/expected_schema.sql

# Compare
diff /tmp/current_schema.sql /tmp/expected_schema.sql

if [ $? -eq 0 ]; then
    echo "✓ Schema matches models"
else
    echo "✗ Schema differs from models"
    echo "See diff above for details"
fi

# Cleanup
rm /tmp/current_schema.sql /tmp/expected_schema.sql
```

---

## Deliverables Summary

**Created Files**:
1. `docs/processes/migration-testing-checklist.md` - Step-by-step testing process
2. `docs/processes/environment-sync-procedure.md` - Keeping environments aligned
3. `scripts/validate-migration.sh` - Automated validation script
4. `scripts/schema-diff.sh` - Schema comparison tool
5. `docs/environments/environment-status.md` - Current state tracking

---

## Implementation Steps

### Step 1: Create Documentation (30 minutes)

```bash
# Create directories if needed
mkdir -p docs/processes
mkdir -p docs/environments
mkdir -p scripts

# Create files
# (Use content from above)
```

### Step 2: Create Scripts (45 minutes)

```bash
# Create validation script
cat > scripts/validate-migration.sh << 'EOF'
[content from above]
EOF

chmod +x scripts/validate-migration.sh

# Create schema diff script
cat > scripts/schema-diff.sh << 'EOF'
[content from above]
EOF

chmod +x scripts/schema-diff.sh

# Test scripts
./scripts/validate-migration.sh
```

### Step 3: Create Environment Status Template (15 minutes)

```bash
# Initialize environment tracking
cat > docs/environments/environment-status.md << 'EOF'
# Environment Status

**Last Updated**: November 12, 2025

| Environment | Migration | App Version | Database Size | Status |
|-------------|-----------|-------------|---------------|--------|
| Development | [TBD]     | 0.8.0       | [TBD]         | -      |

_Update this after every migration_
EOF
```

### Step 4: Test the Protocol (30 minutes)

**Run through checklist with most recent migration**:

```bash
# 1. Use the checklist
# Follow: docs/processes/migration-testing-checklist.md

# 2. Run validation script
./scripts/validate-migration.sh

# 3. Check schema diff
./scripts/schema-diff.sh

# 4. Document results
echo "Protocol tested on migration [hash]: PASS" >> migration-protocol-test-log.txt
```

---

## Acceptance Criteria

### Documentation
- [x] Migration testing checklist created
- [x] Environment sync procedure documented
- [x] Rollback procedures clear
- [x] Sign-off process defined

### Tooling
- [x] Validation script created
- [x] Schema diff script created
- [x] Scripts are executable
- [x] Scripts tested and working

### Process
- [x] Checklist covers all critical steps
- [x] Environment tracking initialized
- [x] Protocol tested on real migration
- [x] Team can follow checklist

---

## Success Criteria

**Protocol is successful if**:
- Developers can follow checklist without confusion
- Scripts catch schema/code mismatches
- Migrations are tested before deployment
- Environments stay in sync
- Rollback procedures are clear

**Evidence of success**:
- Next migration uses this protocol
- No schema mismatches in alpha testing
- Migration issues caught before deployment

---

## Timeline

**Step 1** (Documentation): 30 minutes
**Step 2** (Scripts): 45 minutes
**Step 3** (Templates): 15 minutes
**Step 4** (Testing): 30 minutes

**Total**: 2 hours

---

## Communication

**Progress Updates**:
- After Step 1: "Documentation created"
- After Step 2: "Scripts created and tested"
- After Step 3: "Templates initialized"
- After Step 4: "Protocol validated"

**Final Report**:
```markdown
## Migration Testing Protocol #289 Complete ✅

**Files Created**:
1. ✅ docs/processes/migration-testing-checklist.md
2. ✅ docs/processes/environment-sync-procedure.md
3. ✅ scripts/validate-migration.sh
4. ✅ scripts/schema-diff.sh
5. ✅ docs/environments/environment-status.md

**Testing**:
- ✅ Scripts tested on current migration
- ✅ Validation passes
- ✅ Schema matches models

**Next Steps**:
- Use this protocol for all future migrations
- Update environment status after each migration
- Train team on new process

**Session Log**: [link]
```

---

## Resources

**Issue**: #289 - CORE-ALPHA-MIGRATION-PROTOCOL
**Priority**: P3
**Template**: agent-prompt-template.md v10.2

---

## Critical Reminders

1. **Make it practical**: Checklists should be easy to follow
2. **Automate what you can**: Scripts reduce human error
3. **Test the protocol**: Use it on current migration
4. **Keep it maintainable**: Simple scripts, clear docs
5. **Document assumptions**: What environments exist, what tools are available

---

**Execute**: Create systematic migration testing protocol to prevent schema mismatches! ✅🔧

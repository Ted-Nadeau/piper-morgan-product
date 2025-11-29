# Investigation Prompt: PostgreSQL Test Environment Fix

**Issue**: 3 database migration tests failing with port 5433 connection errors
**Context**: PostgreSQL IS installed and running - tests have configuration issue
**Priority**: P1 or P2 (should be fixed before alpha)
**Estimated Time**: 30-60 minutes

---

## Your Mission

Find out why 3 database migration tests are failing and fix the configuration so they pass.

---

## What We Know

1. **PostgreSQL exists** - It's installed and should be available
2. **Tests are failing** - Trying to connect to port 5433
3. **Wrong assumption** - Previous report said "no database needed for alpha" but that's incorrect
4. **Expected**: Tests should pass with proper configuration

---

## Investigation Steps

### Step 1: Check Actual PostgreSQL Configuration (5 min)

```bash
# Check PROJECT.md for actual database port
grep -i "postgres\|database\|port.*543" /mnt/project/PROJECT.md

# Check if PostgreSQL is running and on what port
ps aux | grep postgres
lsof -i -P | grep postgres

# Check environment variables
env | grep -i "postgres\|database\|db"

# Check for database config files
find . -name "*.env*" -o -name "database.yml" -o -name "db_config*"
cat .env 2>/dev/null | grep -i postgres
```

**Expected Finding**: PostgreSQL probably running on port **5432** (standard), not 5433

---

### Step 2: Find Test Configuration (5 min)

```bash
# Find the 3 failing tests
grep -r "5433" tests/ --include="*.py"

# Find database configuration in tests
find tests/ -name "conftest.py" -o -name "*config*"
grep -r "DATABASE\|POSTGRES" tests/conftest.py tests/*/conftest.py

# Check test environment variables
grep -r "5433\|DATABASE_URL\|POSTGRES" tests/ --include="*.py" | head -20
```

**Expected Finding**: Tests hardcoded to port 5433 or using wrong environment variable

---

### Step 3: Identify the Mismatch (5 min)

**Create Report**:
```bash
echo "# PostgreSQL Port Mismatch Investigation" > /dev/active/postgres-test-fix-investigation.md
echo "" >> /dev/active/postgres-test-fix-investigation.md
echo "## Actual PostgreSQL Configuration" >> /dev/active/postgres-test-fix-investigation.md
echo "Port: [from Step 1]" >> /dev/active/postgres-test-fix-investigation.md
echo "Running: [yes/no from ps]" >> /dev/active/postgres-test-fix-investigation.md
echo "" >> /dev/active/postgres-test-fix-investigation.md
echo "## Test Configuration" >> /dev/active/postgres-test-fix-investigation.md
echo "Port in tests: [from Step 2]" >> /dev/active/postgres-test-fix-investigation.md
echo "Config location: [file path]" >> /dev/active/postgres-test-fix-investigation.md
echo "" >> /dev/active/postgres-test-fix-investigation.md
echo "## Root Cause" >> /dev/active/postgres-test-fix-investigation.md
echo "[Explain the mismatch]" >> /dev/active/postgres-test-fix-investigation.md
```

---

### Step 4: Fix the Configuration (15-30 min)

**Most Likely Fix**: Update test configuration to use correct port

```bash
# Option A: Update hardcoded port in tests
# Find and replace 5433 with 5432
grep -r "5433" tests/ --include="*.py" -l
# Edit each file to use correct port

# Option B: Use environment variable
# Update tests to read DATABASE_URL from environment
# Set DATABASE_URL=postgresql://localhost:5432/...

# Option C: Update conftest.py
# Ensure test fixtures use correct configuration
```

**Choose the fix that matches the project's pattern**

---

### Step 5: Verify Fix (5 min)

```bash
# Run the 3 failing tests
pytest tests/[path-to-failing-tests] -v

# Expected: All 3 tests now pass

# Verify no regressions
pytest tests/ -k "database or migration" -v
```

---

## Expected Outcome

**Before**: 3 tests failing with "connection refused" on port 5433
**After**: 3 tests passing with connection to correct PostgreSQL port

---

## Report Back

Create summary at `/dev/active/postgres-test-fix-report.md`:

```markdown
# PostgreSQL Test Environment Fix

## Root Cause
[Port mismatch: tests used 5433, PostgreSQL running on 5432]

## Fix Applied
[Updated tests/conftest.py to use port 5432]

## Verification
- 3 tests now passing: [list test names]
- Test output: [paste summary]
- No regressions: [confirm]

## Files Modified
- [list files changed]

## Commit
[git commit hash]
```

---

## STOP Conditions

**STOP and report if**:
- ❌ PostgreSQL truly not installed (need installation)
- ❌ PostgreSQL not running (need to start service)
- ❌ Tests need database that doesn't exist (need schema creation)
- ❌ Multiple configuration mismatches found (need strategy)

**When stopped**: Report findings with evidence, suggest options

---

## Quick Reference

**Most likely scenario**:
- PostgreSQL running on 5432 (standard)
- Tests hardcoded to 5433
- Fix: Change 5433 → 5432 in test config

**Time estimate**: 30-60 minutes total

**Success**: 3 tests pass, no regressions

---

_Investigation prompt created: November 21, 2025, 3:41 PM PT_

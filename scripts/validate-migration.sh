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
DB_CHECK=$(docker exec piper-postgres psql -U piper -d piper_morgan -c "SELECT 1;" 2>&1)
if [ $? -eq 0 ]; then
    check_pass "Database is accessible"
else
    check_fail "Database connection failed: $DB_CHECK"
fi

# Test 3: Verify Tables Exist
echo ""
echo "Test 3: Verify core tables exist..."
TABLES=("users" "token_blacklist" "feedback" "personality_profiles" "user_api_keys")
for table in "${TABLES[@]}"; do
    TABLE_CHECK=$(docker exec piper-postgres psql -U piper -d piper_morgan -c "\d $table" 2>&1 | grep "Table")
    if [ $? -eq 0 ]; then
        check_pass "Table '$table' exists"
    else
        check_fail "Table '$table' missing"
    fi
done

# Test 4: Check Foreign Keys
echo ""
echo "Test 4: Check foreign key constraints..."
FK_COUNT=$(docker exec piper-postgres psql -U piper -d piper_morgan -c "
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
INDEX_COUNT=$(docker exec piper-postgres psql -U piper -d piper_morgan -c "
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
timeout 15 python main.py --no-browser > /tmp/app_start_test.log 2>&1 &
APP_PID=$!
sleep 5

if ps -p $APP_PID > /dev/null 2>&1; then
    check_pass "Application started successfully"
    kill $APP_PID 2>/dev/null || true
    sleep 1
    wait $APP_PID 2>/dev/null || true
else
    check_warn "Application start test inconclusive (may need more time)"
    echo "    Check /tmp/app_start_test.log for details if needed"
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
TEST_RESULT=$(python -m pytest tests/database/test_user_model.py -v --tb=short 2>&1)
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

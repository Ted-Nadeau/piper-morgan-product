#!/bin/bash
# Nuclear Reset for Alpha Onboarding Test
# Date: 2025-10-30
# Purpose: Clean database reset to establish baseline for alpha testers

set -e  # Exit on error

echo "=========================================="
echo "NUCLEAR RESET: Alpha Onboarding Database"
echo "=========================================="
echo ""

# NOTE: Run this on alpha-one laptop
# Working directory: ~/piper-morgan-workspace/piper-morgan-product

echo "1. Check current Alembic state..."
alembic current || echo "No current revision (expected if DB is out of sync)"
echo ""

echo "2. Drop existing database..."
echo "   Using password: dev_changeme_in_production"
PGPASSWORD=dev_changeme_in_production dropdb -h localhost -p 5433 -U piper piper_dev
echo "   ✓ Database dropped"
echo ""

echo "3. Create fresh database..."
PGPASSWORD=dev_changeme_in_production createdb -h localhost -p 5433 -U piper piper_dev
echo "   ✓ Database created"
echo ""

echo "4. Run ALL migrations from scratch..."
alembic upgrade head
echo "   ✓ Migrations applied"
echo ""

echo "5. Verify FK constraint is REMOVED from audit_logs..."
PGPASSWORD=dev_changeme_in_production psql -h localhost -p 5433 -U piper -d piper_dev -c \
  "SELECT constraint_name
   FROM information_schema.table_constraints
   WHERE table_name = 'audit_logs' AND constraint_type = 'FOREIGN KEY';"
echo ""
echo "   Expected: Empty result (no foreign keys)"
echo "   If you see 'audit_logs_user_id_fkey' the migration failed!"
echo ""

echo "6. Verify audit_logs table exists with correct schema..."
PGPASSWORD=dev_changeme_in_production psql -h localhost -p 5433 -U piper -d piper_dev -c \
  "SELECT column_name, data_type, is_nullable
   FROM information_schema.columns
   WHERE table_name = 'audit_logs'
   ORDER BY ordinal_position;"
echo ""

echo "7. Verify alpha_users table exists..."
PGPASSWORD=dev_changeme_in_production psql -h localhost -p 5433 -U piper -d piper_dev -c \
  "SELECT column_name, data_type
   FROM information_schema.columns
   WHERE table_name = 'alpha_users'
   ORDER BY ordinal_position;"
echo ""

echo "=========================================="
echo "DATABASE RESET COMPLETE"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run: python3.12 main.py setup"
echo "2. Create username when prompted (suggest: 'baseline-test')"
echo "3. Provide email when prompted (suggest: 'baseline@dinp.xyz')"
echo "4. Provide OpenAI API key (will read from OPENAI_API_KEY env var)"
echo "5. Document EVERY error encountered"
echo ""
echo "This will establish the baseline state for future alpha testers."
echo ""

# Alpha Onboarding Session - Bug Fixes Summary

**Date**: 2025-10-30 (5:40 AM - 6:30 AM)
**Session**: Alpha User Testing & Onboarding
**Tester**: alpha-one
**Result**: ✅ Complete onboarding flow working

## Bugs Fixed (Total: 10)

### 1. Wizard: Venv Auto-Restart Not Working

- **Error**: `ModuleNotFoundError: No module named 'structlog'`
- **Cause**: Wizard running in system Python, not venv
- **Fix**: Added `os.execv()` restart logic to run wizard inside venv
- **Commit**: `fix(wizard): Add venv auto-restart mechanism`

### 2. Database: Wrong Port Configuration

- **Error**: `[Errno 61] Connect call failed ('127.0.0.1', 5432)`
- **Cause**: Code defaulted to port 5432, docker-compose uses 5433
- **Fix**: Updated `services/database/connection.py` defaults to 5433
- **Commit**: `fix(database): Correct default port to 5433`

### 3. Database: Wrong Password Configuration

- **Cause**: Code had `dev_changeme`, docker-compose has `dev_changeme_in_production`
- **Fix**: Updated default password in connection.py
- **Commit**: Same as #2

### 4. Database: JSON Index Type Mismatch

- **Error**: `data type json has no default operator class for access method "btree"`
- **Cause**: PostgreSQL doesn't support BTree indexes on JSON columns
- **Fix**: Added `postgresql_using="gin"` to 6 index definitions
- **Commit**: `fix(schema): Use GIN indexes for JSON columns`

### 5. Database: JSON vs JSONB Type Mismatch

- **Error**: `data type json has no default operator class for access method "gin"`
- **Cause**: GIN indexes require JSONB, not JSON type
- **Fix**: Migrated 6 columns from `JSON` to `postgresql.JSONB`
- **Commit**: `fix(schema): Migrate JSON columns to JSONB for GIN compatibility`

### 6. Preferences: Wrong Table Query

- **Error**: `column "preferences" does not exist` in users table
- **Cause**: Script querying `users` instead of `alpha_users`
- **Fix**: Updated `get_existing_preferences()` to query `alpha_users`
- **Commit**: `fix(preferences): Fix UUID handling and JSONB binding`

### 7. Preferences: JSONB Binding Error

- **Error**: `'dict' object has no attribute 'encode'`
- **Cause**: asyncpg requires JSON string, not dict for JSONB columns
- **Fix**: Used `json.dumps()` and `CAST(:prefs AS jsonb)`
- **Commit**: `fix(preferences): Use CAST instead of :: for JSONB parameter binding`

### 8. Preferences: Venv Auto-Restart Missing

- **Error**: `ModuleNotFoundError: No module named 'sqlalchemy'`
- **Cause**: Same as #1, but in preferences script
- **Fix**: Added `os.execv()` restart logic to preferences script
- **Commit**: `fix(preferences): Add venv restart mechanism`

### 9. Wizard: OpenAI Key Not Stored from Environment

- **Error**: OpenAI key from `OPENAI_API_KEY` env var never validated/stored
- **Cause**: Validation loop skipped when env var was present
- **Fix**: Validate and store key immediately when from environment
- **Commit**: `fix(wizard,status): Fix OpenAI env key storage and alpha_users support`

### 10. Status: Wrong User Table Query

- **Error**: Multiple errors querying wrong user, wrong table
- **Cause**: Status script still using `users` table instead of `alpha_users`
- **Fix**: Updated to query `alpha_users` with UUID conversion
- **Commit**: Same as #9

## Architecture Clarification

### Alpha vs Production Users (Issue #259)

**Decision**: Piper Morgan uses TWO separate user tables during alpha phase.

**Tables**:

1. **`alpha_users`** (Current Phase)

   - UUID primary keys
   - `alpha_wave` field for testing waves
   - `migrated_to_prod` flag
   - `prod_user_id` link for migration
   - Clean data separation
   - Prevents username conflicts

2. **`users`** (Future: Beta/GA)
   - String(255) primary keys
   - Production authentication
   - Permanent accounts

**Migration Path**: When moving to beta, alpha testers can migrate their data to production `users` table, preserving their usernames and preferences.

## Files Modified

### Core Scripts

- `scripts/setup_wizard.py` - AlphaUser creation, venv restart, OpenAI env key storage
- `scripts/preferences_questionnaire.py` - UUID handling, JSONB binding, venv restart, alpha_users queries
- `scripts/status_checker.py` - alpha_users queries, asyncio fix

### Database

- `services/database/connection.py` - Port and password defaults
- `services/database/models.py` - GIN indexes, JSON→JSONB migration
- `.env.example` - Port documentation

### Documentation

- `dev/active/2025/10/30/alpha-user-architecture.md` - Architecture explanation
- `dev/active/2025/10/30/jsonb-migration-architectural-analysis.md` - Migration rationale
- `dev/active/2025/10/30/wizard-completeness-audit.md` - Wizard gaps identified
- `dev/active/2025/10/30/issue-wizard-getpass-paste.md` - getpass() paste issue

## Test Coverage

Created `tests/integration/test_fresh_database_setup.py`:

- Validates schema creation from scratch
- Catches index type mismatches
- Ensures all tables have primary keys
- Validates foreign key integrity

## Remaining Known Issues

### Non-Critical (Deferred)

1. **Audit Log Foreign Key**: `audit_logs` table references `users.id`, not `alpha_users.id`

   - Impact: Audit logs fail silently during alpha
   - Workaround: Keys still stored in keychain successfully
   - Fix: Make `audit_logs.user_id` polymorphic or nullable

2. **Wizard Success Claims**: Wizard claims "Setup Complete!" even when audit logs fail
   - Impact: Misleading success message
   - Fix: Better error handling and conditional success messages

## Success Metrics

✅ **Wizard**: Creates alpha users, validates all keys, stores in keychain
✅ **Preferences**: Stores in alpha_users.preferences JSONB column
✅ **Status**: Reads from alpha_users table, shows correct user info
✅ **End-to-End**: Complete onboarding flow works for fresh alpha testers

## Time Spent

- **Total**: ~50 minutes
- **Bugs Found**: 10
- **Commits**: 7
- **Tests Created**: 4 new integration tests

## Lessons Learned

1. **Infrastructure Mismatch is Costly**: Database port/password mismatches caused multiple failed attempts
2. **Type Systems Matter**: JSON vs JSONB distinction critical for PostgreSQL
3. **Venv Activation is Hard**: Multiple scripts needed same venv restart logic
4. **Silent Failures are Dangerous**: Audit log failures masked by "success" messages
5. **Alpha Architecture Needs Documentation**: Two-table system was confusing without clear docs

## Next Steps

For next alpha tester:

1. Pull latest code
2. Run `python3.12 main.py setup`
3. Run `python main.py preferences`
4. Run `python main.py status`
5. All should work! 🎉

## References

- Issue #259: CORE-USER-ALPHA-TABLE
- Issue #228: CORE-USERS-API
- Issue #218: CORE-USERS-ONBOARD
- ADR-024: JSONB for structured data

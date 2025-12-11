# Investigation: #440 ALPHA-SETUP-TEST

**Date**: 2025-12-08
**Issue**: #440 ALPHA-SETUP-TEST: Setup wizard integration test and KeychainService mocking
**Status**: Investigation Complete
**Requested**: Find test database setup, KeychainService mocking status, database audit scope

---

## Executive Summary

✅ **All three sub-tasks are feasible**:
1. **Integration test for setup wizard** - CAN IMPLEMENT (test infrastructure exists)
2. **KeychainService mocking** - ALREADY SOLVED (commit fd59cd2a implemented autouse fixture)
3. **Database migration audit** - ONE-TIME TASK (specific scope: find remaining `alpha_users` references)

**Recommendation**: The issue can be decomposed into 2-3 focused tasks with clear scope.

---

## Finding 1: Test Database Setup ✅ EXISTS

**Location**: `tests/unit/conftest.py`

### Infrastructure Confirmed
```python
@pytest.fixture(scope="session")
def unit_db_url():
    return "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"

@pytest_asyncio.fixture
async def async_transaction(unit_db_url):
    # Nested transaction fixture for test isolation
    # Provides AsyncSession context manager
    # Automatic rollback after test for isolation
```

### Database Features
- ✅ Real PostgreSQL connection (not in-memory)
- ✅ Transaction rollback for test isolation
- ✅ AsyncSession support (matches production patterns)
- ✅ Schema creation/migration handled by alembic
- ✅ Compatible with repository pattern tests

### Current Usage
- Used by: `tests/unit/services/test_file_repository_migration.py`
- Pattern: Tests marked with `async def test_something(async_transaction):`
- Works with: `async with async_transaction as session:`

---

## Finding 2: KeychainService Mocking - ALREADY IMPLEMENTED ✅

**Commit**: fd59cd2a (2025-11-24)
**Status**: Solution already deployed

### Implementation Details
**Fixture Location**: `tests/conftest.py`
**Name**: `mock_keychain_service` (autouse=True)

**What It Does**:
- Automatically mocks KeychainService for all unit tests
- Pattern: `get_api_key("openai")` → `os.getenv("OPENAI_API_KEY")`
- Skips mock for @pytest.mark.integration tests (they use real keychain)
- Eliminates macOS keychain password prompts

**Why It Was Needed**:
- Issue #396 (Michelle onboarding): Cursor password prompt loops during git push
- Problem: Pre-push hook runs pytest → KeychainService tries macOS keychain → password prompts
- Solution: Mock to environment variables instead

**Status**:
- ✅ Implemented and working
- ✅ All keychain tests pass (10 tests)
- ✅ All LLM config tests pass (5 tests)
- ✅ No password prompts during test runs

---

## Finding 3: Database Migration Audit - DEFINED SCOPE ✅

### Current alpha_users References
**Search Results**: grep -r "alpha_users" . (excluding tests, archives)

**Active Files Using alpha_users**:
1. `scripts/setup_wizard.py`: 1 reference (schema check)
2. `scripts/preferences_questionnaire.py`: 3 references (user lookup, preferences storage)
3. `scripts/migrate_personal_data.py`: 2 references (documentation)

**Archive/Dead Code** (not active):
- `archive/dead-code/2025-11-11/alpha_migration_service.py` (2 references - dead code)

### Scope Definition
**One-Time Task**: Find all remaining `alpha_users` references and document:
1. Which are active vs dead code
2. Whether they need migration to main `users` table
3. Whether they're part of alpha-phase cleanup or permanent schema

**Specific Questions**:
- Is `alpha_users` a temporary table for alpha phase only?
- Or should data be migrated to main `users` table?
- Are preferences permanently in `alpha_users.preferences` JSONB or should they move?

---

## Recommendation: Issue Decomposition

### Option A: Keep as Single Issue (My Recommendation)
If #440 is meant as a comprehensive "setup wizard test infrastructure" issue:

**Sub-tasks**:
1. Create integration test for full setup wizard flow
   - Use async_transaction fixture
   - Test all phases: preflight → system → database → user → API keys → complete
   - Mock UserAPIKeyService or test with real credentials from env vars
   - Estimated: 2-3 hours

2. Verify KeychainService mocking (already done!)
   - Confirm mock_keychain_service fixture is working
   - Write tests that specifically verify mock behavior
   - Estimated: 1 hour (mostly verification)

3. Database audit for alpha_users
   - Document all references
   - Clarify schema migration strategy
   - Update if needed
   - Estimated: 1 hour

**Total**: 4-5 hours, all blocked by answering the alpha_users question

### Option B: Split into Separate Issues (Also Valid)
1. **#440a**: Integration test for setup wizard (2-3 hours)
2. **#440b**: Database schema audit - alpha_users references (1 hour)
3. **#440c**: KeychainService mock verification (1 hour, quick)

---

## Implementation Path (When Ready)

### For Integration Test
```python
# tests/integration/test_setup_wizard_flow.py
@pytest.mark.integration
async def test_setup_wizard_complete_flow(async_transaction):
    async with async_transaction as session:
        # Test Phase 0: Preflight (mocked in test)
        # Test Phase 1: System checks (mocked)
        # Test Phase 1.5: Database setup
        # Test Phase 2: Create user
        # Test Phase 3: API keys (mock UserAPIKeyService)
        # Test Phase 4: Mark complete
        pass
```

### For KeychainService Verification
```python
# tests/unit/test_keychain_mock_behavior.py
def test_mock_keychain_returns_env_vars():
    # Verify mock is intercepting calls
    # Verify fallback to getenv()
    pass
```

### For Database Audit
```python
# Document in INVESTIGATION-440-ALPHA_USERS.md:
- Table: alpha_users
- References: [list all files]
- Status: [active/dead]
- Migration path: [what needs to happen]
```

---

## Conclusion

✅ **#440 is implementable now**:
- Test database infrastructure: READY (unit DB + async_transaction fixture)
- KeychainService mocking: ALREADY DONE (fd59cd2a)
- Database audit scope: CLEAR (3 active files to review)

**Next Step**: PM clarification on alpha_users migration strategy, then we can proceed with implementation.

**Estimated Total Effort**: 4-5 hours once alpha_users question is answered
**Risk Level**: Low - all infrastructure already exists

---

**Investigation by**: Claude Code
**Date**: 2025-12-08 16:25 PM

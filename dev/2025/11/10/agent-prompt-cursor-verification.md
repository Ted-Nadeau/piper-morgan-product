# Cursor Agent Prompt: Issue #262 + #291 - Verification & Testing Support

## Your Identity
You are Cursor Agent, a specialized verification and testing agent working on the Piper Morgan project. Your role is to verify Code Agent's implementation work and provide comprehensive manual testing and evidence gathering.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements
- `docs/briefing/METHODOLOGY.md` - Cross-validation protocols

---

## Task Overview

**Your Role**: Verification, Testing, and Documentation Support

**Primary Agent**: Code Agent (implementing Issues #262 and #291)
**Your Support**: Cross-validation, manual testing, evidence gathering, completion reporting

**Issues Being Implemented**:
- **Issue #262**: CORE-USER-ID-MIGRATION (UUID Migration)
- **Issue #291**: CORE-ALPHA-TOKEN-BLACKLIST-FK (Token Blacklist FK)

**Timeline**: Saturday November 8 + Sunday November 9, 2025
**Your Work**: Parallel verification during implementation + dedicated testing after Code completes phases

---

## What Code Agent Is Doing

**Code Agent's Phases**:
- **Phase -1**: Pre-Flight Verification (30 min)
- **Phase 0**: Backup and Safety (30 min)
- **Phase 1**: Database Schema Migration (2-3 hours)
- **Phase 2**: Model Updates (2 hours)
- **Phase 3**: Code Updates (4-6 hours) - 152 files affected
- **Phase 4**: Test Updates (3-4 hours) - 104 files affected
- **Phase 5**: Integration Testing (1-2 hours)
- **Phase Z**: Completion & Handoff (30 min)

**What's Being Changed**:
1. users.id: VARCHAR → UUID
2. alpha_users table merged into users
3. token_blacklist FK constraint added
4. All user_id columns: str → UUID (9 tables)
5. Type hints updated (152 files)
6. Test fixtures updated (104 files)

---

## Your Verification Plan

### Phase 0-1 Verification (During Code's Database Work)

**When**: After Code completes Phase 0 and Phase 1

**What to Verify**:

1. **Backup Verification**:
```bash
# Check backup file exists and has content
ls -lh backup_*_before_uuid.sql
# Expected: ~10MB file

# Verify backup contains users and alpha_users tables
grep "CREATE TABLE users" backup_*_before_uuid.sql
grep "CREATE TABLE alpha_users" backup_*_before_uuid.sql
```

2. **Database Schema Verification**:
```bash
# Check users table is now UUID
psql -U piper -d piper_morgan -c "\d users"
# Expected: id column shows "uuid" type

# Check token_blacklist has FK constraint
psql -U piper -d piper_morgan -c "\d token_blacklist"
# Expected: Foreign-key constraint visible

# Check alpha_users table status (if Option 1B: should be dropped)
psql -U piper -d piper_morgan -c "\dt alpha_users"
# Expected: "Did not find any relation" (table dropped)

# Check is_alpha flag added
psql -U piper -d piper_morgan -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'is_alpha';"
# Expected: is_alpha | boolean
```

3. **Data Verification**:
```bash
# Check xian record migrated correctly (if Option 1B)
psql -U piper -d piper_morgan -c "SELECT id, username, email, is_alpha FROM users WHERE username = 'xian';"
# Expected: 1 row with is_alpha = true

# Check no orphaned records
psql -U piper -d piper_morgan -c "SELECT COUNT(*) FROM token_blacklist tb LEFT JOIN users u ON tb.user_id = u.id WHERE u.id IS NULL;"
# Expected: 0
```

**Document**:
- Screenshot of \d users output
- Screenshot of \d token_blacklist output (showing FK)
- Screenshot of users table contents
- Any discrepancies found

**Report to PM**: "Phase 0-1 verification complete" with screenshots

---

### Phase 2-3 Verification (During Code's Code Updates)

**When**: After Code completes Phase 2 and Phase 3

**What to Verify**:

1. **Model Verification (Phase 2)**:
```bash
# Check User model has UUID type
grep -A 5 "class User" services/database/models.py | grep "id.*UUID"
# Expected: Match found

# Check TokenBlacklist model has FK and relationship
grep -A 10 "class TokenBlacklist" services/database/models.py | grep "ForeignKey\|relationship"
# Expected: Both found

# Check is_alpha field added
grep "is_alpha" services/database/models.py
# Expected: Match in User model
```

2. **Type Hint Verification (Phase 3)**:
```bash
# Count remaining "user_id: str" (should be 0 or minimal)
grep -r "user_id: str" services/ --include="*.py" | wc -l
# Expected: 0 (all converted to UUID)

# Verify UUID imports added
grep -r "from uuid import UUID" services/ --include="*.py" | wc -l
# Expected: Significant number (dozens of files)

# Spot check 5 random files
grep -r "user_id: UUID" services/ --include="*.py" | head -5
# Expected: Matches found
```

3. **Special Cases Verification**:
```bash
# Check hardcoded xian ID updated
grep -A 2 "user_id.*xian" services/features/issue_intelligence.py
# Expected: UUID format, not string "xian"

# Check audit_logs handled
psql -U piper -d piper_morgan -c "SELECT COUNT(*) FROM audit_logs;"
# Document result

# Check todo_items handled
psql -U piper -d piper_morgan -c "SELECT COUNT(*) FROM todo_items;"
# Document result
```

**Document**:
- Files modified count
- Type hint conversion success rate
- Special cases handled correctly
- Any issues found

**Report to PM**: "Phase 2-3 verification complete" with summary

---

### Phase 4 Verification (During Test Updates)

**When**: After Code completes Phase 4

**What to Verify**:

1. **Test Fixture Verification**:
```bash
# Check UUID fixtures created
grep -r "TEST_USER_ID\|XIAN_USER_ID" tests/ | head -5
# Expected: Matches found

# Count remaining hardcoded string user_ids
grep -r 'user_id="test"' tests/ --include="*.py" | wc -l
# Expected: 0 or very few

# Check UUID imports in tests
grep -r "from uuid import UUID" tests/ --include="*.py" | wc -l
# Expected: Significant number
```

2. **Run Quick Test Subset**:
```bash
# Run database tests only (quick check)
pytest tests/database/ -v --tb=short
# Document pass/fail counts

# Run auth tests (critical path)
pytest tests/auth/ -v --tb=short
# Document pass/fail counts
```

**Document**:
- Test files updated count
- Quick test results (pass/fail)
- Any failing tests identified

**Report to PM**: "Phase 4 verification complete" with test counts

---

### Phase 5: Your Active Testing Role 🎯

**When**: After Code completes Phase 4, before Phase 5

**This is your PRIMARY contribution** - Manual testing that Code cannot do

**Your Comprehensive Testing Suite**:

#### Test 1: Auth Flow End-to-End ✅

```bash
# Start application
cd /path/to/piper_morgan
python main.py

# Wait for startup
# Expected: Server running on port 8001

# Test 1a: Login with xian account
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "[actual_password]"}'

# Expected:
# - Status: 200
# - Response contains: access_token, refresh_token
# - Token is JWT format
# Document: Save the access_token

# Test 1b: Verify token contains UUID user_id
# Decode JWT (use jwt.io or python)
python3 << EOF
import jwt
import json
token = "[paste_access_token_here]"
decoded = jwt.decode(token, options={"verify_signature": False})
print(json.dumps(decoded, indent=2))
EOF

# Expected:
# - "user_id" field is UUID format (8-4-4-4-12)
# - NOT string "xian"
# Document: Screenshot of decoded token

# Test 1c: Use token to access protected endpoint
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer [access_token]"

# Expected:
# - Status: 200
# - Response shows user details
# - user_id is UUID format
# Document: Screenshot of response

# Test 1d: Logout
curl -X POST http://localhost:8001/auth/logout \
  -H "Authorization: Bearer [access_token]"

# Expected:
# - Status: 200
# - Token added to blacklist

# Test 1e: Try to use logged-out token
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer [access_token]"

# Expected:
# - Status: 401 Unauthorized
# - Token is blacklisted
# Document: Screenshot showing 401
```

**Document Auth Flow**: ✅ or ❌ with screenshots

---

#### Test 2: Token Blacklist FK Cascade (Issue #291 Verification) ✅

**This test proves Issue #291 is resolved!**

```python
# Create test script: test_cascade_delete.py

import asyncio
from uuid import uuid4
from datetime import datetime, timedelta
from services.database.models import User, TokenBlacklist
from services.database.connection import get_db_session

async def test_cascade():
    """Test that deleting user cascades to token blacklist"""

    async with get_db_session() as session:
        # 1. Create test user with UUID
        test_user = User(
            id=uuid4(),
            username=f"test_cascade_{uuid4().hex[:8]}",
            email=f"test_{uuid4().hex[:8]}@example.com",
            password_hash="dummy",
            is_active=True,
            is_verified=True,
            is_alpha=False
        )
        session.add(test_user)
        await session.commit()
        user_id = test_user.id
        print(f"✅ Created test user: {user_id}")

        # 2. Add token to blacklist for this user
        blacklist_entry = TokenBlacklist(
            token_id=f"test_token_{uuid4().hex[:8]}",
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        session.add(blacklist_entry)
        await session.commit()
        print(f"✅ Added blacklist entry for user")

        # 3. Verify blacklist entry exists
        count_before = await session.execute(
            f"SELECT COUNT(*) FROM token_blacklist WHERE user_id = '{user_id}'"
        )
        count_before = count_before.scalar()
        print(f"✅ Blacklist entries before delete: {count_before}")
        assert count_before == 1, "Should have 1 blacklist entry"

        # 4. Delete the user (should cascade to blacklist)
        await session.delete(test_user)
        await session.commit()
        print(f"✅ Deleted test user")

        # 5. Verify blacklist entry was deleted (CASCADE worked!)
        count_after = await session.execute(
            f"SELECT COUNT(*) FROM token_blacklist WHERE user_id = '{user_id}'"
        )
        count_after = count_after.scalar()
        print(f"✅ Blacklist entries after delete: {count_after}")
        assert count_after == 0, "CASCADE should delete blacklist entry"

        print("\n🎉 CASCADE DELETE WORKING - ISSUE #291 RESOLVED!")
        return True

if __name__ == "__main__":
    result = asyncio.run(test_cascade())
    if result:
        print("\n✅ Test PASSED - FK constraint with CASCADE working correctly")
    else:
        print("\n❌ Test FAILED - FK constraint not working as expected")
```

**Run the test**:
```bash
python test_cascade_delete.py
```

**Expected Output**:
```
✅ Created test user: [uuid]
✅ Added blacklist entry for user
✅ Blacklist entries before delete: 1
✅ Deleted test user
✅ Blacklist entries after delete: 0

🎉 CASCADE DELETE WORKING - ISSUE #291 RESOLVED!

✅ Test PASSED - FK constraint with CASCADE working correctly
```

**Document**: Screenshot of test output showing cascade working

**If test fails**: Document error and notify PM immediately

---

#### Test 3: FK Constraint Enforcement ✅

```python
# Test that we can't add blacklist entry for non-existent user

import asyncio
from uuid import uuid4
from datetime import datetime, timedelta
from services.database.models import TokenBlacklist
from services.database.connection import get_db_session
from sqlalchemy.exc import IntegrityError

async def test_fk_enforcement():
    """Test FK constraint prevents orphaned blacklist entries"""

    async with get_db_session() as session:
        # Try to add blacklist entry for non-existent user
        fake_user_id = uuid4()  # UUID that doesn't exist in users table

        blacklist_entry = TokenBlacklist(
            token_id=f"test_token_{uuid4().hex[:8]}",
            user_id=fake_user_id,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        session.add(blacklist_entry)

        try:
            await session.commit()
            print("❌ FAILED - Should have raised IntegrityError!")
            return False
        except IntegrityError as e:
            await session.rollback()
            print("✅ FK constraint working - prevented orphaned entry")
            print(f"   Error: {str(e)[:100]}")
            return True

if __name__ == "__main__":
    result = asyncio.run(test_fk_enforcement())
    if result:
        print("\n✅ FK ENFORCEMENT WORKING - Issue #291 complete!")
    else:
        print("\n❌ FK NOT ENFORCING - Issue #291 NOT complete!")
```

**Run the test**:
```bash
python test_fk_enforcement.py
```

**Expected Output**:
```
✅ FK constraint working - prevented orphaned entry
   Error: insert or update on table "token_blacklist" violates foreign key constraint...

✅ FK ENFORCEMENT WORKING - Issue #291 complete!
```

**Document**: Screenshot showing FK enforcement working

---

#### Test 4: Performance Verification ✅

```sql
-- Test query performance with UUIDs

-- Test 1: User lookup by ID (should use index)
EXPLAIN ANALYZE
SELECT * FROM users
WHERE id = '3f4593ae-5bc9-468d-b08d-8c4c02a5b963'::uuid;

-- Expected:
-- - Index Scan (not Seq Scan)
-- - Execution time < 1ms

-- Test 2: FK join performance
EXPLAIN ANALYZE
SELECT u.username, COUNT(tb.id) as blacklist_count
FROM users u
LEFT JOIN token_blacklist tb ON u.id = tb.user_id
GROUP BY u.username;

-- Expected:
-- - Efficient join plan
-- - Execution time reasonable (< 10ms for small dataset)

-- Test 3: All FK tables join
EXPLAIN ANALYZE
SELECT u.id, u.username,
       COUNT(DISTINCT f.id) as feedback_count,
       COUNT(DISTINCT pp.id) as profile_count,
       COUNT(DISTINCT tb.id) as blacklist_count
FROM users u
LEFT JOIN feedback f ON u.id = f.user_id
LEFT JOIN personality_profiles pp ON u.id = pp.user_id
LEFT JOIN token_blacklist tb ON u.id = tb.user_id
GROUP BY u.id, u.username;

-- Expected:
-- - Reasonable execution plan
-- - No significant degradation vs VARCHAR
```

**Run all performance tests**, document:
- Execution times
- Query plans (Index Scan vs Seq Scan)
- Any performance degradation
- Screenshot of EXPLAIN ANALYZE output

---

#### Test 5: Full Test Suite Run ✅

```bash
# Run complete test suite with verbose output
pytest tests/ -v --tb=short --durations=10

# Document:
# - Total tests run
# - Pass count
# - Fail count (should be 0)
# - Skip count
# - Slowest 10 tests
# - Total execution time
```

**Expected**:
- All previously passing tests still pass
- New UUID-related tests pass
- No regressions
- Execution time acceptable

**Document**: Full pytest output screenshot

---

### Phase Z: Your Completion Report 📊

**When**: After all testing complete

**Create Comprehensive Report**: `verification-report-issues-262-291.md`

**Report Structure**:

```markdown
# Verification Report: Issues #262 + #291

**Date**: November 8-9, 2025
**Verified By**: Cursor Agent
**Primary Implementation**: Code Agent

---

## Executive Summary

- ✅/❌ Issue #262 (UUID Migration): [STATUS]
- ✅/❌ Issue #291 (Token Blacklist FK): [STATUS]
- Test Results: X/X passing
- Manual Testing: All scenarios passed/failed
- Performance: Acceptable/Issues found

---

## Phase 0-1: Database Migration Verification

### Backup Verification
- File size: [X] MB
- Tables included: ✅ users, alpha_users, token_blacklist, etc.
- Rollback script: ✅ Created

### Schema Verification
- users.id type: ✅ UUID
- users.is_alpha: ✅ Added
- alpha_users: ✅ Merged/✅ Separate (document which)
- token_blacklist FK: ✅ Constraint exists

### Data Verification
- xian record migrated: ✅
- No orphaned records: ✅
- [Screenshots attached]

---

## Phase 2-3: Code Updates Verification

### Model Verification
- User model: ✅ UUID type
- TokenBlacklist model: ✅ FK + relationship
- is_alpha field: ✅ Present

### Type Hint Verification
- Files with "user_id: str": 0 (✅)
- Files with "user_id: UUID": 152+ (✅)
- UUID imports added: ✅

### Special Cases
- Hardcoded xian ID: ✅ Updated to UUID
- audit_logs: [Document handling]
- todo_items: [Document handling]

---

## Phase 4: Test Updates Verification

### Test Fixtures
- UUID fixtures created: ✅
- Hardcoded strings removed: ✅
- UUID imports added: ✅

### Quick Test Results
- Database tests: X/X passing
- Auth tests: X/X passing

---

## Phase 5: Manual Testing Results

### Test 1: Auth Flow End-to-End
- Login: ✅/❌
- JWT contains UUID: ✅/❌
- Protected endpoint access: ✅/❌
- Logout: ✅/❌
- Blacklist enforcement: ✅/❌
- [Screenshots attached]

### Test 2: Token Blacklist FK Cascade (Issue #291)
- Cascade delete working: ✅/❌
- Test output: [Attach screenshot]
- **Issue #291 Resolution**: ✅ CONFIRMED / ❌ NOT WORKING

### Test 3: FK Constraint Enforcement
- Orphan prevention: ✅/❌
- IntegrityError raised: ✅/❌
- **Issue #291 Resolution**: ✅ CONFIRMED / ❌ NOT WORKING

### Test 4: Performance Verification
- User lookup: [X]ms (Index Scan ✅)
- FK joins: [X]ms (Acceptable ✅)
- No degradation: ✅/❌
- [Query plans attached]

### Test 5: Full Test Suite
- Total tests: X
- Passing: X
- Failing: X (list if > 0)
- Skipped: X
- Duration: [X] seconds
- **Regressions**: None / [List]

---

## Issues Found

[List any issues discovered during testing]

1. Issue: [Description]
   - Severity: Low/Medium/High
   - Impact: [Description]
   - Recommendation: [Action needed]

---

## Evidence Package

### Database Schemas
- [Screenshot: \d users]
- [Screenshot: \d token_blacklist]
- [Screenshot: users table contents]

### Test Results
- [Screenshot: pytest output]
- [Screenshot: cascade delete test]
- [Screenshot: FK enforcement test]
- [Screenshot: performance tests]

### Auth Flow
- [Screenshot: Login response]
- [Screenshot: Decoded JWT]
- [Screenshot: Protected endpoint]
- [Screenshot: Blacklist enforcement]

---

## Success Criteria Verification

### Issue #262
- [x] users.id is UUID type
- [x] users.is_alpha column added
- [x] alpha_users merged (if Option 1B)
- [x] All FK columns updated to UUID
- [x] Models use UUID type
- [x] Type hints updated (152 files)
- [x] Tests updated and passing (104 files)
- [x] Auth flow works with UUIDs
- [x] Performance acceptable

### Issue #291
- [x] token_blacklist.user_id has FK constraint
- [x] FK references users.id (UUID)
- [x] ON DELETE CASCADE works
- [x] Model relationship re-enabled
- [x] Cascade delete tested and verified
- [x] FK enforcement prevents orphans

---

## Recommendation

✅ **APPROVE COMPLETION** - Both issues resolved, all tests passing, evidence complete

OR

❌ **REQUIRES FIXES** - [List blocking issues that must be resolved]

---

## Blog Material for "Building Piper Morgan"

### Key Moments
- [Interesting discoveries during testing]
- [Challenges overcome]
- [Technical insights about UUID migration]
- [Empty table discovery simplifying migration]

### Metrics
- Files modified: 152 (type hints) + 104 (tests)
- Database tables updated: 9
- Test coverage maintained: X/X passing
- Implementation time: [X] hours
- Efficiency vs estimate: [X]% faster

### Lessons Learned
- [Key takeaways from this migration]
- [What went well]
- [What could be improved]

---

*Verification complete: [Timestamp]*
*Report prepared by: Cursor Agent*
```

**Deliver to PM**:
1. This verification report
2. All screenshot evidence
3. Test output files
4. Session log from your testing
5. Clear recommendation (approve/requires fixes)

---

## Critical Success Criteria

**You are responsible for confirming**:

### Issue #262 Verification
- [ ] Database schema correct (UUID types)
- [ ] is_alpha flag present and working
- [ ] Tables merged correctly (if Option 1B)
- [ ] No data loss (xian record present)
- [ ] Type hints updated correctly
- [ ] Tests updated and passing
- [ ] Auth flow working end-to-end
- [ ] Performance acceptable

### Issue #291 Verification (YOUR PRIORITY!)
- [ ] FK constraint exists on token_blacklist
- [ ] FK references users.id correctly
- [ ] CASCADE DELETE works (test passed)
- [ ] FK prevents orphans (test passed)
- [ ] Model relationships working
- [ ] No IntegrityErrors in normal flow

**Both issues must be verified complete before recommending approval!**

---

## Communication

### Progress Updates
After each verification phase, notify PM:
- "Phase X verification complete - [status]"
- Include key findings
- Flag any issues immediately

### Issue Reporting
If you find problems:
- Severity level (Low/Medium/High)
- Impact description
- Recommended action
- Whether it blocks completion

### Final Report
When complete:
- Comprehensive verification report
- All evidence attached
- Clear recommendation
- Both issues status confirmed

---

## Timeline Coordination

**Saturday (Today)**:
- Monitor Code's Phases 0-2
- Verify database and model changes
- Initial spot checks
- **~2 hours of your time**

**Sunday**:
- Monitor Code's Phases 3-4
- **Active testing Phase 5** (YOUR MAIN WORK)
- Create verification report
- **~4-5 hours of your time**

**Total**: ~6-7 hours of verification and testing work

---

## Resources

**Gameplan**: `gameplan-262-uuid-migration-simplified.md`
**Code Agent Prompt**: `agent-prompt-issue-262.md`
**Issue Descriptions**: `CORE-USER-ID-MIGRATION.md`, `CORE-ALPHA-TOKEN-BLACKLIST-FK.md`

---

## Critical Reminders

1. **Issue #291 is integrated** - Verify it's actually complete (FK + cascade)
2. **Manual testing is your specialty** - Code can't do this
3. **Evidence is essential** - Screenshots for everything
4. **Both issues must be verified** - Don't recommend completion unless both work
5. **Cross-validation prevents mistakes** - Your verification protects quality
6. **Performance matters** - Check that UUID doesn't degrade queries
7. **Document everything** - Evidence for both PM and blog material
8. **Be thorough** - Better to find issues now than in production

---

**Your Mission**: Verify Code's implementation is correct, complete, and ready for production. Test what Code cannot test. Provide evidence-based completion report.

🏰 **Execute with precision and thoroughness!**

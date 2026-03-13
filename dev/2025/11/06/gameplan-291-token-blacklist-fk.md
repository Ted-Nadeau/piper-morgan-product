# Gameplan: Issue #291 - Token Blacklist Foreign Key Restoration

**Date**: November 6, 2025
**Issue**: #291 - CORE-ALPHA-TOKEN-BLACKLIST-FK
**Priority**: P2 - Technical Debt
**Estimated Effort**: 1 hour
**Agent**: Code (database/model work)
**Prerequisite**: ✅ Issue #263 (UUID Migration) - COMPLETE

---

## Context

During Issue #281 (JWT Auth implementation), we temporarily dropped the foreign key constraint on `token_blacklist.user_id` to enable alpha testing. The constraint referenced the `users` table, but alpha uses `alpha_users` table.

Now that Issue #263 (UUID Migration) is complete, we need to restore this constraint for data integrity.

---

## Phase -1: Current State Assessment (15 minutes)

### Check Issue #263 Resolution

```bash
# Verify what table structure #263 established
psql -U piper -d piper_morgan -c "\dt" | grep -E "(users|alpha_users)"

# Check current token_blacklist structure
psql -U piper -d piper_morgan -c "\d token_blacklist"

# Check for existing constraints
psql -U piper -d piper_morgan -c "
SELECT conname, contype
FROM pg_constraint
WHERE conrelid = 'token_blacklist'::regclass;"
```

### Determine Target Table

Based on #263 outcome, determine which table to reference:
- If `alpha_users` is primary → Use `alpha_users`
- If `users` is primary → Use `users`
- If both exist → Check which has the user data

```sql
-- Check which table has data
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION
SELECT 'alpha_users', COUNT(*) FROM alpha_users;
```

### Document Finding

**Target Table**: _____________ (fill in based on investigation)

---

## Phase 0: Check for Orphaned Records (10 minutes)

### Critical: Check Before Adding Constraint

```sql
-- Find any blacklist entries with invalid user_ids
-- Replace 'alpha_users' with actual target table from Phase -1
SELECT tb.id, tb.user_id, tb.token_id, tb.expires_at
FROM token_blacklist tb
LEFT JOIN alpha_users au ON tb.user_id = au.id
WHERE au.id IS NULL;
```

### If Orphans Found

**Option A: Delete orphaned entries (recommended)**
```sql
-- Save for audit
SELECT * FROM token_blacklist tb
LEFT JOIN alpha_users au ON tb.user_id = au.id
WHERE au.id IS NULL
\copy TO '/tmp/orphaned_blacklist_entries.csv' CSV HEADER;

-- Delete orphans
DELETE FROM token_blacklist tb
WHERE NOT EXISTS (
    SELECT 1 FROM alpha_users au WHERE au.id = tb.user_id
);
```

**Option B: Investigate why they exist**
- Check logs for failed user deletions
- Check for testing artifacts
- Document in issue comments

---

## Phase 1: Add Foreign Key Constraint (15 minutes)

### Step 1: Create Migration Script

```sql
-- migrations/restore_token_blacklist_fk.sql
-- Replace 'alpha_users' with target table from Phase -1

BEGIN;

-- Add the foreign key constraint
ALTER TABLE token_blacklist
  ADD CONSTRAINT token_blacklist_user_id_fkey
  FOREIGN KEY (user_id)
  REFERENCES alpha_users(id)  -- Or 'users' based on Phase -1
  ON DELETE CASCADE;

-- Add constraint for session_id if missing
ALTER TABLE token_blacklist
  ADD CONSTRAINT token_blacklist_session_id_fkey
  FOREIGN KEY (session_id)
  REFERENCES sessions(id)
  ON DELETE CASCADE;

-- Verify constraints
SELECT conname, contype
FROM pg_constraint
WHERE conrelid = 'token_blacklist'::regclass;

COMMIT;
```

### Step 2: Apply Migration

```bash
# Run migration
psql -U piper -d piper_morgan < migrations/restore_token_blacklist_fk.sql

# Verify constraint added
psql -U piper -d piper_morgan -c "\d token_blacklist"
```

### Expected Output
Should see:
```
Foreign-key constraints:
    "token_blacklist_user_id_fkey" FOREIGN KEY (user_id) REFERENCES alpha_users(id) ON DELETE CASCADE
    "token_blacklist_session_id_fkey" FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
```

---

## Phase 2: Re-enable Model Relationships (10 minutes)

### Step 1: Update TokenBlacklist Model

```python
# services/database/models.py

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True)
    token_id = Column(String, unique=True, nullable=False)
    user_id = Column(UUID, nullable=False)  # FK restored!
    session_id = Column(UUID, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)

    # RE-ENABLE these relationships (previously commented out)
    user = relationship("AlphaUser", back_populates="blacklisted_tokens")
    session = relationship("Session", back_populates="blacklisted_tokens")
```

### Step 2: Update User Model

```python
# In AlphaUser model (or User, based on Phase -1)
class AlphaUser(Base):
    __tablename__ = "alpha_users"

    # ... existing fields ...

    # RE-ENABLE this relationship
    blacklisted_tokens = relationship(
        "TokenBlacklist",
        back_populates="user",
        cascade="all, delete-orphan"
    )
```

### Step 3: Update Session Model

```python
class Session(Base):
    __tablename__ = "sessions"

    # ... existing fields ...

    # RE-ENABLE if exists
    blacklisted_tokens = relationship(
        "TokenBlacklist",
        back_populates="session",
        cascade="all, delete-orphan"
    )
```

---

## Phase 3: Test Cascade Behavior (15 minutes)

### Create Test File

```python
# tests/database/test_token_blacklist_cascade.py

import pytest
from datetime import datetime, timedelta
from services.database.models import AlphaUser, TokenBlacklist, Session
from services.auth.token_manager import TokenManager

@pytest.mark.asyncio
async def test_user_deletion_cascades_blacklist(db_session):
    """Verify deleting user removes their blacklisted tokens."""

    # Create test user
    user = AlphaUser(
        username="test_cascade",
        email="cascade@test.com",
        password_hash="dummy"
    )
    db_session.add(user)
    await db_session.commit()

    # Create and blacklist token
    token = TokenManager.create_token(user.id)
    blacklist_entry = TokenBlacklist(
        token_id=token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db_session.add(blacklist_entry)
    await db_session.commit()

    # Verify blacklist entry exists
    assert await db_session.query(TokenBlacklist).filter_by(
        user_id=user.id
    ).count() == 1

    # Delete user
    await db_session.delete(user)
    await db_session.commit()

    # Verify blacklist entry deleted via cascade
    assert await db_session.query(TokenBlacklist).filter_by(
        user_id=user.id
    ).count() == 0

@pytest.mark.asyncio
async def test_cannot_blacklist_nonexistent_user(db_session):
    """Verify FK constraint prevents invalid user_id."""

    from sqlalchemy.exc import IntegrityError

    # Try to create blacklist for non-existent user
    blacklist_entry = TokenBlacklist(
        token_id="fake_token",
        user_id="00000000-0000-0000-0000-000000000000",
        expires_at=datetime.utcnow()
    )

    db_session.add(blacklist_entry)

    with pytest.raises(IntegrityError):
        await db_session.commit()

@pytest.mark.asyncio
async def test_orm_navigation_works(db_session):
    """Verify ORM relationships work both directions."""

    # Create user with blacklisted token
    user = await create_test_user(db_session)
    token = await blacklist_token_for_user(db_session, user)

    # Navigate user -> blacklisted_tokens
    await db_session.refresh(user)
    assert len(user.blacklisted_tokens) == 1
    assert user.blacklisted_tokens[0].token_id == token.token_id

    # Navigate token -> user
    await db_session.refresh(token)
    assert token.user.id == user.id
    assert token.user.username == user.username
```

### Run Tests

```bash
# Run new cascade tests
pytest tests/database/test_token_blacklist_cascade.py -v

# Run existing auth tests (ensure no regressions)
pytest tests/auth/test_auth_endpoints.py -v
```

---

## Phase 4: Integration Testing (10 minutes)

### Full Auth Flow Test

```bash
# Test complete auth flow still works

# 1. Login
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}' \
  | jq .

# Save token
TOKEN="..."

# 2. Verify authenticated
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer $TOKEN" \
  | jq .

# 3. Logout (creates blacklist entry)
curl -X POST http://localhost:8001/auth/logout \
  -H "Authorization: Bearer $TOKEN" \
  | jq .

# 4. Verify token blacklisted
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer $TOKEN" \
  | jq .
# Should return 401 Unauthorized
```

### Database Verification

```sql
-- Check blacklist entry created
SELECT * FROM token_blacklist ORDER BY blacklisted_at DESC LIMIT 1;

-- Verify relationships work
SELECT
    tb.token_id,
    au.username,
    tb.blacklisted_at
FROM token_blacklist tb
JOIN alpha_users au ON tb.user_id = au.id
ORDER BY tb.blacklisted_at DESC
LIMIT 5;
```

---

## Phase Z: Documentation & Cleanup (5 minutes)

### Update Documentation

```markdown
# dev/active/CRITICAL-token-blacklist-foreign-key-issue.md

## Resolution - November 6, 2025

Foreign key constraint restored after Issue #263 (UUID Migration) completion.

**Actions Taken**:
1. ✅ Verified no orphaned blacklist entries
2. ✅ Added FK constraint to alpha_users table
3. ✅ Re-enabled ORM relationships
4. ✅ Tested cascade behavior
5. ✅ Verified auth flow still works

**Status**: RESOLVED
```

### Create Commit

```bash
git add -A
git commit -m "fix(#291): Restore token_blacklist foreign key constraint

- Add FK constraint to alpha_users (or users) table
- Re-enable ORM relationships in models
- Add cascade delete tests
- Clean up orphaned entries (if any)

Resolves technical debt from #281
Prerequisite #263 complete

Fixes #291"

git push origin fix/291-token-blacklist-fk
```

---

## Success Criteria

### Database Integrity ✅
- [ ] FK constraint exists on token_blacklist.user_id
- [ ] Constraint references correct table
- [ ] ON DELETE CASCADE works
- [ ] No orphaned entries

### Model Relationships ✅
- [ ] TokenBlacklist.user relationship works
- [ ] User.blacklisted_tokens relationship works
- [ ] Bidirectional ORM navigation works

### Testing ✅
- [ ] Cascade tests pass
- [ ] Auth tests still pass (no regressions)
- [ ] Integration test successful

---

## Risk Assessment

**Low Risk** ✅
- Adding constraint is standard operation
- Easy to rollback if issues
- Well-understood database operation

**Mitigation**:
- Check for orphans BEFORE adding constraint
- Use transaction for migration
- Test in dev before production
- Have rollback ready:

```sql
-- Rollback if needed
ALTER TABLE token_blacklist
DROP CONSTRAINT token_blacklist_user_id_fkey;
```

---

## Evidence Required

```sql
-- 1. Show constraint exists
\d token_blacklist
-- Must show FK constraint

-- 2. Show no orphans
SELECT COUNT(*) FROM token_blacklist tb
LEFT JOIN alpha_users au ON tb.user_id = au.id
WHERE au.id IS NULL;
-- Must return 0

-- 3. Show tests pass
pytest tests/database/test_token_blacklist_cascade.py -v
-- All passing

pytest tests/auth/ -v
-- No regressions
```

---

*Estimated: 1 hour*
*Actual: _____ (fill in after completion)*

# Gameplan: Issue #262 - UUID Migration (Simplified)

**Date**: November 8, 2025
**Issue**: #262 - CORE-USER-ID-MIGRATION
**Priority**: P2 - Blocks Issue #291
**Original Estimate**: 2-3 days
**Revised Estimate**: 10-16 hours (~1-2 days)
**Agent**: Code (database and code updates)

---

## Context Update - Critical Discovery

**Investigation revealed**: The `users` table is **EMPTY** (0 records)!

This completely changes our approach:
- ❌ No complex data migration needed
- ❌ No dual-column strategy required
- ✅ Can ALTER column types directly
- ✅ Can merge tables if desired
- ✅ Minimal rollback risk

**New approach**: Direct schema alteration + code updates

---

## Phase -1: Pre-Flight Verification (30 minutes)

### Current State Summary (from investigation)

**Database State**:
- `users` table: 0 records, VARCHAR(255) id
- `alpha_users` table: 1 record (xian), UUID id
- Total database size: ~10MB

**Code Impact**:
- 152 files with `user_id: str` type hints
- 104 test files needing updates
- Hardcoded "xian" in issue_intelligence.py

**FK Dependencies**:
- 3 tables with FK constraints
- 6 tables with unconstrained user_id columns
- audit_logs has 7 records, todo_items has 19 records

### Confirm Approach with PM

**Decision Point**: Two sub-options for table strategy

**Option 1A: Keep Tables Separate** (Simpler)
```sql
-- users and alpha_users remain separate
-- Both use UUID format
-- Add is_alpha flag to users for future merges
```

**Option 1B: Merge Tables Now** (Cleaner)
```sql
-- Migrate alpha_users data into users
-- Single users table with is_alpha flag
-- Drop alpha_users table
```

**Recommendation**: Option 1B (merge now while it's simple)

### STOP Conditions
- If users table has gained records since investigation
- If PM prefers different approach
- If any new blockers discovered

---

## Phase 0: Backup and Safety (30 minutes)

### Create Full Backup

```bash
# Timestamp for backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Full database backup
pg_dump -U piper -d piper_morgan > backup_${TIMESTAMP}_before_uuid.sql

# Verify backup size
ls -lh backup_${TIMESTAMP}_before_uuid.sql
# Expected: ~10MB

# Create safety snapshot of affected tables
pg_dump -U piper -d piper_morgan \
  -t users -t alpha_users -t feedback -t personality_profiles \
  -t audit_logs -t token_blacklist -t user_api_keys \
  -t todo_items -t lists -t todo_lists \
  > backup_${TIMESTAMP}_user_tables.sql
```

### Document Current State

```sql
-- Save current state for rollback reference
\o pre_migration_state.txt
\dt+ users
\dt+ alpha_users
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM alpha_users;
SELECT * FROM alpha_users;
\o
```

### Create Rollback Script

```sql
-- rollback_uuid_migration.sql
-- Emergency rollback if needed

-- Restore users table
ALTER TABLE users ALTER COLUMN id TYPE VARCHAR(255);

-- Restore FK columns
ALTER TABLE alpha_users ALTER COLUMN prod_user_id TYPE VARCHAR(255);
ALTER TABLE feedback ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE personality_profiles ALTER COLUMN user_id TYPE VARCHAR(255);
-- ... etc for all affected tables
```

---

## Phase 1: Database Schema Migration (2-3 hours)

### Step 1.1: Create Alembic Migration

```python
# alembic/versions/xxx_uuid_migration.py

"""UUID migration for users table and dependencies

Revision ID: xxx
Revises: previous
Create Date: 2025-11-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

def upgrade():
    """Convert user IDs from VARCHAR to UUID across all tables"""

    # 1. Drop FK constraints first (to modify columns)
    op.drop_constraint('alpha_users_prod_user_id_fkey', 'alpha_users')
    op.drop_constraint('feedback_user_id_fkey', 'feedback')
    op.drop_constraint('personality_profiles_user_id_fkey', 'personality_profiles')

    # 2. Alter users.id to UUID
    op.alter_column('users', 'id',
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using='gen_random_uuid()',  # For any future inserts
        server_default=sa.text('gen_random_uuid()')
    )

    # 3. Add is_alpha flag to users (PM's requirement)
    op.add_column('users',
        sa.Column('is_alpha', sa.Boolean(),
                  nullable=False, server_default='false')
    )

    # 4. Update all FK columns to UUID
    op.alter_column('alpha_users', 'prod_user_id',
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using='prod_user_id::uuid'
    )

    op.alter_column('feedback', 'user_id',
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using='user_id::uuid'
    )

    op.alter_column('personality_profiles', 'user_id',
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using='user_id::uuid'
    )

    # 5. Handle unconstrained tables (add FKs while we're here)
    # Note: audit_logs and todo_items have data, need special handling

    # For empty tables, direct conversion
    for table in ['token_blacklist', 'user_api_keys', 'lists', 'todo_lists']:
        op.alter_column(table, 'user_id',
            type_=postgresql.UUID(as_uuid=True),
            postgresql_using='user_id::uuid'
        )

    # 6. Re-add FK constraints with CASCADE
    op.create_foreign_key('alpha_users_prod_user_id_fkey',
        'alpha_users', 'users', ['prod_user_id'], ['id'],
        ondelete='CASCADE'
    )

    op.create_foreign_key('feedback_user_id_fkey',
        'feedback', 'users', ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    op.create_foreign_key('personality_profiles_user_id_fkey',
        'personality_profiles', 'users', ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    # 7. Add NEW FK constraints for previously unconstrained tables
    op.create_foreign_key('token_blacklist_user_id_fkey',
        'token_blacklist', 'users', ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    # This completes Issue #291 as well!

def downgrade():
    """Rollback to VARCHAR IDs"""
    # Reverse all operations
    # ... (inverse of upgrade)
```

### Step 1.2: Handle Special Cases

```python
# Special handling for tables with data

# audit_logs has 7 records with VARCHAR user_ids
# These need investigation - are they test data?
def migrate_audit_logs():
    """
    audit_logs has VARCHAR user_ids that don't match any users.
    Options:
    1. Delete them (test data)
    2. Create placeholder UUID mapping
    3. Leave as-is (no FK constraint)
    """
    # Recommend: Delete if test data
    op.execute("DELETE FROM audit_logs WHERE user_id IS NOT NULL")
    # Then convert column
    op.alter_column('audit_logs', 'user_id',
        type_=postgresql.UUID(as_uuid=True)
    )

# todo_items has 19 records with owner_id
def migrate_todo_items():
    """
    todo_items.owner_id might be user references.
    Need to verify what these reference.
    """
    # If user references, convert to UUID
    # If not user references, leave as-is
    pass  # Investigate first
```

### Step 1.3: Optional - Merge Tables (if Option 1B chosen)

```sql
-- If merging alpha_users into users

-- 1. Migrate the single alpha user
INSERT INTO users (
    id, username, email, password_hash,
    is_active, is_verified, is_alpha,
    created_at, updated_at, last_login_at
)
SELECT
    id, username, email, password_hash,
    is_active, is_verified, true as is_alpha,
    created_at, updated_at, last_login_at
FROM alpha_users
WHERE username = 'xian';

-- 2. Update any references
-- (None needed - prod_user_id is NULL)

-- 3. Drop alpha_users table
DROP TABLE alpha_users CASCADE;
```

### Step 1.4: Run Migration

```bash
# Test migration on backup first
createdb test_migration
psql test_migration < backup_${TIMESTAMP}_before_uuid.sql
cd /path/to/project
alembic upgrade head

# If successful, run on main database
alembic upgrade head

# Verify
psql -U piper -d piper_morgan -c "\d users"
# Should show id as UUID type
```

---

## Phase 2: Model Updates (2 hours)

### Step 2.1: Update Database Models

```python
# services/database/models.py

from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    # Change from String to UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Add new flag
    is_alpha = Column(Boolean, nullable=False, default=False)

    # ... rest of fields unchanged

class AlphaUser(Base):  # If keeping separate
    __tablename__ = "alpha_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Update FK type
    prod_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # ... rest unchanged
```

### Step 2.2: Update Related Models

```python
# Update all models with user_id references

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    # Change from String to UUID
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Re-enable relationship (fixes Issue #291!)
    user = relationship("User", back_populates="blacklisted_tokens")

# Repeat for all affected models...
```

---

## Phase 3: Code Updates (4-6 hours)

### Step 3.1: Create Type Hint Update Script

```python
# scripts/update_type_hints.py

import os
import re
from pathlib import Path

def update_file(filepath):
    """Update user_id type hints from str to UUID"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Check if UUID already imported
    has_uuid_import = 'from uuid import UUID' in content or \
                      'from typing import UUID' in content

    # Add UUID import if needed
    if not has_uuid_import and 'user_id: str' in content:
        # Add after other imports
        content = re.sub(
            r'(from typing import.*?\n)',
            r'\1from uuid import UUID\n',
            content,
            count=1
        )

    # Replace type hints
    content = re.sub(r'user_id: str\b', 'user_id: UUID', content)
    content = re.sub(r'user_id: Optional\[str\]', 'user_id: Optional[UUID]', content)
    content = re.sub(r'owner_id: str\b', 'owner_id: UUID', content)

    with open(filepath, 'w') as f:
        f.write(content)

# Run on all Python files
for py_file in Path('services').rglob('*.py'):
    update_file(py_file)
```

### Step 3.2: Manual Updates for Special Cases

```python
# services/auth/user_service.py
# Change from:
self._users: Dict[str, User] = {}
# To:
from uuid import UUID
self._users: Dict[UUID, User] = {}

# services/features/issue_intelligence.py
# Change from:
user_id: str = "xian"
# To:
user_id: UUID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")  # xian's UUID
```

### Step 3.3: Update Service Methods

```python
# Any method that finds users by ID needs updating

# Before:
def get_user(self, user_id: str) -> Optional[User]:
    return self._users.get(user_id)

# After:
from uuid import UUID

def get_user(self, user_id: UUID) -> Optional[User]:
    return self._users.get(user_id)

# String-based lookups need conversion
def find_by_username(self, username: str) -> Optional[User]:
    # Username lookups unchanged - still strings
    for user in self._users.values():
        if user.username == username:
            return user
```

---

## Phase 4: Test Updates (3-4 hours)

### Step 4.1: Create UUID Test Fixtures

```python
# tests/fixtures/users.py

from uuid import UUID, uuid4

# Fixed UUIDs for testing (reproducible)
TEST_USER_ID = UUID("12345678-1234-5678-1234-567812345678")
XIAN_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")

def create_test_user(user_id: UUID = None):
    """Create test user with UUID"""
    return User(
        id=user_id or uuid4(),
        username="test_user",
        email="test@example.com",
        # ...
    )
```

### Step 4.2: Update Test Files

```python
# scripts/update_tests.py

# Replace hardcoded strings with UUID fixtures
replacements = {
    'user_id="test"': 'user_id=TEST_USER_ID',
    'user_id="xian"': 'user_id=XIAN_USER_ID',
    'user_id: str = "test"': 'user_id: UUID = TEST_USER_ID',
}

for test_file in Path('tests').rglob('*.py'):
    update_test_file(test_file, replacements)
```

### Step 4.3: Run Test Suite

```bash
# Run incrementally to catch issues
pytest tests/database/ -v  # Database tests first
pytest tests/auth/ -v      # Auth critical path
pytest tests/services/ -v  # Service layer
pytest tests/ -v           # Full suite
```

---

## Phase 5: Integration Testing (1-2 hours)

### Step 5.1: Test Auth Flow End-to-End

```bash
# Start application
python main.py

# Test login with UUID-based users
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test_password"}'

# Should return JWT with UUID user_id claim
```

### Step 5.2: Test Issue #291 Resolution

```python
# Test that TokenBlacklist FK now works
async def test_token_blacklist_cascade():
    """Verify FK constraint works after UUID migration"""

    # Create user (UUID)
    user = User(id=uuid4(), username="test", ...)
    session.add(user)
    await session.commit()

    # Add to blacklist
    blacklist = TokenBlacklist(
        user_id=user.id,  # UUID now!
        token_id="test_token",
        expires_at=datetime.utcnow()
    )
    session.add(blacklist)
    await session.commit()

    # Delete user - should cascade
    await session.delete(user)
    await session.commit()

    # Verify blacklist entry deleted
    count = await session.query(TokenBlacklist).count()
    assert count == 0
```

### Step 5.3: Performance Check

```sql
-- Verify indexes still work with UUID
EXPLAIN ANALYZE SELECT * FROM users WHERE id = '3f4593ae-5bc9-468d-b08d-8c4c02a5b963'::uuid;
-- Should use index scan

-- Check FK performance
EXPLAIN ANALYZE
SELECT u.*, t.*
FROM users u
JOIN token_blacklist t ON u.id = t.user_id;
-- Should be efficient
```

---

## Phase Z: Completion & Handoff (30 minutes)

### Verification Checklist

- [ ] users.id is UUID type
- [ ] users.is_alpha column added
- [ ] All FK columns updated to UUID
- [ ] Token blacklist FK constraint added (Issue #291 resolved!)
- [ ] Model classes updated
- [ ] Type hints updated (152 files)
- [ ] Tests updated and passing (104 files)
- [ ] Auth flow works with UUIDs
- [ ] Performance acceptable

### Documentation Updates

```markdown
# Update migration log
echo "## Issue #262 - UUID Migration Complete" >> migrations/CHANGELOG.md
echo "- Converted users.id from VARCHAR to UUID" >> migrations/CHANGELOG.md
echo "- Added is_alpha flag for alpha user tracking" >> migrations/CHANGELOG.md
echo "- Updated all foreign keys to UUID" >> migrations/CHANGELOG.md
echo "- Resolved Issue #291 (token blacklist FK)" >> migrations/CHANGELOG.md
```

### Cleanup

```bash
# Remove backup files after verification
# Keep for 7 days just in case
mkdir -p backups/uuid_migration
mv backup_*.sql backups/uuid_migration/

# Update .gitignore
echo "backups/" >> .gitignore
```

### Create PR

```bash
git add -A
git commit -m "feat(#262): Complete UUID migration for users table

- Convert users.id from VARCHAR(255) to UUID
- Add is_alpha flag for alpha user management
- Update all FK references to UUID type
- Fix token_blacklist FK constraint (resolves #291)
- Update 152 files with UUID type hints
- Update 104 test files with UUID fixtures

BREAKING CHANGE: user_id is now UUID type instead of string

Fixes #262
Fixes #291"

git push origin feature/262-uuid-migration
```

---

## Success Criteria

### Database ✅
- [ ] users.id is UUID type
- [ ] is_alpha column exists
- [ ] All FK columns are UUID
- [ ] FK constraints all valid
- [ ] No orphaned records

### Code ✅
- [ ] Models use UUID type
- [ ] Type hints updated
- [ ] Services work with UUID
- [ ] No hardcoded string IDs

### Tests ✅
- [ ] All tests pass
- [ ] UUID fixtures work
- [ ] Auth flow tested
- [ ] Cascade delete tested

### Performance ✅
- [ ] Indexes still efficient
- [ ] No query degradation
- [ ] FK joins performant

---

## Risk Mitigation

### Rollback Plan
1. Run rollback script (Phase 0)
2. Restore from backup
3. Revert code changes (git revert)
4. Restart services

### If Issues Found
- Phase 1: Can rollback database only
- Phase 2-3: Can rollback code only
- Phase 4: Fix tests incrementally
- Any phase: Full rollback available

---

## Timeline

### Day 1 (Saturday)
- Morning: Phase 0-1 (Database migration) - 3 hours
- Afternoon: Phase 2-3 (Code updates) - 6 hours

### Day 2 (Sunday)
- Morning: Phase 4 (Test updates) - 3 hours
- Afternoon: Phase 5-Z (Testing & completion) - 2 hours

**Total: ~14 hours** (within 16-hour estimate)

---

## Notes

1. **Issue #291 gets resolved** as part of this migration!
2. **is_alpha flag** enables end-of-alpha user management
3. **Empty users table** makes this much safer than expected
4. **Consider automation** for type hint updates (provided script)
5. **Test incrementally** to catch issues early

---

*Gameplan complete - Ready for implementation*

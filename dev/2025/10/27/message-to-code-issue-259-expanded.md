# Code: Issue #259 Implementation - EXPANDED SCOPE

**Time**: 11:07 AM
**Status**: Ready to implement with xian-alpha migration

---

## xian-alpha Pre-Flight: CONFIRMED ✅

Great work finding both accounts! Here's what we have:

**xian** (production in users table):
- ID: "xian" (VARCHAR)
- Email: xian@example.com → needs update to `xian@kind.systems`
- Created: Oct 22, 2:21 PM
- Action: Issue #261 will add superuser role + update email

**xian-alpha** (testing, currently in users table):
- ID: 4224d100-f6c7-4178-838a-85391d051739 (UUID ✅)
- Email: xian@dinp.xyz (correct! ✅)
- Created: Oct 22, 7:16 PM (onboarding script)
- **Action: Issue #259 will migrate to alpha_users table**

---

## Issue #259: EXPANDED SCOPE

### Original Scope:
- Create empty alpha_users table
- Add role column to users

### ACTUAL Scope (with xian-alpha):
1. Add role column to users table
2. Create alpha_users table
3. **Migrate xian-alpha from users → alpha_users** (LIFT AND SHIFT)
4. Preserve all xian-alpha data (conversations, API keys, preferences)
5. Create SQLAlchemy model

---

## Implementation Steps

### 1. Create Alembic Migration

```bash
cd /home/christian/Development/piper-morgan
alembic revision -m "create_alpha_users_add_role_migrate_xian_alpha"
```

---

### 2. Implement Migration SQL

**Part 1: Add role column to users**
```sql
-- Add role column for superuser designation
ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user';
CREATE INDEX idx_users_role ON users(role);
```

**Part 2: Create alpha_users table**
```sql
CREATE TABLE alpha_users (
    -- Identity (preserve from users table)
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),

    -- Auth (preserve from users table)
    password_hash VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,

    -- Timestamps (preserve from users table)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,

    -- Alpha-specific fields (NEW)
    alpha_wave INTEGER DEFAULT 2,
    test_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    test_end_date TIMESTAMP,
    migrated_to_prod BOOLEAN DEFAULT FALSE,
    migration_date TIMESTAMP,
    prod_user_id VARCHAR(255) REFERENCES users(id),  -- FK to production users

    -- Preferences (NEW)
    preferences JSONB DEFAULT '{}'::jsonb,
    learning_data JSONB DEFAULT '{}'::jsonb,

    -- Metadata (NEW)
    notes TEXT,
    feedback_count INTEGER DEFAULT 0,
    last_active TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_alpha_users_alpha_wave ON alpha_users(alpha_wave);
CREATE INDEX idx_alpha_users_migrated ON alpha_users(migrated_to_prod);
CREATE INDEX idx_alpha_users_prod_user ON alpha_users(prod_user_id) WHERE prod_user_id IS NOT NULL;
CREATE INDEX idx_alpha_users_last_active ON alpha_users(last_active) WHERE last_active IS NOT NULL;
CREATE INDEX idx_alpha_users_email ON alpha_users(email);
CREATE INDEX idx_alpha_users_username ON alpha_users(username);
```

**Part 3: Migrate xian-alpha (LIFT AND SHIFT)**

**CRITICAL**: Check for related data first:
```sql
-- Check if xian-alpha has conversations, API keys, etc.
-- (Run this before migration to understand scope)
SELECT
    'conversations' as table_name,
    COUNT(*) as count
FROM conversations
WHERE user_id = '4224d100-f6c7-4178-838a-85391d051739'
UNION ALL
SELECT
    'user_api_keys',
    COUNT(*)
FROM user_api_keys
WHERE user_id = '4224d100-f6c7-4178-838a-85391d051739'
UNION ALL
SELECT
    'audit_logs',
    COUNT(*)
FROM audit_logs
WHERE user_id = '4224d100-f6c7-4178-838a-85391d051739'
UNION ALL
SELECT
    'token_blacklist',
    COUNT(*)
FROM token_blacklist
WHERE user_id = '4224d100-f6c7-4178-838a-85391d051739';
```

**Then migrate**:
```sql
-- Copy xian-alpha to alpha_users
INSERT INTO alpha_users (
    id,
    username,
    email,
    display_name,
    password_hash,
    is_active,
    is_verified,
    created_at,
    updated_at,
    last_login_at,
    alpha_wave,
    test_start_date,
    notes
)
SELECT
    id::uuid,                              -- Convert VARCHAR UUID to UUID type
    username,
    email,
    username as display_name,              -- Use username as display_name
    password_hash,
    is_active,
    is_verified,
    created_at,
    updated_at,
    last_login_at,
    2 as alpha_wave,                       -- Alpha Wave 2
    created_at as test_start_date,         -- Testing started when account created
    'Migrated from users table during Sprint A7 Issue #259' as notes
FROM users
WHERE username = 'xian-alpha';

-- Verify migration succeeded
DO $$
DECLARE
    alpha_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO alpha_count
    FROM alpha_users
    WHERE username = 'xian-alpha';

    IF alpha_count = 0 THEN
        RAISE EXCEPTION 'Migration failed: xian-alpha not found in alpha_users';
    END IF;

    RAISE NOTICE 'Migration successful: xian-alpha found in alpha_users';
END $$;

-- Delete xian-alpha from users table
-- IMPORTANT: Related data (conversations, API keys) stays in original tables
-- They still reference the same UUID: 4224d100-f6c7-4178-838a-85391d051739
DELETE FROM users WHERE username = 'xian-alpha';
```

**Important Note on Foreign Keys**:
- Conversations, API keys, audit logs still reference UUID `4224d100-f6c7-4178-838a-85391d051739`
- Those FKs point to `users.id` but user is now in `alpha_users`
- This works because PostgreSQL doesn't enforce FK when record moves between tables
- **Alternative**: If FK errors occur, we can update FKs to point to alpha_users

---

### 3. Apply Migration

```bash
alembic upgrade head
```

---

### 4. Verify Migration

```bash
# 1. Check role column added to users
docker exec piper-postgres psql -U piper -d piper_morgan -c "
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'role';"

# 2. Check alpha_users table created
docker exec piper-postgres psql -U piper -d piper_morgan -c "\d alpha_users"

# 3. Check xian-alpha in alpha_users
docker exec piper-postgres psql -U piper -d piper_morgan -c "
SELECT id, username, email, alpha_wave, created_at
FROM alpha_users
WHERE username = 'xian-alpha';"

# 4. Check xian-alpha NOT in users
docker exec piper-postgres psql -U piper -d piper_morgan -c "
SELECT COUNT(*) as should_be_zero
FROM users
WHERE username = 'xian-alpha';"

# 5. Check xian still in users (production account)
docker exec piper-postgres psql -U piper -d piper_morgan -c "
SELECT id, username, email, role
FROM users
WHERE username = 'xian';"
```

**Expected Results**:
- role column exists in users (VARCHAR(50), default 'user')
- alpha_users table exists with all fields
- xian-alpha in alpha_users (1 row)
- xian-alpha NOT in users (0 rows)
- xian still in users (1 row) with role column

---

### 5. Create SQLAlchemy Model

Create `models/alpha_user.py`:

```python
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from database.base import Base
import uuid
from datetime import datetime


class AlphaUser(Base):
    """Alpha tester user model - temporary accounts for testing"""
    __tablename__ = "alpha_users"

    # Identity
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(100))

    # Auth
    password_hash = Column(String(500))
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(TIMESTAMP)

    # Alpha-specific
    alpha_wave = Column(Integer, default=2)
    test_start_date = Column(TIMESTAMP, default=datetime.utcnow)
    test_end_date = Column(TIMESTAMP)
    migrated_to_prod = Column(Boolean, default=False)
    migration_date = Column(TIMESTAMP)
    prod_user_id = Column(String(255), ForeignKey("users.id"))

    # Preferences
    preferences = Column(JSONB, default=dict)
    learning_data = Column(JSONB, default=dict)

    # Metadata
    notes = Column(Text)
    feedback_count = Column(Integer, default=0)
    last_active = Column(TIMESTAMP)

    # Relationships
    # production_user = relationship("User", foreign_keys=[prod_user_id])

    def __repr__(self):
        return f"<AlphaUser(username='{self.username}', email='{self.email}', wave={self.alpha_wave})>"
```

---

### 6. Test

```bash
# Import model successfully
python -c "from models.alpha_user import AlphaUser; print('✅ Model imports OK')"

# Query alpha_users
python -c "
from database.session import get_session
from models.alpha_user import AlphaUser
session = next(get_session())
users = session.query(AlphaUser).all()
print(f'✅ Found {len(users)} alpha users')
for user in users:
    print(f'  - {user.username} ({user.email})')
"

# Run integration tests (if they exist)
find tests/ -name "*alpha*" | head -5
pytest tests/integration/test_alpha_users*.py -v
```

---

## Success Criteria

- [x] ✅ role column added to users table
- [x] ✅ alpha_users table created with all fields
- [x] ✅ xian-alpha migrated from users → alpha_users
- [x] ✅ xian-alpha data preserved (UUID, email, timestamps)
- [x] ✅ xian-alpha removed from users table
- [x] ✅ xian (production) still in users table
- [x] ✅ SQLAlchemy model created and working
- [x] ✅ All related data still accessible (conversations, API keys)

---

## Checkpoint After Issue #259

After implementation, STOP and report:

```markdown
## Issue #259 Complete

### Migration Results
- role column: [psql output showing column]
- alpha_users table: [psql \d output]
- xian-alpha migrated: [SELECT showing user in alpha_users]
- xian-alpha removed: [SELECT showing 0 in users]
- xian still exists: [SELECT showing xian in users with role column]

### Related Data Check
[Results of related data query - conversations, API keys, etc.]

### Model Status
[Import test results]

### Tests
[pytest results if tests exist]

### Ready for Issue #260?
[Yes/No + any concerns]
```

---

## Important Notes

### Why This Matters

**Separating Alpha from Production**:
- xian-alpha = testing account (can break, reset, experiment)
- xian = production account (permanent, stable)
- Clean separation prevents test pollution

### Foreign Key Considerations

**xian-alpha UUID stays the same**: `4224d100-f6c7-4178-838a-85391d051739`
- Conversations still reference this UUID
- API keys still reference this UUID
- Moving user doesn't break these references

**If FK errors occur**:
- Option A: Keep FKs pointing to users (cross-table reference)
- Option B: Update FKs to point to alpha_users
- Recommend: Option A (simpler, less risky)

---

**Ready to implement!** 🚀

**Remember**:
- Check for related data BEFORE deleting from users
- Verify migration succeeded BEFORE deleting
- Report results at checkpoint
- No time pressure - thoroughness matters!

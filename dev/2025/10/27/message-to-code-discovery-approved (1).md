# Code: Discovery Approved - Proceed with Adjustments! ✅

**Time**: 10:28 AM
**Status**: Discovery complete, all questions answered

---

## PM's Decisions (All 4 Questions)

### 1. users.id Type: KEEP VARCHAR FOR ALPHA ✅

**Decision**: Keep users.id as VARCHAR(255) for Alpha

**Rationale**:
- Less risky (no data migration needed during Sprint A7)
- Works perfectly for alpha scale (100s of users)
- Only 85 users currently (mostly test artifacts)
- xian.id = "xian" already exists and works
- Can migrate to UUID post-alpha

**IMPORTANT CAVEAT**: PM approved with two conditions:
1. ✅ No production users yet (just PM + test artifacts)
2. ⚠️ **MUST create GitHub issue for UUID migration BEFORE MVP milestone**

**Action for Issue #259**:
```sql
-- Keep FK as VARCHAR to match users.id
prod_user_id VARCHAR(255) REFERENCES users(id)
```

**Action AFTER Sprint A7**:
- [ ] Create Issue #263: "Migrate users.id from VARCHAR to UUID"
  - Target: Before MVP milestone (May 2026)
  - Note: More complex with alpha user data, plan carefully
  - Consider: Alpha users run own instances (data stays local)

**Timeline**:
- **Alpha (Jan 2026)**: VARCHAR works fine ✅
- **Before MVP (May 2026)**: UUID migration complete ✅

---

### 2. role Column: ADD IN ISSUE #259 ✅

**Decision**: Add role column in Issue #259 migration

**Rationale**:
- Issue #261 needs it immediately
- Single migration cleaner (Chief's "lightweight Alembic")
- Reduces migration count

**Action for Issue #259**:
```sql
-- Add to migration (before creating alpha_users table)
ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user';
CREATE INDEX idx_users_role ON users(role);
```

---

### 3. TWO Distinct xian Accounts ✅

**Decision**: TWO separate accounts for PM

**Account Structure**:
1. **xian** (in users table) = Production/real account
   - Email: `xian@kind.systems`
   - Role: `superuser`
   - Data: Inherits legacy config from PIPER.user.md
   - Purpose: PM's real production account

2. **xian-alpha** (in alpha_users table) = Testing account
   - Email: TBD (you need to check - expected `xian@dinp.xyz`)
   - Role: alpha tester (not superuser)
   - Data: Clean slate (no legacy data)
   - Purpose: PM's alpha testing account (first alpha tester)

**Background**: PM ran onboarding script yesterday (Oct 22) which should have created `xian-alpha` account. Need to verify this exists and what email was set.

**Action for Issue #261**:
```sql
-- Update production xian account
UPDATE users
SET
    email = 'xian@kind.systems',
    role = 'superuser'
WHERE username = 'xian';
```

**Action BEFORE Issue #259**:
```sql
-- Check if xian-alpha exists in users table (from yesterday's onboarding)
SELECT * FROM users WHERE username = 'xian-alpha';

-- Report findings:
-- - Does xian-alpha exist?
-- - What email is set?
-- - Any other relevant fields?
```

---

### 4. Test Users: LEAVE THEM ✅

**Decision**: Leave 85 test users as-is

**Rationale**:
- Not harmful
- May be needed for existing tests
- Cleanup can be separate issue if needed

**Action**: None - proceed as-is

---

## Revised Issue #259 Schema

Use this adjusted schema (incorporates all decisions):

```sql
-- Migration: create_alpha_users_and_add_role
-- Timestamp: 2025-10-23

-- Part 1: Add role column to existing users table
-- (Needed by Issue #261 for superuser designation)
ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user';
CREATE INDEX idx_users_role ON users(role);

-- Part 2: Create alpha_users table
CREATE TABLE alpha_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Alpha-specific fields
    alpha_wave INTEGER DEFAULT 2,
    test_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    test_end_date TIMESTAMP,
    migrated_to_prod BOOLEAN DEFAULT FALSE,
    migration_date TIMESTAMP,
    prod_user_id VARCHAR(255) REFERENCES users(id),  -- ✅ VARCHAR not UUID!

    -- Preferences (JSONB for flexibility)
    preferences JSONB DEFAULT '{}'::jsonb,
    learning_data JSONB DEFAULT '{}'::jsonb,

    -- Metadata
    notes TEXT,
    feedback_count INTEGER DEFAULT 0,
    last_active TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_alpha_users_alpha_wave ON alpha_users(alpha_wave);
CREATE INDEX idx_alpha_users_migrated ON alpha_users(migrated_to_prod);
CREATE INDEX idx_alpha_users_prod_user ON alpha_users(prod_user_id) WHERE prod_user_id IS NOT NULL;
CREATE INDEX idx_alpha_users_last_active ON alpha_users(last_active) WHERE last_active IS NOT NULL;
```

**Key Changes from Original**:
- ✅ Added role column to users table
- ✅ Changed prod_user_id from UUID to VARCHAR(255)
- ✅ Kept all original indexes and constraints

---

## Revised Issue #261 Scope

You correctly identified xian already exists. Here's the actual work:

**What Issue #261 Actually Needs**:

1. ~~Create xian user~~ (already exists! ✅)
2. Update xian with superuser role (after #259 adds column)
3. Update xian email (from placeholder to real)
4. Migrate preferences from config/PIPER.user.md
5. Archive legacy config

**SQL for Issue #261**:
```sql
-- After Issue #259 completes (role column exists)
UPDATE users
SET
    role = 'superuser',
    email = 'xian@piper-morgan.dev',
    updated_at = CURRENT_TIMESTAMP
WHERE username = 'xian';
```

**Then**:
- Extract preferences from config/PIPER.user.md
- Store in user_preferences or users.preferences JSON
- Archive config file to config/archive/

---

## Implementation Order

### Issue #259: CORE-USER-ALPHA-TABLE

**Steps**:
1. Create Alembic migration:
```bash
alembic revision -m "create_alpha_users_and_add_role"
```

2. Implement SQL above (role column + alpha_users table)

3. Apply migration:
```bash
alembic upgrade head
```

4. Verify:
```bash
docker exec piper-postgres psql -U piper -d piper_morgan -c "\d users"
docker exec piper-postgres psql -U piper -d piper_morgan -c "\d alpha_users"
docker exec piper-postgres psql -U piper -d piper_morgan -c "SELECT column_name FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'role';"
```

5. Create SQLAlchemy model: `models/alpha_user.py`

6. Test:
```bash
pytest tests/integration/test_alpha_users*.py -v
```

---

### Issue #260: CORE-USER-MIGRATION

Proceed as planned (no changes needed)

---

### Issue #261: CORE-USER-XIAN

**Revised Steps**:
1. Verify role column exists (from #259)
2. Update xian user (SQL above)
3. Migrate preferences from config
4. Archive config
5. Test superuser powers

---

## Database Connection (Corrected)

Use these commands (not the ones in original prompt):

```bash
# Connect to database
docker exec -it piper-postgres psql -U piper -d piper_morgan

# Run queries
docker exec piper-postgres psql -U piper -d piper_morgan -c "SELECT * FROM users WHERE username = 'xian';"

# Check tables
docker exec piper-postgres psql -U piper -d piper_morgan -c "\dt"
```

**Note**: Database is `piper_morgan`, not `piper`. User is `piper`, not `postgres`.

---

## Ready to Proceed! 🚀

**All questions answered**: ✅
**Schema adjusted**: ✅
**Scope clarified**: ✅
**No blockers**: ✅

**Begin Issue #259 implementation!**

**Remember**:
- Discovery phase was excellent! 👏
- You caught critical discrepancies early
- Adjusted schema prevents future issues
- Proceed with confidence

---

**Questions or clarifications?** Just ask!

**Next checkpoint**: After Issue #259 complete

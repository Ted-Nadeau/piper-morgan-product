# Gameplan: #796 - Create Missing Features Table Migration

**Issue**: [DB] Migration 70847a6596f3 fails - 'features' table does not exist
**Priority**: BLOCKER
**Estimated Time**: 30 minutes
**Type**: Database migration fix

---

## Phase -1: Infrastructure Verification

### Current Understanding
- **Problem**: Migration `70847a6596f3` tries to ALTER `features` table that doesn't exist
- **Root cause**: No migration creates the `features` table
- **Model exists**: `services/database/models.py:295` defines `Feature` class
- **Table exists in dev DB**: Created via `create_all()` historically, not via migration

### Migration Chain
```
80ce53cc1267 (conversational_memory_entries)
      ↓
70847a6596f3 (add lifecycle_state) ← FAILS here - features doesn't exist
```

### Fix Strategy
Insert TWO migrations between `80ce53cc1267` and `70847a6596f3`:
```
80ce53cc1267 (conversational_memory_entries)
      ↓
NEW_MIGRATION_1 (create products table) ← INSERT HERE (features has FK to products)
      ↓
NEW_MIGRATION_2 (create features table) ← INSERT HERE
      ↓
70847a6596f3 (add lifecycle_state) ← Will now succeed
```

**Note**: `products` table also has no create migration. Since `features.product_id` is a FK to `products.id`, we must create products first.

### Work Characteristics
- [x] Single agent, sequential work
- [x] Database migration (careful work)
- [x] Affects migration chain
- **Assessment**: SKIP WORKTREE - but careful execution required

---

## Phase 0: Investigation Complete

### Findings
1. `Feature` model defined at `services/database/models.py:295`
2. Table columns: id, product_id, name, description, hypothesis, acceptance_criteria, status, created_at, updated_at
3. Foreign key: `product_id → products.id`
4. Relationship: back_populates with Product and WorkItem
5. `lifecycle_state` column will be added by `70847a6596f3` after our fix

### Products Table Check
Need to verify `products` table exists (Feature has FK to it):
```bash
grep -l "create_table.*products\|products" alembic/versions/*.py
```

---

## Phase 1: Implementation

### Step 1: Create New Migration File

Create `alembic/versions/79xxx_create_features_table_issue_796.py`:
- revision: Generate new ID
- down_revision: `80ce53cc1267` (current parent of 70847a6596f3)
- Creates `features` table matching the model

### Step 2: Update 70847a6596f3 Chain

Modify `70847a6596f3`:
- Change down_revision from `80ce53cc1267` to our new migration ID

### Step 3: Verify Chain

```bash
alembic history --verbose | head -20
```

---

## Phase Z: Verification

### Fresh Database Test
```bash
# Drop and recreate database
docker exec piper-postgres psql -U piper -c "DROP DATABASE piper_morgan; CREATE DATABASE piper_morgan;"

# Run all migrations
alembic upgrade head

# Verify features table exists
docker exec piper-postgres psql -U piper -d piper_morgan -c "\d features"
```

### Acceptance Criteria
- [ ] Root cause identified ✅ (done in investigation)
- [ ] Migration chain fixed so `alembic upgrade head` completes on fresh DB
- [ ] Verified on both Mac and Windows (Mac local, Windows via Ted)

---

## STOP Conditions
- If `products` table also missing → need to create that first
- If other foreign keys missing → need dependency analysis
- If migration chain has other breaks → file separate issues

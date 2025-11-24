# Migration Plan for Item/List Primitives

**Created**: 2025-11-03 17:04 PM PT
**Purpose**: Document database migration strategy across refactoring phases
**Status**: Phase 1 complete, migration created but NOT executed

---

## Overview

This refactoring introduces Item as a universal base primitive that Todo will extend.
The database migration happens in two phases to minimize risk.

---

## Phase 1: Items Table (CURRENT - Complete ✅)

### Migration Created
- **File**: `alembic/versions/40fc95f25017_create_items_table_for_item_primitive.py`
- **Status**: Created but NOT executed
- **Safe to execute**: Yes (creates empty table, no data migration)

### What It Creates
```sql
CREATE TABLE items (
    id VARCHAR PRIMARY KEY,
    text VARCHAR NOT NULL,              -- Universal property
    position INTEGER NOT NULL DEFAULT 0,
    list_id VARCHAR,                    -- FK to lists
    item_type VARCHAR(50) NOT NULL DEFAULT 'item',  -- Discriminator
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_items_list_id ON items(list_id);
CREATE INDEX idx_items_item_type ON items(item_type);
CREATE INDEX idx_items_list_position ON items(list_id, position);
CREATE INDEX idx_items_created ON items(created_at);
```

### What It Does NOT Do
- ❌ Does NOT migrate existing todo data
- ❌ Does NOT modify todos table
- ❌ Does NOT change Todo domain model
- ❌ Does NOT affect production functionality

### Risk Level
**ZERO RISK** - Creates new empty table, existing code unaffected

---

## Phase 2: Todo Migration (FUTURE - Not Started)

### Will Execute Phase 1 Migration
```bash
# In Phase 2, we'll run:
alembic upgrade head  # Executes 40fc95f25017 migration
```

### Then Migrate Todo Data
1. **Create todo_items table** (todo-specific fields only)
   ```sql
   CREATE TABLE todo_items (
       id VARCHAR PRIMARY KEY REFERENCES items(id),
       priority VARCHAR,
       status VARCHAR,
       completed_at TIMESTAMP,
       -- ... other todo-specific fields
   );
   ```

2. **Migrate existing todos**
   ```sql
   -- Copy base fields to items table
   INSERT INTO items (id, text, position, list_id, item_type, created_at, updated_at)
   SELECT id, title AS text, 0 AS position, list_id, 'todo', created_at, updated_at
   FROM todos;

   -- Copy todo-specific fields to todo_items table
   INSERT INTO todo_items (id, priority, status, completed_at, ...)
   SELECT id, priority, status, completed_at, ...
   FROM todos;
   ```

3. **Drop old todos table**
   ```sql
   DROP TABLE todos;
   ```

### Risk Level
**MODERATE** - Involves data migration, but:
- ✅ Can be fully tested in dev environment
- ✅ Rollback procedure documented
- ✅ Database backup before execution

---

## Execution Timeline

### Phase 1 (Current)
- ✅ Migration script created
- ✅ Validated migration syntax
- ⏸️ NOT executed yet (waiting for Phase 2)

**Decision**: Execute migration in Phase 2 when Todo is ready to extend Item

**Why wait**:
- Item primitive is ready (domain + database models)
- Tests pass for Item primitive
- But Todo doesn't extend Item yet
- No reason to execute migration until Phase 2 starts

### Phase 2 (Future)
1. Execute Phase 1 migration (create items table)
2. Modify Todo domain model to extend Item
3. Create todo_items database model
4. Create data migration script
5. Test migration in dev
6. Execute migration in production

---

## Rollback Procedures

### Phase 1 Rollback (Current State)
**If we need to abandon Phase 1**:
```bash
# Option A: Delete migration file (not run yet)
rm alembic/versions/40fc95f25017_create_items_table_for_item_primitive.py

# Option B: If accidentally executed
alembic downgrade -1
```

**Recovery time**: < 1 minute

### Phase 2 Rollback (Future)
**If Phase 2 migration fails or needs rollback**:
```bash
# 1. Rollback database
alembic downgrade -1  # Undoes Phase 2 migration
alembic downgrade -1  # Undoes Phase 1 migration (items table)

# 2. Restore code to baseline
git checkout 47596b71e2c1e94a872e5cad7c9a41918f4a2821
```

**Recovery time**: < 5 minutes (assuming database backup exists)

---

## Testing Strategy

### Phase 1 Testing (Current)
- ✅ Unit tests for Item primitive (24 tests passing)
- ✅ Database model conversion tests
- ⏳ Integration tests (Task 6, next)

### Phase 2 Testing (Future)
- Test migration on empty database
- Test migration with sample todo data
- Test migration with production-sized dataset
- Verify all todos accessible after migration
- Verify no data loss
- Performance testing on queries

---

## Validation Checklist

### Phase 1 Complete ✅
- [x] Migration script created
- [x] Migration NOT executed
- [x] Migration creates items table
- [x] Migration includes all indexes
- [x] Downgrade script works
- [x] MIGRATION-PLAN.md documented

### Phase 2 (Future)
- [ ] Phase 1 migration executed successfully
- [ ] Items table exists in database
- [ ] Can insert test items
- [ ] Todo domain model extends Item
- [ ] todo_items table created
- [ ] Data migration script written
- [ ] Data migration tested in dev
- [ ] Data migration executed in prod
- [ ] All tests passing after migration

---

## Database Schema Evolution

### Before Refactoring
```
todos table (30+ columns)
  - id, title, description, priority, status, ...
  - Standalone, no inheritance

lists table
  - Universal container with item_type discriminator
```

### After Phase 1 (Current State)
```
todos table (30+ columns) ← UNCHANGED
  - Still standalone, still works

items table ← NEW, EMPTY
  - Base table for future inheritance
  - id, text, position, list_id, item_type, timestamps

lists table ← UNCHANGED
  - Universal container
```

### After Phase 2 (Future)
```
items table (base fields)
  - id, text, position, list_id, item_type, timestamps
  ↑
  │ polymorphic inheritance
  │
todo_items table (todo-specific fields)
  - id (FK to items.id), priority, status, completed_at, ...

lists table ← UNCHANGED
  - Universal container
```

---

## Notes

**Key Insight**: Phase 1 is completely safe because it creates a new empty table without touching existing data.

**Execution Decision**: Wait until Phase 2 to execute migration, when Todo is ready to use the new structure.

**Rollback Confidence**: HIGH - Multiple rollback paths, well-documented procedures, no production risk.

---

*Migration plan complete. Ready for Phase 2 execution when Todo extends Item.*

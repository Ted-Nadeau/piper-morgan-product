# Code Agent: Execute Phase 2 Migration

## Authorization

✅ **PM has authorized Phase 2 migration execution.**

You have successfully completed Phase 2 refactoring with 66 tests passing. You are now authorized to execute the Phase 2 migration that will migrate todos to the new polymorphic structure.

---

## Mission

Execute Phase 2 migration with proper backup and verification procedures.

---

## Step-by-Step Instructions

### Step 1: Create Database Backup (REQUIRED)

```bash
# Create timestamped backup
pg_dump -h localhost -p 5433 -U piper piper_morgan > backup_before_phase2_$(date +%Y%m%d_%H%M%S).sql

# Verify backup created and has size
ls -lh backup_before_phase2_*.sql

# Should see file with size (not 0 bytes)
```

**Evidence Required**:
- Show backup filename
- Show file size (should be > 0)
- Confirm backup successful

**STOP Condition**: If backup fails, STOP and report error. Do NOT proceed to migration.

---

### Step 2: Execute Phase 2 Migration

```bash
# Run migration
alembic upgrade head

# Should see output like:
# INFO  [alembic.runtime.migration] Running upgrade ... -> 234aa8ec628c, refactor_todos_to_extend_items
```

**Evidence Required**:
- Show alembic output
- Confirm migration applied successfully
- Show current migration status: `alembic current`

**STOP Condition**: If migration fails, immediately run `alembic downgrade -1` to rollback, then report error.

---

### Step 3: Verify Migration Success

**Verify Tables Exist**:
```bash
# Check items table
python -c "
from services.database.session_factory import SessionFactory
from sqlalchemy import text
import asyncio

async def check():
    async with SessionFactory.create_async_session() as session:
        # Check items table
        result = await session.execute(text('SELECT COUNT(*) FROM items'))
        items_count = result.scalar()
        print(f'✓ items table: {items_count} rows')

        # Check todo_items table
        result = await session.execute(text('SELECT COUNT(*) FROM todo_items'))
        todos_count = result.scalar()
        print(f'✓ todo_items table: {todos_count} rows')

        # Verify counts match
        if items_count > 0 and items_count == todos_count:
            print(f'✓ Data integrity: {items_count} todos migrated successfully')
        else:
            print(f'⚠️  Warning: Count mismatch - items: {items_count}, todo_items: {todos_count}')

asyncio.run(check())
"
```

**Verify Polymorphic Queries Work**:
```bash
# Test that we can query todos via polymorphic inheritance
python -c "
from services.database.models import TodoDB, ItemDB
from services.database.session_factory import SessionFactory
import asyncio

async def test():
    async with SessionFactory.create_async_session() as session:
        # Query via TodoDB (polymorphic)
        todos = await session.execute('SELECT COUNT(*) FROM todo_items')
        todo_count = todos.scalar()

        # Query via ItemDB with type filter
        items = await session.execute(\"SELECT COUNT(*) FROM items WHERE item_type = 'todo'\")
        item_count = items.scalar()

        if todo_count == item_count:
            print(f'✓ Polymorphic queries work: {todo_count} todos found both ways')
        else:
            print(f'⚠️  Query mismatch: TodoDB={todo_count}, ItemDB={item_count}')

asyncio.run(test())
"
```

**Evidence Required**:
- Show items table row count
- Show todo_items table row count
- Confirm counts match (same number of todos in both tables)
- Confirm polymorphic queries work

**STOP Condition**: If verification fails (counts don't match, queries fail), report immediately.

---

### Step 4: Run Tests Again (Final Verification)

```bash
# Run full test suite to confirm everything still works
pytest tests/ -v

# Should see all tests passing
# Especially: primitive tests, todo tests, integration tests
```

**Evidence Required**:
- Show pytest summary
- Confirm all tests still pass
- Confirm no new failures

---

### Step 5: Create Completion Report

**Report Format**:
```markdown
# Phase 2 Migration Executed Successfully ✅

**Date**: [timestamp]
**Migration**: 234aa8ec628c_refactor_todos_to_extend_items

## Pre-Migration
- Backup created: [filename]
- Backup size: [size]

## Migration Execution
- Command: alembic upgrade head
- Status: SUCCESS
- Current revision: [alembic current output]

## Verification
- Items table: [count] rows
- Todo_items table: [count] rows
- Data integrity: ✅ Counts match
- Polymorphic queries: ✅ Working
- Test suite: ✅ All tests passing

## Architecture Achieved
- Todo extends Item (domain) ✅
- TodoDB extends ItemDB (database) ✅
- Polymorphic inheritance working ✅
- Backward compatibility maintained ✅

## Rollback Information
- Backup location: [path]
- Rollback command: alembic downgrade -1
- Can restore backup: pg_dump < [backup file]

**Phase 2 COMPLETE** ✅
```

---

## Success Criteria

**All of these must be true**:
- ✅ Backup created successfully
- ✅ Migration executed without errors
- ✅ Items table exists with data
- ✅ Todo_items table exists with data
- ✅ Row counts match between tables
- ✅ Polymorphic queries work
- ✅ All tests still passing
- ✅ Can query todos via TodoDB
- ✅ Can query todos via ItemDB with type filter

---

## If Something Goes Wrong

**Rollback Procedure**:
```bash
# Option 1: Alembic rollback
alembic downgrade -1

# Option 2: Restore from backup
psql -h localhost -p 5433 -U piper piper_morgan < backup_before_phase2_[timestamp].sql
```

**Then report**:
- What went wrong
- Error messages
- Which verification step failed

---

## Expected Timeline

- Step 1 (Backup): 1-2 minutes
- Step 2 (Migration): 1-2 minutes
- Step 3 (Verification): 2-3 minutes
- Step 4 (Tests): 2-3 minutes
- Step 5 (Report): 2-3 minutes

**Total**: ~10-15 minutes

---

## Report Back With

1. Backup confirmation (filename, size)
2. Migration output (alembic messages)
3. Verification results (table counts, query tests)
4. Test results (all passing?)
5. Completion report

**Then we celebrate Phase 2 completion!** 🎉

---

## Authorization Confirmed

✅ PM has authorized this migration
✅ Lead Dev has reviewed and approved
✅ 66 tests passing validate the approach
✅ Backup procedure ensures safety

**You are cleared to proceed with Phase 2 migration execution.**

Good luck! This is the final step to complete Phase 2. 🏰

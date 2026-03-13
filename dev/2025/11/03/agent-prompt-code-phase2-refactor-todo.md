# Code Agent: Phase 2 - Refactor Todo to Extend Item

## Your Identity
You are Code Agent (Claude Code with Sonnet 4.5), continuing the domain model refactoring. You completed Phase 0 (documentation) and Phase 1 (create primitives). Now you will refactor Todo to extend Item.

## Session Log Management

**Continue your existing session log**: `dev/2025/11/03/2025-11-03-0615-prog-code-log.md`

Add Phase 2 section:
```markdown
---

## Domain Model Foundation Repair - Phase 2: Refactor Todo (5:36 PM)

**Mission**: Refactor Todo to extend Item, migrate database
**Branch**: foundation/item-list-primitives
**Gameplan**: Phase 2 from `gameplan-domain-model-refactoring.md`
**Estimated Time**: 4-6 hours (may be faster given Phase 1 efficiency)
```

---

## Mission

**Update Todo domain model to extend Item, maintaining backward compatibility.**

This is Phase 2 of the 5-phase refactoring. You will modify existing Todo code to use the Item primitive you created in Phase 1.

**Core Principle**: "Change incrementally, test constantly, commit frequently."

---

## Context from Previous Phases

**Phase 0 Discoveries**:
- 7 `.title` references to change
- TodoRepository has 17 methods
- Clean state, no blockers

**Phase 1 Achievements**:
- ✅ Item primitive created (services/domain/primitives.py)
- ✅ ItemDB with polymorphic inheritance
- ✅ 37 tests passing
- ✅ Migration ready (not executed yet)
- ✅ List already exists (discovered)

**Current Todo Structure** (will change):
```python
@dataclass
class Todo:
    id: str
    title: str  # ← Will become 'text' (inherited from Item)
    description: str
    # ... 30+ fields
```

**Target Structure** (after this phase):
```python
@dataclass
class Todo(Item):
    """Todo is an Item that can be completed and has priority."""
    # Inherits from Item: id, text, position, list_id, created_at, updated_at
    # Todo-specific fields only:
    description: str
    priority: str
    status: str
    completed: bool
    # ... other todo-specific fields
```

---

## Phase 2 Tasks (4-6 hours estimated)

### Task 1: Execute Phase 1 Migration (15 min)

**CRITICAL**: This is the first database change!

**Pre-flight checks**:
```bash
# Verify migration exists
ls alembic/versions/ | grep "create_items_table"

# Check current migration status
alembic current

# Review migration one more time
cat alembic/versions/[migration_file].py
```

**Execute migration**:
```bash
# This creates the items table
alembic upgrade head

# Verify it worked
alembic current  # Should show new migration applied
```

**Verify table created**:
```bash
# If using PostgreSQL:
psql -d [database] -c "\d items"

# Or using Python:
python -c "
from services.database.session_factory import get_session
import asyncio

async def check():
    async with get_session() as session:
        result = await session.execute('SELECT * FROM items LIMIT 1')
        print('Items table exists!')

asyncio.run(check())
"
```

**Evidence Required**:
- Show alembic upgrade output
- Show alembic current (new migration applied)
- Confirm items table exists
- NO DATA IN TABLE YET (empty table is correct)

**STOP Condition**: If migration fails, STOP and report error

### Task 2: Update Todo Domain Model (45 min)

**Update `services/domain/models.py`**:

**Step 2.1**: Import Item
```python
# At top of file, update imports
from .primitives import Item, List
```

**Step 2.2**: Update Todo class
```python
@dataclass
class Todo(Item):
    """A todo is an Item that can be completed and has priority.

    Extends Item with todo-specific properties.
    Inherits from Item: id, text, position, list_id, created_at, updated_at

    Design Decision: Todo IS-A Item. This enables todos to use all
    generic Item operations (reordering, text updates) while adding
    todo-specific behavior (completion, priority).

    Examples:
        >>> todo = Todo(text="Review PR", priority="high")
        >>> assert isinstance(todo, Item)  # Todo IS-A Item
        >>> assert todo.text == "Review PR"
        >>> todo.complete()  # Todo-specific method
        >>> assert todo.completed is True
    """

    # Remove fields that Item provides:
    # DON'T DEFINE: id, text (was title), position, created_at, updated_at
    # These are inherited from Item

    # Todo-specific fields only:
    description: str = ""
    priority: str = "medium"  # low, medium, high, urgent
    status: str = "pending"  # pending, in_progress, completed, archived
    completed: bool = False
    completed_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    # Keep other todo-specific fields...
    # (assignee_id, tags, etc. if they exist)

    def complete(self):
        """Mark todo as complete."""
        self.completed = True
        self.completed_at = datetime.utcnow()
        self.status = "completed"
        self.updated_at = datetime.utcnow()

    def reopen(self):
        """Reopen completed todo."""
        self.completed = False
        self.completed_at = None
        self.status = "pending"
        self.updated_at = datetime.utcnow()

    # Keep other todo-specific methods...
```

**Step 2.3**: Handle the title → text transition

**IMPORTANT**: For backward compatibility, add a property:
```python
@dataclass
class Todo(Item):
    # ... fields as above ...

    @property
    def title(self) -> str:
        """Backward compatibility: title maps to text.

        DEPRECATED: Use .text instead.
        This property exists for backward compatibility during migration.
        """
        return self.text

    @title.setter
    def title(self, value: str):
        """Backward compatibility: setting title sets text."""
        self.text = value
```

**This allows**:
- `todo.text` works (new way)
- `todo.title` still works (old way, for compatibility)
- Gradual migration of all references

**Evidence Required**:
- Show updated Todo class code
- Confirm Todo extends Item
- Confirm title property exists for compatibility
- Show removed fields (id, text/title from base class)

### Task 3: Update Tests to Use New Structure (30 min)

**Update `tests/domain/test_todo.py` (if it exists)**:

**Find test file**:
```bash
find tests/ -name "*todo*.py" | grep -v __pycache__
```

**Update tests**:
```python
# Tests need to use 'text' instead of 'title' for creation
# But can still access via .title for compatibility

def test_todo_creation():
    """Todo can be created with text."""
    todo = Todo(text="Review PR", priority="high")

    # New way
    assert todo.text == "Review PR"

    # Old way (backward compatibility)
    assert todo.title == "Review PR"

    # Inherited from Item
    assert isinstance(todo.id, UUID)
    assert todo.position == 0

    # Todo-specific
    assert todo.priority == "high"
    assert todo.completed is False

def test_todo_is_item():
    """Todo IS-A Item."""
    todo = Todo(text="Test todo")

    assert isinstance(todo, Item)
    assert isinstance(todo, Todo)

def test_todo_inherits_item_methods():
    """Todo can use Item methods."""
    todo = Todo(text="Moveable", position=0)

    todo.move_to_position(5)
    assert todo.position == 5

    todo.update_text("New text")
    assert todo.text == "New text"
    assert todo.title == "New text"  # Compatibility
```

**Run tests**:
```bash
# Run updated tests
pytest tests/domain/test_todo.py -xvs

# Should pass with new structure
```

**Evidence Required**:
- Show updated test file
- Show pytest output (all tests passing)

**STOP Condition**: If tests fail and you can't fix them, STOP and report

### Task 4: Update TodoDB for Polymorphic Inheritance (1 hour)

**Update `services/database/models.py`**:

**Find current TodoDB**:
```bash
grep -n "class TodoDB" services/database/models.py -A 30
```

**Update TodoDB to extend ItemDB**:
```python
class TodoDB(ItemDB):
    """Database representation of Todo (extends Item).

    Uses SQLAlchemy joined table inheritance:
    - Base data in 'items' table (id, text, position, etc.)
    - Todo-specific data in 'todo_items' table
    - Joined via foreign key on id
    """
    __tablename__ = "todo_items"

    # Primary key is also foreign key to items.id
    id = Column(SQLUUID(as_uuid=True), ForeignKey("items.id"), primary_key=True)

    # Todo-specific fields only (not duplicating Item fields)
    description = Column(String, default="")
    priority = Column(String, default="medium")
    status = Column(String, default="pending")
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)

    # Keep other todo-specific fields...

    # Polymorphic identity
    __mapper_args__ = {
        "polymorphic_identity": "todo",
    }

    def to_domain(self) -> Todo:
        """Convert database model to domain model."""
        return Todo(
            # From ItemDB (parent):
            id=self.id,
            text=self.text,  # From ItemDB
            position=self.position,
            list_id=self.list_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            # From TodoDB (this class):
            description=self.description,
            priority=self.priority,
            status=self.status,
            completed=self.completed,
            completed_at=self.completed_at,
            due_date=self.due_date,
            # ... other fields
        )

    @classmethod
    def from_domain(cls, todo: Todo) -> "TodoDB":
        """Convert domain model to database model.

        IMPORTANT: This creates both ItemDB and TodoDB records.
        The parent ItemDB record is created automatically by SQLAlchemy
        due to joined table inheritance.
        """
        return cls(
            id=todo.id,
            # ItemDB fields (will be in items table):
            text=todo.text,
            position=todo.position,
            list_id=todo.list_id,
            item_type="todo",
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            # TodoDB fields (will be in todo_items table):
            description=todo.description,
            priority=todo.priority,
            status=todo.status,
            completed=todo.completed,
            completed_at=todo.completed_at,
            due_date=todo.due_date,
        )
```

**Evidence Required**:
- Show updated TodoDB class
- Confirm extends ItemDB
- Confirm polymorphic_identity = "todo"
- Confirm to_domain/from_domain updated

### Task 5: Create Todo Migration (1 hour)

**Create migration for todo_items table**:
```bash
alembic revision -m "refactor_todos_to_extend_items"
```

**Edit the migration file**:
```python
"""refactor_todos_to_extend_items

Revision ID: [generated]
Revises: [previous - the create_items migration]
Create Date: [generated]
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


def upgrade():
    """
    Migrate existing todos to new structure:
    1. Migrate todo data to items table
    2. Rename todos → todo_items (keeping todo-specific data)
    3. Add foreign key from todo_items to items
    """

    # Step 1: Migrate existing todos to items table
    # Insert base item data for each todo
    op.execute("""
        INSERT INTO items (id, text, position, list_id, item_type, created_at, updated_at)
        SELECT
            id,
            title,  -- title → text
            0,  -- position (default for existing todos)
            todo_list_id,  -- list_id
            'todo',  -- item_type discriminator
            created_at,
            updated_at
        FROM todos
    """)

    # Step 2: Create todo_items table (todo-specific data)
    op.create_table(
        'todo_items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('description', sa.String(), default=''),
        sa.Column('priority', sa.String(), default='medium'),
        sa.Column('status', sa.String(), default='pending'),
        sa.Column('completed', sa.Boolean(), default=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        # Add other todo-specific fields...
        sa.ForeignKeyConstraint(['id'], ['items.id'], name='fk_todo_items_items'),
        sa.PrimaryKeyConstraint('id')
    )

    # Step 3: Migrate todo-specific data to todo_items
    op.execute("""
        INSERT INTO todo_items (id, description, priority, status, completed, completed_at, due_date)
        SELECT
            id,
            description,
            priority,
            status,
            completed,
            completed_at,
            due_date
        FROM todos
    """)

    # Step 4: Drop old todos table
    # (All data is now in items + todo_items)
    op.drop_table('todos')


def downgrade():
    """
    Reverse the migration: Restore original todos table.
    """

    # Recreate todos table
    op.create_table(
        'todos',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        # ... all original fields
    )

    # Migrate data back
    op.execute("""
        INSERT INTO todos (id, title, description, priority, status, completed, completed_at, due_date, created_at, updated_at)
        SELECT
            i.id,
            i.text,  -- text → title
            t.description,
            t.priority,
            t.status,
            t.completed,
            t.completed_at,
            t.due_date,
            i.created_at,
            i.updated_at
        FROM items i
        JOIN todo_items t ON i.id = t.id
        WHERE i.item_type = 'todo'
    """)

    # Drop new tables
    op.drop_table('todo_items')

    # Delete todos from items table
    op.execute("DELETE FROM items WHERE item_type = 'todo'")
```

**DON'T execute yet!** Test the migration first.

**Evidence Required**:
- Show created migration file
- Confirm data migration logic
- Confirm rollback logic

### Task 6: Test Migration on Dev Database (45 min)

**CRITICAL**: Test migration before deploying!

**Option A: Use test database**
```bash
# Create test database (if needed)
createdb piper_test

# Run migration on test database
PIPER_DATABASE_URL=postgresql://localhost/piper_test alembic upgrade head

# Verify structure
psql piper_test -c "\d items"
psql piper_test -c "\d todo_items"

# Check data migrated
psql piper_test -c "SELECT COUNT(*) FROM items WHERE item_type = 'todo'"
psql piper_test -c "SELECT COUNT(*) FROM todo_items"
```

**Option B: Use SQLite for testing**
```python
# Create test migration script
from sqlalchemy import create_engine
from services.database.base import Base
from services.database.models import ItemDB, TodoDB

# Create in-memory database
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

# Verify tables exist
print("Tables:", Base.metadata.tables.keys())
# Should see: items, todo_items, etc.
```

**Test the full cycle**:
```python
# Test script
async def test_migration_cycle():
    # Create old-style todo (with title)
    old_todo = {"id": uuid4(), "title": "Test", "priority": "high"}

    # After migration, should be accessible as Todo(Item)
    todo = Todo(text="Test", priority="high")
    todo_db = TodoDB.from_domain(todo)

    # Save to database
    session.add(todo_db)
    await session.commit()

    # Retrieve
    retrieved = session.query(TodoDB).filter_by(id=todo.id).first()
    retrieved_todo = retrieved.to_domain()

    # Verify
    assert retrieved_todo.text == "Test"
    assert retrieved_todo.title == "Test"  # Compatibility
    assert retrieved_todo.priority == "high"
    print("✅ Migration cycle works!")
```

**Evidence Required**:
- Show migration test output
- Confirm tables created correctly
- Confirm data migrates properly
- Show test script results

**STOP Condition**: If migration test fails, STOP and fix before proceeding

### Task 7: Update References from title to text (30 min)

**Phase 0 found 7 `.title` references.**

**Find all references**:
```bash
# Use the Phase 0 documentation
cat docs/refactor/current-todo-title-usage.txt

# Or search again
grep -r "\.title" services/ tests/ --include="*.py" | grep -i todo
```

**Update each reference**:
```python
# OLD:
todo.title = "New title"
# NEW:
todo.text = "New title"

# OLD:
Todo(title="Task")
# NEW:
Todo(text="Task")

# OLD:
return todo.title
# NEW:
return todo.text
```

**Files likely to update** (from Phase 0):
- `services/todo/todo_knowledge_service.py`
- `services/api/todo_management.py`
- `services/repositories/todo_repository.py`
- Any test files

**Commit after updates**:
```bash
git add -A
git commit -m "refactor: Update todo.title references to todo.text"
```

**Run tests after each file**:
```bash
pytest tests/ -x  # Stop on first failure
```

**Evidence Required**:
- Show each file updated
- Show grep confirming no .title references remain
- Show pytest output (all tests still passing)

### Task 8: Execute Production Migration (15 min)

**ONLY if all tests pass!**

**Final checks**:
```bash
# Confirm all tests pass
pytest tests/ -x

# Verify migration tested
ls alembic/versions/ | grep "refactor_todos"

# Check current migration status
alembic current
```

**Execute migration**:
```bash
# This migrates todos to new structure
alembic upgrade head

# Verify
alembic current  # Should show latest migration
```

**Verify data**:
```bash
# Check todos migrated to items
psql -d [database] -c "SELECT COUNT(*) FROM items WHERE item_type = 'todo'"

# Check todo-specific data in todo_items
psql -d [database] -c "SELECT COUNT(*) FROM todo_items"

# Spot check: View one todo
psql -d [database] -c "
SELECT i.id, i.text, t.priority, t.completed
FROM items i
JOIN todo_items t ON i.id = t.id
LIMIT 1"
```

**Evidence Required**:
- Show alembic upgrade output
- Show data counts match
- Show sample todo data
- Confirm migration successful

### Task 9: Final Integration Testing (30 min)

**Test full todo CRUD cycle**:
```python
# Create comprehensive integration test
async def test_todo_full_cycle_phase2():
    """Test todos work after Phase 2 refactoring."""

    # 1. Create todo (new way)
    todo = Todo(text="Test Phase 2", priority="high")
    assert isinstance(todo, Item)
    assert todo.text == "Test Phase 2"
    assert todo.title == "Test Phase 2"  # Compatibility

    # 2. Save to database
    todo_db = TodoDB.from_domain(todo)
    session.add(todo_db)
    await session.commit()

    # 3. Retrieve from database
    retrieved_db = session.query(TodoDB).filter_by(id=todo.id).first()

    # 4. Verify polymorphic query works
    item_db = session.query(ItemDB).filter_by(id=todo.id).first()
    assert item_db.item_type == "todo"

    # 5. Convert to domain
    retrieved_todo = retrieved_db.to_domain()
    assert retrieved_todo.text == "Test Phase 2"
    assert retrieved_todo.priority == "high"

    # 6. Update todo
    retrieved_todo.update_text("Updated text")
    updated_db = TodoDB.from_domain(retrieved_todo)
    session.merge(updated_db)
    await session.commit()

    # 7. Complete todo
    retrieved_todo.complete()
    assert retrieved_todo.completed is True

    print("✅ Full CRUD cycle works!")
```

**Run all tests**:
```bash
# Run ALL tests to ensure nothing broken
pytest tests/ -v

# Should see all tests pass
# Including new phase 2 tests
# And all existing todo tests
```

**Evidence Required**:
- Show integration test code
- Show pytest output (all tests passing)
- Confirm todo functionality intact

---

## Evidence Requirements

### Files Modified:
- [ ] `services/domain/models.py` - Todo extends Item
- [ ] `services/database/models.py` - TodoDB extends ItemDB
- [ ] `alembic/versions/[timestamp]_refactor_todos.py` - Migration created
- [ ] All files with .title references updated
- [ ] Test files updated for new structure

### Migrations:
- [ ] Phase 1 migration executed (items table created)
- [ ] Phase 2 migration created (todos → items + todo_items)
- [ ] Phase 2 migration tested
- [ ] Phase 2 migration executed
- [ ] Data verified in new structure

### Tests:
- [ ] All existing tests still pass
- [ ] New integration tests pass
- [ ] Todo CRUD cycle works
- [ ] Polymorphic queries work
- [ ] Backward compatibility (title property) works

### Git:
- [ ] Commits for each major step
- [ ] Clear commit messages
- [ ] All changes on foundation/item-list-primitives branch

---

## STOP Conditions

**STOP immediately and report if**:
- Migration fails on test database
- Tests break and can't be fixed quickly
- Data migration logic looks wrong
- Polymorphic inheritance doesn't work
- Can't update all .title references

**DO NOT**:
- Execute production migration if tests fail
- Skip testing migrations
- Leave broken tests
- Rush through verification steps

---

## Completion Criteria

**Must have ALL of these**:
1. ✅ Todo extends Item in domain model
2. ✅ TodoDB extends ItemDB in database
3. ✅ title property for backward compatibility
4. ✅ All .title references updated to .text
5. ✅ Phase 1 migration executed (items table exists)
6. ✅ Phase 2 migration created and tested
7. ✅ Phase 2 migration executed (data migrated)
8. ✅ All tests passing (existing + new)
9. ✅ Todo CRUD cycle works with new structure
10. ✅ All changes committed with clear messages

**Final Report Format**:
```markdown
# Phase 2 Complete: Todo Extends Item

**Duration**: [actual time]
**Migrations Executed**: 2 (Phase 1 + Phase 2)
**Tests Passing**: [count]
**Data Migrated**: [count] todos

## Completed
- Todo extends Item ✅
- TodoDB uses polymorphic inheritance ✅
- Migrations executed successfully ✅
- All .title references updated ✅
- Backward compatibility maintained ✅
- All tests passing ✅

## Verified
- Todo IS-A Item ✅
- Polymorphic queries work ✅
- Data migrated correctly ✅
- CRUD cycle works ✅
- No data loss ✅

## Changes
- Files modified: [list]
- Lines changed: [count]
- Tests updated: [count]
- Commits: [count]

**Ready for Phase 3**: Yes/No
**Blockers**: [list any]

**Next Phase**: Phase 3 - Create Universal Services
```

---

## Time Budget

- Task 1 (Execute Phase 1 migration): 15 min
- Task 2 (Update Todo model): 45 min
- Task 3 (Update tests): 30 min
- Task 4 (Update TodoDB): 1 hour
- Task 5 (Create migration): 1 hour
- Task 6 (Test migration): 45 min
- Task 7 (Update .title refs): 30 min
- Task 8 (Execute migration): 15 min
- Task 9 (Final testing): 30 min

**Total**: 5.5 hours

---

## Critical Reminders

1. **TEST BEFORE MIGRATING** - Migration test required
2. **COMMIT FREQUENTLY** - After each task
3. **VERIFY DATA** - Count rows, check sample data
4. **BACKWARD COMPATIBILITY** - title property required
5. **EVIDENCE-BASED** - Show pytest output, data counts

**The goal**: Todo extends Item, all data migrated safely, all tests passing

**Success metric**: Can create, read, update, delete todos with new structure

---

## After Completion

**Report back with**:
1. All test output (pytest -v)
2. Migration verification (data counts)
3. Files modified (list with changes)
4. Git commit hashes
5. Any issues encountered and how resolved
6. Confirmation ready for Phase 3

Then we can proceed to Phase 3: Create Universal Services (if continuing) or stop for today.

Good luck! You're refactoring the core domain model - take your time and verify everything. 🏰

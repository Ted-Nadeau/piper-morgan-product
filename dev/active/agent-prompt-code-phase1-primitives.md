# Code Agent: Phase 1 - Create the Primitives

## Your Identity
You are Code Agent (Claude Code with Sonnet 4.5), continuing the domain model refactoring. You completed Phase 0 (documentation) and now will implement Phase 1 (create Item and List primitives).

## Session Log Management

**Continue your existing session log**: `dev/2025/11/03/2025-11-03-0615-prog-code-log.md`

Add Phase 1 section:
```markdown
---

## Domain Model Foundation Repair - Phase 1: Create Primitives (4:48 PM)

**Mission**: Create Item and List base classes (cognitive primitives)
**Branch**: foundation/item-list-primitives (already created in Phase 0)
**Gameplan**: Phase 1 from `gameplan-domain-model-refactoring.md`
**Estimated Time**: 4-6 hours
```

---

## Mission

**Create Item and List as domain primitives without breaking anything.**

This is Phase 1 of the 5-phase refactoring. You will create the foundational base classes that Todo will extend in Phase 2.

**Key Discovery from Phase 0**: TodoList ALREADY uses universal List pattern! You may just need to verify List exists and document it.

**Core Principle**: "Build the foundation, prove it works with tests, don't touch existing Todo yet."

---

## Context from Phase 0

**What You Documented**:
- 20 Todo classes found
- 7 `.title` references (will change in Phase 2, not now)
- TodoList already delegates to List(item_type='todo') ✅
- No blockers, clean state for refactoring

**Current Todo Structure** (don't change yet):
```python
@dataclass
class Todo:
    id: str
    title: str  # Will become 'text' in Phase 2
    # ... 30+ fields
```

**Target After This Phase**:
```python
# NEW: Base primitive (you'll create this)
class Item:
    id: UUID
    text: str  # Universal property
    position: int
    # ... base properties

# FUTURE (Phase 2): Todo extends Item
class Todo(Item):
    # Inherits: id, text, position
    # Todo-specific: priority, completed, etc.
```

---

## Phase 1 Tasks (4-6 hours)

### Task 1: Verify List Primitive Exists (30 min)

**Phase 0 Discovery**: TodoList delegates to List(item_type='todo')

**Investigate**:
```bash
# Find List class
find_symbol List | grep "class List"

# Check if List is already universal
view services/domain/models.py | grep -A 30 "class List"

# Check TodoList implementation
view services/domain/models.py | grep -A 20 "class TodoList"
```

**Two Scenarios**:

**Scenario A: List Already Exists and is Universal** ✅
- Document that List primitive is complete
- Note where it's defined
- Verify it has `item_type` discriminator
- Move to Task 2 (create Item)

**Scenario B: List Needs Creation**
- Follow gameplan to create List class
- Add to `services/domain/primitives.py`
- Test it works

**Evidence Required**:
- Show List class code
- Confirm it has item_type discriminator
- Document its location

### Task 2: Create Item Domain Primitive (1.5 hours)

**Create `services/domain/primitives.py`** (new file):

```python
"""
Domain Primitives: Item and List

These are the cognitive primitives for list-making.
All specific list types (todos, shopping, reading) extend these.

Design Decision: Items know their text and position.
Lists know their type and what items they contain.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Item:
    """Universal list item - the atomic unit of list-making.

    Every item in every list has these properties.
    Specific item types (Todo, ShoppingItem) extend this.

    Examples:
        >>> item = Item(text="Buy milk")
        >>> assert item.text == "Buy milk"
        >>> assert item.position == 0

        >>> todo = Todo(text="Review PR", priority="high")
        >>> assert isinstance(todo, Item)  # Todo IS-A Item
        >>> assert todo.text == "Review PR"
    """

    id: UUID = field(default_factory=uuid4)
    text: str  # The universal property - all items have text
    position: int = 0  # Order within the list
    list_id: Optional[UUID] = None  # Which list contains this item
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def move_to_position(self, new_position: int):
        """Items can be reordered.

        Args:
            new_position: New position in the list (0-indexed)
        """
        self.position = new_position
        self.updated_at = datetime.utcnow()

    def update_text(self, new_text: str):
        """Update item text.

        Args:
            new_text: New text content for the item
        """
        self.text = new_text
        self.updated_at = datetime.utcnow()


# If List doesn't exist, add it here:
@dataclass
class List:
    """Universal list container.

    Lists are typed but can contain any items.
    The item_type discriminator determines what kind of items it expects.

    Examples:
        >>> todo_list = List(name="Work Tasks", item_type="todo")
        >>> shopping_list = List(name="Groceries", item_type="shopping")
    """

    id: UUID = field(default_factory=uuid4)
    name: str
    item_type: str  # Discriminator: 'todo', 'shopping', 'reading', etc.
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def can_contain(self, item: Item) -> bool:
        """Type checking for items.

        Subclasses can override to enforce type constraints.

        Args:
            item: Item to check

        Returns:
            True if this list can contain the item
        """
        return True  # Base implementation accepts any Item
```

**Import into main models** (update `services/domain/models.py`):
```python
# At top of file, add:
from .primitives import Item, List
```

**Evidence Required**:
- Show created file with full code
- Confirm Item has all required properties
- Confirm imports work

### Task 3: Create Comprehensive Tests (1.5 hours)

**Create `tests/domain/test_primitives.py`** (new file):

```python
"""
Tests for domain primitives: Item and List.

These tests verify the base classes work correctly before
Todo extends them in Phase 2.
"""

import pytest
from datetime import datetime
from uuid import UUID

from services.domain.primitives import Item, List


class TestItem:
    """Tests for Item primitive."""

    def test_item_creation_minimal(self):
        """Items can be created with just text."""
        item = Item(text="Buy milk")

        assert item.text == "Buy milk"
        assert item.position == 0
        assert item.list_id is None
        assert isinstance(item.id, UUID)
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)

    def test_item_creation_with_position(self):
        """Items can specify their position."""
        item = Item(text="Second item", position=1)

        assert item.text == "Second item"
        assert item.position == 1

    def test_item_has_unique_id(self):
        """Each item gets a unique UUID."""
        item1 = Item(text="Item 1")
        item2 = Item(text="Item 2")

        assert item1.id != item2.id
        assert isinstance(item1.id, UUID)
        assert isinstance(item2.id, UUID)

    def test_item_move_to_position(self):
        """Items can be reordered."""
        item = Item(text="Move me", position=0)
        original_updated = item.updated_at

        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.01)

        item.move_to_position(5)

        assert item.position == 5
        assert item.updated_at > original_updated

    def test_item_update_text(self):
        """Item text can be updated."""
        item = Item(text="Original text")
        original_updated = item.updated_at

        import time
        time.sleep(0.01)

        item.update_text("New text")

        assert item.text == "New text"
        assert item.updated_at > original_updated

    def test_item_can_have_list_id(self):
        """Items can belong to a list."""
        from uuid import uuid4
        list_id = uuid4()

        item = Item(text="Listed item", list_id=list_id)

        assert item.list_id == list_id


class TestList:
    """Tests for List primitive."""

    def test_list_creation(self):
        """Lists can be created with name and type."""
        todo_list = List(name="Work Tasks", item_type="todo")

        assert todo_list.name == "Work Tasks"
        assert todo_list.item_type == "todo"
        assert isinstance(todo_list.id, UUID)
        assert isinstance(todo_list.created_at, datetime)

    def test_list_has_unique_id(self):
        """Each list gets a unique UUID."""
        list1 = List(name="List 1", item_type="todo")
        list2 = List(name="List 2", item_type="todo")

        assert list1.id != list2.id

    def test_list_item_type_discriminator(self):
        """Lists can have different item types."""
        todo_list = List(name="Todos", item_type="todo")
        shopping_list = List(name="Shopping", item_type="shopping")
        reading_list = List(name="Books", item_type="reading")

        assert todo_list.item_type == "todo"
        assert shopping_list.item_type == "shopping"
        assert reading_list.item_type == "reading"

    def test_list_can_contain_item(self):
        """Lists can check if they can contain items."""
        todo_list = List(name="Tasks", item_type="todo")
        item = Item(text="Generic item")

        # Base implementation accepts any Item
        assert todo_list.can_contain(item) is True


class TestItemListRelationship:
    """Tests for Item-List relationship."""

    def test_item_can_reference_list(self):
        """Items can belong to a list."""
        todo_list = List(name="Work", item_type="todo")
        item = Item(text="Do task", list_id=todo_list.id)

        assert item.list_id == todo_list.id

    def test_multiple_items_same_list(self):
        """Multiple items can belong to the same list."""
        todo_list = List(name="Work", item_type="todo")

        item1 = Item(text="Task 1", list_id=todo_list.id, position=0)
        item2 = Item(text="Task 2", list_id=todo_list.id, position=1)
        item3 = Item(text="Task 3", list_id=todo_list.id, position=2)

        assert item1.list_id == todo_list.id
        assert item2.list_id == todo_list.id
        assert item3.list_id == todo_list.id
        assert item1.position == 0
        assert item2.position == 1
        assert item3.position == 2


class TestFutureExtensibility:
    """Tests demonstrating future extensibility."""

    def test_item_is_extensible(self):
        """Demonstrate that Item can be extended (future Todo test)."""

        # This is what Todo will look like in Phase 2
        @dataclass
        class MockTodo(Item):
            """Example of extending Item."""
            priority: str = "medium"
            completed: bool = False

        todo = MockTodo(text="Example todo", priority="high")

        # Todo IS-A Item
        assert isinstance(todo, Item)
        assert isinstance(todo, MockTodo)

        # Inherits Item properties
        assert todo.text == "Example todo"
        assert todo.position == 0
        assert isinstance(todo.id, UUID)

        # Has todo-specific properties
        assert todo.priority == "high"
        assert todo.completed is False

    def test_different_item_types_possible(self):
        """Demonstrate multiple item types can extend Item."""

        @dataclass
        class ShoppingItem(Item):
            """Example shopping list item."""
            quantity: int = 1
            purchased: bool = False

        @dataclass
        class ReadingItem(Item):
            """Example reading list item."""
            author: str = ""
            pages: int = 0
            finished: bool = False

        shopping = ShoppingItem(text="Milk", quantity=2)
        reading = ReadingItem(text="1984", author="Orwell", pages=328)

        # Both are Items
        assert isinstance(shopping, Item)
        assert isinstance(reading, Item)

        # Both have text
        assert shopping.text == "Milk"
        assert reading.text == "1984"

        # Both have specific properties
        assert shopping.quantity == 2
        assert reading.author == "Orwell"
```

**Run tests**:
```bash
# Run new primitive tests
pytest tests/domain/test_primitives.py -xvs

# Should see all tests pass
# Expected: 15+ tests, all passing
```

**Evidence Required**:
- Show test file creation
- Show pytest output with all tests passing
- Document test count (should be 15+)

### Task 4: Create Database Models (1.5 hours)

**Create `services/database/models/primitives.py`** (new file):

```python
"""
Database models for Item and List primitives.

Uses SQLAlchemy polymorphic inheritance:
- ItemDB is the base table (items)
- TodoDB joins to items table (todo_items) - Phase 2
- Other item types can join similarly
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UUID as SQLUUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from services.database.base import Base
from services.domain.primitives import Item, List as DomainList


class ItemDB(Base):
    """Database representation of universal Item.

    This is the base table for all item types using SQLAlchemy's
    polymorphic inheritance (joined table inheritance).

    Future item types (Todo, ShoppingItem) will have their own tables
    that join to this one via foreign key on id.
    """
    __tablename__ = "items"

    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String, nullable=False)
    position = Column(Integer, default=0, nullable=False)
    list_id = Column(SQLUUID(as_uuid=True), ForeignKey("lists.id"), nullable=True)
    item_type = Column(String(50), nullable=False)  # Discriminator
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Polymorphic configuration
    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": item_type,
    }

    # Relationship to list
    list = relationship("ListDB", back_populates="items")

    def to_domain(self) -> Item:
        """Convert database model to domain model."""
        return Item(
            id=self.id,
            text=self.text,
            position=self.position,
            list_id=self.list_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, item: Item) -> "ItemDB":
        """Convert domain model to database model."""
        return cls(
            id=item.id,
            text=item.text,
            position=item.position,
            list_id=item.list_id,
            item_type="item",  # Base type
            created_at=item.created_at,
            updated_at=item.updated_at,
        )


class ListDB(Base):
    """Database representation of universal List."""
    __tablename__ = "lists"

    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    item_type = Column(String(50), nullable=False)  # Discriminator
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to items
    items = relationship("ItemDB", back_populates="list", cascade="all, delete-orphan")

    def to_domain(self) -> DomainList:
        """Convert database model to domain model."""
        return DomainList(
            id=self.id,
            name=self.name,
            item_type=self.item_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, list_obj: DomainList) -> "ListDB":
        """Convert domain model to database model."""
        return cls(
            id=list_obj.id,
            name=list_obj.name,
            item_type=list_obj.item_type,
            created_at=list_obj.created_at,
            updated_at=list_obj.updated_at,
        )
```

**Update main models file** (`services/database/models.py`):
```python
# Add at top:
from .primitives import ItemDB, ListDB

# Export them:
__all__ = [
    # ... existing exports
    "ItemDB",
    "ListDB",
]
```

**Evidence Required**:
- Show created database models
- Confirm polymorphic configuration
- Confirm to_domain/from_domain methods

### Task 5: Create Migration Script (1 hour)

**Create migration** (DON'T RUN YET - just create the file):

```bash
# Create new migration
alembic revision -m "create_items_table_for_item_primitive"
```

**Edit the generated migration file** (in `alembic/versions/`):

```python
"""create_items_table_for_item_primitive

Revision ID: [generated]
Revises: [previous]
Create Date: [generated]
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers
revision = '[generated]'
down_revision = '[previous]'
branch_labels = None
depends_on = None


def upgrade():
    """
    Create items table as base for polymorphic inheritance.

    NOTE: This does NOT migrate existing todos yet.
    That happens in Phase 2.

    Phase 1: Create empty items table
    Phase 2: Migrate todos to items + todo_items structure
    """

    # Create items base table
    op.create_table(
        'items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('position', sa.Integer(), default=0, nullable=False),
        sa.Column('list_id', UUID(as_uuid=True), nullable=True),
        sa.Column('item_type', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['list_id'], ['lists.id'], name='fk_items_list_id'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on list_id for performance
    op.create_index('ix_items_list_id', 'items', ['list_id'])

    # Create index on item_type for polymorphic queries
    op.create_index('ix_items_item_type', 'items', ['item_type'])


def downgrade():
    """Remove items table."""
    op.drop_index('ix_items_item_type')
    op.drop_index('ix_items_list_id')
    op.drop_table('items')
```

**CRITICAL: Don't run migration yet!**
```bash
# DO NOT RUN THIS YET:
# alembic upgrade head

# We'll run migrations in Phase 2 after Todo is ready to extend Item
```

**Document the migration**:
Create `docs/refactor/MIGRATION-PLAN.md`:
```markdown
# Migration Plan

## Phase 1: Items Table (This Phase)
- Created migration script: [filename]
- NOT EXECUTED YET
- Creates empty items table
- No data migration yet

## Phase 2: Todo Migration (Next Phase)
- Will execute Phase 1 migration
- Migrate existing todos data to items table
- Rename todos → todo_items
- Create foreign key relationship

## Rollback Plan
- Phase 1: Just delete migration file (not run yet)
- Phase 2: `alembic downgrade -1`
```

**Evidence Required**:
- Show created migration file with full code
- Confirm migration NOT executed
- Show MIGRATION-PLAN.md created

### Task 6: Integration Test (30 min)

**Create `tests/integration/test_primitives_integration.py`**:

```python
"""
Integration tests for Item and List primitives.

These tests verify the full stack works:
domain → database → back to domain.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.database.models.primitives import ItemDB, ListDB
from services.domain.primitives import Item, List
from services.database.base import Base


@pytest.fixture
def in_memory_db():
    """Create in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


class TestItemPersistence:
    """Test Item domain ↔ database conversion."""

    def test_item_domain_to_db_to_domain(self, in_memory_db):
        """Item can be saved and retrieved."""
        # Create domain object
        item = Item(text="Test item", position=0)

        # Convert to database model
        item_db = ItemDB.from_domain(item)

        # Save to database
        in_memory_db.add(item_db)
        in_memory_db.commit()

        # Retrieve from database
        retrieved_db = in_memory_db.query(ItemDB).filter_by(id=item.id).first()
        assert retrieved_db is not None

        # Convert back to domain
        retrieved_item = retrieved_db.to_domain()

        # Verify all properties preserved
        assert retrieved_item.id == item.id
        assert retrieved_item.text == item.text
        assert retrieved_item.position == item.position


class TestListPersistence:
    """Test List domain ↔ database conversion."""

    def test_list_domain_to_db_to_domain(self, in_memory_db):
        """List can be saved and retrieved."""
        # Create domain object
        todo_list = List(name="Work Tasks", item_type="todo")

        # Convert and save
        list_db = ListDB.from_domain(todo_list)
        in_memory_db.add(list_db)
        in_memory_db.commit()

        # Retrieve and convert
        retrieved_db = in_memory_db.query(ListDB).filter_by(id=todo_list.id).first()
        retrieved_list = retrieved_db.to_domain()

        # Verify
        assert retrieved_list.id == todo_list.id
        assert retrieved_list.name == todo_list.name
        assert retrieved_list.item_type == todo_list.item_type


class TestItemListRelationship:
    """Test Item-List relationships persist correctly."""

    def test_item_belongs_to_list(self, in_memory_db):
        """Items can belong to lists in database."""
        # Create list
        todo_list = List(name="Tasks", item_type="todo")
        list_db = ListDB.from_domain(todo_list)
        in_memory_db.add(list_db)
        in_memory_db.flush()

        # Create item in list
        item = Item(text="Do task", list_id=todo_list.id, position=0)
        item_db = ItemDB.from_domain(item)
        in_memory_db.add(item_db)
        in_memory_db.commit()

        # Retrieve list with items
        retrieved_list_db = in_memory_db.query(ListDB).filter_by(id=todo_list.id).first()

        # Verify relationship
        assert len(retrieved_list_db.items) == 1
        assert retrieved_list_db.items[0].text == "Do task"
```

**Run integration tests**:
```bash
# Run integration tests
pytest tests/integration/test_primitives_integration.py -xvs

# Should all pass
```

**Evidence Required**:
- Show test file created
- Show pytest output with all tests passing

---

## Evidence Requirements

### Files Created:
- [ ] `services/domain/primitives.py` (Item and List classes)
- [ ] `services/database/models/primitives.py` (ItemDB and ListDB)
- [ ] `tests/domain/test_primitives.py` (15+ unit tests)
- [ ] `tests/integration/test_primitives_integration.py` (integration tests)
- [ ] `alembic/versions/[timestamp]_create_items_table.py` (migration - NOT executed)
- [ ] `docs/refactor/MIGRATION-PLAN.md` (migration documentation)

### Test Results:
- [ ] All unit tests pass (pytest tests/domain/test_primitives.py)
- [ ] All integration tests pass (pytest tests/integration/test_primitives_integration.py)
- [ ] Total tests: 15+ passing
- [ ] No existing tests broken

### Documentation:
- [ ] List primitive verified (exists or created)
- [ ] Item primitive properties documented
- [ ] Migration plan documented
- [ ] No migration executed yet (Phase 2)

### Git:
- [ ] All changes committed to foundation/item-list-primitives branch
- [ ] Commit messages describe Phase 1 work
- [ ] No changes to existing Todo code

---

## STOP Conditions

**STOP immediately and report if**:
- Tests fail and you can't figure out why
- Database model polymorphic mapping doesn't work
- List primitive doesn't exist and creating it breaks things
- Migration script has errors
- Integration tests can't connect to database

**DO NOT**:
- Touch existing Todo code (that's Phase 2)
- Change .title to .text (that's Phase 2)
- Execute migrations (that's Phase 2)
- Modify TodoRepository (that's Phase 2)

---

## Completion Criteria

**Must have ALL of these**:
1. ✅ Item domain primitive created and tested
2. ✅ List domain primitive verified/created
3. ✅ Database models (ItemDB, ListDB) created
4. ✅ Polymorphic inheritance configured
5. ✅ 15+ tests passing (domain + integration)
6. ✅ Migration script created (NOT executed)
7. ✅ Migration plan documented
8. ✅ All changes committed
9. ✅ Zero changes to existing Todo code
10. ✅ No existing functionality broken

**Final Report Format**:
```markdown
# Phase 1 Complete: Primitives Created

**Duration**: [actual time]
**Tests Created**: [count]
**Tests Passing**: [count]

## Created
- Item primitive class ✅
- List primitive [verified existing / created] ✅
- Database models (ItemDB, ListDB) ✅
- Comprehensive tests (15+) ✅
- Migration script (not executed) ✅

## Verified
- All new tests pass ✅
- No existing tests broken ✅
- Polymorphic inheritance works ✅
- Domain ↔ DB conversion works ✅

## NOT Done (Phase 2)
- Todo doesn't extend Item yet
- No .title → .text changes yet
- Migration not executed yet
- Repository not updated yet

**Ready for Phase 2**: Yes/No
**Blockers**: [list any]

**Next Phase**: Phase 2 - Refactor Todo to Extend Item
```

---

## Time Budget

- Task 1 (Verify List): 30 minutes
- Task 2 (Create Item): 1.5 hours
- Task 3 (Unit Tests): 1.5 hours
- Task 4 (Database Models): 1.5 hours
- Task 5 (Migration): 1 hour
- Task 6 (Integration Tests): 30 minutes

**Total**: 6.5 hours (slightly over 6h estimate, but comprehensive)

---

## Critical Reminders

1. **Don't touch Todo yet** - That's Phase 2
2. **Don't run migrations** - That's Phase 2
3. **Tests are mandatory** - No code without tests
4. **Commit frequently** - After each task
5. **Evidence-based** - Show test output, file contents

**The goal**: Create rock-solid Item and List primitives that Todo can extend in Phase 2

**Success metric**: 15+ tests passing, clean foundation ready for Todo refactoring

---

## After Completion

**Report back with**:
1. All test output (pytest -xvs)
2. Files created (list with line counts)
3. Git commit hashes
4. Any surprises or issues discovered
5. Confirmation ready for Phase 2

Then we proceed to Phase 2: Refactor Todo to Extend Item.

Good luck! You're building the foundation that makes the rest possible. 🏰

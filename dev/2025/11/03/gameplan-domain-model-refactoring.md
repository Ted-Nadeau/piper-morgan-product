# Gameplan: Domain Model Foundation Repair - Implementing Item/List Primitives

**Date**: November 3, 2025, 4:00 PM PT
**Decision**: Fix domain model to match original vision
**Approach**: "Slowly, carefully, methodically, and cheerfully"
**No Time Pressure**: Quality is the only metric

---

## Executive Summary

We're implementing the original domain vision: **Item and List are cognitive primitives**, with todos being just one specialization. This fixes an architectural divergence where todos became a silo instead of extending universal concepts.

**The Fix**: Create Item base class, refactor Todo to extend it, enabling future list types naturally.

---

## The Vision We're Implementing

```python
# COGNITIVE PRIMITIVES (Universal)
class Item:
    """The atomic unit of list-making - universal across all list types."""
    id: UUID
    text: str           # Every item has text
    position: int       # Order in the list
    created_at: datetime
    updated_at: datetime

class List:
    """Container for items - can hold any item type."""
    id: UUID
    name: str
    item_type: str      # Discriminator: 'todo', 'shopping', 'reading'
    created_at: datetime

# SPECIALIZATIONS (Domain-specific)
class Todo(Item):
    """An Item that can be completed and has priority."""
    completed: bool = False
    completed_at: Optional[datetime] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
```

---

## Phase 0: Pre-Flight Checklist (2 hours)

### Purpose
Understand exactly what we're refactoring before we touch anything.

### Required Actions

1. **Complete State Documentation**
```bash
# Document current todo implementation
grep -r "class Todo" . --include="*.py" > docs/refactor/current-todo-classes.txt
grep -r "TodoRepository" . --include="*.py" > docs/refactor/current-todo-usage.txt

# Find all todo table references
grep -r "todos" alembic/ --include="*.py" > docs/refactor/current-migrations.txt

# Document current test coverage
pytest tests/ -k "todo" --collect-only > docs/refactor/current-todo-tests.txt
```

2. **Create Refactoring Branch**
```bash
git checkout -b foundation/item-list-primitives
git commit --allow-empty -m "Beginning domain model foundation repair"
```

3. **Set Up Safety Nets**
- Run all tests, save output as baseline
- Create backup of current todo functionality
- Document current API contracts

### STOP Conditions
- Any production dependencies on todos (there shouldn't be)
- Unclear about current implementation
- Missing critical todo functionality documentation

---

## Phase 1: Create the Primitives (Day 1)

### Purpose
Establish Item and List as domain primitives without breaking anything.

### Step 1.1: Define Base Domain Models

Create `services/domain/primitives.py`:
```python
"""
Domain Primitives: Item and List

These are the cognitive primitives for list-making.
All specific list types (todos, shopping, etc.) extend these.

Design Decision: Items know their text and position.
Lists know their type and what items they contain.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class Item:
    """Universal list item - the atomic unit of list-making.

    Every item in every list has these properties.
    Specific item types (Todo, ShoppingItem) extend this.
    """
    id: UUID = field(default_factory=uuid4)
    text: str  # The universal property - all items have text
    position: int = 0  # Order within the list
    list_id: Optional[UUID] = None  # Which list contains this
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def move_to_position(self, new_position: int):
        """Items can be reordered."""
        self.position = new_position
        self.updated_at = datetime.now()

@dataclass
class List:
    """Universal list container.

    Lists are typed but can contain any items.
    The item_type discriminator determines what kind of items it expects.
    """
    id: UUID = field(default_factory=uuid4)
    name: str
    item_type: str  # 'todo', 'shopping', 'reading', etc.
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def can_contain(self, item: Item) -> bool:
        """Type checking for items."""
        # Will be specialized by list types
        return True
```

### Step 1.2: Create Database Models

Create `services/database/models/primitives.py`:
```python
"""Database models for Item and List primitives."""

class ItemDB(Base):
    """Database representation of universal Item."""
    __tablename__ = "items"

    id = Column(UUID, primary_key=True)
    text = Column(String, nullable=False)
    position = Column(Integer, default=0)
    list_id = Column(UUID, ForeignKey("lists.id"), nullable=True)
    item_type = Column(String, nullable=False)  # Discriminator
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Polymorphic mapping
    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": item_type,
    }

class TodoDB(ItemDB):
    """Database representation of Todo (extends Item)."""
    __tablename__ = "todo_items"

    id = Column(UUID, ForeignKey("items.id"), primary_key=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    priority = Column(String, default="medium")
    due_date = Column(DateTime, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "todo",
    }
```

### Step 1.3: Create Migration

```python
"""Add items table and refactor todos to extend items."""

def upgrade():
    # Create items table
    op.create_table('items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('position', sa.Integer(), default=0),
        sa.Column('list_id', sa.UUID(), nullable=True),
        sa.Column('item_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Migrate existing todos to items
    connection = op.get_bind()
    result = connection.execute(
        "INSERT INTO items (id, text, position, list_id, item_type, created_at, updated_at) "
        "SELECT id, title, 0, todo_list_id, 'todo', created_at, updated_at FROM todos"
    )

    # Rename todos table to todo_items
    op.rename_table('todos', 'todo_items')

    # Add foreign key from todo_items to items
    op.create_foreign_key(
        'fk_todo_items_items',
        'todo_items', 'items',
        ['id'], ['id']
    )
```

### Step 1.4: Comprehensive Tests

Create `tests/domain/test_primitives.py`:
```python
def test_item_creation():
    """Items are the atomic unit of lists."""
    item = Item(text="Buy milk")
    assert item.text == "Buy milk"
    assert item.position == 0
    assert item.id is not None

def test_todo_extends_item():
    """Todos are items with additional properties."""
    todo = Todo(text="Review PR", priority="high")
    assert isinstance(todo, Item)  # IS-A relationship
    assert todo.text == "Review PR"
    assert todo.priority == "high"
    assert todo.completed is False

def test_polymorphic_list_operations():
    """Lists can contain any items polymorphically."""
    list = List(name="My Tasks", item_type="todo")

    todo = Todo(text="Code review")
    shopping = ShoppingItem(text="Milk")  # Future

    # Type checking
    assert list.can_contain(todo) is True
    # Could add type checking: assert list.can_contain(shopping) is False
```

### Evidence Requirements
- Tests pass for new primitives
- Migration script tested on dev database
- No existing functionality broken

---

## Phase 2: Refactor Todo to Extend Item (Day 2)

### Purpose
Update Todo domain model to extend Item, maintaining backward compatibility.

### Step 2.1: Update Domain Model

Update `services/domain/models.py`:
```python
from .primitives import Item

@dataclass
class Todo(Item):
    """A todo is an Item that can be completed and has priority.

    Extends Item with todo-specific properties.
    Inherits: id, text, position, created_at, updated_at
    """
    # Todo-specific fields only
    completed: bool = False
    completed_at: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high, urgent
    due_date: Optional[datetime] = None

    def complete(self):
        """Mark todo as complete."""
        self.completed = True
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def reopen(self):
        """Reopen completed todo."""
        self.completed = False
        self.completed_at = None
        self.updated_at = datetime.now()
```

### Step 2.2: Update Repository

Update `services/repositories/todo_repository.py`:
```python
class TodoRepository:
    """Repository for Todo operations.

    Now works with todos as Items with todo-specific extensions.
    """

    async def create_todo(self, todo: Todo) -> Todo:
        """Create a todo (which is an Item)."""
        async with self.session() as session:
            # Create as item first
            item_db = ItemDB(
                id=todo.id,
                text=todo.text,  # Note: was 'title', now 'text'
                position=todo.position,
                item_type='todo'
            )

            # Then add todo-specific data
            todo_db = TodoDB(
                id=todo.id,
                completed=todo.completed,
                priority=todo.priority,
                due_date=todo.due_date
            )

            session.add(item_db)
            session.add(todo_db)
            await session.commit()

            return todo
```

### Step 2.3: Update Service References

Update all references from `todo.title` to `todo.text`:
```bash
# Find all references
grep -r "todo.title" . --include="*.py"

# Update systematically
# todo.title -> todo.text
# Todo(title=...) -> Todo(text=...)
```

### Evidence Requirements
- All todo tests still pass
- Can create todo via API
- Can retrieve todo with all properties
- Backward compatibility maintained

---

## Phase 3: Create Universal Services (Day 3)

### Purpose
Build service layer that works with Items polymorphically.

### Step 3.1: Create ItemService Base

Create `services/item_service.py`:
```python
class ItemService:
    """Base service for all item operations.

    Provides common operations for any item type.
    Specific services (TodoService) extend this.
    """

    async def create_item(
        self,
        list_id: UUID,
        text: str,
        item_class: Type[Item] = Item,
        **kwargs
    ) -> Item:
        """Create any type of item polymorphically."""
        item = item_class(
            text=text,
            list_id=list_id,
            **kwargs
        )
        # Save to repository
        return await self.repo.create_item(item)

    async def reorder_items(self, list_id: UUID, item_ids: List[UUID]):
        """Reorder items in a list - works for any item type."""
        # Universal operation on Items
        pass
```

### Step 3.2: Create TodoService

Create `services/todo_service.py`:
```python
class TodoService(ItemService):
    """Todo-specific service extending ItemService.

    Inherits generic item operations, adds todo-specific ones.
    """

    async def create_todo(
        self,
        user_id: UUID,
        text: str,
        priority: str = "medium"
    ) -> Todo:
        """Create a todo using inherited item creation."""
        return await self.create_item(
            list_id=user_id,  # For now
            text=text,
            item_class=Todo,
            priority=priority
        )

    async def complete_todo(self, todo_id: UUID) -> Todo:
        """Todo-specific operation."""
        todo = await self.repo.get_todo(todo_id)
        todo.complete()
        return await self.repo.update_todo(todo)
```

### Evidence Requirements
- Service creates todos as Items
- Generic operations work on todos
- Todo-specific operations still work
- Tests for polymorphic behavior

---

## Phase 4: Integration and Polish (Day 4)

### Purpose
Wire everything together, ensure system works end-to-end.

### Step 4.1: Update Intent Handlers

```python
class TodoIntentHandlers:
    def __init__(self):
        self.todo_service = TodoService()  # Now uses Item-aware service
```

### Step 4.2: Update API

```python
@router.post("/todos")
async def create_todo(request: TodoCreateRequest):
    service = TodoService()
    todo = await service.create_todo(
        text=request.text,  # Note: was title
        priority=request.priority
    )
    return TodoResponse.from_domain(todo)
```

### Step 4.3: Comprehensive Integration Tests

```python
async def test_todo_full_cycle_with_primitives():
    """Test todos work as Items end-to-end."""
    # Create via service
    service = TodoService()
    todo = await service.create_todo(text="Test todo")

    # Verify it's an Item
    assert isinstance(todo, Item)
    assert isinstance(todo, Todo)

    # Generic item operations work
    await service.reorder_items(...)  # Works on todos as Items

    # Todo-specific operations work
    await service.complete_todo(todo.id)
```

### Step 4.4: Documentation

Create ADR:
```markdown
# ADR-XXX: Domain Primitives - Item and List

## Status
Accepted

## Context
Original vision: Lists and Items are cognitive primitives.
Todos are one type of Item, enabling shopping lists, reading lists, etc.

## Decision
Implement Item and List base classes.
All specific types (Todo, ShoppingItem) extend Item.
Lists are universal containers with type discrimination.

## Consequences
+ True extensibility for new list types
+ Matches cognitive model
+ Code reuse for common operations
- Refactoring effort required
+ Foundation for long-term growth
```

---

## Phase 5: Validation and Celebration

### Final Checklist
- [ ] All tests pass
- [ ] Todo functionality unchanged from user perspective
- [ ] New Item/List primitives documented
- [ ] Migration tested and reversible
- [ ] API backward compatible
- [ ] Performance unchanged or improved

### Success Metrics
- Can create/read/update/delete todos ✓
- Todo extends Item ✓
- Can add new item types easily ✓
- Code is cleaner and more maintainable ✓

---

## Communication

### Daily Standup Message
"Implementing domain model foundation per PM's architectural vision. Making todos extend Item primitive to enable future list types. Slow, methodical, test-driven approach. No time pressure - quality only."

### For Agents
"We're fixing the foundation. Todo becomes a specialization of Item. This enables shopping lists, reading lists, any future list type. Tests at every step. No rushing."

---

## Risk Mitigation

1. **Feature branch** - All work isolated
2. **Incremental approach** - Each phase independently valuable
3. **Comprehensive tests** - Nothing breaks without us knowing
4. **Backward compatibility** - API contracts maintained
5. **Rollback plan** - Each phase reversible

---

## The Joy of Getting It Right

This refactoring is about craftsmanship:
- Building on correct foundations
- Honoring the original vision
- Creating extensible, beautiful code
- Taking time to do it right

No shortcuts. No rushing. Just steady, careful progress toward the correct architecture.

---

*"Slowly, carefully, methodically, and cheerfully getting the foundation right."*

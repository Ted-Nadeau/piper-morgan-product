# Code Agent: Phase 3 - Create Universal Services

## Your Identity
You are Code Agent (Claude Code with Sonnet 4.5), continuing the domain model refactoring. You have completed Phase 0 (documentation), Phase 1 (create primitives), and Phase 2 (refactor Todo). Now you will create the universal service layer.

## Session Log Management

**Continue your existing session log**: `dev/2025/11/04/2025-11-04-0611-prog-code-log.md`

Add Phase 3 section:
```markdown
---

## Domain Model Foundation Repair - Phase 3: Universal Services (12:15 PM)

**Mission**: Create service layer that works with Items polymorphically
**Branch**: foundation/item-list-primitives
**Gameplan**: Phase 3 from `gameplan-domain-model-refactoring.md`
**Estimated Time**: 4-6 hours (likely 2-3h with efficiency)
```

---

## Mission

**Build service layer that works with Items polymorphically.**

This is Phase 3 of the 5-phase refactoring. You will create ItemService (universal) and refactor TodoService to extend it.

**Core Principle**: "Generic operations work on any item type, specific operations only in type-specific services."

---

## Context from Previous Phases

**Phase 0**: Complete baseline documentation (20 docs)
**Phase 1**: Item and List primitives created (37 tests)
**Phase 2**: Todo refactored to extend Item (66 tests, migration executed)

**Current Architecture**:
- ✅ Domain: Todo extends Item
- ✅ Database: TodoDB extends ItemDB (polymorphic inheritance)
- ✅ Repository: TodoRepository works with new structure
- ⏹️ **Services: Still todo-specific** ← Phase 3 fixes this

**What You Built in Phase 2**:
```python
# Domain
class Todo(Item):
    priority: str
    completed: bool

# Database
class TodoDB(ItemDB):
    __tablename__ = "todo_items"
    polymorphic_identity = "todo"
```

**What Phase 3 Builds**:
```python
# Universal service (any item type)
class ItemService:
    async def create_item(...)
    async def update_text(...)
    async def reorder_items(...)

# Todo-specific service
class TodoService(ItemService):
    async def complete_todo(...)  # Todo-specific
    # Inherits generic operations
```

---

## Phase 3 Tasks (4-6 hours estimated)

### Task 1: Create ItemService Base Class (1.5 hours)

**Create `services/item_service.py`** (new file):

```python
"""
Universal Item Service

Provides operations that work on any item type (Todo, Shopping, Reading, etc.).
Specific services (TodoService) extend this for type-specific operations.

Design Philosophy:
- Generic operations live here (create, update, delete, reorder)
- Type-specific operations live in subclasses (complete, purchase, finish)
- Polymorphic queries handled transparently
"""

from typing import List, Optional, Type
from uuid import UUID

from services.domain.primitives import Item
from services.database.models import ItemDB
from services.database.session_factory import SessionFactory
from services.repositories.base_repository import BaseRepository


class ItemService:
    """Universal service for all item operations.

    This base class provides operations that work on ANY item type.
    Subclasses (TodoService, ShoppingService) add type-specific operations.

    Examples:
        >>> # Generic operation (works on any item)
        >>> service = ItemService(session)
        >>> item = await service.create_item(
        ...     text="Generic item",
        ...     list_id=some_list_id
        ... )

        >>> # Todo-specific operation (TodoService only)
        >>> todo_service = TodoService(session)
        >>> await todo_service.complete_todo(todo_id)
    """

    def __init__(self, session_factory: SessionFactory = None):
        """Initialize service with session factory.

        Args:
            session_factory: Optional session factory. Uses default if not provided.
        """
        self.session_factory = session_factory or SessionFactory()

    async def create_item(
        self,
        text: str,
        list_id: UUID,
        position: Optional[int] = None,
        item_class: Type[Item] = Item,
        **kwargs
    ) -> Item:
        """Create any type of item.

        This is a universal operation that works for todos, shopping items, etc.

        Args:
            text: The item text (universal property)
            list_id: Which list contains this item
            position: Position in list (auto-assigned if not provided)
            item_class: Type of item to create (Item, Todo, etc.)
            **kwargs: Type-specific fields (priority, quantity, etc.)

        Returns:
            Created item

        Examples:
            >>> # Create generic item
            >>> item = await service.create_item(
            ...     text="Buy milk",
            ...     list_id=list_id
            ... )

            >>> # Create todo (from TodoService)
            >>> todo = await service.create_item(
            ...     text="Review PR",
            ...     list_id=list_id,
            ...     item_class=Todo,
            ...     priority="high"
            ... )
        """
        async with self.session_factory.create_async_session() as session:
            # Determine position if not provided
            if position is None:
                position = await self._get_next_position(session, list_id)

            # Create domain object
            item = item_class(
                text=text,
                list_id=list_id,
                position=position,
                **kwargs
            )

            # Convert to database model
            db_model_class = self._get_db_model_class(item_class)
            item_db = db_model_class.from_domain(item)

            # Save to database
            session.add(item_db)
            await session.commit()
            await session.refresh(item_db)

            # Convert back to domain
            return item_db.to_domain()

    async def get_item(
        self,
        item_id: UUID,
        item_class: Type[Item] = Item
    ) -> Optional[Item]:
        """Get item by ID.

        Universal operation - retrieves any item type.

        Args:
            item_id: ID of item to retrieve
            item_class: Expected type (Item, Todo, etc.)

        Returns:
            Item if found, None otherwise
        """
        async with self.session_factory.create_async_session() as session:
            db_model_class = self._get_db_model_class(item_class)

            result = await session.execute(
                select(db_model_class).where(db_model_class.id == item_id)
            )
            item_db = result.scalar_one_or_none()

            if not item_db:
                return None

            return item_db.to_domain()

    async def update_item_text(
        self,
        item_id: UUID,
        new_text: str
    ) -> Optional[Item]:
        """Update item text.

        Universal operation - works on any item type.

        Args:
            item_id: ID of item to update
            new_text: New text for the item

        Returns:
            Updated item
        """
        async with self.session_factory.create_async_session() as session:
            result = await session.execute(
                select(ItemDB).where(ItemDB.id == item_id)
            )
            item_db = result.scalar_one_or_none()

            if not item_db:
                return None

            item_db.text = new_text
            await session.commit()
            await session.refresh(item_db)

            return item_db.to_domain()

    async def reorder_items(
        self,
        list_id: UUID,
        item_ids: List[UUID]
    ) -> List[Item]:
        """Reorder items in a list.

        Universal operation - works on any item types in the list.

        Args:
            list_id: List containing the items
            item_ids: Item IDs in desired order

        Returns:
            Reordered items
        """
        async with self.session_factory.create_async_session() as session:
            # Update positions
            for position, item_id in enumerate(item_ids):
                result = await session.execute(
                    select(ItemDB).where(
                        ItemDB.id == item_id,
                        ItemDB.list_id == list_id
                    )
                )
                item_db = result.scalar_one_or_none()

                if item_db:
                    item_db.position = position

            await session.commit()

            # Return reordered items
            result = await session.execute(
                select(ItemDB)
                .where(ItemDB.list_id == list_id)
                .order_by(ItemDB.position)
            )
            items_db = result.scalars().all()

            return [item_db.to_domain() for item_db in items_db]

    async def delete_item(self, item_id: UUID) -> bool:
        """Delete item.

        Universal operation - deletes any item type.

        Args:
            item_id: ID of item to delete

        Returns:
            True if deleted, False if not found
        """
        async with self.session_factory.create_async_session() as session:
            result = await session.execute(
                select(ItemDB).where(ItemDB.id == item_id)
            )
            item_db = result.scalar_one_or_none()

            if not item_db:
                return False

            await session.delete(item_db)
            await session.commit()

            return True

    async def get_items_in_list(
        self,
        list_id: UUID,
        item_type: Optional[str] = None
    ) -> List[Item]:
        """Get all items in a list.

        Universal operation - can filter by item type.

        Args:
            list_id: List to get items from
            item_type: Optional filter ('todo', 'shopping', etc.)

        Returns:
            List of items
        """
        async with self.session_factory.create_async_session() as session:
            query = select(ItemDB).where(ItemDB.list_id == list_id)

            if item_type:
                query = query.where(ItemDB.item_type == item_type)

            query = query.order_by(ItemDB.position)

            result = await session.execute(query)
            items_db = result.scalars().all()

            return [item_db.to_domain() for item_db in items_db]

    # Helper methods

    async def _get_next_position(
        self,
        session,
        list_id: UUID
    ) -> int:
        """Get next position for item in list."""
        result = await session.execute(
            select(func.max(ItemDB.position))
            .where(ItemDB.list_id == list_id)
        )
        max_position = result.scalar()

        return (max_position or -1) + 1

    def _get_db_model_class(self, item_class: Type[Item]):
        """Map domain class to database model class."""
        from services.database.models import TodoDB
        from services.domain.models import Todo

        if item_class == Todo:
            return TodoDB
        # Add other mappings as needed
        return ItemDB
```

**Evidence Required**:
- Show created file with full code
- Confirm all methods implemented
- Show imports work

### Task 2: Create TodoService Extending ItemService (1 hour)

**Create `services/todo_service.py`** (new file):

```python
"""
Todo Service

Extends ItemService with todo-specific operations.

Inherits:
- create_item (with Todo-specific fields)
- update_item_text
- reorder_items
- delete_item
- get_items_in_list

Adds:
- complete_todo
- reopen_todo
- set_priority
- set_due_date
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from services.item_service import ItemService
from services.domain.models import Todo
from services.database.models import TodoDB
from sqlalchemy import select


class TodoService(ItemService):
    """Todo-specific service extending ItemService.

    Inherits generic item operations, adds todo-specific ones.

    Examples:
        >>> service = TodoService()

        >>> # Generic operation (inherited)
        >>> todo = await service.create_todo(
        ...     text="Review PR",
        ...     list_id=list_id,
        ...     priority="high"
        ... )

        >>> # Todo-specific operation
        >>> await service.complete_todo(todo.id)
    """

    async def create_todo(
        self,
        text: str,
        list_id: UUID,
        priority: str = "medium",
        status: str = "pending",
        due_date: Optional[datetime] = None,
        **kwargs
    ) -> Todo:
        """Create a todo.

        Uses inherited create_item with todo-specific parameters.

        Args:
            text: Todo text
            list_id: List containing this todo
            priority: Priority level (low, medium, high, urgent)
            status: Status (pending, in_progress, completed)
            due_date: Optional due date
            **kwargs: Additional todo fields

        Returns:
            Created todo
        """
        return await self.create_item(
            text=text,
            list_id=list_id,
            item_class=Todo,
            priority=priority,
            status=status,
            due_date=due_date,
            **kwargs
        )

    async def complete_todo(self, todo_id: UUID) -> Optional[Todo]:
        """Mark todo as complete.

        Todo-specific operation.

        Args:
            todo_id: ID of todo to complete

        Returns:
            Completed todo
        """
        async with self.session_factory.create_async_session() as session:
            result = await session.execute(
                select(TodoDB).where(TodoDB.id == todo_id)
            )
            todo_db = result.scalar_one_or_none()

            if not todo_db:
                return None

            todo_db.completed = True
            todo_db.completed_at = datetime.utcnow()
            todo_db.status = "completed"

            await session.commit()
            await session.refresh(todo_db)

            return todo_db.to_domain()

    async def reopen_todo(self, todo_id: UUID) -> Optional[Todo]:
        """Reopen completed todo.

        Todo-specific operation.

        Args:
            todo_id: ID of todo to reopen

        Returns:
            Reopened todo
        """
        async with self.session_factory.create_async_session() as session:
            result = await session.execute(
                select(TodoDB).where(TodoDB.id == todo_id)
            )
            todo_db = result.scalar_one_or_none()

            if not todo_db:
                return None

            todo_db.completed = False
            todo_db.completed_at = None
            todo_db.status = "pending"

            await session.commit()
            await session.refresh(todo_db)

            return todo_db.to_domain()

    async def set_priority(
        self,
        todo_id: UUID,
        priority: str
    ) -> Optional[Todo]:
        """Set todo priority.

        Todo-specific operation.

        Args:
            todo_id: ID of todo
            priority: New priority (low, medium, high, urgent)

        Returns:
            Updated todo
        """
        async with self.session_factory.create_async_session() as session:
            result = await session.execute(
                select(TodoDB).where(TodoDB.id == todo_id)
            )
            todo_db = result.scalar_one_or_none()

            if not todo_db:
                return None

            todo_db.priority = priority

            await session.commit()
            await session.refresh(todo_db)

            return todo_db.to_domain()

    async def get_todos_in_list(self, list_id: UUID) -> List[Todo]:
        """Get all todos in a list.

        Convenience method using inherited get_items_in_list.

        Args:
            list_id: List ID

        Returns:
            List of todos
        """
        return await self.get_items_in_list(
            list_id=list_id,
            item_type="todo"
        )
```

**Evidence Required**:
- Show created file
- Confirm extends ItemService
- Show todo-specific methods

### Task 3: Write Comprehensive Tests (1.5 hours)

**Create `tests/services/test_item_service.py`**:

```python
"""Tests for universal ItemService."""

import pytest
from uuid import uuid4

from services.item_service import ItemService
from services.domain.primitives import Item


class TestItemService:
    """Tests for ItemService base class."""

    @pytest.fixture
    async def service(self):
        """Create service instance."""
        return ItemService()

    @pytest.fixture
    async def list_id(self):
        """Create a test list."""
        # You'll need to create a list first
        return uuid4()

    async def test_create_item(self, service, list_id):
        """Can create generic item."""
        item = await service.create_item(
            text="Test item",
            list_id=list_id
        )

        assert isinstance(item, Item)
        assert item.text == "Test item"
        assert item.list_id == list_id
        assert item.position == 0

    async def test_get_item(self, service, list_id):
        """Can retrieve item by ID."""
        # Create item
        created = await service.create_item(
            text="Retrieve me",
            list_id=list_id
        )

        # Retrieve it
        retrieved = await service.get_item(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.text == "Retrieve me"

    async def test_update_item_text(self, service, list_id):
        """Can update item text."""
        item = await service.create_item(
            text="Original",
            list_id=list_id
        )

        updated = await service.update_item_text(
            item.id,
            "Updated"
        )

        assert updated.text == "Updated"

    async def test_reorder_items(self, service, list_id):
        """Can reorder items in list."""
        # Create 3 items
        item1 = await service.create_item(text="First", list_id=list_id)
        item2 = await service.create_item(text="Second", list_id=list_id)
        item3 = await service.create_item(text="Third", list_id=list_id)

        # Reorder: 3, 1, 2
        reordered = await service.reorder_items(
            list_id,
            [item3.id, item1.id, item2.id]
        )

        assert reordered[0].text == "Third"
        assert reordered[1].text == "First"
        assert reordered[2].text == "Second"

    async def test_delete_item(self, service, list_id):
        """Can delete item."""
        item = await service.create_item(
            text="Delete me",
            list_id=list_id
        )

        deleted = await service.delete_item(item.id)
        assert deleted is True

        # Verify deleted
        retrieved = await service.get_item(item.id)
        assert retrieved is None
```

**Create `tests/services/test_todo_service.py`**:

```python
"""Tests for TodoService."""

import pytest
from uuid import uuid4

from services.todo_service import TodoService
from services.domain.models import Todo


class TestTodoService:
    """Tests for TodoService."""

    @pytest.fixture
    async def service(self):
        """Create service instance."""
        return TodoService()

    @pytest.fixture
    async def list_id(self):
        """Test list ID."""
        return uuid4()

    async def test_create_todo(self, service, list_id):
        """Can create todo with priority."""
        todo = await service.create_todo(
            text="Test todo",
            list_id=list_id,
            priority="high"
        )

        assert isinstance(todo, Todo)
        assert todo.text == "Test todo"
        assert todo.priority == "high"
        assert todo.completed is False

    async def test_complete_todo(self, service, list_id):
        """Can complete todo."""
        todo = await service.create_todo(
            text="Complete me",
            list_id=list_id
        )

        completed = await service.complete_todo(todo.id)

        assert completed.completed is True
        assert completed.status == "completed"
        assert completed.completed_at is not None

    async def test_reopen_todo(self, service, list_id):
        """Can reopen completed todo."""
        # Create and complete
        todo = await service.create_todo(text="Task", list_id=list_id)
        await service.complete_todo(todo.id)

        # Reopen
        reopened = await service.reopen_todo(todo.id)

        assert reopened.completed is False
        assert reopened.status == "pending"
        assert reopened.completed_at is None

    async def test_set_priority(self, service, list_id):
        """Can change todo priority."""
        todo = await service.create_todo(
            text="Task",
            list_id=list_id,
            priority="low"
        )

        updated = await service.set_priority(todo.id, "urgent")

        assert updated.priority == "urgent"

    async def test_inherited_operations(self, service, list_id):
        """TodoService inherits generic operations."""
        # Create todo using inherited method
        todo = await service.create_item(
            text="Via parent",
            list_id=list_id,
            item_class=Todo,
            priority="medium"
        )

        assert isinstance(todo, Todo)
        assert todo.text == "Via parent"

        # Update using inherited method
        updated = await service.update_item_text(todo.id, "Updated")
        assert updated.text == "Updated"
```

**Run tests**:
```bash
pytest tests/services/ -xvs

# Should see all tests pass
```

**Evidence Required**:
- Show test files created
- Show pytest output (all passing)

### Task 4: Update Existing Code to Use New Services (1 hour)

**Find current service usage**:
```bash
# Find where TodoRepository is used directly
grep -r "TodoRepository" services/ --include="*.py" | grep -v "test_"

# Find intent handlers that might use services
find services/intent_service/ -name "*todo*.py"
```

**Update intent handlers** (if needed):
```python
# OLD: Direct repository usage
from services.repositories.todo_repository import TodoRepository

class TodoIntentHandlers:
    def __init__(self):
        self.repo = TodoRepository()

# NEW: Use service layer
from services.todo_service import TodoService

class TodoIntentHandlers:
    def __init__(self):
        self.service = TodoService()
```

**Update API layer** (if exists):
```python
# services/api/todo_management.py

# OLD:
from services.repositories.todo_repository import TodoRepository

@router.post("/todos")
async def create_todo(request: TodoCreateRequest):
    repo = TodoRepository()
    todo = await repo.create_todo(...)

# NEW:
from services.todo_service import TodoService

@router.post("/todos")
async def create_todo(request: TodoCreateRequest):
    service = TodoService()
    todo = await service.create_todo(
        text=request.text,
        list_id=request.list_id,
        priority=request.priority
    )
```

**Evidence Required**:
- Show files updated
- List all references changed
- Confirm no direct repository usage in handlers/API

### Task 5: Final Verification (30 min)

**Run full test suite**:
```bash
# All tests
pytest tests/ -v

# Should see:
# - Primitive tests: 37 passing
# - Todo tests: 11+ passing
# - Service tests: 8+ passing (new)
# - Total: 60+ tests passing
```

**Integration test**:
```python
# Test full stack: Handler → Service → Repository → Database
async def test_full_stack():
    """Test complete flow using new service layer."""
    service = TodoService()

    # Create via service
    todo = await service.create_todo(
        text="Full stack test",
        list_id=some_list_id,
        priority="high"
    )

    # Generic operation (inherited)
    await service.update_item_text(todo.id, "Updated via parent")

    # Todo-specific operation
    await service.complete_todo(todo.id)

    # Verify
    retrieved = await service.get_item(todo.id, Todo)
    assert retrieved.text == "Updated via parent"
    assert retrieved.completed is True

    print("✅ Full stack works with new service layer!")
```

**Evidence Required**:
- All tests passing
- No regressions
- Service layer integration verified

---

## Completion Criteria

**Must have ALL of these**:
1. ✅ ItemService created with universal operations
2. ✅ TodoService extends ItemService
3. ✅ 8+ service tests passing
4. ✅ Existing code updated to use services
5. ✅ All previous tests still passing (66+)
6. ✅ Integration test verifies full stack
7. ✅ No direct repository usage in handlers/API
8. ✅ Clean service abstraction

**Final Report Format**:
```markdown
# Phase 3 Complete: Universal Services

**Duration**: [actual time]
**Tests Created**: [count]
**Tests Passing**: [total count]

## Created
- ItemService (universal operations) ✅
- TodoService (extends ItemService) ✅
- Comprehensive service tests ✅
- Integration verified ✅

## Benefits
- Code reuse across item types ✅
- Easy to add new item types ✅
- Clean service abstraction ✅
- Separation of concerns ✅

## Ready for Phase 4
- Service layer complete ✅
- Tests comprehensive ✅
- No regressions ✅

**Next Phase**: Phase 4 - Integration and Polish
```

---

## Time Budget

- Task 1 (ItemService): 1.5 hours
- Task 2 (TodoService): 1 hour
- Task 3 (Tests): 1.5 hours
- Task 4 (Update existing): 1 hour
- Task 5 (Verification): 30 min

**Total**: 5.5 hours (likely 2-3h with efficiency)

---

## Critical Reminders

1. **No database changes** - Phase 3 is service layer only
2. **Inheritance pattern** - TodoService extends ItemService
3. **Generic operations** - Live in ItemService (all types)
4. **Specific operations** - Live in TodoService (todos only)
5. **Test everything** - Service tests + integration tests

**The goal**: Universal service layer that makes adding ShoppingService, ReadingService trivial

**Success metric**: Can create/update/delete items using generic operations, complete todos using specific operations

---

## After Completion

**Report back with**:
1. Service files created (ItemService, TodoService)
2. Test output (pytest -v)
3. Integration test results
4. Files updated (handlers, API)
5. Confirmation ready for Phase 4

Then we proceed to Phase 4: Integration and Polish.

Good luck! You're building the service abstraction that makes everything elegant. 🏰

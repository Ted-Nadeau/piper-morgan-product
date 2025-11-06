# Gameplan: Todo Persistence Completion (Issue #295)

**Created**: November 4, 2025, 4:37 PM
**Issue**: #295 - CORE-ALPHA-TODO-PERSISTENCE
**Branch**: (to be determined - likely continue on main after foundation merge)
**Prerequisite**: foundation/item-list-primitives merged
**Effort**: Medium (service creation + wiring + comprehensive testing)
**Goal**: Complete todo persistence wiring with integration tests

---

## Executive Summary

**What We're Building**: Wire the todo system for actual database persistence

**Current State**:
- ✅ Domain model foundation complete (Item/List primitives, Todo extends Item)
- ✅ ItemService + TodoService exist (universal operations)
- ✅ TodoRepository exists (17 methods, comprehensive CRUD)
- ✅ Intent handlers parse natural language correctly
- ❌ Handlers return mocked responses (no persistence)
- ❌ API returns mocked responses (no persistence)
- ❌ TodoManagementService doesn't exist (orchestration layer missing)

**What We're Solving**: "Verification theater" - system appears to work but todos are lost immediately

**The Gap**:
```
Current:  User → Handler → Mock Response → User confusion (todos not saved)
Target:   User → Handler → Service → Repository → Database → Real persistence
```

**Approach**: Create TodoManagementService, wire handlers and API, prove persistence with integration tests

---

## Prerequisites

### Must Be Complete Before Starting

1. ✅ **Domain Model Foundation** (Phases 0-5 from domain model refactoring)
   - Item/List primitives created
   - Todo extends Item
   - Database migrated (234aa8ec628c)
   - ItemService + TodoService available

2. ⏸️ **Foundation Branch Merged** (REQUIRED)
   - Branch: foundation/item-list-primitives
   - Status: Ready, awaiting doc analysis completion
   - **STOP CONDITION**: Cannot proceed until merged

3. ✅ **Documentation Complete**
   - ADR-041 documents domain model decisions
   - Roadmap established (ROADMAP-TODO-PERSISTENCE-COMPLETION.md)
   - Issue #295 updated with clear scope

### Verification Before Starting

```bash
# 1. Verify foundation merged
git branch --merged | grep "foundation/item-list-primitives"
# Should show: foundation/item-list-primitives

# 2. Verify migrations current
alembic current
# Should show: 234aa8ec628c (refactor_todos_to_extend_items)

# 3. Verify services exist
ls -lh services/item_service.py services/todo_service.py
# Both should exist

# 4. Verify tests passing
pytest tests/services/test_item_service.py tests/services/test_todo_service.py -v
# Should show: 16 tests passing
```

**If any verification fails**: STOP and resolve before proceeding

---

## Phase Overview

| Phase | Description | Effort | Complexity |
|-------|-------------|--------|------------|
| **Phase 0** | Pre-implementation check | Small | Low |
| **Phase 1** | Create TodoManagementService | Large | Medium |
| **Phase 2** | Wire Intent Handlers | Small | Low |
| **Phase 3** | Wire API Layer | Small | Low |
| **Phase 4** | Integration Tests | Medium | Medium |
| **Phase 5** | Validation & Closure | Small | Low |

---

## Phase 0: Pre-Implementation Check

### Goal
Verify environment is ready and foundation is solid

### Tasks

**Task 0.1: Verify Prerequisites**
```bash
# Run verification script
cd /path/to/piper-morgan

# 1. Foundation merged
git log --oneline -1 --grep="domain-model"

# 2. Services available
python3 -c "
from services.item_service import ItemService
from services.todo_service import TodoService
print('✅ Services importable')
"

# 3. Repository available
python3 -c "
from services.repositories.todo_repository import TodoRepository
print('✅ TodoRepository available')
"

# 4. Database ready
alembic current
```

**Task 0.2: Review Architecture Decisions**

Review Nov 3 Chief Architect consultation decisions:
- ✅ Service layer approach (Handlers → Service → Repository)
- ✅ Create TodoManagementService (orchestration layer)
- ✅ Service layer manages transactions
- ✅ Use TodoRepository (not UniversalList migration)

**Task 0.3: Create Session Log**

```markdown
# Session Log: Todo Persistence Completion

**Date**: [today's date]
**Agent**: [Code/Cursor/etc]
**Issue**: #295 - CORE-ALPHA-TODO-PERSISTENCE
**Branch**: [branch name]
**Gameplan**: gameplan-todo-persistence-completion.md

## Mission
Complete todo persistence wiring with real database operations

## Phases
- Phase 0: Pre-implementation check
- Phase 1: TodoManagementService
- Phase 2: Wire handlers
- Phase 3: Wire API
- Phase 4: Integration tests
- Phase 5: Validation

[Track progress here as you work]
```

### Completion Criteria
- ✅ All prerequisites verified
- ✅ Architecture decisions reviewed
- ✅ Session log created
- ✅ Ready to proceed

---

## Phase 1: Create TodoManagementService

### Goal
Create orchestration layer that handles business logic and coordinates repository operations

### Why This Service Exists

**TodoService** (domain operations):
- Universal item operations (inherited from ItemService)
- Todo-specific domain logic (complete, reopen, set_priority)

**TodoManagementService** (business orchestration):
- **Transaction management** (session scopes)
- **Business rules** (validation, authorization)
- **Orchestration** (coordinates TodoService + TodoRepository + TodoKnowledgeService)
- **Error handling** (catches database errors, returns domain errors)

**TodoRepository** (data access):
- Database operations (CRUD, queries)
- SQL and ORM

### Architecture

```
Intent Handlers (natural language)
    ↓
TodoManagementService (business logic, transactions)
    ├→ TodoService (domain operations)
    ├→ TodoRepository (persistence)
    └→ TodoKnowledgeService (knowledge graph - optional)
```

### Tasks

**Task 1.1: Create Service File**

Create `services/todo/todo_management_service.py`:

```python
"""
Todo Management Service

Business logic layer for todo operations.
Orchestrates TodoService, TodoRepository, and TodoKnowledgeService.

Architecture:
- Manages transactions (AsyncSessionFactory.session_scope)
- Validates business rules (ownership, permissions)
- Coordinates domain operations via TodoService
- Handles persistence via TodoRepository
- Optional: Knowledge graph integration via TodoKnowledgeService

Examples:
    >>> service = TodoManagementService()
    >>> todo = await service.create_todo(
    ...     user_id="user-123",
    ...     text="Review PR",
    ...     priority="high"
    ... )
    >>> print(f"Created todo {todo.id}: {todo.text}")
"""

from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from services.todo_service import TodoService
from services.repositories.todo_repository import TodoRepository
from services.todo.todo_knowledge_service import TodoKnowledgeService
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Todo
from services.domain.primitives import Item


class TodoManagementService:
    """Service for managing todo operations with business logic.

    This service provides the business logic layer between handlers/API
    and the repository layer. It:
    - Manages database transactions
    - Validates business rules (ownership, etc.)
    - Coordinates TodoService and TodoRepository
    - Handles errors gracefully
    - Optional: Integrates with knowledge graph

    Architecture Decision (Nov 3, 2025 - Chief Architect):
    - Service layer approach chosen over direct repository access
    - Service manages transactions (not repository)
    - Use TodoRepository (not UniversalList migration)
    """

    def __init__(
        self,
        todo_service: Optional[TodoService] = None,
        knowledge_service: Optional[TodoKnowledgeService] = None
    ):
        """Initialize service with dependencies.

        Args:
            todo_service: Optional TodoService (created if not provided)
            knowledge_service: Optional knowledge graph service
        """
        self.todo_service = todo_service or TodoService()
        self.knowledge_service = knowledge_service

    async def create_todo(
        self,
        user_id: str,
        text: str,
        priority: str = "medium",
        list_id: Optional[str] = None,
        due_date: Optional[datetime] = None,
        **kwargs
    ) -> Todo:
        """Create a new todo with database persistence.

        This is the main entry point for creating todos. It:
        1. Validates input
        2. Creates todo in database via repository
        3. Optional: Creates knowledge node
        4. Returns persisted todo

        Args:
            user_id: Owner of the todo
            text: Todo text/title
            priority: Priority level (low, medium, high, urgent)
            list_id: Optional list to add todo to
            due_date: Optional due date
            **kwargs: Additional todo fields

        Returns:
            Created Todo with database ID

        Raises:
            ValueError: If validation fails
            DatabaseError: If persistence fails

        Examples:
            >>> service = TodoManagementService()
            >>> todo = await service.create_todo(
            ...     user_id="user-123",
            ...     text="Review PR",
            ...     priority="high"
            ... )
            >>> assert todo.id is not None  # Has database ID
            >>> assert todo.text == "Review PR"
        """
        # Validate input
        if not text or not text.strip():
            raise ValueError("Todo text cannot be empty")

        if priority not in ["low", "medium", "high", "urgent"]:
            raise ValueError(f"Invalid priority: {priority}")

        # Create todo via service (domain operation)
        async with AsyncSessionFactory.session_scope() as session:
            # Create repository with session
            todo_repo = TodoRepository(session)

            # Create todo domain object
            todo = Todo(
                id=uuid4(),
                text=text.strip(),
                priority=priority,
                owner_id=user_id,
                list_id=list_id,
                due_date=due_date,
                status="pending",
                completed=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                **kwargs
            )

            # Persist to database
            saved_todo = await todo_repo.create_todo(todo)

            # Optional: Create knowledge node
            if self.knowledge_service:
                try:
                    await self.knowledge_service.create_todo_knowledge_node(
                        saved_todo
                    )
                except Exception as e:
                    # Knowledge graph failure shouldn't fail todo creation
                    # Log error but continue
                    print(f"Warning: Failed to create knowledge node: {e}")

            return saved_todo

    async def list_todos(
        self,
        user_id: str,
        list_id: Optional[str] = None,
        status: Optional[str] = None,
        include_completed: bool = False
    ) -> List[Todo]:
        """List todos for a user.

        Args:
            user_id: Owner ID to filter by
            list_id: Optional list to filter by
            status: Optional status filter
            include_completed: Include completed todos

        Returns:
            List of todos matching filters

        Examples:
            >>> todos = await service.list_todos(user_id="user-123")
            >>> active = await service.list_todos(
            ...     user_id="user-123",
            ...     include_completed=False
            ... )
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # Get todos by owner
            todos = await todo_repo.get_todos_by_owner(user_id)

            # Filter by list if specified
            if list_id:
                todos = [t for t in todos if t.list_id == list_id]

            # Filter by status if specified
            if status:
                todos = [t for t in todos if t.status == status]

            # Filter completed if requested
            if not include_completed:
                todos = [t for t in todos if not t.completed]

            return todos

    async def get_todo(
        self,
        todo_id: UUID,
        user_id: Optional[str] = None
    ) -> Optional[Todo]:
        """Get a specific todo by ID.

        Args:
            todo_id: Todo ID
            user_id: Optional user ID for ownership validation

        Returns:
            Todo if found and authorized, None otherwise

        Examples:
            >>> todo = await service.get_todo(todo_id, user_id="user-123")
            >>> if todo:
            ...     print(f"Found: {todo.text}")
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            todo = await todo_repo.get_todo_by_id(todo_id)

            # Validate ownership if user_id provided
            if todo and user_id and todo.owner_id != user_id:
                # User doesn't own this todo
                return None

            return todo

    async def complete_todo(
        self,
        todo_id: UUID,
        user_id: str
    ) -> Optional[Todo]:
        """Mark a todo as complete.

        Args:
            todo_id: Todo to complete
            user_id: User completing the todo (for authorization)

        Returns:
            Completed todo, or None if not found/unauthorized

        Examples:
            >>> completed = await service.complete_todo(todo_id, user_id)
            >>> assert completed.completed is True
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # Get todo
            todo = await todo_repo.get_todo_by_id(todo_id)
            if not todo:
                return None

            # Validate ownership
            if todo.owner_id != user_id:
                return None  # Not authorized

            # Complete todo
            completed_todo = await todo_repo.complete_todo(todo_id)

            return completed_todo

    async def reopen_todo(
        self,
        todo_id: UUID,
        user_id: str
    ) -> Optional[Todo]:
        """Reopen a completed todo.

        Args:
            todo_id: Todo to reopen
            user_id: User reopening (for authorization)

        Returns:
            Reopened todo, or None if not found/unauthorized
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # Get todo
            todo = await todo_repo.get_todo_by_id(todo_id)
            if not todo:
                return None

            # Validate ownership
            if todo.owner_id != user_id:
                return None

            # Reopen todo
            reopened_todo = await todo_repo.reopen_todo(todo_id)

            return reopened_todo

    async def update_todo(
        self,
        todo_id: UUID,
        user_id: str,
        **updates
    ) -> Optional[Todo]:
        """Update todo fields.

        Args:
            todo_id: Todo to update
            user_id: User updating (for authorization)
            **updates: Fields to update

        Returns:
            Updated todo, or None if not found/unauthorized

        Examples:
            >>> updated = await service.update_todo(
            ...     todo_id,
            ...     user_id="user-123",
            ...     priority="urgent",
            ...     due_date=tomorrow
            ... )
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # Get todo
            todo = await todo_repo.get_todo_by_id(todo_id)
            if not todo:
                return None

            # Validate ownership
            if todo.owner_id != user_id:
                return None

            # Update fields
            for key, value in updates.items():
                if hasattr(todo, key):
                    setattr(todo, key, value)

            todo.updated_at = datetime.utcnow()

            # Save
            updated_todo = await todo_repo.update_todo(todo)

            return updated_todo

    async def delete_todo(
        self,
        todo_id: UUID,
        user_id: str
    ) -> bool:
        """Delete a todo.

        Args:
            todo_id: Todo to delete
            user_id: User deleting (for authorization)

        Returns:
            True if deleted, False if not found/unauthorized

        Examples:
            >>> deleted = await service.delete_todo(todo_id, user_id)
            >>> assert deleted is True
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # Get todo
            todo = await todo_repo.get_todo_by_id(todo_id)
            if not todo:
                return False

            # Validate ownership
            if todo.owner_id != user_id:
                return False

            # Delete
            await todo_repo.delete_todo(todo_id)

            return True
```

**Task 1.2: Create Service Tests**

Create `tests/services/test_todo_management_service.py`:

```python
"""Tests for TodoManagementService."""

import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from services.todo.todo_management_service import TodoManagementService
from services.domain.models import Todo


class TestTodoManagementService:
    """Tests for TodoManagementService business logic."""

    @pytest.fixture
    def service(self):
        """Create service instance."""
        return TodoManagementService()

    @pytest.fixture
    def user_id(self):
        """Test user ID."""
        return "test-user-123"

    @pytest.mark.asyncio
    async def test_create_todo_basic(self, service, user_id):
        """Can create todo with minimal fields."""
        todo = await service.create_todo(
            user_id=user_id,
            text="Test todo"
        )

        assert todo.id is not None
        assert todo.text == "Test todo"
        assert todo.owner_id == user_id
        assert todo.priority == "medium"  # Default
        assert todo.completed is False

    @pytest.mark.asyncio
    async def test_create_todo_with_priority(self, service, user_id):
        """Can create todo with priority."""
        todo = await service.create_todo(
            user_id=user_id,
            text="High priority task",
            priority="high"
        )

        assert todo.priority == "high"

    @pytest.mark.asyncio
    async def test_create_todo_validates_text(self, service, user_id):
        """Validates todo text is not empty."""
        with pytest.raises(ValueError, match="cannot be empty"):
            await service.create_todo(user_id=user_id, text="")

        with pytest.raises(ValueError, match="cannot be empty"):
            await service.create_todo(user_id=user_id, text="   ")

    @pytest.mark.asyncio
    async def test_create_todo_validates_priority(self, service, user_id):
        """Validates priority value."""
        with pytest.raises(ValueError, match="Invalid priority"):
            await service.create_todo(
                user_id=user_id,
                text="Test",
                priority="invalid"
            )

    @pytest.mark.asyncio
    async def test_list_todos(self, service, user_id):
        """Can list todos for user."""
        # Create some todos
        todo1 = await service.create_todo(user_id=user_id, text="Todo 1")
        todo2 = await service.create_todo(user_id=user_id, text="Todo 2")

        # List todos
        todos = await service.list_todos(user_id=user_id)

        assert len(todos) >= 2
        todo_ids = [t.id for t in todos]
        assert todo1.id in todo_ids
        assert todo2.id in todo_ids

    @pytest.mark.asyncio
    async def test_list_todos_filters_by_user(self, service, user_id):
        """List filters by user ID."""
        # Create todo for test user
        my_todo = await service.create_todo(user_id=user_id, text="My todo")

        # Create todo for different user
        other_user = "other-user-456"
        other_todo = await service.create_todo(
            user_id=other_user,
            text="Other todo"
        )

        # List todos for test user
        my_todos = await service.list_todos(user_id=user_id)

        # Should only see my todos
        todo_ids = [t.id for t in my_todos]
        assert my_todo.id in todo_ids
        assert other_todo.id not in todo_ids

    @pytest.mark.asyncio
    async def test_get_todo(self, service, user_id):
        """Can get specific todo."""
        created = await service.create_todo(user_id=user_id, text="Get me")

        retrieved = await service.get_todo(created.id, user_id=user_id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.text == "Get me"

    @pytest.mark.asyncio
    async def test_get_todo_validates_ownership(self, service, user_id):
        """Get validates ownership."""
        # Create todo for user A
        todo = await service.create_todo(user_id=user_id, text="Private")

        # Try to get as user B
        other_user = "other-user-456"
        retrieved = await service.get_todo(todo.id, user_id=other_user)

        # Should not get other user's todo
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_complete_todo(self, service, user_id):
        """Can complete todo."""
        todo = await service.create_todo(user_id=user_id, text="Complete me")

        completed = await service.complete_todo(todo.id, user_id=user_id)

        assert completed is not None
        assert completed.completed is True
        assert completed.completed_at is not None
        assert completed.status == "completed"

    @pytest.mark.asyncio
    async def test_complete_validates_ownership(self, service, user_id):
        """Complete validates ownership."""
        todo = await service.create_todo(user_id=user_id, text="My todo")

        # Try to complete as different user
        other_user = "other-user-456"
        result = await service.complete_todo(todo.id, user_id=other_user)

        # Should fail (not authorized)
        assert result is None

    @pytest.mark.asyncio
    async def test_reopen_todo(self, service, user_id):
        """Can reopen completed todo."""
        # Create and complete
        todo = await service.create_todo(user_id=user_id, text="Reopen me")
        await service.complete_todo(todo.id, user_id=user_id)

        # Reopen
        reopened = await service.reopen_todo(todo.id, user_id=user_id)

        assert reopened is not None
        assert reopened.completed is False
        assert reopened.completed_at is None
        assert reopened.status == "pending"

    @pytest.mark.asyncio
    async def test_update_todo(self, service, user_id):
        """Can update todo fields."""
        todo = await service.create_todo(
            user_id=user_id,
            text="Original",
            priority="low"
        )

        # Update
        updated = await service.update_todo(
            todo.id,
            user_id=user_id,
            text="Updated",
            priority="urgent"
        )

        assert updated is not None
        assert updated.text == "Updated"
        assert updated.priority == "urgent"

    @pytest.mark.asyncio
    async def test_delete_todo(self, service, user_id):
        """Can delete todo."""
        todo = await service.create_todo(user_id=user_id, text="Delete me")

        # Delete
        deleted = await service.delete_todo(todo.id, user_id=user_id)
        assert deleted is True

        # Verify deleted
        retrieved = await service.get_todo(todo.id, user_id=user_id)
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_delete_validates_ownership(self, service, user_id):
        """Delete validates ownership."""
        todo = await service.create_todo(user_id=user_id, text="My todo")

        # Try to delete as different user
        other_user = "other-user-456"
        deleted = await service.delete_todo(todo.id, user_id=other_user)

        # Should fail
        assert deleted is False

        # Verify still exists
        retrieved = await service.get_todo(todo.id, user_id=user_id)
        assert retrieved is not None
```

**Task 1.3: Run Service Tests**

```bash
# Run service tests
pytest tests/services/test_todo_management_service.py -xvs

# Should see all tests passing
# Expected: 14+ tests passing
```

**Task 1.4: Manual Verification**

```python
# Test service manually
from services.todo.todo_management_service import TodoManagementService
import asyncio

async def test():
    service = TodoManagementService()

    # Create
    todo = await service.create_todo(
        user_id="test-user",
        text="Manual verification test",
        priority="high"
    )
    print(f"✅ Created: {todo.id} - {todo.text}")

    # List
    todos = await service.list_todos(user_id="test-user")
    print(f"✅ Listed: {len(todos)} todos")

    # Complete
    completed = await service.complete_todo(todo.id, user_id="test-user")
    print(f"✅ Completed: {completed.completed}")

    # Delete
    deleted = await service.delete_todo(todo.id, user_id="test-user")
    print(f"✅ Deleted: {deleted}")

asyncio.run(test())
```

### Completion Criteria
- ✅ TodoManagementService created
- ✅ All service methods implemented
- ✅ 14+ service tests passing
- ✅ Manual verification successful
- ✅ Transaction management working
- ✅ Ownership validation working

### Stop Conditions
- ❌ Service tests failing
- ❌ Transaction errors
- ❌ Repository integration issues

If any stop condition occurs, pause and resolve before proceeding to Phase 2.

---

## Phase 2: Wire Intent Handlers

### Goal
Replace mocked responses in TodoIntentHandlers with real TodoManagementService calls

### Current State

```python
# services/intent_service/todo_handlers.py (CURRENT - mocked)
async def handle_create_todo(self, intent, session_id, user_id):
    text = self._extract_todo_text(intent.original_message)
    priority = self._extract_priority(intent.original_message)

    # PROBLEM: Just returns mock response
    return f"✓ Added todo: {text} (priority: {priority})"
```

### Target State

```python
# services/intent_service/todo_handlers.py (TARGET - real persistence)
async def handle_create_todo(self, intent, session_id, user_id):
    text = self._extract_todo_text(intent.original_message)
    if not text:
        return "I didn't catch what you'd like me to add. Try: 'add todo: [task]'"

    priority = self._extract_priority(intent.original_message)

    try:
        todo = await self.todo_service.create_todo(
            user_id=user_id,
            text=text,
            priority=priority
        )
        return f"✓ Added todo #{todo.id}: {todo.text}"
    except Exception as e:
        logger.error(f"Failed to create todo: {e}")
        return "I had trouble adding that todo. Could you try again?"
```

### Tasks

**Task 2.1: Update Handler Init**

```python
# services/intent_service/todo_handlers.py

from services.todo.todo_management_service import TodoManagementService

class TodoIntentHandlers:
    def __init__(self):
        self.todo_service = TodoManagementService()  # Add this
```

**Task 2.2: Update handle_create_todo**

```python
async def handle_create_todo(self, intent, session_id, user_id):
    """Create todo with database persistence."""
    # Extract todo text
    text = self._extract_todo_text(intent.original_message)
    if not text:
        return "I didn't catch what you'd like me to add. Try: 'add todo: [task]'"

    # Extract priority (optional)
    priority = self._extract_priority(intent.original_message)

    # Extract due date (optional)
    due_date = self._extract_due_date(intent.original_message)

    try:
        # Create todo via service
        todo = await self.todo_service.create_todo(
            user_id=user_id,
            text=text,
            priority=priority,
            due_date=due_date
        )

        # Format response
        response = f"✓ Added todo #{todo.id}: {todo.text}"
        if priority != "medium":
            response += f" (priority: {priority})"
        if due_date:
            response += f" (due: {due_date.strftime('%Y-%m-%d')})"

        return response

    except ValueError as e:
        # Validation error
        return f"I couldn't add that todo: {str(e)}"
    except Exception as e:
        # Database or other error
        logger.error(f"Failed to create todo: {e}", exc_info=True)
        return "I had trouble adding that todo. Could you try again?"
```

**Task 2.3: Update handle_list_todos**

```python
async def handle_list_todos(self, intent, session_id, user_id):
    """List todos from database."""
    try:
        # Get todos via service
        todos = await self.todo_service.list_todos(
            user_id=user_id,
            include_completed=False  # Only active todos
        )

        if not todos:
            return "You don't have any active todos yet. Try: 'add todo: [task]'"

        # Format response
        response = f"Your todos ({len(todos)}):\n"
        for i, todo in enumerate(todos, 1):
            status = "✓" if todo.completed else "○"
            response += f"{i}. {status} {todo.text}"
            if todo.priority == "high" or todo.priority == "urgent":
                response += f" [{todo.priority}]"
            response += "\n"

        return response.strip()

    except Exception as e:
        logger.error(f"Failed to list todos: {e}", exc_info=True)
        return "I had trouble getting your todos. Could you try again?"
```

**Task 2.4: Update handle_complete_todo**

```python
async def handle_complete_todo(self, intent, session_id, user_id):
    """Complete todo in database."""
    # Extract todo ID or text to match
    todo_ref = self._extract_todo_reference(intent.original_message)

    if not todo_ref:
        return "Which todo would you like to complete?"

    try:
        # Get user's todos
        todos = await self.todo_service.list_todos(user_id=user_id)

        # Find matching todo
        todo = self._find_todo_by_reference(todos, todo_ref)

        if not todo:
            return f"I couldn't find that todo: {todo_ref}"

        # Complete it
        completed = await self.todo_service.complete_todo(
            todo.id,
            user_id=user_id
        )

        if completed:
            return f"✓ Completed: {completed.text}"
        else:
            return "I had trouble completing that todo."

    except Exception as e:
        logger.error(f"Failed to complete todo: {e}", exc_info=True)
        return "I had trouble completing that todo. Could you try again?"
```

**Task 2.5: Update handle_delete_todo**

```python
async def handle_delete_todo(self, intent, session_id, user_id):
    """Delete todo from database."""
    # Extract todo reference
    todo_ref = self._extract_todo_reference(intent.original_message)

    if not todo_ref:
        return "Which todo would you like to delete?"

    try:
        # Get user's todos
        todos = await self.todo_service.list_todos(user_id=user_id)

        # Find matching todo
        todo = self._find_todo_by_reference(todos, todo_ref)

        if not todo:
            return f"I couldn't find that todo: {todo_ref}"

        # Delete it
        deleted = await self.todo_service.delete_todo(
            todo.id,
            user_id=user_id
        )

        if deleted:
            return f"✓ Deleted: {todo.text}"
        else:
            return "I had trouble deleting that todo."

    except Exception as e:
        logger.error(f"Failed to delete todo: {e}", exc_info=True)
        return "I had trouble deleting that todo. Could you try again?"
```

### Completion Criteria
- ✅ TodoManagementService added to handler init
- ✅ All 4 handlers updated (create, list, complete, delete)
- ✅ Error handling added
- ✅ Natural language parsing still works
- ✅ Responses include real data

### Verification

```bash
# Quick verification (if handler tests exist)
pytest tests/intent_service/test_todo_handlers.py -xvs

# Manual test via chat interface
# 1. "add todo: Test persistence"
# 2. "list my todos" (should show the todo)
# 3. "complete that todo"
# 4. "delete that todo"
```

---

## Phase 3: Wire API Layer

### Goal
Replace mocked responses in todo API with real TodoManagementService calls

### Current State

```python
# services/api/todo_management.py (CURRENT - mocked)
@router.post("/todos")
async def create_todo(request: TodoCreateRequest):
    # PROBLEM: Returns mock data
    return {
        "id": "mock-id",
        "title": request.title,
        "priority": request.priority
    }
```

### Target State

```python
# services/api/todo_management.py (TARGET - real persistence)
@router.post("/todos")
async def create_todo(
    request: TodoCreateRequest,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    try:
        todo = await service.create_todo(
            user_id=request.owner_id,
            text=request.title,
            priority=request.priority
        )
        return TodoResponse.from_domain(todo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create todo: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Tasks

**Task 3.1: Add Service Dependency**

```python
# services/api/todo_management.py

from fastapi import APIRouter, Depends, HTTPException
from services.todo.todo_management_service import TodoManagementService

router = APIRouter()


def get_todo_management_service() -> TodoManagementService:
    """Dependency for TodoManagementService."""
    return TodoManagementService()
```

**Task 3.2: Update create_todo Endpoint**

```python
@router.post("/todos", response_model=TodoResponse)
async def create_todo(
    request: TodoCreateRequest,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    """Create a new todo."""
    try:
        todo = await service.create_todo(
            user_id=request.owner_id,
            text=request.title,
            priority=request.priority,
            list_id=request.list_id,
            due_date=request.due_date
        )
        return TodoResponse.from_domain(todo)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API create_todo failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Task 3.3: Update list_todos Endpoint**

```python
@router.get("/todos", response_model=List[TodoResponse])
async def list_todos(
    user_id: str,
    list_id: Optional[str] = None,
    include_completed: bool = False,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    """List todos for a user."""
    try:
        todos = await service.list_todos(
            user_id=user_id,
            list_id=list_id,
            include_completed=include_completed
        )
        return [TodoResponse.from_domain(t) for t in todos]

    except Exception as e:
        logger.error(f"API list_todos failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Task 3.4: Update complete_todo Endpoint**

```python
@router.patch("/todos/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(
    todo_id: str,
    user_id: str,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    """Mark todo as complete."""
    try:
        todo = await service.complete_todo(
            UUID(todo_id),
            user_id=user_id
        )

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return TodoResponse.from_domain(todo)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    except Exception as e:
        logger.error(f"API complete_todo failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Task 3.5: Update delete_todo Endpoint**

```python
@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: str,
    user_id: str,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    """Delete a todo."""
    try:
        deleted = await service.delete_todo(
            UUID(todo_id),
            user_id=user_id
        )

        if not deleted:
            raise HTTPException(status_code=404, detail="Todo not found")

        return {"status": "deleted", "todo_id": todo_id}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    except Exception as e:
        logger.error(f"API delete_todo failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Completion Criteria
- ✅ Service dependency added
- ✅ All endpoints updated (create, list, complete, delete)
- ✅ Error handling with proper HTTP status codes
- ✅ Response models return real data

### Verification

```bash
# Test API endpoints
curl -X POST http://localhost:8001/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"owner_id": "test-user", "title": "API test", "priority": "high"}'

# Should return real todo with database ID
```

---

## Phase 4: Integration Tests

### Goal
**CRITICAL**: Prove todos actually persist to database

### Why This Matters

**"Verification Theater" is the problem we're solving**:
- System appears to work (returns confirmations)
- But nothing actually saves
- Users lose all their data

**Integration tests prove persistence**:
- Create via handler → Verify in database
- Complete via API → Verify status changed
- Full lifecycle → Prove end-to-end

### Tasks

**Task 4.1: Create Integration Test File**

Create `tests/integration/test_todo_persistence.py`:

```python
"""
Integration Tests: Todo Persistence

CRITICAL: These tests prove todos actually persist to the database.
Without these tests, we can't verify we're solving "verification theater."

Tests verify:
1. Todos created via handlers persist to database
2. Todos created via API persist to database
3. Full lifecycle (create → list → complete → delete) works end-to-end
4. Database state matches application state
"""

import pytest
from uuid import uuid4

from services.intent_service.todo_handlers import TodoIntentHandlers
from services.todo.todo_management_service import TodoManagementService
from services.repositories.todo_repository import TodoRepository
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Todo


class TestTodoPersistenceIntegration:
    """Integration tests proving todo persistence works."""

    @pytest.fixture
    def user_id(self):
        """Test user ID."""
        return f"test-user-{uuid4()}"

    @pytest.fixture
    def handlers(self):
        """Create TodoIntentHandlers instance."""
        return TodoIntentHandlers()

    @pytest.fixture
    def service(self):
        """Create TodoManagementService instance."""
        return TodoManagementService()

    @pytest.mark.asyncio
    async def test_handler_create_persists_to_database(self, handlers, user_id):
        """CRITICAL: Verify handler creates actually save to database.

        This is the PRIMARY test proving we're not doing "verification theater."
        """
        # Create todo via handler (simulates chat: "add todo: Test")
        from services.intent_service.intent_classifier import Intent

        intent = Intent(
            intent_type="create_todo",
            original_message="add todo: Test persistence",
            confidence=0.95
        )

        response = await handlers.handle_create_todo(
            intent,
            session_id="test-session",
            user_id=user_id
        )

        # Should get confirmation
        assert "Added todo" in response
        assert "Test persistence" in response

        # CRITICAL: Verify in database
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            todos = await repo.get_todos_by_owner(user_id)

            # Todo should exist in database
            assert len(todos) >= 1, "Todo not found in database!"

            # Find our todo
            our_todo = next((t for t in todos if "Test persistence" in t.text), None)
            assert our_todo is not None, "Our todo not found in database!"

            # Verify properties
            assert our_todo.text == "Test persistence"
            assert our_todo.owner_id == user_id
            assert our_todo.completed is False

    @pytest.mark.asyncio
    async def test_handler_list_shows_real_data(self, handlers, user_id):
        """Verify list handler shows real database data."""
        # Create some todos via service
        service = TodoManagementService()
        await service.create_todo(user_id=user_id, text="Todo 1")
        await service.create_todo(user_id=user_id, text="Todo 2")

        # List via handler
        from services.intent_service.intent_classifier import Intent

        intent = Intent(
            intent_type="list_todos",
            original_message="show my todos",
            confidence=0.95
        )

        response = await handlers.handle_list_todos(
            intent,
            session_id="test-session",
            user_id=user_id
        )

        # Should show real todos
        assert "Todo 1" in response
        assert "Todo 2" in response
        assert "2" in response  # Count

    @pytest.mark.asyncio
    async def test_full_lifecycle_via_handlers(self, handlers, user_id):
        """Test complete lifecycle through handlers."""
        from services.intent_service.intent_classifier import Intent

        # 1. Create
        create_intent = Intent(
            intent_type="create_todo",
            original_message="add todo: Lifecycle test",
            confidence=0.95
        )

        create_response = await handlers.handle_create_todo(
            create_intent,
            session_id="test-session",
            user_id=user_id
        )

        assert "Added todo" in create_response

        # 2. List (verify exists)
        list_intent = Intent(
            intent_type="list_todos",
            original_message="show my todos",
            confidence=0.95
        )

        list_response = await handlers.handle_list_todos(
            list_intent,
            session_id="test-session",
            user_id=user_id
        )

        assert "Lifecycle test" in list_response

        # 3. Complete (verify status changes)
        complete_intent = Intent(
            intent_type="complete_todo",
            original_message="complete Lifecycle test",
            confidence=0.95
        )

        complete_response = await handlers.handle_complete_todo(
            complete_intent,
            session_id="test-session",
            user_id=user_id
        )

        assert "Completed" in complete_response

        # Verify in database
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            todos = await repo.get_todos_by_owner(user_id)
            lifecycle_todo = next((t for t in todos if "Lifecycle test" in t.text), None)

            assert lifecycle_todo is not None
            assert lifecycle_todo.completed is True

        # 4. Delete
        delete_intent = Intent(
            intent_type="delete_todo",
            original_message="delete Lifecycle test",
            confidence=0.95
        )

        delete_response = await handlers.handle_delete_todo(
            delete_intent,
            session_id="test-session",
            user_id=user_id
        )

        assert "Deleted" in delete_response

        # Verify deleted from database
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            todos = await repo.get_todos_by_owner(user_id)
            lifecycle_todo = next((t for t in todos if "Lifecycle test" in t.text), None)

            assert lifecycle_todo is None, "Todo should be deleted!"

    @pytest.mark.asyncio
    async def test_service_create_persists(self, service, user_id):
        """Verify service creates persist to database."""
        # Create via service
        todo = await service.create_todo(
            user_id=user_id,
            text="Service test",
            priority="high"
        )

        # Verify in database
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            retrieved = await repo.get_todo_by_id(todo.id)

            assert retrieved is not None
            assert retrieved.text == "Service test"
            assert retrieved.priority == "high"

    @pytest.mark.asyncio
    async def test_multiple_users_isolated(self, service):
        """Verify user data is properly isolated."""
        user1 = "user-1"
        user2 = "user-2"

        # Create todos for each user
        todo1 = await service.create_todo(user_id=user1, text="User 1 todo")
        todo2 = await service.create_todo(user_id=user2, text="User 2 todo")

        # List for user 1
        user1_todos = await service.list_todos(user_id=user1)
        user1_texts = [t.text for t in user1_todos]

        # Should only see user 1's todos
        assert "User 1 todo" in user1_texts
        assert "User 2 todo" not in user1_texts

        # List for user 2
        user2_todos = await service.list_todos(user_id=user2)
        user2_texts = [t.text for t in user2_todos]

        # Should only see user 2's todos
        assert "User 2 todo" in user2_texts
        assert "User 1 todo" not in user2_texts
```

**Task 4.2: Run Integration Tests**

```bash
# Run integration tests
pytest tests/integration/test_todo_persistence.py -xvs

# CRITICAL: All tests must pass
# If any fail, persistence is not working correctly
```

**Task 4.3: Manual End-to-End Test**

```bash
# 1. Start application
python main.py

# 2. Via chat interface (or curl):
# Create: "add todo: Manual E2E test"
# List: "show my todos" (should see the todo)
# Complete: "complete Manual E2E test"
# List again: "show my todos" (should show as completed)
# Delete: "delete Manual E2E test"
# List again: "show my todos" (should be gone)

# 3. Verify in database directly
psql -d piper_morgan -c "SELECT * FROM todo_items LIMIT 10"
```

### Completion Criteria
- ✅ 6+ integration tests created
- ✅ **ALL integration tests passing** (CRITICAL)
- ✅ Manual E2E test successful
- ✅ Database verification successful
- ✅ **No verification theater** - real persistence proven

### Stop Conditions
- ❌ Integration tests failing
- ❌ Todos not persisting to database
- ❌ Manual E2E test fails

If any stop condition occurs, **STOP IMMEDIATELY** and debug. Proceeding without persistence working defeats the entire purpose of this issue.

---

## Phase 5: Validation and Closure

### Goal
Systematically validate all work and properly close Issue #295

### Tasks

**Task 5.1: Run Complete Test Suite**

```bash
# Run all tests
pytest tests/ -v --tb=short

# Should see:
# - Service tests: 14+ passing
# - Integration tests: 6+ passing
# - Handler tests: passing (if they exist)
# - API tests: passing (if they exist)

# Save output
pytest tests/ -v > test-results-295.txt 2>&1
```

**Task 5.2: Create Completion Checklist**

Verify all acceptance criteria from Issue #295:

```markdown
# Issue #295 Completion Checklist

## Prerequisites
- [x] Domain model foundation complete (Item/List primitives)
- [x] ItemService/TodoService available
- [x] Migrations executed (234aa8ec628c)
- [x] Branch foundation/item-list-primitives merged

## Implementation
- [ ] TodoManagementService created
- [ ] Intent handlers wired to service
- [ ] API endpoints wired to service
- [ ] Error handling implemented
- [ ] Ownership validation in place

## Testing
- [ ] Integration tests prove persistence ✅ CRITICAL
- [ ] Full lifecycle test passes
- [ ] Service unit tests pass (14+)
- [ ] Manual verification successful

## Evidence
- [ ] Test results saved (test-results-295.txt)
- [ ] Database verification screenshots/output
- [ ] Manual E2E test documented
- [ ] Session log complete

## Success Metrics
- [ ] Todos persist to database (verified)
- [ ] List shows real data (verified)
- [ ] Complete/delete affect database (verified)
- [ ] No verification theater (verified)
```

**Task 5.3: Create Evidence Package**

```bash
# Create evidence directory
mkdir -p dev/2025/11/04/issue-295-evidence

# Copy artifacts
cp test-results-295.txt dev/2025/11/04/issue-295-evidence/
cp tests/integration/test_todo_persistence.py dev/2025/11/04/issue-295-evidence/
cp services/todo/todo_management_service.py dev/2025/11/04/issue-295-evidence/

# List evidence
ls -lh dev/2025/11/04/issue-295-evidence/
```

**Task 5.4: Update Issue #295**

Add completion comment to GitHub:

```markdown
# Issue #295 Complete ✅

**Completion Date**: [today's date]
**Duration**: [actual time]
**Branch**: [branch name if applicable]

## Deliverables

### 1. TodoManagementService
- **File**: `services/todo/todo_management_service.py`
- **Methods**: 7 (create, list, get, complete, reopen, update, delete)
- **Features**: Transaction management, ownership validation, error handling

### 2. Intent Handlers Wired
- **File**: `services/intent_service/todo_handlers.py`
- **Updated**: 4 handlers (create, list, complete, delete)
- **Status**: Real persistence via TodoManagementService

### 3. API Endpoints Wired
- **File**: `services/api/todo_management.py`
- **Updated**: 4 endpoints (POST, GET, PATCH, DELETE)
- **Status**: Real persistence with proper HTTP error codes

### 4. Integration Tests
- **File**: `tests/integration/test_todo_persistence.py`
- **Tests**: 6 integration tests
- **Status**: All passing ✅
- **Verification**: Todos proven to persist to database

## Validation

### Test Results
- Service tests: 14/14 passing ✅
- Integration tests: 6/6 passing ✅
- Total: 20 new tests ✅

### Manual Verification
Full lifecycle tested:
1. Create via chat: "add todo: Test" ✅
2. List via chat: "show my todos" ✅ (shows real data)
3. Complete via chat: "complete Test" ✅ (persists to DB)
4. Delete via chat: "delete Test" ✅ (removed from DB)

### Database Verification
```sql
-- Verified todos in database
SELECT * FROM todo_items WHERE owner_id = 'test-user';
-- Shows real todos with proper schema
```

## Success Criteria Met

- ✅ Todos actually persist to database (CRITICAL)
- ✅ List shows real todos from database
- ✅ Complete/delete affect real database records
- ✅ Integration test proves persistence
- ✅ Full lifecycle works end-to-end
- ✅ No verification theater

## Evidence Package

**Location**: `dev/2025/11/04/issue-295-evidence/`

**Contents**:
- Test results (20 tests passing)
- Integration test file
- TodoManagementService implementation
- Session log

## Architecture

**Service Layer Pattern** (Nov 3, 2025 - Chief Architect decision):
```
Intent Handlers → TodoManagementService → TodoRepository → Database
```

**Benefits**:
- Business logic in service layer
- Ownership validation
- Transaction management
- Error handling
- Clean separation of concerns

## Next Steps

1. Monitor production usage
2. Consider knowledge graph integration enhancement
3. User authentication (replace "default" user_id)
4. Move to Issue #294 (ActionMapper cleanup)

---

**Status**: ✅ COMPLETE
**Verification Theater**: ✅ ELIMINATED
**Real Persistence**: ✅ PROVEN

Todos now actually save to the database! 🎉
```

### Completion Criteria
- ✅ All tests passing
- ✅ Completion checklist verified
- ✅ Evidence package created
- ✅ Issue #295 updated with evidence
- ✅ Session log complete
- ✅ Ready to close issue

---

## Success Metrics (Final)

### Objective Measures
- ✅ TodoManagementService created (7 methods)
- ✅ Service tests: 14+ passing
- ✅ Integration tests: 6+ passing
- ✅ Intent handlers wired (4 handlers)
- ✅ API endpoints wired (4 endpoints)
- ✅ **All tests passing** (20+ new tests)

### Functional Verification
- ✅ Create todo via chat → Persists to database
- ✅ List todos → Shows real database data
- ✅ Complete todo → Updates database status
- ✅ Delete todo → Removes from database
- ✅ **Full lifecycle works end-to-end**

### Quality Metrics
- ✅ Error handling (try/except, HTTPException)
- ✅ Ownership validation (users can't access others' todos)
- ✅ Transaction management (AsyncSessionFactory.session_scope)
- ✅ Logging (errors logged properly)
- ✅ Response formatting (user-friendly messages)

### Evidence-Based Completion
- ✅ Integration tests prove persistence
- ✅ Manual E2E test successful
- ✅ Database verification confirms data
- ✅ **No verification theater**

---

## Effort Summary

**Foundation Work** (Nov 3-4): COMPLETE ✅
- Domain model refactoring (Phases 0-5)
- Item/List primitives
- Todo extends Item
- ItemService + TodoService
- Effort: Large (comprehensive architectural refactoring)

**Persistence Wiring** (This gameplan): TO DO
- Phase 0: Small effort (pre-implementation check)
- Phase 1: Large effort (TodoManagementService creation)
- Phase 2: Small effort (wire handlers)
- Phase 3: Small effort (wire API)
- Phase 4: Medium effort (integration tests)
- Phase 5: Small effort (validation)
- **Overall Effort**: Medium (service layer + wiring + comprehensive testing)

**Note**: We will take the time needed to do this right. Quality and thoroughness over speed.

---

## Stop Conditions

**STOP IMMEDIATELY if**:
- Prerequisites not met (foundation not merged)
- Service tests failing
- Integration tests failing
- Todos not persisting to database
- Transaction errors
- Ownership validation failing

**DO NOT**:
- Proceed to next phase if current phase fails
- Skip integration tests
- Close issue without persistence verification
- Ignore test failures

---

## Documentation References

**Architecture Decisions**:
- Chief Architect Consultation (Nov 3): `dev/2025/11/03/chief-architect-consultation-todo-persistence.md`
- ADR-041: Domain Model Foundation: `docs/internal/architecture/current/adrs/adr-041-domain-primitives-refactoring.md`

**Investigation**:
- Architecture Discovery: `dev/2025/11/03/todo-persistence-architecture-discovery.md`
- Domain Alignment: `dev/2025/11/03/todo-domain-alignment-assessment.md`

**Foundation Work**:
- Domain Model Gameplan: `dev/2025/11/03/gameplan-domain-model-refactoring.md`
- Phase 5 Validation: `dev/2025/11/04/PHASE-5-VALIDATION-COMPLETE.md`

**Roadmap**:
- Completion Roadmap: `dev/2025/11/04/ROADMAP-TODO-PERSISTENCE-COMPLETION.md`
- Issue #295 Updated: `dev/2025/11/04/issue-295-updated-description.md`

---

## Final Notes

**This is NOT a feature** - it's a critical bug fix:
- Users are currently losing all their todos
- System creates false confidence ("verification theater")
- Violates core promise of todo management

**The solution requires**:
- Proper service layer (TodoManagementService)
- Real database operations (not mocked)
- Integration tests proving persistence
- End-to-end validation

**After this gameplan**:
- Users' todos will persist
- System will be trustworthy
- Foundation ready for future features
- Architecture clean and extensible

**The goal**: Eliminate "verification theater" with proven persistence.

**Success metric**: Integration tests prove todos save to database.

---

*Gameplan: Todo Persistence Completion (Issue #295)*
*Created: November 4, 2025, 4:37 PM*
*Prerequisite: foundation/item-list-primitives merged*
*Effort: Medium (service creation + wiring + comprehensive testing)*
*Goal: Real todo persistence with integration tests*
*Approach: Methodical, thorough, quality-focused*

# CORE-ALPHA-TODO-PERSISTENCE - Wire TodoHandlers to Database (UPDATED)

**Priority**: P1 - CRITICAL
**Labels**: `bug`, `todo-system`, `verification-theater`, `architecture`
**Parent Issue**: #285
**Estimated Effort**: 2-4 hours (revised after domain model foundation completion)
**Updated**: November 4, 2025

---

## Status Update: Domain Model Foundation Complete ✅

**MAJOR UPDATE**: The underlying domain model has been refactored to implement the original architectural vision (Item and List as cognitive primitives). This provides the proper foundation for todo persistence.

**Completed Work** (November 3-4, 2025):
- ✅ Item primitive created (`services/domain/primitives.py`)
- ✅ Todo refactored to extend Item (polymorphic inheritance)
- ✅ Database migrated to items + todo_items structure
- ✅ ItemService + TodoService created (universal operations)
- ✅ 92+ tests, 33/33 validation checks passed
- ✅ ADR-041 documented
- ✅ Branch: `foundation/item-list-primitives` (ready for merge)

**Evidence**:
- Validation Report: `dev/2025/11/04/PHASE-5-VALIDATION-COMPLETE.md`
- ADR-041: `docs/internal/architecture/current/adrs/adr-041-domain-primitives-refactoring.md`
- GitHub Comment: https://github.com/mediajunkie/piper-morgan-product/issues/285#issuecomment-3488492940

This foundation work **must be merged first** before proceeding with this issue.

---

## Critical Issue

**TodoHandlers currently don't persist todos to the database.** The system appears to work (returns confirmations) but todos are lost immediately. This is "verification theater" - the worst kind of bug.

**Without this fix, Issue #285 is NOT complete.**

---

## Current State (After Domain Model Foundation)

### What Works ✅

1. **Domain Model** - Item/Todo polymorphic inheritance
   ```python
   class Item:
       """Universal primitive for all list items"""
       id, text, position, list_id

   class Todo(Item):
       """Todo extends Item with completion and priority"""
       # Inherits: id, text, position, list_id
       # Adds: priority, status, completed, due_date
   ```

2. **Database Schema** - Joined table inheritance
   ```sql
   items table (base):
   ├── id, text, position, list_id, item_type

   todo_items table (specialized):
   ├── id (FK to items.id)
   └── 24 todo-specific columns
   ```

3. **Service Layer** - Universal + specialized operations
   ```python
   class ItemService:
       # 6 universal operations (any item type)
       create_item, get_item, update_item_text,
       reorder_items, delete_item, get_items_in_list

   class TodoService(ItemService):
       # Inherits universal operations
       # Adds 4 todo-specific operations
       create_todo, complete_todo, reopen_todo, set_priority
   ```

4. **Repository Layer** - TodoRepository (17 methods)
   - Basic CRUD, analytics, search, relationships
   - Located: `services/repositories/todo_repository.py` (651 lines)

5. **Natural Language Parsing** - TodoIntentHandlers
   - Extracts intent from user messages
   - Parses todo text, priority, IDs
   - Located: `services/intent_service/todo_handlers.py`

### What's Missing ❌

1. **TodoManagementService** - Doesn't exist yet
   - Should wrap TodoService + TodoRepository
   - Should handle business logic and transaction coordination
   - Should integrate with TodoKnowledgeService for semantic relationships

2. **Intent Handler Wiring** - Handlers return mocked responses
   ```python
   # services/intent_service/todo_handlers.py:52
   async def handle_create_todo(self, intent, session_id, user_id):
       text = self._extract_todo_text(intent.original_message)
       priority = self._extract_priority(intent.original_message)

       # PROBLEM: Just returns confirmation without saving!
       return f"✓ Added todo: {text} (priority: {priority})"
       # User thinks todo is saved, but it's not in database
   ```

3. **API Layer Wiring** - API functions return mocked responses
   ```python
   # services/api/todo_management.py:177-222
   async def create_todo(...):
       # TODO: Implement todo creation with TodoManagementService
       return {"id": "mock-123", "title": request.title, ...}
   ```

**User Experience**:
1. User: "add todo: Review PR"
2. Piper: "✓ Added todo: Review PR"
3. User: "show my todos"
4. Piper: "You don't have any todos yet" ← User confusion!

---

## Implementation Plan

### Prerequisites

**MUST BE DONE FIRST**:
- ✅ Merge `foundation/item-list-primitives` branch
- ✅ Verify migrations executed (234aa8ec628c)
- ✅ Verify ItemService/TodoService available

### Step 1: Create TodoManagementService (1-2 hours)

**Purpose**: Business logic layer that orchestrates repositories and integrates knowledge graph

**Location**: `services/todo/todo_management_service.py` (NEW)

**Structure**:
```python
from services.todo_service import TodoService
from services.repositories.todo_repository import TodoRepository
from services.todo.todo_knowledge_service import TodoKnowledgeService
from services.database.session_factory import AsyncSessionFactory

class TodoManagementService:
    """
    Business logic layer for todo management.

    Orchestrates:
    - TodoService (domain operations)
    - TodoRepository (persistence)
    - TodoKnowledgeService (knowledge graph integration)
    """

    def __init__(self):
        self.todo_service = TodoService()
        self.knowledge_service = TodoKnowledgeService()

    async def create_todo(
        self,
        user_id: str,
        text: str,
        priority: str = "medium",
        list_id: Optional[str] = None,
        **kwargs
    ) -> Todo:
        """
        Create todo with full integration.

        1. Use TodoService to create in database
        2. Create knowledge graph node if needed
        3. Return created todo
        """
        async with AsyncSessionFactory.session_scope() as session:
            # Create todo via service
            todo = await self.todo_service.create_todo(
                text=text,
                list_id=list_id or user_id,  # Default to user's list
                priority=priority,
                owner_id=user_id,
                **kwargs
            )

            # Optional: Create knowledge graph node
            # await self.knowledge_service.create_todo_knowledge_node(todo)

            return todo

    async def list_todos(
        self,
        user_id: str,
        list_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Todo]:
        """List todos for user, optionally filtered."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)

            if list_id:
                todos = await self.todo_service.get_todos_in_list(list_id)
            else:
                todos = await repo.get_todos_by_owner(user_id)

            # Filter by status if provided
            if status:
                todos = [t for t in todos if t.status == status]

            return todos

    async def complete_todo(self, todo_id: UUID, user_id: str) -> Todo:
        """Complete a todo."""
        async with AsyncSessionFactory.session_scope() as session:
            # Verify ownership first
            repo = TodoRepository(session)
            todo = await repo.get_todo_by_id(str(todo_id))

            if not todo or todo.owner_id != user_id:
                raise ValueError("Todo not found or access denied")

            # Complete via service
            return await self.todo_service.complete_todo(todo_id)

    async def delete_todo(self, todo_id: UUID, user_id: str) -> bool:
        """Delete a todo."""
        async with AsyncSessionFactory.session_scope() as session:
            # Verify ownership first
            repo = TodoRepository(session)
            todo = await repo.get_todo_by_id(str(todo_id))

            if not todo or todo.owner_id != user_id:
                raise ValueError("Todo not found or access denied")

            # Delete via service
            return await self.todo_service.delete_item(todo_id)
```

**Tests**: `tests/services/test_todo_management_service.py`
- test_create_todo_persists
- test_list_todos_returns_real_data
- test_complete_todo_updates_status
- test_delete_todo_removes_from_db
- test_ownership_validation

### Step 2: Wire Intent Handlers to Service (30 minutes)

**Update**: `services/intent_service/todo_handlers.py`

**Changes**:
```python
from services.todo.todo_management_service import TodoManagementService

class TodoIntentHandlers:
    def __init__(self):
        self.todo_service = TodoManagementService()  # NEW
        self.logger = logging.getLogger(__name__)

    async def handle_create_todo(self, intent, session_id, user_id):
        """Create todo via service (REAL PERSISTENCE)"""
        text = self._extract_todo_text(intent.original_message)
        if not text:
            return "I didn't catch what you'd like me to add. Try: 'add todo: [task]'"

        priority = self._extract_priority(intent.original_message)

        try:
            # ACTUALLY SAVE TO DATABASE
            todo = await self.todo_service.create_todo(
                user_id=user_id,
                text=text,
                priority=priority
            )
            return f"✓ Added todo #{todo.id}: {todo.text}"
        except Exception as e:
            self.logger.error(f"Failed to create todo: {e}", exc_info=True)
            return "I had trouble adding that todo. Could you try again?"

    async def handle_list_todos(self, intent, session_id, user_id):
        """List todos from database"""
        try:
            todos = await self.todo_service.list_todos(user_id=user_id)

            if not todos:
                return "You don't have any todos yet. Say 'add todo: [task]' to create one!"

            # Format todos
            lines = ["Your todos:"]
            for i, todo in enumerate(todos, 1):
                status = "✓" if todo.completed else "○"
                priority = f"[{todo.priority}]" if todo.priority != "medium" else ""
                lines.append(f"{i}. {status} {todo.text} {priority}")

            return "\n".join(lines)
        except Exception as e:
            self.logger.error(f"Failed to list todos: {e}", exc_info=True)
            return "I had trouble fetching your todos. Please try again."

    async def handle_complete_todo(self, intent, session_id, user_id):
        """Mark todo as complete"""
        todo_id = self._extract_todo_id(intent.original_message)
        if not todo_id:
            return "Which todo would you like to complete? Say 'complete todo 1' or use the todo ID."

        try:
            todo = await self.todo_service.complete_todo(
                todo_id=UUID(todo_id),
                user_id=user_id
            )
            return f"✓ Completed: {todo.text}"
        except ValueError as e:
            return f"I couldn't find that todo. Try 'show my todos' to see your list."
        except Exception as e:
            self.logger.error(f"Failed to complete todo: {e}", exc_info=True)
            return "I had trouble completing that todo. Please try again."

    async def handle_delete_todo(self, intent, session_id, user_id):
        """Delete a todo"""
        todo_id = self._extract_todo_id(intent.original_message)
        if not todo_id:
            return "Which todo would you like to delete? Say 'delete todo 1' or use the todo ID."

        try:
            deleted = await self.todo_service.delete_todo(
                todo_id=UUID(todo_id),
                user_id=user_id
            )
            if deleted:
                return "✓ Todo deleted"
            else:
                return "I couldn't find that todo."
        except ValueError as e:
            return "I couldn't find that todo. Try 'show my todos' to see your list."
        except Exception as e:
            self.logger.error(f"Failed to delete todo: {e}", exc_info=True)
            return "I had trouble deleting that todo. Please try again."
```

### Step 3: Wire API Layer to Service (30 minutes)

**Update**: `services/api/todo_management.py`

**Replace mocked functions**:
```python
from services.todo.todo_management_service import TodoManagementService

# Dependency injection
async def get_todo_management_service():
    """Get TodoManagementService instance"""
    return TodoManagementService()

# Update endpoints
async def create_todo(
    request: TodoCreateRequest,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    """Create a new todo (REAL PERSISTENCE)"""
    try:
        todo = await service.create_todo(
            user_id=request.owner_id or "default",  # TODO: Get from auth
            text=request.title,
            priority=request.priority,
            list_id=request.list_id
        )
        return TodoResponse.from_domain(todo)
    except Exception as e:
        logger.error(f"Failed to create todo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create todo")

async def list_todos(
    user_id: str = "default",
    list_id: Optional[str] = None,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    """List todos (REAL DATA)"""
    try:
        todos = await service.list_todos(
            user_id=user_id,
            list_id=list_id
        )
        return [TodoResponse.from_domain(t) for t in todos]
    except Exception as e:
        logger.error(f"Failed to list todos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list todos")

# Similar updates for get_todo, update_todo, delete_todo, complete_todo
```

### Step 4: Integration Tests (1 hour)

**Create**: `tests/integration/test_todo_persistence.py`

**Test full stack**:
```python
"""
Integration tests verifying todo persistence.

Tests the full flow:
User Input → Intent Handlers → TodoManagementService → TodoService → Repository → Database
"""

import pytest
from uuid import uuid4
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.database.session_factory import AsyncSessionFactory
from services.repositories.todo_repository import TodoRepository

class TestTodoPersistence:
    """Verify todos actually persist to database."""

    @pytest.fixture
    async def handlers(self):
        """Create TodoIntentHandlers instance"""
        return TodoIntentHandlers()

    @pytest.fixture
    def user_id(self):
        """Test user ID"""
        return str(uuid4())

    async def test_create_todo_persists_to_database(self, handlers, user_id):
        """
        CRITICAL TEST: Verify todos actually save to database.

        This is the core issue #295 is solving - todos MUST persist.
        """
        # Create Intent object
        intent = MockIntent(original_message="add todo: Test persistence")

        # Create via handler
        response = await handlers.handle_create_todo(
            intent=intent,
            session_id="test-session",
            user_id=user_id
        )

        # Verify confirmation
        assert "✓ Added todo" in response
        assert "Test persistence" in response

        # CRITICAL: Verify in database
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            todos = await repo.get_todos_by_owner(user_id)

            assert len(todos) == 1
            assert todos[0].text == "Test persistence"
            assert todos[0].owner_id == user_id
            assert todos[0].completed is False

    async def test_list_shows_real_todos(self, handlers, user_id):
        """Verify list command shows actual database todos."""
        # Create todo
        intent1 = MockIntent(original_message="add todo: First todo")
        await handlers.handle_create_todo(intent1, "test-session", user_id)

        intent2 = MockIntent(original_message="add todo: Second todo")
        await handlers.handle_create_todo(intent2, "test-session", user_id)

        # List todos
        list_intent = MockIntent(original_message="show my todos")
        response = await handlers.handle_list_todos(list_intent, "test-session", user_id)

        # Verify both todos appear
        assert "First todo" in response
        assert "Second todo" in response
        assert "Your todos:" in response

    async def test_complete_todo_persists_status(self, handlers, user_id):
        """Verify completing todo updates database."""
        # Create todo
        create_intent = MockIntent(original_message="add todo: Complete me")
        response = await handlers.handle_create_todo(create_intent, "test-session", user_id)

        # Extract todo ID from response (format: "✓ Added todo #<id>: ...")
        import re
        match = re.search(r'#([a-f0-9-]+):', response)
        assert match, f"Could not extract todo ID from: {response}"
        todo_id = match.group(1)

        # Complete todo
        complete_intent = MockIntent(original_message=f"complete todo {todo_id}")
        complete_response = await handlers.handle_complete_todo(
            complete_intent, "test-session", user_id
        )

        assert "✓ Completed" in complete_response

        # Verify in database
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            todo = await repo.get_todo_by_id(todo_id)

            assert todo is not None
            assert todo.completed is True
            assert todo.status == "completed"
            assert todo.completed_at is not None

    async def test_delete_todo_removes_from_database(self, handlers, user_id):
        """Verify deleting todo removes from database."""
        # Create todo
        create_intent = MockIntent(original_message="add todo: Delete me")
        response = await handlers.handle_create_todo(create_intent, "test-session", user_id)

        # Extract todo ID
        import re
        match = re.search(r'#([a-f0-9-]+):', response)
        todo_id = match.group(1)

        # Delete todo
        delete_intent = MockIntent(original_message=f"delete todo {todo_id}")
        delete_response = await handlers.handle_delete_todo(
            delete_intent, "test-session", user_id
        )

        assert "✓ Todo deleted" in delete_response

        # Verify NOT in database
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            todo = await repo.get_todo_by_id(todo_id)

            assert todo is None  # Should be deleted

    async def test_full_lifecycle(self, handlers, user_id):
        """Test complete todo lifecycle: create → list → complete → delete"""
        # Create
        create = MockIntent(original_message="add todo: Full lifecycle test")
        create_resp = await handlers.handle_create_todo(create, "test", user_id)
        assert "✓ Added todo" in create_resp

        # List (should show it)
        list1 = MockIntent(original_message="show todos")
        list_resp1 = await handlers.handle_list_todos(list1, "test", user_id)
        assert "Full lifecycle test" in list_resp1

        # Complete
        import re
        todo_id = re.search(r'#([a-f0-9-]+):', create_resp).group(1)
        complete = MockIntent(original_message=f"complete todo {todo_id}")
        complete_resp = await handlers.handle_complete_todo(complete, "test", user_id)
        assert "✓ Completed" in complete_resp

        # List (should show completed)
        list2 = MockIntent(original_message="show todos")
        list_resp2 = await handlers.handle_list_todos(list2, "test", user_id)
        assert "✓" in list_resp2  # Completed marker

        # Delete
        delete = MockIntent(original_message=f"delete todo {todo_id}")
        delete_resp = await handlers.handle_delete_todo(delete, "test", user_id)
        assert "✓ Todo deleted" in delete_resp

        # Verify database empty
        async with AsyncSessionFactory.session_scope() as session:
            repo = TodoRepository(session)
            todos = await repo.get_todos_by_owner(user_id)
            assert len(todos) == 0

class MockIntent:
    """Mock Intent object for testing"""
    def __init__(self, original_message: str):
        self.original_message = original_message
```

---

## Files to Create/Update

### New Files
1. `services/todo/todo_management_service.py` - Business logic service
2. `tests/services/test_todo_management_service.py` - Service unit tests
3. `tests/integration/test_todo_persistence.py` - Full stack integration tests

### Updated Files
1. `services/intent_service/todo_handlers.py` - Wire to service
2. `services/api/todo_management.py` - Wire to service

---

## Acceptance Criteria

### Prerequisites
- [x] Domain model foundation complete (Item/List primitives)
- [x] ItemService/TodoService available
- [x] Migrations executed (234aa8ec628c)
- [ ] Branch `foundation/item-list-primitives` merged

### Implementation
- [ ] TodoManagementService created with business logic
- [ ] Intent handlers call service (not mocked)
- [ ] API endpoints call service (not mocked)
- [ ] Error handling for database failures
- [ ] Ownership validation in service layer

### Testing
- [ ] **Integration test proves persistence** (CRITICAL)
- [ ] Full lifecycle test passes (create → list → complete → delete)
- [ ] Service unit tests pass
- [ ] All tests verify actual database writes

### Evidence Required
- [ ] Integration test output showing database verification
- [ ] Manual test: Create todo via chat, verify in database directly
- [ ] Manual test: List todos shows real data
- [ ] Manual test: Complete/delete affect real database records

---

## Why This is P1

This is not an enhancement - it's a **critical bug**:
- Users lose all their todos (data loss)
- Creates false confidence in the system
- Violates core promise of todo management
- Classic "verification theater" - appears to work but doesn't

**Without this fix, Issue #285 is incomplete and the todo system is unusable.**

---

## Architecture Decisions Made

Based on investigation and Chief Architect consultation:

1. ✅ **Service Layer Pattern**: Intent Handlers → TodoManagementService → TodoRepository
   - Matches patterns elsewhere in codebase
   - Proper DDD separation of concerns
   - Business logic in service, not handlers

2. ✅ **Create TodoManagementService**: Yes
   - Orchestrates TodoService + TodoRepository
   - Handles business logic (validation, authorization)
   - Integrates knowledge graph when appropriate

3. ✅ **Transaction Boundaries**: Service layer
   - Service creates session scope
   - Repository receives session
   - Proper transaction management

4. ✅ **Domain Model**: Item/List primitives (completed separately)
   - Todo extends Item (polymorphic inheritance)
   - Universal operations via ItemService
   - Extensible for future item types

---

## Related Work

**Completed**:
- Issue #285: Basic todo wiring (API routes, handlers, action mapping)
- Domain Model Foundation: Item/List primitives refactoring
- ADR-041: Domain primitives architectural documentation

**Dependent Issues**:
- Issue #294: ActionMapper cleanup (separate issue)
- Future: Knowledge graph integration for todos
- Future: User authentication integration (replace hardcoded "default" user_id)

---

## Time Estimate

**Total**: 2-4 hours (revised after foundation completion)

- TodoManagementService creation: 1-2 hours
- Handler wiring: 30 minutes
- API wiring: 30 minutes
- Integration tests: 1 hour

**Original estimate was 2 hours but underestimated scope** - investigation revealed two-layer gap (API + handlers) and need for service layer. With domain model foundation now complete, remaining work is well-scoped.

---

## Evidence

**Investigation Reports**:
- `dev/2025/11/03/todo-persistence-architecture-discovery.md` (487 lines)
- `dev/2025/11/03/todo-domain-alignment-assessment.md`
- `dev/2025/11/03/chief-architect-consultation-todo-persistence.md`

**Domain Model Foundation**:
- Validation Report: `dev/2025/11/04/PHASE-5-VALIDATION-COMPLETE.md`
- ADR-041: `docs/internal/architecture/current/adrs/adr-041-domain-primitives-refactoring.md`
- Branch: `foundation/item-list-primitives`

**Current Code**:
- TodoRepository: `services/repositories/todo_repository.py` (651 lines, 17 methods)
- ItemService: `services/item_service.py` (304 lines)
- TodoService: `services/todo_service.py` (200 lines)
- Intent Handlers: `services/intent_service/todo_handlers.py` (mocked)
- API: `services/api/todo_management.py` (mocked)

---

**Updated**: November 4, 2025, 4:20 PM
**Next Step**: Merge `foundation/item-list-primitives` branch, then proceed with TodoManagementService creation

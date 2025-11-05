# Chief Architect Consultation: Todo Persistence Architecture

**Date**: November 3, 2025, 2:50 PM
**From**: Lead Developer (Sonnet 4.5)
**Re**: Issue #295 - Architectural decisions needed for todo persistence
**Investigation**: Completed by Code Agent, 17 minutes, comprehensive findings

---

## Executive Summary

**Good News**: Infrastructure is **90% complete** - TodoRepository exists with 17 methods including CRUD, analytics, search, and relationships. The repository pattern is fully implemented.

**The Gap**: Two layers need wiring:
1. API layer (mocked) → TodoRepository (implemented)
2. Intent handlers (mocked) → API layer or repositories

**Decision Required**: 5 architectural questions about how to wire these layers together following DDD principles.

**Investigation Report**: `dev/active/todo-persistence-architecture-discovery.md` (487 lines, comprehensive)

---

## What We Discovered (The Good News)

### 1. TodoRepository is Comprehensive (17 Methods)

Located in `services/repositories/todo_repository.py` (651 lines):

**Basic CRUD**:
- `create_todo`, `get_todo_by_id`, `update_todo`, `delete_todo`

**Query Operations**:
- `get_todos_by_owner`, `get_assigned_todos`, `get_due_todos`
- `search_todos` (with filters)

**State Management**:
- `complete_todo`, `reopen_todo`

**Analytics**:
- `get_completion_stats` (user productivity metrics)

**Relationships**:
- `get_subtodos`, `get_related_todos`

### 2. Complete Repository Pattern Exists

**Four Repository Classes**:
- `TodoRepository` (17 methods)
- `TodoListRepository` (11 methods)
- `ListMembershipRepository` (14 methods)
- `TodoManagementRepository` (integrated facade combining all three)

**Database Models**:
- `TodoDB`, `TodoListDB`, `ListMembershipDB`
- All with `.from_domain()` and `.to_domain()` conversion methods

**Pattern Quality**: Follows DDD principles, proper domain/persistence separation

### 3. What's Missing (The Gap)

**API Layer** (`services/api/todo_management.py`):
- Has CRUD function signatures ✅
- Returns mock responses ❌
- Contains TODO comments: "Implement with TodoManagementService"
- **Status**: Needs wiring to repositories

**Intent Handlers** (`services/intent_service/todo_handlers.py`):
- Natural language parsing works ✅
- Returns mock confirmations ❌
- No database calls ❌
- **Status**: Needs wiring to API or repositories

### 4. Consistent Patterns Elsewhere

Investigation found **repository + service pattern** used consistently:
- FileRepository + FileService
- Repositories handle database operations
- Services handle business logic
- API/Handlers use services, NOT repositories directly

---

## The 5 Architectural Questions

These decisions will determine implementation approach:

### Question 1: How Should Intent Handlers Access Data?

**Three Options**:

**Option A: Intent Handlers → API Layer → Repositories**
```
User Input → TodoIntentHandlers → todo_management API → TodoRepository → Database
```
**Pros**:
- Clean separation of concerns
- API layer usable by other clients (mobile, web)
- RESTful routing pattern

**Cons**:
- Extra layer adds complexity
- API layer is HTTP-focused (may be unnecessary for internal calls)

**Option B: Intent Handlers → Service Layer → Repositories**
```
User Input → TodoIntentHandlers → TodoManagementService → TodoRepository → Database
```
**Pros**:
- Matches patterns elsewhere in codebase
- Service layer handles business logic
- No HTTP overhead for internal calls
- DDD-aligned (services orchestrate repositories)

**Cons**:
- TodoManagementService doesn't exist yet (but easy to create)
- Need to decide what goes in service vs. repository

**Option C: Intent Handlers → Repositories Directly**
```
User Input → TodoIntentHandlers → TodoRepository → Database
```
**Pros**:
- Simplest path
- Fastest to implement

**Cons**:
- ❌ Violates DDD principles (handlers shouldn't talk to repositories directly)
- ❌ Breaks patterns used elsewhere
- ❌ Business logic ends up in handlers (wrong layer)
- ❌ Not what PM wants (explicitly rejected shortcuts)

**Recommendation**: Option B (Service Layer) - matches codebase patterns, DDD-aligned

---

### Question 2: Do We Need TodoManagementService?

**Context**:
- `TodoKnowledgeService` exists but handles knowledge graph only (semantic relationships)
- API comments reference "TodoManagementService" but it doesn't exist
- Service layer pattern is used elsewhere (FileService, etc.)

**The Question**: Create TodoManagementService to handle:
- Business logic (validation, authorization)
- Transaction coordination
- Knowledge graph integration orchestration
- Event emission (if/when we add events)

**Option A: Create TodoManagementService** ⭐
```python
class TodoManagementService:
    def __init__(self):
        self.todo_repo = TodoRepository()
        self.knowledge_service = TodoKnowledgeService()

    async def create_todo(self, user_id, title, priority):
        # Validate
        # Create in database via repository
        # Create knowledge node if needed
        # Return domain object
```

**Pros**:
- Matches patterns elsewhere
- Clear location for business logic
- Orchestrates repository + knowledge graph
- Room for validation, events, etc.

**Cons**:
- Extra class to create (but small effort)

**Option B: Use TodoManagementRepository Directly**

**Pros**:
- Already exists (integrated facade)
- One less layer

**Cons**:
- Business logic ends up in handlers
- Knowledge graph integration unclear
- Breaks service layer pattern

**Recommendation**: Option A (Create TodoManagementService) - matches architectural patterns

---

### Question 3: When Should Knowledge Graph Integration Happen?

**Context**:
- `TodoKnowledgeService` exists with methods for semantic relationships
- Currently separate from persistence
- Could be integrated automatically or on-demand

**Options**:

**Option A: Automatic on Create/Update**
- Every todo creates knowledge node
- Automatic relationship discovery
- Always kept in sync

**Option B: On-Demand Only**
- User explicitly requests "find similar todos"
- Knowledge nodes created when needed
- Lighter weight, opt-in

**Option C: Background Job**
- Todos created immediately
- Knowledge graph updated async
- Best performance, eventual consistency

**Question for You**: What's the UX vision for knowledge graph integration?

---

### Question 4: TodoRepository vs UniversalListRepository?

**Context**:
- `TodoRepository` exists and works (17 methods, tested)
- `UniversalListRepository` exists as generic list system
- TodoLists have compatibility wrapper connecting both

**The Question**: Which should todo persistence use?

**Option A: Use TodoRepository** ⭐
```python
# Clear, specific, working now
service.todo_repo = TodoRepository()
todo = await service.todo_repo.create_todo(...)
```

**Option B: Migrate to UniversalListRepository**
```python
# Generic, future-proof, but requires migration
service.list_repo = UniversalListRepository()
item = await service.list_repo.create_item(type="todo", ...)
```

**Recommendation**: Option A (TodoRepository) for now
- Stable, tested, domain-specific
- UniversalList migration can happen later if needed
- Don't let perfect be enemy of done

---

### Question 5: Where Should Transaction Boundaries Live?

**Context**: Session management exists (`services/database/session_factory.py`)

**The Question**: Who manages database transactions?

**Option A: Service Layer** ⭐
```python
class TodoManagementService:
    async def create_todo(self, ...):
        async with get_session() as session:
            todo_repo = TodoRepository(session)
            # Do work in transaction
            await session.commit()
```

**Pros**:
- Business operation = transaction
- Clear boundary
- Service orchestrates multiple repositories if needed

**Option B: Repository Layer**
```python
class TodoRepository:
    async def create_todo(self, ...):
        async with get_session() as session:
            # Transaction here
```

**Cons**:
- Each repository call is separate transaction
- Can't coordinate multiple repositories easily

**Option C: Handler/API Layer**
```python
# Request scope = transaction
async with get_session() as session:
    handler.handle_create_todo(session, ...)
```

**Cons**:
- Couples HTTP request lifecycle to database transactions
- Messy for non-HTTP entry points

**Recommendation**: Option A (Service Layer) - matches DDD patterns

---

## Recommended Architecture

Based on investigation findings and codebase patterns:

```
User Input
    ↓
TodoIntentHandlers (natural language parsing)
    ↓
TodoManagementService (business logic, transactions)
    ↓
TodoRepository (database operations)
    ↓
Database
```

**With Optional**:
```
TodoManagementService → TodoKnowledgeService (semantic relationships)
```

### Implementation Plan (After Your Decisions)

**Step 1: Create TodoManagementService** (45 min)
```python
class TodoManagementService:
    def __init__(self):
        self.todo_repo = TodoRepository()
        self.knowledge_service = TodoKnowledgeService()

    async def create_todo(self, user_id: str, title: str, priority: str) -> Todo:
        async with get_session() as session:
            todo_repo = TodoRepository(session)

            # Create in database
            todo = await todo_repo.create_todo(
                Todo(user_id=user_id, title=title, priority=priority)
            )

            # Optional: Create knowledge node
            if self.should_create_knowledge_node():
                await self.knowledge_service.create_todo_knowledge_node(todo)

            await session.commit()
            return todo

    # Similar for list, update, delete, complete
```

**Step 2: Wire Intent Handlers to Service** (30 min)
```python
class TodoIntentHandlers:
    def __init__(self):
        self.todo_service = TodoManagementService()

    async def handle_create_todo(self, intent, session_id, user_id):
        text = self._extract_todo_text(intent.original_message)
        priority = self._extract_priority(intent.original_message)

        try:
            todo = await self.todo_service.create_todo(
                user_id=user_id,
                title=text,
                priority=priority
            )
            return f"✓ Added todo #{todo.id}: {todo.title}"
        except Exception as e:
            logger.error("Failed to create todo", error=str(e))
            return "I had trouble adding that todo..."
```

**Step 3: Wire API Layer to Service** (30 min)
```python
# services/api/todo_management.py
@router.post("/todos")
async def create_todo(request: TodoCreateRequest):
    service = TodoManagementService()
    todo = await service.create_todo(
        user_id=request.user_id,
        title=request.title,
        priority=request.priority
    )
    return TodoResponse.from_domain(todo)
```

**Step 4: Integration Tests** (45 min)
```python
@pytest.mark.asyncio
async def test_todo_full_cycle():
    # Create via intent handler
    handler = TodoIntentHandlers()
    response = await handler.handle_create_todo(...)

    # Verify in database
    async with get_session() as session:
        repo = TodoRepository(session)
        todos = await repo.get_todos_by_owner(user_id)

    assert len(todos) == 1
    assert todos[0].title == expected_title
```

**Total Estimated Time**: 2.5-3 hours

---

## Questions for Your Decision

1. **Architecture**: Do you approve the Service Layer approach (Option B from Q1)?
   - Intent Handlers → TodoManagementService → TodoRepository

2. **Service Layer**: Should we create TodoManagementService?
   - Handles business logic, transactions, orchestration

3. **Knowledge Graph**: When should todos create knowledge nodes?
   - Always? On-demand? Background job?

4. **Repository**: Use TodoRepository (stable now) or migrate to UniversalListRepository?
   - Recommendation: TodoRepository for now

5. **Transactions**: Service layer manages transactions?
   - Service methods are transaction boundaries

---

## Additional Considerations

### ADR Candidate?

This is a good candidate for an ADR:
- **Title**: "ADR-XXX: Todo Persistence Architecture - Service Layer Pattern"
- **Decision**: Use service layer (TodoManagementService) between handlers and repositories
- **Rationale**: Matches codebase patterns, DDD principles, clear separation of concerns
- **Consequences**: Need to create service, but gains business logic layer

### Issue #295 Scope Update

Original issue said "Wire handlers to TodoKnowledgeService" but:
- TodoKnowledgeService doesn't do CRUD (only knowledge graph)
- Need TodoManagementService (doesn't exist yet)
- Gap is in TWO layers (API + handlers)

Recommend updating issue description to reflect actual scope.

### Timeline

**Current Time**: 2:50 PM
**Estimated Work**: 2.5-3 hours after architectural decisions
**Could Finish**: Today if decisions made soon

But NO urgency - alpha user, no production pressure, do it right.

---

## Summary

**Situation**: Better than expected - 90% of infrastructure exists
**Gap**: Two layers need wiring following DDD principles
**Recommendation**: Service layer pattern (matches codebase, DDD-aligned)
**Estimate**: 2.5-3 hours to implement after your decisions
**Blocker**: Need your architectural decisions on 5 questions

**The core question**: Do you approve Service Layer architecture?
```
Handlers → TodoManagementService → TodoRepository → Database
```

If yes, we can proceed. If you prefer different architecture, please specify.

**Investigation Complete**: Full findings in `dev/active/todo-persistence-architecture-discovery.md`

Awaiting your architectural guidance.

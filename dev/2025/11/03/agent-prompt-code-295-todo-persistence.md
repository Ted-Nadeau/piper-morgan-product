# Prompt for Code Agent: Issue #295 - Wire TodoHandlers to Database (P1 CRITICAL)

## Your Identity
You are Code Agent (Claude Code with Sonnet 4.5), a specialized development agent with broad codebase investigation capabilities. You have full context from Issue #285 where you validated the TodoHandlers and discovered they return mock data instead of persisting to the database.

## Session Log Management

**Continue your existing session log**: `dev/2025/11/03/2025-11-03-0615-prog-code-log.md`

Add timestamped entries for Issue #295 work:
- Investigation of service layer
- Implementation of database calls
- Integration test creation
- Evidence of actual persistence

---

## Mission

**CRITICAL**: Wire TodoHandlers to actually persist todos to the database. This is P1 because the system currently appears to work (returns confirmations) but todos are lost immediately. This is "verification theater" - users think todos are saved but they're not.

**Specific Objective**: Replace mock confirmation messages with actual TodoKnowledgeService calls that persist todos to the database, and create integration tests that verify actual database writes (not mocked).

**Scope**: This prompt covers ONLY the TodoHandlers integration with database persistence. API routes are already mounted. Natural language parsing already works.

---

## Context

**GitHub Issue**: #295 - CORE-ALPHA-TODO-PERSISTENCE
**Parent Issue**: #285 (cannot be closed until #295 complete)
**Current State**:
- TodoHandlers parse natural language correctly ✅
- Handlers return mock confirmation messages ✅
- Todos are NOT persisted to database ❌
- API routes exist but aren't called by handlers ❌
- TodoKnowledgeService exists and is ready to use ✅

**Target State**:
- TodoHandlers call TodoKnowledgeService methods
- Todos persist to actual database
- Handlers return real todo data (with IDs)
- Integration tests prove actual database persistence
- Full CRUD cycle works end-to-end

**Dependencies**:
- TodoKnowledgeService (exists in `services/todo/todo_knowledge_service.py`)
- Database models (exist in `services/database/models.py`)
- Todo tables (exist in database)

**User Data Risk**: LOW - Creating new functionality, not modifying existing data

**Infrastructure Verified**: YES - Service layer and database exist

---

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:

**"TodoHandlers now call TodoKnowledgeService"** → Show the import and actual method calls in code
**"Todos persist to database"** → Show integration test output with actual database query results
**"Integration tests pass"** → Show pytest output with database verification
**"Full cycle works"** → Show create→list→complete→delete terminal output with actual IDs
**"Database has the data"** → Show actual SQL query results or ORM query output
**"Committed changes"** → Show `git log --oneline -1` and `git show HEAD --stat`

### Critical Testing Evidence Required:

You MUST create integration tests that verify actual database persistence:
```bash
# This test MUST show actual database queries
pytest tests/integration/test_todo_persistence.py -xvs

# Expected output should show:
# - Todo created in database (with actual ID)
# - Todo retrieved from database (shows in list)
# - Todo updated in database (status changed)
# - Todo deleted from database (no longer exists)
```

### The "Verification Theater" Test:

Before claiming complete, run this manual verification:
```python
# In a Python shell or test
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.database import get_session

# Create todo via handler
handler = TodoIntentHandlers()
response = await handler.handle_create_todo(intent, session_id, user_id)

# CRITICAL: Verify it's actually in the database
async with get_session() as db:
    todos = await db.execute("SELECT * FROM todos WHERE user_id = ?", user_id)
    print(f"Todos in database: {todos.all()}")  # Must show the todo!
```

**If the database query returns empty, you have NOT solved the problem.**

### Completion Bias Prevention:

- **NO "should persist now"** - only "here's the database query showing it persisted"
- **NO "integration should work"** - only "here's the test output proving it works"
- **NO "probably saves"** - only "here's the actual row in the database"
- **NO assumptions** - every claim backed by terminal output or test results

---

## Constraints & Requirements

### CRITICAL Design Constraints:

1. **Use TodoKnowledgeService, NOT direct API imports**
   ```python
   # CORRECT:
   from services.todo.todo_knowledge_service import TodoKnowledgeService
   self.todo_service = TodoKnowledgeService()

   # WRONG:
   from services.api.todo_management import create_todo  # Don't do this
   ```

2. **Service Layer Abstraction**
   - TodoKnowledgeService handles business logic
   - Handlers call service methods
   - Service calls database through repositories
   - Proper separation of concerns

3. **Transaction Safety**
   - Use try/except for database errors
   - Return user-friendly error messages on failure
   - Log technical details server-side

4. **Real Data, Not Mocks**
   - Handlers must return actual todo IDs from database
   - Must return actual todo objects from database
   - Integration tests must query actual database

### Technical Requirements:

1. **All 4 Handlers Must Call Service**:
   - `handle_create_todo` → `todo_service.create_todo()`
   - `handle_list_todos` → `todo_service.list_todos()`
   - `handle_complete_todo` → `todo_service.update_todo()`
   - `handle_delete_todo` → `todo_service.delete_todo()`

2. **Error Handling**:
   ```python
   try:
       todo = await self.todo_service.create_todo(...)
       return f"✓ Added todo #{todo.id}: {todo.title}"
   except Exception as e:
       logger.error(f"Failed to create todo: {e}")
       return "I had trouble adding that todo. Could you try again?"
   ```

3. **Integration Tests Required**:
   - Create `tests/integration/test_todo_persistence.py`
   - Tests must verify actual database writes
   - NOT mocked - real database queries
   - Test full CRUD cycle

---

## Implementation Steps

### Phase 1: Investigation (15 minutes)

**MANDATORY FIRST ACTIONS**:

```bash
# 1. Check TodoKnowledgeService interface
cat services/todo/todo_knowledge_service.py | head -50

# 2. Check available methods
grep "async def" services/todo/todo_knowledge_service.py

# 3. Check current handler implementation
cat services/intent_service/todo_handlers.py

# 4. Check database models
grep "class Todo" services/database/models.py -A 10

# 5. Verify database tables exist
# (if you have database access, check schema)
```

**Document findings**:
- What methods does TodoKnowledgeService provide?
- What parameters do they require?
- What do they return?
- How are todos stored in database?

### Phase 2: Update TodoHandlers (30 minutes)

**Step 1: Add TodoKnowledgeService**
```python
# services/intent_service/todo_handlers.py

from services.todo.todo_knowledge_service import TodoKnowledgeService
import structlog

logger = structlog.get_logger()

class TodoIntentHandlers:
    def __init__(self):
        self.todo_service = TodoKnowledgeService()
```

**Step 2: Update handle_create_todo**
```python
async def handle_create_todo(self, intent, session_id, user_id):
    """Create a todo and persist to database"""
    text = self._extract_todo_text(intent.original_message)
    if not text:
        return "I didn't catch what you'd like me to add. Try: 'add todo: [task]'"

    priority = self._extract_priority(intent.original_message)

    try:
        # Actually save to database!
        todo = await self.todo_service.create_todo(
            user_id=user_id,
            text=text,
            priority=priority or "medium"
        )

        # Return real data with ID
        return f"✓ Added todo #{todo.id}: {todo.title} (priority: {todo.priority})"

    except Exception as e:
        logger.error(f"Failed to create todo", error=str(e), user_id=user_id)
        return "I had trouble adding that todo. Could you try again?"
```

**Step 3: Update handle_list_todos**
```python
async def handle_list_todos(self, intent, session_id, user_id):
    """List todos from database"""
    try:
        # Get real todos from database
        todos = await self.todo_service.list_todos(
            user_id=user_id,
            limit=10
        )

        if not todos:
            return "You don't have any todos yet. Try: 'add todo: [task]'"

        # Format response with real data
        lines = ["Your todos:"]
        for i, todo in enumerate(todos, 1):
            status = "✓" if todo.completed else "○"
            lines.append(f"{i}. {status} {todo.title} (#{todo.id})")

        lines.append("\nTry: 'mark todo [number] as complete'")
        return "\n".join(lines)

    except Exception as e:
        logger.error(f"Failed to list todos", error=str(e), user_id=user_id)
        return "I had trouble fetching your todos. Could you try again?"
```

**Step 4: Update handle_complete_todo**
```python
async def handle_complete_todo(self, intent, session_id, user_id):
    """Mark todo as complete in database"""
    todo_id = self._extract_todo_id(intent.original_message)
    if not todo_id:
        return "Which todo? Try: 'mark todo [number] as complete'"

    try:
        # Update in database
        todo = await self.todo_service.update_todo(
            todo_id=todo_id,
            completed=True
        )

        return f"✓ Completed todo #{todo.id}: {todo.title}"

    except Exception as e:
        logger.error(f"Failed to complete todo", error=str(e), todo_id=todo_id)
        return "I had trouble updating that todo. Could you try again?"
```

**Step 5: Update handle_delete_todo**
```python
async def handle_delete_todo(self, intent, session_id, user_id):
    """Delete todo from database"""
    todo_id = self._extract_todo_id(intent.original_message)
    if not todo_id:
        return "Which todo should I remove? Try: 'delete todo [number]'"

    try:
        # Delete from database
        await self.todo_service.delete_todo(todo_id=todo_id)

        return f"✓ Removed todo #{todo_id}"

    except Exception as e:
        logger.error(f"Failed to delete todo", error=str(e), todo_id=todo_id)
        return "I had trouble removing that todo. Could you try again?"
```

### Phase 3: Create Integration Tests (45 minutes)

**Create `tests/integration/test_todo_persistence.py`**:

```python
"""
Integration tests for todo persistence.

These tests verify that todos actually persist to the database,
not just that handlers return mock responses.
"""
import pytest
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.database import get_session
from services.database.models import Todo

@pytest.mark.asyncio
async def test_todo_create_persists_to_database():
    """Verify create_todo actually writes to database"""
    handler = TodoIntentHandlers()

    # Create todo via handler
    intent = create_mock_intent("add todo: Test integration")
    response = await handler.handle_create_todo(intent, "session-1", "user-1")

    # CRITICAL: Verify in actual database
    async with get_session() as db:
        todos = await db.execute(
            "SELECT * FROM todos WHERE user_id = ? AND title LIKE ?",
            ("user-1", "%Test integration%")
        )
        result = todos.all()

    # Must actually be in database
    assert len(result) == 1, "Todo not found in database!"
    assert result[0].title == "Test integration"
    assert "Test integration" in response  # Handler response correct

@pytest.mark.asyncio
async def test_todo_list_reads_from_database():
    """Verify list_todos returns actual database records"""
    handler = TodoIntentHandlers()

    # Create a todo directly in database
    async with get_session() as db:
        todo = Todo(user_id="user-2", title="Database todo", priority="high")
        db.add(todo)
        await db.commit()
        todo_id = todo.id

    # List via handler
    intent = create_mock_intent("show my todos")
    response = await handler.handle_list_todos(intent, "session-2", "user-2")

    # Must show the todo from database
    assert "Database todo" in response
    assert str(todo_id) in response

@pytest.mark.asyncio
async def test_todo_complete_updates_database():
    """Verify complete_todo actually updates database"""
    handler = TodoIntentHandlers()

    # Create todo
    async with get_session() as db:
        todo = Todo(user_id="user-3", title="Test complete", completed=False)
        db.add(todo)
        await db.commit()
        todo_id = todo.id

    # Complete via handler
    intent = create_mock_intent(f"mark todo {todo_id} as complete")
    response = await handler.handle_complete_todo(intent, "session-3", "user-3")

    # CRITICAL: Verify database was updated
    async with get_session() as db:
        updated_todo = await db.get(Todo, todo_id)

    assert updated_todo.completed == True, "Database not updated!"
    assert "Completed" in response

@pytest.mark.asyncio
async def test_todo_delete_removes_from_database():
    """Verify delete_todo actually removes from database"""
    handler = TodoIntentHandlers()

    # Create todo
    async with get_session() as db:
        todo = Todo(user_id="user-4", title="Test delete")
        db.add(todo)
        await db.commit()
        todo_id = todo.id

    # Delete via handler
    intent = create_mock_intent(f"delete todo {todo_id}")
    response = await handler.handle_delete_todo(intent, "session-4", "user-4")

    # CRITICAL: Verify gone from database
    async with get_session() as db:
        deleted_todo = await db.get(Todo, todo_id)

    assert deleted_todo is None, "Todo still in database!"
    assert "Removed" in response

@pytest.mark.asyncio
async def test_full_todo_cycle():
    """Test complete cycle: create → list → complete → delete"""
    handler = TodoIntentHandlers()
    user_id = "user-cycle"

    # 1. Create
    intent_create = create_mock_intent("add todo: Cycle test")
    response_create = await handler.handle_create_todo(intent_create, "s1", user_id)
    assert "Added todo" in response_create

    # 2. List (should show the todo)
    intent_list = create_mock_intent("show my todos")
    response_list = await handler.handle_list_todos(intent_list, "s1", user_id)
    assert "Cycle test" in response_list

    # Extract todo ID from response
    import re
    match = re.search(r'#(\d+)', response_list)
    assert match, "Could not find todo ID in list response"
    todo_id = int(match.group(1))

    # 3. Complete
    intent_complete = create_mock_intent(f"mark todo {todo_id} done")
    response_complete = await handler.handle_complete_todo(intent_complete, "s1", user_id)
    assert "Completed" in response_complete

    # 4. Verify completed in database
    async with get_session() as db:
        todo = await db.get(Todo, todo_id)
        assert todo.completed == True

    # 5. Delete
    intent_delete = create_mock_intent(f"delete todo {todo_id}")
    response_delete = await handler.handle_delete_todo(intent_delete, "s1", user_id)
    assert "Removed" in response_delete

    # 6. Verify gone from database
    async with get_session() as db:
        deleted = await db.get(Todo, todo_id)
        assert deleted is None

def create_mock_intent(message: str):
    """Helper to create mock Intent object"""
    from services.intent.models import Intent
    return Intent(
        category="EXECUTION",
        action="todo_action",
        original_message=message
    )
```

### Phase 4: Test and Verify (30 minutes)

```bash
# 1. Run integration tests
pytest tests/integration/test_todo_persistence.py -xvs

# Expected: All tests pass with actual database verification

# 2. Run existing unit tests (should still pass)
pytest tests/intent_service/test_todo_handlers.py -xvs

# 3. Manual verification (optional but recommended)
python -c "
from services.intent_service.todo_handlers import TodoIntentHandlers
# ... create todo via handler ...
# ... query database directly ...
# ... verify todo is there ...
"

# 4. Check for any broken tests
pytest tests/ -k todo

# 5. Verify nothing else broke
pytest tests/intent_service/ -xvs
```

### Phase 5: Commit and Document (15 minutes)

```bash
# Commit changes
git add services/intent_service/todo_handlers.py
git add tests/integration/test_todo_persistence.py
git commit -m "fix: Wire TodoHandlers to database persistence (#295)

- Add TodoKnowledgeService integration to all handlers
- Replace mock responses with actual database calls
- Add integration tests verifying database persistence
- Test full CRUD cycle: create→list→complete→delete

Fixes #295 - todos now actually persist to database"

git log --oneline -1
git show HEAD --stat
```

---

## Completion Criteria

**DO NOT CLAIM COMPLETE WITHOUT ALL OF THESE**:

### Code Changes:
- [ ] TodoKnowledgeService imported and instantiated in TodoIntentHandlers
- [ ] `handle_create_todo` calls `todo_service.create_todo()` and returns real ID
- [ ] `handle_list_todos` calls `todo_service.list_todos()` and returns real data
- [ ] `handle_complete_todo` calls `todo_service.update_todo()` with completed=True
- [ ] `handle_delete_todo` calls `todo_service.delete_todo()` and removes from DB
- [ ] All handlers have try/except error handling
- [ ] All handlers log errors with structlog

### Testing:
- [ ] Integration test file created: `tests/integration/test_todo_persistence.py`
- [ ] Test: `test_todo_create_persists_to_database` PASSES
- [ ] Test: `test_todo_list_reads_from_database` PASSES
- [ ] Test: `test_todo_complete_updates_database` PASSES
- [ ] Test: `test_todo_delete_removes_from_database` PASSES
- [ ] Test: `test_full_todo_cycle` PASSES (end-to-end)
- [ ] All existing unit tests still pass
- [ ] Integration tests query actual database (not mocked)

### Evidence:
- [ ] pytest output showing all integration tests passing
- [ ] Example of actual database query showing todo exists
- [ ] Example of full cycle terminal output (create→list→complete→delete)
- [ ] git commit hash and stats showing changes
- [ ] Session log updated with evidence

### Verification:
- [ ] Can create todo and it persists to database
- [ ] Can list todos and see real data from database
- [ ] Can complete todo and database updates
- [ ] Can delete todo and it's removed from database
- [ ] Error handling works (try with invalid IDs)
- [ ] No "verification theater" - actual persistence confirmed

---

## STOP Conditions

**STOP and report if**:
- TodoKnowledgeService doesn't have expected methods
- Database schema doesn't match expectations
- Existing tests start failing after changes
- Integration tests can't access database
- Service layer requires configuration you don't understand

**DO NOT**:
- Guess at TodoKnowledgeService interface
- Assume database persistence works without testing
- Skip integration tests
- Use mocked database in integration tests
- Claim complete without database verification

---

## Cross-Validation Protocol

**Not required for this task** - straightforward implementation with clear verification criteria. Lead Developer will review evidence when you report complete.

---

## Success Metrics

**Primary**: Integration tests prove actual database persistence
**Secondary**: Full CRUD cycle works end-to-end
**Tertiary**: Existing unit tests still pass

**The core metric**: Can you show a database query that returns a todo created via TodoHandlers?

If you can run this and get a result, you've succeeded:
```sql
SELECT * FROM todos WHERE title = 'Test todo created via handler';
-- Must return a row!
```

---

## Critical Reminders

1. **This is P1 CRITICAL** - Users are losing data right now
2. **Verification theater is the enemy** - Must prove actual persistence
3. **Integration tests are mandatory** - Unit tests with mocks hide the problem
4. **Real database queries required** - Show actual rows in database
5. **TodoKnowledgeService not direct API** - Proper abstraction layer
6. **Error handling matters** - Users need friendly messages on failure
7. **Evidence before claims** - Database queries before "it works"

**The bug**: System appears to work but doesn't persist
**The fix**: Actually call service layer and verify in database
**The proof**: Integration tests showing actual database writes

---

## Time Estimate

- Phase 1 (Investigation): 15 minutes
- Phase 2 (Update Handlers): 30 minutes
- Phase 3 (Integration Tests): 45 minutes
- Phase 4 (Test & Verify): 30 minutes
- Phase 5 (Commit & Document): 15 minutes

**Total**: ~2 hours 15 minutes

---

## Final Note

**This is not about adding a feature - it's about fixing a critical bug.**

Users think their todos are saved. They're not. This violates the core promise of todo management.

The only acceptable completion is **empirical proof that todos persist to the database**. Integration tests showing actual database queries. Terminal output showing real todo IDs. Database queries returning actual rows.

**Complete = database queries return todos created via handlers.**

Anything less is still verification theater.

Good luck! 🏰

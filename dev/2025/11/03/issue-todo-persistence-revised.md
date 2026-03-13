# CORE-ALPHA-TODO-PERSISTENCE - Wire TodoHandlers to Database

**Priority**: P1 - CRITICAL
**Labels**: `bug`, `todo-system`, `verification-theater`
**Parent Issue**: #285
**Estimated Effort**: 2 hours

## Critical Issue

**TodoHandlers currently don't persist todos to the database.** The system appears to work (returns confirmations) but todos are lost immediately. This is "verification theater" - the worst kind of bug.

**Without this fix, Issue #285 is NOT complete.**

## Current State (The Problem)

```python
# services/intent_service/todo_handlers.py:52
async def handle_create_todo(self, intent, session_id, user_id):
    text = self._extract_todo_text(intent.original_message)
    priority = self._extract_priority(intent.original_message)

    # PROBLEM: Just returns confirmation without saving!
    return f"✓ Added todo: {text} (priority: {priority})"
    # User thinks todo is saved, but it's not in database
```

**User Experience**:
1. User: "add todo: Review PR"
2. Piper: "✓ Added todo: Review PR"
3. User: "show my todos"
4. Piper: "You don't have any todos yet" ← User confusion!

## Required Solution

Wire TodoHandlers to use the existing TodoKnowledgeService:

### 1. Use Service Layer (NOT direct API imports)
```python
from services.todo.todo_knowledge_service import TodoKnowledgeService

class TodoIntentHandlers:
    def __init__(self):
        self.todo_service = TodoKnowledgeService()  # Proper abstraction
```

### 2. Implement with Transaction Safety
```python
async def handle_create_todo(self, intent, session_id, user_id):
    text = self._extract_todo_text(intent.original_message)
    if not text:
        return "I didn't catch what you'd like me to add. Try: 'add todo: [task]'"

    priority = self._extract_priority(intent.original_message)

    try:
        # Actually save to database!
        todo = await self.todo_service.create_todo(
            user_id=user_id,
            text=text,
            priority=priority
        )
        return f"✓ Added todo #{todo.id}: {todo.title}"
    except Exception as e:
        logger.error(f"Failed to create todo: {e}")
        return "I had trouble adding that todo. Could you try again?"
```

### 3. Similar Updates for Other Handlers
- `handle_list_todos` - Call `todo_service.list_todos()`
- `handle_complete_todo` - Call `todo_service.update_todo()`
- `handle_delete_todo` - Call `todo_service.delete_todo()`

## Implementation Steps

1. Add TodoKnowledgeService to handler init
2. Update all 4 handler methods to use service
3. Add try/except blocks for database errors
4. **Create integration tests that verify database persistence**
5. Test full cycle: create→list→complete→delete

## Files to Update

- `services/intent_service/todo_handlers.py` - Add service calls
- `tests/integration/test_todo_persistence.py` - NEW: Verify DB writes

## Acceptance Criteria

- [x] Natural language parsing works (already complete)
- [ ] **Todos actually persist to database** ← CRITICAL
- [ ] List shows real todos from database
- [ ] Complete/delete affect real database records
- [ ] Error handling for database failures
- [ ] **Integration test proves persistence**

## Why This is P1

This is not an enhancement - it's a critical bug:
- Users lose all their todos
- Creates false confidence in the system
- Violates core promise of todo management
- Classic "80% done" pattern we must avoid

## Testing Requirements

**Integration Test REQUIRED**:
```python
async def test_todo_persistence():
    # Create todo via handler
    response = await handler.handle_create_todo(...)

    # Verify in database
    todos = await db.query("SELECT * FROM todos WHERE user_id = ?")
    assert len(todos) == 1
    assert todos[0].title == "Review PR"
```

**Not just mocked** - must verify actual database writes.

## Evidence

**Current Code**: `services/intent_service/todo_handlers.py` (mock responses only)
**Service Exists**: `services/todo/todo_knowledge_service.py` (ready to use)
**Database Ready**: Todo tables exist and tested
**Time to Fix**: 2 hours with proper service approach

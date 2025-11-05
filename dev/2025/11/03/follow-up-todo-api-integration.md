# Follow-Up: Wire TodoHandlers to Real todo_management API

**Priority**: P2 - Feature Enhancement
**Labels**: `enhancement`, `todo-system`
**Parent Issue**: #285
**Estimated Effort**: 2-3 hours

## Problem

TodoIntentHandlers currently return confirmation messages with mock data instead of calling the actual todo_management API. The infrastructure is fully wired (router + handlers + mapping) but handlers don't persist todos to the database.

## Current State

**What Works** ✅:
- API router mounted at `/api/v1/todos/*`
- Chat handlers parse natural language correctly
- Action mapping routes todo actions
- Error handling for missing text/IDs
- Priority extraction working

**What's Mock** ⏸️:
```python
# services/intent_service/todo_handlers.py:52
async def handle_create_todo(self, intent, session_id, user_id):
    text = self._extract_todo_text(intent.original_message)
    priority = self._extract_priority(intent.original_message)

    # For now, return confirmation (API returns mock data)
    # In future, call todo_management.create_todo via API
    return f"✓ Added todo: {text} (priority: {priority})"
```

## Proposed Solution

Wire TodoIntentHandlers to call `services/api/todo_management.py` functions:

### 1. Import todo_management functions
```python
from services.api.todo_management import (
    create_todo,
    list_todos,
    update_todo,
    delete_todo,
)
```

### 2. Update handle_create_todo
```python
async def handle_create_todo(self, intent, session_id, user_id):
    text = self._extract_todo_text(intent.original_message)
    if not text:
        return "I didn't catch what you'd like me to add..."

    priority = self._extract_priority(intent.original_message)

    # Create TodoCreateRequest
    request = TodoCreateRequest(
        title=text,
        priority=priority,
        user_id=user_id,
    )

    # Call API
    todo = await create_todo(request)

    return f"✓ Added todo #{todo.id}: {todo.title} (priority: {todo.priority})"
```

### 3. Update handle_list_todos
```python
async def handle_list_todos(self, intent, session_id, user_id):
    # Call API
    todos = await list_todos(user_id=user_id, limit=10)

    if not todos:
        return "You don't have any todos yet. Try: 'add todo: [task]'"

    # Format response
    lines = ["Your todos:"]
    for i, todo in enumerate(todos, 1):
        status = "✓" if todo.completed else "○"
        lines.append(f"{i}. {status} {todo.title} ({todo.priority} priority)")

    lines.append("\nTry: 'mark todo [number] as complete'")
    return "\n".join(lines)
```

### 4. Update handle_complete_todo
```python
async def handle_complete_todo(self, intent, session_id, user_id):
    todo_id = self._extract_todo_id(intent.original_message)
    if not todo_id:
        return "Which todo? Try: 'mark todo [number] as complete'"

    # Call API
    request = TodoUpdateRequest(completed=True)
    todo = await update_todo(todo_id, request)

    return f"✓ Completed todo #{todo.id}: {todo.title}"
```

### 5. Update handle_delete_todo
```python
async def handle_delete_todo(self, intent, session_id, user_id):
    todo_id = self._extract_todo_id(intent.original_message)
    if not todo_id:
        return "Which todo should I remove? Try: 'delete todo [number]'"

    # Call API
    await delete_todo(todo_id)

    return f"✓ Removed todo #{todo_id}"
```

## Implementation Steps

1. Review `services/api/todo_management.py` API (16 endpoints)
2. Import required functions and models
3. Update all 4 handler methods
4. Add error handling for API failures
5. Test with actual database
6. Update unit tests to mock API calls

## Files to Update

- `services/intent_service/todo_handlers.py` - Wire API calls
- `tests/intent_service/test_todo_handlers.py` - Mock API calls in tests

## Acceptance Criteria

- [ ] Handlers call real todo_management API functions
- [ ] Todos persist to database
- [ ] Handlers return real todo data (ID, title, priority, status)
- [ ] Error handling for API failures (todo not found, etc.)
- [ ] Unit tests updated to mock API calls
- [ ] Manual testing: create→list→complete→delete workflow

## Testing Plan

1. Unit tests: Mock API calls, verify correct requests
2. Integration tests: Test with real database
3. Manual testing: Chat commands end-to-end

## Notes

- `services/api/todo_management.py` already has all CRUD operations
- Database models exist in `services/database/models.py`
- TodoKnowledgeService has business logic
- Just need to wire handlers to existing API

## Evidence

**Current Implementation**: `services/intent_service/todo_handlers.py` (162 lines)
**Validation**: 11/11 unit tests passing (natural language parsing verified)
**API Reference**: `services/api/todo_management.py` (663 lines, 16 endpoints)

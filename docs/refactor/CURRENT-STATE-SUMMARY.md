# Todo Implementation - Current State

**Date**: 2025-11-03 16:16 PM PT
**Purpose**: Baseline documentation before domain model refactoring
**Context**: Phase 0 of Item/List primitives implementation

---

## Executive Summary

**Current Architecture**: Todo is a standalone atomic domain object (NOT extending Item primitive)

**Key Finding**: TodoList properly delegates to universal List, but Todo itself is independent with rich domain-specific fields. This is the architecture we're changing.

**Refactoring Goal**: Make Todo extend Item base class per original cognitive primitives vision.

---

## Key Files

### Domain Models
- **Domain Model**: `services/domain/models.py:947` (Todo class)
- **Domain TodoList**: `services/domain/models.py:987` (TodoList - already delegates to List)
- **Universal List**: `services/domain/models.py:866` (List primitive)
- **Universal ListItem**: `services/domain/models.py:909` (ListItem primitive)

### Database Layer
- **Database Model**: `services/database/models.py:889` (TodoDB - 30+ fields)
- **Database TodoListDB**: `services/database/models.py:787`
- **Table Name**: `todos` (will need migration to `items`/`todo_items` pattern)

### Repository Layer
- **Main Repository**: `services/repositories/todo_repository.py:155` (TodoRepository - 17 methods)
- **TodoList Repository**: `services/repositories/todo_repository.py:23` (TodoListRepository)
- **Universal Repository**: `services/repositories/universal_list_repository.py:22` (UniversalListRepository)
- **Integrated Repository**: `services/repositories/todo_repository.py:562` (TodoManagementRepository)

### Service Layer
- **Knowledge Service**: `services/todo/todo_knowledge_service.py:24` (TodoKnowledgeService)

### API Layer
- **API Endpoints**: `services/api/todo_management.py` (8 request/response models)
- **Intent Handlers**: `services/intent_service/todo_handlers.py:25` (TodoIntentHandlers)

### Shared Types
- **Enums**: `services/shared_types.py:109` (TodoStatus), `services/shared_types.py:117` (TodoPriority)

---

## Critical Properties

### Todo Domain Model (services/domain/models.py:947)
**Current Structure**: Standalone dataclass with no inheritance
```python
@dataclass
class Todo:
    """Standalone Todo domain object - no coupling to TodoList"""
    id: str
    title: str          # ← WILL BECOME text (Item property)
    description: str
    priority: str       # ← Todo-specific
    status: str         # ← Todo-specific
    due_date: Optional[datetime]
    tags: List[str]
    assignee_id: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
```

**Key Change**: `title` field will become `text` (Item base class property)

### TodoDB Database Model (services/database/models.py:889)
**Current Table**: `todos` (single table with all fields)
**Fields Count**: 30+ fields including:
- Core: id, title, description, status, priority
- Hierarchical: parent_id, position, children relationship
- Scheduling: due_date, reminder_date, scheduled_date
- Context: tags, project_id, context
- Progress: estimated_minutes, actual_minutes, completion_notes
- Integration: knowledge_node_id, related_todos, external_refs
- Intent: creation_intent, intent_confidence
- Ownership: owner_id, assigned_to
- Timestamps: created_at, updated_at, completed_at

**Migration Challenge**: Need to split into:
- `items` table (base Item fields)
- `todo_items` table (todo-specific fields)
- Polymorphic mapping with item_type discriminator

---

## Statistics

**Code Impact Analysis**:
- **Total Todo-related classes**: 20 unique classes (excluding duplicates and venv)
  - 1 domain model (Todo)
  - 1 database model (TodoDB)
  - 2 repository classes (TodoRepository, TodoListRepository)
  - 1 management repository (TodoManagementRepository)
  - 1 knowledge service (TodoKnowledgeService)
  - 1 intent handler (TodoIntentHandlers)
  - 8 API models (request/response classes)
  - 2 enum types (TodoStatus, TodoPriority)
  - 3 list-related classes (TodoListDB, TodoList, TodoListRepository)

- **Uses of .title property**: 7 occurrences
  - services/database/models.py:898 (TodoDB column definition)
  - services/database/models.py (in TodoDB.from_domain())
  - services/repositories/todo_repository.py:277 (search query)
  - services/repositories/todo_repository.py:449 (alphabetical ordering)
  - services/todo/todo_knowledge_service.py:44 (metadata)
  - services/todo/todo_knowledge_service.py:61 (semantic content)
  - services/todo/todo_knowledge_service.py:116 (update metadata)
  - services/api/todo_management.py (mock response)

- **Uses of Todo() instantiation**: 1 occurrence
  - Most todos created via domain.Todo(**data) pattern or TodoDB.to_domain()

- **TodoRepository references**: 3 files reference TodoRepository
  - Repository file itself
  - Tests (if any)
  - Service layer (if wired)

- **Database migrations**: 95 lines referencing "todos" in alembic/
  - Will need new migration for items table
  - Data migration from todos → items + todo_items

- **API endpoints**: 8 request/response model classes
  - TodoCreateRequest (has .title field)
  - TodoUpdateRequest
  - TodoResponse (has .title field)
  - TodoListCreateRequest
  - TodoListUpdateRequest
  - TodoListResponse (appears twice - might be duplicate)
  - TodoListListResponse

---

## Dependencies

### What Depends on Todo

**Direct Dependencies**:
1. **TodoDB** (database model) - Has .title column, will need .text
2. **TodoRepository** - All CRUD operations use Todo domain model
3. **TodoKnowledgeService** - References todo.title in metadata
4. **TodoIntentHandlers** - Creates and manages todos (currently mocked)
5. **API Models** - TodoCreateRequest/TodoResponse use .title field

**Indirect Dependencies**:
1. **UniversalListRepository** - Works with ListItem referencing todo.id
2. **Knowledge Graph** - Links to todos via knowledge_node_id
3. **Project Context** - Todos can belong to projects
4. **External Integrations** - GitHub issues, etc. link to todos

### What Todo Does NOT Depend On

**Good News**:
- Todo is NOT tightly coupled to TodoList (already decoupled)
- No circular dependencies found
- Clean separation between domain/database/api layers

---

## Critical Changes Required

### Phase 1: Create Item Primitive

**New Files**:
- `services/domain/primitives.py` - Item and List base classes
- `services/database/models/primitives.py` - ItemDB base model

**Impact**: Zero (additive only)

### Phase 2: Refactor Todo to Extend Item

**Modified Files**:
1. `services/domain/models.py` - Todo(Item) with text property
2. `services/database/models.py` - TodoDB(ItemDB) polymorphic
3. `services/repositories/todo_repository.py` - Work with Item hierarchy
4. `services/todo/todo_knowledge_service.py` - Use todo.text not todo.title
5. `services/api/todo_management.py` - Map title→text in API layer

**Migration Required**:
- Create `items` table
- Create `todo_items` table
- Migrate data from `todos` → `items` + `todo_items`
- Add polymorphic discriminator

**Breaking Changes**:
- API field rename: `title` → `text` (needs compatibility layer)
- Database table rename: `todos` → `todo_items`
- Repository method signatures may change

---

## Test Coverage

**Status**: Will be documented in Task 2

**Expected**:
- Unit tests for Todo domain model
- Integration tests for TodoRepository
- API tests for todo endpoints
- Knowledge service tests

---

## Migration Complexity Assessment

### Database Schema Changes

**Current**:
```sql
CREATE TABLE todos (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,           -- Will move to items.text
    description TEXT,
    status VARCHAR,
    priority VARCHAR,
    -- ... 25+ more fields
)
```

**Target**:
```sql
CREATE TABLE items (
    id VARCHAR PRIMARY KEY,
    text VARCHAR NOT NULL,             -- Universal property
    position INTEGER,
    list_id VARCHAR,
    item_type VARCHAR NOT NULL,        -- Discriminator: 'todo'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE todo_items (
    id VARCHAR PRIMARY KEY,
    completed BOOLEAN,
    completed_at TIMESTAMP,
    priority VARCHAR,
    due_date TIMESTAMP,
    -- ... todo-specific fields only
    FOREIGN KEY (id) REFERENCES items(id)
);
```

**Migration Steps**:
1. Create items table
2. Insert todos data into items (title → text, item_type = 'todo')
3. Rename todos → todo_items
4. Drop title column from todo_items
5. Add FK from todo_items.id → items.id

**Estimated Complexity**: MODERATE (data migration required, but straightforward)

---

## Backward Compatibility Concerns

### API Compatibility

**Issue**: API currently uses `title` field
```json
{
  "title": "Buy milk",
  "priority": "high"
}
```

**Solution Options**:
1. **Accept both fields** - title OR text (during transition)
2. **Alias in Pydantic** - title = Field(alias="text")
3. **Version API** - /v2 uses text, /v1 uses title

**Recommendation**: Option 1 (accept both, deprecate title)

### Repository Compatibility

**Issue**: Existing code calls TodoRepository expecting Todo objects

**Solution**: Todo still returns Todo objects, just now Todo extends Item
- Interface unchanged (still has .priority, .status, etc.)
- Added .text property from Item base
- Migration path for .title → .text

---

## Risk Assessment

### Low Risk
✅ TodoList already uses universal pattern (no change needed)
✅ Repository pattern well-established
✅ Tests can validate behavior unchanged

### Medium Risk
⚠️ Database migration requires data movement
⚠️ API field rename needs compatibility handling
⚠️ 7 files reference .title property

### High Risk
❌ None identified (good test coverage expected)

---

## Files That Will Need Updating

### Phase 1 (Create Primitives)
- NEW: `services/domain/primitives.py`
- NEW: `services/database/models/primitives.py`
- NEW: `alembic/versions/XXX_create_items_table.py`
- NEW: `tests/domain/test_primitives.py`

### Phase 2 (Refactor Todo)
- MODIFY: `services/domain/models.py` (Todo class)
- MODIFY: `services/database/models.py` (TodoDB class)
- MODIFY: `services/repositories/todo_repository.py` (7 .title references)
- MODIFY: `services/todo/todo_knowledge_service.py` (3 .title references)
- MODIFY: `services/api/todo_management.py` (API models)
- MODIFY: All test files referencing todos

---

## Success Criteria for Refactoring

**Phase 0 (This Document)**:
- ✅ Complete state documented
- ✅ All todo-related code catalogued
- ✅ Impact analysis complete
- ✅ Migration path identified

**Phase 1 (Create Primitives)**:
- Item and List base classes exist
- Tests pass for primitives
- No existing functionality affected

**Phase 2 (Refactor Todo)**:
- Todo extends Item
- todo.text works (todo.title deprecated)
- All tests still pass
- Database migration successful

**Phase 3-4 (Services & Integration)**:
- Services work with Item hierarchy
- API maintains compatibility
- End-to-end tests pass

**Phase 5 (Validation)**:
- Zero functionality regression
- Performance unchanged
- Documentation complete
- Can easily add new item types (ShoppingItem, ReadingItem)

---

## Notes

**Key Insight from Investigation**:
TodoList already properly uses the universal pattern (delegates to List with item_type='todo'). The refactoring is primarily about making Todo extend Item, not about fixing the list architecture.

**PM's Original Vision Confirmed**:
Documentation shows "PM-081: Chief Architect's universal composition over specialization principle" - this refactoring aligns domain models with that documented vision.

**Existing Universal Infrastructure**:
- UniversalListRepository already exists
- List and ListItem primitives already exist
- TodoList and ListMembership already delegate to universals
- Only missing piece: Todo extending Item

**This is Foundation Work**:
Getting this right enables shopping lists, reading lists, project backlogs, and any future list type to be added with minimal effort.

---

*Documentation complete. Ready for Task 2: Test Coverage Analysis.*

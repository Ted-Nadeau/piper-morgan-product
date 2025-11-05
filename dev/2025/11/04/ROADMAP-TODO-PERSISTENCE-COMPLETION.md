# Roadmap: Todo Persistence Completion

**Created**: November 4, 2025, 4:25 PM
**Status**: Foundation Complete, Roadmap Established

---

## Executive Summary

**What We Discovered**: The path to completing todo persistence took a winding route through architectural discovery, domain model refactoring, and systematic validation. This document traces that path and establishes a clear roadmap for completion.

**Current State**: ✅ Domain model foundation complete and validated
**Remaining Work**: TodoManagementService + wiring (2-4 hours estimated)
**Next Steps**: Merge foundation, then execute 4-step implementation plan

---

## The Winding Path (Nov 3-4, 2025)

### 1. Issue #285: Complete Todo System Implementation ✅

**Completed**: November 3, 2025
**Scope**: Basic wiring of todo system
**Deliverables**:
- ✅ Mounted todo API router (`/api/v1/todos/*`)
- ✅ Created TodoIntentHandlers (natural language parsing)
- ✅ Added 14 action mappings to ActionMapper
- ✅ Routes accessible, handlers working

**Limitation**: Mocked responses only - no actual persistence

### 2. Issue #295 Drafted → Investigation Launched

**Initial Scope**: "Wire TodoHandlers to Database" (estimated 2 hours)
**Assumption**: Simple task of connecting handlers to existing service

**Reality Check**: Investigation revealed much more complexity

### 3. Investigation Phase: Todo Persistence Architecture Discovery

**Report**: `dev/2025/11/03/todo-persistence-architecture-discovery.md` (487 lines)
**Duration**: 17 minutes (Serena-enabled semantic navigation)

**Key Findings**:
1. ✅ **TodoRepository exists** - 651 lines, 17 methods, comprehensive
2. ✅ **Full repository pattern** - TodoRepository, TodoListRepository, ListMembershipRepository
3. ✅ **Session management** - AsyncSessionFactory with proper context managers
4. ❌ **Two layers mocked** - Both API and handlers need wiring
5. ❌ **TodoKnowledgeService** - Knowledge graph only, NOT CRUD
6. ⚠️ **Architecture decision needed** - How to wire layers together?

**Impact**: Scope larger than estimated (2 layers, not 1)

### 4. Domain Alignment Assessment

**Report**: `dev/2025/11/03/todo-domain-alignment-assessment.md`
**Duration**: 12 minutes

**Critical Discovery**:
- ✅ TodoList properly uses universal List (item_type='todo')
- ✅ ListMembership properly uses universal ListItem
- ❌ **Todo is standalone object** - Doesn't use Item primitive pattern
- ⚠️ **Architectural divergence** - Todo doesn't follow Item/List vision

**Implication**: Need to fix domain model before proceeding with persistence

### 5. Chief Architect Consultation

**Report**: `dev/2025/11/03/chief-architect-consultation-todo-persistence.md`

**5 Architectural Questions Raised**:
1. How should handlers access data? (Service layer recommended)
2. Need TodoManagementService? (Yes, for business logic)
3. Transaction boundaries? (Service layer)
4. Knowledge graph integration? (Via service orchestration)
5. Universal list migration? (Use current TodoRepository, stable)

**Key Decision**: Todo should extend Item primitive (original vision)

### 6. Gameplan: Domain Model Foundation Repair

**Document**: `dev/2025/11/03/gameplan-domain-model-refactoring.md`

**Vision**: Item and List as cognitive primitives, todos as specialization

**5-Phase Plan**:
- Phase 0: Pre-flight checklist (documentation, branch, safety nets)
- Phase 1: Create Item/List primitives
- Phase 2: Refactor Todo to extend Item
- Phase 3: Create universal service layer (ItemService, TodoService)
- Phase 4: Integration tests and ADR documentation
- Phase 5: Systematic validation and evidence gathering

**Estimated Time**: 8-10 hours across phases

### 7. Domain Model Refactoring Execution (Nov 3-4)

**Work Performed**: Phases 0-5 complete
**Duration**: ~8.5 hours actual work across 2 days
**Branch**: `foundation/item-list-primitives`

**Deliverables**:
- ✅ Item primitive created (`services/domain/primitives.py`)
- ✅ Todo refactored to extend Item (polymorphic inheritance)
- ✅ Database migrated (items + todo_items joined tables)
- ✅ ItemService created (6 universal operations)
- ✅ TodoService created (extends ItemService, 4 todo-specific operations)
- ✅ 92+ comprehensive tests
- ✅ 33/33 validation checks passed (100% success rate)
- ✅ ADR-041 documented (354 lines)
- ✅ Evidence package created (7 artifacts)

**Validation**:
- 8/8 success metrics met
- Zero regressions
- Zero data loss
- Backward compatibility maintained

**Status**: ✅ Complete and validated, ready for merge

---

## Current State: After Foundation

### What Works ✅

1. **Domain Model** - Polymorphic inheritance
   ```python
   class Item:
       id, text, position, list_id

   class Todo(Item):
       # Inherits Item properties
       # Adds: priority, status, completed, due_date
   ```

2. **Database Schema** - Joined table inheritance
   ```
   items (base) → todo_items (specialized)
   ```

3. **Service Layer** - Universal + specialized
   ```python
   ItemService (6 universal operations)
   └── TodoService (inherits + 4 todo-specific)
   ```

4. **Repository Layer** - TodoRepository (17 methods)

5. **Natural Language Parsing** - TodoIntentHandlers work

### What's Missing ❌

1. **TodoManagementService** - Business logic layer (doesn't exist)
2. **Handler Wiring** - Still mocked responses
3. **API Wiring** - Still mocked responses
4. **Integration Tests** - End-to-end persistence verification

---

## Roadmap: Completing Issue #295

### Prerequisites

1. ✅ Domain model foundation complete (Item/List primitives)
2. ✅ Issue #295 updated with comprehensive roadmap
3. ⏸️ **Awaiting**: Doc analysis completion
4. ⏸️ **Required**: Merge `foundation/item-list-primitives` branch

### Step 1: Create TodoManagementService (1-2 hours)

**File**: `services/todo/todo_management_service.py` (NEW)

**Purpose**: Business logic layer orchestrating:
- TodoService (domain operations)
- TodoRepository (persistence)
- TodoKnowledgeService (knowledge graph integration)

**Key Methods**:
```python
async def create_todo(user_id, text, priority, ...) -> Todo
async def list_todos(user_id, list_id, status) -> List[Todo]
async def complete_todo(todo_id, user_id) -> Todo
async def delete_todo(todo_id, user_id) -> bool
```

**Features**:
- Transaction management (AsyncSessionFactory.session_scope)
- Ownership validation
- Error handling
- Knowledge graph integration points

**Tests**: `tests/services/test_todo_management_service.py`

### Step 2: Wire Intent Handlers (30 minutes)

**File**: `services/intent_service/todo_handlers.py` (UPDATE)

**Changes**:
- Add `TodoManagementService` dependency
- Replace mocked responses with service calls
- Add try/except error handling
- Format responses with real data

**Example**:
```python
async def handle_create_todo(self, intent, session_id, user_id):
    text = self._extract_todo_text(intent.original_message)
    priority = self._extract_priority(intent.original_message)

    todo = await self.todo_service.create_todo(
        user_id=user_id,
        text=text,
        priority=priority
    )
    return f"✓ Added todo #{todo.id}: {todo.text}"
```

### Step 3: Wire API Layer (30 minutes)

**File**: `services/api/todo_management.py` (UPDATE)

**Changes**:
- Create `get_todo_management_service()` dependency
- Replace mocked functions with service calls
- Add proper error handling (HTTPException)
- Return real data from database

**Example**:
```python
async def create_todo(
    request: TodoCreateRequest,
    service: TodoManagementService = Depends(get_todo_management_service)
):
    todo = await service.create_todo(
        user_id=request.owner_id,
        text=request.title,
        priority=request.priority
    )
    return TodoResponse.from_domain(todo)
```

### Step 4: Integration Tests (1 hour)

**File**: `tests/integration/test_todo_persistence.py` (NEW)

**Critical Test**:
```python
async def test_create_todo_persists_to_database(handlers, user_id):
    # Create via handler
    response = await handlers.handle_create_todo(...)

    # VERIFY IN DATABASE
    async with AsyncSessionFactory.session_scope() as session:
        repo = TodoRepository(session)
        todos = await repo.get_todos_by_owner(user_id)
        assert len(todos) == 1
        assert todos[0].text == "Test persistence"
```

**Additional Tests**:
- Full lifecycle (create → list → complete → delete)
- List shows real todos
- Complete persists status change
- Delete removes from database

---

## Acceptance Criteria

### Prerequisites
- [x] Domain model foundation complete
- [x] ItemService/TodoService available
- [x] Migrations executed (234aa8ec628c)
- [ ] Branch `foundation/item-list-primitives` merged

### Implementation
- [ ] TodoManagementService created
- [ ] Intent handlers wired to service
- [ ] API endpoints wired to service
- [ ] Error handling implemented
- [ ] Ownership validation in place

### Testing
- [ ] **Integration test proves persistence** ✅ CRITICAL
- [ ] Full lifecycle test passes
- [ ] Service unit tests pass
- [ ] Manual verification: Create todo via chat, check database

---

## Time Estimates

**Foundation Work** (COMPLETE): ~8.5 hours ✅
**Remaining Work**: 2-4 hours
- TodoManagementService: 1-2 hours
- Handler wiring: 30 minutes
- API wiring: 30 minutes
- Integration tests: 1 hour

**Total Project**: ~10-12 hours (foundation + wiring)

---

## Evidence and Documentation

### Domain Model Foundation (Complete)
- **ADR-041**: `docs/internal/architecture/current/adrs/adr-041-domain-primitives-refactoring.md`
- **Validation Report**: `dev/2025/11/04/PHASE-5-VALIDATION-COMPLETE.md`
- **Evidence Package**: `dev/2025/11/04/phase5-evidence/` (7 artifacts)
- **Session Log**: `dev/2025/11/04/2025-11-04-0611-prog-code-log.md`
- **GitHub Comment**: https://github.com/mediajunkie/piper-morgan-product/issues/285#issuecomment-3488492940

### Investigation Reports
- **Architecture Discovery**: `dev/2025/11/03/todo-persistence-architecture-discovery.md`
- **Domain Alignment**: `dev/2025/11/03/todo-domain-alignment-assessment.md`
- **Chief Architect Consultation**: `dev/2025/11/03/chief-architect-consultation-todo-persistence.md`
- **Gameplan**: `dev/2025/11/03/gameplan-domain-model-refactoring.md`

### Updated Issue
- **Issue #295**: https://github.com/mediajunkie/piper-morgan-product/issues/295
- **Updated Description**: `dev/2025/11/04/issue-295-updated-description.md`

---

## Next Steps

### Immediate (Awaiting)
1. ⏸️ **Doc analysis completion** (other agent working on this)
2. ⏸️ **Merge `foundation/item-list-primitives` branch**

### After Merge (Issue #295 Execution)
1. Create TodoManagementService
2. Wire intent handlers
3. Wire API layer
4. Write integration tests
5. Manual verification
6. Close Issue #295

### Future Work
- Issue #294: ActionMapper cleanup
- User authentication integration (replace "default" user_id)
- Knowledge graph integration enhancement
- Shopping lists, Reading lists, etc. (using Item primitive pattern)

---

## Success Metrics

**Foundation Work**:
- ✅ 33/33 validation checks passed (100%)
- ✅ 8/8 success metrics met
- ✅ 92+ tests passing
- ✅ Zero regressions
- ✅ Zero data loss

**Remaining Work**:
- [ ] Todos persist to database (verified via integration test)
- [ ] List command shows real data
- [ ] Complete/delete affect real database records
- [ ] Full lifecycle works end-to-end
- [ ] No verification theater - real persistence

---

## Architecture Decisions

**Service Layer Pattern**: Intent Handlers → TodoManagementService → TodoRepository ✅
- Matches codebase patterns
- Proper DDD separation
- Business logic in service layer

**Domain Model**: Item/List as primitives ✅
- Todo extends Item (polymorphic inheritance)
- Universal operations via ItemService
- Extensible for future item types

**Transaction Management**: Service layer ✅
- Service creates session scope
- Repository receives session
- Proper error handling and rollback

---

## Why This Matters

**Problem**: Users lose all their todos - "verification theater"
- System appears to work (returns confirmations)
- But nothing actually saves to database
- Creates false confidence, violates core promise

**Solution**: Complete the wiring with proper architecture
- Domain model foundation (complete)
- Business logic service (next)
- Full integration testing (verification)

**Impact**: Usable todo system with real persistence, proper architecture for future extensibility

---

**Status**: Foundation complete, roadmap established, ready to execute
**PM Assessment**: "Excellent. It gives us a roadmap for methodical thorough completion. A++"

---

*Roadmap for Todo Persistence Completion*
*November 4, 2025*
*Claude Code (Programmer Agent)*

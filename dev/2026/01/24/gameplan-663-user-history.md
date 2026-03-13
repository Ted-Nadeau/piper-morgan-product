# Gameplan: #663 MEM-ADR054-P3: User History Enhancements

## Audit Findings

### Current State
- `ConversationDB` exists in `services/database/models.py:631-676`
- Has: `id`, `user_id`, `session_id`, `title`, `context`, `is_active`, `created_at`, `updated_at`, `last_activity_at`
- Missing: `is_private`, `topics`, full-text search

### Domain Model
- `Conversation` exists in `services/domain/models.py:1360-1394`
- Also missing: `is_private`, `topics`

### Scope Assessment
This issue involves:
1. Database schema changes (migration required)
2. Domain model updates
3. New service with 4 methods
4. Full-text search setup (PostgreSQL specific)

Given the complexity and the need for database migrations, I recommend a phased approach that can be tested incrementally.

---

## Implementation Plan

### Phase 1: Domain Models (No Migration)

Create domain models and service interface without database changes. This allows us to:
- Define the API
- Write tests against mocked data
- Defer migration complexity

```python
@dataclass
class ConversationSummary:
    conversation_id: str
    title: str
    started_at: datetime
    last_activity: datetime
    turn_count: int
    topics: List[str]
    preview: str
    is_private: bool = False

@dataclass
class UserHistoryPage:
    conversations: List[ConversationSummary]
    total_count: int
    page: int
    page_size: int
    has_more: bool
```

### Phase 2: User History Service (Repository Pattern)

Implement service with repository abstraction:

```python
class UserHistoryService:
    def __init__(self, repository: UserHistoryRepository):
        self.repository = repository

    async def get_history(self, user_id, page, page_size, include_private) -> UserHistoryPage
    async def search_history(self, user_id, query, limit) -> List[ConversationSummary]
    async def mark_private(self, user_id, conversation_id) -> bool
    async def get_conversation_detail(self, user_id, conversation_id) -> Optional[...]
```

### Phase 3: In-Memory Repository for Testing

Create an in-memory repository implementation that works without database changes:

```python
class InMemoryUserHistoryRepository:
    """For testing without database."""
    conversations: Dict[str, List[ConversationSummary]]
```

### Phase 4: Database Migration (Deferred)

The migration can be created but marked as pending PM approval:
- Add `is_private` column (simple boolean)
- Add `topics` column (JSONB array)
- Full-text search index (PostgreSQL specific)

**Note**: This phase modifies production schema and requires careful coordination.

---

## Completion Matrix (This Issue)

| Criterion | Method | Evidence Required |
|-----------|--------|-------------------|
| ConversationSummary dataclass | Write | Dataclass exists |
| UserHistoryPage dataclass | Write | Dataclass exists |
| UserHistoryService implemented | Write | Class with 4 methods |
| get_history() - paginated | Test | Pagination tests pass |
| search_history() - search | Test | Search tests pass |
| mark_private() - privacy | Test | Privacy tests pass |
| get_conversation_detail() | Test | Detail tests pass |
| Privacy filtering works | Test | Private excluded by default |
| Unit tests for all methods | Test | All tests pass |

### Deferred to Follow-up Issue

| Criterion | Reason |
|-----------|--------|
| Add is_private column | Requires DB migration |
| Add topics column | Requires DB migration |
| Full-text search index | PostgreSQL specific, requires DBA review |
| Migration runs | Production impact |

---

## Key Decisions

1. **Repository pattern** - Decouple service from database details
2. **In-memory testing** - Test service logic without database
3. **Migration deferred** - Create migration script but don't auto-run
4. **Topics optional** - Service works even without topics column

---

## Files Expected

```
services/memory/user_history.py         # Service + models
services/memory/__init__.py             # Update exports
tests/unit/services/memory/test_user_history.py
```

Optional (migration deferred):
```
alembic/versions/XXX_add_conversation_history_fields.py
```

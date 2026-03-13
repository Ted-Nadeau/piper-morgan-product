# Gameplan: #661 WORKSPACE-MEMORY: Context-relevant memory retrieval

## Audit Findings

### Dependencies Now Complete
- #657 MEM-ADR054-P1 ✅ ConversationalMemoryService
- #662 MEM-ADR054-P2 ✅ GreetingContextService
- #663 MEM-ADR054-P3 ✅ UserHistoryService
- #660 WORKSPACE-ISOLATION ✅ ContextIsolation

### Available Interfaces

**ConversationalMemoryService** (#657):
- `get_memory_window(user_id)` → `ConversationalMemoryWindow`
- `record_conversation_end(...)`

**UserHistoryService** (#663):
- `search_history(user_id, query, limit)` → `List[ConversationSummary]`
- `get_history(user_id, page, page_size, include_private)` → `UserHistoryPage`

**ContextIsolation** (#660):
- `can_cross(from_ctx, to_ctx)` → `bool`
- `get_boundary_type(from_ctx, to_ctx)` → `BoundaryType`

### Spec Adjustments

1. **Immediate memory** (conversation buffer) - Not implemented yet, stub for now
2. **Long-term relevance threshold** - UserHistoryService.search_history doesn't have relevance_threshold, use limit instead
3. **entry_context(entry)** - Need to bridge ConversationalMemoryEntry to CategorizedContext

---

## Implementation Plan

### Phase 1: Domain Models

```python
@dataclass
class ContextMemory:
    """Memory relevant to a specific context."""
    immediate: List[Dict[str, Any]]           # Current conversation turns
    working: List[ConversationalMemoryEntry]  # 7-day cross-session
    longterm: List[ConversationSummary]       # High-relevance user history

    def is_empty(self) -> bool: ...
    def total_entries(self) -> int: ...
```

### Phase 2: Memory Retrieval Function

```python
async def get_relevant_memory(
    context: WorkspaceContext,
    user_id: str,
    memory_service: ConversationalMemoryService,
    history_service: UserHistoryService,
    isolation: ContextIsolation,
    categorizer: Optional[Callable[[...], CategorizedContext]] = None
) -> ContextMemory
```

### Phase 3: Context Switch Handler

```python
async def on_context_switch(
    switch: ContextSwitch,
    user_id: str,
    memory_service: ConversationalMemoryService,
    history_service: UserHistoryService,
    isolation: ContextIsolation
) -> ContextMemory
```

### Phase 4: Bridge Functions

Need to bridge existing types to CategorizedContext for isolation:
```python
def categorize_memory_entry(entry: ConversationalMemoryEntry) -> CategorizedContext
def categorize_workspace(ctx: WorkspaceContext) -> CategorizedContext
```

---

## Completion Matrix

| Criterion | Method | Evidence Required |
|-----------|--------|-------------------|
| ContextMemory dataclass defined | Write | Dataclass exists |
| get_relevant_memory() works | Test | Returns populated ContextMemory |
| Memory filtered by isolation | Test | Hard boundaries respected |
| Working memory scoped | Test | 7-day window applied |
| Long-term uses relevance | Test | search_history called with topic |
| Integration with ContextSwitch | Test | on_context_switch works |
| Unit tests with mocked services | Test | All tests pass |

---

## Key Decisions

1. **Immediate memory stubbed** - Conversation buffer not yet implemented
2. **Default categorizer** - Provide sensible default that maps workspace_type to category
3. **Topic extraction from context** - Use metadata/entities for search query
4. **Isolation via callbacks** - Allow custom categorization for flexibility

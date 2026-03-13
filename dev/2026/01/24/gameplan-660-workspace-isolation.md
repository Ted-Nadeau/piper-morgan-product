# Gameplan: #660 WORKSPACE-ISOLATION

## Audit Findings

### Current Infrastructure Gap

The spec assumes contexts have categories like "work", "personal", "client_a". Current `WorkspaceContext` only has:
- `workspace_id`: Unique identifier
- `workspace_type`: "slack", "web", "cli", "api", "unknown"

The spec says "Boundary definitions configurable (not hardcoded categories)" which suggests we should design a flexible categorization system.

### Design Decision

Rather than hardcode specific categories, we'll:
1. Add optional `category` and `tags` fields to context comparison
2. Allow boundary rules to match on workspace_id, workspace_type, OR tags
3. Make the rules engine flexible for future configuration

### Memory Integration Gap

The spec shows `filter_memory_for_context(memories: List[MemoryEntry], ...)` but:
- ConversationalMemoryEntry from #657 doesn't have a `.context` field
- Memory summarization (`.summarized()`) doesn't exist yet

For this issue, we'll:
1. Implement the isolation engine with a generic interface
2. Use a simple `MemoryContext` protocol/type that any memory type can satisfy
3. Defer full memory integration to #661 WORKSPACE-MEMORY

---

## Implementation Plan

### Phase 1: Boundary Types and Rules

Create `services/mux/workspace_isolation.py`:

```python
class BoundaryType(Enum):
    HARD = "hard"      # Never cross
    SOFT = "soft"      # Cross with summarization
    OPEN = "open"      # Free crossing

@dataclass
class BoundaryRule:
    """A single boundary rule matching contexts."""
    category_a: str          # Category or tag to match
    category_b: str          # Other category to match
    boundary_type: BoundaryType

@dataclass
class ContextIsolation:
    """Configurable boundary rules engine."""
    rules: List[BoundaryRule]

    # Default rules (can be overridden)
    DEFAULT_HARD_BOUNDARIES = [
        ("work", "personal"),
        ("client:*", "client:*"),  # Any different clients
    ]
```

### Phase 2: Context Categorization

Add categorization capability to contexts:

```python
@dataclass
class CategorizedContext:
    """Context with category tags for isolation rules."""
    workspace_id: str
    category: str              # Primary category: "work", "personal", "client:acme"
    tags: Set[str] = field(default_factory=set)  # Additional tags

    @classmethod
    def from_workspace_context(
        cls,
        ctx: WorkspaceContext,
        category: str = "unknown",
        tags: Optional[Set[str]] = None
    ) -> "CategorizedContext":
        """Wrap a WorkspaceContext with categories."""
```

### Phase 3: Memory Filtering Protocol

Create a minimal interface for memory filtering that any memory type can implement:

```python
@runtime_checkable
class HasContext(Protocol):
    """Protocol for items that have an associated context."""
    context: CategorizedContext

@runtime_checkable
class Summarizable(Protocol):
    """Protocol for items that can be summarized."""
    def summarized(self) -> "Summarizable": ...

def filter_for_isolation(
    items: List[HasContext],
    target: CategorizedContext,
    isolation: ContextIsolation
) -> List[Any]:
    """Filter items based on isolation rules."""
```

### Phase 4: Tests

Test coverage:
1. BoundaryType enum
2. BoundaryRule matching
3. ContextIsolation.get_boundary_type()
4. Hard boundary blocking
5. Soft boundary summarization (when item is Summarizable)
6. Open boundary pass-through
7. Default rules
8. Custom rules override

---

## Completion Matrix

| Criterion | Method | Evidence Required |
|-----------|--------|-------------------|
| BoundaryType enum defined | Write | Enum exists |
| ContextIsolation class implemented | Write | Class exists with rules |
| Hard boundaries enforced | Test | test_hard_boundary_blocks |
| Soft boundaries trigger summarization | Test | test_soft_boundary_summarizes |
| Open boundaries allow full crossing | Test | test_open_boundary_passes |
| filter_for_isolation applies rules | Test | Integration test |
| Boundary definitions configurable | Test | test_custom_rules |
| Unit tests for each boundary type | Test | All tests pass |
| Tests verify no hard boundary leakage | Test | test_no_hard_leakage |

---

## Key Design Decisions

1. **CategorizedContext wrapper** - Rather than modifying WorkspaceContext, create a wrapper that adds categorization
2. **Protocol-based memory interface** - Use HasContext and Summarizable protocols for flexibility
3. **Rule-based matching** - Support both exact and prefix matching (e.g., "client:*")
4. **Default + custom rules** - Provide sensible defaults that can be overridden
5. **Deferred memory integration** - Full memory filtering integration deferred to #661

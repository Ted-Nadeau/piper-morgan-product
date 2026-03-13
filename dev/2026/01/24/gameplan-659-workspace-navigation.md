# Gameplan: #659 WORKSPACE-NAVIGATION

## Audit Findings

### Dependencies
- #658 WORKSPACE-DETECTION ✅ (just completed) - provides `WorkspaceContext`, `ContextSwitch`

### Existing Patterns
- `services/ui_messages/action_humanizer.py` - ActionHumanizer for humanizing actions
- `services/orchestration/kind_communication.py` - KindCommunicationWrapper for friendly messages
- No existing `humanize` package for durations - will implement simple helper

### Design Alignment
- Pattern aligns with existing UI message patterns
- Will live in `services/mux/` alongside `workspace_detection.py`
- Uses `WorkspaceContext.friendly_name` already implemented in #658

---

## Implementation Plan

### Phase 1: Create Navigation Module

Create `services/mux/workspace_navigation.py`:

1. **NAVIGATION_PATTERNS** dictionary with pattern lists
2. **humanize_duration()** helper function (no external dependency)
3. **navigate_language()** function using ContextSwitch
4. **reference_language()** function for cross-context references

### Phase 2: Tests

Create `tests/unit/services/mux/test_workspace_navigation.py`:

1. Test pattern dictionaries exist
2. Test humanize_duration for various intervals
3. Test navigate_language for explicit switches
4. Test navigate_language for return switches with time_away
5. Test reference_language output format

### Phase 3: Export from __init__.py

Add exports to `services/mux/__init__.py`:
- `navigate_language`
- `reference_language`
- `NAVIGATION_PATTERNS` (if useful externally)

---

## Completion Matrix

| Criterion | Method | Evidence Required |
|-----------|--------|-------------------|
| NAVIGATION_PATTERNS defined | Write | Dict exists with switch_to, return_to, reference keys |
| WORKSPACE_FRIENDLY_NAMES defined | Write | Uses WorkspaceContext.friendly_name from #658 |
| navigate_language() implemented | Write | Function callable |
| reference_language() implemented | Write | Function callable |
| Patterns feel natural | Review | No technical identifiers in output |
| Return switches include time-away | Test | test_return_switch_with_time_away passes |
| Unit tests cover all patterns | Test | All tests pass |
| Pattern selection logic tested | Test | test_pattern_selection passes |

---

## Key Design Decisions

1. **Use WorkspaceContext.friendly_name** - Already implemented in #658, no need for separate WORKSPACE_FRIENDLY_NAMES mapping
2. **Deterministic pattern selection** - Use hash-based selection for consistency in tests (not random.choice)
3. **Simple duration humanizer** - Implement locally rather than adding external dependency
4. **Time-away threshold** - Only show for intervals > 1 hour (matches spec)

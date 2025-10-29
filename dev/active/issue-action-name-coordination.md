# Issue: Fix Action Name Coordination Between Classifier and Handlers

**Priority**: MEDIUM
**Milestone**: Sprint A8
**Labels**: `bug`, `intent-service`, `classifier`, `coordination`
**Estimated Effort**: 2 hours

---

## Problem

The intent classifier generates action names that don't match handler method names, causing "No handler for action" errors. This is a **coordination issue**, not an architectural problem (no duplicate handlers exist).

**Example**:
- **Classifier Output**: `action="create_github_issue"`
- **Handler Method**: `async def _handle_create_issue(...)`
- **Result**: Action not found error

**Root Cause**: Classifier uses descriptive names (e.g., `create_github_issue`) while handlers use generic names (e.g., `create_issue`).

---

## Current Behavior

When a user requests creating a GitHub issue:

1. Classifier identifies intent: `EXECUTION`
2. Classifier generates action: `"create_github_issue"`
3. IntentService looks for handler method: `_handle_create_github_issue`
4. Handler doesn't exist (actual method is `_handle_create_issue`)
5. Error: "No handler for action: create_github_issue"

---

## Solution Options

### Option 1: Action Name Mapping (Recommended)

Create an action mapping layer to translate classifier output to handler names:

```python
# services/intent/action_mapper.py (NEW FILE)
class ActionMapper:
    """Maps classifier action names to handler method names"""

    ACTION_MAPPING = {
        # GitHub actions
        "create_github_issue": "create_issue",
        "list_github_issues": "list_issues",
        "update_github_issue": "update_issue",

        # Notion actions
        "create_notion_page": "create_page",
        "search_notion": "search_pages",

        # Calendar actions
        "check_calendar": "check_schedule",
        "create_event": "create_calendar_event",

        # Generic fallback
        "default": None  # Use action name as-is
    }

    @classmethod
    def map_action(cls, classifier_action: str) -> str:
        """Map classifier action name to handler method name"""
        return cls.ACTION_MAPPING.get(classifier_action, classifier_action)
```

```python
# services/intent/intent_service.py - Use mapper
async def _handle_execution_intent(self, intent: Intent, workflow, session_id: str):
    # Map classifier action to handler method
    handler_action = ActionMapper.map_action(intent.action)

    # Existing handler lookup logic
    handler_method = getattr(self, f"_handle_{handler_action}", None)
    if handler_method:
        return await handler_method(intent, workflow, session_id)
    else:
        # Use conversational error message (from other issue)
        return ConversationalErrorMessages.unknown_action(intent.action)
```

**Pros**:
- Clean separation of concerns
- Easy to maintain and extend
- Supports multiple naming conventions
- Doesn't require classifier changes

**Cons**:
- Adds indirection layer
- Requires maintenance as actions added

---

### Option 2: Standardize Classifier Output

Modify classifier to output handler-compatible action names:

```python
# services/intent_service/classifier.py - Modify output
async def classify(self, message: str) -> Intent:
    # ... existing classification logic ...

    # Standardize action names for handlers
    action = self._standardize_action_name(raw_action)

    return Intent(
        category=category,
        action=action,  # Now matches handler names
        confidence=confidence
    )

def _standardize_action_name(self, action: str) -> str:
    """Remove platform prefixes from action names"""
    # "create_github_issue" -> "create_issue"
    return action.replace("github_", "").replace("notion_", "")
```

**Pros**:
- No mapping layer needed
- Direct compatibility
- Simpler architecture

**Cons**:
- Loses action specificity
- Requires classifier changes
- May break existing patterns

---

### Option 3: Rename Handler Methods

Rename handler methods to match classifier output:

```python
# Change handler method names to match classifier
async def _handle_create_github_issue(self, intent, workflow, session_id):
    # Formerly: _handle_create_issue
    # ...

async def _handle_list_github_issues(self, intent, workflow, session_id):
    # Formerly: _handle_list_issues
    # ...
```

**Pros**:
- Explicit action names
- Clear what each handler does
- No translation needed

**Cons**:
- Many handler renames required
- More verbose
- Platform-specific handlers

---

## Recommended Approach: Option 1 (Action Mapper)

**Why**:
- Maintains clean architecture
- Easy to extend
- Supports multiple naming conventions
- Minimal changes to existing code

---

## Implementation Plan

### Phase 1: Create Action Mapper (30 min)
1. Create `services/intent/action_mapper.py`
2. Define ACTION_MAPPING dictionary
3. Implement `map_action()` method
4. Write unit tests

### Phase 2: Integrate Mapper (30 min)
1. Import ActionMapper in intent_service.py
2. Add mapping call before handler lookup
3. Test with known actions

### Phase 3: Discover All Actions (30 min)
1. Run classifier on common queries
2. Log all action names generated
3. Add mappings for each action
4. Verify coverage

### Phase 4: Add Validation (30 min)
1. Add action registry validation
2. Log unmapped actions for tracking
3. Add conversational fallback for unknown actions
4. Write integration tests

---

## Testing Requirements

### Unit Tests
- [ ] Test action mapping for known actions
- [ ] Test unmapped actions (pass through)
- [ ] Test case sensitivity
- [ ] Test empty/null actions

### Integration Tests
- [ ] Test create_github_issue → create_issue flow
- [ ] Test list_github_issues → list_issues flow
- [ ] Test unknown action → conversational fallback
- [ ] Verify handler methods called correctly

### Discovery Tests
- [ ] Run classifier on 20+ sample queries
- [ ] Log all generated action names
- [ ] Verify all actions have mappings
- [ ] Document unmapped actions

---

## Acceptance Criteria

- [ ] ActionMapper class created with comprehensive mappings
- [ ] IntentService uses mapper before handler lookup
- [ ] All known classifier actions have mappings
- [ ] Unknown actions log warning and show friendly message
- [ ] All tests pass
- [ ] Manual testing confirms actions work correctly
- [ ] Documentation updated with action mapping guide

---

## Action Discovery Checklist

Common queries to test:
- [ ] "Create a GitHub issue for bug X"
- [ ] "List all open GitHub issues"
- [ ] "Update issue #123"
- [ ] "Create a Notion page"
- [ ] "Search Notion for X"
- [ ] "Check my calendar"
- [ ] "Schedule a meeting"
- [ ] "Search files for X"
- [ ] "List projects"
- [ ] "Get project status"

---

## Related Issues

- #XXX: Conversational error messages (uses same fallback)
- #XXX: CONVERSATION handler placement
- #XXX: Learning system investigation

---

## References

- **Gap Analysis**: `dev/2025/10/27/CRITICAL-GAPS-ANALYSIS.md` (Gap 3)
- **Classifier**: `services/intent_service/classifier.py`
- **IntentService**: `services/intent/intent_service.py`
- **Handler Methods**: Lines 300-800+ in intent_service.py

---

## Notes

**NOT a Duplicate Handler Issue**: Only one handler exists for each action. This is purely a name coordination problem.

**Low Risk**: Changes are localized to mapping layer. Existing handlers unchanged.

**Future Benefit**: Action registry enables action discovery and validation.

---

**Created**: October 27, 2025, 12:30 PM
**Reporter**: Lead Developer (Sonnet 4.5)
**Discovered During**: Phase 2 Manual Testing

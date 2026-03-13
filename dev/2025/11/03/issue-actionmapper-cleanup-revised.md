# CORE-ALPHA-ACTIONMAPPER-CLEANUP - Remove Unused Mappings

**Priority**: P3 - Technical Debt
**Labels**: `technical-debt`, `cleanup`, `documentation`
**Parent Issue**: #284
**Estimated Effort**: 1.5 hours

## Problem

ActionMapper contains 66 mappings but only ~14 are actually used. The unused 52 mappings are for non-EXECUTION categories that never route through ActionMapper, creating confusion about the system's architecture.

## Root Cause

IntentService routes by category FIRST:
```python
if intent.category == "QUERY":
    return await self._handle_query_intent(...)      # Direct routing
if intent.category == "EXECUTION":
    return await self._handle_execution_intent(...)  # ← ONLY place ActionMapper is used
if intent.category == "ANALYSIS":
    return await self._handle_analysis_intent(...)   # Direct routing
```

The non-EXECUTION categories work perfectly without ActionMapper - they route by category, not by action name variations.

## Solution: Clean Architecture (Option A)

Remove confusion by cleaning up the unused mappings:

### 1. Remove Unused Mappings
```python
class ActionMapper:
    """Maps EXECUTION-category action variations to handler methods."""

    # BEFORE: 66 mappings including unused ones like:
    # "analyze_competitors": "analyze_competitors",  # NEVER USED (ANALYSIS category)
    # "synthesize_research": "synthesize_research",  # NEVER USED (SYNTHESIS category)

    # AFTER: Only EXECUTION mappings (~14 total)
    ACTION_MAPPING = {
        # GitHub actions
        "create_github_issue": "create_issue",
        "list_github_issues": "list_issues",
        "update_github_issue": "update_issue",

        # Todo actions
        "add_todo": "create_todo",
        "create_todo": "create_todo",
        "mark_todo_complete": "complete_todo",
        "complete_todo": "complete_todo",
        "delete_todo": "delete_todo",
        "remove_todo": "delete_todo",

        # Other EXECUTION actions...
    }
```

### 2. Add Clear Documentation
```python
"""
ActionMapper handles EXECUTION category action name variations ONLY.

Why EXECUTION needs mapping:
- Classifier generates variations like 'create_github_issue'
- Handler method is named 'create_issue'
- ActionMapper bridges this naming gap

Why other categories DON'T need mapping:
- QUERY category: Routes to query handler regardless of action
- ANALYSIS category: Routes to analysis handler regardless of action
- SYNTHESIS category: Routes to synthesis handler regardless of action
- They route by CATEGORY, not by action name

This is by design - EXECUTION actions are more varied and specific,
while other categories have uniform handling within their category.
"""
```

### 3. Verify Other Categories Still Work

Run existing tests to confirm non-EXECUTION categories unaffected:
```bash
pytest tests/intent_service/test_analysis_handler.py -v  # 34 tests pass
pytest tests/intent_service/test_query_handler.py -v
pytest tests/intent_service/test_synthesis_handler.py -v
```

## Why NOT Options B or C

**Option B (Keep unused mappings, add documentation)**:
- Perpetuates confusion
- "Document the mess" instead of cleaning it
- Future developers will wonder why unused mappings exist

**Option C (Category-aware mapper)**:
- Over-engineering for a non-problem
- Other categories work fine without mapping
- Adds unnecessary complexity

## Implementation Steps

1. Back up current ACTION_MAPPING (just in case)
2. Remove all non-EXECUTION mappings (~52 entries)
3. Add comprehensive docstring explaining scope
4. Run all intent handler tests to verify
5. Update any documentation that references ActionMapper

## Files to Update

- `services/intent_service/action_mapper.py` - Remove mappings, add docs
- `tests/intent_service/test_action_mapper.py` - Remove tests for unused mappings

## Acceptance Criteria

- [ ] Only EXECUTION mappings remain (~14 entries)
- [ ] Clear docstring explains EXECUTION-only scope
- [ ] Docstring explains why other categories don't need mapping
- [ ] All intent handler tests still pass (especially non-EXECUTION)
- [ ] No functionality broken

## Evidence of Correct Analysis

**Tests prove other categories work without ActionMapper**:
- 34 analysis handler tests pass
- Query handler tests pass
- Synthesis handler tests pass
- These categories have NEVER used ActionMapper

**Code inspection confirms**:
- `_handle_execution_intent()` is the ONLY place that imports ActionMapper
- Other handlers don't even have the import

## Why This Matters

**Clarity > Completeness**: A focused ActionMapper that only contains what it actually uses is better than a "complete" one full of dead code.

**This prevents**:
- Future confusion about system architecture
- Maintenance of unused code
- Wrong assumptions about how non-EXECUTION categories work

## Notes

The fact that we found 52 unused mappings is actually GOOD architecture - it means each category has appropriate routing logic rather than forcing everything through a single mapper.

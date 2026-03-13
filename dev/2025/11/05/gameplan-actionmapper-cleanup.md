# Gameplan: ActionMapper Cleanup (Issue #294)

**Created**: November 5, 2025, 3:52 PM
**Issue**: #294 - CORE-ALPHA-ACTIONMAPPER-CLEANUP
**Priority**: P3 - Technical Debt
**Effort**: Small (cleanup + documentation + validation)
**Goal**: Remove unused ActionMapper mappings and document EXECUTION-only scope

---

## Executive Summary

**What We're Cleaning**: ActionMapper contains 66 mappings but only ~14 are actually used

**The Problem**:
- 52 unused mappings for non-EXECUTION categories
- These categories route directly by category, never use ActionMapper
- Creates confusion about system architecture
- Perpetuates dead code

**The Solution**:
- Remove unused mappings (~52 entries)
- Keep only EXECUTION mappings (~14 entries)
- Add comprehensive documentation explaining EXECUTION-only scope
- Verify all existing tests still pass

**Why This Matters**: Clarity > Completeness. A focused ActionMapper is better than one full of dead code.

---

## Background: How IntentService Routes

### Current Routing Logic

```python
# services/intent_service/intent_service.py
async def process_intent(self, intent):
    # Routes by CATEGORY first
    if intent.category == "QUERY":
        return await self._handle_query_intent(...)      # Direct routing

    if intent.category == "EXECUTION":
        return await self._handle_execution_intent(...)  # ← ONLY place ActionMapper used

    if intent.category == "ANALYSIS":
        return await self._handle_analysis_intent(...)   # Direct routing

    if intent.category == "SYNTHESIS":
        return await self._handle_synthesis_intent(...) # Direct routing
```

**Key Insight**: Only EXECUTION category uses ActionMapper. Other categories route directly by category, not by action name variations.

### Why EXECUTION Needs ActionMapper

**Problem**: Classifier generates action name variations
```
User: "create a GitHub issue"
→ Classifier: action="create_github_issue"
→ Handler method: create_issue()
→ Need mapping: "create_github_issue" → "create_issue"
```

**EXECUTION actions are varied and specific**, need name normalization.

### Why Other Categories DON'T Need ActionMapper

**Other categories have uniform handling**:
```
User: "what are the top priorities?"
→ Category: QUERY
→ Routes directly to query handler
→ Handler determines how to answer (doesn't need action mapping)
```

**Non-EXECUTION categories route by intent, not specific actions**.

---

## Phase Overview

| Phase | Description | Effort | Risk |
|-------|-------------|--------|------|
| **Phase 0** | Pre-cleanup analysis | Small | Low |
| **Phase 1** | Remove unused mappings | Small | Low |
| **Phase 2** | Add comprehensive documentation | Small | Low |
| **Phase 3** | Verify all tests pass | Small | Low |
| **Phase 4** | Update related documentation | Small | Low |

**Total Effort**: Small (cleanup task with verification)

---

## Phase 0: Pre-Cleanup Analysis

### Goal
Understand current state and verify which mappings are actually used

### Tasks

**Task 0.1: Locate ActionMapper**

```bash
# Find ActionMapper
find . -name "action_mapper.py" -type f

# Expected: services/intent_service/action_mapper.py
```

**Task 0.2: Count Current Mappings**

```bash
# Count mappings in ACTION_MAPPING
grep -c '".*":' services/intent_service/action_mapper.py

# Expected: ~66 mappings
```

**Task 0.3: Identify Usage**

```bash
# Find where ActionMapper is imported
grep -r "from.*action_mapper import" services/

# Expected: Only in services/intent_service/intent_service.py
# Specifically: Only in _handle_execution_intent() method
```

**Task 0.4: Review Execution Handler**

```bash
# Check _handle_execution_intent implementation
grep -A 30 "def _handle_execution_intent" services/intent_service/intent_service.py
```

**Expected Finding**: ActionMapper.get_handler_method() called ONLY for EXECUTION category.

**Task 0.5: Review Test Coverage**

```bash
# Find ActionMapper tests
ls -1 tests/intent_service/test_action_mapper.py

# Find handler tests (these should still pass after cleanup)
ls -1 tests/intent_service/test_*_handler.py

# Expected:
# - test_action_mapper.py (will need updating)
# - test_analysis_handler.py (should pass unchanged)
# - test_query_handler.py (should pass unchanged)
# - test_synthesis_handler.py (should pass unchanged)
```

**Task 0.6: Create Backup**

```bash
# Create backup before changes
cp services/intent_service/action_mapper.py \
   services/intent_service/action_mapper.py.backup

# Note: This is just for safety during cleanup
```

### Completion Criteria
- ✅ ActionMapper location confirmed
- ✅ Current mapping count known (~66)
- ✅ Usage pattern verified (EXECUTION only)
- ✅ Test files identified
- ✅ Backup created

---

## Phase 1: Remove Unused Mappings

### Goal
Remove all non-EXECUTION category mappings, keep only EXECUTION mappings

### Strategy

**Identify EXECUTION Actions**:
- GitHub operations (create_issue, list_issues, update_issue, etc.)
- Todo operations (create_todo, complete_todo, delete_todo, etc.)
- File operations (if any)
- Other direct actions that modify state

**Identify Non-EXECUTION Actions** (TO REMOVE):
- Analysis operations (analyze_competitors, etc.)
- Query operations (search queries, lookups, etc.)
- Synthesis operations (synthesize_research, etc.)
- These route by category, never use ActionMapper

### Tasks

**Task 1.1: Create List of EXECUTION Mappings**

Create file `execution-mappings.txt` listing only EXECUTION category mappings:

```python
# EXECUTION MAPPINGS ONLY (Keep These)

# GitHub Actions
"create_github_issue": "create_issue",
"create_issue": "create_issue",
"make_github_issue": "create_issue",
"new_github_issue": "create_issue",

"list_github_issues": "list_issues",
"list_issues": "list_issues",
"show_github_issues": "list_issues",
"get_issues": "list_issues",

"update_github_issue": "update_issue",
"update_issue": "update_issue",
"modify_issue": "update_issue",

"close_github_issue": "close_issue",
"close_issue": "close_issue",

# Todo Actions
"add_todo": "create_todo",
"create_todo": "create_todo",
"new_todo": "create_todo",

"mark_todo_complete": "complete_todo",
"complete_todo": "complete_todo",
"finish_todo": "complete_todo",
"done_todo": "complete_todo",

"delete_todo": "delete_todo",
"remove_todo": "delete_todo",

"list_todos": "list_todos",
"show_todos": "list_todos",
"get_todos": "list_todos",

# Add any other EXECUTION actions found
```

**Expected**: ~14 mappings total (may vary slightly based on actual code)

**Task 1.2: Update ACTION_MAPPING**

Update `services/intent_service/action_mapper.py`:

```python
"""
ActionMapper - Maps EXECUTION category action name variations to handler methods.

SCOPE: This mapper handles EXECUTION category actions ONLY.

Why EXECUTION needs mapping:
- Classifier generates variations like 'create_github_issue'
- Handler method is named 'create_issue'
- ActionMapper bridges this naming gap

Why other categories DON'T need mapping:
- QUERY category: Routes to query handler regardless of action
- ANALYSIS category: Routes to analysis handler regardless of action
- SYNTHESIS category: Routes to synthesis handler regardless of action
- They route by CATEGORY, not by action name variations

This is by design - EXECUTION actions are more varied and specific,
while other categories have uniform handling within their category.

Architecture Note:
IntentService routes by category FIRST. Only EXECUTION category uses
this mapper. Other categories route directly to their handlers.
"""

class ActionMapper:
    """Maps EXECUTION category action names to handler method names."""

    ACTION_MAPPING = {
        # GitHub Actions
        "create_github_issue": "create_issue",
        "create_issue": "create_issue",
        "make_github_issue": "create_issue",
        "new_github_issue": "create_issue",

        "list_github_issues": "list_issues",
        "list_issues": "list_issues",
        "show_github_issues": "list_issues",
        "get_issues": "list_issues",

        "update_github_issue": "update_issue",
        "update_issue": "update_issue",
        "modify_issue": "update_issue",

        "close_github_issue": "close_issue",
        "close_issue": "close_issue",

        # Todo Actions
        "add_todo": "create_todo",
        "create_todo": "create_todo",
        "new_todo": "create_todo",

        "mark_todo_complete": "complete_todo",
        "complete_todo": "complete_todo",
        "finish_todo": "complete_todo",
        "done_todo": "complete_todo",

        "delete_todo": "delete_todo",
        "remove_todo": "delete_todo",

        "list_todos": "list_todos",
        "show_todos": "list_todos",
        "get_todos": "list_todos",
    }

    @staticmethod
    def get_handler_method(action: str) -> str:
        """
        Map action name to handler method name.

        Args:
            action: Action name from intent (e.g., "create_github_issue")

        Returns:
            Handler method name (e.g., "create_issue")

        Raises:
            ValueError: If action not in mapping

        Note:
            Only EXECUTION category actions should use this mapper.
            Other categories route directly by category.
        """
        if action not in ActionMapper.ACTION_MAPPING:
            raise ValueError(
                f"Unknown action: {action}. "
                f"This mapper handles EXECUTION actions only. "
                f"Other categories route by category, not action name."
            )

        return ActionMapper.ACTION_MAPPING[action]
```

**Task 1.3: Count New Mapping Total**

```bash
# Verify reduced count
grep -c '".*":' services/intent_service/action_mapper.py

# Expected: ~14 (down from 66)
```

### Completion Criteria
- ✅ Non-EXECUTION mappings identified
- ✅ ACTION_MAPPING updated (only EXECUTION actions)
- ✅ Mapping count reduced to ~14
- ✅ Comprehensive docstring added
- ✅ Clear scope documentation

---

## Phase 2: Add Comprehensive Documentation

### Goal
Document the EXECUTION-only scope and architecture clearly

### Tasks

**Task 2.1: Add Module Docstring**

Already done in Phase 1 (see above). Module docstring explains:
- Why EXECUTION needs mapping
- Why other categories don't need mapping
- Architecture decision (route by category first)
- This is by design, not a limitation

**Task 2.2: Add Architecture Comment to IntentService**

Update `services/intent_service/intent_service.py`:

```python
async def _handle_execution_intent(self, intent, session_id, user_id):
    """
    Handle EXECUTION category intents.

    EXECUTION actions use ActionMapper to normalize action name variations.
    This is the ONLY place ActionMapper is used - other categories route
    directly by category without needing action name mapping.

    Why: EXECUTION actions are varied and specific (create_issue, add_todo),
    while other categories have uniform handling (all queries go to query handler).
    """
    from .action_mapper import ActionMapper

    try:
        handler_method_name = ActionMapper.get_handler_method(intent.action)
        # ... rest of implementation
    except ValueError as e:
        # Log error about unmapped action
        self.logger.error(f"Unmapped EXECUTION action: {intent.action}")
        return f"I don't know how to handle that action yet."
```

**Task 2.3: Add Note to README/CLAUDE.md (if applicable)**

If there's documentation about intent handling, add note:

```markdown
## Intent Routing Architecture

IntentService routes by **category first**:

1. **QUERY** → Query handler (direct routing)
2. **ANALYSIS** → Analysis handler (direct routing)
3. **SYNTHESIS** → Synthesis handler (direct routing)
4. **EXECUTION** → ActionMapper → Execution handler (name normalization)

Only EXECUTION uses ActionMapper because:
- EXECUTION actions are varied and specific
- Classifier generates name variations
- Need to map variations to handler methods

Other categories route uniformly within their category.
```

**Task 2.4: Update ActionMapper Test Documentation**

Update `tests/intent_service/test_action_mapper.py` header:

```python
"""
Tests for ActionMapper - EXECUTION category action name mapping.

ActionMapper handles EXECUTION category actions ONLY.
Other categories (QUERY, ANALYSIS, SYNTHESIS) route by category
and don't use action name mapping.

These tests verify:
- EXECUTION action variations map to correct handler methods
- Unknown actions raise appropriate errors
- Mapping is consistent with execution handler expectations
"""
```

### Completion Criteria
- ✅ Module docstring comprehensive
- ✅ IntentService method documented
- ✅ README/CLAUDE.md updated (if needed)
- ✅ Test file documented
- ✅ Architecture clearly explained

---

## Phase 3: Verify All Tests Pass

### Goal
Ensure cleanup doesn't break any functionality

### Tasks

**Task 3.1: Run ActionMapper Tests**

```bash
# Run ActionMapper tests
pytest tests/intent_service/test_action_mapper.py -xvs

# Expected: Some tests may need updating (for removed mappings)
# But core functionality should work
```

**Action if tests fail**:
- Update test to remove tests for non-EXECUTION mappings
- Keep tests for EXECUTION mappings
- Verify test failures are ONLY for removed mappings, not actual bugs

**Task 3.2: Run Analysis Handler Tests**

```bash
# Verify analysis handler still works (doesn't use ActionMapper)
pytest tests/intent_service/test_analysis_handler.py -xvs

# Expected: All tests pass (no changes to analysis handler)
```

**Critical**: If these tests fail, STOP. Analysis handler should be unaffected.

**Task 3.3: Run Query Handler Tests**

```bash
# Verify query handler still works (doesn't use ActionMapper)
pytest tests/intent_service/test_query_handler.py -xvs

# Expected: All tests pass (no changes to query handler)
```

**Critical**: If these tests fail, STOP. Query handler should be unaffected.

**Task 3.4: Run Synthesis Handler Tests**

```bash
# Verify synthesis handler still works (doesn't use ActionMapper)
pytest tests/intent_service/test_synthesis_handler.py -xvs

# Expected: All tests pass (no changes to synthesis handler)
```

**Critical**: If these tests fail, STOP. Synthesis handler should be unaffected.

**Task 3.5: Run Execution Handler Tests**

```bash
# Verify execution handler still works (uses ActionMapper)
pytest tests/intent_service/test_execution_handler.py -xvs

# Expected: All tests pass (EXECUTION mappings still present)
```

**Task 3.6: Run Full Intent Service Test Suite**

```bash
# Run all intent service tests
pytest tests/intent_service/ -xvs

# Expected: All tests pass (except removed mapping tests)
```

**Task 3.7: Manual Verification**

Test actual usage:
```bash
# Start application
python main.py

# Test EXECUTION actions via chat:
# 1. "create a GitHub issue about testing"
# 2. "add a todo: verify ActionMapper cleanup"
# 3. "list my todos"

# Test non-EXECUTION actions via chat:
# 1. "what are my top priorities?" (QUERY)
# 2. "analyze the current sprint" (ANALYSIS)

# All should work normally
```

### Completion Criteria
- ✅ ActionMapper tests passing (after updates)
- ✅ Analysis handler tests passing (unchanged)
- ✅ Query handler tests passing (unchanged)
- ✅ Synthesis handler tests passing (unchanged)
- ✅ Execution handler tests passing
- ✅ Full test suite passing
- ✅ Manual verification successful

### Stop Conditions

**STOP IMMEDIATELY if**:
- Non-EXECUTION handler tests fail
- Execution handler tests fail for EXECUTION actions
- Manual verification shows broken functionality

**DO NOT**:
- Proceed if tests reveal actual bugs
- Ignore test failures
- Skip manual verification

---

## Phase 4: Update Related Documentation

### Goal
Update any documentation that references ActionMapper

### Tasks

**Task 4.1: Search for ActionMapper References**

```bash
# Find all references to ActionMapper
grep -r "ActionMapper" docs/ --include="*.md"
grep -r "action.mapper" docs/ --include="*.md"
grep -r "ACTION_MAPPING" docs/ --include="*.md"
```

**Task 4.2: Update Found Documentation**

For each reference found, update to reflect EXECUTION-only scope:

```markdown
# Before
ActionMapper maps all intent actions to handler methods.

# After
ActionMapper maps EXECUTION category action name variations to handler methods.
Other categories (QUERY, ANALYSIS, SYNTHESIS) route directly by category.
```

**Task 4.3: Update Issue #294 Description**

Mark completion in issue:
- [x] Remove unused mappings
- [x] Add documentation
- [x] Verify tests pass
- [x] Update related docs

**Task 4.4: Create Completion Summary**

Create `ACTION_MAPPER_CLEANUP_COMPLETE.md`:

```markdown
# ActionMapper Cleanup Complete

**Date**: [completion date]
**Issue**: #294

## Summary

ActionMapper cleaned up from 66 mappings to ~14 EXECUTION-only mappings.

## Changes Made

1. **Removed**: 52 unused mappings for non-EXECUTION categories
2. **Kept**: 14 EXECUTION category mappings
3. **Added**: Comprehensive documentation explaining scope
4. **Verified**: All tests passing

## Evidence

- Mapping count: 66 → 14
- Non-EXECUTION handler tests: All passing (unchanged)
- EXECUTION handler tests: All passing
- Manual verification: Successful

## Architecture Clarity

**EXECUTION category**: Uses ActionMapper (action name variations)
**Other categories**: Route directly by category (no mapping needed)

This is by design, not a limitation.
```

### Completion Criteria
- ✅ Documentation references found
- ✅ References updated
- ✅ Issue #294 marked complete
- ✅ Completion summary created

---

## Acceptance Criteria - Final Checklist

### Code Changes
- [ ] Only EXECUTION mappings remain (~14 entries)
- [ ] Non-EXECUTION mappings removed (~52 entries)
- [ ] Clear docstring explains EXECUTION-only scope
- [ ] Error message references category routing

### Documentation
- [ ] Module docstring comprehensive
- [ ] IntentService method documented
- [ ] Test file documented
- [ ] README/CLAUDE.md updated (if needed)
- [ ] Completion summary created

### Testing
- [ ] ActionMapper tests passing
- [ ] Analysis handler tests passing (unchanged)
- [ ] Query handler tests passing (unchanged)
- [ ] Synthesis handler tests passing (unchanged)
- [ ] Execution handler tests passing
- [ ] Manual verification successful

### Evidence
- [ ] Mapping count reduced (66 → ~14)
- [ ] All test results documented
- [ ] Manual test results documented
- [ ] No regressions found

---

## Expected Outcomes

### Before Cleanup
- ❌ 66 mappings (52 unused)
- ❌ Confusion about system architecture
- ❌ Dead code maintained
- ❌ Wrong assumptions possible

### After Cleanup
- ✅ ~14 mappings (all used)
- ✅ Clear architecture documentation
- ✅ No dead code
- ✅ Correct understanding of routing

### Benefits
- **Clarity**: Obvious that only EXECUTION uses mapping
- **Maintenance**: Less code to maintain
- **Understanding**: Clear separation of routing strategies
- **Prevention**: Documentation prevents future confusion

---

## Files to Modify

### Primary File
1. `services/intent_service/action_mapper.py` - Remove mappings, add docs

### Secondary Files
1. `services/intent_service/intent_service.py` - Add architecture comment (optional)
2. `tests/intent_service/test_action_mapper.py` - Update tests for removed mappings
3. `docs/` - Update any references (if found)

### New File
1. `dev/2025/11/05/ACTION_MAPPER_CLEANUP_COMPLETE.md` - Completion summary

---

## Risk Assessment

**Risk Level**: **LOW**

**Why**:
- Non-EXECUTION categories have NEVER used ActionMapper
- Tests prove other handlers work independently
- Code inspection confirms usage pattern
- Easy to revert if issues found (we have backup)

**Mitigation**:
- Comprehensive test coverage
- Manual verification
- Backup file created
- Phase-by-phase approach with stop conditions

---

## Evidence of Correct Analysis

### Tests Prove Architecture

**From existing tests**:
- 34 analysis handler tests pass → Never used ActionMapper
- Query handler tests pass → Never used ActionMapper
- Synthesis handler tests pass → Never used ActionMapper

**Code confirms**:
- `_handle_execution_intent()` only imports ActionMapper
- Other handlers don't have the import
- IntentService routes by category first

**This cleanup is safe**: Removing dead code that was never used.

---

## Why This Matters

### Technical Debt Reduction

**Problem**: Maintaining unused code
- 52 mappings that serve no purpose
- Creates maintenance burden
- Confuses future developers

**Solution**: Remove it
- Clear, focused codebase
- Obvious architecture
- Less to maintain

### Clarity > Completeness

**Philosophy**: A focused ActionMapper containing only what it uses is better than a "complete" one full of dead code.

**Impact**: Future developers immediately understand:
- EXECUTION uses mapping (action variations)
- Other categories don't (route by category)
- This is by design

---

## Timeline Estimate

**Small Effort Task**: Single session work

**Phases**:
- Phase 0: Pre-cleanup analysis (Small)
- Phase 1: Remove mappings (Small)
- Phase 2: Add documentation (Small)
- Phase 3: Verify tests (Small)
- Phase 4: Update docs (Small)

**Note**: We take the time needed to do this right. Quality over speed.

---

## Success Metrics

**Objective Measures**:
- ✅ Mapping count: 66 → ~14
- ✅ All non-EXECUTION handler tests: Passing
- ✅ EXECUTION handler tests: Passing
- ✅ Documentation added: Comprehensive
- ✅ Manual verification: Successful

**Quality Measures**:
- ✅ No regressions
- ✅ Clear architecture explanation
- ✅ Maintainable codebase
- ✅ Proper evidence

---

## Notes

### This is Good Architecture

**Finding 52 unused mappings is actually GOOD** - it means each category has appropriate routing logic rather than forcing everything through a single mapper.

**Separation of concerns**: Different categories need different routing strategies.

### Future Additions

If new EXECUTION actions added:
1. Add to ACTION_MAPPING in action_mapper.py
2. Add corresponding handler method
3. Add test for new mapping
4. Document why it's EXECUTION category

**Clear pattern** for future work.

---

*Gameplan: ActionMapper Cleanup (Issue #294)*
*Created: November 5, 2025, 3:52 PM*
*Effort: Small (cleanup + documentation + verification)*
*Goal: Remove dead code, add clarity*
*Approach: Methodical, evidence-based, quality-focused*

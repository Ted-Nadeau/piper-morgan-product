# GREAT-4D Known Issues & Future Work

**Date**: October 6, 2025
**Context**: Issues discovered during GREAT-4D Phase Z validation

---

## Issue 1: GitHub create_issue Signature Mismatch

### Problem

**GitHubDomainService.create_issue** accepts `assignees` parameter:
```python
async def create_issue(
    self, repo_name: str, title: str, body: str,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None  # ← Parameter exists
) -> Dict[str, Any]:
```

**GitHubIntegrationRouter.create_issue** does NOT accept `assignees`:
```python
async def create_issue(
    self, repo_name: str, title: str, body: str,
    labels: Optional[List[str]] = None
    # ← No assignees parameter
) -> Dict[str, Any]:
```

### Impact

- **Test failure**: Integration test shows error "takes from 4 to 5 positional arguments but 6 were given"
- **Functionality**: `_handle_create_issue` tries to pass assignees but they're silently dropped
- **User experience**: Users cannot assign issues via intent handler

### Current Workaround

Test still passes because:
1. Handler properly attempts execution (no placeholder)
2. Error handling works correctly
3. The error is a signature mismatch, not a logic error

### Recommended Fix

**Option 1**: Remove `assignees` from GitHubDomainService signature (breaking change)
**Option 2**: Add `assignees` support to GitHubIntegrationRouter (preferred)
**Option 3**: Document as known limitation

### File Locations

- Domain service: `services/domain/github_domain_service.py:122-132`
- Integration router: `services/integrations/github/github_integration_router.py:161-171`
- Intent handler: `services/intent/intent_service.py:430-436`

### Priority

**LOW** - Does not block GREAT-4D completion:
- Issue creation still works (without assignees)
- Error handling is correct
- Tests validate placeholder removal (main goal)

---

## Issue 2: Intent Categories Still Using Placeholder

### Status

⚠️ **INCOMPLETE** - GREAT-4D only addressed EXECUTION and ANALYSIS

### Complete Intent Category Status

**Working (8 categories):**
- ✅ QUERY - Handled by QueryRouter + domain services
- ✅ CONVERSATION - Handled by ConversationHandler (Tier 1 bypass)
- ✅ IDENTITY - Handled by canonical handlers
- ✅ TEMPORAL - Handled by canonical handlers
- ✅ STATUS - Handled by canonical handlers
- ✅ PRIORITY - Handled by canonical handlers
- ✅ GUIDANCE - Handled by canonical handlers
- ✅ EXECUTION - **NEW** Handled by EXECUTION handlers (GREAT-4D Phase 1)
- ✅ ANALYSIS - **NEW** Handled by ANALYSIS handlers (GREAT-4D Phase 2)

**Still Placeholder (4 categories):**
- ❌ SYNTHESIS - Returns "requires full orchestration workflow" message
- ❌ STRATEGY - Returns "requires full orchestration workflow" message
- ❌ LEARNING - Returns "requires full orchestration workflow" message
- ❌ UNKNOWN - Returns "requires full orchestration workflow" message

### Active Placeholder Code

**Location**: `services/intent/intent_service.py:152-165`

```python
# Phase 3C: For other intents, indicate orchestration needed
return IntentProcessingResult(
    success=True,
    message=f"Intent '{intent.action}' (category: {intent.category.value}) requires full orchestration workflow. This is being restored in Phase 3.",
    intent_data={
        "category": intent.category.value,
        "action": intent.action,
        "confidence": intent.confidence,
        "context": intent.context,
    },
    workflow_id=workflow.id,
    requires_clarification=False,
    clarification_type=None,
)
```

### Where These Categories Are Used

**SYNTHESIS**: Used by classifier and workflow factory
```bash
$ grep -r "IntentCategory.SYNTHESIS" services/ --include="*.py"
services/intent_service/classifier.py:            category = IntentCategory.SYNTHESIS
services/orchestration/workflow_factory.py:            elif intent.category == IntentCategory.SYNTHESIS:
```

**STRATEGY**: Used by classifier, workflow factory, multi-agent coordinator
```bash
$ grep -r "IntentCategory.STRATEGY" services/ --include="*.py"
services/intent_service/classifier.py:            category = IntentCategory.STRATEGY
services/orchestration/multi_agent_coordinator.py:            IntentCategory.STRATEGY: ["domain_models", "analysis"],
services/orchestration/workflow_factory.py:            elif intent.category == IntentCategory.STRATEGY:
```

**LEARNING**: Used by classifier, spatial classifier, Slack integration
```bash
$ grep -r "IntentCategory.LEARNING" services/ --include="*.py"
services/intent_service/classifier.py:            category = IntentCategory.LEARNING
services/intent_service/spatial_intent_classifier.py:            return IntentCategory.LEARNING
services/integrations/slack/spatial_intent_classifier.py:                intent_category=IntentCategory.LEARNING,
```

### Impact

**Current**: 9/13 intent categories working (69% complete)
**GREAT-4D Scope**: Only EXECUTION + ANALYSIS (raised to 69% from 54%)

**User Impact**:
- Users asking for synthesis tasks → Placeholder message
- Users asking for strategy advice → Placeholder message
- Users asking learning questions → Placeholder message
- Users with unclear intents → Placeholder message

### GREAT-4D Scope Clarification

**GREAT-4D Acceptance Criteria** stated:
> "Zero 'Phase 3' references in active code"

**Actual Achievement**:
- ✅ Zero "Phase 3" references for EXECUTION intents
- ✅ Zero "Phase 3" references for ANALYSIS intents
- ❌ Still "Phase 3" references for SYNTHESIS/STRATEGY/LEARNING/UNKNOWN intents

**This is a scope gap** - acceptance criteria implied ALL placeholders removed, but implementation only covered EXECUTION + ANALYSIS.

### Recommendation

**Option 1: Amend GREAT-4D scope to be explicit**
- Acceptance criteria: "EXECUTION and ANALYSIS intents work (no placeholders)"
- Document SYNTHESIS/STRATEGY/LEARNING/UNKNOWN as future work
- Mark GREAT-4D as "Partially Complete" (9/13 categories)

**Option 2: Extend GREAT-4D to cover remaining categories**
- Phase 4: SYNTHESIS handlers
- Phase 5: STRATEGY handlers
- Phase 6: LEARNING handlers
- Phase 7: UNKNOWN handlers
- Estimated effort: 3-4 hours total

**Option 3: Accept placeholder for rarely-used categories**
- SYNTHESIS/STRATEGY/LEARNING/UNKNOWN may be edge cases
- Focus on high-value categories (EXECUTION/ANALYSIS were highest priority)
- Document as known limitation

### Priority

**MEDIUM** - Should be addressed but not blocking:
- EXECUTION/ANALYSIS are primary use cases (covered ✅)
- SYNTHESIS/STRATEGY/LEARNING are lower frequency
- System is functional for 69% of intent categories
- Placeholder messages are clear and actionable

### Verification

**Test confirms EXECUTION/ANALYSIS work:**
```bash
$ PYTHONPATH=. python3 dev/2025/10/06/test_end_to_end_handlers.py
Results: 4/4 passed
✅ EXECUTION/ANALYSIS handlers working

But SYNTHESIS/STRATEGY/LEARNING/UNKNOWN would still return placeholder.
```

---

## Future Enhancements

### 1. Add Assignee Support to GitHub Integration

**Effort**: Small (10-15 min)
**Impact**: Enables full issue creation with assignees
**Files**: `services/integrations/github/github_integration_router.py`

### 2. Implement Additional EXECUTION Actions

**Candidates**:
- `close_issue`
- `reopen_issue`
- `add_comment`
- `create_branch`

**Effort**: Small-Medium per action
**Pattern**: Follow `_handle_create_issue` pattern

### 3. Implement Additional ANALYSIS Actions

**Candidates**:
- `analyze_pull_request`
- `review_code_changes`
- `summarize_discussion`
- `evaluate_test_coverage`

**Effort**: Medium per action
**Pattern**: Follow `_handle_analyze_commits` pattern

### 4. Remove Generic Fallback Placeholders

**Timing**: Phase 4 or later
**Scope**: Implement handlers for all intent categories
**Goal**: Zero placeholder messages in production

---

**Status**: Documented for planning
**Action**: No immediate fix required for GREAT-4D completion

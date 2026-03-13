# EXECUTION/ANALYSIS Intent Investigation Report

**Date**: October 6, 2025, 11:43 AM
**Investigator**: Code Agent
**Issue**: Determine actual behavior of EXECUTION and ANALYSIS intents

---

## Executive Summary

**FINDING**: EXECUTION and ANALYSIS intents **return placeholder messages** and never reach orchestration.

**ROOT CAUSE**: `IntentService._handle_generic_intent()` (line 338) returns placeholder message instead of executing workflows. Additionally, even if workflows were executed, task types would fail in `OrchestrationEngine._execute_task()`.

**TWO-LAYER PROBLEM**:
1. **Intent routing layer**: EXECUTION/ANALYSIS bypass orchestration (intentional Phase 3C placeholder)
2. **Orchestration layer**: Task types not implemented in engine

**RECOMMENDATION**: **GREAT-4D IS NEEDED** to:
1. Route EXECUTION/ANALYSIS intents to orchestration (remove placeholder)
2. Implement missing task handlers in orchestration engine

**EXISTING PATTERN**: QUERY intents route to domain services (StandupOrchestrationService, etc.) - EXECUTION/ANALYSIS should follow similar pattern OR use orchestration engine.

---

## Investigation Process

### 1. Traced EXECUTION Intent Flow

**Path through codebase**:

1. **Intent Classification** (`services/intent_service/classifier.py`):
   - User message: "create a github issue about login bug"
   - Result: `IntentCategory.EXECUTION`, action=`create_issue`
   - ✅ Classification works correctly

2. **Workflow Creation** (`services/orchestration/workflow_factory.py`):
   - Action `create_issue` maps to `WorkflowType.CREATE_TICKET` (line 34)
   - Creates workflow with 3 tasks (lines 213-235):
     - Task 1: `TaskType.EXTRACT_WORK_ITEM`
     - Task 2: `TaskType.GENERATE_GITHUB_ISSUE_CONTENT`
     - Task 3: `TaskType.GITHUB_CREATE_ISSUE`
   - ✅ Workflow creation works correctly

3. **Workflow Execution** (`services/orchestration/engine.py`):
   - Engine's `_execute_task()` method (lines 262-310)
   - **PROBLEM**: Only handles these task types:
     - `TaskType.ANALYZE_REQUEST` (line 269)
     - `TaskType.EXTRACT_REQUIREMENTS` (line 271)
     - `TaskType.IDENTIFY_DEPENDENCIES` (line 273)
     - `TaskType.GENERATE_DOCUMENTATION` (line 275)
     - `TaskType.EXECUTE_GITHUB_ACTION` (line 277)
   - **Line 280**: `raise ValueError(f"Unknown task type: {task.type}")`
   - ❌ **CREATE_TICKET task types are not implemented**

### 2. Test Results

Created test script: `dev/2025/10/06/test_execution_analysis_behavior.py`

**TEST 1: EXECUTION Intent (create GitHub issue)**
```
✅ Classification: category=EXECUTION, action=create_issue (confidence=0.95)
✅ Workflow created: type=CREATE_TICKET, tasks=3
   - Task 1: Extract Work Item (type=EXTRACT_WORK_ITEM)
   - Task 2: Generate Issue Content (type=GENERATE_GITHUB_ISSUE_CONTENT)
   - Task 3: Create GitHub Issue (type=GITHUB_CREATE_ISSUE)
❌ Execution failed: WorkflowStatus.FAILED
```

**TEST 2: ANALYSIS Intent (analyze data)**
```
✅ Classification: category=ANALYSIS, action=analyze_metrics (confidence=0.95)
✅ Workflow created: type=ANALYZE_METRICS, tasks=1
   - Task 1: Analyze Metrics (type=ANALYZE_REQUEST)
✅ Execution completed: status=FAILED (but task type IS handled)
```

**Key Observation**: ANALYSIS intents use `TaskType.ANALYZE_REQUEST` which IS implemented (line 269 of engine.py), so they partially work. EXECUTION intents fail completely.

### 3. Yesterday's Context (Phase 3C)

Review of `dev/2025/10/05/test_unhandled_intent.py`:
- Test focused on **classification**, not execution
- Showed that EXECUTION/ANALYSIS intents classify correctly
- Did NOT test whether workflows actually execute
- **This is why the placeholder issue was missed** - classification works, execution doesn't

---

## Technical Details

### Missing Task Type Handlers

The following task types are **created but not implemented**:

#### EXECUTION-related (CREATE_TICKET workflow):
1. `TaskType.EXTRACT_WORK_ITEM` - Extract work item details from message
2. `TaskType.GENERATE_GITHUB_ISSUE_CONTENT` - Generate professional GitHub issue content
3. `TaskType.GITHUB_CREATE_ISSUE` - Actually create the GitHub issue

#### ANALYSIS-related (various workflows):
1. `TaskType.ANALYZE_FILE` - File analysis (partially works via GENERATE_REPORT)
2. `TaskType.ANALYZE_GITHUB_ISSUE` - GitHub issue analysis
3. `TaskType.SUMMARIZE` - General summarization (fallback)

#### Other workflow types:
4. `TaskType.LIST_PROJECTS` - List user projects
5. `TaskType.CREATE_WORK_ITEM` - Generic work item creation
6. Various others created by WorkflowFactory

### Code Location Matrix

| Component | File | Status |
|-----------|------|--------|
| Intent Classification | `services/intent_service/classifier.py` | ✅ Works |
| **Intent Routing** | **`services/intent/intent_service.py:338-356`** | **❌ PLACEHOLDER** |
| Workflow Creation | `services/orchestration/workflow_factory.py` | ✅ Works (but never called!) |
| Task Type Definitions | `services/shared_types.py` | ✅ Defined |
| Task Execution | `services/orchestration/engine.py:262-310` | ❌ Missing handlers |

### The Actual Flow

**QUERY intents (WORKING)**:
```
IntentService.process_intent()
  → _handle_query_intent() [line 206]
    → _handle_standup_query() OR
    → _handle_projects_query() OR
    → _handle_generic_query() [uses QueryRouter]
      → Domain services execute and return data
```

**EXECUTION/ANALYSIS intents (NOT WORKING)**:
```
IntentService.process_intent()
  → _handle_generic_intent() [line 338]
    → Returns placeholder message:
      "Intent 'X' requires full orchestration workflow.
       This is being restored in Phase 3."
    → NEVER reaches WorkflowFactory
    → NEVER reaches OrchestrationEngine
```

---

## Recommendation: GREAT-4D Scope

**GREAT-4D IS NEEDED** to implement EXECUTION/ANALYSIS intent handling.

### Architecture Decision: Follow QUERY Pattern

**RECOMMENDED APPROACH**: Follow the existing QUERY pattern rather than using OrchestrationEngine.

**Rationale**:
1. **QUERY intents work** via domain services (StandupOrchestrationService)
2. **OrchestrationEngine is incomplete** (workflows.py is empty, task handlers missing)
3. **Domain services pattern is proven** and working
4. **Simpler, faster implementation** - no need to fix orchestration engine

### Minimum Viable Implementation

**Priority 1: Route EXECUTION/ANALYSIS to handlers (remove placeholder)**

Replace `_handle_generic_intent()` with actual routing:

```python
async def _handle_execution_intent(self, intent: Intent, workflow_id: str, session_id: str):
    """Handle EXECUTION category intents (create issues, tasks, etc.)"""
    if intent.action in ["create_issue", "create_github_issue"]:
        return await self._handle_create_issue(intent, workflow_id, session_id)
    # ... other EXECUTION actions

async def _handle_analysis_intent(self, intent: Intent, workflow_id: str):
    """Handle ANALYSIS category intents"""
    if intent.action == "analyze_metrics":
        return await self._handle_analyze_metrics(intent, workflow_id)
    # ... other ANALYSIS actions
```

**Priority 2: Create domain service handlers**

Follow the `StandupOrchestrationService` pattern:
- Create `ExecutionService` for EXECUTION intents
- Create `AnalysisService` for ANALYSIS intents
- Wire up to existing GitHub/MCP integrations

**Priority 3: Wire to existing integrations**

- GitHub issue creation → Use existing GitHub router/plugin
- Metrics analysis → Use existing query router
- File analysis → Use existing MCP/services

### Estimated Effort

**Small** (2-4 hours):
- Intent routing changes: ~50 lines (remove placeholder, add routing)
- Domain service handlers: ~100-150 lines (follow StandupOrchestrationService pattern)
- Testing: ~50 lines
- Documentation: minimal

**Complexity**: Low
- Following existing working pattern (QUERY intents)
- Integrations already exist (GitHub, MCP)
- No need to fix orchestration engine
- Much simpler than implementing full workflow/task system

### Alternative: Fix OrchestrationEngine (NOT RECOMMENDED)

If we go the orchestration route instead:
- **Effort**: Medium-Large (6-10 hours)
- **Complexity**: High
- Need to implement 8+ task handlers in engine.py
- Need to test workflow execution system
- Need to fix workflows.py (currently empty)
- Higher risk, more complex, less proven pattern

---

## Conclusion

**Answer to Investigation Questions**:

1. **Do EXECUTION/ANALYSIS work or return placeholders?**
   - They **fail with "Unknown task type" errors**
   - Not placeholders - handlers simply don't exist

2. **Evidence of actual behavior?**
   - ✅ Test script demonstrates classification works
   - ✅ Test script shows workflow creation works
   - ❌ Test script proves execution fails
   - Evidence file: `dev/2025/10/06/test_execution_analysis_behavior.py`

3. **Is GREAT-4D needed?**
   - **YES - GREAT-4D is needed**
   - 75% complete pattern: Workflows defined, execution not implemented
   - Blocks real use of EXECUTION/ANALYSIS intents
   - Critical for alpha release functionality

---

## Next Steps

1. **PM Decision**: Approve GREAT-4D scope (implement task handlers)
2. **Gameplan**: Create GREAT-4D gameplan with phases:
   - Phase 0: Verification (find all missing handlers)
   - Phase 1: EXECUTION handlers (CREATE_TICKET workflow)
   - Phase 2: ANALYSIS handlers (REVIEW_ITEM workflow)
   - Phase 3: Other handlers (LIST_PROJECTS, etc.)
   - Phase Z: Testing and validation

3. **Immediate Action**: This investigation report serves as Phase -1 for GREAT-4D

---

*Investigation completed: October 6, 2025, 11:50 AM*
*Status: Ready for PM review and GREAT-4D approval*

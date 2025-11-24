# SLACK-SPATIAL Phase 4 Gameplan - Final Push to Alpha
**Date**: 2025-11-21
**For**: Lead Developer
**Current Status**: 102/120 tests passing (85%)
**Target**: 105-106/113 tests (93-94%) - Alpha Ready

---

## Context from PM Discussion

After reviewing last night's excellent work (102/120 achieved!), we've refined what's actually needed for alpha vs. what can be deferred.

**Key Insight**: We already have OAuth working with Slack in production, so infrastructure exists for testing the critical paths.

---

## Immediate Actions (30 minutes)

### 1. Delete Duplicate Tests ✅
**File**: `tests/unit/services/integrations/slack/test_workflow_integration.py`
**Action**: Delete lines 28-415 (TestSlackWorkflowFactory class)
**Result**: 102/113 tests (90.3% passing)
**Time**: 5 minutes

### 2. Update Pattern-020 Documentation ✅
**File**: `docs/internal/architecture/current/patterns/pattern-020-spatial-metaphor-integration.md`
**Change**: `RoomPurpose.DEVELOPMENT` → `RoomPurpose.PROJECT_WORK`
**Time**: 10 minutes

### 3. Verify New Baseline
**Command**: `pytest tests/unit/services/integrations/slack/ -v`
**Expected**: 102 passed, 11 skipped (90.3%)
**Time**: 5 minutes

---

## Phase 4: Critical Path Tests (2-3 hours)

### Test 1: OAuth → Spatial Workspace Territory
**File**: `test_spatial_system_integration.py::test_oauth_flow_creates_spatial_workspace_territory`

**Why Critical**: Proves OAuth setup initializes spatial context correctly

**Approach**:
```python
# We have working OAuth in production
# Mock the OAuth response using actual production data structure
# Verify spatial territory gets created with correct mappings
```

**Success**: OAuth completion → Spatial workspace initialized

### Test 2: Slack Event → Spatial → Workflow Pipeline (E2E)
**File**: `test_spatial_system_integration.py::test_slack_event_to_spatial_to_workflow_pipeline`

**Why Critical**: THIS IS THE DEMO - proves the entire feature works

**Approach**:
```python
# Start with Slack message event
# → SlackEventHandler processes it
# → SlackSpatialMapper creates SpatialEvent
# → SlackWorkflowFactory creates Workflow
# → Verify workflow has correct spatial context
```

**Success**: Can demonstrate complete flow for alpha

### Test 3: E2E Workflow Creation
**File**: `test_workflow_integration.py::TestWorkflowIntegration::test_end_to_end_workflow_creation`

**Issue**: Non-serializable spatial context
**Fix**: Make spatial context JSON-serializable (add `.to_dict()` methods if needed)

**Why Critical**: Proves workflows can be persisted and executed

---

## What We're Deferring

### To Enterprise Milestone
- **Multi-workspace attention prioritization** - Needs multiple Slack installations
  - Create issue: "SLACK-MULTI-WORKSPACE: Support attention across multiple workspaces"

### To Enhancement Milestone
- **Attention decay with pattern learning** - Needs learning system
  - Create issue: "SLACK-ATTENTION-DECAY: Implement pattern learning for attention models"

- **Spatial memory persistence** - Needs time-series storage
  - Create issue: "SLACK-MEMORY: Persist spatial patterns over time"

### Keep Skipped (Post-MVP Features)
- 5 advanced attention algorithm tests in `test_attention_scenarios_validation.py`
- These are legitimate P3 features, not needed for MVP

---

## Success Criteria

**Before Starting**: 102/113 (90.3%) after deleting duplicates

**Target for Today**:
- 3 critical path tests working
- 105-106/113 tests passing (93-94%)
- Full demo path verified:
  - ✅ Slack message received
  - ✅ Spatial event created
  - ✅ Workflow generated
  - ✅ Workflow executable

**Not Required**:
- Advanced attention algorithms
- Multi-workspace support
- Pattern learning over time

---

## Evidence Required

For each test fixed:
1. Test output showing it passes
2. Brief explanation of what was fixed
3. Verification that no regressions occurred

**Final verification**:
```bash
# Run full suite
pytest tests/unit/services/integrations/slack/ -v

# Expected: ~105 passed, 8 skipped
# The 8 skipped = 5 advanced algorithms + 3 deferred features
```

---

## Time Estimate

- Immediate actions: 30 minutes
- OAuth → Spatial test: 45 minutes
- Event → Workflow pipeline: 60 minutes
- E2E Workflow test: 45 minutes
- Verification & cleanup: 30 minutes

**Total**: 3-3.5 hours

---

## Definition of DONE

✅ 93-94% of valid tests passing (105-106/113)
✅ Critical path works: Slack → Spatial → Workflow
✅ Can demo the feature end-to-end
✅ Issues created for deferred work
✅ Pattern-020 updated
✅ No regressions
✅ Evidence documented

**This completes SLACK-SPATIAL for alpha!**

---

## Questions?

If you hit blockers on any of the 3 critical tests, document what's blocking and we'll reassess. The key is proving the demo path works - everything else can be deferred.

Remember: We already have OAuth working in production, so we have the "real infrastructure" needed for tests 1-2.

---

*Gameplan prepared by: Chief Architect*
*Date: 2025-11-21, 11:30 AM PT*

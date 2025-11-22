# Phase 3.3 Agent Prompt: Fix Remaining 7 Interface Tests
## Issue: SLACK-SPATIAL | Phase 3.3 (Extended) | Priority: P0

**Date**: Thursday, November 20, 2025, 6:50 PM PT
**From**: Lead Developer + PM Authorization
**To**: Code Agent (continuation - checkpoint approved)
**Priority**: P0 (Critical path for alpha)

---

## PM Decision: Option B - Fix All 7 Tests ✅

**PM Statement**: "I think postponing that work doesn't help us when it's on the critical path. It's OK if we need to continue into tomorrow. I feel zero time pressure here. Just a curiosity about what is needed and how to get there, and a willingness to take the care to do it right."

**Authorization**: Proceed with fixing all 7 remaining tests
- No time pressure (can continue tomorrow if needed)
- Focus on doing it right, not rushing
- These are critical path for alpha - must be resolved

---

## Current Status

**Achieved**:
- 96/120 tests passing (80%)
- Task 3.1 complete (11/11 factory tests)
- Archaeological check successful

**Remaining**:
- 7 tests with interface/mock issues
- Goal: 103/120 tests passing (86%)

---

## Mission

Fix the remaining 7 tests systematically to achieve 103/120 passing tests.

**Two Categories**:
1. **5 Pipeline Tests** - Interface mismatches (channel_id vs channel_data)
2. **2 Integration Classes** - Duplicate/mock issues

**Philosophy**: Quality over speed. Take time to understand the issues. Do it right.

---

## 🚨 CRITICAL: Take Your Time

**This is NOT a rush**:
- ✅ You can work into tomorrow if needed
- ✅ Understand before fixing
- ✅ Ask questions if unclear
- ✅ Stop and escalate if architectural issues
- ✅ Document your reasoning

**This IS important**:
- These tests are on critical path for alpha
- We need them working, not skipped
- Interface changes should be done properly
- No shortcuts that create technical debt

---

## Task 3.3.1: Fix Pipeline Interface Tests (5 tests)

### Understanding the Issue

**File**: `tests/unit/services/integrations/slack/test_workflow_pipeline_integration.py`

**Root Cause**: TDD specs written before implementation evolved

**The Mismatch**:
```python
# What tests expect (OLD interface)
spatial_mapper.map_channel_to_room(channel_id="C123")

# What implementation provides (NEW interface)
spatial_mapper.map_channel_to_room(channel_data: Dict[str, Any])
```

**Tests Affected** (5 total):
1. test_slack_help_request_creates_piper_task_workflow
2. test_slack_bug_report_creates_incident_workflow
3. test_slack_feature_request_creates_product_workflow
4. test_workflow_creation_failure_graceful_handling
5. test_tdd_tests_are_comprehensive

---

### Step 1: Investigate Current Interface (Small Effort)

**What to do**:

1. **Check the actual implementation**:
   ```bash
   # Find map_channel_to_room implementation
   grep -n "def map_channel_to_room" services/integrations/slack/spatial_mapper.py -A 10
   ```

2. **Understand what channel_data expects**:
   - What keys are required?
   - What's the structure?
   - Are there examples in other tests?

3. **Document findings**:
   ```bash
   # Create quick reference
   echo "# map_channel_to_room Interface" > /tmp/channel-interface-notes.txt
   echo "Expected signature: ..." >> /tmp/channel-interface-notes.txt
   echo "Required keys: ..." >> /tmp/channel-interface-notes.txt
   ```

**Expected**: Clear understanding of what channel_data should contain

**Evidence**: You should be able to explain: "channel_data needs keys: X, Y, Z"

---

### Step 2: Update Test Helper/Fixture (Medium Effort)

**What to do**:

1. **Find where tests create channel_id calls**:
   ```bash
   grep -n "channel_id=" tests/unit/services/integrations/slack/test_workflow_pipeline_integration.py
   ```

2. **Create a test fixture for channel_data**:
   ```python
   @pytest.fixture
   def sample_channel_data():
       """Sample channel data matching current interface"""
       return {
           'id': 'C123',
           'name': 'general',
           'is_channel': True,
           'is_private': False,
           # Add other required keys based on Step 1
       }
   ```

3. **Or create a helper function**:
   ```python
   def create_channel_data(channel_id: str, **kwargs) -> Dict[str, Any]:
       """Helper to create channel_data dict from channel_id"""
       defaults = {
           'id': channel_id,
           'name': f'channel-{channel_id}',
           'is_channel': True,
           'is_private': False,
       }
       defaults.update(kwargs)
       return defaults
   ```

**Strategy**: Choose fixture or helper based on test structure

**Evidence**: Helper function or fixture created and tested

---

### Step 3: Update Test Calls (Medium-Large Effort)

**What to do**:

1. **Update one test at a time** (don't batch!)

2. **Pattern to follow**:
   ```python
   # OLD
   result = spatial_mapper.map_channel_to_room(channel_id="C123")

   # NEW (using helper)
   channel_data = create_channel_data("C123")
   result = spatial_mapper.map_channel_to_room(channel_data)

   # Or NEW (using fixture)
   result = spatial_mapper.map_channel_to_room(sample_channel_data)
   ```

3. **Update each test**:
   - test_slack_help_request_creates_piper_task_workflow
   - test_slack_bug_report_creates_incident_workflow
   - test_slack_feature_request_creates_product_workflow
   - test_workflow_creation_failure_graceful_handling
   - test_tdd_tests_are_comprehensive

4. **Run each test after updating**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_workflow_pipeline_integration.py::test_slack_help_request_creates_piper_task_workflow -v
   ```

5. **If a test fails**: STOP on that test, understand why, fix it, then move to next

**CRITICAL**: One test at a time. Don't move forward if one fails.

**Evidence**: Each test passes individually before moving to next

---

### Step 4: Verify All 5 Pipeline Tests (Small Effort)

**What to do**:

```bash
# Run all 5 pipeline tests together
pytest tests/unit/services/integrations/slack/test_workflow_pipeline_integration.py -v

# Expected: 5/5 passing
```

**If not all passing**:
- Document which ones fail and why
- Don't proceed to Task 3.3.2 until these 5 pass

**Evidence**: Test output showing 5/5 passing

---

### Checkpoint: Pipeline Tests Complete

**Before proceeding, verify**:
- [ ] All 5 pipeline tests passing
- [ ] Interface changes documented
- [ ] No new regressions
- [ ] Code committed

**Git Commit**:
```bash
git add tests/unit/services/integrations/slack/test_workflow_pipeline_integration.py
git commit -m "fix(SLACK-SPATIAL): Phase 3.3.1 - Fix pipeline interface tests

Updated 5 tests to use channel_data dict instead of channel_id string:
- test_slack_help_request_creates_piper_task_workflow
- test_slack_bug_report_creates_incident_workflow
- test_slack_feature_request_creates_product_workflow
- test_workflow_creation_failure_graceful_handling
- test_tdd_tests_are_comprehensive

Evidence: 5/5 pipeline tests now passing
Phase: 3.3.1 complete (101/120 tests passing)
"
```

---

## Task 3.3.2: Fix Integration Test Classes (2 classes)

### Understanding the Issue

**File**: `tests/unit/services/integrations/slack/test_workflow_integration.py`

**Two test classes currently skipped**:
1. **TestSlackWorkflowFactory** (line 28) - "mock serialization issues"
2. **TestWorkflowIntegration** (line 417) - "end-to-end test issues"

**Your assessment**: TestSlackWorkflowFactory appears to be duplicate of tests we fixed

---

### Step 1: Investigate TestSlackWorkflowFactory (Small Effort)

**What to do**:

1. **Compare with already-fixed tests**:
   ```bash
   # Look at tests we fixed
   cat tests/unit/services/integrations/slack/test_spatial_workflow_factory.py | head -100

   # Compare with TestSlackWorkflowFactory
   sed -n '28,200p' tests/unit/services/integrations/slack/test_workflow_integration.py
   ```

2. **Determine**:
   - Is this truly a duplicate?
   - Or does it test different aspects?
   - What are the differences?

3. **Decision tree**:
   - **If duplicate**: Delete the class entirely
   - **If different**: Apply same fixes as test_spatial_workflow_factory.py
   - **If unclear**: STOP and document, escalate

**Evidence**: Clear assessment of whether duplicate or different

---

### Step 2: Fix or Remove TestSlackWorkflowFactory (Small-Medium Effort)

**If Duplicate** (recommended if truly duplicate):
```python
# Just delete the entire class
# Update skip reason to say "Tests moved to test_spatial_workflow_factory.py"
```

**If Different** (apply same fixes as before):
1. Add `object_id` to mock coordinates
2. Add `mock_intent_classifier` fixture
3. Add `tasks = []` to mock workflows
4. Fix any enum `.value` issues
5. Remove skip decorator

**Run tests**:
```bash
pytest tests/unit/services/integrations/slack/test_workflow_integration.py::TestSlackWorkflowFactory -v
```

**Evidence**: Tests passing or class removed with clear reason

---

### Step 3: Investigate TestWorkflowIntegration (Small Effort)

**What to do**:

1. **Check the skip reason**: "end-to-end test issues"

2. **Look at the tests**:
   ```bash
   sed -n '417,500p' tests/unit/services/integrations/slack/test_workflow_integration.py
   ```

3. **Identify issues**:
   - Mock serialization?
   - IntentClassifier real calls?
   - Missing fixtures?
   - Interface mismatches?

4. **Document**: Create quick notes on what needs fixing

**Evidence**: Clear understanding of what's broken

---

### Step 4: Fix TestWorkflowIntegration (Medium Effort)

**Based on your investigation, apply fixes**:

**Common fixes** (based on your notes):
- Mock serialization issues (object_id, etc.)
- IntentClassifier needs mocking
- Similar to other mock fixes

**Strategy**:
1. Apply same patterns used in test_spatial_workflow_factory.py
2. Add necessary fixtures
3. Update mock objects
4. Remove skip decorator

**Run tests**:
```bash
pytest tests/unit/services/integrations/slack/test_workflow_integration.py::TestWorkflowIntegration -v
```

**If tests fail**:
- Fix one test at a time
- Document issues
- STOP if architectural problems

**Evidence**: Tests passing

---

### Checkpoint: Integration Tests Complete

**Before declaring Phase 3.3 complete, verify**:
- [ ] TestSlackWorkflowFactory fixed or removed
- [ ] TestWorkflowIntegration tests passing
- [ ] All mock issues resolved
- [ ] Code committed

**Git Commit**:
```bash
git add tests/unit/services/integrations/slack/test_workflow_integration.py
git commit -m "fix(SLACK-SPATIAL): Phase 3.3.2 - Fix integration test classes

Fixed 2 test classes:
- TestSlackWorkflowFactory: [removed as duplicate / fixed mock issues]
- TestWorkflowIntegration: Fixed mock serialization + IntentClassifier

Evidence: 2 test classes now passing
Phase: 3.3.2 complete (103/120 tests passing)
"
```

---

## Final Verification

### Full Slack Test Suite

**What to do**:

```bash
# Run complete Slack test suite
pytest tests/unit/services/integrations/slack/ -v --tb=short > dev/2025/11/20/slack-tests-phase3-final.txt 2>&1

# Show summary
tail -30 dev/2025/11/20/slack-tests-phase3-final.txt
```

**Expected**:
- 103/120 tests passing (85.8%)
- 17 skipped (advanced features, post-MVP)
- 0 failures

**If not 103/120**:
- Document what's missing
- Explain why
- Escalate if unexpected

**Evidence**: Test output showing 103/120 passing

---

## Success Criteria

Phase 3 (Extended) is considered **COMPLETE** when:
- ✅ All 5 pipeline tests passing (interface fixed)
- ✅ TestSlackWorkflowFactory fixed or removed
- ✅ TestWorkflowIntegration tests passing
- ✅ 103/120 Slack tests passing total
- ✅ No regressions in existing 96 tests
- ✅ All evidence documented
- ✅ All commits pushed to origin

**NOT complete means**:
- ❌ "102 of 103 tests passing" (must be 103+)
- ❌ "Most interface issues fixed" (must be all)
- ❌ Any rationalization of incompleteness

---

## STOP Conditions

**STOP immediately and escalate if**:
- ❌ Interface changes require modifying production code (not just tests)
- ❌ channel_data structure is unclear or undocumented
- ❌ More than 10 existing tests start failing (>10% regression)
- ❌ IntentClassifier changes needed (architectural)
- ❌ Issues appear to be architectural, not test-related
- ❌ You're stuck on the same test for >30 minutes

**When stopped**:
1. Document what you tried
2. Explain what's blocking
3. Provide specific error messages
4. Note which test you're stuck on
5. Wait for guidance

---

## Evidence Requirements

**Required Deliverables**:

1. **Pipeline Tests Fixed**:
   - File: `dev/2025/11/20/pipeline-interface-fix-notes.txt`
   - Contents: What interface changes were made

2. **Integration Tests Fixed**:
   - File: `dev/2025/11/20/integration-tests-fix-notes.txt`
   - Contents: What was fixed in each class

3. **Final Test Output**:
   - File: `dev/2025/11/20/slack-tests-phase3-final.txt`
   - Contents: 103/120 tests passing

4. **Git Commits**:
   - Minimum 2: Pipeline fixes + Integration fixes
   - Clear descriptions of changes

5. **Session Log**:
   - Complete documentation of Phase 3.3

---

## Working Strategy

### Recommended Approach

**Session 1** (Tonight or tomorrow):
- Task 3.3.1: Fix 5 pipeline tests (1-2 hours)
- Stop after pipeline complete if tired

**Session 2** (If needed):
- Task 3.3.2: Fix 2 integration classes (30-60 min)
- Final verification

**Break Points**:
- After Step 2 of Task 3.3.1 (helper created)
- After pipeline tests complete
- After each integration class

**Don't rush**: Take breaks between tests if needed

---

## Key Principles for This Work

**Quality Over Speed**:
- Understand before fixing
- One test at a time
- Document as you go
- Ask questions if unclear

**Systematic Approach**:
- Investigate first (understand the issue)
- Plan the fix (create helper/fixture)
- Execute carefully (one test at a time)
- Verify thoroughly (run tests after each change)

**Communication**:
- Document your reasoning
- Explain what you tried
- Note any surprises
- Escalate blockers immediately

**No Shortcuts**:
- Don't skip understanding the issue
- Don't batch fixes without testing
- Don't guess at interfaces
- Don't ignore test failures

---

## What Success Looks Like

**End of Phase 3.3**:
- 103/120 Slack tests passing ✅
- All interface mismatches fixed ✅
- All mock issues resolved ✅
- Integration tests working ✅
- Can demo Slack → Workflow in alpha ✅
- No regressions ✅
- Clean, documented work ✅

**Ready for Phase 4**: System Integration (wiring complete pipeline)

---

**Status**: Ready for execution
**Expected Effort**: Medium (1-2 hours, can split across sessions)
**Quality Standard**: 100% completion with evidence
**Timeline**: No pressure - take the time needed to do it right

---

_"Quality over speed - understand before fixing"_
_"One test at a time - verify before proceeding"_
_"Together we are making something incredible"_ 🏗️✨

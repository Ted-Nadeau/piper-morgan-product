# Prompt for Claude Code: SLACK-SPATIAL Phase 4 - Final Alpha Push
**Issue**: SLACK-SPATIAL - Fix Slack Integration for Alpha Testing
**Phase**: Phase 4 (Final) - Critical Path Completion
**Priority**: P0 (Blocks Alpha Testing)
**Date**: Friday, November 21, 2025, 12:45 PM PT
**Estimated Effort**: Medium (3.5-4 hours)

---

## Your Identity

You are Claude Code, a specialized development agent working on the Piper Morgan project. You completed excellent work yesterday (Phases 1-3, +29 tests), achieving 102/120 tests passing (85%). Today you're completing the final phase to make Slack integration alpha-ready.

---

## 🎯 Mission

Complete SLACK-SPATIAL Phase 4 by fixing 3 critical path tests and cleaning up duplicate tests, achieving **105-106/113 tests passing (93-94%)** and proving the complete demo flow: **Slack → Spatial → Workflow**.

**Success Means**:
- Can demonstrate Slack message → Workflow creation end-to-end
- OAuth initialization creates spatial workspace territory
- Workflows are serializable and executable
- Alpha-ready for user testing

---

## 🏗️ Context from Yesterday

**Your Achievement**: Phases 0-3 complete
- Phase 1: +8 tests (quick wins + token investigation)
- Phase 2: +4 tests (OAuth spatial methods, all passed first run)
- Phase 3: +17 tests (factory verification + interface fixes)
- Total: 102/120 passing (85%), 0 regressions

**Key Finding**: TDD spec drift - tests written to aspirational specs diverged from evolved implementation over 4 months. This is normal, not a failure.

**Infrastructure Available**:
- SlackWorkflowFactory: Complete and tested (11 tests passing)
- SlackSpatialMapper: All 4 mapping methods working
- SlackOAuthHandler: All 4 spatial methods implemented
- OAuth working in production: Real infrastructure exists for testing

---

## 🚨 CRITICAL: Infrastructure Verification (MANDATORY FIRST ACTION)

**Before doing ANYTHING else, verify the gameplan assumptions**:

```bash
# Verify infrastructure matches Phase 4 assumptions
echo "=== Infrastructure Check ==="

# 1. Verify OAuth infrastructure exists
ls -la services/integrations/slack/oauth_handler.py
grep -n "class SlackOAuthHandler" services/integrations/slack/oauth_handler.py

# 2. Verify spatial system integration tests exist
ls -la tests/unit/services/integrations/slack/test_spatial_system_integration.py

# 3. Verify workflow integration tests exist
ls -la tests/unit/services/integrations/slack/test_workflow_integration.py

# 4. Check current test status
pytest tests/unit/services/integrations/slack/ -v --collect-only | grep -E "(passed|skipped|failed)"

# 5. Verify duplicate test location
grep -n "class TestSlackWorkflowFactory" tests/unit/services/integrations/slack/test_workflow_integration.py
```

**Expected Results**:
- OAuth handler exists (Phase 2 completed this)
- Test files exist (they should from yesterday)
- 102 tests passing, 18 skipped
- Duplicate class found at lines 28-415

**If reality doesn't match**: STOP and report mismatch with evidence

---

## 📋 Phase 4 Task Breakdown

### Immediate Actions (20-30 minutes) ✅

**Task 4.0.1**: Delete Duplicate Tests (5 min)
**Task 4.0.2**: Update Pattern-020 Documentation (10 min)
**Task 4.0.3**: Verify New Baseline (5 min)

### Critical Path Tests (2-3 hours) ✅

**Task 4.1**: OAuth → Spatial Workspace Territory (45 min)
**Task 4.2**: Slack Event → Spatial → Workflow Pipeline (60 min)
**Task 4.3**: E2E Workflow Creation (45 min)

### Cleanup (30 minutes) ✅

**Task 4.4**: Create Issues for Deferred Work (20 min)
**Task 4.5**: Final Verification (10 min)

---

## 🛠️ TASK 4.0.1: Delete Duplicate Tests (5 minutes)

### Mission
Delete TestSlackWorkflowFactory class (7 duplicate tests) from test_workflow_integration.py to achieve cleaner baseline of 102/113 (90.3%).

### Why This Matters
- 7 tests duplicate test_spatial_workflow_factory.py (11 passing tests)
- Adds confusion and maintenance burden
- Written as TDD specs, superseded by actual implementation tests

### What to Do

**Step 1**: Verify duplicate location
```bash
# Find the class
grep -n "class TestSlackWorkflowFactory" tests/unit/services/integrations/slack/test_workflow_integration.py

# Should show: Line 28
```

**Step 2**: Delete the duplicate class
```bash
# Delete lines 28-415 (entire TestSlackWorkflowFactory class)
# Use your preferred method - sed, manual edit, etc.

# Verify deletion
grep -n "class TestSlackWorkflowFactory" tests/unit/services/integrations/slack/test_workflow_integration.py
# Should return nothing
```

**Step 3**: Verify file is still valid Python
```bash
# Check syntax
python3 -m py_compile tests/unit/services/integrations/slack/test_workflow_integration.py

# Should compile without errors
```

### Evidence Required
- [ ] Before: `grep` showing class at line 28
- [ ] After: `grep` showing class not found
- [ ] Syntax check: Python compilation successful
- [ ] Git diff showing deletion

### Success Criteria
- TestSlackWorkflowFactory class deleted (lines 28-415)
- File still valid Python
- No other changes to file

---

## 🛠️ TASK 4.0.2: Update Pattern-020 Documentation (10 minutes)

### Mission
Update Pattern-020 documentation to reflect evolved enum names: `RoomPurpose.DEVELOPMENT` → `RoomPurpose.PROJECT_WORK`

### Why This Matters
- Documentation has outdated enum value from TDD specs
- Could confuse future developers
- Examples should match current implementation

### What to Do

**Step 1**: Find Pattern-020
```bash
# Locate the pattern file
find . -name "pattern-020*.md" -type f

# Expected: docs/internal/architecture/current/patterns/pattern-020-spatial-metaphor-integration.md
```

**Step 2**: Check current enum usage
```bash
# Find all occurrences of DEVELOPMENT
grep -n "RoomPurpose.DEVELOPMENT" docs/internal/architecture/current/patterns/pattern-020-spatial-metaphor-integration.md

# Note line numbers
```

**Step 3**: Update to PROJECT_WORK
```bash
# Replace DEVELOPMENT with PROJECT_WORK
# (Use sed or manual edit)

sed -i.backup 's/RoomPurpose\.DEVELOPMENT/RoomPurpose.PROJECT_WORK/g' docs/internal/architecture/current/patterns/pattern-020-spatial-metaphor-integration.md

# Verify changes
grep -n "RoomPurpose.PROJECT_WORK" docs/internal/architecture/current/patterns/pattern-020-spatial-metaphor-integration.md
```

**Step 4**: Check for any other outdated enums
```bash
# Quick scan for other potential issues
grep -i "development\|DEVELOPMENT" docs/internal/architecture/current/patterns/pattern-020-spatial-metaphor-integration.md

# Verify they're used in correct context (not enum references)
```

### Evidence Required
- [ ] Before: `grep` showing DEVELOPMENT usage
- [ ] After: `grep` showing PROJECT_WORK usage
- [ ] Git diff showing changes
- [ ] No accidental changes to other content

### Success Criteria
- All RoomPurpose.DEVELOPMENT → RoomPurpose.PROJECT_WORK
- No other unintended changes
- Documentation accurate to current implementation

---

## 🛠️ TASK 4.0.3: Verify New Baseline (5 minutes)

### Mission
Run full Slack test suite to verify 102/113 baseline after deletions.

### What to Do

**Step 1**: Commit immediate changes
```bash
# Stage changes
git add tests/unit/services/integrations/slack/test_workflow_integration.py
git add docs/internal/architecture/current/patterns/pattern-020-spatial-metaphor-integration.md

# Commit
git commit -m "cleanup(SLACK-SPATIAL): Phase 4 - Remove duplicate tests and update docs

- Deleted TestSlackWorkflowFactory (7 duplicate tests, lines 28-415)
- Updated Pattern-020: RoomPurpose.DEVELOPMENT → PROJECT_WORK
- New baseline: 102/113 tests (90.3%)

Phase: 4.0 immediate actions complete
"

# Verify commit
git log --oneline -1
```

**Step 2**: Run full test suite
```bash
# Run all Slack tests
pytest tests/unit/services/integrations/slack/ -v --tb=short > /tmp/phase4-baseline-output.txt 2>&1

# Show summary
tail -30 /tmp/phase4-baseline-output.txt
```

**Step 3**: Verify baseline
```bash
# Extract counts
grep -E "passed|skipped|failed" /tmp/phase4-baseline-output.txt | tail -1

# Expected: "102 passed, 11 skipped"
# (18 skipped - 7 deleted = 11 remaining skipped)
```

### Evidence Required
- [ ] Git commit showing deletions and doc updates
- [ ] Test output showing 102 passed, 11 skipped
- [ ] No test failures
- [ ] Confirmation: 102/113 = 90.3%

### Success Criteria
- 102 tests passing (same as yesterday)
- 11 tests skipped (down from 18)
- 0 test failures
- No regressions from deletions

---

### Checkpoint 1: Immediate Actions Complete ✅

**Before proceeding to Task 4.1, verify**:
- [ ] Duplicate tests deleted
- [ ] Pattern-020 updated
- [ ] Baseline verified: 102/113 passing
- [ ] Changes committed
- [ ] No regressions

**If all verified**: Proceed to Task 4.1 (OAuth → Spatial test)
**If issues**: STOP and report with evidence

---

## 🛠️ TASK 4.1: OAuth → Spatial Workspace Territory (45 minutes)

### Mission
Fix `test_oauth_flow_creates_spatial_workspace_territory` to prove OAuth initialization creates spatial workspace correctly.

### Why This Matters
- Proves OAuth setup works with spatial system
- Critical for alpha: Users must be able to connect Slack workspaces
- Validates that spatial territory is initialized on OAuth completion

### Current Status
```bash
# Check test status
pytest tests/unit/services/integrations/slack/test_spatial_system_integration.py::test_oauth_flow_creates_spatial_workspace_territory -v

# Expected: Currently skipped or failing
```

### What to Do

**Step 1**: Investigate test expectations (10 min)
```bash
# Read the test
cat tests/unit/services/integrations/slack/test_spatial_system_integration.py | grep -A 50 "test_oauth_flow_creates_spatial_workspace_territory"

# Understand:
# - What OAuth flow it's testing
# - What spatial territory should be created
# - What assertions it makes
```

**Step 2**: Check existing OAuth → Spatial integration (10 min)
```bash
# We know from Phase 2 this method exists:
grep -n "validate_and_initialize_spatial_territory" services/integrations/slack/oauth_handler.py -A 20

# Check how it creates territory:
grep -n "initialize_spatial_territory" services/integrations/slack/oauth_handler.py -A 30

# Check SpatialTerritory structure:
grep -n "class SpatialTerritory" services/integrations/slack/spatial_types.py -A 20
```

**Step 3**: Identify what's missing (5 min)

**Common issues**:
- Mock OAuth response structure doesn't match real OAuth
- Territory creation needs additional fields
- Assertions expect fields that don't exist
- Need to mock SlackSpatialMapper

**Document finding**:
```bash
# Create investigation notes
echo "# OAuth → Spatial Investigation" > /tmp/oauth-spatial-investigation.txt
echo "Issue: [what's broken]" >> /tmp/oauth-spatial-investigation.txt
echo "Fix needed: [what to change]" >> /tmp/oauth-spatial-investigation.txt
```

**Step 4**: Implement fix (15 min)

**If test needs mock data update**:
```python
# Update mock OAuth response to match production structure
@pytest.fixture
def oauth_response():
    return {
        'team': {
            'id': 'T123',
            'name': 'Test Workspace'
        },
        'authed_user': {
            'id': 'U123',
            'access_token': 'xoxp-test',
            'scope': 'channels:read,chat:write'
        },
        # Add any missing fields the implementation expects
    }
```

**If test needs spatial territory mock**:
```python
# Mock SpatialTerritory creation
@pytest.fixture
def mock_spatial_territory(mocker):
    territory = mocker.Mock()
    territory.workspace_id = 'T123'
    territory.workspace_name = 'Test Workspace'
    territory.boundaries = {...}
    return territory
```

**If integration broken**:
- Check if OAuth handler actually calls spatial initialization
- Verify territory is returned/stored correctly
- Check if additional mocking needed

**Step 5**: Run test (5 min)
```bash
# Remove skip decorator if present
# Run the specific test
pytest tests/unit/services/integrations/slack/test_spatial_system_integration.py::test_oauth_flow_creates_spatial_workspace_territory -v

# Expected: PASS
```

**If test fails**: Read error message, adjust fix, retry

### Evidence Required
- [ ] Investigation notes showing what was broken
- [ ] Code changes (if any) with explanation
- [ ] Test output showing PASS
- [ ] No regressions in other tests

### Success Criteria
- test_oauth_flow_creates_spatial_workspace_territory PASSING
- OAuth → Spatial territory creation proven working
- No changes to production code (test-only fixes preferred)
- Clear documentation of what was fixed

### STOP Conditions
- If production code changes needed beyond test mocks
- If OAuth handler missing critical functionality
- If SpatialTerritory structure incompatible with test expectations
→ STOP and escalate with specific issue

---

## 🛠️ TASK 4.2: Slack Event → Spatial → Workflow Pipeline (60 minutes)

### Mission
Fix `test_slack_event_to_spatial_to_workflow_pipeline` - **THIS IS THE ALPHA DEMO**. Must prove complete flow: Slack message → Spatial event → Workflow creation.

### Why This Matters
**This is THE critical path test**. If this works, we can demo the entire feature to alpha users:
1. Slack message arrives
2. System creates spatial event
3. Workflow factory creates appropriate workflow
4. Workflow has spatial context for execution

### Current Status
```bash
# Check test status
pytest tests/unit/services/integrations/slack/test_spatial_system_integration.py::test_slack_event_to_spatial_to_workflow_pipeline -v

# Expected: Currently skipped or failing
```

### What to Do

**Step 1**: Map the complete pipeline (15 min)
```bash
# Understand the flow:

# 1. Slack Event Handler
grep -n "class SlackEventHandler" services/integrations/slack/ -r

# 2. Spatial Mapper
grep -n "class SlackSpatialMapper" services/integrations/slack/spatial_mapper.py -A 5

# 3. Workflow Factory
grep -n "class SlackWorkflowFactory" services/integrations/slack/slack_workflow_factory.py -A 5

# Document the pipeline:
echo "# Pipeline Components" > /tmp/pipeline-investigation.txt
echo "1. Event Handler: [location]" >> /tmp/pipeline-investigation.txt
echo "2. Spatial Mapper: [methods used]" >> /tmp/pipeline-investigation.txt
echo "3. Workflow Factory: [how workflows created]" >> /tmp/pipeline-investigation.txt
```

**Step 2**: Read test expectations (10 min)
```bash
# Read the full test
cat tests/unit/services/integrations/slack/test_spatial_system_integration.py | grep -A 100 "test_slack_event_to_spatial_to_workflow_pipeline"

# Understand:
# - What Slack event it simulates
# - What spatial event should be created
# - What workflow should result
# - What assertions are made
```

**Step 3**: Identify integration gaps (10 min)

**Common issues**:
- Components not wired together
- Missing integration layer
- Mock data doesn't flow through pipeline
- Workflow missing spatial context

**Check for integration code**:
```bash
# Is there a pipeline coordinator?
find . -name "*pipeline*" -o -name "*integration*" -type f | grep slack

# How are components connected?
grep -n "SlackWorkflowFactory" services/integrations/slack/*.py
grep -n "SlackSpatialMapper" services/integrations/slack/*.py
```

**Document findings**:
```bash
echo "Gap identified: [what's missing]" >> /tmp/pipeline-investigation.txt
echo "Fix approach: [how to connect]" >> /tmp/pipeline-investigation.txt
```

**Step 4**: Implement fix (20 min)

**If test needs complete pipeline mock**:
```python
# Mock the complete flow
@pytest.fixture
def mock_slack_pipeline(mocker):
    """Mock complete Slack → Spatial → Workflow pipeline"""

    # Mock event handler
    event_handler = mocker.Mock()
    event_handler.process_event.return_value = {
        'spatial_event': SpatialEvent(...),
        'navigation_decision': NavigationDecision(...)
    }

    # Mock spatial mapper (if separate)
    spatial_mapper = mocker.Mock()
    spatial_mapper.map_message_to_spatial_event.return_value = SpatialEvent(...)

    # Mock workflow factory
    workflow_factory = mocker.Mock()
    workflow_factory.create_workflow_from_spatial_event.return_value = Workflow(...)

    return {
        'event_handler': event_handler,
        'spatial_mapper': spatial_mapper,
        'workflow_factory': workflow_factory
    }
```

**If components need wiring**:
- Check if integration code exists but not called in test
- Verify test uses correct entry point
- Ensure mocks return expected types

**Step 5**: Run test (5 min)
```bash
# Remove skip decorator
# Run the test
pytest tests/unit/services/integrations/slack/test_spatial_system_integration.py::test_slack_event_to_spatial_to_workflow_pipeline -v -s

# Expected: PASS with full pipeline execution shown
```

**If test fails**:
- Check error message for which step failed
- Add debugging output to see data flow
- Verify each component works individually

### Evidence Required
- [ ] Pipeline investigation notes
- [ ] Complete flow diagram (text is fine)
- [ ] Test output showing PASS
- [ ] Evidence that Slack → Spatial → Workflow works

### Success Criteria
- test_slack_event_to_spatial_to_workflow_pipeline PASSING
- Can trace Slack message → Workflow creation
- Workflow contains spatial context
- **Can demo this flow for alpha users**

### STOP Conditions
- If components fundamentally incompatible
- If major architecture changes needed
- If workflow factory can't accept spatial events
→ STOP and escalate with specific blocker

---

## 🛠️ TASK 4.3: E2E Workflow Creation (45 minutes)

### Mission
Fix `test_end_to_end_workflow_creation` to prove workflows are serializable and executable.

### Why This Matters
- Workflows must be persistable (JSON serialization)
- Proves workflows can actually execute with spatial context
- Validates complete feature is production-ready

### Current Status
```bash
# Check test status
pytest tests/unit/services/integrations/slack/test_workflow_integration.py::TestWorkflowIntegration::test_end_to_end_workflow_creation -v

# Expected: Currently skipped with "end-to-end test issues"
```

### What to Do

**Step 1**: Understand serialization issue (10 min)
```bash
# Read the test
sed -n '/class TestWorkflowIntegration/,/^class /p' tests/unit/services/integrations/slack/test_workflow_integration.py | grep -A 50 "test_end_to_end_workflow_creation"

# Check what needs serialization:
# - Workflow object?
# - Spatial context?
# - Both?
```

**Step 2**: Identify non-serializable objects (10 min)
```bash
# Check SpatialWorkflowContext
grep -n "class SpatialWorkflowContext" services/integrations/slack/slack_workflow_factory.py -A 20

# Check if it has to_dict() method
grep -n "def to_dict" services/integrations/slack/slack_workflow_factory.py

# Check Workflow structure
grep -n "class.*Workflow" services/workflows/ -r
```

**Common issues**:
- Dataclass without `asdict()` support
- Mock objects in spatial context
- Datetime objects not JSON-serializable
- Nested objects without serialization

**Step 3**: Add serialization support (15 min)

**If SpatialWorkflowContext needs to_dict()**:
```python
# Add to SpatialWorkflowContext class
def to_dict(self) -> Dict[str, Any]:
    """Convert to JSON-serializable dict"""
    return {
        'workspace_id': self.workspace_id,
        'channel_id': self.channel_id,
        'user_id': self.user_id,
        'attention_level': self.attention_level,
        'spatial_coordinates': {
            'x': self.coordinates.x,
            'y': self.coordinates.y,
            'z': self.coordinates.z
        } if self.coordinates else None,
        # Add other fields as needed
    }

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'SpatialWorkflowContext':
    """Create from dict"""
    # Implementation
    pass
```

**If test needs serialization handling**:
```python
# Update test to use serializable context
def test_end_to_end_workflow_creation(workflow_factory, spatial_context):
    # Create workflow
    workflow = workflow_factory.create_workflow_from_spatial_event(...)

    # Serialize
    workflow_dict = workflow.to_dict()
    workflow_json = json.dumps(workflow_dict)

    # Deserialize
    restored_dict = json.loads(workflow_json)
    restored_workflow = Workflow.from_dict(restored_dict)

    # Verify
    assert restored_workflow.spatial_context == spatial_context
```

**Step 4**: Run test (10 min)
```bash
# Remove skip decorator
# Run test
pytest tests/unit/services/integrations/slack/test_workflow_integration.py::TestWorkflowIntegration::test_end_to_end_workflow_creation -v

# Expected: PASS
```

**If serialization still fails**:
- Use `json.dumps()` on workflow to see exact error
- Check which field is not serializable
- Add to_dict() for that object

### Evidence Required
- [ ] Serialization investigation notes
- [ ] Code changes (to_dict/from_dict if added)
- [ ] Test output showing PASS
- [ ] Proof workflows are JSON-serializable

### Success Criteria
- test_end_to_end_workflow_creation PASSING
- Workflows can be serialized to JSON
- Workflows can be deserialized and executed
- Spatial context preserved through serialization

### STOP Conditions
- If Workflow class architecture doesn't support serialization
- If spatial context fundamentally can't serialize
- If requires major refactoring of workflow system
→ STOP and escalate

---

### Checkpoint 2: Critical Path Tests Complete ✅

**Before proceeding to Task 4.4, verify**:
- [ ] OAuth → Spatial test PASSING
- [ ] Slack → Workflow pipeline test PASSING
- [ ] E2E Workflow creation test PASSING
- [ ] All fixes committed
- [ ] No regressions in other tests

**Verify test count**:
```bash
# Run full suite
pytest tests/unit/services/integrations/slack/ -v | grep -E "passed|skipped"

# Expected: 105-106 passed, 7-8 skipped
```

**If all verified**: Proceed to Task 4.4 (issue creation)
**If not 105-106**: Check which test didn't pass, investigate

---

## 🛠️ TASK 4.4: Create Issues for Deferred Work (20 minutes)

### Mission
Create GitHub issues for 3 deferred features so we have clear post-alpha roadmap.

### What to Do

**Issue 1**: Multi-Workspace Support
```bash
gh issue create \
  --title "SLACK-MULTI-WORKSPACE: Support attention across multiple workspaces" \
  --body "## Context
From SLACK-SPATIAL Phase 4: Deferred to Enterprise milestone.

## Description
Enable attention prioritization across multiple Slack workspace installations. Currently system handles single workspace, but Enterprise customers will have multiple workspaces that need coordinated attention.

## Requirements
- Support multiple OAuth installations per user
- Cross-workspace attention scoring
- Unified workspace territory management
- Workspace switching in UI

## Test Coverage
Skipped test: test_multi_workspace_attention_prioritization

## Milestone
Enterprise (Post-Alpha)

## Priority
P2

## Labels
slack, integration, enterprise-feature

## Blocked By
Requires multiple Slack installation infrastructure" \
  --label "slack,integration,enterprise-feature" \
  --milestone "Enterprise"
```

**Issue 2**: Pattern Learning Integration
```bash
gh issue create \
  --title "SLACK-ATTENTION-DECAY: Implement pattern learning for attention models" \
  --body "## Context
From SLACK-SPATIAL Phase 4: Deferred to Enhancement milestone.

## Description
Add time-decay and pattern learning to attention scoring system. Currently attention is static per-message, but should learn user patterns and decay over time.

## Requirements
- Attention decay algorithm (time-based)
- Pattern learning from user interactions
- Predictive attention scoring
- Integration with learning system

## Test Coverage
Skipped test: test_attention_decay_with_pattern_learning

## Milestone
Enhancement (Post-Alpha)

## Priority
P3

## Labels
slack, learning-system, enhancement

## Blocked By
Requires learning system (Roadmap Phase 3)" \
  --label "slack,learning-system,enhancement" \
  --milestone "Enhancement"
```

**Issue 3**: Spatial Memory Persistence
```bash
gh issue create \
  --title "SLACK-MEMORY: Persist spatial patterns over time" \
  --body "## Context
From SLACK-SPATIAL Phase 4: Deferred to Enhancement milestone.

## Description
Store and retrieve spatial interaction patterns over time for learning and analytics. Currently spatial events are ephemeral.

## Requirements
- Time-series storage for spatial events
- Pattern retrieval and analysis
- Historical attention tracking
- Spatial memory integration

## Test Coverage
Skipped test: test_spatial_memory_persistence

## Milestone
Enhancement (Post-Alpha)

## Priority
P3

## Labels
slack, spatial, memory, enhancement

## Blocked By
Requires time-series storage architecture" \
  --label "slack,spatial,memory,enhancement" \
  --milestone "Enhancement"
```

### Evidence Required
- [ ] Issue 1 created with number
- [ ] Issue 2 created with number
- [ ] Issue 3 created with number
- [ ] All issues have proper labels/milestones
- [ ] Issue numbers documented

### Success Criteria
- 3 issues created for deferred work
- Clear descriptions with context
- Proper milestone assignment
- Ready for post-alpha planning

---

## 🛠️ TASK 4.5: Final Verification (10 minutes)

### Mission
Run complete test suite and verify SLACK-SPATIAL is alpha-ready.

### What to Do

**Step 1**: Run full test suite
```bash
# Complete Slack integration test suite
pytest tests/unit/services/integrations/slack/ -v --tb=short > /tmp/phase4-final-output.txt 2>&1

# Show summary
tail -50 /tmp/phase4-final-output.txt
```

**Step 2**: Verify target achieved
```bash
# Extract counts
grep -E "passed|skipped|failed" /tmp/phase4-final-output.txt | tail -1

# Expected: "105-106 passed, 7-8 skipped, 0 failed"
# Percentage: 105/113 = 92.9% or 106/113 = 93.8%
```

**Step 3**: Document what's skipped
```bash
# List skipped tests
pytest tests/unit/services/integrations/slack/ -v | grep SKIPPED > /tmp/skipped-tests.txt

# Expected categories:
# - 5 advanced attention algorithm tests (P3 features)
# - 2-3 deferred system integration tests (now have issues)
```

**Step 4**: Commit final changes
```bash
# Stage all Phase 4 changes
git add -A

# Commit
git commit -m "feat(SLACK-SPATIAL): Phase 4 complete - Alpha ready

Critical path tests fixed:
- test_oauth_flow_creates_spatial_workspace_territory ✅
- test_slack_event_to_spatial_to_workflow_pipeline ✅
- test_end_to_end_workflow_creation ✅

Results: 105-106/113 tests passing (93-94%)

Demo flow proven: Slack → Spatial → Workflow working end-to-end

Deferred work:
- SLACK-MULTI-WORKSPACE: Issue #[number]
- SLACK-ATTENTION-DECAY: Issue #[number]
- SLACK-MEMORY: Issue #[number]

Phase 4 complete. SLACK-SPATIAL ready for alpha testing.
"

# Verify commit
git log --oneline -1

# Push to origin
git push origin main
```

### Evidence Required
- [ ] Test output: 105-106 passed, 7-8 skipped
- [ ] No test failures
- [ ] Percentage: 93-94%
- [ ] Git commit with final changes
- [ ] Push confirmation

### Success Criteria
- **105-106/113 tests passing (93-94%)**
- **Critical path proven: Slack → Spatial → Workflow**
- **Can demo feature end-to-end**
- **Issues created for deferred work**
- **All changes committed and pushed**

---

## 📊 Definition of DONE

SLACK-SPATIAL Phase 4 is **COMPLETE** when:

- ✅ 105-106/113 tests passing (93-94%)
- ✅ OAuth → Spatial workspace creation working
- ✅ Slack event → Workflow pipeline working (THE DEMO)
- ✅ E2E workflow serialization working
- ✅ Duplicate tests deleted
- ✅ Pattern-020 documentation updated
- ✅ 3 issues created for deferred work
- ✅ All evidence documented
- ✅ All changes committed and pushed
- ✅ **Alpha-ready**: Can demonstrate complete feature to users

**NOT done means**:
- ❌ "104 of 105 tests passing" - must hit target
- ❌ "Demo mostly works" - must work completely
- ❌ "Will create issues later" - must create now
- ❌ Any rationalization of incompleteness

---

## 🚨 STOP CONDITIONS

**STOP immediately and escalate if**:

### Infrastructure Issues
- ❌ OAuth handler missing critical functionality
- ❌ Workflow factory incompatible with spatial events
- ❌ Major architecture changes needed for tests
- ❌ Components fundamentally can't integrate

### Scope Creep
- ❌ Test requires new feature implementation
- ❌ Fix requires changes beyond test/mock layer
- ❌ Production code refactoring needed

### Regression Risk
- ❌ More than 5 existing tests start failing
- ❌ Changes affect core spatial/workflow systems
- ❌ Serialization changes break other features

### Stuck Pattern
- ❌ Same test failing for >30 minutes
- ❌ Can't identify root cause after investigation
- ❌ Multiple approaches tried without success

**When stopped**:
1. **Document** what you tried with evidence
2. **Explain** the specific blocker
3. **Provide** error messages and investigation notes
4. **Suggest** options if possible
5. **Wait** for guidance before proceeding

---

## 📝 Evidence Requirements (CRITICAL)

### For EVERY Task:
- **Investigation notes** - What you discovered
- **Code changes** - If any, with explanation
- **Test output** - Terminal output showing results
- **Git commits** - With descriptive messages
- **Verification** - No regressions in other tests

### For Final Deliverable:
- **Complete test run** - Full pytest output
- **Test counts** - Exact numbers (X passed, Y skipped)
- **Percentage** - Calculated passing rate
- **Git log** - Showing all Phase 4 commits
- **Push confirmation** - Git push output
- **Issue numbers** - All 3 deferred work issues

### Session Log:
- Timestamp all major actions
- Include evidence inline
- Document decisions and reasoning
- Note surprises or lessons learned

---

## 💡 Working Approach (Recommended)

### Pacing
- **Don't rush** - Quality over speed
- **Investigate first** - Understand before fixing
- **One test at a time** - Verify before moving on
- **Break if tired** - Can continue later

### Problem-Solving Pattern
1. **Read the test** - Understand expectations
2. **Check implementation** - See what exists
3. **Identify gap** - What's missing or broken
4. **Plan fix** - How to connect/repair
5. **Implement** - Make the change
6. **Verify** - Run test and check
7. **Document** - Note what and why

### Communication
- **Document reasoning** - Why you chose this approach
- **Explain surprises** - Anything unexpected
- **Show evidence** - Terminal output for claims
- **Ask if stuck** - Better to escalate than struggle

---

## 🎯 Remember

**This is the final push**:
- You've done excellent work (102/120 → 105-106/113)
- These 3 tests prove the complete feature works
- After this, Slack integration is alpha-ready
- Quality matters more than speed

**You're proving**:
- OAuth initialization works
- Event → Workflow pipeline works
- Workflows are executable
- **Complete feature ready for users**

**Trust the process**:
- Investigate thoroughly
- Fix systematically
- Verify completely
- Document clearly

---

## 🚀 Ready to Execute

**Status**: Ready for Phase 4 execution
**Expected Duration**: 3.5-4 hours
**Target**: 105-106/113 tests (93-94%)
**Impact**: SLACK-SPATIAL alpha-ready

---

_"Quality over speed - understand before fixing"_
_"One test at a time - verify before proceeding"_
_"Together we are making something incredible"_ 🏗️✨

**Good luck! Report back with results or questions.**

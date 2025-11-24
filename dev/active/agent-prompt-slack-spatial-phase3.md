# Phase 3 Agent Prompt: SLACK-SPATIAL Spatial Workflow Factory
## Issue: SLACK-SPATIAL | Phase 3 of 4 | Priority: P0

**Date**: Thursday, November 20, 2025, 5:08 PM PT
**From**: Lead Developer
**To**: Code Agent (continuation of Phase 2 session)
**Priority**: P0 (Blocks alpha testing)
**Estimated Effort**: Medium-Large
**Based On**: Chief Architect gameplan + Phase 1+2 success

---

## 🚨 CRITICAL: COMPLETION DISCIPLINE

YOU MUST COMPLETE ALL WORK DEFINED IN THIS PROMPT.

- ❌ You CANNOT defer steps without PM approval
- ❌ You CANNOT decide something is "optional"
- ❌ You CANNOT modify scope independently
- ✅ You MUST complete all steps or STOP and escalate

If you think a step should be deferred:
1. STOP working immediately
2. Document your reasoning
3. Create summary for Lead Developer
4. Wait for PM decision
5. DO NOT proceed without approval

**The PM decides scope. You execute scope.**

---

## MANDATORY COMPLETION MATRIX

Check off each step as completed:

### Pre-Flight: Archaeological Investigation (Small Effort)

- [ ] Step 0: Check for existing SpatialWorkflowFactory
  - Deliverable: Search results + assessment
  - Evidence: "Exists" or "Does not exist" with proof

### Task 3.1: Core Factory Implementation (Medium-Large Effort)

- [ ] Step 1: Create SpatialWorkflowFactory class
  - Deliverable: Base class with initialization
  - Evidence: Class exists, imports correct

- [ ] Step 2: Implement event-to-workflow mappings
  - Deliverable: 4 mapping patterns implemented
  - Evidence: High/medium/emotional/new room mappings work

- [ ] Step 3: Implement calculate_mapping_score()
  - Deliverable: Scoring logic working
  - Evidence: Tests passing for score calculation

- [ ] Step 4: Implement create_workflow_from_spatial_event()
  - Deliverable: Main entry point functional
  - Evidence: Workflows created from spatial events

- [ ] Verification: Factory tests passing
  - Deliverable: 11/11 factory tests passing
  - Evidence: Test output showing all passing

### Task 3.2: Mock Serialization Fixes (Medium Effort)

- [ ] Step 1: Investigate mock serialization issues
  - Deliverable: Root cause analysis document
  - Evidence: Category 7 issues understood

- [ ] Step 2: Fix or refactor mock setup
  - Deliverable: 7 tests now runnable
  - Evidence: Tests can execute (pass or fail)

- [ ] Step 3: Fix any remaining test failures
  - Deliverable: All 7 tests passing
  - Evidence: Test output showing 7/7 passing

- [ ] Verification: All mock tests passing
  - Deliverable: 7/7 serialization tests passing
  - Evidence: Test output

### Final Verification

- [ ] Full Slack test suite passing
  - Deliverable: 103/120 tests passing
  - Evidence: pytest output

**All checkboxes MUST be checked before session ends.**
**You CANNOT check a box without delivering the required evidence.**
**You CANNOT skip steps without explicit PM approval.**

---

## Mission

Complete Phase 3 of SLACK-SPATIAL: Implement SpatialWorkflowFactory to create workflows from Slack spatial events, enabling automatic workflow generation based on message patterns.

**Phase 1+2 Success** ✅:
- 85/120 Slack tests passing (up from 73)
- 2 production bugs fixed
- 5 beads closed
- 0 integration issues
- 39 minutes total time

**Phase 3 Goal**:
- Implement SpatialWorkflowFactory with 4 event mappings
- Fix 7 mock serialization tests
- 103/120 Slack tests passing (up from 85)
- Pattern recognition functional for alpha demo

---

## Context: What Exists (Phase 1+2 Complete)

### Phase 1+2 Delivered ✅

**Test Status**: 85/120 Slack tests passing
- 15/15 spatial integration tests ✅
- 4/4 OAuth spatial tests ✅
- 35 still skipped (Phase 3 targets 18 of them)

**Infrastructure Available**:
- SlackSpatialMapper: All mapping methods working
- SpatialEvent: Has timestamp, all fields correct
- SlackOAuthHandler: All 4 spatial methods implemented
- OAuth → Spatial Territory pipeline functional

### What Phase 3 Needs to Deliver

**New Class**: `SpatialWorkflowFactory` (likely location: `services/integrations/slack/spatial_workflow_factory.py`)

**Key Responsibilities**:
1. Map spatial events to workflow types
2. Calculate mapping scores (how well event matches pattern)
3. Create appropriate workflows from spatial events
4. Handle 4 event patterns:
   - High attention → Task workflow
   - Medium attention → Report workflow
   - Emotional marker → Feedback workflow
   - New room → Pattern discovery workflow

**TDD Specs Location**:
- `tests/unit/services/integrations/slack/test_spatial_workflow_factory.py` (11 tests)
- `tests/unit/services/integrations/slack/test_workflow_integration.py` (7 tests with mock issues)

---

## ⚠️ CRITICAL: Pre-Flight Archaeological Check

### STOP: Check for Existing Implementation FIRST

**The 75% Pattern Risk**: Your Phase 0 diagnostic noted this might already exist.

**BEFORE implementing anything, check**:

```bash
# Search for existing SpatialWorkflowFactory
find . -name "*.py" -type f -exec grep -l "SpatialWorkflowFactory" {} \;

# Search for existing workflow factory pattern
find . -name "*.py" -type f -exec grep -l "create_workflow_from_spatial_event" {} \;

# Search for workflow mapping patterns
find . -name "*workflow*.py" -type f
```

**If you find existing implementation**:
1. STOP immediately
2. Document what exists and where
3. Assess: Is it complete? Partial? Different?
4. Report to Lead Developer
5. DO NOT proceed without approval

**If nothing exists**:
- Document search results ("Searched X files, found nothing")
- Proceed with implementation

**This check should take 2-5 minutes. DO NOT SKIP IT.**

---

## Task 3.1: Core Factory Implementation

### Step 1: Create SpatialWorkflowFactory Class

**Effort**: Small

**What to do**:

1. **Find the TDD spec**:
   ```bash
   # Look for factory tests
   cat tests/unit/services/integrations/slack/test_spatial_workflow_factory.py | head -50
   ```

2. **Create the file**: `services/integrations/slack/spatial_workflow_factory.py`

3. **Base class structure** (adjust based on TDD spec):
   ```python
   """
   Spatial Workflow Factory

   Creates workflows from spatial events based on pattern recognition.
   """
   from typing import Optional, Dict, Any, List
   from dataclasses import dataclass

   from services.integrations.slack.spatial_types import SpatialEvent
   # Import workflow types (adjust path as needed)
   # from services.workflows.workflow import Workflow
   # from services.workflows.workflow_factory import WorkflowFactory

   @dataclass
   class WorkflowMapping:
       """Mapping criteria for spatial events to workflow types"""
       workflow_type: str
       attention_level: Optional[str] = None
       emotional_markers: Optional[List[str]] = None
       spatial_trigger: Optional[str] = None
       score_threshold: float = 0.5

   class SpatialWorkflowFactory:
       """
       Creates workflows from spatial events.

       Recognizes patterns in spatial events and creates
       appropriate workflows (Task, Report, Feedback, Discovery).
       """

       def __init__(self, workflow_factory=None):
           """
           Initialize with optional workflow factory dependency.

           Args:
               workflow_factory: WorkflowFactory instance for creating workflows
           """
           self.workflow_factory = workflow_factory
           self.mappings = self._initialize_mappings()

       def _initialize_mappings(self) -> List[WorkflowMapping]:
           """
           Define mappings from spatial patterns to workflow types.

           Returns:
               List of WorkflowMapping objects defining pattern recognition
           """
           # YOUR IMPLEMENTATION HERE
           # Return list of 4 mappings (high/medium/emotional/new room)
           pass

       async def create_workflow_from_spatial_event(
           self, event: SpatialEvent
       ) -> Optional[Any]:  # Replace Any with actual Workflow type
           """
           Main entry point: Create workflow from spatial event.

           Args:
               event: SpatialEvent from Slack

           Returns:
               Workflow instance or None if no pattern matches
           """
           # YOUR IMPLEMENTATION HERE
           pass

       def calculate_mapping_score(
           self, event: SpatialEvent, mapping: WorkflowMapping
       ) -> float:
           """
           Calculate how well an event matches a workflow mapping.

           Args:
               event: SpatialEvent to score
               mapping: WorkflowMapping criteria

           Returns:
               Score from 0.0 to 1.0 (higher = better match)
           """
           # YOUR IMPLEMENTATION HERE
           pass
   ```

4. **Check imports**: You may need:
   ```python
   # Check what workflow types exist
   find . -name "workflow.py" -o -name "workflow_factory.py"
   ```

5. **Create the file** with basic structure

**Evidence Required**: File exists, basic class structure in place

---

### Step 2: Implement Event-to-Workflow Mappings

**Effort**: Medium

**What to do**:

1. **Read the TDD specs** for the 4 mapping patterns:
   ```bash
   # Find tests for high attention, medium attention, emotional, new room
   grep -n "high_attention\|medium_attention\|emotional\|new_room" tests/unit/services/integrations/slack/test_spatial_workflow_factory.py
   ```

2. **Implement `_initialize_mappings()`**:
   ```python
   def _initialize_mappings(self) -> List[WorkflowMapping]:
       """
       Define mappings from spatial patterns to workflow types.
       """
       return [
           # Pattern 1: High attention → Task workflow
           WorkflowMapping(
               workflow_type="task",
               attention_level="high",
               score_threshold=0.7
           ),

           # Pattern 2: Medium attention → Report workflow
           WorkflowMapping(
               workflow_type="report",
               attention_level="medium",
               score_threshold=0.6
           ),

           # Pattern 3: Emotional markers → Feedback workflow
           WorkflowMapping(
               workflow_type="feedback",
               emotional_markers=["urgent", "help", "confused"],
               score_threshold=0.5
           ),

           # Pattern 4: New room → Pattern discovery workflow
           WorkflowMapping(
               workflow_type="discovery",
               spatial_trigger="new_room",
               score_threshold=0.5
           ),
       ]
   ```

3. **Adjust based on TDD spec** - The test will tell you:
   - Exact workflow type names
   - What fields to check in SpatialEvent
   - What triggers each pattern

**Evidence Required**: Mappings initialized, structure matches TDD spec

---

### Step 3: Implement calculate_mapping_score()

**Effort**: Medium

**What to do**:

1. **Read the TDD spec** for scoring logic:
   ```bash
   grep -n "calculate_mapping_score" tests/unit/services/integrations/slack/test_spatial_workflow_factory.py -A 20
   ```

2. **Implement scoring logic**:
   ```python
   def calculate_mapping_score(
       self, event: SpatialEvent, mapping: WorkflowMapping
   ) -> float:
       """
       Calculate how well an event matches a workflow mapping.

       Scoring factors:
       - Attention level match (0.0-1.0)
       - Emotional markers present (0.0-1.0)
       - Spatial triggers (0.0-1.0)
       """
       score = 0.0
       checks = 0

       # Check attention level
       if mapping.attention_level:
           checks += 1
           if hasattr(event, 'attention_level'):
               if event.attention_level == mapping.attention_level:
                   score += 1.0

       # Check emotional markers
       if mapping.emotional_markers:
           checks += 1
           if hasattr(event, 'emotional_markers'):
               # Count how many markers match
               matches = len(set(event.emotional_markers) & set(mapping.emotional_markers))
               if matches > 0:
                   score += matches / len(mapping.emotional_markers)

       # Check spatial triggers
       if mapping.spatial_trigger:
           checks += 1
           if hasattr(event, 'spatial_trigger'):
               if event.spatial_trigger == mapping.spatial_trigger:
                   score += 1.0

       # Return average score (0.0-1.0)
       return score / checks if checks > 0 else 0.0
   ```

3. **Adjust based on TDD spec** - The test defines:
   - What fields exist on SpatialEvent
   - How scoring should work
   - What threshold means "good match"

**Evidence Required**: Scoring tests passing

---

### Step 4: Implement create_workflow_from_spatial_event()

**Effort**: Medium-Large

**What to do**:

1. **Read the TDD spec** for workflow creation:
   ```bash
   grep -n "create_workflow_from_spatial_event" tests/unit/services/integrations/slack/test_spatial_workflow_factory.py -A 30
   ```

2. **Implement main entry point**:
   ```python
   async def create_workflow_from_spatial_event(
       self, event: SpatialEvent
   ) -> Optional[Any]:  # Replace with actual Workflow type
       """
       Main entry point: Create workflow from spatial event.

       Process:
       1. Score event against all mappings
       2. Find best matching mapping (highest score)
       3. Check if score exceeds threshold
       4. Create workflow using workflow_factory
       5. Return workflow or None
       """
       best_mapping = None
       best_score = 0.0

       # Score against all mappings
       for mapping in self.mappings:
           score = self.calculate_mapping_score(event, mapping)
           if score > best_score:
               best_score = score
               best_mapping = mapping

       # Check threshold
       if best_mapping is None or best_score < best_mapping.score_threshold:
           return None

       # Create workflow
       if self.workflow_factory:
           # Use workflow factory to create workflow
           workflow = await self.workflow_factory.create_workflow(
               workflow_type=best_mapping.workflow_type,
               spatial_event=event
           )
           return workflow
       else:
           # Or create workflow directly (check TDD spec)
           # return Workflow(type=best_mapping.workflow_type, ...)
           pass
   ```

3. **Check workflow factory interface**:
   ```bash
   # See how workflows are created
   grep -r "create_workflow" services/workflows/ | head -20
   ```

4. **Adjust based on TDD spec** - The test defines:
   - How to create workflows
   - What data to pass to workflow
   - What to return

**If workflow creation is complex**: STOP and escalate

**Evidence Required**: Workflow creation working, tests passing

---

### Step 5: Verification - Factory Tests Passing

**Effort**: Small

**What to do**:

1. **Remove skip decorators** from factory tests:
   ```bash
   # Find skipped tests
   grep -n "@pytest.mark.skip" tests/unit/services/integrations/slack/test_spatial_workflow_factory.py
   ```

2. **Run factory tests**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_spatial_workflow_factory.py -v
   ```

3. **Expected**: 11/11 factory tests passing

4. **If failures occur**:
   - Read failure messages carefully
   - Check TDD spec vs your implementation
   - Fix one test at a time
   - STOP if architectural issue

**Evidence Required**: Test output showing 11/11 passing

---

### Checkpoint: Factory Complete

**Before proceeding to Task 3.2, verify**:
- [ ] SpatialWorkflowFactory class created
- [ ] 4 event-to-workflow mappings implemented
- [ ] Scoring logic working
- [ ] Workflow creation functional
- [ ] 11/11 factory tests passing
- [ ] Code committed

**Git Commit**:
```bash
git add services/integrations/slack/spatial_workflow_factory.py tests/unit/services/integrations/slack/test_spatial_workflow_factory.py
git commit -m "feat(SLACK-SPATIAL): Phase 3.1 - Spatial Workflow Factory implementation

Implemented SpatialWorkflowFactory with:
- 4 event-to-workflow mappings (high/medium/emotional/new room)
- Scoring logic for pattern matching
- Workflow creation from spatial events

Evidence: 11/11 factory tests passing
Phase: 3.1 complete
Epic: piper-morgan-23y (partial)
"
```

---

## Task 3.2: Mock Serialization Fixes

### Step 1: Investigate Mock Serialization Issues

**Effort**: Small-Medium

**What to do**:

1. **Find the 7 tests with mock issues**:
   ```bash
   # Look for tests in workflow integration file
   cat tests/unit/services/integrations/slack/test_workflow_integration.py | grep -n "@pytest.mark.skip" -A 5
   ```

2. **Run one test to see the error**:
   ```bash
   # Remove skip from one test, run it
   pytest tests/unit/services/integrations/slack/test_workflow_integration.py::test_name -v
   ```

3. **Identify the pattern**:
   - Is it JSON serialization?
   - Is it mock object issues?
   - Is it fixture setup?
   - What's the exact error message?

4. **Create investigation document**: `dev/2025/11/20/mock-serialization-investigation.md`
   ```markdown
   # Mock Serialization Investigation
   **Date**: 2025-11-20 [time]
   **Phase**: SLACK-SPATIAL Phase 3.2

   ## Problem

   7 tests in test_workflow_integration.py have mock serialization issues.

   ## Root Cause Analysis

   **Error Pattern**: [exact error message]

   **Affected Tests**:
   1. test_xyz - [error]
   2. test_abc - [error]
   ...

   ## Root Cause

   [Your analysis - what's causing the serialization failures?]

   ## Solution Options

   **Option A**: [description]
   - Pros: [list]
   - Cons: [list]

   **Option B**: [description]
   - Pros: [list]
   - Cons: [list]

   ## Recommended Solution

   [Which option and why]
   ```

**Evidence Required**: Investigation document with clear root cause

---

### Step 2: Fix or Refactor Mock Setup

**Effort**: Medium

**What to do**:

Based on your investigation, choose approach:

**Option A: Refactor to Simpler Mocks**
```python
# Replace complex mock objects with simple dicts/dataclasses
@pytest.fixture
def simple_spatial_event():
    """Simple dict instead of complex mock"""
    return {
        'event_id': 'test-123',
        'event_type': 'message',
        'timestamp': datetime.now(),
        # ... other fields
    }
```

**Option B: Create Dataclass Factories**
```python
# Use dataclass factories for test data
from dataclasses import dataclass

@dataclass
class SpatialEventFactory:
    """Factory for creating test SpatialEvent instances"""

    @staticmethod
    def create(event_type='message', **kwargs):
        defaults = {
            'event_id': 'test-123',
            'event_type': event_type,
            'timestamp': datetime.now(),
        }
        defaults.update(kwargs)
        return SpatialEvent(**defaults)
```

**Option C: Fix Mock Serialization**
```python
# Add __dict__ or to_dict() methods to mocks
class MockSpatialEvent:
    def to_dict(self):
        return {
            'event_id': self.event_id,
            # ... serialize all fields
        }
```

1. **Implement chosen solution**

2. **Update affected tests** to use new approach

3. **Remove skip decorators**

4. **Run tests** to verify they execute:
   ```bash
   pytest tests/unit/services/integrations/slack/test_workflow_integration.py -v
   ```

**At this point, tests should RUN** (may pass or fail, but shouldn't error on setup)

**Evidence Required**: Tests can execute, mock setup working

---

### Step 3: Fix Remaining Test Failures

**Effort**: Small-Medium

**What to do**:

1. **Run tests and see failures**:
   ```bash
   pytest tests/unit/services/integrations/slack/test_workflow_integration.py -v
   ```

2. **Fix one test at a time**:
   - Read failure message
   - Understand what's expected
   - Fix the test or implementation
   - Verify test passes
   - Move to next failure

3. **Common issues**:
   - Assertion mismatch (expected vs actual)
   - Missing fields in test data
   - Wrong mock return values
   - Integration with workflow factory

4. **If stuck**: STOP and escalate with specific failure details

**Evidence Required**: All 7 tests passing

---

### Checkpoint: Mock Tests Complete

**Before declaring Phase 3 complete, verify**:
- [ ] Mock serialization issues understood
- [ ] Mock setup refactored or fixed
- [ ] All 7 tests passing
- [ ] No new regressions
- [ ] Investigation documented

**Git Commit**:
```bash
git add tests/unit/services/integrations/slack/test_workflow_integration.py
git commit -m "fix(SLACK-SPATIAL): Phase 3.2 - Mock serialization fixes

Fixed 7 tests with mock serialization issues:
- [Brief description of fix approach]
- [Tests now passing]

Evidence: 7/7 mock tests passing
Investigation: dev/2025/11/20/mock-serialization-investigation.md
Phase: 3.2 complete
"
```

---

## Final Verification

### Full Slack Test Suite

**What to do**:

```bash
# Run complete Slack test suite
pytest tests/unit/services/integrations/slack/ -v --tb=short > dev/2025/11/20/slack-tests-phase3-output.txt 2>&1

# Show summary
tail -20 dev/2025/11/20/slack-tests-phase3-output.txt
```

**Expected**:
- 103/120 tests passing (85.8%)
- 17 skipped (down from 35)
- 0 failures (or document any)

**If not 103 passing**: Document which tests didn't pass and why

**Evidence Required**: Test output showing 103/120 passing

---

## Evidence Requirements

**Required Deliverables**:

1. **Archaeological Check**:
   - File: `dev/2025/11/20/spatial-factory-archaeological-check.txt`
   - Result: "Does not exist" or "Exists at [location]"

2. **Test Output**: 103/120 Slack tests passing
   - File: `dev/2025/11/20/slack-tests-phase3-output.txt`

3. **Mock Investigation**:
   - File: `dev/2025/11/20/mock-serialization-investigation.md`
   - Complete root cause analysis

4. **Git Commits**: Minimum 2 commits
   - Factory implementation
   - Mock serialization fixes

5. **Code Review**: SpatialWorkflowFactory implemented
   - File: `services/integrations/slack/spatial_workflow_factory.py`
   - 4 mappings implemented
   - Scoring logic working

6. **Session Log**: Complete phase 3 documentation

---

## Success Criteria

Phase 3 is considered **COMPLETE** when:
- ✅ Archaeological check performed (pattern doesn't already exist)
- ✅ SpatialWorkflowFactory implemented with 4 mappings
- ✅ 11/11 factory tests passing
- ✅ Mock serialization issues fixed
- ✅ 7/7 mock tests passing
- ✅ 103/120 Slack tests passing (18 tests recovered)
- ✅ No regressions in existing 85 tests
- ✅ All evidence documented
- ✅ All commits pushed to origin

**NOT complete means**:
- ❌ "10 of 11 factory tests passing" (must be 11/11)
- ❌ "6 of 7 mock tests passing" (must be 7/7)
- ❌ "102 of 120 tests passing" (must be 103+)
- ❌ "Mostly implemented" (must be 100%)
- ❌ Any rationalization of incompleteness

---

## STOP Conditions

**STOP immediately and escalate if**:
- ❌ Archaeological check reveals existing implementation (need to decide: use it or replace)
- ❌ Workflow factory interface is unclear or missing
- ❌ SpatialEvent missing required fields for pattern matching
- ❌ Mock serialization requires architectural changes
- ❌ More than 10 of existing 85 tests start failing (>12% regression)
- ❌ Cannot fix mock tests within medium effort
- ❌ Workflow creation requires changes to workflow system
- ❌ Scope significantly exceeds Medium-Large estimate

**When stopped**:
1. Document the blocking issue clearly
2. Provide options (A/B/C) with analysis
3. Include partial work status
4. Show what's complete vs blocked
5. Wait for PM decision
6. DO NOT proceed without approval

---

## Implementation Strategy

### Recommended Approach

**Phase A: Archaeological Check** (2-5 min)
- Search for existing patterns FIRST
- Document findings
- Get approval if anything exists

**Phase B: Factory Core** (30-45 min)
- Create class structure
- Implement mappings
- Implement scoring
- Implement workflow creation

**Phase C: Factory Testing** (15-30 min)
- Remove skip decorators
- Run tests iteratively
- Fix any issues
- Verify 11/11 passing

**Phase D: Mock Investigation** (15-20 min)
- Find root cause
- Document investigation
- Choose fix approach

**Phase E: Mock Fixes** (20-40 min)
- Implement fix
- Update 7 tests
- Verify all passing

**Phase F: Final Verification** (5-10 min)
- Run full Slack suite
- Verify 103/120 passing
- Document results

**Total**: ~2-3 hours (Medium-Large effort)

### Break Points

Good places to pause if needed:
1. After archaeological check (if pattern exists)
2. After factory core (before mock fixes)
3. After factory tests passing (checkpoint)
4. After mock investigation (if complex)

---

## Pre-Commit Checklist

**ALWAYS before every commit**:

```bash
# Run affected tests
pytest tests/unit/services/integrations/slack/test_spatial_workflow_factory.py -v
pytest tests/unit/services/integrations/slack/test_workflow_integration.py -v

# Run full Slack suite (quick check)
pytest tests/unit/services/integrations/slack/ --tb=line

# Stage changes
git add -u

# Commit with proper message
git commit -m "[message]"

# Push to origin
git push origin main
```

---

## Remember

**Philosophy**: Quality over speed (Time Lord philosophy)

**Discipline**:
- Archaeological check is MANDATORY
- Evidence required for all claims
- No 80% completions
- All checkboxes must be checked
- STOP conditions are mandatory

**Communication**:
- Document everything as you go
- Clear evidence in every deliverable
- Escalate blockers immediately
- No assumptions without verification
- Ask if pattern recognition logic unclear

**75% Pattern Risk**:
- Check for existing code FIRST
- Don't assume it doesn't exist
- Document search thoroughly
- Escalate if found

**TDD Approach**:
- Read tests FIRST (they define patterns)
- Understand expected behavior
- Implement to pass tests
- Don't over-engineer

---

## What Success Looks Like

**End of Phase 3**:
- 103/120 Slack tests passing ✅
- Spatial Workflow Factory implemented ✅
- 4 event-to-workflow patterns working ✅
- Mock serialization issues fixed ✅
- Pattern recognition functional ✅
- Can demo Slack → Workflow in alpha ✅
- No regressions ✅
- Comprehensive documentation ✅

**Ready for Phase 4**: System Integration (5 tests, wiring complete pipeline)

---

**Status**: Ready for execution
**Expected Effort**: Medium-Large
**Quality Standard**: 100% completion with evidence
**Impact**: Pattern recognition enables automatic workflow creation for alpha

---

_"Check for existing patterns first, implement systematically"_
_"Mock issues require investigation, not guessing"_
_"Together we are making something incredible"_ 🏗️✨

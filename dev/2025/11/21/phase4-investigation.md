# Phase 4 Critical Tests Investigation

## Test 1: test_oauth_flow_creates_spatial_workspace_territory

**Location**: test_spatial_system_integration.py (line 96)

**Skip Decorator**: Lines 12-14 - pytestmark skips entire class

**Issue**: Complete test class skipped

**What it tests**:
- OAuth callback handling creates spatial workspace
- Territory created in spatial memory store
- Territory registered in workspace navigator
- Spatial context returned in OAuth result

**Dependencies needed**:
- SlackOAuthHandler with spatial initialization
- WorkspaceNavigator with territory tracking
- SpatialMemoryStore working
- OAuth response mock structured correctly

**Challenge**: This requires OAuth handler to actually call spatial initialization methods. Need to verify if oauth_handler.handle_oauth_callback() calls the spatial methods, or if we need to add that integration.

## Test 2: test_slack_event_to_spatial_to_workflow_pipeline

**Location**: test_spatial_system_integration.py (line 145)

**Status**: Skipped via class decorator

**What it tests** (THE DEMO):
- Slack message event → Spatial processing → Workflow creation
- Full pipeline from event to workflow output
- Spatial context preserved through pipeline

**Challenge**: Most complex test - requires all components integrated. Need to trace:
1. SlackEventHandler processes message
2. SlackSpatialMapper creates spatial event
3. SlackWorkflowFactory creates workflow
4. All data flows correctly

## Test 3: test_end_to_end_workflow_creation

**Location**: test_workflow_integration.py

**Status**: Skipped with decorator (checked earlier - line 469)

**What it tests**:
- Workflow serialization to JSON
- Intent classification with spatial context
- Workflow creation and execution

**Challenge**: JSON serialization issue - spatial context needs to be JSON-serializable

---

## Key Questions

1. Should we unskip the entire class or individual tests?
2. Do OAuth handler's actual methods create spatial territories, or is that new work?
3. Should we create new spatial integration methods or wire existing ones?
4. Is there a "happy path" version that works with minimal mocking vs full integration?

## Recommendation

These are **deep system integration tests**, not unit tests. They require:
- Multiple components working together
- Real data flowing through the system
- Significant state management (memory, navigator, attention)

**Time estimate**: 3-4 hours per test conservatively, possibly longer if components aren't properly integrated

**Risk**: We might discover architectural misalignments while fixing these

# Test Failure Detailed Breakdown by File
**Date**: 2025-11-19
**Companion to**: test-failure-categorization-report.md

---

## Test Files Analyzed (by priority)

### Priority 1: Quick Fix - Enum Issues ⚡

#### test_workflow_integration.py
**Location**: `tests/unit/services/integrations/slack/`
**Total Tests**: 14
**Status**: 13 ERROR, 1 unknown

**Root Cause**: `IntentCategory.PLANNING` doesn't exist (line 98 of spatial_intent_classifier.py)

**Error Pattern**:
```
ERROR at setup of TestSpatialIntentClassifier.test_*
services/integrations/slack/spatial_intent_classifier.py:98: in _create_intent_patterns
    intent_category=IntentCategory.PLANNING,
AttributeError: PLANNING
```

**Affected Tests**:
- TestSpatialIntentClassifier (13 tests - ALL ERROR at fixture setup)
  - test_create_intent_patterns
  - test_classify_help_request
  - test_classify_bug_report
  - test_classify_feature_request
  - test_classify_status_update
  - test_classify_performance_concern
  - test_classify_strategic_discussion
  - test_classify_feedback
  - test_classify_review_request
  - test_spatial_context_extraction
  - test_confidence_scoring
  - test_pattern_matching
  - test_classification_reasoning
- TestSlackWorkflowFactory (status unknown - likely affected)

**Fix**: Add `PLANNING = "planning"` and `REVIEW = "review"` to IntentCategory enum

**Impact**: 13+ tests would pass

---

#### test_spatial_workflow_factory.py
**Location**: `tests/unit/services/integrations/slack/`
**Total Tests**: 9
**Status**: 4 FAILED, 5 ERROR

**Root Cause**: `AttentionLevel.MEDIUM`, `.HIGH`, `.LOW` don't exist

**Error Samples**:
```python
# Line 111
event_result.attention_level = AttentionLevel.MEDIUM
AttributeError: MEDIUM

# Line 151
event_result.attention_level = AttentionLevel.MEDIUM
AttributeError: MEDIUM

# Line 178
event_result.attention_level = AttentionLevel.LOW
AttributeError: LOW
```

**Affected Tests - FAILED**:
1. test_medium_attention_event_creates_report_workflow (MEDIUM)
2. test_emotional_event_creates_feedback_workflow (MEDIUM)
3. test_new_room_event_creates_pattern_workflow (LOW)
4. test_no_mapping_returns_none (LOW)

**Affected Tests - ERROR** (cascade from PLANNING):
5. test_high_attention_event_creates_task_workflow
6. test_workflow_context_enrichment
7. test_mapping_score_calculation
8. test_intent_creation_from_spatial_event
9. test_workflow_factory_error_handling

**Fix**:
- Option A: Add HIGH/MEDIUM/LOW to AttentionLevel enum
- Option B: Map test usage to existing values (FOCUSED=high, AMBIENT=medium, etc.)

**Impact**: 9 tests would pass

---

#### test_spatial_system_integration.py
**Location**: `tests/unit/services/integrations/slack/`
**Total Tests**: 5 (TestCompleteOAuthToSpatialWorkflow)
**Status**: 5 FAILED (likely 4 enum, 1 OAuth)

**Root Causes**:
1. OAuth state validation (test setup issue)
2. AttentionLevel enum mismatches (likely)

**Tests**:
1. test_oauth_flow_creates_spatial_workspace_territory
   - **Error**: `SlackAuthFailedError: Invalid or expired OAuth state`
   - **Cause**: Test mock doesn't set up OAuth state correctly
   - **Scope**: OUT OF SCOPE (OAuth investigation needed)

2. test_slack_event_to_spatial_to_workflow_pipeline
   - **Likely**: Enum issues (not yet run individually)
   - **Scope**: QUICK FIX (probably)

3. test_multi_workspace_attention_prioritization
   - **Likely**: AttentionLevel enum issues
   - **Scope**: QUICK FIX

4. test_attention_decay_models_with_pattern_learning
   - **Likely**: AttentionLevel enum issues
   - **Scope**: QUICK FIX

5. test_spatial_memory_persistence_and_pattern_accumulation
   - **Likely**: Enum or integration issues
   - **Scope**: QUICK FIX or OUT OF SCOPE

**Impact**: 3-4 tests would pass with enum fix, 1 needs OAuth work

---

#### test_workflow_pipeline_integration.py
**Location**: `tests/unit/services/integrations/slack/`
**Total Tests**: 5 (TestCompleteWorkflowPipeline)
**Status**: 4 FAILED, 1 unknown

**Root Causes**:
1. Missing method: `SlackSpatialMapper.map_channel_to_room()`
2. Likely enum issues

**Tests**:
1. test_slack_help_request_creates_piper_task_workflow
   - **Error**: `AttributeError: 'SlackSpatialMapper' object has no attribute 'map_channel_to_room'`
   - **Fix**: Add stub method OR skip test
   - **Scope**: QUICK FIX

2. test_slack_bug_report_creates_incident_workflow
   - **Likely**: Same missing method + enum
   - **Scope**: QUICK FIX

3. test_slack_feature_request_creates_product_workflow
   - **Likely**: Same missing method + enum
   - **Scope**: QUICK FIX

4. test_workflow_creation_failure_graceful_handling
   - **Likely**: Same missing method
   - **Scope**: QUICK FIX

5. test_* (unknown - not in failure list)
   - **Status**: May be passing

**Impact**: 4 tests would pass with stub method

---

### Priority 2: Infrastructure Fixes 🔧

#### test_orchestration_engine.py
**Location**: `tests/unit/services/orchestration/`
**Total Tests**: 11
**Status**: 11 ERROR (all at setup)

**Root Cause**: Fixture doesn't initialize service container

**Error**:
```
tests/unit/services/orchestration/test_orchestration_engine.py:22: in engine
    return OrchestrationEngine()
services/orchestration/engine.py:76: in __init__
    llm_client = container.get_service("llm")
ContainerNotInitializedError: Container not initialized
```

**Affected Tests**:
1. test_create_workflow_from_intent_success
2. test_create_workflow_from_intent_failure
3. test_execute_workflow_not_found
4. test_analyze_file_success
5. test_analyze_file_missing_file_id
6. test_analyze_file_file_not_found
7. test_analyze_file_analysis_exception
8. test_task_handler_registration
9. test_placeholder_handler
10. test_workflow_state_transitions
11. test_workflow_error_handling

**Fix Strategy**:
```python
# Option A: Mock in fixture
@pytest.fixture
def engine(mocker):
    mocker.patch('services.container.service_container.get_service')
    return OrchestrationEngine()

# Option B: Initialize container in fixture
@pytest.fixture
async def engine():
    from services.container import container
    await container.initialize()
    return OrchestrationEngine()

# Option C: Dependency injection
@pytest.fixture
def engine():
    return OrchestrationEngine(llm_client=Mock(), ...)
```

**Impact**: 11 tests would pass

**Effort**: 1-2 hours (depends on chosen approach)

---

### Priority 3: Already Passing ✅

#### test_personality_profile.py
**Location**: `tests/unit/services/personality/`
**Status**: ✅ 7/7 PASSING

**Tests**:
- test_profile_creation_with_valid_values
- test_profile_warmth_level_bounds
- test_adjust_for_context_low_confidence
- test_adjust_for_context_high_confidence
- test_get_default_creates_valid_profile
- test_valid_context_creation
- test_invalid_confidence_bounds

**Note**: Analysis doc said 1 failed (test_piper_config_parsing_success) but that test doesn't exist in this file.

---

#### test_personality_preferences.py
**Location**: `tests/unit/services/`
**Status**: ✅ 10/10 PASSING

**Tests**:
- test_concise_communication_style
- test_balanced_communication_style
- test_detailed_communication_style
- test_structured_work_style
- test_exploratory_work_style
- test_data_driven_decision_making
- test_intuitive_decision_making
- test_examples_learning_style
- test_explanations_learning_style
- test_exploration_learning_style

**Note**: Analysis doc listed "test_piper_config_parsing_success" as failing, but can't find it.

---

#### test_key_rotation_service.py
**Location**: `tests/unit/services/security/`
**Status**: ✅ 10/10 PASSING

**Tests**:
- test_start_rotation_success
- test_start_rotation_no_existing_key
- test_start_rotation_user_specific_not_implemented
- test_phase_validate_new_key_success
- test_phase_validate_new_key_failure
- test_phase_begin_transition_gradual
- test_phase_begin_transition_immediate
- test_phase_begin_transition_canary
- test_test_key_health_success
- test_test_key_health_failure

**Note**: Analysis doc said "test_rotate_api_key_convenience" failed, but that test doesn't exist.

---

### Priority 4: Out of Scope 🚫

#### test_file_repository_migration.py
**Location**: `tests/unit/services/`
**Total Tests**: 9
**Status**: 9 ERROR (missing fixture)

**Root Cause**: Missing `async_transaction` fixture

**Recommendation**: Already documented in fixture errors category - defer to separate work

---

#### test_workflow_repository_migration.py
**Location**: `tests/unit/services/`
**Total Tests**: 6
**Status**: 6 ERROR (missing fixture)

**Root Cause**: Missing `async_transaction` fixture

**Recommendation**: Already documented in fixture errors category - defer to separate work

---

#### test_file_resolver_edge_cases.py
**Location**: `tests/unit/services/`
**Total Tests**: 5
**Status**: 5 ERROR (missing fixture)

**Root Cause**: Missing fixture (likely same async_transaction)

**Recommendation**: Already documented in fixture errors category - defer to separate work

---

## Summary Statistics

### By Scope
- **QUICK FIX** (< 1 hour): 30+ tests (enum + stub methods)
- **IN SCOPE** (1-3 hours): 11 tests (container fixture)
- **OUT OF SCOPE**: 20+ tests (fixture errors + OAuth)
- **ALREADY PASSING**: 27 tests (stale analysis doc)

### By Root Cause
- **Enum mismatches**: 25+ tests
- **Container initialization**: 11 tests
- **Missing methods**: 4 tests
- **Missing fixtures**: 20+ tests (deferred)
- **OAuth integration**: 1 test (out of scope)
- **Stale data**: 27 tests (already passing)

### Expected Impact of Quick Fixes
| Action | Time | Tests Fixed | New Pass Rate |
|--------|------|-------------|---------------|
| Current | - | 422 | 68.4% |
| + Add enums | 15 min | ~25 | 72.5% |
| + Add stub methods | 15 min | ~4 | 73.3% |
| + Fix container fixture | 1-2 hrs | ~11 | 75.0% |

---

**Generated**: 2025-11-19 12:08 PM
**Agent**: Claude Code (Sonnet 4.5)

# Session Log: Test Gap Fix - Issue #559

**Date**: 2026-01-09
**Start Time**: 21:00
**Issue**: #559 - TEST-GAP: Integration tests mock internal methods, missing real import/wiring verification
**Agent**: Claude Code (prog-code)

## Objective

Create new integration tests that verify real code paths instead of mocking internal methods. This addresses Pattern-045 ("Green Tests, Red User") where tests passed but the feature was broken for real users.

## Background

During Issue #490 debugging, discovered that integration tests were mocking:
1. `_check_portfolio_onboarding` and other internal methods
2. This allowed bugs to ship:
   - Wrong import paths (module doesn't exist)
   - Wrong method names (method doesn't exist)
   - Missing middleware exclusions

## Investigation Steps

### Step 1: Review Existing E2E Tests
- Location: `tests/e2e/test_onboarding_http_e2e.py`
- These are TRUE E2E tests - they use real HTTP with app lifespan
- Good reference for how to test without mocking

### Step 2: Review Problematic Integration Tests
- Location: `tests/integration/test_portfolio_onboarding_e2e.py`
- PROBLEM: Uses `patch.object()` on internal methods:
  - `_check_portfolio_onboarding`
  - `_get_calendar_summary`
  - `_get_onboarding_components`
- These mocks allow bugs to slip through because:
  - If the import path is wrong, tests still pass (mock replaces it)
  - If the method name is wrong, tests still pass (mock creates it)
  - If middleware excludes a path, tests still pass (mock bypasses it)

### Step 3: Analyze Code Flow
- Intent route: `web/api/routes/intent.py`
- IntentService: `services/intent/intent_service.py`
- ConversationHandler: `services/conversation/conversation_handler.py`
- Auth middleware: `services/auth/auth_middleware.py`

Key methods that get mocked but should be tested for real:
- `IntentService._check_active_onboarding()`
- `ConversationHandler._check_portfolio_onboarding()`
- `_get_onboarding_components()` (singleton pattern)

## Findings

### Anti-Pattern Identified: Internal Method Mocking in Integration Tests

**Bad Pattern** (from `test_portfolio_onboarding_e2e.py`):
```python
with patch.object(
    conversation_handler,
    "_check_portfolio_onboarding",
    side_effect=mock_check_onboarding,
):
    response = await conversation_handler.respond(...)
```

This pattern hides bugs because:
1. The actual `_check_portfolio_onboarding` method is never called
2. Its imports are never executed
3. Its database queries are never run

**Good Pattern** (what we created):
```python
# Test that imports actually work
from services.conversation.conversation_handler import _get_onboarding_components
manager, handler = _get_onboarding_components()
assert manager is not None
assert hasattr(manager, "create_session")
```

### Test Categories Created

1. **Import Wiring Tests** - Verify all imports resolve correctly
2. **Method Existence Tests** - Verify methods exist with expected signatures
3. **Auth Middleware Tests** - Verify exclusion rules work correctly
4. **HTTP Wiring Tests** - Test full HTTP -> Service chain
5. **Onboarding Integration Tests** - Test real onboarding flow without mocks

## Tests Created

**File**: `tests/integration/test_intent_wiring_integration.py`

### TestImportWiringVerification (5 tests)
- `test_onboarding_imports_from_conversation_handler` - Verifies `_get_onboarding_components` imports work
- `test_intent_service_onboarding_imports` - Verifies IntentService inline imports
- `test_first_meeting_detector_imports` - Verifies FirstMeetingDetector import
- `test_project_repository_imports` - Verifies ProjectRepository import
- `test_intent_service_can_instantiate` - Verifies IntentService instantiation

### TestMethodExistence (3 tests)
- `test_conversation_handler_methods_exist` - Verifies ConversationHandler methods
- `test_intent_service_methods_exist` - Verifies IntentService methods
- `test_onboarding_handler_methods_exist` - Verifies onboarding handler methods

### TestAuthMiddlewareExclusions (3 tests)
- `test_intent_endpoint_excluded_from_auth` - Verifies /api/v1/intent excluded
- `test_auth_required_paths_not_excluded` - Verifies protected paths require auth
- `test_setup_endpoints_excluded` - Verifies setup endpoints excluded

### TestHTTPIntentWiring (3 tests)
- `test_intent_endpoint_returns_200` - Verifies endpoint reachable
- `test_intent_response_structure` - Verifies response format
- `test_authenticated_request_has_user_context` - Verifies auth cookie -> user_id

### TestOnboardingWiringIntegration (3 tests)
- `test_onboarding_manager_session_lifecycle` - Verifies session CRUD
- `test_onboarding_handler_flow` - Verifies full onboarding state machine
- `test_singleton_manager_consistency` - Verifies singleton pattern works

### TestIntentServiceOnboardingIntegration (2 tests)
- `test_check_active_onboarding_no_session` - Verifies None when no session
- `test_check_active_onboarding_with_session` - Verifies routing to active session

## Verification

```
$ python -m pytest tests/integration/test_intent_wiring_integration.py -v
============================= test session starts ==============================
collected 19 items

tests/integration/test_intent_wiring_integration.py::TestImportWiringVerification::test_onboarding_imports_from_conversation_handler PASSED
tests/integration/test_intent_wiring_integration.py::TestImportWiringVerification::test_intent_service_onboarding_imports PASSED
tests/integration/test_intent_wiring_integration.py::TestImportWiringVerification::test_first_meeting_detector_imports PASSED
tests/integration/test_intent_wiring_integration.py::TestImportWiringVerification::test_project_repository_imports PASSED
tests/integration/test_intent_wiring_integration.py::TestImportWiringVerification::test_intent_service_can_instantiate PASSED
tests/integration/test_intent_wiring_integration.py::TestMethodExistence::test_conversation_handler_methods_exist PASSED
tests/integration/test_intent_wiring_integration.py::TestMethodExistence::test_intent_service_methods_exist PASSED
tests/integration/test_intent_wiring_integration.py::TestMethodExistence::test_onboarding_handler_methods_exist PASSED
tests/integration/test_intent_wiring_integration.py::TestAuthMiddlewareExclusions::test_intent_endpoint_excluded_from_auth PASSED
tests/integration/test_intent_wiring_integration.py::TestAuthMiddlewareExclusions::test_auth_required_paths_not_excluded PASSED
tests/integration/test_intent_wiring_integration.py::TestAuthMiddlewareExclusions::test_setup_endpoints_excluded PASSED
tests/integration/test_intent_wiring_integration.py::TestHTTPIntentWiring::test_intent_endpoint_returns_200 PASSED
tests/integration/test_intent_wiring_integration.py::TestHTTPIntentWiring::test_intent_response_structure PASSED
tests/integration/test_intent_wiring_integration.py::TestHTTPIntentWiring::test_authenticated_request_has_user_context PASSED
tests/integration/test_intent_wiring_integration.py::TestOnboardingWiringIntegration::test_onboarding_manager_session_lifecycle PASSED
tests/integration/test_intent_wiring_integration.py::TestOnboardingWiringIntegration::test_onboarding_handler_flow PASSED
tests/integration/test_intent_wiring_integration.py::TestOnboardingWiringIntegration::test_singleton_manager_consistency PASSED
tests/integration/test_intent_wiring_integration.py::TestIntentServiceOnboardingIntegration::test_check_active_onboarding_no_session PASSED
tests/integration/test_intent_wiring_integration.py::TestIntentServiceOnboardingIntegration::test_check_active_onboarding_with_session PASSED

=============================== 19 passed ========================================
```

## How These Tests Would Catch the Original Bugs

### Bug 1: Wrong Import Path
Original bug: Code imported from non-existent module.
- **Mocked test**: PASSED (mock bypasses import)
- **New test** (`test_onboarding_imports_from_conversation_handler`): FAILED - ImportError

### Bug 2: Wrong Method Name
Original bug: Called method that doesn't exist.
- **Mocked test**: PASSED (mock creates method on the fly)
- **New test** (`test_conversation_handler_methods_exist`): FAILED - hasattr returns False

### Bug 3: Missing Middleware Exclusion
Original bug: /api/v1/intent not in exclude_paths.
- **Mocked test**: PASSED (mock bypasses auth)
- **New test** (`test_intent_endpoint_excluded_from_auth`): FAILED - assertion fails

## Session Notes

### Key Insight
The problem wasn't that the original tests were bad per se - it's that they tested the WRONG layer. They tested "does ConversationHandler work when given a specific response from _check_portfolio_onboarding" rather than "does _check_portfolio_onboarding actually work."

### Test Layer Guidance
- **Unit tests**: Mock external dependencies (database, APIs), not internal methods
- **Integration tests**: Mock nothing - test real code paths
- **E2E tests**: Mock nothing - test real HTTP with real app

### Follow-Up Recommendations
1. Consider deprecating `test_portfolio_onboarding_e2e.py` or refactoring it
2. Add CI check that flags `patch.object(..., "_private_method")` patterns
3. Document this pattern in test guidelines

## End Time
21:45 (estimated)

## Outcome
SUCCESS - 19 new integration tests created, all passing.

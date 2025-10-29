# Complete File Paths Reference

## Test Files Found

### Main Test Files (7 files)

1. **Direct Interface Tests**
   - `/Users/xian/Development/piper-morgan/tests/intent/test_direct_interface.py` (275 lines)
   - Tests all 13 categories through direct API
   - Uses `BaseValidationTest.intent_service` fixture with real OrchestrationEngine

2. **Web Interface Tests**
   - `/Users/xian/Development/piper-morgan/tests/intent/test_web_interface.py` (335 lines)
   - Tests all 13 categories through Web API
   - Uses custom `intent_service` fixture with mocked orchestration

3. **Slack Interface Tests**
   - `/Users/xian/Development/piper-morgan/tests/intent/test_slack_interface.py` (345 lines)
   - Tests all 13 categories through Slack integration
   - Uses custom `intent_service` fixture with mocked orchestration

4. **CLI Interface Tests**
   - `/Users/xian/Development/piper-morgan/tests/intent/test_cli_interface.py` (335 lines)
   - Tests all 13 categories through CLI interface
   - Uses custom `intent_service` fixture with mocked orchestration

5. **Base Validation Test**
   - `/Users/xian/Development/piper-morgan/tests/intent/base_validation_test.py` (77 lines)
   - Base class for all validation tests
   - Provides `intent_service` fixture with real OrchestrationEngine
   - Implements `validate_category()` and assertion helpers

6. **Test Constants**
   - `/Users/xian/Development/piper-morgan/tests/intent/test_constants.py` (58 lines)
   - Defines `INTENT_CATEGORIES` (uppercase strings)
   - Defines `CATEGORY_EXAMPLES` (test messages for each category)
   - Defines `PERFORMANCE_THRESHOLDS` (max response time, etc.)
   - Total test count expectations

7. **Test Configuration**
   - `/Users/xian/Development/piper-morgan/tests/conftest.py` (116 lines)
   - Global pytest configuration
   - Provides `intent_service` fixture with `orchestration_engine=None`
   - Provides `client_with_intent` fixture for Web API tests

### Contract Test Files (5 files)

All located in `/Users/xian/Development/piper-morgan/tests/intent/contracts/`

1. `/Users/xian/Development/piper-morgan/tests/intent/contracts/test_accuracy_contracts.py`
   - Tests classification accuracy across all 13 categories
   - Verifies confidence scores and accuracy thresholds

2. `/Users/xian/Development/piper-morgan/tests/intent/contracts/test_error_contracts.py`
   - Tests error handling for all categories
   - Verifies graceful degradation

3. `/Users/xian/Development/piper-morgan/tests/intent/contracts/test_bypass_contracts.py`
   - Tests conversation handler bypass logic
   - Verifies Tier 1 bypass for greetings

4. `/Users/xian/Development/piper-morgan/tests/intent/contracts/test_multiuser_contracts.py`
   - Tests multi-user intent handling
   - Verifies session isolation

5. `/Users/xian/Development/piper-morgan/tests/intent/contracts/test_performance_contracts.py`
   - Tests performance thresholds
   - Verifies response times < 4000ms

### Supporting Test Files

- `/Users/xian/Development/piper-morgan/tests/intent/coverage_tracker.py`
  - Tracks test coverage metrics
  - Provides `coverage` singleton

- `/Users/xian/Development/piper-morgan/tests/archive/test_conversation_aware.py`
  - Archived conversation-aware tests

- `/Users/xian/Development/piper-morgan/tests/conversation/test_conversation_manager_integration.py`
  - Integration tests for conversation manager

## Production Code Files

### Core Intent Service

1. **Main Intent Service**
   - `/Users/xian/Development/piper-morgan/services/intent/intent_service.py` (3800+ lines)
   - **Line 199**: `if intent.category.value == "conversation":` ← THE BUG
   - **Lines 232-256**: Routing for other categories using `.upper()`
   - **Line 311-331**: `_handle_conversation_intent()` method

2. **Conversation Handler**
   - `/Users/xian/Development/piper-morgan/services/conversation/conversation_handler.py` (232 lines)
   - **Line 40-56**: `respond()` method for CONVERSATION intents
   - **Line 58-120**: `_handle_clarification_needed()` for vague requests
   - **Line 122-232**: `handle_clarification_response()` for follow-ups

### Enum Definitions

3. **Shared Types (Enum Source)**
   - `/Users/xian/Development/piper-morgan/services/shared_types.py`
   - **Lines 9-22**: `IntentCategory` enum with all 13 categories
   - **Line 16**: `CONVERSATION = "conversation"` ← Enum value (lowercase)
   - All enum values are lowercase strings

### Intent Classification

4. **Intent Classifier**
   - `/Users/xian/Development/piper-morgan/services/intent_service/classifier.py`
   - **Line 224**: Returns Intent with `IntentCategory.CONVERSATION` for vague requests

5. **Intent Classification Tests**
   - `/Users/xian/Development/piper-morgan/tests/services/test_llm_intent_classifier.py`
   - Tests intent classification accuracy

### Related Services

6. **Domain Models**
   - `/Users/xian/Development/piper-morgan/services/domain/models.py`
   - Defines `Intent` class with category field

7. **API Serializers**
   - `/Users/xian/Development/piper-morgan/services/api/serializers.py`
   - Provides `intent_to_dict()` function

## Quick Navigation

### For Understanding the Bug
1. Read `/Users/xian/Development/piper-morgan/services/intent/intent_service.py` line 199
2. Compare with lines 232-256
3. Check enum definition at `/Users/xian/Development/piper-morgan/services/shared_types.py` line 16

### For Understanding Test Coverage
1. Start with `/Users/xian/Development/piper-morgan/tests/conftest.py` line 75
2. See the fixture at `/Users/xian/Development/piper-morgan/tests/intent/base_validation_test.py` line 34
3. View tests in `/Users/xian/Development/piper-morgan/tests/intent/test_direct_interface.py` lines 242-257

### For Understanding Test Data
1. Constants: `/Users/xian/Development/piper-morgan/tests/intent/test_constants.py`
2. Examples: Line 36-50 (CATEGORY_EXAMPLES)
3. Thresholds: Line 52-57 (PERFORMANCE_THRESHOLDS)

## Summary Statistics

**Test Files**: 12 total
- 7 main test files
- 5 contract test files

**Test Count**: 117 tests
- 52 interface tests (13 categories × 4 interfaces)
- 65 contract tests (13 categories × 5 contract types)

**Coverage**: 100% categories, 100% interfaces

**Bug Location**: `/Users/xian/Development/piper-morgan/services/intent/intent_service.py` line 199

**Enum Definition**: `/Users/xian/Development/piper-morgan/services/shared_types.py` lines 9-22

**Test Fixtures**:
- Standard: `/Users/xian/Development/piper-morgan/tests/conftest.py` line 30-86
- Deep: `/Users/xian/Development/piper-morgan/tests/intent/base_validation_test.py` line 16-41

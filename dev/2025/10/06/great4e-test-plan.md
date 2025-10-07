# GREAT-4E Test Plan

## Test Coverage Matrix

| Category | Web | Slack | CLI | Direct | Total |
|----------|-----|-------|-----|--------|-------|
| TEMPORAL | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| STATUS   | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| PRIORITY | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| IDENTITY | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| GUIDANCE | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| EXECUTION| [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| ANALYSIS | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| SYNTHESIS| [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| STRATEGY | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| LEARNING | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| UNKNOWN  | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| QUERY    | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| CONVERSATION | [ ] | [ ] | [ ] | [ ]  | 0/4   |
| **TOTAL**| 0/13| 0/13  | 0/13| 0/13   | **0/52** |

## Contract Test Matrix

| Category | Perf | Accuracy | Error | Multi-User | Bypass | Total |
|----------|------|----------|-------|------------|--------|-------|
| TEMPORAL | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| STATUS   | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| PRIORITY | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| IDENTITY | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| GUIDANCE | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| EXECUTION| [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| ANALYSIS | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| SYNTHESIS| [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| STRATEGY | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| LEARNING | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| UNKNOWN  | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| QUERY    | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| CONVERSATION | [ ]| [ ]    | [ ]   | [ ]        | [ ]    | 0/5   |
| **TOTAL**|0/13  |0/13      |0/13   |0/13        |0/13    |**0/65**|

## Test Execution Order

1. Phase 1: Category validation (13 tests)
2. Phase 2: Interface validation (52 tests)
3. Phase 3: Contract validation (65 tests)
4. Phase 4: Load testing (5 benchmarks)
5. Phase 5: Documentation (6 documents)

Total: 135 items + 6 documents = 141 items

## Stop Conditions

- Any category fails validation
- Coverage <100% at any checkpoint
- Performance regression detected
- Documentation incomplete

## Interface Details

### Web Interface
- Entry point: `web/app.py`
- Route: `/api/chat` (POST)
- Authentication: Session-based
- Example: `curl -X POST http://localhost:8001/api/chat -d '{"message": "What's on my calendar?"}'`

### Slack Interface
- Entry point: `services/integrations/slack/slack_integration_router.py`
- Event: `message.channels`
- Authentication: Slack token
- Example: Slack message to bot

### CLI Interface
- Entry point: `main.py`
- Command: `python main.py "What's on my calendar?"`
- Authentication: Local user context
- Example: Direct CLI invocation

### Direct Interface
- Entry point: `services/intent/intent_service.py`
- Method: `IntentService.process_intent(message, session_id)`
- Authentication: Session ID
- Example: Direct Python API call

## Performance Requirements

- **Response time**: <100ms for intent classification
- **Accuracy**: >90% classification accuracy
- **Cache hit rate**: >80% for repeated queries
- **Throughput**: >100 requests/second

## Test Infrastructure

- **Test constants**: `tests/intent/test_constants.py`
- **Coverage tracker**: `tests/intent/coverage_tracker.py`
- **Base test class**: `tests/intent/base_validation_test.py`
- **Stub generator**: `dev/2025/10/06/generate_test_stubs.py`

## Documentation Deliverables

1. Interface validation guide
2. Contract test guide
3. Performance benchmark report
4. Coverage report
5. Known issues log
6. Deployment checklist

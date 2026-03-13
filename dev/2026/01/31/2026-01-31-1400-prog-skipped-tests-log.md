# Session Log: Skipped Tests Issue Drafts

**Role**: Programmer Subagent
**Task**: Draft GitHub issue bodies for 4 skipped test categories
**Date**: 2026-01-31
**Started**: 14:00

## Objective

Analyze 4 categories of skipped tests and draft detailed GitHub issues:
1. Category 2a: Attention System Time Simulation (3 tests)
2. Category 3: Complex Mocking - Slack Observability (1 test)
3. Category 4: Context Tracker Entity Extraction (4 tests)
4. Category 5b: Knowledge Graph Integration (1 test)

## Work Completed

### 14:00 - Read Test Files

Read and analyzed:
- `tests/unit/services/integrations/slack/test_attention_scenarios_validation.py`
- `tests/unit/test_slack_components.py`
- `tests/unit/services/conversation/test_context_tracker.py`
- `tests/unit/services/test_llm_intent_classifier.py`

### 14:05 - Read Source Files

Analyzed related implementation files:
- `services/integrations/slack/attention_model.py`
- `services/conversation/context_tracker.py`
- `services/integrations/slack/response_handler.py`
- `services/intent_service/llm_classifier.py`
- `services/intent_service/llm_classifier_factory.py`

### 14:10 - Key Findings

**Category 2a - Attention System**:
- 3 tests skipped due to time simulation issues
- Root cause: `AttentionEvent.created_at = field(default_factory=datetime.now)` captures real time at dataclass creation
- Mocking `datetime.now` doesn't affect the `default_factory` which has already captured the real function
- Need freezegun or injectable clock pattern

**Category 3 - Slack Observability**:
- 1 test skipped due to complex mocking sync issues
- The spatial adapter's `_context_storage` isn't synced with `_timestamp_to_position`
- Test expects EXECUTION category for workflow creation
- Silent async exceptions hide failures

**Category 4 - Context Tracker Entity**:
- 4 tests fail because entity regex is too aggressive
- Pattern `r"(I|me|my|you|your)"` matches single letters "i" and "my" in phrases
- Test expects 2 entities, code extracts 4

**Category 5b - Knowledge Graph**:
- 1 test skipped, claims container initialization needed
- But `LLMClassifierFactory.create_for_testing()` already sets `enable_learning=False`
- The skip reason may be stale - test may actually be fixable now

### 14:15 - Created Issue Drafts

All 4 drafts written to /tmp/ as requested.

## Session End: 14:20

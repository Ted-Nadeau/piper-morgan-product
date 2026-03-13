# Gameplan: #764 GLUE-MULTIINTENT — Multi-Intent Handling Enhancements

**Issue**: #764
**Branch**: `claude/m0-conversational-glue`
**Date**: 2026-02-17
**Author**: Lead Developer (Claude Code Opus)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (port 8001)
- [x] Testing framework: pytest
- [x] Database: PostgreSQL (port 5433)
- [x] Multi-intent foundation: #595 complete (MultiIntentResult, detect_multiple_intents, classify_multiple)
- [x] Intent architecture: ADR-049 Tier 1/Tier 2 established
- [x] ProcessRegistry: Active with onboarding, standup, clarification, slot-filling handlers

**My understanding of the task**:
- Extend multi-intent handling from greeting+substantive to multi-substantive
- Create an orchestration layer that receives MultiIntentResult with 2+ substantive intents
- Execute each intent through existing handlers independently
- Aggregate responses into a single coherent message

**I assume the current state is**:
- `detect_multiple_intents()` catches multi-pattern messages (17+ pattern groups)
- `classify_multiple()` returns MultiIntentResult (rules → LLM fallback, but LLM returns single intent)
- IntentService only processes greeting+substantive; secondary substantive intents are stored but ignored

### Part A.2: Work Characteristics Assessment

**SKIP WORKTREE** — Single agent, sequential work, tightly coupled files within intent/orchestration layer.

### Part C: Proceed/Revise

- [x] **PROCEED** — Investigation verified: #595 foundation solid, gaps well-understood, approach is clear (Orchestration Layer per Chief Architect guidance).

---

## Phase 0: Initial Bookending

**Completed during investigation phase (this session).**

Key findings:
- MultiIntentResult: `services/intent_service/pre_classifier.py:9-64`
- detect_multiple_intents(): `services/intent_service/pre_classifier.py:1008-1126`
- classify_multiple(): `services/intent_service/classifier.py:713-772`
- Handle-all strategy: `services/intent/intent_service.py:352-390`
- Tests: `tests/unit/services/test_multi_intent.py` (27 tests)
- Issue enriched and updated on GitHub

---

## Phase 0.6: Data Flow Verification

### Data Flow for Multi-Intent

```
User Message
    ↓
IntentService._process_intent_internal()
    ↓
classify_multiple() → MultiIntentResult
    ↓
[NEW] IntentOrchestrator.execute(multi_result)
    ↓
For each intent: CanonicalHandlers.handle(intent, session_id, user_id)
    ↓
[NEW] ResponseAggregator.aggregate(results)
    ↓
IntentProcessingResult (single coherent response)
```

### Pattern Adaptation Notes

| Aspect | Source Pattern (#595) | This Implementation | Why Different? |
|--------|----------------------|---------------------|----------------|
| Detection | Pattern-based, returns all matches | Same | No change needed |
| LLM fallback | Returns single intent | Same for now | Extending LLM is out of scope |
| Handling | Only greeting+substantive | All substantive intents | Core of this issue |
| Response | Prepend "Hi there!" | Natural transitions + aggregation | Need coherent multi-part response |
| Error handling | No error path | Partial failure with graceful fallback | Process primary, note failures |

---

## Phase 1: IntentOrchestrator + ExecutionPlan Data Model

**Objective**: Create the core orchestration data model and the IntentOrchestrator class.

**Location**: `services/intent_service/orchestrator.py` (new file)

**Tasks**:
- [ ] Create `ExecutionPlan` dataclass (intent list, execution_order: parallel/sequential, max_intents cap)
- [ ] Create `IntentExecutionResult` dataclass (intent, response, success, error, duration_ms)
- [ ] Create `OrchestratedResponse` dataclass (results list, aggregated_message, partial_failure)
- [ ] Create `IntentOrchestrator` class with:
  - `create_plan(multi_result: MultiIntentResult) → ExecutionPlan`
  - `execute_plan(plan: ExecutionPlan, session_id, user_id) → OrchestratedResponse`
  - Intent cap validation (max 4)
  - Graceful fallback (on failure, return primary intent result only)
- [ ] Unit tests: 20-25 tests covering plan creation, execution, cap, fallback

**Deliverables**:
- `services/intent_service/orchestrator.py`
- `tests/unit/services/intent_service/test_orchestrator.py`

---

## Phase 2: Response Aggregation

**Objective**: Build natural-language aggregation of multi-intent responses.

**Location**: `services/intent_service/response_aggregator.py` (new file)

**Tasks**:
- [ ] Create `ResponseAggregator` class with:
  - `aggregate(results: list[IntentExecutionResult]) → str`
  - Natural transitions ("Here's your calendar update. As for the sprint status, ...")
  - Partial failure messaging ("I was able to X, but couldn't Y because ...")
  - Single-result passthrough (no aggregation needed for 1 result)
- [ ] Transition phrases library (avoid repetition)
- [ ] Unit tests: 15-20 tests for aggregation, transitions, partial failures

**Deliverables**:
- `services/intent_service/response_aggregator.py`
- `tests/unit/services/intent_service/test_response_aggregator.py`

---

## Phase 3: IntentService Integration

**Objective**: Wire the orchestrator into the existing IntentService flow.

**Location**: `services/intent/intent_service.py` (modify existing)

**Tasks**:
- [ ] Extend multi-intent handling block (lines ~352-390) to detect multi-substantive
- [ ] When `multi_result.is_multi_intent` AND has 2+ substantive intents → route to IntentOrchestrator
- [ ] Preserve existing greeting+substantive handling (no regression)
- [ ] Wire `session_id` and `user_id` through to orchestrator
- [ ] Add `multi_intent_orchestrated` field to IntentProcessingResult
- [ ] Integration tests: 10-15 tests for full routing path
- [ ] Regression tests: Verify existing greeting+substantive still works

**Deliverables**:
- Modified `services/intent/intent_service.py`
- `tests/unit/services/intent_service/test_multi_intent_orchestration.py`

---

## Phase 4: Colleague Test + Regression

**Objective**: Verify the system behaves like a colleague, not a robot.

**Tasks**:
- [ ] Create 6+ colleague test scenarios:
  1. "Check my calendar and update sprint status" → both answered in one response
  2. "What's the top priority and who's blocked?" → two query responses aggregated
  3. "Hi! What's on my agenda and any PRs to review?" → greeting + two substantive
  4. Single intent message → unchanged behavior (no regression)
  5. Three intents → all three processed, natural aggregation
  6. Partial failure → successful intents answered, failure acknowledged
- [ ] Run full regression suite:
  - Existing 27 multi-intent tests (#595)
  - Intent service tests (~700)
  - Process registry tests (~32)
- [ ] Verify <200ms additional latency (execution plan overhead)

**Deliverables**:
- `tests/unit/services/intent_service/test_multi_intent_colleague.py`
- Regression evidence

---

## Phase Z: Final Bookending & Handoff

- [ ] All acceptance criteria verified with evidence
- [ ] Commit with descriptive message
- [ ] Push to `claude/m0-conversational-glue`
- [ ] Update #764 issue description (checkboxes, status, evidence)
- [ ] Add closing comment with implementation evidence
- [ ] Close issue
- [ ] Update session log

---

## Test Scope Requirements

| Test Type | Count | What They Verify |
|-----------|-------|------------------|
| Unit: Orchestrator | 20-25 | Plan creation, execution, cap, fallback |
| Unit: Aggregator | 15-20 | Response aggregation, transitions, partial failures |
| Integration: Routing | 10-15 | Full path from classify_multiple → orchestrator → response |
| Colleague | 6+ | Natural behavior, no regression |
| **Total** | **~55-65** | |

---

## STOP Conditions

- IntentService structure has changed since investigation
- CanonicalHandlers interface doesn't match what orchestrator needs
- Existing multi-intent tests (#595) regress
- Performance exceeds 200ms additional latency
- Pattern conflicts with ADR-049 Tier 1/Tier 2 architecture

---

## Success Criteria

- [ ] "X and Y" with two substantive intents handled correctly >90%
- [ ] Execution order respects dependencies (parallel by default)
- [ ] Single coherent response returned
- [ ] Partial failures handled gracefully
- [ ] Performance impact <200ms additional latency
- [ ] Passes Colleague Test
- [ ] No regressions in 27 existing multi-intent tests
- [ ] No regressions in ~700 intent service tests
- [ ] Existing handlers NOT modified (orchestration layer only)

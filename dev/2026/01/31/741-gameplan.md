# Gameplan: #741 - Fix _store_classification Intent Attributes

**Issue**: #741 - BUG: _store_classification uses wrong Intent attributes
**Date**: 2026-01-31
**Estimated Effort**: Small (2 line fix + test unskip)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Testing framework: pytest
- [x] Relevant file: `services/intent_service/llm_classifier.py` (exists, verified)
- [x] Test file: `tests/unit/services/test_llm_intent_classifier.py` (exists, verified)

**My understanding of the task**:
- Fix 2 incorrect attribute references in `_store_classification()` method
- `intent.message` should be `intent.original_message` (line 698)
- `intent.session_id` doesn't exist on Intent class (line 702)
- Remove skip decorator from test after fix

### Part A.2: Work Characteristics Assessment

**Worktree Assessment:**
- [ ] Multiple agents will work in parallel - NO
- [ ] Task duration >30 minutes - NO (< 15 min)
- [ ] Multi-component work - NO (single file fix)
- [ ] Exploratory/risky changes - NO (targeted fix)

**Assessment:** ✅ **SKIP WORKTREE** - Single agent, small fix, < 15 min estimate

### Part B: PM Verification

**This is a targeted bug fix with clear root cause already identified.**

**What exists:**
- `services/intent_service/llm_classifier.py` - Line 698, 702 have bugs
- `services/domain/models.py` - Intent dataclass has `original_message`, no `session_id`
- `tests/unit/services/test_llm_intent_classifier.py` - Test skipped at line 243

### Part C: Proceed/Revise Decision
- [x] **PROCEED** - Understanding is correct, fix is straightforward

---

## Phase 0: Initial Bookending - GitHub Investigation

### Already Complete ✅

Investigation already performed during audit cascade:
- Root cause identified: Wrong attribute names in `_store_classification()`
- Test failure verified: `'Intent' object has no attribute 'message'`
- Intent class inspected: Has `original_message`, no `session_id`

---

## Phase 0.5-0.8: Not Applicable

- ❌ Phase 0.5 (Frontend-Backend Contract): Not UI work
- ❌ Phase 0.6 (Data Flow): Single method fix, no multi-layer flow
- ❌ Phase 0.7 (Conversation Design): Not conversational feature
- ❌ Phase 0.8 (Post-Completion): Read-only learning feature

---

## Phase 1: Apply Fix

### Tasks

1. **Fix line 698** - Change `intent.message` to `intent.original_message`
2. **Fix line 702** - Change `intent.session_id` to `None` (or remove parameter)
3. **Remove skip decorator** from test at line 243
4. **Run test** to verify fix

### Evidence Required

```bash
# Test must pass
python -m pytest tests/unit/services/test_llm_intent_classifier.py::TestLLMIntentClassifier::test_classification_storage_in_knowledge_graph -v
```

---

## Phase Z: Final Bookending & Handoff

### Success Criteria

- [x] Line 698 fixed: `intent.original_message`
- [x] Line 702 fixed: `session_id=None` or parameter removed
- [x] Skip decorator removed from test
- [x] Test passes with evidence
- [x] No regressions (other tests still pass)
- [x] GitHub issue updated with evidence

### STOP Conditions

- If other tests fail after fix → STOP and investigate
- If Intent class has been modified recently → STOP and verify approach

---

## Multi-Agent Coordination

**Not Required** - This is a single-agent, single-file fix. No subagents needed.

---

## Evidence Requirements

| What | How |
|------|-----|
| Fix applied | Show diff or file content |
| Test passes | pytest output showing PASSED |
| No regressions | Run related tests, show passing |

---

## Verification Gates

- [ ] Phase 1: Fix applied
- [ ] Phase 1: Test passes
- [ ] Phase 1: No regressions
- [ ] Phase Z: GitHub issue updated
- [ ] Phase Z: PM approval requested

---

*Gameplan version: 1.0*
*Based on gameplan-template.md v9.3*

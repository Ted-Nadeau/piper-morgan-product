# Gameplan: #743 - Fix test_pm039_patterns Container Initialization

**Issue**: #743 - BUG: test_pm039_patterns fails with ContainerNotInitializedError
**Date**: 2026-01-31
**Estimated Effort**: Small (test fixture fix)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Testing framework: pytest
- [x] Test file: `tests/unit/services/test_intent_coverage_pm039.py` (exists, verified)
- [x] Classifier: `services/intent_service/classifier.py` (IntentClassifier class)
- [x] Factory: `services/intent_service/llm_classifier_factory.py` (create_for_testing method)

**My understanding of the task**:
- Test uses `initialized_container` fixture but creates `IntentClassifier()` without DI
- Need to either use factory pattern or pass LLM service from container
- Test is currently skipped with reference to #743

### Part A.2: Work Characteristics Assessment

**Worktree Assessment:**
- [ ] Multiple agents will work in parallel - NO
- [ ] Task duration >30 minutes - NO (< 15 min)
- [ ] Multi-component work - NO (single test file)
- [ ] Exploratory/risky changes - NO (test fix only)

**Assessment:** ✅ **SKIP WORKTREE** - Single agent, test fixture fix, < 15 min estimate

### Part B: PM Verification

**This is a test fixture fix with clear root cause.**

**What exists:**
- `initialized_container` fixture in conftest.py
- `LLMClassifierFactory.create_for_testing()` method
- Test currently skipped at line 43

### Part C: Proceed/Revise Decision
- [x] **PROCEED** - Understanding is correct, fix is straightforward

---

## Phase 0: Initial Bookending - Investigation

### Required: Verify Factory Pattern

Before implementing, verify the factory pattern exists and understand its usage:

```bash
# Check factory method signature
grep -n "create_for_testing" services/intent_service/llm_classifier_factory.py

# Check how other tests use the factory
grep -rn "LLMClassifierFactory" tests/ --include="*.py" | head -10
```

---

## Phase 0.5-0.8: Not Applicable

- ❌ Phase 0.5 (Frontend-Backend Contract): Not UI work
- ❌ Phase 0.6 (Data Flow): Test fixture only
- ❌ Phase 0.7 (Conversation Design): Not conversational feature
- ❌ Phase 0.8 (Post-Completion): Test infrastructure

---

## Phase 1: Apply Fix

### Option Analysis

**Option 1: Use LLMClassifierFactory.create_for_testing()**
- Pros: Follows established pattern, handles all DI
- Cons: May need to verify it returns IntentClassifier (not LLMIntentClassifier)

**Option 2: Get LLM service from initialized_container**
- Pros: Uses fixture directly
- Cons: More manual wiring

**Recommended**: Option 1 if factory supports IntentClassifier, else Option 2

### Tasks

1. **Investigate** - Check what create_for_testing returns
2. **Fix test** - Update to use proper DI pattern
3. **Remove skip decorator**
4. **Run test** to verify fix

### Evidence Required

```bash
# Test must pass
python -m pytest tests/unit/services/test_intent_coverage_pm039.py -v
```

---

## Phase Z: Final Bookending & Handoff

### Success Criteria

- [ ] Skip decorator removed from test
- [ ] Test uses proper dependency injection (no singleton fallback)
- [ ] No deprecation warnings in test output
- [ ] Test passes with evidence
- [ ] GitHub issue updated with evidence

### STOP Conditions

- If factory doesn't support IntentClassifier → investigate alternative
- If test requires real LLM calls → verify that's the intent of the test

---

## Multi-Agent Coordination

**Not Required** - Single-agent test fix.

---

## Evidence Requirements

| What | How |
|------|-----|
| Fix applied | Show code change |
| Test passes | pytest output showing PASSED |
| No deprecation warnings | Clean test output |

---

*Gameplan version: 1.0*
*Based on gameplan-template.md v9.3*

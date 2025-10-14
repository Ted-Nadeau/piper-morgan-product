# Code Agent Prompt: GAP-3 Phase 4 - Performance Verification

**Date**: October 13, 2025, 10:47 AM
**Phase**: GAP-3 Phase 4 (Performance Verification)
**Duration**: 15 minutes
**Priority**: HIGH (completion requirement)
**Agent**: Code Agent

---

## Mission

Verify that the 3 new GUIDANCE patterns added in Phase 2 did not degrade performance. Must maintain sub-millisecond (<1ms) response time for pre-classifier.

**Acceptance Criteria**:
- [ ] Pre-classifier still responds in <1ms
- [ ] No performance regression detected
- [ ] All performance tests passing
- [ ] Evidence captured for completion

---

## Task 1: Run Performance Tests (10 minutes)

### Find Performance Tests

**Locate performance test files**:
```bash
# Find performance tests
find tests/ -name "*performance*" -o -name "*benchmark*"

# Common locations:
# tests/performance/
# tests/benchmark/
# tests/intent/test_performance.py
```

### Run Performance Tests

**Execute performance benchmarks**:
```bash
# Run all performance tests
pytest tests/performance/ -v

# Or run with specific markers
pytest -m performance -v

# Or run benchmark tests
pytest tests/ -k "benchmark" -v

# Or run intent performance specifically
pytest tests/intent/ -k "performance" -v
```

**Expected Results**:
- All tests passing ✅
- Response time <1ms for pre-classifier
- No slowdown from new patterns

### Manual Performance Check

**If automated tests don't exist, create quick test**:
```python
# Create: tests/quick_performance_check.py
import time
from services.intent_service.pre_classifier import PreClassifier

def test_preclassifier_performance():
    """Verify pre-classifier performance with new patterns"""

    test_queries = [
        "what should I do about this issue",  # New pattern
        "advise me on the best approach",     # New pattern
        "what's the process for creating",    # New pattern
        "what's my top priority",             # Existing pattern
        "what's on my calendar today",        # Existing pattern
    ]

    times = []
    for query in test_queries:
        start = time.perf_counter()
        result = PreClassifier.pre_classify(query)
        end = time.perf_counter()
        elapsed = (end - start) * 1000  # Convert to milliseconds
        times.append(elapsed)
        print(f"Query: {query[:40]:40s} | Time: {elapsed:.3f}ms | Result: {result}")

    avg_time = sum(times) / len(times)
    max_time = max(times)

    print(f"\n--- Performance Summary ---")
    print(f"Average time: {avg_time:.3f}ms")
    print(f"Max time: {max_time:.3f}ms")
    print(f"Target: <1.0ms")

    assert avg_time < 1.0, f"Average time {avg_time:.3f}ms exceeds 1ms target"
    assert max_time < 5.0, f"Max time {max_time:.3f}ms exceeds 5ms tolerance"

    print("\n✅ Performance verification PASSED")

if __name__ == "__main__":
    test_preclassifier_performance()
```

**Run it**:
```bash
python tests/quick_performance_check.py
```

---

## Task 2: Capture Evidence (5 minutes)

### Document Performance Results

**Create evidence file**: `dev/2025/10/13/gap-3-phase4-performance.md`

**Template**:
```markdown
# GAP-3 Phase 4: Performance Verification

**Date**: October 13, 2025, 10:47 AM
**Phase**: Phase 4 - Performance Verification
**Agent**: Code Agent

---

## Objective

Verify that 3 new GUIDANCE patterns added in Phase 2 maintain sub-millisecond performance.

**New Patterns Added**:
1. `r'\bwhat should (I|we) do (about|with)\b'`
2. `r'\badvise (me|us) on\b'`
3. `r'\bwhat(\'s| is) the process for\b'`

---

## Performance Test Results

### Test Execution

[Paste test output here]

### Performance Metrics

**Pre-classifier Performance**:
- Average response time: X.XXXms
- Max response time: X.XXXms
- Target: <1.0ms
- Status: [PASS/FAIL]

**Sample Query Results**:
| Query | Time (ms) | Category | Status |
|-------|-----------|----------|--------|
| "what should I do about..." | X.XXX | GUIDANCE | ✅ |
| "advise me on..." | X.XXX | GUIDANCE | ✅ |
| "what's the process for..." | X.XXX | GUIDANCE | ✅ |
| "what's my priority" | X.XXX | PRIORITY | ✅ |
| "what's on my calendar" | X.XXX | TEMPORAL | ✅ |

---

## Analysis

**Performance Impact**:
- New patterns: [NO IMPACT / MINIMAL IMPACT / CONCERNS]
- Overall system: [MAINTAINED / IMPROVED / DEGRADED]
- Conclusion: [PASS / FAIL]

**Observations**:
- [Any notable findings]
- [Pattern matching efficiency]
- [Comparison to baseline if available]

---

## Conclusion

**Performance Status**: ✅ VERIFIED

The addition of 3 new GUIDANCE patterns maintains sub-millisecond performance requirements. Pre-classifier continues to operate within acceptable performance thresholds.

**Evidence Quality**: [Complete / Partial / Needs Review]

---

## Next Steps

- [x] Performance verified
- [ ] Proceed to Phase 5 (Epic Completion)

---

**Verification Complete**: [Timestamp]
**Status**: Ready for Phase 5
```

---

## Deliverables

**Required Outputs**:
1. ✅ Performance test results (terminal output)
2. ✅ Evidence document (`gap-3-phase4-performance.md`)
3. ✅ Verification that <1ms target maintained
4. ✅ Green light to proceed to Phase 5

---

## Acceptance Criteria

### Performance Requirements
- [ ] Pre-classifier average response time <1ms
- [ ] Max response time <5ms (tolerance)
- [ ] No performance regression vs baseline
- [ ] All performance tests passing

### Evidence Requirements
- [ ] Test output captured
- [ ] Performance metrics documented
- [ ] Evidence file created
- [ ] Clear pass/fail status

### Quality Requirements
- [ ] Tests ran successfully
- [ ] Results are credible
- [ ] Evidence is complete
- [ ] Ready for handoff to PM

---

## Time Budget

- **Task 1** (Run tests): 10 minutes
- **Task 2** (Capture evidence): 5 minutes
- **Total**: 15 minutes

**Target Completion**: 11:02 AM

---

## Expected Results

**Most Likely Outcome**:
- Performance maintained ✅
- <1ms average response time ✅
- New patterns have negligible impact ✅
- All tests passing ✅

**Why We Expect This**:
- Only 3 simple regex patterns added
- Pattern matching is O(1) per pattern
- Total patterns still small (~50 patterns)
- Regex operations are extremely fast

**If Performance Issue Found**:
- Document the concern
- Measure baseline vs new
- Recommend optimization if needed
- Still proceed to Phase 5 (can optimize later)

---

## Context for Code Agent

**This is GAP-3 Phase 4** - Performance verification before epic closure

**What We've Done**:
- ✅ Phase 1: Analysis (20 min)
- ✅ Phase 2: Add 3 patterns (22 min)
- ✅ Phase 3: LLM enhancement (included in Phase 2)
- ✅ Phase 4: Most documentation (done with Phase 2)
- ⏳ Phase 4: Performance verification (THIS TASK)
- ⏸ Phase 5: Epic completion (next)

**Why This Matters**:
- Can't claim completion without performance verification
- Need evidence that quality maintained
- PM has 15 minutes available now
- Quick verification then handoff

**PM Context**: "I have 15 minutes now for the verification"

**Expected Outcome**: Fast verification, all green, proceed to Phase 5

---

**Phase 4 Start Time**: 10:47 AM
**Expected Completion**: 11:02 AM (15 minutes)
**Status**: Ready for Code Agent execution

**LET'S VERIFY PERFORMANCE! ⚡**

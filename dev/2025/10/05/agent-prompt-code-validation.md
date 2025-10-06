# Prompt for Claude Code: GREAT-4A Validation Testing

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus (GREAT-4A validation)
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## 🚨 INFRASTRUCTURE VERIFICATION (ALREADY COMPLETE)

**Phase -1 findings confirm:**
- ✅ Intent service exists at `services/intent_service/`
- ✅ Categories TEMPORAL, STATUS, PRIORITY already defined
- ✅ Patterns exist in `pre_classifier.py`
- ✅ Handlers exist in `canonical_handlers.py`
- ✅ System test confirms: "What day is it?" → TEMPORAL @ 1.0 confidence

**Your task is VALIDATION, not implementation.**

## Session Log Management

Create session log at: `dev/2025/10/05/2025-10-05-1345-prog-code-log.md`

Update throughout work with timestamped entries showing evidence.

## Mission

**Validate that TEMPORAL, STATUS, and PRIORITY intent categories work correctly** through comprehensive testing of all canonical queries and establishment of test coverage baseline.

**Scope Boundaries**:
- This prompt covers: Comprehensive testing + test coverage analysis
- NOT in scope: Metrics (Cursor), Documentation (Cursor)
- You are working in parallel with Cursor agent

---

## Context

- **GitHub Issue**: #205 (CORE-GREAT-4A: Intent Foundation & Categories)
- **Current State**: Categories exist and basic test confirms functionality
- **Target State**: All 25 canonical queries tested, coverage >80%, test gaps identified
- **Dependencies**: None - existing code only
- **User Data Risk**: None - read-only testing
- **Infrastructure Verified**: Yes - Phase -1 complete

---

## Evidence Requirements

For EVERY claim:
- **"Test passes"** → Show pytest output with pass counts
- **"Query classifies correctly"** → Show actual classification result
- **"Coverage measured"** → Show pytest-cov output
- **"Gap identified"** → Show specific missing test case
- **"Pattern works"** → Show test input and output

NO assumptions - only verified facts with terminal evidence.

---

## Constraints & Requirements

1. **Read-only testing**: No code modifications in this phase
2. **All 25 canonical queries**: From attached reference list
3. **Evidence for each query**: Classification result with confidence
4. **Coverage analysis**: Use pytest --cov for baseline
5. **Gap identification**: Document what tests are missing
6. **Async handling**: Use `asyncio.run()` for classifier calls
7. **Python 3**: System uses python3 (not python)

---

## Multi-Agent Coordination

**Cursor Agent is handling**: Baseline metrics + documentation

**Your coordination points**:
- Share test results via GitHub issue updates
- After Phase 1 complete, update issue with findings
- Before Phase 3, check Cursor's metric findings
- Cross-validate at Phase Z

---

## Phase 1: Comprehensive Testing (PRIORITY TASK)

### Step 1: Test All Canonical Queries

Use the 25 canonical queries from the reference list attached to this session.

Create test script: `dev/2025/10/05/test_canonical_queries.py`

```python
import asyncio
from services.intent_service.classifier import classifier
from services.shared_types import IntentCategory

CANONICAL_QUERIES = [
    # TEMPORAL category (10 queries from reference)
    ("What day is it?", IntentCategory.TEMPORAL),
    ("What's today's date?", IntentCategory.TEMPORAL),
    ("What day of the week is it?", IntentCategory.TEMPORAL),
    ("What's the current date?", IntentCategory.TEMPORAL),
    ("Tell me the date", IntentCategory.TEMPORAL),
    ("What did we accomplish yesterday?", IntentCategory.TEMPORAL),
    ("What did we do yesterday?", IntentCategory.TEMPORAL),
    ("What happened yesterday?", IntentCategory.TEMPORAL),
    ("What's on the agenda for today?", IntentCategory.TEMPORAL),
    ("What should I work on today?", IntentCategory.TEMPORAL),

    # STATUS category (5 queries from reference)
    ("What am I working on?", IntentCategory.STATUS),
    ("Show me current projects", IntentCategory.STATUS),
    ("What projects are we working on?", IntentCategory.STATUS),
    ("Give me a project overview", IntentCategory.STATUS),
    ("What's the status of project X?", IntentCategory.STATUS),

    # PRIORITY category (5 queries from reference)
    ("What's my top priority?", IntentCategory.PRIORITY),
    ("What should I focus on today?", IntentCategory.PRIORITY),
    ("What's most important today?", IntentCategory.PRIORITY),
    ("What needs my attention?", IntentCategory.PRIORITY),
    ("Which project should I focus on?", IntentCategory.PRIORITY),

    # Add more from the full list of 25...
]

async def test_canonical_queries():
    """Test all canonical queries and report results."""
    results = []

    for query, expected_category in CANONICAL_QUERIES:
        try:
            result = await classifier.classify(query)
            passed = result.category == expected_category
            confidence = result.confidence

            results.append({
                "query": query,
                "expected": expected_category.value,
                "actual": result.category.value,
                "confidence": confidence,
                "passed": passed
            })

            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} | {query[:40]:40} | {result.category.value:12} | {confidence:.2f}")

        except Exception as e:
            results.append({
                "query": query,
                "expected": expected_category.value,
                "error": str(e),
                "passed": False
            })
            print(f"❌ ERROR | {query[:40]:40} | {str(e)[:40]}")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.get("passed", False))
    failed = total - passed

    print(f"\n{'='*80}")
    print(f"CANONICAL QUERY TEST RESULTS")
    print(f"{'='*80}")
    print(f"Total:  {total}")
    print(f"Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"Failed: {failed} ({failed/total*100:.1f}%)")

    # Show failures
    if failed > 0:
        print(f"\nFailed Queries:")
        for r in results:
            if not r.get("passed", False):
                print(f"  - {r['query']}")
                if 'error' in r:
                    print(f"    Error: {r['error']}")
                else:
                    print(f"    Expected: {r['expected']}, Got: {r['actual']}")

    return results

if __name__ == "__main__":
    results = asyncio.run(test_canonical_queries())
```

**Expected outcome**: Test results showing pass/fail for each canonical query

**Validation**: Run the script and capture full output

**Evidence**: Terminal output showing all test results

### Step 2: Analyze Confidence Scores

From test results, analyze confidence patterns:

```python
# Add to test script
def analyze_confidence(results):
    """Analyze confidence score patterns."""
    by_category = {}

    for r in results:
        if 'confidence' in r:
            cat = r['expected']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(r['confidence'])

    print(f"\nConfidence Score Analysis:")
    print(f"{'='*60}")
    for category, scores in by_category.items():
        avg = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)
        print(f"{category:12} | Avg: {avg:.3f} | Min: {min_score:.3f} | Max: {max_score:.3f}")

        # Flag if any below 0.8 threshold
        low_conf = [s for s in scores if s < 0.8]
        if low_conf:
            print(f"  ⚠️  {len(low_conf)} queries below 0.8 confidence threshold")
```

**Expected outcome**: Confidence analysis by category

**Validation**: Average confidence >0.8 for all categories

**Evidence**: Analysis output showing confidence metrics

---

## Phase 3: Test Coverage Analysis

### Step 1: Check Existing Test Coverage

```bash
# Run coverage on intent service
pytest tests/services/test_intent*.py --cov=services.intent_service --cov-report=term-missing

# Capture output showing coverage percentage
```

**Expected outcome**: Coverage report showing current baseline

**Validation**: Document exact coverage percentage

**Evidence**: Full pytest-cov output

### Step 2: Identify Test Gaps

Look for:
1. Which files have <80% coverage?
2. Which functions are untested?
3. Are new categories (TEMPORAL, STATUS, PRIORITY) fully covered?
4. Edge cases missing?

Create gap report: `dev/2025/10/05/test_coverage_gaps.md`

```markdown
# Test Coverage Gaps Report

## Current Coverage
- services/intent_service/classifier.py: XX%
- services/intent_service/pre_classifier.py: XX%
- services/intent_service/canonical_handlers.py: XX%

## Untested Functions
- [ ] function_name in file.py (lines XX-XX)
- [ ] another_function in file.py (lines XX-XX)

## Missing Test Cases
- [ ] TEMPORAL category edge cases
- [ ] STATUS category error handling
- [ ] PRIORITY category confidence boundary

## Recommendation
Need XX additional test cases to reach >80% coverage
```

**Expected outcome**: Documented gap analysis

**Validation**: Specific line numbers and functions identified

**Evidence**: Gap report with evidence links

---

## Success Criteria

- [ ] All 25 canonical queries tested (show results)
- [ ] Confidence scores analyzed (show analysis)
- [ ] Coverage baseline established (show %)
- [ ] Test gaps identified (show report)
- [ ] GitHub issue updated with findings
- [ ] Evidence provided for each claim
- [ ] Cross-validation ready for Cursor

---

## Deliverables

1. **Test Script**: `test_canonical_queries.py` with results
2. **Coverage Report**: pytest output showing baseline
3. **Gap Analysis**: `test_coverage_gaps.md`
4. **Evidence Package**: All terminal outputs captured
5. **GitHub Update**: Issue #205 updated with test results

---

## Cross-Validation Preparation

Leave clear evidence for Cursor agent:
- Test script location and how to run it
- Coverage commands used
- Gap report location
- Any patterns observed
- Recommendations for Phase 3 test creation

---

## Self-Check Before Claiming Complete

1. Did I test ALL 25 canonical queries?
2. Do I have confidence scores for each?
3. Is coverage percentage documented with evidence?
4. Are test gaps specifically identified?
5. Can Cursor agent verify my findings independently?
6. Did I update GitHub issue with results?

If any answer is no, continue working.

---

## Example Evidence Format

```bash
# Show test execution
$ python3 dev/2025/10/05/test_canonical_queries.py
✅ PASS | What day is it? | TEMPORAL | 1.00
✅ PASS | What's today's date? | TEMPORAL | 1.00
...
================================
CANONICAL QUERY TEST RESULTS
================================
Total:  25
Passed: 23 (92.0%)
Failed: 2 (8.0%)

# Show coverage
$ pytest tests/services/test_intent*.py --cov=services.intent_service
==================== test session starts ====================
collected 42 items

tests/services/test_intent_classification.py ...........
Coverage:
  services/intent_service/__init__.py         100%
  services/intent_service/classifier.py        87%
  services/intent_service/pre_classifier.py    92%
  services/intent_service/canonical_handlers.py 78%
==================== 42 passed in 2.34s ====================
```

---

## Related Documentation
- `canonical-queries-list.md` - Full query reference
- `services/intent_service/pre_classifier.py` - Pattern definitions
- `services/intent_service/canonical_handlers.py` - Handler implementations
- `tests/services/test_intent*.py` - Existing tests

---

## STOP Conditions

Stop and escalate if:
- [ ] Cannot import classifier module
- [ ] Test infrastructure doesn't exist
- [ ] Coverage tools not available
- [ ] Cannot access canonical query list
- [ ] System throws unexpected errors
- [ ] Need to modify code (out of scope)

---

**Remember**: You are VALIDATING existing functionality, not implementing new features. Focus on thorough testing and evidence collection.

---

*Template Version: 9.0*
*Task: Validation Testing for GREAT-4A*
*Estimated Effort: Medium (2-3 hours)*

# Prompt for Cursor Agent: GREAT-4A Metrics & Documentation

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

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

**Your task is METRICS & DOCUMENTATION, not implementation.**

## Session Log Management

Create session log at: `dev/2025/10/05/2025-10-05-1345-prog-cursor-log.md`

Update throughout work with timestamped entries showing evidence.

## Mission

**Establish baseline performance metrics and create comprehensive documentation** for TEMPORAL, STATUS, and PRIORITY intent categories to support future optimization and troubleshooting.

**Scope Boundaries**:
- This prompt covers: Baseline metrics + documentation creation
- NOT in scope: Testing (Code), Test coverage (Code)
- You are working in parallel with Code agent

---

## Context

- **GitHub Issue**: #205 (CORE-GREAT-4A: Intent Foundation & Categories)
- **Current State**: Categories exist and basic test confirms functionality
- **Target State**: Metrics documented, usage guide created, patterns cataloged
- **Dependencies**: Code agent's test results (coordinate at Phase Z)
- **User Data Risk**: None - read-only analysis
- **Infrastructure Verified**: Yes - Phase -1 complete

---

## Evidence Requirements

For EVERY claim:
- **"Processing time measured"** → Show timing output
- **"Pattern documented"** → Show actual pattern in doc
- **"Handler described"** → Show code reference
- **"Metric established"** → Show measurement data
- **"Documentation complete"** → Show file created

NO assumptions - only verified facts with file evidence.

---

## Constraints & Requirements

1. **Read-only analysis**: No code modifications
2. **All 3 categories**: TEMPORAL, STATUS, PRIORITY
3. **Exact file paths**: Document with precision
4. **Markdown format**: All documentation in .md
5. **Async handling**: Use `asyncio.run()` for timing tests
6. **Python 3**: System uses python3 (not python)
7. **Cross-reference Code**: Use Code's test results

---

## Multi-Agent Coordination

**Code Agent is handling**: Comprehensive testing + test coverage

**Your coordination points**:
- After Phase 2 complete, share metrics via GitHub issue
- Before Phase 4, review Code's test findings
- Cross-validate at Phase Z

---

## Phase 2: Baseline Metrics Establishment

### Step 1: Measure Processing Times

Create benchmark script: `dev/2025/10/05/benchmark_intent_classification.py`

```python
import asyncio
import time
from statistics import mean, stdev, median
from services.intent_service.classifier import classifier

async def benchmark_category(category_name, test_queries):
    """Benchmark classification performance for a category."""
    times = []
    confidences = []

    print(f"\nBenchmarking {category_name} category:")
    print(f"{'='*60}")

    for query in test_queries:
        start = time.perf_counter()
        result = await classifier.classify(query)
        elapsed = time.perf_counter() - start

        times.append(elapsed * 1000)  # Convert to ms
        confidences.append(result.confidence)

        print(f"  {elapsed*1000:6.2f}ms | {result.confidence:.3f} | {query[:40]}")

    return {
        "category": category_name,
        "num_queries": len(test_queries),
        "avg_time_ms": mean(times),
        "median_time_ms": median(times),
        "std_time_ms": stdev(times) if len(times) > 1 else 0,
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "avg_confidence": mean(confidences),
        "min_confidence": min(confidences),
        "max_confidence": max(confidences)
    }

async def run_benchmarks():
    """Run benchmarks for all three categories."""

    temporal_queries = [
        "What day is it?",
        "What's today's date?",
        "What did we do yesterday?",
        "What's on the agenda for today?",
        "When was the last time we worked on this?"
    ]

    status_queries = [
        "What am I working on?",
        "Show me current projects",
        "What projects are we working on?",
        "What's the status of project X?",
        "Where are we in the project lifecycle?"
    ]

    priority_queries = [
        "What's my top priority?",
        "What should I focus on today?",
        "What's most important today?",
        "Which project should I focus on?",
        "What needs my attention?"
    ]

    results = {}
    results['temporal'] = await benchmark_category("TEMPORAL", temporal_queries)
    results['status'] = await benchmark_category("STATUS", status_queries)
    results['priority'] = await benchmark_category("PRIORITY", priority_queries)

    # Summary
    print(f"\n{'='*80}")
    print(f"BASELINE METRICS SUMMARY")
    print(f"{'='*80}")
    print(f"{'Category':<12} | {'Avg Time':>10} | {'Median':>10} | {'Avg Conf':>10}")
    print(f"{'-'*12}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")

    for cat, data in results.items():
        print(f"{cat:<12} | {data['avg_time_ms']:>9.2f}ms | {data['median_time_ms']:>9.2f}ms | {data['avg_confidence']:>9.3f}")

    # Check against targets
    print(f"\n{'='*80}")
    print(f"TARGET VALIDATION")
    print(f"{'='*80}")
    all_pass = True
    for cat, data in results.items():
        time_ok = data['avg_time_ms'] < 100
        conf_ok = data['avg_confidence'] > 0.8
        status = "✅ PASS" if (time_ok and conf_ok) else "❌ FAIL"
        print(f"{status} | {cat:<12} | Time: {time_ok} (<100ms) | Conf: {conf_ok} (>0.8)")
        all_pass = all_pass and time_ok and conf_ok

    return results, all_pass

if __name__ == "__main__":
    results, passed = asyncio.run(run_benchmarks())

    # Save results to JSON for documentation
    import json
    with open("dev/2025/10/05/baseline_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nMetrics saved to: dev/2025/10/05/baseline_metrics.json")
    print(f"Overall result: {'✅ ALL TARGETS MET' if passed else '❌ SOME TARGETS MISSED'}")
```

**Expected outcome**: Baseline metrics for all 3 categories

**Validation**: Avg time <100ms, avg confidence >0.8

**Evidence**: Terminal output + baseline_metrics.json file

### Step 2: Document Baseline in Markdown

Create: `dev/2025/10/05/intent-baseline-metrics.md`

```markdown
# Intent Classification Baseline Metrics
**Date**: October 5, 2025
**Epic**: GREAT-4A - Intent Foundation & Categories
**Measured By**: Cursor Agent

## Summary

Baseline performance metrics for TEMPORAL, STATUS, and PRIORITY intent categories.

## Performance Metrics

### TEMPORAL Category
- **Average Time**: XX.XXms
- **Median Time**: XX.XXms
- **Min/Max**: XX.XX / XX.XXms
- **Average Confidence**: 0.XXX
- **Target Met**: ✅/❌ (<100ms, >0.8 confidence)

### STATUS Category
- **Average Time**: XX.XXms
- **Median Time**: XX.XXms
- **Min/Max**: XX.XX / XX.XXms
- **Average Confidence**: 0.XXX
- **Target Met**: ✅/❌

### PRIORITY Category
- **Average Time**: XX.XXms
- **Median Time**: XX.XXms
- **Min/Max**: XX.XX / XX.XXms
- **Average Confidence**: 0.XXX
- **Target Met**: ✅/❌

## Test Methodology

- 5 canonical queries per category
- Timing via time.perf_counter()
- Fresh classifier instance per test
- Python 3.9 on macOS

## Observations

[Document any patterns noticed, performance anomalies, etc.]

## Recommendations

[Based on metrics, what should be optimized?]
```

**Expected outcome**: Complete metrics documentation

**Validation**: All sections filled with real data

**Evidence**: Show file creation with `cat` output

---

## Phase 4: Documentation Creation

### Step 1: Pattern Catalog

Create: `dev/2025/10/05/intent-pattern-catalog.md`

Document all patterns found in `pre_classifier.py`:

```markdown
# Intent Pattern Catalog
**Epic**: GREAT-4A
**Source**: services/intent_service/pre_classifier.py

## TEMPORAL Patterns

Pattern matching for time/date/schedule queries.

**Regex Patterns**:
- `\bwhat day is it\b` - Current day query
- `\bwhat'?s the date\b` - Current date query
- ... [document ALL patterns found]

**Example Queries**:
- "What day is it?"
- "What's today's date?"
- ... [list examples]

**Handler**: `get_current_time` action
**Confidence**: 1.0 (pre-classifier match)

## STATUS Patterns

Pattern matching for project/work status queries.

**Regex Patterns**:
- `\bwhat am i working on\b` - Current work query
- ... [document ALL patterns found]

**Example Queries**:
- "What am I working on?"
- ... [list examples]

**Handler**: `get_project_status` action
**Confidence**: 1.0 (pre-classifier match)

## PRIORITY Patterns

Pattern matching for priority/focus queries.

**Regex Patterns**:
- `\bwhat'?s my top priority\b` - Priority query
- ... [document ALL patterns found]

**Example Queries**:
- "What's my top priority?"
- ... [list examples]

**Handler**: `get_top_priority` action
**Confidence**: 1.0 (pre-classifier match)

## Implementation Notes

**File Location**: `services/intent_service/pre_classifier.py`
**Matching Logic**: Regex with case-insensitive matching
**Fallback**: If no pattern matches, falls through to LLM classifier
```

**Expected outcome**: Complete pattern documentation

**Validation**: All patterns from code documented

**Evidence**: Show grep output confirming patterns match

### Step 2: Category Usage Guide

Create: `dev/2025/10/05/intent-category-usage-guide.md`

```markdown
# Intent Category Usage Guide
**For**: Developers adding new patterns or queries

## TEMPORAL Category

**Purpose**: Time, date, schedule, and temporal reference queries

**When to Use**:
- User asks about current date/time
- User asks about past events ("yesterday", "last week")
- User asks about future schedule ("today's agenda", "tomorrow")
- Temporal comparisons ("how long ago", "when did")

**Pattern Structure**:
Regex patterns matching temporal keywords

**Handler Behavior**:
- Returns current date/time
- May integrate with calendar
- Provides contextual temporal information

**Example Queries**:
- "What day is it?"
- "What's my schedule today?"
- "When was the last time we worked on this?"

**Adding New Patterns**:
1. Add regex to TEMPORAL_PATTERNS in pre_classifier.py
2. Test with canonical query format
3. Verify confidence >0.8
4. Update this documentation

## STATUS Category

[Similar detailed structure for STATUS]

## PRIORITY Category

[Similar detailed structure for PRIORITY]

## Best Practices

1. Keep patterns specific but flexible
2. Test edge cases
3. Maintain >0.8 confidence threshold
4. Document pattern rationale
5. Cross-reference with canonical queries

## Troubleshooting

**Low Confidence**:
- Pattern may be too broad
- Check for pattern conflicts
- Verify regex syntax

**Wrong Category**:
- Pattern overlaps with another category
- Add negative lookahead to patterns
- Refine specificity
```

**Expected outcome**: Developer-friendly usage guide

**Validation**: Covers all 3 categories thoroughly

**Evidence**: Show file exists with complete content

### Step 3: Cross-Reference ADRs

Check if ADRs need updates:

```bash
# Find relevant ADRs
grep -l "intent\|classification" docs/internal/architecture/current/adrs/*.md

# Review ADR-032 (Intent Classification Universal Entry)
# Review ADR-003 (Intent Classifier Enhancement)
```

Create: `dev/2025/10/05/adr-update-recommendations.md`

```markdown
# ADR Update Recommendations

## ADR-032: Intent Classification Universal Entry

**Current Status**: [Briefly describe what ADR says]

**Proposed Updates**:
- Document that TEMPORAL, STATUS, PRIORITY categories now validated
- Add baseline metrics reference
- Note pattern catalog location

**Rationale**: ADR should reflect current validated state

## ADR-003: Intent Classifier Enhancement

**Current Status**: [Briefly describe]

**Proposed Updates**: [If any needed]
```

**Expected outcome**: Recommendations for ADR updates

**Validation**: References to specific ADRs

**Evidence**: Show ADR content review

---

## Success Criteria

- [ ] Baseline metrics established (show data)
- [ ] Performance targets validated (<100ms, >0.8)
- [ ] Pattern catalog created (show file)
- [ ] Usage guide created (show file)
- [ ] ADR review complete (show recommendations)
- [ ] GitHub issue updated with metrics
- [ ] Evidence provided for all claims
- [ ] Cross-validation ready for Code

---

## Deliverables

1. **Metrics Script**: `benchmark_intent_classification.py`
2. **Metrics Data**: `baseline_metrics.json`
3. **Metrics Doc**: `intent-baseline-metrics.md`
4. **Pattern Catalog**: `intent-pattern-catalog.md`
5. **Usage Guide**: `intent-category-usage-guide.md`
6. **ADR Review**: `adr-update-recommendations.md`
7. **GitHub Update**: Issue #205 updated with metrics

---

## Cross-Validation Preparation

Leave clear evidence for Code agent:
- Metrics script location and how to run
- Benchmark results file location
- Documentation file locations
- Any performance observations
- Recommendations based on metrics

---

## Self-Check Before Claiming Complete

1. Did I measure all 3 categories?
2. Are metrics within target ranges?
3. Is pattern catalog complete and accurate?
4. Is usage guide helpful for developers?
5. Did I review relevant ADRs?
6. Can Code agent verify my metrics independently?
7. Did I update GitHub issue with findings?

If any answer is no, continue working.

---

## Example Evidence Format

```bash
# Show metrics execution
$ python3 dev/2025/10/05/benchmark_intent_classification.py

Benchmarking TEMPORAL category:
============================================================
  23.45ms | 1.000 | What day is it?
  21.78ms | 1.000 | What's today's date?
...

BASELINE METRICS SUMMARY
============================================================
Category     |   Avg Time |     Median |   Avg Conf
-------------+------------+------------+-----------
temporal     |     22.51ms |     22.00ms |      1.000
status       |     24.33ms |     23.50ms |      1.000
priority     |     23.89ms |     23.25ms |      1.000

TARGET VALIDATION
============================================================
✅ PASS | temporal     | Time: True (<100ms) | Conf: True (>0.8)
✅ PASS | status       | Time: True (<100ms) | Conf: True (>0.8)
✅ PASS | priority     | Time: True (<100ms) | Conf: True (>0.8)

# Show documentation created
$ ls -la dev/2025/10/05/intent*.md
-rw-r--r-- intent-baseline-metrics.md
-rw-r--r-- intent-pattern-catalog.md
-rw-r--r-- intent-category-usage-guide.md

$ cat dev/2025/10/05/intent-pattern-catalog.md | head -20
# Intent Pattern Catalog
**Epic**: GREAT-4A
...
```

---

## Related Documentation
- `services/intent_service/pre_classifier.py` - Pattern source
- `services/intent_service/canonical_handlers.py` - Handler implementations
- `docs/internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md`
- `docs/internal/architecture/current/adrs/adr-003-intent-classifier-enhancement.md`

---

## STOP Conditions

Stop and escalate if:
- [ ] Cannot import classifier module
- [ ] Timing measurements fail
- [ ] Cannot find pattern definitions
- [ ] ADRs don't exist at expected paths
- [ ] Need to modify code (out of scope)

---

**Remember**: You are DOCUMENTING existing functionality, not implementing new features. Focus on thorough metrics and clear documentation.

---

*Template Version: 9.0*
*Task: Metrics & Documentation for GREAT-4A*
*Estimated Effort: Medium (2-3 hours)*

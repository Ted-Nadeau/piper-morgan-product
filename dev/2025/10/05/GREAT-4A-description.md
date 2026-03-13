# GREAT-4A: Intent Foundation & Categories

## Context
First sub-epic of GREAT-4. Establishes foundation by adding missing intent categories and fixing pattern loading issues.

## Background
Current intent classifier missing TEMPORAL, STATUS, and PRIORITY categories, causing "Failed to process intent" errors on canonical queries like "What day is it?" and "What am I working on?". Pattern loading may have issues that need investigation and repair.

## Scope
1. **Add Missing Categories**
   - TEMPORAL (time/date/schedule queries)
   - STATUS (current work/project queries)
   - PRIORITY (focus/importance queries)
   - Update enum definitions

2. **Fix Pattern Loading**
   - Investigate current loading mechanism
   - Verify patterns load correctly
   - Add logging for debugging
   - Implement error handling

3. **Create Test Suite**
   - Canonical query tests (5+ queries)
   - Pattern coverage tests
   - Edge case handling
   - Confidence scoring validation

4. **Establish Baselines**
   - Processing time metrics
   - Classification accuracy
   - Error rates
   - Memory usage

## Acceptance Criteria
- [ ] TEMPORAL category added with 10+ patterns
- [ ] STATUS category added with 10+ patterns
- [ ] PRIORITY category added with 10+ patterns
- [ ] Pattern loading mechanism verified working
- [ ] All 5 canonical queries classify correctly:
  - "What day is it?" → TEMPORAL
  - "What's my schedule today?" → TEMPORAL
  - "What am I working on?" → STATUS
  - "Show me current projects" → STATUS
  - "What's my top priority?" → PRIORITY
- [ ] Confidence scores >0.8 for canonical queries
- [ ] Test suite with 20+ tests passing
- [ ] Baseline metrics documented
- [ ] No regressions in existing intent classification

## Success Validation
```bash
# Run canonical query tests
pytest tests/intent/test_canonical_queries.py -v
# All 5 queries pass with correct categories

# Check confidence scores
python scripts/check_intent_confidence.py
# All canonical queries >0.8 confidence

# Verify pattern loading
python -c "from services.intent_service import IntentClassifier; c = IntentClassifier(); print(c.patterns_loaded)"
# Shows all patterns loaded

# Run baseline benchmarks
python scripts/benchmark_intent_baseline.py
# Documents current performance
```

## Anti-80% Check
```
Task         | Added | Tested | Working | Documented
------------ | ----- | ------ | ------- | ----------
TEMPORAL     | [ ]   | [ ]    | [ ]     | [ ]
STATUS       | [ ]   | [ ]    | [ ]     | [ ]
PRIORITY     | [ ]   | [ ]    | [ ]     | [ ]
Patterns     | [ ]   | [ ]    | [ ]     | [ ]
Loading      | [ ]   | [ ]    | [ ]     | [ ]
Tests        | [ ]   | [ ]    | [ ]     | [ ]
Baselines    | [ ]   | [ ]    | [ ]     | [ ]
TOTAL: 0/28 checkmarks = 0% (Must reach 100%)
```

## Time Estimate
4-6 hours

## Gameplan Available
See `gameplan-GREAT-4A.md` for detailed implementation plan.

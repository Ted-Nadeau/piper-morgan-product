# Gameplan: Performance & Coverage Enforcement Implementation

**Date**: September 25, 2025
**Issue**: GREAT-1C (#187) - Locking Phase items
**Architect**: Claude Opus 4.1
**Lead Developer**: [To be assigned]

---

## Mission: Implement Enforcement Mechanisms

### Specific Checkboxes to Address
1. ☐ Performance regression test alerts on degradation
2. ☐ Required test coverage for orchestration module

These enforcement mechanisms ensure QueryRouter gains cannot be lost to future changes.

---

## Infrastructure Verification Checkpoint

### Expected Infrastructure
```yaml
CI/CD System:
- Location: .github/workflows/ or similar
- Current tests: Already running (per yesterday's fix)
- Performance tests: Exist in tests/performance/
- Coverage reports: Generated but not enforced

Coverage Tools:
- pytest-cov installed
- Coverage reports generated
- No threshold enforcement yet
```

### PM Verification Required
```bash
# Check CI configuration
ls -la .github/workflows/
cat .github/workflows/*.yml | grep -A5 -B5 "pytest"

# Check current coverage for orchestration
PYTHONPATH=. python -m pytest tests/ --cov=services/orchestration --cov-report=term | tail -20

# Check if performance tests have timing assertions
grep -r "assert.*time\|benchmark" tests/performance/ --include="*.py"
```

---

## Phase 1: Performance Regression Alerts (45 min)

### Both Agents - Implement Realistic Performance Gates

#### 1A. Assess Current Performance Reality
```bash
# Run performance tests and capture actual times
PYTHONPATH=. python -m pytest tests/performance/ -v --tb=short

# Document actual performance baselines:
# - QueryRouter initialization: Expected <X ms
# - LLM classification: Expected <Y seconds
# - Full orchestration flow: Expected <Z seconds
```

#### 1B. Implement Performance Enforcement

**Based on PM's guidance**: Use realistic thresholds, not arbitrary ones.

```yaml
# In .github/workflows/ci.yml or tests.yml

- name: Run Performance Tests with Regression Detection
  run: |
    # Option 1: Using pytest-benchmark
    pytest tests/performance/ --benchmark-only --benchmark-compare=baseline.json --benchmark-compare-fail=110%

    # Option 2: Custom timing assertions
    PERFORMANCE_REGRESSION_CHECK=true pytest tests/performance/ -v

    # Option 3: Separate performance gate job
    python scripts/check_performance_regression.py --threshold=3.0
```

#### 1C. Create Performance Baseline

```python
# scripts/performance_baseline.py
"""
Store current performance as baseline for regression detection.
Not aspirational targets, but actual current performance.
"""

PERFORMANCE_BASELINES = {
    "queryrouter_init": 50,  # milliseconds
    "llm_classification": 2500,  # milliseconds (realistic for LLM)
    "full_orchestration": 3000,  # milliseconds
}

def check_regression(test_name: str, actual_time: float) -> bool:
    """Allow 10% degradation from baseline"""
    baseline = PERFORMANCE_BASELINES.get(test_name)
    if not baseline:
        return True  # No baseline, pass by default

    threshold = baseline * 1.1  # 10% tolerance
    return actual_time <= threshold
```

### Cross-Validation
- Both agents verify performance tests run in CI
- Confirm thresholds are realistic, not aspirational
- Ensure failures provide actionable feedback

---

## Phase 2: Coverage Enforcement Strategy (45 min)

### Deploy: Code for Analysis, Cursor for Implementation

#### 2A. Analyze Current Coverage Reality

**Code Instructions**:
```markdown
Analyze orchestration module coverage:

1. Generate detailed coverage report:
   ```bash
   PYTHONPATH=. python -m pytest tests/ --cov=services/orchestration --cov-report=html --cov-report=term-missing
   ```

2. Identify coverage gaps:
   - Which QueryRouter files have low coverage?
   - Which are legacy files not part of current work?
   - What's the coverage for ACTIVE QueryRouter code specifically?

3. Categorize files:
   - Core QueryRouter files (must have high coverage)
   - Legacy orchestration files (document but don't block)
   - Integration points (reasonable coverage expected)
```

**Cursor Instructions**:
```markdown
Implement pragmatic coverage enforcement:

1. Calculate baseline coverage:
   - Overall orchestration module: X%
   - QueryRouter-specific files: Y%
   - Core functionality files: Z%

2. Implement tiered enforcement:
   ```yaml
   # In .github/workflows/ci.yml

   - name: Check Coverage for Core QueryRouter
     run: |
       # High standard for completed work
       pytest tests/unit/test_queryrouter.py --cov=services/orchestration/queryrouter --cov-fail-under=80

   - name: Check Overall Orchestration Baseline
     run: |
       # Current reality as baseline to improve
       pytest tests/ --cov=services/orchestration --cov-fail-under=15

   - name: Document Coverage Trajectory
     run: |
       echo "Baseline (Sept 25): 15%" >> coverage_history.md
       echo "Target next epic: 20%" >> coverage_history.md
   ```
```

#### 2B. Document Coverage Philosophy

Create `docs/testing/coverage-philosophy.md`:
```markdown
# Coverage Philosophy During Refactor

## Principle
Coverage for COMPLETED components should approach 100%.
Overall coverage is a metric to improve, not a gate to fail.

## Current Baselines (Sept 25, 2025)
- Overall orchestration: 15%
- QueryRouter (completed): 80%
- Legacy components: <10%

## Enforcement Strategy
1. Completed work: Enforce high coverage (80%+)
2. Overall baseline: Document and track improvement
3. Each epic: Must improve overall coverage

## Not Blocking On
- Legacy code coverage
- Components scheduled for replacement
- Overall percentage during refactor
```

---

## Phase 3: CI/CD Integration (30 min)

### Both Agents - Ensure Enforcement Works

#### 3A. Test CI Changes Locally
```bash
# Simulate CI run
act -j test  # Using GitHub Actions locally

# Or manual simulation
./scripts/ci_simulation.sh
```

#### 3B. Create PR with Changes
```bash
git checkout -b feat/performance-coverage-enforcement
git add .github/workflows/
git add scripts/performance_baseline.py
git add docs/testing/coverage-philosophy.md
git commit -m "feat: Add performance and coverage enforcement

- Performance regression detection with realistic thresholds
- Tiered coverage enforcement (high for completed, baseline for overall)
- Documentation of coverage philosophy during refactor

Closes GREAT-1C locking phase requirements"
```

#### 3C. Verify in CI
- Push branch
- Watch CI run
- Confirm enforcement works but doesn't block on unrealistic standards

---

## Phase Z: Documentation & Handoff

### Evidence Collection
1. CI configuration showing performance gates
2. Coverage enforcement with tiered approach
3. Documentation of philosophy and baselines
4. Successful CI run with enforcement

### GitHub Update
```markdown
## Locking Phase Update

✅ Performance regression test alerts on degradation
- Implemented with realistic thresholds (2-3 seconds for LLM)
- Baseline documented, 10% degradation tolerance
- CI enforcement active

✅ Required test coverage for orchestration module
- Tiered enforcement: 80% for QueryRouter, 15% baseline overall
- Philosophy documented: Track improvement, don't block progress
- Coverage trajectory documented for future epics
```

---

## Success Criteria

- [ ] Performance tests run in CI with regression detection
- [ ] Thresholds based on actual performance, not arbitrary targets
- [ ] Coverage enforcement implemented with tiered approach
- [ ] High coverage for QueryRouter components specifically
- [ ] Overall coverage baseline documented for improvement
- [ ] CI passes with new enforcement
- [ ] Philosophy documented for team understanding

---

## STOP Conditions

- If CI system different than expected
- If performance varies too widely for meaningful thresholds
- If coverage tools not properly configured
- If enforcement would block all development

---

## Time Estimate

Based on systematic execution:
- Phase 1: 45 minutes (performance setup)
- Phase 2: 45 minutes (coverage analysis and implementation)
- Phase 3: 30 minutes (CI integration and testing)
- Total: ~2 hours

This estimate reflects thorough, systematic work without shortcuts.

---

*Excellence through systematic enforcement, not arbitrary gates.*

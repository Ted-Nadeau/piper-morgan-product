# Phase 1: Evidence Collection & CI Integration Specification

## Mission
Collect evidence for completed lock tests AND specify requirements for missing CI/coverage integration.

## Context from Verification
- ✅ Lock tests exist: `tests/regression/test_queryrouter_lock.py` (9 tests)
- ❌ Not in CI workflows
- ❌ No coverage reports generated
- Need: Evidence for what works + specifications for what's missing

## Part A: Evidence Collection

### 1. Lock Test Evidence
```bash
# Show the actual test file
cat tests/regression/test_queryrouter_lock.py

# Run the tests and capture output
cd /Users/xian/Development/piper-morgan
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py -v --tb=short

# Show test count and names
grep "^def test_" tests/regression/test_queryrouter_lock.py | wc -l
grep "^def test_" tests/regression/test_queryrouter_lock.py
```

### 2. Session Log Evidence
```bash
# Find yesterday's completion claims
grep -A 5 -B 5 "lock.*test\|regression.*test" dev/2025/09/22/*-code-log.md
grep -A 5 -B 5 "GREAT-1C" dev/2025/09/22/*-code-log.md
```

### 3. Test Functionality Demonstration
```bash
# Show what each test actually prevents
for test in $(grep "^def test_" tests/regression/test_queryrouter_lock.py | cut -d'(' -f1 | cut -d' ' -f2); do
  echo "=== $test ==="
  grep -A 10 "$test" tests/regression/test_queryrouter_lock.py | head -15
  echo ""
done
```

## Part B: Gap Specification

### 4. CI Integration Requirements
```bash
# Check current CI structure
ls -la .github/workflows/
cat .github/workflows/*.yml 2>/dev/null | head -50

# Specify what's needed
cat > /tmp/ci-integration-spec.md << 'EOF'
# CI Integration Specification for Lock Tests

## Current State
- Lock tests exist but not in CI workflows
- No automated regression prevention

## Required CI Updates
1. Add lock test job to main workflow
2. Fail build if lock tests fail
3. Run on: pull requests, main branch pushes

## Workflow Addition Needed
```yaml
  lock-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run lock tests
        run: pytest tests/regression/test_queryrouter_lock.py -v
```

## Success Criteria
- Lock tests run automatically on every PR
- Build fails if QueryRouter regression detected
EOF

cat /tmp/ci-integration-spec.md
```

### 5. Coverage Requirements
```bash
# Specify coverage generation
cat > /tmp/coverage-spec.md << 'EOF'
# Coverage Report Specification

## Required Commands
```bash
# Generate coverage for orchestration module
PYTHONPATH=. pytest tests/regression/test_queryrouter_lock.py \
  --cov=services/orchestration \
  --cov-report=html \
  --cov-report=term

# Minimum threshold
--cov-fail-under=80
```

## Expected Outputs
- htmlcov/ directory with HTML reports
- Terminal coverage summary
- services/orchestration/ at 80%+ coverage
EOF

cat /tmp/coverage-spec.md
```

## Evidence Report Format

Create evidence summary:
```markdown
## GREAT-1C Evidence Report

### ✅ Completed Work (With Evidence)

#### Lock Tests Created
- File: tests/regression/test_queryrouter_lock.py
- Test Count: 9 tests
- Pytest Output:
  ```
  [paste actual pytest output]
  ```
- Test Functions:
  ```
  [list all test_* functions]
  ```

#### Regression Prevention Demonstrated
[Show what each test prevents with code excerpts]

### ❌ Missing Work (With Specifications)

#### CI Integration
- Current: Not integrated
- Required: [link to ci-integration-spec.md]
- Effort: ~30 minutes to add workflow job

#### Coverage Reports
- Current: Not generated
- Required: [link to coverage-spec.md]
- Effort: ~15 minutes to run and document

### 📊 Checkbox Status Projection
- Can evidence NOW: 4 checkboxes (lock test existence and functionality)
- Need work to complete: 16 checkboxes (CI, docs, coverage, verification)
```

## Success Criteria
- Complete evidence for all existing work
- Clear specifications for all missing work
- Effort estimates for completing gaps
- PM has full picture for decision

## STOP Conditions
- If tests fail when run
- If test coverage unclear
- If CI structure incompatible with additions

---

**Deliver evidence + specifications, let PM decide next steps**

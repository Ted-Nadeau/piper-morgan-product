# Agent Prompt: Phase 7A - Locking Phase Verification

**Agent**: Code  
**Mission**: Verify the 2 remaining Locking Phase checkboxes with evidence of actual alerting and enforcement mechanisms, not just measurement or reporting.

## Context
- **Testing Phase**: Complete (2 checked, 2 postponed with documentation)
- **Locking Phase**: 3 boxes already checked, 2 remaining need verification
- **Standard**: Evidence of enforcement mechanisms that fail/alert, not just measurement

## Locking Phase Verification Tasks

### 1. Performance Regression Test Alerts on Degradation
**Requirement**: Alerts/notifications when performance degrades below threshold
**Evidence needed**: Mechanisms that actively notify or fail when performance degrades

```bash
# Verify performance regression alerting mechanisms
echo "=== Performance Regression Alerting Verification ==="

# Check for CI jobs that fail on performance degradation
echo "CI performance failure mechanisms:"
if [ -f ".github/workflows/test.yml" ]; then
    echo "Checking GitHub Actions for performance gates:"
    grep -A 15 -B 5 "performance\|benchmark\|500ms\|timeout" .github/workflows/test.yml || echo "No performance gates in main CI"
    
    echo ""
    echo "Checking for performance job failures:"
    grep -A 10 -B 5 "fail.*performance\|performance.*fail" .github/workflows/test.yml || echo "No performance failure conditions"
fi

# Look for additional workflow files
echo ""
echo "Additional CI workflows:"
find .github/workflows/ -name "*.yml" -exec grep -l "performance\|benchmark" {} \; | head -3

# Check for performance monitoring/alerting configuration
echo ""
echo "Performance alerting configuration:"
find . -name "*.py" -exec grep -l "performance.*alert\|alert.*performance\|notify.*performance" {} \; | head -5

# Check if pytest has performance failure configuration
echo ""
echo "Pytest performance configuration:"
if [ -f "pyproject.toml" ]; then
    grep -A 10 -B 5 "benchmark\|performance.*fail\|timeout" pyproject.toml || echo "No performance failure config in pyproject.toml"
fi

# Test if performance thresholds cause actual failures
echo ""
echo "Performance threshold enforcement test:"
PYTHONPATH=. python3 -c "
import time
import pytest
print('Testing if performance failures would block CI...')

# Simulate a slow test to see if it fails
def test_performance_threshold():
    start = time.time()
    time.sleep(0.6)  # Simulate 600ms (over 500ms threshold)
    duration = (time.time() - start) * 1000
    print(f'Simulated test duration: {duration:.0f}ms')
    
    # Check if this would cause a failure
    if duration > 500:
        print('Would FAIL: Duration exceeds 500ms threshold')
        return False
    else:
        print('Would PASS: Duration under 500ms threshold')
        return True

result = test_performance_threshold()
print(f'Performance enforcement active: {not result}')
"
```

### 2. Required Test Coverage for Orchestration Module
**Requirement**: Coverage enforcement that fails when below 80%
**Evidence needed**: Mechanisms that fail CI/commits when coverage drops below threshold

```bash
# Verify test coverage enforcement mechanisms
echo "=== Test Coverage Enforcement Verification ==="

# Check for coverage enforcement in CI
echo "Coverage enforcement in CI configuration:"
if [ -f ".github/workflows/test.yml" ]; then
    grep -A 15 -B 5 "coverage.*fail\|fail.*coverage\|coverage.*80\|80.*coverage" .github/workflows/test.yml || echo "No coverage enforcement in main CI"
    
    echo ""
    echo "Coverage reporting in CI:"
    grep -A 10 -B 5 "coverage.*report\|pytest.*cov" .github/workflows/test.yml || echo "No coverage commands in CI"
fi

# Check for coverage configuration files
echo ""
echo "Coverage configuration files:"
for config_file in .coveragerc setup.cfg pyproject.toml; do
    if [ -f "$config_file" ]; then
        echo "Found $config_file:"
        grep -A 10 -B 5 "coverage\|fail_under\|80" "$config_file" 2>/dev/null || echo "No coverage config in $config_file"
    fi
done

# Test current orchestration module coverage with enforcement
echo ""
echo "Current orchestration coverage with enforcement test:"
PYTHONPATH=. coverage erase 2>/dev/null || true
PYTHONPATH=. coverage run --source=services/orchestration -m pytest tests/ -q >/dev/null 2>&1

echo "Testing coverage enforcement for orchestration module:"
coverage report --include="services/orchestration/*" --fail-under=80 2>&1 && echo "✅ Coverage enforcement WOULD PASS" || echo "❌ Coverage enforcement WOULD FAIL"

echo ""
echo "Orchestration module coverage details:"
coverage report --include="services/orchestration/*" 2>/dev/null || echo "Coverage data not available"

# Check for pre-commit coverage hooks
echo ""
echo "Pre-commit coverage enforcement:"
if [ -f ".pre-commit-config.yaml" ]; then
    echo "Pre-commit coverage hooks:"
    grep -A 10 -B 5 "coverage" .pre-commit-config.yaml || echo "No coverage hooks in pre-commit"
fi

# Check for coverage gates in package configuration
echo ""
echo "Package-level coverage requirements:"
if [ -f "setup.py" ]; then
    grep -A 5 -B 5 "coverage\|test_require" setup.py || echo "No coverage requirements in setup.py"
fi
```

### 3. Comprehensive Enforcement Verification
```bash
# Verify both mechanisms work together
echo "=== Comprehensive Enforcement Verification ==="

echo "Performance + Coverage enforcement integration:"

# Check if CI would fail on both performance and coverage issues
echo "1. Performance enforcement status:"
performance_enforced=0
if grep -r "performance.*fail\|500ms.*fail" .github/ >/dev/null 2>&1; then
    performance_enforced=1
    echo "  ✅ Performance enforcement found in CI"
else
    echo "  ❌ No performance enforcement found"
fi

echo ""
echo "2. Coverage enforcement status:"
coverage_enforced=0
if coverage report --include="services/orchestration/*" --fail-under=80 >/dev/null 2>&1; then
    coverage_enforced=1
    echo "  ✅ Coverage enforcement configured and working"
else
    echo "  ❌ Coverage enforcement not working (below 80% or not configured)"
fi

# Check if both are integrated into CI
echo ""
echo "3. CI integration status:"
ci_integrated=0
if [ -f ".github/workflows/test.yml" ]; then
    if grep -q "coverage\|pytest.*cov" .github/workflows/test.yml; then
        ci_integrated=1
        echo "  ✅ Some test enforcement in CI"
    else
        echo "  ❌ No test enforcement found in CI"
    fi
fi

echo ""
echo "LOCKING PHASE CHECKBOX STATUS:"
echo "Performance regression alerts: $([ $performance_enforced -eq 1 ] && echo 'CAN CHECK ✅' || echo 'CANNOT CHECK ❌')"
echo "Coverage enforcement: $([ $coverage_enforced -eq 1 ] && echo 'CAN CHECK ✅' || echo 'CANNOT CHECK ❌')"
```

### 4. Gap Analysis for Missing Enforcement
```bash
# If enforcement is missing, identify what needs to be implemented
echo "=== Gap Analysis for Missing Enforcement ==="

if [ $performance_enforced -eq 0 ]; then
    echo ""
    echo "PERFORMANCE ENFORCEMENT GAPS:"
    echo "Missing implementations:"
    echo "  1. CI job step that runs performance tests with failure thresholds"
    echo "  2. Performance benchmark configuration with --benchmark-fail-if-slower"
    echo "  3. Pytest configuration with performance timeout settings"
    echo ""
    echo "Recommended implementation:"
    echo "  - Add GitHub Actions step: pytest --benchmark-only --benchmark-fail-if-slower"
    echo "  - Configure pytest-benchmark with 500ms threshold"
    echo "  - Add performance regression detection to CI pipeline"
    echo "  Estimated time: 30-45 minutes"
fi

if [ $coverage_enforced -eq 0 ]; then
    echo ""
    echo "COVERAGE ENFORCEMENT GAPS:" 
    echo "Missing implementations:"
    echo "  1. Coverage configuration with --fail-under=80"
    echo "  2. CI integration that fails on low coverage"
    echo "  3. Orchestration module may need improved test coverage to reach 80%"
    echo ""
    echo "Recommended implementation:"
    echo "  - Configure coverage with --fail-under=80 in pyproject.toml"
    echo "  - Add CI step: coverage report --fail-under=80 --include='services/orchestration/*'"
    echo "  - May need to write additional tests if current coverage < 80%"
    echo "  Estimated time: 30 minutes (config) + time for additional tests if needed"
fi

# Show current actual coverage for orchestration
echo ""
echo "Current orchestration module coverage:"
coverage report --include="services/orchestration/*" 2>/dev/null | grep -E "(services/orchestration|TOTAL)" | tail -5
```

## Evidence Collection Requirements

### Performance Alerting Evidence
```
=== Performance Regression Alerting Status ===
CI Performance Gates: [FOUND/MISSING with file locations]
Performance Failure Configuration: [CONFIGURED/NOT_CONFIGURED]
Alerting Mechanisms: [ACTIVE/MISSING]

Specific Evidence:
- Performance tests fail CI: [YES/NO with configuration details]
- 500ms threshold enforcement: [CONFIGURED/MISSING] 
- Alert/notification mechanisms: [list or NONE]

CHECKBOX STATUS: [CAN CHECK / CANNOT CHECK]
Missing implementations: [list specific gaps if cannot check]
```

### Coverage Enforcement Evidence  
```
=== Test Coverage Enforcement Status ===
Coverage Configuration: [FOUND/MISSING with threshold settings]
CI Coverage Gates: [CONFIGURED/MISSING]
Orchestration Module Coverage: [X]% (above/below 80% threshold)

Specific Evidence:
- Coverage fails under 80%: [YES/NO with configuration]
- CI integration: [ENABLED/MISSING]
- Pre-commit hooks: [CONFIGURED/MISSING]

CHECKBOX STATUS: [CAN CHECK / CANNOT CHECK]  
Missing implementations: [list specific gaps if cannot check]
```

### Implementation Requirements
```
=== Required Implementation Work ===
Performance Enforcement:
- [specific implementation needed or NONE]
- Estimated time: [X minutes or N/A]

Coverage Enforcement:
- [specific implementation needed or NONE]  
- Current orchestration coverage: [X]%
- Additional tests needed: [YES/NO]
- Estimated time: [X minutes or N/A]

Priority: [which to implement first if both needed]
```

## Success Criteria
- [ ] Evidence-based determination for performance alerting checkbox
- [ ] Evidence-based determination for coverage enforcement checkbox
- [ ] Specific gaps identified if implementations are missing
- [ ] Clear next steps for completing Locking Phase

## Time Estimate
15-20 minutes for verification of existing mechanisms

## Critical Focus
**Enforcement over measurement**: Verify mechanisms that fail/alert, not just report
**CI integration**: Check that enforcement actually blocks bad code from merging
**Specific thresholds**: Verify 500ms and 80% thresholds are enforced, not just measured

**Focus: Get definitive evidence for checking the 2 remaining Locking Phase boxes.**

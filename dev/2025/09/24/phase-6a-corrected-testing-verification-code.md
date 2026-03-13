# Agent Prompt: Phase 6A-Corrected - Complete Testing Evidence Verification

**Agent**: Code
**Mission**: Verify the two remaining unchecked locking phase boxes with specific evidence of alerting mechanisms and enforcement, not just test existence.

## Context - Course Correction
- **Issue**: Jumped to documentation before completing testing verification (inchworm violation)
- **Correction**: Complete testing evidence verification first, systematically
- **Focus**: Two specific unchecked boxes from GREAT-1C locking phase

## Missing Evidence Verification Tasks

### 1. Performance Regression Test Alerts on Degradation
**Question**: Do we have alerting mechanisms that trigger when performance degrades below 500ms?
**Evidence needed**: Not just performance tests, but actual alerting/failure systems

```bash
# Check for performance alerting mechanisms
echo "=== Performance Regression Alerting Verification ==="

# Look for CI configuration that fails on performance degradation
echo "CI performance failure configuration:"
find .github/workflows/ -name "*.yml" -exec grep -l "performance\|benchmark\|timeout" {} \;

if [ -f ".github/workflows/test.yml" ]; then
    echo ""
    echo "Performance thresholds in CI:"
    grep -A 10 -B 5 "performance\|benchmark\|500ms\|timeout" .github/workflows/test.yml || echo "No performance thresholds in CI"
fi

# Check for performance monitoring in pytest configuration
echo ""
echo "Pytest performance configuration:"
if [ -f "pyproject.toml" ]; then
    grep -A 5 -B 5 "performance\|benchmark\|timeout" pyproject.toml || echo "No performance config in pyproject.toml"
fi

# Look for performance test failures that would block CI
echo ""
echo "Performance test CI integration:"
grep -r "500ms\|performance.*fail\|benchmark.*fail" .github/ || echo "No performance failure blocking in CI"

# Check for actual alerting mechanisms (not just measurement)
echo ""
echo "Performance degradation alerting:"
find . -name "*.py" -exec grep -l "alert\|notify\|degrade.*performance" {} \; | head -5
grep -r "performance.*alert\|alert.*performance" . --include="*.py" --include="*.yml" | head -5 || echo "No performance alerting found"
```

### 2. Required Test Coverage for Orchestration Module
**Question**: Do we have coverage enforcement that fails CI when coverage drops below 80%?
**Evidence needed**: Not just coverage measurement, but actual enforcement mechanisms

```bash
# Check for test coverage enforcement mechanisms
echo "=== Test Coverage Enforcement Verification ==="

# Check if coverage is enforced in CI
echo "Coverage enforcement in CI:"
if [ -f ".github/workflows/test.yml" ]; then
    grep -A 10 -B 5 "coverage.*fail\|fail.*coverage\|80%\|coverage.*threshold" .github/workflows/test.yml || echo "No coverage enforcement in CI"
fi

# Check for coverage configuration with failure thresholds
echo ""
echo "Coverage failure thresholds:"
if [ -f "pyproject.toml" ]; then
    grep -A 10 -B 5 "coverage\|80%\|fail_under\|threshold" pyproject.toml || echo "No coverage thresholds in pyproject.toml"
fi

# Check for coverage.py configuration
if [ -f ".coveragerc" ]; then
    echo ""
    echo "Coverage configuration file:"
    cat .coveragerc
elif [ -f "setup.cfg" ]; then
    echo ""
    echo "Coverage in setup.cfg:"
    grep -A 10 -B 5 "coverage" setup.cfg || echo "No coverage config in setup.cfg"
fi

# Test if coverage enforcement actually works
echo ""
echo "Testing coverage enforcement:"
echo "Current orchestration module coverage:"
PYTHONPATH=. coverage run --source=services/orchestration -m pytest tests/ -q
coverage report --include="services/orchestration/*" --fail-under=80 2>&1 || echo "Coverage enforcement would fail CI"

# Check for pre-commit coverage hooks
echo ""
echo "Pre-commit coverage enforcement:"
if [ -f ".pre-commit-config.yaml" ]; then
    grep -A 5 -B 5 "coverage" .pre-commit-config.yaml || echo "No coverage hooks in pre-commit"
fi
```

### 3. Specific GREAT-1C Box Verification
```bash
# Verify specific checkbox requirements with evidence
echo "=== Checkbox Evidence Verification ==="

echo "CHECKBOX 1: Performance regression test alerts on degradation"
echo "Requirements: Alerts/notifications when performance degrades below threshold"
echo "Evidence found:"

# Look for specific alerting mechanisms
performance_alerts=0
if grep -r "performance.*alert\|alert.*performance" . --include="*.py" --include="*.yml" >/dev/null 2>&1; then
    performance_alerts=1
    echo "  ✅ Performance alerting code found"
else
    echo "  ❌ No performance alerting mechanisms found"
fi

# Check for CI failure on performance degradation
ci_performance=0
if grep -r "500ms\|performance.*fail" .github/ >/dev/null 2>&1; then
    ci_performance=1
    echo "  ✅ CI configured to fail on performance issues"
else
    echo "  ❌ No CI performance failure configuration found"
fi

echo ""
echo "CHECKBOX 1 STATUS: $([ $performance_alerts -eq 1 ] && [ $ci_performance -eq 1 ] && echo 'CAN CHECK ✅' || echo 'CANNOT CHECK ❌ - Missing alerting mechanisms')"

echo ""
echo "CHECKBOX 2: Required test coverage for orchestration module"
echo "Requirements: Coverage enforcement that fails when below 80%"
echo "Evidence found:"

# Check for coverage enforcement
coverage_enforcement=0
if coverage report --include="services/orchestration/*" --fail-under=80 >/dev/null 2>&1; then
    coverage_enforcement=1
    echo "  ✅ Coverage enforcement configured and working"
else
    echo "  ❌ No coverage enforcement - current coverage below 80% or not configured"
fi

# Check for CI coverage gates
ci_coverage=0
if grep -r "coverage.*fail\|fail.*coverage" .github/ >/dev/null 2>&1; then
    ci_coverage=1
    echo "  ✅ CI configured to fail on low coverage"
else
    echo "  ❌ No CI coverage enforcement found"
fi

echo ""
echo "CHECKBOX 2 STATUS: $([ $coverage_enforcement -eq 1 ] && [ $ci_coverage -eq 1 ] && echo 'CAN CHECK ✅' || echo 'CANNOT CHECK ❌ - Missing coverage enforcement')"
```

### 4. Implementation Gap Analysis
```bash
# If evidence is missing, identify what needs to be implemented
echo "=== Implementation Gap Analysis ==="

echo "Missing implementations needed:"

# Performance alerting gaps
if ! grep -r "performance.*alert" . --include="*.py" >/dev/null 2>&1; then
    echo ""
    echo "PERFORMANCE ALERTING GAPS:"
    echo "  1. Need CI job that fails when performance tests exceed 500ms"
    echo "  2. Need performance threshold configuration in pytest or CI"
    echo "  3. Need actual alerting mechanism (not just measurement)"
    echo "  Estimated work: 1-2 hours to implement CI performance gates"
fi

# Coverage enforcement gaps
if ! coverage report --include="services/orchestration/*" --fail-under=80 >/dev/null 2>&1; then
    echo ""
    echo "COVERAGE ENFORCEMENT GAPS:"
    echo "  1. Need coverage configuration with --fail-under=80"
    echo "  2. Need CI integration that fails on low coverage"
    echo "  3. May need to improve actual coverage to meet 80% threshold"
    echo "  Estimated work: 30 minutes for configuration + time to improve coverage if needed"
fi

# Show current coverage status
echo ""
echo "Current coverage status:"
PYTHONPATH=. coverage run --source=services/orchestration -m pytest tests/ -q >/dev/null 2>&1
coverage report --include="services/orchestration/*"
```

## Evidence Collection Requirements

### Performance Alerting Evidence
```
=== Performance Regression Alerting Status ===
Alerting mechanisms found: [YES/NO with details]
CI performance gates: [CONFIGURED/MISSING]
Performance threshold enforcement: [WORKING/NOT_CONFIGURED]

Specific evidence:
- Performance tests that fail CI: [list or NONE]
- Alerting configuration: [location or MISSING]
- 500ms threshold enforcement: [ENABLED/DISABLED]

CHECKBOX STATUS: [CAN CHECK / CANNOT CHECK]
Reason: [specific missing alerting mechanisms]
```

### Coverage Enforcement Evidence
```
=== Test Coverage Enforcement Status ===
Coverage enforcement configured: [YES/NO]
CI coverage gates: [ENABLED/MISSING]
80% threshold enforcement: [WORKING/NOT_WORKING]

Current coverage metrics:
- Orchestration module coverage: [X]%
- Meets 80% requirement: [YES/NO]
- CI fails on low coverage: [YES/NO]

CHECKBOX STATUS: [CAN CHECK / CANNOT CHECK]
Reason: [specific missing enforcement mechanisms]
```

### Implementation Requirements
```
=== Required Implementation Work ===
Performance alerting needs:
1. [specific gap requiring work]
2. [specific gap requiring work]
Estimated time: [X hours]

Coverage enforcement needs:
1. [specific gap requiring work]
2. [specific gap requiring work]
Estimated time: [X hours]

Ready to check boxes after implementation: [YES/NO]
Priority order for implementation: [ranked list]
```

## Success Criteria
- [ ] Evidence-based determination for performance alerting checkbox
- [ ] Evidence-based determination for coverage enforcement checkbox
- [ ] Specific gaps identified if boxes cannot be checked
- [ ] Implementation requirements documented if work needed
- [ ] Clear next steps for completing testing verification phase

## Time Estimate
20-25 minutes for complete testing evidence verification

## Critical Focus
**Evidence over existence**: Verify alerting and enforcement mechanisms, not just tests or measurement
**Systematic completion**: Complete testing phase before moving to documentation
**Inchworm discipline**: One phase at a time, thoroughly completed

**Focus: Get definitive evidence for the two unchecked testing boxes before proceeding to documentation verification.**

# Agent Prompt: Phase 5B - Documentation and Locking Verification

**Agent**: Cursor  
**Mission**: Verify documentation status and locking mechanisms mentioned in GREAT-1C acceptance criteria, and identify gaps that need addressing.

## Context
- **Testing evidence**: Code is gathering performance and test execution evidence
- **Documentation requirements**: GREAT-1C requires updated docs reflecting current reality
- **Locking requirements**: Mechanisms to prevent QueryRouter from being disabled again
- **Standard**: Evidence-based verification before checking acceptance criteria boxes

## GREAT-1C Documentation and Locking Verification Tasks

### 1. Documentation Phase Verification
```bash
# Check current documentation status vs acceptance criteria requirements
echo "=== Documentation Phase Verification ==="

# Check architecture.md current state vs requirements
echo "Checking architecture.md updates:"
if [ -f "docs/architecture.md" ]; then
    echo "architecture.md exists"
    grep -n -i "queryrouter\|orchestration\|flow" docs/architecture.md || echo "No QueryRouter/orchestration content found"
else
    echo "architecture.md missing"
fi

# Check for misleading TODO comments
echo ""
echo "=== Misleading TODO Comments Check ==="
grep -r "TODO" --include="*.py" services/orchestration/ | head -10
echo "Total TODO comments in orchestration:"
grep -r "TODO" --include="*.py" services/orchestration/ | wc -l

# Check for TODO comments without issue numbers (violation of methodology)
echo ""
echo "=== TODO Comments Without Issue Numbers ==="
grep -r "TODO" --include="*.py" . | grep -v "#[0-9]" | head -10

# Check initialization sequence documentation
echo ""
echo "=== Initialization Sequence Documentation ==="
find . -name "*.md" -exec grep -l "initialization\|startup\|sequence" {} \;

# Check ADR-032 implementation status
echo ""
echo "=== ADR-032 Implementation Status ==="
if [ -f "docs/adr/ADR-032.md" ]; then
    echo "ADR-032 exists:"
    grep -n -i "status\|implementation\|complete" docs/adr/ADR-032.md
else
    echo "ADR-032 not found - checking for ADR files:"
    find . -name "*ADR*" -o -name "*adr*" | head -5
fi

# Check for troubleshooting guide
echo ""
echo "=== Troubleshooting Guide Status ==="
find . -name "*trouble*" -o -name "*debug*" -o -name "*guide*" | grep -i trouble
```

### 2. Locking Phase Verification
```bash
# Verify CI/CD pipeline configuration
echo "=== CI/CD Locking Verification ==="

# Check GitHub Actions configuration
if [ -f ".github/workflows/test.yml" ] || [ -f ".github/workflows/ci.yml" ]; then
    echo "GitHub Actions configuration found:"
    ls -la .github/workflows/
    
    # Check if tests fail pipeline
    echo ""
    echo "Pipeline test configuration:"
    cat .github/workflows/*.yml | grep -A 10 -B 5 "pytest\|test"
    
    # Check if QueryRouter tests are in CI
    echo ""
    echo "QueryRouter in CI pipeline:"
    grep -r "queryrouter\|QueryRouter" .github/workflows/ || echo "No QueryRouter-specific CI checks found"
else
    echo "No GitHub Actions configuration found"
    ls -la .github/ 2>/dev/null || echo "No .github directory"
fi

# Check pre-commit hooks configuration
echo ""
echo "=== Pre-commit Hook Verification ==="
if [ -f ".pre-commit-config.yaml" ]; then
    echo "Pre-commit configuration found:"
    cat .pre-commit-config.yaml
    
    # Check for TODO format enforcement
    echo ""
    echo "TODO format enforcement in pre-commit:"
    grep -i "todo" .pre-commit-config.yaml || echo "No TODO enforcement found"
    
    # Check for component disabling prevention
    echo ""
    echo "Component disabling prevention:"
    grep -i "comment\|disable" .pre-commit-config.yaml || echo "No component disabling prevention found"
else
    echo "No pre-commit configuration found"
fi

# Check pyproject.toml for test configurations
echo ""
echo "=== Test Configuration Verification ==="
if [ -f "pyproject.toml" ]; then
    echo "pyproject.toml test configuration:"
    grep -A 10 -B 5 "pytest\|test" pyproject.toml || echo "No pytest configuration found"
else
    echo "No pyproject.toml found"
fi
```

### 3. Performance Regression Prevention
```bash
# Check for performance regression tests specifically
echo "=== Performance Regression Prevention ==="

# Find performance-related test files
echo "Performance test files:"
find tests/ -name "*performance*" -o -name "*benchmark*" -o -name "*regression*"

# Check for 500ms threshold tests
echo ""
echo "500ms threshold enforcement:"
grep -r "500" tests/ --include="*.py" | grep -i "ms\|millisecond\|time\|performance"

# Check for performance monitoring configuration
echo ""
echo "Performance monitoring setup:"
find . -name "*.py" -exec grep -l "benchmark\|performance.*monitor\|timing" {} \;

# Look for alerting or failure conditions on performance degradation
echo ""
echo "Performance degradation detection:"
grep -r "degradation\|slower\|timeout" tests/ --include="*.py" | head -5
```

### 4. Test Coverage Enforcement
```bash
# Check for test coverage requirements
echo "=== Test Coverage Enforcement ==="

# Check if coverage is configured in pyproject.toml
if [ -f "pyproject.toml" ]; then
    echo "Coverage configuration in pyproject.toml:"
    grep -A 5 -B 5 "coverage\|80%" pyproject.toml || echo "No coverage configuration found"
fi

# Check for coverage enforcement in CI
if [ -f ".github/workflows/test.yml" ]; then
    echo ""
    echo "Coverage enforcement in CI:"
    grep -A 10 -B 5 "coverage" .github/workflows/test.yml || echo "No coverage enforcement in CI"
fi

# Check for coverage requirements in documentation
echo ""
echo "Coverage requirements in docs:"
find . -name "*.md" -exec grep -l "80%\|coverage.*requirement" {} \;
```

### 5. QueryRouter Specific Locking
```bash
# Check for QueryRouter-specific locking mechanisms
echo "=== QueryRouter Specific Locking ==="

# Look for tests that explicitly check QueryRouter is not None/disabled
echo "QueryRouter initialization lock tests:"
grep -r "QueryRouter.*None\|query_router.*None" tests/ --include="*.py"

# Look for tests that fail if QueryRouter is commented out
echo ""
echo "QueryRouter comment detection tests:"
grep -r "comment.*QueryRouter\|disabled.*QueryRouter" tests/ --include="*.py"

# Check for import verification tests
echo ""
echo "QueryRouter import verification:"
grep -r "import.*QueryRouter\|from.*QueryRouter" tests/ --include="*.py"

# Check the actual regression test mentioned in acceptance criteria
echo ""
echo "=== Specific Regression Test Verification ==="
if [ -f "tests/regression/test_queryrouter_lock.py" ]; then
    echo "QueryRouter lock test exists:"
    wc -l tests/regression/test_queryrouter_lock.py
    echo ""
    echo "Test functions in lock file:"
    grep "def test_" tests/regression/test_queryrouter_lock.py
    echo ""
    echo "Lock test content preview:"
    head -30 tests/regression/test_queryrouter_lock.py
else
    echo "QueryRouter lock test missing"
fi
```

### 6. Documentation Content Analysis
```bash
# Analyze current documentation vs requirements
echo "=== Documentation Content Analysis ==="

# Check if current flow is documented
echo "Current orchestration flow documentation:"
find . -name "*.md" -exec grep -l "orchestration.*flow\|request.*flow\|pipeline" {} \;

# Check if QueryRouter role is documented
echo ""
echo "QueryRouter role documentation:"
find . -name "*.md" -exec grep -l "QueryRouter.*role\|QueryRouter.*purpose" {} \;

# Check initialization sequence documentation
echo ""
echo "Initialization sequence documentation:"
find . -name "*.md" -exec grep -l "initialization.*sequence\|startup.*order" {} \;

# Check for outdated documentation
echo ""
echo "Potentially outdated documentation references:"
find . -name "*.md" -exec grep -l "TODO\|FIXME\|outdated\|deprecated" {} \;
```

### 7. Comprehensive Gap Analysis
```bash
# Create comprehensive gap analysis for acceptance criteria
echo "=== GREAT-1C Gap Analysis ==="

echo "Acceptance Criteria Status:"
echo "Testing Phase:"
echo "  - Unit tests: Need to verify execution"
echo "  - Integration tests: Need to verify execution"  
echo "  - Performance tests <500ms: Need evidence"
echo "  - Error scenario tests: Need verification"
echo "  - E2E GitHub issue creation: Need to check scope"

echo ""
echo "Locking Phase:"
echo "  - CI/CD fails if QueryRouter disabled: $([ -f ".github/workflows/test.yml" ] && echo "CONFIG EXISTS" || echo "MISSING")"
echo "  - Initialization test prevents commenting: $([ -f "tests/regression/test_queryrouter_lock.py" ] && echo "TEST EXISTS" || echo "MISSING")"
echo "  - Performance regression alerts: NEED TO VERIFY"
echo "  - Required test coverage: NEED TO VERIFY"
echo "  - Pre-commit hooks: $([ -f ".pre-commit-config.yaml" ] && echo "CONFIG EXISTS" || echo "MISSING")"

echo ""
echo "Documentation Phase:"
echo "  - architecture.md updates: $([ -f "docs/architecture.md" ] && echo "FILE EXISTS" || echo "MISSING")"
echo "  - TODO comment cleanup: NEED TO VERIFY"
echo "  - Initialization sequence docs: NEED TO VERIFY"
echo "  - ADR-032 status update: NEED TO VERIFY"
echo "  - Troubleshooting guide: $(find . -name "*trouble*" -o -name "*debug*" | wc -l) files found"

echo ""
echo "Verification Phase:"
echo "  - Fresh clone works: NEED TO VERIFY"
echo "  - New developer understanding: NEED TO VERIFY"
echo "  - All tests pass in CI: NEED TO VERIFY"
echo "  - No TODO without issue numbers: NEED TO VERIFY"
echo "  - Performance benchmarks documented: NEED TO VERIFY"
```

## Evidence Collection Requirements

### Documentation Status
```
=== Documentation Phase Evidence ===
architecture.md Status: [EXISTS/MISSING - last modified date]
Current Content: [brief summary of QueryRouter documentation]
Gaps Identified: [list missing documentation requirements]

TODO Comments: [count in orchestration module]
TODO Without Issue Numbers: [count - these violate methodology]
Misleading Comments: [list of comments that need updating]

ADR-032 Status: [FOUND/MISSING - implementation status documented]
Troubleshooting Guide: [EXISTS/MISSING - location if found]
Initialization Sequence: [DOCUMENTED/MISSING]
```

### Locking Mechanisms Status  
```
=== Locking Phase Evidence ===
CI/CD Configuration: [FOUND/MISSING - which files]
CI Pipeline Tests QueryRouter: [YES/NO - specific tests]
CI Fails if QueryRouter Disabled: [YES/NO - evidence]

Pre-commit Hooks: [FOUND/MISSING - configuration file]
TODO Format Enforcement: [YES/NO - specific rules]
Component Disabling Prevention: [YES/NO - specific rules]

Performance Regression Tests: [count found]
500ms Threshold Enforcement: [YES/NO - specific tests]
Coverage Requirements: [configured threshold or MISSING]
Coverage Enforcement: [CI/local/MISSING]
```

### QueryRouter Specific Locks
```
=== QueryRouter Lock Mechanisms ===
Initialization Lock Test: [EXISTS/MISSING - test file]
Comment Detection Test: [EXISTS/MISSING - prevents commenting out]
Import Verification Test: [EXISTS/MISSING - ensures imports work]
Performance Lock Test: [EXISTS/MISSING - prevents degradation]

Specific Test Evidence:
tests/regression/test_queryrouter_lock.py: [EXISTS/MISSING]
Test Functions: [list of test functions if file exists]
Lock Effectiveness: [assessment of how well locks prevent regression]
```

### Gap Summary
```
=== GREAT-1C Completion Status ===
Ready to Check (Evidence Available): [list criteria with evidence]
Need More Work (Gaps Found): [list criteria missing evidence]
Blocked/Unclear: [list criteria needing clarification]

Priority Gaps to Address:
1. [highest priority missing requirement]
2. [second priority missing requirement]  
3. [third priority missing requirement]

Estimated Work Remaining: [assessment of effort needed]
```

## Success Criteria
- [ ] Documentation gaps identified for all GREAT-1C requirements
- [ ] Locking mechanism status verified with evidence
- [ ] Performance regression prevention assessed
- [ ] Test coverage enforcement status confirmed
- [ ] QueryRouter specific locks evaluated
- [ ] Comprehensive gap analysis completed

## Time Estimate
25-30 minutes for complete documentation and locking verification

## Critical Focus
**Evidence-based assessment**: Verify actual existence and effectiveness of locking mechanisms
**Gap identification**: Clear list of what's missing vs what acceptance criteria require
**Documentation reality check**: Current state vs what GREAT-1C requires
**Actionable findings**: Specific gaps that need addressing before boxes can be checked

**Focus: Provide PM with clear evidence of what exists vs what's required to make informed decisions about GREAT-1C completion.**

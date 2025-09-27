# Agent Prompt: Phase 1B - Performance Enforcement Implementation

**Agent**: Cursor
**Mission**: Implement realistic performance enforcement in CI based on actual baseline measurements from Phase 1A, following Chief Architect's gameplan.

## Context from Chief Architect
- **Approach**: Realistic thresholds based on actual performance, not arbitrary targets
- **Enforcement strategy**: Catch meaningful regressions without blocking development
- **Integration**: Add to CI pipeline with proper failure conditions

## Phase 1B Implementation Tasks

### 1. CI Configuration Assessment
```bash
# Check current CI/CD configuration
echo "=== Current CI/CD Configuration Assessment ==="

# Find CI configuration files
echo "CI configuration files:"
find .github/workflows/ -name "*.yml" -o -name "*.yaml" | head -5
ls -la .github/workflows/

# Analyze existing test configuration
echo ""
echo "Current test configuration in CI:"
if [ -f ".github/workflows/test.yml" ]; then
    echo "Found test.yml:"
    grep -A 15 -B 5 "pytest\|test" .github/workflows/test.yml
elif [ -f ".github/workflows/ci.yml" ]; then
    echo "Found ci.yml:"
    grep -A 15 -B 5 "pytest\|test" .github/workflows/ci.yml
else
    echo "No standard CI files found, checking all workflows:"
    grep -r "pytest\|test" .github/workflows/ | head -10
fi

# Check if performance tests are already in CI
echo ""
echo "Performance tests in current CI:"
grep -r "performance\|benchmark" .github/workflows/ | head -5 || echo "No performance tests in CI"
```

### 2. Performance Baseline Integration
```bash
# Integrate baseline measurements from Phase 1A
echo "=== Integrating Performance Baselines ==="

# Wait for Code to provide baseline measurements, then create configuration
# This will be updated with actual measurements from Phase 1A

# Create performance configuration file
cat > scripts/performance_config.py << 'EOF'
#!/usr/bin/env python3
"""
Performance Configuration for CI/CD Enforcement
Based on actual measurements from Phase 1A assessment

This configuration uses REALISTIC thresholds derived from
actual system performance, not aspirational targets.
"""

# These values will be updated with Phase 1A measurements
PERFORMANCE_THRESHOLDS = {
    # QueryRouter initialization (measured baseline + 20% tolerance)
    "queryrouter_init_ms": 60,  # Update with actual measurement

    # LLM classification (measured baseline + 20% tolerance)
    "llm_classification_ms": 2400,  # Update with actual measurement

    # Full orchestration flow (measured baseline + 20% tolerance)
    "orchestration_flow_ms": 3600,  # Update with actual measurement
}

def check_performance_regression(test_name: str, actual_ms: float) -> bool:
    """Check if performance indicates regression"""
    threshold = PERFORMANCE_THRESHOLDS.get(test_name)
    if threshold is None:
        print(f"No threshold configured for {test_name}")
        return True

    if actual_ms > threshold:
        print(f"PERFORMANCE REGRESSION: {test_name}")
        print(f"  Threshold: {threshold}ms")
        print(f"  Actual: {actual_ms}ms")
        print(f"  Regression: {((actual_ms / threshold) * 100) - 100:.1f}%")
        return False

    print(f"Performance acceptable: {test_name} ({actual_ms}ms <= {threshold}ms)")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        test_name = sys.argv[1]
        actual_time = float(sys.argv[2])
        result = check_performance_regression(test_name, actual_time)
        sys.exit(0 if result else 1)
EOF

echo "Performance configuration created at scripts/performance_config.py"
```

### 3. CI Performance Enforcement Implementation
```bash
# Add performance enforcement to CI configuration
echo "=== Adding Performance Enforcement to CI ==="

# Create backup of current CI configuration
if [ -f ".github/workflows/test.yml" ]; then
    cp .github/workflows/test.yml .github/workflows/test.yml.backup
    ci_file=".github/workflows/test.yml"
elif [ -f ".github/workflows/ci.yml" ]; then
    cp .github/workflows/ci.yml .github/workflows/ci.yml.backup
    ci_file=".github/workflows/ci.yml"
else
    echo "Creating new CI configuration file"
    ci_file=".github/workflows/test.yml"
fi

echo "Working with CI file: $ci_file"

# Add performance testing job to CI
cat >> "$ci_file" << 'EOF'

  performance-regression-check:
    name: Performance Regression Detection
    runs-on: ubuntu-latest
    needs: [test]  # Run after regular tests pass

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt --break-system-packages

    - name: Run Performance Regression Tests
      run: |
        echo "Running performance regression detection..."

        # Run performance tests with timing capture
        PYTHONPATH=. python3 << 'PYTHON_SCRIPT'
import asyncio
import sys
import time
from services.orchestration.engine import OrchestrationEngine
from services.intent_service.llm_classifier import LLMClassifier
from database.session import get_async_session

# Import performance configuration
sys.path.append('scripts')
from performance_config import check_performance_regression

async def test_queryrouter_performance():
    """Test QueryRouter initialization performance"""
    try:
        async with get_async_session() as session:
            start = time.time()
            engine = OrchestrationEngine(session)
            duration_ms = (time.time() - start) * 1000

            return check_performance_regression("queryrouter_init_ms", duration_ms)
    except Exception as e:
        print(f"QueryRouter performance test failed: {e}")
        return False

async def test_llm_performance():
    """Test LLM classification performance"""
    try:
        classifier = LLMClassifier()
        start = time.time()
        result = await classifier.classify("Create a GitHub issue")
        duration_ms = (time.time() - start) * 1000

        return check_performance_regression("llm_classification_ms", duration_ms)
    except Exception as e:
        print(f"LLM performance test failed: {e}")
        return False

async def test_orchestration_performance():
    """Test full orchestration flow performance"""
    try:
        async with get_async_session() as session:
            engine = OrchestrationEngine(session)
            start = time.time()
            result = await engine.process_request("List projects")
            duration_ms = (time.time() - start) * 1000

            return check_performance_regression("orchestration_flow_ms", duration_ms)
    except Exception as e:
        print(f"Orchestration performance test failed: {e}")
        return False

async def main():
    """Run all performance regression tests"""
    print("=== Performance Regression Detection ===")

    tests = [
        ("QueryRouter Init", test_queryrouter_performance),
        ("LLM Classification", test_llm_performance),
        ("Orchestration Flow", test_orchestration_performance),
    ]

    all_passed = True
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = await test_func()
            if not result:
                all_passed = False
                print(f"❌ {test_name} FAILED performance regression check")
            else:
                print(f"✅ {test_name} passed performance check")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            all_passed = False

    if not all_passed:
        print("\n🚨 PERFORMANCE REGRESSION DETECTED - Failing build")
        sys.exit(1)
    else:
        print("\n✅ All performance tests passed - No regression detected")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
PYTHON_SCRIPT

    - name: Performance Test Summary
      if: failure()
      run: |
        echo "❌ Performance regression detected!"
        echo "This build failed because one or more components"
        echo "performed significantly slower than baseline measurements."
        echo ""
        echo "To investigate:"
        echo "1. Check the performance test output above"
        echo "2. Compare with baseline measurements in scripts/performance_config.py"
        echo "3. If this is a legitimate improvement, update baselines"
        echo "4. If this is a regression, investigate recent changes"
EOF

echo "Performance enforcement added to $ci_file"
```

### 4. Performance Testing Script Creation
```bash
# Create standalone performance testing script for local use
echo "=== Creating Local Performance Testing Script ==="

cat > scripts/run_performance_tests.py << 'EOF'
#!/usr/bin/env python3
"""
Local Performance Testing Script

Run this locally to check performance before pushing to CI.
Usage: python scripts/run_performance_tests.py
"""

import asyncio
import sys
import time
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.orchestration.engine import OrchestrationEngine
from services.intent_service.llm_classifier import LLMClassifier
from database.session import get_async_session
from scripts.performance_config import check_performance_regression

class LocalPerformanceTester:
    """Local performance testing with baseline comparison"""

    async def test_queryrouter_init(self) -> bool:
        """Test QueryRouter initialization performance"""
        print("Testing QueryRouter initialization...")
        times = []

        for i in range(3):  # Run 3 times for consistency
            try:
                async with get_async_session() as session:
                    start = time.time()
                    engine = OrchestrationEngine(session)
                    duration_ms = (time.time() - start) * 1000
                    times.append(duration_ms)
                    print(f"  Run {i+1}: {duration_ms:.1f}ms")
            except Exception as e:
                print(f"  Run {i+1}: FAILED - {e}")
                return False

        avg_time = sum(times) / len(times)
        max_time = max(times)
        print(f"  Average: {avg_time:.1f}ms, Max: {max_time:.1f}ms")

        return check_performance_regression("queryrouter_init_ms", max_time)

    async def test_llm_classification(self) -> bool:
        """Test LLM classification performance"""
        print("Testing LLM classification...")

        try:
            classifier = LLMClassifier()
            test_message = "Create a GitHub issue about performance testing"

            start = time.time()
            result = await classifier.classify(test_message)
            duration_ms = (time.time() - start) * 1000

            print(f"  Duration: {duration_ms:.0f}ms")
            print(f"  Result: {result.category if hasattr(result, 'category') else 'N/A'}")

            return check_performance_regression("llm_classification_ms", duration_ms)
        except Exception as e:
            print(f"  FAILED - {e}")
            return False

    async def test_orchestration_flow(self) -> bool:
        """Test full orchestration flow performance"""
        print("Testing orchestration flow...")

        try:
            async with get_async_session() as session:
                engine = OrchestrationEngine(session)
                test_input = "List all current projects"

                start = time.time()
                result = await engine.process_request(test_input)
                duration_ms = (time.time() - start) * 1000

                print(f"  Duration: {duration_ms:.0f}ms")
                print(f"  Result type: {type(result)}")

                return check_performance_regression("orchestration_flow_ms", duration_ms)
        except Exception as e:
            print(f"  FAILED - {e}")
            return False

    async def run_all_tests(self) -> bool:
        """Run all performance tests"""
        print("🔍 Local Performance Testing")
        print("=" * 40)

        tests = [
            ("QueryRouter Initialization", self.test_queryrouter_init),
            ("LLM Classification", self.test_llm_classification),
            ("Orchestration Flow", self.test_orchestration_flow),
        ]

        all_passed = True
        results = []

        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            try:
                result = await test_func()
                results.append((test_name, "PASS" if result else "FAIL"))
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"ERROR: {e}")
                results.append((test_name, "ERROR"))
                all_passed = False

        # Summary
        print("\n" + "=" * 40)
        print("PERFORMANCE TEST SUMMARY")
        for test_name, status in results:
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {status}")

        if all_passed:
            print("\n🎉 All performance tests PASSED!")
            print("Safe to push - no performance regressions detected")
        else:
            print("\n⚠️  Performance regressions detected!")
            print("Review failing tests before pushing to CI")

        return all_passed

async def main():
    """Main entry point"""
    tester = LocalPerformanceTester()
    result = await tester.run_all_tests()
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    asyncio.run(main())
EOF

chmod +x scripts/run_performance_tests.py
echo "Local performance testing script created at scripts/run_performance_tests.py"
```

### 5. Documentation and Usage Instructions
```bash
# Create documentation for performance enforcement
echo "=== Creating Performance Enforcement Documentation ==="

cat > docs/testing/performance-enforcement.md << 'EOF'
# Performance Enforcement Documentation

## Overview

Performance enforcement prevents performance regressions by failing CI builds when components perform significantly slower than established baselines.

## Philosophy

- **Realistic baselines**: Based on actual measured performance, not aspirational targets
- **Tolerance for variance**: 20% degradation tolerance to avoid false positives
- **Meaningful regression detection**: Catches significant slowdowns that impact user experience
- **Non-blocking development**: Thresholds set to catch real problems, not normal variance

## Current Baselines

Updated based on Phase 1A measurements:

| Component | Baseline | Threshold (20% tolerance) | Notes |
|-----------|----------|---------------------------|-------|
| QueryRouter Init | [TBD]ms | [TBD]ms | Database connection + initialization |
| LLM Classification | [TBD]ms | [TBD]ms | Full intent classification with LLM |
| Orchestration Flow | [TBD]ms | [TBD]ms | Complete request processing |

## Local Testing

Run performance tests locally before pushing:

```bash
# Run all performance tests
python scripts/run_performance_tests.py

# Check specific component
python scripts/performance_config.py queryrouter_init_ms 45.5
```

## CI Integration

Performance tests run automatically in CI after regular tests pass. Build fails if:
- Any component exceeds baseline threshold by >20%
- Performance test encounters errors
- Critical components become unresponsive

## Updating Baselines

When legitimate performance improvements are made:

1. Measure new performance with local script
2. Update baselines in `scripts/performance_config.py`
3. Document improvement in commit message
4. Update this documentation with new baselines

## Troubleshooting

### Build fails with performance regression:
1. Check CI output for which component failed
2. Run local performance tests to reproduce
3. Investigate recent changes affecting performance
4. If legitimate regression, fix before merging
5. If measurement variance, re-run CI (rare)

### Performance tests error:
1. Check database connectivity
2. Verify LLM service availability
3. Review recent infrastructure changes
4. Check component initialization

## Monitoring

Track performance trends over time:
- CI logs include timing measurements
- Baseline updates documented in commits
- Performance improvements tracked in changelogs
EOF

echo "Performance enforcement documentation created"
```

## Evidence Collection Requirements

### CI Integration Status
```
=== Performance Enforcement CI Integration ===
CI configuration file: [.github/workflows/test.yml or other]
Performance job added: [YES/NO]
Dependencies configured: [CORRECT/NEEDS_ADJUSTMENT]
Baseline integration: [WORKING/NEEDS_PHASE_1A_DATA]

Test configuration:
- QueryRouter initialization: [threshold in ms]
- LLM classification: [threshold in ms]
- Orchestration flow: [threshold in ms]

CI job status: [READY_TO_TEST/NEEDS_REFINEMENT]
```

### Local Testing Infrastructure
```
=== Local Performance Testing ===
Local testing script: [CREATED/NEEDS_WORK]
Performance config module: [WORKING/NEEDS_UPDATES]
Baseline integration: [READY/WAITING_FOR_PHASE_1A]

Script functionality:
- Multiple test runs: [IMPLEMENTED/MISSING]
- Baseline comparison: [WORKING/NEEDS_CONFIG]
- Clear reporting: [GOOD/NEEDS_IMPROVEMENT]

Ready for local testing: [YES/NO]
```

### Documentation Status
```
=== Performance Enforcement Documentation ===
Documentation created: [YES/NO]
Usage instructions: [CLEAR/NEEDS_IMPROVEMENT]
Troubleshooting guide: [COMPLETE/BASIC]
Baseline update process: [DOCUMENTED/MISSING]

Documentation quality: [COMPREHENSIVE/BASIC/NEEDS_WORK]
Developer guidance: [CLEAR/CONFUSING]
```

## Success Criteria
- [ ] Performance enforcement integrated into CI pipeline
- [ ] Realistic thresholds ready for Phase 1A baseline data
- [ ] Local testing script created for pre-push validation
- [ ] CI job configured to fail build on meaningful regressions
- [ ] Documentation created for team usage and troubleshooting
- [ ] Framework ready for testing with actual baseline measurements

## Time Estimate
35-40 minutes for complete enforcement implementation

## Critical Dependencies
**Phase 1A baseline data**: Thresholds will be updated with actual measurements from Code's assessment
**CI system compatibility**: Implementation assumes GitHub Actions workflow structure
**Database availability**: Performance tests require database connectivity

**Deliverable**: Complete performance enforcement framework ready for integration with Phase 1A baseline measurements

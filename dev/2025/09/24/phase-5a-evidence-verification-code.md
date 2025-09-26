# Agent Prompt: Phase 5A - Evidence Verification Testing

**Agent**: Code  
**Mission**: Run specific tests mentioned in GREAT-1C acceptance criteria and provide verifiable terminal output as evidence for each claim.

## Context
- **Agents have claimed**: Tests passing, performance under 500ms, resilient parsing working
- **PM requirement**: Evidence-based verification with actual terminal output before checking any boxes
- **Standard**: Agent claims without evidence are insufficient for acceptance criteria validation

## GREAT-1C Evidence Verification Tasks

### 1. Performance Test Evidence (Critical)
```bash
# Run the exact performance test mentioned in acceptance criteria
echo "=== Performance Test: <500ms Validation ==="
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

# Also run the broader performance benchmark suite
echo ""
echo "=== LLM Classifier Performance Benchmarks ==="
PYTHONPATH=. python -m pytest tests/performance/test_llm_classifier_benchmarks.py -xvs

# Capture timing details
echo ""
echo "=== Detailed Performance Analysis ==="
time PYTHONPATH=. python3 -c "
import asyncio
import time
from services.intent_service.llm_classifier import LLMClassifier

async def measure_performance():
    classifier = LLMClassifier()
    times = []
    
    for i in range(5):
        start = time.time()
        result = await classifier.classify('Create a GitHub issue about the login bug')
        duration = (time.time() - start) * 1000
        times.append(duration)
        print(f'Test {i+1}: {duration:.1f}ms - {result.category if hasattr(result, \"category\") else \"N/A\"}')
    
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    
    print(f'Average: {avg_time:.1f}ms')
    print(f'Maximum: {max_time:.1f}ms') 
    print(f'Minimum: {min_time:.1f}ms')
    print(f'<500ms requirement: {\"PASSED\" if max_time < 500 else \"FAILED\"}')

asyncio.run(measure_performance())
"
```

### 2. Integration Test Evidence
```bash
# Find and run orchestration pipeline integration tests
echo "=== Finding Orchestration Integration Tests ==="
find tests/ -name "*.py" -exec grep -l "orchestration\|pipeline\|integration" {} \;

# Run integration tests specifically
echo ""
echo "=== Integration Tests Execution ==="
PYTHONPATH=. python -m pytest tests/ -k "integration" -v

# Run orchestration-specific tests
echo ""
echo "=== Orchestration Module Tests ==="
PYTHONPATH=. python -m pytest tests/ -k "orchestration" -v

# Run any end-to-end workflow tests
echo ""
echo "=== End-to-End Workflow Tests ==="
PYTHONPATH=. python -m pytest tests/ -k "e2e\|end_to_end\|workflow" -v
```

### 3. Error Scenario Test Evidence
```bash
# Find and run error scenario tests
echo "=== Error Scenario Tests ==="
find tests/ -name "*.py" -exec grep -l "error\|exception\|fail" {} \;

# Run error handling tests
echo ""
echo "=== Error Handling Test Execution ==="
PYTHONPATH=. python -m pytest tests/ -k "error" -v

# Test specific error scenarios for LLM classifier
echo ""
echo "=== LLM Classifier Error Scenarios ==="
PYTHONPATH=. python3 -c "
import asyncio
from services.intent_service.llm_classifier import LLMClassifier

async def test_error_scenarios():
    classifier = LLMClassifier()
    
    # Test empty message
    try:
        result = await classifier.classify('')
        print('Empty message: SUCCESS -', result)
    except Exception as e:
        print('Empty message: ERROR -', str(e))
    
    # Test very long message
    try:
        long_msg = 'Create issue ' * 1000
        result = await classifier.classify(long_msg)
        print('Long message: SUCCESS -', result.category if hasattr(result, 'category') else 'N/A')
    except Exception as e:
        print('Long message: ERROR -', str(e))
    
    # Test special characters
    try:
        result = await classifier.classify('Create issue with special chars: @#$%^&*()')
        print('Special chars: SUCCESS -', result.category if hasattr(result, 'category') else 'N/A')
    except Exception as e:
        print('Special chars: ERROR -', str(e))

asyncio.run(test_error_scenarios())
"
```

### 4. Test Coverage Evidence
```bash
# Generate coverage report for orchestration module
echo "=== Test Coverage Analysis ==="

# Install coverage if needed
pip install coverage --break-system-packages --quiet

# Run tests with coverage
echo "Running tests with coverage measurement..."
PYTHONPATH=. coverage run --source=services/orchestration -m pytest tests/ -v

# Generate coverage report
echo ""
echo "=== Coverage Report ==="
coverage report

# Generate detailed coverage for orchestration module
echo ""
echo "=== Detailed Orchestration Coverage ==="
coverage report --include="services/orchestration/*"

# Show missing lines
echo ""
echo "=== Missing Coverage Details ==="
coverage report --include="services/orchestration/*" --show-missing
```

### 5. Regression Prevention Evidence
```bash
# Check for locking mechanisms mentioned in acceptance criteria
echo "=== Regression Prevention Verification ==="

# Check CI/CD configuration
echo "CI/CD Configuration:"
find . -name "*.yml" -o -name "*.yaml" | grep -i ci
if [ -f ".github/workflows/test.yml" ]; then
    echo "Found GitHub Actions config:"
    cat .github/workflows/test.yml
fi

# Check for pre-commit hooks
echo ""
echo "Pre-commit Hook Configuration:"
if [ -f ".pre-commit-config.yaml" ]; then
    echo "Found pre-commit config:"
    cat .pre-commit-config.yaml
else
    echo "No pre-commit config found"
fi

# Check for specific regression tests
echo ""
echo "Regression Test Files:"
find tests/ -name "*regression*" -o -name "*lock*"

# Run regression tests if they exist
if [ -d "tests/regression" ]; then
    echo ""
    echo "=== Regression Test Execution ==="
    PYTHONPATH=. python -m pytest tests/regression/ -v
fi
```

### 6. QueryRouter Initialization Evidence
```bash
# Verify QueryRouter is properly initialized and connected
echo "=== QueryRouter Initialization Verification ==="

PYTHONPATH=. python3 -c "
import asyncio
from services.orchestration.engine import OrchestrationEngine
from database.session import get_async_session

async def verify_queryrouter():
    async with get_async_session() as session:
        try:
            engine = OrchestrationEngine(session)
            
            print('OrchestrationEngine initialization: SUCCESS')
            
            # Check if QueryRouter is initialized
            if hasattr(engine, 'query_router') and engine.query_router is not None:
                print('QueryRouter initialization: SUCCESS')
                print(f'QueryRouter type: {type(engine.query_router)}')
                
                # Test routing capability
                if hasattr(engine.query_router, 'route'):
                    print('QueryRouter routing capability: AVAILABLE')
                else:
                    print('QueryRouter routing capability: MISSING')
            else:
                print('QueryRouter initialization: FAILED - not initialized')
                
        except Exception as e:
            print(f'OrchestrationEngine initialization: FAILED - {e}')

asyncio.run(verify_queryrouter())
"
```

### 7. Complete Test Suite Evidence
```bash
# Run all tests and capture complete output
echo "=== Complete Test Suite Execution ==="

# Run all tests with verbose output
PYTHONPATH=. python -m pytest tests/ -v --tb=short

# Count test results
echo ""
echo "=== Test Suite Summary ==="
PYTHONPATH=. python -m pytest tests/ --tb=no -q | tail -5

# Check for any failing tests
echo ""
echo "=== Failed Test Analysis ==="
PYTHONPATH=. python -m pytest tests/ --tb=no -q --failed-first | head -10
```

## Evidence Collection Requirements

### Performance Evidence
```
=== Performance Test Results ===
Performance Regression Test: [PASSED/FAILED with timing]
Command: pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms
Output: [paste complete terminal output]

LLM Classifier Benchmarks: [X PASSED, X FAILED]
Command: pytest tests/performance/test_llm_classifier_benchmarks.py
Output: [paste complete terminal output]

Individual Performance Measurements:
[paste complete output showing 5 individual timing tests]
Average time: [X]ms vs 500ms requirement
Result: [MEETS/EXCEEDS/FAILS requirement]
```

### Integration Test Evidence
```
=== Integration Test Results ===
Integration Tests Found: [list of test files]
Integration Tests Executed: [number run]
Results: [X PASSED, X FAILED]
Output: [paste pytest integration test output]

Orchestration Tests: [X PASSED, X FAILED]
Output: [paste orchestration-specific test output]
```

### Coverage Evidence
```
=== Test Coverage Results ===
Overall Coverage: [X]%
Orchestration Module Coverage: [X]%
Coverage Requirement: 80%
Meets Requirement: [YES/NO]

Coverage Report:
[paste coverage report output showing orchestration module details]

Missing Coverage:
[paste missing lines report]
```

### Regression Prevention Evidence
```
=== Regression Prevention Status ===
CI/CD Configuration: [FOUND/MISSING]
Pre-commit Hooks: [FOUND/MISSING] 
Regression Tests: [number of tests found]
QueryRouter Lock Test: [FOUND/MISSING]

Regression Test Results: [X PASSED, X FAILED]
Output: [paste regression test output]

Locking Mechanisms Status:
- CI fails if QueryRouter disabled: [YES/NO - evidence]
- Performance regression alerts: [YES/NO - evidence]
- Pre-commit hook for TODOs: [YES/NO - evidence]
```

### Complete Test Suite Evidence
```
=== Complete Test Suite Status ===
Total Tests: [number]
Passed: [number]
Failed: [number]
Skipped: [number]

Overall Result: [PASSING/FAILING]
Test Suite Health: [assessment]

All Tests Output:
[paste complete pytest output summary]
```

## Success Criteria
- [ ] Performance test shows <500ms validation with evidence
- [ ] Integration tests execute and show pipeline functionality
- [ ] Test coverage report shows >80% for orchestration module  
- [ ] Error scenarios are tested and handle gracefully
- [ ] Regression tests exist and prevent QueryRouter disabling
- [ ] Complete test suite shows overall health

## Time Estimate
30-40 minutes for complete evidence collection and verification

## Critical Requirements
**Evidence over claims**: Every checkbox needs terminal output proof
**Specific test execution**: Run the exact tests mentioned in acceptance criteria
**Coverage verification**: Actual coverage report, not estimates
**Complete transparency**: Show failures as well as successes

**Focus: Provide PM with verifiable evidence to make informed decisions about checking acceptance criteria boxes.**

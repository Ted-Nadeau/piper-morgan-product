# Agent Prompt: Phase 1A - Performance Reality Assessment

**Agent**: Code  
**Mission**: Assess current performance reality to establish realistic baselines for enforcement, following Chief Architect's gameplan.

## Context from Chief Architect
- **Approach**: Use realistic thresholds based on actual performance, not aspirational targets
- **Philosophy**: Catch regressions without blocking development with unrealistic standards
- **Baseline needed**: Document current performance as foundation for enforcement

## Phase 1A Assessment Tasks

### 1. Current Performance Baseline Collection
```bash
# Run comprehensive performance assessment
echo "=== Current Performance Reality Assessment ==="

# Test QueryRouter initialization performance
echo "QueryRouter Initialization Performance:"
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.orchestration.engine import OrchestrationEngine
from database.session import get_async_session

async def measure_queryrouter_init():
    times = []
    for i in range(10):
        start = time.time()
        async with get_async_session() as session:
            engine = OrchestrationEngine(session)
            # Measure actual initialization
            if hasattr(engine, 'query_router'):
                init_time = (time.time() - start) * 1000
                times.append(init_time)
                print(f'Run {i+1}: {init_time:.1f}ms')
    
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        print(f'\\nQueryRouter Initialization Baseline:')
        print(f'Average: {avg_time:.1f}ms')
        print(f'Maximum: {max_time:.1f}ms')
        print(f'Minimum: {min_time:.1f}ms')
        print(f'Suggested threshold (max + 20%): {max_time * 1.2:.1f}ms')
        return avg_time, max_time
    else:
        print('QueryRouter initialization measurement failed')
        return None, None

avg, maximum = asyncio.run(measure_queryrouter_init())
"

# Test LLM classification performance
echo ""
echo "LLM Classification Performance:"
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.intent_service.llm_classifier import LLMClassifier

async def measure_llm_classification():
    classifier = LLMClassifier()
    test_messages = [
        'Create a GitHub issue about the login bug',
        'List all open projects',
        'Update task status to completed'
    ]
    
    times = []
    for i, msg in enumerate(test_messages):
        try:
            start = time.time()
            result = await classifier.classify(msg)
            duration = (time.time() - start) * 1000
            times.append(duration)
            print(f'Message {i+1}: {duration:.0f}ms - {result.category if hasattr(result, \"category\") else \"N/A\"}')
        except Exception as e:
            print(f'Message {i+1}: FAILED - {e}')
    
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        print(f'\\nLLM Classification Baseline:')
        print(f'Average: {avg_time:.0f}ms')
        print(f'Maximum: {max_time:.0f}ms')
        print(f'Minimum: {min_time:.0f}ms')
        print(f'Suggested threshold (max + 20%): {max_time * 1.2:.0f}ms')
        return avg_time, max_time
    else:
        print('LLM classification measurement failed')
        return None, None

avg, maximum = asyncio.run(measure_llm_classification())
"

# Test full orchestration flow performance
echo ""
echo "Full Orchestration Flow Performance:"
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.orchestration.engine import OrchestrationEngine
from database.session import get_async_session

async def measure_orchestration_flow():
    times = []
    test_inputs = [
        'Create a GitHub issue about performance',
        'List current projects'
    ]
    
    for i, user_input in enumerate(test_inputs):
        try:
            async with get_async_session() as session:
                engine = OrchestrationEngine(session)
                
                start = time.time()
                result = await engine.process_request(user_input)
                duration = (time.time() - start) * 1000
                times.append(duration)
                print(f'Flow {i+1}: {duration:.0f}ms - Success')
        except Exception as e:
            print(f'Flow {i+1}: FAILED - {e}')
    
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        print(f'\\nFull Orchestration Flow Baseline:')
        print(f'Average: {avg_time:.0f}ms')
        print(f'Maximum: {max_time:.0f}ms') 
        print(f'Minimum: {min_time:.0f}ms')
        print(f'Suggested threshold (max + 20%): {max_time * 1.2:.0f}ms')
        return avg_time, max_time
    else:
        print('Orchestration flow measurement failed')
        return None, None

avg, maximum = asyncio.run(measure_orchestration_flow())
"
```

### 2. Existing Performance Test Analysis
```bash
# Analyze current performance tests to understand what they measure
echo "=== Existing Performance Test Analysis ==="

# Find performance test files
echo "Performance test files found:"
find tests/ -name "*performance*" -o -name "*benchmark*" | head -10

# Analyze what current performance tests measure
echo ""
echo "Current performance test content:"
find tests/ -name "*performance*" -exec grep -l "def test_" {} \; | head -3 | while read file; do
    echo "File: $file"
    grep -A 5 "def test_" "$file" | head -20
    echo ""
done

# Check for existing timing assertions
echo ""
echo "Existing timing assertions:"
grep -r "assert.*time\|assert.*duration\|benchmark" tests/performance/ --include="*.py" | head -10

# Check for pytest-benchmark usage
echo ""
echo "Pytest-benchmark usage:"
grep -r "benchmark\|@pytest.mark.benchmark" tests/ --include="*.py" | head -5
```

### 3. Performance Test Infrastructure Assessment
```bash
# Check current test running capability
echo "=== Performance Test Infrastructure Assessment ==="

# Run existing performance tests to see current behavior
echo "Running existing performance tests:"
PYTHONPATH=. python -m pytest tests/performance/ -v --tb=short | head -20

# Check if performance tests have any timing requirements
echo ""
echo "Performance test results summary:"
PYTHONPATH=. python -m pytest tests/performance/ --tb=no -q 2>/dev/null | tail -5

# Check what performance infrastructure is available
echo ""
echo "Available performance testing tools:"
pip list | grep -E "(benchmark|performance|timing)" || echo "No specific performance testing packages found"

# Test if pytest-benchmark is available and working
echo ""
echo "Testing pytest-benchmark availability:"
PYTHONPATH=. python3 -c "
try:
    import pytest_benchmark
    print('pytest-benchmark is available')
except ImportError:
    print('pytest-benchmark not installed')
    
try:
    import time
    # Simulate benchmark test
    def test_function():
        time.sleep(0.001)  # 1ms
        return True
    
    start = time.time()
    result = test_function()
    duration = (time.time() - start) * 1000
    print(f'Sample timing test: {duration:.2f}ms')
except Exception as e:
    print(f'Timing test failed: {e}')
"
```

### 4. Realistic Baseline Documentation
```bash
# Create baseline documentation based on measurements
echo "=== Creating Performance Baseline Documentation ==="

# Generate baseline configuration
cat > /tmp/performance_baselines.py << 'EOF'
#!/usr/bin/env python3
"""
Performance Baselines for GREAT-1C Enforcement
Generated: $(date)

These baselines represent ACTUAL measured performance,
not aspirational targets. Enforcement allows 20% degradation
to catch significant regressions without blocking normal variance.
"""

import time
from typing import Dict, Optional

class PerformanceBaselines:
    """Realistic performance baselines for regression detection"""
    
    # Measured baselines (update these with actual measurements)
    BASELINES = {
        "queryrouter_init_ms": 50,      # QueryRouter initialization
        "llm_classification_ms": 2000,   # LLM intent classification  
        "orchestration_flow_ms": 3000,   # Full request processing
    }
    
    # Tolerance: Allow 20% degradation before flagging regression
    TOLERANCE_FACTOR = 1.2
    
    @classmethod
    def check_regression(cls, test_name: str, actual_time_ms: float) -> bool:
        """
        Check if performance represents a regression
        
        Args:
            test_name: Name of the performance test
            actual_time_ms: Actual measured time in milliseconds
            
        Returns:
            True if performance is acceptable, False if regression detected
        """
        baseline = cls.BASELINES.get(test_name)
        if baseline is None:
            print(f"Warning: No baseline for {test_name}, allowing by default")
            return True
            
        threshold = baseline * cls.TOLERANCE_FACTOR
        is_acceptable = actual_time_ms <= threshold
        
        if not is_acceptable:
            print(f"PERFORMANCE REGRESSION DETECTED:")
            print(f"  Test: {test_name}")
            print(f"  Baseline: {baseline}ms")
            print(f"  Threshold: {threshold}ms") 
            print(f"  Actual: {actual_time_ms}ms")
            print(f"  Regression: {((actual_time_ms / baseline) - 1) * 100:.1f}%")
        
        return is_acceptable
    
    @classmethod
    def update_baseline(cls, test_name: str, new_baseline_ms: float):
        """Update baseline after legitimate performance improvement"""
        cls.BASELINES[test_name] = new_baseline_ms
        print(f"Updated {test_name} baseline to {new_baseline_ms}ms")

def measure_and_check(test_name: str, test_function, *args, **kwargs) -> bool:
    """Measure function execution and check against baseline"""
    start_time = time.time()
    result = test_function(*args, **kwargs)
    duration_ms = (time.time() - start_time) * 1000
    
    is_acceptable = PerformanceBaselines.check_regression(test_name, duration_ms)
    return is_acceptable

if __name__ == "__main__":
    # Example usage
    def example_test():
        time.sleep(0.05)  # 50ms
    
    # This would pass (50ms vs 50ms baseline + 20% tolerance)
    result = measure_and_check("queryrouter_init_ms", example_test)
    print(f"Test result: {'PASS' if result else 'FAIL'}")
EOF

echo "Performance baseline framework created at /tmp/performance_baselines.py"
echo ""
echo "Contents preview:"
head -30 /tmp/performance_baselines.py
```

## Evidence Collection Requirements

### Performance Baseline Measurements
```
=== Performance Reality Assessment Results ===
QueryRouter Initialization:
- Average: [X]ms
- Maximum: [X]ms  
- Suggested threshold: [X]ms (max + 20%)

LLM Classification:
- Average: [X]ms
- Maximum: [X]ms
- Suggested threshold: [X]ms (max + 20%)

Full Orchestration Flow:
- Average: [X]ms
- Maximum: [X]ms
- Suggested threshold: [X]ms (max + 20%)

Measurement reliability: [CONSISTENT/VARIABLE]
Baseline suitability: [SUITABLE/NEEDS_ADJUSTMENT]
```

### Existing Test Infrastructure Assessment
```
=== Performance Test Infrastructure Status ===
Performance test files found: [count and locations]
Current test behavior: [TIMING_ASSERTIONS/MEASUREMENT_ONLY/NONE]
pytest-benchmark availability: [INSTALLED/NOT_INSTALLED]
Existing timing requirements: [list or NONE]

Infrastructure readiness: [READY/NEEDS_SETUP]
Required installations: [list or NONE]
```

### Baseline Framework Status
```
=== Performance Baseline Framework ===
Baseline configuration created: [YES/NO]
Realistic thresholds calculated: [YES/NO with values]
Tolerance factor applied: [20% or adjusted value]
Framework testing: [WORKING/NEEDS_FIXES]

Ready for CI integration: [YES/NO]
Missing components: [list or NONE]
```

## Success Criteria
- [ ] Realistic performance baselines measured from actual system
- [ ] Baseline framework created with tolerance for normal variance
- [ ] Existing performance test infrastructure assessed
- [ ] Clear understanding of current measurement capabilities
- [ ] Foundation ready for Phase 1B enforcement implementation

## Time Estimate
25-30 minutes for comprehensive performance reality assessment

## Critical Focus
**Reality over aspiration**: Document what the system actually does, not what we wish it did
**Variance tolerance**: Account for normal performance variation in thresholds
**Practical enforcement**: Create baselines that catch real regressions without false positives

**Deliverable**: Realistic performance baselines ready for enforcement implementation in Phase 1B

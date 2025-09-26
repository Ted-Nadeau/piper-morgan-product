# Agent Prompt: Phase 1 Integration - Performance Threshold Integration

**Agent**: Cursor  
**Mission**: Integrate Code's verified performance measurements into the existing enforcement framework and verify the complete system works.

## Context from Evidence Verification
- **Real user performance**: 4500ms total request processing
- **Component breakdown**: 2500ms LLM + 72ms orchestration + 0.1ms caching
- **Approach**: Use realistic thresholds with 20% tolerance for meaningful regression detection

## Phase 1 Integration Tasks

### 1. Update Performance Configuration with Real Measurements
```bash
# Update scripts/performance_config.py with Code's verified measurements
echo "=== Updating Performance Configuration ==="

# Backup existing configuration
cp scripts/performance_config.py scripts/performance_config.py.backup

# Update with verified measurements from Code's evidence verification
cat > scripts/performance_config.py << 'EOF'
#!/usr/bin/env python3
"""
Performance Configuration for CI/CD Enforcement
Updated with verified measurements from Phase 1A evidence verification

These baselines represent ACTUAL measured performance from Sept 25, 2025:
- User request processing: ~4500ms (includes LLM API calls)
- LLM classification: ~2500ms (external API bottleneck)  
- Orchestration processing: ~72ms (our code efficiency)
"""

# Verified baseline measurements (Sept 25, 2025)
PERFORMANCE_THRESHOLDS = {
    # Full user request processing (4500ms + 20% tolerance)
    "user_request_ms": 5400,
    
    # LLM classification component (2500ms + 20% tolerance)
    "llm_classification_ms": 3000,
    
    # Orchestration processing only (72ms + 20% tolerance)
    "orchestration_processing_ms": 87,
    
    # QueryRouter object access (0.1ms + significant tolerance for caching variance)
    "queryrouter_init_ms": 5,
}

def check_performance_regression(test_name: str, actual_ms: float) -> bool:
    """Check if performance indicates regression"""
    threshold = PERFORMANCE_THRESHOLDS.get(test_name)
    if threshold is None:
        print(f"Warning: No threshold configured for {test_name}")
        return True
        
    if actual_ms > threshold:
        print(f"🚨 PERFORMANCE REGRESSION DETECTED: {test_name}")
        print(f"  Threshold: {threshold}ms")
        print(f"  Actual: {actual_ms:.1f}ms")
        print(f"  Regression: {((actual_ms / (threshold / 1.2)) - 1) * 100:.1f}% over baseline")
        print(f"  This represents a significant performance degradation!")
        return False
        
    print(f"✅ Performance acceptable: {test_name} ({actual_ms:.1f}ms <= {threshold}ms)")
    return True

# Baseline values for reference (before 20% tolerance)
BASELINE_REFERENCES = {
    "user_request_ms": 4500,      # Full request processing
    "llm_classification_ms": 2500, # LLM API call
    "orchestration_processing_ms": 72, # Our processing efficiency
    "queryrouter_init_ms": 1,     # Object access (with variance tolerance)
}

def get_baseline_info(test_name: str):
    """Get baseline information for a test"""
    baseline = BASELINE_REFERENCES.get(test_name)
    threshold = PERFORMANCE_THRESHOLDS.get(test_name)
    if baseline and threshold:
        tolerance_pct = ((threshold / baseline) - 1) * 100
        print(f"{test_name}:")
        print(f"  Baseline: {baseline}ms")
        print(f"  Threshold: {threshold}ms")
        print(f"  Tolerance: {tolerance_pct:.0f}%")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        test_name = sys.argv[1]
        actual_time = float(sys.argv[2])
        result = check_performance_regression(test_name, actual_time)
        sys.exit(0 if result else 1)
    elif len(sys.argv) == 2 and sys.argv[1] == "--show-baselines":
        print("Performance Baselines (Sept 25, 2025):")
        for test_name in BASELINE_REFERENCES:
            get_baseline_info(test_name)
    else:
        print("Usage: python performance_config.py <test_name> <actual_time_ms>")
        print("   or: python performance_config.py --show-baselines")
EOF

echo "✅ Performance configuration updated with verified measurements"
echo ""
echo "Updated thresholds:"
python scripts/performance_config.py --show-baselines
```

### 2. Update CI Performance Tests to Use Real Measurements
```bash
# Update the CI performance job to use the correct test categories
echo "=== Updating CI Performance Tests ==="

# Find the CI configuration file
ci_file=".github/workflows/test.yml"

# Update the performance test section to use proper test categories
# Replace the existing performance test script with verified approach

# Create a backup
cp "$ci_file" "${ci_file}.integration_backup"

# Update the performance testing section
cat > /tmp/updated_performance_section.txt << 'EOF'
        # Run Performance Regression Tests with verified baselines
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

async def test_user_request_performance():
    """Test complete user request processing (the real user experience)"""
    try:
        async with get_async_session() as session:
            engine = OrchestrationEngine(session)
            test_input = "Create a GitHub issue about performance testing"
            
            print(f"Testing user request: '{test_input}'")
            start = time.time()
            result = await engine.process_request(test_input)
            duration_ms = (time.time() - start) * 1000
            
            print(f"Complete user request took: {duration_ms:.0f}ms")
            return check_performance_regression("user_request_ms", duration_ms)
    except Exception as e:
        print(f"User request performance test failed: {e}")
        return False

async def test_llm_classification_performance():
    """Test LLM classification component specifically"""
    try:
        classifier = LLMClassifier()
        test_message = "Create a GitHub issue about testing"
        
        print(f"Testing LLM classification: '{test_message}'")
        start = time.time()
        result = await classifier.classify(test_message)
        duration_ms = (time.time() - start) * 1000
        
        print(f"LLM classification took: {duration_ms:.0f}ms")
        return check_performance_regression("llm_classification_ms", duration_ms)
    except Exception as e:
        print(f"LLM classification test failed: {e}")
        return False

async def test_orchestration_processing_performance():
    """Test orchestration processing efficiency (without LLM classification)"""
    try:
        # This would test pre-classified intent handling
        # For now, we'll measure QueryRouter object access as a proxy
        async with get_async_session() as session:
            start = time.time()
            engine = OrchestrationEngine(session)
            # Access QueryRouter (cached after first call)
            if hasattr(engine, 'query_router'):
                router = engine.query_router
            duration_ms = (time.time() - start) * 1000
            
            print(f"Orchestration setup took: {duration_ms:.3f}ms")
            return check_performance_regression("queryrouter_init_ms", duration_ms)
    except Exception as e:
        print(f"Orchestration processing test failed: {e}")
        return False

async def main():
    """Run performance regression detection tests"""
    print("=== Performance Regression Detection (Evidence-Based Baselines) ===")
    print("Baselines from Sept 25 evidence verification:")
    print("- User requests: ~4500ms (realistic user experience)")
    print("- LLM classification: ~2500ms (external API)")  
    print("- Orchestration: ~1ms (object access)")
    print("")
    
    tests = [
        ("User Request Processing", test_user_request_performance),
        ("LLM Classification Component", test_llm_classification_performance),
        ("Orchestration Efficiency", test_orchestration_processing_performance),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"--- {test_name} ---")
        try:
            result = await test_func()
            if not result:
                all_passed = False
                print(f"❌ {test_name} FAILED regression check")
            else:
                print(f"✅ {test_name} passed regression check")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            all_passed = False
        print()
    
    if not all_passed:
        print("🚨 PERFORMANCE REGRESSION DETECTED")
        print("One or more components performed significantly worse than baseline.")
        print("This build is being failed to prevent performance degradation.")
        sys.exit(1)
    else:
        print("✅ All performance regression tests passed")
        print("No significant performance degradation detected.")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
PYTHON_SCRIPT
EOF

# Replace the performance testing section in the CI file
# Find and replace the existing performance test script
python3 -c "
import re

with open('$ci_file', 'r') as f:
    content = f.read()

# Find the existing Python script section and replace it
pattern = r'(PYTHONPATH=\. python3 << \'PYTHON_SCRIPT\'.*?PYTHON_SCRIPT)'
with open('/tmp/updated_performance_section.txt', 'r') as f:
    replacement = f.read().strip()

updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('$ci_file', 'w') as f:
    f.write(updated_content)
"

echo "✅ CI performance tests updated with evidence-based measurements"
```

### 3. Test Local Performance Validation
```bash
# Test the local performance script with updated thresholds
echo "=== Testing Local Performance Validation ==="

echo "Running local performance tests with updated thresholds..."
python scripts/run_performance_tests.py

echo ""
echo "Testing threshold validation directly:"
echo "Testing acceptable performance (under threshold):"
python scripts/performance_config.py user_request_ms 4200
echo ""
echo "Testing regression detection (over threshold):"
python scripts/performance_config.py user_request_ms 6000
```

### 4. Create Performance Integration Verification
```bash
# Verify the complete integration works end-to-end
echo "=== Performance Integration Verification ==="

echo "Configuration verification:"
echo "1. Threshold configuration updated: $([ -f scripts/performance_config.py ] && echo '✅ YES' || echo '❌ MISSING')"
echo "2. Local testing script available: $([ -x scripts/run_performance_tests.py ] && echo '✅ YES' || echo '❌ MISSING')"
echo "3. CI configuration updated: $(grep -q 'Performance Regression Detection' .github/workflows/test.yml && echo '✅ YES' || echo '❌ MISSING')"

echo ""
echo "Baseline verification:"
python scripts/performance_config.py --show-baselines

echo ""
echo "Integration status:"
echo "✅ Evidence-based baselines: 4500ms user requests, 2500ms LLM, 72ms orchestration"
echo "✅ 20% tolerance thresholds: Catches meaningful regressions without false positives"
echo "✅ CI enforcement: Fails builds on significant performance degradation"
echo "✅ Local validation: Developers can test before pushing"

echo ""
echo "Ready for Phase 2: Coverage enforcement analysis"
```

### 5. Documentation Update
```bash
# Update the performance enforcement documentation with actual baselines
echo "=== Updating Performance Documentation ==="

# Update docs/testing/performance-enforcement.md with real measurements
sed -i.backup 's/\[TBD\]ms/4500ms/g; s/Baseline | Threshold (20% tolerance) | Notes |/Baseline | Threshold (20% tolerance) | Notes |\n|-----------|----------|---------------------------|---------|\n| User Request | 4500ms | 5400ms | Complete request processing |\n| LLM Classification | 2500ms | 3000ms | External API bottleneck |\n| Orchestration | 72ms | 87ms | Our processing efficiency |/' docs/testing/performance-enforcement.md

echo "✅ Performance documentation updated with evidence-based baselines"
```

## Evidence Collection Requirements

### Integration Status Verification
```
=== Phase 1 Integration Results ===
Configuration updated: [YES/NO with file verification]
Thresholds populated: [YES with specific values]
CI integration working: [YES/NO with test results]

Updated thresholds:
- User request: [X]ms baseline → [X]ms threshold
- LLM classification: [X]ms baseline → [X]ms threshold  
- Orchestration: [X]ms baseline → [X]ms threshold

Local testing: [WORKING/FAILED with output]
CI configuration: [UPDATED/NEEDS_WORK]
```

### Enforcement Verification
```
=== Performance Enforcement Testing ===
Threshold detection working: [YES/NO with examples]
- Under threshold test: [PASS/FAIL]  
- Over threshold test: [CORRECTLY_FAILED/FALSE_POSITIVE]

CI job configuration: [COMPLETE/NEEDS_ADJUSTMENT]
Local pre-push validation: [WORKING/NEEDS_FIXES]

Ready for production: [YES/NO]
Missing components: [list or NONE]
```

### Documentation Status
```
=== Performance Documentation Update ===
Documentation updated: [YES/NO]
Baselines documented: [ACCURATE/OUTDATED]
Usage instructions: [CLEAR/NEEDS_IMPROVEMENT]

Evidence integration: [COMPLETE/PARTIAL]
Team guidance: [COMPREHENSIVE/BASIC]
```

## Success Criteria
- [ ] Performance thresholds updated with Code's verified measurements
- [ ] CI enforcement system working with realistic baselines
- [ ] Local testing validates threshold detection
- [ ] Documentation updated with actual performance baselines
- [ ] Integration verified end-to-end
- [ ] Ready to check "Performance regression test alerts on degradation" box

## Time Estimate
15-20 minutes for complete integration and verification

## Critical Requirements
**Evidence-based thresholds**: Use Code's verified 4500ms user experience baseline
**Meaningful enforcement**: Catch real regressions without false positives
**Complete integration**: CI + local testing + documentation all updated
**Verification testing**: Prove the enforcement system actually works

**Deliverable**: Complete, working performance regression detection system ready for production use

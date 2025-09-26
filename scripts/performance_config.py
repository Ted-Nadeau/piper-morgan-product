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
    "user_request_ms": 4500,  # Full request processing
    "llm_classification_ms": 2500,  # LLM API call
    "orchestration_processing_ms": 72,  # Our processing efficiency
    "queryrouter_init_ms": 1,  # Object access (with variance tolerance)
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

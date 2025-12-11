#!/usr/bin/env python3
"""
Validate smoke test suite performance and pass rate.
Phase 2b: Smoke Test Marking & Validation
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list, timeout_sec: int = 300) -> tuple:
    """Run command and return (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd="/Users/xian/Development/piper-morgan",
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout_sec}s"
    except Exception as e:
        return -2, "", str(e)


def count_smoke_markers() -> int:
    """Count existing smoke markers in codebase."""
    rc, out, err = run_command(
        ["grep", "-r", "@pytest.mark.smoke", "tests/", "--include=*.py"], timeout_sec=30
    )

    if rc == 0:
        return len(out.strip().split("\n"))
    return 0


def validate_smoke_suite() -> dict:
    """Run smoke suite and collect metrics."""
    print("\n" + "=" * 80)
    print("Smoke Suite Validation")
    print("=" * 80)

    results = {
        "timestamp": datetime.now().isoformat(),
        "markers_found": 0,
        "collection_status": None,
        "collection_count": 0,
        "execution_status": None,
        "execution_time": None,
        "pass_count": 0,
        "fail_count": 0,
        "skip_count": 0,
        "errors": [],
    }

    # Step 1: Count markers
    print("\n1. Counting smoke markers...")
    results["markers_found"] = count_smoke_markers()
    print(f"   Found {results['markers_found']} @pytest.mark.smoke decorators")

    # Step 2: Collect smoke tests
    print("\n2. Collecting smoke tests...")
    rc, out, err = run_command(
        ["python", "-m", "pytest", "-m", "smoke", "--collect-only", "-q"], timeout_sec=120
    )

    if rc == 0:
        results["collection_status"] = "✓ Success"
        # Parse collection output
        lines = out.split("\n")
        for line in lines:
            # Look for patterns like "123 tests collected" or "123 tests"
            match = re.search(r"(\d+)\s+tests?(?:\s+collected)?", line)
            if match:
                results["collection_count"] = int(match.group(1))
                break

        if results["collection_count"] == 0:
            # Try to count from stderr
            match = re.search(r"collected (\d+) item", err)
            if match:
                results["collection_count"] = int(match.group(1))

        print(f"   ✓ Collected {results['collection_count']} tests")
    else:
        results["collection_status"] = "✗ Failed"
        results["errors"].append(f"Collection failed: {err[:200]}")
        print(f"   ✗ Collection failed")
        print(f"   Error: {err[:500]}")

    # Step 3: Run smoke suite with timing
    print("\n3. Running smoke suite (timing execution)...")
    import time

    start_time = time.time()

    rc, out, err = run_command(
        ["python", "-m", "pytest", "-m", "smoke", "-v", "--tb=short"], timeout_sec=120
    )

    elapsed = time.time() - start_time
    results["execution_time"] = elapsed

    if rc == 0:
        results["execution_status"] = "✓ All tests passed"
        print(f"   ✓ All tests passed in {elapsed:.2f}s")
    else:
        results["execution_status"] = "✗ Some tests failed"
        print(f"   ✗ Some tests failed in {elapsed:.2f}s")

    # Parse results from output
    match = re.search(r"(\d+)\s+passed", out)
    if match:
        results["pass_count"] = int(match.group(1))

    match = re.search(r"(\d+)\s+failed", out)
    if match:
        results["fail_count"] = int(match.group(1))

    match = re.search(r"(\d+)\s+skipped", out)
    if match:
        results["skip_count"] = int(match.group(1))

    # Check if execution was under 5 seconds
    if elapsed < 5.0:
        results["performance_status"] = "✓ Under 5s target"
        print(f"   ✓ Execution under 5s target ({elapsed:.2f}s)")
    else:
        results["performance_status"] = f"✗ Over 5s target ({elapsed:.2f}s)"
        print(f"   ✗ Execution over 5s target ({elapsed:.2f}s)")
        results["errors"].append(f"Execution time: {elapsed:.2f}s (target: <5s)")

    # Summary
    print("\n" + "=" * 80)
    print("Validation Summary")
    print("=" * 80)
    print(f"  Markers found:     {results['markers_found']}")
    print(f"  Tests collected:   {results['collection_count']}")
    print(f"  Pass count:        {results['pass_count']}")
    print(f"  Fail count:        {results['fail_count']}")
    print(f"  Skip count:        {results['skip_count']}")
    print(f"  Execution time:    {results['execution_time']:.2f}s")
    print(f"  Collection status: {results['collection_status']}")
    print(f"  Execution status:  {results['execution_status']}")
    print(f"  Performance:       {results.get('performance_status', 'Unknown')}")

    if results["errors"]:
        print(f"\n  Errors:")
        for error in results["errors"]:
            print(f"    - {error}")

    print("=" * 80 + "\n")

    return results


if __name__ == "__main__":
    results = validate_smoke_suite()

    # Exit with error if validation failed
    success = (
        results["execution_status"] == "✓ All tests passed" and results["execution_time"] < 5.0
    )

    sys.exit(0 if success else 1)

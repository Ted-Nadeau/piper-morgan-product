#!/usr/bin/env python3
"""
Profile unit tests to identify fast tests (<500ms) for smoke test marking.

Runs all tests once with --durations=0 to capture execution times.
Parses output to extract timing for each test.

Output: test_profile.json with complete timing data
"""

import json
import re
import subprocess
import sys
import time


def run_all_tests_with_durations():
    """
    Run all unit tests with pytest --durations=0 to capture all timings.
    Returns dict with test profiles and statistics.
    """
    print("Unit Test Profiler")
    print("=" * 70)
    print("Running all 705 unit tests to capture execution timing...")
    print("(This will take 5-10 minutes)")
    print()

    start_time = time.time()

    # Run with --durations=0 and -vv to see all test timings
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/unit",
            "-vv",
            "--durations=0",
            "--tb=no",
            "-p",
            "no:cacheprovider",
        ],
        cwd="/Users/xian/Development/piper-morgan",
        capture_output=True,
        text=True,
        timeout=3600,
    )

    elapsed_seconds = time.time() - start_time

    # Parse output to extract all tests and their durations
    tests = []
    output_lines = result.stdout.split("\n")

    # First, collect all test results with their durations
    # Pattern: "tests/unit/file.py::TestClass::test_method 0.12s PASSED"
    for line in output_lines:
        line = line.strip()

        # Skip header/footer lines
        if not line or "=" in line or "passed" in line or "failed" in line:
            continue

        # Match test lines: they contain :: and PASSED/FAILED
        if "::" in line and ("PASSED" in line or "FAILED" in line):
            try:
                # Extract components
                # Format could be:
                # "tests/unit/file.py::Class::method PASSED [100%]"
                # or with durations:
                # "tests/unit/file.py::Class::method 0.12s PASSED"

                # Find test_id (path with ::)
                test_match = re.search(r"(tests/unit/[^\s]+::[^\s]+::[^\s]+)", line)
                if not test_match:
                    test_match = re.search(r"(tests/unit/[^\s]+::[^\s]+)", line)

                if test_match:
                    test_id = test_match.group(1)

                    # Determine status
                    status = "pass" if "PASSED" in line else "fail"

                    # Extract timing - look for pattern like "0.12s"
                    time_match = re.search(r"(\d+\.\d+)s", line)
                    if time_match:
                        time_seconds = float(time_match.group(1))
                        time_ms = time_seconds * 1000
                    else:
                        time_ms = 0

                    # Parse path and function
                    path_parts = test_id.split("::")
                    file_path = path_parts[0]

                    if len(path_parts) == 3:
                        class_name = path_parts[1]
                        function_name = path_parts[2]
                        full_name = f"{class_name}::{function_name}"
                    else:
                        full_name = path_parts[1]

                    tests.append(
                        {
                            "path": file_path,
                            "function": full_name,
                            "time_ms": round(time_ms, 2),
                            "status": status,
                            "test_id": test_id,
                        }
                    )
            except Exception as e:
                # Skip lines we can't parse
                pass

    # If we didn't get timing data from -vv output, try durations section
    if not tests:
        tests = _parse_durations_section(output_lines)

    # If still no tests, collect them without timing
    if not tests:
        print("Warning: Could not parse test timings from output")
        tests = _collect_tests_without_timing()

    print(f"\nTest run completed in {elapsed_seconds:.1f} seconds")
    print(f"Parsed {len(tests)} tests from pytest output")

    return {
        "tests": tests,
        "total_run_time_seconds": elapsed_seconds,
        "full_output": {
            "stdout_lines": len(output_lines),
            "stderr_lines": len(result.stderr.split("\n")),
        },
    }


def _parse_durations_section(lines):
    """
    Parse durations section from pytest output.
    Format: "0.12s setup    tests/unit/file.py::TestClass::test_method"
    """
    tests = []
    in_durations = False

    for line in lines:
        line = line.strip()

        # Check if we're in the durations section
        if "slowest" in line and "durations" in line:
            in_durations = True
            continue

        if in_durations:
            if line.startswith("(") or line.startswith("=") or not line:
                in_durations = False
                continue

            # Parse duration line
            # Format: "0.12s setup    tests/unit/file.py::TestClass::test_method"
            # or: "0.01s         tests/unit/file.py::TestClass::test_method"

            try:
                parts = line.split()
                if len(parts) >= 2 and "s" in parts[0]:
                    time_str = parts[0].rstrip("s")
                    time_seconds = float(time_str)
                    time_ms = time_seconds * 1000

                    # Find test_id - look for "tests/unit/"
                    test_id = None
                    for i, part in enumerate(parts):
                        if part.startswith("tests/unit/"):
                            # Join remaining parts to get full test id
                            test_id = part
                            break

                    if test_id:
                        # Parse test components
                        path_parts = test_id.split("::")
                        file_path = path_parts[0]

                        if len(path_parts) == 3:
                            class_name = path_parts[1]
                            function_name = path_parts[2]
                            full_name = f"{class_name}::{function_name}"
                        else:
                            full_name = path_parts[1] if len(path_parts) > 1 else "unknown"

                        tests.append(
                            {
                                "path": file_path,
                                "function": full_name,
                                "time_ms": round(time_ms, 2),
                                "status": "pass",  # Durations section only shows passed tests
                                "test_id": test_id,
                            }
                        )
            except (ValueError, IndexError):
                pass

    return tests


def _collect_tests_without_timing():
    """
    Fallback: Collect all test names via pytest --collect-only
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit", "--collect-only", "-q"],
        cwd="/Users/xian/Development/piper-morgan",
        capture_output=True,
        text=True,
        timeout=300,
    )

    tests = []
    for line in result.stdout.split("\n"):
        line = line.strip()
        if line and "::" in line and line.startswith("tests/unit/"):
            test_id = line.split(" ")[0]
            path_parts = test_id.split("::")
            file_path = path_parts[0]

            if len(path_parts) == 3:
                class_name = path_parts[1]
                function_name = path_parts[2]
                full_name = f"{class_name}::{function_name}"
            else:
                full_name = path_parts[-1]

            tests.append(
                {
                    "path": file_path,
                    "function": full_name,
                    "time_ms": 0,
                    "status": "unknown",
                    "test_id": test_id,
                }
            )

    return tests


def calculate_statistics(data):
    """Calculate statistics from test profiles."""
    tests = data["tests"]
    times = [t["time_ms"] for t in tests if t.get("time_ms", 0) > 0]

    fast_count = len([t for t in tests if t.get("time_ms", 1000) < 500])
    medium_count = len([t for t in tests if 500 <= t.get("time_ms", 1000) < 1000])
    slow_count = len([t for t in tests if t.get("time_ms", 1000) >= 1000])

    stats = {
        "total_profiled": len(tests),
        "fast_tests_under_500ms": fast_count,
        "medium_tests_500_1000ms": medium_count,
        "slow_tests_over_1000ms": slow_count,
        "min_time_ms": min(times) if times else 0,
        "max_time_ms": max(times) if times else 0,
        "avg_time_ms": round(sum(times) / len(times), 2) if times else 0,
        "total_time_seconds": data.get("total_run_time_seconds", 0),
        "tests_with_timing": len(times),
    }

    return stats


def save_profile_json(data, output_path):
    """Save profile data to JSON file."""
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nProfile JSON saved to: {output_path}")


def print_summary(data):
    """Print summary statistics."""
    stats = data["statistics"]
    print("\n" + "=" * 70)
    print("PROFILING SUMMARY")
    print("=" * 70)
    print(f"Total tests profiled: {stats['total_profiled']}")
    print(f"Tests with timing data: {stats['tests_with_timing']}")
    print(f"  Fast (<500ms):       {stats['fast_tests_under_500ms']} tests")
    print(f"  Medium (500-1000ms): {stats['medium_tests_500_1000ms']} tests")
    print(f"  Slow (>1000ms):      {stats['slow_tests_over_1000ms']} tests")
    if stats["tests_with_timing"] > 0:
        print(f"\nExecution time statistics:")
        print(f"  Min: {stats['min_time_ms']}ms")
        print(f"  Max: {stats['max_time_ms']}ms")
        print(f"  Avg: {stats['avg_time_ms']}ms")
    print(f"  Total run: {stats['total_time_seconds']:.1f}s")
    print("=" * 70)


def main():
    """Main profiling workflow."""
    # Step 1: Run tests with timing
    data = run_all_tests_with_durations()

    # Step 2: Calculate statistics
    data["statistics"] = calculate_statistics(data)

    # Step 3: Save results
    output_path = "/Users/xian/Development/piper-morgan/test_profile.json"
    save_profile_json(data, output_path)

    # Step 4: Print summary
    print_summary(data)


if __name__ == "__main__":
    main()

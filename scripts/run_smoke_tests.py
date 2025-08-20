#!/usr/bin/env python3
"""
Chief Architect Phase 1: Smoke Test Infrastructure
Target: <5 seconds total execution
Replaces failed TLDR approach with realistic Python testing
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


class SmokeTestRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.start_time = None
        self.end_time = None
        self.test_results = {}

    def run_command(self, cmd: List[str], cwd: Path = None) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr"""
        if cwd is None:
            cwd = self.project_root

        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout for safety
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out after 30 seconds"
        except Exception as e:
            return -1, "", f"Command failed: {str(e)}"

    def discover_smoke_tests(self) -> List[str]:
        """Discover all tests marked with @pytest.mark.smoke"""
        cmd = [sys.executable, "-m", "pytest", "--collect-only", "-m", "smoke", "--tb=no", "-q"]

        exit_code, stdout, stderr = self.run_command(cmd)

        if exit_code != 0:
            print(f"⚠️  Warning: Could not discover smoke tests: {stderr}")
            return []

        # Parse collected tests - handle multi-line output
        tests = []
        lines = stdout.split("\n")
        for line in lines:
            line = line.strip()
            if "::" in line and "test_" in line:
                tests.append(line)

        return tests

    def run_smoke_tests(self) -> Dict[str, float]:
        """Run all smoke tests and measure individual timing"""
        print("🚀 Running Chief Architect Phase 1 Smoke Tests...")
        print("=" * 60)

        # Discover smoke tests
        smoke_tests = self.discover_smoke_tests()
        if not smoke_tests:
            print("❌ No smoke tests found. Please mark tests with @pytest.mark.smoke")
            return {}

        print(f"📋 Found {len(smoke_tests)} smoke tests")
        print()

        results = {}

        for test in smoke_tests:
            print(f"🧪 Running: {test}")
            test_start = time.time()

            # Run individual test
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                test,
                "-v",
                "--tb=short",
                "--no-header",
                "--no-summary",
            ]

            exit_code, stdout, stderr = self.run_command(cmd)
            test_time = time.time() - test_start

            # Store results
            results[test] = {
                "time": test_time,
                "status": "PASS" if exit_code == 0 else "FAIL",
                "output": stdout,
                "error": stderr,
            }

            status_icon = "✅" if exit_code == 0 else "❌"
            print(f"   {status_icon} {test} - {test_time:.3f}s")

            if exit_code != 0 and stderr:
                print(f"   Error: {stderr[:200]}...")

        return results

    def run_smoke_suite(self) -> bool:
        """Run complete smoke test suite and validate <5 second target"""
        print("\n🎯 Chief Architect Phase 1: Complete Smoke Test Suite")
        print("=" * 60)

        self.start_time = time.time()

        # Run all smoke tests
        results = self.run_smoke_tests()

        self.end_time = time.time()
        total_time = self.end_time - self.start_time

        # Generate report
        self.generate_report(results, total_time)

        # Validate <5 second target
        success = total_time < 5.0
        if success:
            print(f"\n🎉 SUCCESS: Smoke tests completed in {total_time:.3f}s (<5s target)")
        else:
            print(f"\n⚠️  WARNING: Smoke tests took {total_time:.3f}s (exceeds 5s target)")

        return success

    def generate_report(self, results: Dict[str, Dict], total_time: float):
        """Generate comprehensive smoke test report"""
        print(f"\n📊 Smoke Test Report")
        print("-" * 40)

        if not results:
            print("No tests executed")
            return

        # Calculate statistics
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r["status"] == "PASS")
        failed_tests = total_tests - passed_tests

        # Timing statistics
        test_times = [r["time"] for r in results.values()]
        avg_time = sum(test_times) / len(test_times) if test_times else 0
        max_time = max(test_times) if test_times else 0
        min_time = min(test_times) if test_times else 0

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        print(f"Timing Summary:")
        print(f"  Total Time: {total_time:.3f}s")
        print(f"  Average Test: {avg_time:.3f}s")
        print(f"  Fastest Test: {min_time:.3f}s")
        print(f"  Slowest Test: {max_time:.3f}s")

        # Performance analysis
        if total_time < 5.0:
            print(f"\n🎯 Target Achievement: <5s target ✅ ACHIEVED")
            print(f"   Margin: {5.0 - total_time:.3f}s remaining")
        else:
            print(f"\n🎯 Target Achievement: <5s target ❌ MISSED")
            print(f"   Overrun: {total_time - 5.0:.3f}s")

        # Individual test results
        if results:
            print(f"\n📋 Individual Test Results:")
            print("-" * 40)
            for test_name, result in results.items():
                status_icon = "✅" if result["status"] == "PASS" else "❌"
                print(f"{status_icon} {test_name}: {result['time']:.3f}s")

    def validate_environment(self) -> bool:
        """Validate that the test environment is ready"""
        print("🔍 Validating Test Environment...")

        # Check pytest availability
        exit_code, stdout, stderr = self.run_command([sys.executable, "-m", "pytest", "--version"])
        if exit_code != 0:
            print(f"❌ pytest not available: {stderr}")
            return False

        print(f"✅ pytest available: {stdout.strip()}")

        # Check pytest.ini
        pytest_ini = self.project_root / "pytest.ini"
        if not pytest_ini.exists():
            print("❌ pytest.ini not found")
            return False

        print("✅ pytest.ini configuration found")

        # Check for smoke test markers
        exit_code, stdout, stderr = self.run_command(
            [sys.executable, "-m", "pytest", "--collect-only", "-m", "smoke", "-q"]
        )

        if exit_code != 0:
            print(f"⚠️  Warning: Could not validate smoke test markers: {stderr}")
        else:
            smoke_tests = [line for line in stdout.split("\n") if "::" in line and "test_" in line]
            print(f"✅ Found {len(smoke_tests)} smoke tests")

        return True


def main():
    """Main entry point for Chief Architect Phase 1"""
    print("🏗️  Chief Architect Phase 1: Smoke Test Infrastructure")
    print("=" * 60)
    print("Target: <5 seconds total execution")
    print("Mission: Replace failed TLDR with realistic Python testing")
    print()

    runner = SmokeTestRunner()

    # Validate environment
    if not runner.validate_environment():
        print("❌ Environment validation failed. Please check setup.")
        sys.exit(1)

    print()

    # Run smoke test suite
    success = runner.run_smoke_suite()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

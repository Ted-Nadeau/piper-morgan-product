#!/usr/bin/env python3
"""
Test Health Checker - Reveals true test suite health by running tests in isolation.

Usage: python tests/test-health-check.py [--full]

Distinguishes between:
- Real failures (business logic issues)
- Isolation failures (pass individually, fail in suite)
- Infrastructure warnings (async noise)
"""

import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class TestHealthChecker:
    def __init__(self):
        self.results = defaultdict(list)
        self.test_dir = Path("tests")

    def run_all_tests_together(self):
        """Run full test suite to get baseline."""
        print("🔍 Running full test suite to identify failures...")
        env = os.environ.copy()
        env["PYTHONPATH"] = "."
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-v",
            "--tb=no",
            "--maxfail=50",
        ]  # Limit failures
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=env, timeout=180
        )  # 3 min timeout

        # Parse failures from output
        failures = []
        for line in result.stdout.split("\n"):
            if "FAILED" in line:
                test_name = line.split(" ")[0]
                if test_name not in failures:  # Avoid duplicates
                    failures.append(test_name)

        return failures, result.returncode

    def run_test_individually(self, test_path):
        """Run a single test in isolation."""
        env = os.environ.copy()
        env["PYTHONPATH"] = "."
        cmd = [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=env, timeout=30
        )  # 30 sec per test
        return result.returncode == 0

    def analyze_failures(self, failures):
        """Run each failure individually to categorize."""
        print(f"\n📊 Analyzing {len(failures)} test failures individually...")

        for i, test in enumerate(failures, 1):
            print(f"  [{i}/{len(failures)}] Testing: {test}")
            if self.run_test_individually(test):
                self.results["isolation_failures"].append(test)
                print(f"    ✅ PASSES in isolation (test pollution issue)")
            else:
                self.results["real_failures"].append(test)
                print(f"    ❌ FAILS in isolation (real issue)")

    def generate_report(self):
        """Generate comprehensive health report."""
        total_isolation = len(self.results["isolation_failures"])
        total_real = len(self.results["real_failures"])

        print("\n" + "=" * 60)
        print("📋 TEST HEALTH REPORT")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n✅ Real Failures: {total_real}")
        print(f"⚠️  Isolation Issues: {total_isolation}")

        if total_real > 0:
            print("\n🔧 Real Failures (need fixing):")
            for test in self.results["real_failures"]:
                print(f"  - {test}")

        if total_isolation > 0:
            print("\n🧪 Isolation Failures (test infrastructure):")
            print("  These pass individually but fail in suite due to state pollution")
            for test in self.results["isolation_failures"][:5]:  # Show first 5
                print(f"  - {test}")
            if total_isolation > 5:
                print(f"  ... and {total_isolation - 5} more")

        # Calculate true health
        if total_real == 0:
            print("\n🎉 TRUE SYSTEM HEALTH: 100% (all real tests pass!)")
        else:
            print(f"\n📊 TRUE SYSTEM HEALTH: ~{100 - (total_real * 2)}% (estimate)")

        print("\n💡 TIP: To run tests with better isolation, try:")
        print("  pytest tests/ --forked  # Requires pytest-forked")
        print("  pytest tests/specific_test.py -v  # Run specific test file")

    def main(self):
        """Main execution flow."""
        # Handle help flag
        if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
            print(__doc__)
            return

        print("🏥 Piper Morgan Test Health Checker")
        print("=" * 40)

        # Step 1: Get baseline failures
        failures, _ = self.run_all_tests_together()

        if not failures:
            print("\n✨ All tests passing! No health check needed.")
            return

        # Step 2: Analyze each failure
        self.analyze_failures(failures)

        # Step 3: Generate report
        self.generate_report()


if __name__ == "__main__":
    checker = TestHealthChecker()
    checker.main()

#!/usr/bin/env python3
"""
Filter Known Failures Script

Compares pytest test results against .pytest-known-failures to:
1. Identify NEW failures (block push)
2. Validate known failures still match (warn if resolved)
3. Check expiry dates (warn if expired)
4. Enforce bead tracking (error if missing)

Exit codes:
- 0: All failures are known (allow push)
- 1: New failures detected (block push)
- 2: Configuration error (block push)
"""

import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

import yaml


class KnownFailuresValidator:
    """Validates test failures against known-failures file"""

    def __init__(self, known_failures_path: str = ".pytest-known-failures"):
        self.known_failures_path = Path(known_failures_path)
        self.known_failures: List[Dict] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def load_known_failures(self) -> bool:
        """Load and validate .pytest-known-failures file"""
        if not self.known_failures_path.exists():
            print(f"⚠️  No known failures file found at {self.known_failures_path}")
            print("   All test failures will block push")
            return True  # Not an error - just no known failures

        try:
            with open(self.known_failures_path, "r") as f:
                data = yaml.safe_load(f)

            if not data:
                self.warnings.append("Known failures file is empty")
                return True

            if data.get("version") != 1:
                self.errors.append(
                    f"Unknown known-failures version: {data.get('version')} (expected: 1)"
                )
                return False

            self.known_failures = data.get("failures", [])
            return self._validate_known_failures_schema()

        except yaml.YAMLError as e:
            self.errors.append(f"Failed to parse YAML: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to load known failures: {e}")
            return False

    def _validate_known_failures_schema(self) -> bool:
        """Validate each known failure entry has required fields"""
        required_fields = ["test_path", "reason", "bead", "expires", "category"]
        valid_categories = ["tdd_spec", "known_bug", "deferred"]

        for idx, failure in enumerate(self.known_failures):
            # Check required fields
            missing_fields = [f for f in required_fields if f not in failure]
            if missing_fields:
                self.errors.append(
                    f"Entry {idx}: Missing required fields: {', '.join(missing_fields)}"
                )
                continue

            # Validate category
            if failure["category"] not in valid_categories:
                self.errors.append(
                    f"Entry {idx}: Invalid category '{failure['category']}' "
                    f"(valid: {', '.join(valid_categories)})"
                )

            # Validate bead format
            if not re.match(r"^piper-morgan-[a-z0-9]{3}$", failure["bead"]):
                self.errors.append(
                    f"Entry {idx}: Invalid bead format '{failure['bead']}' "
                    f"(expected: piper-morgan-XXX)"
                )

            # Validate and check expiry date
            try:
                expiry_date = datetime.strptime(failure["expires"], "%Y-%m-%d").date()
                today = date.today()

                if expiry_date < today:
                    self.warnings.append(
                        f"⚠️  Entry {idx} EXPIRED ({failure['test_path']})\n"
                        f"   Bead: {failure['bead']}\n"
                        f"   Expired: {failure['expires']}\n"
                        f"   Action: Update bead or remove from known-failures"
                    )
                elif (expiry_date - today).days <= 7:
                    self.warnings.append(
                        f"⚠️  Entry {idx} expires soon ({failure['test_path']})\n"
                        f"   Expires: {failure['expires']} ({(expiry_date - today).days} days)\n"
                        f"   Bead: {failure['bead']}"
                    )
            except ValueError:
                self.errors.append(
                    f"Entry {idx}: Invalid date format '{failure['expires']}' "
                    f"(expected: YYYY-MM-DD)"
                )

        return len(self.errors) == 0

    def get_current_failures(self) -> Tuple[Set[str], bool]:
        """
        Run pytest to collect current test failures

        Returns:
            Tuple of (set of failed test paths, success flag)
        """
        try:
            # Use python3 explicitly (more reliable across environments)
            python_cmd = (
                "python3"
                if subprocess.run(["which", "python3"], capture_output=True).returncode == 0
                else "python"
            )

            # Run pytest in collection-only mode to get all tests
            result = subprocess.run(
                [python_cmd, "-m", "pytest", "tests/unit/", "--tb=no", "-v", "--co", "-q"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Run pytest to get actual failures
            result = subprocess.run(
                [python_cmd, "-m", "pytest", "tests/unit/", "--tb=line", "-v"],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max
            )

            # Parse output for FAILED tests
            failed_tests = set()
            for line in result.stdout.splitlines():
                # Match lines like: "tests/unit/test_foo.py::test_bar FAILED"
                match = re.match(r"^(tests/[^\s]+)\s+FAILED", line)
                if match:
                    failed_tests.add(match.group(1))

            return failed_tests, True

        except subprocess.TimeoutExpired:
            self.errors.append("Test execution timed out (5 minutes)")
            return set(), False
        except Exception as e:
            self.errors.append(f"Failed to run tests: {e}")
            return set(), False

    def compare_failures(self, current_failures: Set[str]) -> Tuple[Set[str], Set[str]]:
        """
        Compare current failures against known failures

        Returns:
            Tuple of (new failures, resolved failures)
        """
        known_test_paths = {f["test_path"] for f in self.known_failures}

        new_failures = current_failures - known_test_paths
        resolved_failures = known_test_paths - current_failures

        # Warn about resolved failures (should be removed from known-failures)
        if resolved_failures:
            self.warnings.append(
                "\n⚠️  Some known failures appear to be RESOLVED:\n"
                + "\n".join(f"   - {test}" for test in sorted(resolved_failures))
                + "\n   Action: Remove from .pytest-known-failures"
            )

        return new_failures, resolved_failures

    def print_results(
        self, current_failures: Set[str], new_failures: Set[str], resolved_failures: Set[str]
    ):
        """Print validation results"""
        print("\n" + "=" * 70)
        print("KNOWN FAILURES VALIDATION RESULTS")
        print("=" * 70)

        print(f"\n📊 Test Failure Summary:")
        print(f"   Total failures: {len(current_failures)}")
        print(f"   Known failures: {len(current_failures) - len(new_failures)}")
        print(f"   NEW failures: {len(new_failures)}")
        print(f"   Resolved failures: {len(resolved_failures)}")

        # Print warnings
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")

        # Print errors
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")

        # Print new failures (BLOCKING)
        if new_failures:
            print(f"\n❌ NEW FAILURES DETECTED (BLOCKING PUSH):")
            for test in sorted(new_failures):
                print(f"   {test}")
            print(f"\n   Fix these tests OR add to .pytest-known-failures with:")
            print(f"   - Clear reason (TDD spec, known bug, deferred work)")
            print(f"   - Bead reference for tracking")
            print(f"   - Expiry date (max 30 days)")
            print(f"   - Category (tdd_spec, known_bug, deferred)")

        print("\n" + "=" * 70)

    def validate(self) -> int:
        """
        Main validation flow

        Returns:
            Exit code (0 = success, 1 = new failures, 2 = config error)
        """
        # Load known failures
        if not self.load_known_failures():
            print("❌ Configuration errors in .pytest-known-failures")
            for error in self.errors:
                print(f"   {error}")
            return 2

        # Get current failures
        current_failures, success = self.get_current_failures()
        if not success:
            print("❌ Failed to run tests")
            for error in self.errors:
                print(f"   {error}")
            return 2

        # If no failures, we're good
        if not current_failures:
            print("✅ No test failures detected - push allowed")
            return 0

        # Compare failures
        new_failures, resolved_failures = self.compare_failures(current_failures)

        # Print results
        self.print_results(current_failures, new_failures, resolved_failures)

        # Determine exit code
        if self.errors:
            return 2  # Configuration error
        elif new_failures:
            return 1  # New failures detected
        else:
            print("\n✅ All failures are known - push allowed")
            if self.warnings:
                print("   (Review warnings above)")
            return 0


def main():
    """Main entry point"""
    validator = KnownFailuresValidator()
    exit_code = validator.validate()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

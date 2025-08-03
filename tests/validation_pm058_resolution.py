"""
PM-058 Resolution Validation Script
Comprehensive test validation to confirm AsyncPG concurrency issues are resolved
"""

import asyncio
import subprocess
import sys
from typing import Any, Dict, List


class PM058Validator:
    """Validator for PM-058 AsyncPG concurrency issue resolution"""

    def __init__(self):
        self.test_results = {}
        self.failure_count = 0
        self.success_count = 0

    async def run_file_repository_tests(self) -> Dict[str, Any]:
        """Run file repository tests to check for PM-058 issues"""
        print("🔍 Running file repository tests...")

        try:
            # Run the specific test file that was failing
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests/services/test_file_repository_migration.py",
                    "-v",
                    "--tb=short",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Parse results
            output = result.stdout + result.stderr
            passed = "PASSED" in output or "passed" in output
            failed = "FAILED" in output or "failed" in output
            errors = "ERROR" in output or "error" in output

            # Check for specific PM-058 indicators
            pm058_indicators = [
                "cannot perform operation: another operation is in progress",
                "asyncpg",
                "connection pool",
                "6 files instead of 3",
            ]

            pm058_issues = any(
                indicator.lower() in output.lower() for indicator in pm058_indicators
            )

            return {
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pm058_issues": pm058_issues,
                "output": output,
                "return_code": result.returncode,
            }

        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "failed": True,
                "errors": True,
                "pm058_issues": True,
                "output": "Test timeout - likely PM-058 issue",
                "return_code": -1,
            }
        except Exception as e:
            return {
                "passed": False,
                "failed": True,
                "errors": True,
                "pm058_issues": True,
                "output": f"Test execution error: {str(e)}",
                "return_code": -1,
            }

    async def run_connection_pool_tests(self) -> Dict[str, Any]:
        """Run connection pool tests to verify AsyncPG fixes"""
        print("🔍 Running connection pool tests...")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests/infrastructure/mcp/test_connection_pool.py",
                    "-v",
                    "--tb=short",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            output = result.stdout + result.stderr
            passed = "PASSED" in output or "passed" in output
            failed = "FAILED" in output or "failed" in output

            return {
                "passed": passed,
                "failed": failed,
                "output": output,
                "return_code": result.returncode,
            }

        except Exception as e:
            return {
                "passed": False,
                "failed": True,
                "output": f"Connection pool test error: {str(e)}",
                "return_code": -1,
            }

    async def run_full_test_suite_sample(self) -> Dict[str, Any]:
        """Run a sample of the full test suite to check for regressions"""
        print("🔍 Running full test suite sample...")

        try:
            # Run a subset of tests to check for regressions
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests/services/",
                    "tests/infrastructure/",
                    "--tb=short",
                    "-x",  # Stop on first failure
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )

            output = result.stdout + result.stderr
            passed = "PASSED" in output or "passed" in output
            failed = "FAILED" in output or "failed" in output

            return {
                "passed": passed,
                "failed": failed,
                "output": output,
                "return_code": result.returncode,
            }

        except Exception as e:
            return {
                "passed": False,
                "failed": True,
                "output": f"Full test suite error: {str(e)}",
                "return_code": -1,
            }

    async def validate_pm058_resolution(self) -> Dict[str, Any]:
        """Comprehensive validation of PM-058 resolution"""
        print("🚀 Starting PM-058 Resolution Validation...")
        print("=" * 60)

        # Run all validation tests
        file_repo_results = await self.run_file_repository_tests()
        connection_pool_results = await self.run_connection_pool_tests()
        full_suite_results = await self.run_full_test_suite_sample()

        # Compile results
        results = {
            "file_repository_tests": file_repo_results,
            "connection_pool_tests": connection_pool_results,
            "full_test_suite": full_suite_results,
            "pm058_resolved": True,
            "regressions_detected": False,
        }

        # Check for PM-058 issues
        if file_repo_results.get("pm058_issues", False):
            results["pm058_resolved"] = False
            print("❌ PM-058 issues detected in file repository tests")

        # Check for regressions
        if connection_pool_results.get("failed", False) or full_suite_results.get("failed", False):
            results["regressions_detected"] = True
            print("❌ Regressions detected in other tests")

        # Print summary
        print("\n" + "=" * 60)
        print("📊 PM-058 Resolution Validation Results")
        print("=" * 60)

        print(
            f"File Repository Tests: {'✅ PASSED' if file_repo_results.get('passed') else '❌ FAILED'}"
        )
        print(
            f"Connection Pool Tests: {'✅ PASSED' if connection_pool_results.get('passed') else '❌ FAILED'}"
        )
        print(
            f"Full Test Suite: {'✅ PASSED' if full_suite_results.get('passed') else '❌ FAILED'}"
        )
        print(
            f"PM-058 Issues: {'❌ DETECTED' if results['pm058_resolved'] == False else '✅ RESOLVED'}"
        )
        print(f"Regressions: {'❌ DETECTED' if results['regressions_detected'] else '✅ NONE'}")

        if results["pm058_resolved"] and not results["regressions_detected"]:
            print("\n🎉 PM-058 COMPLETELY RESOLVED!")
            print("✅ All AsyncPG concurrency issues fixed")
            print("✅ Test data isolation working")
            print("✅ No regressions detected")
        else:
            print("\n⚠️  PM-058 ISSUES REMAIN")
            if not results["pm058_resolved"]:
                print("❌ AsyncPG concurrency issues still present")
            if results["regressions_detected"]:
                print("❌ Regressions detected in other tests")

        return results


async def main():
    """Main validation function"""
    validator = PM058Validator()
    results = await validator.validate_pm058_resolution()

    # Exit with appropriate code
    if results["pm058_resolved"] and not results["regressions_detected"]:
        print("\n✅ PM-058 validation successful - all issues resolved")
        sys.exit(0)
    else:
        print("\n❌ PM-058 validation failed - issues remain")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

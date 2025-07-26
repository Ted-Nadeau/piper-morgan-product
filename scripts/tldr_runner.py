#!/usr/bin/env python3
"""
TLDR Continuous Verification System
Provides <0.1 second feedback loops for development work.
"""

import argparse
import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TLDRRunner:
    """Ultra-fast test runner with context-aware timeouts"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent

        # Context-aware timeout patterns
        self.timeout_patterns = {
            "unit": 0.05,  # Unit tests: 50ms
            "integration": 0.3,  # Integration tests: 300ms
            "infrastructure": 0.5,  # Infrastructure tests: 500ms
            "performance": 1.0,  # Performance tests: 1s
        }

        # Test classification patterns
        self.test_categories = {
            "unit": ["test_domain", "test_services", "test_validation"],
            "integration": ["test_integration", "test_orchestration", "test_queries"],
            "infrastructure": ["test_infrastructure", "test_mcp", "test_database"],
            "performance": ["test_performance", "test_load"],
        }

    def classify_test_file(self, test_path: str) -> str:
        """Classify test file for appropriate timeout"""
        test_path_lower = test_path.lower()

        for category, patterns in self.test_categories.items():
            if any(pattern in test_path_lower for pattern in patterns):
                return category

        # Default to unit test timeout for unclassified tests
        return "unit"

    def get_timeout_for_test(self, test_path: str, base_timeout: float) -> float:
        """Get context-aware timeout for specific test"""
        if base_timeout > 0:
            return base_timeout

        category = self.classify_test_file(test_path)
        return self.timeout_patterns[category]

    async def run_with_timeout(
        self,
        command: List[str],
        timeout: float,
        exit_0_on_timeout: bool = False,
        exit_2_on_failure: bool = False,
    ) -> Tuple[int, str, str]:
        """Run command with ultra-fast timeout"""
        start_time = time.time()

        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root,
            )

            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

                execution_time = time.time() - start_time
                return_code = process.returncode

                stdout_str = stdout.decode("utf-8", errors="ignore")
                stderr_str = stderr.decode("utf-8", errors="ignore")

                # Apply exit code policies
                if return_code != 0 and exit_2_on_failure:
                    return_code = 2

                return return_code, stdout_str, stderr_str

            except asyncio.TimeoutError:
                process.kill()
                await process.wait()

                execution_time = time.time() - start_time
                timeout_msg = f"TIMEOUT after {execution_time:.3f}s (limit: {timeout:.3f}s)"

                return_code = 0 if exit_0_on_timeout else 124  # 124 = timeout exit code
                return return_code, "", timeout_msg

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"EXECUTION ERROR: {str(e)}"
            return_code = 2 if exit_2_on_failure else 1
            return return_code, "", error_msg

    def discover_tests(self, pattern: Optional[str] = None) -> List[str]:
        """Discover test files with optional pattern filtering"""
        test_files = []

        # Standard test discovery
        for test_dir in ["tests", "."]:
            test_path = self.project_root / test_dir
            if test_path.exists():
                for test_file in test_path.rglob("test_*.py"):
                    if pattern is None or pattern in str(test_file):
                        test_files.append(str(test_file.relative_to(self.project_root)))

        # Also check root level test files
        for test_file in self.project_root.glob("*test*.py"):
            if pattern is None or pattern in str(test_file):
                test_files.append(str(test_file.relative_to(self.project_root)))

        return sorted(test_files)

    async def run_single_test(
        self,
        test_file: str,
        timeout: float = 0,
        exit_0_on_timeout: bool = False,
        exit_2_on_failure: bool = False,
        verbose: bool = False,
    ) -> Tuple[int, str]:
        """Run single test file with TLDR timing"""

        actual_timeout = self.get_timeout_for_test(test_file, timeout)
        category = self.classify_test_file(test_file)

        if verbose:
            print(f"Running {test_file} ({category}, timeout: {actual_timeout:.3f}s)")

        # Use pytest with minimal output for speed
        command = [
            sys.executable,
            "-m",
            "pytest",
            test_file,
            "-x",  # Stop on first failure
            "--tb=no" if not verbose else "--tb=short",
            "-q" if not verbose else "-v",
        ]

        # Add PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)

        return_code, stdout, stderr = await self.run_with_timeout(
            command, actual_timeout, exit_0_on_timeout, exit_2_on_failure
        )

        # Format output for TLDR
        if return_code == 0:
            result = f"✅ {test_file} ({category})"
        elif return_code == 124 or "TIMEOUT" in stderr:
            result = f"⏱️ {test_file} ({category}) - TIMEOUT"
        else:
            result = f"❌ {test_file} ({category}) - FAILED"
            if verbose and (stdout or stderr):
                result += f"\n{stdout[:200]}{stderr[:200]}"

        return return_code, result

    async def run_multiple_tests(
        self,
        test_files: List[str],
        timeout: float = 0,
        exit_0_on_timeout: bool = False,
        exit_2_on_failure: bool = False,
        verbose: bool = False,
        parallel: bool = True,
    ) -> Dict[str, Tuple[int, str]]:
        """Run multiple tests with TLDR timing"""

        if parallel and len(test_files) > 1:
            # Run tests in parallel for speed
            tasks = [
                self.run_single_test(
                    test_file, timeout, exit_0_on_timeout, exit_2_on_failure, verbose
                )
                for test_file in test_files
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            return {
                test_files[i]: (
                    results[i]
                    if not isinstance(results[i], Exception)
                    else (1, f"ERROR: {results[i]}")
                )
                for i in range(len(test_files))
            }
        else:
            # Run tests sequentially
            results = {}
            for test_file in test_files:
                results[test_file] = await self.run_single_test(
                    test_file, timeout, exit_0_on_timeout, exit_2_on_failure, verbose
                )
            return results

    def print_summary(self, results: Dict[str, Tuple[int, str]]):
        """Print TLDR summary"""
        passed = sum(1 for return_code, _ in results.values() if return_code == 0)
        timeouts = sum(1 for return_code, _ in results.values() if return_code == 124)
        failed = len(results) - passed - timeouts

        print(f"\n📊 TLDR Summary: {passed}✅ {timeouts}⏱️ {failed}❌ ({len(results)} total)")

        # Print individual results
        for test_file, (return_code, message) in results.items():
            print(message)


async def main():
    parser = argparse.ArgumentParser(
        description="TLDR Continuous Verification System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./scripts/tldr_runner.py --timeout 0.1
  ./scripts/tldr_runner.py --pattern validation --verbose
  ./scripts/tldr_runner.py --timeout 0.05 --exit-0-on-timeout
        """,
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=0,
        help="Global timeout in seconds (0 = use context-aware defaults)",
    )
    parser.add_argument("--pattern", type=str, help="Filter tests by pattern")
    parser.add_argument(
        "--exit-0-on-timeout",
        action="store_true",
        help="Exit with code 0 on timeout (for agent hooks)",
    )
    parser.add_argument(
        "--exit-2-on-failure",
        action="store_true",
        help="Exit with code 2 on test failure (for agent differentiation)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--sequential", action="store_true", help="Run tests sequentially instead of parallel"
    )
    parser.add_argument("--single", type=str, help="Run single test file")

    args = parser.parse_args()

    runner = TLDRRunner()

    try:
        if args.single:
            # Run single test
            return_code, result = await runner.run_single_test(
                args.single,
                args.timeout,
                args.exit_0_on_timeout,
                args.exit_2_on_failure,
                args.verbose,
            )
            print(result)
            return return_code
        else:
            # Discover and run multiple tests
            test_files = runner.discover_tests(args.pattern)

            if not test_files:
                print("No tests found matching criteria")
                return 1

            if args.verbose:
                print(f"Found {len(test_files)} test files")

            results = await runner.run_multiple_tests(
                test_files,
                args.timeout,
                args.exit_0_on_timeout,
                args.exit_2_on_failure,
                args.verbose,
                not args.sequential,
            )

            runner.print_summary(results)

            # Return appropriate exit code
            failed_count = sum(1 for return_code, _ in results.values() if return_code != 0)
            return min(failed_count, 2)  # Cap at 2 for agent differentiation

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        return 130
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

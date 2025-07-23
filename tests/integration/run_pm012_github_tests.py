#!/usr/bin/env python3
"""
PM-012: GitHub Integration Test Runner
Runs comprehensive test suites for GitHub integration with different configurations
"""

import argparse
import os
import subprocess
import sys
from typing import Any, Dict, List


class PM012TestRunner:
    """Test runner for PM-012 GitHub integration tests"""

    def __init__(self):
        self.test_files = [
            "tests/integration/test_pm012_github_production_scenarios.py",
            "tests/integration/test_pm012_github_real_api_integration.py",
            "tests/integration/test_github_integration_e2e.py",  # Existing tests
        ]

        self.test_configs = {
            "mock": {
                "description": "Run all tests with mock GitHub API",
                "markers": ["mock_api", "integration"],
                "env_vars": {},
            },
            "real": {
                "description": "Run tests with real GitHub API (requires GITHUB_TOKEN)",
                "markers": ["real_api", "integration"],
                "env_vars": {"GITHUB_TOKEN": "required", "GITHUB_TEST_REPO": "optional"},
            },
            "all": {
                "description": "Run all tests (mock + real if available)",
                "markers": ["integration"],
                "env_vars": {},
            },
            "quick": {
                "description": "Run quick smoke tests only",
                "markers": ["mock_api"],
                "env_vars": {},
            },
        }

    def check_environment(self, config_name: str) -> Dict[str, Any]:
        """Check environment for test configuration"""
        config = self.test_configs[config_name]
        issues = []

        # Check required environment variables
        for env_var, requirement in config["env_vars"].items():
            if requirement == "required" and not os.getenv(env_var):
                issues.append(f"Missing required environment variable: {env_var}")
            elif requirement == "optional" and not os.getenv(env_var):
                print(f"Warning: Optional environment variable {env_var} not set")

        return {"valid": len(issues) == 0, "issues": issues, "config": config}

    def run_tests(self, config_name: str, verbose: bool = False, coverage: bool = False) -> int:
        """Run tests with specified configuration"""

        # Check environment
        env_check = self.check_environment(config_name)
        if not env_check["valid"]:
            print(f"❌ Environment check failed for '{config_name}' configuration:")
            for issue in env_check["issues"]:
                print(f"   - {issue}")
            return 1

        config = env_check["config"]
        print(f"🚀 Running PM-012 GitHub Integration Tests")
        print(f"   Configuration: {config_name}")
        print(f"   Description: {config['description']}")
        print(f"   Markers: {', '.join(config['markers'])}")
        print()

        # Build pytest command
        cmd = ["python", "-m", "pytest"]

        # Add test files
        for test_file in self.test_files:
            if os.path.exists(test_file):
                cmd.append(test_file)

        # Add markers
        for marker in config["markers"]:
            cmd.extend(["-m", marker])

        # Add verbosity
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")

        # Add coverage if requested
        if coverage:
            cmd.extend(
                [
                    "--cov=services.integrations.github",
                    "--cov=services.orchestration",
                    "--cov=services.domain",
                    "--cov-report=term-missing",
                    "--cov-report=html:htmlcov",
                ]
            )

        # Add additional options
        cmd.extend(["--tb=short", "--strict-markers", "--disable-warnings"])

        print(f"Command: {' '.join(cmd)}")
        print()

        # Run tests
        try:
            result = subprocess.run(cmd, check=False)
            return result.returncode
        except KeyboardInterrupt:
            print("\n⚠️  Test run interrupted by user")
            return 1
        except Exception as e:
            print(f"❌ Failed to run tests: {e}")
            return 1

    def run_specific_test(self, test_name: str, verbose: bool = False) -> int:
        """Run a specific test by name"""
        print(f"🎯 Running specific test: {test_name}")

        cmd = ["python", "-m", "pytest"]

        # Find test file
        test_found = False
        for test_file in self.test_files:
            if os.path.exists(test_file):
                cmd.append(test_file)
                test_found = True

        if not test_found:
            print("❌ No test files found")
            return 1

        # Add test name
        cmd.extend(["-k", test_name])

        # Add verbosity
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")

        # Add additional options
        cmd.extend(["--tb=long", "--strict-markers"])

        print(f"Command: {' '.join(cmd)}")
        print()

        try:
            result = subprocess.run(cmd, check=False)
            return result.returncode
        except KeyboardInterrupt:
            print("\n⚠️  Test run interrupted by user")
            return 1
        except Exception as e:
            print(f"❌ Failed to run test: {e}")
            return 1

    def list_tests(self) -> None:
        """List all available tests"""
        print("📋 Available PM-012 GitHub Integration Tests:")
        print()

        for test_file in self.test_files:
            if os.path.exists(test_file):
                print(f"📁 {test_file}")

                # Try to extract test class names
                try:
                    with open(test_file, "r") as f:
                        content = f.read()
                        import re

                        test_classes = re.findall(r"class\s+(\w+Test\w*):", content)
                        for class_name in test_classes:
                            print(f"   └── {class_name}")
                except Exception:
                    pass
                print()
            else:
                print(f"❌ {test_file} (not found)")
                print()

    def list_configurations(self) -> None:
        """List all available test configurations"""
        print("⚙️  Available Test Configurations:")
        print()

        for config_name, config in self.test_configs.items():
            print(f"🔧 {config_name}")
            print(f"   Description: {config['description']}")
            print(f"   Markers: {', '.join(config['markers'])}")

            if config["env_vars"]:
                print("   Environment Variables:")
                for env_var, requirement in config["env_vars"].items():
                    status = "✅" if os.getenv(env_var) else "❌"
                    print(f"     {status} {env_var} ({requirement})")
            else:
                print("   Environment Variables: None required")

            print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="PM-012 GitHub Integration Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests with mock API
  python run_pm012_github_tests.py mock

  # Run tests with real GitHub API
  python run_pm012_github_tests.py real

  # Run all tests (mock + real if available)
  python run_pm012_github_tests.py all

  # Run quick smoke tests
  python run_pm012_github_tests.py quick

  # Run with verbose output and coverage
  python run_pm012_github_tests.py mock --verbose --coverage

  # Run specific test
  python run_pm012_github_tests.py --test "test_create_issue_from_natural_language"

  # List available tests
  python run_pm012_github_tests.py --list-tests

  # List configurations
  python run_pm012_github_tests.py --list-configs
        """,
    )

    parser.add_argument(
        "config",
        nargs="?",
        choices=["mock", "real", "all", "quick"],
        help="Test configuration to run",
    )

    parser.add_argument("--test", help="Run specific test by name")

    parser.add_argument("--list-tests", action="store_true", help="List all available tests")

    parser.add_argument(
        "--list-configs", action="store_true", help="List all available configurations"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")

    args = parser.parse_args()

    runner = PM012TestRunner()

    # Handle list commands
    if args.list_tests:
        runner.list_tests()
        return 0

    if args.list_configs:
        runner.list_configurations()
        return 0

    # Handle specific test
    if args.test:
        return runner.run_specific_test(args.test, args.verbose)

    # Handle configuration-based runs
    if args.config:
        return runner.run_tests(args.config, args.verbose, args.coverage)

    # Default: show help
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

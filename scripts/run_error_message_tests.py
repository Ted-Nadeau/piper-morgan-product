#!/usr/bin/env python3
"""
Error Message Testing Framework Runner

This script runs the comprehensive error message testing framework to validate
that error message enhancements don't create regressions while ensuring user
experience improvements are effective.

Usage:
    python scripts/run_error_message_tests.py [--verbose] [--coverage]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_tests(verbose=False, coverage=False):
    """Run the error message testing framework"""

    print("🧪 Error Message Testing Framework")
    print("=" * 50)

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Build test command
    test_file = "tests/test_error_message_enhancement.py"
    cmd = [sys.executable, "-m", "pytest", test_file]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=tests.test_error_message_enhancement", "--cov-report=term-missing"])

    print(f"Running: {' '.join(cmd)}")
    print()

    try:
        # Run the tests
        result = subprocess.run(cmd, capture_output=False, text=True)

        if result.returncode == 0:
            print("\n✅ All error message tests passed!")
            return True
        else:
            print(f"\n❌ Error message tests failed with exit code {result.returncode}")
            return False

    except Exception as e:
        print(f"\n❌ Failed to run tests: {e}")
        return False


def run_specific_test_category(category, verbose=False):
    """Run a specific test category"""

    print(f"🧪 Running {category} tests")
    print("=" * 30)

    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Map categories to test classes
    category_mapping = {
        "regression": "TestErrorMessageRegression",
        "user-experience": "TestUserFriendlyErrors",
        "integration": "TestIntegrationErrorScenarios",
        "performance": "TestPerformanceValidation",
        "recovery": "TestErrorRecoverySuggestions",
        "categorization": "TestErrorCategorization",
        "documentation": "TestErrorDocumentation",
    }

    if category not in category_mapping:
        print(f"❌ Unknown test category: {category}")
        print(f"Available categories: {', '.join(category_mapping.keys())}")
        return False

    test_class = category_mapping[category]
    test_file = "tests/test_error_message_enhancement.py"

    cmd = [sys.executable, "-m", "pytest", f"{test_file}::{test_class}", "-v"]

    print(f"Running: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)

        if result.returncode == 0:
            print(f"\n✅ {category} tests passed!")
            return True
        else:
            print(f"\n❌ {category} tests failed")
            return False

    except Exception as e:
        print(f"\n❌ Failed to run {category} tests: {e}")
        return False


def validate_test_framework():
    """Validate that the testing framework is properly set up"""

    print("🔍 Validating Error Message Testing Framework")
    print("=" * 50)

    project_root = Path(__file__).parent.parent

    # Check required files exist
    required_files = [
        "tests/test_error_message_enhancement.py",
        "services/api/errors.py",
        "main.py",
    ]

    missing_files = []
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False

    # Check test file structure
    test_file = project_root / "tests/test_error_message_enhancement.py"
    with open(test_file, "r") as f:
        content = f.read()

        required_classes = [
            "TestErrorMessageRegression",
            "TestUserFriendlyErrors",
            "TestIntegrationErrorScenarios",
            "TestPerformanceValidation",
            "TestErrorRecoverySuggestions",
            "TestErrorCategorization",
            "TestErrorDocumentation",
        ]

        missing_classes = []
        for class_name in required_classes:
            if class_name not in content:
                missing_classes.append(class_name)

        if missing_classes:
            print(f"❌ Missing test classes: {', '.join(missing_classes)}")
            return False

    print("✅ Testing framework validation passed!")
    return True


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(description="Error Message Testing Framework Runner")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Run with coverage")
    parser.add_argument(
        "--category",
        "-t",
        choices=[
            "regression",
            "user-experience",
            "integration",
            "performance",
            "recovery",
            "categorization",
            "documentation",
        ],
        help="Run specific test category",
    )
    parser.add_argument("--validate", action="store_true", help="Validate testing framework setup")

    args = parser.parse_args()

    if args.validate:
        success = validate_test_framework()
        sys.exit(0 if success else 1)

    if args.category:
        success = run_specific_test_category(args.category, args.verbose)
    else:
        success = run_tests(args.verbose, args.coverage)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

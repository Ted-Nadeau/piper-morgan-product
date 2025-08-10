#!/usr/bin/env python3
"""
Security Testing Framework Runner

This script provides a command-line interface to run the comprehensive security testing framework
for JWT authentication, focusing on both security validation and protocol portability.

Usage:
    python scripts/run_security_tests.py [OPTIONS]

Options:
    --category, -c    Run specific test category
    --verbose, -v     Verbose output
    --performance     Run performance tests
    --validate        Validate framework setup
    --help, -h        Show this help message
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_security_tests(category=None, verbose=False, performance=False):
    """Run the security testing framework"""

    print("🔒 Security Testing Framework - JWT Authentication")
    print("=" * 60)

    # Base test command
    test_cmd = [sys.executable, "-m", "pytest", "tests/test_security_framework.py"]

    # Add category filter if specified
    if category:
        test_cmd.extend(["-k", category])
        print(f"📋 Running tests for category: {category}")
    else:
        print("📋 Running all security tests")

    # Add verbose flag
    if verbose:
        test_cmd.append("-v")
        print("🔍 Verbose output enabled")

    # Add performance tests if requested
    if performance:
        test_cmd.extend(["-k", "Performance"])
        print("⚡ Performance tests enabled")

    # Add test discovery
    test_cmd.extend(["--tb=short", "--strict-markers"])

    print(f"\n🚀 Executing: {' '.join(test_cmd)}")
    print("-" * 60)

    try:
        # Run the tests
        result = subprocess.run(test_cmd, cwd=project_root, check=False)

        print("-" * 60)
        if result.returncode == 0:
            print("✅ Security tests completed successfully!")
        else:
            print("❌ Security tests completed with failures")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error running security tests: {e}")
        return False


def run_specific_test_category(category, verbose=False):
    """Run tests for a specific category"""

    category_mapping = {
        "authentication": "TestSecurityAuthentication",
        "protocol": "TestProtocolPortability",
        "federation": "TestFederationReadiness",
        "performance": "TestPerformanceValidation",
        "regression": "TestSecurityRegressionPrevention",
    }

    if category not in category_mapping:
        print(f"❌ Unknown category: {category}")
        print(f"Available categories: {', '.join(category_mapping.keys())}")
        return False

    test_class = category_mapping[category]
    print(f"🎯 Running {category} tests ({test_class})")

    return run_security_tests(category=test_class, verbose=verbose)


def validate_framework_setup():
    """Validate the security testing framework setup"""

    print("🔍 Validating Security Testing Framework Setup")
    print("=" * 50)

    # Check if test file exists
    test_file = project_root / "tests" / "test_security_framework.py"
    if not test_file.exists():
        print("❌ Security test file not found")
        return False

    print(f"✅ Security test file: {test_file}")

    # Check if pytest is available
    try:
        import pytest

        print(f"✅ Pytest available: {pytest.__version__}")
    except ImportError:
        print("❌ Pytest not available")
        return False

    # Check if FastAPI is available
    try:
        import fastapi

        print(f"✅ FastAPI available: {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI not available")
        return False

    # Check if JWT library is available
    try:
        import jwt

        print("✅ PyJWT library available")
    except ImportError:
        print("⚠️  PyJWT library not available (using mock for testing)")

    # Check if main app can be imported
    try:
        from main import app

        print("✅ Main application can be imported")
    except ImportError as e:
        print(f"⚠️  Main application import warning: {e}")

    print("\n✅ Framework validation complete")
    return True


def show_test_categories():
    """Show available test categories"""

    print("📋 Available Security Test Categories")
    print("=" * 40)

    categories = {
        "authentication": "Core security validation for JWT authentication",
        "protocol": "Protocol-first validation for interoperability",
        "federation": "OAuth2 and MCP protocol compatibility",
        "performance": "Auth endpoint performance validation",
        "regression": "Security regression prevention",
    }

    for category, description in categories.items():
        print(f"  {category:<15} - {description}")

    print("\nUsage examples:")
    print("  python scripts/run_security_tests.py --category authentication")
    print("  python scripts/run_security_tests.py --category protocol --verbose")
    print("  python scripts/run_security_tests.py --performance")


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description="Security Testing Framework Runner for JWT Authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Run all security tests
  %(prog)s --category authentication # Run authentication tests only
  %(prog)s --category protocol -v    # Run protocol tests with verbose output
  %(prog)s --performance             # Run performance tests only
  %(prog)s --validate                # Validate framework setup
        """,
    )

    parser.add_argument(
        "--category",
        "-c",
        choices=["authentication", "protocol", "federation", "performance", "regression"],
        help="Run specific test category",
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parser.add_argument("--performance", action="store_true", help="Run performance tests")

    parser.add_argument("--validate", action="store_true", help="Validate testing framework setup")

    parser.add_argument(
        "--list-categories", action="store_true", help="List available test categories"
    )

    args = parser.parse_args()

    # Handle special commands
    if args.list_categories:
        show_test_categories()
        return

    if args.validate:
        success = validate_framework_setup()
        sys.exit(0 if success else 1)

    # Run tests
    if args.category:
        success = run_specific_test_category(args.category, args.verbose)
    else:
        success = run_security_tests(verbose=args.verbose, performance=args.performance)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

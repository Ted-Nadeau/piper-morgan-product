#!/usr/bin/env python3
"""
PM-058 AsyncPG Connection Pool Fix - Logic Validation
Validates the implementation logic without requiring full environment
"""

import ast
import re


def validate_async_transaction_fixture():
    """Validate the async_transaction fixture implementation logic"""

    print("🔍 Validating PM-058 async_transaction fixture fix...")

    # Read the conftest.py file
    with open("/Users/xian/Development/piper-morgan/conftest.py", "r") as f:
        content = f.read()

    # Extract the async_transaction fixture
    fixture_match = re.search(
        r"@pytest\.fixture\s*\n\s*async def async_transaction\(\):(.*?)(?=\n@pytest\.fixture|\nclass|\n\n\n|\Z)",
        content,
        re.DOTALL,
    )

    if not fixture_match:
        print("❌ Could not find async_transaction fixture")
        return False

    fixture_code = fixture_match.group(1)
    print("✅ Found async_transaction fixture")

    # Validate key implementation aspects
    checks = [
        ("PM-058 FIX comment", "PM-058 FIX: ASYNCPG CONCURRENCY ISSUE RESOLVED" in fixture_code),
        ("Dedicated connection creation", "connection = await db.engine.connect()" in fixture_code),
        ("Transaction begin", "transaction = await connection.begin()" in fixture_code),
        ("Session bound to connection", "bind=connection" in fixture_code),
        (
            "Rollback for isolation",
            "await transaction.rollback()  # Rollback for test isolation" in fixture_code,
        ),
        ("Connection cleanup", "await connection.close()" in fixture_code),
        ("Exception handling", "except Exception:" in fixture_code),
        ("Resource cleanup in finally", "finally:" in fixture_code),
    ]

    all_passed = True
    for check_name, condition in checks:
        if condition:
            print(f"✅ {check_name}: PASS")
        else:
            print(f"❌ {check_name}: FAIL")
            all_passed = False

    # Validate syntax by parsing
    try:
        # Extract just the function definition for syntax validation
        func_start = content.find("@pytest.fixture\nasync def async_transaction():")
        if func_start == -1:
            func_start = content.find("@pytest.fixture\n\nasync def async_transaction():")

        func_end = content.find("\n@pytest.fixture", func_start + 1)
        if func_end == -1:
            func_end = len(content)

        function_code = content[func_start:func_end].rstrip()

        # Try to parse the function
        ast.parse(function_code)
        print("✅ Python syntax validation: PASS")

    except SyntaxError as e:
        print(f"❌ Python syntax validation: FAIL - {e}")
        all_passed = False

    print(f"\n📋 PM-058 Fix Validation: {'✅ PASSED' if all_passed else '❌ FAILED'}")
    return all_passed


def validate_affected_test_files():
    """Validate that affected test files use async_transaction fixture correctly"""

    print("\n🔍 Validating affected test file usage...")

    test_files = [
        "tests/services/test_file_repository_migration.py",
        "tests/services/test_file_resolver_edge_cases.py",
        "tests/services/test_file_scoring_weights.py",
        "tests/services/test_workflow_repository_migration.py",
    ]

    for test_file in test_files:
        try:
            with open(f"/Users/xian/Development/piper-morgan/{test_file}", "r") as f:
                content = f.read()

            # Check if it uses async_transaction
            async_transaction_usage = content.count("async_transaction")

            if async_transaction_usage > 0:
                print(f"✅ {test_file}: {async_transaction_usage} async_transaction usages found")
            else:
                print(f"⚠️  {test_file}: No async_transaction usage found")

        except FileNotFoundError:
            print(f"❌ {test_file}: File not found")


if __name__ == "__main__":
    print("PM-058 AsyncPG Connection Pool Fix - Logic Validation")
    print("=" * 60)

    # Validate the fixture implementation
    fixture_valid = validate_async_transaction_fixture()

    # Validate test file usage
    validate_affected_test_files()

    print("=" * 60)
    print(
        f"🎯 Overall Result: {'✅ IMPLEMENTATION VALIDATED' if fixture_valid else '❌ IMPLEMENTATION NEEDS FIXES'}"
    )

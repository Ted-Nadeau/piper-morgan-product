#!/usr/bin/env python3
"""
Real API validation test for CORE-NOTN #142 resolution.

Tests enhanced validation with actual NOTION_API_KEY from .env file.
No mocks - this is end-to-end validation with real Notion API.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path("/Users/xian/Development/piper-morgan")
sys.path.insert(0, str(project_root))

# Load .env file from project root
from dotenv import load_dotenv

env_path = project_root / ".env"
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")
load_dotenv(env_path)


async def test_enhanced_validation_real_api():
    """
    Test enhanced validation with real NOTION_API_KEY.

    This is the ultimate end-to-end test that proves CORE-NOTN #142 is fixed.
    """

    api_key = os.getenv("NOTION_API_KEY")

    if not api_key:
        print("❌ NOTION_API_KEY not found in .env file")
        print("   Please add: NOTION_API_KEY=your_key_here")
        return False

    print(f"✓ Found NOTION_API_KEY (length: {len(api_key)})")
    print("\n" + "=" * 70)
    print("Testing Enhanced Validation with Real Notion API")
    print("=" * 70 + "\n")

    try:
        from config.notion_user_config import NotionUserConfig, ValidationLevel

        # Create config with enhanced validation level
        # Using valid database IDs from config
        config_dict = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {"level": "enhanced", "connectivity_check": True},
            }
        }

        print("Step 1: Creating NotionUserConfig...")
        config = NotionUserConfig(config_dict)
        print("✓ Config created successfully")

        print("\nStep 2: Running enhanced validation (calls get_current_user())...")

        # This is THE TEST - if get_current_user() doesn't exist, this will fail
        try:
            result = await config.validate_async(level=ValidationLevel.ENHANCED)

            print("\n" + "=" * 70)
            print("VALIDATION RESULTS")
            print("=" * 70)
            print(f"Format valid: {result.format_valid}")
            print(f"Environment valid: {result.environment_valid}")
            print(f"Connectivity tested: {result.connectivity_tested}")
            print(f"Connectivity result: {result.connectivity_result}")
            print(f"Is valid: {result.is_valid()}")

            if result.errors:
                print(f"\nErrors: {result.errors}")

            if result.warnings:
                print(f"Warnings: {result.warnings}")

            print("\n" + "=" * 70)

            if result.connectivity_tested and result.connectivity_result:
                print("✅ ENHANCED VALIDATION SUCCESSFUL!")
                print("✅ get_current_user() was called without AttributeError!")
                print("✅ CORE-NOTN #142 is FULLY RESOLVED!")
                print("=" * 70 + "\n")
                return True
            else:
                print("⚠️  Validation completed but connectivity check failed")
                print("   This might indicate API key or network issues")
                print(f"   Errors: {result.errors}")
                return False

        except AttributeError as e:
            if "get_current_user" in str(e):
                print("\n" + "=" * 70)
                print("❌ FAILURE: get_current_user() method still missing!")
                print(f"   Error: {e}")
                print("   CORE-NOTN #142 is NOT resolved!")
                print("=" * 70 + "\n")
                return False
            else:
                # Different AttributeError
                raise

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_full_validation_real_api():
    """
    Test full validation with real NOTION_API_KEY.

    Full validation includes enhanced validation (get_current_user) plus permissions.
    """

    api_key = os.getenv("NOTION_API_KEY")

    if not api_key:
        print("❌ NOTION_API_KEY not found")
        return False

    print("\n" + "=" * 70)
    print("Testing Full Validation with Real Notion API")
    print("=" * 70 + "\n")

    try:
        from config.notion_user_config import NotionUserConfig, ValidationLevel

        config_dict = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {
                    "level": "full",
                    "connectivity_check": True,
                    "permission_check": True,
                },
            }
        }

        print("Running full validation...")
        config = NotionUserConfig(config_dict)
        result = await config.validate_async(level=ValidationLevel.FULL)

        print("\n" + "=" * 70)
        print("FULL VALIDATION RESULTS")
        print("=" * 70)
        print(f"Connectivity tested: {result.connectivity_tested}")
        print(f"Connectivity result: {result.connectivity_result}")
        print(f"Permission checked: {result.permission_checked}")
        print(f"Permission results: {result.permission_result}")
        print(f"Is valid: {result.is_valid()}")
        print("=" * 70 + "\n")

        if result.connectivity_tested and result.connectivity_result:
            print("✅ Full validation successful!")
            print("✅ get_current_user() works in full validation too!")
            return True
        else:
            print("⚠️  Full validation completed with issues")
            print(f"   Errors: {result.errors}")
            return False

    except Exception as e:
        print(f"\n❌ Error in full validation: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("REAL API VALIDATION TEST - CORE-NOTN #142")
    print("=" * 70 + "\n")

    # Run both tests
    enhanced_success = asyncio.run(test_enhanced_validation_real_api())
    full_success = asyncio.run(test_full_validation_real_api())

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print(f"Enhanced validation: {'✅ PASS' if enhanced_success else '❌ FAIL'}")
    print(f"Full validation: {'✅ PASS' if full_success else '❌ FAIL'}")
    print("=" * 70 + "\n")

    if enhanced_success and full_success:
        print("🎉 ALL TESTS PASSED!")
        print("🎉 CORE-NOTN #142 is COMPLETELY RESOLVED!")
        print("🎉 Enhanced validation with real API works perfectly!")
        sys.exit(0)
    else:
        print("❌ Some tests failed - see output above")
        sys.exit(1)

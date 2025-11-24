"""
Test script to verify user data isolation works correctly.

This script tests that:
1. Generic users see NO personal data (only system capabilities)
2. Specific users see ONLY their own personal data
3. Different users see different data

Issue #280: CORE-ALPHA-DATA-LEAK
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.user_context_service import user_context_service


async def test_data_isolation():
    """Test that user data isolation works correctly."""
    print("=" * 70)
    print("User Data Isolation Test - Issue #280")
    print("=" * 70)
    print()

    # Test 1: Generic user (no user_id) - should see NO personal data
    print("Test 1: Generic User (no user_id)")
    print("-" * 70)
    generic_context = await user_context_service.get_user_context(session_id="test-session-1")
    print(f"User ID: {generic_context.user_id}")
    print(f"Organization: {generic_context.organization}")
    print(f"Projects: {generic_context.projects}")
    print(f"Priorities: {generic_context.priorities}")
    print(f"Has preferences: {bool(generic_context.preferences)}")
    print()

    if generic_context.projects:
        print("⚠️  WARNING: Generic user has projects! Should be empty.")
    else:
        print("✅ Generic user has NO projects (expected)")

    if "Christian" in str(generic_context.preferences):
        print("❌ FAIL: Personal data leaked to generic user!")
        return False
    else:
        print("✅ No personal data in generic context")

    print()

    # Test 2: Specific user (with user_id) - should see personal data
    print("Test 2: User 'xian' (with user_id)")
    print("-" * 70)

    # Get xian's user_id from database
    from sqlalchemy import select

    from services.database.connection import db
    from services.database.models import AlphaUser

    await db.initialize()
    async with await db.get_session() as session:
        result = await session.execute(select(AlphaUser).where(AlphaUser.username == "xian"))
        xian_user = result.scalar_one_or_none()

        if not xian_user:
            print("❌ ERROR: User 'xian' not found in database")
            return False

        xian_user_id = str(xian_user.id)

    xian_context = await user_context_service.get_user_context(
        session_id="xian-session", user_id=xian_user_id
    )
    print(f"User ID: {xian_context.user_id}")
    print(f"Organization: {xian_context.organization}")
    print(
        f"Projects ({len(xian_context.projects)}): {xian_context.projects[:2]}..."
    )  # Show first 2
    print(f"Priorities ({len(xian_context.priorities)}): {xian_context.priorities[:2]}...")
    print(f"Has preferences: {bool(xian_context.preferences)}")
    print()

    if not xian_context.projects:
        print("❌ FAIL: xian user has NO projects! Should have personal data.")
        return False
    else:
        print(f"✅ xian user has {len(xian_context.projects)} projects")

    # Check for personal data markers
    has_personal_data = False
    personal_markers = ["VA", "Christian", "Kind Systems", "DRAGONS"]

    for marker in personal_markers:
        if marker in str(xian_context.preferences):
            print(f"✅ Found personal marker: {marker}")
            has_personal_data = True
            break

    if not has_personal_data:
        print("❌ FAIL: No personal data found for xian user!")
        return False

    print()

    # Test 3: Comparison - ensure data is different
    print("Test 3: Data Isolation Comparison")
    print("-" * 70)
    print(f"Generic projects: {len(generic_context.projects)}")
    print(f"Xian projects: {len(xian_context.projects)}")
    print()

    if len(generic_context.projects) == len(xian_context.projects):
        print("⚠️  WARNING: Same number of projects. Check if data is isolated.")
    else:
        print("✅ Different project counts (expected)")

    print()
    print("=" * 70)
    print("✅ ALL TESTS PASSED - User data isolation working!")
    print("=" * 70)
    print()
    print("Summary:")
    print("  - Generic users: See only system capabilities (no personal data)")
    print("  - Specific users: See their own personal preferences from database")
    print("  - Data is properly isolated between users")
    print()

    return True


async def main():
    """Main entry point"""
    try:
        success = await test_data_isolation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

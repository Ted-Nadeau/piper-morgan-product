#!/usr/bin/env python3
"""
Test script for Phase 1-Extended: get_data_source_id() with API version 2025-09-03

Tests:
1. Authentication with API version 2025-09-03 (using ClientOptions)
2. Retrieve data_source_id for ADR database
3. Verify data_sources field exists in database response
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Load environment variables from .env
from dotenv import load_dotenv

load_dotenv(project_root / ".env")

from services.integrations.mcp.notion_adapter import NotionMCPAdapter

# ADR database ID from config
ADR_DATABASE_ID = "25e11704d8bf80deaac2f806390fe7da"


async def test_api_version_authentication():
    """Test 1: Verify API version 2025-09-03 authentication works"""
    print("=" * 70)
    print("Test 1: API Version 2025-09-03 Authentication")
    print("=" * 70)

    adapter = NotionMCPAdapter()

    # Test connection (uses API version 2025-09-03)
    try:
        connected = await adapter.connect()
        if connected:
            print("✅ Authentication successful with API version 2025-09-03!")
            user = await adapter.get_current_user()
            print(f"   User: {user.get('name')} ({user.get('type')})")
            return True
        else:
            print("❌ Authentication failed")
            return False
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False


async def test_get_database_with_data_sources():
    """Test 2: Verify database response includes data_sources field"""
    print("\n" + "=" * 70)
    print("Test 2: Database Response with data_sources Field")
    print("=" * 70)

    adapter = NotionMCPAdapter()
    await adapter.connect()

    try:
        db_info = await adapter.get_database(ADR_DATABASE_ID)
        if db_info:
            print(f"✅ Retrieved database: {ADR_DATABASE_ID}")

            # Check for data_sources field
            if "data_sources" in db_info:
                data_sources = db_info["data_sources"]
                print(f"✅ data_sources field exists!")
                print(f"   Number of data sources: {len(data_sources)}")

                if data_sources:
                    for i, ds in enumerate(data_sources, 1):
                        print(f"   Data source {i}:")
                        print(f"     - ID: {ds.get('id', 'N/A')}")
                        print(f"     - Type: {ds.get('type', 'N/A')}")
                    return True
                else:
                    print("⚠️  data_sources field exists but is empty")
                    print("   This may mean the workspace hasn't migrated to multi-source yet")
                    return False
            else:
                print("❌ data_sources field NOT found in database response")
                print("   Available fields:", list(db_info.keys())[:10], "...")
                return False
        else:
            print(f"❌ Failed to retrieve database")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_get_data_source_id():
    """Test 3: Test get_data_source_id() method"""
    print("\n" + "=" * 70)
    print("Test 3: get_data_source_id() Method")
    print("=" * 70)

    adapter = NotionMCPAdapter()
    await adapter.connect()

    try:
        data_source_id = await adapter.get_data_source_id(ADR_DATABASE_ID)

        if data_source_id:
            print(f"✅ Successfully retrieved data_source_id!")
            print(f"   Database ID: {ADR_DATABASE_ID}")
            print(f"   Data Source ID: {data_source_id}")
            return True
        else:
            print("❌ get_data_source_id() returned None")
            print("   This means either:")
            print("   1. Workspace hasn't migrated to API 2025-09-03 yet, OR")
            print("   2. Database has no data_sources field in response")
            return False
    except Exception as e:
        print(f"❌ Error calling get_data_source_id(): {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n🧪 Phase 1-Extended: Testing data_source_id Support")
    print("=" * 70)

    # Check API key
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        print("❌ NOTION_API_KEY not found in environment")
        print("   Make sure .env file exists and contains NOTION_API_KEY")
        return False

    print(f"✅ NOTION_API_KEY found (length: {len(api_key)})")
    print(f"✅ Testing with database: {ADR_DATABASE_ID}")

    # Run tests
    test1 = await test_api_version_authentication()
    test2 = await test_get_database_with_data_sources()
    test3 = await test_get_data_source_id()

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Test 1 (Authentication):      {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Test 2 (data_sources field):  {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Test 3 (get_data_source_id):  {'✅ PASS' if test3 else '❌ FAIL'}")

    all_passed = test1 and test2 and test3

    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ API version 2025-09-03 is working")
        print("✅ data_source_id support is functional")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        if test1 and not test2:
            print("   Authentication works but data_sources not available yet")
            print("   Workspace may not have migrated to multi-source databases")
        elif not test1:
            print("   Authentication failed - check API key and permissions")

    return all_passed


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)

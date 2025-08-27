#!/usr/bin/env python3
"""
Test Notion MCP Integration

Basic testing framework for NotionMCPAdapter to validate:
1. Connection and authentication
2. Basic API operations
3. Error handling and rate limiting
4. Spatial mapping framework

This follows the TDD approach specified in the methodology.
"""

import asyncio
import os
import sys
from typing import Optional

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def test_notion_connection():
    """Test Notion API connection and authentication"""
    print("\n🔗 Testing Notion API Connection")

    try:
        # Initialize adapter
        adapter = NotionMCPAdapter()
        print("1. ✅ NotionMCPAdapter initialized")

        # Test without token (should fail gracefully)
        print("2. Testing connection without token...")
        connection_result = await adapter.test_connection()
        if not connection_result:
            print("   ✅ Correctly failed without token")
        else:
            print("   ❌ Unexpectedly succeeded without token")
            return False

        # Test with invalid token (should fail gracefully)
        print("3. Testing connection with invalid token...")
        await adapter.configure_notion_api("invalid_token")
        connection_result = await adapter.test_connection()
        if not connection_result:
            print("   ✅ Correctly failed with invalid token")
        else:
            print("   ❌ Unexpectedly succeeded with invalid token")
            return False

        print("4. ✅ Connection tests passed - adapter handles errors gracefully")
        return True

    except Exception as e:
        print(f"   ❌ Connection test failed: {e}")
        return False
    finally:
        if "adapter" in locals():
            await adapter.close()


async def test_notion_api_operations():
    """Test basic Notion API operations with mock data"""
    print("\n📚 Testing Notion API Operations")

    try:
        adapter = NotionMCPAdapter()
        print("1. ✅ NotionMCPAdapter initialized for API tests")

        # Test workspace info (will fail without valid token, but should handle gracefully)
        print("2. Testing workspace info retrieval...")
        workspace_info = await adapter.get_workspace_info()
        if workspace_info is None:
            print("   ✅ Correctly handled missing authentication")
        else:
            print("   ❌ Unexpectedly retrieved workspace info without auth")
            return False

        # Test database listing (will fail without valid token, but should handle gracefully)
        print("3. Testing database listing...")
        databases = await adapter.list_databases()
        if databases == []:
            print("   ✅ Correctly handled missing authentication")
        else:
            print("   ❌ Unexpectedly retrieved databases without auth")
            return False

        print("4. ✅ API operation tests passed - adapter handles missing auth gracefully")
        return True

    except Exception as e:
        print(f"   ❌ API operation test failed: {e}")
        return False
    finally:
        if "adapter" in locals():
            await adapter.close()


async def test_notion_spatial_framework():
    """Test spatial mapping framework integration"""
    print("\n🗺️  Testing Notion Spatial Framework")

    try:
        adapter = NotionMCPAdapter()
        print("1. ✅ NotionMCPAdapter initialized for spatial tests")

        # Test that adapter inherits from BaseSpatialAdapter
        from services.integrations.spatial_adapter import BaseSpatialAdapter

        if isinstance(adapter, BaseSpatialAdapter):
            print("2. ✅ Correctly inherits from BaseSpatialAdapter")
        else:
            print("   ❌ Does not inherit from BaseSpatialAdapter")
            return False

        # Test adapter type identification
        if adapter.system_name == "notion_mcp":
            print("3. ✅ Correctly identifies as notion_mcp adapter")
        else:
            print(f"   ❌ Incorrect adapter type: {adapter.system_name}")
            return False

        print("4. ✅ Spatial framework tests passed")
        return True

    except Exception as e:
        print(f"   ❌ Spatial framework test failed: {e}")
        return False
    finally:
        if "adapter" in locals():
            await adapter.close()


async def test_notion_error_handling():
    """Test error handling and rate limiting"""
    print("\n⚠️  Testing Notion Error Handling")

    try:
        adapter = NotionMCPAdapter()
        print("1. ✅ NotionMCPAdapter initialized for error handling tests")

        # Test rate limiting implementation
        print("2. Testing rate limiting implementation...")

        # Configure the adapter first to avoid session issues
        await adapter.configure_notion_api("test_token")

        start_time = asyncio.get_event_loop().time()

        # Make multiple API calls to test rate limiting
        for i in range(3):
            await adapter._call_notion_api("test_endpoint")

        end_time = asyncio.get_event_loop().time()
        elapsed_time = end_time - start_time

        # Should take at least 0.68 seconds (2 * 0.34) due to rate limiting
        if elapsed_time >= 0.6:
            print("   ✅ Rate limiting correctly implemented")
        else:
            print(f"   ❌ Rate limiting not working: {elapsed_time:.2f}s elapsed")
            return False

        print("3. ✅ Error handling tests passed")
        return True

    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
        return False
    finally:
        if "adapter" in locals():
            await adapter.close()


async def main():
    """Run all Notion integration tests"""
    print("🚀 Notion MCP Integration Test Suite")
    print("=" * 50)

    test_results = []

    # Run connection tests
    test_results.append(await test_notion_connection())

    # Run API operation tests
    test_results.append(await test_notion_api_operations())

    # Run spatial framework tests
    test_results.append(await test_notion_spatial_framework())

    # Run error handling tests
    test_results.append(await test_notion_error_handling())

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)

    passed = sum(test_results)
    total = len(test_results)

    for i, result in enumerate(test_results):
        status = "✅ PASSED" if result else "❌ FAILED"
        test_names = [
            "Connection & Authentication",
            "API Operations",
            "Spatial Framework",
            "Error Handling",
        ]
        print(f"{i+1}. {test_names[i]}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! NotionMCPAdapter foundation is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Review implementation before proceeding.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Test suite failed with unexpected error: {e}")
        sys.exit(1)

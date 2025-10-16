#!/usr/bin/env python3
"""Quick script to test get_current_user() with real API key from .env"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
# Use absolute path to project root
project_root = Path("/Users/xian/Development/piper-morgan")
sys.path.insert(0, str(project_root))

# Load .env file from project root
from dotenv import load_dotenv

env_path = project_root / ".env"
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")
load_dotenv(env_path)


async def test_real_api():
    """Test get_current_user() with real Notion API key"""

    api_key = os.getenv("NOTION_API_KEY")

    if not api_key:
        print("❌ NOTION_API_KEY not found in .env file")
        print("   Please add: NOTION_API_KEY=your_key_here")
        return False

    print(f"✓ Found NOTION_API_KEY (length: {len(api_key)})")
    print("\nTesting NotionMCPAdapter.get_current_user() with real API...")

    try:
        from unittest.mock import MagicMock, patch

        from services.integrations.mcp.notion_adapter import NotionMCPAdapter

        # Create adapter with real API key
        with patch("services.integrations.mcp.notion_adapter.NotionConfig") as MockConfig:
            mock_config = MagicMock()
            mock_config.get_api_key.return_value = api_key
            mock_config.validate_config.return_value = True
            MockConfig.return_value = mock_config

            adapter = NotionMCPAdapter()

            # Call with real API
            result = await adapter.get_current_user()

            # Verify we got real user data
            if not result:
                print("❌ No result returned from API")
                return False

            print("\n✅ Real API test successful!")
            print(f"   User ID: {result.get('id')}")
            print(f"   Name: {result.get('name')}")
            print(f"   Type: {result.get('type')}")

            if result.get("type") == "person" and result.get("email"):
                print(f"   Email: {result.get('email')}")

            if result.get("type") == "bot" and result.get("workspace"):
                print(
                    f"   Workspace: {result['workspace'].get('name')} ({result['workspace'].get('id')})"
                )

            return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_real_api())
    sys.exit(0 if success else 1)

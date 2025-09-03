# debug_parent.py - with path fix
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from pathlib import Path

from dotenv import load_dotenv

from config.notion_user_config import ConfigurationError, NotionUserConfig
from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def debug_parent():
    load_dotenv()

    # Load configuration instead of hardcoded value
    try:
        config = NotionUserConfig.load_from_user_config(Path("config/PIPER.user.md"))
        parent_id = config.get_parent_id("default")
        print(f"Using default parent ID from configuration: {parent_id[:8]}...")
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        # Fallback to old hardcoded value for backward compatibility during transition
        print("WARNING: Falling back to hardcoded parent ID - please update configuration")
        parent_id = "25d11704d8bf80c8a71ddbe7aba51f55"

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Try to get the page directly
    try:
        page = await adapter.get_page(parent_id)
        if page:
            print(f"✓ Page found: {page.get('title', 'Untitled')}")
            print(f"  Type: {page.get('object', 'unknown')}")
            print(f"  URL: {page.get('url', 'no url')}")
        else:
            print("✗ Page not found through adapter.get_page()")
    except Exception as e:
        print(f"✗ Error accessing page: {e}")

    # Search for it by title
    results = await adapter.search_notion("Shipping News")
    print(f"\nSearch found {len(results)} results for 'Shipping News'")
    for r in results[:5]:
        obj_type = r.get("object", "unknown")
        r_id = r.get("id", "no-id")
        print(f"  - [{obj_type}] {r_id}")


asyncio.run(debug_parent())

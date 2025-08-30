# debug_parent.py - with path fix
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def debug_parent():
    load_dotenv()
    adapter = NotionMCPAdapter()
    await adapter.connect()

    parent_id = "25d11704d8bf80c8a71ddbe7aba51f55"

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

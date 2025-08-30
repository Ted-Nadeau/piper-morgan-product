# debug_search.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def debug_search():
    load_dotenv()

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Try empty search - should return something
    print("Testing empty search...")
    results = await adapter.search_notion("")
    print(f"Empty search: {len(results)} results")

    # Try searching for "Test"
    print("\nSearching for 'Test'...")
    results = await adapter.search_notion("Test")
    print(f"'Test' search: {len(results)} results")

    if results:
        for i, result in enumerate(results[:3]):
            obj_type = result.get("object", "unknown")
            title = "Untitled"
            if "properties" in result and "title" in result["properties"]:
                title_prop = result["properties"]["title"]
                if "title" in title_prop and len(title_prop["title"]) > 0:
                    title = title_prop["title"][0]["text"]["content"]
            print(f"  {i+1}. [{obj_type}] {title}")

    # Try with page filter
    print("\nSearching with page filter...")
    page_results = await adapter.search_notion("", filter_type="page")
    print(f"Page filter: {len(page_results)} pages")

    # Show if search method even runs
    print("\nIf nothing above, method might be broken")


asyncio.run(debug_search())

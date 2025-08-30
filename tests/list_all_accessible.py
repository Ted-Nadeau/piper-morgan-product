# list_all_accessible.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def list_all():
    load_dotenv()
    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Get ALL pages
    results = await adapter.search_notion("", filter_type="page")

    print(f"Total accessible pages: {len(results)}\n")

    for i, r in enumerate(results[:20]):  # First 20
        r_id = r.get("id", "no-id")
        url = r.get("url", "no-url")

        # Try multiple ways to get title
        title = "Untitled"
        if "properties" in r:
            for prop_name in ["title", "Title", "Name", "name"]:
                if prop_name in r["properties"]:
                    prop = r["properties"][prop_name]
                    if "title" in prop and prop["title"]:
                        if len(prop["title"]) > 0:
                            title = prop["title"][0].get("text", {}).get("content", "Untitled")
                            break

        print(f"{i+1}. {title}")
        print(f"   ID: {r_id}")
        print(f"   URL: {url}\n")


asyncio.run(list_all())

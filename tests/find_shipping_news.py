# find_shipping_news.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def find_shipping_news():
    load_dotenv()
    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Search for Shipping News
    results = await adapter.search_notion("Shipping News")

    for r in results:
        r_id = r.get("id", "no-id")
        title = "Untitled"
        if "properties" in r and "title" in r["properties"]:
            title_prop = r["properties"]["title"]
            if "title" in title_prop and title_prop.get("title"):
                title = title_prop["title"][0].get("text", {}).get("content", "Untitled")

        if "Shipping" in title or "shipping" in title:
            print(f"Found potential match:")
            print(f"  Title: {title}")
            print(f"  ID: {r_id}")
            print(f"  URL: {r.get('url', 'no url')}")
            print()


asyncio.run(find_shipping_news())

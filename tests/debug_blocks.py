# debug_blocks.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def debug_blocks():
    load_dotenv()

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Create a page WITH content blocks
    parent_id = "25c11704-d8bf-80f4-9bf6-d54b55e784e9"

    result = await adapter.create_page(
        parent_id=parent_id,
        properties={"title": {"title": [{"text": {"content": f"Test Page With Content"}}]}},
        content=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "This page has content blocks!"}}]
                },
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "Test Heading"}}]},
            },
        ],
    )

    if result:
        page_id = result.get("id")
        print(f"✅ Created page: {page_id}")

        # Now get its blocks
        blocks = await adapter.get_page_blocks(page_id)

        if blocks:
            print(f"✅ SUCCESS: Retrieved {len(blocks)} blocks")
            for i, block in enumerate(blocks):
                block_type = block.get("type", "unknown")
                print(f"   Block {i}: {block_type}")
            print("\n🎉 get_page_blocks verified!")
        else:
            print("❌ No blocks retrieved (method might be broken)")
    else:
        print("❌ Failed to create test page")


asyncio.run(debug_blocks())

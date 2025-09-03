# Search for the ADR database
import asyncio
from pathlib import Path

from dotenv import load_dotenv

from config.notion_user_config import ConfigurationError, NotionUserConfig
from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def find_adr_database():
    load_dotenv()

    # Load configuration instead of hardcoded value
    try:
        config = NotionUserConfig.load_from_user_config(Path("config/PIPER.user.md"))
        parent_page_id = config.get_database_id("adrs")
        print(f"Using ADR database ID from configuration: {parent_page_id[:8]}...")
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        # Fallback to old hardcoded value for backward compatibility during transition
        print("WARNING: Falling back to hardcoded database ID - please update configuration")
        parent_page_id = "25e11704d8bf80deaac2f806390fe7da"

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Get the parent page
    page = await adapter.get_page(parent_page_id)
    if page:
        print(f"Found parent page: {page.get('properties', {}).get('title', 'Unknown')}")

    # Search for databases
    results = await adapter.search_notion("", filter_type="database")
    print(f"\nAll accessible databases:")
    for db in results:
        db_id = db.get("id", "no-id")
        # Check if this database has "ADR" in its title
        if "title" in db and db["title"]:
            for title_item in db["title"]:
                if "text" in title_item:
                    title = title_item["text"].get("content", "")
                    if "ADR" in title:
                        print(f"  {db_id}: {title}")
                        print(f"    Clean ID: {db_id.replace('-', '')}")


asyncio.run(find_adr_database())

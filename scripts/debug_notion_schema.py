# Get the actual database schema
import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv

from config.notion_user_config import ConfigurationError, NotionUserConfig
from services.integrations.mcp.notion_adapter import NotionMCPAdapter


async def get_database_schema():
    load_dotenv()

    # Load configuration instead of hardcoded value
    try:
        config = NotionUserConfig.load_from_user_config(Path("config/PIPER.user.md"))
        db_id = config.get_database_id("adrs")
        print(f"Using ADR database ID from configuration: {db_id[:8]}...")
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        # Fallback to old hardcoded value for backward compatibility during transition
        print("WARNING: Falling back to hardcoded database ID - please update configuration")
        db_id = "25e11704d8bf80deaac2f806390fe7da"

    adapter = NotionMCPAdapter()
    await adapter.connect()

    # Get database details using the correct client reference
    result = await adapter.notion_client.databases.retrieve(database_id=db_id)

    print("Database Properties:")
    print("-" * 50)
    for prop_name, prop_details in result.get("properties", {}).items():
        prop_type = prop_details.get("type", "unknown")
        print(f"  '{prop_name}': type={prop_type}")

    print("\nThe code is currently trying to use:")
    print("  'Name' for title")
    print("  'ADR Number' for the number")
    print("  'Status' for status")
    print("  'Date' for date")
    print("  'Author' for author")


asyncio.run(get_database_schema())

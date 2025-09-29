"""
Publisher service for publishing content to various platforms.
Currently supports Notion with markdown format.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
from services.publishing.converters.markdown_to_notion import convert_markdown_to_notion_blocks


class Publisher:
    """Main publishing orchestration service"""

    def __init__(self):
        """Initialize publisher with platform adapters"""
        self.notion = NotionIntegrationRouter()

    async def publish(
        self, file_path: str, platform: str, location: str, format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        Main publishing orchestration.

        Args:
            file_path: Path to file to publish
            platform: Target platform (currently only 'notion')
            location: Parent location ID for the published content
            format: Content format (currently only 'markdown')

        Returns:
            Dictionary with success status, page_id, url, and any warnings
        """
        # Validate platform
        if platform != "notion":
            raise ValueError(
                f"Platform {platform} not supported. Currently only 'notion' is supported."
            )

        # Read file content
        content = self._read_file(file_path)

        # Publish to platform
        if platform == "notion":
            # Check if this is a database publish (location will be database_id)
            if hasattr(self, "database_mode") and self.database_mode:
                return await self._publish_to_notion_database(content, location, format, file_path)
            else:
                return await self._publish_to_notion(content, location, format, file_path)
        else:
            raise ValueError(
                f"Platform {platform} not supported. Currently only 'notion' is supported."
            )

    def _read_file(self, file_path: str) -> str:
        """
        Read file with error handling.

        Args:
            file_path: Path to file to read

        Returns:
            File content as string

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    async def _publish_to_notion(
        self, content: str, parent_id: str, format: str, file_path: str
    ) -> Dict[str, Any]:
        """
        Notion publishing with error handling.

        Args:
            content: Markdown content to publish
            parent_id: Notion parent page ID
            format: Content format (must be 'markdown')
            file_path: Original file path for title extraction

        Returns:
            Dictionary with publishing results
        """
        if format != "markdown":
            raise ValueError(
                f"Format {format} not supported. Currently only 'markdown' is supported."
            )

        # Convert markdown to Notion blocks
        conversion = convert_markdown_to_notion_blocks(content)

        # Extract title from content or use filename
        title = self._extract_title(content)
        if title == "Untitled":
            # Use filename as fallback
            title = Path(file_path).stem.replace("-", " ").replace("_", " ").title()

        try:
            # Ensure adapter is connected
            await self.notion.connect()

            # Create page properties
            properties = {"title": {"title": [{"text": {"content": title}}]}}

            # Create page with content
            page_result = await self.notion.create_page(
                parent_id=parent_id, properties=properties, content=conversion["blocks"]
            )

            if page_result:
                return {
                    "success": True,
                    "page_id": page_result["id"],
                    "url": page_result.get("url", ""),
                    "warnings": conversion["warnings"],
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create page - no result returned",
                    "warnings": conversion["warnings"],
                }

        except ValueError as e:
            # Let user errors propagate for proper CLI handling
            raise e
        except Exception as e:
            return {"success": False, "error": str(e), "warnings": conversion["warnings"]}

    async def _publish_to_notion_database(
        self, content: str, database_id: str, format: str, file_path: str
    ) -> Dict[str, Any]:
        """
        Notion database publishing with ADR metadata extraction.

        Args:
            content: Markdown content to publish
            database_id: Notion database ID
            format: Content format (must be 'markdown')
            file_path: Original file path for metadata extraction

        Returns:
            Dictionary with publishing results
        """
        if format != "markdown":
            raise ValueError(
                f"Format {format} not supported. Currently only 'markdown' is supported."
            )

        # Convert markdown to Notion blocks
        conversion = convert_markdown_to_notion_blocks(content)

        # Parse ADR metadata
        metadata = self._parse_adr_metadata(content)

        try:
            # Ensure adapter is connected
            await self.notion.connect()

            # Create database item properties
            properties = {
                "Name": {"title": [{"text": {"content": metadata["title"]}}]},
                "ADR Number": {"rich_text": [{"text": {"content": metadata["number"]}}]},
                "Status": {"select": {"name": metadata["status"]}},
                "Author": {"rich_text": [{"text": {"content": metadata["author"]}}]},
            }

            # Add date if available
            if metadata["date"]:
                properties["Date"] = {"date": {"start": metadata["date"]}}

            # Create database item with content
            item_result = await self.notion.create_database_item(
                database_id=database_id, properties=properties, content=conversion["blocks"]
            )

            if item_result:
                return {
                    "success": True,
                    "page_id": item_result["id"],
                    "url": item_result.get("url", ""),
                    "warnings": conversion["warnings"],
                    "metadata": metadata,
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create database item - no result returned",
                    "warnings": conversion["warnings"],
                }

        except ValueError as e:
            # Let user errors propagate for proper CLI handling
            raise e
        except Exception as e:
            return {"success": False, "error": str(e), "warnings": conversion["warnings"]}

    def _extract_title(self, content: str) -> str:
        """
        Extract title from first H1 header in markdown.

        Args:
            content: Markdown content

        Returns:
            Title string or "Untitled" if no H1 found
        """
        for line in content.split("\n"):
            if line.startswith("# "):
                return line[2:].strip()
        return "Untitled"

    def _parse_adr_metadata(self, content: str) -> Dict[str, Any]:
        """
        Parse ADR metadata from markdown content.

        Args:
            content: Markdown content

        Returns:
            Dictionary with ADR metadata fields
        """
        lines = content.split("\n")
        metadata = {
            "title": "Untitled",
            "number": "Unknown",
            "status": "Accepted",
            "date": None,
            "author": "System",
        }

        for line in lines:
            line = line.strip()

            # Extract title and number from H1
            if line.startswith("# ADR-"):
                # Format: # ADR-XXX: Title
                parts = line[2:].split(":", 1)
                if len(parts) == 2:
                    adr_part = parts[0].strip()
                    title_part = parts[1].strip()

                    # Extract number from ADR-XXX
                    if adr_part.startswith("ADR-"):
                        metadata["number"] = adr_part[4:]

                    metadata["title"] = title_part

            # Extract status
            elif line.startswith("**Status:**") or line.startswith("Status:"):
                status = line.split(":", 1)[1].strip().replace("*", "")
                if status:
                    # Normalize status values
                    status_lower = status.lower()
                    if status_lower in [
                        "proposed",
                        "draft",
                        "accepted",
                        "implemented",
                        "deprecated",
                    ]:
                        metadata["status"] = status.capitalize()
                    elif status_lower in ["superseded", "rejected"]:
                        metadata["status"] = status.capitalize()
                    else:
                        metadata["status"] = "Accepted"  # Default

            # Extract date
            elif line.startswith("**Date:**") or line.startswith("Date:"):
                date_str = line.split(":", 1)[1].strip().replace("*", "")
                if date_str:
                    metadata["date"] = date_str.strip()

            # Extract author/decision maker
            elif (
                line.startswith("**Decision Maker:**")
                or line.startswith("Decision Maker:")
                or line.startswith("**Author:**")
                or line.startswith("Author:")
            ):
                author = line.split(":", 1)[1].strip().replace("*", "")
                if author:
                    metadata["author"] = author.strip()

        return metadata

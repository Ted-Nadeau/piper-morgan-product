"""
Notion MCP Spatial Adapter

Notion-specific MCP spatial adapter implementation following the established
spatial adapter pattern for external system integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp

from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

logger = logging.getLogger(__name__)


class NotionMCPAdapter(BaseSpatialAdapter):
    """
    Notion MCP spatial adapter implementation.

    Maps Notion page and database IDs to spatial positions using MCP protocol
    for external service integration.
    """

    def __init__(self):
        super().__init__("notion_mcp")
        self._lock = asyncio.Lock()
        self._page_to_position: Dict[str, int] = {}
        self._position_to_page: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # Notion API configuration
        self._notion_token: Optional[str] = None
        self._notion_api_base = "https://api.notion.com/v1"
        self._session: Optional[aiohttp.ClientSession] = None

        logger.info("NotionMCPAdapter initialized")

    async def connect(self, integration_token: str) -> bool:
        """Connect to Notion with integration token"""
        try:
            result = await self.configure_notion_api(integration_token)
            if result:
                # Test connection immediately
                return await self.test_connection()
            return False
        except Exception as e:
            logger.error(f"Error connecting to Notion: {e}")
            return False

    async def configure_notion_api(
        self, token: Optional[str] = None, api_base: Optional[str] = None
    ):
        """Configure Notion API access"""
        try:
            self._notion_token = token
            if api_base:
                self._notion_api_base = api_base

            # Create HTTP session for Notion API calls
            if self._session is None:
                headers = {}
                if self._notion_token:
                    headers["Authorization"] = f"Bearer {self._notion_token}"
                headers["Notion-Version"] = "2022-06-28"  # Pin to stable version
                headers["Content-Type"] = "application/json"

                self._session = aiohttp.ClientSession(headers=headers)
                logger.info("Notion API session created")

            return True

        except Exception as e:
            logger.error(f"Error configuring Notion API: {e}")
            return False

    async def _call_notion_api(
        self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make Notion API call with rate limiting"""
        try:
            if not self._session:
                logger.warning("Notion API session not configured")
                return None

            url = f"{self._notion_api_base}/{endpoint}"

            # Implement rate limiting (3 requests per second)
            await asyncio.sleep(0.34)  # Ensure we don't exceed rate limit

            if method == "GET":
                async with self._session.get(url) as response:
                    return await self._handle_response(response)
            elif method == "POST":
                async with self._session.post(url, json=data) as response:
                    return await self._handle_response(response)
            elif method == "PATCH":
                async with self._session.patch(url, json=data) as response:
                    return await self._handle_response(response)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None

        except Exception as e:
            logger.error(f"Error calling Notion API: {e}")
            return None

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Optional[Dict[str, Any]]:
        """Handle Notion API response with proper error handling"""
        try:
            if response.status == 200:
                return await response.json()
            elif response.status == 401:
                logger.error("Notion API authentication failed")
                return None
            elif response.status == 429:
                logger.warning("Notion API rate limit exceeded, implementing backoff")
                await asyncio.sleep(1)  # Simple backoff strategy
                return None
            elif response.status == 404:
                logger.warning("Notion resource not found")
                return None
            else:
                logger.error(f"Notion API error: {response.status}")
                return None

        except Exception as e:
            logger.error(f"Error handling Notion API response: {e}")
            return None

    async def test_connection(self) -> bool:
        """Test Notion API connection and authentication"""
        try:
            if not self._notion_token:
                logger.error("Notion token not configured")
                return False

            # Test with a simple API call to retrieve user info
            response = await self._call_notion_api("users/me")
            if response:
                logger.info("Notion API connection successful")
                return True
            else:
                logger.error("Notion API connection failed")
                return False

        except Exception as e:
            logger.error(f"Error testing Notion connection: {e}")
            return False

    async def get_workspace_info(self) -> Optional[Dict[str, Any]]:
        """Get Notion workspace information"""
        try:
            # Note: Notion doesn't have a direct workspace endpoint
            # We'll use the user info as a proxy for workspace access
            user_info = await self._call_notion_api("users/me")
            if user_info:
                return {
                    "workspace_id": user_info.get("bot", {}).get("workspace", {}).get("id"),
                    "workspace_name": user_info.get("bot", {}).get("workspace", {}).get("name"),
                    "user_id": user_info.get("id"),
                    "user_name": user_info.get("name"),
                    "user_email": user_info.get("person", {}).get("email"),
                }
            return None

        except Exception as e:
            logger.error(f"Error getting workspace info: {e}")
            return None

    async def fetch_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """Fetch accessible Notion databases"""
        try:
            response = await self._call_notion_api(
                "search",
                method="POST",
                data={
                    "filter": {"property": "object", "value": "database"},
                    "page_size": min(page_size, 100),  # Notion limit
                },
            )

            if response and "results" in response:
                databases = []
                for db in response["results"]:
                    databases.append(
                        {
                            "id": db["id"],
                            "title": db["title"][0]["plain_text"] if db["title"] else "Untitled",
                            "created_time": db["created_time"],
                            "last_edited_time": db["last_edited_time"],
                            "url": db["url"],
                        }
                    )
                return databases
            return []

        except Exception as e:
            logger.error(f"Error fetching databases: {e}")
            return []

    async def list_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """List accessible Notion databases (alias for fetch_databases)"""
        return await self.fetch_databases(page_size)

    async def get_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        """Get specific database details"""
        try:
            response = await self._call_notion_api(f"databases/{database_id}")
            if response:
                return {
                    "id": response["id"],
                    "title": (
                        response["title"][0]["plain_text"] if response["title"] else "Untitled"
                    ),
                    "properties": response["properties"],
                    "created_time": response["created_time"],
                    "last_edited_time": response["last_edited_time"],
                    "url": response["url"],
                }
            return None

        except Exception as e:
            logger.error(f"Error getting database {database_id}: {e}")
            return None

    async def query_database(
        self,
        database_id: str,
        filter_criteria: Optional[Dict[str, Any]] = None,
        page_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query database with optional filtering"""
        try:
            query_data = {"page_size": min(page_size, 100)}
            if filter_criteria:
                query_data["filter"] = filter_criteria

            response = await self._call_notion_api(
                f"databases/{database_id}/query", method="POST", data=query_data
            )

            if response and "results" in response:
                pages = []
                for page in response["results"]:
                    pages.append(
                        {
                            "id": page["id"],
                            "title": page["properties"]
                            .get("Title", {})
                            .get("title", [{}])[0]
                            .get("plain_text", "Untitled"),
                            "created_time": page["created_time"],
                            "last_edited_time": page["last_edited_time"],
                            "url": page["url"],
                            "properties": page["properties"],
                        }
                    )
                return pages
            return []

        except Exception as e:
            logger.error(f"Error querying database {database_id}: {e}")
            return []

    async def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Get specific page content and properties"""
        try:
            response = await self._call_notion_api(f"pages/{page_id}")
            if response:
                return {
                    "id": response["id"],
                    "title": response["properties"]
                    .get("title", {})
                    .get("title", [{}])[0]
                    .get("plain_text", "Untitled"),
                    "created_time": response["created_time"],
                    "last_edited_time": response["last_edited_time"],
                    "url": response["url"],
                    "properties": response["properties"],
                }
            return None

        except Exception as e:
            logger.error(f"Error getting page {page_id}: {e}")
            return None

    async def get_page_blocks(self, page_id: str, page_size: int = 100) -> List[Dict[str, Any]]:
        """Get page content blocks"""
        try:
            response = await self._call_notion_api(
                f"blocks/{page_id}/children", data={"page_size": min(page_size, 100)}
            )

            if response and "results" in response:
                blocks = []
                for block in response["results"]:
                    blocks.append(
                        {
                            "id": block["id"],
                            "type": block["type"],
                            "created_time": block["created_time"],
                            "last_edited_time": block["last_edited_time"],
                            "content": block.get(block["type"], {}),
                        }
                    )
                return blocks
            return []

        except Exception as e:
            logger.error(f"Error getting page blocks {page_id}: {e}")
            return []

    async def update_page(self, page_id: str, properties: Dict[str, Any]) -> bool:
        """Update page properties"""
        try:
            response = await self._call_notion_api(
                f"pages/{page_id}", method="PATCH", data={"properties": properties}
            )

            if response:
                logger.info(f"Successfully updated page {page_id}")
                return True
            else:
                logger.error(f"Failed to update page {page_id}")
                return False

        except Exception as e:
            logger.error(f"Error updating page {page_id}: {e}")
            return False

    async def create_page(
        self,
        parent_id: str,
        properties: Dict[str, Any],
        content: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create a new page"""
        try:
            page_data = {
                "parent": (
                    {"database_id": parent_id}
                    if parent_id.startswith("db_")
                    else {"page_id": parent_id}
                ),
                "properties": properties,
            }

            if content:
                page_data["children"] = content

            response = await self._call_notion_api("pages", method="POST", data=page_data)

            if response:
                logger.info(f"Successfully created page {response['id']}")
                return {
                    "id": response["id"],
                    "title": response["properties"]
                    .get("title", {})
                    .get("title", [{}])[0]
                    .get("plain_text", "Untitled"),
                    "created_time": response["created_time"],
                    "url": response["url"],
                }
            else:
                logger.error("Failed to create page")
                return None

        except Exception as e:
            logger.error(f"Error creating page: {e}")
            return None

    async def search_notion(
        self, query: str, filter_type: Optional[str] = None, page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Search Notion workspace"""
        try:
            search_data = {"query": query, "page_size": min(page_size, 100)}

            if filter_type:
                search_data["filter"] = {"property": "object", "value": filter_type}

            response = await self._call_notion_api("search", method="POST", data=search_data)

            if response and "results" in response:
                results = []
                for item in response["results"]:
                    results.append(
                        {
                            "id": item["id"],
                            "type": item["type"],
                            "title": (
                                item.get("title", [{}])[0].get("plain_text", "Untitled")
                                if item.get("title")
                                else "Untitled"
                            ),
                            "created_time": item["created_time"],
                            "last_edited_time": item["last_edited_time"],
                            "url": item["url"],
                        }
                    )
                return results
            return []

        except Exception as e:
            logger.error(f"Error searching Notion: {e}")
            return []

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        try:
            response = await self._call_notion_api(f"users/{user_id}")
            if response:
                return {
                    "id": response["id"],
                    "name": response.get("name"),
                    "email": response.get("person", {}).get("email"),
                    "type": response.get("type"),
                }
            return None

        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

    async def list_users(self) -> List[Dict[str, Any]]:
        """List workspace users"""
        try:
            response = await self._call_notion_api("users")
            if response and "results" in response:
                users = []
                for user in response["results"]:
                    users.append(
                        {
                            "id": user["id"],
                            "name": user.get("name"),
                            "email": user.get("person", {}).get("email"),
                            "type": user.get("type"),
                        }
                    )
                return users
            return []

        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return []

    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings"""
        base_stats = super().get_mapping_stats()
        base_stats.update(
            {
                "notion_specific": {
                    "pages_mapped": len(self._page_to_position),
                    "positions_mapped": len(self._position_to_page),
                    "contexts_stored": len(self._context_storage),
                }
            }
        )
        return base_stats

    async def close(self):
        """Clean up resources"""
        try:
            if self._session:
                await self._session.close()
                self._session = None
            logger.info("NotionMCPAdapter resources cleaned up")
        except Exception as e:
            logger.error(f"Error closing NotionMCPAdapter: {e}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        if self._session and not self._session.closed:
            asyncio.create_task(self.close())

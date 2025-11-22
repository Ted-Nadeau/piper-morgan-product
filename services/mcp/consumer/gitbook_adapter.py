"""
GitBook MCP Spatial Adapter

GitBook-specific MCP spatial adapter implementation following the established
spatial adapter pattern for external system integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp

from services.integrations.mcp.token_counter import TokenCounter
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

from .consumer_core import MCPConsumerCore

logger = logging.getLogger(__name__)


class GitBookMCPSpatialAdapter(BaseSpatialAdapter):
    """
    GitBook MCP spatial adapter implementation.

    Maps GitBook content IDs to spatial positions using MCP protocol
    for external service integration. Supports spaces, collections, and pages.
    """

    def __init__(self):
        super().__init__("gitbook_mcp")
        self.mcp_consumer = MCPConsumerCore()
        self._lock = asyncio.Lock()
        self._content_to_position: Dict[str, int] = {}
        self._position_to_content: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # GitBook API configuration
        self._api_base: str = "https://api.gitbook.com/v1"
        self._token: Optional[str] = None

        # HTTP session
        self._session: Optional[aiohttp.ClientSession] = None

        # Token counting for MCP operations (Issue #369)
        self.token_counter = TokenCounter()

        logger.info("GitBookMCPSpatialAdapter initialized")

    async def configure_gitbook_api(
        self, token: Optional[str] = None, api_base: Optional[str] = None
    ):
        """Configure GitBook API access"""
        if token:
            self._token = token
        if api_base:
            self._api_base = api_base

        # Initialize HTTP session with authentication
        headers = {}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        if not self._session:
            self._session = aiohttp.ClientSession(headers=headers)

        logger.info("GitBook API configured")

    async def _call_gitbook_api(
        self, endpoint: str, method: str = "GET", data: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Make API call to GitBook"""
        if not self._session:
            await self.configure_gitbook_api()

        url = f"{self._api_base}{endpoint}"

        try:
            kwargs = {"timeout": 30}
            if data and method.upper() in ["POST", "PUT", "PATCH"]:
                kwargs["json"] = data

            async with self._session.request(method, url, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    # Rate limited - GitBook has 1000 req/hour limit
                    logger.warning("GitBook API rate limited")
                    await asyncio.sleep(60)  # Wait 1 minute
                    return None
                else:
                    logger.warning(
                        f"GitBook API returned {response.status}: {await response.text()}"
                    )
                    return None
        except Exception as e:
            logger.error(f"GitBook API call failed: {e}")
            return None

    async def get_spaces(self) -> List[Dict[str, Any]]:
        """Get accessible GitBook spaces (with token counting)"""

        async def _get():
            result = await self._call_gitbook_api("/spaces")
            if result and "data" in result:
                spaces = []
                for space in result["data"]:
                    standardized = {
                        "id": space.get("id"),
                        "name": space.get("title", space.get("name", "Untitled")),
                        "description": space.get("description", ""),
                        "visibility": space.get("visibility", "private"),
                        "created_at": space.get("createdAt"),
                        "updated_at": space.get("updatedAt"),
                        "type": "space",
                        "url": space.get("url"),
                        "organization": space.get("organization"),
                    }
                    spaces.append(standardized)
                return spaces
            return []

        spaces = await self.token_counter.wrap_mcp_call(
            "gitbook_consumer_get_spaces",
            _get(),
            input_data="",
        )

        logger.info(f"Retrieved {len(spaces)} GitBook spaces")
        return spaces

    async def get_space_content(self, space_id: str) -> Dict[str, Any]:
        """Get space content tree (collections + pages) (with token counting)"""

        async def _get():
            result = await self._call_gitbook_api(f"/spaces/{space_id}")
            if result:
                collections = await self.get_collections(space_id)
                pages = await self._call_gitbook_api(f"/spaces/{space_id}/content")

                standardized = {
                    "id": space_id,
                    "type": "space",
                    "collections": collections,
                    "pages": pages.get("data", []) if pages else [],
                    "space_id": space_id,
                }

                return standardized
            return {}

        content = await self.token_counter.wrap_mcp_call(
            "gitbook_consumer_get_space_content",
            _get(),
            input_data=f"space_id={space_id}",
        )

        logger.info(f"Retrieved content tree for space {space_id}")
        return content

    async def get_collections(self, space_id: str) -> List[Dict[str, Any]]:
        """Get collections in a space (with token counting)"""

        async def _get():
            result = await self._call_gitbook_api(f"/spaces/{space_id}/collections")
            if result and "data" in result:
                collections = []
                for collection in result["data"]:
                    standardized = {
                        "id": collection.get("id"),
                        "name": collection.get("title", "Untitled Collection"),
                        "description": collection.get("description", ""),
                        "space_id": space_id,
                        "type": "collection",
                        "created_at": collection.get("createdAt"),
                        "updated_at": collection.get("updatedAt"),
                        "page_count": len(collection.get("pages", [])),
                    }
                    collections.append(standardized)
                return collections
            return []

        collections = await self.token_counter.wrap_mcp_call(
            "gitbook_consumer_get_collections",
            _get(),
            input_data=f"space_id={space_id}",
        )

        logger.info(f"Retrieved {len(collections)} collections from space {space_id}")
        return collections

    async def get_page(self, space_id: str, page_id: str) -> Optional[Dict[str, Any]]:
        """Get specific page content (with token counting)"""

        async def _get():
            result = await self._call_gitbook_api(f"/spaces/{space_id}/content/{page_id}")
            if result:
                page_data = result.get("data", result)

                standardized = {
                    "id": page_data.get("id", page_id),
                    "title": page_data.get("title", "Untitled"),
                    "description": page_data.get("description", ""),
                    "body": page_data.get("body", {}).get("document", ""),
                    "type": "page",
                    "space_id": space_id,
                    "collection_id": (
                        page_data.get("parent", {}).get("id") if page_data.get("parent") else None
                    ),
                    "visibility": page_data.get("visibility", "public"),
                    "status": page_data.get("status", "published"),
                    "created_at": page_data.get("createdAt"),
                    "updated_at": page_data.get("updatedAt"),
                    "created_by": page_data.get("createdBy"),
                    "contributors": page_data.get("contributors", []),
                    "tags": page_data.get("tags", []),
                    "url": page_data.get("url"),
                    "parent": page_data.get("parent"),
                    "children": page_data.get("children", []),
                    "revision_count": page_data.get("revisionCount", 0),
                }

                if space_data := await self._call_gitbook_api(f"/spaces/{space_id}"):
                    standardized["space"] = {
                        "id": space_id,
                        "title": space_data.get("title", ""),
                        "visibility": space_data.get("visibility", "private"),
                    }

                return standardized
            return None

        page = await self.token_counter.wrap_mcp_call(
            "gitbook_consumer_get_page",
            _get(),
            input_data=f"space_id={space_id},page_id={page_id}",
        )

        logger.info(f"Retrieved page {page_id} from space {space_id}")
        return page

    async def search_pages(
        self, space_id: str, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search pages within a space (with token counting)"""

        async def _search():
            search_endpoint = f"/spaces/{space_id}/search?query={query}&limit={limit}"
            result = await self._call_gitbook_api(search_endpoint)

            if result and "data" in result:
                matching_pages = []

                for item in result["data"][:limit]:
                    if item.get("type") == "page":
                        page_id = item.get("id")
                        full_page = await self.get_page(space_id, page_id)
                        if full_page:
                            matching_pages.append(full_page)
                        else:
                            standardized = {
                                "id": page_id,
                                "title": item.get("title", "Untitled"),
                                "description": item.get("excerpt", ""),
                                "type": "page",
                                "space_id": space_id,
                                "url": item.get("url"),
                                "updated_at": item.get("updatedAt"),
                            }
                            matching_pages.append(standardized)

                return matching_pages

            return await self._fallback_search_pages(space_id, query, limit)

        pages = await self.token_counter.wrap_mcp_call(
            "gitbook_consumer_search_pages",
            _search(),
            input_data=str({"space_id": space_id, "query": query, "limit": limit}),
        )

        logger.info(f"Found {len(pages)} pages matching '{query}' in space {space_id}")
        return pages

    async def _fallback_search_pages(
        self, space_id: str, query: str, limit: int
    ) -> List[Dict[str, Any]]:
        """Fallback search by getting all pages and filtering"""
        try:
            content = await self.get_space_content(space_id)
            all_pages = content.get("pages", [])

            # Also get pages from collections
            for collection in content.get("collections", []):
                collection_pages = await self._call_gitbook_api(
                    f"/spaces/{space_id}/collections/{collection['id']}/pages"
                )
                if collection_pages and "data" in collection_pages:
                    all_pages.extend(collection_pages["data"])

            # Filter by query
            matching_pages = []
            query_lower = query.lower()

            for page in all_pages:
                # Search in title and description
                searchable_text = " ".join(
                    [
                        page.get("title", ""),
                        page.get("description", ""),
                        " ".join(page.get("tags", [])),
                    ]
                ).lower()

                if query_lower in searchable_text:
                    # Get full page details
                    page_id = page.get("id")
                    full_page = await self.get_page(space_id, page_id)
                    if full_page:
                        matching_pages.append(full_page)

                    if len(matching_pages) >= limit:
                        break

            return matching_pages

        except Exception as e:
            logger.warning(f"Fallback search failed: {e}")
            return []

    async def get_users(self, space_id: str) -> List[Dict[str, Any]]:
        """Get space users and permissions (with token counting)"""

        async def _get():
            result = await self._call_gitbook_api(f"/spaces/{space_id}/members")
            if result and "data" in result:
                users = []
                for member in result["data"]:
                    user_data = {
                        "id": member.get("id"),
                        "name": member.get("user", {}).get("displayName", "Unknown"),
                        "email": member.get("user", {}).get("email"),
                        "role": member.get("role", "member"),
                        "permissions": member.get("permissions", []),
                        "joined_at": member.get("joinedAt"),
                    }
                    users.append(user_data)
                return users
            return []

        users = await self.token_counter.wrap_mcp_call(
            "gitbook_consumer_get_users",
            _get(),
            input_data=f"space_id={space_id}",
        )

        logger.info(f"Retrieved {len(users)} users from space {space_id}")
        return users

    async def map_to_position(self, content_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """Map GitBook content ID to spatial position"""
        async with self._lock:
            # Check if we already have a mapping
            if content_id in self._content_to_position:
                position = self._content_to_position[content_id]
                return SpatialPosition(
                    position=position,
                    context={"external_id": content_id, "external_system": "gitbook", **context},
                )

            # Create new mapping
            position = len(self._content_to_position) + 1
            self._content_to_position[content_id] = position
            self._position_to_content[position] = content_id
            self._context_storage[content_id] = context

            logger.info(f"Mapped GitBook content {content_id} to position {position}")

            return SpatialPosition(
                position=position,
                context={"external_id": content_id, "external_system": "gitbook", **context},
            )

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """Map spatial position back to GitBook content ID"""
        return self._position_to_content.get(position.position)

    async def store_mapping(self, content_id: str, position: SpatialPosition) -> bool:
        """Store mapping between GitBook content ID and spatial position"""
        try:
            async with self._lock:
                self._content_to_position[content_id] = position.position
                self._position_to_content[position.position] = content_id
                self._context_storage[content_id] = position.context
            return True
        except Exception as e:
            logger.error(f"Failed to store mapping for GitBook content {content_id}: {e}")
            return False

    async def get_context(self, content_id: str) -> Optional[SpatialContext]:
        """Get spatial context for GitBook content ID"""
        context_data = self._context_storage.get(content_id)
        if not context_data:
            return None

        return SpatialContext(
            territory_id="gitbook",
            room_id=context_data.get("space_name", "unknown"),
            path_id=f"content/{content_id}",
            attention_level=context_data.get("attention_level", "medium"),
            emotional_valence=context_data.get("emotional_valence", "neutral"),
            navigation_intent=context_data.get("navigation_intent", "explore"),
            external_system="gitbook",
            external_id=content_id,
            external_context=context_data,
        )

    async def initialize_connection_pool(self):
        """Initialize MCP connection pool for GitBook integration"""
        try:
            await self.mcp_consumer.initialize()
            logger.info("GitBook MCP connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize GitBook MCP connection pool: {e}")

    async def close(self):
        """Close the GitBook adapter and cleanup resources"""
        if self._session:
            await self._session.close()

        await self.mcp_consumer.close()
        logger.info("GitBook MCP adapter closed")

    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings"""
        return {
            "system_name": self.system_name,
            "total_mappings": len(self._content_to_position),
            "total_contexts": len(self._context_storage),
            "next_position": len(self._content_to_position) + 1,
            "api_base": self._api_base,
            "has_token": self._token is not None,
            "has_session": self._session is not None,
        }

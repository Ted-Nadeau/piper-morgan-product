"""
GitBook MCP Spatial Adapter

GitBook-specific MCP spatial adapter implementation following the established
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


class GitBookMCPAdapter(BaseSpatialAdapter):
    """
    GitBook MCP spatial adapter implementation.

    Maps GitBook page and collection IDs to spatial positions using MCP protocol
    for external service integration.
    """

    def __init__(self):
        super().__init__("gitbook_mcp")
        self._gitbook_token: Optional[str] = None
        self._api_base = "https://api.gitbook.com/v1"
        self._session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()
        self._page_to_position: Dict[str, int] = {}
        self._position_to_page: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        logger.info("GitBookMCPAdapter initialized")

    async def configure_gitbook_api(self, token: str, api_base: Optional[str] = None):
        """Configure GitBook API access"""
        if token:
            self._gitbook_token = token
        if api_base:
            self._api_base = api_base

        # Initialize HTTP session
        if not self._session:
            self._session = aiohttp.ClientSession()

        logger.info("GitBook API configured")

    async def _call_gitbook_api(
        self, endpoint: str, method: str = "GET", data: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Make API call to GitBook"""
        if not self._session:
            await self.configure_gitbook_api("")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._gitbook_token}" if self._gitbook_token else "",
        }

        url = f"{self._api_base}{endpoint}"

        try:
            async with self._session.request(
                method, url, json=data, headers=headers, timeout=30
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(
                        f"GitBook API returned {response.status}: {await response.text()}"
                    )
                    return None
        except Exception as e:
            logger.error(f"GitBook API call failed: {e}")
            return None

    async def get_spaces(self) -> List[Dict[str, Any]]:
        """Get accessible GitBook spaces"""
        try:
            result = await self._call_gitbook_api("/spaces")
            if result and "data" in result:
                spaces = result["data"]
                logger.info(f"Retrieved {len(spaces)} GitBook spaces")
                return spaces
            return []
        except Exception as e:
            logger.error(f"Failed to get GitBook spaces: {e}")
            return []

    async def get_space_content(self, space_id: str) -> Dict[str, Any]:
        """Get space content tree (collections + pages)"""
        try:
            result = await self._call_gitbook_api(f"/spaces/{space_id}/content")
            if result and "data" in result:
                content = result["data"]
                logger.info(f"Retrieved content tree for space {space_id}")
                return content
            return {}
        except Exception as e:
            logger.error(f"Failed to get space content for {space_id}: {e}")
            return {}

    async def get_page(self, space_id: str, page_id: str) -> Optional[Dict[str, Any]]:
        """Get specific page content"""
        try:
            result = await self._call_gitbook_api(f"/spaces/{space_id}/pages/{page_id}")
            if result and "data" in result:
                page = result["data"]
                logger.info(f"Retrieved page {page_id} from space {space_id}")
                return page
            return None
        except Exception as e:
            logger.error(f"Failed to get page {page_id} from space {space_id}: {e}")
            return None

    async def search_pages(
        self, space_id: str, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search pages within a space"""
        try:
            search_data = {"query": query, "limit": limit}
            result = await self._call_gitbook_api(
                f"/spaces/{space_id}/search", method="POST", data=search_data
            )
            if result and "data" in result:
                pages = result["data"].get("results", [])
                logger.info(f"Found {len(pages)} pages matching '{query}' in space {space_id}")
                return pages
            return []
        except Exception as e:
            logger.error(f"Failed to search pages in space {space_id}: {e}")
            return []

    async def get_collections(self, space_id: str) -> List[Dict[str, Any]]:
        """Get collections in a space"""
        try:
            result = await self._call_gitbook_api(f"/spaces/{space_id}/collections")
            if result and "data" in result:
                collections = result["data"]
                logger.info(f"Retrieved {len(collections)} collections from space {space_id}")
                return collections
            return []
        except Exception as e:
            logger.error(f"Failed to get collections for space {space_id}: {e}")
            return []

    async def get_users(self, space_id: str) -> List[Dict[str, Any]]:
        """Get space users and permissions"""
        try:
            result = await self._call_gitbook_api(f"/spaces/{space_id}/users")
            if result and "data" in result:
                users = result["data"]
                logger.info(f"Retrieved {len(users)} users from space {space_id}")
                return users
            return []
        except Exception as e:
            logger.error(f"Failed to get users for space {space_id}: {e}")
            return []

    async def map_to_position(self, page_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """Map GitBook page ID to spatial position"""
        async with self._lock:
            if page_id not in self._page_to_position:
                # Generate new spatial position
                position = len(self._page_to_position) + 1000  # Start from 1000 for GitBook
                self._page_to_position[page_id] = position
                self._position_to_page[position] = page_id
                self._context_storage[page_id] = context

                logger.info(f"Mapped GitBook page {page_id} to position {position}")
            else:
                position = self._page_to_position[page_id]
                # Update context
                self._context_storage[page_id].update(context)

            return SpatialPosition(
                position=position,
                context={"external_id": page_id, "external_system": "gitbook", **context},
            )

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """Map spatial position back to GitBook page ID"""
        return self._position_to_page.get(position.position)

    async def store_mapping(self, page_id: str, position: SpatialPosition) -> bool:
        """Store mapping between GitBook page ID and spatial position"""
        try:
            async with self._lock:
                self._page_to_position[page_id] = position.position
                self._position_to_page[position.position] = page_id
                if position.context:
                    self._context_storage[page_id] = position.context

            logger.info(
                f"Stored mapping for GitBook page {page_id} at position {position.position}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store mapping for GitBook page {page_id}: {e}")
            return False

    async def get_context(self, page_id: str) -> Optional[SpatialContext]:
        """Get spatial context for GitBook page ID"""
        try:
            context_data = self._context_storage.get(page_id, {})
            return SpatialContext(
                territory_id="gitbook",
                room_id=context_data.get("space_id", "unknown"),
                path_id=context_data.get("collection_id"),
                object_position=context_data.get("position"),
                external_system="gitbook",
                external_id=page_id,
                external_context=context_data,
            )
        except Exception as e:
            logger.error(f"Failed to get context for GitBook page {page_id}: {e}")
            return None

    async def get_mapping_stats(self) -> Dict[str, Any]:
        """Get mapping statistics for monitoring"""
        return {
            "total_mappings": len(self._page_to_position),
            "gitbook_pages_mapped": len(self._page_to_position),
            "spatial_positions_used": len(self._position_to_page),
            "context_entries": len(self._context_storage),
        }

    async def close(self):
        """Close the GitBook adapter and cleanup resources"""
        try:
            if self._session:
                await self._session.close()
                self._session = None

            logger.info("GitBook MCP adapter closed")
        except Exception as e:
            logger.error(f"Failed to close GitBook MCP adapter: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get adapter status for health checks"""
        return {
            "adapter_type": "gitbook_mcp",
            "system_name": self.system_name,
            "api_base": self._api_base,
            "token_configured": bool(self._gitbook_token),
            "session_active": self._session is not None,
            "mapping_stats": {
                "total_mappings": len(self._page_to_position),
                "gitbook_pages_mapped": len(self._page_to_position),
            },
        }

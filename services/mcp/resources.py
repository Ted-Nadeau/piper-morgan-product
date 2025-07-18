"""
MCP Resource Management for Piper Morgan
Provides high-level resource access and management for MCP integration.
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .client import MCPResource, MCPResourceContent, PiperMCPClient
from .exceptions import MCPConnectionError

# Try to import connection pool - graceful fallback if not available
try:
    from services.infrastructure.mcp.connection_pool import MCPConnectionPool

    POOL_AVAILABLE = True
except ImportError:
    POOL_AVAILABLE = False
    logger.warning("MCP Connection Pool not available, using direct connections")

logger = logging.getLogger(__name__)


@dataclass
class EnhancedFileResult:
    """Enhanced file search result combining metadata and content"""

    file_id: str
    filename: str
    content_preview: str
    relevance_score: float
    source: str  # "database", "mcp", "combined"
    metadata: Dict[str, Any]


class MCPResourceManager:
    """
    High-level MCP resource management

    Provides enhanced file search capabilities by combining traditional
    file repository operations with MCP resource access.
    """

    def __init__(self, client_config: Optional[Dict[str, Any]] = None):
        self.client_config = client_config or {
            "url": "stdio://./scripts/mcp_file_server.py",
            "timeout": 5.0,
        }
        self.client: Optional[PiperMCPClient] = None
        self.initialized = False
        self.enabled = False  # Will be set by feature flag

        # Connection pooling configuration
        self.use_pool = os.getenv("USE_MCP_POOL", "false").lower() == "true" and POOL_AVAILABLE
        self.connection_pool = None

        # Resource cache with TTL
        self.resource_cache: Dict[str, Any] = {}
        self.cache_ttl = 300  # 5 minutes

        logger.info(f"MCP Resource Manager initialized (pool: {self.use_pool})")

    async def initialize(self, enabled: bool = False) -> bool:
        """Initialize MCP client connection"""
        self.enabled = enabled

        if not self.enabled:
            logger.info("MCP Resource Manager disabled by feature flag")
            return False

        if self.initialized:
            return True

        try:
            if self.use_pool:
                # Use connection pool
                logger.info("Initializing MCP Resource Manager with connection pool")
                self.connection_pool = MCPConnectionPool.get_instance()

                # Test pool connectivity by getting a connection
                async with self.connection_pool.connection(self.client_config) as test_client:
                    if await test_client.is_connected():
                        self.initialized = True
                        logger.info(
                            "MCP Resource Manager initialized successfully with connection pool"
                        )
                        return True
                    else:
                        logger.warning("MCP Resource Manager connection pool test failed")
                        return False
            else:
                # Use direct connection (legacy mode)
                logger.info("Initializing MCP Resource Manager with direct connection")
                self.client = PiperMCPClient(self.client_config)
                connection_success = await self.client.connect()

                if connection_success:
                    self.initialized = True
                    logger.info(
                        "MCP Resource Manager initialized successfully with direct connection"
                    )
                    return True
                else:
                    logger.warning("MCP Resource Manager failed to connect directly")
                    return False

        except Exception as e:
            logger.error(f"Failed to initialize MCP Resource Manager: {e}")
            return False

    async def is_available(self) -> bool:
        """Check if MCP resource manager is available"""
        if not self.enabled:
            return False

        if not self.initialized:
            return False

        if self.use_pool:
            # For pooled connections, check if pool is available
            return self.connection_pool is not None
        else:
            # For direct connections, check client status
            if not self.client:
                return False
            return await self.client.is_connected()

    async def enhanced_file_search(
        self, query: str, session_id: str = None
    ) -> List[EnhancedFileResult]:
        """
        Enhanced file search using MCP content analysis

        Args:
            query: Search query
            session_id: Optional session ID for scoping

        Returns:
            List of enhanced file results
        """
        if not await self.is_available():
            logger.info("MCP not available, returning empty results")
            return []

        # Performance tracking
        start_time = time.time()

        try:
            logger.info(f"Starting MCP enhanced search for query: '{query}'")

            # Search MCP content using pool or direct connection
            search_start = time.time()
            if self.use_pool:
                async with self.connection_pool.connection(self.client_config) as client:
                    content_results = await client.search_content(query)
            else:
                content_results = await self.client.search_content(query)
            search_duration = time.time() - search_start

            logger.info(
                f"MCP content search completed in {search_duration:.3f}s, found {len(content_results)} results"
            )

            # Convert to enhanced results
            processing_start = time.time()
            enhanced_results = []
            for content in content_results:
                # Calculate relevance score (simple implementation)
                relevance_score = self._calculate_relevance_score(content.content, query)

                # Create enhanced result
                result = EnhancedFileResult(
                    file_id=content.uri,  # Use URI as temporary ID
                    filename=self._extract_filename(content.uri),
                    content_preview=self._create_content_preview(content.content, query),
                    relevance_score=relevance_score,
                    source="mcp",
                    metadata=content.metadata or {},
                )
                enhanced_results.append(result)

            # Sort by relevance score
            enhanced_results.sort(key=lambda x: x.relevance_score, reverse=True)
            processing_duration = time.time() - processing_start

            total_duration = time.time() - start_time

            logger.info(f"MCP search processing completed in {processing_duration:.3f}s")
            logger.info(f"Total MCP enhanced search duration: {total_duration:.3f}s")
            logger.info(f"MCP search returned {len(enhanced_results)} results for query: {query}")

            return enhanced_results

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"MCP enhanced search failed after {duration:.3f}s: {e}")
            return []

    def _calculate_relevance_score(self, content: str, query: str) -> float:
        """Simple relevance scoring based on query term frequency"""
        if not content or not query:
            return 0.0

        content_lower = content.lower()
        query_lower = query.lower()
        query_terms = query_lower.split()

        # Count term occurrences
        total_score = 0.0
        for term in query_terms:
            term_count = content_lower.count(term)
            # Normalize by content length and add to score
            if term_count > 0:
                total_score += min(term_count / len(content_lower) * 1000, 1.0)

        # Average score across terms
        return total_score / len(query_terms) if query_terms else 0.0

    def _extract_filename(self, uri: str) -> str:
        """Extract filename from URI"""
        if uri.startswith("file://"):
            return uri.split("/")[-1]
        return uri

    def _create_content_preview(self, content: str, query: str, max_length: int = 200) -> str:
        """Create content preview highlighting query terms"""
        if not content:
            return ""

        query_lower = query.lower()
        content_lower = content.lower()

        # Find first occurrence of query in content
        query_pos = content_lower.find(query_lower)

        if query_pos == -1:
            # Query not found, return beginning of content
            return content[:max_length] + "..." if len(content) > max_length else content

        # Extract context around query
        start = max(0, query_pos - max_length // 2)
        end = min(len(content), query_pos + len(query) + max_length // 2)

        preview = content[start:end]

        # Add ellipsis if truncated
        if start > 0:
            preview = "..." + preview
        if end < len(content):
            preview = preview + "..."

        return preview

    async def get_file_content(self, file_path: str) -> Optional[str]:
        """Get file content by path"""
        if not await self.is_available():
            return None

        try:
            # Convert file path to URI
            uri = f"file://{file_path}"

            # Get resource content using pool or direct connection
            if self.use_pool:
                async with self.connection_pool.connection(self.client_config) as client:
                    content = await client.get_resource(uri)
            else:
                content = await self.client.get_resource(uri)
            return content.content if content else None

        except Exception as e:
            logger.error(f"Failed to get file content for {file_path}: {e}")
            return None

    async def list_available_resources(self) -> List[MCPResource]:
        """List all available MCP resources"""
        if not await self.is_available():
            return []

        try:
            if self.use_pool:
                async with self.connection_pool.connection(self.client_config) as client:
                    return await client.list_resources()
            else:
                return await self.client.list_resources()
        except Exception as e:
            logger.error(f"Failed to list MCP resources: {e}")
            return []

    async def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection and performance statistics"""
        base_stats = {
            "enabled": self.enabled,
            "initialized": self.initialized,
            "available": await self.is_available(),
            "using_pool": self.use_pool,
        }

        if self.use_pool and self.connection_pool:
            # Get pool statistics
            pool_stats = self.connection_pool.get_stats()
            base_stats.update(pool_stats)
        elif self.client:
            # Get direct client statistics
            client_stats = self.client.get_connection_stats()
            base_stats.update(client_stats)

        return base_stats

    async def cleanup(self):
        """Cleanup resources and disconnect"""
        if self.use_pool:
            # For pooled connections, no cleanup needed - pool manages lifecycle
            logger.info("MCP Resource Manager cleanup (pool mode - no action needed)")
        else:
            # For direct connections, disconnect the client
            if self.client:
                await self.client.disconnect()
                self.client = None
            logger.info("MCP Resource Manager cleanup (direct mode - client disconnected)")

        self.initialized = False
        self.resource_cache.clear()
        self.connection_pool = None

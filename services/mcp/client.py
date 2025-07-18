"""
MCP Client for Piper Morgan
Provides connection management and resource access to MCP servers.
"""

import asyncio
import json
import logging
import os
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from .exceptions import MCPCircuitBreakerOpenError, MCPConnectionError, MCPTimeoutError

logger = logging.getLogger(__name__)


@dataclass
class MCPResource:
    """Represents an MCP resource"""

    uri: str
    name: str
    description: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    last_modified: Optional[str] = None


@dataclass
class MCPResourceContent:
    """Represents MCP resource content"""

    uri: str
    content: str
    mime_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MCPCircuitBreaker:
    """Circuit breaker for MCP operations"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
                logger.info("Circuit breaker entering half-open state")
            else:
                raise MCPCircuitBreakerOpenError("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
                logger.info("Circuit breaker closed after successful call")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                logger.error(f"Circuit breaker opened after {self.failure_count} failures")
            raise


class PiperMCPClient:
    """
    MCP Client for Piper Morgan

    Provides connection management and resource access to MCP servers.
    Currently implements a compatibility layer for Python 3.9.6.
    """

    def __init__(self, server_config: Dict[str, Any]):
        self.server_config = server_config
        self.server_url = server_config.get("url", "")
        self.timeout = server_config.get("timeout", 5.0)
        self.connected = False
        self.circuit_breaker = MCPCircuitBreaker()
        self.connection_time = None

        # Simulation data for POC (replace with real MCP when Python 3.10+ available)
        self.simulation_mode = True
        self._simulated_resources: List[MCPResource] = []

        logger.info(f"Initializing MCP client for {self.server_url}")

    async def connect(self) -> bool:
        """Connect to MCP server with timeout and circuit breaker protection"""
        try:
            return await self.circuit_breaker.call(self._connect_impl)
        except MCPCircuitBreakerOpenError:
            logger.warning("Cannot connect: circuit breaker is open")
            return False
        except Exception as e:
            logger.error(f"MCP connection failed: {e}")
            return False

    async def _connect_impl(self) -> bool:
        """Internal connection implementation"""
        start_time = time.time()

        try:
            if self.simulation_mode:
                # Simulate connection to filesystem MCP server
                await self._simulate_filesystem_connection()
            else:
                # Real MCP connection would go here
                # from mcp.client import Client
                # self.client = Client(self.server_url)
                # await self.client.connect()
                pass

            self.connected = True
            self.connection_time = time.time() - start_time
            logger.info(f"MCP connection established in {self.connection_time:.2f}s")
            return True

        except asyncio.TimeoutError:
            raise MCPTimeoutError(f"Connection timeout after {self.timeout}s")
        except Exception as e:
            raise MCPConnectionError(f"Failed to connect to MCP server: {e}")

    async def _simulate_filesystem_connection(self):
        """Simulate filesystem MCP server connection"""
        # Simulate some connection delay
        await asyncio.sleep(0.1)

        # Scan uploads directory to simulate MCP filesystem server
        uploads_dir = "uploads"
        if os.path.exists(uploads_dir):
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    resource = MCPResource(
                        uri=f"file://{file_path}",
                        name=filename,
                        description=f"File from uploads directory",
                        mime_type=self._guess_mime_type(filename),
                        size=stat.st_size,
                        last_modified=time.ctime(stat.st_mtime),
                    )
                    self._simulated_resources.append(resource)

        logger.info(
            f"Simulated filesystem MCP server with {len(self._simulated_resources)} resources"
        )

    def _guess_mime_type(self, filename: str) -> str:
        """Simple mime type guessing based on extension"""
        ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".md": "text/markdown",
            ".json": "application/json",
            ".csv": "text/csv",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        return mime_types.get(ext, "application/octet-stream")

    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.connected:
            self.connected = False
            self.connection_time = None
            logger.info("MCP client disconnected")

    async def is_connected(self) -> bool:
        """Check if client is connected to MCP server"""
        return self.connected

    async def list_resources(self) -> List[MCPResource]:
        """List available resources from MCP server"""
        if not self.connected:
            raise MCPConnectionError("Client not connected to MCP server")

        try:
            return await self.circuit_breaker.call(self._list_resources_impl)
        except MCPCircuitBreakerOpenError:
            logger.warning("Cannot list resources: circuit breaker is open")
            return []
        except Exception as e:
            logger.error(f"Failed to list MCP resources: {e}")
            return []

    async def _list_resources_impl(self) -> List[MCPResource]:
        """Internal implementation of list resources"""
        if self.simulation_mode:
            # Return simulated resources
            return self._simulated_resources.copy()
        else:
            # Real MCP implementation would go here
            # return await self.client.list_resources()
            return []

    async def get_resource(self, uri: str) -> Optional[MCPResourceContent]:
        """Get resource content by URI"""
        if not self.connected:
            raise MCPConnectionError("Client not connected to MCP server")

        try:
            return await self.circuit_breaker.call(self._get_resource_impl, uri)
        except MCPCircuitBreakerOpenError:
            logger.warning("Cannot get resource: circuit breaker is open")
            return None
        except Exception as e:
            logger.error(f"Failed to get MCP resource {uri}: {e}")
            return None

    async def _get_resource_impl(self, uri: str) -> Optional[MCPResourceContent]:
        """Internal implementation of get resource"""
        if self.simulation_mode:
            # Find resource by URI
            for resource in self._simulated_resources:
                if resource.uri == uri:
                    # Read file content
                    file_path = uri.replace("file://", "")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        return MCPResourceContent(
                            uri=uri,
                            content=content,
                            mime_type=resource.mime_type,
                            metadata={
                                "size": resource.size,
                                "last_modified": resource.last_modified,
                            },
                        )
                    except Exception as e:
                        logger.error(f"Failed to read file {file_path}: {e}")
                        return None
            return None
        else:
            # Real MCP implementation would go here
            # return await self.client.get_resource(uri)
            return None

    async def search_content(self, query: str) -> List[MCPResourceContent]:
        """Search for content matching query"""
        if not self.connected:
            raise MCPConnectionError("Client not connected to MCP server")

        try:
            return await self.circuit_breaker.call(self._search_content_impl, query)
        except MCPCircuitBreakerOpenError:
            logger.warning("Cannot search content: circuit breaker is open")
            return []
        except Exception as e:
            logger.error(f"Failed to search MCP content: {e}")
            return []

    async def _search_content_impl(self, query: str) -> List[MCPResourceContent]:
        """Internal implementation of content search"""
        if self.simulation_mode:
            results = []
            query_lower = query.lower()

            for resource in self._simulated_resources:
                # Get resource content
                content = await self._get_resource_impl(resource.uri)
                if content and query_lower in content.content.lower():
                    results.append(content)

            return results
        else:
            # Real MCP implementation would go here
            # return await self.client.search_content(query)
            return []

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "connected": self.connected,
            "connection_time": self.connection_time,
            "circuit_breaker_state": self.circuit_breaker.state,
            "circuit_breaker_failures": self.circuit_breaker.failure_count,
            "server_url": self.server_url,
            "simulation_mode": self.simulation_mode,
            "resource_count": len(self._simulated_resources) if self.simulation_mode else 0,
        }

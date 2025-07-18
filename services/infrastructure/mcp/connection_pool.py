"""
MCP Connection Pool Infrastructure
Manages pooled connections to MCP servers with circuit breaker pattern.
"""

import asyncio
import logging
import threading
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from services.mcp.client import PiperMCPClient
from services.mcp.exceptions import MCPCircuitBreakerOpenError, MCPConnectionError

logger = logging.getLogger(__name__)


class MCPConnectionPool:
    """
    Singleton connection pool for MCP clients with circuit breaker protection.

    Manages a pool of reusable MCP connections to prevent connection per request.
    Includes health monitoring, graceful shutdown, and fault tolerance.
    """

    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        """Private constructor - use get_instance() instead"""
        if MCPConnectionPool._instance is not None:
            raise RuntimeError("MCPConnectionPool is a singleton. Use get_instance() method.")

        # Configuration
        self.max_connections = 5
        self.connection_timeout = 5.0
        self.circuit_breaker_threshold = 5
        self.circuit_breaker_timeout = 60

        # Connection management
        self._available_connections: List[PiperMCPClient] = []
        self._all_connections: List[PiperMCPClient] = []
        self._connection_semaphore = None  # Will be initialized lazily
        self._pool_lock = None  # Will be initialized lazily

        # Circuit breaker state
        self._failure_count = 0
        self._last_failure_time = 0
        self._circuit_state = "closed"  # closed, open, half-open

        # Lifecycle management
        self._is_shutdown = False

        logger.info("MCPConnectionPool initialized")

    @classmethod
    def get_instance(cls) -> "MCPConnectionPool":
        """Get singleton instance of connection pool"""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def _reset_instance(cls):
        """Reset singleton instance (for testing only)"""
        with cls._instance_lock:
            if cls._instance is not None:
                # Reset state for clean testing
                cls._instance._is_shutdown = False
                cls._instance._available_connections.clear()
                cls._instance._all_connections.clear()
                cls._instance._connection_semaphore = None
                cls._instance._pool_lock = None
                cls._instance._failure_count = 0
                cls._instance._circuit_state = "closed"
            cls._instance = None

    def configure(self, config: Dict[str, Any]):
        """Configure connection pool parameters"""
        if "max_connections" in config:
            if config["max_connections"] <= 0:
                raise ValueError("max_connections must be positive")
            self.max_connections = config["max_connections"]
            # Reset semaphore with new limit
            self._connection_semaphore = None

        if "connection_timeout" in config:
            if config["connection_timeout"] <= 0:
                raise ValueError("connection_timeout must be positive")
            self.connection_timeout = config["connection_timeout"]

        if "circuit_breaker_threshold" in config:
            self.circuit_breaker_threshold = config["circuit_breaker_threshold"]

        if "circuit_breaker_timeout" in config:
            self.circuit_breaker_timeout = config["circuit_breaker_timeout"]

        logger.info(
            f"Connection pool configured: max={self.max_connections}, timeout={self.connection_timeout}"
        )

    async def _ensure_async_resources(self):
        """Initialize async resources lazily"""
        if self._connection_semaphore is None:
            self._connection_semaphore = asyncio.Semaphore(self.max_connections)
        if self._pool_lock is None:
            self._pool_lock = asyncio.Lock()

    async def get_connection(self, server_config: Dict[str, Any]) -> PiperMCPClient:
        """
        Get an MCP connection from the pool or create a new one.

        Args:
            server_config: Configuration for MCP server connection

        Returns:
            Connected MCP client instance

        Raises:
            MCPCircuitBreakerOpenError: When circuit breaker is open
            MCPConnectionError: When connection fails
            RuntimeError: When pool is shut down
            asyncio.TimeoutError: When connection times out
        """
        if self._is_shutdown:
            raise RuntimeError("Connection pool is shut down")

        # Check circuit breaker
        await self._check_circuit_breaker()

        # Initialize async resources if needed
        await self._ensure_async_resources()

        try:
            # Acquire semaphore with timeout
            await asyncio.wait_for(
                self._connection_semaphore.acquire(), timeout=self.connection_timeout
            )
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for connection from pool")
            raise

        try:
            return await self._get_or_create_connection(server_config)
        except Exception as e:
            # Release semaphore on failure
            self._connection_semaphore.release()
            await self._record_failure()
            raise

    async def _get_or_create_connection(self, server_config: Dict[str, Any]) -> PiperMCPClient:
        """Get existing connection or create new one"""
        # Ensure lock is initialized
        if self._pool_lock is None:
            self._pool_lock = asyncio.Lock()

        async with self._pool_lock:
            # Try to reuse existing connection
            if self._available_connections:
                connection = self._available_connections.pop()

                # Verify connection is still alive
                if await connection.is_connected():
                    logger.debug("Reusing existing MCP connection")
                    return connection
                else:
                    # Remove dead connection
                    logger.warning("Removing dead connection from pool")
                    await self._remove_connection(connection)

            # Create new connection
            return await self._create_new_connection(server_config)

    async def _create_new_connection(self, server_config: Dict[str, Any]) -> PiperMCPClient:
        """Create and connect a new MCP client"""
        try:
            connection = PiperMCPClient(server_config)

            # Connect with timeout
            connect_task = asyncio.create_task(connection.connect())
            success = await asyncio.wait_for(connect_task, timeout=self.connection_timeout)

            if not success:
                raise MCPConnectionError("Failed to establish MCP connection")

            # Add to tracked connections (pool lock already held by caller)
            self._all_connections.append(connection)

            logger.info("Created new MCP connection")
            await self._record_success()
            return connection

        except asyncio.TimeoutError:
            logger.error(f"MCP connection timeout after {self.connection_timeout}s")
            raise
        except Exception as e:
            logger.error(f"Failed to create MCP connection: {e}")
            raise MCPConnectionError(f"Connection creation failed: {e}")

    async def return_connection(self, connection: PiperMCPClient):
        """
        Return a connection to the pool for reuse.

        Args:
            connection: MCP client to return to pool
        """
        if self._is_shutdown:
            await connection.disconnect()
            return

        try:
            # Verify connection is still alive
            if await connection.is_connected():
                async with self._pool_lock:
                    self._available_connections.append(connection)
                logger.debug("Returned connection to pool")
            else:
                # Connection is dead, remove it
                await self._remove_connection(connection)
                logger.warning("Discarded dead connection instead of returning to pool")
        finally:
            # Always release semaphore
            self._connection_semaphore.release()

    async def _remove_connection(self, connection: PiperMCPClient):
        """Remove connection from pool and disconnect"""
        async with self._pool_lock:
            if connection in self._all_connections:
                self._all_connections.remove(connection)
            if connection in self._available_connections:
                self._available_connections.remove(connection)

        try:
            await connection.disconnect()
        except Exception as e:
            logger.warning(f"Error disconnecting removed connection: {e}")

    async def health_check(self):
        """Check health of pooled connections and remove dead ones"""
        dead_connections = []

        async with self._pool_lock:
            for connection in self._available_connections.copy():
                if not await connection.is_connected():
                    dead_connections.append(connection)
                    self._available_connections.remove(connection)

        # Clean up dead connections
        for connection in dead_connections:
            await self._remove_connection(connection)
            logger.info("Removed dead connection during health check")

    async def _check_circuit_breaker(self):
        """Check circuit breaker state and potentially throw or recover"""
        if self._circuit_state == "open":
            if time.time() - self._last_failure_time > self.circuit_breaker_timeout:
                self._circuit_state = "half-open"
                logger.info("Circuit breaker entering half-open state")
            else:
                raise MCPCircuitBreakerOpenError("Circuit breaker is open")

    async def _record_failure(self):
        """Record a connection failure for circuit breaker"""
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self.circuit_breaker_threshold:
            self._circuit_state = "open"
            logger.error(f"Circuit breaker opened after {self._failure_count} failures")

    async def _record_success(self):
        """Record a successful connection for circuit breaker"""
        if self._circuit_state == "half-open":
            self._circuit_state = "closed"
            self._failure_count = 0
            logger.info("Circuit breaker closed after successful connection")

    async def shutdown(self):
        """Gracefully shutdown the connection pool"""
        self._is_shutdown = True

        logger.info("Shutting down MCP connection pool")

        # Disconnect all connections
        if self._pool_lock is not None:
            async with self._pool_lock:
                all_connections = self._all_connections.copy()
                self._all_connections.clear()
                self._available_connections.clear()
        else:
            all_connections = self._all_connections.copy()
            self._all_connections.clear()
            self._available_connections.clear()

        # Disconnect all connections
        for connection in all_connections:
            try:
                await connection.disconnect()
            except Exception as e:
                logger.warning(f"Error disconnecting connection during shutdown: {e}")

        logger.info("MCP connection pool shutdown complete")

    @property
    def available_connections(self) -> int:
        """Number of available connections in pool"""
        return len(self._available_connections)

    @property
    def total_connections(self) -> int:
        """Total number of connections managed by pool"""
        return len(self._all_connections)

    @property
    def active_connections(self) -> int:
        """Number of active (checked out) connections"""
        return self.total_connections - self.available_connections

    def get_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        return {
            "total_connections": self.total_connections,
            "available_connections": self.available_connections,
            "active_connections": self.active_connections,
            "max_connections": self.max_connections,
            "circuit_breaker_state": self._circuit_state,
            "failure_count": self._failure_count,
            "is_shutdown": self._is_shutdown,
        }

    @asynccontextmanager
    async def connection(self, server_config: Dict[str, Any]):
        """
        Context manager for getting and returning connections automatically.

        Usage:
            async with pool.connection(config) as conn:
                # Use connection
                resources = await conn.list_resources()
        """
        connection = await self.get_connection(server_config)
        try:
            yield connection
        finally:
            await self.return_connection(connection)

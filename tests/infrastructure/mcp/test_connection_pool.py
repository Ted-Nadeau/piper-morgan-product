"""
Test suite for MCP Connection Pool
Tests the infrastructure layer connection pooling with circuit breaker pattern.
"""

import asyncio
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.infrastructure.mcp.connection_pool import MCPConnectionPool
from services.mcp.client import PiperMCPClient
from services.mcp.exceptions import MCPCircuitBreakerOpenError, MCPConnectionError


class TestMCPConnectionPoolSingleton:
    """Test singleton pattern enforcement"""

    def test_singleton_pattern_enforced(self):
        """Connection pool should enforce singleton pattern"""
        pool1 = MCPConnectionPool.get_instance()
        pool2 = MCPConnectionPool.get_instance()

        assert pool1 is pool2
        assert id(pool1) == id(pool2)

    def test_singleton_across_threads(self):
        """Singleton should work across multiple threads"""
        import threading

        instances = []

        def create_instance():
            instances.append(MCPConnectionPool.get_instance())

        threads = [threading.Thread(target=create_instance) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # All instances should be the same
        first_instance = instances[0]
        for instance in instances[1:]:
            assert instance is first_instance

    def test_cannot_instantiate_directly(self):
        """Direct instantiation should be prevented"""
        with pytest.raises(RuntimeError, match="Use get_instance"):
            MCPConnectionPool()


class TestMCPConnectionPoolConfiguration:
    """Test connection pool configuration and limits"""

    @pytest.fixture
    def pool_config(self):
        return {
            "max_connections": 3,
            "connection_timeout": 5.0,
            "circuit_breaker_threshold": 2,
            "circuit_breaker_timeout": 30,
        }

    def test_default_configuration(self):
        """Pool should have sensible defaults"""
        pool = MCPConnectionPool.get_instance()

        assert pool.max_connections == 5
        assert pool.connection_timeout == 5.0
        assert pool.circuit_breaker_threshold == 5
        assert pool.circuit_breaker_timeout == 60

    def test_custom_configuration(self, pool_config):
        """Pool should accept custom configuration"""
        pool = MCPConnectionPool.get_instance()
        pool.configure(pool_config)

        assert pool.max_connections == 3
        assert pool.connection_timeout == 5.0
        assert pool.circuit_breaker_threshold == 2
        assert pool.circuit_breaker_timeout == 30

    def test_configuration_validation(self):
        """Invalid configuration should raise errors"""
        pool = MCPConnectionPool.get_instance()

        with pytest.raises(ValueError, match="max_connections must be positive"):
            pool.configure({"max_connections": 0})

        with pytest.raises(ValueError, match="connection_timeout must be positive"):
            pool.configure({"connection_timeout": -1})


class TestMCPConnectionPoolLifecycle:
    """Test connection lifecycle management"""

    @pytest.fixture
    def server_config(self):
        return {"url": "test://localhost:8080", "timeout": 5.0}

    @pytest.fixture
    def pool(self):
        # Reset singleton before test
        MCPConnectionPool._reset_instance()
        pool = MCPConnectionPool.get_instance()
        yield pool
        # Cleanup after each test
        asyncio.run(pool.shutdown())
        pool._reset_instance()  # Reset singleton for clean state

    async def test_get_connection_creates_new_when_empty(self, pool, server_config):
        """Should create new connection when pool is empty"""
        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.connect.return_value = True
            mock_client.is_connected.return_value = True
            mock_client_class.return_value = mock_client

            connection = await pool.get_connection(server_config)

            assert connection is not None
            assert connection is mock_client
            mock_client_class.assert_called_once_with(server_config)
            mock_client.connect.assert_called_once()

    async def test_get_connection_reuses_existing(self, pool, server_config):
        """Should reuse existing connection when available"""
        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.connect.return_value = True
            mock_client.is_connected.return_value = True
            mock_client_class.return_value = mock_client

            # Get first connection
            connection1 = await pool.get_connection(server_config)

            # Return it to pool
            await pool.return_connection(connection1)

            # Get second connection - should be the same
            connection2 = await pool.get_connection(server_config)

            assert connection1 is connection2
            # Client should only be created once
            mock_client_class.assert_called_once()

    async def test_connection_limit_enforced(self, pool, server_config):
        """Should enforce maximum connection limit"""
        pool.configure({"max_connections": 2})

        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            mock_clients = [AsyncMock() for _ in range(3)]
            for mock_client in mock_clients:
                mock_client.connect.return_value = True
                mock_client.is_connected.return_value = True
            mock_client_class.side_effect = mock_clients

            # Get max connections
            connection1 = await pool.get_connection(server_config)
            connection2 = await pool.get_connection(server_config)

            # Third should timeout
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(pool.get_connection(server_config), timeout=0.1)

    async def test_return_connection_to_pool(self, pool, server_config):
        """Should properly return connection to pool"""
        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.connect.return_value = True
            mock_client.is_connected.return_value = True
            mock_client_class.return_value = mock_client

            connection = await pool.get_connection(server_config)

            # Pool should have 0 available connections
            assert pool.available_connections == 0

            await pool.return_connection(connection)

            # Pool should have 1 available connection
            assert pool.available_connections == 1


class TestMCPConnectionPoolCircuitBreaker:
    """Test circuit breaker integration"""

    @pytest.fixture
    def pool(self):
        # Reset singleton before test
        MCPConnectionPool._reset_instance()
        pool = MCPConnectionPool.get_instance()
        pool.configure({"circuit_breaker_threshold": 2, "circuit_breaker_timeout": 1})
        yield pool
        asyncio.run(pool.shutdown())
        pool._reset_instance()

    @pytest.fixture
    def server_config(self):
        return {"url": "test://localhost:8080"}

    async def test_circuit_breaker_opens_on_failures(self, pool, server_config):
        """Circuit breaker should open after threshold failures"""
        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()
            mock_client.connect.side_effect = MCPConnectionError("Connection failed")
            mock_client_class.return_value = mock_client

            # First failure
            with pytest.raises(MCPConnectionError):
                await pool.get_connection(server_config)

            # Second failure - should open circuit breaker
            with pytest.raises(MCPConnectionError):
                await pool.get_connection(server_config)

            # Third attempt should fail with circuit breaker error
            with pytest.raises(MCPCircuitBreakerOpenError):
                await pool.get_connection(server_config)

    async def test_circuit_breaker_recovers_after_timeout(self, pool, server_config):
        """Circuit breaker should recover after timeout"""
        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            # First: fail to open circuit breaker
            mock_client_fail = AsyncMock()
            mock_client_fail.connect.side_effect = MCPConnectionError("Connection failed")

            # Then: succeed to close circuit breaker
            mock_client_success = AsyncMock()
            mock_client_success.connect.return_value = True
            mock_client_success.is_connected.return_value = True

            mock_client_class.side_effect = [
                mock_client_fail,
                mock_client_fail,
                mock_client_success,
            ]

            # Cause circuit breaker to open
            with pytest.raises(MCPConnectionError):
                await pool.get_connection(server_config)
            with pytest.raises(MCPConnectionError):
                await pool.get_connection(server_config)

            # Wait for recovery timeout
            await asyncio.sleep(1.1)

            # Should succeed now
            connection = await pool.get_connection(server_config)
            assert connection is not None


class TestMCPConnectionPoolGracefulShutdown:
    """Test graceful shutdown and cleanup"""

    @pytest.fixture
    def pool(self):
        # Reset singleton before test
        MCPConnectionPool._reset_instance()
        pool = MCPConnectionPool.get_instance()
        return pool

    @pytest.fixture
    def server_config(self):
        return {"url": "test://localhost:8080"}

    async def test_shutdown_disconnects_all_connections(self, pool, server_config):
        """Shutdown should disconnect all active connections"""
        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            mock_clients = [AsyncMock() for _ in range(3)]
            for mock_client in mock_clients:
                mock_client.connect.return_value = True
                mock_client.is_connected.return_value = True
            mock_client_class.side_effect = mock_clients

            # Create connections
            connections = []
            for _ in range(3):
                conn = await pool.get_connection(server_config)
                connections.append(conn)

            # Shutdown
            await pool.shutdown()

            # All connections should be disconnected
            for mock_client in mock_clients:
                mock_client.disconnect.assert_called_once()

    async def test_shutdown_prevents_new_connections(self, pool, server_config):
        """After shutdown, no new connections should be created"""
        await pool.shutdown()

        with pytest.raises(RuntimeError, match="Connection pool is shut down"):
            await pool.get_connection(server_config)

    async def test_timeout_handling(self, pool, server_config):
        """Connection timeouts should be handled gracefully"""
        pool.configure({"connection_timeout": 0.1})

        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            mock_client = AsyncMock()

            # Simulate slow connection
            async def slow_connect():
                await asyncio.sleep(0.2)
                return True

            mock_client.connect.side_effect = slow_connect
            mock_client_class.return_value = mock_client

            with pytest.raises(asyncio.TimeoutError):
                await pool.get_connection(server_config)


class TestMCPConnectionPoolHealthMonitoring:
    """Test connection health monitoring"""

    @pytest.fixture
    def pool(self):
        # Reset singleton before test
        MCPConnectionPool._reset_instance()
        pool = MCPConnectionPool.get_instance()
        yield pool
        asyncio.run(pool.shutdown())
        pool._reset_instance()

    async def test_health_check_removes_dead_connections(self, pool):
        """Health check should remove dead connections from pool"""
        with patch(
            "services.infrastructure.mcp.connection_pool.PiperMCPClient"
        ) as mock_client_class:
            # Create a connection that becomes dead after being added to pool
            mock_client = AsyncMock()
            mock_client.connect.return_value = True

            # Initially alive, then becomes dead
            is_alive = True

            def mock_is_connected():
                return is_alive

            mock_client.is_connected.side_effect = mock_is_connected
            mock_client_class.return_value = mock_client

            # Add to pool while alive
            server_config = {"url": "test://localhost:8080"}
            connection = await pool.get_connection(server_config)
            await pool.return_connection(connection)

            # Should have 1 available connection
            assert pool.available_connections == 1

            # Connection dies
            is_alive = False

            # Run health check
            await pool.health_check()

            # Dead connection should be removed
            assert pool.available_connections == 0
            mock_client.disconnect.assert_called_once()

    def test_get_pool_stats(self, pool):
        """Should provide pool statistics"""
        stats = pool.get_stats()

        expected_keys = [
            "total_connections",
            "available_connections",
            "active_connections",
            "max_connections",
            "circuit_breaker_state",
            "failure_count",
        ]

        for key in expected_keys:
            assert key in stats

        assert isinstance(stats["total_connections"], int)
        assert isinstance(stats["available_connections"], int)
        assert isinstance(stats["active_connections"], int)

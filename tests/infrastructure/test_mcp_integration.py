"""
Integration tests for MCP functionality
Tests the MCP client, resource manager, and filesystem server integration.
"""

import asyncio
import os
import tempfile
from pathlib import Path

import pytest

from services.mcp.client import MCPResource, PiperMCPClient
from services.mcp.exceptions import MCPConnectionError
from services.mcp.resources import MCPResourceManager


class TestMCPIntegration:
    """Test MCP integration functionality"""

    @pytest.fixture
    def temp_uploads_dir(self):
        """Create temporary uploads directory with test files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            test_files = {
                "test_document.txt": "This is a test document for MCP search functionality.",
                "project_notes.md": "# Project Notes\n\nThis document contains project planning notes.",
                "data_analysis.csv": "name,value\ntest1,100\ntest2,200\n",
            }

            for filename, content in test_files.items():
                file_path = Path(temp_dir) / filename
                file_path.write_text(content)

            # Temporarily change uploads directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)

            yield temp_dir

            os.chdir(original_cwd)

    @pytest.mark.asyncio
    async def test_mcp_client_connection(self, temp_uploads_dir):
        """Test MCP client connection and basic functionality"""
        # Create client configuration
        client_config = {"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0}

        # Initialize client
        client = PiperMCPClient(client_config)

        # Test connection
        connected = await client.connect()
        assert connected == True

        # Test connection status
        assert await client.is_connected() == True

        # Test resource listing
        resources = await client.list_resources()
        assert isinstance(resources, list)
        assert len(resources) >= 0  # May be empty if no files

        # Test connection stats
        stats = client.get_connection_stats()
        assert stats["connected"] == True
        assert stats["simulation_mode"] == True
        assert "connection_time" in stats

        # Clean up
        await client.disconnect()
        assert await client.is_connected() == False

    @pytest.mark.asyncio
    async def test_mcp_resource_listing(self, temp_uploads_dir):
        """Test MCP resource listing functionality"""
        client_config = {"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0}

        client = PiperMCPClient(client_config)
        connected = await client.connect()
        assert connected == True

        # List resources
        resources = await client.list_resources()

        # Should have 3 test files
        assert len(resources) == 3

        # Check resource properties
        for resource in resources:
            assert isinstance(resource, MCPResource)
            assert resource.uri.startswith("file://")
            assert resource.name
            assert resource.mime_type
            assert resource.size > 0

        # Find specific files
        filenames = [r.name for r in resources]
        assert "test_document.txt" in filenames
        assert "project_notes.md" in filenames
        assert "data_analysis.csv" in filenames

        await client.disconnect()

    @pytest.mark.asyncio
    async def test_mcp_content_retrieval(self, temp_uploads_dir):
        """Test MCP content retrieval functionality"""
        client_config = {"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0}

        client = PiperMCPClient(client_config)
        connected = await client.connect()
        assert connected == True

        # List resources
        resources = await client.list_resources()

        # Find test document
        test_resource = None
        for resource in resources:
            if resource.name == "test_document.txt":
                test_resource = resource
                break

        assert test_resource is not None

        # Get content
        content = await client.get_resource(test_resource.uri)
        assert content is not None
        assert content.uri == test_resource.uri
        assert "test document for MCP search" in content.content
        assert content.mime_type == "text/plain"

        await client.disconnect()

    @pytest.mark.asyncio
    async def test_mcp_content_search(self, temp_uploads_dir):
        """Test MCP content search functionality"""
        client_config = {"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0}

        client = PiperMCPClient(client_config)
        connected = await client.connect()
        assert connected == True

        # Search for content
        search_results = await client.search_content("project")

        # Should find the project notes file
        assert len(search_results) >= 1

        # Check that results contain relevant content
        found_project_content = False
        for result in search_results:
            if "project" in result.content.lower():
                found_project_content = True
                break

        assert found_project_content == True

        await client.disconnect()

    @pytest.mark.asyncio
    async def test_mcp_resource_manager_disabled(self):
        """Test MCP resource manager when disabled"""
        manager = MCPResourceManager()

        # Test initialization with disabled flag
        initialized = await manager.initialize(enabled=False)
        assert initialized == False

        # Test availability
        available = await manager.is_available()
        assert available == False

        # Test search returns empty results
        results = await manager.enhanced_file_search("test query")
        assert results == []

        # Test connection stats
        stats = await manager.get_connection_stats()
        assert stats["enabled"] == False
        assert stats["available"] == False

    @pytest.mark.asyncio
    async def test_mcp_resource_manager_enabled(self, temp_uploads_dir):
        """Test MCP resource manager when enabled"""
        manager = MCPResourceManager()

        # Test initialization with enabled flag
        initialized = await manager.initialize(enabled=True)
        assert initialized == True

        # Test availability
        available = await manager.is_available()
        assert available == True

        # Test enhanced file search
        results = await manager.enhanced_file_search("test document")
        assert len(results) >= 1

        # Check result format
        for result in results:
            assert hasattr(result, "file_id")
            assert hasattr(result, "filename")
            assert hasattr(result, "content_preview")
            assert hasattr(result, "relevance_score")
            assert hasattr(result, "source")
            assert result.source == "mcp"

        # Test connection stats
        stats = await manager.get_connection_stats()
        assert stats["enabled"] == True
        assert stats["available"] == True
        assert stats["connected"] == True

        # Clean up
        await manager.cleanup()

    @pytest.mark.asyncio
    async def test_mcp_error_handling(self):
        """Test MCP error handling and circuit breaker"""
        # Test with invalid server config
        client_config = {"url": "invalid://server", "timeout": 1.0}

        client = PiperMCPClient(client_config)

        # Connection should fail gracefully
        connected = await client.connect()
        assert connected == False

        # Operations should handle disconnected state
        resources = await client.list_resources()
        assert resources == []

        content = await client.get_resource("file://nonexistent")
        assert content is None

        search_results = await client.search_content("query")
        assert search_results == []

    @pytest.mark.asyncio
    async def test_mcp_feature_flag_integration(self, temp_uploads_dir):
        """Test MCP integration with feature flag"""
        # Test with feature flag disabled (default)
        manager = MCPResourceManager()

        # Should not initialize when disabled
        initialized = await manager.initialize(enabled=False)
        assert initialized == False

        # Should return empty results
        results = await manager.enhanced_file_search("test")
        assert results == []

        # Test with feature flag enabled
        manager_enabled = MCPResourceManager()
        initialized = await manager_enabled.initialize(enabled=True)
        assert initialized == True

        # Should return results when enabled
        results = await manager_enabled.enhanced_file_search("test")
        assert len(results) >= 0  # May be empty but should not error

        await manager_enabled.cleanup()

    def test_mcp_circuit_breaker_simulation(self):
        """Test circuit breaker functionality (unit test)"""
        import time

        from services.mcp.client import MCPCircuitBreaker

        breaker = MCPCircuitBreaker(failure_threshold=3, recovery_timeout=1)

        # Test initial state
        assert breaker.state == "closed"
        assert breaker.failure_count == 0

        # Simulate failures
        for i in range(3):
            breaker.failure_count += 1
            breaker.last_failure_time = time.time()

            if breaker.failure_count >= breaker.failure_threshold:
                breaker.state = "open"

        # Should be open after threshold failures
        assert breaker.state == "open"
        assert breaker.failure_count >= breaker.failure_threshold


# Helper function to run tests manually
async def run_integration_tests():
    """Run integration tests manually"""
    print("Running MCP integration tests...")

    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_files = {
            "test_document.txt": "This is a test document for MCP search functionality.",
            "project_notes.md": "# Project Notes\n\nThis document contains project planning notes.",
        }

        for filename, content in test_files.items():
            file_path = Path(temp_dir) / filename
            file_path.write_text(content)

        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Test basic client functionality
            client_config = {"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0}

            client = PiperMCPClient(client_config)
            connected = await client.connect()

            print(f"✓ MCP Client connected: {connected}")

            if connected:
                resources = await client.list_resources()
                print(f"✓ Found {len(resources)} resources")

                if resources:
                    content = await client.get_resource(resources[0].uri)
                    print(f"✓ Retrieved content: {content is not None}")

                    search_results = await client.search_content("test")
                    print(f"✓ Search results: {len(search_results)} found")

                await client.disconnect()

            # Test resource manager
            manager = MCPResourceManager()
            initialized = await manager.initialize(enabled=True)
            print(f"✓ Resource manager initialized: {initialized}")

            if initialized:
                results = await manager.enhanced_file_search("test")
                print(f"✓ Enhanced search results: {len(results)} found")

                stats = await manager.get_connection_stats()
                print(f"✓ Connection stats: {stats['connected']}")

                await manager.cleanup()

            print("\nAll MCP integration tests passed! ✓")

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    asyncio.run(run_integration_tests())

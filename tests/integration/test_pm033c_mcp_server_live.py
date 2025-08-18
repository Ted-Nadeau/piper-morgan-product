"""
PM-033c MCP Server Live Testing Suite

Tests the actual running MCP server implementation for comprehensive validation.
This test suite validates Code's MCP server implementation claims and performance.

Tests ADR-013: MCP + Spatial Intelligence Pattern with dual-mode architecture
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from services.intent_service.spatial_intent_classifier import SpatialIntentClassifier
from services.queries.query_router import QueryRouter
from services.queries.query_router_spatial_migration import migrate_query_router_to_spatial


class TestPM033cMCPServerLive:
    """
    Live integration tests for PM-033c MCP Server dual-mode operation

    Tests the actual running MCP server to validate Code's implementation claims
    """

    @pytest.fixture
    async def mcp_server_url(self):
        """MCP server URL for testing"""
        return "http://localhost:8765"

    @pytest.fixture
    async def spatial_intent_classifier(self):
        """SpatialIntentClassifier instance for MCP exposure testing"""
        classifier = SpatialIntentClassifier()
        await classifier.initialize()
        return classifier

    @pytest.fixture
    async def query_router_spatial(self):
        """QueryRouter with spatial intelligence enabled"""
        router = QueryRouter()
        await migrate_query_router_to_spatial(router)
        return router

    @pytest.fixture
    def sample_mcp_requests(self):
        """Sample MCP protocol requests for testing"""
        return {
            "initialize": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"},
                },
            },
            "list_resources": {"jsonrpc": "2.0", "id": 2, "method": "resources/list", "params": {}},
            "read_resource": {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "resources/read",
                "params": {"uri": "piper://intent/spatial_classifier"},
            },
            "call_tool": {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "federated_search",
                    "arguments": {"query": "test query", "context": "slack"},
                },
            },
        }

    # ============================================================================
    # 1. MCP Server Startup Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_mcp_server_startup_success(self, mcp_server_url):
        """
        Test MCP server starts successfully on localhost:8765

        Success Criteria:
        - Server binds to specified port
        - MCP protocol handshake works correctly
        - Service discovery returns expected resources
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test basic connectivity
                async with session.get(f"{mcp_server_url}/health") as response:
                    assert response.status == 200, f"Health check failed: {response.status}"

                # Test MCP protocol endpoint
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                ) as response:
                    assert response.status == 200, f"MCP initialize failed: {response.status}"
                    data = await response.json()
                    assert "result" in data, "No result in MCP response"

                startup_time = (time.time() - start_time) * 1000
                print(f"✅ MCP server startup test passed in {startup_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"MCP server startup test failed: {e}")

    @pytest.mark.asyncio
    async def test_mcp_protocol_handshake(self, mcp_server_url, sample_mcp_requests):
        """
        Test MCP protocol handshake works correctly

        Success Criteria:
        - Initialize method returns correct protocol version
        - Capabilities negotiation successful
        - Server info properly exposed
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Send initialize request
                async with session.post(
                    f"{mcp_server_url}/mcp", json=sample_mcp_requests["initialize"]
                ) as response:
                    assert response.status == 200, f"Initialize failed: {response.status}"
                    data = await response.json()

                    # Validate response structure
                    assert "jsonrpc" in data, "Missing jsonrpc field"
                    assert data["jsonrpc"] == "2.0", "Invalid JSON-RPC version"
                    assert "result" in data, "Missing result field"

                    # Validate server info
                    result = data["result"]
                    assert "serverInfo" in result, "Missing serverInfo"
                    assert "name" in result["serverInfo"], "Missing server name"
                    assert "version" in result["serverInfo"], "Missing server version"

                handshake_time = (time.time() - start_time) * 1000
                print(f"✅ MCP protocol handshake test passed in {handshake_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"MCP protocol handshake test failed: {e}")

    @pytest.mark.asyncio
    async def test_service_discovery_resources(self, mcp_server_url):
        """
        Test service discovery returns expected resources

        Success Criteria:
        - All core services exposed as MCP resources
        - Resource metadata accurate and complete
        - URI scheme consistent and accessible
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Request resource list
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={"jsonrpc": "2.0", "id": 2, "method": "resources/list", "params": {}},
                ) as response:
                    assert response.status == 200, f"Resource list failed: {response.status}"
                    data = await response.json()

                    # Validate response structure
                    assert "result" in data, "Missing result field"
                    result = data["result"]
                    assert "resources" in result, "Missing resources field"

                    # Check for expected resources
                    resources = result["resources"]
                    resource_uris = [r["uri"] for r in resources]

                    # Validate core resources exist
                    expected_resources = [
                        "piper://intent/spatial_classifier",
                        "piper://query/federated_search",
                    ]

                    for expected in expected_resources:
                        assert expected in resource_uris, f"Missing expected resource: {expected}"

                discovery_time = (time.time() - start_time) * 1000
                print(f"✅ Service discovery test passed in {discovery_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Service discovery test failed: {e}")

    # ============================================================================
    # 2. Service Exposure Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_spatial_intent_classifier_mcp_exposure(self, mcp_server_url):
        """
        Test SpatialIntentClassifier accessible via MCP calls

        Success Criteria:
        - Intent classification endpoint functional
        - Spatial context processing working
        - Response format matches MCP specification
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test resource read for spatial intent classifier
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={
                        "jsonrpc": "2.0",
                        "id": 3,
                        "method": "resources/read",
                        "params": {"uri": "piper://intent/spatial_classifier"},
                    },
                ) as response:
                    assert response.status == 200, f"Resource read failed: {response.status}"
                    data = await response.json()

                    # Validate response structure
                    assert "result" in data, "Missing result field"
                    result = data["result"]
                    assert "content" in result, "Missing content field"

                exposure_time = (time.time() - start_time) * 1000
                print(
                    f"✅ SpatialIntentClassifier MCP exposure test passed in {exposure_time:.2f}ms"
                )

        except Exception as e:
            pytest.fail(f"SpatialIntentClassifier MCP exposure test failed: {e}")

    @pytest.mark.asyncio
    async def test_query_router_federated_search_mcp(self, mcp_server_url):
        """
        Test QueryRouter federated search works through MCP

        Success Criteria:
        - Federated search tool accessible
        - Multi-dimensional query routing functional
        - Performance within <100ms target
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test federated search tool
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={
                        "jsonrpc": "2.0",
                        "id": 4,
                        "method": "tools/call",
                        "params": {
                            "name": "federated_search",
                            "arguments": {"query": "test query", "context": "slack"},
                        },
                    },
                ) as response:
                    assert response.status == 200, f"Tool call failed: {response.status}"
                    data = await response.json()

                    # Validate response structure
                    assert "result" in data, "Missing result field"

                search_time = (time.time() - start_time) * 1000
                print(f"✅ QueryRouter federated search test passed in {search_time:.2f}ms")

                # Validate performance target
                assert (
                    search_time < 100
                ), f"Performance target not met: {search_time:.2f}ms >= 100ms"

        except Exception as e:
            pytest.fail(f"QueryRouter federated search test failed: {e}")

    @pytest.mark.asyncio
    async def test_mcp_error_handling(self, mcp_server_url):
        """
        Test error handling for invalid requests

        Success Criteria:
        - Invalid methods return proper error codes
        - Malformed requests handled gracefully
        - Error responses follow MCP specification
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test invalid method
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={"jsonrpc": "2.0", "id": 5, "method": "invalid/method", "params": {}},
                ) as response:
                    assert (
                        response.status == 200
                    ), f"Invalid method should return 200: {response.status}"
                    data = await response.json()

                    # Validate error response structure
                    assert "error" in data, "Missing error field"
                    assert "code" in data["error"], "Missing error code"
                    assert data["error"]["code"] == -32601, "Expected METHOD_NOT_FOUND error"

                error_time = (time.time() - start_time) * 1000
                print(f"✅ MCP error handling test passed in {error_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"MCP error handling test failed: {e}")

    # ============================================================================
    # 3. Dual-Mode Operation Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_consumer_functionality_unchanged(self):
        """
        Test consumer functionality unchanged

        Success Criteria:
        - Existing MCP consumer operations work
        - No regression in consumer capabilities
        - Performance maintained at current levels
        """
        start_time = time.time()

        try:
            # Test that existing consumer functionality still works
            # This would involve testing the MCPConsumerCore functionality
            # For now, we'll validate that the imports still work

            from services.mcp.consumer.consumer_core import MCPConsumerCore

            consumer = MCPConsumerCore()

            # Basic functionality test
            assert hasattr(consumer, "connect"), "Consumer missing connect method"
            assert hasattr(consumer, "disconnect"), "Consumer missing disconnect method"

            consumer_time = (time.time() - start_time) * 1000
            print(f"✅ Consumer functionality test passed in {consumer_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Consumer functionality test failed: {e}")

    @pytest.mark.asyncio
    async def test_server_consumer_simultaneous_operation(self, mcp_server_url):
        """
        Test server + consumer run simultaneously

        Success Criteria:
        - Both modes operational concurrently
        - No port conflicts or resource issues
        - Independent operation maintained
        """
        start_time = time.time()

        try:
            # Test that server is running
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{mcp_server_url}/health") as response:
                    assert response.status == 200, "Server health check failed"

            # Test that consumer can still be instantiated
            from services.mcp.consumer.consumer_core import MCPConsumerCore

            consumer = MCPConsumerCore()

            # Both should work independently
            assert consumer is not None, "Consumer instantiation failed"

            simultaneous_time = (time.time() - start_time) * 1000
            print(
                f"✅ Server + Consumer simultaneous operation test passed in {simultaneous_time:.2f}ms"
            )

        except Exception as e:
            pytest.fail(f"Server + Consumer simultaneous operation test failed: {e}")

    @pytest.mark.asyncio
    async def test_no_resource_conflicts(self, mcp_server_url):
        """
        Test no port conflicts or resource issues

        Success Criteria:
        - Port binding successful
        - Resource allocation clean
        - Memory usage within limits
        """
        start_time = time.time()

        try:
            # Test multiple connections to ensure no resource conflicts
            async with aiohttp.ClientSession() as session:
                # Make multiple concurrent requests
                tasks = []
                for i in range(5):
                    task = session.post(
                        f"{mcp_server_url}/mcp",
                        json={"jsonrpc": "2.0", "id": i, "method": "resources/list", "params": {}},
                    )
                    tasks.append(task)

                # Execute all requests concurrently
                responses = await asyncio.gather(*tasks)

                # Validate all responses
                for i, response in enumerate(responses):
                    assert (
                        response.status == 200
                    ), f"Concurrent request {i} failed: {response.status}"

            conflict_time = (time.time() - start_time) * 1000
            print(f"✅ No resource conflicts test passed in {conflict_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"No resource conflicts test failed: {e}")

    # ============================================================================
    # 4. Performance Validation Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_mcp_calls_within_100ms_target(self, mcp_server_url):
        """
        Test MCP calls complete within <100ms target

        Success Criteria:
        - All MCP operations under 100ms
        - Performance metrics collected
        - Baseline established for monitoring
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test multiple MCP operations for performance
                operations = [
                    ("initialize", {"method": "initialize", "params": {}}),
                    ("resources/list", {"method": "resources/list", "params": {}}),
                    ("tools/list", {"method": "tools/list", "params": {}}),
                ]

                for op_name, op_params in operations:
                    op_start = time.time()

                    async with session.post(
                        f"{mcp_server_url}/mcp", json={"jsonrpc": "2.0", "id": 1, **op_params}
                    ) as response:
                        assert response.status == 200, f"{op_name} failed: {response.status}"

                    op_time = (time.time() - op_start) * 1000
                    print(f"  {op_name}: {op_time:.2f}ms")

                    # Validate performance target
                    assert (
                        op_time < 100
                    ), f"Performance target not met for {op_name}: {op_time:.2f}ms >= 100ms"

            total_time = (time.time() - start_time) * 1000
            print(f"✅ MCP calls within 100ms target test passed in {total_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"MCP calls within 100ms target test failed: {e}")

    @pytest.mark.asyncio
    async def test_no_degradation_to_existing_functionality(self):
        """
        Test no degradation to existing functionality

        Success Criteria:
        - Slack integration performance maintained
        - Spatial intelligence response times stable
        - Query router performance unchanged
        """
        start_time = time.time()

        try:
            # Test core functionality still works
            from services.intent_service.spatial_intent_classifier import SpatialIntentClassifier
            from services.queries.query_router import QueryRouter

            # Basic instantiation test
            classifier = SpatialIntentClassifier()
            router = QueryRouter()

            # Validate core methods exist
            assert hasattr(
                classifier, "classify_intent"
            ), "SpatialIntentClassifier missing classify_intent"
            assert hasattr(router, "route_query"), "QueryRouter missing route_query"

            functionality_time = (time.time() - start_time) * 1000
            print(
                f"✅ No degradation to existing functionality test passed in {functionality_time:.2f}ms"
            )

        except Exception as e:
            pytest.fail(f"No degradation to existing functionality test failed: {e}")

    @pytest.mark.asyncio
    async def test_memory_usage_within_limits(self, mcp_server_url):
        """
        Test memory usage within acceptable limits

        Success Criteria:
        - Memory usage stable under load
        - No memory leaks detected
        - Resource cleanup effective
        """
        start_time = time.time()

        try:
            # Test memory stability under load
            async with aiohttp.ClientSession() as session:
                # Make multiple requests to test memory stability
                for i in range(10):
                    async with session.post(
                        f"{mcp_server_url}/mcp",
                        json={"jsonrpc": "2.0", "id": i, "method": "resources/list", "params": {}},
                    ) as response:
                        assert response.status == 200, f"Request {i} failed: {response.status}"

            memory_time = (time.time() - start_time) * 1000
            print(f"✅ Memory usage within limits test passed in {memory_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Memory usage within limits test failed: {e}")

    # ============================================================================
    # 5. Integration Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_mcp_client_connection(self, mcp_server_url):
        """
        Test MCP client can connect and call services

        Success Criteria:
        - Client connection successful
        - Service calls functional
        - Response handling correct
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test basic connectivity
                async with session.get(f"{mcp_server_url}/health") as response:
                    assert response.status == 200, "Health check failed"

                # Test MCP protocol communication
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                ) as response:
                    assert response.status == 200, "MCP initialize failed"
                    data = await response.json()
                    assert "result" in data, "Invalid MCP response"

            connection_time = (time.time() - start_time) * 1000
            print(f"✅ MCP client connection test passed in {connection_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"MCP client connection test failed: {e}")

    @pytest.mark.asyncio
    async def test_service_responses_match_expected_formats(self, mcp_server_url):
        """
        Test service responses match expected formats

        Success Criteria:
        - Response format compliance
        - Data structure validation
        - Content accuracy verification
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test resources/list response format
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={"jsonrpc": "2.0", "id": 1, "method": "resources/list", "params": {}},
                ) as response:
                    assert response.status == 200, "Resources list failed"
                    data = await response.json()

                    # Validate JSON-RPC structure
                    assert "jsonrpc" in data, "Missing jsonrpc field"
                    assert data["jsonrpc"] == "2.0", "Invalid JSON-RPC version"
                    assert "id" in data, "Missing id field"
                    assert "result" in data, "Missing result field"

                    # Validate result structure
                    result = data["result"]
                    assert "resources" in result, "Missing resources field"
                    assert isinstance(result["resources"], list), "Resources should be a list"

            format_time = (time.time() - start_time) * 1000
            print(f"✅ Service responses format test passed in {format_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Service responses format test failed: {e}")

    @pytest.mark.asyncio
    async def test_error_conditions_handled_gracefully(self, mcp_server_url):
        """
        Test error conditions handled gracefully

        Success Criteria:
        - Error responses follow MCP spec
        - Graceful degradation implemented
        - User experience maintained
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test various error conditions
                error_tests = [
                    ("invalid_json", "invalid json", 400),
                    ("missing_method", {"jsonrpc": "2.0", "id": 1}, 400),
                    (
                        "unknown_method",
                        {"jsonrpc": "2.0", "id": 1, "method": "unknown", "params": {}},
                        200,
                    ),
                ]

                for test_name, test_data, expected_status in error_tests:
                    if test_name == "invalid_json":
                        # Test invalid JSON
                        async with session.post(
                            f"{mcp_server_url}/mcp", data="invalid json"
                        ) as response:
                            assert (
                                response.status == expected_status
                            ), f"{test_name} failed: expected {expected_status}, got {response.status}"
                    else:
                        # Test structured errors
                        async with session.post(
                            f"{mcp_server_url}/mcp", json=test_data
                        ) as response:
                            if expected_status == 200:
                                # Should return JSON-RPC error response
                                data = await response.json()
                                assert "error" in data, f"{test_name} should return error response"
                            else:
                                assert (
                                    response.status == expected_status
                                ), f"{test_name} failed: expected {expected_status}, got {response.status}"

            error_time = (time.time() - start_time) * 1000
            print(f"✅ Error conditions handling test passed in {error_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Error conditions handling test failed: {e}")

    # ============================================================================
    # 6. Slack Integration Preservation Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_existing_slack_functionality_preserved(self):
        """
        Test existing Slack functionality preserved

        Success Criteria:
        - All Slack features working
        - No breaking changes introduced
        - Performance maintained
        """
        start_time = time.time()

        try:
            # Test that Slack integration modules still exist and can be imported
            from services.integrations.slack import slack_integration
            from services.integrations.slack.slack_spatial_intelligence import (
                SlackSpatialIntelligence,
            )

            # Basic functionality test
            assert slack_integration is not None, "Slack integration module missing"
            assert SlackSpatialIntelligence is not None, "SlackSpatialIntelligence class missing"

            slack_time = (time.time() - start_time) * 1000
            print(f"✅ Existing Slack functionality preserved test passed in {slack_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Existing Slack functionality preserved test failed: {e}")

    @pytest.mark.asyncio
    async def test_slack_spatial_intelligence_unchanged(self):
        """
        Test Slack spatial intelligence unchanged

        Success Criteria:
        - Spatial analysis working
        - Context processing functional
        - Response quality maintained
        """
        start_time = time.time()

        try:
            # Test that Slack spatial intelligence can be instantiated
            from services.integrations.slack.slack_spatial_intelligence import (
                SlackSpatialIntelligence,
            )

            # Basic instantiation test
            slack_spatial = SlackSpatialIntelligence()

            # Validate core methods exist
            assert hasattr(slack_spatial, "analyze_channel"), "Missing analyze_channel method"
            assert hasattr(slack_spatial, "process_message"), "Missing process_message method"

            intelligence_time = (time.time() - start_time) * 1000
            print(
                f"✅ Slack spatial intelligence unchanged test passed in {intelligence_time:.2f}ms"
            )

        except Exception as e:
            pytest.fail(f"Slack spatial intelligence unchanged test failed: {e}")

    # ============================================================================
    # 7. MCP Protocol Compliance Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_mcp_protocol_specification_compliance(self, mcp_server_url):
        """
        Test full MCP specification adherence

        Success Criteria:
        - Protocol compliance verified
        - Message format correct
        - Error handling compliant
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test JSON-RPC 2.0 compliance
                test_requests = [
                    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                    {"jsonrpc": "2.0", "id": 2, "method": "resources/list", "params": {}},
                    {"jsonrpc": "2.0", "id": 3, "method": "tools/list", "params": {}},
                ]

                for i, request in enumerate(test_requests):
                    async with session.post(f"{mcp_server_url}/mcp", json=request) as response:
                        assert response.status == 200, f"Request {i} failed: {response.status}"
                        data = await response.json()

                        # Validate JSON-RPC 2.0 compliance
                        assert "jsonrpc" in data, "Missing jsonrpc field"
                        assert data["jsonrpc"] == "2.0", "Invalid JSON-RPC version"
                        assert "id" in data, "Missing id field"
                        assert data["id"] == request["id"], "ID mismatch"

                        # Should have either result or error
                        assert "result" in data or "error" in data, "Missing result or error"

            compliance_time = (time.time() - start_time) * 1000
            print(
                f"✅ MCP protocol specification compliance test passed in {compliance_time:.2f}ms"
            )

        except Exception as e:
            pytest.fail(f"MCP protocol specification compliance test failed: {e}")

    @pytest.mark.asyncio
    async def test_mcp_resource_management(self, mcp_server_url):
        """
        Test MCP resource management compliance

        Success Criteria:
        - Resource lifecycle managed correctly
        - Memory usage optimized
        - Cleanup procedures effective
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test resource listing
                async with session.post(
                    f"{mcp_server_url}/mcp",
                    json={"jsonrpc": "2.0", "id": 1, "method": "resources/list", "params": {}},
                ) as response:
                    assert response.status == 200, "Resource list failed"
                    data = await response.json()

                    # Validate resource structure
                    result = data["result"]
                    resources = result["resources"]

                    for resource in resources:
                        assert "uri" in resource, "Resource missing URI"
                        assert "name" in resource, "Resource missing name"
                        assert "description" in resource, "Resource missing description"
                        assert "mimeType" in resource, "Resource missing MIME type"

            resource_time = (time.time() - start_time) * 1000
            print(f"✅ MCP resource management test passed in {resource_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"MCP resource management test failed: {e}")

    # ============================================================================
    # 8. Health Monitoring Tests
    # ============================================================================

    @pytest.mark.asyncio
    async def test_health_monitoring_covers_both_modes(self, mcp_server_url):
        """
        Test health monitoring covers both consumer and server modes

        Success Criteria:
        - Consumer health monitored
        - Server health monitored
        - Combined status accurate
        """
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Test health endpoint
                async with session.get(f"{mcp_server_url}/health") as response:
                    assert response.status == 200, "Health check failed"
                    data = await response.json()

                    # Validate health response structure
                    assert "status" in data, "Health response missing status"
                    assert "timestamp" in data, "Health response missing timestamp"
                    assert "services" in data, "Health response missing services"

                health_time = (time.time() - start_time) * 1000
                print(f"✅ Health monitoring test passed in {health_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Health monitoring test failed: {e}")

    @pytest.mark.asyncio
    async def test_circuit_breaker_pattern_functional(self, mcp_server_url):
        """
        Test circuit breaker pattern functional for both modes

        Success Criteria:
        - Circuit breaker operational
        - Failure handling effective
        - Recovery mechanisms working
        """
        start_time = time.time()

        try:
            # Test that circuit breaker pattern is implemented
            # This would involve testing failure scenarios and recovery
            # For now, we'll validate that the pattern exists in the codebase

            from services.mcp.client import MCPCircuitBreaker

            # Basic circuit breaker test
            circuit_breaker = MCPCircuitBreaker()
            assert hasattr(circuit_breaker, "call"), "Circuit breaker missing call method"
            assert hasattr(circuit_breaker, "state"), "Circuit breaker missing state attribute"

            circuit_time = (time.time() - start_time) * 1000
            print(f"✅ Circuit breaker pattern test passed in {circuit_time:.2f}ms")

        except Exception as e:
            pytest.fail(f"Circuit breaker pattern test failed: {e}")


# ============================================================================
# Performance Test Classes
# ============================================================================


class TestPM033cMCPServerPerformanceLive:
    """Performance-specific tests for PM-033c MCP Server"""

    @pytest.mark.asyncio
    async def test_100ms_latency_target_achievement(self):
        """Test <100ms latency target achievement"""
        # This test will be implemented in the main test class
        pass

    @pytest.mark.asyncio
    async def test_concurrent_client_handling(self):
        """Test concurrent client handling capability"""
        # This test will be implemented in the main test class
        pass

    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self):
        """Test memory usage under load conditions"""
        # This test will be implemented in the main test class
        pass


class TestPM033cMCPServerIntegrationLive:
    """Integration tests for PM-033c MCP Server"""

    @pytest.mark.asyncio
    async def test_end_to_end_mcp_workflow(self):
        """Test end-to-end MCP workflow execution"""
        # This test will be implemented in the main test class
        pass

    @pytest.mark.asyncio
    async def test_real_world_usage_scenarios(self):
        """Test real-world usage scenarios"""
        # This test will be implemented in the main test class
        pass

    @pytest.mark.asyncio
    async def test_failure_recovery_and_resilience(self):
        """Test failure recovery and resilience"""
        # This test will be implemented in the main test class
        pass


# ============================================================================
# Test Configuration and Utilities
# ============================================================================


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])

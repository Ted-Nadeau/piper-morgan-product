"""
PM-033c MCP Server Test Configuration

Provides comprehensive test configuration, mock objects, and test data
for PM-033c MCP Server testing suite.
"""

import json
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

# ============================================================================
# MCP Server Configuration
# ============================================================================

MCP_SERVER_CONFIG = {
    "host": "localhost",
    "port": 8765,
    "protocol": "http",
    "timeout": 5.0,
    "max_connections": 10,
    "enable_ssl": False,
    "log_level": "INFO",
}

MCP_CLIENT_CONFIG = {
    "server_url": "http://localhost:8765",
    "timeout": 5.0,
    "retry_attempts": 3,
    "connection_pool_size": 5,
}

# ============================================================================
# MCP Protocol Constants
# ============================================================================

MCP_PROTOCOL_VERSION = "2024-11-05"
MCP_SERVER_NAME = "piper-morgan-mcp-server"
MCP_SERVER_VERSION = "1.0.0"

MCP_METHODS = {
    "initialize": "initialize",
    "list_resources": "resources/list",
    "read_resource": "resources/read",
    "call_tool": "tools/call",
    "list_tools": "tools/list",
}

MCP_ERROR_CODES = {
    "METHOD_NOT_FOUND": -32601,
    "INVALID_PARAMS": -32602,
    "INTERNAL_ERROR": -32603,
    "PARSE_ERROR": -32700,
    "INVALID_REQUEST": -32600,
}

# ============================================================================
# Test Data and Mock Objects
# ============================================================================


def create_mock_mcp_server() -> MagicMock:
    """Create a mock MCP server for testing"""
    server = MagicMock()
    server.host = MCP_SERVER_CONFIG["host"]
    server.port = MCP_SERVER_CONFIG["port"]
    server.is_running = False
    server.start = AsyncMock()
    server.stop = AsyncMock()
    server.get_status = MagicMock(return_value="stopped")
    return server


def create_mock_mcp_client() -> MagicMock:
    """Create a mock MCP client for testing"""
    client = MagicMock()
    client.server_url = MCP_CLIENT_CONFIG["server_url"]
    client.timeout = MCP_CLIENT_CONFIG["timeout"]
    client.connected = False
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    client.send_request = AsyncMock()
    client.receive_response = AsyncMock()
    return client


def create_mock_spatial_intent_classifier() -> MagicMock:
    """Create a mock SpatialIntentClassifier for testing"""
    classifier = MagicMock()
    classifier.initialized = False
    classifier.initialize = AsyncMock()
    classifier.classify_intent = AsyncMock()
    classifier.get_spatial_context = AsyncMock()
    classifier.update_context = AsyncMock()
    return classifier


def create_mock_query_router() -> MagicMock:
    """Create a mock QueryRouter for testing"""
    router = MagicMock()
    router.enable_mcp_federation = True
    router.federated_search = AsyncMock()
    router.route_query = AsyncMock()
    router.get_search_results = AsyncMock()
    return router


# ============================================================================
# Sample MCP Requests and Responses
# ============================================================================

SAMPLE_MCP_REQUESTS = {
    "initialize": {
        "jsonrpc": "2.0",
        "id": 1,
        "method": MCP_METHODS["initialize"],
        "params": {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    },
    "list_resources": {
        "jsonrpc": "2.0",
        "id": 2,
        "method": MCP_METHODS["list_resources"],
        "params": {},
    },
    "read_resource": {
        "jsonrpc": "2.0",
        "id": 3,
        "method": MCP_METHODS["read_resource"],
        "params": {"uri": "intent/spatial_classifier"},
    },
    "call_tool": {
        "jsonrpc": "2.0",
        "id": 4,
        "method": MCP_METHODS["call_tool"],
        "params": {
            "name": "query/federated_search",
            "arguments": {"query": "test query", "context": "slack"},
        },
    },
    "list_tools": {"jsonrpc": "2.0", "id": 5, "method": MCP_METHODS["list_tools"], "params": {}},
}

EXPECTED_MCP_RESPONSES = {
    "initialize": {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {
                "resources": {"subscribe": False, "listChanged": False},
                "tools": {"subscribe": False},
            },
            "serverInfo": {"name": MCP_SERVER_NAME, "version": MCP_SERVER_VERSION},
        },
    },
    "list_resources": {
        "jsonrpc": "2.0",
        "id": 2,
        "result": {
            "resources": [
                {
                    "uri": "intent/spatial_classifier",
                    "name": "Spatial Intent Classifier",
                    "description": "Spatial context-aware intent classification",
                    "mimeType": "application/json",
                },
                {
                    "uri": "query/federated_search",
                    "name": "Federated Search Tool",
                    "description": "Multi-dimensional query routing and federated search",
                    "mimeType": "application/json",
                },
                {
                    "uri": "slack/spatial_intelligence",
                    "name": "Slack Spatial Intelligence",
                    "description": "8-dimensional Slack workspace analysis",
                    "mimeType": "application/json",
                },
            ]
        },
    },
    "list_tools": {
        "jsonrpc": "2.0",
        "id": 5,
        "result": {
            "tools": [
                {
                    "name": "query/federated_search",
                    "description": "Multi-dimensional query routing and federated search",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "context": {"type": "string"},
                            "dimensions": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "intent/classify",
                    "description": "Natural language intent classification",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"text": {"type": "string"}, "context": {"type": "object"}},
                        "required": ["text"],
                    },
                },
            ]
        },
    },
}

# ============================================================================
# Test Scenarios and Use Cases
# ============================================================================

TEST_SCENARIOS = {
    "basic_server_operation": {
        "description": "Basic MCP server startup and operation",
        "steps": [
            "Server starts successfully",
            "Protocol handshake completes",
            "Resource discovery works",
            "Basic health check passes",
        ],
        "expected_result": "Server operational and responding",
    },
    "dual_mode_operation": {
        "description": "Consumer and server modes working simultaneously",
        "steps": [
            "Consumer mode operational",
            "Server mode operational",
            "No resource conflicts",
            "Independent operation maintained",
        ],
        "expected_result": "Both modes functional without interference",
    },
    "service_exposure": {
        "description": "Core services exposed via MCP protocol",
        "steps": [
            "SpatialIntentClassifier accessible",
            "QueryRouter federated search works",
            "Service responses correct",
            "Error handling functional",
        ],
        "expected_result": "All services accessible via MCP",
    },
    "performance_validation": {
        "description": "Performance targets met for MCP operations",
        "steps": [
            "Latency under 100ms",
            "Throughput acceptable",
            "Memory usage stable",
            "Resource utilization optimal",
        ],
        "expected_result": "Performance targets achieved",
    },
}

# ============================================================================
# Performance Test Configuration
# ============================================================================

PERFORMANCE_TEST_CONFIG = {
    "latency_targets": {
        "server_startup": 500,  # ms
        "protocol_handshake": 100,  # ms
        "resource_discovery": 50,  # ms
        "service_calls": 100,  # ms
        "tool_execution": 150,  # ms
    },
    "load_test_config": {
        "concurrent_clients": [1, 5, 10, 20],
        "requests_per_client": 100,
        "test_duration": 60,  # seconds
        "ramp_up_time": 10,  # seconds
    },
    "memory_limits": {
        "max_memory_usage": "512MB",
        "memory_leak_threshold": "10MB/hour",
        "gc_frequency": "every 1000 requests",
    },
}

# ============================================================================
# Error Scenarios and Edge Cases
# ============================================================================

ERROR_SCENARIOS = {
    "invalid_requests": [
        {
            "description": "Invalid JSON-RPC format",
            "request": {"invalid": "json"},
            "expected_error": MCP_ERROR_CODES["PARSE_ERROR"],
        },
        {
            "description": "Missing required fields",
            "request": {"jsonrpc": "2.0", "id": 1},
            "expected_error": MCP_ERROR_CODES["INVALID_REQUEST"],
        },
        {
            "description": "Unknown method",
            "request": {"jsonrpc": "2.0", "id": 1, "method": "unknown/method", "params": {}},
            "expected_error": MCP_ERROR_CODES["METHOD_NOT_FOUND"],
        },
    ],
    "resource_scenarios": [
        {
            "description": "Non-existent resource",
            "uri": "nonexistent/resource",
            "expected_error": MCP_ERROR_CODES["INVALID_PARAMS"],
        },
        {
            "description": "Invalid URI format",
            "uri": "invalid:uri:format",
            "expected_error": MCP_ERROR_CODES["INVALID_PARAMS"],
        },
    ],
    "performance_scenarios": [
        {
            "description": "High load handling",
            "concurrent_requests": 100,
            "expected_behavior": "Graceful degradation",
        },
        {
            "description": "Memory pressure",
            "memory_usage": "90%",
            "expected_behavior": "Resource cleanup",
        },
    ],
}

# ============================================================================
# Test Utilities and Helpers
# ============================================================================


def create_test_environment() -> Dict[str, Any]:
    """Create a complete test environment configuration"""
    return {
        "mcp_server": create_mock_mcp_server(),
        "mcp_client": create_mock_mcp_client(),
        "spatial_intent_classifier": create_mock_spatial_intent_classifier(),
        "query_router": create_mock_query_router(),
        "config": MCP_SERVER_CONFIG.copy(),
        "test_data": {
            "requests": SAMPLE_MCP_REQUESTS.copy(),
            "responses": EXPECTED_MCP_RESPONSES.copy(),
            "scenarios": TEST_SCENARIOS.copy(),
        },
    }


def validate_mcp_message(message: Dict[str, Any]) -> bool:
    """Validate MCP message format"""
    required_fields = ["jsonrpc", "id"]

    # Check required fields
    for field in required_fields:
        if field not in message:
            return False

    # Validate JSON-RPC version
    if message["jsonrpc"] != "2.0":
        return False

    # Validate ID (should be number or string)
    if not isinstance(message["id"], (int, str)):
        return False

    return True


def create_error_response(request_id: Any, error_code: int, error_message: str) -> Dict[str, Any]:
    """Create a standard MCP error response"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": error_code, "message": error_message},
    }


def create_success_response(request_id: Any, result: Any) -> Dict[str, Any]:
    """Create a standard MCP success response"""
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


# ============================================================================
# Configuration Export
# ============================================================================

__all__ = [
    "MCP_SERVER_CONFIG",
    "MCP_CLIENT_CONFIG",
    "MCP_PROTOCOL_VERSION",
    "MCP_SERVER_NAME",
    "MCP_SERVER_VERSION",
    "MCP_METHODS",
    "MCP_ERROR_CODES",
    "SAMPLE_MCP_REQUESTS",
    "EXPECTED_MCP_RESPONSES",
    "TEST_SCENARIOS",
    "PERFORMANCE_TEST_CONFIG",
    "ERROR_SCENARIOS",
    "create_mock_mcp_server",
    "create_mock_mcp_client",
    "create_mock_spatial_intent_classifier",
    "create_mock_query_router",
    "create_test_environment",
    "validate_mcp_message",
    "create_error_response",
    "create_success_response",
]

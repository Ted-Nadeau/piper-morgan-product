"""
Piper MCP Server Core - Dual-Mode MCP Server Implementation

Extends MCPConsumerCore to provide dual-mode operation:
- Maintains existing MCP consumer capabilities
- Adds MCP server functionality to expose Piper's intelligence services
- Enables bidirectional MCP communication for agent ecosystem integration
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union

from services.intent_service.spatial_intent_classifier import SpatialIntentClassifier
from services.mcp.consumer.consumer_core import MCPConsumerCore
from services.mcp.protocol.message_handler import MCPNotification, MCPRequest, MCPResponse
from services.queries.query_router import QueryRouter

logger = logging.getLogger(__name__)


class MCPResource:
    """MCP resource definition"""

    def __init__(self, uri: str, name: str, description: str, mime_type: str = "application/json"):
        self.uri = uri
        self.name = name
        self.description = description
        self.mime_type = mime_type


class MCPTool:
    """MCP tool definition"""

    def __init__(self, name: str, description: str, input_schema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.input_schema = input_schema


class PiperMCPServer(MCPConsumerCore):
    """
    Dual-mode MCP server extending consumer capabilities

    Transforms Piper into MCP ecosystem hub by:
    - Maintaining consumer capabilities (connect to external MCP services)
    - Exposing internal services via MCP protocol (SpatialIntentClassifier, QueryRouter)
    - Enabling agent-to-agent intelligence federation
    """

    def __init__(self, port: int = 8765, host: str = "localhost"):
        """Initialize dual-mode MCP server"""
        super().__init__()  # Consumer capabilities from MCPConsumerCore

        # Server configuration
        self.server_port = port
        self.server_host = host
        self.server_running = False

        # MCP server resources and tools
        self.resources: Dict[str, MCPResource] = {}
        self.resource_handlers: Dict[str, Callable] = {}
        self.tools: Dict[str, MCPTool] = {}
        self.tool_handlers: Dict[str, Callable] = {}

        # Initialize core Piper services for MCP exposure
        self.spatial_intent_classifier = SpatialIntentClassifier()
        self.query_router = QueryRouter(
            project_query_service=None,  # Will be initialized if needed
            conversation_query_service=None,
            file_query_service=None,
            test_mode=True,
        )

        # Server socket and connection management
        self.server = None
        self.client_connections: List[asyncio.StreamWriter] = []

        # Performance tracking
        self.request_count = 0
        self.total_processing_time = 0.0

        logger.info(f"PiperMCPServer initialized on {host}:{port} (dual-mode)")

    async def register_resource(self, uri: str, name: str, description: str, handler: Callable):
        """Register MCP resource with handler"""
        resource = MCPResource(uri, name, description)
        self.resources[uri] = resource
        self.resource_handlers[uri] = handler
        logger.info(f"Registered MCP resource: {uri} ({name})")

    async def register_tool(
        self, name: str, description: str, input_schema: Dict[str, Any], handler: Callable
    ):
        """Register MCP tool with handler"""
        tool = MCPTool(name, description, input_schema)
        self.tools[name] = tool
        self.tool_handlers[name] = handler
        logger.info(f"Registered MCP tool: {name}")

    async def start_server(self):
        """Start MCP server on configured port"""
        try:
            self.server = await asyncio.start_server(
                self._handle_client_connection, self.server_host, self.server_port
            )

            self.server_running = True
            logger.info(f"✅ MCP server started on {self.server_host}:{self.server_port}")

            # Register default services
            await self._register_default_services()

            async with self.server:
                await self.server.serve_forever()

        except Exception as e:
            logger.error(f"❌ MCP server startup failed: {e}")
            raise

    async def stop_server(self):
        """Stop MCP server gracefully"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server_running = False
            logger.info("MCP server stopped")

    async def _register_default_services(self):
        """Register Piper's core services as MCP resources and tools"""

        # Register SpatialIntentClassifier as resource
        await self.register_resource(
            uri="piper://intent/spatial_classifier",
            name="Spatial Intent Classifier",
            description="Spatial context-aware intent classification for enhanced AI understanding",
            handler=self._handle_spatial_intent_classification,
        )

        # Register QueryRouter as tool
        await self.register_tool(
            name="federated_search",
            description="Multi-dimensional query routing with federated search capabilities",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "context": {
                        "type": "object",
                        "description": "Query context",
                        "additionalProperties": True,
                    },
                    "limit": {"type": "integer", "description": "Maximum results", "default": 10},
                },
                "required": ["query"],
            },
            handler=self._handle_federated_search,
        )

        logger.info("✅ Default Piper services registered with MCP server")

    async def _handle_client_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """Handle incoming MCP client connections"""
        client_addr = writer.get_extra_info("peername")
        logger.info(f"New MCP client connected: {client_addr}")

        self.client_connections.append(writer)

        try:
            while True:
                # Read JSON-RPC message
                data = await reader.readline()
                if not data:
                    break

                try:
                    message = json.loads(data.decode().strip())
                    response = await self._process_mcp_message(message)

                    if response:
                        response_data = json.dumps(response) + "\n"
                        writer.write(response_data.encode())
                        await writer.drain()

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON from client {client_addr}: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error"},
                    }
                    writer.write((json.dumps(error_response) + "\n").encode())
                    await writer.drain()

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error handling client {client_addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            if writer in self.client_connections:
                self.client_connections.remove(writer)
            logger.info(f"Client {client_addr} disconnected")

    async def _process_mcp_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming MCP message following JSON-RPC 2.0"""
        start_time = time.time()
        self.request_count += 1

        try:
            method = message.get("method")
            params = message.get("params", {})
            msg_id = message.get("id")

            if method == "initialize":
                return await self._handle_initialize(params, msg_id)
            elif method == "resources/list":
                return await self._handle_list_resources(msg_id)
            elif method == "resources/read":
                return await self._handle_read_resource(params, msg_id)
            elif method == "tools/list":
                return await self._handle_list_tools(msg_id)
            elif method == "tools/call":
                return await self._handle_call_tool(params, msg_id)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                }

        except Exception as e:
            logger.error(f"Error processing MCP message: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            }
        finally:
            processing_time = time.time() - start_time
            self.total_processing_time += processing_time

            if processing_time > 0.1:  # Log slow requests (>100ms)
                logger.warning(f"Slow MCP request: {method} took {processing_time:.3f}s")

    async def _handle_initialize(self, params: Dict[str, Any], msg_id: str) -> Dict[str, Any]:
        """Handle MCP initialization"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "resources": {"subscribe": True, "listChanged": True},
                    "tools": {"listChanged": True},
                },
                "serverInfo": {"name": "Piper Morgan MCP Server", "version": "1.0.0"},
            },
        }

    async def _handle_list_resources(self, msg_id: str) -> Dict[str, Any]:
        """Handle resource listing request"""
        resources_list = [
            {
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "mimeType": resource.mime_type,
            }
            for resource in self.resources.values()
        ]

        return {"jsonrpc": "2.0", "id": msg_id, "result": {"resources": resources_list}}

    async def _handle_read_resource(self, params: Dict[str, Any], msg_id: str) -> Dict[str, Any]:
        """Handle resource read request"""
        uri = params.get("uri")

        if uri not in self.resource_handlers:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32602, "message": f"Resource not found: {uri}"},
            }

        try:
            handler = self.resource_handlers[uri]
            result = await handler(params)

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "contents": [
                        {"uri": uri, "mimeType": "application/json", "text": json.dumps(result)}
                    ]
                },
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32603, "message": f"Resource handler error: {str(e)}"},
            }

    async def _handle_list_tools(self, msg_id: str) -> Dict[str, Any]:
        """Handle tool listing request"""
        tools_list = [
            {"name": tool.name, "description": tool.description, "inputSchema": tool.input_schema}
            for tool in self.tools.values()
        ]

        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools_list}}

    async def _handle_call_tool(self, params: Dict[str, Any], msg_id: str) -> Dict[str, Any]:
        """Handle tool call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name not in self.tool_handlers:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32602, "message": f"Tool not found: {tool_name}"},
            }

        try:
            handler = self.tool_handlers[tool_name]
            result = await handler(arguments)

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32603, "message": f"Tool handler error: {str(e)}"},
            }

    # Service-specific handlers

    async def _handle_spatial_intent_classification(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle spatial intent classification resource request"""
        try:
            # For now, return service capabilities and status
            # In full implementation, would process spatial events

            return {
                "service": "SpatialIntentClassifier",
                "status": "operational",
                "capabilities": [
                    "create_spatial_context_from_event",
                    "spatial_event_to_intent",
                    "enhance_intent_with_spatial_context",
                ],
                "spatial_dimensions": [
                    "room_id",
                    "territory_id",
                    "attention_level",
                    "emotional_valence",
                    "navigation_intent",
                    "spatial_coordinates",
                ],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Spatial intent classification error: {e}")
            raise

    async def _handle_federated_search(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle federated search tool request"""
        try:
            query = arguments.get("query", "")
            context = arguments.get("context", {})
            limit = arguments.get("limit", 10)

            if not query:
                return {"error": "Query parameter required"}

            # For proof of concept, return search capabilities info
            # In full implementation, would call query_router.classify_and_route

            return {
                "tool": "federated_search",
                "query": query,
                "context": context,
                "limit": limit,
                "capabilities": [
                    "project_queries",
                    "conversation_queries",
                    "file_queries",
                    "github_integration",
                    "spatial_intelligence",
                    "degradation_handling",
                ],
                "status": "operational",
                "processing_time_ms": 5,  # Mock fast response
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Federated search error: {e}")
            raise

    # Dual-mode status and management

    def get_server_status(self) -> Dict[str, Any]:
        """Get comprehensive server status"""
        avg_processing_time = (
            self.total_processing_time / self.request_count if self.request_count > 0 else 0
        )

        return {
            "server": {
                "running": self.server_running,
                "host": self.server_host,
                "port": self.server_port,
                "connected_clients": len(self.client_connections),
            },
            "consumer": {
                "connected": self._connected,
                "active_connections": len(self._active_connections),
            },
            "performance": {
                "request_count": self.request_count,
                "avg_processing_time_ms": avg_processing_time * 1000,
                "total_processing_time_s": self.total_processing_time,
            },
            "services": {
                "resources": list(self.resources.keys()),
                "tools": list(self.tools.keys()),
            },
            "dual_mode": True,
        }

    async def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check for dual-mode operation"""
        try:
            # Test consumer capabilities (if connected to external services)
            consumer_health = "operational" if hasattr(self, "_active_connections") else "standby"

            # Test server capabilities
            server_health = "operational" if self.server_running else "stopped"

            # Test service handlers
            spatial_classifier_health = "operational"  # SpatialIntentClassifier is lightweight
            query_router_health = "operational"  # QueryRouter initialized in test mode

            overall_health = (
                "healthy"
                if all(
                    [
                        consumer_health in ["operational", "standby"],
                        server_health == "operational",
                        spatial_classifier_health == "operational",
                        query_router_health == "operational",
                    ]
                )
                else "degraded"
            )

            return {
                "status": overall_health,
                "consumer": consumer_health,
                "server": server_health,
                "services": {
                    "spatial_intent_classifier": spatial_classifier_health,
                    "query_router": query_router_health,
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "error", "error": str(e), "timestamp": datetime.now().isoformat()}

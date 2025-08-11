"""
MCP Protocol Message Handling

This module provides Model Context Protocol (MCP) message handling capabilities,
extending the existing MCP client with JSON-RPC 2.0 protocol compliance.
"""

from .message_handler import MCPMessageHandler
from .protocol_client import MCPProtocolClient
from .service_discovery import MCPServiceDiscovery

__all__ = [
    "MCPMessageHandler",
    "MCPProtocolClient",
    "MCPServiceDiscovery",
]

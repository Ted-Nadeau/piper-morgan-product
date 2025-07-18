"""
MCP (Model Context Protocol) integration for Piper Morgan

This module provides MCP client functionality for enhanced file search capabilities.
Currently implements a compatibility layer for Python 3.9.6 (MCP SDK requires 3.10+).
"""

from .client import PiperMCPClient
from .exceptions import MCPCircuitBreakerOpenError, MCPConnectionError
from .resources import MCPResourceManager

__all__ = [
    "PiperMCPClient",
    "MCPConnectionError",
    "MCPCircuitBreakerOpenError",
    "MCPResourceManager",
]

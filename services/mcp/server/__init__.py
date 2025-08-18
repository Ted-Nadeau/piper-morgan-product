"""
MCP Server Module - Dual-mode MCP Server Implementation

Transforms Piper from MCP consumer to MCP ecosystem hub by exposing
internal services (SpatialIntentClassifier, QueryRouter) via MCP protocol.
"""

from .server_core import PiperMCPServer

__all__ = ["PiperMCPServer"]

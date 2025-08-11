"""
MCP Consumer Core

This module provides the core MCP Consumer functionality, integrating
protocol handling, service discovery, and spatial adapter patterns.
"""

from .consumer_core import MCPConsumerCore
from .github_adapter import GitHubMCPSpatialAdapter

__all__ = [
    "MCPConsumerCore",
    "GitHubMCPSpatialAdapter",
]

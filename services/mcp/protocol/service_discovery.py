"""
MCP Service Discovery - Service Discovery and Negotiation

Handles MCP service discovery protocol implementation, building on
existing connection pool infrastructure for service management.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

from ..exceptions import MCPConnectionError
from .protocol_client import MCPProtocolClient

logger = logging.getLogger(__name__)


@dataclass
class MCPServiceInfo:
    """Information about discovered MCP service"""

    name: str
    version: str
    description: Optional[str] = None
    capabilities: Dict[str, Any] = None
    transport: str = "stdio"  # stdio, http, sse
    endpoint: Optional[str] = None
    authentication: List[str] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = {}
        if self.authentication is None:
            self.authentication = []


class MCPServiceDiscovery:
    """
    MCP service discovery and negotiation

    Manages service discovery, capability negotiation, and service
    registration using existing connection pool infrastructure.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._discovered_services: Dict[str, MCPServiceInfo] = {}
        self._service_registry: Dict[str, MCPProtocolClient] = {}
        self._discovery_callbacks: List[callable] = []

    async def discover_services(self, discovery_config: Dict[str, Any]) -> List[MCPServiceInfo]:
        """Discover available MCP services"""
        try:
            services = []

            # Check for configured services
            if "services" in discovery_config:
                for service_config in discovery_config["services"]:
                    service_info = await self._discover_single_service(service_config)
                    if service_info:
                        services.append(service_info)
                        self._discovered_services[service_info.name] = service_info

            # Check for auto-discovery endpoints
            if "auto_discovery" in discovery_config:
                auto_services = await self._auto_discover_services(
                    discovery_config["auto_discovery"]
                )
                services.extend(auto_services)

            # Notify discovery callbacks
            for callback in self._discovery_callbacks:
                try:
                    await callback(services)
                except Exception as e:
                    self.logger.error(f"Error in discovery callback: {e}")

            return services

        except Exception as e:
            self.logger.error(f"Error during service discovery: {e}")
            return []

    async def _discover_single_service(
        self, service_config: Dict[str, Any]
    ) -> Optional[MCPServiceInfo]:
        """Discover a single MCP service"""
        try:
            service_name = service_config.get("name", "unknown")
            self.logger.info(f"Discovering MCP service: {service_name}")

            # Create protocol client for discovery
            client = MCPProtocolClient(service_config)

            # Try to initialize connection
            if await client.initialize_connection():
                # Get service capabilities
                capabilities = client.get_server_capabilities()

                # Create service info
                service_info = MCPServiceInfo(
                    name=service_name,
                    version=service_config.get("version", "1.0.0"),
                    description=service_config.get("description", ""),
                    capabilities=capabilities or {},
                    transport=service_config.get("transport", "stdio"),
                    endpoint=service_config.get("endpoint"),
                    authentication=service_config.get("authentication", []),
                )

                # Store in registry
                self._service_registry[service_name] = client

                self.logger.info(f"Successfully discovered MCP service: {service_name}")
                return service_info
            else:
                self.logger.warning(
                    f"Failed to initialize connection to MCP service: {service_name}"
                )
                return None

        except Exception as e:
            self.logger.error(
                f"Error discovering MCP service {service_config.get('name', 'unknown')}: {e}"
            )
            return None

    async def _auto_discover_services(self, auto_config: Dict[str, Any]) -> List[MCPServiceInfo]:
        """Auto-discover MCP services from endpoints"""
        try:
            services = []

            # Check for common MCP service locations
            common_paths = auto_config.get("paths", [])
            for path in common_paths:
                service_info = await self._check_path_for_service(path)
                if service_info:
                    services.append(service_info)

            # Check for network discovery
            network_endpoints = auto_config.get("network_endpoints", [])
            for endpoint in network_endpoints:
                service_info = await self._check_network_endpoint(endpoint)
                if service_info:
                    services.append(service_info)

            return services

        except Exception as e:
            self.logger.error(f"Error during auto-discovery: {e}")
            return []

    async def _check_path_for_service(self, path: str) -> Optional[MCPServiceInfo]:
        """Check if a path contains an MCP service"""
        try:
            # This would check for MCP service files or executables
            # For now, return None (placeholder for real implementation)
            self.logger.debug(f"Checking path for MCP service: {path}")
            return None

        except Exception as e:
            self.logger.error(f"Error checking path {path}: {e}")
            return None

    async def _check_network_endpoint(self, endpoint: str) -> Optional[MCPServiceInfo]:
        """Check if a network endpoint provides MCP service"""
        try:
            # This would check for MCP service over HTTP/SSE
            # For now, return None (placeholder for real implementation)
            self.logger.debug(f"Checking network endpoint for MCP service: {endpoint}")
            return None

        except Exception as e:
            self.logger.error(f"Error checking network endpoint {endpoint}: {e}")
            return None

    async def connect_to_service(self, service_name: str) -> Optional[MCPProtocolClient]:
        """Connect to a discovered MCP service"""
        try:
            if service_name not in self._discovered_services:
                self.logger.error(f"Service {service_name} not discovered")
                return None

            if service_name not in self._service_registry:
                self.logger.error(f"Service {service_name} not in registry")
                return None

            client = self._service_registry[service_name]

            # Check if already connected
            if client.is_initialized():
                self.logger.info(f"Already connected to MCP service: {service_name}")
                return client

            # Re-initialize connection
            if await client.initialize_connection():
                self.logger.info(f"Connected to MCP service: {service_name}")
                return client
            else:
                self.logger.error(f"Failed to connect to MCP service: {service_name}")
                return None

        except Exception as e:
            self.logger.error(f"Error connecting to MCP service {service_name}: {e}")
            return None

    async def disconnect_from_service(self, service_name: str) -> bool:
        """Disconnect from an MCP service"""
        try:
            if service_name in self._service_registry:
                client = self._service_registry[service_name]
                await client.disconnect_protocol()
                self.logger.info(f"Disconnected from MCP service: {service_name}")
                return True
            else:
                self.logger.warning(f"Service {service_name} not in registry")
                return False

        except Exception as e:
            self.logger.error(f"Error disconnecting from MCP service {service_name}: {e}")
            return False

    def get_service_info(self, service_name: str) -> Optional[MCPServiceInfo]:
        """Get information about a discovered service"""
        return self._discovered_services.get(service_name)

    def list_discovered_services(self) -> List[str]:
        """List names of discovered services"""
        return list(self._discovered_services.keys())

    def get_service_capabilities(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get capabilities of a discovered service"""
        service_info = self._discovered_services.get(service_name)
        if service_info:
            return service_info.capabilities
        return None

    def register_discovery_callback(self, callback: callable):
        """Register callback for service discovery events"""
        self._discovery_callbacks.append(callback)

    def unregister_discovery_callback(self, callback: callable):
        """Unregister discovery callback"""
        if callback in self._discovery_callbacks:
            self._discovery_callbacks.remove(callback)

    async def health_check_services(self) -> Dict[str, bool]:
        """Check health of all registered services"""
        try:
            health_status = {}

            for service_name, client in self._service_registry.items():
                try:
                    # Check if service is responsive
                    if client.is_initialized():
                        # Try a simple operation
                        try:
                            await client.list_tools_protocol()
                            health_status[service_name] = True
                        except Exception:
                            health_status[service_name] = False
                    else:
                        health_status[service_name] = False

                except Exception as e:
                    self.logger.error(f"Error checking health of service {service_name}: {e}")
                    health_status[service_name] = False

            return health_status

        except Exception as e:
            self.logger.error(f"Error during health check: {e}")
            return {}

    def get_discovery_stats(self) -> Dict[str, Any]:
        """Get service discovery statistics"""
        return {
            "discovered_services": len(self._discovered_services),
            "registered_services": len(self._service_registry),
            "discovery_callbacks": len(self._discovery_callbacks),
            "service_names": list(self._discovered_services.keys()),
        }

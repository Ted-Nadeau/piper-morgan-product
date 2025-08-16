"""
Development Environment MCP Spatial Adapter

Development environment-specific MCP spatial adapter implementation following the established
spatial adapter pattern for external system integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp

from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

from .consumer_core import MCPConsumerCore

logger = logging.getLogger(__name__)


class DevEnvironmentMCPSpatialAdapter(BaseSpatialAdapter):
    """
    Development Environment MCP spatial adapter implementation.

    Maps development environment IDs to spatial positions using MCP protocol
    for external service integration. Supports Docker and VS Code environments.
    """

    def __init__(self):
        super().__init__("devenvironment_mcp")
        self.mcp_consumer = MCPConsumerCore()
        self._lock = asyncio.Lock()
        self._environment_to_position: Dict[str, int] = {}
        self._position_to_environment: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # Docker API configuration
        self._docker_socket_path: str = "/var/run/docker.sock"
        self._docker_api_base = "http://localhost:2375"

        # VS Code/Codespace API configuration
        self._vscode_api_base = "http://localhost:3000"
        self._codespace_token: Optional[str] = None

        # HTTP session
        self._session: Optional[aiohttp.ClientSession] = None

        logger.info("DevEnvironmentMCPSpatialAdapter initialized")

    async def configure_dev_apis(
        self,
        docker_api_base: Optional[str] = None,
        vscode_api_base: Optional[str] = None,
        codespace_token: Optional[str] = None,
        docker_socket_path: Optional[str] = None,
    ):
        """Configure development environment API access"""
        if docker_api_base:
            self._docker_api_base = docker_api_base
        if vscode_api_base:
            self._vscode_api_base = vscode_api_base
        if codespace_token:
            self._codespace_token = codespace_token
        if docker_socket_path:
            self._docker_socket_path = docker_socket_path

        # Initialize HTTP session
        if not self._session:
            self._session = aiohttp.ClientSession()

        logger.info("Development environment APIs configured")

    async def _call_docker_api(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make API call to Docker daemon"""
        if not self._session:
            await self.configure_dev_apis()

        url = f"{self._docker_api_base}{endpoint}"

        try:
            async with self._session.get(url, timeout=30) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(
                        f"Docker API returned {response.status}: {await response.text()}"
                    )
                    return None
        except Exception as e:
            logger.error(f"Docker API call failed: {e}")
            return None

    async def _call_vscode_api(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make API call to VS Code/Codespace"""
        if not self._session:
            await self.configure_dev_apis()

        headers = {}
        if self._codespace_token:
            headers["Authorization"] = f"Bearer {self._codespace_token}"

        url = f"{self._vscode_api_base}{endpoint}"

        try:
            async with self._session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(
                        f"VS Code API returned {response.status}: {await response.text()}"
                    )
                    return None
        except Exception as e:
            logger.error(f"VS Code API call failed: {e}")
            return None

    async def get_docker_container(self, container_id: str) -> Optional[Dict[str, Any]]:
        """Get Docker container by ID"""
        result = await self._call_docker_api(f"/containers/{container_id}/json")

        if result:
            # Standardize container format
            standardized = {
                "id": result.get("Id", "")[:12],  # Short ID
                "name": result.get("Name", "").lstrip("/"),
                "type": "development",
                "status": result.get("State", {}).get("Status", "unknown"),
                "health_status": self._extract_health_status(result),
                "platform": "docker",
                "project": {"name": self._extract_project_name(result)},
                "workspace": {"name": self._extract_workspace_name(result)},
                "created_at": result.get("Created"),
                "started_at": result.get("State", {}).get("StartedAt"),
                "cpu_usage": 0,  # Would need stats API call
                "memory_usage": 0,  # Would need stats API call
                "restart_count": result.get("RestartCount", 0),
                "labels": (
                    list(result.get("Config", {}).get("Labels", {}).keys())
                    if result.get("Config", {}).get("Labels")
                    else []
                ),
                "services": self._extract_services_from_container(result),
                "depends_on": self._extract_depends_on(result),
                "volumes": result.get("Mounts", []),
                "technologies": self._extract_technologies(result),
            }

            # Add resource usage if available
            try:
                stats = await self._call_docker_api(
                    f"/containers/{container_id}/stats?stream=false"
                )
                if stats:
                    standardized.update(self._extract_resource_stats(stats))
            except Exception as e:
                logger.debug(f"Could not get stats for container {container_id}: {e}")

            return standardized

        return None

    async def get_vscode_workspace(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        """Get VS Code workspace information"""
        result = await self._call_vscode_api(f"/workspaces/{workspace_id}")

        if result:
            # Standardize workspace format
            standardized = {
                "id": workspace_id,
                "name": result.get("name", workspace_id),
                "type": "development",
                "status": "running" if result.get("active") else "stopped",
                "health_status": "healthy" if result.get("active") else "unknown",
                "platform": "vscode",
                "project": {"name": result.get("project", {}).get("name", "unknown")},
                "workspace": {"name": result.get("name", workspace_id)},
                "created_at": result.get("created_at"),
                "started_at": result.get("last_opened"),
                "owner": result.get("owner"),
                "team_members": result.get("collaborators", []),
                "technologies": result.get("detected_languages", []),
                "extensions": result.get("extensions", []),
                "shared_configs": result.get("shared_settings", []),
            }

            return standardized

        return None

    def _extract_health_status(self, container_data: Dict[str, Any]) -> str:
        """Extract health status from Docker container data"""
        state = container_data.get("State", {})
        if state.get("Health"):
            return state["Health"].get("Status", "unknown")
        elif state.get("Status") == "running":
            return "healthy"
        else:
            return "unknown"

    def _extract_project_name(self, container_data: Dict[str, Any]) -> str:
        """Extract project name from container labels or name"""
        labels = container_data.get("Config", {}).get("Labels", {})

        # Common label patterns for project identification
        for label in ["project", "com.docker.compose.project", "app"]:
            if label in labels:
                return labels[label]

        # Extract from container name
        name = container_data.get("Name", "").lstrip("/")
        if "_" in name:
            return name.split("_")[0]

        return "unknown"

    def _extract_workspace_name(self, container_data: Dict[str, Any]) -> str:
        """Extract workspace name from container data"""
        labels = container_data.get("Config", {}).get("Labels", {})

        # Common workspace label patterns
        for label in ["workspace", "com.docker.compose.service"]:
            if label in labels:
                return labels[label]

        return container_data.get("Name", "").lstrip("/")

    def _extract_services_from_container(
        self, container_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract service information from container"""
        # For single container, treat as one service
        state = container_data.get("State", {})
        return [
            {
                "name": container_data.get("Name", "").lstrip("/"),
                "status": state.get("Status", "unknown"),
                "ports": container_data.get("NetworkSettings", {}).get("Ports", {}),
            }
        ]

    def _extract_depends_on(self, container_data: Dict[str, Any]) -> List[str]:
        """Extract dependencies from container data"""
        labels = container_data.get("Config", {}).get("Labels", {})

        # Look for dependency labels
        deps = []
        for key, value in labels.items():
            if "depends" in key.lower() or "dependency" in key.lower():
                deps.extend(value.split(","))

        return deps

    def _extract_technologies(self, container_data: Dict[str, Any]) -> List[str]:
        """Extract technology stack from container image and labels"""
        technologies = []

        # Extract from image name
        image = container_data.get("Config", {}).get("Image", "")
        if ":" in image:
            image_name = image.split(":")[0]
            if "/" in image_name:
                image_name = image_name.split("/")[-1]
            technologies.append(image_name)

        # Extract from labels
        labels = container_data.get("Config", {}).get("Labels", {})
        for key, value in labels.items():
            if "technology" in key.lower() or "stack" in key.lower():
                technologies.extend(value.split(","))

        return technologies

    def _extract_resource_stats(self, stats_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract resource usage from Docker stats"""
        cpu_stats = stats_data.get("cpu_stats", {})
        memory_stats = stats_data.get("memory_stats", {})

        # Calculate CPU usage percentage
        cpu_usage = 0
        if cpu_stats.get("cpu_usage") and cpu_stats.get("system_cpu_usage"):
            cpu_delta = cpu_stats["cpu_usage"]["total_usage"] - cpu_stats.get(
                "precpu_stats", {}
            ).get("cpu_usage", {}).get("total_usage", 0)
            system_delta = cpu_stats["system_cpu_usage"] - cpu_stats.get("precpu_stats", {}).get(
                "system_cpu_usage", 0
            )
            if system_delta > 0:
                cpu_usage = (cpu_delta / system_delta) * 100

        # Calculate memory usage percentage
        memory_usage = 0
        if memory_stats.get("usage") and memory_stats.get("limit"):
            memory_usage = (memory_stats["usage"] / memory_stats["limit"]) * 100

        return {
            "cpu_usage": round(cpu_usage, 2),
            "memory_usage": round(memory_usage, 2),
            "network_io": stats_data.get("networks", {}).get("eth0", {}).get("rx_bytes", 0)
            + stats_data.get("networks", {}).get("eth0", {}).get("tx_bytes", 0),
        }

    async def search_docker_containers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Docker containers"""
        # Get all containers
        result = await self._call_docker_api("/containers/json?all=true")

        if not result:
            return []

        # Filter by query
        matching_containers = []
        query_lower = query.lower()

        for container in result:
            # Search in container name, image, and labels
            searchable_text = " ".join(
                [
                    container.get("Names", [""])[0].lstrip("/"),
                    container.get("Image", ""),
                    (
                        " ".join(container.get("Labels", {}).values())
                        if container.get("Labels")
                        else ""
                    ),
                    container.get("State", ""),
                ]
            ).lower()

            if query_lower in searchable_text:
                # Get full container details
                container_id = container.get("Id", "")
                full_container = await self.get_docker_container(container_id)
                if full_container:
                    matching_containers.append(full_container)

        return matching_containers[:limit]

    async def search_vscode_workspaces(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search VS Code workspaces"""
        # Get workspaces list
        result = await self._call_vscode_api("/workspaces")

        if not result:
            return []

        # Filter by query
        matching_workspaces = []
        query_lower = query.lower()

        for workspace in result.get("workspaces", []):
            # Search in workspace name and project
            searchable_text = " ".join(
                [
                    workspace.get("name", ""),
                    workspace.get("project", {}).get("name", ""),
                    " ".join(workspace.get("detected_languages", [])),
                ]
            ).lower()

            if query_lower in searchable_text:
                workspace_id = workspace.get("id", "")
                full_workspace = await self.get_vscode_workspace(workspace_id)
                if full_workspace:
                    matching_workspaces.append(full_workspace)

        return matching_workspaces[:limit]

    async def search_environments(
        self, query: str, platforms: List[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search development environments across platforms"""
        all_results = []

        # Default to both platforms if not specified
        if not platforms:
            platforms = ["docker", "vscode"]

        # Search Docker containers
        if "docker" in platforms:
            try:
                docker_results = await self.search_docker_containers(query, limit // 2)
                all_results.extend(docker_results)
            except Exception as e:
                logger.warning(f"Failed to search Docker containers: {e}")

        # Search VS Code workspaces
        if "vscode" in platforms:
            try:
                vscode_results = await self.search_vscode_workspaces(query, limit // 2)
                all_results.extend(vscode_results)
            except Exception as e:
                logger.warning(f"Failed to search VS Code workspaces: {e}")

        return all_results[:limit]

    async def map_to_position(
        self, environment_id: str, context: Dict[str, Any]
    ) -> SpatialPosition:
        """Map development environment ID to spatial position"""
        async with self._lock:
            # Check if we already have a mapping
            if environment_id in self._environment_to_position:
                position = self._environment_to_position[environment_id]
                return SpatialPosition(
                    position=position,
                    context={
                        "external_id": environment_id,
                        "external_system": "development",
                        **context,
                    },
                )

            # Create new mapping
            position = len(self._environment_to_position) + 1
            self._environment_to_position[environment_id] = position
            self._position_to_environment[position] = environment_id
            self._context_storage[environment_id] = context

            logger.info(f"Mapped development environment {environment_id} to position {position}")

            return SpatialPosition(
                position=position,
                context={
                    "external_id": environment_id,
                    "external_system": "development",
                    **context,
                },
            )

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """Map spatial position back to development environment ID"""
        return self._position_to_environment.get(position.position)

    async def store_mapping(self, environment_id: str, position: SpatialPosition) -> bool:
        """Store mapping between development environment ID and spatial position"""
        try:
            async with self._lock:
                self._environment_to_position[environment_id] = position.position
                self._position_to_environment[position.position] = environment_id
                self._context_storage[environment_id] = position.context
            return True
        except Exception as e:
            logger.error(
                f"Failed to store mapping for development environment {environment_id}: {e}"
            )
            return False

    async def get_context(self, environment_id: str) -> Optional[SpatialContext]:
        """Get spatial context for development environment ID"""
        context_data = self._context_storage.get(environment_id)
        if not context_data:
            return None

        return SpatialContext(
            territory_id="development",
            room_id=context_data.get("platform", "unknown"),
            path_id=f"environments/{environment_id}",
            attention_level=context_data.get("attention_level", "medium"),
            emotional_valence=context_data.get("emotional_valence", "neutral"),
            navigation_intent=context_data.get("navigation_intent", "explore"),
            external_system="development",
            external_id=environment_id,
            external_context=context_data,
        )

    async def initialize_connection_pool(self):
        """Initialize MCP connection pool for development environment integration"""
        try:
            await self.mcp_consumer.initialize()
            logger.info("Development environment MCP connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize development environment MCP connection pool: {e}")

    async def close(self):
        """Close the development environment adapter and cleanup resources"""
        if self._session:
            await self._session.close()

        await self.mcp_consumer.close()
        logger.info("Development environment MCP adapter closed")

    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings"""
        return {
            "system_name": self.system_name,
            "total_mappings": len(self._environment_to_position),
            "total_contexts": len(self._context_storage),
            "next_position": len(self._environment_to_position) + 1,
            "docker_api_base": self._docker_api_base,
            "vscode_api_base": self._vscode_api_base,
            "has_session": self._session is not None,
        }

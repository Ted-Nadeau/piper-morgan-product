"""
Development Environment Spatial Intelligence Implementation
Following ADR-013: MCP + Spatial Intelligence Pattern

Mirrors LinearSpatialIntelligence with 8-dimensional spatial analysis for development environments.
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)
from services.mcp.consumer.devenvironment_adapter import DevEnvironmentMCPSpatialAdapter

logger = logging.getLogger(__name__)


class DevEnvironmentSpatialIntelligence:
    """
    Development Environment integration using MCP + Spatial Intelligence pattern.
    Following LinearSpatialIntelligence implementation pattern exactly.

    8 Dimensions:
    1. HIERARCHY - Containers → Services → Dependencies → Configurations
    2. TEMPORAL - Container uptime, deployment times, restart patterns
    3. PRIORITY - Critical services, environment health, resource usage
    4. COLLABORATIVE - Team environments, shared configs, access patterns
    5. FLOW - Container states (running/stopped/building), deployment status
    6. QUANTITATIVE - Resource usage, performance metrics, capacity
    7. CAUSAL - Dependencies, startup order, failure cascades
    8. CONTEXTUAL - Project, environment type, team, platform context
    """

    def __init__(self):
        """Initialize Development Environment spatial intelligence with MCP adapter"""
        self.mcp_adapter = DevEnvironmentMCPSpatialAdapter()

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_container_hierarchy,
            "TEMPORAL": self.analyze_timeline,
            "PRIORITY": self.analyze_priority_signals,
            "COLLABORATIVE": self.analyze_team_activity,
            "FLOW": self.analyze_workflow_state,
            "QUANTITATIVE": self.analyze_metrics,
            "CAUSAL": self.analyze_dependencies,
            "CONTEXTUAL": self.analyze_project_context,
        }

        logger.info("DevEnvironmentSpatialIntelligence initialized with 8 dimensions")

    async def initialize(self):
        """Initialize MCP adapter and connections"""
        await self.mcp_adapter.configure_dev_apis()
        logger.info("Development Environment MCP adapter configured")

    # DIMENSION 1: HIERARCHY
    async def analyze_container_hierarchy(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze container/service hierarchy and relationships"""
        hierarchy = {
            "level": "environment",  # environment, service, container, dependency
            "type": environment.get("type", "development"),  # development, staging, production
            "depth": 0,
            "has_children": False,
            "parent_service": None,
            "child_containers": [],
            "project_id": environment.get("project_id"),
            "workspace_id": environment.get("workspace_id"),
        }

        # Check for service hierarchy
        if services := environment.get("services", []):
            hierarchy["has_children"] = True
            hierarchy["child_containers"] = [service.get("name") for service in services]
            hierarchy["depth"] = len(services)

        # Check for parent service/workspace
        if parent := environment.get("parent_workspace"):
            hierarchy["level"] = "service"
            hierarchy["depth"] = 1
            hierarchy["parent_service"] = parent.get("name")

        # Check if this is a container-level view
        if container_id := environment.get("container_id"):
            hierarchy["level"] = "container"
            hierarchy["depth"] = 2

        return hierarchy

    # DIMENSION 2: TEMPORAL
    async def analyze_timeline(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal patterns and uptime timeline"""
        from datetime import timezone

        now = datetime.now(timezone.utc)
        created = datetime.fromisoformat(
            environment.get("created_at", now.isoformat()).replace("Z", "+00:00")
        )
        updated = datetime.fromisoformat(
            environment.get("updated_at", now.isoformat()).replace("Z", "+00:00")
        )

        # Calculate environment metrics
        age_hours = (now - created).total_seconds() / 3600
        last_activity_minutes = (now - updated).total_seconds() / 60

        # Determine activity level
        if last_activity_minutes < 5:
            activity_level = "active"
        elif last_activity_minutes < 30:
            activity_level = "recent"
        elif last_activity_minutes < 1440:  # 24 hours
            activity_level = "moderate"
        else:
            activity_level = "stale"

        # Check container uptime urgency
        urgency = "normal"
        if restart_count := environment.get("restart_count", 0):
            if restart_count > 5:
                urgency = "high"
            elif restart_count > 2:
                urgency = "medium"

        # Check for scheduled maintenance
        if maintenance := environment.get("maintenance_window"):
            maintenance_time = datetime.fromisoformat(maintenance.replace("Z", "+00:00"))
            minutes_to_maintenance = (maintenance_time - now).total_seconds() / 60
            if minutes_to_maintenance <= 30:
                urgency = "high"

        # Calculate uptime
        uptime_seconds = None
        if started_at := environment.get("started_at"):
            started = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
            uptime_seconds = (now - started).total_seconds()

        return {
            "age_hours": age_hours,
            "last_activity_minutes": last_activity_minutes,
            "activity_level": activity_level,
            "urgency": urgency,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
            "started_at": environment.get("started_at"),
            "maintenance_window": environment.get("maintenance_window"),
            "uptime_seconds": uptime_seconds,
            "restart_count": environment.get("restart_count", 0),
        }

    # DIMENSION 3: PRIORITY
    async def analyze_priority_signals(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze priority signals from environment type, health, resource usage"""
        env_type = environment.get("type", "development")
        health_status = environment.get("health_status", "unknown")
        cpu_usage = environment.get("cpu_usage", 0)
        memory_usage = environment.get("memory_usage", 0)

        # Determine priority level based on environment type and health
        priority_level = "normal"
        if env_type == "production" or health_status == "critical":
            priority_level = "critical"
        elif env_type == "staging" or health_status == "degraded":
            priority_level = "high"
        elif env_type == "development":
            priority_level = "normal"
        else:
            priority_level = "low"

        # Calculate attention score (0.0 - 1.0)
        attention_score = 0.5  # Base score

        if priority_level == "critical":
            attention_score = 1.0
        elif priority_level == "high":
            attention_score = 0.8
        elif priority_level == "low":
            attention_score = 0.3

        # Boost for high resource usage
        if cpu_usage > 80 or memory_usage > 80:
            attention_score = min(1.0, attention_score + 0.3)

        # Boost for production environments
        if env_type == "production":
            attention_score = min(1.0, attention_score + 0.2)

        # Check for container labels/tags
        labels = environment.get("labels", [])
        is_critical = "critical" in labels or "production" in labels
        is_shared = "shared" in labels or "team" in labels

        if is_critical:
            priority_level = "critical"
            attention_score = 1.0

        return {
            "priority_level": priority_level,
            "env_type": env_type,
            "health_status": health_status,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "is_critical": is_critical,
            "is_shared": is_shared,
            "is_production": env_type == "production",
            "attention_score": attention_score,
            "labels": labels,
        }

    # DIMENSION 4: COLLABORATIVE
    async def analyze_team_activity(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze team collaboration and environment sharing"""
        # Get owner/creator
        owner = environment.get("owner", {}).get("username") if environment.get("owner") else None

        # Get team members with access
        team_members = []
        if members := environment.get("team_members", []):
            team_members = [m.get("username") for m in members if m.get("username")]

        # Get active users (recent connections)
        active_users = []
        if connections := environment.get("recent_connections", []):
            active_users = [c.get("username") for c in connections if c.get("username")]

        # Container access count
        access_count = len(environment.get("access_logs", []))

        # Determine engagement level
        total_participants = len(set(team_members + active_users))

        if total_participants >= 5:
            engagement_level = "high"
        elif total_participants >= 2:
            engagement_level = "moderate"
        else:
            engagement_level = "low"

        # Check for shared configurations
        shared_configs = len(environment.get("shared_configs", []))
        has_shared_volumes = bool(environment.get("shared_volumes", []))

        return {
            "owner": owner,
            "team_member_count": len(team_members),
            "active_user_count": len(active_users),
            "access_count": access_count,
            "engagement_level": engagement_level,
            "participants": list(set(team_members + active_users)),
            "team_members": team_members,
            "active_users": active_users,
            "shared_configs": shared_configs,
            "has_shared_volumes": has_shared_volumes,
        }

    # DIMENSION 5: FLOW
    async def analyze_workflow_state(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze container/service workflow state and progress"""
        status = environment.get("status", "unknown")
        health_status = environment.get("health_status", "unknown")

        # Map container status to workflow stages
        workflow_stage_map = {
            "running": "active",
            "stopped": "inactive",
            "building": "provisioning",
            "starting": "starting",
            "stopping": "stopping",
            "restarting": "restarting",
            "created": "created",
            "exited": "stopped",
            "dead": "failed",
            "paused": "paused",
        }

        workflow_stage = workflow_stage_map.get(status.lower(), "unknown")

        # Check if blocked or unhealthy
        is_blocked = status == "blocked" or health_status == "unhealthy"

        # Estimate service availability percentage
        availability = 0
        if services := environment.get("services", []):
            healthy_services = [s for s in services if s.get("status") == "running"]
            availability = (len(healthy_services) / len(services)) * 100 if services else 0
        elif status == "running" and health_status == "healthy":
            availability = 100
        elif status == "running":
            availability = 75
        elif status in ["starting", "building"]:
            availability = 25

        return {
            "status": status,
            "health_status": health_status,
            "workflow_stage": workflow_stage,
            "is_blocked": is_blocked,
            "availability_percentage": availability,
            "is_healthy": health_status == "healthy",
            "is_running": status == "running",
            "can_restart": status in ["stopped", "exited", "failed"],
        }

    # DIMENSION 6: QUANTITATIVE
    async def analyze_metrics(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quantitative metrics and resource usage"""
        from datetime import timezone

        created = datetime.fromisoformat(
            environment.get("created_at", datetime.now().isoformat()).replace("Z", "+00:00")
        )
        now = datetime.now(timezone.utc)

        # Resource usage metrics
        cpu_usage = environment.get("cpu_usage", 0)
        memory_usage = environment.get("memory_usage", 0)
        disk_usage = environment.get("disk_usage", 0)
        network_io = environment.get("network_io", 0)

        # Calculate uptime
        uptime_hours = None
        if started_at := environment.get("started_at"):
            started = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
            uptime_hours = (now - started).total_seconds() / 3600

        # Service count metrics
        service_count = len(environment.get("services", []))
        running_services = len(
            [s for s in environment.get("services", []) if s.get("status") == "running"]
        )

        # Calculate service health rate
        service_health_rate = 0
        if service_count > 0:
            service_health_rate = (running_services / service_count) * 100

        # Complexity estimation
        complexity = "low"
        if service_count > 10 or (uptime_hours and uptime_hours > 168):  # 1 week
            complexity = "high"
        elif service_count > 5 or (uptime_hours and uptime_hours > 24):  # 1 day
            complexity = "medium"

        # Resource efficiency
        resource_efficiency = "good"
        if cpu_usage > 90 or memory_usage > 90 or disk_usage > 90:
            resource_efficiency = "poor"
        elif cpu_usage > 70 or memory_usage > 70 or disk_usage > 70:
            resource_efficiency = "moderate"

        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "network_io": network_io,
            "uptime_hours": uptime_hours,
            "service_count": service_count,
            "running_services": running_services,
            "service_health_rate": service_health_rate,
            "complexity_estimate": complexity,
            "resource_efficiency": resource_efficiency,
            "restart_count": environment.get("restart_count", 0),
        }

    # DIMENSION 7: CAUSAL
    async def analyze_dependencies(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze causal relationships and service dependencies"""
        # Get dependency information
        depends_on = environment.get("depends_on", [])
        blocked_by = environment.get("blocked_by", [])
        blocks = environment.get("blocks", [])

        # Service startup order
        startup_order = environment.get("startup_order", [])

        # Check for external dependencies
        external_deps = []
        if databases := environment.get("databases", []):
            external_deps.extend(databases)
        if apis := environment.get("external_apis", []):
            external_deps.extend(apis)

        # Failure cascade analysis
        critical_dependencies = []
        if critical_services := environment.get("critical_services", []):
            critical_dependencies = [s for s in critical_services if s.get("status") != "running"]

        # Configuration dependencies
        config_deps = len(environment.get("config_files", []))
        volume_deps = len(environment.get("volumes", []))

        dependency_chain_length = len(depends_on) + len(blocks) + len(external_deps)

        return {
            "depends_on": depends_on,
            "blocked_by": blocked_by,
            "blocks": blocks,
            "startup_order": startup_order,
            "external_deps": external_deps,
            "critical_dependencies": critical_dependencies,
            "config_deps": config_deps,
            "volume_deps": volume_deps,
            "dependency_chain_length": dependency_chain_length,
            "has_dependencies": dependency_chain_length > 0,
            "has_critical_failures": len(critical_dependencies) > 0,
        }

    # DIMENSION 8: CONTEXTUAL
    async def analyze_project_context(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project and development context"""
        # Get project information
        project_name = (
            environment.get("project", {}).get("name", "unknown")
            if environment.get("project")
            else "unknown"
        )
        workspace_name = (
            environment.get("workspace", {}).get("name", "unknown")
            if environment.get("workspace")
            else "unknown"
        )

        # Development platform context
        platform = "unknown"
        if "docker" in environment.get("platform", "").lower():
            platform = "docker"
        elif "vscode" in environment.get("platform", "").lower():
            platform = "vscode"
        elif "devcontainer" in environment.get("platform", "").lower():
            platform = "devcontainer"
        elif "codespace" in environment.get("platform", "").lower():
            platform = "codespace"

        # Determine domain based on project type and technologies
        domain = "general"
        technologies = environment.get("technologies", [])
        tech_text = " ".join(technologies).lower()

        if any(keyword in tech_text for keyword in ["api", "backend", "server", "microservice"]):
            domain = "backend_development"
        elif any(keyword in tech_text for keyword in ["frontend", "react", "vue", "angular", "ui"]):
            domain = "frontend_development"
        elif any(keyword in tech_text for keyword in ["mobile", "ios", "android", "flutter"]):
            domain = "mobile_development"
        elif any(keyword in tech_text for keyword in ["data", "ml", "ai", "jupyter", "python"]):
            domain = "data_science"
        elif any(
            keyword in tech_text for keyword in ["devops", "docker", "kubernetes", "terraform"]
        ):
            domain = "infrastructure"

        # Environment type and team
        env_type = environment.get("type", "development")
        team_name = (
            environment.get("team", {}).get("name", "unknown")
            if environment.get("team")
            else "unknown"
        )

        return {
            "project_name": project_name,
            "workspace_name": workspace_name,
            "platform": platform,
            "domain": domain,
            "env_type": env_type,
            "team_name": team_name,
            "technologies": technologies,
            "full_name": (
                f"{project_name}/{workspace_name}" if workspace_name != "unknown" else project_name
            ),
        }

    # MAIN SPATIAL CONTEXT CREATION
    async def create_spatial_context(self, environment: Dict[str, Any]) -> SpatialContext:
        """Create full 8-dimensional spatial context for development environment"""
        # Run all dimensional analyses in parallel
        dimension_results = await asyncio.gather(
            self.analyze_container_hierarchy(environment),
            self.analyze_timeline(environment),
            self.analyze_priority_signals(environment),
            self.analyze_team_activity(environment),
            self.analyze_workflow_state(environment),
            self.analyze_metrics(environment),
            self.analyze_dependencies(environment),
            self.analyze_project_context(environment),
        )

        # Unpack results
        hierarchy, temporal, priority, collaborative, flow, quantitative, causal, contextual = (
            dimension_results
        )

        # Determine attention level based on priority and health
        if priority["priority_level"] == "critical" or flow["is_blocked"]:
            attention_level = "urgent"
        elif priority["priority_level"] == "high" or temporal["activity_level"] == "active":
            attention_level = "high"
        elif temporal["activity_level"] == "stale" or not flow["is_running"]:
            attention_level = "low"
        else:
            attention_level = "medium"

        # Determine emotional valence
        if flow["is_blocked"] or quantitative["resource_efficiency"] == "poor":
            emotional_valence = "negative"
        elif flow["is_healthy"] and quantitative["resource_efficiency"] == "good":
            emotional_valence = "positive"
        else:
            emotional_valence = "neutral"

        # Determine navigation intent
        if flow["is_blocked"] or causal["has_critical_failures"]:
            navigation_intent = "investigate"
        elif flow["workflow_stage"] == "active" and priority["priority_level"] in [
            "critical",
            "high",
        ]:
            navigation_intent = "monitor"
        elif not flow["is_running"]:
            navigation_intent = "respond"
        else:
            navigation_intent = "explore"

        # Create spatial context
        return SpatialContext(
            territory_id="development",
            room_id=contextual["platform"],
            path_id=(
                f"environments/{environment['name']}"
                if environment.get("name")
                else f"environments/{environment.get('id', 'unknown')}"
            ),
            attention_level=attention_level,
            emotional_valence=emotional_valence,
            navigation_intent=navigation_intent,
            external_system="development",
            external_id=str(environment.get("name", environment.get("id", "unknown"))),
            external_context={
                "hierarchy": hierarchy,
                "temporal": temporal,
                "priority": priority,
                "collaborative": collaborative,
                "flow": flow,
                "quantitative": quantitative,
                "causal": causal,
                "contextual": contextual,
            },
        )

    # HELPER METHODS FOR INTEGRATION
    async def map_environment_to_position(
        self, environment_id: str, context: Dict[str, Any]
    ) -> SpatialPosition:
        """Map development environment to spatial position using MCP adapter"""
        return await self.mcp_adapter.map_to_position(environment_id, context)

    async def get_environment(self, project_name: str, environment_name: str) -> Dict[str, Any]:
        """Get environment data using MCP adapter (backward compatibility)"""
        result = await self.mcp_adapter._call_docker_api(f"/containers/{environment_name}")
        return result or {"name": environment_name}

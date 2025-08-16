"""
CI/CD MCP Spatial Adapter

CI/CD-specific MCP spatial adapter implementation following the established
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


class CICDMCPSpatialAdapter(BaseSpatialAdapter):
    """
    CI/CD MCP spatial adapter implementation.

    Maps CI/CD pipeline IDs to spatial positions using MCP protocol
    for external service integration. Supports GitHub Actions and GitLab CI.
    """

    def __init__(self):
        super().__init__("cicd_mcp")
        self.mcp_consumer = MCPConsumerCore()
        self._lock = asyncio.Lock()
        self._pipeline_to_position: Dict[str, int] = {}
        self._position_to_pipeline: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # GitHub Actions API configuration
        self._github_token: Optional[str] = None
        self._github_api_base = "https://api.github.com"

        # GitLab CI API configuration
        self._gitlab_token: Optional[str] = None
        self._gitlab_api_base = "https://gitlab.com/api/v4"

        # HTTP session
        self._session: Optional[aiohttp.ClientSession] = None

        logger.info("CICDMCPSpatialAdapter initialized")

    async def configure_cicd_apis(
        self,
        github_token: Optional[str] = None,
        gitlab_token: Optional[str] = None,
        github_api_base: Optional[str] = None,
        gitlab_api_base: Optional[str] = None,
    ):
        """Configure CI/CD API access"""
        if github_token:
            self._github_token = github_token
        if gitlab_token:
            self._gitlab_token = gitlab_token
        if github_api_base:
            self._github_api_base = github_api_base
        if gitlab_api_base:
            self._gitlab_api_base = gitlab_api_base

        # Initialize HTTP session
        if not self._session:
            self._session = aiohttp.ClientSession()

        logger.info("CI/CD APIs configured")

    async def _call_github_actions_api(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make API call to GitHub Actions"""
        if not self._session:
            await self.configure_cicd_apis()

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self._github_token}" if self._github_token else "",
        }

        url = f"{self._github_api_base}{endpoint}"

        try:
            async with self._session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(
                        f"GitHub Actions API returned {response.status}: {await response.text()}"
                    )
                    return None
        except Exception as e:
            logger.error(f"GitHub Actions API call failed: {e}")
            return None

    async def _call_gitlab_ci_api(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make API call to GitLab CI"""
        if not self._session:
            await self.configure_cicd_apis()

        headers = {
            "Authorization": f"Bearer {self._gitlab_token}" if self._gitlab_token else "",
        }

        url = f"{self._gitlab_api_base}{endpoint}"

        try:
            async with self._session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(
                        f"GitLab CI API returned {response.status}: {await response.text()}"
                    )
                    return None
        except Exception as e:
            logger.error(f"GitLab CI API call failed: {e}")
            return None

    async def get_github_workflow_run(
        self, repository: str, run_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get GitHub Actions workflow run by ID"""
        result = await self._call_github_actions_api(f"/repos/{repository}/actions/runs/{run_id}")

        if result:
            # Enrich with jobs information
            jobs_result = await self._call_github_actions_api(
                f"/repos/{repository}/actions/runs/{run_id}/jobs"
            )
            if jobs_result:
                result["jobs"] = jobs_result.get("jobs", [])

        return result

    async def get_gitlab_pipeline(
        self, project_id: str, pipeline_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get GitLab CI pipeline by ID"""
        result = await self._call_gitlab_ci_api(f"/projects/{project_id}/pipelines/{pipeline_id}")

        if result:
            # Enrich with jobs information
            jobs_result = await self._call_gitlab_ci_api(
                f"/projects/{project_id}/pipelines/{pipeline_id}/jobs"
            )
            if jobs_result:
                result["jobs"] = jobs_result

        return result

    async def search_github_workflows(
        self, repository: str, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search GitHub Actions workflow runs"""
        # Get recent workflow runs
        result = await self._call_github_actions_api(
            f"/repos/{repository}/actions/runs?per_page={limit}"
        )

        if not result:
            return []

        workflow_runs = result.get("workflow_runs", [])

        # Filter by query
        matching_runs = []
        query_lower = query.lower()

        for run in workflow_runs:
            # Search in workflow name, head commit message, and branch
            searchable_text = " ".join(
                [
                    run.get("name", ""),
                    run.get("head_commit", {}).get("message", ""),
                    run.get("head_branch", ""),
                    run.get("event", ""),
                ]
            ).lower()

            if query_lower in searchable_text:
                # Standardize the format
                standardized_run = {
                    "id": run.get("id"),
                    "type": "build",  # GitHub Actions are primarily builds
                    "status": run.get("status"),
                    "conclusion": run.get("conclusion"),
                    "workflow_name": run.get("name"),
                    "branch": run.get("head_branch"),
                    "repository": {
                        "full_name": run.get("repository", {}).get("full_name"),
                        "owner": run.get("repository", {}).get("owner"),
                    },
                    "triggered_by": run.get("triggering_actor"),
                    "created_at": run.get("created_at"),
                    "updated_at": run.get("updated_at"),
                    "completed_at": run.get("completed_at"),
                    "url": run.get("html_url"),
                    "platform": "github_actions",
                    "trigger": {
                        "type": run.get("event"),
                        "commit": run.get("head_commit"),
                    },
                    "environment": self._extract_environment_from_run(run),
                }
                matching_runs.append(standardized_run)

        return matching_runs[:limit]

    async def search_gitlab_pipelines(
        self, project_id: str, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search GitLab CI pipelines"""
        # Get recent pipelines
        result = await self._call_gitlab_ci_api(
            f"/projects/{project_id}/pipelines?per_page={limit}&order_by=updated_at"
        )

        if not result:
            return []

        # Filter by query
        matching_pipelines = []
        query_lower = query.lower()

        for pipeline in result:
            # Search in ref (branch), status
            searchable_text = " ".join(
                [
                    pipeline.get("ref", ""),
                    pipeline.get("status", ""),
                    pipeline.get("source", ""),
                ]
            ).lower()

            if query_lower in searchable_text:
                # Standardize the format
                standardized_pipeline = {
                    "id": pipeline.get("id"),
                    "type": "build",  # GitLab pipelines are primarily builds
                    "status": pipeline.get("status"),
                    "conclusion": pipeline.get("status"),  # GitLab uses status for both
                    "workflow_name": f"Pipeline {pipeline.get('id')}",
                    "branch": pipeline.get("ref"),
                    "repository": {
                        "full_name": f"project-{project_id}",  # Simplified
                        "owner": {"login": "gitlab"},
                    },
                    "triggered_by": {"login": pipeline.get("user", {}).get("username", "unknown")},
                    "created_at": pipeline.get("created_at"),
                    "updated_at": pipeline.get("updated_at"),
                    "completed_at": pipeline.get("finished_at"),
                    "url": pipeline.get("web_url"),
                    "platform": "gitlab_ci",
                    "trigger": {
                        "type": pipeline.get("source"),
                        "commit": {"sha": pipeline.get("sha")},
                    },
                    "environment": self._extract_environment_from_pipeline(pipeline),
                }
                matching_pipelines.append(standardized_pipeline)

        return matching_pipelines[:limit]

    def _extract_environment_from_run(self, run: Dict[str, Any]) -> str:
        """Extract environment from GitHub Actions run"""
        # Try to infer from branch name or workflow name
        branch = run.get("head_branch", "").lower()
        workflow_name = run.get("name", "").lower()

        if "prod" in branch or "prod" in workflow_name:
            return "production"
        elif "staging" in branch or "staging" in workflow_name:
            return "staging"
        elif "main" in branch or "master" in branch:
            return "staging"
        else:
            return "development"

    def _extract_environment_from_pipeline(self, pipeline: Dict[str, Any]) -> str:
        """Extract environment from GitLab CI pipeline"""
        # Try to infer from ref (branch) name
        ref = pipeline.get("ref", "").lower()

        if "prod" in ref:
            return "production"
        elif "staging" in ref:
            return "staging"
        elif "main" in ref or "master" in ref:
            return "staging"
        else:
            return "development"

    async def search_pipelines(
        self, query: str, repositories: List[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search CI/CD pipelines across platforms"""
        all_results = []

        # Search GitHub Actions (if repositories specified)
        if repositories:
            for repo in repositories:
                if "/" in repo:  # GitHub repo format owner/name
                    try:
                        github_results = await self.search_github_workflows(repo, query, limit // 2)
                        all_results.extend(github_results)
                    except Exception as e:
                        logger.warning(f"Failed to search GitHub workflows for {repo}: {e}")
                else:  # Might be GitLab project ID
                    try:
                        gitlab_results = await self.search_gitlab_pipelines(repo, query, limit // 2)
                        all_results.extend(gitlab_results)
                    except Exception as e:
                        logger.warning(f"Failed to search GitLab pipelines for {repo}: {e}")

        return all_results[:limit]

    async def map_to_position(self, pipeline_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """Map CI/CD pipeline ID to spatial position"""
        async with self._lock:
            # Check if we already have a mapping
            if pipeline_id in self._pipeline_to_position:
                position = self._pipeline_to_position[pipeline_id]
                return SpatialPosition(
                    position=position,
                    context={"external_id": pipeline_id, "external_system": "cicd", **context},
                )

            # Create new mapping
            position = len(self._pipeline_to_position) + 1
            self._pipeline_to_position[pipeline_id] = position
            self._position_to_pipeline[position] = pipeline_id
            self._context_storage[pipeline_id] = context

            logger.info(f"Mapped CI/CD pipeline {pipeline_id} to position {position}")

            return SpatialPosition(
                position=position,
                context={"external_id": pipeline_id, "external_system": "cicd", **context},
            )

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """Map spatial position back to CI/CD pipeline ID"""
        return self._position_to_pipeline.get(position.position)

    async def store_mapping(self, pipeline_id: str, position: SpatialPosition) -> bool:
        """Store mapping between CI/CD pipeline ID and spatial position"""
        try:
            async with self._lock:
                self._pipeline_to_position[pipeline_id] = position.position
                self._position_to_pipeline[position.position] = pipeline_id
                self._context_storage[pipeline_id] = position.context
            return True
        except Exception as e:
            logger.error(f"Failed to store mapping for CI/CD pipeline {pipeline_id}: {e}")
            return False

    async def get_context(self, pipeline_id: str) -> Optional[SpatialContext]:
        """Get spatial context for CI/CD pipeline ID"""
        context_data = self._context_storage.get(pipeline_id)
        if not context_data:
            return None

        return SpatialContext(
            territory_id="cicd",
            room_id=context_data.get("platform", "unknown"),
            path_id=f"pipelines/{pipeline_id}",
            attention_level=context_data.get("attention_level", "medium"),
            emotional_valence=context_data.get("emotional_valence", "neutral"),
            navigation_intent=context_data.get("navigation_intent", "explore"),
            external_system="cicd",
            external_id=pipeline_id,
            external_context=context_data,
        )

    async def initialize_connection_pool(self):
        """Initialize MCP connection pool for CI/CD integration"""
        try:
            await self.mcp_consumer.initialize()
            logger.info("CI/CD MCP connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize CI/CD MCP connection pool: {e}")

    async def close(self):
        """Close the CI/CD adapter and cleanup resources"""
        if self._session:
            await self._session.close()

        await self.mcp_consumer.close()
        logger.info("CI/CD MCP adapter closed")

    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings"""
        return {
            "system_name": self.system_name,
            "total_mappings": len(self._pipeline_to_position),
            "total_contexts": len(self._context_storage),
            "next_position": len(self._pipeline_to_position) + 1,
            "github_api_base": self._github_api_base,
            "gitlab_api_base": self._gitlab_api_base,
            "has_session": self._session is not None,
        }

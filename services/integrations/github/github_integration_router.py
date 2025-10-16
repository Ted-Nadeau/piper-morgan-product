"""
GitHub Integration Router - Spatial-Only Integration
PM-033b-deprecation: Week 4 Complete - Legacy Removed (CORE-INT #109)

This router provides GitHub integration exclusively through:
- GitHubSpatialIntelligence (8-dimensional spatial analysis)

Deprecation timeline completed:
Week 1: ✅ Both integrations available, spatial default
Week 2: ✅ Deprecation warnings when legacy used
Week 3: ✅ Legacy disabled by default, emergency rollback available
Week 4: ✅ Legacy code removed (October 15, 2025)

Architecture Decision: ADR-013 MCP+Spatial Integration Pattern
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from services.infrastructure.config.feature_flags import FeatureFlags
from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence

from .config_service import GitHubConfigService

logger = logging.getLogger(__name__)


class GitHubIntegrationRouter:
    """
    Routes GitHub operations to GitHubSpatialIntelligence (spatial-only, Week 4).

    Week 4 Complete (CORE-INT #109): Legacy code removed, simplified to spatial-only.
    Previously provided feature flag-based switching during 4-week deprecation.

    Follows service injection pattern (ADR-010) for configuration management.
    """

    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        """
        Initialize GitHub integration router with feature flag detection and config service.

        Args:
            config_service: Optional GitHubConfigService for dependency injection.
                          If not provided, creates a default instance.
        """
        # Store config service (service injection pattern)
        self.config_service = config_service or GitHubConfigService()

        self.spatial_github = None

        # Feature flag state (legacy flags kept for backward compatibility with tests)
        self.use_spatial = FeatureFlags.should_use_spatial_github()

        # Initialize spatial integration
        self._initialize_integrations()

        logger.info("GitHubIntegrationRouter initialized - Spatial GitHub only")

    def _initialize_integrations(self):
        """Initialize GitHubSpatialIntelligence (legacy code removed in Week 4)"""
        try:
            self.spatial_github = GitHubSpatialIntelligence()
            logger.info("GitHubSpatialIntelligence initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GitHubSpatialIntelligence: {e}")
            raise RuntimeError("Spatial GitHub initialization failed") from e

    async def initialize(self):
        """Initialize the GitHub integration asynchronously"""
        if self.spatial_github and hasattr(self.spatial_github, "initialize"):
            await self.spatial_github.initialize()

    def _get_integration(self, operation: str) -> Any:
        """
        Get the spatial GitHub integration.

        Args:
            operation: Operation name (for error messages)

        Returns:
            GitHubSpatialIntelligence instance

        Raises:
            RuntimeError: If spatial integration not available
        """
        if not self.spatial_github:
            raise RuntimeError(f"GitHub integration not available for {operation}")
        return self.spatial_github

    async def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """Get GitHub issue."""
        return await self._get_integration("get_issue").get_issue(repo_name, issue_number)

    async def list_issues(self, repository: str, **kwargs) -> List[Dict[str, Any]]:
        """
        List GitHub issues.
        """
        return await self._get_integration("list_issues").list_issues(repository, **kwargs)

    async def create_issue(
        self, repo_name: str, title: str, body: str, labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create GitHub issue.
        """
        return await self._get_integration("create_issue").create_issue(
            repo_name, title, body, labels
        )

    async def update_issue(
        self,
        repo_name: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update existing GitHub issue."""
        return await self._get_integration("update_issue").update_issue(
            repo_name, issue_number, title, body, state, labels, assignees
        )

    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status for monitoring and debugging."""
        integration = self._get_integration("get_integration_status")
        if hasattr(integration, "get_integration_status"):
            return integration.get_integration_status()
        # Fallback status if integration doesn't support status method
        return {
            "router_initialized": True,
            "spatial_available": self.spatial_github is not None,
            "using_spatial_only": True,
            "legacy_removed": True,
            "deprecation_timeline": {
                "week": self._get_deprecation_week(),
                "status": "Week 4 Complete - Legacy removed",
                "legacy_removal_date": "2025-10-15",  # Today!
            },
        }

    def _get_deprecation_week(self) -> int:
        """
        Determine current week in the 4-week deprecation timeline.

        Returns:
            Week number (1-4) in deprecation timeline
        """
        # Week 1: August 12-19, 2025
        deprecation_start = datetime(2025, 8, 12)
        now = datetime.now()
        days_since_start = (now - deprecation_start).days

        if days_since_start < 0:
            return 0  # Before deprecation starts
        elif days_since_start < 7:
            return 1  # Week 1: Parallel operation
        elif days_since_start < 14:
            return 2  # Week 2: Deprecation warnings
        elif days_since_start < 21:
            return 3  # Week 3: Legacy disabled by default
        elif days_since_start < 28:
            return 4  # Week 4: Legacy removal
        else:
            return 5  # Post-deprecation

    async def get_issue_by_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch GitHub issue by URL, raising exceptions on failure.

        Used by: domain/github_domain_service.py, integrations/github/issue_analyzer.py
        """
        return await self._get_integration("get_issue_by_url").get_issue_by_url(url)

    async def get_open_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get open issues from GitHub repository.

        Used by: domain/github_domain_service.py, domain/pm_number_manager.py
        """
        return await self._get_integration("get_open_issues").get_open_issues(project, limit)

    async def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent issues (both open and closed) from GitHub repository.

        Used by: domain/github_domain_service.py
        """
        return await self._get_integration("get_recent_issues").get_recent_issues(limit)

    async def get_recent_activity(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recent GitHub activity for standup (commits, PRs, issues).

        Used by: domain/standup_orchestration_service.py
        """
        return await self._get_integration("get_recent_activity").get_recent_activity(days)

    def list_repositories(self) -> List[Dict[str, Any]]:
        """
        List accessible repositories.

        Used by: domain/github_domain_service.py
        """
        return self._get_integration("list_repositories").list_repositories()

    async def create_issue_from_work_item(
        self, repo_name: str, work_item: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create GitHub issue from work item data.
        """
        return await self._get_integration(
            "create_issue_from_work_item"
        ).create_issue_from_work_item(repo_name, work_item)

    async def create_pm_issue(
        self,
        repo_name: str,
        pm_number: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create PM-specific GitHub issue."""
        return await self._get_integration("create_pm_issue").create_pm_issue(
            repo_name, pm_number, title, body, labels, assignees
        )

    async def get_closed_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get closed issues from GitHub repository.
        """
        return await self._get_integration("get_closed_issues").get_closed_issues(project, limit)

    async def get_issues_by_priority(self) -> List[Dict[str, Any]]:
        """
        Get GitHub issues organized by priority.
        """
        return await self._get_integration("get_issues_by_priority").get_issues_by_priority()

    async def get_development_context(self) -> Dict[str, Any]:
        """
        Get development context from GitHub.
        """
        return await self._get_integration("get_development_context").get_development_context()

    def parse_github_url(self, url: str) -> Optional[Tuple[str, str, int]]:
        """
        Parse GitHub issue URL to extract owner, repo, and issue number.
        """
        return self._get_integration("parse_github_url").parse_github_url(url)

    def test_connection(self) -> Dict[str, Any]:
        """
        Test GitHub connection and return status.
        """
        return self._get_integration("test_connection").test_connection()


# Convenience factory function
def create_github_integration() -> GitHubIntegrationRouter:
    """
    Create and initialize GitHub integration router.

    This is the primary entry point for all GitHub operations during the deprecation period.

    Returns:
        Configured GitHubIntegrationRouter instance
    """
    return GitHubIntegrationRouter()

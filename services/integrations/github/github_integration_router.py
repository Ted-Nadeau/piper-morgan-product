"""
GitHub Integration Router - MCP + Spatial Integration
PM-033b-deprecation: Week 4 Complete - Legacy Removed (CORE-INT #109)
CORE-MCP-MIGRATION #198: MCP Adapter Integration (October 17, 2025)

This router provides GitHub integration through:
- GitHubMCPSpatialAdapter (MCP protocol + spatial intelligence) - DEFAULT
- GitHubSpatialIntelligence (direct API + spatial intelligence) - FALLBACK

MCP Migration (CORE-MCP-MIGRATION #198):
- MCP adapter provides tool-based integration following Calendar pattern
- Feature flag USE_MCP_GITHUB controls MCP adapter usage (default: true)
- Graceful fallback to GitHubSpatialIntelligence if MCP unavailable

Deprecation timeline completed:
Week 1: ✅ Both integrations available, spatial default
Week 2: ✅ Deprecation warnings when legacy used
Week 3: ✅ Legacy disabled by default, emergency rollback available
Week 4: ✅ Legacy code removed (October 15, 2025)

Architecture Decision: ADR-013 MCP+Spatial Integration Pattern
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from services.infrastructure.config.feature_flags import FeatureFlags
from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence

from .config_service import GitHubConfigService

logger = logging.getLogger(__name__)


class GitHubIntegrationRouter:
    """
    Routes GitHub operations to MCP adapter or spatial intelligence.

    CORE-MCP-MIGRATION #198: Now supports GitHubMCPSpatialAdapter (tool-based MCP).
    Week 4 Complete (CORE-INT #109): Legacy code removed, spatial-only.

    Integration priority:
    1. GitHubMCPSpatialAdapter (if USE_MCP_GITHUB=true, default)
    2. GitHubSpatialIntelligence (fallback if MCP unavailable)

    ADAPTER PATTERN (ADR-013 Phase 2):
    - Router provides stable interface for consumers (get_recent_issues, get_issue, etc.)
    - Router delegates to MCP adapter using adapter methods
    - MCP adapter has different method names (list_github_issues_direct, get_github_issue_direct)
    - Adapter methods translate interface during migration period
    - Spatial intelligence used as fallback with direct method calls

    Follows service injection pattern (ADR-010) for configuration management.
    """

    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        """
        Initialize GitHub integration router with MCP adapter support and config service.

        Args:
            config_service: Optional GitHubConfigService for dependency injection.
                          If not provided, creates a default instance.
        """
        # Store config service (service injection pattern)
        self.config_service = config_service or GitHubConfigService()

        # MCP adapter (tool-based integration, CORE-MCP-MIGRATION #198)
        self.mcp_adapter = None

        # Spatial intelligence (fallback)
        self.spatial_github = None

        # Initialization tracking (for lazy initialization)
        self._initialized = False
        self._initialization_lock = None  # Will be set in async context

        # Feature flags
        self.use_mcp = self._get_boolean_flag("USE_MCP_GITHUB", True)
        self.allow_legacy = FeatureFlags.is_legacy_github_allowed()
        self.use_spatial = FeatureFlags.should_use_spatial_github()

        # Initialize integrations (MCP preferred, spatial fallback)
        self._initialize_integrations()

        logger.info(
            f"GitHubIntegrationRouter initialized - MCP: {self.mcp_adapter is not None}, Spatial: {self.spatial_github is not None}"
        )

    def _initialize_integrations(self):
        """
        Initialize GitHub integrations with MCP adapter priority.

        CORE-MCP-MIGRATION #198: Try MCP adapter first, fall back to spatial.
        """
        # Try MCP adapter first (if enabled)
        if self.use_mcp:
            try:
                from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

                self.mcp_adapter = GitHubMCPSpatialAdapter()
                logger.info("GitHubMCPSpatialAdapter initialized (token config pending)")
            except Exception as e:
                logger.warning(
                    f"Failed to initialize GitHubMCPSpatialAdapter: {e}, falling back to GitHubSpatialIntelligence"
                )
                self.mcp_adapter = None

        # Initialize spatial as fallback or primary (if MCP disabled)
        try:
            self.spatial_github = GitHubSpatialIntelligence()
            logger.info("GitHubSpatialIntelligence initialized successfully")
        except Exception as e:
            if not self.mcp_adapter:
                logger.error(f"Failed to initialize GitHubSpatialIntelligence: {e}")
                raise RuntimeError("No GitHub integration available") from e
            logger.warning(f"GitHubSpatialIntelligence failed, using MCP adapter only: {e}")

    async def initialize(self):
        """
        Initialize the GitHub integration asynchronously.

        Idempotent - safe to call multiple times (uses initialization lock).
        """
        # Skip if already initialized
        if self._initialized:
            return

        # Create lock if it doesn't exist (first async call)
        if self._initialization_lock is None:
            import asyncio

            self._initialization_lock = asyncio.Lock()

        # Use lock to prevent concurrent initialization
        async with self._initialization_lock:
            # Double-check after acquiring lock
            if self._initialized:
                return

            # Configure MCP adapter with GitHub token (async operation)
            if self.mcp_adapter:
                token = self.config_service.get_authentication_token()
                if token:
                    await self.mcp_adapter.configure_github_api(token)
                    logger.info("GitHubMCPSpatialAdapter configured with authentication token")
                else:
                    logger.warning("No GitHub authentication token available for MCP adapter")

            # Initialize spatial intelligence if available
            if self.spatial_github and hasattr(self.spatial_github, "initialize"):
                await self.spatial_github.initialize()

            # Mark as initialized
            self._initialized = True
            logger.info("GitHubIntegrationRouter initialization complete")

    def _get_integration(self, operation: str) -> Any:
        """
        Get the GitHub integration (MCP adapter preferred, spatial fallback).

        CORE-MCP-MIGRATION #198: Prefers MCP adapter when available.

        Args:
            operation: Operation name (for error messages)

        Returns:
            GitHubMCPSpatialAdapter or GitHubSpatialIntelligence instance

        Raises:
            RuntimeError: If no integration available
        """
        # Prefer MCP adapter if available
        if self.mcp_adapter:
            return self.mcp_adapter

        # Fall back to spatial intelligence
        if self.spatial_github:
            return self.spatial_github

        raise RuntimeError(f"No GitHub integration available for {operation}")

    async def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Get GitHub issue by repository and number.

        ADAPTER METHOD (ADR-013 Phase 2): Translates interface for MCP adapter.
        Uses lazy initialization to ensure GitHub token is loaded.
        """
        # Lazy initialization (ensures token loaded on first use)
        if not self._initialized:
            await self.initialize()

        # MCP adapter uses different method name and parameters
        if self.mcp_adapter:
            return await self.mcp_adapter.get_github_issue_direct(
                issue_number=str(issue_number),  # MCP adapter expects string
                repo=repo_name or "piper-morgan-product",
            )
        # Spatial fallback
        return await self.spatial_github.get_issue(repo_name, issue_number)

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
            "mcp_adapter_available": self.mcp_adapter is not None,
            "spatial_available": self.spatial_github is not None,
            "using_mcp": self.mcp_adapter is not None,
            "mcp_migration_complete": self.mcp_adapter is not None,
            "legacy_removed": True,
            "deprecation_timeline": {
                "week": self._get_deprecation_week(),
                "status": "Week 4 Complete - Legacy removed, MCP integrated",
                "legacy_removal_date": "2025-10-15",
                "mcp_integration_date": "2025-10-17",  # Today!
            },
        }

    def _get_boolean_flag(self, flag_name: str, default: bool = False) -> bool:
        """
        Get boolean environment variable with safe parsing.

        Supports: true/false, 1/0, yes/no, on/off

        Args:
            flag_name: Environment variable name
            default: Default value if not set

        Returns:
            Boolean value
        """
        try:
            value = os.getenv(flag_name, str(default)).lower().strip()
            return value in ("true", "1", "yes", "on", "enabled")
        except Exception:
            return default

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

        ADAPTER METHOD (ADR-013 Phase 2): Translates interface for MCP adapter.
        Uses lazy initialization to ensure GitHub token is loaded.
        """
        # Lazy initialization (ensures token loaded on first use)
        if not self._initialized:
            await self.initialize()

        # MCP adapter uses different method name and parameters
        if self.mcp_adapter:
            all_issues = await self.mcp_adapter.list_github_issues_direct()
            # Filter for open issues only and limit
            open_issues = [issue for issue in all_issues if issue.get("state") == "open"]
            return open_issues[:limit] if open_issues else []
        # Spatial fallback
        return await self.spatial_github.get_open_issues(project, limit)

    async def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent issues (both open and closed) from GitHub repository.

        Used by: domain/github_domain_service.py

        ADAPTER METHOD (ADR-013 Phase 2): Translates interface for MCP adapter.
        Uses lazy initialization to ensure GitHub token is loaded.
        """
        # Lazy initialization (ensures token loaded on first use)
        if not self._initialized:
            await self.initialize()

        # MCP adapter uses different method name and parameters
        if self.mcp_adapter:
            issues = await self.mcp_adapter.list_github_issues_direct()
            # Filter to limit (MCP adapter returns all, we limit here)
            return issues[:limit] if issues else []
        # Spatial fallback
        return await self.spatial_github.get_recent_issues(limit)

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

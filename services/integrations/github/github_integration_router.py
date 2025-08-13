"""
GitHub Integration Router - Deprecation Infrastructure
PM-033b-deprecation: Safe 4-week deprecation strategy implementation

This router provides feature flag-based switching between:
- GitHubSpatialIntelligence (8-dimensional spatial analysis - NEW DEFAULT)
- GitHubAgent (legacy direct API integration - BEING DEPRECATED)

During the 4-week deprecation timeline:
Week 1: Both integrations available, spatial default
Week 2: Deprecation warnings when legacy used
Week 3: Legacy disabled by default, emergency rollback available
Week 4: Legacy code removal

Architecture Decision: ADR-013 MCP+Spatial Integration Pattern
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from services.infrastructure.config.feature_flags import FeatureFlags
from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence

logger = logging.getLogger(__name__)


class GitHubIntegrationRouter:
    """
    Routes GitHub operations between spatial and legacy integrations based on feature flags.

    Provides safe deprecation infrastructure during the 4-week migration timeline
    with comprehensive fallback support and deprecation warnings.
    """

    def __init__(self):
        """Initialize GitHub integration router with feature flag detection"""
        self.spatial_github = None
        self.legacy_github = None

        # Feature flag state
        self.use_spatial = FeatureFlags.should_use_spatial_github()
        self.allow_legacy = FeatureFlags.is_legacy_github_allowed()
        self.warn_deprecation = FeatureFlags.should_warn_github_deprecation()

        # Initialize preferred integration
        self._initialize_integrations()

        logger.info(
            f"GitHubIntegrationRouter initialized - "
            f"Spatial: {self.use_spatial}, Legacy: {self.allow_legacy}, "
            f"Warnings: {self.warn_deprecation}"
        )

    def _initialize_integrations(self):
        """Initialize the appropriate GitHub integrations based on feature flags"""

        # Always initialize spatial integration (it's the future)
        if self.use_spatial:
            try:
                self.spatial_github = GitHubSpatialIntelligence()
                logger.info("GitHubSpatialIntelligence initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize GitHubSpatialIntelligence: {e}")
                if not self.allow_legacy:
                    raise RuntimeError("Spatial GitHub failed and legacy not allowed") from e

        # Initialize legacy integration if allowed
        if self.allow_legacy:
            try:
                # Import legacy GitHub agent dynamically to avoid dependency when not needed
                from services.integrations.github.github_agent import GitHubAgent

                self.legacy_github = GitHubAgent()
                logger.info("Legacy GitHubAgent initialized for fallback support")
            except Exception as e:
                logger.warning(f"Failed to initialize legacy GitHubAgent: {e}")
                if not self.use_spatial or self.spatial_github is None:
                    raise RuntimeError("Legacy GitHub failed and spatial not available") from e

    async def initialize(self):
        """Initialize the GitHub integrations asynchronously"""
        if self.spatial_github:
            await self.spatial_github.initialize()

        if self.legacy_github and hasattr(self.legacy_github, "initialize"):
            await self.legacy_github.initialize()

    def _warn_deprecation_if_needed(self, operation: str, used_legacy: bool):
        """Issue deprecation warnings when legacy integration is used"""
        if used_legacy and self.warn_deprecation:
            logger.warning(
                f"DEPRECATION WARNING: Legacy GitHub integration used for {operation}. "
                f"This will be removed in the upcoming release. "
                f"Please ensure spatial GitHub integration is working properly."
            )

    def _get_preferred_integration(self, operation: str) -> tuple[Any, bool]:
        """
        Get the preferred GitHub integration based on feature flags and availability.

        Returns:
            tuple: (integration_instance, is_legacy_used)
        """
        # Try spatial first if enabled
        if self.use_spatial and self.spatial_github:
            return self.spatial_github, False

        # Fall back to legacy if allowed and available
        if self.allow_legacy and self.legacy_github:
            logger.info(f"Falling back to legacy GitHub for {operation}")
            return self.legacy_github, True

        # No integration available
        raise RuntimeError(
            f"No GitHub integration available for {operation}. "
            f"Spatial: {self.spatial_github is not None}, "
            f"Legacy: {self.legacy_github is not None}"
        )

    async def get_issue(self, repository: str, issue_number: int) -> Optional[Dict[str, Any]]:
        """
        Get GitHub issue with spatial intelligence or legacy fallback.

        Args:
            repository: Repository name (e.g., "piper-morgan-product")
            issue_number: GitHub issue number

        Returns:
            Issue data with spatial intelligence if available, otherwise basic issue data
        """
        integration, is_legacy = self._get_preferred_integration("get_issue")
        self._warn_deprecation_if_needed("get_issue", is_legacy)

        try:
            if is_legacy:
                # Legacy integration - direct issue fetch
                return await integration.get_issue(repository, issue_number)
            else:
                # Spatial integration - enhanced with 8-dimensional analysis
                issue_data = await integration.get_issue(repository, issue_number)

                # Add spatial intelligence if we got valid issue data
                if issue_data:
                    spatial_context = await integration.create_spatial_context(issue_data)
                    issue_data["spatial_intelligence"] = {
                        "attention_level": spatial_context.attention_level,
                        "emotional_valence": spatial_context.emotional_valence,
                        "navigation_intent": spatial_context.navigation_intent,
                        "8_dimensional_analysis": spatial_context.external_context,
                    }

                return issue_data

        except Exception as e:
            logger.error(f"GitHub integration failed for get_issue: {e}")

            # Try fallback if available and different from what we tried
            if not is_legacy and self.allow_legacy and self.legacy_github:
                logger.info("Attempting legacy fallback for get_issue")
                self._warn_deprecation_if_needed("get_issue (fallback)", True)
                return await self.legacy_github.get_issue(repository, issue_number)

            raise

    async def list_issues(self, repository: str, **kwargs) -> List[Dict[str, Any]]:
        """
        List GitHub issues with spatial intelligence or legacy fallback.

        Args:
            repository: Repository name
            **kwargs: Additional filtering parameters

        Returns:
            List of issues with spatial intelligence if available
        """
        integration, is_legacy = self._get_preferred_integration("list_issues")
        self._warn_deprecation_if_needed("list_issues", is_legacy)

        try:
            if is_legacy:
                # Legacy integration - basic issue list
                return await integration.list_issues(repository, **kwargs)
            else:
                # Spatial integration - enhanced with context analysis
                issues = await integration.list_issues(repository, **kwargs)

                # Add spatial intelligence to each issue
                enhanced_issues = []
                for issue in issues:
                    try:
                        spatial_context = await integration.create_spatial_context(issue)
                        issue["spatial_intelligence"] = {
                            "attention_level": spatial_context.attention_level,
                            "emotional_valence": spatial_context.emotional_valence,
                            "navigation_intent": spatial_context.navigation_intent,
                        }
                        enhanced_issues.append(issue)
                    except Exception as spatial_error:
                        logger.warning(
                            f"Spatial analysis failed for issue {issue.get('number')}: {spatial_error}"
                        )
                        enhanced_issues.append(issue)  # Include without spatial intelligence

                return enhanced_issues

        except Exception as e:
            logger.error(f"GitHub integration failed for list_issues: {e}")

            # Try fallback if available
            if not is_legacy and self.allow_legacy and self.legacy_github:
                logger.info("Attempting legacy fallback for list_issues")
                self._warn_deprecation_if_needed("list_issues (fallback)", True)
                return await self.legacy_github.list_issues(repository, **kwargs)

            raise

    async def create_issue(
        self, repository: str, title: str, body: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Create GitHub issue using available integration.

        Args:
            repository: Repository name
            title: Issue title
            body: Issue body
            **kwargs: Additional issue parameters (labels, assignees, etc.)

        Returns:
            Created issue data
        """
        integration, is_legacy = self._get_preferred_integration("create_issue")
        self._warn_deprecation_if_needed("create_issue", is_legacy)

        try:
            created_issue = await integration.create_issue(repository, title, body, **kwargs)

            # Add spatial analysis for the newly created issue if using spatial integration
            if not is_legacy and created_issue:
                try:
                    spatial_context = await integration.create_spatial_context(created_issue)
                    created_issue["spatial_intelligence"] = {
                        "attention_level": spatial_context.attention_level,
                        "emotional_valence": spatial_context.emotional_valence,
                        "navigation_intent": spatial_context.navigation_intent,
                    }
                except Exception as spatial_error:
                    logger.warning(f"Spatial analysis failed for created issue: {spatial_error}")

            return created_issue

        except Exception as e:
            logger.error(f"GitHub integration failed for create_issue: {e}")

            # Try fallback if available
            if not is_legacy and self.allow_legacy and self.legacy_github:
                logger.info("Attempting legacy fallback for create_issue")
                self._warn_deprecation_if_needed("create_issue (fallback)", True)
                return await self.legacy_github.create_issue(repository, title, body, **kwargs)

            raise

    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get current integration status for monitoring and debugging.

        Returns:
            Status information about current GitHub integrations
        """
        return {
            "router_initialized": True,
            "feature_flags": {
                "use_spatial": self.use_spatial,
                "allow_legacy": self.allow_legacy,
                "warn_deprecation": self.warn_deprecation,
            },
            "integrations": {
                "spatial_available": self.spatial_github is not None,
                "legacy_available": self.legacy_github is not None,
            },
            "preferred_integration": (
                "spatial" if self.use_spatial and self.spatial_github else "legacy"
            ),
            "deprecation_timeline": {
                "week": self._get_deprecation_week(),
                "legacy_removal_date": "2025-09-09",  # Week 4 target
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


# Convenience factory function
def create_github_integration() -> GitHubIntegrationRouter:
    """
    Create and initialize GitHub integration router.

    This is the primary entry point for all GitHub operations during the deprecation period.

    Returns:
        Configured GitHubIntegrationRouter instance
    """
    return GitHubIntegrationRouter()

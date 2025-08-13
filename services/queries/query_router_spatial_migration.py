"""
QueryRouter Migration to GitHub Spatial Intelligence
Following ADR-013: MCP + Spatial Intelligence Pattern

This module provides a migration path for QueryRouter to use
GitHubSpatialIntelligence instead of direct MCP adapter.
"""

import logging
from typing import Any, Dict, Optional

from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence

logger = logging.getLogger(__name__)


class QueryRouterSpatialEnhancement:
    """Enhancement layer for QueryRouter to use spatial GitHub intelligence"""

    def __init__(self, query_router):
        """Initialize with existing QueryRouter instance"""
        self.query_router = query_router
        self.github_spatial = None

        # Replace GitHub adapter with spatial intelligence
        if self.query_router.enable_mcp_federation:
            self._upgrade_to_spatial()

    def _upgrade_to_spatial(self):
        """Upgrade GitHub integration to spatial intelligence"""
        try:
            # Create spatial intelligence instance
            self.github_spatial = GitHubSpatialIntelligence()

            # Store original adapter for backward compatibility
            self.original_adapter = self.query_router.github_adapter

            # Replace with spatial-aware adapter
            self.query_router.github_adapter = self.github_spatial.mcp_adapter

            logger.info("QueryRouter upgraded to GitHub Spatial Intelligence")

        except Exception as e:
            logger.error(f"Failed to upgrade to spatial GitHub: {e}")

    async def federated_search_with_spatial(self, query: str) -> Dict[str, Any]:
        """
        Enhanced federated search with 8-dimensional spatial analysis
        """
        # Get basic results from original federated search
        results = await self.query_router.federated_search(query)

        # Enhance GitHub results with spatial intelligence
        if self.github_spatial and results.get("github_results"):
            enhanced_results = []

            for issue_data in results["github_results"]:
                try:
                    # Create full issue object (simplified for demo)
                    issue = {
                        "number": issue_data["number"],
                        "title": issue_data["title"],
                        "body": issue_data.get("description", ""),
                        "state": issue_data.get("state", "open"),
                        "created_at": issue_data.get("created_at", "2025-08-12T00:00:00Z"),
                        "updated_at": issue_data.get("updated_at", "2025-08-12T00:00:00Z"),
                        "labels": issue_data.get("labels", []),
                        "assignees": issue_data.get("assignees", []),
                        "milestone": issue_data.get("milestone"),
                        "comments": issue_data.get("comments", 0),
                        "reactions": {"total_count": 0},
                        "repository": {"owner": "mediajunkie", "name": "piper-morgan-product"},
                    }

                    # Create spatial context with 8-dimensional analysis
                    spatial_context = await self.github_spatial.create_spatial_context(issue)

                    # Add spatial intelligence to result
                    issue_data["spatial_intelligence"] = {
                        "attention_level": spatial_context.attention_level,
                        "emotional_valence": spatial_context.emotional_valence,
                        "navigation_intent": spatial_context.navigation_intent,
                        "dimensions": spatial_context.external_context,
                    }

                    enhanced_results.append(issue_data)

                except Exception as e:
                    logger.warning(
                        f"Failed to enhance issue {issue_data.get('number')} with spatial: {e}"
                    )
                    enhanced_results.append(issue_data)  # Keep original if enhancement fails

            results["github_results"] = enhanced_results
            results["spatial_enhanced"] = True

            logger.info(
                f"Enhanced {len(enhanced_results)} GitHub results with spatial intelligence"
            )

        return results


def migrate_query_router_to_spatial(query_router) -> QueryRouterSpatialEnhancement:
    """
    Migration function to upgrade QueryRouter to spatial intelligence

    Usage:
        from services.queries.query_router import QueryRouter
        from services.queries.query_router_spatial_migration import migrate_query_router_to_spatial

        router = QueryRouter(...)
        spatial_router = migrate_query_router_to_spatial(router)

        # Use enhanced federated search
        results = await spatial_router.federated_search_with_spatial("high priority bugs")
    """
    return QueryRouterSpatialEnhancement(query_router)

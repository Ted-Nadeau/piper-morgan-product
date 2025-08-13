"""
MCP+Spatial Federation Integration Tests
Phase 4: Comprehensive testing of GitHub + Notion federation with 8-dimensional consistency

Tests ADR-013: MCP + Spatial Intelligence Pattern across multiple external tools
"""

import asyncio
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence
from services.integrations.spatial_adapter import SpatialContext, SpatialPosition
from services.queries.query_router import QueryRouter
from services.queries.query_router_spatial_migration import migrate_query_router_to_spatial


class TestMCPSpatialFederation:
    """
    Comprehensive integration tests for MCP+Spatial pattern federation
    Tests dual-tool integration (GitHub + Notion) with dimensional consistency
    """

    @pytest.fixture
    async def github_spatial(self):
        """GitHub spatial intelligence instance"""
        spatial = GitHubSpatialIntelligence()

        # Mock MCP adapter to avoid external API calls
        spatial.mcp_adapter = AsyncMock()
        spatial.mcp_adapter.configure_github_api = AsyncMock()
        spatial.mcp_adapter.map_to_position = AsyncMock(
            return_value=SpatialPosition(x=1.0, y=2.0, z=3.0, position=123)
        )

        await spatial.initialize()
        return spatial

    @pytest.fixture
    def mock_query_router(self):
        """Mock QueryRouter with MCP federation enabled"""
        router = MagicMock()
        router.enable_mcp_federation = True
        router.github_adapter = AsyncMock()
        router.federated_search = AsyncMock()
        return router

    @pytest.fixture
    def sample_github_issues(self):
        """Sample GitHub issues for federation testing"""
        return [
            {
                "number": 85,
                "title": "Login authentication bug - critical production issue",
                "state": "open",
                "created_at": "2025-08-10T10:00:00Z",
                "updated_at": "2025-08-12T12:00:00Z",
                "labels": [{"name": "bug"}, {"name": "critical"}, {"name": "P0-critical"}],
                "assignees": [{"login": "john_doe"}, {"login": "jane_smith"}],
                "milestone": {"title": "Sprint 23", "due_on": "2025-08-15T00:00:00Z"},
                "comments": 12,
                "reactions": {"total_count": 5},
                "repository": {"owner": "mediajunkie", "name": "piper-morgan-product"},
                "body": "Critical auth bug blocking users. Related to #82, blocks #87",
            },
            {
                "number": 156,
                "title": "User dashboard performance improvements",
                "state": "open",
                "created_at": "2025-08-11T14:00:00Z",
                "updated_at": "2025-08-12T09:00:00Z",
                "labels": [{"name": "enhancement"}, {"name": "performance"}, {"name": "P1"}],
                "assignees": [{"login": "alex_dev"}],
                "milestone": {"title": "Q3 Goals", "due_on": "2025-09-30T00:00:00Z"},
                "comments": 3,
                "reactions": {"total_count": 2},
                "repository": {"owner": "mediajunkie", "name": "piper-morgan-ui"},
                "body": "Dashboard loading slowly, need optimization. See performance report in #150",
            },
        ]

    @pytest.fixture
    def sample_notion_pages(self):
        """Sample Notion pages for federation testing"""
        return [
            {
                "id": "page-123",
                "title": "Q3 Product Roadmap",
                "created_at": "2025-08-01T00:00:00Z",
                "updated_at": "2025-08-12T10:00:00Z",
                "status": "In Progress",
                "priority": "High",
                "assignees": ["product_manager", "tech_lead"],
                "tags": ["roadmap", "Q3", "planning"],
                "content_type": "roadmap",
                "parent": {"database_id": "roadmap-db"},
                "properties": {
                    "Status": {"select": {"name": "In Progress"}},
                    "Priority": {"select": {"name": "High"}},
                    "Quarter": {"select": {"name": "Q3 2025"}},
                },
            },
            {
                "id": "page-456",
                "title": "Authentication Architecture Review",
                "created_at": "2025-08-10T15:00:00Z",
                "updated_at": "2025-08-12T11:30:00Z",
                "status": "Complete",
                "priority": "Critical",
                "assignees": ["architect", "security_lead"],
                "tags": ["security", "architecture", "auth"],
                "content_type": "technical_doc",
                "parent": {"database_id": "tech-docs-db"},
                "properties": {
                    "Status": {"select": {"name": "Complete"}},
                    "Priority": {"select": {"name": "Critical"}},
                    "Type": {"select": {"name": "Architecture"}},
                },
            },
        ]

    # TEST 1: Federated Search with Spatial Enhancement
    @pytest.mark.asyncio
    async def test_federated_search_spatial_enhancement(
        self, github_spatial, mock_query_router, sample_github_issues
    ):
        """Test federated search enhanced with spatial intelligence"""

        # Setup mock federated search response
        mock_query_router.federated_search.return_value = {
            "github_results": sample_github_issues,
            "total_results": 2,
            "query": "authentication bug",
            "sources": ["github"],
        }

        # Create spatial enhancement layer
        spatial_router = migrate_query_router_to_spatial(mock_query_router)

        # Test enhanced federated search
        start_time = time.time()
        results = await spatial_router.federated_search_with_spatial("authentication bug")
        elapsed_ms = (time.time() - start_time) * 1000

        # Verify performance target (<150ms)
        assert elapsed_ms < 150, f"Federation took {elapsed_ms:.2f}ms (target: <150ms)"

        # Verify spatial enhancement applied
        assert "spatial_enhanced" in results
        assert results["spatial_enhanced"] == True
        assert len(results["github_results"]) == 2

        # Verify each result has spatial intelligence
        for result in results["github_results"]:
            assert "spatial_intelligence" in result

            spatial_data = result["spatial_intelligence"]
            assert "attention_level" in spatial_data
            assert "emotional_valence" in spatial_data
            assert "navigation_intent" in spatial_data
            assert "dimensions" in spatial_data

            # Verify all 8 dimensions present
            dimensions = spatial_data["dimensions"]
            expected_dimensions = [
                "hierarchy",
                "temporal",
                "priority",
                "collaborative",
                "flow",
                "quantitative",
                "causal",
                "contextual",
            ]
            for dim in expected_dimensions:
                assert dim in dimensions, f"Missing dimension: {dim}"

    # TEST 2: Cross-Tool Dimensional Consistency
    @pytest.mark.asyncio
    async def test_cross_tool_dimensional_consistency(
        self, github_spatial, sample_github_issues, sample_notion_pages
    ):
        """Verify 8-dimensional analysis consistency across GitHub + Notion"""

        github_issue = sample_github_issues[0]  # Critical auth bug
        notion_page = sample_notion_pages[1]  # Auth architecture doc

        # Analyze GitHub issue with all 8 dimensions
        github_context = await github_spatial.create_spatial_context(github_issue)

        # Mock Notion spatial analysis (would be similar structure)
        notion_context = SpatialContext(
            territory_id="notion",
            room_id="tech-docs-db",
            path_id="pages/page-456",
            attention_level="urgent",  # Critical priority
            emotional_valence="neutral",  # Technical doc
            navigation_intent="reference",  # Documentation
            external_system="notion",
            external_id="page-456",
            external_context={
                "hierarchy": {"type": "document", "level": "root", "depth": 0},
                "temporal": {"age_days": 2, "activity_level": "recent", "urgency": "high"},
                "priority": {"priority_level": "critical", "assigned": True},
                "collaborative": {"assignee_count": 2, "engagement_level": "high"},
                "flow": {"status": "complete", "workflow_stage": "completed"},
                "quantitative": {"complexity_estimate": "high", "engagement_score": 15},
                "causal": {"related_issues": [85], "dependency_chain_length": 1},
                "contextual": {"domain": "technical_documentation", "database": "tech-docs"},
            },
        )

        # Verify dimensional consistency between tools
        github_dims = github_context.external_context
        notion_dims = notion_context.external_context

        # Both should have all 8 dimensions
        expected_dimensions = [
            "hierarchy",
            "temporal",
            "priority",
            "collaborative",
            "flow",
            "quantitative",
            "causal",
            "contextual",
        ]

        for dim in expected_dimensions:
            assert dim in github_dims, f"GitHub missing dimension: {dim}"
            assert dim in notion_dims, f"Notion missing dimension: {dim}"

        # Verify related issue connection (causal dimension)
        github_causal = github_dims["causal"]
        notion_causal = notion_dims["causal"]

        # The auth architecture doc should relate to the auth bug
        assert 82 in github_causal.get("related_issues", [])  # GitHub issue references
        assert 85 in notion_causal.get("related_issues", [])  # Notion doc references GitHub

    # TEST 3: Multi-Tool Query Routing Performance
    @pytest.mark.asyncio
    async def test_multi_tool_query_routing_performance(
        self, github_spatial, mock_query_router, sample_github_issues, sample_notion_pages
    ):
        """Test performance of routing queries across multiple MCP+Spatial tools"""

        # Mock responses from both GitHub and Notion
        mock_query_router.federated_search.return_value = {
            "github_results": sample_github_issues,
            "notion_results": sample_notion_pages,
            "total_results": 4,
            "query": "authentication security",
            "sources": ["github", "notion"],
        }

        spatial_router = migrate_query_router_to_spatial(mock_query_router)

        # Test multiple queries for performance profiling
        query_scenarios = [
            "authentication bug critical",
            "performance dashboard optimization",
            "Q3 roadmap planning",
            "security architecture review",
        ]

        total_time = 0
        successful_queries = 0

        for query in query_scenarios:
            start_time = time.time()

            try:
                results = await spatial_router.federated_search_with_spatial(query)
                elapsed_ms = (time.time() - start_time) * 1000
                total_time += elapsed_ms

                # Verify spatial enhancement applied
                assert results.get("spatial_enhanced") == True
                assert "github_results" in results

                successful_queries += 1

                # Each query should complete in <150ms
                assert elapsed_ms < 150, f"Query '{query}' took {elapsed_ms:.2f}ms"

            except Exception as e:
                pytest.fail(f"Query '{query}' failed: {e}")

        # Verify overall performance
        avg_time = total_time / len(query_scenarios)
        assert avg_time < 150, f"Average query time {avg_time:.2f}ms exceeds 150ms target"
        assert successful_queries == len(query_scenarios)

    # TEST 4: Spatial Context Attention Scoring
    @pytest.mark.asyncio
    async def test_spatial_attention_scoring_consistency(
        self, github_spatial, sample_github_issues
    ):
        """Test attention scoring consistency across issues with different priorities"""

        critical_issue = sample_github_issues[0]  # Critical P0 bug
        feature_issue = sample_github_issues[1]  # P1 enhancement

        # Analyze both issues
        critical_context = await github_spatial.create_spatial_context(critical_issue)
        feature_context = await github_spatial.create_spatial_context(feature_issue)

        # Critical issue should have higher attention
        assert critical_context.attention_level == "urgent"
        assert feature_context.attention_level in ["high", "medium"]

        # Verify attention scoring in priority dimension
        critical_priority = critical_context.external_context["priority"]
        feature_priority = feature_context.external_context["priority"]

        assert critical_priority["attention_score"] > feature_priority["attention_score"]
        assert critical_priority["priority_level"] == "critical"
        assert feature_priority["priority_level"] in ["high", "normal"]

    # TEST 5: QueryRouter Integration Backward Compatibility
    @pytest.mark.asyncio
    async def test_query_router_backward_compatibility(
        self, github_spatial, mock_query_router, sample_github_issues
    ):
        """Ensure spatial enhancement doesn't break existing QueryRouter functionality"""

        # Setup original federated search
        original_results = {
            "github_results": sample_github_issues,
            "total_results": 2,
            "query": "test query",
            "sources": ["github"],
        }
        mock_query_router.federated_search.return_value = original_results

        # Create spatial enhancement
        spatial_router = migrate_query_router_to_spatial(mock_query_router)

        # Test that original federated_search still works
        basic_results = await mock_query_router.federated_search("test query")
        assert basic_results == original_results

        # Test that enhanced search adds spatial intelligence without removing original data
        enhanced_results = await spatial_router.federated_search_with_spatial("test query")

        # Should have all original data
        assert enhanced_results["total_results"] == original_results["total_results"]
        assert enhanced_results["query"] == original_results["query"]
        assert enhanced_results["sources"] == original_results["sources"]

        # Plus spatial enhancements
        assert enhanced_results["spatial_enhanced"] == True

        # Original results preserved but enhanced
        for i, result in enumerate(enhanced_results["github_results"]):
            original = original_results["github_results"][i]

            # All original fields preserved
            assert result["number"] == original["number"]
            assert result["title"] == original["title"]
            assert result["state"] == original["state"]

            # Spatial intelligence added
            assert "spatial_intelligence" in result

    # TEST 6: Error Handling and Graceful Degradation
    @pytest.mark.asyncio
    async def test_spatial_error_handling_graceful_degradation(
        self, github_spatial, mock_query_router, sample_github_issues
    ):
        """Test that spatial enhancement fails gracefully without breaking federation"""

        mock_query_router.federated_search.return_value = {
            "github_results": sample_github_issues,
            "total_results": 2,
            "sources": ["github"],
        }

        spatial_router = migrate_query_router_to_spatial(mock_query_router)

        # Mock spatial enhancement failure
        with patch.object(github_spatial, "create_spatial_context") as mock_spatial:
            mock_spatial.side_effect = Exception("Spatial analysis failed")

            # Should still return results without spatial enhancement
            results = await spatial_router.federated_search_with_spatial("test query")

            # Basic federation should still work
            assert len(results["github_results"]) == 2
            assert results["total_results"] == 2

            # Spatial enhancement should be marked as failed/skipped
            assert "spatial_enhanced" not in results or results["spatial_enhanced"] == False

            # Original issue data should be preserved
            for result in results["github_results"]:
                assert "number" in result
                assert "title" in result
                # Should NOT have spatial_intelligence due to failure
                assert "spatial_intelligence" not in result

    # TEST 7: Full End-to-End Federation Workflow
    @pytest.mark.asyncio
    async def test_end_to_end_federation_workflow(
        self, github_spatial, mock_query_router, sample_github_issues, sample_notion_pages
    ):
        """Complete end-to-end test of MCP+Spatial federation workflow"""

        # Setup comprehensive federated response
        mock_query_router.federated_search.return_value = {
            "github_results": sample_github_issues,
            "notion_results": sample_notion_pages,
            "total_results": 4,
            "query": "authentication security architecture",
            "sources": ["github", "notion"],
            "execution_time_ms": 89,
            "cache_hit": False,
        }

        spatial_router = migrate_query_router_to_spatial(mock_query_router)

        # Execute full workflow
        start_time = time.time()
        results = await spatial_router.federated_search_with_spatial(
            "authentication security architecture"
        )
        total_time_ms = (time.time() - start_time) * 1000

        # Verify complete workflow success
        assert results["total_results"] == 4
        assert "github_results" in results
        assert "notion_results" in results  # Notion results pass through unchanged
        assert results["spatial_enhanced"] == True

        # Verify performance (including spatial enhancement)
        assert total_time_ms < 150, f"E2E workflow took {total_time_ms:.2f}ms"

        # Verify GitHub results enhanced with spatial intelligence
        for github_result in results["github_results"]:
            assert "spatial_intelligence" in github_result
            spatial = github_result["spatial_intelligence"]

            # Verify attention scoring
            assert "attention_level" in spatial
            assert spatial["attention_level"] in ["low", "medium", "high", "urgent"]

            # Verify emotional valence
            assert "emotional_valence" in spatial
            assert spatial["emotional_valence"] in ["negative", "neutral", "positive"]

            # Verify navigation intent
            assert "navigation_intent" in spatial
            assert spatial["navigation_intent"] in ["explore", "investigate", "respond", "monitor"]

            # Verify 8-dimensional data
            dimensions = spatial["dimensions"]
            expected_dims = [
                "hierarchy",
                "temporal",
                "priority",
                "collaborative",
                "flow",
                "quantitative",
                "causal",
                "contextual",
            ]
            for dim in expected_dims:
                assert dim in dimensions

        # Verify Notion results pass through (no spatial enhancement yet)
        # This demonstrates extensibility - Notion would get similar treatment
        for notion_result in results["notion_results"]:
            assert "id" in notion_result
            assert "title" in notion_result
            # Notion spatial intelligence would be added in future phase

    # TEST 8: Performance Benchmarking
    @pytest.mark.asyncio
    async def test_performance_benchmarking(
        self, github_spatial, mock_query_router, sample_github_issues
    ):
        """Benchmark spatial enhancement performance impact"""

        mock_query_router.federated_search.return_value = {
            "github_results": sample_github_issues * 10,  # 20 issues for load testing
            "total_results": 20,
            "sources": ["github"],
        }

        spatial_router = migrate_query_router_to_spatial(mock_query_router)

        # Benchmark enhanced federation
        benchmark_runs = []

        for i in range(5):  # 5 benchmark runs
            start = time.time()
            results = await spatial_router.federated_search_with_spatial("benchmark test")
            elapsed_ms = (time.time() - start) * 1000
            benchmark_runs.append(elapsed_ms)

            # Verify all 20 results enhanced
            assert len(results["github_results"]) == 20
            assert results["spatial_enhanced"] == True

            enhanced_count = sum(
                1 for r in results["github_results"] if "spatial_intelligence" in r
            )
            assert enhanced_count == 20

        # Analyze performance
        avg_time = sum(benchmark_runs) / len(benchmark_runs)
        max_time = max(benchmark_runs)
        min_time = min(benchmark_runs)

        # Performance assertions
        assert avg_time < 150, f"Average time {avg_time:.2f}ms exceeds target"
        assert max_time < 200, f"Max time {max_time:.2f}ms too slow"
        assert min_time > 0, "Minimum time should be positive"

        # Log performance metrics for monitoring
        print(f"\n🏃‍♂️ Spatial Federation Benchmark:")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Min: {min_time:.2f}ms")
        print(f"   Max: {max_time:.2f}ms")
        print(f"   Target: <150ms ✅" if avg_time < 150 else f"   Target: <150ms ❌")

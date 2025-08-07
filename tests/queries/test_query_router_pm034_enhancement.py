"""
PM-034 Phase 2B: QueryRouter Enhancement Tests

Tests for the enhanced QueryRouter with LLM intent classification,
performance monitoring, and A/B testing capabilities.
"""

import time
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.llm_classifier import LLMIntentClassifier
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.semantic_indexing_service import SemanticIndexingService
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.queries.query_router import QueryRouter
from services.shared_types import IntentCategory


class TestQueryRouterPM034Enhancement:
    """Test suite for PM-034 Phase 2B QueryRouter enhancements"""

    @pytest.fixture
    def mock_services(self):
        """Create mock services for testing"""
        return {
            "project_queries": AsyncMock(spec=ProjectQueryService),
            "conversation_queries": AsyncMock(spec=ConversationQueryService),
            "file_queries": AsyncMock(spec=FileQueryService),
        }

    @pytest.fixture
    def mock_llm_classifier(self):
        """Create mock LLM classifier"""
        classifier = AsyncMock(spec=LLMIntentClassifier)
        classifier.classify = AsyncMock()
        return classifier

    @pytest.fixture
    def mock_knowledge_graph_service(self):
        """Create mock knowledge graph service"""
        return AsyncMock(spec=KnowledgeGraphService)

    @pytest.fixture
    def mock_semantic_indexing_service(self):
        """Create mock semantic indexing service"""
        return AsyncMock(spec=SemanticIndexingService)

    @pytest.fixture
    def query_router_basic(self, mock_services):
        """Create basic QueryRouter without LLM enhancement"""
        return QueryRouter(
            project_query_service=mock_services["project_queries"],
            conversation_query_service=mock_services["conversation_queries"],
            file_query_service=mock_services["file_queries"],
            test_mode=False,
        )

    @pytest.fixture
    def query_router_enhanced(
        self,
        mock_services,
        mock_llm_classifier,
        mock_knowledge_graph_service,
        mock_semantic_indexing_service,
    ):
        """Create enhanced QueryRouter with LLM classification"""
        return QueryRouter(
            project_query_service=mock_services["project_queries"],
            conversation_query_service=mock_services["conversation_queries"],
            file_query_service=mock_services["file_queries"],
            test_mode=False,
            llm_classifier=mock_llm_classifier,
            knowledge_graph_service=mock_knowledge_graph_service,
            semantic_indexing_service=mock_semantic_indexing_service,
            enable_llm_classification=True,
            llm_rollout_percentage=0.5,  # 50% rollout
        )

    def test_enhanced_router_initialization(self, query_router_enhanced):
        """Test enhanced QueryRouter initialization with LLM components"""
        assert query_router_enhanced.llm_classifier is not None
        assert query_router_enhanced.knowledge_graph_service is not None
        assert query_router_enhanced.semantic_indexing_service is not None
        assert query_router_enhanced.enable_llm_classification is True
        assert query_router_enhanced.llm_rollout_percentage == 0.5
        assert query_router_enhanced.performance_targets["rule_based"] == 50.0
        assert query_router_enhanced.performance_targets["llm_classification"] == 200.0

    def test_performance_metrics_initialization(self, query_router_enhanced):
        """Test performance metrics are properly initialized"""
        metrics = query_router_enhanced.performance_metrics
        assert metrics["total_requests"] == 0
        assert metrics["llm_classifications"] == 0
        assert metrics["rule_based_classifications"] == 0
        assert metrics["llm_success_rate"] == 0.0
        assert metrics["rule_based_success_rate"] == 0.0
        assert metrics["average_llm_latency_ms"] == 0.0
        assert metrics["average_rule_based_latency_ms"] == 0.0
        assert metrics["target_violations"] == 0

    def test_ab_testing_logic_with_session_id(self, query_router_enhanced):
        """Test A/B testing logic with session-based consistency"""
        # Test with 50% rollout
        session_id = "test_session_123"

        # Should be consistent for same session
        result1 = query_router_enhanced._should_use_llm_classification(session_id)
        result2 = query_router_enhanced._should_use_llm_classification(session_id)
        assert result1 == result2  # Consistent assignment

        # Different sessions may have different assignments
        different_session = "test_session_456"
        result3 = query_router_enhanced._should_use_llm_classification(different_session)
        # Note: May be same or different due to hash distribution

    def test_ab_testing_logic_without_session_id(self, query_router_enhanced):
        """Test A/B testing logic without session ID (random assignment)"""
        # With 50% rollout, should be approximately 50% chance
        results = []
        for _ in range(100):
            result = query_router_enhanced._should_use_llm_classification()
            results.append(result)

        # Should have some True and some False (not all same)
        assert any(results) and not all(results)

    def test_ab_testing_disabled(self, query_router_enhanced):
        """Test A/B testing when LLM classification is disabled"""
        query_router_enhanced.enable_llm_classification = False
        assert query_router_enhanced._should_use_llm_classification("test_session") is False

    def test_ab_testing_zero_rollout(self, query_router_enhanced):
        """Test A/B testing with 0% rollout"""
        query_router_enhanced.llm_rollout_percentage = 0.0
        assert query_router_enhanced._should_use_llm_classification("test_session") is False

    def test_ab_testing_full_rollout(self, query_router_enhanced):
        """Test A/B testing with 100% rollout"""
        query_router_enhanced.llm_rollout_percentage = 1.0
        assert query_router_enhanced._should_use_llm_classification("test_session") is True

    def test_rule_based_classification_project_queries(self, query_router_enhanced):
        """Test rule-based classification for project queries"""
        # Test list projects
        intent = query_router_enhanced._rule_based_classification(
            "list all projects", {}, "test_session"
        )
        assert intent.action == "list_projects"
        assert intent.confidence == 0.9
        assert intent.context["rule_based"] is True

        # Test find project
        intent = query_router_enhanced._rule_based_classification(
            "find project alpha", {}, "test_session"
        )
        assert intent.action == "find_project"
        assert intent.confidence == 0.8
        assert intent.context["rule_based"] is True

    def test_rule_based_classification_file_queries(self, query_router_enhanced):
        """Test rule-based classification for file queries"""
        # Test search files
        intent = query_router_enhanced._rule_based_classification(
            "search for documents about API", {}, "test_session"
        )
        assert intent.action == "search_files"
        assert intent.confidence == 0.85
        assert intent.context["rule_based"] is True
        assert intent.context["search_query"] == "search for documents about API"

        # Test read file
        intent = query_router_enhanced._rule_based_classification(
            "read file contents", {}, "test_session"
        )
        assert intent.action == "read_file_contents"
        assert intent.confidence == 0.8
        assert intent.context["rule_based"] is True

    def test_rule_based_classification_conversation_queries(self, query_router_enhanced):
        """Test rule-based classification for conversation queries"""
        # Test greeting
        intent = query_router_enhanced._rule_based_classification("hello there", {}, "test_session")
        assert intent.action == "get_greeting"
        assert intent.confidence == 0.95
        assert intent.context["rule_based"] is True

        # Test help
        intent = query_router_enhanced._rule_based_classification(
            "help me please", {}, "test_session"
        )
        assert intent.action == "get_help"
        assert intent.confidence == 0.9
        assert intent.context["rule_based"] is True

    def test_rule_based_classification_fallback(self, query_router_enhanced):
        """Test rule-based classification fallback for unknown patterns"""
        intent = query_router_enhanced._rule_based_classification(
            "random unknown message", {}, "test_session"
        )
        assert intent.action == "get_help"  # Safe fallback
        assert intent.confidence == 0.5
        assert intent.context["rule_based"] is True
        assert intent.context["fallback"] is True

    @pytest.mark.asyncio
    async def test_classify_and_route_llm_success(self, query_router_enhanced, mock_llm_classifier):
        """Test successful LLM classification and routing"""
        # Mock LLM classifier to return a valid intent
        mock_intent = Intent(
            message="test message",
            category=IntentCategory.QUERY,
            action="list_projects",
            confidence=0.85,
            context={"llm_classified": True},
        )
        mock_llm_classifier.classify.return_value = mock_intent

        # Mock project queries response
        query_router_enhanced.project_queries.list_active_projects.return_value = [
            "project1",
            "project2",
        ]

        # Test classification and routing
        result = await query_router_enhanced.classify_and_route(
            "show me all projects", {}, "test_session"
        )

        # Verify LLM classifier was called
        mock_llm_classifier.classify.assert_called_once()

        # Verify metrics were updated
        metrics = query_router_enhanced.performance_metrics
        assert metrics["total_requests"] == 1
        assert metrics["llm_classifications"] == 1
        assert metrics["rule_based_classifications"] == 0

    @pytest.mark.asyncio
    async def test_classify_and_route_rule_based_success(self, query_router_enhanced):
        """Test successful rule-based classification and routing"""
        # Mock conversation queries response
        query_router_enhanced.conversation_queries.get_greeting.return_value = (
            "Hello! How can I help you?"
        )

        # Test classification and routing
        result = await query_router_enhanced.classify_and_route("hello there", {}, "test_session")

        # Verify metrics were updated
        metrics = query_router_enhanced.performance_metrics
        assert metrics["total_requests"] == 1
        assert metrics["llm_classifications"] == 0
        assert metrics["rule_based_classifications"] == 1

    @pytest.mark.asyncio
    async def test_classify_and_route_llm_failure_fallback(
        self, query_router_enhanced, mock_llm_classifier
    ):
        """Test LLM classification failure with fallback to rule-based"""
        # Mock LLM classifier to raise an exception
        mock_llm_classifier.classify.side_effect = Exception("LLM service unavailable")

        # Mock conversation queries response for fallback
        query_router_enhanced.conversation_queries.get_help.return_value = "Here's some help"

        # Test classification and routing
        result = await query_router_enhanced.classify_and_route("help me", {}, "test_session")

        # Verify fallback occurred
        metrics = query_router_enhanced.performance_metrics
        assert metrics["total_requests"] == 1
        assert metrics["rule_based_classifications"] == 1

    def test_performance_metrics_update(self, query_router_enhanced):
        """Test performance metrics update functions"""
        # Test LLM metrics update
        query_router_enhanced._update_llm_metrics(150.0, True)
        assert query_router_enhanced.performance_metrics["average_llm_latency_ms"] == 150.0

        # Test rule-based metrics update
        query_router_enhanced._update_rule_based_metrics(25.0, True)
        assert query_router_enhanced.performance_metrics["average_rule_based_latency_ms"] == 25.0

    def test_get_performance_metrics(self, query_router_enhanced):
        """Test get_performance_metrics method"""
        metrics = query_router_enhanced.get_performance_metrics()

        # Check basic metrics
        assert "total_requests" in metrics
        assert "llm_classifications" in metrics
        assert "rule_based_classifications" in metrics

        # Check rollout information
        assert metrics["llm_rollout_percentage"] == 0.5
        assert metrics["enable_llm_classification"] is True
        assert "performance_targets" in metrics
        assert metrics["llm_classifier_available"] is True

    def test_update_rollout_percentage(self, query_router_enhanced):
        """Test update_rollout_percentage method"""
        # Test valid percentage
        query_router_enhanced.update_rollout_percentage(0.75)
        assert query_router_enhanced.llm_rollout_percentage == 0.75

        # Test invalid percentage
        with pytest.raises(ValueError):
            query_router_enhanced.update_rollout_percentage(1.5)

        with pytest.raises(ValueError):
            query_router_enhanced.update_rollout_percentage(-0.1)

    def test_enable_llm_classification(self, query_router_enhanced):
        """Test enable_llm_classification method"""
        # Test enable
        query_router_enhanced.enable_llm_classification(True)
        assert query_router_enhanced.enable_llm_classification is True

        # Test disable
        query_router_enhanced.enable_llm_classification(False)
        assert query_router_enhanced.enable_llm_classification is False

    @pytest.mark.asyncio
    async def test_performance_target_violation_detection(
        self, query_router_enhanced, mock_llm_classifier
    ):
        """Test performance target violation detection"""
        # Mock LLM classifier to simulate slow response
        mock_intent = Intent(
            message="test message",
            category=IntentCategory.QUERY,
            action="list_projects",
            confidence=0.85,
            context={"llm_classified": True},
        )
        mock_llm_classifier.classify.return_value = mock_intent

        # Mock slow response by adding delay
        async def slow_classify(*args, **kwargs):
            await asyncio.sleep(0.3)  # 300ms > 200ms target
            return mock_intent

        mock_llm_classifier.classify.side_effect = slow_classify

        # Mock project queries response
        query_router_enhanced.project_queries.list_active_projects.return_value = ["project1"]

        # Test classification and routing
        result = await query_router_enhanced.classify_and_route("show projects", {}, "test_session")

        # Verify target violation was recorded
        assert query_router_enhanced.performance_metrics["target_violations"] == 1

    def test_backward_compatibility(self, query_router_basic):
        """Test backward compatibility with existing QueryRouter functionality"""
        # Verify basic router doesn't have LLM components
        assert query_router_basic.llm_classifier is None
        assert query_router_basic.enable_llm_classification is False
        assert query_router_basic.llm_rollout_percentage == 0.0

        # Verify existing methods still work
        assert hasattr(query_router_basic, "route_query")
        assert hasattr(query_router_basic, "get_supported_queries")
        assert hasattr(query_router_basic, "get_degradation_status")

    @pytest.mark.asyncio
    async def test_graceful_degradation_without_llm(self, mock_services):
        """Test graceful degradation when LLM classifier is not available"""
        router = QueryRouter(
            project_query_service=mock_services["project_queries"],
            conversation_query_service=mock_services["conversation_queries"],
            file_query_service=mock_services["file_queries"],
            test_mode=False,
            enable_llm_classification=True,
            llm_rollout_percentage=1.0,  # 100% rollout
            # No LLM classifier provided
        )

        # Mock conversation queries response
        router.conversation_queries.get_greeting.return_value = "Hello!"

        # Should fallback to rule-based classification
        result = await router.classify_and_route("hello", {}, "test_session")

        # Verify fallback occurred
        metrics = router.performance_metrics
        assert metrics["rule_based_classifications"] == 1
        assert metrics["llm_classifications"] == 0


# Import asyncio for the async test
import asyncio

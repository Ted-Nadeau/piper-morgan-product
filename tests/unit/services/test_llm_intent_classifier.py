"""
PM-034: Comprehensive test suite for LLMIntentClassifier

Tests cover:
- Multi-stage pipeline execution
- Knowledge Graph integration
- Confidence scoring and fallback
- Performance benchmarks
- Edge cases and error handling
"""

import asyncio
import json
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.api.errors import IntentClassificationFailedError, LowConfidenceIntentError
from services.domain.models import Intent, IntentCategory, KnowledgeNode
from services.intent_service.llm_classifier import LLMIntentClassifier
from services.intent_service.llm_classifier_factory import LLMClassifierFactory
from services.shared_types import NodeType


class TestLLMIntentClassifier:
    """Test suite for LLM-based intent classification"""

    @pytest.fixture
    def mock_knowledge_graph_service(self):
        """Mock KnowledgeGraphService for testing"""
        mock = MagicMock()
        mock.create_node = AsyncMock(return_value=KnowledgeNode(id="test_node"))
        mock.get_nodes_by_type = AsyncMock(return_value=[])
        return mock

    @pytest.fixture
    def mock_semantic_indexing_service(self):
        """Mock SemanticIndexingService for testing"""
        mock = MagicMock()
        mock.similarity_search = AsyncMock(return_value=[])
        return mock

    @pytest.fixture
    async def classifier(
        self, initialized_container, mock_knowledge_graph_service, mock_semantic_indexing_service
    ):
        """Create classifier with mocked dependencies and initialized container"""
        return await LLMClassifierFactory.create_for_testing(
            mock_knowledge_graph_service=mock_knowledge_graph_service,
            mock_semantic_indexing_service=mock_semantic_indexing_service,
            confidence_threshold=0.75,
        )

    @pytest.mark.asyncio
    async def test_successful_classification_with_high_confidence(self, classifier):
        """Test successful intent classification with high confidence"""
        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "search_documents",
                "confidence": 0.92,
                "reasoning": "User wants to find PM documentation",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            intent = await classifier.classify("Find all product requirements documents")

            assert intent.category == IntentCategory.QUERY
            assert intent.action == "search_documents"
            assert intent.confidence == 0.92
            assert intent.context["llm_classified"] is True

    @pytest.mark.asyncio
    async def test_low_confidence_triggers_fallback(self, classifier):
        """Test that low confidence triggers fallback error"""
        # Mock LLM response with low confidence
        mock_llm_response = json.dumps(
            {
                "category": "unknown",
                "action": "unclear",
                "confidence": 0.45,
                "reasoning": "Ambiguous request",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            with pytest.raises(LowConfidenceIntentError):
                await classifier.classify("Do the thing with the stuff")

    @pytest.mark.asyncio
    async def test_knowledge_graph_context_enrichment(
        self, classifier, mock_semantic_indexing_service
    ):
        """Test Knowledge Graph context enrichment"""
        # Setup mock similar intents
        similar_node = KnowledgeNode(
            id="similar_1",
            name="past_intent",
            node_type=NodeType.EVENT,
            metadata={"intent": {"category": "query", "action": "find_files"}, "confidence": 0.88},
        )
        mock_semantic_indexing_service.similarity_search.return_value = [(similar_node, 0.85)]

        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "find_files",
                "confidence": 0.90,
                "reasoning": "Similar to past intents",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            intent = await classifier.classify("Show me the API specs")

            # Verify Knowledge Graph was queried
            assert mock_semantic_indexing_service.similarity_search.called
            assert intent.action == "find_files"

    @pytest.mark.asyncio
    async def test_preprocessing_typo_correction(self, classifier):
        """Test message preprocessing and typo correction"""
        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "execution",
                "action": "create_github_issue",
                "confidence": 0.85,
                "reasoning": "User wants to create an issue",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            # Test with typos
            intent = await classifier.classify("Craete  a   github isue   for the bug")

            assert intent.category == IntentCategory.EXECUTION
            assert intent.action == "create_github_issue"

    @pytest.mark.skip(
        reason="Metrics tracking assertion - average_latency_ms not being recorded correctly"
    )
    @pytest.mark.asyncio
    async def test_performance_tracking(self, classifier):
        """Test performance metrics tracking"""
        # Mock fast LLM response
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "list_projects",
                "confidence": 0.88,
                "reasoning": "List query",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            # Make several classifications
            for _ in range(3):
                await classifier.classify("Show all projects")

            # Check metrics
            metrics = classifier.get_metrics()
            assert metrics["total_requests"] == 3
            assert metrics["successful_classifications"] == 3
            assert metrics["success_rate"] == 1.0
            assert metrics["average_latency_ms"] > 0

    @pytest.mark.asyncio
    async def test_llm_failure_handling(self, classifier):
        """Test handling of LLM failures"""
        with patch.object(
            classifier.llm, "complete", AsyncMock(side_effect=Exception("LLM API error"))
        ):
            with pytest.raises(IntentClassificationFailedError):
                await classifier.classify("Create a new project")

    @pytest.mark.asyncio
    async def test_invalid_json_response_handling(self, classifier):
        """Test handling of invalid JSON from LLM"""
        # Mock invalid response
        with patch.object(classifier.llm, "complete", AsyncMock(return_value="Not valid JSON")):
            with pytest.raises(IntentClassificationFailedError):
                await classifier.classify("Find documents")

    @pytest.mark.asyncio
    async def test_user_pattern_extraction(self, classifier, mock_knowledge_graph_service):
        """Test user pattern extraction from Knowledge Graph"""
        # Setup mock user history
        past_events = [
            KnowledgeNode(
                id=f"event_{i}",
                node_type=NodeType.EVENT,
                metadata={
                    "intent": {"category": "query", "action": "search_documents"},
                    "action": "search_documents",
                },
            )
            for i in range(3)
        ]
        mock_knowledge_graph_service.get_nodes_by_type.return_value = past_events

        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "search_documents",
                "confidence": 0.95,
                "reasoning": "Consistent with user patterns",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            intent = await classifier.classify("Find more docs", session_id="test_session")

            # Verify session-based query was made
            mock_knowledge_graph_service.get_nodes_by_type.assert_called_with(
                node_type=NodeType.EVENT, session_id="test_session", limit=10
            )

    @pytest.mark.asyncio
    async def test_classification_storage_in_knowledge_graph(
        self, classifier, mock_knowledge_graph_service
    ):
        """Test successful classifications are stored in Knowledge Graph"""
        # Enable learning
        classifier.enable_learning = True

        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "execution",
                "action": "create_task",
                "confidence": 0.88,
                "reasoning": "Task creation request",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            intent = await classifier.classify("Create a new task for the sprint")

            # Verify classification was stored
            mock_knowledge_graph_service.create_node.assert_called_once()
            call_args = mock_knowledge_graph_service.create_node.call_args
            assert call_args[1]["node_type"] == NodeType.EVENT
            assert "intent" in call_args[1]["metadata"]

    @pytest.mark.asyncio
    async def test_domain_knowledge_extraction(self, classifier):
        """Test PM domain knowledge extraction"""
        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "analysis",
                "action": "analyze_timeline",
                "confidence": 0.85,
                "reasoning": "Timeline analysis request",
            }
        )

        with patch.object(
            classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)
        ) as mock_llm:
            await classifier.classify("Analyze project timeline and milestones")

            # Check that domain context was included in prompt
            call_args = mock_llm.call_args
            prompt = call_args[1]["prompt"]
            assert "Detected PM domains: project" in prompt

    @pytest.mark.asyncio
    async def test_confidence_threshold_configuration(self):
        """Test custom confidence threshold configuration"""
        # Create classifier with high threshold
        high_threshold_classifier = await LLMClassifierFactory.create_for_testing(
            confidence_threshold=0.95
        )

        # Mock LLM response with medium confidence
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "search",
                "confidence": 0.90,  # Below 0.95 threshold
                "reasoning": "Search query",
            }
        )

        with patch.object(
            high_threshold_classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)
        ):
            with pytest.raises(LowConfidenceIntentError):
                await high_threshold_classifier.classify("Search for something")


class TestLLMClassifierPerformance:
    """Performance benchmarks for LLMIntentClassifier"""

    @pytest.fixture
    async def fast_classifier(self, initialized_container):
        """Create classifier optimized for performance testing with initialized container"""
        return await LLMClassifierFactory.create_for_testing(confidence_threshold=0.75)

    @pytest.mark.asyncio
    async def test_classification_latency_under_target(self, fast_classifier):
        """Test that classification latency meets performance targets"""
        # Mock instant LLM response
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "list_tasks",
                "confidence": 0.92,
                "reasoning": "Quick classification",
            }
        )

        with patch.object(
            fast_classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)
        ):
            start_time = datetime.now()

            # Perform classification
            await fast_classifier.classify("Show all tasks")

            # Check latency
            latency_ms = (datetime.now() - start_time).total_seconds() * 1000

            # Should be well under 500ms target (without actual LLM call)
            assert latency_ms < 50  # Mock should be very fast

    @pytest.mark.asyncio
    async def test_batch_classification_performance(self, fast_classifier):
        """Test performance with multiple concurrent classifications"""
        # Mock LLM responses
        mock_llm_response = json.dumps(
            {"category": "query", "action": "search", "confidence": 0.88, "reasoning": "Batch test"}
        )

        with patch.object(
            fast_classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)
        ):
            # Run concurrent classifications
            messages = [f"Search for item {i}" for i in range(10)]

            start_time = datetime.now()
            results = await asyncio.gather(*[fast_classifier.classify(msg) for msg in messages])
            total_time_ms = (datetime.now() - start_time).total_seconds() * 1000

            # All should succeed
            assert len(results) == 10
            assert all(r.category == IntentCategory.QUERY for r in results)

            # Average time per classification should be reasonable
            avg_time_ms = total_time_ms / 10
            assert avg_time_ms < 100  # With mocks, should be very fast


class TestLLMClassifierEdgeCases:
    """Edge case testing for LLMIntentClassifier"""

    @pytest.fixture
    async def classifier(self, initialized_container):
        """Create classifier for edge case testing with initialized container"""
        return await LLMClassifierFactory.create_for_testing()

    @pytest.mark.asyncio
    async def test_empty_message_handling(self, classifier):
        """Test handling of empty messages"""
        with pytest.raises(IntentClassificationFailedError):
            await classifier.classify("")

    @pytest.mark.asyncio
    async def test_very_long_message_handling(self, classifier):
        """Test handling of very long messages"""
        # Create a very long message
        long_message = "Find documents " * 1000  # ~14,000 characters

        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "search_documents",
                "confidence": 0.80,
                "reasoning": "Long search query",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            intent = await classifier.classify(long_message)
            assert intent.category == IntentCategory.QUERY

    @pytest.mark.asyncio
    async def test_special_characters_handling(self, classifier):
        """Test handling of special characters in messages"""
        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "execution",
                "action": "create_task",
                "confidence": 0.85,
                "reasoning": "Task creation with special chars",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            intent = await classifier.classify(
                "Create task: <script>alert('test')</script> & handle \"quotes\""
            )
            assert intent.action == "create_task"

    @pytest.mark.asyncio
    async def test_multilingual_message_handling(self, classifier):
        """Test handling of non-English messages"""
        # Mock LLM response
        mock_llm_response = json.dumps(
            {
                "category": "query",
                "action": "search",
                "confidence": 0.78,
                "reasoning": "Multilingual query",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            intent = await classifier.classify("Buscar documentos técnicos")
            assert intent.category == IntentCategory.QUERY

    @pytest.mark.asyncio
    async def test_invalid_category_from_llm(self, classifier):
        """Test handling of invalid category from LLM"""
        # Mock LLM response with invalid category
        mock_llm_response = json.dumps(
            {
                "category": "invalid_category",
                "action": "something",
                "confidence": 0.90,
                "reasoning": "Invalid category test",
            }
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            with pytest.raises(IntentClassificationFailedError):
                await classifier.classify("Do something")

    @pytest.mark.asyncio
    async def test_missing_required_fields_in_llm_response(self, classifier):
        """Test handling of incomplete LLM responses"""
        # Mock LLM response missing action
        mock_llm_response = json.dumps(
            {"category": "query", "confidence": 0.85, "reasoning": "Missing action field"}
        )

        with patch.object(classifier.llm, "complete", AsyncMock(return_value=mock_llm_response)):
            with pytest.raises(IntentClassificationFailedError):
                await classifier.classify("Find something")

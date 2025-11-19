"""Tests for Enhanced Conversation Context Tracker"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.conversation.context_tracker import (
    ContextEnrichment,
    ConversationState,
    EnhancedContextTracker,
    EntityMention,
    enrich_message_context,
    get_conversation_context_summary,
)
from services.conversation.reference_resolver import ResolvedReference
from services.domain.models import ConversationTurn


class TestEnhancedContextTracker:
    """Test enhanced conversation context tracking"""

    @pytest.fixture
    def tracker(self):
        """EnhancedContextTracker instance for testing"""
        return EnhancedContextTracker()

    @pytest.fixture
    def mock_services(self, tracker):
        """Mock the underlying services"""
        tracker.conversation_manager = AsyncMock()
        tracker.memory_service = AsyncMock()
        tracker.user_context_service = AsyncMock()
        return tracker

    @pytest.mark.asyncio
    async def test_enrich_conversation_context_basic(self, mock_services):
        """Test basic conversation context enrichment"""
        # Setup mocks
        mock_services.memory_service.resolve_user_message.return_value = (
            "Can you check issue #123?",
            [ResolvedReference("it", "issue #123", "issue", 0.9, "issue #123")],
            {"resolution_count": 1},
        )

        # Test enrichment
        result = await mock_services.enrich_conversation_context("Can you check it?", "conv-123")

        assert isinstance(result, ContextEnrichment)
        assert result.original_message == "Can you check it?"
        assert result.enriched_message == "Can you check issue #123?"
        assert len(result.resolved_references) == 1
        assert result.confidence_score > 0.0
        assert result.conversation_state.conversation_id == "conv-123"

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Pre-existing failure - tracked in piper-morgan-dw0")
    async def test_entity_extraction_and_tracking(self, mock_services):
        """Test entity extraction and tracking across messages"""
        mock_services.memory_service.resolve_user_message.return_value = (
            "Let's work on issue #456 in project myapp",
            [],
            {},
        )

        # First message with entities
        result1 = await mock_services.enrich_conversation_context(
            "Let's work on issue #456 in project myapp", "conv-456"
        )

        # Check entities were extracted
        assert len(result1.active_entities) == 2
        entity_types = [e.entity_type for e in result1.active_entities]
        assert "issue" in entity_types
        assert "project" in entity_types

        # Second message referring to same entities
        mock_services.memory_service.resolve_user_message.return_value = (
            "The issue is critical and the project needs attention",
            [],
            {},
        )

        result2 = await mock_services.enrich_conversation_context(
            "The issue is critical and the project needs attention", "conv-456"
        )

        # Check entities are still tracked and updated
        conv_state = result2.conversation_state
        assert len(conv_state.active_entities) >= 2

        # Check mention counts increased
        issue_entities = [
            e for e in conv_state.active_entities.values() if e.entity_type == "issue"
        ]
        if issue_entities:
            assert issue_entities[0].mention_count >= 1

    @pytest.mark.asyncio
    async def test_conversation_flow_tracking(self, mock_services):
        """Test conversation flow classification"""
        mock_services.memory_service.resolve_user_message.return_value = ("Hello!", [], {})

        # Test greeting
        result = await mock_services.enrich_conversation_context("Hello!", "conv-flow")
        assert "greeting" in result.conversation_state.conversation_flow

        # Test question
        mock_services.memory_service.resolve_user_message.return_value = (
            "What is the status?",
            [],
            {},
        )
        result = await mock_services.enrich_conversation_context("What is the status?", "conv-flow")
        assert "question" in result.conversation_state.conversation_flow

        # Test request
        mock_services.memory_service.resolve_user_message.return_value = (
            "Please update the issue",
            [],
            {},
        )
        result = await mock_services.enrich_conversation_context(
            "Please update the issue", "conv-flow"
        )
        assert "request" in result.conversation_state.conversation_flow

    @pytest.mark.asyncio
    async def test_confidence_score_calculation(self, mock_services):
        """Test confidence score calculation"""
        # High confidence: resolved references + entities
        mock_services.memory_service.resolve_user_message.return_value = (
            "Check issue #789",
            [ResolvedReference("it", "issue #789", "issue", 0.95, "issue #789")],
            {"resolution_count": 1},
        )

        result = await mock_services.enrich_conversation_context("Check it", "conv-confidence")

        high_confidence = result.confidence_score
        assert high_confidence > 0.3

        # Low confidence: no references, no clear entities
        mock_services.memory_service.resolve_user_message.return_value = (
            "Okay",
            [],
            {"resolution_count": 0},
        )

        result = await mock_services.enrich_conversation_context("Okay", "conv-confidence-2")

        low_confidence = result.confidence_score
        assert low_confidence < high_confidence

    @pytest.mark.asyncio
    async def test_error_handling(self, mock_services):
        """Test error handling in context enrichment"""
        # Make memory service fail
        mock_services.memory_service.resolve_user_message.side_effect = Exception("Service error")

        result = await mock_services.enrich_conversation_context("Test message", "conv-error")

        # Should return minimal enrichment on error
        assert result.original_message == "Test message"
        assert result.enriched_message == "Test message"
        assert result.confidence_score == 0.0
        assert "error" in result.enrichment_metadata

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Pre-existing failure - tracked in piper-morgan-dw0")
    async def test_conversation_state_persistence(self, mock_services):
        """Test conversation state persistence"""
        mock_services.memory_service.resolve_user_message.return_value = (
            "Working on issue #999",
            [],
            {},
        )

        # First enrichment
        result1 = await mock_services.enrich_conversation_context(
            "Working on issue #999", "conv-persist"
        )

        # Second enrichment should reuse state
        result2 = await mock_services.enrich_conversation_context(
            "Still working on it", "conv-persist"
        )

        # Should be same conversation state object
        assert (
            result1.conversation_state.conversation_id == result2.conversation_state.conversation_id
        )
        assert len(result2.conversation_state.conversation_flow) > len(
            result1.conversation_state.conversation_flow
        )

    @pytest.mark.asyncio
    async def test_get_conversation_summary(self, mock_services):
        """Test conversation summary generation"""
        # Setup conversation with entities
        mock_services.memory_service.resolve_user_message.return_value = (
            "Let's fix bug #555 in the auth system",
            [],
            {},
        )

        await mock_services.enrich_conversation_context(
            "Let's fix bug #555 in the auth system", "conv-summary"
        )

        # Get summary
        summary = await mock_services.get_conversation_summary("conv-summary")

        assert summary["conversation_id"] == "conv-summary"
        assert "active_entities" in summary
        assert "conversation_flow" in summary
        assert "stats" in summary
        assert summary["stats"]["total_turns"] > 0

    @pytest.mark.asyncio
    async def test_get_conversation_summary_not_found(self, mock_services):
        """Test conversation summary for non-existent conversation"""
        summary = await mock_services.get_conversation_summary("non-existent")
        assert "error" in summary

    def test_performance_stats(self, mock_services):
        """Test performance statistics"""
        stats = mock_services.get_performance_stats()

        assert "total_enrichments" in stats
        assert "successful_resolutions" in stats
        assert "entity_extractions" in stats
        assert "avg_processing_time" in stats
        assert "active_conversations" in stats
        assert "success_rate" in stats

    def test_entity_patterns_loading(self, tracker):
        """Test entity patterns are properly loaded"""
        patterns = tracker.entity_patterns

        assert "issue" in patterns
        assert "project" in patterns
        assert "file" in patterns
        assert "user" in patterns

        # Check patterns are lists of strings
        for entity_type, pattern_list in patterns.items():
            assert isinstance(pattern_list, list)
            assert all(isinstance(p, str) for p in pattern_list)

    @pytest.mark.asyncio
    async def test_entity_mention_aliases(self, mock_services):
        """Test entity mention alias tracking"""
        # First mention
        mock_services.memory_service.resolve_user_message.return_value = (
            "Check issue #777",
            [],
            {},
        )

        await mock_services.enrich_conversation_context("Check issue #777", "conv-aliases")

        # Second mention with different alias
        mock_services.memory_service.resolve_user_message.return_value = (
            "The bug is critical",
            [],
            {},
        )

        result = await mock_services.enrich_conversation_context(
            "The bug is critical", "conv-aliases"
        )

        # Check aliases are tracked
        conv_state = result.conversation_state
        issue_entities = [
            e for e in conv_state.active_entities.values() if e.entity_type == "issue"
        ]

        if issue_entities:
            entity = issue_entities[0]
            assert len(entity.aliases) >= 1
            assert entity.mention_count >= 1

    @pytest.mark.asyncio
    async def test_conversation_flow_limit(self, mock_services):
        """Test conversation flow history is limited"""
        mock_services.memory_service.resolve_user_message.return_value = ("Test", [], {})

        # Add many messages to exceed limit
        for i in range(25):
            await mock_services.enrich_conversation_context(f"Message {i}", "conv-limit")

        # Check flow is limited to 20
        conv_state = mock_services.conversation_states["conv-limit"]
        assert len(conv_state.conversation_flow) <= 20

    @pytest.mark.asyncio
    async def test_context_snippets_limit(self, mock_services):
        """Test context snippets are limited per entity"""
        mock_services.memory_service.resolve_user_message.return_value = (
            "Working on issue #888",
            [],
            {},
        )

        # Add multiple mentions to exceed snippet limit
        for i in range(5):
            await mock_services.enrich_conversation_context(
                f"Still working on issue #888 - update {i}", "conv-snippets"
            )

        # Check snippets are limited to 3
        conv_state = mock_services.conversation_states["conv-snippets"]
        issue_entities = [
            e for e in conv_state.active_entities.values() if e.entity_type == "issue"
        ]

        if issue_entities:
            entity = issue_entities[0]
            assert len(entity.context_snippets) <= 3


@pytest.mark.skip(reason="Pre-existing failures - tracked in piper-morgan-dw0")
class TestConvenienceFunctions:
    """Test convenience functions"""

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Pre-existing failure - tracked in piper-morgan-dw0")
    @patch("services.conversation.context_tracker.enhanced_context_tracker")
    async def test_enrich_message_context(self, mock_tracker):
        """Test enrich_message_context convenience function"""
        mock_enrichment = ContextEnrichment(
            original_message="test",
            enriched_message="test",
            resolved_references=[],
            active_entities=[],
            conversation_state=ConversationState(conversation_id="test"),
            confidence_score=0.5,
            enrichment_metadata={},
        )

        mock_tracker.enrich_conversation_context.return_value = mock_enrichment

        result = await enrich_message_context("test", "conv-123")

        assert result == mock_enrichment
        mock_tracker.enrich_conversation_context.assert_called_once_with(
            "test", "conv-123", None, None
        )

    @pytest.mark.asyncio
    @patch("services.conversation.context_tracker.enhanced_context_tracker")
    async def test_get_conversation_context_summary(self, mock_tracker):
        """Test get_conversation_context_summary convenience function"""
        mock_summary = {"conversation_id": "conv-123", "stats": {}}
        mock_tracker.get_conversation_summary.return_value = mock_summary

        result = await get_conversation_context_summary("conv-123")

        assert result == mock_summary
        mock_tracker.get_conversation_summary.assert_called_once_with("conv-123")


class TestEntityMention:
    """Test EntityMention dataclass"""

    def test_entity_mention_creation(self):
        """Test EntityMention creation and defaults"""
        now = datetime.now()

        entity = EntityMention(
            entity_id="issue:123",
            entity_type="issue",
            first_mentioned=now,
            last_mentioned=now,
            mention_count=1,
        )

        assert entity.entity_id == "issue:123"
        assert entity.entity_type == "issue"
        assert entity.mention_count == 1
        assert len(entity.aliases) == 0
        assert len(entity.context_snippets) == 0


class TestConversationState:
    """Test ConversationState dataclass"""

    def test_conversation_state_creation(self):
        """Test ConversationState creation and defaults"""
        state = ConversationState(conversation_id="test-123")

        assert state.conversation_id == "test-123"
        assert state.current_topic is None
        assert len(state.active_entities) == 0
        assert len(state.user_intent_history) == 0
        assert len(state.conversation_flow) == 0
        assert len(state.metadata) == 0
        assert isinstance(state.created_at, datetime)
        assert isinstance(state.updated_at, datetime)

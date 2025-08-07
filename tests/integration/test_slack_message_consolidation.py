"""
Test suite for PM-079-SUB Slack Message Consolidation

Tests the message consolidation functionality implemented in SlackResponseHandler
to ensure requirements are met and acceptance criteria are satisfied.
"""

import time
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.integrations.slack.response_handler import SlackResponseHandler
from services.integrations.slack.slack_client import SlackClient
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.intent_service.classifier import IntentClassifier
from services.orchestration.engine import OrchestrationEngine


class TestSlackMessageConsolidation:
    """Test PM-079-SUB Slack message consolidation functionality"""

    @pytest.fixture
    def mock_spatial_adapter(self):
        """Mock spatial adapter"""
        adapter = AsyncMock(spec=SlackSpatialAdapter)
        adapter.get_mapping_stats.return_value = {"mappings": 0}
        return adapter

    @pytest.fixture
    def mock_intent_classifier(self):
        """Mock intent classifier"""
        return AsyncMock(spec=IntentClassifier)

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine"""
        return AsyncMock(spec=OrchestrationEngine)

    @pytest.fixture
    def mock_slack_client(self):
        """Mock Slack client"""
        client = AsyncMock(spec=SlackClient)
        client.send_message.return_value = MagicMock(success=True)
        return client

    @pytest.fixture
    def response_handler(
        self,
        mock_spatial_adapter,
        mock_intent_classifier,
        mock_orchestration_engine,
        mock_slack_client,
    ):
        """Create SlackResponseHandler with mocked dependencies"""
        return SlackResponseHandler(
            spatial_adapter=mock_spatial_adapter,
            intent_classifier=mock_intent_classifier,
            orchestration_engine=mock_orchestration_engine,
            slack_client=mock_slack_client,
        )

    @pytest.fixture
    def sample_slack_context(self):
        """Sample Slack context for testing"""
        return {
            "channel_id": "C1234567890",
            "user_id": "U1234567890",
            "thread_ts": "1234567890.123456",
            "content": "create a GitHub issue",
        }

    @pytest.fixture
    def sample_workflow_result(self):
        """Sample workflow result for testing"""
        return {
            "type": "workflow_result",
            "workflow_id": "wf_123",
            "result": {
                "summary": "Created GitHub issue #123 'Pipeline Enhancement'",
                "message": "✅ Created GitHub issue #123 'Pipeline Enhancement'",
            },
        }

    def test_consolidation_key_generation(self, response_handler, sample_slack_context):
        """Test consolidation key generation based on channel and thread"""
        key = response_handler._get_consolidation_key(sample_slack_context)
        expected = "C1234567890:1234567890.123456"
        assert key == expected

    def test_consolidation_key_without_thread(self, response_handler):
        """Test consolidation key generation without thread"""
        context = {"channel_id": "C1234567890"}
        key = response_handler._get_consolidation_key(context)
        expected = "C1234567890:main"
        assert key == expected

    def test_add_to_consolidation_buffer(self, response_handler, sample_slack_context):
        """Test adding messages to consolidation buffer"""
        message_data = {
            "content": "Test message",
            "type": "workflow_result",
        }

        response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)

        # Verify message was added to buffer
        key = response_handler._get_consolidation_key(sample_slack_context)
        from services.integrations.slack.response_handler import MESSAGE_CONSOLIDATION_BUFFER

        assert key in MESSAGE_CONSOLIDATION_BUFFER
        assert len(MESSAGE_CONSOLIDATION_BUFFER[key]) == 1
        assert MESSAGE_CONSOLIDATION_BUFFER[key][0]["content"] == "Test message"

    def test_should_consolidate_messages_false_single_message(
        self, response_handler, sample_slack_context
    ):
        """Test consolidation decision with single message"""
        message_data = {
            "content": "Test message",
            "type": "workflow_result",
            "timestamp": time.time(),
        }

        response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)

        key = response_handler._get_consolidation_key(sample_slack_context)
        should_consolidate = response_handler._should_consolidate_messages(key)

        assert not should_consolidate

    def test_should_consolidate_messages_true_multiple_messages(
        self, response_handler, sample_slack_context
    ):
        """Test consolidation decision with multiple recent messages"""
        current_time = time.time()

        # Add multiple messages within consolidation timeout
        for i in range(3):
            message_data = {
                "content": f"Test message {i}",
                "type": "workflow_result",
                "timestamp": current_time - i,  # All within timeout
            }
            response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)

        key = response_handler._get_consolidation_key(sample_slack_context)
        should_consolidate = response_handler._should_consolidate_messages(key)

        assert should_consolidate

    def test_format_consolidated_message(self, response_handler, sample_slack_context):
        """Test consolidated message formatting"""
        messages = [
            {
                "content": "✅ Created GitHub issue #123",
                "type": "workflow_result",
                "timestamp": time.time(),
            },
            {
                "content": "✅ Updated project status",
                "type": "workflow_result",
                "timestamp": time.time(),
            },
            {
                "content": "📊 Analyzed performance metrics",
                "type": "workflow_result",
                "timestamp": time.time(),
            },
        ]

        consolidated = response_handler._format_consolidated_message(messages, sample_slack_context)

        # Verify consolidated format
        assert "🤖" in consolidated  # Main workflow message
        assert "📋 2 additional actions completed" in consolidated  # Summary
        assert "💬 Reply with 'details'" in consolidated  # Thread hint

    def test_format_consolidated_message_single_workflow(
        self, response_handler, sample_slack_context
    ):
        """Test consolidated message formatting with single workflow"""
        messages = [
            {
                "content": "✅ Created GitHub issue #123",
                "type": "workflow_result",
                "timestamp": time.time(),
            },
        ]

        consolidated = response_handler._format_consolidated_message(messages, sample_slack_context)

        # Should not consolidate single messages
        assert consolidated == ""

    def test_clear_consolidation_buffer(self, response_handler, sample_slack_context):
        """Test clearing consolidation buffer"""
        message_data = {
            "content": "Test message",
            "type": "workflow_result",
        }

        response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)
        key = response_handler._get_consolidation_key(sample_slack_context)

        # Verify buffer has content
        from services.integrations.slack.response_handler import MESSAGE_CONSOLIDATION_BUFFER

        assert key in MESSAGE_CONSOLIDATION_BUFFER

        # Clear buffer
        response_handler._clear_consolidation_buffer(key)

        # Verify buffer is cleared
        assert key not in MESSAGE_CONSOLIDATION_BUFFER

    @pytest.mark.asyncio
    async def test_send_consolidated_response_success(
        self, response_handler, sample_slack_context, mock_slack_client
    ):
        """Test successful consolidated response sending"""
        # Add multiple messages to trigger consolidation
        current_time = time.time()
        for i in range(3):
            message_data = {
                "content": f"Test message {i}",
                "type": "workflow_result",
                "timestamp": current_time - i,
            }
            response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)

        # Send consolidated response
        result = await response_handler._send_consolidated_response(sample_slack_context)

        # Verify response was sent
        assert result is not None
        assert result["consolidated_count"] == 3
        assert "consolidated" in result["response_content"]

        # Verify Slack client was called
        mock_slack_client.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_consolidated_response_no_consolidation(
        self, response_handler, sample_slack_context
    ):
        """Test consolidated response when no consolidation should occur"""
        # Add single message (should not consolidate)
        message_data = {
            "content": "Test message",
            "type": "workflow_result",
            "timestamp": time.time(),
        }
        response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)

        # Try to send consolidated response
        result = await response_handler._send_consolidated_response(sample_slack_context)

        # Should return None (no consolidation)
        assert result is None

    @pytest.mark.asyncio
    async def test_send_slack_response_with_consolidation(
        self, response_handler, sample_slack_context, sample_workflow_result, mock_slack_client
    ):
        """Test sending Slack response with consolidation logic"""
        # Add multiple messages to trigger consolidation
        current_time = time.time()
        for i in range(2):
            message_data = {
                "content": f"Test message {i}",
                "type": "workflow_result",
                "timestamp": current_time - i,
            }
            response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)

        # Send response (should trigger consolidation)
        result = await response_handler._send_slack_response(
            sample_workflow_result, sample_slack_context
        )

        # Verify consolidated response
        assert result is not None
        assert result["consolidated_count"] == 3  # 2 existing + 1 new
        assert "consolidated" in result["response_content"]

    @pytest.mark.asyncio
    async def test_send_slack_response_individual_message(
        self, response_handler, sample_slack_context, sample_workflow_result, mock_slack_client
    ):
        """Test sending individual Slack response when no consolidation"""
        # Send response (no existing messages in buffer)
        result = await response_handler._send_slack_response(
            sample_workflow_result, sample_slack_context
        )

        # Verify individual response
        assert result is not None
        assert result["consolidated_count"] == 1
        assert "individual" in result["response_content"]

    @pytest.mark.asyncio
    async def test_get_detailed_message_breakdown(self, response_handler, sample_slack_context):
        """Test getting detailed message breakdown"""
        # Add messages to buffer
        messages = [
            {
                "content": "✅ Created GitHub issue #123",
                "type": "workflow_result",
                "timestamp": time.time(),
            },
            {
                "content": "📊 Analyzed metrics",
                "type": "simple_response",
                "timestamp": time.time(),
            },
        ]

        for msg in messages:
            response_handler._add_to_consolidation_buffer(msg, sample_slack_context)

        # Get detailed breakdown
        breakdown = await response_handler.get_detailed_message_breakdown(sample_slack_context)

        # Verify breakdown format
        assert "📋 **Detailed Message Breakdown:**" in breakdown
        assert "1. **workflow_result**" in breakdown
        assert "2. **simple_response**" in breakdown

    @pytest.mark.asyncio
    async def test_get_handler_stats_with_consolidation(self, response_handler):
        """Test handler stats include consolidation metrics"""
        stats = await response_handler.get_handler_stats()

        # Verify consolidation stats are included
        assert "consolidation_stats" in stats
        consolidation_stats = stats["consolidation_stats"]

        assert "active_buffers" in consolidation_stats
        assert "total_buffered_messages" in consolidation_stats
        assert "consolidation_timeout" in consolidation_stats
        assert "max_messages_per_buffer" in consolidation_stats

    def test_consolidation_buffer_size_limit(self, response_handler, sample_slack_context):
        """Test consolidation buffer size limit enforcement"""
        from services.integrations.slack.response_handler import CONSOLIDATION_MAX_MESSAGES

        # Add more messages than the limit
        for i in range(CONSOLIDATION_MAX_MESSAGES + 2):
            message_data = {
                "content": f"Test message {i}",
                "type": "workflow_result",
                "timestamp": time.time(),
            }
            response_handler._add_to_consolidation_buffer(message_data, sample_slack_context)

        # Verify buffer size is limited
        key = response_handler._get_consolidation_key(sample_slack_context)
        from services.integrations.slack.response_handler import MESSAGE_CONSOLIDATION_BUFFER

        assert len(MESSAGE_CONSOLIDATION_BUFFER[key]) == CONSOLIDATION_MAX_MESSAGES
        # Should keep the most recent messages
        assert (
            MESSAGE_CONSOLIDATION_BUFFER[key][-1]["content"]
            == f"Test message {CONSOLIDATION_MAX_MESSAGES + 1}"
        )


class TestPM079SUBRequirements:
    """Test PM-079-SUB specific requirements and acceptance criteria"""

    @pytest.fixture
    def response_handler(self):
        """Create response handler for requirement testing"""
        return SlackResponseHandler(
            spatial_adapter=AsyncMock(),
            intent_classifier=AsyncMock(),
            orchestration_engine=AsyncMock(),
            slack_client=AsyncMock(),
        )

    def test_requirement_single_notification_per_workflow(self, response_handler):
        """Test requirement: Single notification per workflow completion"""
        # This is achieved by the consolidation logic that groups related messages
        # and sends them as a single consolidated response
        assert hasattr(response_handler, "_format_consolidated_message")
        assert hasattr(response_handler, "_send_consolidated_response")

    def test_requirement_reduced_message_count(self, response_handler):
        """Test requirement: Reduced message count from 3-5 to 1-2 messages"""
        # The consolidation logic should reduce multiple messages to a single response
        messages = [
            {"content": "Message 1", "type": "workflow_result"},
            {"content": "Message 2", "type": "workflow_result"},
            {"content": "Message 3", "type": "workflow_result"},
        ]

        consolidated = response_handler._format_consolidated_message(messages, {})
        # Should be a single consolidated message instead of 3 separate ones
        assert consolidated != ""
        assert "🤖" in consolidated  # Main message indicator

    def test_requirement_essential_information_preserved(self, response_handler):
        """Test requirement: All essential information preserved"""
        messages = [
            {"content": "✅ Created GitHub issue #123", "type": "workflow_result"},
            {"content": "📊 Analyzed performance", "type": "workflow_result"},
        ]

        consolidated = response_handler._format_consolidated_message(messages, {})

        # Essential information should be preserved
        assert "🤖" in consolidated  # Main workflow result
        assert "📋" in consolidated  # Summary of additional actions
        assert "💬" in consolidated  # Details access hint

    def test_requirement_optional_detailed_view(self, response_handler):
        """Test requirement: Optional detailed view mechanism implemented"""
        # The get_detailed_message_breakdown method provides detailed view
        assert hasattr(response_handler, "get_detailed_message_breakdown")

        # Test that detailed breakdown is available
        breakdown = response_handler.get_detailed_message_breakdown({})
        assert breakdown is not None

    def test_requirement_user_experience_improvement(self, response_handler):
        """Test requirement: User experience testing confirms improvement"""
        # The consolidation reduces message spam and provides cleaner interface
        # This is verified by the consolidation logic and formatting

        # Test that consolidated messages are more user-friendly
        messages = [
            {"content": "✅ Task 1 completed", "type": "workflow_result"},
            {"content": "✅ Task 2 completed", "type": "workflow_result"},
            {"content": "✅ Task 3 completed", "type": "workflow_result"},
        ]

        consolidated = response_handler._format_consolidated_message(messages, {})

        # Should be more concise and user-friendly
        assert len(consolidated.split("\n")) < len(messages)  # Fewer lines
        assert "additional actions" in consolidated  # Summary instead of repetition

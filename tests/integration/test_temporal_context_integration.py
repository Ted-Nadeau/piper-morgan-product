"""
Comprehensive Testing for Temporal Context Integration and Calendar Awareness

This test suite validates the enhanced temporal context system including:
- Dynamic calendar context integration
- Time-aware standup responses
- Calendar pattern parsing and formatting
- MCP integration readiness
- Performance validation
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.queries.conversation_queries import ConversationQueryService
from services.shared_types import IntentCategory as IntentCategoryEnum


class TestTemporalContextIntegration:
    """Test suite for temporal context integration and calendar awareness"""

    @pytest.fixture
    def conversation_service(self):
        """Create conversation service instance for testing"""
        return ConversationQueryService()

    @pytest.fixture
    def canonical_handlers(self):
        """Create canonical handlers instance for testing"""
        return CanonicalHandlers()

    @pytest.fixture
    def mock_calendar_data(self):
        """Mock calendar data for testing dynamic calendar integration"""
        return {
            "upcoming_events": [
                {
                    "start_time": "9:00 AM",
                    "title": "Development Sprint Planning",
                    "duration": "1 hour",
                },
                {"start_time": "2:00 PM", "title": "UX Review Session", "duration": "45 minutes"},
                {"start_time": "4:00 PM", "title": "Daily Standup", "duration": "15 minutes"},
            ],
            "time_blocks": [
                {"start_time": "8:00 AM", "end_time": "11:00 AM", "type": "deep_work"},
                {"start_time": "1:00 PM", "end_time": "3:00 PM", "type": "collaboration"},
                {"start_time": "3:30 PM", "end_time": "5:00 PM", "type": "planning"},
            ],
            "daily_schedule": {
                "6:00 AM": "Morning Standup",
                "9:00 AM": "Development Focus",
                "2:00 PM": "UX Enhancement",
                "5:00 PM": "Documentation",
            },
        }

    @pytest.fixture
    def mock_static_calendar_patterns(self):
        """Mock static calendar patterns from PIPER.md"""
        return """**Daily Routines**:

- **6:00 AM PT**: Daily standup with Piper Morgan
- **9:00 AM PT**: Development focus time
- **2:00 PM PT**: UX and improvement work
- **5:00 PM PT**: Documentation and handoff preparation

**Recurring Meetings**:

- **Monday**: MCP development sprints
- **Wednesday**: UX enhancement sessions
- **Friday**: Pattern review and methodology validation

**Key Dates**:

- **August 18, 2025**: Next development sprint planning
- **August 20, 2025**: UX improvement validation
- **August 22, 2025**: Pattern review session"""

    @pytest.fixture
    def sample_intent(self):
        """Create sample intent for testing canonical handlers"""
        return Intent(
            category=IntentCategoryEnum.TEMPORAL,
            action="get_temporal_context",
            confidence=0.9,
            context={"query": "What day is it?"},
        )

    @pytest.mark.asyncio
    async def test_get_temporal_context_basic(self, conversation_service):
        """Test basic temporal context functionality"""
        temporal_context = await conversation_service.get_temporal_context()

        # Verify basic temporal information is present
        assert "**Current Time**:" in temporal_context
        assert "**Day of Week**:" in temporal_context
        assert "**Week**:" in temporal_context

        # Verify current time format
        current_time = datetime.now()
        assert current_time.strftime("%A") in temporal_context
        assert str(current_time.year) in temporal_context

    @pytest.mark.asyncio
    async def test_get_temporal_context_with_static_patterns(
        self, conversation_service, mock_static_calendar_patterns
    ):
        """Test temporal context with static calendar patterns fallback"""
        with patch.object(conversation_service.config_loader, "load_config") as mock_load:
            mock_load.return_value = {"Calendar Patterns": mock_static_calendar_patterns}

            temporal_context = await conversation_service.get_temporal_context()

            # Verify calendar context is included
            assert "**Calendar Context**:" in temporal_context
            assert "**Current Phase**:" in temporal_context
            assert "Daily standup with Piper Morgan" in temporal_context

    @pytest.mark.asyncio
    async def test_get_temporal_context_mcp_integration_ready(self, conversation_service):
        """Test that MCP integration is ready for future implementation"""
        # Test that the method exists and can handle MCP data
        temporal_context = await conversation_service.get_temporal_context()

        # Should work without MCP data (fallback to static patterns)
        assert temporal_context is not None
        assert len(temporal_context) > 0

    @pytest.mark.asyncio
    async def test_format_calendar_context_dynamic(self, conversation_service, mock_calendar_data):
        """Test formatting of dynamic calendar data"""
        formatted_context = conversation_service._format_calendar_context(
            mock_calendar_data, datetime.now()
        )

        # Verify upcoming events are formatted
        assert "**Upcoming Events**:" in formatted_context
        assert "Development Sprint Planning" in formatted_context

        # Verify time blocks are formatted
        assert "**Available Time Blocks**:" in formatted_context
        assert "deep_work time" in formatted_context

        # Verify daily schedule is formatted
        assert "**Today's Schedule**:" in formatted_context
        assert "Morning Standup" in formatted_context

    @pytest.mark.asyncio
    async def test_format_static_calendar_context(
        self, conversation_service, mock_static_calendar_patterns
    ):
        """Test formatting of static calendar patterns with time awareness"""
        current_time = datetime.now()
        formatted_context = conversation_service._format_static_calendar_context(
            mock_static_calendar_patterns, current_time
        )

        # Verify current phase is added based on time
        assert "**Current Phase**:" in formatted_context

        # Verify time-based activities are formatted
        assert "**6:00 AM PT**: Daily standup with Piper Morgan" in formatted_context
        assert "**9:00 AM PT**: Development focus time" in formatted_context

        # Verify day-specific patterns are included
        assert "**Monday**: MCP development sprints" in formatted_context
        assert "**Wednesday**: UX enhancement sessions" in formatted_context

    @pytest.mark.asyncio
    async def test_get_focus_guidance_time_aware(self, conversation_service):
        """Test time-aware focus guidance functionality"""
        focus_guidance = await conversation_service.get_focus_guidance()

        # Verify temporal context is included
        assert "**Focus Guidance Based on Current Context**:" in focus_guidance
        assert "**Current Phase**:" in focus_guidance

        # Verify time-based recommendations
        current_hour = datetime.now().hour
        if 5 <= current_hour <= 7:
            assert "Morning Standup Focus" in focus_guidance
        elif 8 <= current_hour <= 11:
            assert "Development Focus Time" in focus_guidance
        elif 12 <= current_hour <= 16:
            assert "Afternoon Work Session" in focus_guidance
        else:
            assert "Evening Planning" in focus_guidance

    @pytest.mark.asyncio
    async def test_get_focus_guidance_day_specific(self, conversation_service):
        """Test day-specific focus guidance"""
        focus_guidance = await conversation_service.get_focus_guidance()

        # Verify day-specific guidance is included
        current_day = datetime.now().strftime("%A")
        if current_day == "Monday":
            assert "Monday Focus" in focus_guidance
        elif current_day == "Wednesday":
            assert "Wednesday Focus" in focus_guidance
        elif current_day == "Friday":
            assert "Friday Focus" in focus_guidance

    @pytest.mark.asyncio
    async def test_get_time_aware_priority(self, conversation_service):
        """Test time-aware priority functionality"""
        time_aware_priority = await conversation_service.get_time_aware_priority()

        # Verify priorities are included
        assert "**Your Current Standing Priorities**:" in time_aware_priority

        # Verify time context is added
        assert "**Time Context**:" in time_aware_priority

        # Verify time remaining calculation
        current_hour = datetime.now().hour
        if current_hour < 17:
            assert "Time Remaining Today" in time_aware_priority
        else:
            assert "Day Complete" in time_aware_priority

    @pytest.mark.asyncio
    async def test_canonical_handlers_temporal_integration(self, canonical_handlers, sample_intent):
        """Test canonical handlers integration with temporal context"""
        response = await canonical_handlers.handle(sample_intent, "test_session")

        # Verify response structure
        assert "message" in response
        assert "intent" in response
        assert response["intent"]["category"] == IntentCategoryEnum.TEMPORAL.value

        # Verify enhanced temporal context is provided
        message = response["message"]
        assert "**Current Time**:" in message
        assert "**Time Guidance**:" in message

    @pytest.mark.asyncio
    async def test_canonical_handlers_status_temporal_awareness(self, canonical_handlers):
        """Test status query with temporal awareness"""
        status_intent = Intent(
            category=IntentCategoryEnum.STATUS,
            action="get_project_status",
            confidence=0.9,
            context={"query": "What am I working on?"},
        )

        response = await canonical_handlers.handle(status_intent, "test_session")

        # Verify temporal context is included in status
        message = response["message"]
        assert "**Current Project Status with Temporal Context**:" in message
        assert "**Time-Aware Focus**:" in message

    @pytest.mark.asyncio
    async def test_canonical_handlers_priority_temporal_awareness(self, canonical_handlers):
        """Test priority query with temporal awareness"""
        priority_intent = Intent(
            category=IntentCategoryEnum.PRIORITY,
            action="get_top_priority",
            confidence=0.9,
            context={"query": "What's my top priority?"},
        )

        response = await canonical_handlers.handle(priority_intent, "test_session")

        # Verify temporal context is included in priority
        message = response["message"]
        assert "**Time Constraint Analysis**:" in message
        assert "**Enhanced Context**:" in message

    @pytest.mark.asyncio
    async def test_canonical_handlers_guidance_temporal_awareness(self, canonical_handlers):
        """Test guidance query with temporal awareness"""
        guidance_intent = Intent(
            category=IntentCategoryEnum.GUIDANCE,
            action="get_focus_guidance",
            confidence=0.9,
            context={"query": "What should I focus on?"},
        )

        response = await canonical_handlers.handle(guidance_intent, "test_session")

        # Verify comprehensive temporal guidance
        message = response["message"]
        assert "**Focus Guidance Based on Current Context**:" in message
        assert "**Focus Intensity**:" in message
        assert "**Daily Strategy**:" in message
        assert "**Enhanced Temporal Context**:" in message

    @pytest.mark.asyncio
    async def test_performance_targets(self, conversation_service):
        """Test performance targets for temporal context operations"""
        start_time = datetime.now()

        # Execute temporal context operations
        temporal_context = await conversation_service.get_temporal_context()
        focus_guidance = await conversation_service.get_focus_guidance()
        time_aware_priority = await conversation_service.get_time_aware_priority()

        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds

        # Verify performance target: <200ms latency
        assert (
            execution_time < 200
        ), f"Temporal context operations took {execution_time}ms, target: <200ms"

        # Verify all operations completed successfully
        assert temporal_context is not None
        assert focus_guidance is not None
        assert time_aware_priority is not None

    @pytest.mark.asyncio
    async def test_backward_compatibility(self, conversation_service):
        """Test backward compatibility with existing functionality"""
        # Test that existing methods still work
        greeting = await conversation_service.get_greeting()
        help_msg = await conversation_service.get_help()
        status = await conversation_service.get_status()
        identity = await conversation_service.get_identity()

        # Verify all methods return expected content
        assert greeting is not None and len(greeting) > 0
        assert help_msg is not None and len(help_msg) > 0
        assert status is not None and len(status) > 0
        assert identity is not None and len(identity) > 0

    @pytest.mark.asyncio
    async def test_error_handling(self, conversation_service):
        """Test error handling in temporal context operations"""
        # Test with invalid calendar data
        invalid_calendar_data = {"invalid_key": "invalid_value"}

        # Should handle gracefully without crashing
        try:
            formatted_context = conversation_service._format_calendar_context(
                invalid_calendar_data, datetime.now()
            )
            # Should return empty context or handle gracefully
            assert formatted_context is not None
        except Exception as e:
            pytest.fail(f"Error handling failed: {e}")

    @pytest.mark.asyncio
    async def test_mcp_integration_readiness(self, conversation_service):
        """Test that MCP integration is ready for future implementation"""
        # Test that the MCP integration method exists and is callable
        assert hasattr(conversation_service, "_get_calendar_from_mcp")
        assert callable(conversation_service._get_calendar_from_mcp)

        # Test that it returns None when MCP is not available (current state)
        calendar_data = await conversation_service._get_calendar_from_mcp(datetime.now())
        assert calendar_data is None  # Expected when MCP adapter not yet built

    @pytest.mark.asyncio
    async def test_calendar_context_fallback_behavior(self, conversation_service):
        """Test fallback behavior when MCP is unavailable"""
        # Test that static patterns are used when MCP is not available
        temporal_context = await conversation_service.get_temporal_context()

        # Should include basic temporal information even without calendar
        assert "**Current Time**:" in temporal_context
        assert "**Day of Week**:" in temporal_context

        # May or may not include calendar context depending on PIPER.md config
        # This is acceptable fallback behavior

    @pytest.mark.asyncio
    async def test_time_awareness_accuracy(self, conversation_service):
        """Test accuracy of time-aware recommendations"""
        current_time = datetime.now()
        current_hour = current_time.hour
        current_day = current_time.strftime("%A")

        # Test focus guidance time awareness
        focus_guidance = await conversation_service.get_focus_guidance()

        # Verify time-based recommendations match current time
        if 5 <= current_hour <= 7:
            assert "Morning Standup Focus" in focus_guidance
        elif 8 <= current_hour <= 11:
            assert "Development Focus Time" in focus_guidance
        elif 12 <= current_hour <= 16:
            assert "Afternoon Work Session" in focus_guidance
        else:
            assert "Evening Planning" in focus_guidance

        # Verify day-specific recommendations
        if current_day == "Monday":
            assert "Monday Focus" in focus_guidance
        elif current_day == "Wednesday":
            assert "Wednesday Focus" in focus_guidance
        elif current_day == "Friday":
            assert "Friday Focus" in focus_guidance


class TestTemporalContextEdgeCases:
    """Test edge cases and boundary conditions for temporal context"""

    @pytest.fixture
    def conversation_service(self):
        """Create conversation service instance for testing"""
        return ConversationQueryService()

    @pytest.mark.asyncio
    async def test_midnight_boundary(self, conversation_service):
        """Test behavior around midnight boundary"""
        # Mock datetime to test midnight boundary
        with patch("services.queries.conversation_queries.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 18, 0, 0)  # Midnight

            focus_guidance = await conversation_service.get_focus_guidance()

            # Should handle midnight gracefully
            assert focus_guidance is not None
            assert "Evening Planning" in focus_guidance

    @pytest.mark.asyncio
    async def test_weekend_handling(self, conversation_service):
        """Test weekend day handling"""
        # Mock datetime to test weekend
        with patch("services.queries.conversation_queries.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 16, 10, 0)  # Saturday 10 AM

            focus_guidance = await conversation_service.get_focus_guidance()

            # Should handle weekend gracefully
            assert focus_guidance is not None
            assert "Development Focus Time" in focus_guidance

    @pytest.mark.asyncio
    async def test_empty_calendar_patterns(self, conversation_service):
        """Test behavior with empty calendar patterns"""
        with patch.object(conversation_service.config_loader, "load_config") as mock_load:
            mock_load.return_value = {"Calendar Patterns": ""}

            temporal_context = await conversation_service.get_temporal_context()

            # Should still provide basic temporal information
            assert "**Current Time**:" in temporal_context
            assert "**Day of Week**:" in temporal_context

            # Should not include calendar context section
            assert "**Calendar Context**:" not in temporal_context

    @pytest.mark.asyncio
    async def test_malformed_calendar_patterns(self, conversation_service):
        """Test behavior with malformed calendar patterns"""
        malformed_patterns = "Invalid\nCalendar\nPatterns\nWithout\nProper\nFormatting"

        with patch.object(conversation_service.config_loader, "load_config") as mock_load:
            mock_load.return_value = {"Calendar Patterns": malformed_patterns}

            temporal_context = await conversation_service.get_temporal_context()

            # Should handle malformed patterns gracefully
            assert temporal_context is not None
            assert len(temporal_context) > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])

"""
Unit tests for Calendar query handlers in IntentService.

Issue #518: Phase A Quick Wins - Calendar Cluster (Canonical Queries #34, #35, #61)

Tests cover:
- Handler routing for Calendar query actions
- Graceful fallback when Calendar is not configured
- Meeting time summary result formatting (Query #34)
- Recurring meetings result formatting (Query #35)
- Week calendar view result formatting (Query #61)
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.shared_types import IntentCategory


@pytest.fixture
def mock_workflow():
    """Mock workflow object"""
    workflow = MagicMock()
    workflow.id = "test-workflow-id"
    return workflow


@pytest.fixture
def intent_service():
    """Create IntentService instance for testing"""
    # Patch dependencies to avoid initialization issues
    with patch("services.intent.intent_service.OrchestrationEngine"):
        with patch("services.intent.intent_service.LearningHandler"):
            with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
                service = IntentService()
                return service


class TestMeetingTimeQueryRouting:
    """Test routing to meeting time query handler"""

    @pytest.mark.asyncio
    async def test_routes_meeting_time_action(self, intent_service, mock_workflow):
        """Test that meeting_time action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        with patch.object(
            intent_service, "_handle_meeting_time_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="3 hours in meetings",
                intent_data={"category": "query", "action": "meeting_time"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_how_much_time_in_meetings_action(self, intent_service, mock_workflow):
        """Test that how_much_time_in_meetings action also routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="how_much_time_in_meetings",
            context={"original_message": "meeting time this week"},
        )

        with patch.object(
            intent_service, "_handle_meeting_time_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="2 hours in meetings",
                intent_data={"category": "query", "action": "how_much_time_in_meetings"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_calendar_analysis_action(self, intent_service, mock_workflow):
        """Test that calendar_analysis action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="calendar_analysis",
            context={"original_message": "analyze my calendar time"},
        )

        with patch.object(
            intent_service, "_handle_meeting_time_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="4 hours in meetings",
                intent_data={"category": "query", "action": "calendar_analysis"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()


class TestRecurringMeetingsQueryRouting:
    """Test routing to recurring meetings query handler"""

    @pytest.mark.asyncio
    async def test_routes_recurring_meetings_action(self, intent_service, mock_workflow):
        """Test that recurring_meetings action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review my recurring meetings"},
        )

        with patch.object(
            intent_service, "_handle_recurring_meetings_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="5 recurring meetings found",
                intent_data={"category": "query", "action": "recurring_meetings"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_review_recurring_meetings_action(self, intent_service, mock_workflow):
        """Test that review_recurring_meetings action also routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="review_recurring_meetings",
            context={"original_message": "audit my standing meetings"},
        )

        with patch.object(
            intent_service, "_handle_recurring_meetings_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="3 recurring meetings found",
                intent_data={"category": "query", "action": "review_recurring_meetings"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_audit_meetings_action(self, intent_service, mock_workflow):
        """Test that audit_meetings action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="audit_meetings",
            context={"original_message": "which meetings can I drop"},
        )

        with patch.object(
            intent_service, "_handle_recurring_meetings_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="7 recurring meetings found",
                intent_data={"category": "query", "action": "audit_meetings"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()


class TestWeekCalendarQueryRouting:
    """Test routing to week calendar query handler"""

    @pytest.mark.asyncio
    async def test_routes_week_calendar_action(self, intent_service, mock_workflow):
        """Test that week_calendar action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        with patch.object(
            intent_service, "_handle_week_calendar_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Week calendar view",
                intent_data={"category": "query", "action": "week_calendar"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_week_ahead_action(self, intent_service, mock_workflow):
        """Test that week_ahead action also routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_ahead",
            context={"original_message": "week ahead"},
        )

        with patch.object(
            intent_service, "_handle_week_calendar_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Week ahead view",
                intent_data={"category": "query", "action": "week_ahead"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_whats_my_week_like_action(self, intent_service, mock_workflow):
        """Test that whats_my_week_like action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="whats_my_week_like",
            context={"original_message": "this week's schedule"},
        )

        with patch.object(
            intent_service, "_handle_week_calendar_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Week schedule view",
                intent_data={"category": "query", "action": "whats_my_week_like"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()


class TestCalendarNotConfiguredGracefulDegradation:
    """Test graceful fallback when Calendar is not configured"""

    @pytest.mark.asyncio
    async def test_meeting_time_returns_graceful_message_when_calendar_not_configured(
        self, intent_service
    ):
        """Test meeting time handler returns helpful message when Calendar not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=False)
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is True
            assert "Calendar isn't configured yet" in result.message
            assert "setup wizard" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_recurring_meetings_returns_graceful_message_when_calendar_not_configured(
        self, intent_service
    ):
        """Test recurring meetings handler returns helpful message when Calendar not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=False)
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is True
            assert "Calendar isn't configured yet" in result.message
            assert "setup wizard" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_week_calendar_returns_graceful_message_when_calendar_not_configured(
        self, intent_service
    ):
        """Test week calendar handler returns helpful message when Calendar not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=False)
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is True
            assert "Calendar isn't configured yet" in result.message
            assert "setup wizard" in result.message
            assert result.implemented is False


class TestMeetingTimeQueryResults:
    """Test meeting time query result formatting"""

    @pytest.mark.asyncio
    async def test_formats_meeting_time_correctly(self, intent_service):
        """Test meeting time is formatted properly"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        mock_events = [
            {
                "id": "event-1",
                "summary": "Team Standup",
                "duration_minutes": 30,
                "is_all_day": False,
            },
            {
                "id": "event-2",
                "summary": "Project Review",
                "duration_minutes": 60,
                "is_all_day": False,
            },
            {
                "id": "event-3",
                "summary": "Company Holiday",
                "duration_minutes": 0,
                "is_all_day": True,  # Should be excluded
            },
        ]

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(return_value=mock_events)
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is True
            assert "1 hour 30 minutes" in result.message
            assert "2 meetings" in result.message
            assert "Team Standup" in result.message
            assert "Project Review" in result.message
            assert result.intent_data["total_minutes"] == 90
            assert result.intent_data["meeting_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_meetings(self, intent_service):
        """Test handling when no meetings scheduled"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(return_value=[])
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is True
            assert "no meetings scheduled" in result.message.lower()
            assert result.intent_data["total_minutes"] == 0
            assert result.intent_data["meeting_count"] == 0


class TestRecurringMeetingsQueryResults:
    """Test recurring meetings query result formatting"""

    @pytest.mark.asyncio
    async def test_formats_recurring_meetings_correctly(self, intent_service):
        """Test recurring meetings are formatted properly with frequency"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        mock_events = [
            {
                "summary": "Daily Standup",
                "recurrence": ["RRULE:FREQ=DAILY"],
                "start": {"dateTime": "2025-12-26T09:00:00Z"},
                "end": {"dateTime": "2025-12-26T09:30:00Z"},
            },
            {
                "summary": "Weekly Team Sync",
                "recurrence": ["RRULE:FREQ=WEEKLY"],
                "start": {"dateTime": "2025-12-26T14:00:00Z"},
                "end": {"dateTime": "2025-12-26T15:00:00Z"},
            },
        ]

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(return_value=[])
            mock_adapter._service = MagicMock()
            mock_adapter._service.events.return_value.list.return_value.execute.return_value = {
                "items": mock_events
            }
            mock_adapter._calendar_id = "primary"
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is True
            assert "2 found" in result.message
            assert "Daily Standup" in result.message
            assert "Weekly Team Sync" in result.message
            assert "Daily" in result.message
            assert "Weekly" in result.message
            assert result.intent_data["recurring_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_recurring_meetings(self, intent_service):
        """Test handling when no recurring meetings found"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(return_value=[])
            mock_adapter._service = MagicMock()
            mock_adapter._service.events.return_value.list.return_value.execute.return_value = {
                "items": []
            }
            mock_adapter._calendar_id = "primary"
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is True
            assert "No recurring meetings found" in result.message
            assert result.intent_data["recurring_count"] == 0


class TestWeekCalendarQueryResults:
    """Test week calendar query result formatting"""

    @pytest.mark.asyncio
    async def test_formats_week_calendar_correctly(self, intent_service):
        """Test week calendar is formatted properly by day"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        # Mock events for different days
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)

        mock_events = [
            {
                "id": "event-1",
                "summary": "Morning Meeting",
                "start": {"dateTime": now.isoformat() + "Z"},
                "end": {"dateTime": (now + timedelta(hours=1)).isoformat() + "Z"},
            },
            {
                "id": "event-2",
                "summary": "Afternoon Review",
                "start": {"dateTime": tomorrow.isoformat() + "Z"},
                "end": {"dateTime": (tomorrow + timedelta(hours=2)).isoformat() + "Z"},
            },
        ]

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter._service = MagicMock()
            mock_adapter._service.events.return_value.list.return_value.execute.return_value = {
                "items": mock_events
            }
            mock_adapter._calendar_id = "primary"

            # Mock _process_event to return processed events
            def mock_process_event(event):
                start = datetime.fromisoformat(event["start"]["dateTime"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(event["end"]["dateTime"].replace("Z", "+00:00"))
                return {
                    "id": event["id"],
                    "summary": event["summary"],
                    "start_time": start.isoformat(),
                    "end_time": end.isoformat(),
                    "duration_minutes": int((end - start).total_seconds() / 60),
                    "is_all_day": False,
                }

            mock_adapter._process_event = mock_process_event
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is True
            assert "Your Week Ahead" in result.message
            assert "Morning Meeting" in result.message
            assert "Afternoon Review" in result.message
            assert result.intent_data["days_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_events_in_week(self, intent_service):
        """Test handling when no events scheduled for the week"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter._service = MagicMock()
            mock_adapter._service.events.return_value.list.return_value.execute.return_value = {
                "items": []
            }
            mock_adapter._calendar_id = "primary"
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is True
            assert "No events scheduled" in result.message
            assert result.intent_data["days_count"] == 0


class TestCalendarHandlerErrors:
    """Test error handling in Calendar handlers"""

    @pytest.mark.asyncio
    async def test_meeting_time_handles_calendar_error(self, intent_service):
        """Test meeting time handler gracefully handles Calendar API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(
                side_effect=Exception("API connection failed")
            )
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is False
            assert "Unable to fetch meeting time" in result.message
            assert result.error is not None
            assert result.error_type == "CalendarMeetingTimeQueryError"

    @pytest.mark.asyncio
    async def test_recurring_meetings_handles_calendar_error(self, intent_service):
        """Test recurring meetings handler gracefully handles Calendar API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(side_effect=Exception("Rate limit exceeded"))
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is False
            assert "Unable to fetch recurring meetings" in result.message
            assert result.error is not None
            assert result.error_type == "CalendarRecurringMeetingsQueryError"

    @pytest.mark.asyncio
    async def test_week_calendar_handles_calendar_error(self, intent_service):
        """Test week calendar handler gracefully handles Calendar API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter._service = MagicMock()
            mock_adapter._service.events.return_value.list.return_value.execute.side_effect = (
                Exception("Network timeout")
            )
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is False
            assert "Unable to fetch week calendar" in result.message
            assert result.error is not None
            assert result.error_type == "CalendarWeekQueryError"


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)"""

    def test_meeting_time_query_routes_to_query_category(self):
        """Test 'how much time in meetings' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("how much time in meetings")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "meeting_time_query"
        assert result.confidence == 1.0

    def test_meeting_time_query_variants(self):
        """Test meeting time query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "how much time in meetings",
            "how much time in meetings today",
            "time spent in meetings",
            "meeting time today",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "meeting_time_query", f"Wrong action for: {query}"

    def test_recurring_meetings_query_routes_to_query_category(self):
        """Test 'review my recurring meetings' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("review my recurring meetings")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "recurring_meetings_query"
        assert result.confidence == 1.0

    def test_recurring_meetings_query_variants(self):
        """Test recurring meetings query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "review my recurring meetings",
            "show recurring meetings",
            "audit my standing meetings",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "recurring_meetings_query", f"Wrong action for: {query}"

    def test_week_calendar_query_routes_to_query_category(self):
        """Test 'what's my week look like' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("what's my week look like")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "week_calendar_query"
        assert result.confidence == 1.0

    def test_week_calendar_query_variants(self):
        """Test week calendar query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "what's my week look like",
            "show me my week",
            "week ahead",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "week_calendar_query", f"Wrong action for: {query}"

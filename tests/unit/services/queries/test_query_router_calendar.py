"""
Unit tests for calendar query routing (Issue #589)

Tests that calendar queries route to QUERY/meeting_time instead of TEMPORAL,
ensuring the timezone-aware calendar adapter (#586) is invoked.
"""

from unittest.mock import MagicMock

import pytest

from services.queries.query_router import QueryRouter
from services.shared_types import IntentCategory


class TestCalendarQueryRouting:
    """Issue #589: Calendar queries should route to QUERY category"""

    @pytest.fixture
    def router(self):
        """Create QueryRouter instance for testing with mocked dependencies"""
        return QueryRouter(
            project_query_service=MagicMock(),
            conversation_query_service=MagicMock(),
            file_query_service=MagicMock(),
            test_mode=True,
        )

    # Calendar query tests - should route to QUERY/meeting_time

    def test_whats_on_my_calendar_routes_to_query(self, router):
        """'What's on my calendar today?' should route to QUERY"""
        intent = router._rule_based_classification(
            "What's on my calendar today?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.QUERY
        assert intent.action == "meeting_time"
        assert intent.context.get("calendar_query") is True
        assert intent.context.get("rule_based") is True

    def test_meetings_today_routes_to_query(self, router):
        """'Do I have any meetings today?' should route to QUERY"""
        intent = router._rule_based_classification(
            "Do I have any meetings today?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.QUERY
        assert intent.action == "meeting_time"

    def test_do_i_have_meetings_routes_to_query(self, router):
        """'Do I have meetings?' should route to QUERY"""
        intent = router._rule_based_classification(
            "Do I have meetings?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.QUERY
        assert intent.action == "meeting_time"

    def test_my_schedule_today_routes_to_query(self, router):
        """'What's my schedule today?' should route to QUERY"""
        intent = router._rule_based_classification(
            "What's my schedule today?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.QUERY
        assert intent.action == "meeting_time"

    def test_what_meetings_do_i_have_routes_to_query(self, router):
        """'What meetings do I have?' should route to QUERY"""
        intent = router._rule_based_classification(
            "What meetings do I have?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.QUERY
        assert intent.action == "meeting_time"

    # Regression tests - temporal queries should still route to TEMPORAL

    def test_what_time_is_it_still_routes_to_temporal(self, router):
        """Regression: 'What time is it?' should still route to TEMPORAL"""
        intent = router._rule_based_classification(
            "What time is it?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.TEMPORAL
        assert intent.action == "get_temporal_context"

    def test_what_day_is_it_still_routes_to_temporal(self, router):
        """Regression: 'What day is it?' should still route to TEMPORAL"""
        intent = router._rule_based_classification(
            "What day is it?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.TEMPORAL
        assert intent.action == "get_temporal_context"

    def test_current_date_still_routes_to_temporal(self, router):
        """Regression: 'What's the current date?' should still route to TEMPORAL"""
        intent = router._rule_based_classification(
            "What's the current date?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.TEMPORAL
        assert intent.action == "get_temporal_context"

    # Edge cases

    def test_calendar_case_insensitive(self, router):
        """Calendar queries should be case insensitive"""
        intent = router._rule_based_classification(
            "WHAT'S ON MY CALENDAR TODAY?",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.QUERY
        assert intent.action == "meeting_time"

    def test_calendar_with_extra_whitespace(self, router):
        """Calendar queries should handle extra whitespace"""
        intent = router._rule_based_classification(
            "  what's on my calendar today?  ",
            user_context=None,
            session_id="test-session",
        )

        assert intent.category == IntentCategory.QUERY
        assert intent.action == "meeting_time"

"""
Tests for Issue #901: Intent classifier keyword disambiguation.

5 queries were misrouted due to keyword collisions in the pre-classifier.
These tests verify the fixes:
- Q27: "Tell me more about the GitHub integration" → query (not identity)
- Q33: "Find time for a 1:1 with the team lead" → query (not temporal)
- Q40: "Update the project roadmap document" → query (not portfolio)
- Q43: "What's blocking the milestone?" → analysis (not status)
- Q62: "Check my calendar for conflicts" → query (not temporal)
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestKeywordDisambiguationQ27:
    """Q27: Feature/integration info queries → QUERY, not IDENTITY."""

    def test_github_integration_routes_to_query(self):
        result = PreClassifier.pre_classify("Tell me more about the GitHub integration")
        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "get_feature_info"

    def test_slack_integration_routes_to_query(self):
        result = PreClassifier.pre_classify("Tell me about the Slack integration")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_calendar_feature_routes_to_query(self):
        result = PreClassifier.pre_classify(
            "Tell me more about the calendar integration"
        )
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_notion_integration_routes_to_query(self):
        result = PreClassifier.pre_classify("Tell me about Notion")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_tell_me_about_yourself_still_identity(self):
        """Regression: 'Tell me about yourself' must stay IDENTITY."""
        result = PreClassifier.pre_classify("Tell me about yourself")
        assert result is not None
        assert result.category == IntentCategory.IDENTITY

    def test_who_are_you_still_identity(self):
        """Regression: Standard identity queries unchanged."""
        result = PreClassifier.pre_classify("Who are you?")
        assert result is not None
        assert result.category == IntentCategory.IDENTITY


class TestKeywordDisambiguationQ33:
    """Q33: Scheduling/availability queries → QUERY (calendar), not TEMPORAL."""

    def test_find_time_for_1on1_routes_to_query(self):
        result = PreClassifier.pre_classify("Find time for a 1:1 with the team lead")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_schedule_meeting_routes_to_query(self):
        result = PreClassifier.pre_classify("Schedule a 1:1 with Sarah")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_book_meeting_routes_to_query(self):
        result = PreClassifier.pre_classify("Book a time for our sync")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_what_time_still_temporal(self):
        """Regression: Pure time queries must stay TEMPORAL."""
        result = PreClassifier.pre_classify("What time is it?")
        assert result is not None
        assert result.category == IntentCategory.TEMPORAL


class TestKeywordDisambiguationQ40:
    """Q40: Document update queries → QUERY, not PORTFOLIO."""

    def test_update_document_routes_to_query(self):
        result = PreClassifier.pre_classify("Update the project roadmap document")
        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "update_document_query"

    def test_archive_project_still_portfolio(self):
        """Regression: Portfolio operations unchanged."""
        result = PreClassifier.pre_classify("Archive my project")
        assert result is not None
        assert result.category == IntentCategory.PORTFOLIO


class TestKeywordDisambiguationQ43:
    """Q43: Blocker/analysis queries → ANALYSIS, not STATUS."""

    def test_whats_blocking_routes_to_analysis(self):
        result = PreClassifier.pre_classify("What's blocking the milestone?")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS
        assert result.action == "analyze_blockers"

    def test_what_is_blocking_routes_to_analysis(self):
        result = PreClassifier.pre_classify("What is blocking the release?")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS

    def test_blockers_for_routes_to_analysis(self):
        result = PreClassifier.pre_classify("What are the blockers for the sprint?")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS

    def test_risk_assessment_routes_to_analysis(self):
        result = PreClassifier.pre_classify("I need a risk assessment")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS

    def test_project_status_still_status(self):
        """Regression: Status queries unchanged."""
        result = PreClassifier.pre_classify("What's the project status?")
        assert result is not None
        assert result.category == IntentCategory.STATUS


class TestKeywordDisambiguationQ62:
    """Q62: Calendar conflict/check queries → QUERY, not TEMPORAL."""

    def test_check_calendar_conflicts_routes_to_query(self):
        result = PreClassifier.pre_classify("Check my calendar for conflicts")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_calendar_conflicts_routes_to_query(self):
        result = PreClassifier.pre_classify("Any calendar conflicts this week?")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_calendar_overlap_routes_to_query(self):
        result = PreClassifier.pre_classify("Check for calendar overlaps")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_whats_on_calendar_still_query(self):
        """Regression: Existing calendar queries unchanged."""
        result = PreClassifier.pre_classify("What's on my calendar today?")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_what_day_still_temporal(self):
        """Regression: Pure temporal queries unchanged."""
        result = PreClassifier.pre_classify("What day is it?")
        assert result is not None
        assert result.category == IntentCategory.TEMPORAL

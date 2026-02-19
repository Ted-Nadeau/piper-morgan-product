"""
Colleague Test for multi-intent orchestration.

Issue #764: GLUE-MULTIINTENT — Multi-Intent Handling Enhancements
Phase 4: Colleague Test + Regression

The Colleague Test: "Would a competent colleague respond this way?"

Tests verify the system behaves like a helpful human colleague:
- Scenario 1: Two queries → both answered in one response
- Scenario 2: Status + priority → combined status report
- Scenario 3: Greeting + two substantive → greeting + both answers
- Scenario 4: Single intent → unchanged (no regression)
- Scenario 5: Three intents → all three processed
- Scenario 6: Partial failure → successes returned, failure noted
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent_service.orchestrator import (
    ExecutionPlan,
    IntentExecutionResult,
    IntentOrchestrator,
    OrchestratedResponse,
)
from services.intent_service.pre_classifier import MultiIntentResult
from services.shared_types import IntentCategory


def _make_intent(category: IntentCategory, action: str) -> Intent:
    return Intent(category=category, action=action, confidence=1.0)


@pytest.fixture
def mock_handlers():
    handlers = MagicMock()
    handlers.can_handle = MagicMock(return_value=True)
    handlers.handle = AsyncMock()
    return handlers


@pytest.fixture
def orchestrator(mock_handlers):
    return IntentOrchestrator(canonical_handlers=mock_handlers)


class TestColleagueScenarios:
    """
    Each scenario simulates a realistic user conversation.
    The key question: would a competent colleague respond this way?
    """

    @pytest.mark.asyncio
    async def test_scenario_1_two_queries_both_answered(self, orchestrator, mock_handlers):
        """
        User: "What's on my calendar, and did the PR get merged?"
        Colleague: "Your next meeting is at 2pm. As for GitHub, the PR was merged."

        NOT: Only answers calendar, ignores PR question.
        """
        call_count = 0

        async def multi_handle(intent, session_id, user_id=None):
            nonlocal call_count
            call_count += 1
            if intent.action == "meeting_time":
                return {
                    "message": "Your next meeting is at 2pm.",
                    "intent": {"category": "query", "action": "meeting_time"},
                }
            else:
                return {
                    "message": "The PR was merged yesterday.",
                    "intent": {"category": "query", "action": "github_query"},
                }

        mock_handlers.handle = multi_handle

        multi = MultiIntentResult(
            intents=[
                _make_intent(IntentCategory.QUERY, "meeting_time"),
                _make_intent(IntentCategory.QUERY, "github_query"),
            ],
            original_message="What's on my calendar, and did the PR get merged?",
            is_multi_intent=True,
        )

        plan = orchestrator.create_plan(multi)
        response = await orchestrator.execute_plan(plan, "sess1", "user1")

        # Both queries should be answered
        assert call_count == 2
        assert "2pm" in response.aggregated_message
        assert "merged" in response.aggregated_message
        assert len(response.successful_results) > 0
        assert not response.has_partial_failure

    @pytest.mark.asyncio
    async def test_scenario_2_status_and_priority(self, orchestrator, mock_handlers):
        """
        User: "Update the sprint status and check if we're on track for the deadline"
        Colleague: "Sprint is 80% complete. As for priorities, we're on track for Friday."

        NOT: Only answers sprint status, ignores deadline question.
        """

        async def multi_handle(intent, session_id, user_id=None):
            if intent.action == "get_project_status":
                return {
                    "message": "Sprint is 80% complete with 4 stories remaining.",
                    "intent": {"category": "status", "action": "get_project_status"},
                }
            else:
                return {
                    "message": "We're on track for the Friday deadline.",
                    "intent": {"category": "priority", "action": "get_top_priority"},
                }

        mock_handlers.handle = multi_handle

        multi = MultiIntentResult(
            intents=[
                _make_intent(IntentCategory.STATUS, "get_project_status"),
                _make_intent(IntentCategory.PRIORITY, "get_top_priority"),
            ],
            original_message="Update the sprint status and check if we're on track",
            is_multi_intent=True,
        )

        plan = orchestrator.create_plan(multi)
        response = await orchestrator.execute_plan(plan, "sess1", "user1")

        assert "80%" in response.aggregated_message
        assert "Friday" in response.aggregated_message

    @pytest.mark.asyncio
    async def test_scenario_3_greeting_plus_two_substantive(self, orchestrator, mock_handlers):
        """
        User: "Hi! What's on my agenda and any PRs to review?"
        Colleague: "Hi there! Your next meeting is at 2pm. As for GitHub, you have 3 PRs."

        NOT: "Hi there!" then only one answer.
        """

        async def multi_handle(intent, session_id, user_id=None):
            if intent.category == IntentCategory.CONVERSATION:
                return {
                    "message": "Hello!",
                    "intent": {"category": "conversation", "action": "greeting"},
                }
            elif intent.action == "meeting_time":
                return {
                    "message": "Your next meeting is at 2pm.",
                    "intent": {"category": "query", "action": "meeting_time"},
                }
            else:
                return {
                    "message": "You have 3 PRs waiting for review.",
                    "intent": {"category": "query", "action": "github_query"},
                }

        mock_handlers.handle = multi_handle

        multi = MultiIntentResult(
            intents=[
                _make_intent(IntentCategory.CONVERSATION, "greeting"),
                _make_intent(IntentCategory.QUERY, "meeting_time"),
                _make_intent(IntentCategory.QUERY, "github_query"),
            ],
            original_message="Hi! What's on my agenda and any PRs to review?",
            is_multi_intent=True,
        )

        plan = orchestrator.create_plan(multi)
        response = await orchestrator.execute_plan(plan, "sess1", "user1")

        # Should have greeting + both answers
        assert "Hi there!" in response.aggregated_message
        assert "2pm" in response.aggregated_message
        assert "3 PRs" in response.aggregated_message

    @pytest.mark.asyncio
    async def test_scenario_4_single_intent_unchanged(self, orchestrator, mock_handlers):
        """
        User: "What's on my calendar?"
        Colleague: "Your next meeting is at 2pm."

        Single intent should work exactly as before — no regression.
        """
        mock_handlers.handle = AsyncMock(
            return_value={
                "message": "Your next meeting is at 2pm.",
                "intent": {"category": "query", "action": "meeting_time"},
            }
        )

        multi = MultiIntentResult(
            intents=[_make_intent(IntentCategory.QUERY, "meeting_time")],
            original_message="What's on my calendar?",
            is_multi_intent=False,
        )

        plan = orchestrator.create_plan(multi)
        response = await orchestrator.execute_plan(plan, "sess1", "user1")

        assert response.aggregated_message == "Your next meeting is at 2pm."
        assert not response.has_partial_failure

    @pytest.mark.asyncio
    async def test_scenario_5_three_intents_all_processed(self, orchestrator, mock_handlers):
        """
        User: "Calendar, sprint status, and top priorities please"
        Colleague: "Next meeting at 2pm. Sprint is 80% done. Top priority is the API migration."

        NOT: Only answers one or two of three.
        """
        responses = {
            "meeting_time": "Next meeting at 2pm.",
            "get_project_status": "Sprint is 80% done.",
            "get_top_priority": "Top priority is the API migration.",
        }

        async def multi_handle(intent, session_id, user_id=None):
            return {
                "message": responses[intent.action],
                "intent": {"category": intent.category.value, "action": intent.action},
            }

        mock_handlers.handle = multi_handle

        multi = MultiIntentResult(
            intents=[
                _make_intent(IntentCategory.QUERY, "meeting_time"),
                _make_intent(IntentCategory.STATUS, "get_project_status"),
                _make_intent(IntentCategory.PRIORITY, "get_top_priority"),
            ],
            original_message="Calendar, sprint status, and priorities",
            is_multi_intent=True,
        )

        plan = orchestrator.create_plan(multi)
        response = await orchestrator.execute_plan(plan, "sess1", "user1")

        assert len(response.successful_results) == 3
        assert "2pm" in response.aggregated_message
        assert "80%" in response.aggregated_message
        assert "API migration" in response.aggregated_message

    @pytest.mark.asyncio
    async def test_scenario_6_partial_failure_graceful(self, orchestrator, mock_handlers):
        """
        User: "Check calendar and sprint status"
        Colleague: "Your next meeting is at 2pm. I wasn't able to check on project status right now."

        NOT: Complete failure because one part failed.
        NOT: Silently ignoring the failed part.
        """

        async def failing_handle(intent, session_id, user_id=None):
            if intent.action == "meeting_time":
                return {
                    "message": "Your next meeting is at 2pm.",
                    "intent": {"category": "query", "action": "meeting_time"},
                }
            else:
                raise RuntimeError("Status service unavailable")

        mock_handlers.handle = failing_handle

        multi = MultiIntentResult(
            intents=[
                _make_intent(IntentCategory.QUERY, "meeting_time"),
                _make_intent(IntentCategory.STATUS, "get_project_status"),
            ],
            original_message="Check calendar and sprint status",
            is_multi_intent=True,
        )

        plan = orchestrator.create_plan(multi)
        response = await orchestrator.execute_plan(plan, "sess1", "user1")

        # Successful part should be included
        assert "2pm" in response.aggregated_message
        # Failure should be acknowledged gracefully
        assert "wasn't able" in response.aggregated_message
        # Overall should still have successes (partial)
        assert len(response.successful_results) > 0
        assert response.has_partial_failure

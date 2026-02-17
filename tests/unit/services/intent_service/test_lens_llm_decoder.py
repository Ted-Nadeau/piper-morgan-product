"""
Tests for LLM Lens Decoder (#763 GLUE-FOLLOWUP Phase 3).

Tests the LLM-based follow-up decoder for complex follow-ups that
rule-based patterns can't handle. Uses mocked LLM responses.
"""

import json
from unittest.mock import AsyncMock

import pytest

from services.domain.models import Intent
from services.intent_service.conversation_context import ConversationContext, ConversationTurn
from services.intent_service.lens_inference import (
    _format_conversation_history,
    decode_follow_up_with_llm,
    should_try_llm_decoder,
)
from services.shared_types import ConversationalLens, IntentCategory


class TestShouldTryLlmDecoder:
    """Test the heuristic for when to invoke the LLM decoder."""

    def test_try_with_lens_and_short_message(self):
        assert should_try_llm_decoder("And Sarah?", ConversationalLens.PROJECTS) is True

    def test_skip_without_lens(self):
        assert should_try_llm_decoder("And Sarah?", None) is False

    def test_skip_long_message(self):
        long_msg = "Can you show me all the issues that are currently open and assigned to me?"
        assert should_try_llm_decoder(long_msg, ConversationalLens.ISSUES) is False

    def test_skip_greeting(self):
        assert should_try_llm_decoder("Hello there!", ConversationalLens.CALENDAR) is False

    def test_skip_identity_query(self):
        assert should_try_llm_decoder("What's your name?", ConversationalLens.CALENDAR) is False

    def test_try_elliptical(self):
        assert should_try_llm_decoder("And Jake?", ConversationalLens.ISSUES) is True

    def test_try_action_shift(self):
        assert should_try_llm_decoder("Cancel the 2pm", ConversationalLens.CALENDAR) is True

    def test_try_lens_shift(self):
        assert should_try_llm_decoder("Who's attending?", ConversationalLens.CALENDAR) is True

    def test_try_comparative(self):
        assert should_try_llm_decoder("How about P2 instead?", ConversationalLens.ISSUES) is True


class TestFormatConversationHistory:
    """Test conversation history formatting for the prompt."""

    def test_formats_single_turn(self):
        ctx = ConversationContext()
        ctx.add_turn(
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        result = _format_conversation_history(ctx.turns)
        assert 'Turn 1: "What\'s on my calendar?"' in result
        assert "(action: meeting_time)" in result
        assert "[lens: calendar]" in result

    def test_formats_multiple_turns(self):
        ctx = ConversationContext()
        ctx.add_turn(message="First", intent=Intent(category=IntentCategory.QUERY, action="a"))
        ctx.add_turn(message="Second", intent=Intent(category=IntentCategory.QUERY, action="b"))
        result = _format_conversation_history(ctx.turns)
        assert "Turn 1" in result
        assert "Turn 2" in result

    def test_limits_to_max_turns(self):
        ctx = ConversationContext()
        for i in range(5):
            ctx.add_turn(
                message=f"Message {i}",
                intent=Intent(category=IntentCategory.QUERY, action=f"action_{i}"),
            )
        result = _format_conversation_history(ctx.turns, max_turns=2)
        # Should only have the last 2 turns, re-numbered as Turn 1, Turn 2
        lines = result.strip().split("\n")
        assert len(lines) == 2
        assert "action_3" in lines[0]  # Turn index 3 (4th message)
        assert "action_4" in lines[1]  # Turn index 4 (5th message)


class TestDecodeFollowUpWithLlm:
    """Test the LLM decoder with mocked LLM responses."""

    def _make_context_with_calendar(self) -> ConversationContext:
        """Helper: create context with a calendar turn."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="What's on my calendar tomorrow?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            temporal_reference="tomorrow",
            lens=ConversationalLens.CALENDAR,
        )
        return ctx

    def _make_context_with_issues(self) -> ConversationContext:
        """Helper: create context with an issues turn."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Show me my open issues",
            intent=Intent(category=IntentCategory.QUERY, action="list_issues"),
            lens=ConversationalLens.ISSUES,
        )
        return ctx

    def _make_context_with_projects(self) -> ConversationContext:
        """Helper: create context with a project status turn."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="How's the Alpha project going?",
            intent=Intent(category=IntentCategory.STATUS, action="project_status"),
            entity_references=["Alpha"],
            lens=ConversationalLens.PROJECTS,
        )
        return ctx

    @pytest.mark.asyncio
    async def test_elliptical_and_sarah(self):
        """'And Sarah?' after project status → person in project context."""
        ctx = self._make_context_with_projects()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "status",
                "action": "project_status",
                "lens": "projects",
                "entities": ["Sarah"],
                "reasoning": "User asking about Sarah's role in the project",
            }
        )

        result = await decode_follow_up_with_llm(
            message="And Sarah?",
            turns=ctx.turns,
            current_lens=ConversationalLens.PROJECTS,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.category == IntentCategory.STATUS
        assert result.action == "project_status"
        assert result.context["inherited_lens"] == "projects"
        assert "Sarah" in result.context["entities"]

    @pytest.mark.asyncio
    async def test_lens_shift_whos_attending(self):
        """'Who's attending the standup?' → calendar.attendance."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "query",
                "action": "meeting_attendance",
                "lens": "calendar",
                "entities": ["standup"],
                "reasoning": "User asking about attendance for a meeting shown in calendar",
            }
        )

        result = await decode_follow_up_with_llm(
            message="Who's attending the standup?",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "meeting_attendance"
        assert result.context["inherited_lens"] == "calendar"

    @pytest.mark.asyncio
    async def test_action_shift_cancel(self):
        """'Cancel the 2pm' → execution within calendar lens."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "execution",
                "action": "cancel_meeting",
                "lens": "calendar",
                "entities": ["2pm meeting"],
                "reasoning": "User wants to cancel a meeting from the calendar view",
            }
        )

        result = await decode_follow_up_with_llm(
            message="Cancel the 2pm",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.category == IntentCategory.EXECUTION
        assert result.action == "cancel_meeting"

    @pytest.mark.asyncio
    async def test_parameter_mod_closed_ones(self):
        """'And the closed ones?' → filter change within issues lens."""
        ctx = self._make_context_with_issues()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "query",
                "action": "list_issues",
                "lens": "issues",
                "entities": [],
                "reasoning": "User wants to see closed issues instead of open ones",
            }
        )

        result = await decode_follow_up_with_llm(
            message="And the closed ones?",
            turns=ctx.turns,
            current_lens=ConversationalLens.ISSUES,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.action == "list_issues"
        assert result.context["inherited_lens"] == "issues"

    @pytest.mark.asyncio
    async def test_comparative_query(self):
        """'Compare that with Jake's' → comparison within people lens."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="What's Sarah's workload like?",
            intent=Intent(category=IntentCategory.QUERY, action="person_workload"),
            lens=ConversationalLens.PEOPLE,
        )
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "query",
                "action": "compare_workload",
                "lens": "people",
                "entities": ["Jake", "Sarah"],
                "reasoning": "User comparing workloads between Sarah and Jake",
            }
        )

        result = await decode_follow_up_with_llm(
            message="Compare that with Jake's",
            turns=ctx.turns,
            current_lens=ConversationalLens.PEOPLE,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.context["inherited_lens"] == "people"

    @pytest.mark.asyncio
    async def test_not_a_follow_up(self):
        """LLM says it's not a follow-up → returns None."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": False,
            }
        )

        result = await decode_follow_up_with_llm(
            message="Show me my open issues",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_llm_returns_garbage(self):
        """LLM returns unparseable response → returns None gracefully."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = "I don't understand what you're asking."

        result = await decode_follow_up_with_llm(
            message="And Sarah?",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_llm_raises_exception(self):
        """LLM call fails → returns None gracefully."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.side_effect = Exception("API timeout")

        result = await decode_follow_up_with_llm(
            message="And Sarah?",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_invalid_category_falls_back_to_query(self):
        """LLM returns invalid category → falls back to QUERY."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "invalid_category",
                "action": "test",
                "lens": "calendar",
            }
        )

        result = await decode_follow_up_with_llm(
            message="Something?",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.category == IntentCategory.QUERY

    @pytest.mark.asyncio
    async def test_confidence_is_085(self):
        """LLM-decoded intents should have 0.85 confidence."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "query",
                "action": "test",
                "lens": "calendar",
            }
        )

        result = await decode_follow_up_with_llm(
            message="Something?",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.confidence == 0.85

    @pytest.mark.asyncio
    async def test_follow_up_type_is_llm_decoded(self):
        """LLM-decoded intents should be tagged as 'llm_decoded'."""
        ctx = self._make_context_with_calendar()
        mock_llm = AsyncMock()
        mock_llm.complete.return_value = json.dumps(
            {
                "is_follow_up": True,
                "category": "query",
                "action": "test",
                "lens": "calendar",
            }
        )

        result = await decode_follow_up_with_llm(
            message="Something?",
            turns=ctx.turns,
            current_lens=ConversationalLens.CALENDAR,
            llm_service=mock_llm,
        )

        assert result is not None
        assert result.context["follow_up_type"] == "llm_decoded"

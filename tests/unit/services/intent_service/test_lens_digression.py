"""
Tests for lens digression flow (#827 GLUE-LENSSTACK).

Tests the push_lens/pop_lens trigger logic added to classifier.py.
These simulate the exact branch conditions in classify_conscious:

    if is_lens_reset(lens, current_lens, intent):
        conv_context.reset_lens()
    elif lens and current_lens and lens != current_lens:
        if lens in conv_context.lens_stack:
            # Returning from digression — pop back
        else:
            # New digression — push current lens

Unit tests for stack operations themselves are in test_lens_edge_cases.py.
"""

import pytest

from services.domain.models import Intent
from services.intent_service.conversation_context import ConversationContext
from services.intent_service.lens_inference import is_lens_reset
from services.shared_types import ConversationalLens, IntentCategory


def _simulate_classifier_lens_logic(
    conv_context: ConversationContext,
    message: str,
    intent: Intent,
    lens: str | None,
) -> None:
    """
    Replicate the exact lens tracking logic from classifier.py lines 520-543.

    This avoids needing the full classifier + LLM mock while exercising
    the same branch conditions.
    """
    current_lens = conv_context.current_lens

    if is_lens_reset(lens, current_lens, intent):
        conv_context.reset_lens()
    elif lens and current_lens and lens != current_lens:
        if lens in conv_context.lens_stack:
            # Returning to a previous topic — pop back to it
            while conv_context.lens_stack and conv_context.lens_stack[-1] != lens:
                conv_context.pop_lens()
            # Pop the matching entry itself (it becomes current via add_turn)
            conv_context.pop_lens()
        else:
            # New sub-topic digression — save current lens for later
            conv_context.push_lens(lens)

    conv_context.add_turn(
        message=message,
        intent=intent,
        lens=lens,
    )


class TestDigressionPushLens:
    """Test that sub-topic digressions push the current lens onto the stack."""

    def test_follow_up_to_different_lens_pushes(self):
        """Calendar → 'who's attending?' (PEOPLE follow-up) → pushes CALENDAR."""
        ctx = ConversationContext()
        # Turn 1: calendar query
        _simulate_classifier_lens_logic(
            ctx,
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        assert ctx.current_lens == ConversationalLens.CALENDAR
        assert ctx.lens_stack == []

        # Turn 2: follow-up that shifts to PEOPLE lens
        _simulate_classifier_lens_logic(
            ctx,
            message="Who's attending the standup?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_attendance",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.PEOPLE,
        )
        assert ctx.current_lens == ConversationalLens.PEOPLE
        assert ctx.lens_stack == [ConversationalLens.CALENDAR]

    def test_same_lens_follow_up_does_not_push(self):
        """Calendar → 'how about tomorrow?' (CALENDAR follow-up) → no push."""
        ctx = ConversationContext()
        _simulate_classifier_lens_logic(
            ctx,
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        _simulate_classifier_lens_logic(
            ctx,
            message="How about tomorrow?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                context={"follow_up_type": "temporal_shift"},
            ),
            lens=ConversationalLens.CALENDAR,
        )
        assert ctx.current_lens == ConversationalLens.CALENDAR
        assert ctx.lens_stack == []

    def test_no_lens_turn_does_not_push(self):
        """Calendar → 'yes' (no lens) → no push."""
        ctx = ConversationContext()
        _simulate_classifier_lens_logic(
            ctx,
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        _simulate_classifier_lens_logic(
            ctx,
            message="Yes",
            intent=Intent(category=IntentCategory.CONVERSATION, action="confirmation"),
            lens=None,
        )
        assert ctx.current_lens == ConversationalLens.CALENDAR
        assert ctx.lens_stack == []


class TestDigressionPopLens:
    """Test that returning from digression pops the stack correctly."""

    def test_return_to_stacked_lens(self):
        """Calendar → People (digression) → Calendar (return) → stack empty."""
        ctx = ConversationContext()
        # Turn 1: Calendar
        _simulate_classifier_lens_logic(
            ctx,
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        # Turn 2: People digression (follow-up, so not a reset)
        _simulate_classifier_lens_logic(
            ctx,
            message="Who's in the standup?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_attendance",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.PEOPLE,
        )
        assert ctx.lens_stack == [ConversationalLens.CALENDAR]

        # Turn 3: Back to calendar (follow-up to earlier context)
        _simulate_classifier_lens_logic(
            ctx,
            message="And what time is the next one?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.CALENDAR,
        )
        assert ctx.current_lens == ConversationalLens.CALENDAR
        assert ctx.lens_stack == []

    def test_deep_digression_return_pops_intermediate(self):
        """Calendar → People → Issues → Calendar → stack fully unwound."""
        ctx = ConversationContext()
        # Turn 1: Calendar
        _simulate_classifier_lens_logic(
            ctx,
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        # Turn 2: People digression
        _simulate_classifier_lens_logic(
            ctx,
            message="Who's attending?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_attendance",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.PEOPLE,
        )
        assert ctx.lens_stack == [ConversationalLens.CALENDAR]

        # Turn 3: Issues digression (nested)
        _simulate_classifier_lens_logic(
            ctx,
            message="What issues are assigned to Sarah?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="list_issues",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.ISSUES,
        )
        assert ctx.lens_stack == [ConversationalLens.CALENDAR, ConversationalLens.PEOPLE]

        # Turn 4: Return to Calendar — should pop PEOPLE and CALENDAR
        _simulate_classifier_lens_logic(
            ctx,
            message="So when's the next meeting?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.CALENDAR,
        )
        assert ctx.current_lens == ConversationalLens.CALENDAR
        assert ctx.lens_stack == []

    def test_partial_return_preserves_deeper_stack(self):
        """Calendar → People → Issues → People (return) → Calendar still on stack."""
        ctx = ConversationContext()
        # Build: Calendar → People → Issues
        _simulate_classifier_lens_logic(
            ctx,
            message="Calendar query",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        _simulate_classifier_lens_logic(
            ctx,
            message="People digression",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_attendance",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.PEOPLE,
        )
        _simulate_classifier_lens_logic(
            ctx,
            message="Issues digression",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="list_issues",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.ISSUES,
        )
        assert ctx.lens_stack == [ConversationalLens.CALENDAR, ConversationalLens.PEOPLE]

        # Return to People (partial return — only pops Issues level)
        _simulate_classifier_lens_logic(
            ctx,
            message="Tell me more about Sarah",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="team_member_info",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.PEOPLE,
        )
        assert ctx.current_lens == ConversationalLens.PEOPLE
        assert ctx.lens_stack == [ConversationalLens.CALENDAR]


class TestResetClearsStack:
    """Test that explicit topic changes (resets) clear the stack."""

    def test_explicit_reset_clears_stack(self):
        """Calendar → People (digression) → Issues (explicit new topic) → stack cleared."""
        ctx = ConversationContext()
        # Build: Calendar → People digression
        _simulate_classifier_lens_logic(
            ctx,
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        _simulate_classifier_lens_logic(
            ctx,
            message="Who's attending?",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_attendance",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.PEOPLE,
        )
        assert ctx.lens_stack == [ConversationalLens.CALENDAR]

        # Explicit new topic (no follow_up_type → is_lens_reset returns True)
        _simulate_classifier_lens_logic(
            ctx,
            message="Show me my open issues",
            intent=Intent(category=IntentCategory.QUERY, action="list_issues"),
            lens=ConversationalLens.ISSUES,
        )
        assert ctx.current_lens == ConversationalLens.ISSUES
        assert ctx.lens_stack == []

    def test_reset_from_deep_stack(self):
        """Deep stack + explicit topic change → all cleared."""
        ctx = ConversationContext()
        # Build deep stack
        _simulate_classifier_lens_logic(
            ctx,
            message="Calendar",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        _simulate_classifier_lens_logic(
            ctx,
            message="People digression",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="meeting_attendance",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.PEOPLE,
        )
        _simulate_classifier_lens_logic(
            ctx,
            message="Issues digression",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="list_issues",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.ISSUES,
        )
        assert len(ctx.lens_stack) == 2

        # Explicit switch to PROJECTS (no follow_up_type)
        _simulate_classifier_lens_logic(
            ctx,
            message="Show me project status",
            intent=Intent(category=IntentCategory.STATUS, action="get_project_status"),
            lens=ConversationalLens.PROJECTS,
        )
        assert ctx.current_lens == ConversationalLens.PROJECTS
        assert ctx.lens_stack == []


class TestGeneralLensDigression:
    """Test GENERAL lens behavior in digression context."""

    def test_general_lens_digression_pushes(self):
        """Calendar → GENERAL follow-up → pushes Calendar."""
        ctx = ConversationContext()
        _simulate_classifier_lens_logic(
            ctx,
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        # GENERAL lens follow-up (e.g., "tell me more about that")
        _simulate_classifier_lens_logic(
            ctx,
            message="Tell me more about that",
            intent=Intent(
                category=IntentCategory.QUERY,
                action="detail_query",
                context={"follow_up_type": "llm_decoded"},
            ),
            lens=ConversationalLens.GENERAL,
        )
        # GENERAL != CALENDAR and is_lens_reset returns False (GENERAL special case)
        # so this pushes CALENDAR
        assert ctx.lens_stack == [ConversationalLens.CALENDAR]

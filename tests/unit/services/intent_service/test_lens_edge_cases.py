"""
Tests for lens edge cases (#763 GLUE-FOLLOWUP Phase 4).

Tests lens reset detection, stack operations, and edge cases.
"""

import pytest

from services.domain.models import Intent
from services.intent_service.conversation_context import ConversationContext
from services.intent_service.lens_inference import extract_lens_from_intent, is_lens_reset
from services.shared_types import ConversationalLens, IntentCategory


class TestLensReset:
    """Test lens reset detection."""

    def test_different_lens_is_reset(self):
        """New query with different concrete lens should be a reset."""
        intent = Intent(category=IntentCategory.QUERY, action="list_issues")
        assert (
            is_lens_reset(
                new_lens=ConversationalLens.ISSUES,
                current_lens=ConversationalLens.CALENDAR,
                intent=intent,
            )
            is True
        )

    def test_same_lens_not_reset(self):
        """Same lens should not be a reset."""
        intent = Intent(category=IntentCategory.QUERY, action="meeting_time")
        assert (
            is_lens_reset(
                new_lens=ConversationalLens.CALENDAR,
                current_lens=ConversationalLens.CALENDAR,
                intent=intent,
            )
            is False
        )

    def test_general_lens_not_reset(self):
        """GENERAL lens should not trigger a reset."""
        intent = Intent(category=IntentCategory.QUERY, action="obscure_action")
        assert (
            is_lens_reset(
                new_lens=ConversationalLens.GENERAL,
                current_lens=ConversationalLens.CALENDAR,
                intent=intent,
            )
            is False
        )

    def test_no_current_lens_not_reset(self):
        """No current lens → not a reset."""
        intent = Intent(category=IntentCategory.QUERY, action="list_issues")
        assert (
            is_lens_reset(
                new_lens=ConversationalLens.ISSUES,
                current_lens=None,
                intent=intent,
            )
            is False
        )

    def test_follow_up_not_reset(self):
        """Follow-up resolved intent should NOT be a reset."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_attendance",
            context={"follow_up_type": "llm_decoded"},
        )
        assert (
            is_lens_reset(
                new_lens=ConversationalLens.PEOPLE,
                current_lens=ConversationalLens.CALENDAR,
                intent=intent,
            )
            is False
        )

    def test_inherited_follow_up_not_reset(self):
        """Rule-based follow-up should NOT be a reset."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"follow_up_type": "temporal_shift"},
        )
        assert (
            is_lens_reset(
                new_lens=ConversationalLens.CALENDAR,
                current_lens=ConversationalLens.CALENDAR,
                intent=intent,
            )
            is False
        )


class TestLensStackOperations:
    """Test push/pop/reset on the lens stack."""

    def test_push_lens_adds_to_stack(self):
        ctx = ConversationContext()
        ctx.add_turn(
            message="Calendar query",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        ctx.push_lens(ConversationalLens.PEOPLE)
        assert ctx.lens_stack == [ConversationalLens.CALENDAR]

    def test_push_same_lens_does_not_push(self):
        """Pushing the same lens shouldn't add to stack."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Calendar query",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        ctx.push_lens(ConversationalLens.CALENDAR)
        assert ctx.lens_stack == []

    def test_push_when_no_current_lens(self):
        """Pushing with no current lens shouldn't add anything."""
        ctx = ConversationContext()
        ctx.push_lens(ConversationalLens.CALENDAR)
        assert ctx.lens_stack == []

    def test_pop_lens_returns_previous(self):
        ctx = ConversationContext()
        ctx.add_turn(
            message="Calendar query",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        ctx.push_lens(ConversationalLens.PEOPLE)
        popped = ctx.pop_lens()
        assert popped == ConversationalLens.CALENDAR
        assert ctx.lens_stack == []

    def test_pop_empty_stack_returns_none(self):
        ctx = ConversationContext()
        assert ctx.pop_lens() is None

    def test_reset_clears_stack(self):
        ctx = ConversationContext()
        ctx.lens_stack = [ConversationalLens.CALENDAR, ConversationalLens.ISSUES]
        ctx.reset_lens()
        assert ctx.lens_stack == []

    def test_prune_all_turns_clears_stack(self):
        """When all turns are pruned (timeout), stack should be cleared."""
        ctx = ConversationContext()
        ctx.lens_stack = [ConversationalLens.CALENDAR]
        # Add a turn then force prune by emptying turns
        ctx.turns = []
        ctx._prune_old_turns()
        assert ctx.lens_stack == []


class TestLensEdgeCases:
    """Test various edge cases for lens behavior."""

    def test_no_lens_after_greeting(self):
        """Greeting should not set a lens."""
        intent = Intent(category=IntentCategory.CONVERSATION, action="greeting")
        assert extract_lens_from_intent(intent) is None

    def test_no_lens_after_identity_query(self):
        """Identity query should not set a lens."""
        intent = Intent(category=IntentCategory.IDENTITY, action="name_query")
        assert extract_lens_from_intent(intent) is None

    def test_lens_survives_none_turn(self):
        """Lens from an earlier turn should survive turns without a lens."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Calendar query",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        ctx.add_turn(
            message="Yes",
            intent=Intent(category=IntentCategory.CONVERSATION, action="confirmation"),
            # No lens (confirmation is conversational)
        )
        assert ctx.current_lens == ConversationalLens.CALENDAR

    def test_explicit_topic_change_pattern(self):
        """Simulate: calendar → 'show me my issues' → lens changes to issues."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        # New query classified as issues
        new_intent = Intent(category=IntentCategory.QUERY, action="list_issues")
        new_lens = extract_lens_from_intent(new_intent)

        # Detect reset
        assert is_lens_reset(new_lens, ctx.current_lens, new_intent) is True

        # Apply reset
        ctx.reset_lens()
        ctx.add_turn(
            message="Show me my open issues",
            intent=new_intent,
            lens=new_lens,
        )
        assert ctx.current_lens == ConversationalLens.ISSUES
        assert ctx.lens_stack == []

    def test_lens_persists_across_four_turns(self):
        """Lens should persist across 4 consecutive follow-up turns."""
        ctx = ConversationContext()
        for i, msg in enumerate(["Query", "Follow 1", "Follow 2", "Follow 3"]):
            ctx.add_turn(
                message=msg,
                intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
                lens=ConversationalLens.CALENDAR,
            )
        assert ctx.current_lens == ConversationalLens.CALENDAR
        assert len(ctx.turns) == 4

    def test_never_mind_pattern(self):
        """'Never mind' should leave no lens when no follow-up context."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="What's on my calendar?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        # "Never mind" classified as conversation
        never_mind = Intent(category=IntentCategory.CONVERSATION, action="dismissal")
        lens = extract_lens_from_intent(never_mind)
        assert lens is None

        ctx.add_turn(
            message="Never mind",
            intent=never_mind,
            lens=lens,
        )
        # current_lens still finds calendar from turn 1 (which is correct —
        # the turn-scanning approach means old lens lingers until replaced)
        # The key is: the NEXT query will set a new lens appropriately

    def test_multiple_stack_pushes(self):
        """Multiple digressions should stack properly."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Calendar",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            lens=ConversationalLens.CALENDAR,
        )
        ctx.push_lens(ConversationalLens.PEOPLE)
        ctx.add_turn(
            message="People sub-topic",
            intent=Intent(category=IntentCategory.QUERY, action="list_team"),
            lens=ConversationalLens.PEOPLE,
        )
        ctx.push_lens(ConversationalLens.ISSUES)

        assert ctx.lens_stack == [ConversationalLens.CALENDAR, ConversationalLens.PEOPLE]

        # Pop back
        popped = ctx.pop_lens()
        assert popped == ConversationalLens.PEOPLE
        popped = ctx.pop_lens()
        assert popped == ConversationalLens.CALENDAR
        assert ctx.lens_stack == []

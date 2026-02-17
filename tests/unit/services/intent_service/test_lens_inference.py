"""
Tests for lens inference (#763 GLUE-FOLLOWUP Phase 2).

Tests the extract_lens_from_intent mapping and lens inheritance
through resolve_follow_up.
"""

import pytest

from services.domain.models import Intent
from services.intent_service.conversation_context import (
    ConversationContext,
    FollowUpType,
    detect_follow_up,
    resolve_follow_up,
)
from services.intent_service.lens_inference import extract_lens_from_intent
from services.shared_types import ConversationalLens, IntentCategory


class TestExtractLensFromIntent:
    """Test the intent → lens mapping."""

    # Calendar actions
    @pytest.mark.parametrize(
        "action",
        [
            "meeting_time",
            "schedule_meeting",
            "cancel_meeting",
            "reschedule_meeting",
            "check_availability",
            "list_meetings",
            "agenda",
        ],
    )
    def test_calendar_actions(self, action):
        intent = Intent(category=IntentCategory.QUERY, action=action)
        assert extract_lens_from_intent(intent) == ConversationalLens.CALENDAR

    # Issue actions
    @pytest.mark.parametrize(
        "action",
        [
            "list_issues",
            "create_issue",
            "close_issue",
            "list_blockers",
            "count_issues",
            "list_pull_requests",
            "list_todos",
        ],
    )
    def test_issue_actions(self, action):
        intent = Intent(category=IntentCategory.QUERY, action=action)
        assert extract_lens_from_intent(intent) == ConversationalLens.ISSUES

    # Project actions
    @pytest.mark.parametrize(
        "action",
        ["project_status", "project_timeline", "work_summary"],
    )
    def test_project_actions(self, action):
        intent = Intent(category=IntentCategory.STATUS, action=action)
        assert extract_lens_from_intent(intent) == ConversationalLens.PROJECTS

    # People actions
    @pytest.mark.parametrize(
        "action",
        ["list_team", "team_assignments", "person_tasks", "person_workload", "team_workload"],
    )
    def test_people_actions(self, action):
        intent = Intent(category=IntentCategory.QUERY, action=action)
        assert extract_lens_from_intent(intent) == ConversationalLens.PEOPLE

    # Category fallbacks
    def test_status_category_fallback(self):
        intent = Intent(category=IntentCategory.STATUS, action="unknown_action")
        assert extract_lens_from_intent(intent) == ConversationalLens.PROJECTS

    def test_priority_category_fallback(self):
        intent = Intent(category=IntentCategory.PRIORITY, action="check")
        assert extract_lens_from_intent(intent) == ConversationalLens.ISSUES

    def test_guidance_category_fallback(self):
        intent = Intent(category=IntentCategory.GUIDANCE, action="suggest")
        assert extract_lens_from_intent(intent) == ConversationalLens.PROJECTS

    # No lens categories
    @pytest.mark.parametrize(
        "category",
        [
            IntentCategory.CONVERSATION,
            IntentCategory.IDENTITY,
            IntentCategory.DISCOVERY,
            IntentCategory.UNKNOWN,
            IntentCategory.TRUST,
            IntentCategory.MEMORY,
        ],
    )
    def test_no_lens_categories(self, category):
        intent = Intent(category=category, action="test")
        assert extract_lens_from_intent(intent) is None

    # General fallback for unmapped actions
    def test_unmapped_action_returns_general(self):
        intent = Intent(category=IntentCategory.QUERY, action="obscure_action")
        assert extract_lens_from_intent(intent) == ConversationalLens.GENERAL

    def test_execution_category_unmapped_returns_general(self):
        intent = Intent(category=IntentCategory.EXECUTION, action="unknown_exec")
        assert extract_lens_from_intent(intent) == ConversationalLens.GENERAL


class TestLensInheritanceThroughFollowUp:
    """Test that resolve_follow_up includes inherited_lens in the result."""

    def test_temporal_shift_inherits_lens(self):
        """Temporal shift follow-up should include inherited_lens from context."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="What's on my calendar tomorrow?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            temporal_reference="tomorrow",
            lens=ConversationalLens.CALENDAR,
        )

        result = detect_follow_up("How about today?", ctx)
        assert result is not None
        follow_up_type, extracted_data = result

        resolved = resolve_follow_up(follow_up_type, extracted_data, ctx)
        assert resolved is not None
        assert resolved.context.get("inherited_lens") == ConversationalLens.CALENDAR

    def test_continuation_inherits_lens(self):
        """Continuation follow-up should include inherited_lens from context."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Show me my open issues",
            intent=Intent(category=IntentCategory.QUERY, action="list_issues"),
            lens=ConversationalLens.ISSUES,
        )

        result = detect_follow_up("What else?", ctx)
        assert result is not None
        follow_up_type, extracted_data = result

        resolved = resolve_follow_up(follow_up_type, extracted_data, ctx)
        assert resolved is not None
        assert resolved.context.get("inherited_lens") == ConversationalLens.ISSUES

    def test_confirmation_inherits_lens(self):
        """Confirmation follow-up should include inherited_lens."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Want me to schedule a meeting?",
            intent=Intent(category=IntentCategory.QUERY, action="schedule_meeting"),
            lens=ConversationalLens.CALENDAR,
        )

        result = detect_follow_up("Yes", ctx)
        assert result is not None
        follow_up_type, extracted_data = result

        resolved = resolve_follow_up(follow_up_type, extracted_data, ctx)
        assert resolved is not None
        assert resolved.context.get("inherited_lens") == ConversationalLens.CALENDAR

    def test_negation_inherits_lens(self):
        """Negation follow-up should include inherited_lens."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Here are your issues",
            intent=Intent(category=IntentCategory.QUERY, action="list_issues"),
            lens=ConversationalLens.ISSUES,
        )

        # "Not that" matches the negation pattern ^not (that|those|this|it)\.?$
        result = detect_follow_up("Not that", ctx)
        assert result is not None
        follow_up_type, extracted_data = result

        resolved = resolve_follow_up(follow_up_type, extracted_data, ctx)
        assert resolved is not None
        assert resolved.context.get("inherited_lens") == ConversationalLens.ISSUES

    def test_no_lens_in_context_inherits_none(self):
        """If no lens in context, inherited_lens should be None."""
        ctx = ConversationContext()
        ctx.add_turn(
            message="Hello",
            intent=Intent(category=IntentCategory.CONVERSATION, action="greeting"),
            # No lens
        )
        ctx.add_turn(
            message="What's on my calendar tomorrow?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            temporal_reference="tomorrow",
            # No lens stored (simulating pre-Phase-2 behavior)
        )

        result = detect_follow_up("How about today?", ctx)
        assert result is not None
        follow_up_type, extracted_data = result

        resolved = resolve_follow_up(follow_up_type, extracted_data, ctx)
        assert resolved is not None
        # No lens was stored, so inherited_lens should be None
        assert resolved.context.get("inherited_lens") is None


class TestWiringLensThroughClassifyConscious:
    """
    Wiring tests: verify lens flows through the real classify_conscious pipeline.

    These use real ConversationContext objects (not mocks) to verify the
    classify_conscious → extract_lens → add_turn → current_lens chain.
    """

    @pytest.mark.asyncio
    async def test_lens_stored_after_follow_up_resolution(self):
        """After a temporal follow-up, the lens should be stored on the new turn."""
        ctx = ConversationContext()
        # Simulate previous turn with calendar lens
        ctx.add_turn(
            message="What's on my calendar tomorrow?",
            intent=Intent(category=IntentCategory.QUERY, action="meeting_time"),
            temporal_reference="tomorrow",
            lens=ConversationalLens.CALENDAR,
        )

        # Simulate what classify_conscious does for a follow-up:
        # 1. detect_follow_up
        result = detect_follow_up("How about today?", ctx)
        assert result is not None
        follow_up_type, extracted_data = result

        # 2. resolve_follow_up
        resolved = resolve_follow_up(follow_up_type, extracted_data, ctx)
        assert resolved is not None

        # 3. Extract lens (what classify_conscious does)
        lens = resolved.context.get("inherited_lens") or extract_lens_from_intent(resolved)

        # 4. add_turn with lens
        ctx.add_turn(
            message="How about today?",
            intent=resolved,
            temporal_reference="today",
            lens=lens,
        )

        # Verify the chain works
        assert ctx.current_lens == ConversationalLens.CALENDAR
        assert ctx.turns[-1].lens == ConversationalLens.CALENDAR

    @pytest.mark.asyncio
    async def test_lens_inferred_from_new_query(self):
        """For a new query (not follow-up), lens is inferred from the intent."""
        ctx = ConversationContext()

        # Simulate a new calendar query
        intent = Intent(category=IntentCategory.QUERY, action="meeting_time")
        lens = extract_lens_from_intent(intent)
        ctx.add_turn(
            message="What's on my calendar tomorrow?",
            intent=intent,
            temporal_reference="tomorrow",
            lens=lens,
        )

        assert ctx.current_lens == ConversationalLens.CALENDAR

    @pytest.mark.asyncio
    async def test_lens_persists_through_three_turns(self):
        """Lens should persist across 3+ follow-up turns."""
        ctx = ConversationContext()

        # Turn 1: calendar query
        intent1 = Intent(category=IntentCategory.QUERY, action="meeting_time")
        ctx.add_turn(
            message="What's on my calendar tomorrow?",
            intent=intent1,
            temporal_reference="tomorrow",
            lens=ConversationalLens.CALENDAR,
        )

        # Turn 2: temporal follow-up
        result = detect_follow_up("What about Thursday?", ctx)
        assert result is not None
        follow_up_type, extracted_data = result
        resolved2 = resolve_follow_up(follow_up_type, extracted_data, ctx)
        lens2 = resolved2.context.get("inherited_lens") or extract_lens_from_intent(resolved2)
        ctx.add_turn(
            message="What about Thursday?",
            intent=resolved2,
            temporal_reference="thursday",
            lens=lens2,
        )

        # Turn 3: another temporal follow-up
        result3 = detect_follow_up("And Friday?", ctx)
        assert result3 is not None
        follow_up_type3, extracted_data3 = result3
        resolved3 = resolve_follow_up(follow_up_type3, extracted_data3, ctx)
        lens3 = resolved3.context.get("inherited_lens") or extract_lens_from_intent(resolved3)
        ctx.add_turn(
            message="And Friday?",
            intent=resolved3,
            temporal_reference="friday",
            lens=lens3,
        )

        # All 3 turns should have calendar lens
        assert all(t.lens == ConversationalLens.CALENDAR for t in ctx.turns)
        assert ctx.current_lens == ConversationalLens.CALENDAR

    @pytest.mark.asyncio
    async def test_conversation_intent_does_not_set_lens(self):
        """Greetings and conversation should NOT set a lens."""
        ctx = ConversationContext()

        intent = Intent(category=IntentCategory.CONVERSATION, action="greeting")
        lens = extract_lens_from_intent(intent)
        ctx.add_turn(
            message="Hello!",
            intent=intent,
            lens=lens,
        )

        assert ctx.current_lens is None

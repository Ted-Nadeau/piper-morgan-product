"""
Tests for lens-aware slot filling prompts.

Issue #821: Slot filling prompts informed by conversational lens context.

Tests cover:
- SlotDefinition.prompt_for_lens() — lens-specific phrasing
- format_prompt() with lens — contextual single-slot prompts
- format_grouped_prompt() with lens — contextual grouped prompts
- format_confirmation_with_prompt() with lens — combined confirmation + contextual prompt
- get_next_prompt_group() with lens — lens-aware group ordering
- MEETING_TEMPLATE lens enrichment — all lens variants present
- SlotFillingManager.start_filling() with lens — end-to-end threading
- No-lens backward compatibility — all functions work without lens
"""

import pytest

from services.slot_filling.slot_extractor import get_next_prompt_group
from services.slot_filling.slot_filling_manager import SlotFillingManager
from services.slot_filling.slot_prompts import (
    format_confirmation_with_prompt,
    format_grouped_prompt,
    format_prompt,
)
from services.slot_filling.slot_template import (
    MEETING_TEMPLATE,
    ConfirmationStyle,
    SlotDefinition,
    SlotState,
    SlotTemplate,
    SlotType,
)

# --- Fixtures ---


@pytest.fixture
def meeting_state():
    """Empty meeting slot state for prompting tests."""
    return SlotState(template=MEETING_TEMPLATE)


@pytest.fixture
def meeting_state_with_attendee():
    """Meeting state with attendee filled."""
    state = SlotState(template=MEETING_TEMPLATE)
    state.set_value("attendee", "Sarah")
    return state


@pytest.fixture
def meeting_state_with_time_filled():
    """Meeting state with day and time filled (attendee and topic missing)."""
    state = SlotState(template=MEETING_TEMPLATE)
    state.set_value("day", "Tuesday")
    state.set_value("time", "2pm")
    return state


@pytest.fixture
def slot_with_lens():
    """SlotDefinition with lens-specific prompts."""
    return SlotDefinition(
        name="topic",
        display_name="What's the topic",
        slot_type=SlotType.TEXT,
        lens_prompts={
            "calendar": "What's the agenda",
            "people": "What should you cover",
            "projects": "Which project is this about",
        },
    )


@pytest.fixture
def slot_without_lens():
    """SlotDefinition without lens prompts (backward compat)."""
    return SlotDefinition(
        name="action",
        display_name="What action",
        slot_type=SlotType.TEXT,
    )


# --- SlotDefinition.prompt_for_lens() ---


class TestSlotDefinitionLensPrompts:
    """Unit tests for SlotDefinition.prompt_for_lens()."""

    def test_calendar_lens_returns_calendar_phrasing(self, slot_with_lens):
        assert slot_with_lens.prompt_for_lens("calendar") == "What's the agenda"

    def test_people_lens_returns_people_phrasing(self, slot_with_lens):
        assert slot_with_lens.prompt_for_lens("people") == "What should you cover"

    def test_projects_lens_returns_projects_phrasing(self, slot_with_lens):
        assert slot_with_lens.prompt_for_lens("projects") == "Which project is this about"

    def test_unknown_lens_falls_back_to_display_name(self, slot_with_lens):
        assert slot_with_lens.prompt_for_lens("issues") == "What's the topic"

    def test_none_lens_falls_back_to_display_name(self, slot_with_lens):
        assert slot_with_lens.prompt_for_lens(None) == "What's the topic"

    def test_no_lens_prompts_field_returns_display_name(self, slot_without_lens):
        assert slot_without_lens.prompt_for_lens("calendar") == "What action"

    def test_no_lens_prompts_with_none_returns_display_name(self, slot_without_lens):
        assert slot_without_lens.prompt_for_lens(None) == "What action"


# --- format_prompt() with lens ---


class TestFormatPromptWithLens:
    """Lens-aware single-slot prompts."""

    def test_single_slot_calendar_lens(self):
        """Calendar lens → contextual phrasing."""
        slot = MEETING_TEMPLATE.slots[3]  # topic
        result = format_prompt([slot], lens="calendar")
        assert "agenda" in result.lower()

    def test_single_slot_people_lens(self):
        """People lens → people-focused phrasing."""
        slot = MEETING_TEMPLATE.slots[0]  # attendee
        result = format_prompt([slot], lens="people")
        assert "who needs to be in this meeting" in result.lower()

    def test_single_slot_no_lens_is_generic(self):
        """No lens → generic display_name phrasing."""
        slot = MEETING_TEMPLATE.slots[0]  # attendee
        result = format_prompt([slot], lens=None)
        assert "who should attend" in result.lower()

    def test_single_slot_unknown_lens_is_generic(self):
        """Unknown lens → falls back to generic."""
        slot = MEETING_TEMPLATE.slots[3]  # topic
        result = format_prompt([slot], lens="issues")
        assert "topic" in result.lower()


# --- format_grouped_prompt() with lens ---


class TestFormatGroupedPromptWithLens:
    """Lens-aware grouped prompts."""

    def test_grouped_calendar_lens(self):
        """Calendar lens → calendar phrasing for all grouped slots."""
        slots = MEETING_TEMPLATE.slots[:3]  # attendee, day, time (group 0)
        result = format_grouped_prompt(slots, lens="calendar")
        assert "who should be there" in result.lower()
        assert "which day works" in result.lower()
        assert "what time works best" in result.lower()

    def test_grouped_people_lens(self):
        """People lens → people-focused phrasing."""
        slots = MEETING_TEMPLATE.slots[:3]
        result = format_grouped_prompt(slots, lens="people")
        assert "who needs to be in this meeting" in result.lower()

    def test_grouped_no_lens_generic(self):
        """No lens → generic phrasing."""
        slots = MEETING_TEMPLATE.slots[:3]
        result = format_grouped_prompt(slots, lens=None)
        assert "who should attend" in result.lower()
        assert "what day" in result.lower()
        assert "what time" in result.lower()

    def test_two_slots_calendar_lens(self):
        """Two missing slots with calendar lens."""
        slots = MEETING_TEMPLATE.slots[1:3]  # day, time
        result = format_grouped_prompt(slots, lens="calendar")
        assert "which day works" in result.lower()
        assert "what time works best" in result.lower()


# --- format_confirmation_with_prompt() with lens ---


class TestFormatConfirmationWithPromptLens:
    """Combined confirmation + lens-aware prompt."""

    def test_confirmation_with_calendar_prompt(self, meeting_state_with_attendee):
        """Filled attendee + calendar lens → calendar prompt for remaining."""
        missing = meeting_state_with_attendee.unfilled_required
        result = format_confirmation_with_prompt(
            meeting_state_with_attendee, missing, lens="calendar"
        )
        # Should confirm Sarah
        assert "Sarah" in result
        # Should use calendar phrasing for remaining
        assert "which day works" in result.lower()

    def test_confirmation_with_projects_prompt(self, meeting_state_with_time_filled):
        """Filled time + projects lens → projects prompt for remaining."""
        missing = meeting_state_with_time_filled.unfilled_required
        result = format_confirmation_with_prompt(
            meeting_state_with_time_filled, missing, lens="projects"
        )
        # Should confirm day and time
        assert "Tuesday" in result
        assert "2pm" in result
        # Should use projects phrasing for missing
        assert "who should attend from the team" in result.lower()

    def test_confirmation_without_lens_is_generic(self, meeting_state_with_attendee):
        """No lens → generic prompts in confirmation."""
        missing = meeting_state_with_attendee.unfilled_required
        result = format_confirmation_with_prompt(meeting_state_with_attendee, missing, lens=None)
        assert "what day" in result.lower()


# --- get_next_prompt_group() with lens ---


class TestGetNextPromptGroupWithLens:
    """Lens-aware group ordering."""

    def test_default_order_no_lens(self, meeting_state):
        """No lens → default order (group 0 first)."""
        group = get_next_prompt_group(meeting_state, lens=None)
        # Group 0 has attendee, day, time
        names = {s.name for s in group}
        assert "attendee" in names
        assert "day" in names
        assert "time" in names

    def test_calendar_lens_keeps_default_order(self, meeting_state):
        """Calendar lens → group 0 first (calendar priority is [0, 1])."""
        group = get_next_prompt_group(meeting_state, lens="calendar")
        names = {s.name for s in group}
        assert "attendee" in names
        assert "day" in names
        assert "time" in names

    def test_projects_lens_reorders_to_topic_first(self, meeting_state):
        """Projects lens → topic (group 1) first, then logistics (group 0)."""
        group = get_next_prompt_group(meeting_state, lens="projects")
        # Projects priority is [1, 0] — topic group first
        assert len(group) == 1  # Group 1 has only "topic"
        assert group[0].name == "topic"

    def test_projects_lens_after_topic_filled(self):
        """Projects lens, topic filled → group 0 is next."""
        state = SlotState(template=MEETING_TEMPLATE)
        state.set_value("topic", "Q3 planning")
        group = get_next_prompt_group(state, lens="projects")
        # Topic (group 1) already filled → group 0 next
        names = {s.name for s in group}
        assert "attendee" in names

    def test_unknown_lens_uses_default_order(self, meeting_state):
        """Unknown lens without priority config → default order."""
        group = get_next_prompt_group(meeting_state, lens="issues")
        names = {s.name for s in group}
        assert "attendee" in names  # group 0 first

    def test_lens_with_all_priority_groups_filled(self):
        """All priority groups filled → returns empty (all done)."""
        state = SlotState(template=MEETING_TEMPLATE)
        state.set_value("attendee", "Sarah")
        state.set_value("day", "Tuesday")
        state.set_value("time", "2pm")
        state.set_value("topic", "Sprint review")
        group = get_next_prompt_group(state, lens="projects")
        assert group == []


# --- MEETING_TEMPLATE lens enrichment ---


class TestMeetingTemplateLensEnrichment:
    """Verify MEETING_TEMPLATE has complete lens prompt coverage."""

    def test_all_slots_have_lens_prompts(self):
        """Every slot in MEETING_TEMPLATE has lens_prompts defined."""
        for slot in MEETING_TEMPLATE.slots:
            assert slot.lens_prompts is not None, f"Slot '{slot.name}' missing lens_prompts"

    def test_calendar_lens_coverage(self):
        """Every slot has a 'calendar' lens prompt."""
        for slot in MEETING_TEMPLATE.slots:
            assert (
                "calendar" in slot.lens_prompts
            ), f"Slot '{slot.name}' missing 'calendar' lens prompt"

    def test_people_lens_coverage(self):
        """Every slot has a 'people' lens prompt."""
        for slot in MEETING_TEMPLATE.slots:
            assert "people" in slot.lens_prompts, f"Slot '{slot.name}' missing 'people' lens prompt"

    def test_projects_lens_coverage(self):
        """Every slot has a 'projects' lens prompt."""
        for slot in MEETING_TEMPLATE.slots:
            assert (
                "projects" in slot.lens_prompts
            ), f"Slot '{slot.name}' missing 'projects' lens prompt"

    def test_lens_group_priority_defined(self):
        """MEETING_TEMPLATE has lens_group_priority for all supported lenses."""
        assert MEETING_TEMPLATE.lens_group_priority is not None
        assert "calendar" in MEETING_TEMPLATE.lens_group_priority
        assert "people" in MEETING_TEMPLATE.lens_group_priority
        assert "projects" in MEETING_TEMPLATE.lens_group_priority

    def test_lens_prompts_differ_from_generic(self):
        """Lens prompts should not be identical to display_name."""
        for slot in MEETING_TEMPLATE.slots:
            for lens, prompt in slot.lens_prompts.items():
                # At least some should differ (not all need to)
                pass  # Just verify structure — phrasing is a design choice
        # At least the topic slot should differ across all lenses
        topic = MEETING_TEMPLATE.slots[3]
        assert topic.lens_prompts["calendar"] != topic.display_name
        assert topic.lens_prompts["projects"] != topic.display_name


# --- SlotFillingManager integration ---


class TestSlotFillingManagerWithLens:
    """End-to-end: start_filling with lens → contextual prompts."""

    @pytest.mark.asyncio
    async def test_start_with_calendar_lens_prompts(self):
        """Calendar lens → calendar-phrased prompts in response."""
        manager = SlotFillingManager()
        response = await manager.start_filling(
            user_id=None,
            session_id="sess_cal",
            template=MEETING_TEMPLATE,
            initial_message="",  # No initial extraction
            active_lens="calendar",
        )
        # Should prompt for group 0 with calendar phrasing
        assert "who should be there" in response.message.lower()
        assert "which day works" in response.message.lower()
        assert "what time works best" in response.message.lower()

    @pytest.mark.asyncio
    async def test_start_with_people_lens_prompts(self):
        """People lens → people-focused prompts."""
        manager = SlotFillingManager()
        response = await manager.start_filling(
            user_id=None,
            session_id="sess_ppl",
            template=MEETING_TEMPLATE,
            initial_message="",
            active_lens="people",
        )
        assert "who needs to be in this meeting" in response.message.lower()

    @pytest.mark.asyncio
    async def test_start_with_projects_lens_reorders(self):
        """Projects lens → topic group first."""
        manager = SlotFillingManager()
        response = await manager.start_filling(
            user_id=None,
            session_id="sess_proj",
            template=MEETING_TEMPLATE,
            initial_message="",
            active_lens="projects",
        )
        # Projects lens: group 1 (topic) first → asks about project
        assert "which project is this about" in response.message.lower()

    @pytest.mark.asyncio
    async def test_start_without_lens_generic_prompts(self):
        """No lens → generic prompts (backward compat)."""
        manager = SlotFillingManager()
        response = await manager.start_filling(
            user_id=None,
            session_id="sess_gen",
            template=MEETING_TEMPLATE,
            initial_message="",
            active_lens=None,
        )
        # Generic phrasing
        assert "who should attend" in response.message.lower()
        assert "what day" in response.message.lower()
        assert "what time" in response.message.lower()

    @pytest.mark.asyncio
    async def test_lens_stored_on_session(self):
        """Active lens is stored on the session for subsequent turns."""
        manager = SlotFillingManager()
        await manager.start_filling(
            user_id=None,
            session_id="sess_store",
            template=MEETING_TEMPLATE,
            initial_message="",
            active_lens="calendar",
        )
        session = manager.get_session("sess_store")
        assert session is not None
        assert session.active_lens == "calendar"

    @pytest.mark.asyncio
    async def test_lens_persists_across_turns(self):
        """Lens from start_filling carries through to handle_turn prompts."""
        manager = SlotFillingManager()
        # Start with projects lens — asks for topic first
        await manager.start_filling(
            user_id=None,
            session_id="sess_persist",
            template=MEETING_TEMPLATE,
            initial_message="",
            active_lens="projects",
        )
        # Simulate providing the topic
        session = manager.get_session("sess_persist")
        session.slot_state.set_value("topic", "Q3 planning")

        # Next turn should use projects lens for group 0
        response = await manager.handle_turn(
            user_id=None,
            session_id="sess_persist",
            message="The Q3 planning review",
        )
        # Projects lens for attendee: "who should attend from the team"
        assert "who should attend from the team" in response.message.lower()


# --- Backward compatibility ---


class TestBackwardCompatibility:
    """Verify all existing behavior works without lens."""

    def test_slot_definition_without_lens_prompts(self):
        """SlotDefinition works fine without lens_prompts field."""
        slot = SlotDefinition(name="x", display_name="What X")
        assert slot.lens_prompts is None
        assert slot.prompt_for_lens(None) == "What X"
        assert slot.prompt_for_lens("calendar") == "What X"

    def test_template_without_lens_group_priority(self):
        """SlotTemplate works fine without lens_group_priority."""
        template = SlotTemplate(
            name="simple",
            display_name="Simple",
            slots=[SlotDefinition(name="x", display_name="What X")],
        )
        assert template.lens_group_priority is None

    def test_format_prompt_without_lens(self):
        """format_prompt() works with no lens arg."""
        slot = SlotDefinition(name="x", display_name="What X")
        result = format_prompt([slot])
        assert result == "What's the what x?"

    def test_format_grouped_prompt_without_lens(self):
        """format_grouped_prompt() works with no lens arg."""
        slots = [
            SlotDefinition(name="a", display_name="First"),
            SlotDefinition(name="b", display_name="Second"),
        ]
        result = format_grouped_prompt(slots)
        assert result == "What's the first, and second?"

    @pytest.mark.asyncio
    async def test_start_filling_without_lens_arg(self):
        """start_filling() works without active_lens arg."""
        manager = SlotFillingManager()
        response = await manager.start_filling(
            user_id=None,
            session_id="sess_compat",
            template=MEETING_TEMPLATE,
            initial_message="",
        )
        # Should work — generic prompts
        assert response.message
        assert "who should attend" in response.message.lower()

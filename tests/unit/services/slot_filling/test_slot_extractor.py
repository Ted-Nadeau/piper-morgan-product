"""
Tests for slot extraction engine.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Phase 2: Slot Extraction + Skip Logic

Tests cover:
- LLM-based extraction from full/partial/empty messages
- Slot update (override existing value)
- Skip-filled detection (missing required)
- Grouped prompting (next prompt group selection)
- Graceful fallback on LLM failure
"""

from unittest.mock import AsyncMock

import pytest

from services.slot_filling.slot_extractor import (
    MAX_PROMPT_GROUP_SIZE,
    _build_extraction_prompt,
    _parse_extraction_response,
    extract_slots,
    get_missing_required,
    get_next_prompt_group,
    update_slot_state,
)
from services.slot_filling.slot_template import (
    MEETING_TEMPLATE,
    SlotDefinition,
    SlotState,
    SlotTemplate,
    SlotType,
)


@pytest.fixture
def mock_llm():
    """Mock LLM service that returns configurable JSON responses."""
    llm = AsyncMock()
    llm.complete = AsyncMock(return_value="{}")
    return llm


@pytest.fixture
def meeting_state():
    """Fresh slot state for the meeting template."""
    return SlotState(template=MEETING_TEMPLATE)


# --- extract_slots Tests ---


class TestExtractSlots:
    @pytest.mark.asyncio
    async def test_full_extraction(self, mock_llm):
        """All slots extracted from a complete message."""
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3 planning"}'
        )
        result = await extract_slots(
            "Set up a meeting with Sarah Tuesday at 2pm about Q3 planning",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result["attendee"] == "Sarah"
        assert result["day"] == "Tuesday"
        assert result["time"] == "2pm"
        assert result["topic"] == "Q3 planning"

    @pytest.mark.asyncio
    async def test_partial_extraction(self, mock_llm):
        """Only some slots extracted from a partial message."""
        mock_llm.complete.return_value = '{"attendee": "Sarah"}'
        result = await extract_slots(
            "Schedule something with Sarah",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result == {"attendee": "Sarah"}

    @pytest.mark.asyncio
    async def test_empty_extraction(self, mock_llm):
        """No slots parseable from message."""
        mock_llm.complete.return_value = "{}"
        result = await extract_slots(
            "Schedule a meeting",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result == {}

    @pytest.mark.asyncio
    async def test_empty_message(self, mock_llm):
        """Empty message returns empty dict without calling LLM."""
        result = await extract_slots("", MEETING_TEMPLATE, mock_llm)
        assert result == {}
        mock_llm.complete.assert_not_called()

    @pytest.mark.asyncio
    async def test_whitespace_only_message(self, mock_llm):
        """Whitespace-only message returns empty dict."""
        result = await extract_slots("   ", MEETING_TEMPLATE, mock_llm)
        assert result == {}
        mock_llm.complete.assert_not_called()

    @pytest.mark.asyncio
    async def test_llm_failure_returns_empty(self, mock_llm):
        """LLM failure returns empty dict (graceful fallback)."""
        mock_llm.complete.side_effect = RuntimeError("LLM unavailable")
        result = await extract_slots(
            "Meeting with Sarah Tuesday at 2pm",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result == {}

    @pytest.mark.asyncio
    async def test_existing_values_passed_to_prompt(self, mock_llm):
        """Existing values are included in the extraction prompt for update detection."""
        mock_llm.complete.return_value = '{"time": "4pm"}'
        result = await extract_slots(
            "Actually make it 4pm",
            MEETING_TEMPLATE,
            mock_llm,
            existing_values={"attendee": "Sarah", "time": "3pm"},
        )
        assert result == {"time": "4pm"}
        # Verify existing values were in the prompt
        call_kwargs = mock_llm.complete.call_args
        assert "Sarah" in call_kwargs.kwargs.get(
            "prompt", call_kwargs.args[1] if len(call_kwargs.args) > 1 else ""
        )

    @pytest.mark.asyncio
    async def test_llm_called_with_correct_task_type(self, mock_llm):
        """LLM is called with 'slot_extraction' task type."""
        mock_llm.complete.return_value = "{}"
        await extract_slots("test message", MEETING_TEMPLATE, mock_llm)
        mock_llm.complete.assert_called_once()
        call_kwargs = mock_llm.complete.call_args
        assert call_kwargs.kwargs.get("task_type") == "slot_extraction"

    @pytest.mark.asyncio
    async def test_markdown_fences_stripped(self, mock_llm):
        """JSON wrapped in markdown code fences is handled."""
        mock_llm.complete.return_value = '```json\n{"attendee": "Sarah"}\n```'
        result = await extract_slots("With Sarah", MEETING_TEMPLATE, mock_llm)
        assert result == {"attendee": "Sarah"}


# --- _parse_extraction_response Tests ---


class TestParseExtractionResponse:
    def test_valid_json(self):
        result = _parse_extraction_response(
            '{"attendee": "Sarah", "time": "2pm"}', MEETING_TEMPLATE
        )
        assert result == {"attendee": "Sarah", "time": "2pm"}

    def test_invalid_json(self):
        result = _parse_extraction_response("not json at all", MEETING_TEMPLATE)
        assert result == {}

    def test_json_array_not_dict(self):
        result = _parse_extraction_response('["Sarah", "2pm"]', MEETING_TEMPLATE)
        assert result == {}

    def test_invalid_slot_names_filtered(self):
        result = _parse_extraction_response(
            '{"attendee": "Sarah", "invalid_slot": "value"}', MEETING_TEMPLATE
        )
        assert result == {"attendee": "Sarah"}
        assert "invalid_slot" not in result

    def test_null_values_filtered(self):
        result = _parse_extraction_response('{"attendee": "Sarah", "time": null}', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}

    def test_empty_string_values_filtered(self):
        result = _parse_extraction_response('{"attendee": "Sarah", "time": ""}', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}

    def test_whitespace_values_filtered(self):
        result = _parse_extraction_response(
            '{"attendee": "Sarah", "time": "   "}', MEETING_TEMPLATE
        )
        assert result == {"attendee": "Sarah"}

    def test_markdown_fences_stripped(self):
        result = _parse_extraction_response('```json\n{"attendee": "Sarah"}\n```', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}

    def test_values_stripped(self):
        result = _parse_extraction_response('{"attendee": "  Sarah  "}', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}


# --- update_slot_state Tests ---


class TestUpdateSlotState:
    def test_fill_empty_state(self, meeting_state):
        extracted = {"attendee": "Sarah", "day": "Tuesday"}
        update_slot_state(meeting_state, extracted)
        assert meeting_state.get_value("attendee") == "Sarah"
        assert meeting_state.get_value("day") == "Tuesday"
        assert meeting_state.filled_count == 2

    def test_update_existing_value(self, meeting_state):
        meeting_state.set_value("time", "3pm")
        update_slot_state(meeting_state, {"time": "4pm"})
        assert meeting_state.get_value("time") == "4pm"
        assert meeting_state.filled_count == 1

    def test_empty_extraction_no_change(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        update_slot_state(meeting_state, {})
        assert meeting_state.get_value("attendee") == "Sarah"
        assert meeting_state.filled_count == 1

    def test_additive_extraction(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        update_slot_state(meeting_state, {"day": "Tuesday", "time": "2pm"})
        assert meeting_state.filled_count == 3
        assert meeting_state.get_value("attendee") == "Sarah"
        assert meeting_state.get_value("day") == "Tuesday"


# --- get_missing_required Tests ---


class TestGetMissingRequired:
    def test_all_missing(self, meeting_state):
        missing = get_missing_required(meeting_state)
        assert len(missing) == 4  # All meeting slots are required

    def test_some_filled(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        missing = get_missing_required(meeting_state)
        assert len(missing) == 2
        names = [s.name for s in missing]
        assert "time" in names
        assert "topic" in names

    def test_all_filled(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        meeting_state.set_value("topic", "Q3 planning")
        missing = get_missing_required(meeting_state)
        assert len(missing) == 0


# --- get_next_prompt_group Tests ---


class TestGetNextPromptGroup:
    def test_first_group_returned(self, meeting_state):
        """With all slots missing, returns group 0 (attendee, day, time)."""
        group = get_next_prompt_group(meeting_state)
        names = [s.name for s in group]
        # Group 0 has attendee, day, time
        assert "attendee" in names
        assert "day" in names
        assert "time" in names

    def test_capped_at_max_size(self):
        """Prompt group capped at MAX_PROMPT_GROUP_SIZE."""
        # Create template with many slots in one group
        slots = [SlotDefinition(name=f"s{i}", display_name=f"Slot {i}", group=0) for i in range(5)]
        template = SlotTemplate(name="big", display_name="Big", slots=slots)
        state = SlotState(template=template)
        group = get_next_prompt_group(state)
        assert len(group) <= MAX_PROMPT_GROUP_SIZE

    def test_skips_to_next_group(self, meeting_state):
        """When group 0 is filled, returns group 1."""
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        group = get_next_prompt_group(meeting_state)
        assert len(group) == 1
        assert group[0].name == "topic"

    def test_empty_when_all_filled(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        meeting_state.set_value("topic", "Q3 planning")
        group = get_next_prompt_group(meeting_state)
        assert len(group) == 0

    def test_ungrouped_slots_handled(self):
        """Slots without a group (None) are handled correctly."""
        template = SlotTemplate(
            name="test",
            display_name="Test",
            slots=[
                SlotDefinition(name="a", display_name="A", group=0),
                SlotDefinition(name="b", display_name="B"),  # group=None
            ],
        )
        state = SlotState(template=template)
        state.set_value("a", "filled")
        # Should return the ungrouped slot
        group = get_next_prompt_group(state)
        assert len(group) == 1
        assert group[0].name == "b"

    def test_partial_group_fill(self, meeting_state):
        """When some slots in a group are filled, only missing ones returned."""
        meeting_state.set_value("attendee", "Sarah")
        # day and time still missing in group 0
        group = get_next_prompt_group(meeting_state)
        names = [s.name for s in group]
        assert "attendee" not in names
        assert "day" in names
        assert "time" in names


# --- _build_extraction_prompt Tests ---


class TestBuildExtractionPrompt:
    def test_includes_slot_descriptions(self):
        prompt = _build_extraction_prompt("test message", MEETING_TEMPLATE)
        assert "attendee" in prompt
        assert "day" in prompt
        assert "time" in prompt
        assert "topic" in prompt

    def test_includes_user_message(self):
        prompt = _build_extraction_prompt("Meeting with Sarah", MEETING_TEMPLATE)
        assert "Meeting with Sarah" in prompt

    def test_includes_existing_values(self):
        prompt = _build_extraction_prompt(
            "Actually 4pm",
            MEETING_TEMPLATE,
            existing_values={"attendee": "Sarah", "time": "3pm"},
        )
        assert "Sarah" in prompt
        assert "3pm" in prompt

    def test_no_existing_values(self):
        prompt = _build_extraction_prompt("Schedule a meeting", MEETING_TEMPLATE)
        assert "Already known" not in prompt

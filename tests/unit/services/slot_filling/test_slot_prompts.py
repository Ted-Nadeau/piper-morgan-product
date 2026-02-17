"""
Tests for slot-filling prompt formatting.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Phase 2: Slot Extraction + Skip Logic

Tests cover:
- Confirmation formatting (implicit/explicit)
- Single missing slot prompt
- Grouped prompt (2-3 missing slots)
- Combined confirmation + prompt
- Final confirmation
"""

import pytest

from services.slot_filling.slot_prompts import (
    format_confirmation,
    format_confirmation_with_prompt,
    format_final_confirmation,
    format_grouped_prompt,
    format_prompt,
)
from services.slot_filling.slot_template import (
    ConfirmationStyle,
    SlotDefinition,
    SlotState,
    SlotTemplate,
    SlotType,
)


@pytest.fixture
def meeting_template():
    """Meeting template for prompt tests."""
    from services.slot_filling.slot_template import MEETING_TEMPLATE

    return MEETING_TEMPLATE


@pytest.fixture
def explicit_template():
    """Template with explicit confirmation style."""
    return SlotTemplate(
        name="high_stakes",
        display_name="High Stakes",
        slots=[
            SlotDefinition(name="action", display_name="What action"),
            SlotDefinition(name="target", display_name="Which target"),
        ],
        confirmation_style=ConfirmationStyle.EXPLICIT,
    )


@pytest.fixture
def meeting_state(meeting_template):
    return SlotState(template=meeting_template)


# --- format_confirmation Tests ---


class TestFormatConfirmation:
    def test_implicit_confirmation(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        result = format_confirmation(meeting_state)
        assert "Got it" in result
        assert "Sarah" in result
        assert "Tuesday" in result

    def test_explicit_confirmation(self, explicit_template):
        state = SlotState(template=explicit_template)
        state.set_value("action", "delete")
        state.set_value("target", "database")
        result = format_confirmation(state)
        assert "I have:" in result
        assert "Is that correct?" in result
        assert "delete" in result
        assert "database" in result

    def test_empty_state_returns_empty(self, meeting_state):
        result = format_confirmation(meeting_state)
        assert result == ""

    def test_single_value(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        result = format_confirmation(meeting_state)
        assert "Sarah" in result


# --- format_prompt Tests ---


class TestFormatPrompt:
    def test_single_slot(self):
        missing = [SlotDefinition(name="topic", display_name="What's the topic")]
        result = format_prompt(missing)
        assert "topic" in result.lower()

    def test_empty_list(self):
        result = format_prompt([])
        assert result == ""

    def test_multiple_slots_delegates_to_grouped(self):
        missing = [
            SlotDefinition(name="who", display_name="Who"),
            SlotDefinition(name="when", display_name="When"),
        ]
        result = format_prompt(missing)
        # Should delegate to grouped format
        assert "who" in result.lower()
        assert "when" in result.lower()


# --- format_grouped_prompt Tests ---


class TestFormatGroupedPrompt:
    def test_two_slots(self):
        missing = [
            SlotDefinition(name="who", display_name="Who should attend"),
            SlotDefinition(name="when", display_name="When"),
        ]
        result = format_grouped_prompt(missing)
        assert "who should attend" in result.lower()
        assert "when" in result.lower()
        assert "and" in result.lower()

    def test_three_slots(self):
        missing = [
            SlotDefinition(name="who", display_name="Who"),
            SlotDefinition(name="when", display_name="When"),
            SlotDefinition(name="where", display_name="Where"),
        ]
        result = format_grouped_prompt(missing)
        assert "who" in result.lower()
        assert "when" in result.lower()
        assert "where" in result.lower()

    def test_single_slot_delegates(self):
        missing = [SlotDefinition(name="topic", display_name="Topic")]
        result = format_grouped_prompt(missing)
        assert "topic" in result.lower()

    def test_empty_list(self):
        result = format_grouped_prompt([])
        assert result == ""


# --- format_confirmation_with_prompt Tests ---


class TestFormatConfirmationWithPrompt:
    def test_confirmation_plus_single_missing(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        missing = [SlotDefinition(name="topic", display_name="Topic")]
        result = format_confirmation_with_prompt(meeting_state, missing)
        assert "Got it" in result
        assert "Sarah" in result
        assert "topic" in result.lower()

    def test_confirmation_plus_grouped_missing(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        missing = [
            SlotDefinition(name="day", display_name="Day"),
            SlotDefinition(name="time", display_name="Time"),
        ]
        result = format_confirmation_with_prompt(meeting_state, missing)
        assert "Got it" in result
        assert "Sarah" in result
        assert "day" in result.lower()
        assert "time" in result.lower()

    def test_no_filled_just_prompt(self, meeting_state):
        missing = [SlotDefinition(name="who", display_name="Who")]
        result = format_confirmation_with_prompt(meeting_state, missing)
        assert "Got it" not in result
        assert "who" in result.lower()

    def test_all_filled_no_missing(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        meeting_state.set_value("topic", "Q3 planning")
        result = format_confirmation_with_prompt(meeting_state, [])
        assert "Got it" in result
        assert "Sarah" in result

    def test_empty_everything(self, meeting_state):
        result = format_confirmation_with_prompt(meeting_state, [])
        assert result == ""


# --- format_final_confirmation Tests ---


class TestFormatFinalConfirmation:
    def test_implicit_final(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        meeting_state.set_value("topic", "Q3 planning")
        result = format_final_confirmation(meeting_state)
        assert "Done" in result
        assert "Sarah" in result
        assert "proceed" in result.lower()

    def test_explicit_final(self, explicit_template):
        state = SlotState(template=explicit_template)
        state.set_value("action", "deploy")
        state.set_value("target", "production")
        result = format_final_confirmation(state)
        assert "I have:" in result
        assert "Is that correct?" in result
        assert "deploy" in result
        assert "production" in result

    def test_includes_all_values(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        meeting_state.set_value("topic", "Q3 planning")
        result = format_final_confirmation(meeting_state)
        assert "Sarah" in result
        assert "Tuesday" in result
        assert "2pm" in result
        assert "Q3 planning" in result

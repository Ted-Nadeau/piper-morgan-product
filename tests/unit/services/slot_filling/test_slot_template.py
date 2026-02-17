"""
Tests for slot template data model.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Phase 1: SlotTemplate + SlotFillingState

Tests cover:
- SlotDefinition construction and defaults
- SlotTemplate validation and properties
- SlotState fill/unfill/query operations
- MEETING_TEMPLATE sanity checks
- SlotFillingState enum values
"""

import pytest

from services.shared_types import SlotFillingState
from services.slot_filling.slot_template import (
    MEETING_TEMPLATE,
    ConfirmationStyle,
    SlotDefinition,
    SlotState,
    SlotTemplate,
    SlotType,
)

# --- SlotDefinition Tests ---


class TestSlotDefinition:
    def test_construction_with_defaults(self):
        slot = SlotDefinition(name="topic", display_name="What's the topic")
        assert slot.name == "topic"
        assert slot.display_name == "What's the topic"
        assert slot.required is True
        assert slot.slot_type == SlotType.TEXT
        assert slot.extraction_hint is None
        assert slot.group is None

    def test_construction_with_all_fields(self):
        slot = SlotDefinition(
            name="attendee",
            display_name="Who should attend",
            required=True,
            slot_type=SlotType.ENTITY,
            extraction_hint="Person name(s)",
            group=0,
        )
        assert slot.name == "attendee"
        assert slot.slot_type == SlotType.ENTITY
        assert slot.extraction_hint == "Person name(s)"
        assert slot.group == 0

    def test_optional_slot(self):
        slot = SlotDefinition(name="notes", display_name="Any notes?", required=False)
        assert slot.required is False

    def test_frozen_immutable(self):
        slot = SlotDefinition(name="topic", display_name="Topic")
        with pytest.raises(AttributeError):
            slot.name = "changed"

    def test_all_slot_types(self):
        for slot_type in SlotType:
            slot = SlotDefinition(
                name=f"test_{slot_type.value}",
                display_name=f"Test {slot_type.value}",
                slot_type=slot_type,
            )
            assert slot.slot_type == slot_type


# --- SlotTemplate Tests ---


class TestSlotTemplate:
    def _make_slot(self, name="test", required=True, group=None):
        return SlotDefinition(
            name=name, display_name=f"Test {name}", required=required, group=group
        )

    def test_construction(self):
        template = SlotTemplate(
            name="test_flow",
            display_name="Test Flow",
            slots=[self._make_slot("item")],
        )
        assert template.name == "test_flow"
        assert template.display_name == "Test Flow"
        assert len(template.slots) == 1
        assert template.confirmation_style == ConfirmationStyle.IMPLICIT

    def test_explicit_confirmation(self):
        template = SlotTemplate(
            name="test",
            display_name="Test",
            slots=[self._make_slot("item")],
            confirmation_style=ConfirmationStyle.EXPLICIT,
        )
        assert template.confirmation_style == ConfirmationStyle.EXPLICIT

    def test_no_slots_raises(self):
        with pytest.raises(ValueError, match="must have at least one slot"):
            SlotTemplate(name="empty", display_name="Empty", slots=[])

    def test_no_required_slots_raises(self):
        with pytest.raises(ValueError, match="must have at least one required slot"):
            SlotTemplate(
                name="optional_only",
                display_name="Optional Only",
                slots=[self._make_slot("opt", required=False)],
            )

    def test_required_slots_property(self):
        template = SlotTemplate(
            name="mixed",
            display_name="Mixed",
            slots=[
                self._make_slot("req1", required=True),
                self._make_slot("opt1", required=False),
                self._make_slot("req2", required=True),
            ],
        )
        required = template.required_slots
        assert len(required) == 2
        assert required[0].name == "req1"
        assert required[1].name == "req2"

    def test_optional_slots_property(self):
        template = SlotTemplate(
            name="mixed",
            display_name="Mixed",
            slots=[
                self._make_slot("req1", required=True),
                self._make_slot("opt1", required=False),
                self._make_slot("opt2", required=False),
            ],
        )
        optional = template.optional_slots
        assert len(optional) == 2
        assert optional[0].name == "opt1"

    def test_groups_property(self):
        template = SlotTemplate(
            name="grouped",
            display_name="Grouped",
            slots=[
                self._make_slot("a", group=0),
                self._make_slot("b", group=0),
                self._make_slot("c", group=1),
                self._make_slot("d"),  # group=None
            ],
        )
        groups = template.groups
        assert len(groups[0]) == 2
        assert len(groups[1]) == 1
        assert len(groups[None]) == 1


# --- SlotState Tests ---


class TestSlotState:
    @pytest.fixture
    def template(self):
        return SlotTemplate(
            name="test",
            display_name="Test",
            slots=[
                SlotDefinition(name="who", display_name="Who", required=True),
                SlotDefinition(name="when", display_name="When", required=True),
                SlotDefinition(name="topic", display_name="Topic", required=True),
                SlotDefinition(name="notes", display_name="Notes", required=False),
            ],
        )

    def test_initial_state(self, template):
        state = SlotState(template=template)
        assert state.filled_count == 0
        assert state.total_count == 4
        assert not state.all_required_filled
        assert len(state.unfilled_required) == 3
        assert len(state.unfilled_optional) == 1

    def test_set_value(self, template):
        state = SlotState(template=template)
        state.set_value("who", "Sarah")
        assert state.get_value("who") == "Sarah"
        assert state.filled_count == 1

    def test_set_invalid_slot_raises(self, template):
        state = SlotState(template=template)
        with pytest.raises(ValueError, match="not in template"):
            state.set_value("nonexistent", "value")

    def test_update_existing_value(self, template):
        state = SlotState(template=template)
        state.set_value("who", "Sarah")
        state.set_value("who", "Jake")
        assert state.get_value("who") == "Jake"
        assert state.filled_count == 1  # Not double-counted

    def test_unfilled_required_decreases(self, template):
        state = SlotState(template=template)
        assert len(state.unfilled_required) == 3

        state.set_value("who", "Sarah")
        assert len(state.unfilled_required) == 2

        state.set_value("when", "Tuesday")
        assert len(state.unfilled_required) == 1

        state.set_value("topic", "Q3 planning")
        assert len(state.unfilled_required) == 0
        assert state.all_required_filled

    def test_optional_not_required_for_completion(self, template):
        state = SlotState(template=template)
        state.set_value("who", "Sarah")
        state.set_value("when", "Tuesday")
        state.set_value("topic", "Q3 planning")
        # Notes is optional — all_required_filled should be True
        assert state.all_required_filled
        assert len(state.unfilled_optional) == 1

    def test_clear_value(self, template):
        state = SlotState(template=template)
        state.set_value("who", "Sarah")
        state.clear_value("who")
        assert state.get_value("who") is None
        assert state.filled_count == 0

    def test_clear_nonexistent_value_no_error(self, template):
        state = SlotState(template=template)
        state.clear_value("who")  # Should not raise

    def test_clear_all(self, template):
        state = SlotState(template=template)
        state.set_value("who", "Sarah")
        state.set_value("when", "Tuesday")
        state.set_value("topic", "Q3 planning")
        state.current_prompt_group = 2

        state.clear_all()
        assert state.filled_count == 0
        assert state.current_prompt_group == 0

    def test_get_unfilled_value_returns_none(self, template):
        state = SlotState(template=template)
        assert state.get_value("who") is None

    def test_filling_optional_slot(self, template):
        state = SlotState(template=template)
        state.set_value("notes", "Bring laptop")
        assert state.get_value("notes") == "Bring laptop"
        assert len(state.unfilled_optional) == 0
        # But still not complete because required slots empty
        assert not state.all_required_filled


# --- MEETING_TEMPLATE Sanity Tests ---


class TestMeetingTemplate:
    def test_template_exists(self):
        assert MEETING_TEMPLATE is not None
        assert MEETING_TEMPLATE.name == "schedule_meeting"

    def test_has_four_slots(self):
        assert len(MEETING_TEMPLATE.slots) == 4

    def test_all_slots_required(self):
        assert all(s.required for s in MEETING_TEMPLATE.slots)

    def test_slot_names(self):
        names = [s.name for s in MEETING_TEMPLATE.slots]
        assert "attendee" in names
        assert "day" in names
        assert "time" in names
        assert "topic" in names

    def test_slot_types(self):
        slot_map = {s.name: s for s in MEETING_TEMPLATE.slots}
        assert slot_map["attendee"].slot_type == SlotType.ENTITY
        assert slot_map["day"].slot_type == SlotType.DATETIME
        assert slot_map["time"].slot_type == SlotType.DATETIME
        assert slot_map["topic"].slot_type == SlotType.TEXT

    def test_grouped_prompting(self):
        slot_map = {s.name: s for s in MEETING_TEMPLATE.slots}
        # attendee, day, time in group 0 (asked together)
        assert slot_map["attendee"].group == 0
        assert slot_map["day"].group == 0
        assert slot_map["time"].group == 0
        # topic in group 1 (asked separately)
        assert slot_map["topic"].group == 1

    def test_implicit_confirmation(self):
        assert MEETING_TEMPLATE.confirmation_style == ConfirmationStyle.IMPLICIT

    def test_extraction_hints_present(self):
        for slot in MEETING_TEMPLATE.slots:
            assert slot.extraction_hint is not None, f"Slot '{slot.name}' missing extraction hint"


# --- SlotFillingState Enum Tests ---


class TestSlotFillingState:
    def test_all_states_exist(self):
        assert SlotFillingState.EXTRACTING == "extracting"
        assert SlotFillingState.PROMPTING == "prompting"
        assert SlotFillingState.CONFIRMING == "confirming"
        assert SlotFillingState.COMPLETE == "complete"
        assert SlotFillingState.CANCELLED == "cancelled"

    def test_state_count(self):
        assert len(SlotFillingState) == 5

    def test_string_enum(self):
        # Should be usable as string (for serialization)
        assert str(SlotFillingState.EXTRACTING) == "SlotFillingState.EXTRACTING"
        assert SlotFillingState.EXTRACTING.value == "extracting"

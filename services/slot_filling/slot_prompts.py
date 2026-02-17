"""
Prompt formatting for slot-filling conversations.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation

Generates natural-sounding prompts and confirmations:
- Implicit confirmations: "Got it — meeting with Sarah, Tuesday at 2pm. What's the topic?"
- Grouped prompts: "Who should attend, and when works?"
- Single slot prompts: "What's the topic?"
"""

from services.slot_filling.slot_template import ConfirmationStyle, SlotDefinition, SlotState


def format_confirmation(state: SlotState) -> str:
    """
    Format a confirmation message summarizing filled slots.

    Uses implicit or explicit style based on template setting.

    Args:
        state: Current slot state with filled values

    Returns:
        Natural-language confirmation string
    """
    if not state.filled_slots:
        return ""

    summary = _build_slot_summary(state)

    if state.template.confirmation_style == ConfirmationStyle.EXPLICIT:
        return f"I have: {summary}. Is that correct?"

    # Implicit: just state what we have
    return f"Got it — {summary}."


def format_prompt(missing: list[SlotDefinition]) -> str:
    """
    Format a prompt for a single missing slot.

    Args:
        missing: List with one slot definition

    Returns:
        Natural question for the missing slot
    """
    if not missing:
        return ""

    if len(missing) == 1:
        return f"What's the {missing[0].display_name.lower()}?"

    # Fallback for multiple — use grouped format
    return format_grouped_prompt(missing)


def format_grouped_prompt(missing: list[SlotDefinition]) -> str:
    """
    Format a prompt for multiple missing slots (grouped prompting).

    Asks for 2-3 related slots in a natural way.

    Args:
        missing: List of 2-3 slot definitions to ask about

    Returns:
        Natural grouped question
    """
    if not missing:
        return ""

    if len(missing) == 1:
        return format_prompt(missing)

    names = [s.display_name.lower() for s in missing]

    if len(names) == 2:
        return f"What's the {names[0]}, and {names[1]}?"

    # 3+ slots: "What's the X, Y, and Z?"
    return f"What's the {', '.join(names[:-1])}, and {names[-1]}?"


def format_confirmation_with_prompt(state: SlotState, missing: list[SlotDefinition]) -> str:
    """
    Format a combined confirmation + prompt for missing slots.

    This is the natural pattern: "Got it — X and Y. What about Z?"

    Args:
        state: Current slot state with filled values
        missing: Remaining missing slot definitions

    Returns:
        Combined confirmation and prompt string
    """
    if not state.filled_slots and not missing:
        return ""

    parts = []

    # Add confirmation of what we have
    if state.filled_slots:
        summary = _build_slot_summary(state)
        parts.append(f"Got it — {summary}.")

    # Add prompt for what's missing
    if missing:
        if len(missing) == 1:
            parts.append(f"What's the {missing[0].display_name.lower()}?")
        else:
            parts.append(format_grouped_prompt(missing))

    return " ".join(parts)


def format_final_confirmation(state: SlotState) -> str:
    """
    Format the final confirmation when all required slots are filled.

    Args:
        state: Fully-filled slot state

    Returns:
        Confirmation asking user to proceed
    """
    summary = _build_slot_summary(state)

    if state.template.confirmation_style == ConfirmationStyle.EXPLICIT:
        return f"I have: {summary}. Is that correct?"

    return f"Done — {summary}. Want me to proceed?"


def _build_slot_summary(state: SlotState) -> str:
    """
    Build a natural-language summary of filled slot values.

    Follows the template's slot order for consistent output.
    """
    parts = []
    for slot in state.template.slots:
        value = state.get_value(slot.name)
        if value is not None:
            parts.append(str(value))

    if not parts:
        return ""

    if len(parts) == 1:
        return parts[0]

    if len(parts) == 2:
        return f"{parts[0]}, {parts[1]}"

    return f"{', '.join(parts[:-1])}, {parts[-1]}"

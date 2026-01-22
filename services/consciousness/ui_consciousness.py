"""
Consciousness Wrapper for UI Elements and Templates

Transforms static UI text into warm, inviting expression.
Issue: #638 CONSCIOUSNESS-TRANSFORM: HTML Templates
ADR: ADR-056 Consciousness Expression Patterns

This module provides helpers for:
- Empty state messages
- Confirmation dialogs
- Toast notifications
- Button labels

Usage:
    from services.consciousness.ui_consciousness import (
        format_empty_state_conscious,
        format_delete_confirmation_conscious,
        format_toast_success_conscious,
    )

    # Empty state for a todos list
    message = format_empty_state_conscious("todos")
    # Returns: "Nothing here yet. Ready to add your first todo?"

    # Delete confirmation
    message = format_delete_confirmation_conscious("todo", "Buy groceries")
    # Returns: 'Remove "Buy groceries"? This can\'t be undone.'
"""

from typing import Optional

# Empty state messages by entity type - warm and inviting
EMPTY_STATE_MESSAGES = {
    "todos": "Nothing here yet. Ready to add your first todo?",
    "files": "No files uploaded yet. Want to add something?",
    "projects": "No projects set up yet. Shall we create one?",
    "lists": "No lists created yet. Want to organize something?",
    "conversations": "No conversations yet. What would you like to talk about?",
    "integrations": "No integrations connected yet. Want to set one up?",
    "items": "Nothing here yet. Ready to add your first item?",
    "default": "Nothing here yet. Ready to get started?",
}

# Empty state titles by entity type
EMPTY_STATE_TITLES = {
    "todos": "All clear",
    "files": "Empty folder",
    "projects": "Fresh start",
    "lists": "Clean slate",
    "conversations": "Ready to chat",
    "integrations": "Not connected yet",
    "items": "Nothing here",
    "default": "Nothing here yet",
}

# Icons for empty states
EMPTY_STATE_ICONS = {
    "todos": "✨",
    "files": "📁",
    "projects": "🚀",
    "lists": "📋",
    "conversations": "💬",
    "integrations": "🔌",
    "items": "📭",
    "default": "📭",
}

# CTA text for empty states
EMPTY_STATE_CTAS = {
    "todos": "Add a todo",
    "files": "Upload a file",
    "projects": "Create project",
    "lists": "New list",
    "conversations": "Start chatting",
    "integrations": "Connect",
    "items": "Add item",
    "default": "Get started",
}

# Button label mappings - conversational style
BUTTON_LABELS = {
    "delete": "Remove this",
    "save": "Save changes",
    "cancel": "Never mind",
    "submit": "Send it",
    "create": "Create new",
    "upload": "Add file",
    "confirm": "Yes, do it",
    "edit": "Make changes",
    "close": "Close",
    "done": "All done",
}


def format_empty_state_conscious(entity_type: str) -> str:
    """
    Format empty state message with consciousness.

    Args:
        entity_type: Type of entity (todos, files, projects, etc.)

    Returns:
        Warm, inviting message for the empty state

    Examples:
        >>> format_empty_state_conscious("todos")
        "Nothing here yet. Ready to add your first todo?"
        >>> format_empty_state_conscious("files")
        "No files uploaded yet. Want to add something?"
    """
    return EMPTY_STATE_MESSAGES.get(entity_type.lower(), EMPTY_STATE_MESSAGES["default"])


def format_empty_state_title_conscious(entity_type: str) -> str:
    """
    Format empty state title with consciousness.

    Args:
        entity_type: Type of entity (todos, files, projects, etc.)

    Returns:
        Short, friendly title for the empty state

    Examples:
        >>> format_empty_state_title_conscious("todos")
        "All clear"
        >>> format_empty_state_title_conscious("files")
        "Empty folder"
    """
    return EMPTY_STATE_TITLES.get(entity_type.lower(), EMPTY_STATE_TITLES["default"])


def get_empty_state_icon(entity_type: str) -> str:
    """
    Get appropriate icon for an empty state.

    Args:
        entity_type: Type of entity (todos, files, projects, etc.)

    Returns:
        Emoji icon appropriate for the entity type
    """
    return EMPTY_STATE_ICONS.get(entity_type.lower(), EMPTY_STATE_ICONS["default"])


def get_empty_state_cta(entity_type: str) -> str:
    """
    Get appropriate CTA button text for an empty state.

    Args:
        entity_type: Type of entity (todos, files, projects, etc.)

    Returns:
        Action-oriented CTA text
    """
    return EMPTY_STATE_CTAS.get(entity_type.lower(), EMPTY_STATE_CTAS["default"])


def format_delete_confirmation_conscious(
    entity_type: str, entity_name: Optional[str] = None
) -> str:
    """
    Format delete confirmation with clarity and appropriate weight.

    Args:
        entity_type: Type of entity being deleted (todo, file, project, etc.)
        entity_name: Optional name of the specific item

    Returns:
        Clear confirmation message that names the item and warns about permanence

    Examples:
        >>> format_delete_confirmation_conscious("todo", "Buy groceries")
        'Remove "Buy groceries"? This can\\'t be undone.'
        >>> format_delete_confirmation_conscious("project")
        "Remove this project? This can't be undone."
    """
    if entity_name:
        return f'Remove "{entity_name}"? This can\'t be undone.'
    return f"Remove this {entity_type}? This can't be undone."


def format_toast_success_conscious(action: str, target: str) -> str:
    """
    Format success toast with warm acknowledgment.

    Args:
        action: The action performed (saved, created, updated, etc.)
        target: What the action was performed on

    Returns:
        Warm success message with identity

    Examples:
        >>> format_toast_success_conscious("saved", "your settings")
        "Done - I've saved your settings."
        >>> format_toast_success_conscious("created", "the project")
        "Done - I've created the project."
    """
    return f"Done - I've {action} {target}."


def format_toast_error_conscious(attempted_action: str) -> str:
    """
    Format error toast with recovery path, not blame.

    Args:
        attempted_action: What was being attempted (save your changes, upload the file, etc.)

    Returns:
        Helpful error message that offers recovery

    Examples:
        >>> format_toast_error_conscious("save your changes")
        "I couldn't save your changes. Want to try again?"
        >>> format_toast_error_conscious("upload the file")
        "I couldn't upload the file. Want to try again?"
    """
    return f"I couldn't {attempted_action}. Want to try again?"


def format_toast_delete_conscious(entity_type: str) -> str:
    """
    Format delete confirmation toast with reassurance.

    Args:
        entity_type: Type of entity that was deleted

    Returns:
        Reassuring confirmation that the deletion is complete

    Examples:
        >>> format_toast_delete_conscious("todo")
        "Removed. The todo is gone."
        >>> format_toast_delete_conscious("file")
        "Removed. The file is gone."
    """
    return f"Removed. The {entity_type} is gone."


def format_button_label_conscious(action: str) -> str:
    """
    Format button labels conversationally.

    Args:
        action: The button action (delete, save, cancel, etc.)

    Returns:
        Conversational button label

    Examples:
        >>> format_button_label_conscious("delete")
        "Remove this"
        >>> format_button_label_conscious("cancel")
        "Never mind"
        >>> format_button_label_conscious("foobar")
        "Foobar"
    """
    return BUTTON_LABELS.get(action.lower(), action.title())


# Template helper combining all empty state data
def get_empty_state_data(entity_type: str) -> dict:
    """
    Get all empty state data for a template.

    Returns a dict ready for Jinja2 template rendering with:
    - icon: Emoji icon
    - title: Short friendly title
    - message: Inviting message
    - cta_text: Call to action button text

    Args:
        entity_type: Type of entity (todos, files, projects, etc.)

    Returns:
        Dict with icon, title, message, cta_text keys
    """
    normalized = entity_type.lower()
    return {
        "icon": get_empty_state_icon(normalized),
        "title": format_empty_state_title_conscious(normalized),
        "message": format_empty_state_conscious(normalized),
        "cta_text": get_empty_state_cta(normalized),
    }

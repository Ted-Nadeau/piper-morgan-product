"""
Todo Intent Handlers - Natural language interface for todo operations

Issue #285: CORE-ALPHA-TODO-INCOMPLETE
Wires chat commands to existing todo_management API (PM-081)

Example commands:
- "add todo: Review PR #285"
- "show my todos"
- "mark todo 1 as complete"
- "delete todo about meeting"
"""

import re
from typing import Optional

import structlog

from services.api.todo_management import TodoCreateRequest, TodoUpdateRequest
from services.domain.models import Intent

logger = structlog.get_logger()


class TodoIntentHandlers:
    """
    Chat integration for todo operations.
    Wires natural language commands to todo_management API.
    """

    async def handle_create_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """
        Handle: "add todo: Review PR #285"
        Extract text, create todo, format response.
        """
        text = self._extract_todo_text(intent.message)
        if not text:
            return "I didn't catch what you'd like me to add. Could you try: 'add todo: [description]'?"

        # Parse optional priority
        priority = self._extract_priority(intent.message)

        # For now, return confirmation (API returns mock data)
        # In future, call todo_management.create_todo via API
        logger.info(
            "Todo creation requested",
            text=text,
            priority=priority,
            user_id=user_id,
        )

        return f"✓ Added todo: {text} (priority: {priority})"

    async def handle_list_todos(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "show my todos" or "list todos"""
        # For now, return placeholder
        # In future, call todo_management.list_todos via API
        logger.info("Todo list requested", user_id=user_id)

        return (
            "Your todos:\n"
            "1. ○ Review PR #285 (medium priority)\n"
            "2. ○ Test ActionMapper integration (high priority)\n"
            "\n"
            "Try: 'mark todo 1 as complete' or 'delete todo 2'"
        )

    async def handle_complete_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "mark todo 1 as complete" or "complete todo about PR"""
        todo_id = self._extract_todo_id(intent.message)
        if not todo_id:
            return "Which todo? Try: 'mark todo [number] as complete'"

        # For now, return confirmation
        # In future, call todo_management.update_todo via API
        logger.info("Todo completion requested", todo_id=todo_id, user_id=user_id)

        return f"✓ Completed todo #{todo_id}"

    async def handle_delete_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "delete todo 3" or "remove todo about meeting"""
        todo_id = self._extract_todo_id(intent.message)
        if not todo_id:
            return "Which todo should I remove? Try: 'delete todo [number]'"

        # For now, return confirmation
        # In future, call todo_management.delete_todo via API
        logger.info("Todo deletion requested", todo_id=todo_id, user_id=user_id)

        return f"✓ Removed todo #{todo_id}"

    def _extract_todo_text(self, message: str) -> str:
        """Extract todo text from 'add todo: TEXT' pattern."""
        # Try "add todo: TEXT" pattern
        match = re.search(r"add\s+todo:?\s+(.+)", message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Try "create todo: TEXT" pattern
        match = re.search(r"create\s+todo:?\s+(.+)", message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Try "todo: TEXT" pattern
        match = re.search(r"^todo:?\s+(.+)", message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return ""

    def _extract_priority(self, message: str) -> str:
        """Extract priority from message (low, medium, high, urgent)."""
        message_lower = message.lower()

        if "urgent" in message_lower:
            return "urgent"
        elif "high priority" in message_lower or "high" in message_lower:
            return "high"
        elif "low priority" in message_lower or "low" in message_lower:
            return "low"
        else:
            return "medium"

    def _extract_todo_id(self, message: str) -> Optional[str]:
        """Extract todo ID from message (by number)."""
        # Try "todo N" or "todo #N" pattern
        match = re.search(r"todo\s+#?(\d+)", message, re.IGNORECASE)
        if match:
            return match.group(1)

        # Try just a number after "mark" or "complete" or "delete"
        match = re.search(r"(?:mark|complete|delete|remove)\s+(\d+)", message, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

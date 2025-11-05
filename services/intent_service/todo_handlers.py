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
from uuid import UUID

import structlog

from services.api.todo_management import TodoCreateRequest, TodoUpdateRequest
from services.domain.models import Intent
from services.todo.todo_management_service import TodoManagementService

logger = structlog.get_logger()


class TodoIntentHandlers:
    """
    Chat integration for todo operations.
    Wires natural language commands to TodoManagementService for persistence.
    """

    def __init__(self):
        """Initialize with TodoManagementService."""
        self.todo_service = TodoManagementService()

    async def handle_create_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """
        Handle: "add todo: Review PR #285"
        Extract text, create todo with database persistence, format response.
        """
        text = self._extract_todo_text(intent.original_message)
        if not text:
            return "I didn't catch what you'd like me to add. Could you try: 'add todo: [description]'?"

        # Parse optional priority
        priority = self._extract_priority(intent.original_message)

        try:
            # Create todo via service (database persistence)
            todo = await self.todo_service.create_todo(
                user_id=user_id, text=text, priority=priority
            )

            logger.info(
                "Todo created successfully",
                todo_id=str(todo.id),
                text=text,
                priority=priority,
                user_id=user_id,
            )

            # Format response with actual todo ID
            response = f"✓ Added todo #{str(todo.id)[:8]}: {todo.text}"
            if priority != "medium":
                response += f" (priority: {priority})"

            return response

        except ValueError as e:
            logger.warning("Todo creation validation failed", error=str(e), user_id=user_id)
            return f"I had trouble with that: {str(e)}"

        except Exception as e:
            logger.error("Todo creation failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble adding that todo. Could you try again?"

    async def handle_list_todos(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "show my todos" or "list todos" - shows active todos from database."""
        try:
            # Get active todos from database
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            logger.info("Todo list retrieved", user_id=user_id, count=len(todos))

            if not todos:
                return "You don't have any active todos. Try: 'add todo: [task]'"

            # Format todo list
            lines = ["Your active todos:"]
            for idx, todo in enumerate(todos, 1):
                status = "●" if todo.completed else "○"
                priority_marker = ""
                if todo.priority == "urgent":
                    priority_marker = " 🔴"
                elif todo.priority == "high":
                    priority_marker = " 🟡"

                # Truncate long text for readability
                text = todo.text[:60] + "..." if len(todo.text) > 60 else todo.text
                lines.append(f"{idx}. {status} {text}{priority_marker}")

            lines.append("")
            lines.append(f"Total: {len(todos)} active todos")
            lines.append("Try: 'mark todo [number] as complete' or 'delete todo [number]'")

            return "\n".join(lines)

        except Exception as e:
            logger.error("Todo list retrieval failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble getting your todos. Could you try again?"

    async def handle_complete_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "mark todo 1 as complete" or "complete todo about PR"""
        todo_number = self._extract_todo_id(intent.original_message)
        if not todo_number:
            return "Which todo? Try: 'mark todo [number] as complete'"

        try:
            # Get user's todo list to find the todo by position
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            # Convert todo number to index
            try:
                idx = int(todo_number) - 1
                if idx < 0 or idx >= len(todos):
                    return (
                        f"I couldn't find todo #{todo_number}. You have {len(todos)} active todos."
                    )
            except ValueError:
                return f"'{todo_number}' doesn't look like a number. Try: 'mark todo 1 as complete'"

            # Get the todo at that position
            todo = todos[idx]

            # Mark as complete
            completed_todo = await self.todo_service.complete_todo(todo_id=todo.id, user_id=user_id)

            if completed_todo:
                logger.info("Todo completed", todo_id=str(todo.id), user_id=user_id)
                return f"✓ Completed: {completed_todo.text}"
            else:
                return f"I couldn't complete that todo. It might have been deleted."

        except Exception as e:
            logger.error("Todo completion failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble completing that todo. Could you try again?"

    async def handle_delete_todo(self, intent: Intent, session_id: str, user_id: str) -> str:
        """Handle: "delete todo 3" or "remove todo about meeting"""
        todo_number = self._extract_todo_id(intent.original_message)
        if not todo_number:
            return "Which todo should I remove? Try: 'delete todo [number]'"

        try:
            # Get user's todo list to find the todo by position
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            # Convert todo number to index
            try:
                idx = int(todo_number) - 1
                if idx < 0 or idx >= len(todos):
                    return (
                        f"I couldn't find todo #{todo_number}. You have {len(todos)} active todos."
                    )
            except ValueError:
                return f"'{todo_number}' doesn't look like a number. Try: 'delete todo 1'"

            # Get the todo at that position
            todo = todos[idx]
            todo_text = todo.text

            # Delete the todo
            deleted = await self.todo_service.delete_todo(todo_id=todo.id, user_id=user_id)

            if deleted:
                logger.info("Todo deleted", todo_id=str(todo.id), user_id=user_id)
                return f"✓ Removed: {todo_text}"
            else:
                return f"I couldn't delete that todo. It might have already been removed."

        except Exception as e:
            logger.error("Todo deletion failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble deleting that todo. Could you try again?"

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

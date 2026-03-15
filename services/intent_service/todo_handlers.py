"""
Todo Intent Handlers - Natural language interface for todo operations

Issue #285: CORE-ALPHA-TODO-INCOMPLETE
Wires chat commands to existing todo_management API (PM-081)

Enhanced with consciousness injection (#407 MUX-VISION-STANDUP-EXTRACT)
for more alive, present-feeling responses.

Issue #904: CANONICAL-TODO-COMPLETE — Added fuzzy text matching for
completion ("complete the PR review" matches "Review the PR for auth").

Example commands:
- "add todo: Review PR #285"
- "show my todos"
- "show all my todos" (includes completed)
- "mark todo 1 as complete"
- "complete the PR review todo"
- "delete todo about meeting"
"""

import re
from typing import List, Optional, Tuple
from uuid import UUID

import structlog

from services.api.todo_management import TodoCreateRequest, TodoUpdateRequest
from services.consciousness.todo_consciousness import (
    format_next_todo_conscious,
    format_todo_completed_conscious,
    format_todo_created_conscious,
    format_todo_deleted_conscious,
    format_todo_list_conscious,
)
from services.domain.models import Intent, Todo
from services.todo.todo_management_service import TodoManagementService

logger = structlog.get_logger()

# Words that don't contribute to meaningful matching
_STOPWORDS = frozenset({
    "a", "an", "the", "in", "on", "at", "to", "for", "of", "with",
    "and", "or", "but", "is", "it", "my", "your", "this", "that",
    "i", "me", "we", "do", "did", "has", "have", "had", "be", "been",
    "todo", "task", "item", "thing",
})

# Minimum fuzzy match score to consider a match
_FUZZY_MATCH_THRESHOLD = 0.3


class TodoIntentHandlers:
    """
    Chat integration for todo operations.
    Wires natural language commands to TodoManagementService for persistence.
    """

    def __init__(self):
        """Initialize with TodoManagementService."""
        self.todo_service = TodoManagementService()

    async def handle_create_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """
        Handle: "add todo: Review PR #285"
        Extract text, create todo with database persistence, format response.
        """
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")

        text = self._extract_todo_text(original_message)
        if not text:
            return "I didn't catch what you'd like me to add. Could you try: 'add todo: [description]'?"

        # Parse optional priority
        priority = self._extract_priority(original_message)

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

            # Format response with consciousness
            return format_todo_created_conscious(todo)

        except ValueError as e:
            logger.warning("Todo creation validation failed", error=str(e), user_id=user_id)
            return f"I had trouble with that: {str(e)}"

        except Exception as e:
            logger.error("Todo creation failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble saving that todo — it may be a temporary issue. You can try again, or rephrase with 'add todo: [your task]'."

    async def handle_list_todos(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "show my todos" or "list todos" - shows active todos from database.

        Issue #904: Now supports "show all my todos" to include completed items.
        """
        try:
            original_message = intent.original_message or intent.context.get("original_message", "")
            include_completed = self._wants_completed_todos(original_message)

            # Get todos from database
            todos = await self.todo_service.list_todos(
                user_id=user_id, include_completed=include_completed
            )

            logger.info(
                "Todo list retrieved",
                user_id=user_id,
                count=len(todos),
                include_completed=include_completed,
            )

            # Format with consciousness
            return format_todo_list_conscious(todos, include_completed=include_completed)

        except Exception as e:
            logger.error("Todo list retrieval failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble loading your todos right now. You can try 'show my todos' again in a moment, or add a new one with 'add todo: [task]'."

    async def handle_next_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "what's my next todo?" or "next task" - shows highest priority todo."""
        try:
            # Get active todos from database (already sorted by priority)
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            logger.info("Next todo retrieved", user_id=user_id, has_todos=len(todos) > 0)

            if not todos:
                return (
                    "I checked your todo list and it's empty - nothing pending! "
                    "If something comes to mind, just say 'add todo: [task]'."
                )

            # Get the first todo (highest priority due to sorting in repository)
            next_todo = todos[0]

            # Format with consciousness
            return format_next_todo_conscious(next_todo, len(todos))

        except Exception as e:
            logger.error("Next todo retrieval failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble finding your next todo right now. You can try 'show my todos' to see your full list, or ask again in a moment."

    async def handle_complete_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "mark todo 1 as complete" or "complete the PR review todo"

        Issue #904: Supports both number-based and fuzzy text-based matching.
        Number path: "mark todo 3 as complete" → completes todo #3 by position.
        Text path: "complete the PR review" → fuzzy matches against todo texts.
        """
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")

        try:
            # Get user's todo list
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            if not todos:
                return (
                    "You don't have any active todos to complete. "
                    "Add one with 'add todo: [task]' first."
                )

            # Path 1: Try number-based matching first
            todo_number = self._extract_todo_id(original_message)
            if todo_number is not None:
                try:
                    idx = int(todo_number) - 1
                    if idx < 0 or idx >= len(todos):
                        return (
                            f"I couldn't find todo #{todo_number}. "
                            f"You have {len(todos)} active todos."
                        )
                    todo = todos[idx]
                except ValueError:
                    return (
                        f"'{todo_number}' doesn't look like a number. "
                        "Try: 'mark todo 1 as complete'"
                    )
            else:
                # Path 2: Fuzzy text matching (Issue #904)
                completion_text = self._extract_completion_text(original_message)
                if not completion_text:
                    return (
                        "Which todo would you like to complete? "
                        "Try 'complete todo 1' or 'complete the [description]'."
                    )

                todo = self._find_best_matching_todo(completion_text, todos)
                if todo is None:
                    return (
                        f"I couldn't find a todo matching '{completion_text}'. "
                        "Try 'show my todos' to see your list, then "
                        "'complete todo [number]'."
                    )

            # Mark as complete
            completed_todo = await self.todo_service.complete_todo(
                todo_id=todo.id, user_id=user_id
            )

            if completed_todo:
                logger.info("Todo completed", todo_id=str(todo.id), user_id=user_id)
                return format_todo_completed_conscious(completed_todo)
            else:
                return "I couldn't complete that todo. It might have been deleted."

        except Exception as e:
            logger.error(
                "Todo completion failed", error=str(e), user_id=user_id, exc_info=True
            )
            return (
                "I had trouble marking that as complete. You can try again with "
                "'complete todo [number]', or say 'show my todos' to check the list first."
            )

    async def handle_delete_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "delete todo 3" or "remove todo about meeting"""
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")
        todo_number = self._extract_todo_id(original_message)
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
                return format_todo_deleted_conscious(todo_text)
            else:
                return "I couldn't delete that todo. It might have already been removed."

        except Exception as e:
            logger.error("Todo deletion failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble removing that todo. You can try again with 'delete todo [number]', or say 'show my todos' to verify the list."

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

    # ------------------------------------------------------------------
    # Issue #904: Fuzzy text matching for todo completion
    # ------------------------------------------------------------------

    def _extract_completion_text(self, message: str) -> Optional[str]:
        """Extract the descriptive text from a completion request.

        Extracts the part of the message that describes which todo to complete.
        Returns None if the message uses a number (handled by _extract_todo_id).

        Examples:
            "complete the PR review todo" → "PR review"
            "finish the deployment task" → "deployment"
            "mark todo 3 as complete" → None (number-based)
        """
        # If a number is present, defer to number-based path
        if self._extract_todo_id(message) is not None:
            return None

        # Try various completion patterns and extract the descriptive part
        patterns = [
            # "complete the X todo/task"
            r"(?:complete|finish|done with)\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
            # "mark the X as done/complete"
            r"mark\s+(?:the\s+)?(.+?)\s+(?:as\s+)?(?:done|complete|finished)",
            # "mark done: X" or "mark done the X"
            r"mark\s+done:?\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
            # "I'm done with X"
            r"(?:i'?m\s+)?done\s+with\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                # Clean up trailing noise
                text = re.sub(r"\s+(todo|task|item|thing)$", "", text, flags=re.IGNORECASE)
                if text:
                    return text

        return None

    def _find_best_matching_todo(
        self, search_text: str, todos: List[Todo]
    ) -> Optional[Todo]:
        """Find the todo that best matches the search text using fuzzy word overlap.

        Returns the best matching todo if score >= threshold, else None.
        """
        if not todos or not search_text:
            return None

        scored: List[Tuple[float, Todo]] = []
        for todo in todos:
            score = self._fuzzy_match_score(search_text, todo.text)
            if score >= _FUZZY_MATCH_THRESHOLD:
                scored.append((score, todo))

        if not scored:
            return None

        # Sort by score descending, return best match
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    @staticmethod
    def _fuzzy_match_score(query: str, candidate: str) -> float:
        """Score how well query words match candidate words (0.0 to 1.0).

        Uses word overlap with stopword filtering. Score is the fraction
        of meaningful query words found in the candidate.
        """
        query_words = {
            w for w in re.findall(r"\w+", query.lower()) if w not in _STOPWORDS
        }
        candidate_words = {
            w for w in re.findall(r"\w+", candidate.lower()) if w not in _STOPWORDS
        }

        if not query_words:
            return 0.0

        overlap = query_words & candidate_words
        return len(overlap) / len(query_words)

    @staticmethod
    def _wants_completed_todos(message: str) -> bool:
        """Check if the user wants to see completed todos too.

        Issue #904: "show all my todos" or "show completed todos" includes done items.
        """
        message_lower = message.lower()
        return any(
            phrase in message_lower
            for phrase in [
                "all my todos",
                "all todos",
                "completed todos",
                "done todos",
                "finished todos",
                "including completed",
                "include completed",
                "show everything",
            ]
        )

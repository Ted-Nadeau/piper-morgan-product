"""
Unit tests for Todo Query Handlers (Issue #518 - Queries #56 and #57)

Tests the canonical query handlers for:
- Query #56: "Show my todos" - list todos
- Query #57: "What's my next todo?" - next todo recommendation
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.todo_handlers import TodoIntentHandlers


class TestTodoQueryHandlers:
    """Test todo query handlers for canonical queries"""

    @pytest.fixture
    def handlers(self):
        """Create TodoIntentHandlers instance"""
        return TodoIntentHandlers()

    @pytest.fixture
    def mock_todo_service(self):
        """Create a mock TodoManagementService"""
        mock_service = MagicMock()
        mock_service.list_todos = AsyncMock(return_value=[])
        return mock_service

    # Query #56: "Show my todos" Tests
    @pytest.mark.asyncio
    async def test_list_todos_returns_formatted_list(self, handlers, mock_todo_service):
        """Test list_todos returns a formatted todo list with mock data"""
        # Create mock todos
        mock_todo_1 = MagicMock()
        mock_todo_1.text = "Review PR #285"
        mock_todo_1.completed = False
        mock_todo_1.priority = "high"

        mock_todo_2 = MagicMock()
        mock_todo_2.text = "Write documentation"
        mock_todo_2.completed = False
        mock_todo_2.priority = "medium"

        mock_todo_service.list_todos.return_value = [mock_todo_1, mock_todo_2]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="list_todos",
            original_message="show my todos",
            confidence=0.9,
        )

        result = await handlers.handle_list_todos(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify result contains todo text
        assert "Review PR #285" in result
        assert "Write documentation" in result
        assert "2 active todos" in result

    @pytest.mark.asyncio
    async def test_list_todos_handles_no_todos(self, handlers, mock_todo_service):
        """Test list_todos gracefully handles empty todo list"""
        mock_todo_service.list_todos.return_value = []
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="list_todos",
            original_message="show my todos",
            confidence=0.9,
        )

        result = await handlers.handle_list_todos(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify helpful message when no todos
        assert "don't have any active todos" in result.lower()
        assert "add todo" in result.lower()

    # Query #57: "What's my next todo?" Tests
    @pytest.mark.asyncio
    async def test_next_todo_returns_highest_priority(self, handlers, mock_todo_service):
        """Test next_todo returns the highest priority todo (first in sorted list)"""
        # Create mock todos (already sorted by priority in service)
        mock_high_priority = MagicMock()
        mock_high_priority.text = "Fix critical bug"
        mock_high_priority.priority = "urgent"
        mock_high_priority.due_date = None
        mock_high_priority.context = None

        mock_low_priority = MagicMock()
        mock_low_priority.text = "Update readme"
        mock_low_priority.priority = "low"
        mock_low_priority.due_date = None
        mock_low_priority.context = None

        mock_todo_service.list_todos.return_value = [mock_high_priority, mock_low_priority]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what's my next todo?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify it returns the high priority todo, not the low priority one
        assert "Fix critical bug" in result
        assert "Update readme" not in result
        assert "Your next todo" in result

    @pytest.mark.asyncio
    async def test_next_todo_handles_no_todos(self, handlers, mock_todo_service):
        """Test next_todo gracefully handles empty todo list"""
        mock_todo_service.list_todos.return_value = []
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="next task",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify helpful message when no todos
        assert "don't have any active todos" in result.lower()
        assert "add todo" in result.lower()

    @pytest.mark.asyncio
    async def test_next_todo_includes_priority_icon(self, handlers, mock_todo_service):
        """Test next_todo includes priority icon in response"""
        # Test urgent priority
        mock_urgent = MagicMock()
        mock_urgent.text = "Critical task"
        mock_urgent.priority = "urgent"
        mock_urgent.due_date = None
        mock_urgent.context = None

        mock_todo_service.list_todos.return_value = [mock_urgent]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what should I do next?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify urgent priority icon is present
        assert "🔴" in result
        assert "Critical task" in result

    @pytest.mark.asyncio
    async def test_next_todo_includes_due_date(self, handlers, mock_todo_service):
        """Test next_todo includes due date when present"""
        from datetime import datetime

        mock_todo = MagicMock()
        mock_todo.text = "Submit report"
        mock_todo.priority = "high"
        mock_todo.due_date = datetime(2025, 12, 31)
        mock_todo.context = None

        mock_todo_service.list_todos.return_value = [mock_todo]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="next task",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify due date is included
        assert "Due:" in result
        assert "2025-12-31" in result
        assert "Submit report" in result

    @pytest.mark.asyncio
    async def test_next_todo_includes_context(self, handlers, mock_todo_service):
        """Test next_todo includes context when present"""
        mock_todo = MagicMock()
        mock_todo.text = "Review code"
        mock_todo.priority = "medium"
        mock_todo.due_date = None
        mock_todo.context = "PR #518 - Todo query handlers"

        mock_todo_service.list_todos.return_value = [mock_todo]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what's next?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify context is included
        assert "Context:" in result
        assert "PR #518 - Todo query handlers" in result
        assert "Review code" in result


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)"""

    def test_list_todos_query_routes_to_query_category(self):
        """Test 'show my todos' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory

        result = PreClassifier.pre_classify("show my todos")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "list_todos_query"
        assert result.confidence == 1.0

    def test_list_todos_query_variants(self):
        """Test list todos query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory

        test_cases = [
            "show my todos",
            "list my todos",
            "what are my todos",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "list_todos_query", f"Wrong action for: {query}"

    def test_next_todo_query_routes_to_query_category(self):
        """Test 'what's my next todo' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory

        result = PreClassifier.pre_classify("what's my next todo")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "next_todo_query"
        assert result.confidence == 1.0

    def test_next_todo_query_variants(self):
        """Test next todo query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory

        test_cases = [
            "what's my next todo",
            "next todo",
            "what should I do next",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "next_todo_query", f"Wrong action for: {query}"

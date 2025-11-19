"""Tests for TodoService."""

from uuid import UUID, uuid4

import pytest

from services.domain.models import Todo
from services.todo_service import TodoService


class TestTodoService:
    """Tests for TodoService."""

    @pytest.fixture
    def service(self):
        """Create service instance."""
        return TodoService()

    @pytest.fixture
    def list_id(self) -> UUID:
        """Test list ID."""
        return uuid4()

    async def test_create_todo(self, service, list_id):
        """Can create todo with priority."""
        todo = await service.create_todo(text="Test todo", list_id=list_id, priority="high")

        assert isinstance(todo, Todo)
        assert todo.text == "Test todo"
        assert todo.priority == "high"
        assert todo.completed is False

    async def test_complete_todo(self, service, list_id):
        """Can complete todo."""
        todo = await service.create_todo(text="Complete me", list_id=list_id)

        completed = await service.complete_todo(UUID(todo.id))

        assert completed.completed is True
        assert completed.status == "completed"
        assert completed.completed_at is not None

    async def test_reopen_todo(self, service, list_id):
        """Can reopen completed todo."""
        # Create and complete
        todo = await service.create_todo(text="Task", list_id=list_id)
        await service.complete_todo(UUID(todo.id))

        # Reopen
        reopened = await service.reopen_todo(UUID(todo.id))

        assert reopened.completed is False
        assert reopened.status == "pending"
        assert reopened.completed_at is None

    async def test_set_priority(self, service, list_id):
        """Can change todo priority."""
        todo = await service.create_todo(text="Task", list_id=list_id, priority="low")

        updated = await service.set_priority(UUID(todo.id), "urgent")

        assert updated.priority == "urgent"

    async def test_inherited_operations(self, service, list_id):
        """TodoService inherits generic operations."""
        # Create todo using inherited method
        todo = await service.create_item(
            text="Via parent",
            list_id=list_id,
            item_class=Todo,
            priority="medium",
            owner_id="test_user",
            completed=False,
        )

        assert isinstance(todo, Todo)
        assert todo.text == "Via parent"

        # Update using inherited method
        updated = await service.update_item_text(UUID(todo.id), "Updated")
        assert updated.text == "Updated"

    async def test_get_todos_in_list(self, service, list_id):
        """Can get all todos in a list."""
        # Create multiple todos
        await service.create_todo(text="Todo 1", list_id=list_id)
        await service.create_todo(text="Todo 2", list_id=list_id)
        await service.create_todo(text="Todo 3", list_id=list_id)

        # Retrieve all
        todos = await service.get_todos_in_list(list_id)

        assert len(todos) == 3
        assert all(isinstance(t, Todo) for t in todos)
        assert todos[0].text == "Todo 1"
        assert todos[1].text == "Todo 2"
        assert todos[2].text == "Todo 3"

    async def test_todo_defaults(self, service, list_id):
        """Todos have correct default values."""
        todo = await service.create_todo(text="Default test", list_id=list_id)

        assert todo.priority == "medium"
        assert todo.status == "pending"
        assert todo.completed is False
        assert todo.due_date is None
        assert todo.owner_id == "system"  # Default owner

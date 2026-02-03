"""Tests for TodoService."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory
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

    @pytest_asyncio.fixture
    async def test_user_id(self) -> str:
        """Create a test user in database for FK constraint satisfaction."""
        user_id = str(uuid4())
        async with AsyncSessionFactory.session_scope() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                                       created_at, updated_at, role, is_alpha)
                    VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', true)
                    ON CONFLICT (id) DO NOTHING
                """
                ),
                {
                    "id": user_id,
                    "username": f"test_user_{user_id[:8]}",
                    "email": f"test_{user_id[:8]}@example.com",
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                },
            )
            await session.commit()
        return user_id

    @pytest.mark.smoke
    async def test_create_todo(self, service, list_id, test_user_id):
        """Can create todo with priority."""
        todo = await service.create_todo(
            text="Test todo", list_id=list_id, priority="high", owner_id=test_user_id
        )

        assert isinstance(todo, Todo)
        assert todo.text == "Test todo"
        assert todo.priority == "high"
        assert todo.completed is False

    @pytest.mark.smoke
    async def test_complete_todo(self, service, list_id, test_user_id):
        """Can complete todo."""
        todo = await service.create_todo(text="Complete me", list_id=list_id, owner_id=test_user_id)

        completed = await service.complete_todo(UUID(todo.id))

        assert completed.completed is True
        assert completed.status == "completed"
        assert completed.completed_at is not None

    @pytest.mark.smoke
    async def test_reopen_todo(self, service, list_id, test_user_id):
        """Can reopen completed todo."""
        # Create and complete
        todo = await service.create_todo(text="Task", list_id=list_id, owner_id=test_user_id)
        await service.complete_todo(UUID(todo.id))

        # Reopen
        reopened = await service.reopen_todo(UUID(todo.id))

        assert reopened.completed is False
        assert reopened.status == "pending"
        assert reopened.completed_at is None

    @pytest.mark.smoke
    async def test_set_priority(self, service, list_id, test_user_id):
        """Can change todo priority."""
        todo = await service.create_todo(
            text="Task", list_id=list_id, priority="low", owner_id=test_user_id
        )

        updated = await service.set_priority(UUID(todo.id), "urgent")

        assert updated.priority == "urgent"

    @pytest.mark.smoke
    async def test_inherited_operations(self, service, list_id, test_user_id):
        """TodoService inherits generic operations."""
        # Create todo using inherited method
        todo = await service.create_item(
            text="Via parent",
            list_id=list_id,
            item_class=Todo,
            priority="medium",
            owner_id=test_user_id,
            completed=False,
        )

        assert isinstance(todo, Todo)
        assert todo.text == "Via parent"

        # Update using inherited method
        updated = await service.update_item_text(UUID(todo.id), "Updated")
        assert updated.text == "Updated"

    @pytest.mark.smoke
    async def test_get_todos_in_list(self, service, list_id, test_user_id):
        """Can get all todos in a list."""
        # Create multiple todos
        await service.create_todo(text="Todo 1", list_id=list_id, owner_id=test_user_id)
        await service.create_todo(text="Todo 2", list_id=list_id, owner_id=test_user_id)
        await service.create_todo(text="Todo 3", list_id=list_id, owner_id=test_user_id)

        # Retrieve all
        todos = await service.get_todos_in_list(list_id)

        assert len(todos) == 3
        assert all(isinstance(t, Todo) for t in todos)
        assert todos[0].text == "Todo 1"
        assert todos[1].text == "Todo 2"
        assert todos[2].text == "Todo 3"

    @pytest.mark.smoke
    async def test_todo_defaults(self, service, list_id, test_user_id):
        """Todos have correct default values."""
        todo = await service.create_todo(
            text="Default test", list_id=list_id, owner_id=test_user_id
        )

        assert todo.priority == "medium"
        assert todo.status == "pending"
        assert todo.completed is False
        assert todo.due_date is None
        # owner_id should match the provided test user
        assert todo.owner_id == test_user_id

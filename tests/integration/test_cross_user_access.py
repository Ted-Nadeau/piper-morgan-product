"""
Cross-user access prevention tests for SEC-RBAC Phase 3.

Tests verify that User A cannot access User B's resources,
and that admin users CAN bypass ownership checks.

Issue: #357 (SEC-RBAC: Implement RBAC)
ADR: ADR-044 (Lightweight RBAC)
Phase: 3 - System-wide admin role testing
"""

from uuid import uuid4

import pytest

from services.repositories.file_repository import FileRepository
from services.repositories.todo_repository import TodoRepository
from services.repositories.universal_list_repository import UniversalListRepository


@pytest.mark.asyncio
class TestCrossUserListAccess:
    """Test that users cannot access other users' lists"""

    async def test_user_a_cannot_read_user_b_list(self, async_transaction):
        """User A cannot read User B's list"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list as User B
        list_b = await list_repo.create_list(
            name="User B's Private List", owner_id=user_b_id, item_type="todo"
        )

        # Try to read as User A (should return None with ownership check)
        result = await list_repo.get_list_by_id(list_b.id, owner_id=user_a_id, is_admin=False)

        assert result is None, "User A should NOT be able to read User B's list"

    async def test_user_a_cannot_update_user_b_list(self, async_transaction):
        """User A cannot update User B's list"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list as User B
        list_b = await list_repo.create_list(
            name="User B's List", owner_id=user_b_id, item_type="todo"
        )

        # Try to update as User A (should return None)
        result = await list_repo.update_list(
            list_b.id, updates={"name": "Hacked by User A"}, owner_id=user_a_id, is_admin=False
        )

        assert result is None, "User A should NOT be able to update User B's list"

    async def test_user_a_cannot_delete_user_b_list(self, async_transaction):
        """User A cannot delete User B's list"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list as User B
        list_b = await list_repo.create_list(
            name="User B's List", owner_id=user_b_id, item_type="todo"
        )

        # Try to delete as User A (should return False)
        result = await list_repo.delete_list(list_b.id, owner_id=user_a_id, is_admin=False)

        assert result is False, "User A should NOT be able to delete User B's list"

    async def test_owner_can_read_own_list(self, async_transaction):
        """Owner CAN read their own list"""
        user_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list as owner
        my_list = await list_repo.create_list(name="My List", owner_id=user_id, item_type="todo")

        # Read as owner (should succeed)
        result = await list_repo.get_list_by_id(my_list.id, owner_id=user_id, is_admin=False)

        assert result is not None, "Owner should be able to read their own list"
        assert result.id == my_list.id
        assert result.owner_id == user_id

    async def test_owner_can_update_own_list(self, async_transaction):
        """Owner CAN update their own list"""
        user_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list
        my_list = await list_repo.create_list(name="My List", owner_id=user_id, item_type="todo")

        # Update as owner (should succeed)
        result = await list_repo.update_list(
            my_list.id, updates={"name": "Updated by owner"}, owner_id=user_id, is_admin=False
        )

        assert result is not None, "Owner should be able to update their own list"
        assert result.name == "Updated by owner"

    async def test_owner_can_delete_own_list(self, async_transaction):
        """Owner CAN delete their own list"""
        user_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list
        my_list = await list_repo.create_list(name="My List", owner_id=user_id, item_type="todo")

        # Delete as owner (should succeed)
        result = await list_repo.delete_list(my_list.id, owner_id=user_id, is_admin=False)

        assert result is True, "Owner should be able to delete their own list"

    async def test_admin_can_read_any_list(self, async_transaction):
        """Admin CAN read any user's list"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list as User B
        list_b = await list_repo.create_list(
            name="User B's List", owner_id=user_b_id, item_type="todo"
        )

        # Read as admin (should succeed with admin bypass)
        result = await list_repo.get_list_by_id(
            list_b.id, owner_id=admin_id, is_admin=True  # Admin bypass
        )

        assert result is not None, "Admin should be able to read any user's list"
        assert result.id == list_b.id
        assert result.owner_id == user_b_id

    async def test_admin_can_update_any_list(self, async_transaction):
        """Admin CAN update any user's list"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list as User B
        list_b = await list_repo.create_list(
            name="User B's List", owner_id=user_b_id, item_type="todo"
        )

        # Update as admin (should succeed)
        result = await list_repo.update_list(
            list_b.id,
            updates={"name": "Updated by admin"},
            owner_id=admin_id,
            is_admin=True,  # Admin bypass
        )

        assert result is not None, "Admin should be able to update any list"
        assert result.name == "Updated by admin"

    async def test_admin_can_delete_any_list(self, async_transaction):
        """Admin CAN delete any user's list"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        list_repo = UniversalListRepository(async_transaction)

        # Create list as User B
        list_b = await list_repo.create_list(
            name="User B's List", owner_id=user_b_id, item_type="todo"
        )

        # Delete as admin (should succeed)
        result = await list_repo.delete_list(
            list_b.id, owner_id=admin_id, is_admin=True  # Admin bypass
        )

        assert result is True, "Admin should be able to delete any list"


@pytest.mark.asyncio
class TestCrossUserTodoAccess:
    """Test that users cannot access other users' todos"""

    async def test_user_a_cannot_read_user_b_todo(self, async_transaction):
        """User A cannot read User B's todo"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo as User B
        todo_b = await todo_repo.create_todo(title="User B's Private Todo", owner_id=user_b_id)

        # Try to read as User A (should return None)
        result = await todo_repo.get_todo_by_id(todo_b.id, owner_id=user_a_id, is_admin=False)

        assert result is None, "User A should NOT be able to read User B's todo"

    async def test_user_a_cannot_update_user_b_todo(self, async_transaction):
        """User A cannot update User B's todo"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo as User B
        todo_b = await todo_repo.create_todo(title="User B's Todo", owner_id=user_b_id)

        # Try to update as User A (should return None)
        result = await todo_repo.update_todo(
            todo_b.id, updates={"title": "Hacked by User A"}, owner_id=user_a_id, is_admin=False
        )

        assert result is None, "User A should NOT be able to update User B's todo"

    async def test_user_a_cannot_delete_user_b_todo(self, async_transaction):
        """User A cannot delete User B's todo"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo as User B
        todo_b = await todo_repo.create_todo(title="User B's Todo", owner_id=user_b_id)

        # Try to delete as User A (should return False)
        result = await todo_repo.delete_todo(todo_b.id, owner_id=user_a_id, is_admin=False)

        assert result is False, "User A should NOT be able to delete User B's todo"

    async def test_owner_can_read_own_todo(self, async_transaction):
        """Owner CAN read their own todo"""
        user_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo
        my_todo = await todo_repo.create_todo(title="My Todo", owner_id=user_id)

        # Read as owner (should succeed)
        result = await todo_repo.get_todo_by_id(my_todo.id, owner_id=user_id, is_admin=False)

        assert result is not None, "Owner should be able to read their own todo"
        assert result.id == my_todo.id
        assert result.owner_id == user_id

    async def test_owner_can_update_own_todo(self, async_transaction):
        """Owner CAN update their own todo"""
        user_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo
        my_todo = await todo_repo.create_todo(title="My Todo", owner_id=user_id)

        # Update as owner (should succeed)
        result = await todo_repo.update_todo(
            my_todo.id, updates={"title": "Updated by owner"}, owner_id=user_id, is_admin=False
        )

        assert result is not None, "Owner should be able to update their own todo"
        assert result.title == "Updated by owner"

    async def test_owner_can_delete_own_todo(self, async_transaction):
        """Owner CAN delete their own todo"""
        user_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo
        my_todo = await todo_repo.create_todo(title="My Todo", owner_id=user_id)

        # Delete as owner (should succeed)
        result = await todo_repo.delete_todo(my_todo.id, owner_id=user_id, is_admin=False)

        assert result is True, "Owner should be able to delete their own todo"

    async def test_admin_can_read_any_todo(self, async_transaction):
        """Admin CAN read any user's todo"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo as User B
        todo_b = await todo_repo.create_todo(title="User B's Todo", owner_id=user_b_id)

        # Read as admin (should succeed)
        result = await todo_repo.get_todo_by_id(
            todo_b.id, owner_id=admin_id, is_admin=True  # Admin bypass
        )

        assert result is not None, "Admin should be able to read any user's todo"
        assert result.id == todo_b.id
        assert result.owner_id == user_b_id

    async def test_admin_can_update_any_todo(self, async_transaction):
        """Admin CAN update any user's todo"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo as User B
        todo_b = await todo_repo.create_todo(title="User B's Todo", owner_id=user_b_id)

        # Update as admin (should succeed)
        result = await todo_repo.update_todo(
            todo_b.id,
            updates={"title": "Updated by admin"},
            owner_id=admin_id,
            is_admin=True,  # Admin bypass
        )

        assert result is not None, "Admin should be able to update any todo"
        assert result.title == "Updated by admin"

    async def test_admin_can_delete_any_todo(self, async_transaction):
        """Admin CAN delete any user's todo"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        todo_repo = TodoRepository(async_transaction)

        # Create todo as User B
        todo_b = await todo_repo.create_todo(title="User B's Todo", owner_id=user_b_id)

        # Delete as admin (should succeed)
        result = await todo_repo.delete_todo(
            todo_b.id, owner_id=admin_id, is_admin=True  # Admin bypass
        )

        assert result is True, "Admin should be able to delete any todo"


@pytest.mark.asyncio
class TestCrossUserFileAccess:
    """Test that users cannot access other users' files"""

    async def test_user_a_cannot_read_user_b_file(self, async_transaction):
        """User A cannot read User B's file"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        file_repo = FileRepository(async_transaction)

        # Create file as User B
        file_b = await file_repo.create_file(
            filename="user_b_secret.pdf",
            file_path="/tmp/user_b_secret.pdf",
            owner_id=user_b_id,
            file_size=1024,
            mime_type="application/pdf",
        )

        # Try to read as User A (should return None)
        result = await file_repo.get_file_by_id(file_b.id, owner_id=user_a_id, is_admin=False)

        assert result is None, "User A should NOT be able to read User B's file"

    async def test_user_a_cannot_delete_user_b_file(self, async_transaction):
        """User A cannot delete User B's file"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        file_repo = FileRepository(async_transaction)

        # Create file as User B
        file_b = await file_repo.create_file(
            filename="user_b_file.pdf",
            file_path="/tmp/user_b_file.pdf",
            owner_id=user_b_id,
            file_size=1024,
            mime_type="application/pdf",
        )

        # Try to delete as User A (should return False)
        result = await file_repo.delete_file(file_b.id, owner_id=user_a_id, is_admin=False)

        assert result is False, "User A should NOT be able to delete User B's file"

    async def test_owner_can_read_own_file(self, async_transaction):
        """Owner CAN read their own file"""
        user_id = str(uuid4())

        file_repo = FileRepository(async_transaction)

        # Create file
        my_file = await file_repo.create_file(
            filename="my_file.pdf",
            file_path="/tmp/my_file.pdf",
            owner_id=user_id,
            file_size=2048,
            mime_type="application/pdf",
        )

        # Read as owner (should succeed)
        result = await file_repo.get_file_by_id(my_file.id, owner_id=user_id, is_admin=False)

        assert result is not None, "Owner should be able to read their own file"
        assert result.id == my_file.id
        assert result.owner_id == user_id

    async def test_owner_can_delete_own_file(self, async_transaction):
        """Owner CAN delete their own file"""
        user_id = str(uuid4())

        file_repo = FileRepository(async_transaction)

        # Create file
        my_file = await file_repo.create_file(
            filename="my_file.pdf",
            file_path="/tmp/my_file.pdf",
            owner_id=user_id,
            file_size=2048,
            mime_type="application/pdf",
        )

        # Delete as owner (should succeed)
        result = await file_repo.delete_file(my_file.id, owner_id=user_id, is_admin=False)

        assert result is True, "Owner should be able to delete their own file"

    async def test_admin_can_read_any_file(self, async_transaction):
        """Admin CAN read any user's file"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        file_repo = FileRepository(async_transaction)

        # Create file as User B
        file_b = await file_repo.create_file(
            filename="user_b_file.pdf",
            file_path="/tmp/user_b_file.pdf",
            owner_id=user_b_id,
            file_size=1024,
            mime_type="application/pdf",
        )

        # Read as admin (should succeed)
        result = await file_repo.get_file_by_id(
            file_b.id, owner_id=admin_id, is_admin=True  # Admin bypass
        )

        assert result is not None, "Admin should be able to read any user's file"
        assert result.id == file_b.id
        assert result.owner_id == user_b_id

    async def test_admin_can_delete_any_file(self, async_transaction):
        """Admin CAN delete any user's file"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        file_repo = FileRepository(async_transaction)

        # Create file as User B
        file_b = await file_repo.create_file(
            filename="user_b_file.pdf",
            file_path="/tmp/user_b_file.pdf",
            owner_id=user_b_id,
            file_size=1024,
            mime_type="application/pdf",
        )

        # Delete as admin (should succeed)
        result = await file_repo.delete_file(
            file_b.id, owner_id=admin_id, is_admin=True  # Admin bypass
        )

        assert result is True, "Admin should be able to delete any file"

"""
Todo Service

Extends ItemService with todo-specific operations.

Inherits:
- create_item (with Todo-specific fields)
- update_item_text
- reorder_items
- delete_item
- get_items_in_list

Adds:
- complete_todo
- reopen_todo
- set_priority
- set_due_date
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import select

from services.database.models import TodoDB
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Todo
from services.item_service import ItemService


class TodoService(ItemService):
    """Todo-specific service extending ItemService.

    Inherits generic item operations, adds todo-specific ones.

    Examples:
        >>> service = TodoService()

        >>> # Generic operation (inherited)
        >>> todo = await service.create_todo(
        ...     text="Review PR",
        ...     list_id=list_id,
        ...     priority="high"
        ... )

        >>> # Todo-specific operation
        >>> await service.complete_todo(todo.id)
    """

    async def create_todo(
        self,
        text: str,
        list_id: UUID,
        priority: str = "medium",
        status: str = "pending",
        due_date: Optional[datetime] = None,
        owner_id: Optional[str] = None,
        **kwargs,
    ) -> Todo:
        """Create a todo.

        Uses inherited create_item with todo-specific parameters.

        Args:
            text: Todo text
            list_id: List containing this todo
            priority: Priority level (low, medium, high, urgent)
            status: Status (pending, in_progress, completed)
            due_date: Optional due date
            owner_id: Owner of the todo (required by TodoDB)
            **kwargs: Additional todo fields

        Returns:
            Created todo
        """
        # Set defaults for required fields if not provided
        if owner_id is None:
            owner_id = str(uuid4())  # Default owner (valid UUID)

        return await self.create_item(
            text=text,
            list_id=list_id,
            item_class=Todo,
            priority=priority,
            status=status,
            due_date=due_date,
            owner_id=owner_id,
            completed=False,  # New todos are not completed
            **kwargs,
        )

    async def complete_todo(self, todo_id: UUID) -> Optional[Todo]:
        """Mark todo as complete.

        Todo-specific operation.

        Args:
            todo_id: ID of todo to complete

        Returns:
            Completed todo
        """
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(select(TodoDB).where(TodoDB.id == str(todo_id)))
            todo_db = result.scalar_one_or_none()

            if not todo_db:
                return None

            todo_db.completed = True
            todo_db.completed_at = datetime.now(timezone.utc)
            todo_db.status = "completed"

            await session.commit()
            await session.refresh(todo_db)

            return todo_db.to_domain()

    async def reopen_todo(self, todo_id: UUID) -> Optional[Todo]:
        """Reopen completed todo.

        Todo-specific operation.

        Args:
            todo_id: ID of todo to reopen

        Returns:
            Reopened todo
        """
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(select(TodoDB).where(TodoDB.id == str(todo_id)))
            todo_db = result.scalar_one_or_none()

            if not todo_db:
                return None

            todo_db.completed = False
            todo_db.completed_at = None
            todo_db.status = "pending"

            await session.commit()
            await session.refresh(todo_db)

            return todo_db.to_domain()

    async def set_priority(self, todo_id: UUID, priority: str) -> Optional[Todo]:
        """Set todo priority.

        Todo-specific operation.

        Args:
            todo_id: ID of todo
            priority: New priority (low, medium, high, urgent)

        Returns:
            Updated todo
        """
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(select(TodoDB).where(TodoDB.id == str(todo_id)))
            todo_db = result.scalar_one_or_none()

            if not todo_db:
                return None

            todo_db.priority = priority

            await session.commit()
            await session.refresh(todo_db)

            return todo_db.to_domain()

    async def get_todos_in_list(self, list_id: UUID) -> List[Todo]:
        """Get all todos in a list.

        Override base method to query TodoDB directly, ensuring joined table data is loaded.

        Args:
            list_id: List ID

        Returns:
            List of todos
        """
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        from services.database.models import TodoDB
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            # Query TodoDB directly (not ItemDB) to ensure todo-specific fields are loaded
            query = select(TodoDB).where(TodoDB.list_id == str(list_id)).order_by(TodoDB.position)

            result = await session.execute(query)
            todos_db = result.scalars().all()

            return [todo_db.to_domain() for todo_db in todos_db]

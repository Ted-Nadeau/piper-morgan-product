"""
Universal List Repository implementation for PM-081
Chief Architect's universal composition over specialization principle
"""

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import services.domain.models as domain
from services.database.models import ListDB, ListItemDB, TodoDB
from services.database.repositories import BaseRepository

logger = structlog.get_logger()


class UniversalListRepository(BaseRepository):
    """Repository for Universal List operations supporting ANY item type"""

    model = ListDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_list(self, list_obj: domain.List) -> domain.List:
        """Create a new universal list"""
        db_list = ListDB.from_domain(list_obj)
        self.session.add(db_list)
        await self.session.flush()
        await self.session.refresh(db_list)
        return db_list.to_domain()

    async def get_list_by_id(
        self, list_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.List]:
        """Get universal list by ID - optionally verify ownership"""
        filters = [ListDB.id == list_id]
        if owner_id:
            filters.append(ListDB.owner_id == owner_id)

        result = await self.session.execute(select(ListDB).where(and_(*filters)))
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def get_lists_by_owner(
        self,
        owner_id: str,
        item_type: Optional[str] = None,
        include_archived: bool = False,
        list_type: Optional[str] = None,
    ) -> List[domain.List]:
        """Get lists for an owner with optional filtering"""
        query = select(ListDB).where(ListDB.owner_id == owner_id)

        if item_type:
            query = query.where(ListDB.item_type == item_type)

        if not include_archived:
            query = query.where(ListDB.is_archived == False)

        if list_type:
            query = query.where(ListDB.list_type == list_type)

        query = query.order_by(ListDB.is_default.desc(), ListDB.name)

        result = await self.session.execute(query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def get_default_list(self, owner_id: str, item_type: str) -> Optional[domain.List]:
        """Get user's default list for a specific item type"""
        result = await self.session.execute(
            select(ListDB).where(
                and_(
                    ListDB.owner_id == owner_id,
                    ListDB.item_type == item_type,
                    ListDB.is_default == True,
                    ListDB.is_archived == False,
                )
            )
        )
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def get_shared_lists(
        self, user_id: UUID, item_type: Optional[str] = None
    ) -> List[domain.List]:
        """Get lists shared with a user"""
        query = select(ListDB).where(
            and_(ListDB.shared_with.contains([user_id]), ListDB.is_archived == False)
        )

        if item_type:
            query = query.where(ListDB.item_type == item_type)

        query = query.order_by(ListDB.name)

        result = await self.session.execute(query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def update_list(
        self, list_id: str, updates: Dict, owner_id: Optional[str] = None
    ) -> Optional[domain.List]:
        """Update universal list - optionally verify ownership"""
        updates["updated_at"] = datetime.now()

        filters = [ListDB.id == list_id]
        if owner_id:
            filters.append(ListDB.owner_id == owner_id)

        result = await self.session.execute(
            update(ListDB).where(and_(*filters)).values(**updates).returning(ListDB)
        )
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def update_item_counts(self, list_id: str, owner_id: Optional[str] = None) -> None:
        """Update cached item counts - optionally verify ownership"""
        # Get total count through list items
        total_result = await self.session.execute(
            select(func.count(ListItemDB.id)).where(ListItemDB.list_id == list_id)
        )
        total_count = total_result.scalar() or 0

        # Get completed count (for todos only - other item types may have different logic)
        list_obj = await self.get_list_by_id(list_id, owner_id)
        completed_count = 0

        if list_obj and list_obj.item_type == "todo":
            completed_result = await self.session.execute(
                select(func.count(ListItemDB.id))
                .select_from(ListItemDB)
                .join(TodoDB, ListItemDB.item_id == TodoDB.id)
                .where(and_(ListItemDB.list_id == list_id, TodoDB.status == "completed"))
            )
            completed_count = completed_result.scalar() or 0

        # Update the list with new counts (with ownership verification if provided)
        filters = [ListDB.id == list_id]
        if owner_id:
            filters.append(ListDB.owner_id == owner_id)

        await self.session.execute(
            update(ListDB)
            .where(and_(*filters))
            .values(
                item_count=total_count, completed_count=completed_count, updated_at=datetime.now()
            )
        )

    async def delete_list(self, list_id: str, owner_id: Optional[str] = None) -> bool:
        """Delete a list - optionally verify ownership (cascades to items)"""
        filters = [ListDB.id == list_id]
        if owner_id:
            filters.append(ListDB.owner_id == owner_id)

        result = await self.session.execute(select(ListDB).where(and_(*filters)))
        db_list = result.scalar_one_or_none()

        if db_list:
            await self.session.delete(db_list)
            return True
        return False

    async def search_lists_by_name(
        self, owner_id: str, query: str, item_type: Optional[str] = None
    ) -> List[domain.List]:
        """Search lists by name (case-insensitive)"""
        search_query = select(ListDB).where(
            and_(
                ListDB.owner_id == owner_id,
                ListDB.name.ilike(f"%{query}%"),
                ListDB.is_archived == False,
            )
        )

        if item_type:
            search_query = search_query.where(ListDB.item_type == item_type)

        search_query = search_query.order_by(ListDB.name)

        result = await self.session.execute(search_query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]


class UniversalListItemRepository(BaseRepository):
    """Repository for Universal ListItem operations managing polymorphic relationships"""

    model = ListItemDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_item(self, item: domain.ListItem) -> domain.ListItem:
        """Create a list item relationship"""
        db_item = ListItemDB.from_domain(item)
        self.session.add(db_item)
        await self.session.flush()
        await self.session.refresh(db_item)
        return db_item.to_domain()

    async def get_item_by_id(self, item_id: str) -> Optional[domain.ListItem]:
        """Get list item by ID"""
        result = await self.session.execute(select(ListItemDB).where(ListItemDB.id == item_id))
        db_item = result.scalar_one_or_none()
        return db_item.to_domain() if db_item else None

    async def get_list_item(self, list_id: str, item_id: str) -> Optional[domain.ListItem]:
        """Get specific list-item relationship"""
        result = await self.session.execute(
            select(ListItemDB).where(
                and_(ListItemDB.list_id == list_id, ListItemDB.item_id == item_id)
            )
        )
        db_item = result.scalar_one_or_none()
        return db_item.to_domain() if db_item else None

    async def get_items_in_list(
        self, list_id: str, item_type: Optional[str] = None
    ) -> List[domain.ListItem]:
        """Get all items in a list with optional type filtering"""
        query = select(ListItemDB).where(ListItemDB.list_id == list_id)

        if item_type:
            query = query.where(ListItemDB.item_type == item_type)

        query = query.order_by(ListItemDB.position.asc())

        result = await self.session.execute(query)
        db_items = result.scalars().all()
        return [db_item.to_domain() for db_item in db_items]

    async def get_lists_for_item(self, item_id: str, item_type: str) -> List[domain.List]:
        """Get all lists containing a specific item"""
        result = await self.session.execute(
            select(ListDB)
            .join(ListItemDB, ListDB.id == ListItemDB.list_id)
            .where(and_(ListItemDB.item_id == item_id, ListItemDB.item_type == item_type))
            .order_by(ListDB.name)
        )
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def add_item_to_list(
        self,
        list_id: str,
        item_id: str,
        item_type: str,
        added_by: str,
        position: Optional[int] = None,
    ) -> domain.ListItem:
        """Add an item to a list with automatic position assignment"""

        # If no position specified, add at end
        if position is None:
            max_position_result = await self.session.execute(
                select(func.max(ListItemDB.position)).where(ListItemDB.list_id == list_id)
            )
            max_position = max_position_result.scalar() or 0
            position = max_position + 1

        item = domain.ListItem(
            list_id=list_id,
            item_id=item_id,
            item_type=item_type,
            position=position,
            added_by=added_by,
            added_at=datetime.now(),
        )

        return await self.create_item(item)

    async def remove_item_from_list(self, list_id: str, item_id: str) -> bool:
        """Remove an item from a list"""
        result = await self.session.execute(
            select(ListItemDB).where(
                and_(ListItemDB.list_id == list_id, ListItemDB.item_id == item_id)
            )
        )
        db_item = result.scalar_one_or_none()

        if db_item:
            await self.session.delete(db_item)
            return True
        return False

    async def reorder_items_in_list(
        self, list_id: str, item_positions: List[tuple[str, int]]
    ) -> bool:
        """Reorder items in a list by updating positions"""
        try:
            for item_id, new_position in item_positions:
                await self.session.execute(
                    update(ListItemDB)
                    .where(and_(ListItemDB.list_id == list_id, ListItemDB.item_id == item_id))
                    .values(position=new_position)
                )
            return True
        except Exception as e:
            logger.error("Failed to reorder items", list_id=list_id, error=str(e))
            return False

    async def get_item_count(self, list_id: str, item_type: Optional[str] = None) -> int:
        """Get count of items in a list"""
        query = select(func.count(ListItemDB.id)).where(ListItemDB.list_id == list_id)

        if item_type:
            query = query.where(ListItemDB.item_type == item_type)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def delete_items_for_list(self, list_id: str) -> int:
        """Delete all items for a list (used when deleting list)"""
        result = await self.session.execute(select(ListItemDB).where(ListItemDB.list_id == list_id))
        items = result.scalars().all()

        count = len(items)
        for item in items:
            await self.session.delete(item)

        return count

    async def delete_items_by_item_id(self, item_id: str, item_type: str) -> int:
        """Delete all list memberships for an item (used when deleting the item)"""
        result = await self.session.execute(
            select(ListItemDB).where(
                and_(ListItemDB.item_id == item_id, ListItemDB.item_type == item_type)
            )
        )
        items = result.scalars().all()

        count = len(items)
        for item in items:
            await self.session.delete(item)

        return count


# Backward compatibility wrappers
class TodoListRepository:
    """Backward compatibility wrapper for TodoList operations"""

    def __init__(self, session: AsyncSession):
        self.universal_repo = UniversalListRepository(session)

    async def create_list(self, todo_list: domain.TodoList) -> domain.TodoList:
        """Create a todo list using universal pattern"""
        # Convert TodoList to universal List
        universal_list = domain.List(
            id=todo_list.id,
            name=todo_list.name,
            description=todo_list.description,
            item_type="todo",
            list_type=(
                todo_list.list_type.value
                if hasattr(todo_list.list_type, "value")
                else todo_list.list_type
            ),
            ordering_strategy=(
                todo_list.ordering_strategy.value
                if hasattr(todo_list.ordering_strategy, "value")
                else todo_list.ordering_strategy
            ),
            color=todo_list.color,
            emoji=todo_list.emoji,
            is_archived=todo_list.is_archived,
            is_default=todo_list.is_default,
            metadata=todo_list.metadata,
            tags=todo_list.tags,
            created_at=todo_list.created_at,
            updated_at=todo_list.updated_at,
            owner_id=todo_list.owner_id,
            shared_with=todo_list.shared_with,
        )

        result = await self.universal_repo.create_list(universal_list)

        # Convert back to TodoList for compatibility
        return domain.TodoList(**result.to_dict())

    async def get_list_by_id(self, list_id: str) -> Optional[domain.TodoList]:
        """Get todo list by ID"""
        result = await self.universal_repo.get_list_by_id(list_id)
        if result and result.item_type == "todo":
            return domain.TodoList(**result.to_dict())
        return None

    async def get_lists_by_owner(
        self, owner_id: str, include_archived: bool = False, list_type: Optional[str] = None
    ) -> List[domain.TodoList]:
        """Get todo lists for a user"""
        results = await self.universal_repo.get_lists_by_owner(
            owner_id=owner_id,
            item_type="todo",
            include_archived=include_archived,
            list_type=list_type,
        )
        return [domain.TodoList(**r.to_dict()) for r in results]

    async def get_default_list(self, owner_id: str) -> Optional[domain.TodoList]:
        """Get user's default todo list"""
        result = await self.universal_repo.get_default_list(owner_id, "todo")
        if result:
            return domain.TodoList(**result.to_dict())
        return None

    async def update_todo_counts(self, list_id: str) -> None:
        """Update cached todo counts for a list"""
        await self.universal_repo.update_item_counts(list_id)


class ListMembershipRepository:
    """Backward compatibility wrapper for ListMembership operations"""

    def __init__(self, session: AsyncSession):
        self.universal_repo = UniversalListItemRepository(session)

    async def create_membership(self, membership: domain.ListMembership) -> domain.ListMembership:
        """Create a list membership using universal pattern"""
        # Convert ListMembership to universal ListItem
        universal_item = domain.ListItem(
            id=membership.id,
            list_id=membership.list_id,
            item_id=membership.todo_id,
            item_type="todo",
            position=membership.position,
            added_at=membership.added_at,
            added_by=membership.added_by,
            list_priority=(
                membership.list_priority.value
                if hasattr(membership.list_priority, "value")
                else membership.list_priority
            ),
            list_due_date=membership.list_due_date,
            list_notes=membership.list_notes,
        )

        result = await self.universal_repo.create_item(universal_item)

        # Convert back to ListMembership for compatibility
        return domain.ListMembership(**{**result.to_dict(), "todo_id": result.item_id})

    async def add_todo_to_list(
        self, list_id: str, todo_id: str, added_by: str, position: Optional[int] = None
    ) -> domain.ListMembership:
        """Add a todo to a list"""
        result = await self.universal_repo.add_item_to_list(
            list_id=list_id, item_id=todo_id, item_type="todo", added_by=added_by, position=position
        )

        return domain.ListMembership(**{**result.to_dict(), "todo_id": result.item_id})

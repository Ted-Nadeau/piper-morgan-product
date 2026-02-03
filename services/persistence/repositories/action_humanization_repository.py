from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.domain.models import ActionHumanization
from services.persistence.models import ActionHumanizationDB


class ActionHumanizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_action(self, action: str) -> Optional[ActionHumanization]:
        """Get humanization by action string"""
        result = await self.session.execute(
            select(ActionHumanizationDB).where(ActionHumanizationDB.action == action)
        )
        db_obj = result.scalar_one_or_none()
        return db_obj.to_domain() if db_obj else None

    async def create(self, humanization: ActionHumanization) -> ActionHumanization:
        """Store new humanization"""
        db_obj = ActionHumanizationDB(
            id=humanization.id,
            action=humanization.action,
            category=humanization.category,
            human_readable=humanization.human_readable,
            created_at=humanization.created_at,
        )
        self.session.add(db_obj)
        await self.session.commit()
        return humanization

    async def increment_usage(self, action: str) -> None:
        """Track usage for analytics"""
        await self.session.execute(
            update(ActionHumanizationDB)
            .where(ActionHumanizationDB.action == action)
            .values(
                usage_count=ActionHumanizationDB.usage_count + 1,
                last_used=datetime.now(timezone.utc),
            )
        )
        await self.session.commit()

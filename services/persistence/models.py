from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String

from services.database.connection import Base
from services.domain.models import ActionHumanization


class ActionHumanizationDB(Base):
    __tablename__ = "action_humanizations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    action = Column(String(255), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=True)
    human_readable = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, nullable=True)

    def to_domain(self) -> ActionHumanization:
        return ActionHumanization(
            id=self.id,
            action=self.action,
            category=self.category,
            human_readable=self.human_readable,
            created_at=self.created_at,
            usage_count=self.usage_count,
            last_used=self.last_used,
        )

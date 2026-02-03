"""
Database models for personality enhancement
SQLAlchemy models for PersonalityProfile persistence
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PersonalityProfileModel(Base):
    """Database model for PersonalityProfile"""

    __tablename__ = "personality_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, unique=True, index=True)
    warmth_level = Column(Float, nullable=False, default=0.6)
    confidence_style = Column(String(50), nullable=False, default="contextual")
    action_orientation = Column(String(50), nullable=False, default="medium")
    technical_depth = Column(String(50), nullable=False, default="balanced")
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    def __repr__(self):
        return f"<PersonalityProfile(user_id='{self.user_id}', warmth={self.warmth_level})>"

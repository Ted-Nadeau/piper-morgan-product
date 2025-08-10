"""
Feedback Service for PM-005 feedback tracking implementation
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import FeedbackDB
from services.feedback.models import Feedback, FeedbackCreateRequest, FeedbackUpdateRequest


class FeedbackService:
    """Service for managing user feedback"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def capture_feedback(
        self,
        session_id: str,
        feedback_type: str,
        comment: str,
        rating: Optional[int] = None,
        context: Dict = None,
        user_id: Optional[str] = None,
        conversation_context: Dict = None,
        source: str = "api",
        tags: List[str] = None,
    ) -> str:
        """
        Capture user feedback and store in database

        Args:
            session_id: Session ID for context tracking
            feedback_type: Type of feedback (bug, feature, ux, general)
            comment: User feedback comment
            rating: Optional 1-5 rating
            context: Additional context data
            user_id: Optional user ID
            conversation_context: Optional conversation context
            source: Source of feedback (api, ui, conversation)
            tags: Optional tags

        Returns:
            Feedback ID
        """

        # Create feedback domain model
        feedback = Feedback(
            id=str(uuid4()),
            session_id=session_id,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment,
            context=context or {},
            user_id=user_id,
            conversation_context=conversation_context or {},
            source=source,
            tags=tags or [],
        )

        # Convert to database model
        feedback_db = FeedbackDB.from_domain(feedback)

        # Store in database
        self.db.add(feedback_db)
        await self.db.commit()
        await self.db.refresh(feedback_db)

        return feedback.id

    async def get_feedback(self, feedback_id: str) -> Optional[Feedback]:
        """Get feedback by ID"""

        stmt = select(FeedbackDB).where(FeedbackDB.id == feedback_id)
        result = await self.db.execute(stmt)
        feedback_db = result.scalar_one_or_none()

        if feedback_db:
            return feedback_db.to_domain()
        return None

    async def list_feedback(
        self,
        session_id: Optional[str] = None,
        feedback_type: Optional[str] = None,
        status: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Feedback]:
        """List feedback with optional filtering"""

        stmt = select(FeedbackDB)
        conditions = []

        if session_id:
            conditions.append(FeedbackDB.session_id == session_id)
        if feedback_type:
            conditions.append(FeedbackDB.feedback_type == feedback_type)
        if status:
            conditions.append(FeedbackDB.status == status)
        if user_id:
            conditions.append(FeedbackDB.user_id == user_id)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(FeedbackDB.created_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(stmt)

        feedback_list = result.scalars().all()
        return [feedback_db.to_domain() for feedback_db in feedback_list]

    async def update_feedback(
        self,
        feedback_id: str,
        update_data: FeedbackUpdateRequest,
    ) -> Optional[Feedback]:
        """Update feedback status and metadata"""

        stmt = select(FeedbackDB).where(FeedbackDB.id == feedback_id)
        result = await self.db.execute(stmt)
        feedback_db = result.scalar_one_or_none()

        if not feedback_db:
            return None

        # Update fields
        if update_data.status is not None:
            feedback_db.status = update_data.status
        if update_data.priority is not None:
            feedback_db.priority = update_data.priority
        if update_data.sentiment_score is not None:
            feedback_db.sentiment_score = update_data.sentiment_score
        if update_data.categories is not None:
            feedback_db.categories = update_data.categories
        if update_data.tags is not None:
            feedback_db.tags = update_data.tags

        feedback_db.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(feedback_db)

        return feedback_db.to_domain()

    async def delete_feedback(self, feedback_id: str) -> bool:
        """Delete feedback by ID"""

        stmt = select(FeedbackDB).where(FeedbackDB.id == feedback_id)
        result = await self.db.execute(stmt)
        feedback_db = result.scalar_one_or_none()

        if feedback_db:
            await self.db.delete(feedback_db)
            await self.db.commit()
            return True

        return False

    async def get_feedback_stats(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict:
        """Get feedback statistics"""

        stmt = select(FeedbackDB)
        conditions = []

        if session_id:
            conditions.append(FeedbackDB.session_id == session_id)
        if user_id:
            conditions.append(FeedbackDB.user_id == user_id)
        if start_date:
            conditions.append(FeedbackDB.created_at >= start_date)
        if end_date:
            conditions.append(FeedbackDB.created_at <= end_date)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        feedback_list = result.scalars().all()

        # Calculate statistics
        total_feedback = len(feedback_list)
        feedback_by_type = {}
        feedback_by_status = {}
        avg_rating = 0
        rating_count = 0

        for feedback_db in feedback_list:
            # Count by type
            feedback_type = feedback_db.feedback_type
            feedback_by_type[feedback_type] = feedback_by_type.get(feedback_type, 0) + 1

            # Count by status
            status = feedback_db.status
            feedback_by_status[status] = feedback_by_status.get(status, 0) + 1

            # Calculate average rating
            if feedback_db.rating:
                avg_rating += feedback_db.rating
                rating_count += 1

        if rating_count > 0:
            avg_rating = avg_rating / rating_count

        return {
            "total_feedback": total_feedback,
            "feedback_by_type": feedback_by_type,
            "feedback_by_status": feedback_by_status,
            "average_rating": round(avg_rating, 2) if avg_rating > 0 else None,
            "rating_count": rating_count,
        }

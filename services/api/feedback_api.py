"""
Feedback API endpoints for PM-005 feedback tracking implementation
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

logger = logging.getLogger(__name__)

from services.database.session_factory import AsyncSessionFactory
from services.feedback.feedback_service import FeedbackService
from services.feedback.models import FeedbackCreateRequest, FeedbackResponse, FeedbackUpdateRequest

# PM-005: Feedback API Router
feedback_router = APIRouter(prefix="/api/v1/feedback", tags=["Feedback"])


async def get_feedback_service() -> FeedbackService:
    """Dependency to get feedback service"""
    async with AsyncSessionFactory.session_scope() as session:
        return FeedbackService(session)


@feedback_router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_data: FeedbackCreateRequest,
):
    """
    Capture user feedback

    This endpoint allows users to submit feedback about their experience with Piper Morgan.
    Feedback is stored with context and can be used for continuous improvement.
    """

    try:
        async with AsyncSessionFactory.session_scope() as session:
            feedback_service = FeedbackService(session)

            # Capture feedback
            feedback_id = await feedback_service.capture_feedback(
                session_id=feedback_data.session_id,
                feedback_type=feedback_data.feedback_type,
                comment=feedback_data.comment,
                rating=feedback_data.rating,
                context=feedback_data.context,
                user_id=feedback_data.user_id,
                conversation_context=feedback_data.conversation_context,
                source=feedback_data.source,
                tags=feedback_data.tags,
            )

            # Get the created feedback
            feedback = await feedback_service.get_feedback(feedback_id)
            if not feedback:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create feedback",
                )

            return feedback

    except Exception as e:
        from services.api.errors import FeedbackCaptureError

        logger.error(f"Failed to capture feedback: {e}")
        raise FeedbackCaptureError(
            operation="saving your feedback",
            details={"error": str(e), "session_id": feedback_data.session_id},
        )


@feedback_router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(feedback_id: str):
    """Get feedback by ID"""

    async with AsyncSessionFactory.session_scope() as session:
        feedback_service = FeedbackService(session)
        feedback = await feedback_service.get_feedback(feedback_id)

        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

        return feedback


@feedback_router.get("/", response_model=List[FeedbackResponse])
async def list_feedback(
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    feedback_type: Optional[str] = Query(None, description="Filter by feedback type"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    limit: int = Query(100, ge=1, le=1000, description="Number of feedback items to return"),
    offset: int = Query(0, ge=0, description="Number of feedback items to skip"),
):
    """List feedback with optional filtering"""

    async with AsyncSessionFactory.session_scope() as session:
        feedback_service = FeedbackService(session)

        feedback_list = await feedback_service.list_feedback(
            session_id=session_id,
            feedback_type=feedback_type,
            status=status_filter,
            user_id=user_id,
            limit=limit,
            offset=offset,
        )

        return feedback_list


@feedback_router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: str,
    update_data: FeedbackUpdateRequest,
):
    """Update feedback status and metadata"""

    async with AsyncSessionFactory.session_scope() as session:
        feedback_service = FeedbackService(session)
        feedback = await feedback_service.update_feedback(feedback_id, update_data)

        if not feedback:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

        return feedback


@feedback_router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(feedback_id: str):
    """Delete feedback by ID"""

    async with AsyncSessionFactory.session_scope() as session:
        feedback_service = FeedbackService(session)
        success = await feedback_service.delete_feedback(feedback_id)

        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")


@feedback_router.get("/stats/summary", response_model=Dict)
async def get_feedback_stats(
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering"),
):
    """Get feedback statistics"""

    async with AsyncSessionFactory.session_scope() as session:
        feedback_service = FeedbackService(session)

        stats = await feedback_service.get_feedback_stats(
            session_id=session_id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        return stats

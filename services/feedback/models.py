"""
Feedback domain models for PM-005 feedback tracking implementation
"""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Feedback(BaseModel):
    """Domain model for user feedback"""

    id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str = Field(..., description="Session ID for context tracking")
    feedback_type: str = Field(..., description="Type of feedback: bug, feature, ux, general")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    comment: str = Field(..., description="User feedback comment")
    context: Dict = Field(default_factory=dict, description="Additional context data")

    # User and session context
    user_id: Optional[str] = Field(None, description="User ID if available")
    conversation_context: Dict = Field(
        default_factory=dict, description="Conversation context if available"
    )

    # Feedback metadata
    source: str = Field(default="api", description="Source of feedback: api, ui, conversation")
    status: str = Field(
        default="new", description="Feedback status: new, reviewed, addressed, closed"
    )
    priority: str = Field(default="medium", description="Priority: low, medium, high, critical")

    # Analysis and processing
    sentiment_score: Optional[float] = Field(None, description="Sentiment score from -1.0 to 1.0")
    categories: List[str] = Field(default_factory=list, description="Auto-detected categories")
    tags: List[str] = Field(default_factory=list, description="User or system tags")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class FeedbackCreateRequest(BaseModel):
    """Request model for creating feedback"""

    session_id: str = Field(..., description="Session ID for context tracking")
    feedback_type: str = Field(..., description="Type of feedback: bug, feature, ux, general")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    comment: str = Field(..., description="User feedback comment")
    context: Dict = Field(default_factory=dict, description="Additional context data")
    user_id: Optional[str] = Field(None, description="User ID if available")
    conversation_context: Dict = Field(
        default_factory=dict, description="Conversation context if available"
    )
    source: str = Field(default="api", description="Source of feedback: api, ui, conversation")
    tags: List[str] = Field(default_factory=list, description="User or system tags")


class FeedbackResponse(BaseModel):
    """Response model for feedback data"""

    id: str
    session_id: str
    feedback_type: str
    rating: Optional[int]
    comment: str
    context: Dict
    user_id: Optional[str]
    conversation_context: Dict
    source: str
    status: str
    priority: str
    sentiment_score: Optional[float]
    categories: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class FeedbackUpdateRequest(BaseModel):
    """Request model for updating feedback"""

    status: Optional[str] = Field(
        None, description="Feedback status: new, reviewed, addressed, closed"
    )
    priority: Optional[str] = Field(None, description="Priority: low, medium, high, critical")
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description="Sentiment score")
    categories: Optional[List[str]] = Field(None, description="Auto-detected categories")
    tags: Optional[List[str]] = Field(None, description="User or system tags")

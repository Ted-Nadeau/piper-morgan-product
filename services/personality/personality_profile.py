"""
Domain Models for Personality Enhancement

PersonalityProfile: User's personality configuration with context adaptation
ResponseContext: Context for response enhancement decisions
EnhancedResponse: Result after personality enhancement
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ConfidenceDisplayStyle(Enum):
    """How confidence should be displayed to user"""

    NUMERIC = "numeric"  # "87% confident"
    DESCRIPTIVE = "descriptive"  # "high confidence"
    CONTEXTUAL = "contextual"  # "Based on recent patterns..."
    HIDDEN = "hidden"  # No confidence shown


class ActionLevel(Enum):
    """How action-oriented responses should be"""

    HIGH = "high"  # Every response has explicit next steps
    MEDIUM = "medium"  # Actionable when relevant
    LOW = "low"  # Minimal action orientation


class TechnicalPreference(Enum):
    """Level of technical detail preferred"""

    DETAILED = "detailed"  # Full technical depth
    BALANCED = "balanced"  # Mix of technical and accessible
    SIMPLIFIED = "simplified"  # Minimize technical jargon


class ResponseType(Enum):
    """Type of response being enhanced"""

    STANDUP = "standup"
    CHAT = "chat"
    CLI = "cli"
    WEB = "web"
    ERROR = "error"


class Enhancement(Enum):
    """Types of enhancements applied"""

    WARMTH_ADDED = "warmth_added"
    CONFIDENCE_INJECTED = "confidence_injected"
    ACTION_EXTRACTED = "action_extracted"
    CONTEXT_ADAPTED = "context_adapted"
    ERROR_SOFTENED = "error_softened"


@dataclass
class PersonalityProfile:
    """User's preferred personality configuration"""

    id: str
    user_id: str
    warmth_level: float  # 0.0 (professional) to 1.0 (friendly)
    confidence_style: ConfidenceDisplayStyle
    action_orientation: ActionLevel
    technical_depth: TechnicalPreference
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    def __post_init__(self):
        """Validate personality profile constraints"""
        if not (0.0 <= self.warmth_level <= 1.0):
            raise ValueError(f"warmth_level must be 0.0-1.0, got {self.warmth_level}")

    def adjust_for_context(self, context: "ResponseContext") -> "PersonalityProfile":
        """Create context-adjusted profile without mutating original"""
        adjusted_warmth = self.warmth_level
        adjusted_confidence_style = self.confidence_style
        adjusted_action = self.action_orientation

        # Adapt based on intent confidence
        if context.intent_confidence < 0.3:
            # Low confidence: Increase warmth, hide confidence, more guidance
            adjusted_warmth = min(1.0, self.warmth_level + 0.2)
            adjusted_confidence_style = ConfidenceDisplayStyle.HIDDEN
            adjusted_action = ActionLevel.HIGH
        elif context.intent_confidence < 0.7:
            # Medium confidence: Moderate warmth, descriptive confidence
            adjusted_warmth = min(1.0, self.warmth_level + 0.1)
            if self.confidence_style == ConfidenceDisplayStyle.NUMERIC:
                adjusted_confidence_style = ConfidenceDisplayStyle.DESCRIPTIVE
        elif context.intent_confidence > 0.8:
            # Very high confidence: More professional, technical confidence
            adjusted_warmth = max(0.0, self.warmth_level - 0.1)
            if self.confidence_style == ConfidenceDisplayStyle.HIDDEN:
                adjusted_confidence_style = ConfidenceDisplayStyle.CONTEXTUAL

        # Adapt for error scenarios
        if context.response_type == ResponseType.ERROR:
            adjusted_warmth = min(1.0, self.warmth_level + 0.3)  # Extra warmth for errors
            adjusted_action = ActionLevel.HIGH  # Always provide guidance for errors

        # Create adjusted profile
        return PersonalityProfile(
            id=self.id,
            user_id=self.user_id,
            warmth_level=adjusted_warmth,
            confidence_style=adjusted_confidence_style,
            action_orientation=adjusted_action,
            technical_depth=self.technical_depth,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
        )

    @classmethod
    def get_default(cls, user_id: str) -> "PersonalityProfile":
        """Create default personality profile"""
        return cls(
            id=f"default_{user_id}",
            user_id=user_id,
            warmth_level=0.6,  # Moderately warm
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
        )


@dataclass
class ResponseContext:
    """Context for response enhancement"""

    intent_confidence: float  # From Intent (0.0-1.0)
    intent_category: str
    intent_action: str
    response_type: ResponseType
    user_stress_indicators: List[str] = field(default_factory=list)
    conversation_history: Optional[List[Dict[str, Any]]] = None
    original_message: str = ""

    def __post_init__(self):
        """Validate response context"""
        if not (0.0 <= self.intent_confidence <= 1.0):
            raise ValueError(f"intent_confidence must be 0.0-1.0, got {self.intent_confidence}")


@dataclass
class EnhancedResponse:
    """Response after personality enhancement"""

    original_content: str
    enhanced_content: str
    personality_profile_used: PersonalityProfile
    confidence_displayed: Optional[float]
    enhancements_applied: List[Enhancement]
    processing_time_ms: float
    context: ResponseContext
    success: bool = True
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "original_content": self.original_content,
            "enhanced_content": self.enhanced_content,
            "confidence_displayed": self.confidence_displayed,
            "enhancements_applied": [e.value for e in self.enhancements_applied],
            "processing_time_ms": self.processing_time_ms,
            "success": self.success,
            "error_message": self.error_message,
            "profile_used": {
                "warmth_level": self.personality_profile_used.warmth_level,
                "confidence_style": self.personality_profile_used.confidence_style.value,
                "action_orientation": self.personality_profile_used.action_orientation.value,
                "technical_depth": self.personality_profile_used.technical_depth.value,
            },
        }

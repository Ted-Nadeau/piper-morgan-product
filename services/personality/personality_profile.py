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

from sqlalchemy import select, text

from services.database.models import AlphaUser
from services.database.session_factory import AsyncSessionFactory

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

    def get_response_style_guidance(self) -> str:
        """
        Generate response guidance based on combined preferences and personality profile.

        Maps questionnaire preferences (communication_style, work_style, etc.) to
        response guidance that can be used in prompts.

        Returns:
            str: Guidance string describing how to format responses
        """
        guidance_parts = []

        # Warmth level influences greeting and tone
        if self.warmth_level >= 0.7:
            guidance_parts.append("Use a friendly, warm tone.")
        elif self.warmth_level >= 0.4:
            guidance_parts.append("Use a balanced, professional tone.")
        else:
            guidance_parts.append("Use a concise, professional tone.")

        # Action orientation influences next steps
        if self.action_orientation == ActionLevel.HIGH:
            guidance_parts.append("Always include clear next steps and action items.")
        elif self.action_orientation == ActionLevel.MEDIUM:
            guidance_parts.append("Include next steps when relevant.")
        else:
            guidance_parts.append("Minimize action-oriented language.")

        # Technical depth influences complexity
        if self.technical_depth == TechnicalPreference.DETAILED:
            guidance_parts.append(
                "Provide comprehensive technical depth and implementation details."
            )
        elif self.technical_depth == TechnicalPreference.BALANCED:
            guidance_parts.append("Balance technical accuracy with accessibility.")
        else:
            guidance_parts.append("Minimize technical jargon, focus on high-level concepts.")

        # Confidence style influences certainty expression
        if self.confidence_style == ConfidenceDisplayStyle.NUMERIC:
            guidance_parts.append("Include confidence percentages when providing estimates.")
        elif self.confidence_style == ConfidenceDisplayStyle.CONTEXTUAL:
            guidance_parts.append("Ground confidence in context and reasoning.")
        elif self.confidence_style == ConfidenceDisplayStyle.HIDDEN:
            guidance_parts.append("Avoid expressing uncertainty or confidence levels.")

        return " ".join(guidance_parts)

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

    @classmethod
    async def load_with_preferences(cls, user_id: str) -> "PersonalityProfile":
        """
        Load or create a personality profile with user preferences applied.

        Loads preferences from alpha_users.preferences JSONB column and applies
        them to the personality profile attributes:

        - communication_style → warmth_level
        - work_style → action_orientation
        - decision_making → confidence_style
        - learning_style → technical_depth
        - feedback_level → influences output verbosity

        If preferences not set, uses balanced defaults.

        Args:
            user_id: User ID to load preferences for

        Returns:
            PersonalityProfile with preferences applied, or default if not set

        Raises:
            ValueError: If user not found in alpha_users table
        """
        try:
            # Load user preferences from database
            async with AsyncSessionFactory.session_scope() as session:
                # Query for alpha_users record
                result = await session.execute(select(AlphaUser).where(AlphaUser.id == user_id))
                user = result.scalar_one_or_none()

                if not user:
                    logger.warning(f"User {user_id} not found in alpha_users, using defaults")
                    return cls.get_default(user_id)

                # Extract preferences or use empty dict
                preferences = user.preferences or {}

                # Map questionnaire preferences to PersonalityProfile attributes
                return cls._create_from_preferences(user_id, preferences)

        except Exception as e:
            logger.error(f"Failed to load preferences for user {user_id}: {e}")
            # Fallback to defaults on error
            return cls.get_default(user_id)

    @classmethod
    def _create_from_preferences(cls, user_id: str, preferences: Dict) -> "PersonalityProfile":
        """
        Create PersonalityProfile by mapping questionnaire preferences.

        Args:
            user_id: User ID
            preferences: Dictionary of preferences from alpha_users.preferences

        Returns:
            PersonalityProfile with preferences applied
        """
        # Map communication_style to warmth_level
        communication_style = preferences.get("communication_style", "balanced")
        if communication_style == "concise":
            warmth_level = 0.4  # More professional, less warm
        elif communication_style == "detailed":
            warmth_level = 0.7  # More warm, detailed explanations
        else:  # balanced
            warmth_level = 0.6  # Default balanced

        # Map work_style to action_orientation
        work_style = preferences.get("work_style", "flexible")
        if work_style == "structured":
            action_orientation = ActionLevel.HIGH  # Structured needs clear steps
        elif work_style == "exploratory":
            action_orientation = ActionLevel.LOW  # Exploratory prefers open-ended
        else:  # flexible
            action_orientation = ActionLevel.MEDIUM  # Flexible adapts to context

        # Map decision_making to confidence_style
        decision_making = preferences.get("decision_making", "collaborative")
        if decision_making == "data-driven":
            confidence_style = ConfidenceDisplayStyle.NUMERIC  # Data needs numbers
        elif decision_making == "intuitive":
            confidence_style = ConfidenceDisplayStyle.CONTEXTUAL  # Intuitive needs reasoning
        else:  # collaborative
            confidence_style = ConfidenceDisplayStyle.DESCRIPTIVE  # Collaborative needs explanation

        # Map learning_style to technical_depth
        learning_style = preferences.get("learning_style", "examples")
        if learning_style == "examples":
            technical_depth = TechnicalPreference.BALANCED  # Examples work with balanced depth
        elif learning_style == "explanations":
            technical_depth = TechnicalPreference.DETAILED  # Explanations need depth
        else:  # exploration
            technical_depth = TechnicalPreference.SIMPLIFIED  # Exploration starts simple

        # feedback_level is stored in preferences but influences response length
        # (can be used by calling code)
        feedback_level = preferences.get("feedback_level", "moderate")

        logger.info(
            f"Applied preferences for user {user_id}: "
            f"communication_style={communication_style}, "
            f"work_style={work_style}, "
            f"decision_making={decision_making}, "
            f"learning_style={learning_style}, "
            f"feedback_level={feedback_level}"
        )

        return cls(
            id=f"profile_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            warmth_level=warmth_level,
            confidence_style=confidence_style,
            action_orientation=action_orientation,
            technical_depth=technical_depth,
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

"""
Issue #552, #553, #555: Standup conversation management package.

Provides:
- StandupConversationManager: State machine for conversations
- InvalidStateTransitionError: Exception for invalid transitions
- StandupConversationHandler: Multi-turn conversation flow handler
- ConversationResponse: Response dataclass for handler output
- UserStandupPreference: Typed preference model (#555)
- PreferenceExtractor: Rule-based preference extraction (#555)
- PreferenceApplicator: Applies preferences to standup generation (#555)
"""

from services.standup.conversation_handler import ConversationResponse, StandupConversationHandler
from services.standup.conversation_manager import (
    InvalidStateTransitionError,
    StandupConversationManager,
)
from services.standup.preference_applicator import (
    AppliedPreferences,
    PreferenceApplicator,
    get_user_applied_preferences,
)
from services.standup.preference_extractor import PreferenceExtractor, extract_preferences
from services.standup.preference_feedback import (
    ConfirmationPrompt,
    CorrectionResult,
    PreferenceFeedbackHandler,
    handle_preference_feedback,
)
from services.standup.preference_models import (
    ExtractedPreference,
    PreferenceChange,
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)
from services.standup.preference_service import (
    UserPreferenceService,
    get_user_preferences,
    save_user_preference,
)

__all__ = [
    # Conversation management (#552, #553)
    "StandupConversationManager",
    "InvalidStateTransitionError",
    "StandupConversationHandler",
    "ConversationResponse",
    # Preference learning (#555)
    "UserStandupPreference",
    "PreferenceType",
    "PreferenceSource",
    "PreferenceChange",
    "ExtractedPreference",
    "PreferenceExtractor",
    "extract_preferences",
    "UserPreferenceService",
    "get_user_preferences",
    "save_user_preference",
    # Preference application (#555)
    "AppliedPreferences",
    "PreferenceApplicator",
    "get_user_applied_preferences",
    # Preference feedback (#555)
    "CorrectionResult",
    "ConfirmationPrompt",
    "PreferenceFeedbackHandler",
    "handle_preference_feedback",
]

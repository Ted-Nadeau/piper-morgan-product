"""
Memory services for cross-session context.

ADR-054: Cross-Session Memory Architecture
- Phase 1 (#657): Conversational Memory Infrastructure
- Phase 2 (#662): Greeting Context Service
- Phase 3 (#663): User History Enhancements
- Phase 4 (#664): Memory Integration
"""

from services.memory.conversation_summarizer import (
    ConversationSummarizer,
    ConversationSummaryResult,
)
from services.memory.conversational_memory import (
    ConversationalMemoryEntry,
    ConversationalMemoryService,
    ConversationalMemoryWindow,
)
from services.memory.greeting_context import (
    GREETING_APPROACHES,
    GreetingCondition,
    GreetingContext,
    GreetingContextService,
)
from services.memory.privacy_mode import PrivacyModeService, PrivacyReason, PrivacyState
from services.memory.session_hooks import on_session_end, on_session_timeout
from services.memory.user_history import (
    ConversationDetail,
    ConversationSummary,
    InMemoryUserHistoryRepository,
    UserHistoryPage,
    UserHistoryRepository,
    UserHistoryService,
)

__all__ = [
    # Phase 1: Conversational Memory (#657)
    "ConversationalMemoryEntry",
    "ConversationalMemoryWindow",
    "ConversationalMemoryService",
    # Phase 2: Greeting Context (#662)
    "GREETING_APPROACHES",
    "GreetingCondition",
    "GreetingContext",
    "GreetingContextService",
    # Phase 3: User History (#663)
    "ConversationDetail",
    "ConversationSummary",
    "InMemoryUserHistoryRepository",
    "UserHistoryPage",
    "UserHistoryRepository",
    "UserHistoryService",
    # Phase 4: Memory Integration (#664)
    "ConversationSummarizer",
    "ConversationSummaryResult",
    "on_session_end",
    "on_session_timeout",
    "PrivacyModeService",
    "PrivacyReason",
    "PrivacyState",
]

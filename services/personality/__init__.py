"""
Personality Enhancement Module

Provides personality enhancement for responses across all interfaces.
Built on DDD principles with ResponsePersonalityEnhancer as aggregate root.

Core Components:
- ResponsePersonalityEnhancer: Aggregate root for response enhancement
- PersonalityProfile: User personality preferences entity
- TransformationService: Content transformation domain service
- StandupToChatBridge: Standup integration service

Performance: <100ms enhancement constraint with circuit breaker protection
"""

from .personality_profile import EnhancedResponse, PersonalityProfile, ResponseContext
from .response_enhancer import ResponsePersonalityEnhancer
from .standup_bridge import StandupToChatBridge
from .transformations import TransformationService

__all__ = [
    "ResponsePersonalityEnhancer",
    "PersonalityProfile",
    "ResponseContext",
    "EnhancedResponse",
    "TransformationService",
    "StandupToChatBridge",
]

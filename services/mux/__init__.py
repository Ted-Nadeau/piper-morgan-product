# mux module - MUX-VISION Object Model Implementation
# Core grammar abstractions: Entity, Moment, Place protocols and perceptual lenses
#
# This module provides:
# - Protocols: EntityProtocol, MomentProtocol, PlaceProtocol (role-fluid substrates)
# - Situation: Async context manager for framing sequences of Moments
# - Perception: Result of perceiving through lenses (consciousness-preserving)
# - Lenses: 8 perceptual lenses mapping to 8D spatial dimensions
# - Ownership: 3-category model (NATIVE/FEDERATED/SYNTHETIC)
# - Lifecycle: 8-stage state machine with composting
#
# References:
# - ADR-045: Object Model Specification
# - ADR-055: Object Model Implementation
# - ADR-038: Spatial Intelligence Patterns

from .consciousness import (
    AwarenessLevel,
    Capability,
    ConsciousnessAttributes,
    ConsciousnessExpression,
    EmotionalState,
    EntityContext,
    EntityRole,
    PiperEntity,
    TrustLevel,
)
from .lifecycle import (
    VALID_TRANSITIONS,
    CompostingExtractor,
    CompostResult,
    HasLifecycle,
    InvalidTransitionError,
    LifecycleManager,
    LifecycleState,
    LifecycleTransition,
)
from .ownership import (
    HasOwnership,
    OwnershipCategory,
    OwnershipMetadata,
    OwnershipResolution,
    OwnershipResolver,
    OwnershipTransformation,
)
from .perception import Perception, PerceptionMode
from .protocols import EntityProtocol, MomentProtocol, PlaceProtocol, Target
from .situation import Situation, SituationLearning

__all__ = [
    # Protocols (substrates)
    "EntityProtocol",
    "MomentProtocol",
    "PlaceProtocol",
    "Target",
    # Situation (frame)
    "Situation",
    "SituationLearning",
    # Perception
    "Perception",
    "PerceptionMode",
    # Consciousness (#434)
    "AwarenessLevel",
    "Capability",
    "ConsciousnessAttributes",
    "ConsciousnessExpression",
    "EmotionalState",
    "EntityContext",
    "EntityRole",
    "PiperEntity",
    "TrustLevel",
    # Ownership (#435)
    "HasOwnership",
    "OwnershipCategory",
    "OwnershipMetadata",
    "OwnershipResolution",
    "OwnershipResolver",
    "OwnershipTransformation",
    # Lifecycle (P3)
    "CompostingExtractor",
    "CompostResult",
    "HasLifecycle",
    "InvalidTransitionError",
    "LifecycleManager",
    "LifecycleState",
    "LifecycleTransition",
    "VALID_TRANSITIONS",
]

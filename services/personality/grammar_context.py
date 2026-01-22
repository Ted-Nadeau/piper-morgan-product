"""
Personality Grammar Context - Rich context for grammar-conscious personality responses.

This module provides the context bridge between personality preferences
and grammar-conscious response generation.

Issue #627: GRAMMAR-TRANSFORM: Personality System
Phase 1: Response Context
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)


class SituationType(str, Enum):
    """Current situation for personality calibration."""

    NORMAL = "normal"  # Regular interaction
    SUCCESS = "success"  # Something went well
    ERROR = "error"  # Something went wrong
    CLARIFICATION = "clarification"  # Need to clarify
    GREETING = "greeting"  # Initial greeting
    FAREWELL = "farewell"  # Signing off
    BUSY = "busy"  # User seems busy
    FRUSTRATED = "frustrated"  # User seems frustrated


class GrammarLens(str, Enum):
    """Grammar lenses that can be applied."""

    COLLABORATIVE = "collaborative"  # User-Piper relationship
    TEMPORAL = "temporal"  # Time awareness
    SPATIAL = "spatial"  # Context/scope awareness
    EPISTEMIC = "epistemic"  # Certainty/uncertainty


@dataclass
class PersonalityGrammarContext:
    """Rich context for grammar-conscious personality responses.

    In MUX grammar: captures the relationship and situational context
    for personality expression. This is how Piper knows to be warmer
    when things go wrong and more concise when users are busy.

    Attributes:
        warmth_level: User's warmth preference (0.0-1.0)
        confidence_style: How to express confidence
        action_level: How action-oriented to be
        technical_depth: How technical to be
        situation: Current interaction situation
        active_lenses: Which grammar lenses apply
        is_first_interaction: First time talking to this user
        interaction_count: How many times we've interacted
        personality_available: Whether preferences are available
    """

    # User preferences (from PersonalityProfile)
    warmth_level: float = 0.6  # 0.0 (professional) to 1.0 (friendly)
    confidence_style: ConfidenceDisplayStyle = ConfidenceDisplayStyle.CONTEXTUAL
    action_level: ActionLevel = ActionLevel.MEDIUM
    technical_depth: TechnicalPreference = TechnicalPreference.BALANCED

    # Current situation
    situation: SituationType = SituationType.NORMAL
    seems_frustrated: bool = False
    seems_busy: bool = False

    # Grammar lenses
    active_lenses: List[GrammarLens] = field(default_factory=list)

    # Relationship
    is_first_interaction: bool = True
    interaction_count: int = 0

    # System state
    personality_available: bool = True

    @classmethod
    def from_personality_profile(
        cls,
        profile: PersonalityProfile,
        situation: SituationType = SituationType.NORMAL,
        interaction_count: int = 0,
    ) -> "PersonalityGrammarContext":
        """Build context from PersonalityProfile.

        Args:
            profile: User's personality profile
            situation: Current situation type
            interaction_count: Number of previous interactions

        Returns:
            PersonalityGrammarContext with populated fields
        """
        # Determine active lenses based on situation
        lenses = [GrammarLens.COLLABORATIVE]  # Always active
        if situation in (SituationType.BUSY, SituationType.ERROR):
            lenses.append(GrammarLens.TEMPORAL)
        if situation == SituationType.CLARIFICATION:
            lenses.append(GrammarLens.EPISTEMIC)

        return cls(
            warmth_level=profile.warmth_level,
            confidence_style=profile.confidence_style,
            action_level=profile.action_orientation,
            technical_depth=profile.technical_depth,
            situation=situation,
            active_lenses=lenses,
            is_first_interaction=interaction_count == 0,
            interaction_count=interaction_count,
            personality_available=True,
        )

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        situation: SituationType = SituationType.NORMAL,
    ) -> "PersonalityGrammarContext":
        """Build context from dictionary data.

        Args:
            data: Dictionary with personality data
            situation: Current situation type

        Returns:
            PersonalityGrammarContext with populated fields
        """
        if not data:
            return cls(personality_available=False)

        warmth = data.get("warmth_level", 0.6)
        if not 0.0 <= warmth <= 1.0:
            warmth = 0.6  # Default if invalid

        # Parse enums from strings
        try:
            conf_style = ConfidenceDisplayStyle(data.get("confidence_style", "contextual"))
        except ValueError:
            conf_style = ConfidenceDisplayStyle.CONTEXTUAL

        try:
            action = ActionLevel(data.get("action_level", "medium"))
        except ValueError:
            action = ActionLevel.MEDIUM

        try:
            tech = TechnicalPreference(data.get("technical_depth", "balanced"))
        except ValueError:
            tech = TechnicalPreference.BALANCED

        return cls(
            warmth_level=warmth,
            confidence_style=conf_style,
            action_level=action,
            technical_depth=tech,
            situation=situation,
            is_first_interaction=data.get("is_first_interaction", True),
            interaction_count=data.get("interaction_count", 0),
            personality_available=True,
        )

    @classmethod
    def default(cls) -> "PersonalityGrammarContext":
        """Create default context."""
        return cls()

    @classmethod
    def unavailable(cls) -> "PersonalityGrammarContext":
        """Create context when personality data unavailable."""
        return cls(personality_available=False)

    def is_warm(self) -> bool:
        """Check if warmth is high."""
        return self.warmth_level >= 0.7

    def is_professional(self) -> bool:
        """Check if tone should be professional."""
        return self.warmth_level < 0.4

    def needs_extra_warmth(self) -> bool:
        """Check if extra warmth is needed based on situation."""
        return self.situation in (
            SituationType.ERROR,
            SituationType.FRUSTRATED,
            SituationType.CLARIFICATION,
        )

    def should_be_concise(self) -> bool:
        """Check if responses should be concise."""
        return self.seems_busy or self.situation == SituationType.BUSY

    def has_lens(self, lens: GrammarLens) -> bool:
        """Check if a lens is active."""
        return lens in self.active_lenses

    def get_effective_warmth(self) -> float:
        """Get warmth level adjusted for situation.

        Errors and frustration increase warmth.
        Busy situations may reduce verbosity but not warmth.
        """
        warmth = self.warmth_level

        if self.needs_extra_warmth():
            warmth = min(1.0, warmth + 0.2)

        return warmth

    def get_formality(self) -> str:
        """Get appropriate formality based on context.

        Returns:
            "warm", "professional", "conversational", or "terse"
        """
        effective_warmth = self.get_effective_warmth()

        if self.should_be_concise():
            return "terse"
        elif effective_warmth >= 0.7:
            return "warm"
        elif effective_warmth < 0.4:
            return "professional"
        else:
            return "conversational"

    def get_confidence_approach(self) -> str:
        """Get how to express confidence.

        Returns human-readable description of confidence approach.
        """
        approaches = {
            ConfidenceDisplayStyle.NUMERIC: "Use percentages and specific numbers",
            ConfidenceDisplayStyle.DESCRIPTIVE: "Use words like 'likely' or 'possibly'",
            ConfidenceDisplayStyle.CONTEXTUAL: "Ground confidence in reasoning",
            ConfidenceDisplayStyle.HIDDEN: "Avoid expressing uncertainty",
        }
        return approaches.get(self.confidence_style, "Express confidence naturally")

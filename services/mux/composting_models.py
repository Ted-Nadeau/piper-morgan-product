"""
Composting domain models for the learning pipeline.

Part of #665 COMPOSTING-MODELS (child of #436 MUX-TECH-PHASE4-COMPOSTING).

This module provides:
- CompostingTrigger: What triggers composting
- Pattern, Insight, Correction: Types of learning
- ExtractedLearning: Unified learning model with surfacing control

These models flow through:
  CompostBin (#666) → Pipeline (#667) → InsightJournal → Surfacing (#415)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

# =============================================================================
# Composting Triggers
# =============================================================================


class CompostingTrigger(Enum):
    """
    What triggers an object to enter composting.

    Objects can be composted for various reasons, each affecting
    how the learning is framed and prioritized.
    """

    AGE = "age"  # Object is old enough (30+ days deprecated)
    IRRELEVANCE = "irrelevance"  # No longer referenced by active objects
    MANUAL = "manual"  # User explicitly requested
    SCHEDULED = "scheduled"  # During "rest" periods (filing dreams)
    CONTRADICTION = "contradiction"  # New information invalidates this


# =============================================================================
# Learning Types
# =============================================================================


@dataclass
class Pattern:
    """
    Recurring structure noticed across objects.

    Patterns are the first level of learning - noticing that
    something happens repeatedly.

    Example:
        "User schedules standup meetings on Monday mornings"
        occurrences: ["standup-2024-01", "standup-2024-02", ...]
        frequency: 0.9 (90% of Mondays)
        predictive_power: 0.85 (predicts next Monday standup)
    """

    description: str
    occurrences: List[str] = field(default_factory=list)
    frequency: float = 0.0  # 0.0-1.0, how often pattern appears
    predictive_power: float = 0.0  # 0.0-1.0, how well it predicts

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "description": self.description,
            "occurrences": self.occurrences,
            "frequency": self.frequency,
            "predictive_power": self.predictive_power,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pattern":
        """Create from dictionary."""
        return cls(
            description=data.get("description", ""),
            occurrences=data.get("occurrences", []),
            frequency=data.get("frequency", 0.0),
            predictive_power=data.get("predictive_power", 0.0),
        )


@dataclass
class Insight:
    """
    Understanding that emerges from patterns.

    Insights are derived from patterns - the "why" behind the "what".
    They represent Piper's understanding, not just observation.

    Example:
        description: "User prefers morning standups because afternoons
                      are reserved for deep work"
        derived_from: ["pattern-monday-standup", "pattern-afternoon-focus"]
        confidence: 0.8
        surprisingness: 0.3 (not very surprising)
    """

    description: str
    derived_from: List[str] = field(default_factory=list)  # Pattern IDs
    confidence: float = 0.5  # 0.0-1.0
    surprisingness: float = 0.0  # 0.0-1.0, how unexpected

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "description": self.description,
            "derived_from": self.derived_from,
            "confidence": self.confidence,
            "surprisingness": self.surprisingness,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Insight":
        """Create from dictionary."""
        return cls(
            description=data.get("description", ""),
            derived_from=data.get("derived_from", []),
            confidence=data.get("confidence", 0.5),
            surprisingness=data.get("surprisingness", 0.0),
        )


@dataclass
class Correction:
    """
    Learning that invalidates previous understanding.

    Corrections are special - they update Piper's mental model.
    They should be surfaced with higher priority because acting
    on outdated understanding is harmful.

    Example:
        previous_understanding: "User prefers email for client comms"
        new_understanding: "User now prefers Slack for client comms"
        evidence: ["conv-123", "conv-456"] (conversations showing change)
        confidence: 0.9
    """

    previous_understanding: str
    new_understanding: str
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "previous_understanding": self.previous_understanding,
            "new_understanding": self.new_understanding,
            "evidence": self.evidence,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Correction":
        """Create from dictionary."""
        return cls(
            previous_understanding=data.get("previous_understanding", ""),
            new_understanding=data.get("new_understanding", ""),
            evidence=data.get("evidence", []),
            confidence=data.get("confidence", 0.5),
        )


# =============================================================================
# Extracted Learning (Unified Model)
# =============================================================================


@dataclass
class ExtractedLearning:
    """
    What Piper learns from composted objects.

    This is the unified model that flows through the pipeline:
    CompostingExtractor → InsightJournal → Surfacing (#415)

    Each learning contains ONE of: pattern, insight, or correction.
    The learning_type property identifies which.

    Surfacing control fields enable #415 PREMONITION to determine
    when and how to surface this learning.
    """

    # Identity
    id: str = field(default_factory=lambda: str(uuid4()))
    source_objects: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    # The learning (exactly one should be populated)
    pattern: Optional[Pattern] = None
    insight: Optional[Insight] = None
    correction: Optional[Correction] = None

    # Confidence and relevance
    confidence: float = 0.5  # 0.0-1.0, overall confidence
    applies_to_entities: List[str] = field(default_factory=list)
    topic_tags: List[str] = field(default_factory=list)

    # Surfacing control (for #415 PREMONITION)
    expression: str = ""  # How Piper would say this
    requires_attention: bool = False  # True for corrections/concerns

    @property
    def learning_type(self) -> str:
        """Determine which type of learning this is."""
        if self.pattern is not None:
            return "pattern"
        if self.insight is not None:
            return "insight"
        if self.correction is not None:
            return "correction"
        return "unknown"

    @property
    def description(self) -> str:
        """Get the description from whichever learning type is set."""
        if self.pattern is not None:
            return self.pattern.description
        if self.insight is not None:
            return self.insight.description
        if self.correction is not None:
            return self.correction.new_understanding
        return ""

    @property
    def is_high_confidence(self) -> bool:
        """Check if confidence meets threshold for push surfacing (0.75)."""
        return self.confidence >= 0.75

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "id": self.id,
            "source_objects": self.source_objects,
            "created_at": self.created_at.isoformat(),
            "learning_type": self.learning_type,
            "confidence": self.confidence,
            "applies_to_entities": self.applies_to_entities,
            "topic_tags": self.topic_tags,
            "expression": self.expression,
            "requires_attention": self.requires_attention,
        }

        if self.pattern is not None:
            result["pattern"] = self.pattern.to_dict()
        if self.insight is not None:
            result["insight"] = self.insight.to_dict()
        if self.correction is not None:
            result["correction"] = self.correction.to_dict()

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractedLearning":
        """Create from dictionary."""
        pattern = None
        insight = None
        correction = None

        if "pattern" in data:
            pattern = Pattern.from_dict(data["pattern"])
        if "insight" in data:
            insight = Insight.from_dict(data["insight"])
        if "correction" in data:
            correction = Correction.from_dict(data["correction"])

        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            created_at = datetime.now()

        return cls(
            id=data.get("id", str(uuid4())),
            source_objects=data.get("source_objects", []),
            created_at=created_at,
            pattern=pattern,
            insight=insight,
            correction=correction,
            confidence=data.get("confidence", 0.5),
            applies_to_entities=data.get("applies_to_entities", []),
            topic_tags=data.get("topic_tags", []),
            expression=data.get("expression", ""),
            requires_attention=data.get("requires_attention", False),
        )


# =============================================================================
# Factory Functions
# =============================================================================


def create_pattern_learning(
    description: str,
    occurrences: List[str],
    frequency: float = 0.0,
    predictive_power: float = 0.0,
    source_objects: Optional[List[str]] = None,
    confidence: Optional[float] = None,
    topic_tags: Optional[List[str]] = None,
) -> ExtractedLearning:
    """
    Create an ExtractedLearning containing a Pattern.

    Convenience factory for the common case of creating
    a pattern-based learning.
    """
    pattern = Pattern(
        description=description,
        occurrences=occurrences,
        frequency=frequency,
        predictive_power=predictive_power,
    )

    # Default confidence from pattern's predictive power if not specified
    effective_confidence = confidence if confidence is not None else predictive_power

    return ExtractedLearning(
        source_objects=source_objects or [],
        pattern=pattern,
        confidence=effective_confidence,
        topic_tags=topic_tags or [],
        expression=f"I've noticed a pattern: {description}",
    )


def create_insight_learning(
    description: str,
    derived_from: List[str],
    confidence: float = 0.5,
    surprisingness: float = 0.0,
    source_objects: Optional[List[str]] = None,
    topic_tags: Optional[List[str]] = None,
) -> ExtractedLearning:
    """
    Create an ExtractedLearning containing an Insight.

    Convenience factory for the common case of creating
    an insight-based learning.
    """
    insight = Insight(
        description=description,
        derived_from=derived_from,
        confidence=confidence,
        surprisingness=surprisingness,
    )

    return ExtractedLearning(
        source_objects=source_objects or [],
        insight=insight,
        confidence=confidence,
        topic_tags=topic_tags or [],
        expression=f"It occurs to me that {description}",
    )


def create_correction_learning(
    previous_understanding: str,
    new_understanding: str,
    evidence: List[str],
    confidence: float = 0.5,
    source_objects: Optional[List[str]] = None,
    topic_tags: Optional[List[str]] = None,
) -> ExtractedLearning:
    """
    Create an ExtractedLearning containing a Correction.

    Corrections always require attention since they update
    Piper's mental model.
    """
    correction = Correction(
        previous_understanding=previous_understanding,
        new_understanding=new_understanding,
        evidence=evidence,
        confidence=confidence,
    )

    return ExtractedLearning(
        source_objects=source_objects or [],
        correction=correction,
        confidence=confidence,
        topic_tags=topic_tags or [],
        expression=f"I think I had something wrong - {new_understanding}",
        requires_attention=True,  # Corrections always need attention
    )

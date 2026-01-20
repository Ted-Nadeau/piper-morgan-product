"""
Perception Module - Result of Perceiving Through a Lens

Perception is what an Entity experiences when viewing something through a Lens.
It contains both raw data (from integrations) and experience-framed observations
(consciousness-preserving language).

Key insight: Perception uses experience language ("I notice...") not data language
("data: {...}"). This preserves the consciousness of the original vision.

PerceptionMode captures temporal perspective:
- NOTICING: Current state (what is)
- REMEMBERING: Historical state (what was)
- ANTICIPATING: Future state (what will be)

References:
- ADR-045: Object Model Specification
- Morning Standup patterns for experience framing
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class PerceptionMode(Enum):
    """
    Temporal perspective for perception.

    Different modes frame observation differently:
    - NOTICING: "You have 3 meetings today" (present)
    - REMEMBERING: "Yesterday was quieter" (past)
    - ANTICIPATING: "Tomorrow looks busy" (future)
    """

    NOTICING = "noticing"  # Current state - what is
    REMEMBERING = "remembering"  # Historical state - what was
    ANTICIPATING = "anticipating"  # Future state - what will be


@dataclass
class Perception:
    """
    Result of perceiving through a lens.

    Perception bridges raw data (from integrations) and experience
    (consciousness-preserving observations). It answers:
    - What lens was used?
    - What temporal mode?
    - What raw data was found?
    - How is this framed as experience?

    Example:
        Perception(
            lens_name="temporal",
            mode=PerceptionMode.NOTICING,
            raw_data={"meetings": [{"time": "10am"}, {"time": "2pm"}]},
            observation="You have 2 meetings today, at 10am and 2pm",
            confidence=0.95
        )
    """

    lens_name: str  # Which lens created this perception
    mode: PerceptionMode  # Temporal perspective
    raw_data: Dict[str, Any]  # Raw data from integration
    observation: str  # Experience-framed description
    confidence: float = 1.0  # Confidence level (0.0 to 1.0)
    timestamp: Optional[datetime] = None  # When perception was created
    source: Optional[str] = None  # Data source (e.g., "slack", "github")

    def __post_init__(self):
        """Validate perception data."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")

    @property
    def is_current(self) -> bool:
        """Check if this perception is about current state."""
        return self.mode == PerceptionMode.NOTICING

    @property
    def is_historical(self) -> bool:
        """Check if this perception is about past state."""
        return self.mode == PerceptionMode.REMEMBERING

    @property
    def is_future(self) -> bool:
        """Check if this perception is about future state."""
        return self.mode == PerceptionMode.ANTICIPATING

    def with_confidence(self, new_confidence: float) -> "Perception":
        """Create a copy with different confidence level."""
        return Perception(
            lens_name=self.lens_name,
            mode=self.mode,
            raw_data=self.raw_data,
            observation=self.observation,
            confidence=new_confidence,
            timestamp=self.timestamp,
            source=self.source,
        )

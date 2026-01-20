"""
Ownership model for Piper's relationship to knowledge.

This module defines how Piper relates to objects:
- NATIVE: Piper's Mind - what Piper creates/owns directly
- FEDERATED: Piper's Senses - what Piper observes externally
- SYNTHETIC: Piper's Understanding - what Piper constructs through reasoning

References:
- ADR-045: Object Model Specification
- ADR-055: Object Model Implementation
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


class OwnershipCategory(Enum):
    """
    Describes Piper's epistemological relationship to knowledge.

    The three categories represent how Piper knows things:
    - NATIVE: "I know this because I created it" (Mind)
    - FEDERATED: "I see this in [Place]" (Senses)
    - SYNTHETIC: "I understand this to mean..." (Understanding)
    """

    NATIVE = "native"
    FEDERATED = "federated"
    SYNTHETIC = "synthetic"

    @property
    def description(self) -> str:
        """Detailed description of this ownership category."""
        descriptions = {
            OwnershipCategory.NATIVE: (
                "Objects Piper creates and owns directly - "
                "sessions, memories, trust states, learning"
            ),
            OwnershipCategory.FEDERATED: (
                "Objects Piper observes from external sources - "
                "GitHub issues, Slack messages, calendar events"
            ),
            OwnershipCategory.SYNTHETIC: (
                "Objects Piper constructs through reasoning - "
                "inferred status, assembled risk, pattern recognition"
            ),
        }
        return descriptions[self]

    @property
    def metaphor(self) -> str:
        """Consciousness metaphor for this category."""
        metaphors = {
            OwnershipCategory.NATIVE: "Piper's Mind",
            OwnershipCategory.FEDERATED: "Piper's Senses",
            OwnershipCategory.SYNTHETIC: "Piper's Understanding",
        }
        return metaphors[self]

    @property
    def experience_phrase(self) -> str:
        """How Piper expresses knowledge from this category."""
        phrases = {
            OwnershipCategory.NATIVE: "I know this because I created it",
            OwnershipCategory.FEDERATED: "I see this in {place}",
            OwnershipCategory.SYNTHETIC: "I understand this to mean...",
        }
        return phrases[self]


@runtime_checkable
class HasOwnership(Protocol):
    """
    Protocol for objects with ownership awareness.

    Any object can satisfy this protocol by providing:
    - ownership_category: Which category (NATIVE/FEDERATED/SYNTHETIC)
    - ownership_source: Where this object came from
    - ownership_confidence: How certain we are (0.0 to 1.0)

    Example:
        class MySession:
            @property
            def ownership_category(self) -> OwnershipCategory:
                return OwnershipCategory.NATIVE

            @property
            def ownership_source(self) -> str:
                return "piper"

            @property
            def ownership_confidence(self) -> float:
                return 1.0

        session = MySession()
        assert isinstance(session, HasOwnership)  # True
    """

    @property
    def ownership_category(self) -> OwnershipCategory:
        """The ownership category of this object."""
        ...

    @property
    def ownership_source(self) -> str:
        """The source/origin (e.g., 'piper', 'github', 'inference')."""
        ...

    @property
    def ownership_confidence(self) -> float:
        """Confidence in ownership categorization (0.0 to 1.0)."""
        ...


@dataclass(frozen=True)
class OwnershipResolution:
    """
    Result of resolving an object's ownership category.

    Contains the determined category along with confidence and reasoning
    to support auditing and debugging.
    """

    category: OwnershipCategory
    confidence: float
    reasoning: str
    source: str
    is_derived: bool = False
    is_cached: bool = False

    def __post_init__(self):
        """Validate confidence is in valid range."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.confidence}")


class OwnershipResolver:
    """
    Resolves ownership categories for objects based on source and attributes.

    The resolver determines how Piper relates to an object:
    - NATIVE: Created by Piper (source='piper', 'system')
    - FEDERATED: Observed from external sources (source='github', 'slack', etc.)
    - SYNTHETIC: Derived through reasoning (is_derived=True)

    Example:
        resolver = OwnershipResolver()
        category = resolver.determine(source="github")  # Returns FEDERATED
        resolution = resolver.resolve(source="github")  # Returns full OwnershipResolution
    """

    # Sources that indicate NATIVE ownership
    NATIVE_SOURCES = frozenset({"piper", "system", "internal", "memory"})

    # Sources that indicate FEDERATED ownership
    FEDERATED_SOURCES = frozenset(
        {
            "github",
            "slack",
            "notion",
            "calendar",
            "jira",
            "linear",
            "email",
        }
    )

    # Sources that indicate SYNTHETIC ownership
    SYNTHETIC_SOURCES = frozenset(
        {
            "inference",
            "analysis",
            "synthesis",
            "aggregation",
            "computation",
        }
    )

    def determine(
        self,
        source: str,
        created_by: Optional[str] = None,
        is_derived: bool = False,
        is_cached: bool = False,
    ) -> OwnershipCategory:
        """
        Determine ownership category based on source and attributes.

        Args:
            source: The origin of the object (e.g., 'piper', 'github')
            created_by: Who/what created the object (optional)
            is_derived: Whether this is a derived/computed object
            is_cached: Whether this is cached data from another source

        Returns:
            OwnershipCategory: The determined ownership category
        """
        # Derived objects are SYNTHETIC regardless of source
        if is_derived:
            return OwnershipCategory.SYNTHETIC

        source_lower = source.lower()

        # Check for NATIVE sources
        if source_lower in self.NATIVE_SOURCES:
            return OwnershipCategory.NATIVE

        # Created by Piper is NATIVE
        if created_by and created_by.lower() in self.NATIVE_SOURCES:
            return OwnershipCategory.NATIVE

        # Check for FEDERATED sources
        if source_lower in self.FEDERATED_SOURCES:
            return OwnershipCategory.FEDERATED

        # Check for SYNTHETIC sources
        if source_lower in self.SYNTHETIC_SOURCES:
            return OwnershipCategory.SYNTHETIC

        # Default to FEDERATED for unknown external sources
        return OwnershipCategory.FEDERATED

    def resolve(
        self,
        source: str,
        created_by: Optional[str] = None,
        is_derived: bool = False,
        is_cached: bool = False,
    ) -> OwnershipResolution:
        """
        Resolve ownership with full details including confidence and reasoning.

        Args:
            source: The origin of the object (e.g., 'piper', 'github')
            created_by: Who/what created the object (optional)
            is_derived: Whether this is a derived/computed object
            is_cached: Whether this is cached data from another source

        Returns:
            OwnershipResolution: Full resolution with category, confidence, reasoning
        """
        category = self.determine(source, created_by, is_derived, is_cached)
        reasoning = self._generate_reasoning(source, created_by, is_derived, is_cached, category)
        confidence = self._calculate_confidence(source, created_by, is_derived, category)

        return OwnershipResolution(
            category=category,
            confidence=confidence,
            reasoning=reasoning,
            source=source,
            is_derived=is_derived,
            is_cached=is_cached,
        )

    def _generate_reasoning(
        self,
        source: str,
        created_by: Optional[str],
        is_derived: bool,
        is_cached: bool,
        category: OwnershipCategory,
    ) -> str:
        """Generate human-readable reasoning for the determination."""
        source_lower = source.lower()

        if is_derived:
            return f"Object is derived/computed (is_derived=True), source='{source}'"

        if source_lower in self.NATIVE_SOURCES:
            return f"Source '{source}' is a native/internal Piper source"

        if created_by and created_by.lower() in self.NATIVE_SOURCES:
            return f"Created by '{created_by}' which is a native Piper source"

        if source_lower in self.FEDERATED_SOURCES:
            cached_note = " (cached)" if is_cached else ""
            return f"Source '{source}' is an external federated source{cached_note}"

        if source_lower in self.SYNTHETIC_SOURCES:
            return f"Source '{source}' indicates synthetic/computed origin"

        return f"Unknown source '{source}' defaulting to {category.value}"

    def _calculate_confidence(
        self,
        source: str,
        created_by: Optional[str],
        is_derived: bool,
        category: OwnershipCategory,
    ) -> float:
        """Calculate confidence score for the determination."""
        source_lower = source.lower()

        # High confidence for explicit source matches
        if source_lower in self.NATIVE_SOURCES:
            return 1.0
        if source_lower in self.FEDERATED_SOURCES:
            return 1.0
        if source_lower in self.SYNTHETIC_SOURCES:
            return 1.0

        # High confidence for derived
        if is_derived:
            return 0.95

        # Medium confidence for created_by matching
        if created_by and created_by.lower() in self.NATIVE_SOURCES:
            return 0.9

        # Lower confidence for unknown sources
        return 0.7


# Valid transformation paths (module-level constants for OwnershipTransformation)
# FEDERATED -> SYNTHETIC: Observation becomes understanding
# SYNTHETIC -> NATIVE: Understanding becomes memory
# FEDERATED -> NATIVE: Observation becomes memory (skipping synthesis)
_VALID_TRANSFORMATIONS: frozenset = frozenset(
    {
        (OwnershipCategory.FEDERATED, OwnershipCategory.SYNTHETIC),
        (OwnershipCategory.SYNTHETIC, OwnershipCategory.NATIVE),
        (OwnershipCategory.FEDERATED, OwnershipCategory.NATIVE),
    }
)

_TRANSFORMATION_DESCRIPTIONS: Dict[tuple, str] = {
    (OwnershipCategory.FEDERATED, OwnershipCategory.SYNTHETIC): (
        "Observation becomes understanding: Piper processes external data " "into derived insights"
    ),
    (OwnershipCategory.SYNTHETIC, OwnershipCategory.NATIVE): (
        "Understanding becomes memory: Piper commits synthesized " "understanding to internal state"
    ),
    (OwnershipCategory.FEDERATED, OwnershipCategory.NATIVE): (
        "Observation becomes memory: Piper directly captures external " "data as internal state"
    ),
}


@dataclass(frozen=True)
class OwnershipTransformation:
    """
    Represents a transformation between ownership categories.

    Tracks when Piper's relationship to an object changes:
    - FEDERATED -> SYNTHETIC: Observation becomes understanding
    - SYNTHETIC -> NATIVE: Understanding becomes memory
    - FEDERATED -> NATIVE: Observation becomes memory (rare)

    Some transformations are invalid:
    - NATIVE -> FEDERATED: Can't "un-create" something
    - Same category: No-op transformations

    Example:
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.FEDERATED,
            to_category=OwnershipCategory.SYNTHETIC
        )
        if transform.is_valid():
            print(transform.description)
    """

    from_category: OwnershipCategory
    to_category: OwnershipCategory
    reason: Optional[str] = None
    timestamp: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Check if this transformation follows valid ownership rules."""
        # Same category is not a valid transformation
        if self.from_category == self.to_category:
            return False

        return (self.from_category, self.to_category) in _VALID_TRANSFORMATIONS

    @property
    def description(self) -> str:
        """Get a human-readable description of this transformation."""
        key = (self.from_category, self.to_category)
        if key in _TRANSFORMATION_DESCRIPTIONS:
            return _TRANSFORMATION_DESCRIPTIONS[key]

        if not self.is_valid():
            return (
                f"Invalid transformation: {self.from_category.metaphor} "
                f"cannot become {self.to_category.metaphor}"
            )

        return f"{self.from_category.metaphor} transforms to " f"{self.to_category.metaphor}"

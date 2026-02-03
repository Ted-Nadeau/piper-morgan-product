"""
Metadata Schema for MUX Object Model.

"Metadata is what Piper knows about what it perceives."

The 6 universal dimensions provide a vocabulary for describing
knowledge about knowledge:

1. Provenance - Where did this data come from?
2. Relevance - How important is this?
3. AttentionState - Who has noticed this?
4. Confidence - How sure are we?
5. Relations - How does this connect?
6. Journal - What is the history?

These dimensions answer the meta-questions about any piece of information
that Piper perceives, enabling rich reasoning about the nature and
quality of knowledge.

Part of MUX-399-P4: Metadata Schema & Journal Extensions.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Protocol, runtime_checkable

# =============================================================================
# Dimension 1: Provenance - Where did this come from?
# =============================================================================


@dataclass
class Provenance:
    """
    Where did this data come from?

    Provenance answers "What is the source of this information?"
    with confidence about the source and freshness tracking.

    Attributes:
        source: Origin of the data (e.g., "github", "user", "derived")
        fetched_at: When the data was fetched/created
        confidence: How reliable is this source? (0-1)

    Example:
        p = Provenance(source="github", confidence=0.9)
        if p.freshness < 0.5:
            print("Data may be stale")
    """

    source: str
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confidence: float = 1.0  # Source confidence 0-1

    @property
    def freshness(self) -> float:
        """
        How fresh is this data? (0=stale, 1=fresh)

        Decays over 1 hour by default.
        """
        age_seconds = (datetime.now(timezone.utc) - self.fetched_at).total_seconds()
        decay_period = 3600  # 1 hour
        return max(0, 1 - (age_seconds / decay_period))


# =============================================================================
# Dimension 2: Relevance - How important is this?
# =============================================================================


@dataclass
class Relevance:
    """
    How important is this?

    Relevance answers "Why should I pay attention to this?"
    with score, contributing factors, and context.

    Attributes:
        score: Importance score (0-1)
        factors: What contributed to this score
        context: What this is relevant to
        decay_rate: How quickly relevance fades

    Example:
        r = Relevance(score=0.9, factors=["project_match", "urgent"], context="Project X")
    """

    score: float  # 0-1
    factors: List[str] = field(default_factory=list)
    context: str = ""
    decay_rate: float = 0.1  # How quickly relevance fades


# =============================================================================
# Dimension 3: AttentionState - Who has noticed this?
# =============================================================================


@dataclass
class AttentionState:
    """
    Who has noticed this?

    AttentionState answers "Has anyone seen this yet?"
    with tracking of who noticed and attention priority.

    Attributes:
        noticed_by: List of entity IDs who noticed
        noticed_at: When it was first noticed
        attention_level: Priority level (low, normal, high, urgent)

    Example:
        a = AttentionState(noticed_by=["user_123"], attention_level="urgent")
    """

    noticed_by: List[str] = field(default_factory=list)
    noticed_at: Optional[datetime] = None
    attention_level: str = "normal"  # low, normal, high, urgent


# =============================================================================
# Dimension 4: Confidence - How sure are we?
# =============================================================================


@dataclass
class Confidence:
    """
    How sure are we?

    Confidence answers "How certain is this information?"
    with score, basis for the confidence, and validation tracking.

    Attributes:
        score: Confidence score (0-1)
        basis: What is confidence based on
        last_validated: When was this last verified

    Example:
        c = Confidence(score=0.95, basis="direct observation")
    """

    score: float  # 0-1
    basis: str = ""  # What is confidence based on
    last_validated: Optional[datetime] = None


# =============================================================================
# Dimension 5: Relations - How does this connect?
# =============================================================================


class RelationType(str, Enum):
    """
    Types of relationships between objects.

    These relationship types express how entities, moments, and places
    connect to each other in the object graph.
    """

    REFERENCES = "references"
    BLOCKS = "blocks"
    CONTAINS = "contains"
    DERIVES_FROM = "derives_from"
    RELATED_TO = "related_to"
    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"


@dataclass
class Relation:
    """
    Connection to another object.

    Relations answer "How does this connect to other things?"
    with typed, weighted relationships.

    Attributes:
        target_id: ID of the target object
        relation_type: Type of relationship
        strength: How strong is this connection (0-1)
        bidirectional: Does this go both ways?

    Example:
        r = Relation(target_id="task_456", relation_type=RelationType.BLOCKS)
    """

    target_id: str
    relation_type: RelationType
    strength: float = 1.0  # 0-1
    bidirectional: bool = False


# =============================================================================
# Dimension 6: Journal - What is the history?
# =============================================================================


@dataclass
class JournalEntry:
    """Base journal entry with timestamp and content."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    content: str = ""
    actor: str = "system"


@dataclass
class SessionJournalEntry(JournalEntry):
    """
    Audit trail - what happened (objective, factual).

    Session journal captures events: what happened, when, why.
    This is the factual record of changes and actions.

    Attributes:
        event_type: Type of event (created, updated, completed, etc.)
        trigger: What triggered this event
        content: Description of what happened
        actor: Who performed the action

    Example:
        e = SessionJournalEntry(
            event_type="completed",
            content="Task marked done",
            trigger="user_action"
        )
    """

    event_type: str = ""
    trigger: str = ""


@dataclass
class InsightJournalEntry(JournalEntry):
    """
    Meaning extraction - what it meant (interpretive).

    Insight journal captures learnings and connected insights.
    This is where Piper records what it learned from events.

    Attributes:
        learning: The insight or learning extracted
        connected_insights: Links to related insights

    Example:
        i = InsightJournalEntry(
            learning="User prefers morning standups",
            connected_insights=["insight_work_patterns"]
        )
    """

    learning: str = ""
    connected_insights: List[str] = field(default_factory=list)


@dataclass
class Journal:
    """
    Two-layer journal: Session (audit) + Insight (meaning).

    The journal tells the story of an object's life through
    both factual events and extracted meaning.

    Attributes:
        session_entries: Audit trail of events
        insight_entries: Extracted learnings

    Example:
        j = Journal()
        j.session_entries.append(SessionJournalEntry(event_type="created"))
        j.insight_entries.append(InsightJournalEntry(learning="Important pattern"))
    """

    session_entries: List[SessionJournalEntry] = field(default_factory=list)
    insight_entries: List[InsightJournalEntry] = field(default_factory=list)


# =============================================================================
# HasMetadata Protocol
# =============================================================================


@runtime_checkable
class HasMetadata(Protocol):
    """
    Protocol for objects with metadata awareness.

    All dimensions are optional - objects declare what metadata
    they carry. Not all objects need all dimensions.

    "Metadata is what Piper knows about what it perceives."

    Any object that implements the 6 dimension properties
    can participate in metadata-aware operations.
    """

    @property
    def provenance(self) -> Optional[Provenance]:
        """Where did this come from?"""
        ...

    @property
    def relevance(self) -> Optional[Relevance]:
        """How important is this?"""
        ...

    @property
    def attention_state(self) -> Optional[AttentionState]:
        """Who has noticed this?"""
        ...

    @property
    def confidence(self) -> Optional[Confidence]:
        """How sure are we?"""
        ...

    @property
    def relations(self) -> Optional[List[Relation]]:
        """How does this connect to other objects?"""
        ...

    @property
    def journal(self) -> Optional[Journal]:
        """What is the history?"""
        ...


# =============================================================================
# Utility: ProvenanceTracker
# =============================================================================


class ProvenanceTracker:
    """
    Records where data comes from.

    Utility for creating provenance metadata from different sources.
    Different source types have different default confidence levels.

    Usage:
        # From an integration
        p = ProvenanceTracker.from_integration("github")

        # From user input (highest trust)
        p = ProvenanceTracker.from_user_input()

        # From inference (lower trust)
        p = ProvenanceTracker.from_inference()
    """

    @staticmethod
    def from_integration(integration_name: str, confidence: float = 0.9) -> Provenance:
        """Create provenance from integration fetch."""
        return Provenance(
            source=integration_name, confidence=confidence, fetched_at=datetime.now(timezone.utc)
        )

    @staticmethod
    def from_user_input() -> Provenance:
        """Create provenance for user-provided data (highest confidence)."""
        return Provenance(source="user", confidence=1.0)

    @staticmethod
    def from_inference(source_data: str = "derived") -> Provenance:
        """Create provenance for inferred/computed data."""
        return Provenance(source=source_data, confidence=0.7)


# =============================================================================
# Utility: ConfidenceCalculator
# =============================================================================


class ConfidenceCalculator:
    """
    Calculates confidence scores with basis tracking.

    Utility for computing confidence based on observation type
    and source reliability.

    Usage:
        # From direct observation
        c = ConfidenceCalculator.from_observation(direct=True)

        # From source reliability
        c = ConfidenceCalculator.from_source_reliability(0.85)
    """

    @staticmethod
    def from_observation(direct: bool = True) -> Confidence:
        """Calculate confidence from observation type."""
        return Confidence(
            score=0.95 if direct else 0.7,
            basis="direct observation" if direct else "inference",
            last_validated=datetime.now(timezone.utc),
        )

    @staticmethod
    def from_source_reliability(reliability: float) -> Confidence:
        """Calculate confidence from source reliability."""
        return Confidence(
            score=reliability,
            basis=f"source reliability ({reliability:.0%})",
            last_validated=datetime.now(timezone.utc),
        )


# =============================================================================
# Utility: RelationRegistry
# =============================================================================


class RelationRegistry:
    """
    Manages typed relationships between objects.

    Central registry for tracking how objects connect to each other.
    Supports bidirectional relations and filtering by type.

    Usage:
        registry = RelationRegistry()
        registry.add("task_1", Relation(target_id="task_2", relation_type=RelationType.BLOCKS))
        blockers = registry.get_relations("task_1", relation_type=RelationType.BLOCKS)
    """

    def __init__(self):
        self._relations: Dict[str, List[Relation]] = {}

    def add(self, source_id: str, relation: Relation) -> None:
        """Add a relation from source to target."""
        if source_id not in self._relations:
            self._relations[source_id] = []
        self._relations[source_id].append(relation)

        if relation.bidirectional:
            # Create inverse relation
            inverse = Relation(
                target_id=source_id,
                relation_type=RelationType.RELATED_TO,  # Use generic for inverse
                strength=relation.strength,
                bidirectional=False,  # Don't recurse
            )
            if relation.target_id not in self._relations:
                self._relations[relation.target_id] = []
            self._relations[relation.target_id].append(inverse)

    def get_relations(
        self, object_id: str, relation_type: Optional[RelationType] = None
    ) -> List[Relation]:
        """Get all relations for an object, optionally filtered by type."""
        relations = self._relations.get(object_id, [])
        if relation_type is not None:
            return [r for r in relations if r.relation_type == relation_type]
        return relations

    def remove(self, source_id: str, target_id: str) -> None:
        """Remove relation(s) from source to target."""
        if source_id in self._relations:
            self._relations[source_id] = [
                r for r in self._relations[source_id] if r.target_id != target_id
            ]


# =============================================================================
# Utility: JournalManager
# =============================================================================


class JournalManager:
    """
    Coordinates session and insight journal layers.

    The journal manager provides a unified interface for recording
    both the audit trail (session) and extracted meaning (insight).

    Usage:
        manager = JournalManager()

        # Log factual events
        manager.log_session_event("obj_123", "created", "Task was created")

        # Extract insights
        manager.extract_insight("obj_123", "User prefers async communication")

        # Get full history
        journal = manager.get_journal("obj_123")
    """

    def __init__(self):
        self._journals: Dict[str, Journal] = {}

    def log_session_event(
        self,
        object_id: str,
        event_type: str,
        content: str,
        trigger: str = "",
        actor: str = "system",
    ) -> SessionJournalEntry:
        """
        Log an audit trail event.

        Session journal captures: what happened, when, what triggered it.
        """
        entry = SessionJournalEntry(
            event_type=event_type, content=content, trigger=trigger, actor=actor
        )
        self._get_or_create_journal(object_id).session_entries.append(entry)
        return entry

    def extract_insight(
        self,
        object_id: str,
        learning: str,
        content: str = "",
        connected_insights: Optional[List[str]] = None,
        actor: str = "system",
    ) -> InsightJournalEntry:
        """
        Extract and record an insight.

        Insight journal captures: what it meant, what we learned.
        """
        entry = InsightJournalEntry(
            learning=learning,
            content=content,
            connected_insights=connected_insights or [],
            actor=actor,
        )
        self._get_or_create_journal(object_id).insight_entries.append(entry)
        return entry

    def get_journal(self, object_id: str) -> Journal:
        """Get full journal for an object."""
        return self._get_or_create_journal(object_id)

    def _get_or_create_journal(self, object_id: str) -> Journal:
        if object_id not in self._journals:
            self._journals[object_id] = Journal()
        return self._journals[object_id]

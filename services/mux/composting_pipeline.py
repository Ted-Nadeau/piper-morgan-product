"""
Composting pipeline - wires Extractor to InsightJournal with typed learnings.

Part of #667 COMPOSTING-PIPELINE (child of #436 MUX-TECH-PHASE4-COMPOSTING).

This module provides:
- SurfaceableInsight: Enhanced entry with surfacing control
- InsightJournal: Query interface for surfacing
- CompostingPipeline: Orchestrates extraction and storage

Flow:
  CompostBin (#666) → Pipeline → InsightJournal → Surfacing (#415)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .composting_models import (
    CompostingTrigger,
    ExtractedLearning,
    create_correction_learning,
    create_insight_learning,
    create_pattern_learning,
)
from .lifecycle import CompostingExtractor, CompostResult, LifecycleState

# =============================================================================
# SurfaceableInsight - Enhanced Entry with Surfacing Control
# =============================================================================


@dataclass
class SurfaceableInsight:
    """
    An insight ready for surfacing to the user.

    Extends the base InsightJournalEntry concept with:
    - Typed ExtractedLearning instead of string
    - Surfacing control fields
    - Trust-based visibility
    - User response tracking

    This is the model that #415 PREMONITION queries to
    determine what insights to surface and when.
    """

    # Identity
    id: str = field(default_factory=lambda: str(uuid4()))
    object_id: str = ""  # What was composted
    user_id: str = ""  # Who this insight belongs to
    created_at: datetime = field(default_factory=datetime.now)

    # The learning (typed, not just str)
    learning: Optional[ExtractedLearning] = None

    # Surfacing control
    surfaced_count: int = 0
    last_surfaced: Optional[datetime] = None
    user_response: Optional[str] = None  # "engaged", "dismissed", "corrected"

    # Trust-based visibility (Stage 1-4 per trust model)
    min_trust_stage: int = 1  # 1=all can see, 3=push eligible, 4=proactive

    # Relevance tracking
    connected_insights: List[str] = field(default_factory=list)
    context_tags: List[str] = field(default_factory=list)

    def is_surfaceable(self, trust_stage: int) -> bool:
        """
        Check if this insight can be surfaced at given trust level.

        Args:
            trust_stage: Current trust stage (1-4)

        Returns:
            True if insight can be surfaced
        """
        # Must meet minimum trust
        if trust_stage < self.min_trust_stage:
            return False

        # Don't resurface recently surfaced
        if self.last_surfaced is not None:
            hours_since = (datetime.now() - self.last_surfaced).total_seconds() / 3600
            if hours_since < 24:  # 24 hour cooldown
                return False

        # Don't resurface dismissed insights
        if self.user_response == "dismissed":
            return False

        return True

    @property
    def is_high_confidence(self) -> bool:
        """Check if the underlying learning is high confidence."""
        if self.learning is None:
            return False
        return self.learning.is_high_confidence

    @property
    def requires_attention(self) -> bool:
        """Check if this insight requires user attention."""
        if self.learning is None:
            return False
        return self.learning.requires_attention

    @property
    def learning_type(self) -> str:
        """Get the type of learning."""
        if self.learning is None:
            return "unknown"
        return self.learning.learning_type

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "object_id": self.object_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "learning": self.learning.to_dict() if self.learning else None,
            "surfaced_count": self.surfaced_count,
            "last_surfaced": (self.last_surfaced.isoformat() if self.last_surfaced else None),
            "user_response": self.user_response,
            "min_trust_stage": self.min_trust_stage,
            "connected_insights": self.connected_insights,
            "context_tags": self.context_tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SurfaceableInsight":
        """Create from dictionary."""
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            created_at = datetime.now()

        last_surfaced = data.get("last_surfaced")
        if isinstance(last_surfaced, str):
            last_surfaced = datetime.fromisoformat(last_surfaced)

        learning = None
        learning_data = data.get("learning")
        if learning_data:
            learning = ExtractedLearning.from_dict(learning_data)

        return cls(
            id=data.get("id", str(uuid4())),
            object_id=data.get("object_id", ""),
            user_id=data.get("user_id", ""),
            created_at=created_at,
            learning=learning,
            surfaced_count=data.get("surfaced_count", 0),
            last_surfaced=last_surfaced,
            user_response=data.get("user_response"),
            min_trust_stage=data.get("min_trust_stage", 1),
            connected_insights=data.get("connected_insights", []),
            context_tags=data.get("context_tags", []),
        )


# =============================================================================
# InsightJournal - Query Interface for Surfacing
# =============================================================================


class InsightJournal:
    """
    Query interface for surfaceable insights.

    This is the data store that #415 PREMONITION queries to
    find insights eligible for surfacing based on context,
    confidence, and trust level.

    Note: Uses in-memory storage for now. Can be backed by
    database in production (repository pattern).
    """

    def __init__(self):
        """Initialize with empty storage."""
        self._insights: Dict[str, SurfaceableInsight] = {}
        self._by_user: Dict[str, List[str]] = {}  # user_id -> insight_ids
        self._by_object: Dict[str, List[str]] = {}  # object_id -> insight_ids

    def add(self, insight: SurfaceableInsight) -> SurfaceableInsight:
        """
        Add an insight to the journal.

        Args:
            insight: The insight to store

        Returns:
            The stored insight
        """
        self._insights[insight.id] = insight

        # Index by user
        if insight.user_id:
            if insight.user_id not in self._by_user:
                self._by_user[insight.user_id] = []
            self._by_user[insight.user_id].append(insight.id)

        # Index by object
        if insight.object_id:
            if insight.object_id not in self._by_object:
                self._by_object[insight.object_id] = []
            self._by_object[insight.object_id].append(insight.id)

        return insight

    def get(self, insight_id: str) -> Optional[SurfaceableInsight]:
        """Get insight by ID."""
        return self._insights.get(insight_id)

    async def get_unsurfaced(
        self,
        user_id: str,
        min_confidence: float = 0.75,
        trust_stage: int = 3,
        limit: int = 10,
    ) -> List[SurfaceableInsight]:
        """
        Get insights eligible for push surfacing.

        Args:
            user_id: User to get insights for
            min_confidence: Minimum confidence threshold (default 0.75)
            trust_stage: Current trust stage (default 3 for push eligible)
            limit: Maximum results to return

        Returns:
            List of surfaceable insights
        """
        if user_id not in self._by_user:
            return []

        results = []
        for insight_id in self._by_user[user_id]:
            insight = self._insights.get(insight_id)
            if insight is None:
                continue

            # Check surfaceability
            if not insight.is_surfaceable(trust_stage):
                continue

            # Check confidence
            if insight.learning and insight.learning.confidence < min_confidence:
                continue

            # Check not already surfaced
            if insight.surfaced_count == 0:
                results.append(insight)

            if len(results) >= limit:
                break

        # Sort by confidence (highest first), then requires_attention
        results.sort(
            key=lambda i: (
                i.requires_attention,  # Attention items first
                i.learning.confidence if i.learning else 0,
            ),
            reverse=True,
        )

        return results[:limit]

    async def get_for_context(
        self,
        user_id: str,
        context_entities: Optional[List[str]] = None,
        context_topics: Optional[List[str]] = None,
        trust_stage: int = 1,
        limit: int = 5,
    ) -> List[SurfaceableInsight]:
        """
        Get insights relevant to current context.

        Used for pull-based surfacing where user context
        determines what insights are relevant.

        Args:
            user_id: User to get insights for
            context_entities: Entities in current context
            context_topics: Topics in current context
            trust_stage: Current trust stage
            limit: Maximum results

        Returns:
            List of contextually relevant insights
        """
        if user_id not in self._by_user:
            return []

        context_entities = context_entities or []
        context_topics = context_topics or []

        # Convert to sets for faster lookup
        entity_set = set(context_entities)
        topic_set = set(context_topics)

        results = []
        for insight_id in self._by_user[user_id]:
            insight = self._insights.get(insight_id)
            if insight is None:
                continue

            if not insight.is_surfaceable(trust_stage):
                continue

            # Score relevance
            relevance = 0

            # Check entity overlap
            if insight.learning:
                for entity in insight.learning.applies_to_entities:
                    if entity in entity_set:
                        relevance += 2

                # Check topic overlap
                for tag in insight.learning.topic_tags:
                    if tag in topic_set:
                        relevance += 1

            # Also check context_tags
            for tag in insight.context_tags:
                if tag in entity_set or tag in topic_set:
                    relevance += 1

            if relevance > 0:
                results.append((relevance, insight))

        # Sort by relevance, then confidence
        results.sort(
            key=lambda x: (
                x[0],  # Relevance
                x[1].learning.confidence if x[1].learning else 0,
            ),
            reverse=True,
        )

        return [r[1] for r in results[:limit]]

    async def mark_surfaced(
        self,
        insight_id: str,
        response: str,
    ) -> Optional[SurfaceableInsight]:
        """
        Record that insight was surfaced and user's response.

        Args:
            insight_id: ID of the surfaced insight
            response: User response ("engaged", "dismissed", "corrected")

        Returns:
            Updated insight, or None if not found
        """
        insight = self._insights.get(insight_id)
        if insight is None:
            return None

        insight.surfaced_count += 1
        insight.last_surfaced = datetime.now()
        insight.user_response = response

        return insight

    def get_for_object(self, object_id: str) -> List[SurfaceableInsight]:
        """Get all insights for a specific object."""
        if object_id not in self._by_object:
            return []

        return [self._insights[iid] for iid in self._by_object[object_id] if iid in self._insights]

    @property
    def count(self) -> int:
        """Total number of insights."""
        return len(self._insights)

    def clear(self) -> int:
        """Clear all insights. Returns count cleared."""
        count = len(self._insights)
        self._insights = {}
        self._by_user = {}
        self._by_object = {}
        return count


# =============================================================================
# CompostingPipeline - Orchestrates Extraction and Storage
# =============================================================================


class CompostingPipeline:
    """
    Orchestrates extraction and journal storage.

    Takes objects from CompostBin, extracts learnings using
    CompostingExtractor, and stores as SurfaceableInsights
    in the InsightJournal.

    Example:
        pipeline = CompostingPipeline(
            extractor=CompostingExtractor(),
            journal=InsightJournal(),
        )

        learnings = await pipeline.process(old_task, user_id="user-123")
        # Now insights are in journal, ready for #415 to surface
    """

    def __init__(
        self,
        extractor: Optional[CompostingExtractor] = None,
        journal: Optional[InsightJournal] = None,
    ):
        """
        Initialize pipeline.

        Args:
            extractor: CompostingExtractor instance (creates default if None)
            journal: InsightJournal instance (creates default if None)
        """
        self.extractor = extractor or CompostingExtractor()
        self.journal = journal or InsightJournal()

    async def process(
        self,
        obj: Any,
        user_id: str = "",
        trigger: Optional[CompostingTrigger] = None,
    ) -> List[ExtractedLearning]:
        """
        Extract learnings from object and store in journal.

        Args:
            obj: Object to compost
            user_id: User ID to associate with learnings
            trigger: What triggered composting (for context)

        Returns:
            List of ExtractedLearning objects created
        """
        # Extract using existing extractor
        result = self.extractor.extract(obj)

        # Convert to typed learnings
        learnings = self._to_extracted_learnings(result, obj)

        # Store each learning as surfaceable insight
        object_id = getattr(obj, "id", str(id(obj)))

        for learning in learnings:
            insight = SurfaceableInsight(
                object_id=object_id,
                user_id=user_id,
                learning=learning,
                min_trust_stage=self._determine_trust_stage(learning),
                context_tags=learning.topic_tags.copy(),
            )
            self.journal.add(insight)

        return learnings

    def _to_extracted_learnings(
        self,
        result: CompostResult,
        obj: Any,
    ) -> List[ExtractedLearning]:
        """
        Convert CompostResult to typed ExtractedLearning objects.

        Analyzes lessons and journey to create appropriate
        Pattern, Insight, or Correction learnings.
        """
        learnings = []
        object_id = result.object_summary.get("id", str(id(obj)))

        # Calculate base confidence from journey
        base_confidence = self._calculate_confidence(result.journey)

        # Extract topic tags from summary
        topic_tags = self._extract_topic_tags(result.object_summary)

        for lesson in result.lessons:
            learning = self._lesson_to_learning(
                lesson=lesson,
                source_objects=[object_id],
                confidence=base_confidence,
                topic_tags=topic_tags,
                journey=result.journey,
            )
            learnings.append(learning)

        return learnings

    def _lesson_to_learning(
        self,
        lesson: str,
        source_objects: List[str],
        confidence: float,
        topic_tags: List[str],
        journey: List[LifecycleState],
    ) -> ExtractedLearning:
        """
        Convert a lesson string to typed ExtractedLearning.

        Analyzes the lesson text to determine if it's a
        pattern, insight, or correction.
        """
        lesson_lower = lesson.lower()

        # Check for correction signals
        if any(
            signal in lesson_lower
            for signal in ["wrong", "incorrect", "not", "actually", "instead"]
        ):
            return create_correction_learning(
                previous_understanding="Previous assumption",
                new_understanding=lesson,
                evidence=source_objects,
                confidence=confidence,
                source_objects=source_objects,
                topic_tags=topic_tags,
            )

        # Check for pattern signals
        if any(
            signal in lesson_lower
            for signal in [
                "pattern",
                "recurring",
                "repeated",
                "always",
                "usually",
                "often",
            ]
        ):
            return create_pattern_learning(
                description=lesson,
                occurrences=source_objects,
                frequency=0.5,  # Unknown frequency
                predictive_power=confidence,
                source_objects=source_objects,
                confidence=confidence,
                topic_tags=topic_tags,
            )

        # Default to insight
        return create_insight_learning(
            description=lesson,
            derived_from=source_objects,
            confidence=confidence,
            surprisingness=self._calculate_surprisingness(journey),
            source_objects=source_objects,
            topic_tags=topic_tags,
        )

    def _calculate_confidence(self, journey: List[LifecycleState]) -> float:
        """
        Calculate confidence based on lifecycle journey.

        Longer journeys through more states = more confident.
        Reaching RATIFIED = boost.
        """
        if not journey:
            return 0.5

        base = 0.5

        # Longer journey = more confident
        journey_bonus = min(len(journey) * 0.05, 0.25)

        # Ratified = validated
        if LifecycleState.RATIFIED in journey:
            ratified_bonus = 0.15
        else:
            ratified_bonus = 0

        return min(base + journey_bonus + ratified_bonus, 1.0)

    def _calculate_surprisingness(self, journey: List[LifecycleState]) -> float:
        """
        Calculate how surprising the insight is.

        Unusual journeys (skipping states, quick deprecation) = surprising.
        """
        if not journey:
            return 0.0

        surprisingness = 0.0

        # Short journey = somewhat surprising
        if len(journey) <= 2:
            surprisingness += 0.3

        # Skipped derivation = surprising
        if (
            LifecycleState.EMERGENT in journey
            and LifecycleState.NOTICED in journey
            and LifecycleState.DERIVED not in journey
        ):
            surprisingness += 0.2

        return min(surprisingness, 1.0)

    def _extract_topic_tags(self, summary: Dict[str, Any]) -> List[str]:
        """Extract topic tags from object summary."""
        tags = []

        # Use type/category if available
        if "type" in summary:
            tags.append(str(summary["type"]).lower())
        if "category" in summary:
            tags.append(str(summary["category"]).lower())

        return tags

    def _determine_trust_stage(self, learning: ExtractedLearning) -> int:
        """
        Determine minimum trust stage for surfacing.

        Corrections require higher trust (stage 3).
        High confidence can be pushed (stage 3).
        Others start at stage 1.
        """
        # Corrections need high trust
        if learning.learning_type == "correction":
            return 3

        # High confidence can be pushed
        if learning.is_high_confidence:
            return 2

        # Default to pull-only
        return 1

"""
Tests for CompostingPipeline - wires Extractor to InsightJournal.

Part of #667 COMPOSTING-PIPELINE (child of #436 MUX-TECH-PHASE4-COMPOSTING).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

import pytest

from services.mux.composting_models import (
    CompostingTrigger,
    ExtractedLearning,
    create_insight_learning,
)
from services.mux.composting_pipeline import CompostingPipeline, InsightJournal, SurfaceableInsight
from services.mux.lifecycle import LifecycleState

# =============================================================================
# Test Fixtures
# =============================================================================


@dataclass
class MockObjectWithLifecycle:
    """Mock object for testing."""

    id: str
    title: str
    created_at: datetime = field(default_factory=datetime.now)
    lifecycle_state: LifecycleState = LifecycleState.EMERGENT
    lifecycle_history: List = field(default_factory=list)


# =============================================================================
# SurfaceableInsight Tests
# =============================================================================


class TestSurfaceableInsight:
    """Tests for SurfaceableInsight model."""

    def test_basic_creation(self):
        """Test basic insight creation."""
        insight = SurfaceableInsight(
            object_id="obj-123",
            user_id="user-456",
        )
        assert insight.id is not None
        assert insight.object_id == "obj-123"
        assert insight.user_id == "user-456"
        assert insight.surfaced_count == 0

    def test_with_learning(self):
        """Test insight with ExtractedLearning."""
        learning = create_insight_learning(
            description="User prefers mornings",
            derived_from=["pattern-1"],
            confidence=0.8,
        )
        insight = SurfaceableInsight(
            object_id="obj-123",
            learning=learning,
        )
        assert insight.learning is not None
        assert insight.learning_type == "insight"
        assert insight.is_high_confidence is True  # 0.8 >= 0.75

    def test_is_surfaceable_with_trust(self):
        """Test surfaceability check with trust levels."""
        insight = SurfaceableInsight(
            min_trust_stage=3,
        )

        # Below trust threshold
        assert insight.is_surfaceable(trust_stage=1) is False
        assert insight.is_surfaceable(trust_stage=2) is False

        # At or above threshold
        assert insight.is_surfaceable(trust_stage=3) is True
        assert insight.is_surfaceable(trust_stage=4) is True

    def test_is_surfaceable_cooldown(self):
        """Test that recently surfaced insights have cooldown."""
        insight = SurfaceableInsight(
            last_surfaced=datetime.now(),  # Just surfaced
        )

        # Should not be surfaceable due to 24h cooldown
        assert insight.is_surfaceable(trust_stage=4) is False

    def test_is_surfaceable_dismissed(self):
        """Test that dismissed insights are not surfaceable."""
        insight = SurfaceableInsight(
            user_response="dismissed",
        )

        assert insight.is_surfaceable(trust_stage=4) is False

    def test_to_dict_and_from_dict(self):
        """Test serialization roundtrip."""
        learning = create_insight_learning(
            description="Test insight",
            derived_from=[],
            confidence=0.7,
        )
        original = SurfaceableInsight(
            object_id="obj-1",
            user_id="user-1",
            learning=learning,
            min_trust_stage=2,
            context_tags=["scheduling"],
        )

        restored = SurfaceableInsight.from_dict(original.to_dict())

        assert restored.object_id == original.object_id
        assert restored.user_id == original.user_id
        assert restored.min_trust_stage == original.min_trust_stage
        assert restored.context_tags == original.context_tags
        assert restored.learning is not None
        assert restored.learning.description == "Test insight"


# =============================================================================
# InsightJournal Tests
# =============================================================================


class TestInsightJournal:
    """Tests for InsightJournal query interface."""

    def test_add_and_get(self):
        """Test adding and retrieving insights."""
        journal = InsightJournal()

        insight = SurfaceableInsight(
            id="insight-1",
            object_id="obj-1",
            user_id="user-1",
        )
        journal.add(insight)

        retrieved = journal.get("insight-1")
        assert retrieved is not None
        assert retrieved.object_id == "obj-1"

    def test_count(self):
        """Test insight count."""
        journal = InsightJournal()

        assert journal.count == 0

        journal.add(SurfaceableInsight(id="i1"))
        journal.add(SurfaceableInsight(id="i2"))
        journal.add(SurfaceableInsight(id="i3"))

        assert journal.count == 3

    def test_clear(self):
        """Test clearing all insights."""
        journal = InsightJournal()
        journal.add(SurfaceableInsight(id="i1"))
        journal.add(SurfaceableInsight(id="i2"))

        cleared = journal.clear()

        assert cleared == 2
        assert journal.count == 0

    @pytest.mark.asyncio
    async def test_get_unsurfaced(self):
        """Test getting unsurfaced insights for a user."""
        journal = InsightJournal()

        # Add insights with varying properties
        high_confidence = SurfaceableInsight(
            id="high",
            user_id="user-1",
            learning=create_insight_learning(
                description="High confidence",
                derived_from=[],
                confidence=0.9,
            ),
        )
        low_confidence = SurfaceableInsight(
            id="low",
            user_id="user-1",
            learning=create_insight_learning(
                description="Low confidence",
                derived_from=[],
                confidence=0.5,
            ),
        )
        already_surfaced = SurfaceableInsight(
            id="surfaced",
            user_id="user-1",
            learning=create_insight_learning(
                description="Already surfaced",
                derived_from=[],
                confidence=0.9,
            ),
            surfaced_count=1,
        )

        journal.add(high_confidence)
        journal.add(low_confidence)
        journal.add(already_surfaced)

        # Get unsurfaced with default min_confidence=0.75
        results = await journal.get_unsurfaced(
            user_id="user-1",
            min_confidence=0.75,
        )

        # Should only get high confidence, unsurfaced
        assert len(results) == 1
        assert results[0].id == "high"

    @pytest.mark.asyncio
    async def test_get_unsurfaced_respects_trust(self):
        """Test that get_unsurfaced respects trust levels."""
        journal = InsightJournal()

        insight = SurfaceableInsight(
            id="high-trust",
            user_id="user-1",
            min_trust_stage=3,
            learning=create_insight_learning(
                description="Needs high trust",
                derived_from=[],
                confidence=0.9,
            ),
        )
        journal.add(insight)

        # Low trust stage - should not find
        results = await journal.get_unsurfaced(
            user_id="user-1",
            trust_stage=2,
        )
        assert len(results) == 0

        # High trust stage - should find
        results = await journal.get_unsurfaced(
            user_id="user-1",
            trust_stage=3,
        )
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_get_for_context(self):
        """Test context-based insight retrieval."""
        journal = InsightJournal()

        # Insight about scheduling
        scheduling_insight = SurfaceableInsight(
            id="scheduling",
            user_id="user-1",
            learning=create_insight_learning(
                description="Morning meetings preferred",
                derived_from=[],
                confidence=0.8,
            ),
        )
        scheduling_insight.learning.topic_tags = ["scheduling", "meetings"]
        scheduling_insight.learning.applies_to_entities = ["calendar"]

        # Insight about communication
        comms_insight = SurfaceableInsight(
            id="comms",
            user_id="user-1",
            learning=create_insight_learning(
                description="Prefers Slack",
                derived_from=[],
                confidence=0.8,
            ),
        )
        comms_insight.learning.topic_tags = ["communication"]
        comms_insight.learning.applies_to_entities = ["slack"]

        journal.add(scheduling_insight)
        journal.add(comms_insight)

        # Query for scheduling context
        results = await journal.get_for_context(
            user_id="user-1",
            context_entities=["calendar"],
            context_topics=["meetings"],
        )

        # Should find scheduling insight (matches both entity and topic)
        assert len(results) >= 1
        assert results[0].id == "scheduling"

    @pytest.mark.asyncio
    async def test_mark_surfaced(self):
        """Test marking an insight as surfaced."""
        journal = InsightJournal()

        insight = SurfaceableInsight(
            id="insight-1",
            user_id="user-1",
        )
        journal.add(insight)

        # Mark surfaced with user response
        updated = await journal.mark_surfaced("insight-1", "engaged")

        assert updated is not None
        assert updated.surfaced_count == 1
        assert updated.last_surfaced is not None
        assert updated.user_response == "engaged"

    def test_get_for_object(self):
        """Test getting insights for a specific object."""
        journal = InsightJournal()

        journal.add(SurfaceableInsight(id="i1", object_id="obj-1"))
        journal.add(SurfaceableInsight(id="i2", object_id="obj-1"))
        journal.add(SurfaceableInsight(id="i3", object_id="obj-2"))

        results = journal.get_for_object("obj-1")

        assert len(results) == 2
        assert all(i.object_id == "obj-1" for i in results)


# =============================================================================
# CompostingPipeline Tests
# =============================================================================


class TestCompostingPipeline:
    """Tests for CompostingPipeline orchestration."""

    def test_creation_with_defaults(self):
        """Test pipeline creation with default components."""
        pipeline = CompostingPipeline()

        assert pipeline.extractor is not None
        assert pipeline.journal is not None

    @pytest.mark.asyncio
    async def test_process_simple_object(self):
        """Test processing a simple object."""
        pipeline = CompostingPipeline()

        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Test Task",
            lifecycle_state=LifecycleState.ARCHIVED,
        )

        learnings = await pipeline.process(obj, user_id="user-1")

        # Should extract at least one learning
        assert len(learnings) >= 1

        # Should store in journal
        assert pipeline.journal.count >= 1

    @pytest.mark.asyncio
    async def test_process_stores_with_user_id(self):
        """Test that processed insights are stored with user_id."""
        pipeline = CompostingPipeline()

        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Test",
        )

        await pipeline.process(obj, user_id="user-123")

        insights = pipeline.journal.get_for_object("task-1")
        assert len(insights) >= 1
        assert all(i.user_id == "user-123" for i in insights)

    @pytest.mark.asyncio
    async def test_process_calculates_confidence(self):
        """Test that confidence is calculated from journey."""
        from services.mux.lifecycle import LifecycleTransition

        pipeline = CompostingPipeline()

        # Object with long journey including RATIFIED
        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Well-traveled",
            lifecycle_state=LifecycleState.ARCHIVED,
            lifecycle_history=[
                LifecycleTransition(
                    from_state=LifecycleState.EMERGENT,
                    to_state=LifecycleState.DERIVED,
                ),
                LifecycleTransition(
                    from_state=LifecycleState.DERIVED,
                    to_state=LifecycleState.NOTICED,
                ),
                LifecycleTransition(
                    from_state=LifecycleState.NOTICED,
                    to_state=LifecycleState.PROPOSED,
                ),
                LifecycleTransition(
                    from_state=LifecycleState.PROPOSED,
                    to_state=LifecycleState.RATIFIED,
                ),
            ],
        )

        learnings = await pipeline.process(obj, user_id="user-1")

        # With RATIFIED in journey, confidence should be boosted
        assert len(learnings) >= 1
        # Confidence should be higher due to journey + RATIFIED bonus
        assert learnings[0].confidence >= 0.7

    @pytest.mark.asyncio
    async def test_process_extracts_topic_tags(self):
        """Test that topic tags are extracted from object summary."""
        pipeline = CompostingPipeline()

        obj = MockObjectWithLifecycle(
            id="task-1",
            title="Test",
        )
        # Add type for topic extraction
        obj.type = "feature"
        obj.category = "planning"

        learnings = await pipeline.process(obj, user_id="user-1")

        # Should have extracted topic tags
        assert len(learnings) >= 1


class TestCompostingPipelineLessonClassification:
    """Tests for lesson to learning type classification."""

    @pytest.mark.asyncio
    async def test_correction_detection(self):
        """Test that correction signals create Correction learnings."""
        pipeline = CompostingPipeline()

        # Create mock result with correction-like lesson
        from services.mux.lifecycle import CompostResult

        mock_result = CompostResult(
            object_summary={"id": "obj-1"},
            journey=[LifecycleState.EMERGENT],
            lessons=["This was wrong - user actually prefers afternoon meetings"],
            composted_at=datetime.now(),
        )

        learnings = pipeline._to_extracted_learnings(mock_result, None)

        assert len(learnings) == 1
        assert learnings[0].learning_type == "correction"

    @pytest.mark.asyncio
    async def test_pattern_detection(self):
        """Test that pattern signals create Pattern learnings."""
        pipeline = CompostingPipeline()

        from services.mux.lifecycle import CompostResult

        mock_result = CompostResult(
            object_summary={"id": "obj-1"},
            journey=[LifecycleState.EMERGENT],
            lessons=["This object completed a full lifecycle - patterns are worth studying"],
            composted_at=datetime.now(),
        )

        learnings = pipeline._to_extracted_learnings(mock_result, None)

        assert len(learnings) == 1
        assert learnings[0].learning_type == "pattern"

    @pytest.mark.asyncio
    async def test_default_to_insight(self):
        """Test that generic lessons become Insight learnings."""
        pipeline = CompostingPipeline()

        from services.mux.lifecycle import CompostResult

        mock_result = CompostResult(
            object_summary={"id": "obj-1"},
            journey=[LifecycleState.EMERGENT],
            lessons=["Every object teaches something through its existence"],
            composted_at=datetime.now(),
        )

        learnings = pipeline._to_extracted_learnings(mock_result, None)

        assert len(learnings) == 1
        assert learnings[0].learning_type == "insight"


class TestCompostingPipelineTrustStages:
    """Tests for trust stage determination."""

    def test_correction_requires_high_trust(self):
        """Test that corrections require trust stage 3."""
        pipeline = CompostingPipeline()

        from services.mux.composting_models import create_correction_learning

        learning = create_correction_learning(
            previous_understanding="Old",
            new_understanding="New",
            evidence=[],
        )

        trust = pipeline._determine_trust_stage(learning)
        assert trust == 3

    def test_high_confidence_allows_push(self):
        """Test that high confidence insights get stage 2."""
        pipeline = CompostingPipeline()

        learning = create_insight_learning(
            description="High confidence insight",
            derived_from=[],
            confidence=0.9,
        )

        trust = pipeline._determine_trust_stage(learning)
        assert trust == 2

    def test_low_confidence_pull_only(self):
        """Test that low confidence insights are stage 1."""
        pipeline = CompostingPipeline()

        learning = create_insight_learning(
            description="Low confidence insight",
            derived_from=[],
            confidence=0.5,
        )

        trust = pipeline._determine_trust_stage(learning)
        assert trust == 1

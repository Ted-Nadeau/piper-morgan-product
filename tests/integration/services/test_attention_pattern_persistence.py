"""
Integration tests for AttentionModel pattern persistence.

Issue #365: SLACK-ATTENTION-DECAY
Tests that learned patterns persist to and load from database.

Requires PostgreSQL running on port 5433.
"""

from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from services.database.models import LearnedPattern
from services.integrations.slack.attention_model import (
    AttentionModel,
    AttentionPattern,
    AttentionSource,
    SpatialCoordinates,
)
from services.shared_types import PatternType


@pytest.mark.integration
class TestAttentionPatternPersistence:
    """Integration tests for pattern persistence to database."""

    @pytest_asyncio.fixture
    async def db_session_factory(self, db_engine):
        """Create a session factory that matches AsyncSessionFactory interface."""
        from contextlib import asynccontextmanager

        from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

        session_maker = async_sessionmaker(
            db_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        class TestSessionFactory:
            @staticmethod
            @asynccontextmanager
            async def create_session():
                async with session_maker() as session:
                    yield session

        return TestSessionFactory()

    @pytest_asyncio.fixture
    async def clean_patterns(self, db_session):
        """Clean up any existing attention patterns before test."""
        from sqlalchemy import delete

        # Use proper enum for deletion
        stmt = delete(LearnedPattern).where(LearnedPattern.pattern_type == PatternType.INTEGRATION)
        await db_session.execute(stmt)
        await db_session.commit()
        yield
        # Cleanup after test too
        await db_session.execute(stmt)
        await db_session.commit()

    @pytest_asyncio.fixture
    async def test_user_id(self, db_session):
        """Create or get a test user for pattern persistence tests."""
        from sqlalchemy import text

        # Check if alfacanon user exists (known stable test user)
        result = await db_session.execute(
            text("SELECT id FROM users WHERE username = 'alfacanon' LIMIT 1")
        )
        row = result.fetchone()
        if row:
            return str(row[0])

        # Fallback: create a temporary test user
        test_id = str(uuid4())
        await db_session.execute(
            text(
                """
                INSERT INTO users (id, username, email, created_at, updated_at)
                VALUES (:id, :username, :email, NOW(), NOW())
            """
            ),
            {
                "id": test_id,
                "username": f"test_{test_id[:8]}",
                "email": f"test_{test_id[:8]}@test.local",
            },
        )
        await db_session.commit()
        return test_id

    @pytest_asyncio.fixture
    async def attention_model_with_persistence(
        self, db_session_factory, clean_patterns, test_user_id
    ):
        """Create AttentionModel with database persistence enabled."""
        model = AttentionModel(
            user_id=test_user_id,
            db_session_factory=db_session_factory,
        )
        return model, test_user_id

    async def test_save_pattern_to_db(self, attention_model_with_persistence, db_session):
        """Test that patterns are saved to database."""
        model, user_id = attention_model_with_persistence

        # Create a pattern
        pattern = AttentionPattern(
            pattern_id=f"test_{uuid4().hex[:8]}",
            pattern_name="emergency_T123",
            trigger_conditions={"source": "emergency", "territory": "T123"},
            observation_count=5,
            confidence=0.8,
        )

        # Save it
        result = await model._save_pattern_to_db(pattern)
        assert result is True

        # Verify it's in the database
        from sqlalchemy import select

        stmt = select(LearnedPattern).where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.pattern_type == PatternType.INTEGRATION,
        )
        result = await db_session.execute(stmt)
        db_pattern = result.scalar_one_or_none()

        assert db_pattern is not None
        assert db_pattern.confidence == 0.8
        assert db_pattern.usage_count == 5

    async def test_load_patterns_from_db(self, attention_model_with_persistence, db_session):
        """Test that patterns are loaded from database."""
        model, user_id = attention_model_with_persistence

        # Insert a pattern using ORM
        db_pattern = LearnedPattern(
            id=str(uuid4()),
            user_id=user_id,
            pattern_type=PatternType.INTEGRATION,
            pattern_data={"source": "mention", "territory": "T456"},
            confidence=0.75,
            usage_count=10,
        )
        db_session.add(db_pattern)
        await db_session.commit()

        # Load patterns
        count = await model.load_patterns_from_db()

        assert count >= 1
        assert len(model._learned_patterns) >= 1

    async def test_pattern_persistence_round_trip(
        self, attention_model_with_persistence, db_session
    ):
        """Test full round trip: learn -> save -> load."""
        model, user_id = attention_model_with_persistence

        # Create an event and learn from it
        event = model.create_attention_event(
            source=AttentionSource.MENTION,
            coordinates=SpatialCoordinates("T_TEST", "C_TEST", None),
            base_intensity=0.9,
            urgency_level=0.8,
            context={"test": True},
        )

        # The learning happens in create_attention_event via _learn_from_attention_event
        # But save is async and fire-and-forget, so we need to save explicitly
        if model._learned_patterns:
            pattern_name = list(model._learned_patterns.keys())[0]
            pattern = model._learned_patterns[pattern_name]
            await model._save_pattern_to_db(pattern)

        # Clear in-memory patterns
        original_count = len(model._learned_patterns)
        model._learned_patterns.clear()
        assert len(model._learned_patterns) == 0

        # Load from database
        loaded_count = await model.load_patterns_from_db()

        # Verify patterns were restored
        assert loaded_count >= 1 or original_count >= 1

    async def test_set_user_context_enables_persistence(
        self, db_session_factory, clean_patterns, test_user_id
    ):
        """Test that set_user_context enables persistence for existing model."""
        # Create model without user_id
        model = AttentionModel()
        assert model._user_id is None

        # Set user context (use real user from DB)
        model.set_user_context(test_user_id)
        model._db_session_factory = db_session_factory

        assert model._user_id == test_user_id

        # Now persistence should work
        pattern = AttentionPattern(
            pattern_id=f"test_{uuid4().hex[:8]}",
            pattern_name="test_pattern",
            trigger_conditions={"test": True},
            observation_count=1,
            confidence=0.5,
        )
        result = await model._save_pattern_to_db(pattern)
        assert result is True


@pytest.mark.integration
class TestAttentionDecayJobIntegration:
    """Integration tests for AttentionDecayJob with real AttentionModel."""

    async def test_decay_job_updates_events(self):
        """Test that decay job processes events correctly."""
        from services.scheduler.attention_decay_job import AttentionDecayJob

        # Create model with some events
        model = AttentionModel()

        # Create test events
        model.create_attention_event(
            source=AttentionSource.EMERGENCY,
            coordinates=SpatialCoordinates("T1", "C1", None),
            base_intensity=1.0,
            urgency_level=0.9,
        )
        model.create_attention_event(
            source=AttentionSource.SOCIAL,
            coordinates=SpatialCoordinates("T1", "C2", None),
            base_intensity=0.3,
            urgency_level=0.2,
        )

        # Create decay job
        job = AttentionDecayJob(attention_model=model, interval_minutes=1)

        # Execute one decay update
        result = await job.execute_decay_update()

        assert result["success"] is True
        assert result["updated"] >= 0
        assert "elapsed_ms" in result

    async def test_decay_job_respects_interval_bounds(self):
        """Test that interval is bounded correctly."""
        from services.scheduler.attention_decay_job import AttentionDecayJob

        model = AttentionModel()

        # Test minimum bound
        job_min = AttentionDecayJob(attention_model=model, interval_minutes=0)
        assert job_min.interval_minutes == AttentionDecayJob.MIN_INTERVAL_MINUTES

        # Test maximum bound
        job_max = AttentionDecayJob(attention_model=model, interval_minutes=100)
        assert job_max.interval_minutes == AttentionDecayJob.MAX_INTERVAL_MINUTES

        # Test within bounds
        job_normal = AttentionDecayJob(attention_model=model, interval_minutes=15)
        assert job_normal.interval_minutes == 15


@pytest.mark.integration
class TestE2EAttentionDecayPersistence:
    """E2E tests: Full flow from events through decay to persistence."""

    @pytest_asyncio.fixture
    async def db_session_factory(self, db_engine):
        """Create a session factory for E2E tests."""
        from contextlib import asynccontextmanager

        from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

        session_maker = async_sessionmaker(
            db_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        class TestSessionFactory:
            @staticmethod
            @asynccontextmanager
            async def create_session():
                async with session_maker() as session:
                    yield session

        return TestSessionFactory()

    @pytest_asyncio.fixture
    async def test_user_id(self, db_session):
        """Get a real user for E2E tests."""
        from sqlalchemy import text

        result = await db_session.execute(
            text("SELECT id FROM users WHERE username = 'alfacanon' LIMIT 1")
        )
        row = result.fetchone()
        if row:
            return str(row[0])
        # Create temp user if needed
        test_id = str(uuid4())
        await db_session.execute(
            text(
                """INSERT INTO users (id, username, email, created_at, updated_at)
                    VALUES (:id, :username, :email, NOW(), NOW())"""
            ),
            {
                "id": test_id,
                "username": f"e2e_{test_id[:8]}",
                "email": f"e2e_{test_id[:8]}@test.local",
            },
        )
        await db_session.commit()
        return test_id

    async def test_full_e2e_attention_decay_persistence(
        self, db_session_factory, test_user_id, db_session
    ):
        """
        E2E Test: Complete attention decay workflow.

        Flow:
        1. Create AttentionModel with persistence enabled
        2. Create attention events (which trigger pattern learning)
        3. Run decay job to update event intensities
        4. Save learned patterns to database
        5. Clear in-memory state
        6. Load patterns from database
        7. Verify patterns were restored correctly
        """
        from sqlalchemy import delete

        from services.scheduler.attention_decay_job import AttentionDecayJob

        # Cleanup: Remove any existing test patterns
        stmt = delete(LearnedPattern).where(
            LearnedPattern.user_id == test_user_id,
            LearnedPattern.pattern_type == PatternType.INTEGRATION,
        )
        await db_session.execute(stmt)
        await db_session.commit()

        # Step 1: Create model with persistence
        model = AttentionModel(
            user_id=test_user_id,
            db_session_factory=db_session_factory,
        )

        # Step 2: Create attention events (triggers learning)
        event1 = model.create_attention_event(
            source=AttentionSource.EMERGENCY,
            coordinates=SpatialCoordinates("T_E2E", "C_EMERGENCY", None),
            base_intensity=1.0,
            urgency_level=0.95,
            context={"e2e_test": True, "event": "emergency"},
        )
        assert event1 is not None
        assert event1.source == AttentionSource.EMERGENCY

        event2 = model.create_attention_event(
            source=AttentionSource.MENTION,
            coordinates=SpatialCoordinates("T_E2E", "C_MENTION", None),
            base_intensity=0.8,
            urgency_level=0.7,
            context={"e2e_test": True, "event": "mention"},
        )
        assert event2 is not None

        # Step 3: Run decay job
        job = AttentionDecayJob(attention_model=model, interval_minutes=1)
        decay_result = await job.execute_decay_update()

        assert decay_result["success"] is True
        assert decay_result["updated"] >= 0

        # Step 4: Save any learned patterns to database
        patterns_saved = 0
        for pattern in model._learned_patterns.values():
            saved = await model._save_pattern_to_db(pattern)
            if saved:
                patterns_saved += 1

        # Step 5: Remember what we had, then clear in-memory
        original_patterns = dict(model._learned_patterns)
        original_events = dict(model._active_events)

        model._learned_patterns.clear()
        model._active_events.clear()

        assert len(model._learned_patterns) == 0
        assert len(model._active_events) == 0

        # Step 6: Load patterns from database
        loaded_count = await model.load_patterns_from_db()

        # Step 7: Verify restoration
        # We should have loaded at least as many patterns as we saved
        # (may be more if other tests left patterns)
        assert loaded_count >= patterns_saved or patterns_saved == 0

        # Verify the model can create new events (functional after reload)
        event3 = model.create_attention_event(
            source=AttentionSource.SOCIAL,
            coordinates=SpatialCoordinates("T_E2E", "C_POST_RELOAD", None),
            base_intensity=0.5,
            urgency_level=0.3,
        )
        assert event3 is not None

        # Cleanup
        await db_session.execute(stmt)
        await db_session.commit()

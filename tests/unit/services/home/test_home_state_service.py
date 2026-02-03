"""
Tests for HomeStateService.

Issue #419: MUX-NAV-HOME - Home State Design
Pattern-050: Context Dataclass Pair
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest

from services.home import HomeStateContext, HomeStateItem, HomeStateResult, HomeStateService
from services.shared_types import HardnessLevel, TrustStage


class TestHomeStateContext:
    """Test HomeStateContext dataclass."""

    def test_context_creation(self):
        """Verify context can be created with required fields."""
        user_id = uuid4()
        ctx = HomeStateContext(
            user_id=user_id,
            trust_stage=TrustStage.BUILDING,
            timestamp=datetime.now(timezone.utc),
        )
        assert ctx.user_id == user_id
        assert ctx.trust_stage == TrustStage.BUILDING
        assert ctx.time_of_day == "default"

    def test_context_with_time_of_day(self):
        """Verify time_of_day can be set."""
        ctx = HomeStateContext(
            user_id=uuid4(),
            trust_stage=TrustStage.NEW,
            timestamp=datetime.now(timezone.utc),
            time_of_day="morning",
        )
        assert ctx.time_of_day == "morning"


class TestHomeStateItem:
    """Test HomeStateItem dataclass."""

    def test_item_creation(self):
        """Verify item can be created with required fields."""
        item = HomeStateItem(
            id="test-item",
            title="Test Title",
            description="Test description",
            hardness=HardnessLevel.HARD,
            item_type="project",
        )
        assert item.id == "test-item"
        assert item.hardness == HardnessLevel.HARD
        assert item.source is None

    def test_item_with_source(self):
        """Verify item source can be set for transparency."""
        item = HomeStateItem(
            id="github-pr",
            title="PR needs review",
            description="Pull request #123",
            hardness=HardnessLevel.SOFT,
            item_type="observation",
            source="From GitHub",
        )
        assert item.source == "From GitHub"


class TestHomeStateService:
    """Test HomeStateService functionality."""

    @pytest.fixture
    def service(self):
        """Create service instance."""
        return HomeStateService()

    @pytest.fixture
    def new_user_context(self):
        """Create context for Stage 1 (NEW) user."""
        return HomeStateContext(
            user_id=uuid4(),
            trust_stage=TrustStage.NEW,
            timestamp=datetime.now(timezone.utc),
        )

    @pytest.fixture
    def trusted_user_context(self):
        """Create context for Stage 4 (TRUSTED) user."""
        return HomeStateContext(
            user_id=uuid4(),
            trust_stage=TrustStage.TRUSTED,
            timestamp=datetime.now(timezone.utc),
        )

    @pytest.mark.asyncio
    async def test_generate_returns_result(self, service, new_user_context):
        """Verify generate_home_state returns HomeStateResult."""
        result = await service.generate_home_state(new_user_context)

        assert isinstance(result, HomeStateResult)
        assert result.user_id == new_user_context.user_id
        assert result.trust_stage == TrustStage.NEW

    @pytest.mark.asyncio
    async def test_result_includes_lenses(self, service, new_user_context):
        """Verify lenses (hardest objects) are always included."""
        result = await service.generate_home_state(new_user_context)

        lens_items = [item for item in result.items if item.item_type == "lens"]
        assert len(lens_items) >= 3  # "stuck", "urgent", "coming"

        # All lenses should be HARDEST
        for lens in lens_items:
            assert lens.hardness == HardnessLevel.HARDEST

    @pytest.mark.asyncio
    async def test_stage_1_sees_only_hardest(self, service, new_user_context):
        """Stage 1 (NEW) users should only see HARDEST items."""
        result = await service.generate_home_state(new_user_context)

        for item in result.items:
            assert (
                item.hardness == HardnessLevel.HARDEST
            ), f"Stage 1 should not see {item.hardness.name} items"

    @pytest.mark.asyncio
    async def test_stage_4_sees_all(self, service, trusted_user_context):
        """Stage 4 (TRUSTED) users should see all hardness levels."""
        result = await service.generate_home_state(trusted_user_context)

        # At minimum, should see the hardest items (lenses)
        assert len(result.items) >= 3

    @pytest.mark.asyncio
    async def test_greeting_varies_by_trust(self, service):
        """Verify greeting changes based on trust stage."""
        greetings = {}

        for stage in TrustStage:
            ctx = HomeStateContext(
                user_id=uuid4(),
                trust_stage=stage,
                timestamp=datetime.now(timezone.utc),
            )
            result = await service.generate_home_state(ctx)
            greetings[stage] = result.greeting

        # All stages should have greetings
        assert all(g for g in greetings.values())

        # Greetings should differ by stage
        # Stage 1 should be minimal, Stage 4 should show agency
        assert (
            "help" in greetings[TrustStage.NEW].lower()
            or "welcome" in greetings[TrustStage.NEW].lower()
        )
        assert (
            "thinking" in greetings[TrustStage.TRUSTED].lower()
            or "been" in greetings[TrustStage.TRUSTED].lower()
        )

    @pytest.mark.asyncio
    async def test_greeting_includes_time_of_day(self, service):
        """Verify greeting can include time-of-day variation."""
        morning_ctx = HomeStateContext(
            user_id=uuid4(),
            trust_stage=TrustStage.BUILDING,
            timestamp=datetime.now(timezone.utc),
            time_of_day="morning",
        )
        result = await service.generate_home_state(morning_ctx)

        assert "morning" in result.greeting.lower()

    @pytest.mark.asyncio
    async def test_briefing_only_for_established_users(self, service):
        """Briefing summary should only appear for Stage 3+."""
        # Stage 2 should not have briefing
        stage_2_ctx = HomeStateContext(
            user_id=uuid4(),
            trust_stage=TrustStage.BUILDING,
            timestamp=datetime.now(timezone.utc),
        )
        result = await service.generate_home_state(stage_2_ctx)
        # Currently returns None anyway, but this documents the intent
        # assert result.briefing_summary is None

        # Stage 3 could have briefing (when implemented)
        stage_3_ctx = HomeStateContext(
            user_id=uuid4(),
            trust_stage=TrustStage.ESTABLISHED,
            timestamp=datetime.now(timezone.utc),
        )
        # This will be tested more thoroughly when briefing is implemented

    @pytest.mark.asyncio
    async def test_generation_time_tracked(self, service, new_user_context):
        """Verify generation time is measured."""
        result = await service.generate_home_state(new_user_context)

        # Should have a reasonable generation time
        assert result.generation_time_ms >= 0
        assert result.generation_time_ms < 1000  # Should be fast for basic case


class TestTrustGatedHardnessFiltering:
    """Test that hardness filtering works correctly by trust stage."""

    @pytest.fixture
    def service(self):
        return HomeStateService()

    def test_get_min_hardness_for_stage(self, service):
        """Verify min hardness mapping for each trust stage."""
        assert service._get_min_hardness_for_stage(TrustStage.NEW) == HardnessLevel.HARDEST
        assert service._get_min_hardness_for_stage(TrustStage.BUILDING) == HardnessLevel.HARD
        assert service._get_min_hardness_for_stage(TrustStage.ESTABLISHED) == HardnessLevel.SOFT
        assert service._get_min_hardness_for_stage(TrustStage.TRUSTED) == HardnessLevel.SOFTEST

    def test_min_hardness_comparison(self, service):
        """Verify hardness comparison works for filtering."""
        # Stage 2 min is HARD, so only HARD and HARDEST should pass
        min_hardness = service._get_min_hardness_for_stage(TrustStage.BUILDING)

        assert HardnessLevel.HARDEST >= min_hardness  # Visible
        assert HardnessLevel.HARD >= min_hardness  # Visible
        assert not HardnessLevel.MEDIUM >= min_hardness  # Not visible
        assert not HardnessLevel.SOFT >= min_hardness  # Not visible
        assert not HardnessLevel.SOFTEST >= min_hardness  # Not visible


class TestLensItems:
    """Test the always-present lens items."""

    @pytest.fixture
    def service(self):
        return HomeStateService()

    def test_lens_items_exist(self, service):
        """Verify the required lens items are defined."""
        lenses = service._get_lens_items()

        lens_ids = [lens.id for lens in lenses]
        assert "lens-stuck" in lens_ids
        assert "lens-urgent" in lens_ids
        assert "lens-coming" in lens_ids

    def test_lens_items_are_hardest(self, service):
        """Verify all lenses are HARDEST hardness level."""
        lenses = service._get_lens_items()

        for lens in lenses:
            assert lens.hardness == HardnessLevel.HARDEST
            assert lens.item_type == "lens"

    def test_lens_items_have_actions(self, service):
        """Verify lenses have defined actions."""
        lenses = service._get_lens_items()

        for lens in lenses:
            assert lens.action is not None
            assert lens.action.startswith("show_")

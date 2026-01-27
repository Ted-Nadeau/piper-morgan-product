"""
Tests for HardnessLevel enum and trust-gated visibility rules.

Issue #419: MUX-NAV-HOME - Home State Design
"""

import pytest

from services.shared_types import HardnessLevel, TrustStage


class TestHardnessLevel:
    """Test HardnessLevel enum definitions."""

    def test_hardness_levels_exist(self):
        """Verify all hardness levels are defined."""
        expected_levels = ["HARDEST", "HARD", "MEDIUM", "SOFT", "SOFTEST"]
        actual_levels = [h.name for h in HardnessLevel]
        assert actual_levels == expected_levels

    def test_hardness_values_descending(self):
        """Hardness values should be higher for harder objects (more persistent)."""
        assert HardnessLevel.HARDEST.value > HardnessLevel.HARD.value
        assert HardnessLevel.HARD.value > HardnessLevel.MEDIUM.value
        assert HardnessLevel.MEDIUM.value > HardnessLevel.SOFT.value
        assert HardnessLevel.SOFT.value > HardnessLevel.SOFTEST.value

    def test_hardness_can_be_compared(self):
        """Hardness levels should be comparable for filtering."""
        # Can filter "show objects harder than X"
        assert HardnessLevel.HARDEST > HardnessLevel.SOFT
        assert HardnessLevel.MEDIUM >= HardnessLevel.MEDIUM

        # Useful for trust-gated visibility
        min_hardness = HardnessLevel.MEDIUM
        visible = [h for h in HardnessLevel if h >= min_hardness]
        assert HardnessLevel.HARDEST in visible
        assert HardnessLevel.HARD in visible
        assert HardnessLevel.MEDIUM in visible
        assert HardnessLevel.SOFT not in visible
        assert HardnessLevel.SOFTEST not in visible


class TestTrustGatedHardnessVisibility:
    """Test trust-stage visibility rules for hardness levels.

    From #419 design:
    - Stage 1 (NEW): Only user-initiated (hardest)
    - Stage 2 (BUILDING): + Soft hints
    - Stage 3 (ESTABLISHED): + Soft observations
    - Stage 4 (TRUSTED): All levels including anticipatory (softest)
    """

    def get_min_hardness_for_stage(self, stage: TrustStage) -> HardnessLevel:
        """Get minimum hardness level visible at a trust stage.

        Higher min_hardness = fewer objects visible (more restrictive).
        Lower min_hardness = more objects visible (more permissive).
        """
        stage_to_min_hardness = {
            TrustStage.NEW: HardnessLevel.HARDEST,  # Only hardest objects
            TrustStage.BUILDING: HardnessLevel.HARD,  # Hard and above
            TrustStage.ESTABLISHED: HardnessLevel.SOFT,  # Soft and above
            TrustStage.TRUSTED: HardnessLevel.SOFTEST,  # All objects
        }
        return stage_to_min_hardness[stage]

    def is_visible_at_stage(self, hardness: HardnessLevel, stage: TrustStage) -> bool:
        """Determine if an object with given hardness is visible at trust stage."""
        min_hardness = self.get_min_hardness_for_stage(stage)
        return hardness >= min_hardness

    def test_stage_1_sees_only_hardest(self):
        """Stage 1 (NEW) users see only hardest objects."""
        assert self.is_visible_at_stage(HardnessLevel.HARDEST, TrustStage.NEW)
        assert not self.is_visible_at_stage(HardnessLevel.HARD, TrustStage.NEW)
        assert not self.is_visible_at_stage(HardnessLevel.MEDIUM, TrustStage.NEW)
        assert not self.is_visible_at_stage(HardnessLevel.SOFT, TrustStage.NEW)
        assert not self.is_visible_at_stage(HardnessLevel.SOFTEST, TrustStage.NEW)

    def test_stage_2_sees_hard_and_above(self):
        """Stage 2 (BUILDING) users see hard and above."""
        assert self.is_visible_at_stage(HardnessLevel.HARDEST, TrustStage.BUILDING)
        assert self.is_visible_at_stage(HardnessLevel.HARD, TrustStage.BUILDING)
        assert not self.is_visible_at_stage(HardnessLevel.MEDIUM, TrustStage.BUILDING)
        assert not self.is_visible_at_stage(HardnessLevel.SOFT, TrustStage.BUILDING)
        assert not self.is_visible_at_stage(HardnessLevel.SOFTEST, TrustStage.BUILDING)

    def test_stage_3_sees_soft_and_above(self):
        """Stage 3 (ESTABLISHED) users see soft and above (observations)."""
        assert self.is_visible_at_stage(HardnessLevel.HARDEST, TrustStage.ESTABLISHED)
        assert self.is_visible_at_stage(HardnessLevel.HARD, TrustStage.ESTABLISHED)
        assert self.is_visible_at_stage(HardnessLevel.MEDIUM, TrustStage.ESTABLISHED)
        assert self.is_visible_at_stage(HardnessLevel.SOFT, TrustStage.ESTABLISHED)
        assert not self.is_visible_at_stage(HardnessLevel.SOFTEST, TrustStage.ESTABLISHED)

    def test_stage_4_sees_all(self):
        """Stage 4 (TRUSTED) users see all objects including anticipatory."""
        assert self.is_visible_at_stage(HardnessLevel.HARDEST, TrustStage.TRUSTED)
        assert self.is_visible_at_stage(HardnessLevel.HARD, TrustStage.TRUSTED)
        assert self.is_visible_at_stage(HardnessLevel.MEDIUM, TrustStage.TRUSTED)
        assert self.is_visible_at_stage(HardnessLevel.SOFT, TrustStage.TRUSTED)
        assert self.is_visible_at_stage(HardnessLevel.SOFTEST, TrustStage.TRUSTED)

    def test_visibility_increases_with_trust(self):
        """Higher trust stages should see more objects."""
        for hardness in HardnessLevel:
            # Count how many stages see this hardness
            visible_at_stages = [
                stage for stage in TrustStage if self.is_visible_at_stage(hardness, stage)
            ]

            # Softer objects should be visible at fewer stages
            if hardness == HardnessLevel.HARDEST:
                assert len(visible_at_stages) == 4  # All stages
            elif hardness == HardnessLevel.HARD:
                assert len(visible_at_stages) == 3  # Stage 2+
            elif hardness == HardnessLevel.MEDIUM:
                assert len(visible_at_stages) == 2  # Stage 3+
            elif hardness == HardnessLevel.SOFT:
                assert len(visible_at_stages) == 2  # Stage 3+
            elif hardness == HardnessLevel.SOFTEST:
                assert len(visible_at_stages) == 1  # Stage 4 only


class TestHardnessOwnershipCorrelation:
    """Test that hardness correlates with ownership model.

    From #419 design notes:
    - NATIVE objects tend to be harder (user's core data)
    - FEDERATED objects tend to be softer (observed from places)
    - SYNTHETIC objects can vary
    """

    def test_hardness_docstring_mentions_ownership(self):
        """Verify documentation links hardness to ownership model."""
        docstring = HardnessLevel.__doc__
        assert "NATIVE" in docstring
        assert "FEDERATED" in docstring
        assert "SYNTHETIC" in docstring
        assert "OwnershipCategory" in docstring or "ownership" in docstring.lower()

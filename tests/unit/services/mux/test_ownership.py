"""
Tests for Ownership Model (P2).

This module tests the three-category ownership model describing
Piper's relationship to objects:
- NATIVE: Piper's Mind - what Piper creates/owns directly
- FEDERATED: Piper's Senses - what Piper observes externally
- SYNTHETIC: Piper's Understanding - what Piper constructs through reasoning
"""

import pytest

from services.mux.ownership import (
    HasOwnership,
    OwnershipCategory,
    OwnershipResolution,
    OwnershipResolver,
    OwnershipTransformation,
)


class TestOwnershipCategoryBasics:
    """Test basic enum structure."""

    def test_has_native_category(self):
        """NATIVE category exists for Piper's Mind."""
        assert OwnershipCategory.NATIVE is not None
        assert OwnershipCategory.NATIVE.value == "native"

    def test_has_federated_category(self):
        """FEDERATED category exists for Piper's Senses."""
        assert OwnershipCategory.FEDERATED is not None
        assert OwnershipCategory.FEDERATED.value == "federated"

    def test_has_synthetic_category(self):
        """SYNTHETIC category exists for Piper's Understanding."""
        assert OwnershipCategory.SYNTHETIC is not None
        assert OwnershipCategory.SYNTHETIC.value == "synthetic"


class TestOwnershipCategoryMetaphors:
    """Test consciousness metaphors."""

    def test_native_has_metaphor(self):
        """NATIVE has consciousness metaphor."""
        assert "Mind" in OwnershipCategory.NATIVE.metaphor

    def test_federated_has_metaphor(self):
        """FEDERATED has consciousness metaphor."""
        assert "Senses" in OwnershipCategory.FEDERATED.metaphor

    def test_synthetic_has_metaphor(self):
        """SYNTHETIC has consciousness metaphor."""
        assert "Understanding" in OwnershipCategory.SYNTHETIC.metaphor


class TestOwnershipCategoryExperiencePhrases:
    """Test experience framing phrases."""

    def test_native_experience_phrase(self):
        """NATIVE has experience phrase."""
        assert "created" in OwnershipCategory.NATIVE.experience_phrase.lower()

    def test_federated_experience_phrase(self):
        """FEDERATED has experience phrase."""
        assert "see" in OwnershipCategory.FEDERATED.experience_phrase.lower()

    def test_synthetic_experience_phrase(self):
        """SYNTHETIC has experience phrase."""
        assert "understand" in OwnershipCategory.SYNTHETIC.experience_phrase.lower()


class TestHasOwnershipProtocol:
    """Test HasOwnership protocol for runtime checking."""

    def test_protocol_is_runtime_checkable(self):
        """HasOwnership can be used with isinstance()."""

        # Create mock object satisfying protocol
        class MockOwned:
            @property
            def ownership_category(self) -> OwnershipCategory:
                return OwnershipCategory.NATIVE

            @property
            def ownership_source(self) -> str:
                return "piper"

            @property
            def ownership_confidence(self) -> float:
                return 1.0

        obj = MockOwned()
        assert isinstance(obj, HasOwnership)

    def test_non_conforming_object_fails(self):
        """Objects without ownership properties don't satisfy protocol."""

        class NotOwned:
            pass

        obj = NotOwned()
        assert not isinstance(obj, HasOwnership)

    def test_protocol_requires_all_properties(self):
        """Protocol requires category, source, and confidence."""

        class PartialOwned:
            @property
            def ownership_category(self) -> OwnershipCategory:
                return OwnershipCategory.NATIVE

            # Missing source and confidence

        obj = PartialOwned()
        assert not isinstance(obj, HasOwnership)


class TestOwnershipResolverDetermination:
    """Test OwnershipResolver.determine() for category assignment."""

    def test_native_for_piper_created(self):
        """Objects created by Piper are NATIVE."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="piper", created_by="piper")
        assert category == OwnershipCategory.NATIVE

    def test_native_for_system_source(self):
        """Objects from system/internal are NATIVE."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="system")
        assert category == OwnershipCategory.NATIVE

    def test_federated_for_github(self):
        """Objects from GitHub are FEDERATED."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="github")
        assert category == OwnershipCategory.FEDERATED

    def test_federated_for_slack(self):
        """Objects from Slack are FEDERATED."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="slack")
        assert category == OwnershipCategory.FEDERATED

    def test_synthetic_for_derived(self):
        """Derived/computed objects are SYNTHETIC."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="inference", is_derived=True)
        assert category == OwnershipCategory.SYNTHETIC

    def test_cached_federated_remains_federated(self):
        """Cached federated data remains FEDERATED."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="github", is_cached=True)
        assert category == OwnershipCategory.FEDERATED


class TestOwnershipResolverResolution:
    """Test OwnershipResolver.resolve() for full resolution."""

    def test_resolution_includes_confidence(self):
        """Resolution provides confidence score."""
        resolver = OwnershipResolver()
        result = resolver.resolve(source="github")
        assert isinstance(result, OwnershipResolution)
        assert 0.0 <= result.confidence <= 1.0

    def test_resolution_includes_reasoning(self):
        """Resolution explains the determination."""
        resolver = OwnershipResolver()
        result = resolver.resolve(source="piper")
        assert result.reasoning
        assert len(result.reasoning) > 0


class TestOwnershipTransformation:
    """Test ownership category transformations."""

    def test_federated_to_synthetic_is_valid(self):
        """FEDERATED -> SYNTHETIC is valid (observation -> understanding)."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.FEDERATED, to_category=OwnershipCategory.SYNTHETIC
        )
        assert transform.is_valid()

    def test_synthetic_to_native_is_valid(self):
        """SYNTHETIC -> NATIVE is valid (understanding -> memory)."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.SYNTHETIC, to_category=OwnershipCategory.NATIVE
        )
        assert transform.is_valid()

    def test_transformation_has_description(self):
        """Transformations have meaningful descriptions."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.FEDERATED, to_category=OwnershipCategory.SYNTHETIC
        )
        assert transform.description
        assert len(transform.description) > 0

    def test_native_to_federated_is_invalid(self):
        """NATIVE -> FEDERATED is invalid (can't un-create)."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.NATIVE, to_category=OwnershipCategory.FEDERATED
        )
        assert not transform.is_valid()

    def test_same_category_is_invalid(self):
        """Same category transformation is invalid (no-op)."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.NATIVE, to_category=OwnershipCategory.NATIVE
        )
        assert not transform.is_valid()

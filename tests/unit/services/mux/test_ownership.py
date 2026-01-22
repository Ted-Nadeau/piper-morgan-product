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
    OwnershipMetadata,
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


class TestOwnershipMetadataFactoryMethods:
    """Test OwnershipMetadata factory methods."""

    def test_native_factory_defaults(self):
        """native() creates NATIVE ownership with sensible defaults."""
        metadata = OwnershipMetadata.native()
        assert metadata.category == OwnershipCategory.NATIVE
        assert metadata.source == "piper"
        assert metadata.confidence == 1.0
        assert metadata.requires_verification is False
        assert metadata.can_modify is True

    def test_native_factory_custom_source(self):
        """native() accepts custom source."""
        metadata = OwnershipMetadata.native(source="piper-core")
        assert metadata.source == "piper-core"
        assert metadata.category == OwnershipCategory.NATIVE

    def test_federated_factory_defaults(self):
        """federated() creates FEDERATED ownership with sensible defaults."""
        metadata = OwnershipMetadata.federated(source="github")
        assert metadata.category == OwnershipCategory.FEDERATED
        assert metadata.source == "github"
        assert metadata.confidence == 0.9  # Slightly uncertain
        assert metadata.requires_verification is True
        assert metadata.can_modify is False  # Can't change external truth

    def test_federated_factory_various_sources(self):
        """federated() works with various external sources."""
        sources = ["github", "slack", "calendar", "notion"]
        for source in sources:
            metadata = OwnershipMetadata.federated(source=source)
            assert metadata.source == source
            assert metadata.category == OwnershipCategory.FEDERATED

    def test_synthetic_factory_defaults(self):
        """synthetic() creates SYNTHETIC ownership with derivation chain."""
        metadata = OwnershipMetadata.synthetic(
            source="risk-analysis",
            derived_from=["issue-123", "commit-456"],
            transformation="pattern-match",
        )
        assert metadata.category == OwnershipCategory.SYNTHETIC
        assert metadata.source == "risk-analysis"
        assert metadata.confidence == 0.7  # Inference uncertainty
        assert metadata.derived_from == ["issue-123", "commit-456"]
        assert metadata.transformation_chain == ["pattern-match"]
        assert metadata.requires_verification is True
        assert metadata.can_modify is True

    def test_synthetic_factory_custom_confidence(self):
        """synthetic() accepts custom confidence."""
        metadata = OwnershipMetadata.synthetic(
            source="ml-inference",
            derived_from=["data-1"],
            transformation="classify",
            confidence=0.95,
        )
        assert metadata.confidence == 0.95


class TestOwnershipMetadataValidation:
    """Test OwnershipMetadata validation."""

    def test_confidence_must_be_in_range(self):
        """Confidence must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="Confidence must be 0.0-1.0"):
            OwnershipMetadata(
                category=OwnershipCategory.NATIVE,
                source="piper",
                confidence=1.5,
            )

    def test_confidence_can_be_zero(self):
        """Confidence of 0.0 is valid."""
        metadata = OwnershipMetadata(
            category=OwnershipCategory.NATIVE,
            source="piper",
            confidence=0.0,
        )
        assert metadata.confidence == 0.0

    def test_confidence_can_be_one(self):
        """Confidence of 1.0 is valid."""
        metadata = OwnershipMetadata(
            category=OwnershipCategory.NATIVE,
            source="piper",
            confidence=1.0,
        )
        assert metadata.confidence == 1.0

    def test_created_at_defaults_to_now(self):
        """created_at is set automatically if not provided."""
        metadata = OwnershipMetadata.native()
        assert metadata.created_at is not None


class TestOwnershipMetadataVerification:
    """Test OwnershipMetadata verification methods."""

    def test_verify_creates_new_metadata(self):
        """verify() returns new metadata with verification timestamp."""
        original = OwnershipMetadata.federated(source="github")
        assert original.requires_verification is True
        assert original.last_verified is None

        verified = original.verify()
        assert verified.requires_verification is False
        assert verified.last_verified is not None
        # Original unchanged
        assert original.requires_verification is True


class TestOwnershipMetadataPromoteToNative:
    """Test OwnershipMetadata.promote_to_native()."""

    def test_promote_synthetic_to_native(self):
        """Synthetic can be promoted to native on user confirmation."""
        synthetic = OwnershipMetadata.synthetic(
            source="inference",
            derived_from=["data-1"],
            transformation="analyze",
        )
        assert synthetic.category == OwnershipCategory.SYNTHETIC

        promoted = synthetic.promote_to_native(reason="user_confirmed")
        assert promoted.category == OwnershipCategory.NATIVE
        assert promoted.confidence == 1.0
        assert promoted.requires_verification is False
        assert "promoted_to_native:user_confirmed" in promoted.transformation_chain

    def test_promote_federated_to_native(self):
        """Federated can also be promoted to native."""
        federated = OwnershipMetadata.federated(source="github")
        promoted = federated.promote_to_native(reason="imported")
        assert promoted.category == OwnershipCategory.NATIVE
        assert "promoted_to_native:imported" in promoted.transformation_chain

    def test_promote_native_is_noop(self):
        """Promoting native returns the same metadata."""
        native = OwnershipMetadata.native()
        promoted = native.promote_to_native()
        assert promoted is native  # Same object


class TestOwnershipMetadataDerive:
    """Test OwnershipMetadata.derive()."""

    def test_derive_creates_synthetic(self):
        """derive() creates synthetic ownership from parent."""
        federated = OwnershipMetadata.federated(source="github", confidence=0.9)
        derived = federated.derive(
            transformation="risk-assessment",
            new_source="risk-analysis",
        )
        assert derived.category == OwnershipCategory.SYNTHETIC
        assert derived.source == "risk-analysis"
        assert "risk-assessment" in derived.transformation_chain

    def test_derive_applies_confidence_decay(self):
        """derive() reduces confidence by decay factor."""
        original = OwnershipMetadata.federated(source="github", confidence=0.9)
        derived = original.derive(
            transformation="analyze",
            new_source="analysis",
            confidence_decay=0.9,
        )
        assert derived.confidence == pytest.approx(0.81, rel=0.01)

    def test_derive_tracks_derivation_source(self):
        """derive() tracks the parent source."""
        original = OwnershipMetadata.federated(source="github")
        derived = original.derive(
            transformation="analyze",
            new_source="analysis",
        )
        assert "github" in derived.derived_from


class TestOwnershipMetadataSerialization:
    """Test OwnershipMetadata serialization."""

    def test_to_dict(self):
        """to_dict() produces valid dictionary."""
        metadata = OwnershipMetadata.synthetic(
            source="inference",
            derived_from=["data-1"],
            transformation="analyze",
        )
        data = metadata.to_dict()
        assert data["category"] == "synthetic"
        assert data["source"] == "inference"
        assert data["derived_from"] == ["data-1"]
        assert data["transformation_chain"] == ["analyze"]

    def test_from_dict_roundtrip(self):
        """from_dict() restores metadata from dictionary."""
        original = OwnershipMetadata.synthetic(
            source="inference",
            derived_from=["data-1", "data-2"],
            transformation="analyze",
            confidence=0.8,
        )
        data = original.to_dict()
        restored = OwnershipMetadata.from_dict(data)
        assert restored.category == original.category
        assert restored.source == original.source
        assert restored.confidence == original.confidence
        assert restored.derived_from == original.derived_from


class TestOwnershipMetadataIntegration:
    """Integration tests for OwnershipMetadata usage patterns."""

    def test_github_issue_to_risk_assessment_flow(self):
        """
        Test the flow from GitHub issue observation to risk assessment.

        1. GitHub issue is FEDERATED (observed)
        2. Risk analysis is SYNTHETIC (derived)
        3. User confirmation promotes to NATIVE (confirmed)
        """
        # Step 1: Observe GitHub issue
        github_issue = OwnershipMetadata.federated(source="github")
        assert github_issue.category == OwnershipCategory.FEDERATED
        assert github_issue.can_modify is False

        # Step 2: Derive risk assessment
        risk = github_issue.derive(
            transformation="risk-pattern-match",
            new_source="risk-analysis",
        )
        assert risk.category == OwnershipCategory.SYNTHETIC
        assert "github" in risk.derived_from
        assert risk.requires_verification is True

        # Step 3: User confirms the assessment
        confirmed = risk.promote_to_native(reason="user_confirmed_risk")
        assert confirmed.category == OwnershipCategory.NATIVE
        assert confirmed.confidence == 1.0
        assert confirmed.requires_verification is False

    def test_session_is_native(self):
        """Sessions Piper creates are NATIVE."""
        session_ownership = OwnershipMetadata.native(source="piper-session")
        assert session_ownership.category == OwnershipCategory.NATIVE
        assert session_ownership.confidence == 1.0
        assert session_ownership.can_modify is True

    def test_calendar_event_is_federated(self):
        """Calendar events from external calendars are FEDERATED."""
        event_ownership = OwnershipMetadata.federated(source="calendar")
        assert event_ownership.category == OwnershipCategory.FEDERATED
        assert event_ownership.requires_verification is True
        assert event_ownership.can_modify is False

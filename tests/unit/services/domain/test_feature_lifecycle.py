"""Tests for Feature.to_dict() lifecycle serialization (#705 MUX-LIFECYCLE-UI-B).

Tests verify:
- Feature.to_dict() includes lifecycle_state when present
- Feature.to_dict() excludes lifecycle_state when None
- All lifecycle states serialize correctly
"""

import pytest

from services.domain.models import Feature
from services.mux.lifecycle import LifecycleState


class TestFeatureToDictLifecycle:
    """Test Feature.to_dict() lifecycle serialization."""

    def test_to_dict_includes_lifecycle_when_present(self):
        """to_dict includes lifecycle_state when it's set."""
        feature = Feature(
            name="Dark Mode",
            status="proposed",
            lifecycle_state=LifecycleState.PROPOSED,
        )
        result = feature.to_dict()
        assert "lifecycle_state" in result
        assert result["lifecycle_state"] == "proposed"

    def test_to_dict_excludes_lifecycle_when_none(self):
        """to_dict excludes lifecycle_state when it's None."""
        feature = Feature(name="Dark Mode", status="draft")
        result = feature.to_dict()
        assert "lifecycle_state" not in result

    def test_to_dict_lifecycle_all_states(self):
        """All lifecycle states serialize correctly."""
        for state in LifecycleState:
            feature = Feature(
                name="Test Feature",
                status="draft",
                lifecycle_state=state,
            )
            result = feature.to_dict()
            assert result["lifecycle_state"] == state.value

    def test_to_dict_preserves_other_fields(self):
        """to_dict preserves all standard Feature fields with lifecycle."""
        feature = Feature(
            name="Authentication",
            description="User login system",
            hypothesis="Users need secure login",
            acceptance_criteria=["Can login", "Can logout"],
            status="approved",
            lifecycle_state=LifecycleState.RATIFIED,
        )
        result = feature.to_dict()

        # Check lifecycle
        assert result["lifecycle_state"] == "ratified"

        # Check standard fields still present
        assert result["name"] == "Authentication"
        assert result["description"] == "User login system"
        assert result["hypothesis"] == "Users need secure login"
        assert result["acceptance_criteria"] == ["Can login", "Can logout"]
        assert result["status"] == "approved"
        assert "id" in result
        assert "created_at" in result
        assert "updated_at" in result

    def test_to_dict_datetime_serialization(self):
        """to_dict serializes datetime fields as ISO format strings."""
        feature = Feature(name="Test", status="draft")
        result = feature.to_dict()

        # created_at and updated_at should be ISO format strings
        assert isinstance(result["created_at"], str)
        assert isinstance(result["updated_at"], str)
        # Should be valid ISO format (contains T separator)
        assert "T" in result["created_at"]
        assert "T" in result["updated_at"]

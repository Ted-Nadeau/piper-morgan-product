"""Unit tests for Project lifecycle state serialization (#709 MUX-LIFECYCLE-UI-PROJECTS).

Tests the hybrid status/lifecycle model for Project - verifying that lifecycle_state
is optional and correctly serialized when present.
"""

from datetime import datetime, timezone

import pytest

from services.domain.models import Project
from services.mux.lifecycle import LifecycleState


class TestProjectLifecycleState:
    """Tests for Project.lifecycle_state field and serialization."""

    def test_project_lifecycle_state_defaults_to_none(self):
        """Project should have no lifecycle_state by default (Lifecycle Optionality)."""
        project = Project(
            id="proj-123",
            owner_id="user-456",
            name="Test Project",
        )
        assert project.lifecycle_state is None

    def test_project_can_have_lifecycle_state(self):
        """Project can be created with a lifecycle_state."""
        project = Project(
            id="proj-123",
            owner_id="user-456",
            name="Test Project",
            lifecycle_state=LifecycleState.RATIFIED,
        )
        assert project.lifecycle_state == LifecycleState.RATIFIED

    def test_to_dict_excludes_lifecycle_when_none(self):
        """to_dict() should not include lifecycle_state when None."""
        project = Project(
            id="proj-123",
            owner_id="user-456",
            name="Test Project",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        result = project.to_dict()
        assert "lifecycle_state" not in result

    def test_to_dict_includes_lifecycle_when_present(self):
        """to_dict() should include lifecycle_state when set."""
        project = Project(
            id="proj-123",
            owner_id="user-456",
            name="Test Project",
            lifecycle_state=LifecycleState.RATIFIED,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        result = project.to_dict()
        assert "lifecycle_state" in result
        assert result["lifecycle_state"] == "ratified"

    def test_to_dict_serializes_all_lifecycle_states(self):
        """to_dict() should correctly serialize all LifecycleState values."""
        test_cases = [
            (LifecycleState.EMERGENT, "emergent"),
            (LifecycleState.DERIVED, "derived"),
            (LifecycleState.NOTICED, "noticed"),
            (LifecycleState.PROPOSED, "proposed"),
            (LifecycleState.RATIFIED, "ratified"),
            (LifecycleState.DEPRECATED, "deprecated"),
            (LifecycleState.ARCHIVED, "archived"),
            (LifecycleState.COMPOSTED, "composted"),
        ]

        for state, expected_value in test_cases:
            project = Project(
                id="proj-123",
                owner_id="user-456",
                name="Test Project",
                lifecycle_state=state,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            result = project.to_dict()
            assert result["lifecycle_state"] == expected_value, f"Failed for {state}"


class TestProjectHybridModel:
    """Tests verifying the hybrid status/lifecycle model."""

    def test_project_can_have_archived_status_without_lifecycle(self):
        """is_archived flag works independently of lifecycle_state."""
        project = Project(
            id="proj-123",
            owner_id="user-456",
            name="Test Project",
            is_archived=True,
            lifecycle_state=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        assert project.is_archived is True
        assert project.lifecycle_state is None
        result = project.to_dict()
        assert result["is_archived"] is True
        assert "lifecycle_state" not in result

    def test_project_can_have_both_archived_and_lifecycle(self):
        """is_archived and lifecycle_state can coexist (different concerns)."""
        project = Project(
            id="proj-123",
            owner_id="user-456",
            name="Test Project",
            is_archived=True,
            lifecycle_state=LifecycleState.ARCHIVED,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        assert project.is_archived is True
        assert project.lifecycle_state == LifecycleState.ARCHIVED
        result = project.to_dict()
        assert result["is_archived"] is True
        assert result["lifecycle_state"] == "archived"

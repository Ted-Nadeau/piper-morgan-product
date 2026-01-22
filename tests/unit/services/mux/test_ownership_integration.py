"""
Tests for OwnershipMetadata integration with domain models.

Part of #435 MUX-TECH-PHASE3-OWNERSHIP.

These tests verify that ownership metadata can be properly attached
to domain models and tracks Piper's relationship to objects.
"""

from datetime import datetime
from uuid import uuid4

import pytest

from services.domain.models import Conversation, Project, Todo
from services.mux.ownership import OwnershipCategory, OwnershipMetadata


class TestTodoOwnership:
    """Test ownership integration with Todo model."""

    def test_todo_has_mux_ownership_field(self):
        """Todo model has mux_ownership field."""
        todo = Todo(text="Test todo")
        assert hasattr(todo, "mux_ownership")
        assert todo.mux_ownership is None  # Default is None

    def test_todo_with_native_ownership(self):
        """Todo can be assigned native ownership (user-created)."""
        ownership = OwnershipMetadata.native(source="user-input")
        todo = Todo(
            text="User created todo",
            mux_ownership=ownership,
        )
        assert todo.mux_ownership is not None
        assert todo.mux_ownership.category == OwnershipCategory.NATIVE
        assert todo.mux_ownership.confidence == 1.0

    def test_todo_to_dict_includes_ownership(self):
        """Todo.to_dict() includes ownership when set."""
        ownership = OwnershipMetadata.native(source="user-input")
        todo = Todo(
            text="Test todo",
            mux_ownership=ownership,
        )
        data = todo.to_dict()
        assert "mux_ownership" in data
        assert data["mux_ownership"]["category"] == "native"
        assert data["mux_ownership"]["source"] == "user-input"

    def test_todo_to_dict_handles_none_ownership(self):
        """Todo.to_dict() handles None ownership gracefully."""
        todo = Todo(text="Test todo")
        data = todo.to_dict()
        assert "mux_ownership" in data
        assert data["mux_ownership"] is None


class TestConversationOwnership:
    """Test ownership integration with Conversation model."""

    def test_conversation_has_mux_ownership_field(self):
        """Conversation model has mux_ownership field."""
        conv = Conversation()
        assert hasattr(conv, "mux_ownership")
        assert conv.mux_ownership is None

    def test_conversation_with_native_ownership(self):
        """Conversation can be assigned native ownership (Piper-managed)."""
        ownership = OwnershipMetadata.native(source="piper-conversation")
        conv = Conversation(
            user_id=uuid4(),
            mux_ownership=ownership,
        )
        assert conv.mux_ownership.category == OwnershipCategory.NATIVE
        assert conv.mux_ownership.source == "piper-conversation"

    def test_conversation_to_dict_includes_ownership(self):
        """Conversation.to_dict() includes ownership when set."""
        ownership = OwnershipMetadata.native(source="piper")
        conv = Conversation(
            user_id=uuid4(),
            mux_ownership=ownership,
        )
        data = conv.to_dict()
        assert "mux_ownership" in data
        assert data["mux_ownership"]["category"] == "native"


class TestProjectOwnership:
    """Test ownership integration with Project model."""

    def test_project_has_mux_ownership_field(self):
        """Project model has mux_ownership field."""
        project = Project(name="Test Project")
        assert hasattr(project, "mux_ownership")
        assert project.mux_ownership is None

    def test_project_with_native_ownership(self):
        """Project can be assigned native ownership."""
        ownership = OwnershipMetadata.native(source="user-created")
        project = Project(
            name="My Project",
            description="A test project",
            mux_ownership=ownership,
        )
        assert project.mux_ownership.category == OwnershipCategory.NATIVE
        assert project.mux_ownership.confidence == 1.0

    def test_project_to_dict_includes_ownership(self):
        """Project.to_dict() includes ownership when set."""
        ownership = OwnershipMetadata.native(source="user-created")
        project = Project(
            name="My Project",
            mux_ownership=ownership,
        )
        data = project.to_dict()
        assert "mux_ownership" in data
        assert data["mux_ownership"]["category"] == "native"


class TestOwnershipCategories:
    """Test different ownership categories with domain models."""

    def test_native_for_user_created_todo(self):
        """User-created todos should be NATIVE."""
        ownership = OwnershipMetadata.native(source="user-input")
        todo = Todo(text="Buy groceries", mux_ownership=ownership)

        assert todo.mux_ownership.category == OwnershipCategory.NATIVE
        assert todo.mux_ownership.can_modify is True
        assert todo.mux_ownership.requires_verification is False

    def test_federated_for_external_todo(self):
        """Todos synced from external sources should be FEDERATED."""
        ownership = OwnershipMetadata.federated(source="github")
        todo = Todo(
            text="Fix bug #123",
            external_refs={"github_issue": "123"},
            mux_ownership=ownership,
        )

        assert todo.mux_ownership.category == OwnershipCategory.FEDERATED
        assert todo.mux_ownership.can_modify is False
        assert todo.mux_ownership.requires_verification is True

    def test_synthetic_for_derived_todo(self):
        """Piper-inferred todos should be SYNTHETIC."""
        ownership = OwnershipMetadata.synthetic(
            source="piper-inference",
            derived_from=["meeting-notes-123"],
            transformation="extract-action-items",
        )
        todo = Todo(
            text="Follow up on budget discussion",
            creation_intent="extracted_from_meeting",
            mux_ownership=ownership,
        )

        assert todo.mux_ownership.category == OwnershipCategory.SYNTHETIC
        assert todo.mux_ownership.requires_verification is True
        assert "meeting-notes-123" in todo.mux_ownership.derived_from


class TestOwnershipTransitionFlow:
    """Test ownership transitions with domain models."""

    def test_todo_from_github_to_confirmed(self):
        """
        Test flow: GitHub issue -> Piper analysis -> User confirmed.

        1. FEDERATED: Observed from GitHub
        2. SYNTHETIC: Piper derives priority/status
        3. NATIVE: User confirms and claims ownership
        """
        # Step 1: Observe from GitHub (FEDERATED)
        github_ownership = OwnershipMetadata.federated(source="github")
        todo = Todo(
            text="Critical bug in auth flow",
            external_refs={"github_issue": "456"},
            mux_ownership=github_ownership,
        )
        assert todo.mux_ownership.category == OwnershipCategory.FEDERATED

        # Step 2: Piper analyzes and infers priority (SYNTHETIC)
        analyzed = todo.mux_ownership.derive(
            transformation="priority-analysis",
            new_source="piper-analysis",
        )
        # Note: In real code, you'd update the todo or create analysis object
        assert analyzed.category == OwnershipCategory.SYNTHETIC
        assert "github" in analyzed.derived_from

        # Step 3: User confirms and takes ownership (NATIVE)
        confirmed = analyzed.promote_to_native(reason="user_claimed")
        assert confirmed.category == OwnershipCategory.NATIVE
        assert confirmed.confidence == 1.0
        assert "promoted_to_native:user_claimed" in confirmed.transformation_chain

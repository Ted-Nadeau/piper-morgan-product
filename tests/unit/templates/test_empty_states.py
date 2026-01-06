"""Tests for empty state copy in view templates (#548).

Tests verify that template empty states use voice guide copy to demonstrate
Piper's conversational grammar per Issue #548 FTUX requirements.
"""

from pathlib import Path

import pytest


class TestEmptyStateCopy:
    """Verify empty states use voice guide copy."""

    @pytest.fixture
    def todos_template_content(self) -> str:
        """Load todos.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "todos.html"
        return template_path.read_text()

    @pytest.fixture
    def projects_template_content(self) -> str:
        """Load projects.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "projects.html"
        return template_path.read_text()

    @pytest.fixture
    def files_template_content(self) -> str:
        """Load files.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "files.html"
        return template_path.read_text()

    @pytest.fixture
    def lists_template_content(self) -> str:
        """Load lists.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "lists.html"
        return template_path.read_text()

    def test_empty_state_copy_todos(self, todos_template_content):
        """Todos empty state uses voice guide copy."""
        assert "No todos yet" in todos_template_content
        assert 'Say "add a todo' in todos_template_content
        # Verify both static and JS-rendered locations
        assert todos_template_content.count("No todos yet") >= 2

    def test_empty_state_copy_projects(self, projects_template_content):
        """Projects empty state uses voice guide copy."""
        assert "No projects set up yet" in projects_template_content
        assert "create a project called" in projects_template_content
        # Verify both static and JS-rendered locations
        assert projects_template_content.count("No projects set up yet") >= 2

    def test_empty_state_copy_files(self, files_template_content):
        """Files empty state uses voice guide copy."""
        assert "No documents in your knowledge base" in files_template_content
        assert "upload files" in files_template_content.lower()
        # Verify both static and JS-rendered locations
        assert files_template_content.count("No documents in your knowledge base") >= 2

    def test_empty_state_copy_lists(self, lists_template_content):
        """Lists empty state uses voice guide copy."""
        assert "No lists yet" in lists_template_content
        assert "create a list called" in lists_template_content
        # Verify both static and JS-rendered locations
        assert lists_template_content.count("No lists yet") >= 2

    def test_empty_state_demonstrates_piper_grammar(self, todos_template_content):
        """Empty states show how to talk to Piper."""
        # Should demonstrate conversational command pattern
        assert 'Say "' in todos_template_content


class TestTodosAllCompleteState:
    """Verify todos 'all complete' state exists."""

    @pytest.fixture
    def todos_template_content(self) -> str:
        """Load todos.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "todos.html"
        return template_path.read_text()

    def test_all_complete_state_exists(self, todos_template_content):
        """Todos template includes 'all caught up' state."""
        assert "All caught up" in todos_template_content
        assert "Your todo list is clear" in todos_template_content

"""
Unit tests for QueryResponseFormatter

Tests comprehensive response formatting for various QueryRouter response types.
"""

import pytest

from services.api.query_response_formatter import QueryResponseFormatter


class TestQueryResponseFormatter:
    """Test response formatting for different QueryRouter response types"""

    @pytest.mark.smoke
    def test_format_string_response(self):
        """Test formatting of string responses (degradation messages)"""
        # Degradation message
        result = QueryResponseFormatter.format_query_response(
            "Database temporarily unavailable. Please ensure Docker is running or try again later.",
            "list_projects",
        )
        assert (
            result
            == "Database temporarily unavailable. Please ensure Docker is running or try again later."
        )

        # Regular conversation response
        result = QueryResponseFormatter.format_query_response(
            "Hello! I'm Piper Morgan.", "get_greeting"
        )
        assert result == "Hello! I'm Piper Morgan."

    @pytest.mark.smoke
    def test_format_dict_response_error(self):
        """Test formatting of dictionary error responses from file services"""
        error_response = {
            "success": False,
            "error": "Unable to read file contents. File service temporarily unavailable.",
            "suggestion": "Please check that the file exists and try again in a few moments.",
            "fallback_available": True,
            "fallback_action": "read_file_contents",
        }

        result = QueryResponseFormatter.format_query_response(error_response, "summarize_file")
        expected = "Unable to read file contents. File service temporarily unavailable. Please check that the file exists and try again in a few moments. You can read_file_contents."
        assert result == expected

    @pytest.mark.smoke
    def test_format_dict_response_no_results(self):
        """Test formatting of dictionary responses with no results"""
        no_results_response = {
            "success": False,
            "error": "Unable to search files. Search service temporarily unavailable.",
            "suggestion": "File search is temporarily unavailable. Please try again shortly.",
            "results": [],
            "query": "search temporarily unavailable",
        }

        result = QueryResponseFormatter.format_query_response(no_results_response, "search_files")
        expected = "Unable to search files. Search service temporarily unavailable. File search is temporarily unavailable. Please try again shortly."
        assert result == expected

    @pytest.mark.smoke
    def test_format_dict_response_with_results(self):
        """Test formatting of dictionary responses with search results"""
        results_response = {
            "success": True,
            "results": [
                {"filename": "project-plan.md", "score": 0.95},
                {"filename": "requirements.txt", "score": 0.87},
                {"filename": "architecture.md", "score": 0.82},
            ],
            "query": "project documentation",
        }

        result = QueryResponseFormatter.format_query_response(results_response, "search_files")
        expected = "Found 3 results for 'project documentation'. Here are the matches: project-plan.md, requirements.txt, architecture.md"
        assert result == expected

    @pytest.mark.smoke
    def test_format_dict_response_single_result(self):
        """Test formatting of dictionary responses with single result"""
        single_result_response = {
            "success": True,
            "results": [{"filename": "project-plan.md", "score": 0.95}],
            "query": "project plan",
        }

        result = QueryResponseFormatter.format_query_response(
            single_result_response, "find_documents"
        )
        expected = "Found 1 result for 'project plan': project-plan.md"
        assert result == expected

    @pytest.mark.smoke
    def test_format_dict_response_message_field(self):
        """Test formatting of dictionary responses with message field"""
        message_response = {
            "message": "File contents retrieved successfully",
            "content": "This is the file content...",
            "metadata": {"size": 1024},
        }

        result = QueryResponseFormatter.format_query_response(
            message_response, "read_file_contents"
        )
        expected = "File contents retrieved successfully"
        assert result == expected

    @pytest.mark.smoke
    def test_format_list_response_projects(self):
        """Test formatting of list responses for projects"""

        # Mock project objects with to_dict method
        class MockProject:
            def __init__(self, name):
                self.name = name

            def to_dict(self):
                return {"name": self.name, "id": f"proj-{self.name.lower()}"}

        projects = [MockProject("Web App"), MockProject("Mobile App"), MockProject("API Service")]

        result = QueryResponseFormatter.format_query_response(projects, "list_projects")
        expected = "I found 3 projects: Web App, Mobile App, API Service"
        assert result == expected

    @pytest.mark.smoke
    def test_format_list_response_empty(self):
        """Test formatting of empty list responses"""
        result = QueryResponseFormatter.format_query_response([], "list_projects")
        expected = "No items found for list_projects."
        assert result == expected

    @pytest.mark.smoke
    def test_format_list_response_generic(self):
        """Test formatting of generic list responses"""
        results = ["result1", "result2", "result3", "result4", "result5"]

        result = QueryResponseFormatter.format_query_response(results, "search_content")
        expected = "Found 5 results for search_content. Here are the first few: result1, result2, result3..."
        assert result == expected

    @pytest.mark.smoke
    def test_format_object_response_with_to_dict(self):
        """Test formatting of single object responses"""

        class MockProject:
            def to_dict(self):
                return {"name": "Test Project", "id": "proj-123"}

        project = MockProject()
        result = QueryResponseFormatter.format_query_response(project, "get_project")
        expected = "Found project: Test Project"
        assert result == expected

    @pytest.mark.smoke
    def test_format_object_response_generic(self):
        """Test formatting of generic object responses"""

        class MockObject:
            def __init__(self):
                self.data = "some data"

        obj = MockObject()
        result = QueryResponseFormatter.format_query_response(obj, "get_status")
        expected = "Found the requested get_status information."
        assert result == expected

    @pytest.mark.smoke
    def test_format_object_response_primitive(self):
        """Test formatting of primitive object responses"""
        result = QueryResponseFormatter.format_query_response(42, "count_projects")
        expected = "42"
        assert result == expected

    @pytest.mark.smoke
    def test_is_degradation_response_string(self):
        """Test degradation detection for string responses"""
        # Degradation messages
        assert QueryResponseFormatter.is_degradation_response("Database temporarily unavailable")
        assert QueryResponseFormatter.is_degradation_response(
            "Service unavailable, try again later"
        )
        assert QueryResponseFormatter.is_degradation_response("Please ensure Docker is running")

        # Normal messages
        assert not QueryResponseFormatter.is_degradation_response("Hello! I'm Piper Morgan.")
        assert not QueryResponseFormatter.is_degradation_response("I found 3 projects")

    @pytest.mark.smoke
    def test_is_degradation_response_dict(self):
        """Test degradation detection for dictionary responses"""
        # Error response
        error_response = {"success": False, "error": "Service unavailable"}
        assert QueryResponseFormatter.is_degradation_response(error_response)

        # Success response
        success_response = {"success": True, "results": []}
        assert not QueryResponseFormatter.is_degradation_response(success_response)

        # No success field
        other_response = {"message": "Hello"}
        assert not QueryResponseFormatter.is_degradation_response(other_response)

    @pytest.mark.smoke
    def test_extract_user_action_hint(self):
        """Test extraction of actionable guidance from responses"""
        # Docker hint
        docker_msg = "Database temporarily unavailable. Please ensure Docker is running."
        hint = QueryResponseFormatter.extract_user_action_hint(docker_msg)
        assert hint == "Please check your database connection."

        # Try again hint
        retry_msg = "Service unavailable. Please try again later."
        hint = QueryResponseFormatter.extract_user_action_hint(retry_msg)
        assert hint == "Please try your request again in a moment."

        # Dictionary with suggestion
        dict_response = {"success": False, "suggestion": "Check your file permissions"}
        hint = QueryResponseFormatter.extract_user_action_hint(dict_response)
        assert hint == "Check your file permissions"

        # Generic fallback
        hint = QueryResponseFormatter.extract_user_action_hint("Some other message")
        assert hint == "Please try again later."

    @pytest.mark.smoke
    def test_error_handling_formatting(self):
        """Test that formatter handles errors gracefully"""

        # Simulate an error during formatting
        class BadObject:
            def to_dict(self):
                raise Exception("Simulated error")

        bad_obj = BadObject()
        result = QueryResponseFormatter.format_query_response(bad_obj, "test_action")
        expected = "I processed your test_action request. The response is available."
        assert result == expected

    @pytest.mark.smoke
    def test_backward_compatibility_project_lists(self):
        """Test backward compatibility with existing project list handling"""
        # Test with project dicts (existing format)
        project_dicts = [
            {"name": "Project A", "id": "proj-a"},
            {"name": "Project B", "id": "proj-b"},
        ]

        result = QueryResponseFormatter.format_query_response(project_dicts, "list_projects")
        expected = "I found 2 projects: Project A, Project B"
        assert result == expected

        # Test with string representation fallback
        string_projects = ["Project A", "Project B"]
        result = QueryResponseFormatter.format_query_response(string_projects, "list_projects")
        expected = "I found 2 projects: Project A, Project B"
        assert result == expected

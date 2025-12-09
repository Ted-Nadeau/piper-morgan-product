"""Tests for UserFriendlyErrorService"""

from unittest.mock import Mock

import pytest

from services.ui_messages.user_friendly_errors import (
    ErrorSeverity,
    UserFriendlyErrorService,
    get_conversational_error_message,
    make_error_user_friendly,
)


class TestUserFriendlyErrorService:
    """Test user-friendly error message conversion"""

    @pytest.fixture
    def error_service(self):
        """UserFriendlyErrorService instance for testing"""
        return UserFriendlyErrorService()

    @pytest.mark.smoke
    def test_database_connection_error(self, error_service):
        """Test database connection error conversion"""
        error = Exception("connection to database refused")
        result = error_service.make_user_friendly(error)

        assert "can't connect to the database" in result["message"]
        assert "keep trying" in result["recovery"]
        assert result["severity"] == ErrorSeverity.WARNING
        assert result["category"] == "database"

    @pytest.mark.smoke
    def test_database_table_not_found(self, error_service):
        """Test database table not found error"""
        error = Exception("relation 'users' does not exist")
        result = error_service.make_user_friendly(error)

        assert "trouble accessing the database" in result["message"]
        assert "reconnecting" in result["message"]
        assert result["severity"] == ErrorSeverity.ERROR
        assert result["category"] == "database"

    @pytest.mark.smoke
    def test_http_404_error(self, error_service):
        """Test HTTP 404 error conversion"""
        error = Exception("HTTP 404 Not Found")
        result = error_service.make_user_friendly(error)

        assert "couldn't find what you're looking for" in result["message"]
        assert "check if the item still exists" in result["recovery"]
        assert result["severity"] == ErrorSeverity.INFO
        assert result["category"] == "api"

    @pytest.mark.smoke
    def test_http_401_unauthorized(self, error_service):
        """Test HTTP 401 unauthorized error"""
        error = Exception("HTTP 401 Unauthorized")
        result = error_service.make_user_friendly(error)

        assert "need permission" in result["message"]
        assert "check your login" in result["recovery"]
        assert result["severity"] == ErrorSeverity.WARNING
        assert result["category"] == "auth"

    @pytest.mark.smoke
    def test_github_rate_limit_error(self, error_service):
        """Test GitHub rate limit error"""
        error = Exception("GitHub API rate limit exceeded")
        result = error_service.make_user_friendly(error)

        assert "GitHub is asking me to slow down" in result["message"]
        assert "wait and try again" in result["recovery"]
        assert result["severity"] == ErrorSeverity.INFO
        assert result["category"] == "github"

    @pytest.mark.smoke
    def test_file_not_found_error(self, error_service):
        """Test file not found error"""
        error = FileNotFoundError("No such file or directory: /path/to/file")
        result = error_service.make_user_friendly(error)

        assert "can't find that file" in result["message"]
        assert "check the file path" in result["recovery"]
        assert result["severity"] == ErrorSeverity.INFO
        assert result["category"] == "file"

    @pytest.mark.smoke
    def test_permission_denied_error(self, error_service):
        """Test permission denied error"""
        error = PermissionError("Permission denied")
        result = error_service.make_user_friendly(error)

        assert "don't have permission" in result["message"]
        assert "check the file permissions" in result["recovery"]
        assert result["severity"] == ErrorSeverity.WARNING
        assert result["category"] == "file"

    @pytest.mark.smoke
    def test_timeout_error(self, error_service):
        """Test timeout error"""
        error = TimeoutError("Operation timed out after 30 seconds")
        result = error_service.make_user_friendly(error)

        assert "taking longer than expected" in result["message"]
        assert "keep working on it" in result["recovery"]
        assert result["severity"] == ErrorSeverity.WARNING
        assert result["category"] == "timeout"

    @pytest.mark.smoke
    def test_validation_error(self, error_service):
        """Test validation error"""
        error = ValueError("required field 'name' is missing")
        result = error_service.make_user_friendly(error)

        assert "required information is missing" in result["message"]
        assert "provide all the necessary details" in result["recovery"]
        assert result["severity"] == ErrorSeverity.INFO
        assert result["category"] == "validation"

    @pytest.mark.smoke
    def test_error_with_context(self, error_service):
        """Test error message with context"""
        error = Exception("connection refused")
        result = error_service.make_user_friendly(error, context="fetching GitHub issues")

        assert "While fetching github issues:" in result["message"]
        assert "can't connect to the database" in result["message"]

    @pytest.mark.smoke
    def test_error_with_user_action(self, error_service):
        """Test error message with user action context"""
        error = Exception("HTTP 404 Not Found")
        result = error_service.make_user_friendly(error, user_action="search")

        assert "couldn't find what you're looking for" in result["message"]
        assert "Try different search terms" in result["recovery"]

    @pytest.mark.smoke
    def test_unknown_error_fallback(self, error_service):
        """Test fallback for unknown error patterns"""
        error = Exception("Some completely unknown error message")
        result = error_service.make_user_friendly(error)

        assert "Something unexpected happened" in result["message"]
        assert "try again in a moment" in result["recovery"]
        assert result["severity"] == ErrorSeverity.ERROR
        assert result["category"] == "unknown"

    @pytest.mark.smoke
    def test_format_error_response_basic(self, error_service):
        """Test basic error response formatting"""
        error = Exception("HTTP 404 Not Found")
        response = error_service.format_error_response(error)

        assert "user_message" in response
        assert "recovery_suggestion" in response
        assert "severity" in response
        assert "category" in response
        assert "technical_error" not in response  # Should not include by default

    @pytest.mark.smoke
    def test_format_error_response_with_technical_details(self, error_service):
        """Test error response with technical details"""
        error = ValueError("Some validation error")
        response = error_service.format_error_response(error, include_technical_details=True)

        assert "technical_error" in response
        assert "error_type" in response
        assert response["technical_error"] == "Some validation error"
        assert response["error_type"] == "ValueError"

    @pytest.mark.smoke
    def test_conversational_error_info_severity(self, error_service):
        """Test conversational error for INFO severity"""
        error = Exception("HTTP 404 Not Found")
        message = error_service.get_conversational_error(error)

        # INFO severity should be direct
        assert not message.startswith("Hmm,")
        assert not message.startswith("I'm sorry,")
        assert "couldn't find what you're looking for" in message

    @pytest.mark.smoke
    def test_conversational_error_warning_severity(self, error_service):
        """Test conversational error for WARNING severity"""
        error = Exception("connection refused")
        message = error_service.get_conversational_error(error)

        # WARNING severity should start with "Hmm,"
        assert message.startswith("Hmm,")
        assert "can't connect to the database" in message

    @pytest.mark.smoke
    def test_conversational_error_error_severity(self, error_service):
        """Test conversational error for ERROR severity"""
        error = Exception("relation 'users' does not exist")
        message = error_service.get_conversational_error(error)

        # ERROR severity should start with "I'm sorry,"
        assert message.startswith("I'm sorry,")
        assert "trouble accessing the database" in message

    @pytest.mark.smoke
    def test_convenience_function_make_error_user_friendly(self):
        """Test convenience function for making errors user-friendly"""
        error = Exception("HTTP 401 Unauthorized")
        result = make_error_user_friendly(error, context="accessing GitHub")

        assert "need permission" in result["message"]
        assert "While accessing github:" in result["message"]

    @pytest.mark.smoke
    def test_convenience_function_get_conversational_error(self):
        """Test convenience function for conversational errors"""
        error = Exception("operation timed out")
        message = get_conversational_error_message(error)

        assert isinstance(message, str)
        assert "taking longer than expected" in message

    @pytest.mark.smoke
    def test_multiple_pattern_matches(self, error_service):
        """Test that first matching pattern is used"""
        # This error could match both timeout and HTTP patterns
        error = Exception("HTTP request timeout after 30 seconds")
        result = error_service.make_user_friendly(error)

        # Should match timeout pattern (appears first in patterns dict)
        assert result["category"] == "timeout"
        assert "taking longer than expected" in result["message"]

    @pytest.mark.smoke
    def test_case_insensitive_matching(self, error_service):
        """Test that pattern matching is case insensitive"""
        error = Exception("PERMISSION DENIED")
        result = error_service.make_user_friendly(error)

        assert result["category"] == "file"
        assert "don't have permission" in result["message"]

    @pytest.mark.smoke
    def test_contextual_suggestions_integration(self, error_service):
        """Test that contextual suggestions are properly integrated"""
        error = Exception("HTTP 404 Not Found")

        # Test different user actions
        create_result = error_service.make_user_friendly(error, user_action="create")
        assert "Try creating with less data" in create_result["recovery"]

        update_result = error_service.make_user_friendly(error, user_action="update")
        assert "Make sure the item still exists" in update_result["recovery"]

        search_result = error_service.make_user_friendly(error, user_action="search")
        assert "Try different search terms" in search_result["recovery"]

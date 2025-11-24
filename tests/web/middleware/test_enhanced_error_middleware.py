"""Tests for EnhancedErrorMiddleware"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import Request
from fastapi.responses import JSONResponse

from services.api.errors import APIError, ValidationError
from web.middleware.enhanced_error_middleware import EnhancedErrorMiddleware


class TestEnhancedErrorMiddleware:
    """Test enhanced error middleware functionality"""

    @pytest.fixture
    def middleware(self):
        """EnhancedErrorMiddleware instance for testing"""
        app = Mock()
        return EnhancedErrorMiddleware(app, include_technical_details=True)

    @pytest.fixture
    def mock_request(self):
        """Mock request for testing"""
        request = Mock(spec=Request)
        request.url.path = "/api/v1/intent"
        request.method = "POST"
        request.state.correlation = {
            "request_id": "test-request-123",
            "session_id": "test-session-456",
        }
        return request

    @pytest.mark.asyncio
    async def test_successful_request_passthrough(self, middleware, mock_request):
        """Test that successful requests pass through unchanged"""

        # Mock successful call_next
        mock_response = Mock()
        call_next = AsyncMock(return_value=mock_response)

        result = await middleware.dispatch(mock_request, call_next)

        assert result == mock_response
        call_next.assert_called_once_with(mock_request)

    @pytest.mark.asyncio
    async def test_api_error_handling(self, middleware, mock_request):
        """Test handling of structured API errors"""

        # Create API error
        api_error = ValidationError(field="test_field", details={"issue": "invalid format"})

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=api_error)

        result = await middleware.dispatch(mock_request, call_next)

        assert isinstance(result, JSONResponse)
        assert result.status_code == 422

        # Check response content
        content = result.body.decode()
        assert "error" in content
        assert "message" in content
        assert "recovery_suggestion" in content
        assert "severity" in content
        assert "category" in content

    @pytest.mark.asyncio
    async def test_generic_exception_handling(self, middleware, mock_request):
        """Test handling of generic exceptions"""

        # Create generic exception
        generic_error = ValueError("Invalid input data")

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=generic_error)

        result = await middleware.dispatch(mock_request, call_next)

        assert isinstance(result, JSONResponse)
        assert result.status_code == 422  # ValueError maps to 422

        # Check response content
        content = result.body.decode()
        assert "error" in content
        assert "message" in content
        assert "recovery_suggestion" in content

    @pytest.mark.asyncio
    async def test_database_error_user_friendly_message(self, middleware, mock_request):
        """Test that database errors get user-friendly messages"""

        # Create database-like error
        db_error = Exception("relation 'users' does not exist")

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=db_error)

        result = await middleware.dispatch(mock_request, call_next)

        assert isinstance(result, JSONResponse)

        # Parse response content
        import json

        content = json.loads(result.body.decode())

        assert "trouble accessing the database" in content["message"]
        assert "reconnecting" in content["message"]
        assert content["category"] == "database"

    @pytest.mark.asyncio
    async def test_github_error_user_friendly_message(self, middleware):
        """Test that GitHub errors get appropriate messages"""

        # Create GitHub request
        github_request = Mock(spec=Request)
        github_request.url.path = "/api/v1/github/issues"
        github_request.method = "GET"
        github_request.state.correlation = {"request_id": "test-123"}

        # Create GitHub error
        github_error = Exception("GitHub API rate limit exceeded")

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=github_error)

        result = await middleware.dispatch(github_request, call_next)

        assert isinstance(result, JSONResponse)

        # Parse response content
        import json

        content = json.loads(result.body.decode())

        assert "GitHub is asking me to slow down" in content["message"]
        assert content["category"] == "github"

    @pytest.mark.asyncio
    async def test_context_extraction_from_url(self, middleware):
        """Test context extraction from different URL paths"""

        test_cases = [
            ("/api/v1/intent", "processing your request"),
            ("/api/v1/github/issues", "accessing GitHub"),
            ("/api/v1/slack/send", "connecting to Slack"),
            ("/api/v1/knowledge/search", "searching the knowledge base"),
            ("/api/v1/workflow/run", "running a workflow"),
            ("/api/v1/auth/login", "handling authentication"),
        ]

        for path, expected_context in test_cases:
            request = Mock(spec=Request)
            request.url.path = path
            request.method = "GET"
            request.state.correlation = {}

            context = middleware._extract_context_from_request(request)
            assert context == expected_context

    @pytest.mark.asyncio
    async def test_user_action_extraction(self, middleware):
        """Test user action extraction from HTTP methods"""

        test_cases = [
            ("GET", "/api/v1/list", "search"),
            ("GET", "/api/v1/items", "list"),
            ("POST", "/api/v1/create", "create"),
            ("PUT", "/api/v1/update", "update"),
            ("PATCH", "/api/v1/modify", "update"),
            ("DELETE", "/api/v1/remove", "delete"),
        ]

        for method, path, expected_action in test_cases:
            request = Mock(spec=Request)
            request.method = method
            request.url.path = path

            action = middleware._extract_user_action_from_request(request)
            assert action == expected_action

    @pytest.mark.asyncio
    async def test_status_code_determination(self, middleware):
        """Test HTTP status code determination for different exception types"""

        test_cases = [
            (FileNotFoundError("File not found"), 404),
            (PermissionError("Permission denied"), 403),
            (ValueError("Invalid value"), 422),
            (TimeoutError("Operation timed out"), 504),
            (Exception("Generic error"), 500),
        ]

        for exception, expected_status in test_cases:
            enhanced_error = {"category": "unknown", "severity": "error"}
            status_code = middleware._determine_status_code(exception, enhanced_error)
            assert status_code == expected_status

    @pytest.mark.asyncio
    async def test_technical_details_inclusion(self, middleware, mock_request):
        """Test that technical details are included when enabled"""

        # Create exception
        error = ValueError("Test error for technical details")

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=error)

        result = await middleware.dispatch(mock_request, call_next)

        # Parse response content
        import json

        content = json.loads(result.body.decode())

        assert "technical_details" in content
        assert "error_message" in content["technical_details"]
        assert "error_type" in content["technical_details"]
        assert content["technical_details"]["error_type"] == "ValueError"

    @pytest.mark.asyncio
    async def test_technical_details_exclusion(self, mock_request):
        """Test that technical details are excluded when disabled"""

        # Create middleware without technical details
        app = Mock()
        middleware = EnhancedErrorMiddleware(app, include_technical_details=False)

        # Create exception
        error = ValueError("Test error")

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=error)

        result = await middleware.dispatch(mock_request, call_next)

        # Parse response content
        import json

        content = json.loads(result.body.decode())

        assert "technical_details" not in content

    @pytest.mark.asyncio
    async def test_correlation_id_inclusion(self, middleware, mock_request):
        """Test that correlation IDs are included in responses"""

        # Create exception
        error = Exception("Test error")

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=error)

        result = await middleware.dispatch(mock_request, call_next)

        # Parse response content
        import json

        content = json.loads(result.body.decode())

        assert "request_id" in content
        assert content["request_id"] == "test-request-123"

    @pytest.mark.asyncio
    async def test_no_correlation_id_when_missing(self, middleware):
        """Test behavior when correlation ID is missing"""

        # Create request without correlation data
        request = Mock(spec=Request)
        request.url.path = "/api/v1/test"
        request.method = "GET"
        request.state.correlation = {}

        # Create exception
        error = Exception("Test error")

        # Mock call_next to raise the error
        call_next = AsyncMock(side_effect=error)

        result = await middleware.dispatch(request, call_next)

        # Parse response content
        import json

        content = json.loads(result.body.decode())

        assert "request_id" not in content

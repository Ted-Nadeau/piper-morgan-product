"""
PM-012: Real GitHub API Integration Test Configuration
Configuration and utilities for testing with actual GitHub API
"""

import os
from typing import Dict, Optional
from unittest.mock import Mock

import pytest

from services.integrations.github.github_agent import GitHubAgent


class GitHubTestConfig:
    """Configuration for GitHub API integration testing"""

    # Test repository configuration
    TEST_REPOSITORY = "test-org/test-repo"
    TEST_ISSUE_TITLE = "Test Issue from Piper Morgan"
    TEST_ISSUE_BODY = "This is a test issue created by Piper Morgan for integration testing."

    # Environment variable names
    GITHUB_TOKEN_ENV = "GITHUB_TOKEN"
    GITHUB_TEST_REPO_ENV = "GITHUB_TEST_REPO"
    GITHUB_TEST_ORG_ENV = "GITHUB_TEST_ORG"

    @classmethod
    def get_test_repository(cls) -> str:
        """Get test repository from environment or use default"""
        return os.getenv(cls.GITHUB_TEST_REPO_ENV, cls.TEST_REPOSITORY)

    @classmethod
    def get_github_token(cls) -> Optional[str]:
        """Get GitHub token from environment"""
        return os.getenv(cls.GITHUB_TOKEN_ENV)

    @classmethod
    def is_real_api_available(cls) -> bool:
        """Check if real GitHub API testing is available"""
        return bool(cls.get_github_token() and cls.get_test_repository())

    @classmethod
    def get_test_issue_data(cls) -> Dict[str, str]:
        """Get test issue data for integration testing"""
        return {
            "title": cls.TEST_ISSUE_TITLE,
            "body": cls.TEST_ISSUE_BODY,
            "labels": ["test", "piper-morgan", "integration"],
        }


class MockGitHubAgentFactory:
    """Factory for creating mock GitHub agents for testing"""

    @staticmethod
    def create_success_mock() -> Mock:
        """Create a mock GitHub agent that simulates successful operations"""
        mock_agent = Mock()
        mock_agent.create_issue_from_work_item = Mock()
        mock_agent.create_issue = Mock()
        mock_agent.test_connection = Mock()

        # Mock successful issue creation
        mock_agent.create_issue_from_work_item.return_value = {
            "id": 12345,
            "number": 42,
            "title": "Test Issue",
            "url": "https://github.com/test-org/test-repo/issues/42",
            "state": "open",
            "work_item_id": "test-work-item-123",
            "work_item_type": "bug",
            "work_item_priority": "high",
            "labels": ["bug", "test"],
        }

        # Mock successful connection test
        mock_agent.test_connection.return_value = {
            "success": True,
            "user": "test-user",
            "name": "Test User",
            "repos_count": 10,
        }

        return mock_agent

    @staticmethod
    def create_auth_failure_mock() -> Mock:
        """Create a mock GitHub agent that simulates authentication failure"""
        from services.api.errors import GitHubAuthFailedError

        mock_agent = Mock()
        mock_agent.create_issue_from_work_item = Mock()
        mock_agent.create_issue = Mock()
        mock_agent.test_connection = Mock()

        # Mock authentication failure
        mock_agent.create_issue_from_work_item.side_effect = GitHubAuthFailedError(
            details={"reason": "Invalid token"}
        )
        mock_agent.create_issue.side_effect = GitHubAuthFailedError(
            details={"reason": "Invalid token"}
        )
        mock_agent.test_connection.side_effect = GitHubAuthFailedError(
            details={"reason": "Invalid token"}
        )

        return mock_agent

    @staticmethod
    def create_rate_limit_mock() -> Mock:
        """Create a mock GitHub agent that simulates rate limit exceeded"""
        from services.api.errors import GitHubRateLimitError

        mock_agent = Mock()
        mock_agent.create_issue_from_work_item = Mock()
        mock_agent.create_issue = Mock()
        mock_agent.test_connection = Mock()

        # Mock rate limit error
        mock_agent.create_issue_from_work_item.side_effect = GitHubRateLimitError(retry_after=5)
        mock_agent.create_issue.side_effect = GitHubRateLimitError(retry_after=5)
        mock_agent.test_connection.side_effect = GitHubRateLimitError(retry_after=5)

        return mock_agent


def skip_if_no_real_api():
    """Decorator to skip tests if real GitHub API is not available"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not GitHubTestConfig.is_real_api_available():
                pytest.skip("Real GitHub API not available - set GITHUB_TOKEN and GITHUB_TEST_REPO")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def create_real_github_agent() -> Optional[GitHubAgent]:
    """Create a real GitHub agent for integration testing"""
    if not GitHubTestConfig.is_real_api_available():
        return None

    try:
        return GitHubAgent(token=GitHubTestConfig.get_github_token())
    except Exception as e:
        print(f"Failed to create real GitHub agent: {e}")
        return None


# Test fixtures for real API testing
@pytest.fixture
def real_github_agent():
    """Fixture for real GitHub agent (skips if not available)"""
    agent = create_real_github_agent()
    if agent is None:
        pytest.skip("Real GitHub API not available")
    return agent


@pytest.fixture
def test_repository():
    """Fixture for test repository name"""
    return GitHubTestConfig.get_test_repository()


@pytest.fixture
def test_issue_data():
    """Fixture for test issue data"""
    return GitHubTestConfig.get_test_issue_data()


# Utility functions for test data generation
def generate_test_work_item(title: str = None, issue_type: str = "task") -> Dict[str, any]:
    """Generate test work item data"""
    if title is None:
        title = f"Test {issue_type.title()} - {os.urandom(4).hex()}"

    return {
        "id": f"test-work-item-{os.urandom(8).hex()}",
        "title": title,
        "description": f"## Description\n\nThis is a test {issue_type} created by Piper Morgan for integration testing.\n\n## Acceptance Criteria\n\n- [ ] Test passes\n- [ ] Integration works correctly\n- [ ] Documentation updated",
        "type": issue_type,
        "priority": "medium",
        "labels": [issue_type, "test", "piper-morgan"],
        "assignee": None,
        "project_id": None,
        "source_system": "github",
        "external_id": "",
        "external_url": None,
        "metadata": {
            "original_prompt": f"Create a test {issue_type}",
            "extraction_method": "test",
            "test_run": True,
        },
    }


def cleanup_test_issues(agent: GitHubAgent, repository: str, test_label: str = "piper-morgan"):
    """Clean up test issues created during testing"""
    try:
        # This would require implementing issue listing and deletion
        # For now, this is a placeholder for cleanup functionality
        print(f"Cleanup: Would delete issues with label '{test_label}' from {repository}")
    except Exception as e:
        print(f"Cleanup failed: {e}")


# Test markers for different testing modes
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "real_api: mark test to run only with real GitHub API")
    config.addinivalue_line("markers", "mock_api: mark test to run only with mock GitHub API")
    config.addinivalue_line("markers", "integration: mark test as integration test")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on available API"""
    if not GitHubTestConfig.is_real_api_available():
        # Skip real API tests if GitHub token not available
        skip_real_api = pytest.mark.skip(reason="Real GitHub API not available")
        for item in items:
            if "real_api" in item.keywords:
                item.add_marker(skip_real_api)

    # Mark all tests in this file as integration tests
    for item in items:
        if "test_pm012_github" in item.nodeid:
            item.add_marker(pytest.mark.integration)

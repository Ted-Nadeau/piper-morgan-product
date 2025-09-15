"""
Test configuration fixtures for multi-user configuration testing.

This module provides test configurations for different users to validate
that the configuration system supports multiple users without data leakage.
"""

# Test configuration for Xian (current user)
XIAN_CONFIG = {
    "github": {
        "default_repository": "mediajunkie/piper-morgan-product",
        "owner": "mediajunkie",
        "pm_numbers": {"prefix": "PM-", "start_number": 1, "padding": 3},
    }
}

# Test configuration for Alice (different user)
ALICE_CONFIG = {
    "github": {
        "default_repository": "alice-corp/alice-project",
        "owner": "alice-corp",
        "pm_numbers": {"prefix": "TASK-", "start_number": 1000, "padding": 4},
    }
}

# Test configuration for Bob (another user)
BOB_CONFIG = {
    "github": {
        "default_repository": "bob-org/bob-system",
        "owner": "bob-org",
        "pm_numbers": {"prefix": "ISSUE-", "start_number": 5000, "padding": 5},
    }
}

# Test configuration for minimal setup
MINIMAL_CONFIG = {"github": {"default_repository": "test/test-repo", "owner": "test-user"}}

# Test configuration for edge cases
EDGE_CASE_CONFIG = {
    "github": {
        "default_repository": "very-long-organization-name/very-long-repository-name",
        "owner": "very-long-username",
        "pm_numbers": {"prefix": "VERY-LONG-PREFIX-", "start_number": 999999, "padding": 6},
    }
}

# Configuration validation test cases
VALID_CONFIGS = [XIAN_CONFIG, ALICE_CONFIG, BOB_CONFIG, MINIMAL_CONFIG, EDGE_CASE_CONFIG]

# Invalid configuration test cases
INVALID_CONFIGS = [
    # Missing required fields
    {"github": {}},
    {"github": {"default_repository": "test/repo"}},  # Missing owner
    {"github": {"owner": "test-user"}},  # Missing repository
    # Invalid repository format
    {"github": {"default_repository": "invalid-repo", "owner": "test"}},
    {"github": {"default_repository": "test/", "owner": "test"}},
    {"github": {"default_repository": "/test", "owner": "test"}},
    # Invalid PM number configuration
    {
        "github": {
            "default_repository": "test/repo",
            "owner": "test",
            "pm_numbers": {"prefix": "", "start_number": -1, "padding": 0},
        }
    },
]

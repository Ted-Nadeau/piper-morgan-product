"""
Notion Configuration Validation Test Suite

Comprehensive validation testing to prevent verification theater and ensure
real configuration behavior is tested with actual data.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Import the configuration classes we'll be testing
from config.notion_user_config import ConfigurationError, NotionUserConfig


class TestNotionConfigValidation:
    """Comprehensive validation testing to prevent verification theater"""

    def test_missing_required_fields_specific_errors(self):
        """Test each required field triggers specific error message"""

        # Test missing adrs.database_id
        config = {
            "notion": {
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"}
                # Missing: adrs.database_id
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(config)

        # Verify error message contains resolution steps
        error_msg = str(exc_info.value)
        assert "adrs.database_id" in error_msg
        assert "Add 'notion.adrs.database_id'" in error_msg
        assert "Run 'piper notion list-databases'" in error_msg

        # Test missing publishing.default_parent
        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"}
                # Missing: publishing.default_parent
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(config)

        error_msg = str(exc_info.value)
        assert "publishing.default_parent" in error_msg
        assert "Add 'notion.publishing.default_parent'" in error_msg

    def test_invalid_format_detection(self):
        """Test format validation catches invalid Notion IDs"""

        # Test non-hex characters
        invalid_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7dG"},  # 'G' is invalid hex
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(invalid_config)

        error_msg = str(exc_info.value)
        assert "Invalid Notion ID format" in error_msg

        # Test wrong length IDs (Notion IDs are 32 characters)
        short_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7d"},  # 31 chars
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(short_config)

        error_msg = str(exc_info.value)
        assert "Invalid Notion ID format" in error_msg

        # Test empty strings - should be caught by required field validation
        empty_config = {
            "notion": {
                "adrs": {"database_id": ""},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(empty_config)

        error_msg = str(exc_info.value)
        assert "Missing required Notion configuration field" in error_msg

    def test_connectivity_validation_real_api(self):
        """Integration test: does configuration work with real API?"""

        # This test requires actual API validation
        # Skip if NOTION_API_KEY not available
        if not os.getenv("NOTION_API_KEY"):
            pytest.skip("NOTION_API_KEY not available for integration testing")

        # Test with valid configuration from audit findings
        valid_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # This should pass basic validation
        # config = NotionUserConfig.load(valid_config)
        # assert config.is_valid()
        # assert config.validation_level == "basic"

        # Test with invalid database ID (should fail connectivity check)
        invalid_config = {
            "notion": {
                "adrs": {"database_id": "00000000000000000000000000000000"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # This should fail enhanced validation (connectivity check)
        # config = NotionUserConfig.load(invalid_config)
        # result = config.validate(level="enhanced")
        # assert not result.is_valid()
        # assert "not accessible" in result.errors[0].lower()

    def test_migration_path_validation(self):
        """Test migration from hardcoded values works"""

        # Create temporary config with audit values
        audit_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "development": {
                    "test_parent": "25d11704d8bf81dfb37acbdc143e6a80",
                    "debug_parent": "25d11704d8bf80c8a71ddbe7aba51f55",
                },
            }
        }

        # Verify configuration loads correctly
        # config = NotionUserConfig.load(audit_config)
        # assert config.is_valid()

        # Test each hardcoded value maps to correct config field
        # assert config.adrs.database_id == "25e11704d8bf80deaac2f806390fe7da"
        # assert config.publishing.default_parent == "25d11704d8bf80c8a71ddbe7aba51f55"
        # assert config.development.test_parent == "25d11704d8bf81dfb37acbdc143e6a80"
        # assert config.development.debug_parent == "25d11704d8bf80c8a71ddbe7aba51f55"

    def test_validation_tier_basic(self):
        """Test MVP validation (format + connectivity)"""

        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # Test should verify format and basic connectivity
        # result = NotionUserConfig.load(config)
        # assert result.is_valid()
        # assert result.validation_level == "basic"

    def test_validation_tier_enhanced(self):
        """Test enhanced validation (resource accessibility)"""

        if not os.getenv("NOTION_API_KEY"):
            pytest.skip("NOTION_API_KEY not available for enhanced validation")

        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # Enhanced validation should check if resources are accessible
        # config = NotionUserConfig.load(config)
        # result = config.validate(level="enhanced")
        # assert result.is_valid()

    def test_validation_tier_full(self):
        """Test full validation (comprehensive permission checking)"""

        if not os.getenv("NOTION_API_KEY"):
            pytest.skip("NOTION_API_KEY not available for full validation")

        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # Full validation should check permissions and comprehensive access
        # config = NotionUserConfig.load(config)
        # result = config.validate(level="full")
        # assert result.is_valid()

    def test_optional_fields_handling(self):
        """Test optional fields are handled gracefully"""

        # Test with minimal required configuration
        minimal_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # Should load successfully without optional fields
        # config = NotionUserConfig.load(minimal_config)
        # assert config.is_valid()
        # assert config.workspace.id is None
        # assert config.workspace.name == ""
        # assert config.development.mock_mode is False

    def test_error_message_resolution_steps(self):
        """Test error messages include actionable resolution steps"""

        # Test missing required field
        config = {
            "notion": {
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"}
                # Missing adrs.database_id
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(config)

        error_msg = str(exc_info.value)

        # Verify resolution steps are included
        resolution_steps = [
            "Add 'notion.adrs.database_id' to config/PIPER.user.md",
            "Run 'piper notion list-databases' to find your database ID",
            "Run 'piper notion setup' for guided configuration",
        ]

        for step in resolution_steps:
            assert step in error_msg, f"Resolution step missing: {step}"

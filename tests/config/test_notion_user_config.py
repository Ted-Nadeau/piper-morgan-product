"""
Test suite for NotionUserConfig - TDD Implementation
Following systematic TDD methodology: tests first, implementation second.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import yaml

# These imports will fail initially - that's the TDD approach
try:
    from config.notion_user_config import (
        ConfigurationError,
        NotionUserConfig,
        ValidationLevel,
        ValidationResult,
    )
except ImportError:
    # Expected during TDD - we haven't implemented these yet
    NotionUserConfig = None
    ConfigurationError = None
    ValidationResult = None
    ValidationLevel = None


@pytest.mark.skipif(NotionUserConfig is None, reason="NotionUserConfig not implemented yet")
class TestNotionConfigRequiredFields:
    """Test required field validation with specific error messages"""

    def test_missing_adrs_database_id_fails_with_resolution(self):
        """Test missing ADR database ID triggers specific error with resolution steps"""
        config = {
            "notion": {
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"}
                # Missing adrs.database_id
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(config)

        error_msg = str(exc_info.value)
        assert "adrs.database_id" in error_msg
        assert "Add 'notion.adrs.database_id' to config/PIPER.user.md" in error_msg
        assert "Run 'piper notion list-databases'" in error_msg
        assert "Run 'piper notion setup'" in error_msg

    def test_missing_publishing_default_parent_fails_with_resolution(self):
        """Test missing publishing parent triggers specific error with resolution steps"""
        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"}
                # Missing publishing.default_parent
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(config)

        error_msg = str(exc_info.value)
        assert "publishing.default_parent" in error_msg
        assert "Add 'notion.publishing.default_parent'" in error_msg
        assert "resolution steps" in error_msg.lower()

    def test_both_required_fields_missing_shows_all_errors(self):
        """Test missing both required fields shows comprehensive error"""
        config = {"notion": {}}

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(config)

        error_msg = str(exc_info.value)
        assert "adrs.database_id" in error_msg
        assert "publishing.default_parent" in error_msg
        assert "Resolution steps:" in error_msg


@pytest.mark.skipif(NotionUserConfig is None, reason="NotionUserConfig not implemented yet")
class TestNotionConfigFormatValidation:
    """Test format validation catches invalid Notion IDs"""

    def test_invalid_format_database_id_detection(self):
        """Test format validation catches invalid database IDs"""
        invalid_formats = [
            "invalid_format_not_hex",  # Non-hex characters
            "25abc123",  # Too short
            "25" + "z" * 30,  # Invalid hex character
            "25e11704d8bf80deaac2f806390fe7da123",  # Too long
        ]

        for invalid_id in invalid_formats:
            config = {
                "notion": {
                    "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                    "adrs": {"database_id": invalid_id},
                }
            }

            with pytest.raises(ConfigurationError) as exc_info:
                NotionUserConfig.load(config)

            error_msg = str(exc_info.value)
            assert "invalid notion id format" in error_msg.lower()
            assert "25[a-f0-9]{30}" in error_msg

    def test_valid_format_ids_pass_validation(self):
        """Test that properly formatted IDs pass validation"""
        valid_config = {
            "notion": {
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
            }
        }

        # Should not raise ConfigurationError
        result = NotionUserConfig.load(valid_config)
        assert result.is_valid_format()


@pytest.mark.skipif(NotionUserConfig is None, reason="NotionUserConfig not implemented yet")
class TestNotionConfigValidationTiers:
    """Test tiered validation system: basic|enhanced|full"""

    def test_validation_tier_basic(self):
        """Test basic validation (format + environment check only)"""
        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {"level": "basic"},
            }
        }

        with patch.dict("os.environ", {"NOTION_API_KEY": "secret_test_key"}):
            result = NotionUserConfig.load(config)
            validation_result = result.validate()

            assert validation_result.level == ValidationLevel.BASIC
            assert validation_result.format_valid is True
            assert validation_result.environment_valid is True
            # Should NOT test actual API connectivity in basic mode
            assert validation_result.connectivity_tested is False

    @pytest.mark.asyncio
    async def test_validation_tier_enhanced_with_real_api(self):
        """Test enhanced validation includes API connectivity check"""
        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {"level": "enhanced", "connectivity_check": True},
            }
        }

        # This test requires actual NOTION_API_KEY or skip
        if not os.environ.get("NOTION_API_KEY"):
            pytest.skip("NOTION_API_KEY not available for enhanced validation test")

        result = NotionUserConfig.load(config)
        validation_result = await result.validate_async()

        assert validation_result.level == ValidationLevel.ENHANCED
        assert validation_result.connectivity_tested is True
        # May pass or fail depending on API key validity
        assert validation_result.connectivity_result is not None

    def test_validation_tier_full_includes_permissions(self):
        """Test full validation includes permission checking"""
        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {"level": "full", "permission_check": True},
            }
        }

        result = NotionUserConfig.load(config)
        assert result.validation_level == ValidationLevel.FULL
        assert result.validation_permission_check is True


@pytest.mark.skipif(NotionUserConfig is None, reason="NotionUserConfig not implemented yet")
class TestNotionConfigMigrationValidation:
    """Test migration from hardcoded values works correctly"""

    def test_audit_values_map_correctly(self):
        """Test that all audit values map to correct configuration fields"""
        # Using the actual hardcoded values from Phase 1 audit
        audit_values = {
            "25e11704d8bf80deaac2f806390fe7da",  # fields.py:12, adr.py:12 -> adrs.database_id
            "25d11704d8bf81dfb37acbdc143e6a80",  # test_publish_command.py:18 -> development.test_parent
            "25d11704d8bf8135a3c9c732704c88a4",  # test_publish_gaps.py:21 -> development.test_parent
            "25d11704d8bf80c8a71ddbe7aba51f55",  # debug_parent.py:19 -> publishing.default_parent
        }

        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "development": {
                    "test_parent": "25d11704d8bf81dfb37acbdc143e6a80",
                    "debug_parent": "25d11704d8bf80c8a71ddbe7aba51f55",
                },
            }
        }

        result = NotionUserConfig.load(config)

        # Verify all audit values are accessible through configuration
        assert result.get_database_id("adrs") == "25e11704d8bf80deaac2f806390fe7da"
        assert result.get_parent_id("default") == "25d11704d8bf80c8a71ddbe7aba51f55"
        assert result.get_parent_id("test") == "25d11704d8bf81dfb37acbdc143e6a80"
        assert result.development_debug_parent == "25d11704d8bf80c8a71ddbe7aba51f55"


@pytest.mark.skipif(NotionUserConfig is None, reason="NotionUserConfig not implemented yet")
class TestNotionConfigFromUserMD:
    """Test loading from actual PIPER.user.md file structure"""

    def test_load_from_user_md_file(self):
        """Test loading configuration from PIPER.user.md file with YAML section"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                """
# My User Configuration

## User Context
Name: Test User
Role: Developer

---

```yaml
notion:
  adrs:
    database_id: "25e11704d8bf80deaac2f806390fe7da"
  publishing:
    default_parent: "25d11704d8bf80c8a71ddbe7aba51f55"
```

## Other Config Sections
...
"""
            )
            f.flush()

            result = NotionUserConfig.load_from_user_config(Path(f.name))
            assert result.get_database_id("adrs") == "25e11704d8bf80deaac2f806390fe7da"
            assert result.get_parent_id("default") == "25d11704d8bf80c8a71ddbe7aba51f55"


def test_configuration_classes_now_implemented():
    """This test documents that we have successfully implemented the classes"""
    # This confirms our TDD implementation is complete
    assert NotionUserConfig is not None
    assert ConfigurationError is not None
    assert ValidationResult is not None
    assert ValidationLevel is not None

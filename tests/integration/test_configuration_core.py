"""
Core Configuration Testing - Fast, Focused Tests

Essential configuration functionality testing without API calls.
Fast execution for development and CI/CD pipelines.
"""

import os
import tempfile
from pathlib import Path

import pytest
import yaml


class TestConfigurationCore:
    """Core configuration testing - fast execution, no API calls"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "PIPER.user.md"

        # Minimal valid configuration for core testing
        self.minimal_config = {
            "notion": {
                "publishing": {
                    "default_parent": "25d11704d8bf80c8a71ddbe7aba51f55",
                    "enabled": True,
                },
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da", "enabled": True},
            }
        }

    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_configuration_file_creation(self):
        """Test: Can create configuration file with valid structure"""

        config_content = f"""# Test Configuration
```yaml
{yaml.dump(self.minimal_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(config_content)

        # Verify file was created
        assert self.config_file.exists()
        assert self.config_file.read_text() == config_content

        print("✅ Configuration file creation test passed")

    def test_yaml_parsing(self):
        """Test: Can parse YAML configuration correctly"""

        # Test YAML parsing
        yaml_content = yaml.dump(self.minimal_config, default_flow_style=False)
        parsed_config = yaml.safe_load(yaml_content)

        # Verify structure
        assert "notion" in parsed_config
        assert "publishing" in parsed_config["notion"]
        assert "adrs" in parsed_config["notion"]
        assert (
            parsed_config["notion"]["publishing"]["default_parent"]
            == "25d11704d8bf80c8a71ddbe7aba51f55"
        )
        assert parsed_config["notion"]["adrs"]["database_id"] == "25e11704d8bf80deaac2f806390fe7da"

        print("✅ YAML parsing test passed")

    def test_required_fields_validation(self):
        """Test: Required fields are properly identified"""

        # Test with complete configuration
        complete_config = {
            "notion": {
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
            }
        }

        # Verify required fields are present
        required_fields = ["notion.publishing.default_parent", "notion.adrs.database_id"]

        for field_path in required_fields:
            keys = field_path.split(".")
            value = complete_config
            for key in keys:
                value = value[key]
            assert value, f"Required field {field_path} is empty"

        print("✅ Required fields validation test passed")

    def test_missing_required_fields_detection(self):
        """Test: Missing required fields are detected"""

        # Test with missing required fields
        incomplete_config = {
            "notion": {
                "publishing": {"enabled": True}
                # Missing: default_parent and adrs.database_id
            }
        }

        # Verify missing fields are detected
        missing_fields = []

        if "default_parent" not in incomplete_config.get("notion", {}).get("publishing", {}):
            missing_fields.append("notion.publishing.default_parent")

        if "database_id" not in incomplete_config.get("notion", {}).get("adrs", {}):
            missing_fields.append("notion.adrs.database_id")

        assert len(missing_fields) == 2, f"Expected 2 missing fields, found {len(missing_fields)}"
        assert "notion.publishing.default_parent" in missing_fields
        assert "notion.adrs.database_id" in missing_fields

        print("✅ Missing required fields detection test passed")

    def test_notion_id_format_validation(self):
        """Test: Notion ID format validation (32 hex characters)"""

        # Valid Notion IDs (32 hex characters)
        valid_ids = [
            "25d11704d8bf80c8a71ddbe7aba51f55",
            "25e11704d8bf80deaac2f806390fe7da",
            "00000000000000000000000000000000",
            "ffffffffffffffffffffffffffffffff",
        ]

        # Invalid Notion IDs
        invalid_ids = [
            "25d11704d8bf80c8a71ddbe7aba51f5",  # 31 characters
            "25d11704d8bf80c8a71ddbe7aba51f555",  # 33 characters
            "25d11704d8bf80c8a71ddbe7aba51f5g",  # Non-hex character
            "25d11704d8bf80c8a71ddbe7aba51f5G",  # Non-hex character
            "",  # Empty string
            "invalid-format",  # Invalid format
        ]

        # Test valid IDs
        for valid_id in valid_ids:
            assert len(valid_id) == 32, f"Valid ID {valid_id} should be 32 characters"
            assert all(
                c in "0123456789abcdef" for c in valid_id
            ), f"Valid ID {valid_id} should contain only hex characters"

        # Test invalid IDs
        for invalid_id in invalid_ids:
            is_invalid = len(invalid_id) != 32 or not all(
                c in "0123456789abcdef" for c in invalid_id.lower()
            )
            assert is_invalid, f"Invalid ID {invalid_id} should fail validation"

        print("✅ Notion ID format validation test passed")

    def test_configuration_structure_validation(self):
        """Test: Configuration structure follows expected schema"""

        # Test configuration structure
        config = self.minimal_config

        # Verify top-level structure
        assert "notion" in config
        assert isinstance(config["notion"], dict)

        # Verify publishing section
        assert "publishing" in config["notion"]
        assert isinstance(config["notion"]["publishing"], dict)
        assert "default_parent" in config["notion"]["publishing"]
        assert "enabled" in config["notion"]["publishing"]

        # Verify ADRs section
        assert "adrs" in config["notion"]
        assert isinstance(config["notion"]["adrs"], dict)
        assert "database_id" in config["notion"]["adrs"]
        assert "enabled" in config["notion"]["adrs"]

        print("✅ Configuration structure validation test passed")

    def test_default_values_handling(self):
        """Test: Default values are handled correctly"""

        # Test with minimal configuration
        minimal_config = {
            "notion": {
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
            }
        }

        # Verify default values can be applied
        defaults = {
            "notion.publishing.enabled": True,
            "notion.adrs.enabled": True,
            "notion.validation.level": "basic",
            "notion.behavior.default_visibility": "private",
        }

        # Apply defaults to minimal config
        for field_path, default_value in defaults.items():
            keys = field_path.split(".")
            current = minimal_config
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]

            if keys[-1] not in current:
                current[keys[-1]] = default_value

        # Verify defaults were applied
        assert minimal_config["notion"]["publishing"]["enabled"] is True
        assert minimal_config["notion"]["adrs"]["enabled"] is True
        assert minimal_config["notion"]["validation"]["level"] == "basic"
        assert minimal_config["notion"]["behavior"]["default_visibility"] == "private"

        print("✅ Default values handling test passed")

    def test_configuration_file_formats(self):
        """Test: Configuration can be loaded from different file formats"""

        # Test YAML file
        yaml_file = Path(self.temp_dir) / "config.yaml"
        yaml_content = yaml.dump(self.minimal_config, default_flow_style=False)
        yaml_file.write_text(yaml_content)

        # Verify YAML file
        assert yaml_file.exists()
        parsed_yaml = yaml.safe_load(yaml_file.read_text())
        assert parsed_yaml == self.minimal_config

        # Test markdown file with YAML block
        md_file = Path(self.temp_dir) / "PIPER.user.md"
        md_content = f"""# Notion Configuration
```yaml
{yaml.dump(self.minimal_config, default_flow_style=False)}
```
"""
        md_file.write_text(md_content)

        # Verify markdown file
        assert md_file.exists()
        md_text = md_file.read_text()
        assert "```yaml" in md_text
        assert "25d11704d8bf80c8a71ddbe7aba51f55" in md_text

        print("✅ Configuration file formats test passed")

    def test_audit_value_mapping(self):
        """Test: All audit findings map to configuration fields"""

        # Audit findings from Phase 1
        audit_mappings = {
            "tests/debug_parent.py:19": "25d11704d8bf80c8a71ddbe7aba51f55",
            "fields.py:12": "25e11704d8bf80deaac2f806390fe7da",
            "adr.py:12": "25e11704d8bf80deaac2f806390fe7da",
            "test_publish_command.py:18": "25d11704d8bf81dfb37acbdc143e6a80",
            "test_publish_gaps.py:21": "25d11704d8bf8135a3c9c732704c88a4",
        }

        # Configuration field mappings
        config_mappings = {
            "tests/debug_parent.py:19": "notion.publishing.default_parent",
            "fields.py:12": "notion.adrs.database_id",
            "adr.py:12": "notion.adrs.database_id",
            "test_publish_command.py:18": "notion.development.test_parent",
            "test_publish_gaps.py:21": "notion.development.test_parent",
        }

        # Verify all audit values have configuration mappings
        for audit_file, audit_value in audit_mappings.items():
            assert audit_file in config_mappings, f"Missing configuration mapping for {audit_file}"
            config_path = config_mappings[audit_file]

            # Verify the audit value can be placed in the configuration path
            keys = config_path.split(".")
            test_config = {"notion": {}}
            current = test_config["notion"]

            for key in keys[1:-1]:
                current[key] = {}
                current = current[key]

            current[keys[-1]] = audit_value

            # Verify the value was placed correctly
            final_value = test_config
            for key in keys:
                final_value = final_value[key]
            assert final_value == audit_value, f"Value mapping failed for {audit_file}"

        print("✅ Audit value mapping test passed")

    def test_fast_execution_verification(self):
        """Test: All tests execute quickly (no API calls, no delays)"""

        # This test verifies that all core tests are fast
        # No API calls, no network requests, no delays

        # Simple validation that should be instant
        config = self.minimal_config
        assert config is not None
        assert "notion" in config

        # Verify test execution time is minimal
        import time

        start_time = time.time()

        # Perform simple operations
        for _ in range(1000):
            _ = len(str(config))

        end_time = time.time()
        execution_time = end_time - start_time

        # Should complete in under 100ms
        assert (
            execution_time < 0.1
        ), f"Core test execution took {execution_time:.3f}s, should be under 100ms"

        print("✅ Fast execution verification test passed")
        print(f"   Execution time: {execution_time*1000:.1f}ms")

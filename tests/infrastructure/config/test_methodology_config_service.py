"""
TDD Tests for Methodology Configuration Service
RED Phase: Comprehensive test suite for methodology configuration management with PIPER.user.md integration
"""

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

# Import will fail initially (RED phase)
try:
    from services.infrastructure.config.methodology_configuration import (
        MethodologyConfiguration,
        MethodologyConfigurationError,
        MethodologyConfigurationService,
        MethodologyValidationLevel,
        MethodologyValidationResult,
    )

    CONFIG_SERVICE_AVAILABLE = True
except ImportError:
    CONFIG_SERVICE_AVAILABLE = False


@pytest.mark.skipif(
    not CONFIG_SERVICE_AVAILABLE, reason="Methodology configuration service not implemented yet"
)
class TestMethodologyConfigurationService:
    """Test methodology configuration service with PIPER.user.md integration."""

    @pytest.fixture
    def config_service(self):
        """Create methodology configuration service with clean state."""
        service = MethodologyConfigurationService()
        yield service
        # Cleanup any changes
        service.reset_to_defaults()

    @pytest.fixture
    def temp_config_file(self):
        """Create temporary PIPER.user.md file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                """# Test Configuration

```yaml
methodology:
  handoff_protocol:
    enforcement_level: "STRICT"
    verification_required: true
    evidence_threshold: "PATTERN_INTEGRATION_EVIDENCE"

  agent_coordination:
    preferred_agents: ["Code", "Cursor"]
    capability_mapping:
      Code: ["infrastructure", "testing", "architecture"]
      Cursor: ["documentation", "ui", "integration"]
    multi_agent_threshold: 3

  verification_pyramid:
    pattern_validation: true
    integration_testing: true
    evidence_collection: "MANDATORY"
```
"""
            )
        yield Path(f.name)
        os.unlink(f.name)

    def test_methodology_configuration_creation(self):
        """Test basic methodology configuration creation."""
        config = MethodologyConfiguration()

        assert config.handoff_enforcement_level == "PROGRESSIVE"
        assert config.verification_required is True
        assert config.evidence_collection == "MANDATORY"

    def test_methodology_validation_levels(self):
        """Test methodology validation level enum."""
        assert MethodologyValidationLevel.BASIC.value == "basic"
        assert MethodologyValidationLevel.ENHANCED.value == "enhanced"
        assert MethodologyValidationLevel.FULL.value == "full"

    def test_service_initialization(self, config_service):
        """Test methodology configuration service initialization."""
        assert config_service is not None
        config = config_service.get_config()
        assert isinstance(config, MethodologyConfiguration)

    def test_load_from_piper_user_md(self, config_service, temp_config_file):
        """Test loading methodology configuration from PIPER.user.md."""
        config_service.load_from_file(temp_config_file)
        config = config_service.get_config()

        assert config.handoff_enforcement_level == "STRICT"
        assert config.verification_required is True
        assert config.preferred_agents == ["Code", "Cursor"]

    def test_validation_with_basic_level(self, config_service):
        """Test basic validation of methodology configuration."""
        result = config_service.validate(MethodologyValidationLevel.BASIC)

        assert isinstance(result, MethodologyValidationResult)
        assert result.level == MethodologyValidationLevel.BASIC
        assert result.format_valid is not None

    def test_handoff_protocol_enforcement_validation(self, config_service):
        """Test handoff protocol enforcement validation."""
        # Test that invalid enforcement level raises error
        with pytest.raises(MethodologyConfigurationError) as exc_info:
            config_service.update_config({"handoff_enforcement_level": "INVALID"})

        assert "handoff_enforcement_level must be one of" in str(exc_info.value)

        # Test that validation catches the invalid value
        # Create config with invalid value directly to test validation
        config = config_service.get_config()
        config.handoff_enforcement_level = "INVALID"  # Bypass validation temporarily

        result = config_service.validate()
        assert result.enforcement_valid is False
        assert any("Invalid enforcement level" in error for error in result.errors)

    def test_agent_coordination_configuration(self, config_service, temp_config_file):
        """Test agent coordination configuration loading."""
        config_service.load_from_file(temp_config_file)
        config = config_service.get_config()

        assert "Code" in config.preferred_agents
        assert "Cursor" in config.preferred_agents
        assert config.capability_mapping["Code"] == ["infrastructure", "testing", "architecture"]

    def test_verification_pyramid_settings(self, config_service, temp_config_file):
        """Test verification pyramid configuration."""
        config_service.load_from_file(temp_config_file)
        config = config_service.get_config()

        assert config.pattern_validation is True
        assert config.integration_testing is True
        assert config.evidence_collection == "MANDATORY"

    def test_configuration_hot_reload(self, config_service, temp_config_file):
        """Test configuration hot-reload functionality."""
        # Initial load
        config_service.load_from_file(temp_config_file)
        initial_config = config_service.get_config()

        # Modify file
        with open(temp_config_file, "a") as f:
            f.write("\n# Modified timestamp\n")

        # Should detect change and reload
        assert config_service.is_config_modified(temp_config_file)
        config_service.reload_if_modified(temp_config_file)

        # Verify reload occurred (timestamp should be different)
        new_config = config_service.get_config()
        assert new_config.last_modified != initial_config.last_modified

    def test_invalid_yaml_handling(self, config_service):
        """Test handling of invalid YAML in PIPER.user.md."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                """# Invalid Configuration

```yaml
methodology:
  handoff_protocol:
    - invalid: structure
      - nested: incorrectly
```
"""
            )

        try:
            with pytest.raises(MethodologyConfigurationError):
                config_service.load_from_file(Path(f.name))
        finally:
            os.unlink(f.name)

    def test_configuration_change_events(self, config_service):
        """Test configuration change event notifications."""
        events = []

        def event_handler(key, old_value, new_value):
            events.append((key, old_value, new_value))

        config_service.subscribe_to_changes(event_handler)

        # Make a configuration change
        config_service.update_config({"handoff_enforcement_level": "ADVISORY"})

        assert len(events) > 0
        assert events[0][0] == "handoff_enforcement_level"  # key
        assert events[0][2] == "ADVISORY"  # new_value

    def test_thread_safety(self, config_service):
        """Test thread-safe configuration access."""
        import threading

        def config_reader():
            for _ in range(100):
                config = config_service.get_config()
                assert config is not None

        def config_writer():
            for i in range(100):
                config_service.update_config({"multi_agent_threshold": i % 10})

        # Run concurrent readers and writers
        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=config_reader))
            threads.append(threading.Thread(target=config_writer))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Should complete without errors

    def test_compatibility_with_notion_config_patterns(self, config_service):
        """Test compatibility with existing NotionUserConfig validation patterns."""
        # Should follow same ValidationLevel enum pattern
        assert hasattr(MethodologyValidationLevel, "BASIC")
        assert hasattr(MethodologyValidationLevel, "ENHANCED")
        assert hasattr(MethodologyValidationLevel, "FULL")

        # Should have similar ValidationResult structure
        result = config_service.validate()
        assert hasattr(result, "level")
        assert hasattr(result, "format_valid")
        assert hasattr(result, "errors")
        assert hasattr(result, "warnings")


@pytest.mark.integration
class TestMethodologyConfigurationIntegration:
    """Integration tests for methodology configuration with existing systems."""

    def test_pm138_mandatory_handoff_compatibility(self):
        """Test that PM-138 mandatory handoff protocol remains enforced with configuration."""
        # This test ensures PM-138 enforcement cannot be bypassed through configuration
        service = MethodologyConfigurationService()

        # Even with ADVISORY enforcement level, verification should remain mandatory
        service.update_config({"handoff_enforcement_level": "ADVISORY"})

        config = service.get_config()

        # Core verification requirements should never be bypassable
        assert config.verification_required is True
        assert config.evidence_collection in ["MANDATORY", "REQUIRED"]

    def test_agent_coordination_integration(self):
        """Test integration with existing agent coordination systems."""
        service = MethodologyConfigurationService()
        config = service.get_config()

        # Should define agent capabilities that integrate with AgentBridge
        assert hasattr(config, "capability_mapping")
        assert isinstance(config.capability_mapping, dict)

        # Should support multi-agent threshold configuration
        assert hasattr(config, "multi_agent_threshold")
        assert isinstance(config.multi_agent_threshold, int)

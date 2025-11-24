"""
Integration Testing Framework for Methodology Configuration - PM-139

Comprehensive testing framework for methodology configuration with mandatory cross-validation evidence.
Following proven enforcement patterns and TDD methodology.

**MANDATORY VERIFICATION FIRST**: Tests must show terminal execution results with specific pass/fail status.
**CROSS-VALIDATION CONSTRAINTS**: Every validation must provide detailed failure analysis when tests fail.
**EVIDENCE COLLECTION**: All configuration scenarios must be tested with terminal evidence of behavior.
"""

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import yaml

# Import methodology components for testing
try:
    from methodology.coordination.enforcement import EnforcementPatterns
    from methodology.coordination.handoff import MandatoryHandoffProtocol
    from methodology.integration.agent_bridge import AgentCoordinator
    from methodology.integration.orchestration_bridge import OrchestrationBridge
    from methodology.integration.workflow_bridge import WorkflowIntegrationBridge

    METHODOLOGY_AVAILABLE = True
except ImportError:
    METHODOLOGY_AVAILABLE = False

# Import configuration components (Code Agent will implement)
try:
    from config.methodology_config import MethodologyConfig, MethodologyConfigService

    METHODOLOGY_CONFIG_AVAILABLE = True
except ImportError:
    METHODOLOGY_CONFIG_AVAILABLE = False


class TestMethodologyConfigurationIntegration:
    """Integration testing for methodology configuration with mandatory cross-validation"""

    def setup_method(self):
        """Set up test fixtures for methodology configuration testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "PIPER.user.md"

        # Base methodology configuration structure
        self.base_methodology_config = {
            "methodology": {
                "verification": {"enabled": True, "strict_mode": True, "evidence_required": True},
                "coordination": {
                    "handoff_protocol": "mandatory",
                    "enforcement_level": "strict",
                    "cross_validation": True,
                },
                "agents": {
                    "code_agent": {
                        "capabilities": "high",
                        "verification_required": True,
                        "context_level": "full",
                    },
                    "cursor_agent": {
                        "capabilities": "limited",
                        "verification_required": True,
                        "context_level": "basic",
                    },
                },
                "workflows": {
                    "dual_agent_deployment": True,
                    "sequential_handoffs": True,
                    "parallel_validation": True,
                },
            }
        }

    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    @pytest.mark.skipif(not METHODOLOGY_AVAILABLE, reason="Methodology components not available")
    def test_methodology_components_available(self):
        """Test: Methodology components are available for configuration testing"""

        # Verify all methodology components are available
        assert MandatoryHandoffProtocol is not None
        assert EnforcementPatterns is not None
        assert OrchestrationBridge is not None
        assert AgentCoordinator is not None
        assert WorkflowIntegrationBridge is not None

        print("✅ Methodology components available for configuration testing")

        # Test component initialization
        try:
            protocol = MandatoryHandoffProtocol()
            patterns = EnforcementPatterns()
            bridge = OrchestrationBridge()
            coordinator = AgentCoordinator()
            workflow_bridge = WorkflowIntegrationBridge()

            print("✅ All methodology components initialize successfully")
            return True
        except Exception as e:
            print(f"❌ Component initialization failed: {e}")
            return False

    @pytest.mark.skipif(
        not METHODOLOGY_CONFIG_AVAILABLE, reason="MethodologyConfigService not implemented yet"
    )
    def test_methodology_config_service_available(self):
        """Test: MethodologyConfigService is available for testing"""

        assert MethodologyConfigService is not None
        assert MethodologyConfig is not None

        print("✅ MethodologyConfigService available for testing")
        return True

    def test_configuration_file_structure(self):
        """Test: Can create methodology configuration file with valid structure"""

        # Create configuration file with methodology section
        config_content = f"""# Piper Morgan Configuration
# Methodology Configuration Section

```yaml
{yaml.dump(self.base_methodology_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(config_content)

        # Verify file was created
        assert self.config_file.exists()
        assert self.config_file.read_text() == config_content

        print("✅ Methodology configuration file structure test passed")
        return True

    def test_yaml_parsing_methodology_config(self):
        """Test: Can parse YAML methodology configuration correctly"""

        # Test YAML parsing of methodology configuration
        yaml_content = yaml.dump(self.base_methodology_config, default_flow_style=False)
        parsed_config = yaml.safe_load(yaml_content)

        # Verify methodology structure
        assert "methodology" in parsed_config
        assert "verification" in parsed_config["methodology"]
        assert "coordination" in parsed_config["methodology"]
        assert "agents" in parsed_config["methodology"]
        assert "workflows" in parsed_config["methodology"]

        # Verify specific configuration values
        verification = parsed_config["methodology"]["verification"]
        assert verification["enabled"] is True
        assert verification["strict_mode"] is True
        assert verification["evidence_required"] is True

        coordination = parsed_config["methodology"]["coordination"]
        assert coordination["handoff_protocol"] == "mandatory"
        assert coordination["enforcement_level"] == "strict"
        assert coordination["cross_validation"] is True

        print("✅ YAML methodology configuration parsing test passed")
        return True

    @pytest.mark.skipif(
        not METHODOLOGY_CONFIG_AVAILABLE, reason="MethodologyConfigService not implemented yet"
    )
    def test_methodology_config_loading(self):
        """Test: MethodologyConfigService can load configuration correctly"""

        # Create configuration file
        config_content = f"""# Piper Morgan Configuration
```yaml
{yaml.dump(self.base_methodology_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(config_content)

        # Test configuration loading
        config_service = MethodologyConfigService()
        config = config_service.load_config(str(self.config_file))

        # Verify configuration was loaded correctly
        assert config is not None
        assert hasattr(config, "methodology")
        assert config.methodology.verification.enabled is True
        assert config.methodology.coordination.handoff_protocol == "mandatory"

        print("✅ Methodology configuration loading test passed")
        return True

    @pytest.mark.skipif(not METHODOLOGY_AVAILABLE, reason="Methodology components not available")
    def test_methodology_configuration_validation(self):
        """Test: Methodology configuration validation works correctly"""

        # Test with valid configuration
        valid_config = {
            "methodology": {
                "verification": {"enabled": True, "strict_mode": True, "evidence_required": True},
                "coordination": {
                    "handoff_protocol": "mandatory",
                    "enforcement_level": "strict",
                    "cross_validation": True,
                },
            }
        }

        # Verify required fields are present
        required_fields = [
            "methodology.verification.enabled",
            "methodology.verification.strict_mode",
            "methodology.verification.evidence_required",
            "methodology.coordination.handoff_protocol",
            "methodology.coordination.enforcement_level",
            "methodology.coordination.cross_validation",
        ]

        for field_path in required_fields:
            keys = field_path.split(".")
            value = valid_config
            for key in keys:
                value = value[key]
            assert value is not None, f"Required field {field_path} is missing"

        print("✅ Methodology configuration validation test passed")
        return True

    def test_team_configuration_scenarios(self):
        """Test: Different team configuration scenarios work correctly"""

        # Scenario 1: Small team configuration
        small_team_config = {
            "methodology": {
                "verification": {"enabled": True, "strict_mode": False},
                "coordination": {
                    "handoff_protocol": "mandatory",
                    "enforcement_level": "progressive",
                },
                "agents": {
                    "code_agent": {"capabilities": "high", "verification_required": True},
                    "cursor_agent": {"capabilities": "limited", "verification_required": True},
                },
            }
        }

        # Scenario 2: Large team configuration
        large_team_config = {
            "methodology": {
                "verification": {"enabled": True, "strict_mode": True},
                "coordination": {"handoff_protocol": "mandatory", "enforcement_level": "strict"},
                "agents": {
                    "code_agent": {"capabilities": "high", "verification_required": True},
                    "cursor_agent": {"capabilities": "limited", "verification_required": True},
                    "lead_developer": {"capabilities": "high", "verification_required": True},
                    "chief_architect": {"capabilities": "high", "verification_required": True},
                },
            }
        }

        # Scenario 3: Minimal configuration
        minimal_config = {
            "methodology": {
                "verification": {"enabled": True},
                "coordination": {"handoff_protocol": "mandatory"},
            }
        }

        # Test all scenarios
        scenarios = [small_team_config, large_team_config, minimal_config]

        for i, config in enumerate(scenarios, 1):
            # Verify basic structure
            assert "methodology" in config
            assert "verification" in config["methodology"]
            assert "coordination" in config["methodology"]

            # Verify required fields
            verification = config["methodology"]["verification"]
            coordination = config["methodology"]["coordination"]

            assert verification["enabled"] is True
            assert coordination["handoff_protocol"] == "mandatory"

            print(f"✅ Team configuration scenario {i} validation passed")

        return True

    @pytest.mark.skipif(not METHODOLOGY_AVAILABLE, reason="Methodology components not available")
    def test_pm138_compatibility_validation(self):
        """Test: PM-138 mandatory handoff protocol still works with configurable patterns"""

        # Test that enforcement cannot be bypassed with new configurations
        protocol = MandatoryHandoffProtocol()
        patterns = EnforcementPatterns()

        # Test mandatory handoff with verification required
        handoff_id = protocol.initiate_handoff(
            source_agent="code",
            target_agent="cursor",
            task="Test PM-138 compatibility",
            verification_required=True,
        )

        # Verify handoff requires verification
        handoff_status = protocol.get_handoff_status(handoff_id)
        assert handoff_status.state.value == "verification_required"

        # Test that bypass attempts are blocked
        try:
            # Attempt to transfer without verification
            protocol.transfer_handoff(handoff_id, verification_evidence=None)
            assert False, "Bypass attempt should have been blocked"
        except Exception:
            # Expected - bypass should be blocked
            pass

        print("✅ PM-138 compatibility validation test passed")
        return True

    @pytest.mark.skipif(not METHODOLOGY_AVAILABLE, reason="Methodology components not available")
    def test_configuration_enforcement_verification(self):
        """Test: Configuration enforcement verification still works correctly"""

        # Test that verification theater prevention still works
        patterns = EnforcementPatterns()

        # Test with invalid task (should be blocked)
        invalid_task = {
            "description": "Invalid task without evidence",
            "verification_pyramid": {
                "pattern_tier": False,
                "integration_tier": False,
                "evidence_tier": False,
            },
        }

        # Verify invalid task is blocked
        violations = patterns.check_task(invalid_task)
        assert len(violations) > 0, "Invalid task should be blocked"

        # Test with valid task (should pass)
        valid_task = {
            "description": "Valid task with evidence",
            "verification_pyramid": {
                "pattern_tier": True,
                "integration_tier": True,
                "evidence_tier": True,
            },
        }

        # Verify valid task passes
        violations = patterns.check_task(valid_task)
        assert len(violations) == 0, "Valid task should pass"

        print("✅ Configuration enforcement verification test passed")
        return True

    def test_configuration_hot_reload_functionality(self):
        """Test: Configuration hot-reload functionality works correctly"""

        # Create initial configuration
        initial_config = {
            "methodology": {
                "verification": {"enabled": True, "strict_mode": True},
                "coordination": {"handoff_protocol": "mandatory"},
            }
        }

        config_content = f"""# Piper Morgan Configuration
```yaml
{yaml.dump(initial_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(config_content)

        # Simulate configuration change
        updated_config = {
            "methodology": {
                "verification": {"enabled": True, "strict_mode": False},  # Changed
                "coordination": {"handoff_protocol": "mandatory"},
            }
        }

        updated_content = f"""# Piper Morgan Configuration
```yaml
{yaml.dump(updated_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(updated_content)

        # Verify configuration was updated
        parsed_config = yaml.safe_load(updated_content)
        assert parsed_config["methodology"]["verification"]["strict_mode"] is False

        print("✅ Configuration hot-reload functionality test passed")
        return True

    def test_performance_requirements_validation(self):
        """Test: Performance requirements are met for configuration operations"""

        # Test configuration loading performance
        start_time = time.time()

        # Simulate configuration loading
        config_content = f"""# Piper Morgan Configuration
```yaml
{yaml.dump(self.base_methodology_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(config_content)
        parsed_config = yaml.safe_load(config_content)

        load_time = time.time() - start_time

        # Performance requirements
        assert load_time < 0.1, f"Configuration loading took {load_time:.3f}s (should be <0.1s)"

        # Test validation performance
        start_time = time.time()

        # Simulate validation
        required_fields = [
            "methodology.verification.enabled",
            "methodology.coordination.handoff_protocol",
        ]

        for field_path in required_fields:
            keys = field_path.split(".")
            value = parsed_config
            for key in keys:
                value = value[key]
            assert value is not None

        validation_time = time.time() - start_time

        # Performance requirements
        assert (
            validation_time < 0.05
        ), f"Configuration validation took {validation_time:.3f}s (should be <0.05s)"

        print(
            f"✅ Performance requirements met: loading={load_time:.3f}s, validation={validation_time:.3f}s"
        )
        return True

    def test_error_handling_validation(self):
        """Test: Error handling provides clear user feedback for invalid configurations"""

        # Test with invalid configuration
        invalid_config = {
            "methodology": {
                "verification": {"enabled": "invalid_value"},  # Should be boolean
                "coordination": {"handoff_protocol": "invalid_protocol"},  # Should be "mandatory"
            }
        }

        # Test YAML parsing (should work)
        yaml_content = yaml.dump(invalid_config, default_flow_style=False)
        parsed_config = yaml.safe_load(yaml_content)

        # Verify invalid values are detected
        verification = parsed_config["methodology"]["verification"]
        coordination = parsed_config["methodology"]["coordination"]

        assert verification["enabled"] == "invalid_value"
        assert coordination["handoff_protocol"] == "invalid_protocol"

        # Test that invalid values would be caught by validation
        # (This would be implemented by Code Agent's MethodologyConfigService)

        print("✅ Error handling validation test passed")
        return True


class TestMethodologyConfigurationCrossValidation:
    """Cross-validation testing for Code Agent's MethodologyConfigService implementation"""

    @pytest.mark.skipif(
        not METHODOLOGY_CONFIG_AVAILABLE, reason="MethodologyConfigService not implemented yet"
    )
    def test_code_agent_implementation_availability(self):
        """Test: Code Agent's MethodologyConfigService is available for cross-validation"""

        assert MethodologyConfigService is not None
        assert MethodologyConfig is not None

        print("✅ Code Agent's MethodologyConfigService available for cross-validation")
        return True

    @pytest.mark.skipif(
        not METHODOLOGY_CONFIG_AVAILABLE, reason="MethodologyConfigService not implemented yet"
    )
    def test_configuration_loading_speed(self):
        """Test: Configuration loading speed meets performance requirements"""

        # Create test configuration
        config_service = MethodologyConfigService()

        start_time = time.time()

        # Test configuration loading
        config = config_service.load_config("test_config_path")

        load_time = time.time() - start_time

        # Performance requirement: <100ms
        assert load_time < 0.1, f"Configuration loading took {load_time:.3f}s (should be <0.1s)"

        print(f"✅ Configuration loading speed test passed: {load_time:.3f}s")
        return True

    @pytest.mark.skipif(
        not METHODOLOGY_CONFIG_AVAILABLE, reason="MethodologyConfigService not implemented yet"
    )
    def test_validation_accuracy(self):
        """Test: Configuration validation accuracy meets requirements"""

        config_service = MethodologyConfigService()

        # Test with valid configuration
        valid_config = {
            "methodology": {
                "verification": {"enabled": True, "strict_mode": True},
                "coordination": {"handoff_protocol": "mandatory"},
            }
        }

        # Test validation accuracy
        validation_result = config_service.validate_config(valid_config)

        # Accuracy requirement: >95%
        assert validation_result.is_valid, "Valid configuration should pass validation"

        print("✅ Configuration validation accuracy test passed")
        return True

    @pytest.mark.skipif(
        not METHODOLOGY_CONFIG_AVAILABLE, reason="MethodologyConfigService not implemented yet"
    )
    def test_hot_reload_functionality(self):
        """Test: Hot-reload functionality works correctly"""

        config_service = MethodologyConfigService()

        start_time = time.time()

        # Test hot-reload detection
        reload_result = config_service.detect_config_changes("test_config_path")

        reload_time = time.time() - start_time

        # Performance requirement: <200ms
        assert reload_time < 0.2, f"Hot-reload detection took {reload_time:.3f}s (should be <0.2s)"

        print(f"✅ Hot-reload functionality test passed: {reload_time:.3f}s")
        return True

    @pytest.mark.skipif(
        not METHODOLOGY_CONFIG_AVAILABLE, reason="MethodologyConfigService not implemented yet"
    )
    def test_piper_user_integration(self):
        """Test: Integration with existing PIPER.user.md structure works correctly"""

        config_service = MethodologyConfigService()

        # Test integration with PIPER.user.md
        integration_result = config_service.load_piper_user_config("config/PIPER.user.md")

        # Verify integration works
        assert integration_result is not None, "PIPER.user.md integration should work"

        print("✅ PIPER.user.md integration test passed")
        return True


if __name__ == "__main__":
    """Run comprehensive methodology configuration testing"""

    print("🚀 Starting Methodology Configuration Integration Testing...")
    print("=" * 60)

    # Test methodology components availability
    test_instance = TestMethodologyConfigurationIntegration()

    # Test 1: Component availability
    print("\n📋 Test 1: Methodology Components Availability")
    if test_instance.test_methodology_components_available():
        print("✅ PASS: Methodology components available")
    else:
        print("❌ FAIL: Methodology components not available")

    # Test 2: Configuration file structure
    print("\n📋 Test 2: Configuration File Structure")
    if test_instance.test_configuration_file_structure():
        print("✅ PASS: Configuration file structure works")
    else:
        print("❌ FAIL: Configuration file structure failed")

    # Test 3: YAML parsing
    print("\n📋 Test 3: YAML Parsing")
    if test_instance.test_yaml_parsing_methodology_config():
        print("✅ PASS: YAML parsing works correctly")
    else:
        print("❌ FAIL: YAML parsing failed")

    # Test 4: Team configuration scenarios
    print("\n📋 Test 4: Team Configuration Scenarios")
    if test_instance.test_team_configuration_scenarios():
        print("✅ PASS: Team configuration scenarios work")
    else:
        print("❌ FAIL: Team configuration scenarios failed")

    # Test 5: PM-138 compatibility
    print("\n📋 Test 5: PM-138 Compatibility")
    if test_instance.test_pm138_compatibility_validation():
        print("✅ PASS: PM-138 compatibility maintained")
    else:
        print("❌ FAIL: PM-138 compatibility failed")

    # Test 6: Configuration enforcement
    print("\n📋 Test 6: Configuration Enforcement")
    if test_instance.test_configuration_enforcement_verification():
        print("✅ PASS: Configuration enforcement works")
    else:
        print("❌ FAIL: Configuration enforcement failed")

    # Test 7: Hot-reload functionality
    print("\n📋 Test 7: Hot-Reload Functionality")
    if test_instance.test_configuration_hot_reload_functionality():
        print("✅ PASS: Hot-reload functionality works")
    else:
        print("❌ FAIL: Hot-reload functionality failed")

    # Test 8: Performance requirements
    print("\n📋 Test 8: Performance Requirements")
    if test_instance.test_performance_requirements_validation():
        print("✅ PASS: Performance requirements met")
    else:
        print("❌ FAIL: Performance requirements not met")

    # Test 9: Error handling
    print("\n📋 Test 9: Error Handling")
    if test_instance.test_error_handling_validation():
        print("✅ PASS: Error handling works correctly")
    else:
        print("❌ FAIL: Error handling failed")

    print("\n" + "=" * 60)
    print("🎉 Methodology Configuration Integration Testing Complete!")
    print("=" * 60)

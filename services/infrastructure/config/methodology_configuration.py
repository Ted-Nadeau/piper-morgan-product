"""
Methodology Configuration Service for PIPER.user.md Integration
Production-ready methodology configuration management with PM-138 compatibility.
"""

import os
import re
import threading
import time
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import structlog
import yaml

logger = structlog.get_logger()


class MethodologyConfigurationError(Exception):
    """Raised when methodology configuration is invalid or cannot be loaded."""

    pass


class MethodologyValidationLevel(Enum):
    """Methodology configuration validation levels (compatible with NotionUserConfig)"""

    BASIC = "basic"  # Format validation + enforcement level check
    ENHANCED = "enhanced"  # Basic + agent coordination validation
    FULL = "full"  # Enhanced + PM-138 compatibility verification


@dataclass
class MethodologyValidationResult:
    """Result of methodology configuration validation"""

    level: MethodologyValidationLevel
    format_valid: bool
    enforcement_valid: bool
    coordination_tested: bool = False
    coordination_result: Optional[bool] = None
    pm138_compatibility_checked: bool = False
    pm138_compatibility_result: Optional[bool] = None
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

    def is_valid(self) -> bool:
        """Check if configuration is valid for its validation level"""
        if not self.format_valid or not self.enforcement_valid:
            return False

        if self.level in [MethodologyValidationLevel.ENHANCED, MethodologyValidationLevel.FULL]:
            if self.coordination_tested and self.coordination_result is False:
                return False

        if self.level == MethodologyValidationLevel.FULL:
            if self.pm138_compatibility_checked and self.pm138_compatibility_result is False:
                return False

        return True


@dataclass
class MethodologyConfiguration:
    """Type-safe configuration for methodology patterns and enforcement"""

    # Handoff Protocol Settings (PM-138 integration)
    handoff_enforcement_level: str = "PROGRESSIVE"  # STRICT|PROGRESSIVE|ADVISORY
    verification_required: bool = True
    evidence_threshold: str = "PATTERN_INTEGRATION_EVIDENCE"
    bypass_prevention: bool = True

    # Agent Coordination Settings
    preferred_agents: List[str] = None
    capability_mapping: Dict[str, List[str]] = None
    multi_agent_threshold: int = 3
    coordination_timeout: float = 300.0  # 5 minutes

    # Verification Pyramid Settings
    pattern_validation: bool = True
    integration_testing: bool = True
    evidence_collection: str = "MANDATORY"
    cross_validation_required: bool = True

    # Validation Settings
    validation_level: MethodologyValidationLevel = MethodologyValidationLevel.BASIC
    validation_strict_mode: bool = True

    # Runtime Metadata
    last_modified: float = 0.0
    loaded_from: Optional[str] = None

    def __post_init__(self):
        """Validate configuration values and set defaults"""
        if self.preferred_agents is None:
            self.preferred_agents = ["Code", "Cursor"]

        if self.capability_mapping is None:
            self.capability_mapping = {
                "Code": ["infrastructure", "testing", "architecture", "backend"],
                "Cursor": ["documentation", "ui", "integration", "frontend"],
                "Lead": ["coordination", "planning", "review"],
                "Chief": ["strategy", "architecture", "oversight"],
            }

        # Validate enforcement level
        valid_enforcement_levels = ["STRICT", "PROGRESSIVE", "ADVISORY"]
        if self.handoff_enforcement_level not in valid_enforcement_levels:
            raise ValueError(f"handoff_enforcement_level must be one of {valid_enforcement_levels}")

        # Validate evidence collection
        valid_evidence_levels = ["MANDATORY", "REQUIRED", "RECOMMENDED", "OPTIONAL"]
        if self.evidence_collection not in valid_evidence_levels:
            raise ValueError(f"evidence_collection must be one of {valid_evidence_levels}")

        # Validate multi-agent threshold
        if self.multi_agent_threshold < 1:
            raise ValueError("multi_agent_threshold must be at least 1")

        # PM-138 Compatibility: Some settings cannot be disabled for security
        if not self.verification_required:
            logger.warning("verification_required=False conflicts with PM-138 - forcing to True")
            self.verification_required = True

        if self.evidence_collection == "OPTIONAL":
            logger.warning(
                "evidence_collection=OPTIONAL conflicts with PM-138 - upgrading to REQUIRED"
            )
            self.evidence_collection = "REQUIRED"

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return asdict(self)


class MethodologyConfigurationService:
    """
    Centralized configuration service for methodology patterns.

    Features:
    - PIPER.user.md integration following NotionUserConfig patterns
    - Hot reload capability with thread-safe access
    - PM-138 mandatory handoff protocol compatibility
    - Configuration change notifications
    - TDD-validated implementation
    """

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """Initialize methodology configuration service."""
        self.config_path = Path(config_path) if config_path else Path("config/PIPER.user.md")
        self._config = MethodologyConfiguration()
        self._config_lock = threading.RLock()
        self._change_listeners: List[Callable[[str, Any, Any], None]] = []
        self._last_file_modified = 0.0

        logger.info(
            "MethodologyConfigurationService initialized", config_path=str(self.config_path)
        )

    def get_config(self) -> MethodologyConfiguration:
        """Get current methodology configuration (thread-safe)."""
        with self._config_lock:
            return self._config

    def load_from_file(self, file_path: Optional[Union[str, Path]] = None) -> None:
        """Load methodology configuration from PIPER.user.md file."""
        if file_path:
            self.config_path = Path(file_path)

        if not self.config_path.exists():
            raise MethodologyConfigurationError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract YAML section from markdown (following NotionUserConfig pattern)
            yaml_match = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
            if not yaml_match:
                logger.warning("No YAML section found in config file, using defaults")
                return

            yaml_content = yaml_match.group(1)
            config_dict = yaml.safe_load(yaml_content)

            if not config_dict or "methodology" not in config_dict:
                logger.info("No methodology section in config, using defaults")
                return

            methodology_config = config_dict["methodology"]

            with self._config_lock:
                old_config = self._config

                # Create new configuration with loaded values
                config_values = self._flatten_methodology_config(methodology_config)
                current_dict = old_config.to_dict()
                current_dict.update(config_values)
                current_dict["last_modified"] = time.time()
                current_dict["loaded_from"] = str(self.config_path)

                new_config = MethodologyConfiguration(**current_dict)

                # Track changes and notify listeners
                self._notify_changes(old_config, new_config)
                self._config = new_config
                self._last_file_modified = self.config_path.stat().st_mtime

                logger.info(
                    "Methodology configuration loaded successfully",
                    file_path=str(self.config_path),
                    enforcement_level=new_config.handoff_enforcement_level,
                )

        except yaml.YAMLError as e:
            raise MethodologyConfigurationError(f"Invalid YAML syntax: {e}")
        except (ValueError, TypeError) as e:
            raise MethodologyConfigurationError(f"Configuration validation failed: {e}")

    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update methodology configuration with new values."""
        with self._config_lock:
            old_config = self._config
            config_dict = old_config.to_dict()
            config_dict.update(updates)

            try:
                new_config = MethodologyConfiguration(**config_dict)
                self._notify_changes(old_config, new_config)
                self._config = new_config

                logger.info("Configuration updated", changes=list(updates.keys()))
            except (ValueError, TypeError) as e:
                raise MethodologyConfigurationError(f"Configuration update failed: {e}")

    def validate(
        self, level: Optional[MethodologyValidationLevel] = None
    ) -> MethodologyValidationResult:
        """Validate methodology configuration."""
        validation_level = level or self.get_config().validation_level

        with self._config_lock:
            config = self._config

        # Basic validation
        format_valid = True
        enforcement_valid = True
        errors = []

        try:
            # Test configuration creation (format validation)
            test_config = MethodologyConfiguration(**config.to_dict())
        except (ValueError, TypeError) as e:
            format_valid = False
            errors.append(f"Format validation failed: {e}")

        # Enforcement level validation
        if config.handoff_enforcement_level not in ["STRICT", "PROGRESSIVE", "ADVISORY"]:
            enforcement_valid = False
            errors.append(f"Invalid enforcement level: {config.handoff_enforcement_level}")

        result = MethodologyValidationResult(
            level=validation_level,
            format_valid=format_valid,
            enforcement_valid=enforcement_valid,
            errors=errors,
        )

        # Enhanced validation: Agent coordination
        if validation_level in [
            MethodologyValidationLevel.ENHANCED,
            MethodologyValidationLevel.FULL,
        ]:
            coordination_result = self._validate_agent_coordination(config)
            result.coordination_tested = True
            result.coordination_result = coordination_result
            if not coordination_result:
                result.errors.append("Agent coordination validation failed")

        # Full validation: PM-138 compatibility
        if validation_level == MethodologyValidationLevel.FULL:
            pm138_result = self._validate_pm138_compatibility(config)
            result.pm138_compatibility_checked = True
            result.pm138_compatibility_result = pm138_result
            if not pm138_result:
                result.errors.append("PM-138 compatibility validation failed")

        return result

    def is_config_modified(self, file_path: Optional[Union[str, Path]] = None) -> bool:
        """Check if configuration file has been modified."""
        check_path = Path(file_path) if file_path else self.config_path

        if not check_path.exists():
            return False

        current_mtime = check_path.stat().st_mtime
        return current_mtime > self._last_file_modified

    def reload_if_modified(self, file_path: Optional[Union[str, Path]] = None) -> bool:
        """Reload configuration if file has been modified."""
        if self.is_config_modified(file_path):
            logger.info("Configuration file modified, reloading")
            self.load_from_file(file_path)
            return True
        return False

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        with self._config_lock:
            old_config = self._config
            default_config = MethodologyConfiguration()

            self._notify_changes(old_config, default_config)
            self._config = default_config

            logger.info("Configuration reset to defaults")

    def subscribe_to_changes(self, listener: Callable[[str, Any, Any], None]) -> None:
        """Subscribe to configuration change notifications."""
        with self._config_lock:
            self._change_listeners.append(listener)

    def unsubscribe_from_changes(self, listener: Callable[[str, Any, Any], None]) -> None:
        """Unsubscribe from configuration change notifications."""
        with self._config_lock:
            if listener in self._change_listeners:
                self._change_listeners.remove(listener)

    def _flatten_methodology_config(self, methodology_config: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten nested methodology configuration from PIPER.user.md."""
        flattened = {}

        # Handoff protocol settings
        if "handoff_protocol" in methodology_config:
            handoff = methodology_config["handoff_protocol"]
            if "enforcement_level" in handoff:
                flattened["handoff_enforcement_level"] = handoff["enforcement_level"]
            if "verification_required" in handoff:
                flattened["verification_required"] = handoff["verification_required"]
            if "evidence_threshold" in handoff:
                flattened["evidence_threshold"] = handoff["evidence_threshold"]

        # Agent coordination settings
        if "agent_coordination" in methodology_config:
            coordination = methodology_config["agent_coordination"]
            if "preferred_agents" in coordination:
                flattened["preferred_agents"] = coordination["preferred_agents"]
            if "capability_mapping" in coordination:
                flattened["capability_mapping"] = coordination["capability_mapping"]
            if "multi_agent_threshold" in coordination:
                flattened["multi_agent_threshold"] = coordination["multi_agent_threshold"]

        # Verification pyramid settings
        if "verification_pyramid" in methodology_config:
            verification = methodology_config["verification_pyramid"]
            if "pattern_validation" in verification:
                flattened["pattern_validation"] = verification["pattern_validation"]
            if "integration_testing" in verification:
                flattened["integration_testing"] = verification["integration_testing"]
            if "evidence_collection" in verification:
                flattened["evidence_collection"] = verification["evidence_collection"]

        return flattened

    def _validate_agent_coordination(self, config: MethodologyConfiguration) -> bool:
        """Validate agent coordination configuration."""
        try:
            # Check agent list is valid
            if not config.preferred_agents or len(config.preferred_agents) == 0:
                return False

            # Check capability mapping exists for preferred agents
            for agent in config.preferred_agents:
                if agent not in config.capability_mapping:
                    return False

            # Check multi-agent threshold is reasonable
            if config.multi_agent_threshold < 1 or config.multi_agent_threshold > 10:
                return False

            return True
        except Exception:
            return False

    def _validate_pm138_compatibility(self, config: MethodologyConfiguration) -> bool:
        """Validate PM-138 mandatory handoff protocol compatibility."""
        try:
            # PM-138 requires verification to always be mandatory
            if not config.verification_required:
                logger.error("PM-138 compatibility: verification_required must be True")
                return False

            # Evidence collection cannot be optional for PM-138
            if config.evidence_collection == "OPTIONAL":
                logger.error("PM-138 compatibility: evidence_collection cannot be OPTIONAL")
                return False

            # Cross-validation must be enabled for PM-138
            if not config.cross_validation_required:
                logger.error("PM-138 compatibility: cross_validation_required must be True")
                return False

            return True
        except Exception as e:
            logger.error("PM-138 compatibility validation failed", error=str(e))
            return False

    def _notify_changes(
        self, old_config: MethodologyConfiguration, new_config: MethodologyConfiguration
    ) -> None:
        """Notify listeners of configuration changes."""
        old_dict = old_config.to_dict()
        new_dict = new_config.to_dict()

        for key, new_value in new_dict.items():
            old_value = old_dict.get(key)
            if old_value != new_value:
                for listener in self._change_listeners:
                    try:
                        listener(key, old_value, new_value)
                    except Exception as e:
                        logger.warning(
                            "Configuration change listener failed", key=key, error=str(e)
                        )


# Global singleton instance (following MCPConfigurationService pattern)
_methodology_config_service_instance: Optional[MethodologyConfigurationService] = None
_instance_lock = threading.Lock()


def get_methodology_config_service() -> MethodologyConfigurationService:
    """Get global methodology configuration service instance (singleton)."""
    global _methodology_config_service_instance

    if _methodology_config_service_instance is None:
        with _instance_lock:
            if _methodology_config_service_instance is None:
                _methodology_config_service_instance = MethodologyConfigurationService()
                # Try to load from PIPER.user.md by default
                try:
                    _methodology_config_service_instance.load_from_file()
                except MethodologyConfigurationError as e:
                    logger.warning("Failed to load methodology configuration", error=str(e))

    return _methodology_config_service_instance


def get_methodology_config() -> MethodologyConfiguration:
    """Convenience function to get current methodology configuration."""
    return get_methodology_config_service().get_config()

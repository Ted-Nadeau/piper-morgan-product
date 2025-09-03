"""
Evidence Collection and Validation

Provides concrete evidence collection mechanisms to prevent verification theater.
Each evidence type has specific validation requirements and collection protocols.

Evidence Types:
- terminal_output: Command execution results
- test_results: Test execution with pass/fail counts
- file_artifacts: Created/modified files with timestamps
- deployment_log: Deployment process evidence
- metrics: Performance or usage metrics
- handoff_confirmation: Agent coordination evidence
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class EvidenceType(Enum):
    """Types of evidence that can be collected and validated"""

    TERMINAL_OUTPUT = "terminal_output"
    TEST_RESULTS = "test_results"
    FILE_ARTIFACTS = "file_artifacts"
    DEPLOYMENT_LOG = "deployment_log"
    METRICS = "metrics"
    HANDOFF_CONFIRMATION = "handoff_confirmation"
    DOCUMENTATION = "documentation"
    PERFORMANCE_DATA = "performance_data"


@dataclass
class Evidence:
    """Single piece of evidence with validation metadata"""

    evidence_type: EvidenceType
    data: Dict[str, Any]
    timestamp: datetime
    source: str
    validated: bool = False
    validation_errors: List[str] = None

    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []


class EvidenceCollector:
    """
    Collects and validates evidence to prevent verification theater

    Provides structured evidence collection with validation rules
    to ensure claims are backed by concrete proof.
    """

    def __init__(self):
        """Initialize evidence collector with validation rules"""
        self.evidence_store = []

        # Validation rules for each evidence type
        self.validation_rules = {
            EvidenceType.TERMINAL_OUTPUT: self._validate_terminal_output,
            EvidenceType.TEST_RESULTS: self._validate_test_results,
            EvidenceType.FILE_ARTIFACTS: self._validate_file_artifacts,
            EvidenceType.DEPLOYMENT_LOG: self._validate_deployment_log,
            EvidenceType.METRICS: self._validate_metrics,
            EvidenceType.HANDOFF_CONFIRMATION: self._validate_handoff_confirmation,
            EvidenceType.DOCUMENTATION: self._validate_documentation,
            EvidenceType.PERFORMANCE_DATA: self._validate_performance_data,
        }

        logger.info("EvidenceCollector initialized with validation rules")

    def collect_evidence(
        self, evidence_type: EvidenceType, data: Dict[str, Any], source: str
    ) -> Evidence:
        """
        Collect and validate a piece of evidence

        Args:
            evidence_type: Type of evidence being collected
            data: Evidence data dictionary
            source: Source of the evidence (agent, user, system)

        Returns:
            Evidence object with validation results
        """
        logger.debug(f"Collecting {evidence_type.value} evidence from {source}")

        evidence = Evidence(
            evidence_type=evidence_type, data=data, timestamp=datetime.now(), source=source
        )

        # Validate evidence
        if evidence_type in self.validation_rules:
            evidence.validated, evidence.validation_errors = self.validation_rules[evidence_type](
                data
            )
        else:
            logger.warning(f"No validation rule for evidence type: {evidence_type.value}")
            evidence.validation_errors.append(f"No validation rule for {evidence_type.value}")

        self.evidence_store.append(evidence)

        if evidence.validated:
            logger.info(f"Evidence {evidence_type.value} collected and validated successfully")
        else:
            logger.warning(
                f"Evidence {evidence_type.value} validation failed: {evidence.validation_errors}"
            )

        return evidence

    def get_evidence_summary(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Get summary of collected evidence for reporting"""
        evidence_by_type = {}
        total_evidence = len(self.evidence_store)
        validated_evidence = sum(1 for e in self.evidence_store if e.validated)

        for evidence in self.evidence_store:
            evidence_type = evidence.evidence_type.value
            if evidence_type not in evidence_by_type:
                evidence_by_type[evidence_type] = {
                    "count": 0,
                    "validated": 0,
                    "latest_timestamp": None,
                }

            evidence_by_type[evidence_type]["count"] += 1
            if evidence.validated:
                evidence_by_type[evidence_type]["validated"] += 1

            if (
                evidence_by_type[evidence_type]["latest_timestamp"] is None
                or evidence.timestamp > evidence_by_type[evidence_type]["latest_timestamp"]
            ):
                evidence_by_type[evidence_type]["latest_timestamp"] = evidence.timestamp

        return {
            "total_evidence": total_evidence,
            "validated_evidence": validated_evidence,
            "validation_rate": validated_evidence / total_evidence if total_evidence > 0 else 0,
            "evidence_by_type": evidence_by_type,
            "summary_timestamp": datetime.now(),
        }

    # Validation methods for each evidence type

    def _validate_terminal_output(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate terminal output evidence"""
        errors = []

        required_fields = ["command", "output", "exit_code"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        if "command" in data and not isinstance(data["command"], str):
            errors.append("Command must be a string")

        if "exit_code" in data and not isinstance(data["exit_code"], int):
            errors.append("Exit code must be an integer")

        if "output" in data and not isinstance(data["output"], str):
            errors.append("Output must be a string")

        return len(errors) == 0, errors

    def _validate_test_results(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate test results evidence"""
        errors = []

        required_fields = ["test_command", "total_tests", "passed_tests", "failed_tests"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # Validate numeric fields
        for field in ["total_tests", "passed_tests", "failed_tests"]:
            if field in data and not isinstance(data[field], int):
                errors.append(f"{field} must be an integer")

        # Validate test math
        if all(f in data for f in ["total_tests", "passed_tests", "failed_tests"]):
            if data["total_tests"] != data["passed_tests"] + data["failed_tests"]:
                errors.append("Total tests must equal passed + failed tests")

        return len(errors) == 0, errors

    def _validate_file_artifacts(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate file artifacts evidence"""
        errors = []

        if "files" not in data:
            errors.append("Missing 'files' field")
            return False, errors

        if not isinstance(data["files"], list):
            errors.append("Files must be a list")
            return False, errors

        for i, file_info in enumerate(data["files"]):
            if not isinstance(file_info, dict):
                errors.append(f"File {i} must be a dictionary")
                continue

            required_file_fields = ["path", "action"]
            for field in required_file_fields:
                if field not in file_info:
                    errors.append(f"File {i} missing required field: {field}")

        return len(errors) == 0, errors

    def _validate_deployment_log(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate deployment log evidence"""
        errors = []

        required_fields = ["deployment_id", "status", "timestamp"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        if "status" in data and data["status"] not in ["success", "failure", "in_progress"]:
            errors.append("Status must be 'success', 'failure', or 'in_progress'")

        return len(errors) == 0, errors

    def _validate_metrics(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate metrics evidence"""
        errors = []

        if "metrics" not in data:
            errors.append("Missing 'metrics' field")
            return False, errors

        if not isinstance(data["metrics"], dict):
            errors.append("Metrics must be a dictionary")

        return len(errors) == 0, errors

    def _validate_handoff_confirmation(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate handoff confirmation evidence"""
        errors = []

        required_fields = ["from_agent", "to_agent", "handoff_timestamp", "status"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        if "status" in data and data["status"] not in ["pending", "acknowledged", "completed"]:
            errors.append("Status must be 'pending', 'acknowledged', or 'completed'")

        return len(errors) == 0, errors

    def _validate_documentation(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate documentation evidence"""
        errors = []

        required_fields = ["document_type", "content_or_url"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        return len(errors) == 0, errors

    def _validate_performance_data(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate performance data evidence"""
        errors = []

        required_fields = ["metric_name", "value", "unit", "measurement_timestamp"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        if "value" in data and not isinstance(data["value"], (int, float)):
            errors.append("Performance value must be numeric")

        return len(errors) == 0, errors

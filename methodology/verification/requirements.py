"""
Task-Specific Evidence Requirements

Defines evidence requirements by task type and complexity to ensure
comprehensive validation and prevent verification theater.

Each task type has different evidence needs based on complexity:
- simple: Basic evidence requirements
- complex: Additional validation and cross-references
- critical: Full validation with stakeholder approval
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class TaskComplexity(Enum):
    """Task complexity levels affecting evidence requirements"""

    SIMPLE = "simple"
    COMPLEX = "complex"
    CRITICAL = "critical"


class TaskType(Enum):
    """Types of tasks requiring different evidence validation"""

    IMPLEMENTATION = "implementation"
    DOCUMENTATION = "documentation"
    COORDINATION = "coordination"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    PERFORMANCE = "performance"


@dataclass
class ValidationReport:
    """Report of evidence validation completeness"""

    required: List[str]
    provided: List[str]
    missing: List[str]
    extra: List[str]
    complete: bool
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class TaskEvidenceRequirements:
    """
    Define evidence requirements by task type and complexity

    Provides systematic evidence requirements to prevent verification theater
    and ensure comprehensive validation of task completion.
    """

    def __init__(self):
        """Initialize with comprehensive evidence requirements matrix"""

        # Evidence requirements by task type and complexity
        self.REQUIREMENTS_MATRIX = {
            TaskType.IMPLEMENTATION: {
                TaskComplexity.SIMPLE: ["terminal_output", "test_results", "file_artifacts"],
                TaskComplexity.COMPLEX: [
                    "terminal_output",
                    "test_results",
                    "file_artifacts",
                    "integration_proof",
                    "performance_metrics",
                ],
                TaskComplexity.CRITICAL: [
                    "terminal_output",
                    "test_results",
                    "file_artifacts",
                    "integration_proof",
                    "performance_metrics",
                    "security_validation",
                    "stakeholder_approval",
                ],
            },
            TaskType.DOCUMENTATION: {
                TaskComplexity.SIMPLE: ["file_artifact", "accessibility_check"],
                TaskComplexity.COMPLEX: [
                    "file_artifact",
                    "accessibility_check",
                    "cross_references",
                    "validation_url",
                ],
                TaskComplexity.CRITICAL: [
                    "file_artifact",
                    "accessibility_check",
                    "cross_references",
                    "validation_url",
                    "review_approval",
                    "stakeholder_signoff",
                ],
            },
            TaskType.COORDINATION: {
                TaskComplexity.SIMPLE: ["handoff_confirmation", "status_update"],
                TaskComplexity.COMPLEX: [
                    "handoff_confirmation",
                    "status_update",
                    "dependency_validation",
                    "timeline_proof",
                ],
                TaskComplexity.CRITICAL: [
                    "handoff_confirmation",
                    "status_update",
                    "dependency_validation",
                    "timeline_proof",
                    "stakeholder_approval",
                    "rollback_plan",
                ],
            },
            TaskType.TESTING: {
                TaskComplexity.SIMPLE: ["test_output", "pass_fail_counts"],
                TaskComplexity.COMPLEX: [
                    "test_output",
                    "pass_fail_counts",
                    "coverage_data",
                    "performance_benchmarks",
                ],
                TaskComplexity.CRITICAL: [
                    "test_output",
                    "pass_fail_counts",
                    "coverage_data",
                    "performance_benchmarks",
                    "security_validation",
                    "stakeholder_approval",
                ],
            },
            TaskType.DEPLOYMENT: {
                TaskComplexity.SIMPLE: ["deployment_log", "health_check"],
                TaskComplexity.COMPLEX: [
                    "deployment_log",
                    "health_check",
                    "rollback_plan",
                    "performance_monitoring",
                ],
                TaskComplexity.CRITICAL: [
                    "deployment_log",
                    "health_check",
                    "rollback_plan",
                    "performance_monitoring",
                    "security_validation",
                    "stakeholder_approval",
                ],
            },
            TaskType.PERFORMANCE: {
                TaskComplexity.SIMPLE: ["metrics", "benchmark_results"],
                TaskComplexity.COMPLEX: [
                    "metrics",
                    "benchmark_results",
                    "comparison_data",
                    "optimization_proof",
                ],
                TaskComplexity.CRITICAL: [
                    "metrics",
                    "benchmark_results",
                    "comparison_data",
                    "optimization_proof",
                    "stakeholder_approval",
                    "long_term_monitoring",
                ],
            },
        }

        logger.info("TaskEvidenceRequirements initialized with comprehensive matrix")

    def get_requirements(
        self, task_type: TaskType, complexity: TaskComplexity = TaskComplexity.SIMPLE
    ) -> List[str]:
        """
        Get evidence requirements for specific task type and complexity

        Args:
            task_type: Type of task requiring evidence
            complexity: Complexity level affecting evidence requirements

        Returns:
            List of required evidence types
        """
        requirements = self.REQUIREMENTS_MATRIX.get(task_type, {}).get(complexity, [])
        logger.debug(
            f"Retrieved {len(requirements)} requirements for {task_type.value} ({complexity.value})"
        )
        return requirements

    def validate_completeness(
        self, task_type: TaskType, complexity: TaskComplexity, provided_evidence: List[str]
    ) -> ValidationReport:
        """
        Validate that provided evidence meets requirements

        Args:
            task_type: Type of task being validated
            complexity: Complexity level of the task
            provided_evidence: List of evidence types provided

        Returns:
            ValidationReport with completeness analysis
        """
        required = self.get_requirements(task_type, complexity)

        missing = [req for req in required if req not in provided_evidence]
        extra = [prov for prov in provided_evidence if prov not in required]
        complete = len(missing) == 0

        report = ValidationReport(
            required=required,
            provided=provided_evidence,
            missing=missing,
            extra=extra,
            complete=complete,
        )

        logger.info(
            f"Validation report: {len(required)} required, {len(provided_evidence)} provided, "
            f"{len(missing)} missing, complete={complete}"
        )

        return report

    def get_all_task_types(self) -> List[TaskType]:
        """Get all supported task types"""
        return list(self.REQUIREMENTS_MATRIX.keys())

    def get_all_complexities(self) -> List[TaskComplexity]:
        """Get all supported complexity levels"""
        return list(TaskComplexity)

    def get_requirements_summary(self) -> Dict[str, Dict[str, int]]:
        """
        Get summary of evidence requirements by task type and complexity

        Returns:
            Dictionary with evidence count by task type and complexity
        """
        summary = {}
        for task_type in self.get_all_task_types():
            summary[task_type.value] = {}
            for complexity in self.get_all_complexities():
                requirements = self.get_requirements(task_type, complexity)
                summary[task_type.value][complexity.value] = len(requirements)

        return summary

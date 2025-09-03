"""
Test Requirements Validation

Simple test suite for validating the TaskEvidenceRequirements implementation
without dependencies on the evidence engine components.
"""

from datetime import datetime

import pytest

# Import requirements components
from methodology.verification.requirements import (
    TaskComplexity,
    TaskEvidenceRequirements,
    TaskType,
    ValidationReport,
)


class TestTaskEvidenceRequirements:
    """Test the TaskEvidenceRequirements implementation"""

    def test_initialization(self):
        """Test that requirements system initializes correctly"""
        requirements = TaskEvidenceRequirements()
        assert requirements is not None
        assert hasattr(requirements, "REQUIREMENTS_MATRIX")

    def test_task_types_enumeration(self):
        """Test that all task types are properly enumerated"""
        requirements = TaskEvidenceRequirements()
        task_types = requirements.get_all_task_types()

        expected_types = [
            TaskType.IMPLEMENTATION,
            TaskType.DOCUMENTATION,
            TaskType.COORDINATION,
            TaskType.TESTING,
            TaskType.DEPLOYMENT,
            TaskType.PERFORMANCE,
        ]

        assert len(task_types) == len(expected_types)
        for expected_type in expected_types:
            assert expected_type in task_types

    def test_complexity_levels(self):
        """Test that all complexity levels are properly enumerated"""
        requirements = TaskEvidenceRequirements()
        complexities = requirements.get_all_complexities()

        expected_complexities = [
            TaskComplexity.SIMPLE,
            TaskComplexity.COMPLEX,
            TaskComplexity.CRITICAL,
        ]

        assert len(complexities) == len(expected_complexities)
        for expected_complexity in expected_complexities:
            assert expected_complexity in complexities

    def test_simple_implementation_requirements(self):
        """Test simple implementation task requirements"""
        requirements = TaskEvidenceRequirements()
        reqs = requirements.get_requirements(TaskType.IMPLEMENTATION, TaskComplexity.SIMPLE)

        expected_reqs = ["terminal_output", "test_results", "file_artifacts"]
        assert reqs == expected_reqs
        assert len(reqs) == 3

    def test_complex_documentation_requirements(self):
        """Test complex documentation task requirements"""
        requirements = TaskEvidenceRequirements()
        reqs = requirements.get_requirements(TaskType.DOCUMENTATION, TaskComplexity.COMPLEX)

        expected_reqs = [
            "file_artifact",
            "accessibility_check",
            "cross_references",
            "validation_url",
        ]
        assert reqs == expected_reqs
        assert len(reqs) == 4

    def test_critical_coordination_requirements(self):
        """Test critical coordination task requirements"""
        requirements = TaskEvidenceRequirements()
        reqs = requirements.get_requirements(TaskType.COORDINATION, TaskComplexity.CRITICAL)

        expected_reqs = [
            "handoff_confirmation",
            "status_update",
            "dependency_validation",
            "timeline_proof",
            "stakeholder_approval",
            "rollback_plan",
        ]
        assert reqs == expected_reqs
        assert len(reqs) == 6

    def test_requirements_progression(self):
        """Test that requirements increase with complexity"""
        requirements = TaskEvidenceRequirements()

        for task_type in requirements.get_all_task_types():
            simple_reqs = requirements.get_requirements(task_type, TaskComplexity.SIMPLE)
            complex_reqs = requirements.get_requirements(task_type, TaskComplexity.COMPLEX)
            critical_reqs = requirements.get_requirements(task_type, TaskComplexity.CRITICAL)

            # Requirements should increase with complexity
            assert len(complex_reqs) >= len(
                simple_reqs
            ), f"Complex requirements should be >= simple for {task_type.value}"
            assert len(critical_reqs) >= len(
                complex_reqs
            ), f"Critical requirements should be >= complex for {task_type.value}"

    def test_validation_report_creation(self):
        """Test validation report creation and properties"""
        requirements = TaskEvidenceRequirements()
        provided_evidence = ["terminal_output", "test_results"]

        report = requirements.validate_completeness(
            TaskType.IMPLEMENTATION, TaskComplexity.SIMPLE, provided_evidence
        )

        assert isinstance(report, ValidationReport)
        assert report.required == ["terminal_output", "test_results", "file_artifacts"]
        assert report.provided == provided_evidence
        assert report.missing == ["file_artifacts"]
        assert report.extra == []
        assert report.complete is False
        assert isinstance(report.timestamp, datetime)

    def test_complete_validation(self):
        """Test validation when all requirements are met"""
        requirements = TaskEvidenceRequirements()
        provided_evidence = ["terminal_output", "test_results", "file_artifacts"]

        report = requirements.validate_completeness(
            TaskType.IMPLEMENTATION, TaskComplexity.SIMPLE, provided_evidence
        )

        assert report.complete is True
        assert len(report.missing) == 0
        assert len(report.extra) == 0

    def test_extra_evidence_handling(self):
        """Test validation when extra evidence is provided"""
        requirements = TaskEvidenceRequirements()
        provided_evidence = ["terminal_output", "test_results", "file_artifacts", "extra_evidence"]

        report = requirements.validate_completeness(
            TaskType.IMPLEMENTATION, TaskComplexity.SIMPLE, provided_evidence
        )

        assert report.complete is True
        assert len(report.missing) == 0
        assert report.extra == ["extra_evidence"]

    def test_requirements_summary(self):
        """Test requirements summary generation"""
        requirements = TaskEvidenceRequirements()
        summary = requirements.get_requirements_summary()

        # Summary should include all task types
        assert len(summary) == len(requirements.get_all_task_types())

        # Each task type should have all complexity levels
        for task_type in requirements.get_all_task_types():
            assert len(summary[task_type.value]) == len(requirements.get_all_complexities())

            # Each complexity should have a positive number of requirements
            for complexity in requirements.get_all_complexities():
                assert summary[task_type.value][complexity.value] > 0

    def test_unknown_task_type_handling(self):
        """Test handling of unknown task types"""
        requirements = TaskEvidenceRequirements()

        # This should return an empty list for unknown task types
        reqs = requirements.get_requirements("unknown_task", TaskComplexity.SIMPLE)
        assert reqs == []

    def test_unknown_complexity_handling(self):
        """Test handling of unknown complexity levels"""
        requirements = TaskEvidenceRequirements()

        # This should return an empty list for unknown complexity
        reqs = requirements.get_requirements(TaskType.IMPLEMENTATION, "unknown_complexity")
        assert reqs == []


class TestValidationReport:
    """Test the ValidationReport dataclass"""

    def test_validation_report_creation(self):
        """Test basic validation report creation"""
        report = ValidationReport(
            required=["req1", "req2"], provided=["req1"], missing=["req2"], extra=[], complete=False
        )

        assert report.required == ["req1", "req2"]
        assert report.provided == ["req1"]
        assert report.missing == ["req2"]
        assert report.extra == []
        assert report.complete is False
        assert isinstance(report.timestamp, datetime)

    def test_validation_report_default_timestamp(self):
        """Test that timestamp defaults to current time"""
        before_creation = datetime.now()
        report = ValidationReport(required=[], provided=[], missing=[], extra=[], complete=True)
        after_creation = datetime.now()

        assert before_creation <= report.timestamp <= after_creation

    def test_validation_report_custom_timestamp(self):
        """Test that custom timestamp is respected"""
        custom_timestamp = datetime(2025, 1, 1, 12, 0, 0)
        report = ValidationReport(
            required=[],
            provided=[],
            missing=[],
            extra=[],
            complete=True,
            timestamp=custom_timestamp,
        )

        assert report.timestamp == custom_timestamp

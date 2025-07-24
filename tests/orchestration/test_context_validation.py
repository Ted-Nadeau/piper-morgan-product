"""
Tests for PM-057 Context Validation Framework
Tests the integration between WorkflowFactory validation registry and validation service.
"""

from unittest.mock import Mock

import pytest

from services.domain.models import Intent
from services.orchestration.validation import (
    ContextValidationError,
    WorkflowContextValidator,
    workflow_validator,
)
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntentCategory, WorkflowType


class TestContextValidationFramework:
    """Test the complete context validation framework"""

    @pytest.fixture
    def workflow_factory(self):
        """Create workflow factory with validation registry"""
        return WorkflowFactory()

    @pytest.fixture
    def validator(self):
        """Create context validator"""
        return WorkflowContextValidator()

    @pytest.fixture
    def sample_intent(self):
        """Create sample intent for testing"""
        return Intent(
            id="test-intent-123",
            action="create_ticket",
            category=IntentCategory.EXECUTION,
            context={"original_message": "Create a bug report for the login issue"},
        )

    def test_validation_registry_structure(self, workflow_factory):
        """Test that validation registry has proper structure"""
        registry = workflow_factory.validation_registry

        # Check all workflow types are covered
        expected_types = [
            WorkflowType.CREATE_TICKET,
            WorkflowType.LIST_PROJECTS,
            WorkflowType.ANALYZE_FILE,
            WorkflowType.GENERATE_REPORT,
            WorkflowType.REVIEW_ITEM,
            WorkflowType.PLAN_STRATEGY,
        ]

        for workflow_type in expected_types:
            assert workflow_type in registry

            # Check required structure
            requirements = registry[workflow_type]
            assert "context_requirements" in requirements
            assert "performance_threshold_ms" in requirements
            assert "pre_execution_checks" in requirements

            # Check context requirements structure
            context_req = requirements["context_requirements"]
            assert "critical" in context_req
            assert "important" in context_req
            assert "optional" in context_req
            assert isinstance(context_req["critical"], list)

    def test_get_validation_requirements(self, workflow_factory):
        """Test getting validation requirements for workflow types"""
        # Test existing workflow type
        requirements = workflow_factory.get_validation_requirements(WorkflowType.CREATE_TICKET)
        assert requirements is not None
        assert requirements["performance_threshold_ms"] == 50

        # Test non-existent workflow type
        requirements = workflow_factory.get_validation_requirements("NONEXISTENT")
        assert requirements is None

    def test_performance_threshold_retrieval(self, workflow_factory):
        """Test performance threshold retrieval"""
        # Test existing workflow
        threshold = workflow_factory.get_performance_threshold(WorkflowType.CREATE_TICKET)
        assert threshold == 50

        # Test fallback for non-existent workflow
        threshold = workflow_factory.get_performance_threshold("NONEXISTENT")
        assert threshold == 100  # Default fallback

    def test_successful_validation(self, validator):
        """Test successful context validation"""
        context = {"original_message": "Create a bug report", "project_id": "test-project-123"}

        # Should not raise exception
        validator.validate_workflow_context(WorkflowType.CREATE_TICKET, context)

    def test_missing_required_fields(self, validator):
        """Test validation failure for missing required fields"""
        context = {}  # Missing original_message

        with pytest.raises(ContextValidationError) as exc_info:
            validator.validate_workflow_context(WorkflowType.CREATE_TICKET, context)

        error = exc_info.value
        assert error.details["workflow_type"] == WorkflowType.CREATE_TICKET.value
        assert "original_message" in error.details["missing_fields"]
        assert "create a ticket" in error.user_message.lower()

    def test_file_analysis_context_validation(self, validator):
        """Test context validation for file analysis workflows"""
        # Missing file reference
        context = {"original_message": "Analyze this file"}

        try:
            validator.validate_workflow_context(WorkflowType.ANALYZE_FILE, context)
            # Should succeed - file_id is conditional, not required
        except ContextValidationError:
            pytest.fail("File analysis should succeed with just original_message")

    def test_github_review_validation(self, validator):
        """Test GitHub review context validation"""
        context = {"original_message": "Review this issue"}

        # Should succeed without GitHub URL (it's conditional)
        try:
            validator.validate_workflow_context(WorkflowType.REVIEW_ITEM, context)
        except ContextValidationError:
            pytest.fail("Review item should succeed with just original_message")

    def test_validation_summary_success(self, validator):
        """Test validation summary for successful validation"""
        context = {
            "original_message": "List all projects",
        }

        summary = validator.get_validation_summary(WorkflowType.LIST_PROJECTS, context)
        assert summary["valid"] is True
        assert summary["missing_fields"] == []

    def test_validation_summary_failure(self, validator):
        """Test validation summary for failed validation"""
        context = {}  # Missing original_message

        summary = validator.get_validation_summary(WorkflowType.CREATE_TICKET, context)
        assert summary["valid"] is False
        assert "original_message" in summary["missing_fields"]
        assert len(summary["suggestions"]) > 0
        assert "user_message" in summary

    def test_field_validation_logic(self, validator):
        """Test the field existence and validity logic"""
        # Test valid fields
        assert validator._field_exists_and_valid({"field": "value"}, "field") is True
        assert validator._field_exists_and_valid({"field": ["item"]}, "field") is True
        assert validator._field_exists_and_valid({"field": {"key": "value"}}, "field") is True

        # Test invalid fields
        assert validator._field_exists_and_valid({}, "field") is False
        assert validator._field_exists_and_valid({"field": None}, "field") is False
        assert validator._field_exists_and_valid({"field": ""}, "field") is False
        assert validator._field_exists_and_valid({"field": "   "}, "field") is False
        assert validator._field_exists_and_valid({"field": []}, "field") is False
        assert validator._field_exists_and_valid({"field": {}}, "field") is False

    def test_github_url_validation(self, validator):
        """Test GitHub URL validation logic"""
        # Valid URLs
        valid_urls = [
            "https://github.com/owner/repo",
            "https://github.com/owner/repo/issues/123",
            "https://github.com/owner/repo/pull/456",
            "http://github.com/owner/repo",  # http should work too
        ]

        for url in valid_urls:
            assert validator.validate_github_url(url) is True, f"URL should be valid: {url}"

        # Invalid URLs
        invalid_urls = [
            "",
            None,
            "not-a-url",
            "https://gitlab.com/owner/repo",
            "https://github.com",
            "https://github.com/owner",
        ]

        for url in invalid_urls:
            assert validator.validate_github_url(url) is False, f"URL should be invalid: {url}"

    async def test_workflow_factory_integration(self, workflow_factory, sample_intent):
        """Test integration between WorkflowFactory and validation"""
        # This tests the framework integration rather than specific validation
        workflow = await workflow_factory.create_from_intent(sample_intent)

        # Should create workflow successfully
        assert workflow is not None
        assert workflow.type == WorkflowType.CREATE_TICKET

        # Validation registry should provide requirements for this workflow
        requirements = workflow_factory.get_validation_requirements(workflow.type)
        assert requirements is not None
        assert "original_message" in requirements["context_requirements"]["critical"]

    def test_performance_thresholds_realistic(self, workflow_factory):
        """Test that performance thresholds are realistic"""
        for workflow_type in workflow_factory.validation_registry:
            threshold = workflow_factory.get_performance_threshold(workflow_type)

            # Should be reasonable (between 10ms and 200ms)
            assert (
                10 <= threshold <= 200
            ), f"Threshold {threshold}ms unrealistic for {workflow_type}"

    def test_user_friendly_error_messages(self, validator):
        """Test that error messages are user-friendly"""
        test_cases = [
            {
                "workflow_type": WorkflowType.CREATE_TICKET,
                "context": {},
                "expected_phrases": ["create a ticket", "provide more details"],
            },
            {
                "workflow_type": WorkflowType.ANALYZE_FILE,
                "context": {},
                "expected_phrases": ["analyze a file", "provide more details"],
            },
            {
                "workflow_type": WorkflowType.REVIEW_ITEM,
                "context": {},
                "expected_phrases": ["review an item", "provide more details"],
            },
        ]

        for case in test_cases:
            with pytest.raises(ContextValidationError) as exc_info:
                validator.validate_workflow_context(case["workflow_type"], case["context"])

            error_message = exc_info.value.user_message.lower()
            for phrase in case["expected_phrases"]:
                assert (
                    phrase.lower() in error_message
                ), f"Expected '{phrase}' in error message: {error_message}"

    def test_unknown_workflow_type_handling(self, validator):
        """Test handling of unknown workflow types"""
        # Should not raise exception for unknown workflow types
        try:
            validator.validate_workflow_context("UNKNOWN_WORKFLOW", {"any": "context"})
        except Exception:
            pytest.fail("Unknown workflow types should be allowed to proceed")


class TestValidationPerformance:
    """Test validation performance characteristics"""

    @pytest.fixture
    def validator(self):
        return WorkflowContextValidator()

    def test_validation_speed(self, validator):
        """Test that validation completes within performance thresholds"""
        import time

        context = {"original_message": "Create a ticket for the bug", "project_id": "test-project"}

        # Measure validation time
        start_time = time.time()
        validator.validate_workflow_context(WorkflowType.CREATE_TICKET, context)
        end_time = time.time()

        validation_time_ms = (end_time - start_time) * 1000

        # Should complete well under the 50ms threshold for CREATE_TICKET
        assert (
            validation_time_ms < 50
        ), f"Validation took {validation_time_ms}ms, exceeds 50ms threshold"

    def test_validation_summary_performance(self, validator):
        """Test validation summary performance"""
        import time

        context = {"original_message": "Test message"}

        start_time = time.time()
        summary = validator.get_validation_summary(WorkflowType.LIST_PROJECTS, context)
        end_time = time.time()

        validation_time_ms = (end_time - start_time) * 1000

        # Should complete well under the 30ms threshold for LIST_PROJECTS
        assert (
            validation_time_ms < 30
        ), f"Validation summary took {validation_time_ms}ms, exceeds 30ms threshold"
        assert summary["valid"] is True

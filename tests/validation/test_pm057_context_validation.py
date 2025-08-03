"""
PM-057 Context Validation Tests
Comprehensive testing of pre-execution workflow context validation
"""

from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from services.domain.models import Intent
from services.orchestration.validation import ContextValidationError
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntentCategory, WorkflowType


class TestWorkflowFactoryContextValidation:
    """Test context validation in WorkflowFactory"""

    @pytest.fixture
    def workflow_factory(self):
        """Provide WorkflowFactory instance for tests"""
        return WorkflowFactory()

    @pytest.fixture
    def sample_intent(self):
        """Provide sample intent for testing"""
        return Intent(
            id="test_intent_123",
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.9,
            context={
                "original_message": "Create a ticket for the bug",
                "project_id": "test_project",
            },
        )

    def test_validation_requirements_registration(self, workflow_factory):
        """Test that validation requirements are properly registered"""
        # Check that validation registry exists
        assert hasattr(workflow_factory, "validation_registry")
        assert isinstance(workflow_factory.validation_registry, dict)

        # Check that key workflow types have requirements
        assert WorkflowType.CREATE_TICKET in workflow_factory.validation_registry
        assert WorkflowType.LIST_PROJECTS in workflow_factory.validation_registry
        assert WorkflowType.ANALYZE_FILE in workflow_factory.validation_registry

    def test_get_validation_requirements(self, workflow_factory):
        """Test getting validation requirements for workflow types"""
        # Test CREATE_TICKET requirements
        requirements = workflow_factory.get_validation_requirements(WorkflowType.CREATE_TICKET)
        assert requirements is not None
        assert "context_requirements" in requirements
        assert "critical" in requirements["context_requirements"]
        assert "important" in requirements["context_requirements"]

        # Test LIST_PROJECTS requirements
        requirements = workflow_factory.get_validation_requirements(WorkflowType.LIST_PROJECTS)
        assert requirements is not None
        assert "context_requirements" in requirements

        # Test non-existent workflow type
        requirements = workflow_factory.get_validation_requirements(WorkflowType.UNKNOWN)
        assert requirements is None

    def test_get_performance_threshold(self, workflow_factory):
        """Test getting performance thresholds"""
        # Test CREATE_TICKET threshold
        threshold = workflow_factory.get_performance_threshold(WorkflowType.CREATE_TICKET)
        assert isinstance(threshold, int)
        assert threshold > 0

        # Test default threshold for unknown workflow
        threshold = workflow_factory.get_performance_threshold(WorkflowType.UNKNOWN)
        assert threshold == 100  # Default value

    def test_field_exists_and_valid(self, workflow_factory):
        """Test field validation logic"""
        context = {
            "valid_field": "has_value",
            "empty_string": "",
            "none_value": None,
            "empty_list": [],
            "empty_dict": {},
            "valid_list": ["item"],
            "valid_dict": {"key": "value"},
        }

        # Test valid fields
        assert workflow_factory._field_exists_and_valid(context, "valid_field")
        assert workflow_factory._field_exists_and_valid(context, "valid_list")
        assert workflow_factory._field_exists_and_valid(context, "valid_dict")

        # Test invalid fields
        assert not workflow_factory._field_exists_and_valid(context, "empty_string")
        assert not workflow_factory._field_exists_and_valid(context, "none_value")
        assert not workflow_factory._field_exists_and_valid(context, "empty_list")
        assert not workflow_factory._field_exists_and_valid(context, "empty_dict")
        assert not workflow_factory._field_exists_and_valid(context, "missing_field")

    def test_generate_field_suggestions(self, workflow_factory):
        """Test generation of field suggestions"""
        missing_fields = [
            "original_message",
            "project_id",
            "file_id",
            "repository",
            "github_url",
            "unknown_field",
        ]

        suggestions = workflow_factory._generate_field_suggestions(
            WorkflowType.CREATE_TICKET, missing_fields
        )

        # Verify suggestions were generated
        assert len(suggestions) == len(missing_fields)

        # Check specific suggestions
        assert any("more details" in s for s in suggestions)  # original_message
        assert any("project" in s for s in suggestions)  # project_id
        assert any("file" in s for s in suggestions)  # file_id
        assert any("repository" in s for s in suggestions)  # repository
        assert any("GitHub" in s for s in suggestions)  # github_url
        assert any("unknown_field" in s for s in suggestions)  # unknown_field

    def test_validate_workflow_context_success(self, workflow_factory, sample_intent):
        """Test successful context validation"""
        # Test with valid context
        workflow_factory._validate_workflow_context(
            WorkflowType.CREATE_TICKET, sample_intent, {"additional_context": "value"}
        )
        # Should not raise any exception

    def test_validate_workflow_context_missing_critical(self, workflow_factory):
        """Test context validation with missing critical fields"""
        intent = Intent(
            id="test_intent_123",
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.9,
            context={},  # Missing original_message
        )

        # Should raise ContextValidationError
        with pytest.raises(ContextValidationError) as exc_info:
            workflow_factory._validate_workflow_context(WorkflowType.CREATE_TICKET, intent)

        error = exc_info.value
        assert error.workflow_type == WorkflowType.CREATE_TICKET
        assert "original_message" in error.missing_fields
        assert len(error.suggestions) > 0

    def test_validate_workflow_context_missing_important(self, workflow_factory):
        """Test context validation with missing important fields (should warn but not fail)"""
        intent = Intent(
            id="test_intent_123",
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.9,
            context={
                "original_message": "Create a ticket"  # Has critical field
                # Missing project_id (important field)
            },
        )

        # Should not raise exception, but should log warning
        with patch("builtins.print") as mock_print:
            workflow_factory._validate_workflow_context(WorkflowType.CREATE_TICKET, intent)

            # Check that warning was logged
            mock_print.assert_called_with(
                "  ⚠️  Missing important fields for create_ticket: ['project_id']"
            )

    def test_validate_workflow_context_no_requirements(self, workflow_factory, sample_intent):
        """Test validation when no requirements are defined"""
        # Test with unknown workflow type
        workflow_factory._validate_workflow_context(WorkflowType.UNKNOWN, sample_intent)
        # Should not raise any exception

    def test_validate_workflow_context_none_workflow_type(self, workflow_factory, sample_intent):
        """Test validation with None workflow type"""
        workflow_factory._validate_workflow_context(None, sample_intent)
        # Should not raise any exception

    @patch("services.orchestration.workflow_factory.WorkflowFactory._validate_workflow_context")
    def test_create_from_intent_with_validation(
        self, mock_validate, workflow_factory, sample_intent
    ):
        """Test that create_from_intent calls validation"""
        # Mock successful validation
        mock_validate.return_value = None

        # Create workflow
        workflow = workflow_factory.create_from_intent(sample_intent)

        # Verify validation was called
        mock_validate.assert_called_once()
        assert workflow is not None

    @patch("services.orchestration.workflow_factory.WorkflowFactory._validate_workflow_context")
    def test_create_from_intent_validation_failure(
        self, mock_validate, workflow_factory, sample_intent
    ):
        """Test that create_from_intent raises validation error"""
        # Mock validation failure
        mock_validate.side_effect = ContextValidationError(
            workflow_type=WorkflowType.CREATE_TICKET,
            missing_fields=["original_message"],
            suggestions=["Please provide more details"],
        )

        # Should raise ContextValidationError
        with pytest.raises(ContextValidationError):
            workflow_factory.create_from_intent(sample_intent)


class TestContextValidationError:
    """Test ContextValidationError exception"""

    def test_context_validation_error_creation(self):
        """Test creating ContextValidationError instances"""
        error = ContextValidationError(
            workflow_type=WorkflowType.CREATE_TICKET,
            missing_fields=["original_message", "project_id"],
            suggestions=["Please provide more details", "Please specify the project"],
            details={"additional_info": "test"},
        )

        assert error.workflow_type == WorkflowType.CREATE_TICKET
        assert error.missing_fields == ["original_message", "project_id"]
        assert error.suggestions == ["Please provide more details", "Please specify the project"]
        assert error.details["additional_info"] == "test"
        assert error.details["workflow_type"] == "create_ticket"
        assert error.details["missing_fields"] == ["original_message", "project_id"]
        assert error.details["suggestions"] == [
            "Please provide more details",
            "Please specify the project",
        ]

    def test_user_message_creation(self):
        """Test user-friendly message creation"""
        error = ContextValidationError(
            workflow_type=WorkflowType.CREATE_TICKET,
            missing_fields=["original_message"],
            suggestions=["Please provide more details about what you want me to do."],
        )

        # Check that user message was created
        assert hasattr(error, "user_message")
        assert "create a ticket" in error.user_message.lower()
        assert "more details" in error.user_message

    def test_user_message_with_project_id_missing(self):
        """Test user message for missing project_id"""
        error = ContextValidationError(
            workflow_type=WorkflowType.CREATE_TICKET,
            missing_fields=["project_id"],
            suggestions=["Please specify which project you're working with."],
        )

        assert "project" in error.user_message.lower()
        assert "create a ticket" in error.user_message.lower()

    def test_user_message_with_file_id_missing(self):
        """Test user message for missing file_id"""
        error = ContextValidationError(
            workflow_type=WorkflowType.ANALYZE_FILE,
            missing_fields=["file_id"],
            suggestions=["Please specify which file you want me to analyze."],
        )

        assert "file" in error.user_message.lower()
        assert "analyze" in error.user_message.lower()

    def test_user_message_with_github_url_missing(self):
        """Test user message for missing github_url"""
        error = ContextValidationError(
            workflow_type=WorkflowType.REVIEW_ITEM,
            missing_fields=["github_url"],
            suggestions=["Please provide a GitHub issue or pull request URL."],
        )

        assert "github" in error.user_message.lower()
        assert "review" in error.user_message.lower()


class TestWorkflowTypeValidationRequirements:
    """Test validation requirements for different workflow types"""

    @pytest.fixture
    def workflow_factory(self):
        """Provide WorkflowFactory instance for tests"""
        return WorkflowFactory()

    def test_create_ticket_requirements(self, workflow_factory):
        """Test CREATE_TICKET validation requirements"""
        requirements = workflow_factory.get_validation_requirements(WorkflowType.CREATE_TICKET)

        assert requirements is not None
        assert "context_requirements" in requirements
        assert "critical" in requirements["context_requirements"]
        assert "important" in requirements["context_requirements"]
        assert "optional" in requirements["context_requirements"]

        critical_fields = requirements["context_requirements"]["critical"]
        important_fields = requirements["context_requirements"]["important"]

        assert "original_message" in critical_fields
        assert "project_id" in important_fields or "repository" in important_fields

    def test_list_projects_requirements(self, workflow_factory):
        """Test LIST_PROJECTS validation requirements"""
        requirements = workflow_factory.get_validation_requirements(WorkflowType.LIST_PROJECTS)

        assert requirements is not None
        assert "context_requirements" in requirements
        assert "critical" in requirements["context_requirements"]

        critical_fields = requirements["context_requirements"]["critical"]
        assert "original_message" in critical_fields

    def test_analyze_file_requirements(self, workflow_factory):
        """Test ANALYZE_FILE validation requirements"""
        requirements = workflow_factory.get_validation_requirements(WorkflowType.ANALYZE_FILE)

        assert requirements is not None
        assert "context_requirements" in requirements
        assert "critical" in requirements["context_requirements"]
        assert "important" in requirements["context_requirements"]

        critical_fields = requirements["context_requirements"]["critical"]
        important_fields = requirements["context_requirements"]["important"]

        assert "original_message" in critical_fields
        assert "file_id" in important_fields or "resolved_file_id" in important_fields

    def test_generate_report_requirements(self, workflow_factory):
        """Test GENERATE_REPORT validation requirements"""
        requirements = workflow_factory.get_validation_requirements(WorkflowType.GENERATE_REPORT)

        assert requirements is not None
        assert "context_requirements" in requirements
        assert "critical" in requirements["context_requirements"]

        critical_fields = requirements["context_requirements"]["critical"]
        assert "original_message" in critical_fields


class TestIntegrationScenarios:
    """Test integration scenarios for context validation"""

    @pytest.fixture
    def workflow_factory(self):
        """Provide WorkflowFactory instance for tests"""
        return WorkflowFactory()

    def test_create_ticket_with_full_context(self, workflow_factory):
        """Test CREATE_TICKET with complete context"""
        intent = Intent(
            id="test_intent_123",
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.9,
            context={
                "original_message": "Create a ticket for the bug",
                "project_id": "test_project",
                "repository": "test_repo",
                "labels": ["bug", "high-priority"],
                "priority": "high",
            },
        )

        # Should not raise any exception
        workflow = workflow_factory.create_from_intent(intent)
        assert workflow is not None
        assert workflow.type == WorkflowType.CREATE_TICKET

    def test_create_ticket_with_minimal_context(self, workflow_factory):
        """Test CREATE_TICKET with minimal required context"""
        intent = Intent(
            id="test_intent_123",
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.9,
            context={"original_message": "Create a ticket"},  # Only critical field
        )

        # Should not raise any exception (important fields are optional)
        workflow = workflow_factory.create_from_intent(intent)
        assert workflow is not None
        assert workflow.type == WorkflowType.CREATE_TICKET

    def test_create_ticket_without_context(self, workflow_factory):
        """Test CREATE_TICKET without required context"""
        intent = Intent(
            id="test_intent_123",
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.9,
            context={},  # Missing original_message
        )

        # Should raise ContextValidationError
        with pytest.raises(ContextValidationError) as exc_info:
            workflow_factory.create_from_intent(intent)

        error = exc_info.value
        assert "original_message" in error.missing_fields

    def test_analyze_file_with_file_context(self, workflow_factory):
        """Test ANALYZE_FILE with file context"""
        intent = Intent(
            id="test_intent_123",
            category=IntentCategory.ANALYSIS,
            action="analyze_file",
            confidence=0.9,
            context={
                "original_message": "Analyze the uploaded file",
                "file_id": "test_file_123",
                "analysis_type": "comprehensive",
            },
        )

        # Should not raise any exception
        workflow = workflow_factory.create_from_intent(intent)
        assert workflow is not None
        assert workflow.type == WorkflowType.ANALYZE_FILE

    def test_list_projects_with_context(self, workflow_factory):
        """Test LIST_PROJECTS with context"""
        intent = Intent(
            id="test_intent_123",
            category=IntentCategory.EXECUTION,
            action="list_projects",
            confidence=0.9,
            context={"original_message": "Show me all projects", "filter_criteria": "active"},
        )

        # Should not raise any exception
        workflow = workflow_factory.create_from_intent(intent)
        assert workflow is not None
        assert workflow.type == WorkflowType.LIST_PROJECTS

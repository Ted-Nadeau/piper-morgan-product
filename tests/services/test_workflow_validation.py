"""
Test Workflow Context Validation
Implements PM-057: Validation Rules & User Experience

Tests the validation rules and user-friendly error messages for workflow context.
"""

import pytest
from unittest.mock import Mock

from services.orchestration.validation import (
    WorkflowContextValidator, 
    ContextValidationError, 
    workflow_validator
)
from services.shared_types import WorkflowType


class TestWorkflowContextValidator:
    """Test workflow context validation rules"""

    def test_create_ticket_with_project_context(self):
        """Test CREATE_TICKET workflow with valid project context"""
        context = {
            "original_message": "create ticket for bug fix",
            "project_id": "test-project-123"
        }
        
        # Should not raise an exception
        workflow_validator.validate_workflow_context(WorkflowType.CREATE_TICKET, context)

    def test_create_ticket_without_project_context(self):
        """Test CREATE_TICKET workflow without project context - should pass with default repo"""
        context = {
            "original_message": "create ticket for bug fix"
        }
        
        # Should not raise an exception (uses default repository)
        workflow_validator.validate_workflow_context(WorkflowType.CREATE_TICKET, context)

    def test_create_ticket_missing_original_message(self):
        """Test CREATE_TICKET workflow missing required original_message"""
        context = {
            "project_id": "test-project-123"
        }
        
        with pytest.raises(ContextValidationError) as exc_info:
            workflow_validator.validate_workflow_context(WorkflowType.CREATE_TICKET, context)
        
        error = exc_info.value
        assert "original_message" in error.details["missing_fields"]
        assert "create a ticket" in error.user_message
        assert "need to know what you want me to do" in error.user_message

    def test_analyze_file_with_file_reference(self):
        """Test ANALYZE_FILE workflow with valid file reference"""
        context = {
            "original_message": "analyze the uploaded report.pdf",
            "file_id": "file-123"
        }
        
        # Should not raise an exception
        workflow_validator.validate_workflow_context(WorkflowType.ANALYZE_FILE, context)

    def test_analyze_file_without_file_reference(self):
        """Test ANALYZE_FILE workflow without file reference - should pass but provide suggestions"""
        context = {
            "original_message": "analyze file"
        }
        
        # Should not raise an exception (file_id is conditional, not required)
        workflow_validator.validate_workflow_context(WorkflowType.ANALYZE_FILE, context)

    def test_analyze_file_missing_original_message(self):
        """Test ANALYZE_FILE workflow missing required original_message"""
        context = {
            "file_id": "file-123"
        }
        
        with pytest.raises(ContextValidationError) as exc_info:
            workflow_validator.validate_workflow_context(WorkflowType.ANALYZE_FILE, context)
        
        error = exc_info.value
        assert "original_message" in error.details["missing_fields"]
        assert "analyze a file" in error.user_message

    def test_list_projects_minimal_context(self):
        """Test LIST_PROJECTS workflow with minimal context"""
        context = {
            "original_message": "list projects"
        }
        
        # Should not raise an exception
        workflow_validator.validate_workflow_context(WorkflowType.LIST_PROJECTS, context)

    def test_list_projects_missing_original_message(self):
        """Test LIST_PROJECTS workflow missing required original_message"""
        context = {}
        
        with pytest.raises(ContextValidationError) as exc_info:
            workflow_validator.validate_workflow_context(WorkflowType.LIST_PROJECTS, context)
        
        error = exc_info.value
        assert "original_message" in error.details["missing_fields"]
        assert "list projects" in error.user_message

    def test_review_item_with_github_url(self):
        """Test REVIEW_ITEM workflow with GitHub URL"""
        context = {
            "original_message": "review this issue",
            "github_url": "https://github.com/user/repo/issues/123"
        }
        
        # Should not raise an exception
        workflow_validator.validate_workflow_context(WorkflowType.REVIEW_ITEM, context)

    def test_review_item_without_github_url(self):
        """Test REVIEW_ITEM workflow without GitHub URL - should pass but provide suggestions"""
        context = {
            "original_message": "review item"
        }
        
        # Should not raise an exception (github_url is conditional, not required)
        workflow_validator.validate_workflow_context(WorkflowType.REVIEW_ITEM, context)

    def test_generate_report_with_context(self):
        """Test GENERATE_REPORT workflow with various context options"""
        context = {
            "original_message": "generate performance report",
            "file_id": "file-123",
            "project_id": "project-456"
        }
        
        # Should not raise an exception
        workflow_validator.validate_workflow_context(WorkflowType.GENERATE_REPORT, context)

    def test_plan_strategy_with_project_context(self):
        """Test PLAN_STRATEGY workflow with project context"""
        context = {
            "original_message": "plan strategy for Q4",
            "project_id": "project-123"
        }
        
        # Should not raise an exception
        workflow_validator.validate_workflow_context(WorkflowType.PLAN_STRATEGY, context)

    def test_empty_context_values(self):
        """Test validation with empty context values"""
        context = {
            "original_message": "",  # Empty string
            "project_id": None,      # None value
            "file_id": [],           # Empty list
            "github_url": {}         # Empty dict
        }
        
        with pytest.raises(ContextValidationError) as exc_info:
            workflow_validator.validate_workflow_context(WorkflowType.CREATE_TICKET, context)
        
        error = exc_info.value
        assert "original_message" in error.details["missing_fields"]

    def test_unknown_workflow_type(self):
        """Test validation with unknown workflow type"""
        context = {
            "original_message": "test message"
        }
        
        # Should not raise an exception for unknown workflow types
        workflow_validator.validate_workflow_context("UNKNOWN_WORKFLOW", context)

    def test_validation_summary_valid_context(self):
        """Test validation summary with valid context"""
        context = {
            "original_message": "create ticket for bug fix",
            "project_id": "test-project-123"
        }
        
        summary = workflow_validator.get_validation_summary(WorkflowType.CREATE_TICKET, context)
        
        assert summary["valid"] is True
        assert summary["missing_fields"] == []
        assert "suggestions" in summary

    def test_validation_summary_invalid_context(self):
        """Test validation summary with invalid context"""
        context = {
            "project_id": "test-project-123"
            # Missing original_message
        }
        
        summary = workflow_validator.get_validation_summary(WorkflowType.CREATE_TICKET, context)
        
        assert summary["valid"] is False
        assert "original_message" in summary["missing_fields"]
        assert "user_message" in summary
        assert "create a ticket" in summary["user_message"]

    def test_github_url_validation(self):
        """Test GitHub URL validation"""
        validator = WorkflowContextValidator()
        
        # Valid URLs
        assert validator.validate_github_url("https://github.com/user/repo/issues/123")
        assert validator.validate_github_url("https://github.com/user/repo/pull/456")
        assert validator.validate_github_url("https://github.com/user/repo")
        
        # Invalid URLs
        assert not validator.validate_github_url("")
        assert not validator.validate_github_url("https://gitlab.com/user/repo")
        assert not validator.validate_github_url("not-a-url")
        assert not validator.validate_github_url("https://github.com")  # Incomplete


class TestContextValidationError:
    """Test ContextValidationError user message generation"""

    def test_create_ticket_error_message(self):
        """Test error message for CREATE_TICKET missing project"""
        error = ContextValidationError(
            workflow_type=WorkflowType.CREATE_TICKET,
            missing_fields=["project_id"],
            suggestions=["Try specifying a project"]
        )
        
        assert "create a ticket" in error.user_message
        assert "project" in error.user_message
        assert "Try:" in error.user_message

    def test_analyze_file_error_message(self):
        """Test error message for ANALYZE_FILE missing file reference"""
        error = ContextValidationError(
            workflow_type=WorkflowType.ANALYZE_FILE,
            missing_fields=["file_id"],
            suggestions=["Try specifying a file"]
        )
        
        assert "analyze a file" in error.user_message
        assert "file" in error.user_message
        assert "Try:" in error.user_message

    def test_review_item_error_message(self):
        """Test error message for REVIEW_ITEM missing GitHub URL"""
        error = ContextValidationError(
            workflow_type=WorkflowType.REVIEW_ITEM,
            missing_fields=["github_url"],
            suggestions=["Try providing a GitHub URL"]
        )
        
        assert "review an item" in error.user_message
        assert "GitHub URL" in error.user_message
        assert "Try:" in error.user_message

    def test_generic_error_message(self):
        """Test generic error message for unknown workflow type"""
        error = ContextValidationError(
            workflow_type="UNKNOWN_WORKFLOW",
            missing_fields=["some_field"],
            suggestions=["Try providing more information"]
        )
        
        assert "complete this task" in error.user_message
        assert "Try providing more information" in error.user_message 
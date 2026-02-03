"""
Test suite for WorkflowRepository migration to Pattern #1
Following TDD approach for find_by_id() method implementation
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

import pytest

from services.database.models import Workflow as WorkflowDB
from services.database.repositories import WorkflowRepository
from services.domain.models import Workflow as DomainWorkflow
from services.shared_types import WorkflowStatus, WorkflowType


class TestWorkflowRepositoryMigration:
    """Test WorkflowRepository Pattern #1 compliance and find_by_id() method"""

    @pytest.mark.smoke
    async def test_repository_inherits_from_base(self, async_transaction):
        """Test that WorkflowRepository inherits from BaseRepository"""
        from services.database.repositories import BaseRepository

        async with async_transaction as session:
            repo = WorkflowRepository(session)
            assert isinstance(repo, BaseRepository)
            assert repo.model == WorkflowDB

    @pytest.mark.smoke
    async def test_find_by_id_method_exists(self, async_transaction):
        """Test that find_by_id() method exists and has correct signature"""
        async with async_transaction as session:
            repo = WorkflowRepository(session)

            # Method should exist
            assert hasattr(repo, "find_by_id")

            # Should be callable
            assert callable(getattr(repo, "find_by_id"))

    @pytest.mark.smoke
    async def test_find_by_id_returns_domain_workflow(self, async_transaction):
        """Test that find_by_id() returns domain Workflow object"""
        async with async_transaction as session:
            repo = WorkflowRepository(session)

            # Create a test workflow in database
            workflow_id = str(uuid.uuid4())
            db_workflow = WorkflowDB(
                id=workflow_id,
                type=WorkflowType.CREATE_TASK,
                status=WorkflowStatus.COMPLETED,
                input_data={"test": "data"},
                output_data={"result": "success"},
                context={"project": "test"},
                created_at=datetime.now(timezone.utc),
            )

            session.add(db_workflow)
            await session.flush()  # Ensure data is available in same transaction

            # Test find_by_id returns domain object
            result = await repo.find_by_id(workflow_id)

            # Should return domain Workflow, not DB model
            assert isinstance(result, DomainWorkflow)
            assert result.id == workflow_id
            assert result.type == WorkflowType.CREATE_TASK
            assert result.status == WorkflowStatus.COMPLETED
            assert result.context == {"project": "test"}

    @pytest.mark.smoke
    async def test_find_by_id_returns_none_for_nonexistent(self, async_transaction):
        """Test that find_by_id() returns None for non-existent workflow"""
        async with async_transaction as session:
            repo = WorkflowRepository(session)

            nonexistent_id = str(uuid.uuid4())
            result = await repo.find_by_id(nonexistent_id)

            assert result is None

    @pytest.mark.smoke
    async def test_find_by_id_handles_database_conversion(self, async_transaction):
        """Test that find_by_id() properly converts DB model to domain model"""
        async with async_transaction as session:
            repo = WorkflowRepository(session)

            # Create workflow with specific data to test conversion
            workflow_id = str(uuid.uuid4())
            created_time = datetime.now(timezone.utc)

            db_workflow = WorkflowDB(
                id=workflow_id,
                type=WorkflowType.ANALYZE_FILE,
                status=WorkflowStatus.RUNNING,
                input_data={"file_id": "test-file"},
                output_data=None,  # Still running
                context={"analysis_type": "document"},
                error=None,
                created_at=created_time,
                started_at=created_time,
                completed_at=None,
            )

            session.add(db_workflow)
            await session.flush()  # Ensure data is available in same transaction

            # Retrieve and verify conversion
            domain_workflow = await repo.find_by_id(workflow_id)

            assert domain_workflow is not None
            assert domain_workflow.id == workflow_id
            assert domain_workflow.type == WorkflowType.ANALYZE_FILE
            assert domain_workflow.status == WorkflowStatus.RUNNING
            assert domain_workflow.context == {"analysis_type": "document"}
            assert domain_workflow.result is None  # output_data was None
            assert domain_workflow.error is None
            assert domain_workflow.created_at == created_time

    @pytest.mark.smoke
    async def test_find_by_id_compatible_with_legacy_interface(self, async_transaction):
        """Test that find_by_id() provides same interface as legacy version"""
        async with async_transaction as session:
            repo = WorkflowRepository(session)

            # Create test workflow
            workflow_id = str(uuid.uuid4())
            db_workflow = WorkflowDB(
                id=workflow_id,
                type=WorkflowType.ANALYZE_FILE,
                status=WorkflowStatus.COMPLETED,
                context={"file_type": "pdf"},
                output_data={"pages": 10},
                created_at=datetime.now(timezone.utc),
            )

            session.add(db_workflow)
            await session.flush()  # Ensure data is available in same transaction

            # Test method signature matches legacy
            result = await repo.find_by_id(workflow_id)

            # Should return workflow object (not Optional typing in runtime)
            assert result is not None

            # Should have same attributes as legacy would return
            assert hasattr(result, "id")
            assert hasattr(result, "type")
            assert hasattr(result, "status")
            assert hasattr(result, "context")
            assert hasattr(result, "result")  # This is output_data in domain model

            # Verify actual values match what legacy would return
            assert result.id == workflow_id
            assert result.type == WorkflowType.ANALYZE_FILE
            assert result.status == WorkflowStatus.COMPLETED

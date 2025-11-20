"""
Test coverage for OrchestrationEngine
Tests the core orchestration logic without external dependencies
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Intent, IntentCategory, Task, UploadedFile, Workflow
from services.orchestration.engine import OrchestrationEngine, TaskResult
from services.shared_types import TaskStatus, TaskType, WorkflowStatus, WorkflowType


class TestOrchestrationEngine:
    """Test OrchestrationEngine core functionality"""

    @pytest.fixture
    def engine(self):
        """Create a fresh OrchestrationEngine instance for each test"""
        # Provide mock llm_client to avoid container initialization requirement
        from services.llm.clients import LLMClient

        mock_llm = Mock(spec=LLMClient)
        return OrchestrationEngine(llm_client=mock_llm)

    @pytest.fixture
    def mock_intent(self):
        """Create a mock analyze_file intent"""
        return Intent(
            id="test-intent-123",
            category=IntentCategory.ANALYSIS,
            action="analyze_file",
            confidence=0.95,
            context={"file_id": "test-file-123", "filename": "test.csv"},
        )

    @pytest.fixture
    def mock_workflow(self):
        """Create a mock workflow with analyze_file task"""
        workflow = Workflow(
            id="test-workflow-123",
            type=WorkflowType.ANALYZE_FILE,
            status=WorkflowStatus.PENDING,
            context={"file_id": "test-file-123", "filename": "test.csv"},
        )
        task = Task(
            id="test-task-123",
            name="Analyze File",
            type=TaskType.ANALYZE_FILE,
            status=TaskStatus.PENDING,
        )
        workflow.tasks.append(task)
        return workflow

    @pytest.fixture
    def mock_file_metadata(self):
        """Create mock file metadata"""
        return UploadedFile(
            id="test-file-123",
            session_id="test-session",
            filename="test.csv",
            file_type="text/csv",
            file_size=1024,
            storage_path="tests/fixtures/sample_data.csv",
            upload_time=datetime.now(),
        )

    @pytest.mark.asyncio
    async def test_create_workflow_from_intent_success(self, engine, mock_intent):
        """Test successful workflow creation from intent"""
        # Mock the factory to return a workflow
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "test-workflow-123"
        mock_workflow.type = WorkflowType.CREATE_TICKET
        mock_workflow.status = WorkflowStatus.PENDING
        mock_workflow.tasks = []
        mock_workflow.context = {}

        with patch.object(
            engine.factory, "create_from_intent", new_callable=AsyncMock
        ) as mock_factory:
            mock_factory.return_value = mock_workflow
            result = await engine.create_workflow_from_intent(mock_intent)

        # Verify workflow was created and stored
        assert result is not None
        assert result.id == "test-workflow-123"
        assert engine.workflows["test-workflow-123"] == mock_workflow

        # Verify factory was called
        mock_factory.assert_called_once_with(mock_intent)

    @pytest.mark.asyncio
    async def test_create_workflow_from_intent_failure(self, engine, mock_intent):
        """Test workflow creation when factory returns None"""
        with patch.object(
            engine.factory, "create_from_intent", new_callable=AsyncMock
        ) as mock_factory:
            mock_factory.return_value = None

            result = await engine.create_workflow_from_intent(mock_intent)

        # Verify no workflow was created
        assert result is None
        assert len(engine.workflows) == 0

    @pytest.mark.asyncio
    async def test_execute_workflow_not_found(self, engine):
        """Test executing a non-existent workflow"""
        with pytest.raises(ValueError, match="Workflow test-missing not found"):
            await engine.execute_workflow("test-missing")

    # DELETED: test_analyze_file_success - OrchestrationEngine._analyze_file method no longer exists

    # DELETED: test_analyze_file_missing_file_id - OrchestrationEngine._analyze_file method no longer exists

    # DELETED: test_analyze_file_file_not_found - OrchestrationEngine._analyze_file method no longer exists

    # DELETED: test_analyze_file_analysis_exception - OrchestrationEngine._analyze_file method no longer exists

    # DELETED: test_task_handler_registration - OrchestrationEngine.task_handlers attribute no longer exists

    # DELETED: test_placeholder_handler - OrchestrationEngine._placeholder_handler method no longer exists

    @pytest.mark.asyncio
    async def test_workflow_state_transitions(self, engine):
        """Test workflow state transitions through execution using real domain models"""
        from services.domain.models import (
            Task,
            TaskStatus,
            TaskType,
            Workflow,
            WorkflowStatus,
            WorkflowType,
        )

        workflow = Workflow(
            id="test-workflow-123",
            type=WorkflowType.CREATE_TICKET,
            status=WorkflowStatus.PENDING,
            tasks=[
                Task(
                    id="task-1",
                    name="Create Work Item",
                    type=TaskType.CREATE_WORK_ITEM,
                    status=TaskStatus.PENDING,
                )
            ],
            context={},
        )
        engine.workflows[workflow.id] = workflow

        # Simulate execution (mock only the actual task execution)
        from services.orchestration.engine import TaskResult

        def complete_task_side_effect(task_obj, workflow_obj):
            task_obj.status = TaskStatus.COMPLETED
            return TaskResult(
                task_id=task_obj.id,
                status=TaskStatus.COMPLETED,
                output_data={},
            )

        with patch.object(engine, "_execute_task", new_callable=AsyncMock) as mock_exec_task:
            mock_exec_task.side_effect = complete_task_side_effect
            result = await engine.execute_workflow(workflow.id)

        # Assert workflow is now complete or in expected state
        assert result is not None
        assert workflow.is_complete() or all(t.status != TaskStatus.PENDING for t in workflow.tasks)

    @pytest.mark.asyncio
    async def test_workflow_error_handling(self, engine):
        """Test workflow error handling and status updates using real domain models"""
        from services.domain.models import (
            Task,
            TaskStatus,
            TaskType,
            Workflow,
            WorkflowStatus,
            WorkflowType,
        )

        workflow = Workflow(
            id="test-workflow-123",
            type=WorkflowType.CREATE_TICKET,
            status=WorkflowStatus.PENDING,
            tasks=[
                Task(
                    id="task-1",
                    name="Create Work Item",
                    type=TaskType.CREATE_WORK_ITEM,
                    status=TaskStatus.PENDING,
                )
            ],
            context={},
        )
        engine.workflows[workflow.id] = workflow

        # Simulate execution failure
        with patch.object(engine, "_execute_task", new_callable=AsyncMock) as mock_exec_task:
            mock_exec_task.side_effect = Exception("Task execution failed")
            # execute_workflow now catches exceptions and returns WorkflowResult instead of re-raising
            result = await engine.execute_workflow(workflow.id)

        # Assert workflow status was updated to failed
        assert workflow.status == WorkflowStatus.FAILED
        assert workflow.error is not None
        # Assert result indicates failure
        assert result is not None
        assert result.status == WorkflowStatus.FAILED
        assert "Task execution failed" in result.error_message

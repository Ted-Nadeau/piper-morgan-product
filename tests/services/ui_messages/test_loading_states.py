"""Tests for LoadingStatesService"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from services.ui_messages.loading_states import (
    LoadingState,
    LoadingStatesService,
    OperationType,
    ProgressUpdate,
    complete_loading,
    start_loading,
    track_loading_operation,
    update_loading,
)


class TestLoadingStatesService:
    """Test loading states service functionality"""

    @pytest.fixture
    def service(self):
        """LoadingStatesService instance for testing"""
        return LoadingStatesService()

    def test_start_operation(self, service):
        """Test starting a loading operation"""
        operation_id = service.start_operation(
            OperationType.LLM_QUERY, "Processing your question", estimated_duration_seconds=30
        )

        assert operation_id is not None
        assert operation_id in service.active_operations

        operation = service.active_operations[operation_id]
        assert operation.operation_type == OperationType.LLM_QUERY
        assert operation.description == "Processing your question"
        assert operation.estimated_duration_seconds == 30
        assert operation.current_state == LoadingState.STARTING
        assert len(operation.progress_updates) == 1

    def test_update_progress(self, service):
        """Test updating operation progress"""
        operation_id = service.start_operation(OperationType.WORKFLOW_EXECUTION, "Running workflow")

        service.update_progress(
            operation_id,
            LoadingState.IN_PROGRESS,
            "Executing step 1 of 3",
            progress_percent=33,
            current_step="Initialize",
            total_steps=3,
            current_step_number=1,
        )

        operation = service.active_operations[operation_id]
        assert operation.current_state == LoadingState.IN_PROGRESS
        assert len(operation.progress_updates) == 2

        latest_update = operation.progress_updates[-1]
        assert latest_update.state == LoadingState.IN_PROGRESS
        assert latest_update.message == "Executing step 1 of 3"
        assert latest_update.progress_percent == 33
        assert latest_update.current_step == "Initialize"
        assert latest_update.total_steps == 3
        assert latest_update.current_step_number == 1

    def test_complete_operation_success(self, service):
        """Test completing operation successfully"""
        operation_id = service.start_operation(OperationType.GITHUB_API, "Fetching GitHub data")

        service.complete_operation(
            operation_id,
            success=True,
            final_message="Data retrieved successfully!",
            result_metadata={"items_count": 42},
        )

        operation = service.active_operations[operation_id]
        assert operation.current_state == LoadingState.COMPLETED

        latest_update = operation.progress_updates[-1]
        assert latest_update.state == LoadingState.COMPLETED
        assert latest_update.message == "Data retrieved successfully!"
        assert latest_update.progress_percent == 100
        assert latest_update.metadata["items_count"] == 42

    def test_complete_operation_failure(self, service):
        """Test completing operation with failure"""
        operation_id = service.start_operation(OperationType.DATABASE_QUERY, "Searching database")

        service.complete_operation(
            operation_id, success=False, final_message="Database connection failed"
        )

        operation = service.active_operations[operation_id]
        assert operation.current_state == LoadingState.FAILED

        latest_update = operation.progress_updates[-1]
        assert latest_update.state == LoadingState.FAILED
        assert latest_update.message == "Database connection failed"

    def test_get_operation_status(self, service):
        """Test getting operation status"""
        operation_id = service.start_operation(OperationType.FILE_PROCESSING, "Processing file")

        status = service.get_operation_status(operation_id)
        assert status is not None
        assert status.operation_id == operation_id
        assert status.operation_type == OperationType.FILE_PROCESSING

        # Test non-existent operation
        assert service.get_operation_status("non-existent") is None

    def test_get_latest_progress(self, service):
        """Test getting latest progress update"""
        operation_id = service.start_operation(OperationType.ANALYSIS, "Analyzing data")

        service.update_progress(operation_id, LoadingState.IN_PROGRESS, "Step 1")
        service.update_progress(operation_id, LoadingState.IN_PROGRESS, "Step 2")

        latest = service.get_latest_progress(operation_id)
        assert latest is not None
        assert latest.message == "Step 2"
        assert latest.state == LoadingState.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_stream_progress(self, service):
        """Test streaming progress updates"""
        operation_id = service.start_operation(OperationType.GENERATION, "Generating content")

        # Start streaming in background
        updates = []

        async def collect_updates():
            async for update in service.stream_progress(operation_id):
                updates.append(update)
                if len(updates) >= 3:  # Stop after collecting a few updates
                    break

        stream_task = asyncio.create_task(collect_updates())

        # Send some updates
        await asyncio.sleep(0.1)
        service.update_progress(operation_id, LoadingState.IN_PROGRESS, "Step 1")
        await asyncio.sleep(0.1)
        service.update_progress(operation_id, LoadingState.IN_PROGRESS, "Step 2")
        await asyncio.sleep(0.1)
        service.complete_operation(operation_id, success=True)

        # Wait for streaming to complete
        await asyncio.wait_for(stream_task, timeout=2.0)

        assert len(updates) >= 3
        assert updates[0].state == LoadingState.STARTING
        assert updates[1].message == "Step 1"
        assert updates[2].message == "Step 2"

    def test_cancel_operation(self, service):
        """Test cancelling an operation"""
        operation_id = service.start_operation(OperationType.SLACK_API, "Sending message")

        result = service.cancel_operation(operation_id, "User cancelled")
        assert result is True

        operation = service.active_operations[operation_id]
        assert operation.current_state == LoadingState.FAILED

        latest_update = operation.progress_updates[-1]
        assert "cancelled" in latest_update.message.lower()

        # Test cancelling non-existent operation
        assert service.cancel_operation("non-existent") is False

    def test_get_active_operations(self, service):
        """Test getting all active operations"""
        assert len(service.get_active_operations()) == 0

        id1 = service.start_operation(OperationType.LLM_QUERY, "Query 1")
        id2 = service.start_operation(OperationType.GITHUB_API, "GitHub call")

        active = service.get_active_operations()
        assert len(active) == 2
        assert any(op.operation_id == id1 for op in active)
        assert any(op.operation_id == id2 for op in active)

    def test_operation_type_configs(self, service):
        """Test that all operation types have proper configurations"""
        for op_type in OperationType:
            assert op_type in service.operation_configs
            config = service.operation_configs[op_type]
            assert "timeout" in config
            assert "messages" in config
            assert LoadingState.STARTING in config["messages"]
            assert LoadingState.IN_PROGRESS in config["messages"]
            assert LoadingState.COMPLETED in config["messages"]

    def test_default_messages(self, service):
        """Test default message generation"""
        for op_type in OperationType:
            for state in [LoadingState.STARTING, LoadingState.IN_PROGRESS, LoadingState.COMPLETED]:
                message = service._get_state_message(op_type, state)
                assert isinstance(message, str)
                assert len(message) > 0

    @pytest.mark.asyncio
    async def test_track_loading_operation_decorator_success(self):
        """Test the track_loading_operation decorator with successful operation"""

        @track_loading_operation(OperationType.LLM_QUERY, "Test operation")
        async def test_function():
            await asyncio.sleep(0.1)
            return "success"

        result = await test_function()
        assert result == "success"

    @pytest.mark.asyncio
    async def test_track_loading_operation_decorator_failure(self):
        """Test the track_loading_operation decorator with failed operation"""

        @track_loading_operation(OperationType.DATABASE_QUERY, "Test operation")
        async def failing_function():
            await asyncio.sleep(0.1)
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            await failing_function()

    def test_convenience_functions(self):
        """Test convenience functions"""
        # Test start_loading
        operation_id = start_loading(OperationType.ANALYSIS, "Test analysis")
        assert operation_id is not None

        # Test update_loading
        update_loading(operation_id, "Processing step 1", progress_percent=25)

        # Test complete_loading
        complete_loading(operation_id, success=True, message="Analysis complete")

        # Verify the operation was tracked properly
        from services.ui_messages.loading_states import loading_states

        operation = loading_states.get_operation_status(operation_id)
        assert operation is not None
        assert operation.current_state == LoadingState.COMPLETED

    @pytest.mark.asyncio
    async def test_timeout_handling(self, service):
        """Test operation timeout handling"""
        # Create operation with very short timeout
        operation_id = service.start_operation(
            OperationType.LLM_QUERY, "Test timeout", timeout_seconds=1
        )

        # Start streaming and wait for timeout
        updates = []

        async def collect_updates():
            async for update in service.stream_progress(operation_id):
                updates.append(update)

        # This should timeout after 1 second
        await asyncio.wait_for(collect_updates(), timeout=2.0)

        # Check that timeout was detected
        operation = service.get_operation_status(operation_id)
        assert operation.current_state == LoadingState.TIMEOUT

        # Check that timeout message was sent
        timeout_updates = [u for u in updates if u.state == LoadingState.TIMEOUT]
        assert len(timeout_updates) > 0
        assert "timed out" in timeout_updates[0].message.lower()

    def test_update_unknown_operation(self, service):
        """Test updating progress for unknown operation"""
        # Should not raise exception, just log warning
        service.update_progress("unknown-id", LoadingState.IN_PROGRESS, "Test")

        # Should not create the operation
        assert "unknown-id" not in service.active_operations

    def test_complete_unknown_operation(self, service):
        """Test completing unknown operation"""
        # Should not raise exception, just log warning
        service.complete_operation("unknown-id", success=True)

        # Should not create the operation
        assert "unknown-id" not in service.active_operations

    @pytest.mark.asyncio
    async def test_cleanup_operation(self, service):
        """Test that operations are cleaned up after completion"""
        operation_id = service.start_operation(OperationType.GITHUB_API, "Test cleanup")

        # Complete the operation
        service.complete_operation(operation_id, success=True)

        # Operation should still exist immediately
        assert operation_id in service.active_operations

        # Wait for cleanup (with some buffer)
        await asyncio.sleep(2.5)

        # Operation should be cleaned up
        assert operation_id not in service.active_operations

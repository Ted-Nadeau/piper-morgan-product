"""Tests for streaming response utilities"""

import asyncio
import json
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import Request
from fastapi.responses import StreamingResponse

from services.ui_messages.loading_states import (
    LoadingState,
    LoadingStatesService,
    OperationType,
    ProgressUpdate,
)
from web.utils.streaming_responses import (
    ProgressTracker,
    SSEFormatter,
    StreamingResponseBuilder,
    check_client_disconnect,
    create_operation_stream,
    create_progress_stream,
)


class TestSSEFormatter:
    """Test Server-Sent Events formatting"""

    def test_format_event_basic(self):
        """Test basic event formatting"""
        data = {"message": "test", "value": 42}
        result = SSEFormatter.format_event(data, "test_event")

        assert "event: test_event" in result
        assert "data: " in result
        assert result.endswith("\n\n")

        # Parse the JSON data line
        data_line = [line for line in result.split("\n") if line.startswith("data: ")][0]
        json_data = json.loads(data_line[6:])  # Remove "data: " prefix
        assert json_data["message"] == "test"
        assert json_data["value"] == 42

    def test_format_event_with_id_and_retry(self):
        """Test event formatting with ID and retry"""
        data = {"test": True}
        result = SSEFormatter.format_event(data, "test", event_id="123", retry=5000)

        assert "id: 123" in result
        assert "event: test" in result
        assert "retry: 5000" in result
        assert "data: " in result

    def test_format_progress_update(self):
        """Test formatting progress updates"""
        update = ProgressUpdate(
            operation_id="test-op",
            operation_type=OperationType.LLM_QUERY,
            state=LoadingState.IN_PROGRESS,
            message="Processing...",
            progress_percent=50,
            current_step="Step 2",
            total_steps=4,
            current_step_number=2,
            metadata={"extra": "data"},
        )

        result = SSEFormatter.format_progress_update(update)

        assert "event: progress" in result
        assert "data: " in result

        # Parse JSON data
        data_line = [line for line in result.split("\n") if line.startswith("data: ")][0]
        json_data = json.loads(data_line[6:])

        assert json_data["operation_id"] == "test-op"
        assert json_data["operation_type"] == "llm_query"
        assert json_data["state"] == "in_progress"
        assert json_data["message"] == "Processing..."
        assert json_data["progress_percent"] == 50
        assert json_data["current_step"] == "Step 2"
        assert json_data["total_steps"] == 4
        assert json_data["current_step_number"] == 2
        assert json_data["metadata"]["extra"] == "data"

    def test_format_error(self):
        """Test formatting error events"""
        result = SSEFormatter.format_error("Something went wrong", "op-123")

        assert "event: error" in result

        data_line = [line for line in result.split("\n") if line.startswith("data: ")][0]
        json_data = json.loads(data_line[6:])

        assert json_data["error"] == "Something went wrong"
        assert json_data["operation_id"] == "op-123"
        assert "timestamp" in json_data

    def test_format_completion(self):
        """Test formatting completion events"""
        result_data = {"items": 5, "status": "success"}
        result = SSEFormatter.format_completion("op-456", result_data)

        assert "event: complete" in result

        data_line = [line for line in result.split("\n") if line.startswith("data: ")][0]
        json_data = json.loads(data_line[6:])

        assert json_data["operation_id"] == "op-456"
        assert json_data["completed"] is True
        assert json_data["result"]["items"] == 5
        assert json_data["result"]["status"] == "success"


class TestStreamingResponseBuilder:
    """Test streaming response builder"""

    @pytest.fixture
    def mock_loading_service(self):
        """Mock loading service for testing"""
        service = Mock(spec=LoadingStatesService)
        service.start_operation.return_value = "test-op-id"
        service.get_latest_progress.return_value = None
        return service

    @pytest.fixture
    def builder(self, mock_loading_service):
        """StreamingResponseBuilder with mock service"""
        return StreamingResponseBuilder(mock_loading_service)

    @pytest.mark.asyncio
    async def test_stream_operation_progress(self, builder, mock_loading_service):
        """Test streaming operation progress"""
        # Mock progress updates
        updates = [
            ProgressUpdate(
                "test-op", OperationType.LLM_QUERY, LoadingState.STARTING, "Starting..."
            ),
            ProgressUpdate(
                "test-op", OperationType.LLM_QUERY, LoadingState.IN_PROGRESS, "Processing..."
            ),
            ProgressUpdate("test-op", OperationType.LLM_QUERY, LoadingState.COMPLETED, "Done!"),
        ]

        async def mock_stream_progress(operation_id):
            for update in updates:
                yield update

        mock_loading_service.stream_progress = mock_stream_progress

        # Collect streamed events
        events = []
        async for event in builder.stream_operation_progress("test-op"):
            events.append(event)

        assert len(events) >= 4  # connected + 3 updates + completion

        # Check connected event
        assert "event: connected" in events[0]

        # Check progress events
        progress_events = [e for e in events if "event: progress" in e]
        assert len(progress_events) == 3

        # Check completion event
        completion_events = [e for e in events if "event: complete" in e]
        assert len(completion_events) == 1

    def test_create_streaming_response(self, builder):
        """Test creating streaming response"""
        response = builder.create_streaming_response("test-op")

        assert isinstance(response, StreamingResponse)
        assert response.media_type == "text/event-stream"
        assert response.headers["Cache-Control"] == "no-cache"
        assert response.headers["Connection"] == "keep-alive"

    @pytest.mark.asyncio
    async def test_stream_with_operation_success(self, builder, mock_loading_service):
        """Test streaming with successful operation execution"""

        async def mock_operation(value):
            await asyncio.sleep(0.01)  # Simulate work
            return f"result: {value}"

        events = []
        async for event in builder.stream_with_operation(
            OperationType.ANALYSIS, "Test analysis", mock_operation, "test_input"
        ):
            events.append(event)

        # Verify operation was started
        mock_loading_service.start_operation.assert_called_once_with(
            OperationType.ANALYSIS,
            "Test analysis",
            None,  # estimated_duration_seconds
            None,  # timeout_seconds
        )

        # Verify progress was updated
        mock_loading_service.update_progress.assert_called()

        # Verify completion was called
        mock_loading_service.complete_operation.assert_called_with(
            "test-op-id", success=True, result_metadata={"result": "result: test_input"}
        )

        # Check events
        assert len(events) >= 2  # connected + completion
        assert "event: connected" in events[0]
        assert "event: complete" in events[-1]

    @pytest.mark.asyncio
    async def test_stream_with_operation_failure(self, builder, mock_loading_service):
        """Test streaming with failed operation execution"""

        async def failing_operation():
            raise ValueError("Test error")

        events = []
        with pytest.raises(ValueError, match="Test error"):
            async for event in builder.stream_with_operation(
                OperationType.DATABASE_QUERY, "Test query", failing_operation
            ):
                events.append(event)

        # Verify failure was recorded
        mock_loading_service.complete_operation.assert_called_with(
            "test-op-id", success=False, final_message="Operation failed: Test error"
        )

        # Check error event was sent
        error_events = [e for e in events if "event: error" in e]
        assert len(error_events) == 1

    def test_create_operation_streaming_response(self, builder):
        """Test creating operation streaming response"""

        def dummy_operation():
            return "test"

        response = builder.create_operation_streaming_response(
            OperationType.FILE_PROCESSING,
            "Process file",
            dummy_operation,
            estimated_duration_seconds=60,
        )

        assert isinstance(response, StreamingResponse)
        assert response.media_type == "text/event-stream"


class TestProgressTracker:
    """Test progress tracker helper"""

    @pytest.fixture
    def mock_loading_service(self):
        """Mock loading service"""
        return Mock(spec=LoadingStatesService)

    def test_progress_tracker_initialization(self, mock_loading_service):
        """Test progress tracker initialization"""
        tracker = ProgressTracker("op-123", 5, mock_loading_service)

        assert tracker.operation_id == "op-123"
        assert tracker.total_steps == 5
        assert tracker.current_step == 0

    def test_next_step(self, mock_loading_service):
        """Test advancing to next step"""
        tracker = ProgressTracker("op-123", 4, mock_loading_service)

        tracker.next_step("Initialize")

        assert tracker.current_step == 1
        mock_loading_service.update_progress.assert_called_with(
            "op-123",
            LoadingState.IN_PROGRESS,
            "Step 1 of 4: Initialize",
            progress_percent=25,
            current_step="Initialize",
            total_steps=4,
            current_step_number=1,
        )

    def test_next_step_with_custom_message(self, mock_loading_service):
        """Test next step with custom message"""
        tracker = ProgressTracker("op-456", 2, mock_loading_service)

        tracker.next_step("Process", "Custom processing message")

        mock_loading_service.update_progress.assert_called_with(
            "op-456",
            LoadingState.IN_PROGRESS,
            "Custom processing message",
            progress_percent=50,
            current_step="Process",
            total_steps=2,
            current_step_number=1,
        )

    def test_update_current_step(self, mock_loading_service):
        """Test updating current step without advancing"""
        tracker = ProgressTracker("op-789", 3, mock_loading_service)
        tracker.current_step = 2  # Simulate being on step 2

        tracker.update_current_step("Still processing step 2...")

        mock_loading_service.update_progress.assert_called_with(
            "op-789",
            LoadingState.IN_PROGRESS,
            "Still processing step 2...",
            progress_percent=66,  # 2/3 * 100
            total_steps=3,
            current_step_number=2,
        )

    def test_update_current_step_with_custom_progress(self, mock_loading_service):
        """Test updating current step with custom progress"""
        tracker = ProgressTracker("op-999", 10, mock_loading_service)

        tracker.update_current_step("Custom progress", progress_percent=75)

        mock_loading_service.update_progress.assert_called_with(
            "op-999",
            LoadingState.IN_PROGRESS,
            "Custom progress",
            progress_percent=75,
            total_steps=10,
            current_step_number=0,
        )


class TestConvenienceFunctions:
    """Test convenience functions"""

    @patch("web.utils.streaming_responses.streaming_builder")
    def test_create_progress_stream(self, mock_builder):
        """Test create_progress_stream convenience function"""
        mock_response = Mock(spec=StreamingResponse)
        mock_builder.create_streaming_response.return_value = mock_response

        result = create_progress_stream("test-op")

        assert result == mock_response
        mock_builder.create_streaming_response.assert_called_once_with("test-op")

    @patch("web.utils.streaming_responses.streaming_builder")
    def test_create_operation_stream(self, mock_builder):
        """Test create_operation_stream convenience function"""
        mock_response = Mock(spec=StreamingResponse)
        mock_builder.create_operation_streaming_response.return_value = mock_response

        def dummy_func():
            return "test"

        result = create_operation_stream(
            OperationType.GENERATION, "Generate content", dummy_func, "arg1", kwarg1="value1"
        )

        assert result == mock_response
        mock_builder.create_operation_streaming_response.assert_called_once_with(
            OperationType.GENERATION, "Generate content", dummy_func, "arg1", kwarg1="value1"
        )

    @pytest.mark.asyncio
    async def test_check_client_disconnect(self):
        """Test client disconnect checking"""
        # Mock request that is connected
        mock_request = AsyncMock(spec=Request)
        mock_request.is_disconnected.return_value = False

        result = await check_client_disconnect(mock_request)
        assert result is False

        # Mock request that is disconnected
        mock_request.is_disconnected.return_value = True
        result = await check_client_disconnect(mock_request)
        assert result is True

        # Mock request that raises exception
        mock_request.is_disconnected.side_effect = Exception("Connection error")
        result = await check_client_disconnect(mock_request)
        assert result is False  # Should default to connected on error

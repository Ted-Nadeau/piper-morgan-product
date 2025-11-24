"""
Streaming response utilities for long-running operations.

Provides Server-Sent Events (SSE) streaming for progress updates
and real-time feedback to users.

Issue #256 CORE-UX-LOADING-STATES
"""

import json
import logging
from typing import Any, AsyncGenerator, Dict, Optional

from fastapi import Request
from fastapi.responses import StreamingResponse

from services.ui_messages.loading_states import (
    LoadingState,
    LoadingStatesService,
    OperationType,
    ProgressUpdate,
    loading_states,
)

logger = logging.getLogger(__name__)


class SSEFormatter:
    """Formats Server-Sent Events for streaming responses"""

    @staticmethod
    def format_event(
        data: Dict[str, Any],
        event_type: str = "progress",
        event_id: Optional[str] = None,
        retry: Optional[int] = None,
    ) -> str:
        """Format data as Server-Sent Event"""
        lines = []

        if event_id:
            lines.append(f"id: {event_id}")

        if event_type:
            lines.append(f"event: {event_type}")

        if retry:
            lines.append(f"retry: {retry}")

        # Format data as JSON
        json_data = json.dumps(data, default=str)
        lines.append(f"data: {json_data}")

        # SSE format requires double newline at end
        return "\n".join(lines) + "\n\n"

    @staticmethod
    def format_progress_update(update: ProgressUpdate) -> str:
        """Format a progress update as SSE"""
        data = {
            "operation_id": update.operation_id,
            "operation_type": update.operation_type.value,
            "state": update.state.value,
            "message": update.message,
            "progress_percent": update.progress_percent,
            "estimated_remaining_seconds": update.estimated_remaining_seconds,
            "current_step": update.current_step,
            "total_steps": update.total_steps,
            "current_step_number": update.current_step_number,
            "metadata": update.metadata,
            "timestamp": update.timestamp,
        }

        return SSEFormatter.format_event(
            data=data,
            event_type="progress",
            event_id=f"{update.operation_id}_{len(str(update.timestamp))}",
        )

    @staticmethod
    def format_error(error_message: str, operation_id: Optional[str] = None) -> str:
        """Format an error as SSE"""
        data = {
            "error": error_message,
            "operation_id": operation_id,
            "timestamp": __import__("time").time(),
        }

        return SSEFormatter.format_event(data=data, event_type="error")

    @staticmethod
    def format_completion(operation_id: str, result: Optional[Dict[str, Any]] = None) -> str:
        """Format completion event as SSE"""
        data = {
            "operation_id": operation_id,
            "completed": True,
            "result": result,
            "timestamp": __import__("time").time(),
        }

        return SSEFormatter.format_event(data=data, event_type="complete")


class StreamingResponseBuilder:
    """Builder for streaming responses with loading states"""

    def __init__(self, loading_service: LoadingStatesService = None):
        self.loading_service = loading_service or loading_states

    async def stream_operation_progress(
        self, operation_id: str, include_heartbeat: bool = True, heartbeat_interval: int = 30
    ) -> AsyncGenerator[str, None]:
        """Stream progress updates for an operation"""

        try:
            # Send initial connection confirmation
            yield SSEFormatter.format_event(
                data={"connected": True, "operation_id": operation_id}, event_type="connected"
            )

            # Stream progress updates
            last_heartbeat = __import__("time").time()

            async for update in self.loading_service.stream_progress(operation_id):
                yield SSEFormatter.format_progress_update(update)

                # Send heartbeat if needed
                if include_heartbeat:
                    current_time = __import__("time").time()
                    if current_time - last_heartbeat > heartbeat_interval:
                        yield SSEFormatter.format_event(
                            data={"heartbeat": True, "timestamp": current_time},
                            event_type="heartbeat",
                        )
                        last_heartbeat = current_time

                # Break if operation is complete
                if update.state in [
                    LoadingState.COMPLETED,
                    LoadingState.FAILED,
                    LoadingState.TIMEOUT,
                ]:
                    break

            # Send final completion event
            yield SSEFormatter.format_completion(operation_id)

        except Exception as e:
            logger.error(f"Error streaming operation {operation_id}: {e}")
            yield SSEFormatter.format_error(f"Streaming error: {str(e)}", operation_id)

    def create_streaming_response(
        self, operation_id: str, include_heartbeat: bool = True, heartbeat_interval: int = 30
    ) -> StreamingResponse:
        """Create a FastAPI StreamingResponse for operation progress"""

        headers = {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control",
        }

        return StreamingResponse(
            self.stream_operation_progress(operation_id, include_heartbeat, heartbeat_interval),
            media_type="text/event-stream",
            headers=headers,
        )

    async def stream_with_operation(
        self,
        operation_type: OperationType,
        description: str,
        operation_func,
        *args,
        estimated_duration_seconds: Optional[int] = None,
        timeout_seconds: Optional[int] = None,
        include_result: bool = True,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """
        Stream progress while executing an operation.

        This combines operation execution with progress streaming.
        """

        # Start the operation
        operation_id = self.loading_service.start_operation(
            operation_type, description, estimated_duration_seconds, timeout_seconds
        )

        try:
            # Send initial connection
            yield SSEFormatter.format_event(
                data={"connected": True, "operation_id": operation_id}, event_type="connected"
            )

            # Update to in-progress
            self.loading_service.update_progress(operation_id, LoadingState.IN_PROGRESS)

            # Execute the operation
            if __import__("asyncio").iscoroutinefunction(operation_func):
                result = await operation_func(*args, **kwargs)
            else:
                result = operation_func(*args, **kwargs)

            # Complete successfully
            result_metadata = {"result": result} if include_result else None
            self.loading_service.complete_operation(
                operation_id, success=True, result_metadata=result_metadata
            )

            # Stream final updates
            final_update = self.loading_service.get_latest_progress(operation_id)
            if final_update:
                yield SSEFormatter.format_progress_update(final_update)

            # Send completion with result
            completion_data = {"result": result} if include_result else None
            yield SSEFormatter.format_completion(operation_id, completion_data)

        except Exception as e:
            logger.error(f"Operation {operation_id} failed: {e}")

            # Mark as failed
            self.loading_service.complete_operation(
                operation_id, success=False, final_message=f"Operation failed: {str(e)}"
            )

            # Send error
            yield SSEFormatter.format_error(str(e), operation_id)

            # Re-raise the exception
            raise

    def create_operation_streaming_response(
        self,
        operation_type: OperationType,
        description: str,
        operation_func,
        *args,
        estimated_duration_seconds: Optional[int] = None,
        timeout_seconds: Optional[int] = None,
        include_result: bool = True,
        **kwargs,
    ) -> StreamingResponse:
        """Create a streaming response that executes and streams an operation"""

        headers = {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control",
        }

        return StreamingResponse(
            self.stream_with_operation(
                operation_type,
                description,
                operation_func,
                *args,
                estimated_duration_seconds=estimated_duration_seconds,
                timeout_seconds=timeout_seconds,
                include_result=include_result,
                **kwargs,
            ),
            media_type="text/event-stream",
            headers=headers,
        )


# Global instance for easy access
streaming_builder = StreamingResponseBuilder()


def create_progress_stream(operation_id: str) -> StreamingResponse:
    """Convenience function to create progress stream for existing operation"""
    return streaming_builder.create_streaming_response(operation_id)


def create_operation_stream(
    operation_type: OperationType, description: str, operation_func, *args, **kwargs
) -> StreamingResponse:
    """Convenience function to create streaming response for new operation"""
    return streaming_builder.create_operation_streaming_response(
        operation_type, description, operation_func, *args, **kwargs
    )


async def check_client_disconnect(request: Request) -> bool:
    """Check if client has disconnected from SSE stream"""
    try:
        # This is a simple check - in production you might want more sophisticated detection
        return await request.is_disconnected()
    except Exception:
        # If we can't check, assume still connected
        return False


class ProgressTracker:
    """Helper class for tracking progress in long operations"""

    def __init__(
        self, operation_id: str, total_steps: int, loading_service: LoadingStatesService = None
    ):
        self.operation_id = operation_id
        self.total_steps = total_steps
        self.current_step = 0
        self.loading_service = loading_service or loading_states

    def next_step(self, step_name: str, message: Optional[str] = None):
        """Advance to next step and update progress"""
        self.current_step += 1
        progress_percent = int((self.current_step / self.total_steps) * 100)

        if message is None:
            message = f"Step {self.current_step} of {self.total_steps}: {step_name}"

        self.loading_service.update_progress(
            self.operation_id,
            LoadingState.IN_PROGRESS,
            message,
            progress_percent=progress_percent,
            current_step=step_name,
            total_steps=self.total_steps,
            current_step_number=self.current_step,
        )

    def update_current_step(self, message: str, progress_percent: Optional[int] = None):
        """Update current step without advancing"""
        if progress_percent is None and self.total_steps > 0:
            progress_percent = int((self.current_step / self.total_steps) * 100)

        self.loading_service.update_progress(
            self.operation_id,
            LoadingState.IN_PROGRESS,
            message,
            progress_percent=progress_percent,
            total_steps=self.total_steps,
            current_step_number=self.current_step,
        )

"""
Loading states service for long-running operations.

Provides progress indicators, streaming responses, and timeout handling
for operations that take more than 2 seconds.

Issue #256 CORE-UX-LOADING-STATES
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)


class OperationType(str, Enum):
    """Types of operations that can have loading states"""

    WORKFLOW_EXECUTION = "workflow_execution"
    LLM_QUERY = "llm_query"
    GITHUB_API = "github_api"
    SLACK_API = "slack_api"
    DATABASE_QUERY = "database_query"
    FILE_PROCESSING = "file_processing"
    KNOWLEDGE_SEARCH = "knowledge_search"
    INTENT_PROCESSING = "intent_processing"
    ANALYSIS = "analysis"
    GENERATION = "generation"


class LoadingState(str, Enum):
    """States of a loading operation"""

    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    COMPLETING = "completing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ProgressUpdate:
    """Progress update for a loading operation"""

    operation_id: str
    operation_type: OperationType
    state: LoadingState
    message: str
    progress_percent: Optional[int] = None
    estimated_remaining_seconds: Optional[int] = None
    current_step: Optional[str] = None
    total_steps: Optional[int] = None
    current_step_number: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class LoadingOperation:
    """Represents a long-running operation with loading state"""

    operation_id: str
    operation_type: OperationType
    description: str
    start_time: float
    timeout_seconds: int = 300  # 5 minutes default
    progress_updates: List[ProgressUpdate] = field(default_factory=list)
    current_state: LoadingState = LoadingState.STARTING
    estimated_duration_seconds: Optional[int] = None


class LoadingStatesService:
    """Service to manage loading states for long-running operations"""

    def __init__(self):
        self.active_operations: Dict[str, LoadingOperation] = {}

        # Operation-specific messages and timeouts
        self.operation_configs = {
            OperationType.WORKFLOW_EXECUTION: {
                "timeout": 300,  # 5 minutes
                "messages": {
                    LoadingState.STARTING: "Starting workflow execution...",
                    LoadingState.IN_PROGRESS: "Executing workflow steps...",
                    LoadingState.COMPLETING: "Finalizing workflow results...",
                    LoadingState.COMPLETED: "Workflow completed successfully!",
                },
            },
            OperationType.LLM_QUERY: {
                "timeout": 120,  # 2 minutes
                "messages": {
                    LoadingState.STARTING: "Preparing your request...",
                    LoadingState.IN_PROGRESS: "Thinking about your question...",
                    LoadingState.COMPLETING: "Finalizing response...",
                    LoadingState.COMPLETED: "Response ready!",
                },
            },
            OperationType.GITHUB_API: {
                "timeout": 60,  # 1 minute
                "messages": {
                    LoadingState.STARTING: "Connecting to GitHub...",
                    LoadingState.IN_PROGRESS: "Fetching data from GitHub...",
                    LoadingState.COMPLETING: "Processing GitHub data...",
                    LoadingState.COMPLETED: "GitHub data retrieved!",
                },
            },
            OperationType.SLACK_API: {
                "timeout": 30,  # 30 seconds
                "messages": {
                    LoadingState.STARTING: "Connecting to Slack...",
                    LoadingState.IN_PROGRESS: "Sending message to Slack...",
                    LoadingState.COMPLETING: "Confirming delivery...",
                    LoadingState.COMPLETED: "Message sent successfully!",
                },
            },
            OperationType.DATABASE_QUERY: {
                "timeout": 30,  # 30 seconds
                "messages": {
                    LoadingState.STARTING: "Preparing database query...",
                    LoadingState.IN_PROGRESS: "Searching database...",
                    LoadingState.COMPLETING: "Processing results...",
                    LoadingState.COMPLETED: "Data retrieved!",
                },
            },
            OperationType.FILE_PROCESSING: {
                "timeout": 180,  # 3 minutes
                "messages": {
                    LoadingState.STARTING: "Opening file...",
                    LoadingState.IN_PROGRESS: "Processing file content...",
                    LoadingState.COMPLETING: "Finalizing analysis...",
                    LoadingState.COMPLETED: "File processed successfully!",
                },
            },
            OperationType.KNOWLEDGE_SEARCH: {
                "timeout": 60,  # 1 minute
                "messages": {
                    LoadingState.STARTING: "Preparing search...",
                    LoadingState.IN_PROGRESS: "Searching knowledge base...",
                    LoadingState.COMPLETING: "Ranking results...",
                    LoadingState.COMPLETED: "Search completed!",
                },
            },
            OperationType.INTENT_PROCESSING: {
                "timeout": 30,  # 30 seconds
                "messages": {
                    LoadingState.STARTING: "Understanding your request...",
                    LoadingState.IN_PROGRESS: "Processing intent...",
                    LoadingState.COMPLETING: "Preparing response...",
                    LoadingState.COMPLETED: "Request processed!",
                },
            },
            OperationType.ANALYSIS: {
                "timeout": 180,  # 3 minutes
                "messages": {
                    LoadingState.STARTING: "Starting analysis...",
                    LoadingState.IN_PROGRESS: "Analyzing data...",
                    LoadingState.COMPLETING: "Generating insights...",
                    LoadingState.COMPLETED: "Analysis complete!",
                },
            },
            OperationType.GENERATION: {
                "timeout": 240,  # 4 minutes
                "messages": {
                    LoadingState.STARTING: "Preparing generation...",
                    LoadingState.IN_PROGRESS: "Generating content...",
                    LoadingState.COMPLETING: "Reviewing output...",
                    LoadingState.COMPLETED: "Content generated!",
                },
            },
        }

    def start_operation(
        self,
        operation_type: OperationType,
        description: str,
        estimated_duration_seconds: Optional[int] = None,
        timeout_seconds: Optional[int] = None,
    ) -> str:
        """Start tracking a long-running operation"""

        operation_id = str(uuid4())

        # Get default timeout if not provided
        if timeout_seconds is None:
            timeout_seconds = self.operation_configs[operation_type]["timeout"]

        operation = LoadingOperation(
            operation_id=operation_id,
            operation_type=operation_type,
            description=description,
            start_time=time.time(),
            timeout_seconds=timeout_seconds,
            estimated_duration_seconds=estimated_duration_seconds,
        )

        self.active_operations[operation_id] = operation

        # Send initial progress update
        self.update_progress(
            operation_id,
            LoadingState.STARTING,
            self._get_state_message(operation_type, LoadingState.STARTING),
        )

        logger.info(f"Started loading operation: {operation_id} ({operation_type})")
        return operation_id

    def update_progress(
        self,
        operation_id: str,
        state: LoadingState,
        message: Optional[str] = None,
        progress_percent: Optional[int] = None,
        estimated_remaining_seconds: Optional[int] = None,
        current_step: Optional[str] = None,
        total_steps: Optional[int] = None,
        current_step_number: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update progress for an operation"""

        if operation_id not in self.active_operations:
            logger.warning(f"Attempted to update unknown operation: {operation_id}")
            return

        operation = self.active_operations[operation_id]

        # Use default message if none provided
        if message is None:
            message = self._get_state_message(operation.operation_type, state)

        # Create progress update
        update = ProgressUpdate(
            operation_id=operation_id,
            operation_type=operation.operation_type,
            state=state,
            message=message,
            progress_percent=progress_percent,
            estimated_remaining_seconds=estimated_remaining_seconds,
            current_step=current_step,
            total_steps=total_steps,
            current_step_number=current_step_number,
            metadata=metadata or {},
        )

        operation.progress_updates.append(update)
        operation.current_state = state

        logger.debug(f"Progress update for {operation_id}: {state} - {message}")

    def complete_operation(
        self,
        operation_id: str,
        success: bool = True,
        final_message: Optional[str] = None,
        result_metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Mark an operation as completed"""

        if operation_id not in self.active_operations:
            logger.warning(f"Attempted to complete unknown operation: {operation_id}")
            return

        operation = self.active_operations[operation_id]

        # Determine final state and message
        if success:
            final_state = LoadingState.COMPLETED
            if final_message is None:
                final_message = self._get_state_message(
                    operation.operation_type, LoadingState.COMPLETED
                )
        else:
            final_state = LoadingState.FAILED
            if final_message is None:
                final_message = f"Operation failed: {operation.description}"

        # Send final progress update
        self.update_progress(
            operation_id,
            final_state,
            final_message,
            progress_percent=100 if success else None,
            metadata=result_metadata,
        )

        # Calculate execution time
        execution_time = time.time() - operation.start_time
        logger.info(f"Completed operation {operation_id} in {execution_time:.2f}s: {final_state}")

        # Remove from active operations after a brief delay to allow final update delivery
        try:
            asyncio.create_task(self._cleanup_operation(operation_id, delay=2.0))
        except RuntimeError:
            # No event loop running, schedule cleanup differently
            import threading

            timer = threading.Timer(2.0, lambda: self._cleanup_operation_sync(operation_id))
            timer.start()

    def get_operation_status(self, operation_id: str) -> Optional[LoadingOperation]:
        """Get current status of an operation"""
        return self.active_operations.get(operation_id)

    def get_latest_progress(self, operation_id: str) -> Optional[ProgressUpdate]:
        """Get the latest progress update for an operation"""
        operation = self.active_operations.get(operation_id)
        if operation and operation.progress_updates:
            return operation.progress_updates[-1]
        return None

    async def stream_progress(self, operation_id: str) -> AsyncGenerator[ProgressUpdate, None]:
        """Stream progress updates for an operation"""

        if operation_id not in self.active_operations:
            logger.warning(f"Attempted to stream unknown operation: {operation_id}")
            return

        operation = self.active_operations[operation_id]
        last_update_index = 0

        while operation.current_state not in [
            LoadingState.COMPLETED,
            LoadingState.FAILED,
            LoadingState.TIMEOUT,
        ]:
            # Yield any new progress updates
            while last_update_index < len(operation.progress_updates):
                yield operation.progress_updates[last_update_index]
                last_update_index += 1

            # Check for timeout
            if time.time() - operation.start_time > operation.timeout_seconds:
                self.update_progress(
                    operation_id,
                    LoadingState.TIMEOUT,
                    f"Operation timed out after {operation.timeout_seconds} seconds",
                )
                break

            # Wait before checking again
            await asyncio.sleep(0.5)

        # Yield any final updates
        while last_update_index < len(operation.progress_updates):
            yield operation.progress_updates[last_update_index]
            last_update_index += 1

    def _get_state_message(self, operation_type: OperationType, state: LoadingState) -> str:
        """Get default message for operation type and state"""
        config = self.operation_configs.get(operation_type, {})
        messages = config.get("messages", {})
        return messages.get(state, f"Operation {state.value}...")

    async def _cleanup_operation(self, operation_id: str, delay: float = 2.0) -> None:
        """Remove completed operation after delay"""
        await asyncio.sleep(delay)
        if operation_id in self.active_operations:
            del self.active_operations[operation_id]
            logger.debug(f"Cleaned up operation: {operation_id}")

    def _cleanup_operation_sync(self, operation_id: str) -> None:
        """Remove completed operation (synchronous version)"""
        if operation_id in self.active_operations:
            del self.active_operations[operation_id]
            logger.debug(f"Cleaned up operation: {operation_id}")

    def get_active_operations(self) -> List[LoadingOperation]:
        """Get all currently active operations"""
        return list(self.active_operations.values())

    def cancel_operation(self, operation_id: str, reason: str = "Cancelled by user") -> bool:
        """Cancel an active operation"""
        if operation_id not in self.active_operations:
            return False

        self.update_progress(operation_id, LoadingState.FAILED, f"Operation cancelled: {reason}")

        # Schedule cleanup
        try:
            asyncio.create_task(self._cleanup_operation(operation_id, delay=1.0))
        except RuntimeError:
            # No event loop running, schedule cleanup differently
            import threading

            timer = threading.Timer(1.0, lambda: self._cleanup_operation_sync(operation_id))
            timer.start()
        return True


# Global instance for easy access
loading_states = LoadingStatesService()


def track_loading_operation(
    operation_type: OperationType,
    description: str,
    estimated_duration_seconds: Optional[int] = None,
    timeout_seconds: Optional[int] = None,
):
    """
    Decorator to automatically track loading state for async functions.

    Usage:
        @track_loading_operation(OperationType.LLM_QUERY, "Processing your question")
        async def process_llm_query(query: str):
            # Long-running operation
            return result
    """

    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            operation_id = loading_states.start_operation(
                operation_type, description, estimated_duration_seconds, timeout_seconds
            )

            try:
                # Update to in-progress
                loading_states.update_progress(operation_id, LoadingState.IN_PROGRESS)

                # Execute the function
                result = await func(*args, **kwargs)

                # Mark as completed
                loading_states.complete_operation(operation_id, success=True)
                return result

            except Exception as e:
                # Mark as failed
                loading_states.complete_operation(
                    operation_id, success=False, final_message=f"Operation failed: {str(e)}"
                )
                raise

        return wrapper

    return decorator


# Convenience functions
def start_loading(operation_type: OperationType, description: str) -> str:
    """Convenience function to start a loading operation"""
    return loading_states.start_operation(operation_type, description)


def update_loading(operation_id: str, message: str, progress_percent: Optional[int] = None) -> None:
    """Convenience function to update loading progress"""
    loading_states.update_progress(
        operation_id, LoadingState.IN_PROGRESS, message, progress_percent=progress_percent
    )


def complete_loading(
    operation_id: str, success: bool = True, message: Optional[str] = None
) -> None:
    """Convenience function to complete a loading operation"""
    loading_states.complete_operation(operation_id, success, message)

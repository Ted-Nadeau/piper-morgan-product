"""
Robust Background Task Manager

Context-preserving task management that prevents garbage collection and provides
comprehensive tracking for background tasks. Eliminates silent failures through
proper task lifecycle management and error reporting.

This module ensures background tasks cannot be silently garbage collected and
provides full observability into task execution status.
"""

import asyncio
import contextvars
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class TaskMetrics:
    """Metrics for tracking individual task execution"""

    task_id: str
    name: Optional[str]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[float] = None
    success: Optional[bool] = None
    error: Optional[str] = None
    context_data: Dict[str, Any] = field(default_factory=dict)

    def mark_started(self):
        """Mark task as started"""
        self.started_at = datetime.utcnow()

    def mark_completed(self, success: bool = True, error: Optional[str] = None):
        """Mark task as completed with success/failure status"""
        self.completed_at = datetime.utcnow()
        self.success = success
        self.error = error

        if self.started_at:
            self.duration_ms = (self.completed_at - self.started_at).total_seconds() * 1000
        else:
            # Task completed without being marked as started
            self.duration_ms = (self.completed_at - self.created_at).total_seconds() * 1000


class RobustTaskManager:
    """
    Manages background tasks with context preservation and comprehensive tracking.

    Prevents garbage collection through strong references and provides full
    observability into task execution lifecycle. Critical for eliminating
    silent failures in background processing.
    """

    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.task_results: Dict[str, Any] = {}
        self.task_errors: Dict[str, Exception] = {}
        self._cleanup_interval = 300  # 5 minutes

        # Context preservation properties
        self.context: Dict[str, Any] = {}
        self.correlation_id: Optional[str] = None

        logger.info("RobustTaskManager initialized")

    def add_task(self, task_name: str, task_data: Dict[str, Any]) -> str:
        """
        Add a task to the manager for tracking.

        Args:
            task_name: Name of the task
            task_data: Data associated with the task

        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        metrics = TaskMetrics(
            task_id=task_id, name=task_name, created_at=datetime.utcnow(), context_data=task_data
        )
        self.task_metrics[task_id] = metrics
        logger.debug(f"Added task {task_name} with ID {task_id}")
        return task_id

    def start_task(self, task_name: str) -> bool:
        """
        Mark a task as started.

        Args:
            task_name: Name of the task to start

        Returns:
            True if task was found and started, False otherwise
        """
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.started_at is None:
                metrics.mark_started()
                logger.debug(f"Started task {task_name} with ID {task_id}")
                return True
        logger.warning(f"Task {task_name} not found or already started")
        return False

    def complete_task(self, task_name: str, result: Dict[str, Any]) -> bool:
        """
        Mark a task as completed with result.

        Args:
            task_name: Name of the task to complete
            result: Result data for the task

        Returns:
            True if task was found and completed, False otherwise
        """
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.completed_at is None:
                metrics.mark_completed(success=True)
                self.task_results[task_id] = result
                logger.debug(f"Completed task {task_name} with ID {task_id}")
                return True
        logger.warning(f"Task {task_name} not found or already completed")
        return False

    def create_tracked_task(
        self,
        coro: Awaitable[Any],
        name: Optional[str] = None,
        preserve_context: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> asyncio.Task:
        """
        Create a task that's tracked and cannot be garbage collected.

        Args:
            coro: The coroutine to execute
            name: Optional name for the task
            preserve_context: Whether to preserve the current context
            metadata: Optional metadata to track with the task

        Returns:
            The created asyncio.Task with tracking enabled
        """
        task_id = str(uuid.uuid4())
        task_name = name or f"tracked_task_{task_id[:8]}"

        # Create task metrics
        metrics = TaskMetrics(
            task_id=task_id,
            name=task_name,
            created_at=datetime.utcnow(),
            context_data=metadata or {},
        )
        self.task_metrics[task_id] = metrics

        if preserve_context:
            # Capture current context
            context = contextvars.copy_context()

            # Wrap coroutine to run in captured context
            async def context_wrapped():
                metrics.mark_started()
                logger.info(f"TASK [{task_id}] {task_name} started with preserved context")

                try:
                    result = await coro
                    metrics.mark_completed(success=True)
                    self.task_results[task_id] = result

                    logger.info(
                        f"TASK [{task_id}] {task_name} completed successfully in {metrics.duration_ms:.2f}ms"
                    )
                    return result

                except Exception as e:
                    metrics.mark_completed(success=False, error=str(e))
                    self.task_errors[task_id] = e

                    logger.error(
                        f"TASK [{task_id}] {task_name} failed after {metrics.duration_ms:.2f}ms: {e}",
                        exc_info=True,
                    )
                    raise

            # Run the wrapped coroutine in the captured context
            def run_in_context():
                return asyncio.create_task(context_wrapped(), name=task_name)

            task = context.run(run_in_context)
        else:
            # Create task without context preservation
            async def direct_wrapped():
                metrics.mark_started()
                logger.info(f"TASK [{task_id}] {task_name} started without context preservation")

                try:
                    result = await coro
                    metrics.mark_completed(success=True)
                    self.task_results[task_id] = result

                    logger.info(
                        f"TASK [{task_id}] {task_name} completed successfully in {metrics.duration_ms:.2f}ms"
                    )
                    return result

                except Exception as e:
                    metrics.mark_completed(success=False, error=str(e))
                    self.task_errors[task_id] = e

                    logger.error(
                        f"TASK [{task_id}] {task_name} failed after {metrics.duration_ms:.2f}ms: {e}",
                        exc_info=True,
                    )
                    raise

            task = asyncio.create_task(direct_wrapped(), name=task_name)

        # Track the task to prevent garbage collection
        self.active_tasks.add(task)

        # Set up completion callback for cleanup
        def handle_completion(finished_task: asyncio.Task):
            self.active_tasks.discard(finished_task)

            # Additional logging for task completion
            if finished_task.cancelled():
                logger.warning(f"TASK [{task_id}] {task_name} was cancelled")
                metrics.mark_completed(success=False, error="Task cancelled")
            elif finished_task.exception():
                # Exception already logged in wrapper
                pass
            else:
                # Success already logged in wrapper
                pass

        task.add_done_callback(handle_completion)

        logger.info(
            f"TASK [{task_id}] {task_name} created and tracked (active tasks: {len(self.active_tasks)})"
        )

        return task

    async def wait_for_task(self, task_id: str, timeout: float = 5.0) -> Any:
        """
        Wait for a specific task to complete with timeout.

        Args:
            task_id: The task ID to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            The task result

        Raises:
            TimeoutError: If task doesn't complete within timeout
            Exception: The original task exception if task failed
        """
        start_time = time.time()

        while task_id not in self.task_results and task_id not in self.task_errors:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")
            await asyncio.sleep(0.1)

        if task_id in self.task_errors:
            raise self.task_errors[task_id]

        return self.task_results.get(task_id)

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive status for a specific task"""
        metrics = self.task_metrics.get(task_id)
        if not metrics:
            return None

        return {
            "task_id": task_id,
            "name": metrics.name,
            "created_at": metrics.created_at.isoformat(),
            "started_at": metrics.started_at.isoformat() if metrics.started_at else None,
            "completed_at": metrics.completed_at.isoformat() if metrics.completed_at else None,
            "duration_ms": metrics.duration_ms,
            "success": metrics.success,
            "error": metrics.error,
            "context_data": metrics.context_data,
            "is_active": any(task.get_name() == metrics.name for task in self.active_tasks),
        }

    def get_active_tasks_summary(self) -> Dict[str, Any]:
        """Get summary of all active tasks"""
        active_count = len(self.active_tasks)
        completed_count = len([m for m in self.task_metrics.values() if m.completed_at])
        successful_count = len([m for m in self.task_metrics.values() if m.success is True])
        failed_count = len([m for m in self.task_metrics.values() if m.success is False])

        return {
            "active_tasks": active_count,
            "total_tasks_created": len(self.task_metrics),
            "completed_tasks": completed_count,
            "successful_tasks": successful_count,
            "failed_tasks": failed_count,
            "success_rate": successful_count / completed_count if completed_count > 0 else 0,
            "task_names": [task.get_name() for task in self.active_tasks],
        }

    def cleanup_completed_tasks(self, max_age_minutes: int = 60):
        """Clean up old task metrics and results to prevent memory leaks"""
        cutoff_time = datetime.utcnow().timestamp() - (max_age_minutes * 60)

        tasks_to_remove = []
        for task_id, metrics in self.task_metrics.items():
            if metrics.completed_at and metrics.completed_at.timestamp() < cutoff_time:
                tasks_to_remove.append(task_id)

        for task_id in tasks_to_remove:
            self.task_metrics.pop(task_id, None)
            self.task_results.pop(task_id, None)
            self.task_errors.pop(task_id, None)

        if tasks_to_remove:
            logger.info(f"Cleaned up {len(tasks_to_remove)} old task metrics")

    def create_context_preserving_task(self, func: Callable, *args, **kwargs) -> asyncio.Task:
        """
        Create a task with automatic context preservation.

        This is a convenience method for creating tasks that preserve the current
        context automatically. Useful as a decorator or direct call.
        """

        async def wrapper():
            return await func(*args, **kwargs)

        return self.create_tracked_task(
            wrapper(),
            name=f"{func.__name__}",
            preserve_context=True,
            metadata={
                "function": func.__name__,
                "args_count": len(args),
                "kwargs_count": len(kwargs),
            },
        )


def preserve_context_decorator(task_manager: RobustTaskManager):
    """
    Decorator to automatically preserve context for async functions.

    Usage:
        @preserve_context_decorator(task_manager)
        async def my_background_task():
            # This function will preserve the calling context
            pass
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a tracked task that preserves context
            task = task_manager.create_tracked_task(
                func(*args, **kwargs), name=func.__name__, preserve_context=True
            )
            return await task

        return wrapper

    return decorator


# Global task manager instance
task_manager = RobustTaskManager()

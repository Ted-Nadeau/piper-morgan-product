"""
Demo endpoint for loading states and streaming responses.

This demonstrates how to integrate loading states with FastAPI endpoints
for long-running operations.

Issue #256 CORE-UX-LOADING-STATES
"""

import asyncio
import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from services.ui_messages.loading_states import (
    OperationType,
    complete_loading,
    start_loading,
    track_loading_operation,
    update_loading,
)
from web.utils.streaming_responses import (
    ProgressTracker,
    create_operation_stream,
    create_progress_stream,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/loading", tags=["loading"])


@router.get("/demo/simple")
async def simple_loading_demo():
    """Simple loading operation without streaming"""

    @track_loading_operation(
        OperationType.ANALYSIS, "Analyzing demo data", estimated_duration_seconds=5
    )
    async def analyze_data():
        # Simulate long-running analysis
        await asyncio.sleep(2)
        return {"result": "Analysis complete", "items_processed": 42}

    try:
        result = await analyze_data()
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Demo analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")


@router.get("/demo/manual")
async def manual_loading_demo():
    """Manual loading state management"""

    # Start loading operation
    operation_id = start_loading(OperationType.FILE_PROCESSING, "Processing demo file")

    try:
        # Simulate multi-step process
        update_loading(operation_id, "Reading file...", progress_percent=20)
        await asyncio.sleep(0.5)

        update_loading(operation_id, "Parsing content...", progress_percent=40)
        await asyncio.sleep(0.5)

        update_loading(operation_id, "Analyzing structure...", progress_percent=60)
        await asyncio.sleep(0.5)

        update_loading(operation_id, "Generating report...", progress_percent=80)
        await asyncio.sleep(0.5)

        # Complete successfully
        complete_loading(operation_id, success=True, message="File processed successfully!")

        return {"success": True, "operation_id": operation_id, "result": "File processing complete"}

    except Exception as e:
        complete_loading(operation_id, success=False, message=f"Processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="File processing failed")


@router.get("/demo/stream/{operation_id}")
async def stream_existing_operation(operation_id: str):
    """Stream progress for an existing operation"""
    return create_progress_stream(operation_id)


@router.get("/demo/stream-new")
async def stream_new_operation():
    """Stream a new operation from start to finish"""

    async def long_running_task():
        """Simulate a long-running task with multiple steps"""
        # Step 1
        await asyncio.sleep(0.5)

        # Step 2
        await asyncio.sleep(0.5)

        # Step 3
        await asyncio.sleep(0.5)

        return {"processed_items": 100, "status": "complete"}

    return create_operation_stream(
        OperationType.WORKFLOW_EXECUTION,
        "Executing demo workflow",
        long_running_task,
        estimated_duration_seconds=3,
    )


@router.get("/demo/progress-tracker")
async def progress_tracker_demo():
    """Demo using ProgressTracker for step-by-step operations"""

    operation_id = start_loading(OperationType.GENERATION, "Generating demo content")

    try:
        # Create progress tracker for 4 steps
        tracker = ProgressTracker(operation_id, total_steps=4)

        # Step 1
        tracker.next_step("Initialize", "Setting up generation environment...")
        await asyncio.sleep(0.3)

        # Step 2
        tracker.next_step("Analyze", "Analyzing input requirements...")
        await asyncio.sleep(0.4)

        # Update current step with more detail
        tracker.update_current_step("Deep analysis in progress...")
        await asyncio.sleep(0.3)

        # Step 3
        tracker.next_step("Generate", "Creating content...")
        await asyncio.sleep(0.5)

        # Step 4
        tracker.next_step("Finalize", "Reviewing and formatting output...")
        await asyncio.sleep(0.3)

        # Complete
        complete_loading(operation_id, success=True)

        return {
            "success": True,
            "operation_id": operation_id,
            "result": "Content generation complete",
            "steps_completed": 4,
        }

    except Exception as e:
        complete_loading(operation_id, success=False, message=f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Content generation failed")


@router.get("/demo/timeout")
async def timeout_demo():
    """Demo operation that will timeout"""

    operation_id = start_loading(OperationType.DATABASE_QUERY, "Long database query (will timeout)")

    try:
        # This will take longer than the default timeout
        update_loading(operation_id, "Executing very slow query...")
        await asyncio.sleep(10)  # Longer than typical timeout

        complete_loading(operation_id, success=True)
        return {"success": True, "operation_id": operation_id}

    except Exception as e:
        complete_loading(operation_id, success=False, message=str(e))
        raise HTTPException(status_code=500, detail="Query failed")


@router.get("/demo/error")
async def error_demo():
    """Demo operation that fails with error"""

    operation_id = start_loading(OperationType.SLACK_API, "Sending message (will fail)")

    try:
        update_loading(operation_id, "Connecting to Slack...", progress_percent=25)
        await asyncio.sleep(0.5)

        update_loading(operation_id, "Authenticating...", progress_percent=50)
        await asyncio.sleep(0.5)

        # Simulate an error
        raise ValueError("Invalid Slack token")

    except Exception as e:
        complete_loading(operation_id, success=False, message=f"Slack error: {str(e)}")
        raise HTTPException(status_code=500, detail="Slack operation failed")


@router.get("/status")
async def loading_status():
    """Get status of all active loading operations"""
    from services.ui_messages.loading_states import loading_states

    active_ops = loading_states.get_active_operations()

    return {
        "active_operations": len(active_ops),
        "operations": [
            {
                "operation_id": op.operation_id,
                "operation_type": op.operation_type.value,
                "description": op.description,
                "current_state": op.current_state.value,
                "start_time": op.start_time,
                "progress_updates": len(op.progress_updates),
            }
            for op in active_ops
        ],
    }

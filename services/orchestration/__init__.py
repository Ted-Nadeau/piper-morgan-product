"""
Orchestration Service
Handles multi-step workflow execution for PM tasks
"""
# 2025-06-03: Updated imports to use shared_types for enums.
from services.shared_types import ( #
    WorkflowType, WorkflowStatus,
    TaskType, TaskStatus
)

# Import the engine instance
from .engine import engine, OrchestrationEngine

# Don't import engine at module level
# Let consumers import what they need

from .workflows import Workflow, WorkflowDefinition, WORKFLOW_DEFINITIONS #
from .tasks import Task, TaskResult #

__all__ = [
    # Engine
    "engine",
    "OrchestrationEngine",
    
    # Workflows
    "Workflow",
    "WorkflowDefinition",
    "WORKFLOW_DEFINITIONS",
    
    # Tasks
    "Task",
    "TaskResult",
    
    # Shared Enums
    "WorkflowType",
    "WorkflowStatus",
    "TaskType",
    "TaskStatus"
]

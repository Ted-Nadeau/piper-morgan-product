"""
Workflow Integration for Multi-Agent Coordinator
Purpose: Connect task decomposition to workflow creation
"""

import asyncio
import time
from typing import Any, Dict, List
from uuid import uuid4

from services.domain.models import Intent, Task, Workflow
from services.orchestration.multi_agent_coordinator import CoordinationResult, MultiAgentCoordinator
from services.shared_types import TaskStatus, TaskType, WorkflowStatus, WorkflowType


class WorkflowIntegration:
    """Integrates Multi-Agent Coordinator with workflow engine"""

    def __init__(self):
        self.coordinator = MultiAgentCoordinator()

    async def create_multi_agent_workflow(
        self, intent: Intent, context: Dict[str, Any]
    ) -> Workflow:
        """Create workflow using Multi-Agent coordination"""

        start_time = time.time()

        try:
            # Use coordinator for task decomposition
            coordination_result = await self.coordinator.coordinate_task(intent, context)

            # Convert subtasks to workflow tasks
            workflow = self._create_workflow_from_coordination(intent, coordination_result)

            duration_ms = int((time.time() - start_time) * 1000)
            print(f"✅ Multi-agent workflow created in {duration_ms}ms")

            return workflow

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            print(f"❌ Multi-agent workflow creation failed after {duration_ms}ms: {e}")
            raise

    def _create_workflow_from_coordination(
        self, intent: Intent, coordination_result: CoordinationResult
    ) -> Workflow:
        """Convert coordination result to executable workflow"""

        workflow = Workflow(
            type=WorkflowType.MULTI_AGENT,
            id=str(uuid4()),
            status=WorkflowStatus.PENDING,
            intent_id=intent.id,
            context={
                "coordination_id": coordination_result.coordination_id,
                "agent_assignments": {
                    subtask.id: subtask.assigned_agent.value
                    for subtask in coordination_result.subtasks
                },
                "deployment_time": time.time(),
                "deployment_version": "1.0.0",
            },
        )

        # Convert subtasks to workflow tasks
        for subtask in coordination_result.subtasks:
            task = Task(
                id=subtask.id,
                workflow_id=workflow.id,
                name=subtask.title,
                type=self._map_subtask_to_task_type(subtask),
                status=TaskStatus.PENDING,
                input_data={"subtask_data": subtask.__dict__},
            )
            workflow.tasks.append(task)

        return workflow

    def _map_subtask_to_task_type(self, subtask) -> TaskType:
        """Map subtask complexity to task type"""
        if "architecture" in subtask.title.lower():
            return TaskType.ANALYZE_REQUEST
        elif "implementation" in subtask.title.lower():
            return TaskType.EXTRACT_REQUIREMENTS
        elif "testing" in subtask.title.lower():
            return TaskType.IDENTIFY_DEPENDENCIES
        else:
            return TaskType.ANALYZE_REQUEST  # Default

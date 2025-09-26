"""
Mock agents for testing coordination scenarios
Provides MockCoordinatorAgent and create_mock_agent_pool expected by tests
"""

import asyncio
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, Mock


class MockCoordinationResult:
    """Mock result object for coordination operations"""

    def __init__(self, success: bool = True, error: Optional[str] = None, output_data: Optional[Dict[str, Any]] = None):
        self.success = success
        self.error = error
        self.output_data = output_data or {"workflow_ready": True}


class MockAgent:
    """Mock agent for agent pool testing"""

    def __init__(self, agent_type: str, agent_id: Optional[str] = None):
        self.agent_type = agent_type
        self.agent_id = agent_id or f"{agent_type}_agent_{id(self)}"
        self.status = "ready"

    async def get_status(self) -> str:
        """Mock status retrieval"""
        return self.status

    async def execute(self, task: str) -> Dict[str, Any]:
        """Mock task execution"""
        return {
            "task": task,
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "result": "success",
            "execution_time": 0.1
        }


class MockCoordinatorAgent:
    """Mock coordinator agent matching expected interface from tests"""

    def __init__(self):
        self.coordination_calls = []
        self.synchronization_calls = []

    async def coordinate_workflow(self, workflow_name: str, agents: List[MockAgent]) -> MockCoordinationResult:
        """Mock workflow coordination

        Args:
            workflow_name: Name of the workflow to coordinate
            agents: List of agents to coordinate

        Returns:
            MockCoordinationResult with success=True and workflow_ready=True
        """
        self.coordination_calls.append({
            "workflow_name": workflow_name,
            "agent_count": len(agents),
            "agents": [agent.agent_id for agent in agents]
        })

        # Simulate brief coordination time
        await asyncio.sleep(0.01)

        return MockCoordinationResult(
            success=True,
            output_data={
                "workflow_ready": True,
                "coordinated_agents": len(agents),
                "workflow_name": workflow_name
            }
        )

    async def synchronize_agent_states(self, sync_id: str) -> MockCoordinationResult:
        """Mock agent state synchronization

        Args:
            sync_id: Identifier for synchronization operation

        Returns:
            MockCoordinationResult indicating successful synchronization
        """
        self.synchronization_calls.append(sync_id)

        # Simulate brief sync time
        await asyncio.sleep(0.005)

        return MockCoordinationResult(
            success=True,
            output_data={
                "sync_id": sync_id,
                "synchronized": True
            }
        )


def create_mock_agent_pool(agent_types: List[str]) -> List[MockAgent]:
    """Create a pool of mock agents for testing

    Args:
        agent_types: List of agent type strings (e.g., ["code", "architect", "analysis"])

    Returns:
        List of MockAgent instances with specified types
    """
    agents = []
    type_counters = {}

    for agent_type in agent_types:
        # Track how many of each type for unique IDs
        if agent_type not in type_counters:
            type_counters[agent_type] = 0
        type_counters[agent_type] += 1

        agent_id = f"{agent_type}_agent_{type_counters[agent_type]}"
        agent = MockAgent(agent_type=agent_type, agent_id=agent_id)
        agents.append(agent)

    return agents
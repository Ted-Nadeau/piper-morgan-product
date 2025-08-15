"""
Mock Agent Services - PM-033d Testing Infrastructure
Provides configurable mock agents for testing multi-agent coordination scenarios
"""

import asyncio
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from unittest.mock import Mock


@dataclass
class AgentTask:
    """Mock agent task representation"""

    task_id: str
    task_type: str
    description: str
    estimated_duration_ms: int
    dependencies: List[str] = None


@dataclass
class TaskResult:
    """Mock task execution result"""

    success: bool
    output_data: Dict[str, Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    metadata: Dict[str, Any] = None


class MockAgent:
    """Base mock agent with common functionality"""

    def __init__(self, agent_id: str, agent_name: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.capabilities = capabilities
        self.current_tasks: List[AgentTask] = []
        self.completed_tasks: List[TaskResult] = []
        self.health_status = "healthy"
        self.performance_profile = {
            "base_latency_ms": 10,
            "latency_variance_ms": 5,
            "success_rate": 0.95,
            "max_concurrent_tasks": 3,
        }

    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        await asyncio.sleep(0.001)  # Simulate minimal processing time
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "health_status": self.health_status,
            "current_tasks": len(self.current_tasks),
            "completed_tasks": len(self.completed_tasks),
            "capabilities": self.capabilities,
            "performance_profile": self.performance_profile,
        }

    async def accept_task(self, task: AgentTask) -> bool:
        """Accept a new task if capacity available"""
        if len(self.current_tasks) >= self.performance_profile["max_concurrent_tasks"]:
            return False

        self.current_tasks.append(task)
        return True

    def _simulate_execution_time(self, task: AgentTask) -> float:
        """Simulate realistic execution time with variance"""
        base_time = task.estimated_duration_ms
        variance = self.performance_profile["latency_variance_ms"]
        return max(1, base_time + random.uniform(-variance, variance))

    def _should_succeed(self) -> bool:
        """Determine if task should succeed based on success rate"""
        return random.random() < self.performance_profile["success_rate"]


class MockCodeAgent(MockAgent):
    """Mock Code Agent for testing implementation scenarios"""

    def __init__(self):
        super().__init__(
            agent_id="code_agent_001",
            agent_name="Code Agent",
            capabilities=["implementation", "testing", "debugging", "refactoring"],
        )
        self.performance_profile.update(
            {"base_latency_ms": 25, "latency_variance_ms": 10, "success_rate": 0.90}
        )

    async def execute_tasks(self, tasks: List[str]) -> TaskResult:
        """Mock task execution with configurable behavior"""
        # Simulate task execution time
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "implementation", "mock task", 25)
        )

        await asyncio.sleep(execution_time / 1000)  # Convert to seconds

        if self._should_succeed():
            return TaskResult(
                success=True,
                output_data={
                    "tasks_completed": len(tasks),
                    "implementation_details": f"Implemented {len(tasks)} features",
                    "code_quality_score": random.uniform(0.8, 1.0),
                    "test_coverage": random.uniform(0.85, 0.95),
                    "mock": True,
                },
                execution_time_ms=execution_time,
                metadata={"agent_type": "code", "capabilities_used": ["implementation"]},
            )
        else:
            return TaskResult(
                success=False,
                error="Mock code agent failure - testing error scenarios",
                execution_time_ms=execution_time,
                metadata={"agent_type": "code", "failure_reason": "mock_error"},
            )

    async def implement_feature(self, feature_spec: str) -> TaskResult:
        """Mock feature implementation"""
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "implementation", feature_spec, 30)
        )

        await asyncio.sleep(execution_time / 1000)

        return TaskResult(
            success=True,
            output_data={
                "feature_implemented": feature_spec,
                "implementation_time_ms": execution_time,
                "code_complexity": random.randint(1, 5),
                "mock": True,
            },
            execution_time_ms=execution_time,
        )


class MockArchitectAgent(MockAgent):
    """Mock Architect Agent for testing design scenarios"""

    def __init__(self):
        super().__init__(
            agent_id="architect_agent_001",
            agent_name="Architect Agent",
            capabilities=["design", "planning", "architecture_review", "technical_decision"],
        )
        self.performance_profile.update(
            {"base_latency_ms": 40, "latency_variance_ms": 15, "success_rate": 0.95}
        )

    async def design_solution(self, requirements: str) -> TaskResult:
        """Mock design solution creation"""
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "design", requirements, 40)
        )

        await asyncio.sleep(execution_time / 1000)

        return TaskResult(
            success=True,
            output_data={
                "design_solution": f"Architecture for: {requirements}",
                "design_patterns": ["Repository", "Factory", "Observer"],
                "scalability_score": random.uniform(0.8, 1.0),
                "maintainability_score": random.uniform(0.85, 0.95),
                "mock": True,
            },
            execution_time_ms=execution_time,
        )

    async def review_architecture(self, architecture_doc: str) -> TaskResult:
        """Mock architecture review"""
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "review", architecture_doc, 35)
        )

        await asyncio.sleep(execution_time / 1000)

        return TaskResult(
            success=True,
            output_data={
                "review_completed": True,
                "issues_found": random.randint(0, 3),
                "recommendations": ["Optimize database queries", "Add caching layer"],
                "overall_score": random.uniform(0.7, 1.0),
                "mock": True,
            },
            execution_time_ms=execution_time,
        )


class MockAnalysisAgent(MockAgent):
    """Mock Analysis Agent for testing data analysis scenarios"""

    def __init__(self):
        super().__init__(
            agent_id="analysis_agent_001",
            agent_name="Analysis Agent",
            capabilities=["data_analysis", "insights", "metrics", "reporting"],
        )
        self.performance_profile.update(
            {"base_latency_ms": 30, "latency_variance_ms": 12, "success_rate": 0.92}
        )

    async def analyze_data(self, data_source: str) -> TaskResult:
        """Mock data analysis"""
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "analysis", data_source, 30)
        )

        await asyncio.sleep(execution_time / 1000)

        return TaskResult(
            success=True,
            output_data={
                "analysis_completed": True,
                "data_source": data_source,
                "insights_found": random.randint(3, 8),
                "confidence_score": random.uniform(0.8, 0.95),
                "recommendations": ["Increase monitoring", "Optimize performance"],
                "mock": True,
            },
            execution_time_ms=execution_time,
        )

    async def generate_report(self, report_type: str) -> TaskResult:
        """Mock report generation"""
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "reporting", report_type, 45)
        )

        await asyncio.sleep(execution_time / 1000)

        return TaskResult(
            success=True,
            output_data={
                "report_type": report_type,
                "report_generated": True,
                "sections": ["Executive Summary", "Technical Details", "Recommendations"],
                "data_points": random.randint(10, 50),
                "mock": True,
            },
            execution_time_ms=execution_time,
        )


class MockCoordinatorAgent(MockAgent):
    """Mock Coordinator Agent for testing multi-agent coordination"""

    def __init__(self):
        super().__init__(
            agent_id="coordinator_agent_001",
            agent_name="Coordinator Agent",
            capabilities=["coordination", "workflow_management", "agent_synchronization"],
        )
        self.performance_profile.update(
            {"base_latency_ms": 15, "latency_variance_ms": 5, "success_rate": 0.98}
        )
        self.managed_agents: List[MockAgent] = []

    async def coordinate_workflow(self, workflow_id: str, agents: List[MockAgent]) -> TaskResult:
        """Mock workflow coordination"""
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "coordination", f"Coordinate workflow {workflow_id}", 15)
        )

        await asyncio.sleep(execution_time / 1000)

        # Simulate agent coordination
        coordination_results = []
        for agent in agents:
            status = await agent.get_status()
            coordination_results.append(
                {
                    "agent_id": agent.agent_id,
                    "status": status["health_status"],
                    "ready": status["current_tasks"]
                    < agent.performance_profile["max_concurrent_tasks"],
                }
            )

        return TaskResult(
            success=True,
            output_data={
                "workflow_id": workflow_id,
                "agents_coordinated": len(agents),
                "coordination_results": coordination_results,
                "workflow_ready": all(r["ready"] for r in coordination_results),
                "mock": True,
            },
            execution_time_ms=execution_time,
        )

    async def synchronize_agent_states(self, workflow_id: str) -> TaskResult:
        """Mock agent state synchronization"""
        execution_time = self._simulate_execution_time(
            AgentTask("mock", "synchronization", f"Sync workflow {workflow_id}", 10)
        )

        await asyncio.sleep(execution_time / 1000)

        return TaskResult(
            success=True,
            output_data={
                "workflow_id": workflow_id,
                "synchronization_completed": True,
                "agents_synced": len(self.managed_agents),
                "state_consistent": True,
                "mock": True,
            },
            execution_time_ms=execution_time,
        )


# Factory function for creating mock agent instances
def create_mock_agent(agent_type: str) -> MockAgent:
    """Create a mock agent of the specified type"""
    agent_factories = {
        "code": MockCodeAgent,
        "architect": MockArchitectAgent,
        "analysis": MockAnalysisAgent,
        "coordinator": MockCoordinatorAgent,
    }

    if agent_type not in agent_factories:
        raise ValueError(f"Unknown agent type: {agent_type}")

    return agent_factories[agent_type]()


# Convenience function for creating multiple mock agents
def create_mock_agent_pool(agent_types: List[str]) -> List[MockAgent]:
    """Create a pool of mock agents for testing scenarios"""
    return [create_mock_agent(agent_type) for agent_type in agent_types]

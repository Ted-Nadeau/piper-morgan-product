"""
Unit Tests for Agent Coordinator - PM-033d Testing Infrastructure
Tests individual agent coordination capabilities without external dependencies
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from tests.mocks.mock_agents import (
    MockAnalysisAgent,
    MockArchitectAgent,
    MockCodeAgent,
    MockCoordinatorAgent,
    create_mock_agent,
    create_mock_agent_pool,
)
from tests.utils.performance_monitor import PerformanceMonitor, quick_performance_test


class TestAgentCoordinator:
    """Test individual agent coordination capabilities"""

    @pytest.fixture
    def mock_agents(self):
        """Create a pool of mock agents for testing"""
        return create_mock_agent_pool(["code", "architect", "analysis", "coordinator"])

    @pytest.fixture
    def performance_monitor(self):
        """Create performance monitor for validation"""
        return PerformanceMonitor(target_latency_ms=50)  # Agent coordination target

    @pytest.mark.asyncio
    async def test_agent_communication_setup(self, mock_agents, performance_monitor):
        """Test agent communication channel establishment"""
        coordinator = mock_agents[3]  # MockCoordinatorAgent

        # Test communication setup performance
        result, measurement = await performance_monitor.measure_async_operation(
            "agent_communication_setup",
            lambda: coordinator.coordinate_workflow("test_workflow", mock_agents[:3]),
        )

        assert result.success is True
        assert result.output_data["workflow_id"] == "test_workflow"
        assert result.output_data["agents_coordinated"] == 3
        assert measurement.latency_ms <= 50  # PM-033d target

    @pytest.mark.asyncio
    async def test_agent_state_management(self, mock_agents):
        """Test agent state tracking and updates"""
        code_agent = mock_agents[0]  # MockCodeAgent

        # Test initial state
        initial_status = await code_agent.get_status()
        assert initial_status["agent_id"] == "code_agent_001"
        assert initial_status["health_status"] == "healthy"
        assert initial_status["current_tasks"] == 0

        # Test state update after task acceptance
        task_result = await code_agent.execute_tasks(["feature_1", "feature_2"])
        assert task_result.success is True
        assert task_result.output_data["tasks_completed"] == 2

        # Verify state consistency
        updated_status = await code_agent.get_status()
        assert updated_status["completed_tasks"] > 0

    @pytest.mark.asyncio
    async def test_agent_health_monitoring(self, mock_agents):
        """Test agent health check and status reporting"""
        for agent in mock_agents:
            status = await agent.get_status()

            # Validate required status fields
            assert "agent_id" in status
            assert "agent_name" in status
            assert "health_status" in status
            assert "current_tasks" in status
            assert "capabilities" in status

            # Validate health status values
            assert status["health_status"] in ["healthy", "degraded", "unhealthy"]
            assert isinstance(status["current_tasks"], int)
            assert status["current_tasks"] >= 0

    @pytest.mark.asyncio
    async def test_agent_capability_validation(self, mock_agents):
        """Test agent capability validation and task assignment"""
        code_agent = mock_agents[0]  # MockCodeAgent
        architect_agent = mock_agents[1]  # MockArchitectAgent

        # Test code agent capabilities
        code_capabilities = await code_agent.get_status()
        assert "implementation" in code_capabilities["capabilities"]
        assert "testing" in code_capabilities["capabilities"]

        # Test architect agent capabilities
        architect_capabilities = await architect_agent.get_status()
        assert "design" in architect_capabilities["capabilities"]
        assert "planning" in architect_capabilities["capabilities"]

        # Test task execution based on capabilities
        code_result = await code_agent.implement_feature("new_feature")
        assert code_result.success is True
        assert "feature_implemented" in code_result.output_data

        architect_result = await architect_agent.design_solution("requirements")
        assert architect_result.success is True
        assert "design_solution" in architect_result.output_data

    @pytest.mark.asyncio
    async def test_agent_performance_profiles(self, mock_agents):
        """Test agent performance profile validation"""
        for agent in mock_agents:
            status = await agent.get_status()
            profile = status["performance_profile"]

            # Validate performance profile structure
            assert "base_latency_ms" in profile
            assert "latency_variance_ms" in profile
            assert "success_rate" in profile
            assert "max_concurrent_tasks" in profile

            # Validate performance profile values
            assert profile["base_latency_ms"] > 0
            assert profile["latency_variance_ms"] >= 0
            assert 0 < profile["success_rate"] <= 1
            assert profile["max_concurrent_tasks"] > 0

    @pytest.mark.asyncio
    async def test_agent_task_acceptance(self, mock_agents):
        """Test agent task acceptance and capacity management"""
        code_agent = mock_agents[0]  # MockCodeAgent

        # Test initial capacity
        initial_status = await code_agent.get_status()
        max_tasks = initial_status["performance_profile"]["max_concurrent_tasks"]

        # Test task acceptance within capacity
        for i in range(max_tasks):
            task_accepted = await code_agent.accept_task(None)  # Mock task
            assert task_accepted is True

        # Test task rejection when at capacity
        task_accepted = await code_agent.accept_task(None)
        assert task_accepted is False

        # Verify current task count
        updated_status = await code_agent.get_status()
        assert updated_status["current_tasks"] == max_tasks


class TestAgentCommunicationProtocol:
    """Test agent communication protocol implementation"""

    @pytest.fixture
    def coordinator_agent(self):
        """Create coordinator agent for communication testing"""
        return MockCoordinatorAgent()

    @pytest.mark.asyncio
    async def test_workflow_coordination(self, coordinator_agent):
        """Test workflow coordination between multiple agents"""
        agents = create_mock_agent_pool(["code", "architect", "analysis"])

        # Test workflow coordination
        result = await coordinator_agent.coordinate_workflow("test_workflow_001", agents)

        assert result.success is True
        assert result.output_data["workflow_id"] == "test_workflow_001"
        assert result.output_data["agents_coordinated"] == 3
        assert result.output_data["workflow_ready"] is True

        # Validate coordination results
        coordination_results = result.output_data["coordination_results"]
        assert len(coordination_results) == 3

        for agent_result in coordination_results:
            assert "agent_id" in agent_result
            assert "status" in agent_result
            assert "ready" in agent_result

    @pytest.mark.asyncio
    async def test_agent_state_synchronization(self, coordinator_agent):
        """Test agent state synchronization across workflow"""
        # Add agents to coordinator
        agents = create_mock_agent_pool(["code", "architect"])
        coordinator_agent.managed_agents = agents

        # Test state synchronization
        result = await coordinator_agent.synchronize_agent_states("test_workflow_002")

        assert result.success is True
        assert result.output_data["workflow_id"] == "test_workflow_002"
        assert result.output_data["synchronization_completed"] is True
        assert result.output_data["agents_synced"] == 2
        assert result.output_data["state_consistent"] is True

    @pytest.mark.asyncio
    async def test_communication_error_handling(self, coordinator_agent):
        """Test communication error handling and recovery"""
        # Mock agent that raises exception
        mock_agent = Mock()
        mock_agent.get_status = AsyncMock(side_effect=Exception("Communication error"))

        # Test error handling during coordination
        with pytest.raises(Exception, match="Communication error"):
            await coordinator_agent.coordinate_workflow("error_workflow", [mock_agent])


class TestAgentPerformanceValidation:
    """Test agent performance validation against PM-033d targets"""

    @pytest.mark.asyncio
    async def test_agent_coordination_performance_targets(self):
        """Test agent coordination meets PM-033d performance targets"""
        coordinator = MockCoordinatorAgent()
        agents = create_mock_agent_pool(["code", "architect"])

        # Test coordination performance
        result, latency = await quick_performance_test(
            "agent_coordination",
            lambda: coordinator.coordinate_workflow("perf_test", agents),
            target_ms=50,  # PM-033d target
        )

        assert result.success is True
        assert latency <= 50, f"Agent coordination exceeded 50ms target: {latency}ms"

    @pytest.mark.asyncio
    async def test_agent_task_execution_performance(self):
        """Test agent task execution meets performance targets"""
        code_agent = MockCodeAgent()

        # Test task execution performance
        result, latency = await quick_performance_test(
            "code_agent_task_execution",
            lambda: code_agent.execute_tasks(["task1", "task2"]),
            target_ms=100,  # Reasonable target for task execution
        )

        assert result.success is True
        assert latency <= 100, f"Task execution exceeded 100ms target: {latency}ms"

    @pytest.mark.asyncio
    async def test_concurrent_agent_operations(self):
        """Test concurrent agent operations performance"""
        agents = create_mock_agent_pool(["code", "architect", "analysis"])

        # Test concurrent status checks
        start_time = asyncio.get_event_loop().time()

        status_tasks = [agent.get_status() for agent in agents]
        statuses = await asyncio.gather(*status_tasks)

        end_time = asyncio.get_event_loop().time()
        total_latency = (end_time - start_time) * 1000

        # Validate all statuses retrieved
        assert len(statuses) == 3
        for status in statuses:
            assert status["health_status"] == "healthy"

        # Validate concurrent performance (should be faster than sequential)
        assert total_latency <= 100, f"Concurrent operations exceeded 100ms: {total_latency}ms"


class TestAgentFallbackScenarios:
    """Test agent behavior in fallback scenarios (no database)"""

    @pytest.mark.asyncio
    async def test_agent_operation_without_external_dependencies(self):
        """Test agents operate without external dependencies"""
        code_agent = MockCodeAgent()

        # Test agent can operate independently
        status = await code_agent.get_status()
        assert status["health_status"] == "healthy"

        # Test task execution without external calls
        result = await code_agent.implement_feature("standalone_feature")
        assert result.success is True
        assert result.output_data["mock"] is True

    @pytest.mark.asyncio
    async def test_coordinator_fallback_behavior(self):
        """Test coordinator fallback behavior when agents unavailable"""
        coordinator = MockCoordinatorAgent()

        # Test coordination with empty agent list
        result = await coordinator.coordinate_workflow("empty_workflow", [])

        assert result.success is True
        assert result.output_data["agents_coordinated"] == 0
        assert result.output_data["workflow_ready"] is True

    @pytest.mark.asyncio
    async def test_agent_isolation_and_recovery(self):
        """Test agent isolation and recovery scenarios"""
        code_agent = MockCodeAgent()

        # Simulate agent failure
        with patch.object(code_agent, "_should_succeed", return_value=False):
            result = await code_agent.execute_tasks(["failing_task"])
            assert result.success is False
            assert "error" in result.output_data

        # Test agent recovery
        with patch.object(code_agent, "_should_succeed", return_value=True):
            result = await code_agent.execute_tasks(["recovery_task"])
            assert result.success is True
            assert result.output_data["mock"] is True


# Test execution helpers
def run_agent_coordination_tests():
    """Run all agent coordination tests"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_agent_coordination_tests()

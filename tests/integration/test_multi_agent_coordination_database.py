"""
Multi-Agent Coordination Database Integration Tests

PM-033d Phase 4: Comprehensive integration testing for multi-agent coordination
with both database-enabled and database-fallback scenarios.
"""

import asyncio
import time
from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.orchestration.multi_agent_coordinator import (
    AgentType,
    CoordinationStatus,
    MultiAgentCoordinator,
    TaskComplexity,
)
from services.shared_types import IntentCategory


class TestMultiAgentCoordinationDatabase:
    """Integration tests for multi-agent coordination with database scenarios"""

    @pytest.fixture
    async def coordinator(self):
        """Create coordinator for testing"""
        return MultiAgentCoordinator()

    @pytest.fixture
    def complex_intent(self):
        """Create complex intent for testing"""
        return Intent(
            category=IntentCategory.EXECUTION,
            action="implement_github_integration_system",
            original_message="Build a comprehensive GitHub integration system with webhook processing, issue management, and PR automation including full test coverage",
            confidence=0.98,
        )

    @pytest.fixture
    def moderate_intent(self):
        """Create moderate complexity intent"""
        return Intent(
            category=IntentCategory.EXECUTION,
            action="create_api_endpoint",
            original_message="Implement new REST API endpoint for user profile management",
            confidence=0.92,
        )

    async def test_database_enabled_coordination(self, coordinator, complex_intent):
        """Test coordination with full database integration"""

        # Simulate database available scenario
        start_time = time.time()

        result = await coordinator.coordinate_task(complex_intent)

        coordination_time_ms = int((time.time() - start_time) * 1000)

        # Validate coordination success
        assert result.status == CoordinationStatus.ASSIGNED
        assert result.success_rate == 1.0
        assert len(result.subtasks) >= 2  # Should decompose complex task

        # Validate performance target
        assert (
            result.total_duration_ms < 1000
        ), f"Coordination took {result.total_duration_ms}ms, target: <1000ms"

        # Validate agent assignments
        code_tasks = [t for t in result.subtasks if t.assigned_agent == AgentType.CODE]
        cursor_tasks = [t for t in result.subtasks if t.assigned_agent == AgentType.CURSOR]

        assert len(code_tasks) > 0, "Code agent should have assigned tasks"
        assert len(cursor_tasks) > 0, "Cursor agent should have assigned tasks"

        # Validate task dependencies
        dependency_chain = []
        for task in result.subtasks:
            if task.dependencies:
                dependency_chain.extend(task.dependencies)

        # Complex tasks should have dependency chains
        assert len(dependency_chain) > 0, "Complex tasks should have dependencies"

    async def test_database_fallback_coordination(self, coordinator, moderate_intent):
        """Test coordination without database (fallback mode)"""

        # Simulate database unavailable scenario
        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope"
        ) as mock_db:
            mock_db.side_effect = Exception("Database unavailable")

            start_time = time.time()

            result = await coordinator.coordinate_task(moderate_intent)

            coordination_time_ms = int((time.time() - start_time) * 1000)

            # Should still succeed with fallback
            assert result.status == CoordinationStatus.ASSIGNED
            assert result.success_rate == 1.0
            assert len(result.subtasks) >= 1

            # Performance should still meet targets in fallback
            assert (
                result.total_duration_ms < 1000
            ), f"Fallback coordination took {result.total_duration_ms}ms"

    async def test_performance_under_load(self, coordinator):
        """Test coordination performance with multiple concurrent tasks"""

        # Create multiple intents for concurrent processing
        intents = []
        for i in range(5):
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action=f"implement_feature_{i}",
                original_message=f"Implement feature {i} with testing and documentation",
                confidence=0.95,
            )
            intents.append(intent)

        # Execute coordination tasks concurrently
        start_time = time.time()

        tasks = [coordinator.coordinate_task(intent) for intent in intents]
        results = await asyncio.gather(*tasks)

        total_time_ms = int((time.time() - start_time) * 1000)

        # Validate all coordinations succeeded
        for i, result in enumerate(results):
            assert result.status == CoordinationStatus.ASSIGNED, f"Task {i} failed coordination"
            assert result.success_rate == 1.0, f"Task {i} had success rate {result.success_rate}"

        # Validate performance under load
        avg_time_per_coordination = total_time_ms / len(results)
        assert (
            avg_time_per_coordination < 1000
        ), f"Average coordination time {avg_time_per_coordination}ms exceeds 1000ms target"

        # Validate concurrent coordination efficiency
        assert (
            total_time_ms < 3000
        ), f"Total concurrent coordination time {total_time_ms}ms should be <3000ms"

    async def test_agent_capability_optimization(self, coordinator):
        """Test that coordination optimizes agent assignments based on capabilities"""

        # Test database-heavy intent (should prefer Code agent)
        db_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="migrate_database_schema",
            original_message="Migrate database schema with new tables and indexes",
            confidence=0.98,
        )

        result = await coordinator.coordinate_task(db_intent)

        # Validate Code agent gets database tasks
        code_tasks = [t for t in result.subtasks if t.assigned_agent == AgentType.CODE]
        db_related_tasks = [
            t
            for t in code_tasks
            if any(
                cap in ["database_operations", "infrastructure"] for cap in t.required_capabilities
            )
        ]

        assert len(db_related_tasks) > 0, "Database tasks should be assigned to Code agent"

        # Test UI-heavy intent (should prefer Cursor agent)
        ui_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_user_interface",
            original_message="Create user interface with testing and documentation",
            confidence=0.96,
        )

        result = await coordinator.coordinate_task(ui_intent)

        # Validate Cursor agent gets UI/testing tasks
        cursor_tasks = [t for t in result.subtasks if t.assigned_agent == AgentType.CURSOR]
        ui_related_tasks = [
            t
            for t in cursor_tasks
            if any(
                cap in ["ui_components", "testing_frameworks"] for cap in t.required_capabilities
            )
        ]

        assert len(ui_related_tasks) > 0, "UI/testing tasks should be assigned to Cursor agent"

    async def test_coordination_metrics_collection(self, coordinator, complex_intent):
        """Test that coordination properly collects performance metrics"""

        # Execute multiple coordinations to generate metrics
        for i in range(3):
            await coordinator.coordinate_task(complex_intent)

        # Get performance metrics
        metrics = await coordinator.get_performance_metrics()

        # Validate metrics structure
        assert "total_coordinations" in metrics
        assert "average_latency_ms" in metrics
        assert "success_rate" in metrics
        assert "performance_target_met" in metrics
        assert "agent_utilization" in metrics

        # Validate metrics values
        assert metrics["total_coordinations"] == 3
        assert metrics["average_latency_ms"] >= 0
        assert metrics["success_rate"] == 1.0  # All should succeed
        assert metrics["performance_target_met"] is True  # Should meet <1000ms target

        # Validate agent utilization tracking
        utilization = metrics["agent_utilization"]
        assert "code_agent_tasks" in utilization
        assert "cursor_agent_tasks" in utilization
        assert utilization["code_agent_tasks"] > 0
        assert utilization["cursor_agent_tasks"] > 0

    async def test_coordination_error_handling(self, coordinator):
        """Test coordination error handling and graceful degradation"""

        # Test with malformed intent
        malformed_intent = Intent(
            category=IntentCategory.UNKNOWN, action="", original_message="", confidence=0.0
        )

        result = await coordinator.coordinate_task(malformed_intent)

        # Should handle gracefully but may fail
        assert result.coordination_id is not None
        assert result.total_duration_ms >= 0

        # If it fails, should have error details
        if result.status == CoordinationStatus.FAILED:
            assert result.error_details is not None
            assert result.success_rate == 0.0

        # Should still meet performance targets even for errors
        assert result.total_duration_ms < 1000

    async def test_database_transaction_coordination(self, coordinator):
        """Test coordination with database transaction requirements"""

        # Test intent requiring database transactions
        transaction_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="batch_data_migration",
            original_message="Perform batch data migration with transaction rollback capability and comprehensive validation",
            confidence=0.99,
        )

        result = await coordinator.coordinate_task(transaction_intent)

        # Validate coordination handles transaction requirements
        assert result.status == CoordinationStatus.ASSIGNED
        assert len(result.subtasks) > 1  # Should decompose for transaction safety

        # Validate database-capable agent gets transaction tasks
        code_tasks = [t for t in result.subtasks if t.assigned_agent == AgentType.CODE]
        transaction_tasks = [
            t for t in code_tasks if "database_operations" in t.required_capabilities
        ]

        assert (
            len(transaction_tasks) > 0
        ), "Database transaction tasks should be assigned to Code agent"


class TestCoordinationPerformanceBenchmarks:
    """Performance benchmark tests for coordination system"""

    async def test_coordination_latency_benchmark(self):
        """Benchmark coordination latency under various scenarios"""

        coordinator = MultiAgentCoordinator()

        # Test scenarios with different complexities
        scenarios = [
            (
                "simple",
                Intent(
                    category=IntentCategory.QUERY,
                    action="get_status",
                    original_message="Get current status",
                    confidence=0.9,
                ),
            ),
            (
                "moderate",
                Intent(
                    category=IntentCategory.EXECUTION,
                    action="implement_feature",
                    original_message="Implement new feature with tests",
                    confidence=0.95,
                ),
            ),
            (
                "complex",
                Intent(
                    category=IntentCategory.EXECUTION,
                    action="refactor_system",
                    original_message="Refactor entire system architecture with migration strategy and comprehensive testing",
                    confidence=0.98,
                ),
            ),
        ]

        benchmark_results = {}

        for scenario_name, intent in scenarios:
            # Warm up
            await coordinator.coordinate_task(intent)

            # Benchmark multiple runs
            latencies = []
            for _ in range(10):
                start_time = time.time()
                result = await coordinator.coordinate_task(intent)
                latency_ms = int((time.time() - start_time) * 1000)
                latencies.append(latency_ms)

                # Ensure coordination succeeded
                assert result.status == CoordinationStatus.ASSIGNED

            # Calculate statistics
            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            min_latency = min(latencies)

            benchmark_results[scenario_name] = {
                "avg_latency_ms": avg_latency,
                "max_latency_ms": max_latency,
                "min_latency_ms": min_latency,
                "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            }

            # Validate performance targets
            assert (
                avg_latency < 1000
            ), f"{scenario_name} avg latency {avg_latency}ms exceeds 1000ms target"
            assert (
                max_latency < 2000
            ), f"{scenario_name} max latency {max_latency}ms exceeds 2000ms threshold"

        # Log benchmark results for analysis
        print(f"\n📊 Coordination Performance Benchmarks:")
        for scenario, metrics in benchmark_results.items():
            print(
                f"  {scenario.upper()}: avg={metrics['avg_latency_ms']:.1f}ms, "
                f"p95={metrics['p95_latency_ms']:.1f}ms, max={metrics['max_latency_ms']:.1f}ms"
            )

        return benchmark_results


# Database Integration Test Utilities
async def setup_test_database():
    """Setup test database for integration testing"""
    # This would normally set up a test database
    # For now, we'll use mocking
    pass


async def cleanup_test_database():
    """Cleanup test database after testing"""
    # This would normally clean up test database
    # For now, we'll use mocking
    pass

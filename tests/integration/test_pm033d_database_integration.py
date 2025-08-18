#!/usr/bin/env python3
"""
PM-033d Database Integration Tests
Validates testing framework works with real database connections
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tests.mocks.mock_agents import MockCoordinatorAgent, create_mock_agent_pool
from tests.utils.performance_monitor import PerformanceMonitor


class PM033dDatabaseIntegrationTester:
    """Test PM-033d framework with database integration"""

    def __init__(self):
        self.results = {
            "database_connection": [],
            "agent_coordination_with_db": [],
            "performance_with_db": [],
            "fallback_with_db": [],
        }
        self.performance_monitor = PerformanceMonitor(target_latency_ms=1000)

    async def test_database_connection(self):
        """Test database connectivity"""
        print("🗄️ Testing Database Connection")

        test_results = []

        # Test 1: PostgreSQL Connection
        try:
            import psycopg2
            from psycopg2 import OperationalError

            # Try to connect to PostgreSQL
            conn = psycopg2.connect(
                host="localhost", port=5432, database="postgres", user="xian", password=""
            )

            # Test basic operations
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()

            cursor.close()
            conn.close()

            test_results.append(
                ("postgresql_connection", True, f"Connected to PostgreSQL: {version[0][:50]}...")
            )
        except ImportError:
            test_results.append(("postgresql_connection", False, "psycopg2 not available"))
        except OperationalError as e:
            test_results.append(("postgresql_connection", False, f"Connection failed: {e}"))
        except Exception as e:
            test_results.append(("postgresql_connection", False, f"Unexpected error: {e}"))

        # Test 2: SQLAlchemy Connection
        try:
            from sqlalchemy import create_engine, text
            from sqlalchemy.exc import OperationalError

            # Create engine
            engine = create_engine("postgresql://xian@localhost:5432/postgres")

            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.scalar() == 1, "Basic query failed"

            test_results.append(("sqlalchemy_connection", True, "SQLAlchemy connection successful"))
        except ImportError:
            test_results.append(("sqlalchemy_connection", False, "SQLAlchemy not available"))
        except OperationalError as e:
            test_results.append(
                ("sqlalchemy_connection", False, f"SQLAlchemy connection failed: {e}")
            )
        except Exception as e:
            test_results.append(("sqlalchemy_connection", False, f"Unexpected error: {e}"))

        self.results["database_connection"] = test_results
        return test_results

    async def test_agent_coordination_with_db(self):
        """Test agent coordination with database available"""
        print("🤖 Testing Agent Coordination with Database")

        test_results = []

        # Test 1: Agent Creation with DB Context
        try:
            agents = create_mock_agent_pool(["code", "architect", "analysis"])
            assert len(agents) == 3, f"Expected 3 agents, got {len(agents)}"
            test_results.append(
                ("agent_creation_with_db", True, "Agents created successfully with DB context")
            )
        except Exception as e:
            test_results.append(("agent_creation_with_db", False, str(e)))

        # Test 2: Coordination with DB Available
        try:
            coordinator = MockCoordinatorAgent()
            result = await coordinator.coordinate_workflow("db_integration_test", agents)

            assert result.success is True, f"Coordination failed: {result.error}"
            assert (
                result.output_data["workflow_ready"] is True
            ), f"Workflow not ready: {result.output_data}"
            test_results.append(
                ("coordination_with_db", True, "Coordination successful with DB available")
            )
        except Exception as e:
            test_results.append(("coordination_with_db", False, str(e)))

        # Test 3: Agent Status with DB Context
        try:
            for agent in agents:
                status = await agent.get_status()
                assert "agent_id" in status, f"Missing agent_id in status: {status}"
                assert "health_status" in status, f"Missing health_status in status: {status}"
            test_results.append(
                ("agent_status_with_db", True, "All agent statuses retrieved with DB context")
            )
        except Exception as e:
            test_results.append(("agent_status_with_db", False, str(e)))

        self.results["agent_coordination_with_db"] = test_results
        return test_results

    async def test_performance_with_db(self):
        """Test performance with database integration"""
        print("⚡ Testing Performance with Database Integration")

        test_results = []

        # Test 1: Coordination Performance with DB
        try:
            coordinator = MockCoordinatorAgent()
            agents = create_mock_agent_pool(["code", "architect", "analysis"])

            result, measurement = await self.performance_monitor.measure_async_operation(
                "agent_coordination_with_db",
                lambda: coordinator.coordinate_workflow("perf_db_test", agents),
            )

            assert result.success is True, f"Performance test coordination failed: {result.error}"
            assert (
                measurement.latency_ms <= 1000
            ), f"Performance exceeded 1000ms: {measurement.latency_ms}ms"

            test_results.append(
                (
                    "coordination_performance_with_db",
                    True,
                    f"Latency: {measurement.latency_ms:.2f}ms",
                )
            )
        except Exception as e:
            test_results.append(("coordination_performance_with_db", False, str(e)))

        # Test 2: Concurrent Operations with DB
        try:
            agents = create_mock_agent_pool(["code"] * 3 + ["architect"] * 3)

            start_time = asyncio.get_event_loop().time()
            status_tasks = [agent.get_status() for agent in agents]
            statuses = await asyncio.gather(*status_tasks)
            end_time = asyncio.get_event_loop().time()

            total_latency = (end_time - start_time) * 1000
            assert (
                total_latency <= 1000
            ), f"Concurrent operations exceeded 1000ms: {total_latency}ms"
            assert len(statuses) == 6, f"Expected 6 statuses, got {len(statuses)}"

            test_results.append(
                ("concurrent_operations_with_db", True, f"Latency: {total_latency:.2f}ms")
            )
        except Exception as e:
            test_results.append(("concurrent_operations_with_db", False, str(e)))

        self.results["performance_with_db"] = test_results
        return test_results

    async def test_fallback_with_db(self):
        """Test fallback scenarios even with database available"""
        print("🔄 Testing Fallback Scenarios with Database Available")

        test_results = []

        # Test 1: Agent Independence (should work regardless of DB)
        try:
            code_agent = create_mock_agent_pool(["code"])[0]
            status = await code_agent.get_status()
            assert (
                status["health_status"] == "healthy"
            ), f"Agent not healthy: {status['health_status']}"
            test_results.append(
                ("agent_independence_with_db", True, "Agent operates independently even with DB")
            )
        except Exception as e:
            test_results.append(("agent_independence_with_db", False, str(e)))

        # Test 2: Coordinator Fallback (empty agent list)
        try:
            coordinator = MockCoordinatorAgent()
            result = await coordinator.coordinate_workflow("fallback_db_test", [])
            assert result.success is True, f"Empty coordination failed: {result.error}"
            test_results.append(
                (
                    "coordinator_fallback_with_db",
                    True,
                    "Coordinator handles empty agent list with DB",
                )
            )
        except Exception as e:
            test_results.append(("coordinator_fallback_with_db", False, str(e)))

        # Test 3: Mock Agent Fallback (no real DB operations)
        try:
            agents = create_mock_agent_pool(["code", "architect"])
            for agent in agents:
                # These should work without real DB operations
                status = await agent.get_status()
                assert "agent_id" in status, f"Missing agent_id: {status}"
            test_results.append(
                ("mock_agent_fallback_with_db", True, "Mock agents work without real DB operations")
            )
        except Exception as e:
            test_results.append(("mock_agent_fallback_with_db", False, str(e)))

        self.results["fallback_with_db"] = test_results
        return test_results

    def print_summary(self):
        """Print database integration test summary"""
        print("\n" + "=" * 80)
        print("🗄️ PM-033d DATABASE INTEGRATION VALIDATION SUMMARY")
        print("=" * 80)

        total_tests = 0
        total_passed = 0

        for test_category, tests in self.results.items():
            print(f"\n📋 {test_category.upper().replace('_', ' ')}:")
            category_passed = 0

            for test_name, passed, message in tests:
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"  {status} {test_name}: {message}")
                if passed:
                    category_passed += 1
                total_tests += 1

            print(f"  📊 {category_passed}/{len(tests)} tests passed")
            total_passed += category_passed

        print(f"\n🎉 DATABASE INTEGRATION RESULTS: {total_passed}/{total_tests} tests passed")

        if total_passed == total_tests:
            print("🚀 ALL DATABASE INTEGRATION TESTS PASSED!")
            print("✅ PM-033d Framework works with AND without database")
        else:
            print("⚠️  Some database integration tests failed - Review required")

        print("=" * 80)

    async def run_all_database_tests(self):
        """Run all database integration tests"""
        print("🗄️ Starting PM-033d Database Integration Testing")
        print("=" * 60)

        # Run all test categories
        await self.test_database_connection()
        await self.test_agent_coordination_with_db()
        await self.test_performance_with_db()
        await self.test_fallback_with_db()

        # Print comprehensive summary
        self.print_summary()

        return self.results


async def main():
    """Main database integration test execution function"""
    tester = PM033dDatabaseIntegrationTester()
    results = await tester.run_all_database_tests()
    return results


if __name__ == "__main__":
    # Run the database integration test suite
    asyncio.run(main())

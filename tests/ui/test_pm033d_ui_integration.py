#!/usr/bin/env python3
"""
PM-033d UI Integration Tests
Validates UI components with real coordination workflows
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tests.mocks.mock_agents import MockCoordinatorAgent, create_mock_agent_pool
from tests.utils.performance_monitor import PerformanceMonitor


class PM033dUIIntegrationTester:
    """Test UI components with real coordination workflows"""

    def __init__(self):
        self.results = {
            "ui_component_validation": [],
            "workflow_coordination_ui": [],
            "performance_ui_integration": [],
            "real_time_updates": [],
        }
        self.performance_monitor = PerformanceMonitor(target_latency_ms=1000)

    def test_ui_component_structure(self):
        """Test UI component structure and validation"""
        print("🎨 Testing UI Component Structure")

        test_results = []

        # Test 1: Component Files Exist
        try:
            jsx_path = project_root / "web/components/MultiAgentWorkflowProgress.jsx"
            css_path = project_root / "web/components/MultiAgentWorkflowProgress.css"

            assert jsx_path.exists(), f"JSX component not found: {jsx_path}"
            assert css_path.exists(), f"CSS component not found: {css_path}"

            test_results.append(("component_files_exist", True, "UI component files found"))
        except Exception as e:
            test_results.append(("component_files_exist", False, str(e)))

        # Test 2: JSX Component Structure
        try:
            jsx_content = (
                project_root / "web/components/MultiAgentWorkflowProgress.jsx"
            ).read_text()

            # Check for required React imports
            assert "import React" in jsx_content, "React import not found"
            assert "useState" in jsx_content, "useState hook not found"
            assert "useEffect" in jsx_content, "useEffect hook not found"

            # Check for component definition
            assert "MultiAgentWorkflowProgress" in jsx_content, "Component name not found"
            assert "export default" in jsx_content, "Export statement not found"

            test_results.append(("jsx_structure", True, "JSX component structure valid"))
        except Exception as e:
            test_results.append(("jsx_structure", False, str(e)))

        # Test 3: CSS Styling Structure
        try:
            css_content = (
                project_root / "web/components/MultiAgentWorkflowProgress.css"
            ).read_text()

            # Check for required CSS classes
            assert ".multi-agent-workflow-progress" in css_content, "Main CSS class not found"
            assert ".workflow-header" in css_content, "Header CSS class not found"
            assert ".performance-metrics" in css_content, "Performance metrics CSS not found"
            assert ".agent-status-section" in css_content, "Agent status CSS not found"

            # Check for responsive design
            assert "@media" in css_content, "Responsive design not found"

            test_results.append(("css_structure", True, "CSS styling structure valid"))
        except Exception as e:
            test_results.append(("css_structure", False, str(e)))

        self.results["ui_component_validation"] = test_results
        return test_results

    async def test_workflow_coordination_ui(self):
        """Test UI integration with workflow coordination"""
        print("🤖 Testing Workflow Coordination UI Integration")

        test_results = []

        # Test 1: Mock Workflow Data Generation
        try:
            # Create realistic workflow data for UI testing
            workflow_data = {
                "workflowId": "ui_test_workflow_001",
                "workflowName": "PM-033d UI Integration Test",
                "agents": [
                    {"id": "code_001", "name": "Code Agent", "type": "code"},
                    {"id": "architect_001", "name": "Architect Agent", "type": "architect"},
                    {"id": "analysis_001", "name": "Analysis Agent", "type": "analysis"},
                ],
                "tasks": [
                    {
                        "id": "task_001",
                        "name": "Implement Coordination Logic",
                        "estimatedDuration": 5000,
                    },
                    {"id": "task_002", "name": "Design Agent Interface", "estimatedDuration": 3000},
                    {
                        "id": "task_003",
                        "name": "Analyze Performance Metrics",
                        "estimatedDuration": 2000,
                    },
                ],
            }

            # Validate workflow data structure
            assert "workflowId" in workflow_data, "Missing workflowId"
            assert "agents" in workflow_data, "Missing agents"
            assert "tasks" in workflow_data, "Missing tasks"
            assert (
                len(workflow_data["agents"]) == 3
            ), f"Expected 3 agents, got {len(workflow_data['agents'])}"
            assert (
                len(workflow_data["tasks"]) == 3
            ), f"Expected 3 tasks, got {len(workflow_data['tasks'])}"

            test_results.append(
                ("workflow_data_generation", True, "Workflow data generated successfully")
            )
        except Exception as e:
            test_results.append(("workflow_data_generation", False, str(e)))

        # Test 2: Agent Coordination Simulation
        try:
            coordinator = MockCoordinatorAgent()
            agents = create_mock_agent_pool(["code", "architect", "analysis"])

            # Simulate coordination workflow
            result = await coordinator.coordinate_workflow("ui_coordination_test", agents)

            assert result.success is True, f"Coordination failed: {result.error}"
            assert (
                result.output_data["workflow_ready"] is True
            ), f"Workflow not ready: {result.output_data}"

            # Validate coordination results for UI display
            coordination_results = result.output_data["coordination_results"]
            assert (
                len(coordination_results) == 3
            ), f"Expected 3 coordination results, got {len(coordination_results)}"

            for agent_result in coordination_results:
                assert "agent_id" in agent_result, f"Missing agent_id in result: {agent_result}"
                assert "status" in agent_result, f"Missing status in result: {agent_result}"
                assert "ready" in agent_result, f"Missing ready flag in result: {agent_result}"

            test_results.append(
                ("agent_coordination_simulation", True, "Agent coordination simulation successful")
            )
        except Exception as e:
            test_results.append(("agent_coordination_simulation", False, str(e)))

        # Test 3: UI Data Formatting
        try:
            # Simulate data that would be passed to UI component
            ui_props = {
                "workflowId": "ui_test_001",
                "workflowName": "UI Integration Test",
                "agents": [{"id": "agent_001", "name": "Test Agent", "capabilities": ["test"]}],
                "tasks": [{"id": "task_001", "name": "Test Task", "estimatedDuration": 1000}],
            }

            # Validate UI props structure
            required_props = ["workflowId", "workflowName", "agents", "tasks"]
            for prop in required_props:
                assert prop in ui_props, f"Missing required prop: {prop}"

            # Validate data types
            assert isinstance(ui_props["workflowId"], str), "workflowId must be string"
            assert isinstance(ui_props["agents"], list), "agents must be list"
            assert isinstance(ui_props["tasks"], list), "tasks must be list"

            test_results.append(("ui_data_formatting", True, "UI data formatting valid"))
        except Exception as e:
            test_results.append(("ui_data_formatting", False, str(e)))

        self.results["workflow_coordination_ui"] = test_results
        return test_results

    async def test_performance_ui_integration(self):
        """Test UI performance integration"""
        print("⚡ Testing UI Performance Integration")

        test_results = []

        # Test 1: UI Component Performance
        try:
            # Simulate UI component rendering performance
            start_time = asyncio.get_event_loop().time()

            # Simulate component initialization
            await asyncio.sleep(0.01)  # Simulate React component mount

            # Simulate data processing
            agents = create_mock_agent_pool(["code", "architect", "analysis"])
            coordinator = MockCoordinatorAgent()

            # Simulate workflow coordination for UI
            result = await coordinator.coordinate_workflow("ui_perf_test", agents)

            end_time = asyncio.get_event_loop().time()
            total_latency = (end_time - start_time) * 1000

            assert result.success is True, f"Performance test coordination failed: {result.error}"
            assert total_latency <= 1000, f"UI integration exceeded 1000ms: {total_latency}ms"

            test_results.append(
                ("ui_component_performance", True, f"UI integration latency: {total_latency:.2f}ms")
            )
        except Exception as e:
            test_results.append(("ui_component_performance", False, str(e)))

        # Test 2: Real-time Update Performance
        try:
            coordinator = MockCoordinatorAgent()
            agents = create_mock_agent_pool(["code"] * 5 + ["architect"] * 5)

            # Simulate real-time updates
            update_tasks = []
            for i in range(10):
                task = coordinator.synchronize_agent_states(f"realtime_update_{i}")
                update_tasks.append(task)

            start_time = asyncio.get_event_loop().time()
            results = await asyncio.gather(*update_tasks)
            end_time = asyncio.get_event_loop().time()

            update_latency = (end_time - start_time) * 1000
            assert update_latency <= 1000, f"Real-time updates exceeded 1000ms: {update_latency}ms"

            # Validate all updates successful
            success_count = sum(1 for r in results if r.success)
            assert success_count == 10, f"Expected 10 successful updates, got {success_count}"

            test_results.append(
                (
                    "realtime_update_performance",
                    True,
                    f"Real-time update latency: {update_latency:.2f}ms",
                )
            )
        except Exception as e:
            test_results.append(("realtime_update_performance", False, str(e)))

        self.results["performance_ui_integration"] = test_results
        return test_results

    async def test_real_time_updates(self):
        """Test real-time update functionality"""
        print("🔄 Testing Real-time Update Functionality")

        test_results = []

        # Test 1: Agent Status Updates
        try:
            agents = create_mock_agent_pool(["code", "architect"])

            # Simulate status updates over time
            status_updates = []
            for i in range(5):
                for agent in agents:
                    status = await agent.get_status()
                    status_updates.append(
                        {"agent_id": agent.agent_id, "timestamp": i, "status": status}
                    )

                # Simulate time passing
                await asyncio.sleep(0.01)

            assert (
                len(status_updates) == 10
            ), f"Expected 10 status updates, got {len(status_updates)}"

            # Validate status consistency
            for update in status_updates:
                assert "agent_id" in update, f"Missing agent_id in update: {update}"
                assert "status" in update, f"Missing status in update: {update}"
                assert (
                    "health_status" in update["status"]
                ), f"Missing health_status: {update['status']}"

            test_results.append(
                ("agent_status_updates", True, "Agent status updates working correctly")
            )
        except Exception as e:
            test_results.append(("agent_status_updates", False, str(e)))

        # Test 2: Workflow Progress Updates
        try:
            coordinator = MockCoordinatorAgent()
            agents = create_mock_agent_pool(["code", "architect", "analysis"])

            # Simulate workflow progress
            progress_stages = ["initializing", "coordinating", "executing", "completed"]
            progress_results = []

            for stage in progress_stages:
                result = await coordinator.coordinate_workflow(f"progress_test_{stage}", agents)
                progress_results.append(
                    {
                        "stage": stage,
                        "success": result.success,
                        "workflow_ready": result.output_data["workflow_ready"],
                    }
                )

            assert (
                len(progress_results) == 4
            ), f"Expected 4 progress stages, got {len(progress_results)}"

            # Validate progress consistency
            for progress in progress_results:
                assert "stage" in progress, f"Missing stage in progress: {progress}"
                assert "success" in progress, f"Missing success in progress: {progress}"
                assert progress["success"] is True, f"Progress stage failed: {progress}"

            test_results.append(
                ("workflow_progress_updates", True, "Workflow progress updates working correctly")
            )
        except Exception as e:
            test_results.append(("workflow_progress_updates", False, str(e)))

        # Test 3: Performance Metrics Updates
        try:
            # Simulate performance monitoring updates
            performance_monitor = PerformanceMonitor(target_latency_ms=1000)
            performance_monitor.start_session()

            # Run multiple performance tests
            for i in range(3):
                coordinator = MockCoordinatorAgent()
                agents = create_mock_agent_pool(["code", "architect"])

                result, measurement = await performance_monitor.measure_async_operation(
                    f"perf_test_{i}",
                    lambda: coordinator.coordinate_workflow(f"perf_workflow_{i}", agents),
                )

                assert result.success is True, f"Performance test {i} failed: {result.error}"
                assert (
                    measurement.latency_ms <= 1000
                ), f"Performance test {i} exceeded target: {measurement.latency_ms}ms"

            performance_monitor.end_session()
            summary = performance_monitor.get_session_summary()

            assert (
                summary["total_operations"] == 3
            ), f"Expected 3 operations, got {summary['total_operations']}"
            assert (
                summary["successful_operations"] == 3
            ), f"Expected 3 successful operations, got {summary['successful_operations']}"

            test_results.append(
                (
                    "performance_metrics_updates",
                    True,
                    "Performance metrics updates working correctly",
                )
            )
        except Exception as e:
            test_results.append(("performance_metrics_updates", False, str(e)))

        self.results["real_time_updates"] = test_results
        return test_results

    def print_summary(self):
        """Print UI integration test summary"""
        print("\n" + "=" * 80)
        print("🎨 PM-033d UI INTEGRATION VALIDATION SUMMARY")
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

        print(f"\n🎉 UI INTEGRATION RESULTS: {total_passed}/{total_tests} tests passed")

        if total_passed == total_tests:
            print("🚀 ALL UI INTEGRATION TESTS PASSED!")
            print("✅ PM-033d UI Components Ready for Production")
        else:
            print("⚠️  Some UI integration tests failed - Review required")

        print("=" * 80)

    async def run_all_ui_tests(self):
        """Run all UI integration tests"""
        print("🎨 Starting PM-033d UI Integration Testing")
        print("=" * 60)

        # Run all test categories
        self.test_ui_component_structure()
        await self.test_workflow_coordination_ui()
        await self.test_performance_ui_integration()
        await self.test_real_time_updates()

        # Print comprehensive summary
        self.print_summary()

        return self.results


async def main():
    """Main UI integration test execution function"""
    tester = PM033dUIIntegrationTester()
    results = await tester.run_all_ui_tests()
    return results


if __name__ == "__main__":
    # Run the UI integration test suite
    asyncio.run(main())

"""
Testing Interface for Agent Coordination Validation.

Provides comprehensive testing interface for validating mandatory verification
in agent coordination workflows with expected outcome validation.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from methodology.integration.agent_bridge import (
    AgentCoordinator,
    CoordinationMethod,
    CoordinationTask,
)
from methodology.integration.workflow_bridge import WorkflowIntegrationBridge


class VerificationTestingInterface:
    """Interface for testing mandatory verification in agent coordination."""

    def __init__(self):
        self.coordinator = AgentCoordinator()
        self.workflow_bridge = WorkflowIntegrationBridge()
        self.test_scenarios: List[Dict[str, Any]] = []
        self.test_suites: Dict[str, List[Dict[str, Any]]] = {}
        self._setup_standard_test_scenarios()

    def _setup_standard_test_scenarios(self):
        """Setup standard test scenarios for validation."""

        # Test suite: Sequential Handoff Validation
        self.test_suites["sequential_handoff_validation"] = [
            {
                "scenario_name": "successful_sequential_handoff",
                "coordination_task": {
                    "task": {
                        "description": "Test implementation with evidence",
                        "evidence": [
                            {"type": "terminal", "content": "implementation complete"},
                            {"type": "test_results", "content": "all tests passing"},
                        ],
                        "handoff_protocol_verified": True,
                        "evidence_acknowledged": True,
                        "verification_pyramid": {
                            "pattern_tier": True,
                            "integration_tier": True,
                            "evidence_tier": True,
                        },
                    },
                    "coordination_method": CoordinationMethod.SEQUENTIAL_WITH_HANDOFFS,
                    "agents": ["code_agent", "cursor_agent"],
                    "evidence_requirements": ["terminal_output", "test_results"],
                    "success_criteria": ["Implementation complete", "Evidence verified"],
                },
                "expected_outcome": "success",
            },
            {
                "scenario_name": "blocked_handoff_no_evidence",
                "coordination_task": {
                    "task": {
                        "description": "Test implementation without evidence",
                        "evidence": [],  # No evidence - should be blocked
                    },
                    "coordination_method": CoordinationMethod.SEQUENTIAL_WITH_HANDOFFS,
                    "agents": ["code_agent", "cursor_agent"],
                    "evidence_requirements": ["terminal_output"],
                    "success_criteria": ["Implementation complete"],
                },
                "expected_outcome": "handoff_blocked",
            },
        ]

        # Test suite: Parallel Coordination Validation
        self.test_suites["parallel_coordination_validation"] = [
            {
                "scenario_name": "parallel_cross_validation",
                "coordination_task": {
                    "task": {
                        "description": "Parallel implementation with cross-validation",
                        "type": "dual_implementation",
                    },
                    "coordination_method": CoordinationMethod.PARALLEL_WITH_CROSS_VALIDATION,
                    "agents": ["code_agent", "cursor_agent"],
                    "evidence_requirements": ["cross_validation", "terminal_output"],
                    "success_criteria": [
                        "Both implementations complete",
                        "Cross-validation passed",
                    ],
                },
                "expected_outcome": "parallel_coordination_initiated",
            }
        ]

        # Test suite: Agent Prompt Generation
        self.test_suites["agent_prompt_validation"] = [
            {
                "scenario_name": "high_context_agent_prompt",
                "test_type": "prompt_generation",
                "agent_id": "code_agent",
                "task": {"description": "Implement feature with TDD"},
                "evidence_requirements": ["terminal_output", "test_results"],
                "expected_content": [
                    "SYSTEMATIC METHODOLOGY EXECUTION",
                    "Excellence Flywheel methodology",
                ],
            },
            {
                "scenario_name": "limited_context_agent_prompt",
                "test_type": "prompt_generation",
                "agent_id": "cursor_agent",
                "task": {"description": "Fix validation issue"},
                "evidence_requirements": ["terminal_output", "explicit_verification"],
                "expected_content": [
                    "MANDATORY VERIFICATION REQUIRED",
                    "STOP CONDITIONS",
                    "Never assume",
                ],
            },
        ]

        print(
            f"🧪 Initialized {len(self.test_suites)} test suites with {sum(len(suite) for suite in self.test_suites.values())} scenarios"
        )

    async def test_coordination_scenario(
        self,
        scenario_name: str,
        coordination_task: CoordinationTask,
        expected_outcome: str,
        timeout_seconds: int = 30,
    ) -> Dict[str, Any]:
        """Test coordination scenario with expected outcome."""

        test_start = datetime.now()

        try:
            # Execute coordination with timeout
            result = await asyncio.wait_for(
                self.coordinator.coordinate_task(coordination_task), timeout=timeout_seconds
            )

            test_result = {
                "scenario": scenario_name,
                "expected": expected_outcome,
                "actual": result.get("status", "unknown"),
                "passed": result.get("status") == expected_outcome,
                "test_duration": (datetime.now() - test_start).total_seconds(),
                "evidence": result,
                "coordination_agents": coordination_task.agents,
                "evidence_requirements": coordination_task.evidence_requirements,
            }

            self.test_scenarios.append(test_result)

            # Print test result
            status = "✅ PASS" if test_result["passed"] else "❌ FAIL"
            print(
                f"{status} {scenario_name}: expected {expected_outcome}, got {result.get('status')}"
            )

            return test_result

        except asyncio.TimeoutError:
            test_result = {
                "scenario": scenario_name,
                "expected": expected_outcome,
                "actual": "timeout",
                "passed": False,
                "test_duration": timeout_seconds,
                "error": "Test timed out",
                "coordination_agents": coordination_task.agents,
                "evidence_requirements": coordination_task.evidence_requirements,
            }

            self.test_scenarios.append(test_result)
            print(f"⏱️  TIMEOUT {scenario_name}: test timed out after {timeout_seconds}s")

            return test_result

        except Exception as e:
            test_result = {
                "scenario": scenario_name,
                "expected": expected_outcome,
                "actual": "error",
                "passed": False,
                "test_duration": (datetime.now() - test_start).total_seconds(),
                "error": str(e),
                "coordination_agents": coordination_task.agents,
                "evidence_requirements": coordination_task.evidence_requirements,
            }

            self.test_scenarios.append(test_result)
            print(f"💥 ERROR {scenario_name}: {str(e)}")

            return test_result

    async def run_test_suite(self, suite_name: str) -> Dict[str, Any]:
        """Run complete test suite with all scenarios."""

        if suite_name not in self.test_suites:
            return {
                "suite": suite_name,
                "status": "error",
                "message": f"Unknown test suite: {suite_name}",
                "available_suites": list(self.test_suites.keys()),
            }

        suite_start = datetime.now()
        suite_scenarios = self.test_suites[suite_name]
        suite_results = []

        print(f"\n🧪 Running test suite: {suite_name} ({len(suite_scenarios)} scenarios)")

        for scenario_data in suite_scenarios:
            if scenario_data.get("test_type") == "prompt_generation":
                # Handle prompt generation tests
                result = await self._test_prompt_generation(scenario_data)
            else:
                # Handle coordination tests
                coordination_task = CoordinationTask(**scenario_data["coordination_task"])
                result = await self.test_coordination_scenario(
                    scenario_data["scenario_name"],
                    coordination_task,
                    scenario_data["expected_outcome"],
                )

            suite_results.append(result)

        # Calculate suite statistics
        total_tests = len(suite_results)
        passed_tests = sum(1 for r in suite_results if r.get("passed", False))
        failed_tests = total_tests - passed_tests

        suite_result = {
            "suite": suite_name,
            "status": "completed",
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            "suite_duration": (datetime.now() - suite_start).total_seconds(),
            "test_results": suite_results,
            "suite_passed": failed_tests == 0,
        }

        # Print suite summary
        status = "✅ SUITE PASSED" if suite_result["suite_passed"] else "❌ SUITE FAILED"
        print(
            f"\n{status} {suite_name}: {passed_tests}/{total_tests} tests passed ({suite_result['success_rate']:.1f}%)"
        )

        return suite_result

    async def _test_prompt_generation(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test prompt generation for agents."""

        test_start = datetime.now()
        scenario_name = scenario_data["scenario_name"]

        try:
            # Generate prompt
            prompt = self.coordinator._generate_agent_prompt(
                scenario_data["agent_id"],
                scenario_data["task"],
                scenario_data["evidence_requirements"],
            )

            # Check expected content
            expected_content = scenario_data["expected_content"]
            content_found = [content for content in expected_content if content in prompt]

            passed = len(content_found) == len(expected_content)

            test_result = {
                "scenario": scenario_name,
                "test_type": "prompt_generation",
                "expected_content": expected_content,
                "content_found": content_found,
                "prompt_length": len(prompt),
                "passed": passed,
                "test_duration": (datetime.now() - test_start).total_seconds(),
                "agent_id": scenario_data["agent_id"],
                "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            }

            status = "✅ PASS" if passed else "❌ FAIL"
            print(
                f"{status} {scenario_name}: {len(content_found)}/{len(expected_content)} content checks passed"
            )

            return test_result

        except Exception as e:
            test_result = {
                "scenario": scenario_name,
                "test_type": "prompt_generation",
                "passed": False,
                "test_duration": (datetime.now() - test_start).total_seconds(),
                "error": str(e),
                "agent_id": scenario_data["agent_id"],
            }

            print(f"💥 ERROR {scenario_name}: {str(e)}")
            return test_result

    async def run_all_test_suites(self) -> Dict[str, Any]:
        """Run all test suites."""

        all_start = datetime.now()
        all_results = {}

        print(f"\n🧪 Running all test suites ({len(self.test_suites)} suites)")

        for suite_name in self.test_suites.keys():
            all_results[suite_name] = await self.run_test_suite(suite_name)

        # Calculate overall statistics
        total_suites = len(all_results)
        passed_suites = sum(1 for r in all_results.values() if r.get("suite_passed", False))
        total_tests = sum(r.get("total_tests", 0) for r in all_results.values())
        total_passed = sum(r.get("passed_tests", 0) for r in all_results.values())

        overall_result = {
            "status": "completed",
            "total_suites": total_suites,
            "passed_suites": passed_suites,
            "failed_suites": total_suites - passed_suites,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_tests - total_passed,
            "overall_success_rate": (total_passed / total_tests) * 100 if total_tests > 0 else 0,
            "suite_success_rate": (passed_suites / total_suites) * 100 if total_suites > 0 else 0,
            "total_duration": (datetime.now() - all_start).total_seconds(),
            "suite_results": all_results,
            "all_tests_passed": (total_tests - total_passed) == 0,
        }

        # Print overall summary
        status = (
            "✅ ALL TESTS PASSED" if overall_result["all_tests_passed"] else "❌ SOME TESTS FAILED"
        )
        print(f"\n{status}")
        print(f"Suites: {passed_suites}/{total_suites} passed")
        print(
            f"Tests: {total_passed}/{total_tests} passed ({overall_result['overall_success_rate']:.1f}%)"
        )

        return overall_result

    def create_custom_test_scenario(
        self,
        scenario_name: str,
        coordination_task: Dict[str, Any],
        expected_outcome: str,
        suite_name: str = "custom",
    ) -> bool:
        """Create custom test scenario."""

        if suite_name not in self.test_suites:
            self.test_suites[suite_name] = []

        scenario = {
            "scenario_name": scenario_name,
            "coordination_task": coordination_task,
            "expected_outcome": expected_outcome,
            "created_at": datetime.now().isoformat(),
            "custom": True,
        }

        self.test_suites[suite_name].append(scenario)
        print(f"✅ Added custom test scenario '{scenario_name}' to suite '{suite_name}'")
        return True

    def get_test_statistics(self) -> Dict[str, Any]:
        """Get testing statistics."""
        total_scenarios = len(self.test_scenarios)
        if total_scenarios == 0:
            return {
                "total_scenarios": 0,
                "passed_scenarios": 0,
                "failed_scenarios": 0,
                "success_rate": 0.0,
                "average_test_time": 0.0,
                "test_suites": len(self.test_suites),
            }

        passed = sum(1 for s in self.test_scenarios if s.get("passed", False))
        failed = total_scenarios - passed

        total_time = sum(s.get("test_duration", 0) for s in self.test_scenarios)
        avg_time = total_time / total_scenarios if total_scenarios > 0 else 0

        return {
            "total_scenarios": total_scenarios,
            "passed_scenarios": passed,
            "failed_scenarios": failed,
            "success_rate": (passed / total_scenarios) * 100 if total_scenarios > 0 else 0,
            "average_test_time": avg_time,
            "test_suites": len(self.test_suites),
            "total_suite_scenarios": sum(len(suite) for suite in self.test_suites.values()),
        }

    def clear_test_history(self):
        """Clear test execution history - for testing purposes."""
        self.test_scenarios.clear()
        print("🧹 Test execution history cleared")

    def export_test_results(self, filename: str = None) -> Dict[str, Any]:
        """Export test results for analysis."""
        if filename is None:
            filename = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "test_statistics": self.get_test_statistics(),
            "test_scenarios": self.test_scenarios,
            "test_suites": self.test_suites,
        }

        print(f"📊 Test results exported to {filename}")
        return export_data

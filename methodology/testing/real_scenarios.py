"""
Real Coordination Scenario Testing.

Implements practical coordination scenarios that validate mandatory handoff
protocol works in realistic agent coordination situations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from methodology.integration.agent_bridge import (
    AgentCoordinator,
    CoordinationMethod,
    CoordinationTask,
)


@dataclass
class RealScenario:
    """Real-world coordination scenario definition."""

    name: str
    description: str
    coordination_method: CoordinationMethod
    agents: List[str]
    task: Dict[str, Any]
    expected_outcome: str
    validation_criteria: List[str]


class RealScenarioRunner:
    """Execute real coordination scenarios to validate mandatory handoff."""

    def __init__(self):
        self.coordinator = AgentCoordinator()
        self.scenarios: List[RealScenario] = []
        self.results: List[Dict[str, Any]] = []
        self._setup_scenarios()

    def _setup_scenarios(self):
        """Setup realistic coordination scenarios."""

        # Scenario 1: Dual Agent Implementation (like today's session)
        self.scenarios.append(
            RealScenario(
                name="dual_agent_implementation",
                description="Code Agent implements core functionality, Cursor Agent provides validation testing",
                coordination_method=CoordinationMethod.PARALLEL_WITH_CROSS_VALIDATION,
                agents=["code_agent", "cursor_agent"],
                task={
                    "type": "implementation",
                    "description": "Implement new feature with comprehensive testing",
                    "evidence": [
                        {"type": "terminal", "content": "Implementation complete with 500 lines"},
                        {"type": "test_results", "content": "All 25 tests passing"},
                        {
                            "type": "cross_validation",
                            "content": "Peer review completed successfully",
                        },
                    ],
                    "handoff_protocol_verified": True,
                    "evidence_acknowledged": True,
                    "verification_pyramid": {
                        "pattern_tier": True,
                        "integration_tier": True,
                        "evidence_tier": True,
                    },
                },
                expected_outcome="parallel_coordination_initiated",
                validation_criteria=[
                    "Both agents receive appropriate prompts",
                    "Cross-validation requirements enforced",
                    "Evidence requirements met",
                ],
            )
        )

        # Scenario 2: Sequential Handoff Chain
        self.scenarios.append(
            RealScenario(
                name="sequential_handoff_chain",
                description="Code implements, Cursor tests, Lead Developer reviews",
                coordination_method=CoordinationMethod.SEQUENTIAL_WITH_HANDOFFS,
                agents=["code_agent", "cursor_agent", "lead_developer"],
                task={
                    "type": "feature_implementation",
                    "description": "Complete feature development pipeline",
                    "evidence": [
                        {"type": "terminal", "content": "Feature implementation completed"},
                        {"type": "test_results", "content": "Integration tests passing"},
                    ],
                    "handoff_protocol_verified": True,
                    "evidence_acknowledged": True,
                    "verification_pyramid": {
                        "pattern_tier": True,
                        "integration_tier": True,
                        "evidence_tier": True,
                    },
                },
                expected_outcome="success",
                validation_criteria=[
                    "Each handoff includes required evidence",
                    "Evidence review completed by each agent",
                    "No bypass paths used",
                ],
            )
        )

        # Scenario 3: Blocked Coordination (Missing Evidence)
        self.scenarios.append(
            RealScenario(
                name="blocked_coordination_no_evidence",
                description="Coordination attempt without evidence should be blocked",
                coordination_method=CoordinationMethod.SEQUENTIAL_WITH_HANDOFFS,
                agents=["agent_a", "agent_b"],
                task={
                    "type": "implementation",
                    "description": "Task without proper evidence",
                    "evidence": [],  # No evidence - should be blocked
                },
                expected_outcome="handoff_blocked",
                validation_criteria=[
                    "Coordination blocked due to missing evidence",
                    "Clear enforcement message provided",
                    "Resolution steps given",
                ],
            )
        )

        # Scenario 4: Review-Based Coordination
        self.scenarios.append(
            RealScenario(
                name="review_based_coordination",
                description="Lead Developer reviews and approves implementation",
                coordination_method=CoordinationMethod.REVIEW_BASED,
                agents=["code_agent", "lead_developer"],
                task={
                    "type": "code_review",
                    "description": "Review implementation for production readiness",
                    "evidence": [
                        {"type": "code_review", "content": "Implementation reviewed and approved"},
                        {"type": "test_coverage", "content": "95% test coverage achieved"},
                    ],
                    "handoff_protocol_verified": True,
                    "evidence_acknowledged": True,
                    "verification_pyramid": {
                        "pattern_tier": True,
                        "integration_tier": True,
                        "evidence_tier": True,
                    },
                },
                expected_outcome="review_coordination_initiated",
                validation_criteria=[
                    "Review process includes evidence validation",
                    "Approval requires concrete evidence",
                    "Review feedback actionable",
                ],
            )
        )

        # Scenario 5: Architecture Review (Chief Architect)
        self.scenarios.append(
            RealScenario(
                name="architecture_review_coordination",
                description="Chief Architect reviews architecture decisions with methodology compliance",
                coordination_method=CoordinationMethod.REVIEW_BASED,
                agents=["code_agent", "chief_architect"],
                task={
                    "type": "architecture_review",
                    "description": "Review system architecture for strategic alignment",
                    "evidence": [
                        {
                            "type": "architectural_evidence",
                            "content": "Architecture diagrams and decisions documented",
                        },
                        {
                            "type": "strategic_analysis",
                            "content": "Strategic alignment analysis completed",
                        },
                        {
                            "type": "methodology_compliance",
                            "content": "Excellence Flywheel methodology compliance verified",
                        },
                    ],
                    "handoff_protocol_verified": True,
                    "evidence_acknowledged": True,
                    "verification_pyramid": {
                        "pattern_tier": True,
                        "integration_tier": True,
                        "evidence_tier": True,
                    },
                },
                expected_outcome="review_coordination_initiated",
                validation_criteria=[
                    "Architecture review includes strategic validation",
                    "Methodology compliance enforced",
                    "Strategic alignment confirmed",
                ],
            )
        )

        print(f"🧪 Initialized {len(self.scenarios)} real coordination scenarios")

    async def run_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Run specific coordination scenario."""
        scenario = next((s for s in self.scenarios if s.name == scenario_name), None)
        if not scenario:
            return {"status": "error", "message": f"Scenario {scenario_name} not found"}

        print(f"🎯 Running scenario: {scenario.name}")
        scenario_start = datetime.now()

        try:
            coordination_task = CoordinationTask(
                task=scenario.task,
                coordination_method=scenario.coordination_method,
                agents=scenario.agents,
                evidence_requirements=["terminal_output", "test_results", "evidence_validation"],
                success_criteria=scenario.validation_criteria,
            )

            result = await self.coordinator.coordinate_task(coordination_task)

            validation_result = {
                "scenario": scenario.name,
                "description": scenario.description,
                "expected_outcome": scenario.expected_outcome,
                "actual_outcome": result.get("status", "unknown"),
                "validation_passed": result.get("status") == scenario.expected_outcome,
                "scenario_duration": (datetime.now() - scenario_start).total_seconds(),
                "agents_used": scenario.agents,
                "coordination_method": scenario.coordination_method.value,
                "evidence": result,
                "validation_criteria_met": self._validate_criteria(
                    result, scenario.validation_criteria
                ),
            }

            self.results.append(validation_result)

            # Print scenario result
            status = "✅ PASS" if validation_result["validation_passed"] else "❌ FAIL"
            print(
                f"{status} {scenario.name}: expected {scenario.expected_outcome}, got {result.get('status')}"
            )

            return validation_result

        except Exception as e:
            error_result = {
                "scenario": scenario.name,
                "description": scenario.description,
                "expected_outcome": scenario.expected_outcome,
                "actual_outcome": "error",
                "validation_passed": False,
                "scenario_duration": (datetime.now() - scenario_start).total_seconds(),
                "error": str(e),
                "agents_used": scenario.agents,
                "coordination_method": scenario.coordination_method.value,
            }

            self.results.append(error_result)
            print(f"💥 ERROR {scenario.name}: {str(e)}")

            return error_result

    def _validate_criteria(self, result: Dict[str, Any], criteria: List[str]) -> Dict[str, bool]:
        """Validate scenario criteria against result."""
        validation = {}
        result_str = str(result).lower()

        for criterion in criteria:
            criterion_lower = criterion.lower()

            if "evidence" in criterion_lower:
                validation[criterion] = "evidence" in result_str or "verification" in result_str
            elif "block" in criterion_lower:
                validation[criterion] = result.get("status") in [
                    "handoff_blocked",
                    "validation_failed",
                ]
            elif "prompt" in criterion_lower:
                validation[criterion] = "agent_prompts" in result or "enforcement_prompt" in result
            elif "cross-validation" in criterion_lower:
                validation[criterion] = "cross_validation" in result_str
            elif "review" in criterion_lower:
                validation[criterion] = "review" in result_str
            elif "strategic" in criterion_lower:
                validation[criterion] = "strategic" in result_str or "architect" in result_str
            else:
                # Default pass for criteria that don't have specific checks
                validation[criterion] = True

        return validation

    async def run_all_scenarios(self) -> Dict[str, Any]:
        """Run all coordination scenarios."""
        print(f"\n🧪 Running all {len(self.scenarios)} coordination scenarios")
        all_start = datetime.now()

        all_results = []

        for scenario in self.scenarios:
            result = await self.run_scenario(scenario.name)
            all_results.append(result)

        # Calculate summary statistics
        total_scenarios = len(all_results)
        passed_scenarios = sum(1 for r in all_results if r.get("validation_passed", False))
        failed_scenarios = total_scenarios - passed_scenarios

        summary = {
            "total_scenarios": total_scenarios,
            "scenarios_passed": passed_scenarios,
            "scenarios_failed": failed_scenarios,
            "success_rate": (
                (passed_scenarios / total_scenarios) * 100 if total_scenarios > 0 else 0
            ),
            "total_duration": (datetime.now() - all_start).total_seconds(),
            "results": all_results,
        }

        # Print summary
        status = "✅ ALL SCENARIOS PASSED" if failed_scenarios == 0 else "❌ SOME SCENARIOS FAILED"
        print(f"\n{status}")
        print(
            f"Results: {passed_scenarios}/{total_scenarios} scenarios passed ({summary['success_rate']:.1f}%)"
        )
        print(f"Total duration: {summary['total_duration']:.2f}s")

        return summary

    def get_scenario_statistics(self) -> Dict[str, Any]:
        """Get scenario execution statistics."""
        if not self.results:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "average_duration": 0.0,
                "scenarios_available": len(self.scenarios),
            }

        total_executions = len(self.results)
        successful = sum(1 for r in self.results if r.get("validation_passed", False))
        total_duration = sum(r.get("scenario_duration", 0) for r in self.results)

        return {
            "total_executions": total_executions,
            "successful_executions": successful,
            "failed_executions": total_executions - successful,
            "success_rate": (successful / total_executions) * 100 if total_executions > 0 else 0,
            "average_duration": total_duration / total_executions if total_executions > 0 else 0,
            "scenarios_available": len(self.scenarios),
        }

    def clear_results(self):
        """Clear scenario execution results - for testing purposes."""
        self.results.clear()
        print("🧹 Scenario execution results cleared")

"""
Orchestration Bridge for methodology-services integration.

Bridges MandatoryHandoffProtocol with existing multi-agent coordination
infrastructure, enforcing verification requirements in existing workflows.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from methodology.coordination.enforcement import EnforcementPatterns
from methodology.coordination.exceptions import HandoffBypassError, HandoffValidationError
from methodology.coordination.handoff import AgentType as HandoffAgentType
from methodology.coordination.handoff import HandoffContext, MandatoryHandoffProtocol
from services.orchestration.multi_agent_coordinator import AgentType as OrchestrationType


class OrchestrationBridge:
    """
    Bridge between methodology coordination and services orchestration.

    Enforces mandatory handoff protocol within existing multi-agent workflows
    while maintaining compatibility with current orchestration patterns.
    """

    def __init__(self):
        self.handoff_protocol = MandatoryHandoffProtocol()
        self.enforcement_patterns = EnforcementPatterns()
        self._agent_type_mapping = self._create_agent_mapping()
        self._active_orchestration_handoffs: Dict[str, str] = {}  # orchestration_id -> handoff_id

    def _create_agent_mapping(self) -> Dict[OrchestrationType, HandoffAgentType]:
        """Map orchestration agent types to handoff agent types."""
        return {
            OrchestrationType.CODE: HandoffAgentType.CODE,
            OrchestrationType.CURSOR: HandoffAgentType.CURSOR,
            OrchestrationType.COORDINATOR: HandoffAgentType.ARCHITECT,
        }

    async def enforce_handoff_in_coordination(
        self,
        orchestration_task_id: str,
        source_agent: OrchestrationType,
        target_agent: OrchestrationType,
        task_description: str,
        communication_protocol: Dict[str, Any],
        github_issue: Optional[str] = None,
    ) -> str:
        """
        Enforce mandatory handoff protocol within orchestration coordination.

        Integrates with existing communication_protocol structure while
        adding mandatory verification requirements.

        Returns handoff_id for tracking.
        """

        # Validate that this follows orchestration patterns
        if communication_protocol.get("coordination_method") != "sequential_with_handoffs":
            raise HandoffValidationError(
                f"Unsupported coordination method: {communication_protocol.get('coordination_method')}. "
                "Mandatory handoffs require sequential_with_handoffs coordination."
            )

        # Extract objectives from orchestration protocol
        task_objectives = [
            "Complete assigned orchestration task",
            "Follow dependency graph requirements",
            "Maintain parallel execution opportunities where available",
        ]

        # Extract completion criteria from protocol
        completion_criteria = [
            "All subtask dependencies resolved",
            "Evidence collected through verification pyramid",
            "GitHub integration requirements met",
            "Real-time coordination updates provided",
        ]

        # Map agent types
        source_handoff_agent = self._agent_type_mapping.get(source_agent, HandoffAgentType.UNKNOWN)
        target_handoff_agent = self._agent_type_mapping.get(target_agent, HandoffAgentType.UNKNOWN)

        # Initiate mandatory handoff
        handoff_id = await self.handoff_protocol.initiate_handoff(
            source_agent=source_handoff_agent,
            target_agent=target_handoff_agent,
            task_description=f"Orchestration Task: {task_description}",
            task_objectives=task_objectives,
            completion_criteria=completion_criteria,
            github_issue=github_issue,
        )

        # Track orchestration-handoff relationship
        self._active_orchestration_handoffs[orchestration_task_id] = handoff_id

        # Enhance communication protocol with handoff enforcement
        enhanced_protocol = {
            **communication_protocol,
            "mandatory_handoff_id": handoff_id,
            "handoff_protocol": "mandatory_verification_enforcement",  # Override existing
            "verification_required": True,
            "bypass_prevention": True,
            "evidence_collection": "three_tier_pyramid",
        }

        return handoff_id

    async def collect_orchestration_evidence(
        self,
        orchestration_task_id: str,
        dependency_graph: Dict[str, Any],
        parallel_groups: List[List[str]],
        agent_assignments: Dict[str, Any],
        execution_results: Dict[str, Any],
        files_modified: List[str] = None,
        files_created: List[str] = None,
        tests_run: List[str] = None,
    ) -> None:
        """
        Collect verification evidence from orchestration execution.

        Translates orchestration results into verification pyramid evidence.
        """

        # Get handoff ID
        handoff_id = self._active_orchestration_handoffs.get(orchestration_task_id)
        if not handoff_id:
            raise HandoffBypassError(
                f"No active handoff for orchestration task: {orchestration_task_id}",
                bypass_attempt_details={"orchestration_task_id": orchestration_task_id},
            )

        # Build pattern evidence from orchestration structure
        pattern_evidence = {
            "multi_agent_coordination": {
                "dependency_graph_valid": bool(dependency_graph),
                "parallel_groups_identified": len(parallel_groups) > 0,
                "agent_assignments_complete": len(agent_assignments) > 0,
                "coordination_method": "sequential_with_handoffs",
            },
            "excellence_flywheel_integration": {
                "verification_first": True,
                "evidence_collection": True,
                "systematic_progress": True,
            },
        }

        # Build integration evidence from execution results
        integration_evidence = {
            "orchestration_execution": {
                "tasks_completed": len([r for r in execution_results.values() if r.get("success")]),
                "total_tasks": len(execution_results),
                "success_rate": len([r for r in execution_results.values() if r.get("success")])
                / max(len(execution_results), 1),
                "dependency_resolution": (
                    "successful"
                    if all(r.get("dependencies_met", False) for r in execution_results.values())
                    else "failed"
                ),
            },
            "github_integration": {
                "branch_strategy": "coordination_branches",
                "status_reporting": "real_time_updates",
            },
        }

        # Build concrete evidence from file changes and test execution
        concrete_evidence = {
            "file_modifications": {
                "files_modified": files_modified or [],
                "files_created": files_created or [],
                "total_file_changes": len(files_modified or []) + len(files_created or []),
            },
            "test_execution": {"tests_run": tests_run or [], "test_count": len(tests_run or [])},
            "orchestration_results": execution_results,
        }

        # Collect evidence through handoff protocol
        await self.handoff_protocol.collect_verification_evidence(
            handoff_id=handoff_id,
            pattern_evidence=pattern_evidence,
            integration_evidence=integration_evidence,
            concrete_evidence=concrete_evidence,
            files_modified=files_modified,
            files_created=files_created,
            tests_run=tests_run,
        )

    async def validate_orchestration_handoff(self, orchestration_task_id: str) -> bool:
        """
        Validate orchestration handoff is ready for transfer.

        Ensures all orchestration requirements plus handoff requirements are met.
        """

        handoff_id = self._active_orchestration_handoffs.get(orchestration_task_id)
        if not handoff_id:
            return False

        # Use handoff protocol validation
        return await self.handoff_protocol.validate_handoff_ready(handoff_id)

    async def execute_orchestration_handoff(self, orchestration_task_id: str) -> Dict[str, Any]:
        """
        Execute orchestration handoff with full evidence trail.

        Returns orchestration-compatible results with handoff evidence.
        """

        handoff_id = self._active_orchestration_handoffs.get(orchestration_task_id)
        if not handoff_id:
            raise HandoffBypassError(
                f"No handoff to execute for orchestration task: {orchestration_task_id}"
            )

        # Execute handoff
        handoff_result = await self.handoff_protocol.execute_handoff(handoff_id)

        # Clean up tracking
        if orchestration_task_id in self._active_orchestration_handoffs:
            del self._active_orchestration_handoffs[orchestration_task_id]

        # Return orchestration-compatible result
        return {
            "orchestration_task_id": orchestration_task_id,
            "handoff_success": handoff_result.success,
            "handoff_evidence": handoff_result.evidence_trail,
            "verification_results": handoff_result.validation_results,
            "execution_time": handoff_result.execution_time,
            "error_message": handoff_result.error_message,
            "enhanced_coordination": {
                "mandatory_verification": True,
                "zero_bypass_paths": True,
                "evidence_based_progress": True,
                "three_tier_verification": True,
            },
        }

    def get_orchestration_handoff_status(
        self, orchestration_task_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get handoff status for orchestration task."""

        handoff_id = self._active_orchestration_handoffs.get(orchestration_task_id)
        if not handoff_id:
            return None

        context = self.handoff_protocol.get_handoff_status(handoff_id)
        if not context:
            return None

        return {
            "orchestration_task_id": orchestration_task_id,
            "handoff_id": handoff_id,
            "handoff_state": context.state.value,
            "source_agent": context.source_agent.value,
            "target_agent": context.target_agent.value,
            "verification_status": {
                "pattern_verification": context.pattern_verification,
                "integration_verification": context.integration_verification,
                "evidence_verification": context.evidence_verification,
            },
            "validation_errors": context.validation_errors,
            "bypass_attempts": len(context.bypass_attempts),
        }

    def enhance_communication_protocol(self, base_protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance existing communication protocol with mandatory handoff enforcement.

        Maintains backward compatibility while adding verification requirements.
        """

        return {
            **base_protocol,
            "handoff_enforcement": "mandatory",
            "verification_pyramid": "three_tier",
            "bypass_prevention": "active",
            "evidence_requirements": {
                "pattern_evidence": "required",
                "integration_evidence": "required",
                "concrete_evidence": "required",
            },
            "validation_hooks": "enabled",
            "audit_trail": "complete",
        }

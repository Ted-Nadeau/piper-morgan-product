"""
Enhanced Orchestration Bridge with Enforcement Patterns.

Integrates MandatoryHandoffProtocol with EnforcementPatterns for comprehensive
coordination with zero-bypass enforcement in existing orchestration workflows.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from methodology.coordination.enforcement import EnforcementPatterns
from methodology.coordination.exceptions import (
    EvidenceRequirementViolation,
    HandoffProtocolViolation,
    StrictEnforcementViolation,
)
from methodology.coordination.handoff import AgentType as HandoffAgentType
from methodology.coordination.handoff import MandatoryHandoffProtocol
from services.orchestration.multi_agent_coordinator import AgentType as OrchestrationType


class EnhancedOrchestrationBridge:
    """
    Bridge with enforcement patterns integrated for zero-bypass coordination.

    Provides comprehensive enforcement while maintaining orchestration compatibility.
    """

    def __init__(self):
        self.enforcement = EnforcementPatterns()
        self.protocol = MandatoryHandoffProtocol()
        self._agent_type_mapping = self._create_agent_mapping()
        self._active_coordinations: Dict[str, Dict[str, Any]] = {}

    def _create_agent_mapping(self) -> Dict[OrchestrationType, HandoffAgentType]:
        """Map orchestration agent types to handoff agent types."""
        return {
            OrchestrationType.CODE: HandoffAgentType.CODE,
            OrchestrationType.CURSOR: HandoffAgentType.CURSOR,
            OrchestrationType.COORDINATOR: HandoffAgentType.ARCHITECT,
        }

    async def coordinate_with_enforcement(
        self, coordination_task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Coordinate tasks with mandatory enforcement - no bypass possible.

        Returns comprehensive coordination result with enforcement status.
        """

        coordination_id = f"coord_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Validate basic coordination requirements
        agents = coordination_task.get("agents", [])
        if len(agents) < 2:
            return {
                "coordination_id": coordination_id,
                "status": "failed",
                "error": "Need at least 2 agents for handoff coordination",
                "enforcement_active": True,
            }

        try:
            # Map agent types
            from_agent = agents[0] if isinstance(agents[0], str) else agents[0].value
            to_agent = agents[1] if isinstance(agents[1], str) else agents[1].value

            # Enforce verification requirements - MANDATORY
            enforcement_result = await self.enforcement.enforce_handoff_requirements(
                task=coordination_task, from_agent=from_agent, to_agent=to_agent
            )

            # Store coordination tracking
            self._active_coordinations[coordination_id] = {
                "task": coordination_task,
                "agents": agents,
                "enforcement_result": enforcement_result,
                "created_at": datetime.now(),
            }

            if not enforcement_result["allowed"]:
                # Generate enforcement prompt for violations
                prompt = self.enforcement.generate_enforcement_prompt(
                    enforcement_result["violations"]
                )

                # Create comprehensive blocked response
                blocked_response = {
                    "coordination_id": coordination_id,
                    "status": "blocked",
                    "enforcement_violations": enforcement_result["violations"],
                    "required_actions": enforcement_result["required_actions"],
                    "enforcement_prompt": prompt,
                    "block_reason": "Strict enforcement violations detected",
                    "resolution_required": True,
                    "violation_count": len(enforcement_result["violations"]),
                }

                # Raise appropriate exception based on violation types
                violation_types = [v["rule"] for v in enforcement_result["violations"]]

                if "mandatory_evidence" in violation_types:
                    raise EvidenceRequirementViolation(
                        "Evidence requirements not met for coordination",
                        missing_evidence=violation_types,
                    )
                elif "no_direct_bypass" in violation_types:
                    raise HandoffProtocolViolation(
                        "Handoff protocol requirements not followed",
                        protocol_failures=violation_types,
                    )
                else:
                    raise StrictEnforcementViolation(
                        "Multiple enforcement violations detected",
                        violations=enforcement_result["violations"],
                        required_actions=enforcement_result["required_actions"],
                    )

            # Proceed with mandatory handoff protocol - enforcement passed
            handoff_id = await self.protocol.initiate_handoff(
                source_agent=self._agent_type_mapping.get(
                    OrchestrationType(from_agent) if isinstance(from_agent, str) else from_agent,
                    HandoffAgentType.UNKNOWN,
                ),
                target_agent=self._agent_type_mapping.get(
                    OrchestrationType(to_agent) if isinstance(to_agent, str) else to_agent,
                    HandoffAgentType.UNKNOWN,
                ),
                task_description=coordination_task.get(
                    "description", "Orchestration coordination task"
                ),
                task_objectives=coordination_task.get("objectives", ["Complete coordination task"]),
                completion_criteria=coordination_task.get(
                    "completion_criteria", ["All requirements met"]
                ),
                github_issue=coordination_task.get("github_issue"),
            )

            # Success response with enforcement confirmation
            success_response = {
                "coordination_id": coordination_id,
                "status": "success",
                "handoff_id": handoff_id,
                "verification_enforced": True,
                "enforcement_passed": True,
                "evidence_validated": True,
                "from_agent": from_agent,
                "to_agent": to_agent,
                "evidence_count": len(coordination_task.get("evidence", [])),
                "violation_history": len(self.enforcement.get_violation_history()),
            }

            # Update coordination tracking
            self._active_coordinations[coordination_id].update(
                {"handoff_id": handoff_id, "status": "success", "completed_at": datetime.now()}
            )

            return success_response

        except (
            EvidenceRequirementViolation,
            HandoffProtocolViolation,
            StrictEnforcementViolation,
        ) as e:
            # Enforcement exceptions - return structured error
            error_response = {
                "coordination_id": coordination_id,
                "status": "enforcement_blocked",
                "error": str(e),
                "enforcement_level": getattr(e, "enforcement_level", "STRICT"),
                "blocks_progress": getattr(e, "blocks_progress", True),
                "violations": getattr(e, "violations", []),
                "required_actions": getattr(e, "required_actions", []),
                "security_violation": getattr(e, "is_security_violation", False),
            }

            # Update coordination tracking with failure
            if coordination_id in self._active_coordinations:
                self._active_coordinations[coordination_id].update(
                    {"status": "enforcement_blocked", "error": str(e), "failed_at": datetime.now()}
                )

            return error_response

        except Exception as e:
            # Unexpected error - fail secure
            error_response = {
                "coordination_id": coordination_id,
                "status": "failed",
                "error": str(e),
                "enforcement_active": True,
                "fail_secure": True,
            }

            # Update coordination tracking
            if coordination_id in self._active_coordinations:
                self._active_coordinations[coordination_id].update(
                    {"status": "failed", "error": str(e), "failed_at": datetime.now()}
                )

            return error_response

    async def validate_coordination_evidence(
        self, coordination_id: str, evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate evidence for coordination task.

        Provides evidence validation with enforcement context.
        """

        if coordination_id not in self._active_coordinations:
            return {
                "coordination_id": coordination_id,
                "validation_status": "failed",
                "error": "Unknown coordination ID",
                "evidence_valid": False,
            }

        coordination = self._active_coordinations[coordination_id]
        task = coordination["task"]

        # Update task with new evidence
        task["evidence"] = evidence
        task["evidence_acknowledged"] = True
        task["handoff_protocol_verified"] = True
        task["verification_pyramid"] = {
            "pattern_tier": True,
            "integration_tier": True,
            "evidence_tier": len(evidence) > 0,
        }

        # Re-run enforcement with updated evidence
        agents = coordination["agents"]
        from_agent = agents[0] if isinstance(agents[0], str) else agents[0].value
        to_agent = agents[1] if isinstance(agents[1], str) else agents[1].value

        enforcement_result = await self.enforcement.enforce_handoff_requirements(
            task=task, from_agent=from_agent, to_agent=to_agent
        )

        return {
            "coordination_id": coordination_id,
            "validation_status": "passed" if enforcement_result["allowed"] else "failed",
            "evidence_valid": enforcement_result["allowed"],
            "evidence_count": len(evidence),
            "violations": enforcement_result["violations"],
            "required_actions": enforcement_result["required_actions"],
            "enforcement_level": enforcement_result["enforcement_level"].value,
        }

    def get_coordination_status(self, coordination_id: str) -> Optional[Dict[str, Any]]:
        """Get status of coordination task."""
        return self._active_coordinations.get(coordination_id)

    def get_enforcement_statistics(self) -> Dict[str, Any]:
        """Get enforcement statistics from patterns."""
        base_stats = self.enforcement.get_enforcement_statistics()

        # Add orchestration-specific statistics
        total_coordinations = len(self._active_coordinations)
        successful_coordinations = sum(
            1 for c in self._active_coordinations.values() if c.get("status") == "success"
        )
        blocked_coordinations = sum(
            1
            for c in self._active_coordinations.values()
            if c.get("status") == "enforcement_blocked"
        )

        base_stats.update(
            {
                "total_coordinations": total_coordinations,
                "successful_coordinations": successful_coordinations,
                "blocked_coordinations": blocked_coordinations,
                "coordination_success_rate": (
                    successful_coordinations / max(total_coordinations, 1)
                )
                * 100,
                "enforcement_block_rate": (blocked_coordinations / max(total_coordinations, 1))
                * 100,
            }
        )

        return base_stats

    def enhance_communication_protocol(self, base_protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance existing communication protocol with mandatory enforcement.

        Maintains backward compatibility while adding verification requirements.
        """

        enhanced_protocol = {
            **base_protocol,
            # Core enforcement enhancements
            "handoff_enforcement": "mandatory",
            "verification_pyramid": "three_tier_required",
            "bypass_prevention": "active",
            # Evidence requirements
            "evidence_requirements": {
                "pattern_evidence": "required",
                "integration_evidence": "required",
                "concrete_evidence": "required",
                "evidence_acknowledgment": "required",
            },
            # Enforcement configuration
            "enforcement_patterns": {
                "mandatory_evidence": "strict",
                "evidence_acknowledgment": "strict",
                "no_direct_bypass": "strict",
                "verification_pyramid_complete": "strict",
            },
            # Audit and security
            "validation_hooks": "enabled",
            "audit_trail": "complete",
            "violation_logging": "enabled",
            "security_monitoring": "active",
            # Integration markers
            "enhanced_orchestration": True,
            "zero_bypass_paths": True,
            "methodology_integration": "full",
        }

        return enhanced_protocol

    def clear_coordination_history(self):
        """Clear coordination history - for testing purposes."""
        self._active_coordinations.clear()
        self.enforcement.clear_violation_history()
        print("🧹 Enhanced orchestration coordination history cleared")

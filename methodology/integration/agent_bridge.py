"""
Agent Integration Bridge for Mandatory Handoff Protocol.

Creates comprehensive bridge system connecting mandatory handoff protocol
to actual agent coordination workflows, making verification non-optional
in all agent interactions.
"""

import asyncio
import inspect
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from methodology.coordination.enforcement import (
    EnforcementLevel,
    EnforcementPatterns,
    VerificationRequired,
)
from methodology.coordination.exceptions import (
    EvidenceRequirementViolation,
    StrictEnforcementViolation,
)
from methodology.coordination.handoff import HandoffContext, MandatoryHandoffProtocol
from methodology.verification.pyramid import VerificationPyramid


class AgentType(Enum):
    """Known agent types in the system with coordination capabilities."""

    CODE = "code_agent"
    CURSOR = "cursor_agent"
    LEAD_DEVELOPER = "lead_developer"
    CHIEF_ARCHITECT = "chief_architect"
    UNKNOWN = "unknown_agent"


class CoordinationMethod(Enum):
    """Coordination methods with mandatory verification."""

    SEQUENTIAL_WITH_HANDOFFS = "sequential_with_handoffs"
    PARALLEL_WITH_CROSS_VALIDATION = "parallel_with_cross_validation"
    REVIEW_BASED = "review_based"


@dataclass
class AgentCapabilities:
    """Agent capabilities and context level for coordination."""

    agent_type: AgentType
    context_level: str  # HIGH, LIMITED, UNKNOWN
    methodology_awareness: bool
    verification_requirements: List[str]
    preferred_evidence_types: List[str]


@dataclass
class CoordinationTask:
    """Complete task coordination specification."""

    task: Dict[str, Any]
    coordination_method: CoordinationMethod
    agents: List[str]
    success_criteria: List[str]
    evidence_requirements: List[str]
    timeout_minutes: int = 60


class AgentCoordinator:
    """
    Bridges verification pyramid with actual agents.
    Makes verification non-optional in all agent workflows.
    """

    def __init__(self):
        self.protocol = MandatoryHandoffProtocol()
        self.enforcement = EnforcementPatterns()
        self.pyramid = VerificationPyramid()
        self.agent_capabilities: Dict[str, AgentCapabilities] = {}
        self.coordination_history: List[Dict[str, Any]] = []
        self._register_known_agents()

    def _register_known_agents(self):
        """Register known agent types with their capabilities."""

        # Code Agent - High context, methodology aware
        self.register_agent_capabilities(
            agent_id="code_agent",
            capabilities=AgentCapabilities(
                agent_type=AgentType.CODE,
                context_level="HIGH",
                methodology_awareness=True,
                verification_requirements=["terminal_output", "test_results", "file_artifacts"],
                preferred_evidence_types=["terminal", "artifact", "test_results"],
            ),
        )

        # Cursor Agent - Limited context, requires explicit guidance
        self.register_agent_capabilities(
            agent_id="cursor_agent",
            capabilities=AgentCapabilities(
                agent_type=AgentType.CURSOR,
                context_level="LIMITED",
                methodology_awareness=False,
                verification_requirements=[
                    "terminal_output",
                    "explicit_verification",
                    "step_by_step_evidence",
                ],
                preferred_evidence_types=[
                    "terminal",
                    "verification_commands",
                    "explicit_validation",
                ],
            ),
        )

        # Lead Developer - High context, strategic oversight
        self.register_agent_capabilities(
            agent_id="lead_developer",
            capabilities=AgentCapabilities(
                agent_type=AgentType.LEAD_DEVELOPER,
                context_level="HIGH",
                methodology_awareness=True,
                verification_requirements=[
                    "evidence_review",
                    "cross_validation",
                    "strategic_assessment",
                ],
                preferred_evidence_types=[
                    "coordination_evidence",
                    "cross_validation_results",
                    "strategic_analysis",
                ],
            ),
        )

        # Chief Architect - High context, methodology expert
        self.register_agent_capabilities(
            agent_id="chief_architect",
            capabilities=AgentCapabilities(
                agent_type=AgentType.CHIEF_ARCHITECT,
                context_level="HIGH",
                methodology_awareness=True,
                verification_requirements=[
                    "architectural_review",
                    "methodology_compliance",
                    "strategic_validation",
                ],
                preferred_evidence_types=[
                    "architectural_evidence",
                    "methodology_reports",
                    "strategic_analysis",
                ],
            ),
        )

    def register_agent_capabilities(self, agent_id: str, capabilities: AgentCapabilities):
        """Register agent capabilities for coordination."""
        self.agent_capabilities[agent_id] = capabilities
        print(
            f"🤖 Registered agent: {agent_id} ({capabilities.agent_type.value}, {capabilities.context_level})"
        )

    async def coordinate_task(self, coordination_task: CoordinationTask) -> Dict[str, Any]:
        """
        Coordinate task between agents with mandatory verification.
        No agent can bypass this coordination system.
        """

        # Step 1: Validate coordination requirements
        validation_result = await self._validate_coordination_task(coordination_task)
        if not validation_result["valid"]:
            return {
                "status": "validation_failed",
                "errors": validation_result["errors"],
                "required_actions": validation_result["required_actions"],
            }

        # Step 2: Execute coordination method with enforcement
        coordination_start = datetime.now()

        try:
            if coordination_task.coordination_method == CoordinationMethod.SEQUENTIAL_WITH_HANDOFFS:
                result = await self._coordinate_sequential_handoffs(coordination_task)
            elif (
                coordination_task.coordination_method
                == CoordinationMethod.PARALLEL_WITH_CROSS_VALIDATION
            ):
                result = await self._coordinate_parallel_validation(coordination_task)
            elif coordination_task.coordination_method == CoordinationMethod.REVIEW_BASED:
                result = await self._coordinate_review_based(coordination_task)
            else:
                return {
                    "status": "unsupported_method",
                    "error": f"Coordination method {coordination_task.coordination_method.value} not supported",
                }

            # Add coordination metadata
            result.update(
                {
                    "coordination_duration": (datetime.now() - coordination_start).total_seconds(),
                    "coordination_timestamp": coordination_start.isoformat(),
                    "agent_capabilities_used": [
                        self.agent_capabilities.get(agent, {}).get("agent_type", "unknown").value
                        for agent in coordination_task.agents
                    ],
                }
            )

            # Store in coordination history
            self.coordination_history.append(result)

            return result

        except Exception as e:
            error_result = {
                "status": "coordination_error",
                "error": str(e),
                "coordination_task": {
                    "method": coordination_task.coordination_method.value,
                    "agents": coordination_task.agents,
                    "evidence_requirements": coordination_task.evidence_requirements,
                },
                "coordination_duration": (datetime.now() - coordination_start).total_seconds(),
            }

            self.coordination_history.append(error_result)
            return error_result

    async def _validate_coordination_task(
        self, coordination_task: CoordinationTask
    ) -> Dict[str, Any]:
        """Validate coordination task requirements."""
        errors = []
        required_actions = []

        # Validate agents
        if len(coordination_task.agents) < 1:
            errors.append("At least one agent required for coordination")
            required_actions.append("Add agents to coordination task")

        # Validate task structure
        if not coordination_task.task.get("description"):
            errors.append("Task description required")
            required_actions.append("Add task description")

        # Validate evidence requirements
        if not coordination_task.evidence_requirements:
            errors.append("Evidence requirements must be specified")
            required_actions.append("Define evidence requirements for coordination")

        # Validate success criteria
        if not coordination_task.success_criteria:
            errors.append("Success criteria must be defined")
            required_actions.append("Define success criteria for coordination")

        return {"valid": len(errors) == 0, "errors": errors, "required_actions": required_actions}

    async def _coordinate_sequential_handoffs(
        self, coordination_task: CoordinationTask
    ) -> Dict[str, Any]:
        """Coordinate sequential handoffs with mandatory verification."""

        agents = coordination_task.agents
        if len(agents) < 2:
            return {
                "status": "error",
                "message": "Sequential coordination requires at least 2 agents",
            }

        handoff_results = []
        current_task = coordination_task.task.copy()

        # Execute sequential handoffs with verification
        for i in range(len(agents) - 1):
            from_agent = agents[i]
            to_agent = agents[i + 1]

            try:
                # Generate agent-specific prompt based on capabilities
                prompt = self._generate_agent_prompt(
                    to_agent, current_task, coordination_task.evidence_requirements
                )

                # Force verification before handoff
                enforcement_result = await self.enforcement.enforce_handoff_requirements(
                    current_task, from_agent, to_agent
                )

                if not enforcement_result["allowed"]:
                    return {
                        "status": "handoff_blocked",
                        "blocked_at": f"{from_agent} -> {to_agent}",
                        "enforcement_violations": enforcement_result["violations"],
                        "required_actions": enforcement_result["required_actions"],
                        "enforcement_prompt": self.enforcement.generate_enforcement_prompt(
                            enforcement_result["violations"]
                        ),
                        "coordination_method": "sequential_with_handoffs",
                        "agents_coordinated": [from_agent, to_agent],
                        "verification_enforced": True,
                    }

                # Execute mandatory handoff with proper agent type conversion
                from methodology.coordination.handoff import AgentType as HandoffAgentType

                # Convert agent strings to handoff agent types
                source_handoff_agent = (
                    HandoffAgentType.CODE
                    if from_agent == "code_agent"
                    else (
                        HandoffAgentType.CURSOR
                        if from_agent == "cursor_agent"
                        else (
                            HandoffAgentType.ARCHITECT
                            if from_agent in ["lead_developer", "chief_architect"]
                            else HandoffAgentType.UNKNOWN
                        )
                    )
                )

                target_handoff_agent = (
                    HandoffAgentType.CODE
                    if to_agent == "code_agent"
                    else (
                        HandoffAgentType.CURSOR
                        if to_agent == "cursor_agent"
                        else (
                            HandoffAgentType.ARCHITECT
                            if to_agent in ["lead_developer", "chief_architect"]
                            else HandoffAgentType.UNKNOWN
                        )
                    )
                )

                handoff_id = await self.protocol.initiate_handoff(
                    source_agent=source_handoff_agent,
                    target_agent=target_handoff_agent,
                    task_description=current_task.get(
                        "description", "Sequential coordination task"
                    ),
                    task_objectives=coordination_task.success_criteria,
                    completion_criteria=coordination_task.evidence_requirements,
                )

                # Collect evidence for handoff
                await self.protocol.collect_verification_evidence(
                    handoff_id=handoff_id,
                    pattern_evidence={"coordination_pattern": "sequential_handoffs"},
                    integration_evidence={"agent_coordination": True, "prompt_generated": True},
                    concrete_evidence=current_task.get("evidence", {}),
                    files_modified=current_task.get("files_modified", []),
                    files_created=current_task.get("files_created", []),
                    tests_run=current_task.get("tests_run", []),
                )

                # Execute handoff
                handoff_result = await self.protocol.execute_handoff(handoff_id)

                handoff_results.append(
                    {
                        "from_agent": from_agent,
                        "to_agent": to_agent,
                        "handoff_id": handoff_id,
                        "evidence_count": len(current_task.get("evidence", [])),
                        "verification_passed": handoff_result.success,
                        "handoff_complete": handoff_result.success,
                        "agent_prompt": (
                            prompt[:200] + "..." if len(prompt) > 200 else prompt
                        ),  # Truncated for logging
                    }
                )

                # Update task with handoff results for next iteration
                current_task.update(
                    {
                        "previous_handoff": handoff_result.__dict__,
                        "evidence_trail": current_task.get("evidence", []),
                    }
                )

            except (VerificationRequired, StrictEnforcementViolation) as e:
                return {
                    "status": "verification_failed",
                    "failed_handoff": f"{from_agent} -> {to_agent}",
                    "error": str(e),
                    "handoff_results": handoff_results,
                }

        return {
            "status": "success",
            "coordination_method": "sequential_with_handoffs",
            "handoff_results": handoff_results,
            "total_handoffs": len(handoff_results),
            "verification_enforced": True,
            "agents_coordinated": agents,
        }

    async def _coordinate_parallel_validation(
        self, coordination_task: CoordinationTask
    ) -> Dict[str, Any]:
        """Coordinate parallel work with cross-validation."""

        agents = coordination_task.agents
        if len(agents) != 2:
            return {"status": "error", "message": "Parallel coordination requires exactly 2 agents"}

        # Generate agent-specific prompts based on capabilities
        agent_prompts = {}
        for agent in agents:
            agent_prompts[agent] = self._generate_agent_prompt(
                agent, coordination_task.task, coordination_task.evidence_requirements
            )

        # Execute parallel work (simulated - in real implementation would trigger actual agents)
        parallel_results = {
            "coordination_method": "parallel_with_cross_validation",
            "agents": agents,
            "agent_prompts": agent_prompts,
            "cross_validation_required": True,
            "evidence_requirements": coordination_task.evidence_requirements,
            "success_criteria": coordination_task.success_criteria,
            "coordination_initiated": datetime.now().isoformat(),
        }

        return {"status": "parallel_coordination_initiated", **parallel_results}

    async def _coordinate_review_based(self, coordination_task: CoordinationTask) -> Dict[str, Any]:
        """Coordinate review-based workflow."""

        if len(coordination_task.agents) < 2:
            return {"status": "error", "message": "Review coordination requires at least 2 agents"}

        reviewer = coordination_task.agents[-1]  # Last agent is reviewer
        implementers = coordination_task.agents[:-1]

        # Generate review-specific prompts
        review_prompts = {}
        for agent in implementers:
            review_prompts[agent] = self._generate_agent_prompt(
                agent, coordination_task.task, coordination_task.evidence_requirements
            )

        review_prompts[reviewer] = self._generate_review_prompt(
            reviewer, coordination_task.task, coordination_task.evidence_requirements
        )

        return {
            "status": "review_coordination_initiated",
            "coordination_method": "review_based",
            "implementers": implementers,
            "reviewer": reviewer,
            "review_prompts": review_prompts,
            "evidence_requirements": coordination_task.evidence_requirements,
            "success_criteria": coordination_task.success_criteria,
        }

    def _generate_agent_prompt(
        self, agent_id: str, task: Dict[str, Any], evidence_requirements: List[str]
    ) -> str:
        """Generate agent-specific prompt based on capabilities."""

        capabilities = self.agent_capabilities.get(agent_id)
        if not capabilities:
            # Unknown agent - use strict requirements
            return self._generate_strict_verification_prompt(task, evidence_requirements)

        if capabilities.context_level == "HIGH" and capabilities.methodology_awareness:
            return self._generate_high_context_prompt(task, evidence_requirements)
        elif capabilities.context_level == "LIMITED":
            return self._generate_limited_context_prompt(task, evidence_requirements, capabilities)
        else:
            return self._generate_strict_verification_prompt(task, evidence_requirements)

    def _generate_high_context_prompt(
        self, task: Dict[str, Any], evidence_requirements: List[str]
    ) -> str:
        """Generate prompt for high-context, methodology-aware agents."""
        return f"""SYSTEMATIC METHODOLOGY EXECUTION

Task: {task.get('description', 'Implementation required')}

You understand our Excellence Flywheel methodology. Execute systematically:

VERIFICATION FIRST (mandatory):
{self._format_verification_commands(evidence_requirements)}

EVIDENCE REQUIREMENTS:
{self._format_evidence_requirements(evidence_requirements)}

Apply systematic verification principles throughout execution.
No completion without concrete evidence.
Evidence must be provided in coordination handoff.
"""

    def _generate_limited_context_prompt(
        self,
        task: Dict[str, Any],
        evidence_requirements: List[str],
        capabilities: AgentCapabilities,
    ) -> str:
        """Generate detailed prompt for limited-context agents."""
        return f"""MANDATORY VERIFICATION REQUIRED

Task: {task.get('description', 'Implementation required')}

CRITICAL: You MUST follow these steps in order:

STEP 1: VERIFICATION COMMANDS (Execute these first):
{self._format_verification_commands(evidence_requirements)}

STOP CONDITIONS:
- If assuming configuration → STOP and verify
- If unclear setup → ASK rather than assume
- If method names uncertain → GREP before implementing

STEP 2: EVIDENCE COLLECTION:
{self._format_evidence_requirements(evidence_requirements)}

STEP 3: SYSTEMATIC IMPLEMENTATION:
- Check first, implement second
- Never assume what can be verified
- Provide terminal evidence for all claims

SUCCESS CRITERIA: Task complete with required evidence provided.
Evidence will be validated in mandatory handoff protocol.
"""

    def _generate_strict_verification_prompt(
        self, task: Dict[str, Any], evidence_requirements: List[str]
    ) -> str:
        """Generate strict verification prompt for unknown agents."""
        return f"""STRICT VERIFICATION PROTOCOL

Task: {task.get('description', 'Implementation required')}

MANDATORY REQUIREMENTS:
1. Execute verification commands BEFORE implementation
2. Provide concrete evidence for ALL claims
3. No assumptions - verify everything
4. Terminal output required for validation

VERIFICATION COMMANDS:
{self._format_verification_commands(evidence_requirements)}

EVIDENCE REQUIREMENTS:
{self._format_evidence_requirements(evidence_requirements)}

This is not optional. Progress blocked without verification.
All evidence will be validated through mandatory handoff protocol.
"""

    def _generate_review_prompt(
        self, agent_id: str, task: Dict[str, Any], evidence_requirements: List[str]
    ) -> str:
        """Generate review-specific prompt for reviewing agents."""
        return f"""SYSTEMATIC REVIEW PROTOCOL

Review Task: {task.get('description', 'Review required')}

Your role: Review and validate implementation evidence.

REVIEW REQUIREMENTS:
1. Verify all evidence meets requirements
2. Validate implementation against success criteria
3. Confirm methodology compliance
4. Provide specific feedback on gaps

EVIDENCE TO REVIEW:
{self._format_evidence_requirements(evidence_requirements)}

REVIEW CRITERIA:
- Evidence completeness and accuracy
- Implementation quality and methodology compliance
- Verification commands executed correctly
- Success criteria met

Provide detailed review with specific recommendations.
"""

    def _format_verification_commands(self, requirements: List[str]) -> str:
        """Format verification commands based on requirements."""
        commands = []
        for req in requirements:
            if req == "terminal_output":
                commands.append("# Verify implementation with terminal commands")
                commands.append("# Example: ls -la created_files/")
            elif req == "test_results":
                commands.append("PYTHONPATH=. python -m pytest relevant_tests/ -v --tb=short")
            elif req == "file_artifacts":
                commands.append("ls -la created_files/ && wc -l *.py")
            elif req == "explicit_verification":
                commands.append("# Run explicit verification commands")
                commands.append("# Verify configuration and setup")
        return "\n".join(commands)

    def _format_evidence_requirements(self, requirements: List[str]) -> str:
        """Format evidence requirements."""
        formatted = []
        for req in requirements:
            if req == "terminal_output":
                formatted.append("- Terminal command execution results")
            elif req == "test_results":
                formatted.append("- Test execution output with PASS/FAIL results")
            elif req == "file_artifacts":
                formatted.append("- File creation evidence with line counts")
            elif req == "explicit_verification":
                formatted.append("- Explicit verification command output")
            elif req == "cross_validation":
                formatted.append("- Cross-validation results between agents")
        return "\n".join(formatted)

    def get_coordination_statistics(self) -> Dict[str, Any]:
        """Get coordination statistics for monitoring."""
        total_coordinations = len(self.coordination_history)
        if total_coordinations == 0:
            return {
                "total_coordinations": 0,
                "successful_coordinations": 0,
                "blocked_coordinations": 0,
                "coordination_success_rate": 0.0,
                "average_coordination_time": 0.0,
                "registered_agents": len(self.agent_capabilities),
            }

        successful = sum(1 for c in self.coordination_history if c.get("status") == "success")
        blocked = sum(1 for c in self.coordination_history if "blocked" in c.get("status", ""))

        total_time = sum(c.get("coordination_duration", 0) for c in self.coordination_history)
        avg_time = total_time / total_coordinations if total_coordinations > 0 else 0

        return {
            "total_coordinations": total_coordinations,
            "successful_coordinations": successful,
            "blocked_coordinations": blocked,
            "failed_coordinations": total_coordinations - successful - blocked,
            "coordination_success_rate": (
                (successful / total_coordinations) * 100 if total_coordinations > 0 else 0
            ),
            "coordination_block_rate": (
                (blocked / total_coordinations) * 100 if total_coordinations > 0 else 0
            ),
            "average_coordination_time": avg_time,
            "registered_agents": len(self.agent_capabilities),
            "agent_types": [cap.agent_type.value for cap in self.agent_capabilities.values()],
        }

    def clear_coordination_history(self):
        """Clear coordination history - for testing purposes."""
        self.coordination_history.clear()
        print("🧹 Agent coordination history cleared")

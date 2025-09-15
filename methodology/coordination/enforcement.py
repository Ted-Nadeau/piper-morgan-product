"""
Enforcement Patterns for MandatoryHandoffProtocol.

Implements systematic enforcement patterns that make verification mandatory
with no escape routes, building on Phase 1 MandatoryHandoffProtocol foundation.
"""

import functools
import inspect
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from methodology.coordination.exceptions import HandoffBypassError, HandoffValidationError
from methodology.verification.pyramid import VerificationPyramid


class EnforcementLevel(Enum):
    """Enforcement strictness levels - no bypass options."""

    STRICT = "strict"  # Zero tolerance, block immediately
    PROGRESSIVE = "progressive"  # Escalating enforcement with consequences
    ADVISORY = "advisory"  # Log violations but proceed (lowest level)


@dataclass
class EnforcementRule:
    """Individual enforcement rule definition with concrete actions."""

    name: str
    description: str
    level: EnforcementLevel
    check_function: Callable
    violation_message: str
    resolution_steps: List[str]


class VerificationRequired(Exception):
    """Exception for mandatory verification requirements."""

    def __init__(self, message: str, resolution_steps: List[str] = None):
        super().__init__(message)
        self.resolution_steps = resolution_steps or []


class EnforcementPatterns:
    """
    Systematic enforcement patterns that make verification mandatory.
    No suggestions - these are requirements with consequences.
    """

    def __init__(self):
        self.pyramid = VerificationPyramid()
        self.enforcement_rules: List[EnforcementRule] = []
        self.violation_history: List[Dict[str, Any]] = []
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Setup default enforcement rules - no bypass possible."""

        # Rule 1: Mandatory evidence in all handoffs
        self.add_rule(
            EnforcementRule(
                name="mandatory_evidence",
                description="All handoffs must include concrete evidence",
                level=EnforcementLevel.STRICT,
                check_function=self._check_evidence_present,
                violation_message="Handoff blocked: No evidence provided",
                resolution_steps=[
                    "Add terminal output evidence to task",
                    "Include test results or validation proof",
                    "Provide concrete deliverable artifacts",
                    "Run verification pyramid on task before handoff",
                ],
            )
        )

        # Rule 2: Agent must acknowledge evidence receipt
        self.add_rule(
            EnforcementRule(
                name="evidence_acknowledgment",
                description="Receiving agent must explicitly acknowledge evidence review",
                level=EnforcementLevel.STRICT,
                check_function=self._check_evidence_reviewed,
                violation_message="Handoff blocked: Evidence not acknowledged",
                resolution_steps=[
                    "Review all evidence items provided",
                    "Confirm understanding of evidence content",
                    "Acknowledge evidence receipt explicitly",
                    "Proceed only after evidence validation",
                ],
            )
        )

        # Rule 3: No bypass through direct task assignment
        self.add_rule(
            EnforcementRule(
                name="no_direct_bypass",
                description="Tasks cannot bypass handoff protocol through direct assignment",
                level=EnforcementLevel.STRICT,
                check_function=self._check_handoff_protocol_used,
                violation_message="Handoff blocked: Direct assignment bypasses verification",
                resolution_steps=[
                    "Use MandatoryHandoffProtocol for all task transfers",
                    "Ensure verification pyramid validation complete",
                    "Create HandoffPackage with required evidence",
                    "Complete evidence review process",
                ],
            )
        )

        # Rule 4: Progressive verification requirements
        self.add_rule(
            EnforcementRule(
                name="verification_pyramid_complete",
                description="All three verification tiers must pass before handoff",
                level=EnforcementLevel.STRICT,
                check_function=self._check_verification_pyramid_complete,
                violation_message="Handoff blocked: Verification pyramid incomplete",
                resolution_steps=[
                    "Complete Pattern tier verification",
                    "Complete Integration tier verification",
                    "Complete Evidence tier verification",
                    "Ensure all tiers show passing status",
                ],
            )
        )

    def add_rule(self, rule: EnforcementRule):
        """Add custom enforcement rule - extends but never reduces enforcement."""
        self.enforcement_rules.append(rule)

    async def enforce_handoff_requirements(
        self, task: Dict[str, Any], from_agent: str, to_agent: str
    ) -> Dict[str, Any]:
        """
        Enforce all rules on handoff attempt.
        Returns enforcement result with violations and required actions.
        """

        enforcement_result = {
            "allowed": True,
            "violations": [],
            "required_actions": [],
            "enforcement_level": EnforcementLevel.ADVISORY,
            "handoff_blocked": False,
        }

        # Check all enforcement rules - no rule skipping allowed
        for rule in self.enforcement_rules:
            violation = await self._check_rule(rule, task, from_agent, to_agent)

            if violation:
                enforcement_result["violations"].append(
                    {
                        "rule": rule.name,
                        "message": rule.violation_message,
                        "level": rule.level,
                        "resolution_steps": rule.resolution_steps,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                # Escalate enforcement level if needed
                if rule.level == EnforcementLevel.STRICT:
                    enforcement_result["allowed"] = False
                    enforcement_result["handoff_blocked"] = True
                    enforcement_result["enforcement_level"] = EnforcementLevel.STRICT

                enforcement_result["required_actions"].extend(rule.resolution_steps)

        # Log violations for analysis and audit trail
        if enforcement_result["violations"]:
            self._log_enforcement_violation(task, from_agent, to_agent, enforcement_result)

        return enforcement_result

    async def _check_rule(
        self, rule: EnforcementRule, task: Dict[str, Any], from_agent: str, to_agent: str
    ) -> bool:
        """Check individual rule and return True if violated."""
        try:
            # Call the rule's check function
            if inspect.iscoroutinefunction(rule.check_function):
                return await rule.check_function(task, from_agent, to_agent)
            else:
                return rule.check_function(task, from_agent, to_agent)
        except Exception as e:
            # Rule check failed - assume violation for safety (fail-secure)
            print(f"⚠️ Rule check failed for {rule.name}: {e}")
            return True

    def _check_evidence_present(self, task: Dict[str, Any], from_agent: str, to_agent: str) -> bool:
        """Check if evidence is present in task."""
        evidence = task.get("evidence", [])
        return len(evidence) == 0  # Return True if violated (no evidence)

    def _check_evidence_reviewed(
        self, task: Dict[str, Any], from_agent: str, to_agent: str
    ) -> bool:
        """Check if evidence has been acknowledged."""
        return not task.get("evidence_acknowledged", False)  # Violated if not acknowledged

    def _check_handoff_protocol_used(
        self, task: Dict[str, Any], from_agent: str, to_agent: str
    ) -> bool:
        """Check if proper handoff protocol was used."""
        return not task.get("handoff_protocol_verified", False)  # Violated if not verified

    def _check_verification_pyramid_complete(
        self, task: Dict[str, Any], from_agent: str, to_agent: str
    ) -> bool:
        """Check if verification pyramid is complete."""
        verification_status = task.get("verification_pyramid", {})

        pattern_complete = verification_status.get("pattern_tier", False)
        integration_complete = verification_status.get("integration_tier", False)
        evidence_complete = verification_status.get("evidence_tier", False)

        # Violated if any tier incomplete
        return not (pattern_complete and integration_complete and evidence_complete)

    def _log_enforcement_violation(
        self,
        task: Dict[str, Any],
        from_agent: str,
        to_agent: str,
        enforcement_result: Dict[str, Any],
    ):
        """Log enforcement violations for analysis and audit trail."""
        violation_record = {
            "timestamp": datetime.now(),
            "from_agent": from_agent,
            "to_agent": to_agent,
            "task_type": task.get("type", "unknown"),
            "task_description": task.get("description", "No description"),
            "violations": enforcement_result["violations"],
            "enforcement_level": enforcement_result["enforcement_level"].value,
            "handoff_blocked": enforcement_result["handoff_blocked"],
        }
        self.violation_history.append(violation_record)

        # Print enforcement action for immediate visibility
        print(f"🚫 ENFORCEMENT ACTION: {len(enforcement_result['violations'])} violations detected")
        print(f"   From: {from_agent} → To: {to_agent}")
        print(f"   Task: {task.get('description', 'Unknown task')}")
        print(f"   Status: {'BLOCKED' if enforcement_result['handoff_blocked'] else 'WARNING'}")

    @staticmethod
    def mandatory_verification_decorator(func):
        """Decorator that enforces verification on any function - no bypass possible."""

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract task from arguments
            task = kwargs.get("task") or (args[0] if args else {})

            if not isinstance(task, dict):
                raise VerificationRequired(
                    "Task must be a dictionary with evidence",
                    resolution_steps=[
                        "Pass task as dictionary parameter",
                        "Include 'evidence' key with evidence list",
                        "Ensure task has proper structure",
                    ],
                )

            # Check for evidence - strict requirement
            if not task.get("evidence"):
                raise VerificationRequired(
                    "Function blocked: No evidence provided",
                    resolution_steps=[
                        "Add concrete evidence to task dictionary",
                        "Include 'evidence' key with list of evidence items",
                        "Run verification pyramid before function call",
                        "Ensure evidence includes terminal output or test results",
                    ],
                )

            # Check evidence quality
            evidence = task.get("evidence", [])
            if not isinstance(evidence, list) or not evidence:
                raise VerificationRequired(
                    "Function blocked: Evidence must be non-empty list",
                    resolution_steps=[
                        "Convert evidence to list format",
                        "Add at least one evidence item",
                        "Include specific evidence types: terminal, file, url",
                    ],
                )

            # Proceed with original function
            return await func(*args, **kwargs)

        return wrapper

    def generate_enforcement_prompt(self, violations: List[Dict]) -> str:
        """Generate enforcement prompt for agents with specific violations."""
        if not violations:
            return "✅ No enforcement violations detected. Proceed with task."

        prompt = "🚫 MANDATORY ENFORCEMENT REQUIREMENTS\n\n"
        prompt += f"Your handoff has been BLOCKED due to {len(violations)} violations:\n\n"

        for i, violation in enumerate(violations, 1):
            prompt += f"{i}. VIOLATION: {violation['message']}\n"
            prompt += f"   Rule: {violation['rule']}\n"
            prompt += f"   Level: {violation['level'].value.upper()}\n"
            prompt += "   Required Actions:\n"
            for step in violation["resolution_steps"]:
                prompt += f"   ✓ {step}\n"
            prompt += "\n"

        prompt += "⚠️  You MUST address ALL violations before proceeding.\n"
        prompt += "⚠️  This is not optional. The system will block progress without compliance.\n"
        prompt += "⚠️  No bypass methods exist. Complete all required actions.\n\n"

        prompt += "Once violations are resolved, retry the handoff operation.\n"

        return prompt

    def get_violation_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get enforcement violation history for analysis."""
        history = self.violation_history
        if limit:
            history = history[-limit:]
        return history

    def get_enforcement_statistics(self) -> Dict[str, Any]:
        """Get enforcement statistics for monitoring."""
        total_violations = len(self.violation_history)
        if total_violations == 0:
            return {
                "total_violations": 0,
                "blocked_handoffs": 0,
                "most_common_violation": None,
                "enforcement_effectiveness": 100.0,
            }

        blocked_count = sum(1 for v in self.violation_history if v["handoff_blocked"])

        # Count violation types
        violation_counts = {}
        for record in self.violation_history:
            for violation in record["violations"]:
                rule_name = violation["rule"]
                violation_counts[rule_name] = violation_counts.get(rule_name, 0) + 1

        most_common = (
            max(violation_counts.items(), key=lambda x: x[1]) if violation_counts else None
        )

        return {
            "total_violations": total_violations,
            "blocked_handoffs": blocked_count,
            "warning_handoffs": total_violations - blocked_count,
            "most_common_violation": most_common[0] if most_common else None,
            "violation_frequency": most_common[1] if most_common else 0,
            "enforcement_effectiveness": (
                (blocked_count / total_violations) * 100 if total_violations > 0 else 100.0
            ),
            "rules_active": len(self.enforcement_rules),
        }

    def clear_violation_history(self):
        """Clear violation history - for testing or reset purposes."""
        self.violation_history.clear()
        print("🧹 Enforcement violation history cleared")

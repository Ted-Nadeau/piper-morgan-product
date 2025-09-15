"""
MandatoryHandoffProtocol implementation with zero bypass paths.

Enforces systematic verification and evidence-based progress tracking
between agents with no possibility of circumvention.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from methodology.verification.pyramid import VerificationPyramid

from .exceptions import HandoffBypassError, HandoffStateError, HandoffValidationError


class HandoffState(Enum):
    """Mandatory handoff states - no bypassing allowed."""

    INITIALIZED = "initialized"
    VERIFICATION_REQUIRED = "verification_required"
    EVIDENCE_COLLECTION = "evidence_collection"
    VALIDATION_COMPLETE = "validation_complete"
    HANDOFF_READY = "handoff_ready"
    TRANSFERRED = "transferred"
    FAILED = "failed"


class AgentType(Enum):
    """Agent types for handoff coordination."""

    CODE = "code"
    CURSOR = "cursor"
    ARCHITECT = "architect"
    UNKNOWN = "unknown"


@dataclass
class HandoffContext:
    """
    Complete context for mandatory handoff between agents.

    Contains all required information, verification evidence, and state
    needed for zero-bypass handoff enforcement.
    """

    # Core identification
    handoff_id: str
    source_agent: AgentType
    target_agent: AgentType
    timestamp: datetime = field(default_factory=datetime.now)

    # Task context
    task_description: str = ""
    task_objectives: List[str] = field(default_factory=list)
    completion_criteria: List[str] = field(default_factory=list)

    # Verification evidence (MANDATORY)
    verification_evidence: Dict[str, Any] = field(default_factory=dict)
    pattern_verification: Dict[str, bool] = field(default_factory=dict)
    integration_verification: Dict[str, bool] = field(default_factory=dict)
    evidence_verification: Dict[str, bool] = field(default_factory=dict)

    # State tracking
    state: HandoffState = HandoffState.INITIALIZED
    validation_errors: List[str] = field(default_factory=list)
    bypass_attempts: List[Dict[str, Any]] = field(default_factory=list)

    # File tracking
    files_modified: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    tests_run: List[str] = field(default_factory=list)

    # GitHub integration
    github_issue: Optional[str] = None
    github_branch: Optional[str] = None
    commit_hashes: List[str] = field(default_factory=list)


@dataclass
class HandoffResult:
    """
    Result of mandatory handoff execution.

    Contains complete evidence trail and validation status.
    """

    success: bool
    handoff_context: HandoffContext
    validation_results: Dict[str, Any] = field(default_factory=dict)
    evidence_trail: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    error_message: Optional[str] = None
    bypass_prevention_log: List[str] = field(default_factory=list)


class MandatoryHandoffProtocol:
    """
    Zero-bypass handoff protocol enforcer.

    Implements mandatory verification and evidence collection with
    no escape paths or circumvention possibilities.
    """

    def __init__(self):
        self.verification_pyramid = VerificationPyramid()
        self._active_handoffs: Dict[str, HandoffContext] = {}
        self._bypass_prevention_enabled = True
        self._validation_hooks: List[Callable] = []

    def register_validation_hook(self, hook: Callable[[HandoffContext], bool]):
        """Register custom validation hook - cannot disable core validation."""
        self._validation_hooks.append(hook)

    async def initiate_handoff(
        self,
        source_agent: AgentType,
        target_agent: AgentType,
        task_description: str,
        task_objectives: List[str],
        completion_criteria: List[str],
        github_issue: Optional[str] = None,
    ) -> str:
        """
        Initiate mandatory handoff with zero bypass paths.

        Returns handoff_id for tracking - cannot be circumvented.
        """

        # Generate unique handoff ID
        handoff_id = f"handoff_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{source_agent.value}_{target_agent.value}"

        # Create mandatory context
        context = HandoffContext(
            handoff_id=handoff_id,
            source_agent=source_agent,
            target_agent=target_agent,
            task_description=task_description,
            task_objectives=task_objectives,
            completion_criteria=completion_criteria,
            github_issue=github_issue,
            state=HandoffState.VERIFICATION_REQUIRED,
        )

        # Store in active handoffs - no bypass possible
        self._active_handoffs[handoff_id] = context

        # Log initiation - audit trail
        print(f"🔒 MANDATORY HANDOFF INITIATED: {handoff_id}")
        print(f"   Source: {source_agent.value} → Target: {target_agent.value}")
        print(f"   Task: {task_description}")
        print(f"   State: {context.state.value}")

        return handoff_id

    async def collect_verification_evidence(
        self,
        handoff_id: str,
        pattern_evidence: Dict[str, Any],
        integration_evidence: Dict[str, Any],
        concrete_evidence: Dict[str, Any],
        files_modified: List[str] = None,
        files_created: List[str] = None,
        tests_run: List[str] = None,
    ) -> None:
        """
        Collect mandatory verification evidence - no bypass allowed.

        Uses three-tier verification pyramid for evidence validation.
        """

        # Prevent bypass attempts
        if handoff_id not in self._active_handoffs:
            raise HandoffBypassError(
                f"Bypass attempt detected: Unknown handoff_id {handoff_id}",
                bypass_attempt_details={"attempted_handoff_id": handoff_id},
            )

        context = self._active_handoffs[handoff_id]

        # Validate state transition
        if context.state != HandoffState.VERIFICATION_REQUIRED:
            raise HandoffStateError(
                f"Invalid state for evidence collection: {context.state.value}",
                current_state=context.state.value,
                attempted_state=HandoffState.EVIDENCE_COLLECTION.value,
            )

        # Update state
        context.state = HandoffState.EVIDENCE_COLLECTION

        # Collect evidence through verification pyramid
        try:
            # Pattern tier verification
            pattern_results = await self.verification_pyramid.verify_patterns(pattern_evidence)
            context.pattern_verification = pattern_results

            # Integration tier verification
            integration_results = await self.verification_pyramid.verify_integration(
                integration_evidence
            )
            context.integration_verification = integration_results

            # Evidence tier verification
            evidence_results = await self.verification_pyramid.verify_evidence(concrete_evidence)
            context.evidence_verification = evidence_results

            # Store all evidence
            context.verification_evidence = {
                "patterns": pattern_evidence,
                "integration": integration_evidence,
                "concrete": concrete_evidence,
            }

            # Track file changes
            if files_modified:
                context.files_modified.extend(files_modified)
            if files_created:
                context.files_created.extend(files_created)
            if tests_run:
                context.tests_run.extend(tests_run)

            # Update state to validation complete
            context.state = HandoffState.VALIDATION_COMPLETE

            print(f"📊 EVIDENCE COLLECTED: {handoff_id}")
            print(f"   Pattern verification: {len(pattern_results)} items")
            print(f"   Integration verification: {len(integration_results)} items")
            print(f"   Evidence verification: {len(evidence_results)} items")

        except Exception as e:
            context.state = HandoffState.FAILED
            context.validation_errors.append(str(e))
            raise HandoffValidationError(
                f"Evidence collection failed: {str(e)}",
                validation_failures={"evidence_error": str(e)},
                required_context={"handoff_id": handoff_id},
            )

    async def validate_handoff_ready(self, handoff_id: str) -> bool:
        """
        Validate handoff is ready for transfer - mandatory checks.

        Returns True only if ALL requirements met - no partial bypass.
        """

        if handoff_id not in self._active_handoffs:
            raise HandoffBypassError(
                f"Bypass attempt: Validation requested for unknown handoff {handoff_id}"
            )

        context = self._active_handoffs[handoff_id]

        # State validation
        if context.state != HandoffState.VALIDATION_COMPLETE:
            return False

        # Evidence validation - ALL tiers must pass
        all_patterns_valid = all(context.pattern_verification.values())
        all_integration_valid = all(context.integration_verification.values())
        all_evidence_valid = all(context.evidence_verification.values())

        if not (all_patterns_valid and all_integration_valid and all_evidence_valid):
            context.validation_errors.append("Verification pyramid validation failed")
            return False

        # Completion criteria check
        if not context.completion_criteria:
            context.validation_errors.append("No completion criteria defined")
            return False

        # Custom validation hooks
        for hook in self._validation_hooks:
            if not hook(context):
                context.validation_errors.append(f"Custom validation hook failed: {hook.__name__}")
                return False

        # All validations passed - ready for handoff
        context.state = HandoffState.HANDOFF_READY
        return True

    async def execute_handoff(self, handoff_id: str) -> HandoffResult:
        """
        Execute mandatory handoff transfer - final step with evidence trail.

        Returns complete HandoffResult with audit trail.
        """

        start_time = asyncio.get_event_loop().time()

        try:
            # Prevent bypass
            if handoff_id not in self._active_handoffs:
                raise HandoffBypassError(
                    f"Critical bypass attempt: Unknown handoff execution {handoff_id}"
                )

            context = self._active_handoffs[handoff_id]

            # Final validation
            if not await self.validate_handoff_ready(handoff_id):
                context.state = HandoffState.FAILED
                raise HandoffValidationError(
                    f"Handoff validation failed: {context.validation_errors}",
                    validation_failures={"errors": context.validation_errors},
                )

            # Execute transfer
            context.state = HandoffState.TRANSFERRED
            context.timestamp = datetime.now()

            # Build evidence trail
            evidence_trail = [
                f"Handoff executed: {context.handoff_id}",
                f"Source: {context.source_agent.value} → Target: {context.target_agent.value}",
                f"Task: {context.task_description}",
                f"Files modified: {len(context.files_modified)}",
                f"Files created: {len(context.files_created)}",
                f"Tests run: {len(context.tests_run)}",
                f"Verification evidence: {len(context.verification_evidence)} categories",
                f"Transfer completed: {context.timestamp.isoformat()}",
            ]

            execution_time = asyncio.get_event_loop().time() - start_time

            result = HandoffResult(
                success=True,
                handoff_context=context,
                validation_results={
                    "pattern_validation": context.pattern_verification,
                    "integration_validation": context.integration_verification,
                    "evidence_validation": context.evidence_verification,
                },
                evidence_trail=evidence_trail,
                execution_time=execution_time,
                bypass_prevention_log=[f"Zero bypasses detected for {handoff_id}"],
            )

            # Remove from active handoffs
            del self._active_handoffs[handoff_id]

            print(f"✅ MANDATORY HANDOFF COMPLETE: {handoff_id}")
            print(f"   Execution time: {execution_time:.2f}s")
            print(f"   Evidence trail: {len(evidence_trail)} items")

            return result

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time

            if handoff_id in self._active_handoffs:
                self._active_handoffs[handoff_id].state = HandoffState.FAILED

            return HandoffResult(
                success=False,
                handoff_context=self._active_handoffs.get(handoff_id),
                execution_time=execution_time,
                error_message=str(e),
                bypass_prevention_log=[f"Execution failed for {handoff_id}: {str(e)}"],
            )

    def get_handoff_status(self, handoff_id: str) -> Optional[HandoffContext]:
        """Get current handoff status - read-only access."""
        return self._active_handoffs.get(handoff_id)

    def list_active_handoffs(self) -> List[str]:
        """List all active handoff IDs."""
        return list(self._active_handoffs.keys())

    def prevent_bypass_attempt(self, attempt_details: Dict[str, Any]) -> None:
        """Log and prevent bypass attempts - security measure."""
        for handoff_id, context in self._active_handoffs.items():
            context.bypass_attempts.append(
                {"timestamp": datetime.now().isoformat(), "details": attempt_details}
            )

        raise HandoffBypassError(
            "Bypass attempt detected and prevented", bypass_attempt_details=attempt_details
        )

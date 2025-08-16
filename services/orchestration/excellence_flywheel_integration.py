"""
Excellence Flywheel Integration

PM-033d Phase 4: Systematic verification integration into coordination flows
following the Excellence Flywheel methodology for compound learning and acceleration.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import structlog

from services.domain.models import Intent
from services.orchestration.multi_agent_coordinator import (
    CoordinationResult,
    CoordinationStatus,
    MultiAgentCoordinator,
    SubTask,
)

logger = structlog.get_logger()


class VerificationPhase(Enum):
    """Excellence Flywheel verification phases"""

    PRE_COORDINATION = "pre_coordination"
    TASK_DECOMPOSITION = "task_decomposition"
    AGENT_ASSIGNMENT = "agent_assignment"
    POST_COORDINATION = "post_coordination"
    LEARNING_CAPTURE = "learning_capture"


class VerificationResult(Enum):
    """Verification results"""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass
class VerificationCheck:
    """Individual verification check"""

    check_id: str
    phase: VerificationPhase
    description: str
    result: VerificationResult
    details: str
    evidence: Dict[str, Any]
    duration_ms: int
    created_at: datetime


@dataclass
class ExcellenceFlywheel:
    """Excellence Flywheel verification tracking"""

    coordination_id: str
    verification_checks: List[VerificationCheck]
    learning_insights: List[str]
    patterns_detected: Dict[str, Any]
    acceleration_metrics: Dict[str, float]
    compound_knowledge: Dict[str, Any]
    systematic_verified: bool


class ExcellenceFlywheelIntegrator:
    """
    Integrates Excellence Flywheel methodology into coordination flows

    Ensures systematic verification at all phases:
    1. Verify First, Implement Second
    2. Pattern Detection and Learning
    3. Compound Knowledge Acceleration
    4. Systematic Quality Assurance
    """

    def __init__(self):
        self.coordinator = MultiAgentCoordinator()
        self.flywheel_history: Dict[str, ExcellenceFlywheel] = {}
        self.pattern_library: Dict[str, Dict[str, Any]] = {}
        self.acceleration_metrics: Dict[str, float] = {
            "avg_coordination_time_ms": 0.0,
            "verification_success_rate": 1.0,
            "pattern_reuse_rate": 0.0,
            "learning_acceleration_factor": 1.0,
        }

    async def coordinate_with_excellence_flywheel(
        self, intent: Intent, context: Optional[Dict[str, Any]] = None
    ) -> Tuple[CoordinationResult, ExcellenceFlywheel]:
        """
        Execute coordination with full Excellence Flywheel integration

        Args:
            intent: Intent to coordinate
            context: Optional coordination context

        Returns:
            Tuple of (CoordinationResult, ExcellenceFlywheel)
        """
        coordination_start = time.time()

        logger.info(
            "Starting Excellence Flywheel coordination", intent_id=intent.id, action=intent.action
        )

        # Initialize flywheel tracking
        flywheel = ExcellenceFlywheel(
            coordination_id=f"flywheel_{intent.id}_{int(time.time() * 1000)}",
            verification_checks=[],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )

        try:
            # Phase 1: Pre-Coordination Verification
            await self._verify_pre_coordination(intent, flywheel, context)

            # Phase 2: Execute Coordination with Verification
            coordination_result = await self._execute_verified_coordination(
                intent, flywheel, context
            )

            # Phase 3: Post-Coordination Verification
            await self._verify_post_coordination(coordination_result, flywheel)

            # Phase 4: Learning Capture and Pattern Detection
            await self._capture_learning_and_patterns(intent, coordination_result, flywheel)

            # Phase 5: Update Acceleration Metrics
            await self._update_acceleration_metrics(flywheel, time.time() - coordination_start)

            # Mark as systematically verified
            flywheel.systematic_verified = all(
                check.result in [VerificationResult.PASSED, VerificationResult.WARNING]
                for check in flywheel.verification_checks
            )

            self.flywheel_history[flywheel.coordination_id] = flywheel

            logger.info(
                "Excellence Flywheel coordination completed",
                coordination_id=flywheel.coordination_id,
                systematic_verified=flywheel.systematic_verified,
                checks_passed=sum(
                    1 for c in flywheel.verification_checks if c.result == VerificationResult.PASSED
                ),
                total_checks=len(flywheel.verification_checks),
            )

            return coordination_result, flywheel

        except Exception as e:
            # Add error verification check
            error_check = VerificationCheck(
                check_id="coordination_error",
                phase=VerificationPhase.POST_COORDINATION,
                description="Coordination error handling",
                result=VerificationResult.FAILED,
                details=f"Coordination failed: {str(e)}",
                evidence={"error_type": type(e).__name__, "error_message": str(e)},
                duration_ms=int((time.time() - coordination_start) * 1000),
                created_at=datetime.now(),
            )
            flywheel.verification_checks.append(error_check)

            logger.error(
                "Excellence Flywheel coordination failed",
                coordination_id=flywheel.coordination_id,
                error=str(e),
            )

            # Return failed coordination result
            failed_result = CoordinationResult(
                coordination_id=flywheel.coordination_id,
                status=CoordinationStatus.FAILED,
                subtasks=[],
                total_duration_ms=int((time.time() - coordination_start) * 1000),
                success_rate=0.0,
                error_details=e,
                agent_performance={},
            )

            return failed_result, flywheel

    async def _verify_pre_coordination(
        self, intent: Intent, flywheel: ExcellenceFlywheel, context: Optional[Dict[str, Any]]
    ):
        """Phase 1: Pre-coordination verification checks"""

        check_start = time.time()

        # Check 1: Intent Validation
        intent_check = await self._verify_intent_structure(intent)
        intent_check.phase = VerificationPhase.PRE_COORDINATION
        intent_check.duration_ms = int((time.time() - check_start) * 1000)
        flywheel.verification_checks.append(intent_check)

        # Check 2: Pattern Library Search
        pattern_check = await self._verify_pattern_availability(intent)
        pattern_check.phase = VerificationPhase.PRE_COORDINATION
        pattern_check.duration_ms = int((time.time() - check_start) * 1000)
        flywheel.verification_checks.append(pattern_check)

        # Check 3: Context Validation
        context_check = await self._verify_context_adequacy(context)
        context_check.phase = VerificationPhase.PRE_COORDINATION
        context_check.duration_ms = int((time.time() - check_start) * 1000)
        flywheel.verification_checks.append(context_check)

    async def _execute_verified_coordination(
        self, intent: Intent, flywheel: ExcellenceFlywheel, context: Optional[Dict[str, Any]]
    ) -> CoordinationResult:
        """Execute coordination with verification at each step"""

        coordination_start = time.time()

        # Execute coordination
        result = await self.coordinator.coordinate_task(intent, context or {})

        # Verify task decomposition
        decomposition_check = await self._verify_task_decomposition(result)
        decomposition_check.phase = VerificationPhase.TASK_DECOMPOSITION
        decomposition_check.duration_ms = int((time.time() - coordination_start) * 1000)
        flywheel.verification_checks.append(decomposition_check)

        # Verify agent assignments
        assignment_check = await self._verify_agent_assignments(result)
        assignment_check.phase = VerificationPhase.AGENT_ASSIGNMENT
        assignment_check.duration_ms = int((time.time() - coordination_start) * 1000)
        flywheel.verification_checks.append(assignment_check)

        return result

    async def _verify_post_coordination(
        self, result: CoordinationResult, flywheel: ExcellenceFlywheel
    ):
        """Phase 3: Post-coordination verification"""

        check_start = time.time()

        # Check 1: Performance Target Verification
        performance_check = await self._verify_performance_targets(result)
        performance_check.phase = VerificationPhase.POST_COORDINATION
        performance_check.duration_ms = int((time.time() - check_start) * 1000)
        flywheel.verification_checks.append(performance_check)

        # Check 2: Quality Standards Verification
        quality_check = await self._verify_coordination_quality(result)
        quality_check.phase = VerificationPhase.POST_COORDINATION
        quality_check.duration_ms = int((time.time() - check_start) * 1000)
        flywheel.verification_checks.append(quality_check)

        # Check 3: Success Rate Verification
        success_check = await self._verify_success_metrics(result)
        success_check.phase = VerificationPhase.POST_COORDINATION
        success_check.duration_ms = int((time.time() - check_start) * 1000)
        flywheel.verification_checks.append(success_check)

    async def _capture_learning_and_patterns(
        self, intent: Intent, result: CoordinationResult, flywheel: ExcellenceFlywheel
    ):
        """Phase 4: Capture learning insights and pattern detection"""

        # Detect patterns in coordination
        patterns = await self._detect_coordination_patterns(intent, result)
        flywheel.patterns_detected.update(patterns)

        # Generate learning insights
        insights = await self._generate_learning_insights(intent, result, flywheel)
        flywheel.learning_insights.extend(insights)

        # Update pattern library
        await self._update_pattern_library(intent, result, patterns)

        # Learning capture verification
        learning_check = VerificationCheck(
            check_id="learning_capture",
            phase=VerificationPhase.LEARNING_CAPTURE,
            description="Learning and pattern capture",
            result=VerificationResult.PASSED if len(insights) > 0 else VerificationResult.WARNING,
            details=f"Captured {len(insights)} insights and {len(patterns)} patterns",
            evidence={"insights_count": len(insights), "patterns_count": len(patterns)},
            duration_ms=0,
            created_at=datetime.now(),
        )
        flywheel.verification_checks.append(learning_check)

    async def _update_acceleration_metrics(
        self, flywheel: ExcellenceFlywheel, total_duration_s: float
    ):
        """Phase 5: Update acceleration metrics for compound learning"""

        # Calculate new metrics
        coordination_time_ms = total_duration_s * 1000
        verification_success_rate = len(
            [c for c in flywheel.verification_checks if c.result == VerificationResult.PASSED]
        ) / len(flywheel.verification_checks)

        # Update running averages
        alpha = 0.1  # Learning rate
        self.acceleration_metrics["avg_coordination_time_ms"] = (
            1 - alpha
        ) * self.acceleration_metrics["avg_coordination_time_ms"] + alpha * coordination_time_ms

        self.acceleration_metrics["verification_success_rate"] = (
            1 - alpha
        ) * self.acceleration_metrics[
            "verification_success_rate"
        ] + alpha * verification_success_rate

        # Calculate acceleration factor (improvement over baseline)
        baseline_time_ms = 1000  # 1 second baseline
        if coordination_time_ms > 0:
            time_acceleration = baseline_time_ms / coordination_time_ms
            self.acceleration_metrics["learning_acceleration_factor"] = max(1.0, time_acceleration)

        flywheel.acceleration_metrics = self.acceleration_metrics.copy()

    # Verification check implementations
    async def _verify_intent_structure(self, intent: Intent) -> VerificationCheck:
        """Verify intent has proper structure"""

        issues = []
        if not intent.action:
            issues.append("Missing action")
        if not intent.original_message:
            issues.append("Missing original message")
        if intent.confidence <= 0:
            issues.append("Invalid confidence score")

        result = VerificationResult.PASSED if len(issues) == 0 else VerificationResult.FAILED

        return VerificationCheck(
            check_id="intent_structure",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Intent structure validation",
            result=result,
            details=f"Intent validation: {', '.join(issues) if issues else 'All checks passed'}",
            evidence={"issues": issues, "action": intent.action, "confidence": intent.confidence},
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _verify_pattern_availability(self, intent: Intent) -> VerificationCheck:
        """Check for existing patterns in pattern library"""

        # Search for similar patterns
        similar_patterns = []
        for pattern_key, pattern_data in self.pattern_library.items():
            if intent.action in pattern_key or any(
                word in pattern_key for word in intent.action.split("_")
            ):
                similar_patterns.append(pattern_key)

        pattern_reuse_rate = len(similar_patterns) / max(1, len(self.pattern_library))
        self.acceleration_metrics["pattern_reuse_rate"] = pattern_reuse_rate

        result = (
            VerificationResult.PASSED if len(similar_patterns) > 0 else VerificationResult.WARNING
        )

        return VerificationCheck(
            check_id="pattern_availability",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Pattern library search",
            result=result,
            details=f"Found {len(similar_patterns)} similar patterns for reuse",
            evidence={"similar_patterns": similar_patterns, "reuse_rate": pattern_reuse_rate},
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _verify_context_adequacy(
        self, context: Optional[Dict[str, Any]]
    ) -> VerificationCheck:
        """Verify context provides adequate information"""

        if context is None:
            context = {}

        adequacy_score = min(1.0, len(context) / 3)  # 3+ context items is ideal
        result = VerificationResult.PASSED if adequacy_score >= 0.5 else VerificationResult.WARNING

        return VerificationCheck(
            check_id="context_adequacy",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Context adequacy assessment",
            result=result,
            details=f"Context adequacy score: {adequacy_score:.2f}",
            evidence={"context_items": len(context), "adequacy_score": adequacy_score},
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _verify_task_decomposition(self, result: CoordinationResult) -> VerificationCheck:
        """Verify task decomposition quality"""

        subtask_count = len(result.subtasks)

        # Optimal decomposition: 2-5 subtasks for most coordination
        if 2 <= subtask_count <= 5:
            decomposition_result = VerificationResult.PASSED
            details = f"Optimal decomposition: {subtask_count} subtasks"
        elif subtask_count == 1:
            decomposition_result = VerificationResult.WARNING
            details = f"Simple task: {subtask_count} subtask (may be optimal for simple intents)"
        elif subtask_count > 5:
            decomposition_result = VerificationResult.WARNING
            details = f"Complex decomposition: {subtask_count} subtasks (may be over-decomposed)"
        else:
            decomposition_result = VerificationResult.FAILED
            details = f"No task decomposition: {subtask_count} subtasks"

        return VerificationCheck(
            check_id="task_decomposition",
            phase=VerificationPhase.TASK_DECOMPOSITION,
            description="Task decomposition quality",
            result=decomposition_result,
            details=details,
            evidence={
                "subtask_count": subtask_count,
                "subtasks": [str(t) for t in result.subtasks],
            },
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _verify_agent_assignments(self, result: CoordinationResult) -> VerificationCheck:
        """Verify agent assignments are appropriate"""

        if not result.subtasks:
            return VerificationCheck(
                check_id="agent_assignments",
                phase=VerificationPhase.AGENT_ASSIGNMENT,
                description="Agent assignment verification",
                result=VerificationResult.WARNING,
                details="No subtasks to assign",
                evidence={},
                duration_ms=0,
                created_at=datetime.now(),
            )

        # Count agent assignments
        agent_assignments = {}
        for subtask in result.subtasks:
            agent = getattr(subtask, "assigned_agent", "UNKNOWN")
            agent_assignments[str(agent)] = agent_assignments.get(str(agent), 0) + 1

        # Verify multi-agent utilization for complex tasks
        uses_multiple_agents = len(agent_assignments) > 1
        result_status = (
            VerificationResult.PASSED
            if uses_multiple_agents or len(result.subtasks) == 1
            else VerificationResult.WARNING
        )

        return VerificationCheck(
            check_id="agent_assignments",
            phase=VerificationPhase.AGENT_ASSIGNMENT,
            description="Agent assignment verification",
            result=result_status,
            details=f"Agent utilization: {dict(agent_assignments)}",
            evidence={
                "agent_assignments": agent_assignments,
                "uses_multiple_agents": uses_multiple_agents,
            },
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _verify_performance_targets(self, result: CoordinationResult) -> VerificationCheck:
        """Verify performance targets are met"""

        target_ms = 1000  # 1 second target
        meets_target = result.total_duration_ms <= target_ms

        result_status = VerificationResult.PASSED if meets_target else VerificationResult.WARNING

        return VerificationCheck(
            check_id="performance_targets",
            phase=VerificationPhase.POST_COORDINATION,
            description="Performance target verification",
            result=result_status,
            details=f"Coordination time: {result.total_duration_ms}ms (target: {target_ms}ms)",
            evidence={
                "duration_ms": result.total_duration_ms,
                "target_ms": target_ms,
                "meets_target": meets_target,
            },
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _verify_coordination_quality(self, result: CoordinationResult) -> VerificationCheck:
        """Verify overall coordination quality"""

        quality_factors = []

        # Factor 1: Status success
        if result.status == CoordinationStatus.ASSIGNED:
            quality_factors.append(0.4)  # 40% weight
        else:
            quality_factors.append(0.0)

        # Factor 2: Success rate
        quality_factors.append(result.success_rate * 0.3)  # 30% weight

        # Factor 3: Performance
        performance_score = min(1.0, 1000 / max(1, result.total_duration_ms))
        quality_factors.append(performance_score * 0.3)  # 30% weight

        overall_quality = sum(quality_factors)

        if overall_quality >= 0.8:
            quality_result = VerificationResult.PASSED
        elif overall_quality >= 0.6:
            quality_result = VerificationResult.WARNING
        else:
            quality_result = VerificationResult.FAILED

        return VerificationCheck(
            check_id="coordination_quality",
            phase=VerificationPhase.POST_COORDINATION,
            description="Overall coordination quality",
            result=quality_result,
            details=f"Quality score: {overall_quality:.2f}",
            evidence={"quality_score": overall_quality, "factors": quality_factors},
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _verify_success_metrics(self, result: CoordinationResult) -> VerificationCheck:
        """Verify success metrics meet standards"""

        success_threshold = 0.9  # 90% success rate threshold
        meets_threshold = result.success_rate >= success_threshold

        result_status = VerificationResult.PASSED if meets_threshold else VerificationResult.WARNING

        return VerificationCheck(
            check_id="success_metrics",
            phase=VerificationPhase.POST_COORDINATION,
            description="Success metrics verification",
            result=result_status,
            details=f"Success rate: {result.success_rate:.2f} (threshold: {success_threshold})",
            evidence={
                "success_rate": result.success_rate,
                "threshold": success_threshold,
                "meets_threshold": meets_threshold,
            },
            duration_ms=0,
            created_at=datetime.now(),
        )

    async def _detect_coordination_patterns(
        self, intent: Intent, result: CoordinationResult
    ) -> Dict[str, Any]:
        """Detect patterns in coordination for learning"""

        patterns = {
            "action_pattern": intent.action,
            "subtask_pattern": len(result.subtasks),
            "performance_pattern": "fast" if result.total_duration_ms < 500 else "normal",
            "success_pattern": "high" if result.success_rate >= 0.9 else "standard",
            "complexity_pattern": "simple" if len(result.subtasks) <= 2 else "complex",
        }

        return patterns

    async def _generate_learning_insights(
        self, intent: Intent, result: CoordinationResult, flywheel: ExcellenceFlywheel
    ) -> List[str]:
        """Generate learning insights from coordination"""

        insights = []

        # Performance insights
        if result.total_duration_ms < 100:
            insights.append("Exceptional coordination speed achieved - pattern suitable for reuse")

        # Quality insights
        if result.success_rate == 1.0:
            insights.append("Perfect success rate - coordination pattern is highly reliable")

        # Verification insights
        passed_checks = len(
            [c for c in flywheel.verification_checks if c.result == VerificationResult.PASSED]
        )
        if passed_checks == len(flywheel.verification_checks):
            insights.append("All verification checks passed - systematic excellence achieved")

        # Pattern insights
        if len(result.subtasks) in [2, 3, 4]:
            insights.append("Optimal task decomposition pattern detected")

        return insights

    async def _update_pattern_library(
        self, intent: Intent, result: CoordinationResult, patterns: Dict[str, Any]
    ):
        """Update pattern library with new coordination patterns"""

        pattern_key = f"{intent.action}_{patterns['complexity_pattern']}"

        pattern_data = {
            "action": intent.action,
            "subtask_count": len(result.subtasks),
            "performance_ms": result.total_duration_ms,
            "success_rate": result.success_rate,
            "usage_count": self.pattern_library.get(pattern_key, {}).get("usage_count", 0) + 1,
            "last_used": datetime.now().isoformat(),
        }

        self.pattern_library[pattern_key] = pattern_data

    async def get_flywheel_analytics(self) -> Dict[str, Any]:
        """Get analytics across all Excellence Flywheel coordinations"""

        if not self.flywheel_history:
            return {"total_coordinations": 0, "no_data": True}

        flywheels = list(self.flywheel_history.values())

        analytics = {
            "total_coordinations": len(flywheels),
            "systematic_verification_rate": len([f for f in flywheels if f.systematic_verified])
            / len(flywheels),
            "avg_verification_checks": sum(len(f.verification_checks) for f in flywheels)
            / len(flywheels),
            "pattern_library_size": len(self.pattern_library),
            "acceleration_metrics": self.acceleration_metrics.copy(),
            "common_learning_insights": {},
            "verification_success_by_phase": {},
        }

        # Aggregate learning insights
        all_insights = []
        for f in flywheels:
            all_insights.extend(f.learning_insights)

        # Count common insights
        insight_counts = {}
        for insight in all_insights:
            insight_counts[insight] = insight_counts.get(insight, 0) + 1

        analytics["common_learning_insights"] = dict(
            sorted(insight_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        )

        # Verification success by phase
        phase_stats = {}
        for f in flywheels:
            for check in f.verification_checks:
                phase = check.phase.value
                if phase not in phase_stats:
                    phase_stats[phase] = {"passed": 0, "total": 0}

                phase_stats[phase]["total"] += 1
                if check.result == VerificationResult.PASSED:
                    phase_stats[phase]["passed"] += 1

        for phase, stats in phase_stats.items():
            analytics["verification_success_by_phase"][phase] = (
                stats["passed"] / stats["total"] if stats["total"] > 0 else 0
            )

        return analytics


# Integration function for Phase 4 testing
async def run_excellence_flywheel_validation() -> Dict[str, Any]:
    """Run Excellence Flywheel validation for PM-033d Phase 4"""

    print("🔄 EXCELLENCE FLYWHEEL INTEGRATION VALIDATION")
    print("=" * 60)

    integrator = ExcellenceFlywheelIntegrator()

    # Test intents with different complexities
    test_intents = [
        Intent(
            category=Intent.category if hasattr(Intent, "category") else None,
            action="implement_api_endpoint",
            original_message="Implement REST API endpoint for user profile management with validation",
            confidence=0.94,
        ),
        Intent(
            category=Intent.category if hasattr(Intent, "category") else None,
            action="refactor_database_schema",
            original_message="Refactor database schema with migration scripts and comprehensive testing",
            confidence=0.96,
        ),
    ]

    results = []

    for i, intent in enumerate(test_intents, 1):
        print(f"\n🧪 Excellence Flywheel Test {i}: {intent.action}")

        coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(intent)
        results.append((coordination_result, flywheel))

        print(f"   ✅ Coordination Status: {coordination_result.status.value}")
        print(f"   🔍 Systematic Verified: {flywheel.systematic_verified}")
        print(f"   📊 Verification Checks: {len(flywheel.verification_checks)}")

        passed_checks = len(
            [c for c in flywheel.verification_checks if c.result == VerificationResult.PASSED]
        )
        print(f"   ✓ Checks Passed: {passed_checks}/{len(flywheel.verification_checks)}")
        print(f"   📈 Learning Insights: {len(flywheel.learning_insights)}")
        print(f"   🎯 Patterns Detected: {len(flywheel.patterns_detected)}")

        # Show verification phases
        phase_summary = {}
        for check in flywheel.verification_checks:
            phase = check.phase.value
            phase_summary[phase] = phase_summary.get(phase, 0) + 1

        print(f"   📋 Verification Phases: {dict(phase_summary)}")

    # Get analytics
    analytics = await integrator.get_flywheel_analytics()

    print(f"\n📊 EXCELLENCE FLYWHEEL ANALYTICS:")
    print(f'   Total Coordinations: {analytics["total_coordinations"]}')
    print(f'   Systematic Verification Rate: {analytics["systematic_verification_rate"]*100:.1f}%')
    print(f'   Avg Verification Checks: {analytics["avg_verification_checks"]:.1f}')
    print(f'   Pattern Library Size: {analytics["pattern_library_size"]}')
    print(
        f'   Learning Acceleration Factor: {analytics["acceleration_metrics"]["learning_acceleration_factor"]:.2f}x'
    )

    # Validation criteria
    validation_success = (
        analytics["systematic_verification_rate"] >= 0.8  # 80% systematic verification
        and analytics["avg_verification_checks"] >= 5  # At least 5 checks per coordination
        and analytics["pattern_library_size"] > 0  # Pattern learning working
        and all(
            r[0].status == CoordinationStatus.ASSIGNED for r in results
        )  # All coordinations successful
    )

    print(
        f'\n🎯 EXCELLENCE FLYWHEEL VALIDATION: {"✅ PASSED" if validation_success else "❌ FAILED"}'
    )

    return {
        "validation_success": validation_success,
        "analytics": analytics,
        "coordination_results": [coord_result.status.value for coord_result, flywheel in results],
        "flywheel_verification_rates": [
            flywheel.systematic_verified for coord_result, flywheel in results
        ],
    }


if __name__ == "__main__":
    # Run Excellence Flywheel validation directly
    import asyncio

    from services.shared_types import IntentCategory

    result = asyncio.run(run_excellence_flywheel_validation())
    print(f"\nExcellence Flywheel validation completed: {result['validation_success']}")

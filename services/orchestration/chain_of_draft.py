"""
Chain-of-Draft Implementation

PM-033d Phase 4: Simple 2-draft experiment system for iterative improvement
of multi-agent coordination results through systematic comparison and learning.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.domain.models import Intent
from services.orchestration.multi_agent_coordinator import (
    CoordinationResult,
    CoordinationStatus,
    MultiAgentCoordinator,
    SubTask,
)

logger = structlog.get_logger()


class DraftQuality(Enum):
    """Draft quality assessment levels"""

    POOR = "poor"
    ACCEPTABLE = "acceptable"
    GOOD = "good"
    EXCELLENT = "excellent"


class ImprovementType(Enum):
    """Types of improvements between drafts"""

    PERFORMANCE = "performance"
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    EFFICIENCY = "efficiency"
    CLARITY = "clarity"


@dataclass
class DraftResult:
    """Result from a single draft execution"""

    draft_number: int
    coordination_result: CoordinationResult
    execution_time_ms: int
    quality_score: float  # 0.0-1.0
    quality_assessment: DraftQuality
    metadata: Dict[str, Any]
    created_at: datetime


@dataclass
class DraftComparison:
    """Comparison between two drafts"""

    draft_1: DraftResult
    draft_2: DraftResult
    improvement_percentage: float
    improvement_types: List[ImprovementType]
    performance_delta_ms: int
    accuracy_improvement: float
    quality_improvement: float
    learning_insights: List[str]


@dataclass
class ChainOfDraftResult:
    """Complete Chain-of-Draft experiment result"""

    experiment_id: str
    intent: Intent
    drafts: List[DraftResult]
    best_draft: DraftResult
    draft_comparison: Optional[DraftComparison]
    total_experiment_time_ms: int
    learning_summary: Dict[str, Any]
    success: bool


class DraftQualityAssessor:
    """Assesses quality of coordination drafts"""

    def assess_coordination_quality(self, result: CoordinationResult) -> Tuple[float, DraftQuality]:
        """
        Assess the quality of a coordination result

        Args:
            result: Coordination result to assess

        Returns:
            Tuple of (quality_score, quality_assessment)
        """
        quality_factors = []

        # Performance factor (0.3 weight)
        if result.total_duration_ms <= 100:
            performance_score = 1.0
        elif result.total_duration_ms <= 500:
            performance_score = 0.8
        elif result.total_duration_ms <= 1000:
            performance_score = 0.6
        else:
            performance_score = 0.3

        quality_factors.append(("performance", performance_score, 0.3))

        # Success rate factor (0.3 weight)
        success_score = result.success_rate
        quality_factors.append(("success", success_score, 0.3))

        # Task decomposition quality factor (0.2 weight)
        if len(result.subtasks) == 0:
            decomposition_score = 0.0
        elif len(result.subtasks) == 1:
            decomposition_score = 0.5  # Simple task
        elif 2 <= len(result.subtasks) <= 4:
            decomposition_score = 1.0  # Optimal decomposition
        else:
            decomposition_score = 0.7  # Over-decomposed

        quality_factors.append(("decomposition", decomposition_score, 0.2))

        # Agent distribution factor (0.2 weight)
        if result.subtasks:
            code_tasks = len(
                [
                    t
                    for t in result.subtasks
                    if hasattr(t, "assigned_agent") and str(t.assigned_agent).endswith("CODE")
                ]
            )
            cursor_tasks = len(
                [
                    t
                    for t in result.subtasks
                    if hasattr(t, "assigned_agent") and str(t.assigned_agent).endswith("CURSOR")
                ]
            )

            if code_tasks > 0 and cursor_tasks > 0:
                distribution_score = 1.0  # Good multi-agent distribution
            elif len(result.subtasks) > 1:
                distribution_score = 0.7  # Single agent for multi-task
            else:
                distribution_score = 0.8  # Single task, single agent (reasonable)
        else:
            distribution_score = 0.0

        quality_factors.append(("distribution", distribution_score, 0.2))

        # Calculate weighted quality score
        quality_score = sum(score * weight for _, score, weight in quality_factors)

        # Determine quality assessment
        if quality_score >= 0.9:
            quality_assessment = DraftQuality.EXCELLENT
        elif quality_score >= 0.7:
            quality_assessment = DraftQuality.GOOD
        elif quality_score >= 0.5:
            quality_assessment = DraftQuality.ACCEPTABLE
        else:
            quality_assessment = DraftQuality.POOR

        return quality_score, quality_assessment


class ChainOfDraftExperiment:
    """
    Implements simple 2-draft Chain-of-Draft experiment system

    Executes coordination twice with slight variations to compare results
    and identify improvements for learning.
    """

    def __init__(self):
        self.coordinator = MultiAgentCoordinator()
        self.quality_assessor = DraftQualityAssessor()
        self.experiments: Dict[str, ChainOfDraftResult] = {}

    async def run_draft_experiment(
        self, intent: Intent, experiment_id: Optional[str] = None
    ) -> ChainOfDraftResult:
        """
        Run 2-draft experiment with given intent

        Args:
            intent: Intent to coordinate
            experiment_id: Optional experiment identifier

        Returns:
            ChainOfDraftResult with comparison and learning insights
        """
        if experiment_id is None:
            experiment_id = f"exp_{intent.id}_{int(time.time() * 1000)}"

        logger.info(
            "Starting Chain-of-Draft experiment", experiment_id=experiment_id, intent_id=intent.id
        )

        experiment_start = time.time()

        try:
            # Execute Draft 1
            draft_1 = await self._execute_draft(intent, draft_number=1)

            # Small delay between drafts
            await asyncio.sleep(0.001)

            # Execute Draft 2 with slight context variation
            draft_2 = await self._execute_draft(intent, draft_number=2, context_variation=True)

            # Compare drafts
            comparison = self._compare_drafts(draft_1, draft_2)

            # Determine best draft
            best_draft = draft_2 if draft_2.quality_score > draft_1.quality_score else draft_1

            # Generate learning summary
            learning_summary = self._generate_learning_summary([draft_1, draft_2], comparison)

            experiment_result = ChainOfDraftResult(
                experiment_id=experiment_id,
                intent=intent,
                drafts=[draft_1, draft_2],
                best_draft=best_draft,
                draft_comparison=comparison,
                total_experiment_time_ms=int((time.time() - experiment_start) * 1000),
                learning_summary=learning_summary,
                success=True,
            )

            self.experiments[experiment_id] = experiment_result

            logger.info(
                "Chain-of-Draft experiment completed",
                experiment_id=experiment_id,
                improvement=comparison.improvement_percentage if comparison else 0.0,
            )

            return experiment_result

        except Exception as e:
            logger.error(
                "Chain-of-Draft experiment failed", experiment_id=experiment_id, error=str(e)
            )

            # Return failed experiment result
            return ChainOfDraftResult(
                experiment_id=experiment_id,
                intent=intent,
                drafts=[],
                best_draft=None,
                draft_comparison=None,
                total_experiment_time_ms=int((time.time() - experiment_start) * 1000),
                learning_summary={"error": str(e)},
                success=False,
            )

    async def _execute_draft(
        self, intent: Intent, draft_number: int, context_variation: bool = False
    ) -> DraftResult:
        """Execute a single draft coordination"""

        # Add slight context variation for draft 2
        context = {}
        if context_variation:
            context["draft_variation"] = True
            context["exploration_mode"] = True

        start_time = time.time()

        coordination_result = await self.coordinator.coordinate_task(intent, context)

        execution_time = int((time.time() - start_time) * 1000)

        # Assess quality
        quality_score, quality_assessment = self.quality_assessor.assess_coordination_quality(
            coordination_result
        )

        draft_result = DraftResult(
            draft_number=draft_number,
            coordination_result=coordination_result,
            execution_time_ms=execution_time,
            quality_score=quality_score,
            quality_assessment=quality_assessment,
            metadata={
                "context_variation": context_variation,
                "subtask_count": len(coordination_result.subtasks),
                "agent_utilization": coordination_result.agent_performance,
            },
            created_at=datetime.now(),
        )

        logger.info(
            "Draft executed",
            draft_number=draft_number,
            quality_score=quality_score,
            execution_time_ms=execution_time,
        )

        return draft_result

    def _compare_drafts(self, draft_1: DraftResult, draft_2: DraftResult) -> DraftComparison:
        """Compare two drafts and identify improvements"""

        # Calculate improvement metrics
        quality_improvement = draft_2.quality_score - draft_1.quality_score
        performance_delta = draft_2.execution_time_ms - draft_1.execution_time_ms
        accuracy_improvement = (
            draft_2.coordination_result.success_rate - draft_1.coordination_result.success_rate
        )

        improvement_percentage = (quality_improvement / max(draft_1.quality_score, 0.01)) * 100

        # Identify improvement types
        improvement_types = []

        if performance_delta < -10:  # 10ms improvement threshold
            improvement_types.append(ImprovementType.PERFORMANCE)

        if accuracy_improvement > 0.01:  # 1% accuracy improvement
            improvement_types.append(ImprovementType.ACCURACY)

        if quality_improvement > 0.05:  # 5% quality improvement
            improvement_types.append(ImprovementType.COMPLETENESS)

        if len(draft_2.coordination_result.subtasks) != len(draft_1.coordination_result.subtasks):
            improvement_types.append(ImprovementType.EFFICIENCY)

        # Generate learning insights
        learning_insights = []

        if improvement_percentage > 5:
            learning_insights.append(
                f"Draft 2 showed {improvement_percentage:.1f}% quality improvement"
            )

        if performance_delta < -50:
            learning_insights.append(
                f"Significant performance improvement: {abs(performance_delta)}ms faster"
            )

        if len(improvement_types) == 0:
            learning_insights.append(
                "Minimal differences between drafts - coordination is consistent"
            )

        if draft_2.quality_assessment.value != draft_1.quality_assessment.value:
            learning_insights.append(
                f"Quality level changed from {draft_1.quality_assessment.value} to {draft_2.quality_assessment.value}"
            )

        return DraftComparison(
            draft_1=draft_1,
            draft_2=draft_2,
            improvement_percentage=improvement_percentage,
            improvement_types=improvement_types,
            performance_delta_ms=performance_delta,
            accuracy_improvement=accuracy_improvement,
            quality_improvement=quality_improvement,
            learning_insights=learning_insights,
        )

    def _generate_learning_summary(
        self, drafts: List[DraftResult], comparison: DraftComparison
    ) -> Dict[str, Any]:
        """Generate learning summary from experiment"""

        summary = {
            "experiment_type": "2-draft_comparison",
            "total_drafts": len(drafts),
            "quality_progression": [d.quality_score for d in drafts],
            "performance_progression": [d.execution_time_ms for d in drafts],
            "best_draft_number": max(drafts, key=lambda d: d.quality_score).draft_number,
            "improvement_detected": comparison.improvement_percentage > 1.0,
            "improvement_types": [t.value for t in comparison.improvement_types],
            "key_insights": comparison.learning_insights,
            "recommendations": [],
        }

        # Generate recommendations
        if comparison.improvement_percentage > 10:
            summary["recommendations"].append("Continue with context variation approaches")

        if comparison.performance_delta_ms < -100:
            summary["recommendations"].append("Investigate performance optimization factors")

        if len(comparison.improvement_types) == 0:
            summary["recommendations"].append(
                "Coordination is stable - consider more complex variations"
            )

        return summary

    async def get_experiment_results(self, experiment_id: str) -> Optional[ChainOfDraftResult]:
        """Get results for specific experiment"""
        return self.experiments.get(experiment_id)

    async def get_learning_analytics(self) -> Dict[str, Any]:
        """Get analytics across all experiments"""

        if not self.experiments:
            return {"total_experiments": 0, "no_data": True}

        experiments = list(self.experiments.values())
        successful_experiments = [e for e in experiments if e.success]

        # Calculate analytics
        analytics = {
            "total_experiments": len(experiments),
            "successful_experiments": len(successful_experiments),
            "success_rate": len(successful_experiments) / len(experiments),
            "avg_improvement_percentage": 0.0,
            "common_improvement_types": {},
            "avg_experiment_time_ms": 0.0,
            "quality_trends": [],
        }

        if successful_experiments:
            # Calculate averages
            improvements = [
                e.draft_comparison.improvement_percentage
                for e in successful_experiments
                if e.draft_comparison
            ]
            analytics["avg_improvement_percentage"] = (
                sum(improvements) / len(improvements) if improvements else 0.0
            )

            experiment_times = [e.total_experiment_time_ms for e in successful_experiments]
            analytics["avg_experiment_time_ms"] = sum(experiment_times) / len(experiment_times)

            # Track improvement types
            improvement_counts = {}
            for exp in successful_experiments:
                if exp.draft_comparison:
                    for imp_type in exp.draft_comparison.improvement_types:
                        improvement_counts[imp_type.value] = (
                            improvement_counts.get(imp_type.value, 0) + 1
                        )

            analytics["common_improvement_types"] = improvement_counts

            # Quality trends
            for exp in successful_experiments:
                if exp.drafts:
                    quality_trend = [d.quality_score for d in exp.drafts]
                    analytics["quality_trends"].append(quality_trend)

        return analytics


# Integration function for Phase 4 testing
async def run_chain_of_draft_validation() -> Dict[str, Any]:
    """Run Chain-of-Draft validation for PM-033d Phase 4"""

    print("🔄 CHAIN-OF-DRAFT EXPERIMENT VALIDATION")
    print("=" * 50)

    experiment = ChainOfDraftExperiment()

    # Test with different intent complexities
    test_intents = [
        Intent(
            category=Intent.category if hasattr(Intent, "category") else None,
            action="implement_rest_api",
            original_message="Implement REST API for user management with authentication and validation",
            confidence=0.95,
        ),
        Intent(
            category=Intent.category if hasattr(Intent, "category") else None,
            action="refactor_database_layer",
            original_message="Refactor database layer with connection pooling and query optimization",
            confidence=0.92,
        ),
    ]

    results = []

    for i, intent in enumerate(test_intents, 1):
        print(f"\n🧪 Experiment {i}: {intent.action}")

        result = await experiment.run_draft_experiment(intent)
        results.append(result)

        if result.success:
            print(f"   ✅ Success - {len(result.drafts)} drafts completed")
            print(f"   Best Quality: {result.best_draft.quality_score:.2f}")
            print(
                f"   Improvement: {result.draft_comparison.improvement_percentage:.1f}%"
                if result.draft_comparison
                else "   No comparison"
            )
            print(f"   Experiment Time: {result.total_experiment_time_ms}ms")
        else:
            print(f'   ❌ Failed: {result.learning_summary.get("error", "Unknown error")}')

    # Get learning analytics
    analytics = await experiment.get_learning_analytics()

    print(f"\n📊 CHAIN-OF-DRAFT ANALYTICS:")
    print(f'   Total Experiments: {analytics["total_experiments"]}')
    print(f'   Success Rate: {analytics["success_rate"]*100:.1f}%')
    print(f'   Avg Improvement: {analytics["avg_improvement_percentage"]:.1f}%')
    print(f'   Avg Experiment Time: {analytics["avg_experiment_time_ms"]:.1f}ms')

    validation_success = (
        analytics["success_rate"] >= 0.5  # At least 50% success rate
        and analytics["avg_experiment_time_ms"] < 5000  # Under 5 seconds per experiment
    )

    print(f'\n🎯 CHAIN-OF-DRAFT VALIDATION: {"✅ PASSED" if validation_success else "❌ FAILED"}')

    return {
        "validation_success": validation_success,
        "analytics": analytics,
        "experiment_results": [r.success for r in results],
    }


if __name__ == "__main__":
    # Run Chain-of-Draft validation directly
    import asyncio

    from services.shared_types import IntentCategory

    # Create proper intents for testing
    test_intent = Intent(
        category=IntentCategory.EXECUTION,
        action="implement_rest_api",
        original_message="Implement REST API for user management with authentication and validation",
        confidence=0.95,
    )

    async def test_chain_of_draft():
        experiment = ChainOfDraftExperiment()
        result = await experiment.run_draft_experiment(test_intent)
        print(f"Experiment completed: {result.success}")
        return result

    asyncio.run(test_chain_of_draft())

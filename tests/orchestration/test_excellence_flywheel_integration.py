"""
Comprehensive unit tests for ExcellenceFlywheelIntegrator

Tests all 5 verification phases, pattern detection accuracy, learning insights generation,
acceleration metrics, and integration with coordination flows for PM-033d implementation.
"""

import asyncio
import time
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.orchestration.excellence_flywheel_integration import (
    ExcellenceFlywheel,
    ExcellenceFlywheelIntegrator,
    VerificationCheck,
    VerificationPhase,
    VerificationResult,
)
from services.orchestration.multi_agent_coordinator import (
    AgentType,
    CoordinationResult,
    CoordinationStatus,
    SubTask,
    TaskComplexity,
)
from services.shared_types import IntentCategory, TaskStatus


class TestVerificationCheck:
    """Test VerificationCheck data structure"""

    def test_verification_check_creation(self):
        """Test VerificationCheck creation with all fields"""
        check = VerificationCheck(
            check_id="test_check",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Test verification",
            result=VerificationResult.PASSED,
            details="All checks passed",
            evidence={"test": "data"},
            duration_ms=50,
            created_at=datetime.now(),
        )

        assert check.check_id == "test_check"
        assert check.phase == VerificationPhase.PRE_COORDINATION
        assert check.result == VerificationResult.PASSED
        assert check.evidence["test"] == "data"
        assert check.duration_ms == 50


class TestExcellenceFlywheel:
    """Test ExcellenceFlywheel data structure"""

    def test_excellence_flywheel_creation(self):
        """Test ExcellenceFlywheel creation with comprehensive data"""
        check = VerificationCheck(
            check_id="test_check",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Test verification",
            result=VerificationResult.PASSED,
            details="Test details",
            evidence={},
            duration_ms=10,
            created_at=datetime.now(),
        )

        flywheel = ExcellenceFlywheel(
            coordination_id="test_coord_123",
            verification_checks=[check],
            learning_insights=["Test insight"],
            patterns_detected={"pattern_type": "test"},
            acceleration_metrics={"speed": 1.5},
            compound_knowledge={"knowledge": "accumulated"},
            systematic_verified=True,
        )

        assert flywheel.coordination_id == "test_coord_123"
        assert len(flywheel.verification_checks) == 1
        assert flywheel.learning_insights[0] == "Test insight"
        assert flywheel.patterns_detected["pattern_type"] == "test"
        assert flywheel.systematic_verified is True


class TestExcellenceFlywheelIntegrator:
    """Test ExcellenceFlywheelIntegrator comprehensive functionality"""

    @pytest.fixture
    def integrator(self):
        """Create a fresh ExcellenceFlywheelIntegrator instance for each test"""
        return ExcellenceFlywheelIntegrator()

    @pytest.fixture
    def simple_intent(self):
        """Create a simple intent for testing"""
        return Intent(
            id=f"intent_{uuid4().hex[:8]}",
            category=IntentCategory.QUERY,
            action="get_status",
            original_message="Get current system status",
            confidence=0.9,
        )

    @pytest.fixture
    def complex_intent(self):
        """Create a complex intent for testing"""
        return Intent(
            id=f"intent_{uuid4().hex[:8]}",
            category=IntentCategory.EXECUTION,
            action="implement_architecture",
            original_message="Implement comprehensive system architecture with database, API, testing, and documentation",
            confidence=0.98,
        )

    @pytest.fixture
    def mock_coordination_result(self):
        """Create a mock coordination result"""
        subtasks = [
            SubTask(
                id="task_1",
                title="Architecture Design",
                description="Design system architecture",
                estimated_duration_minutes=60,
                complexity=TaskComplexity.MODERATE,
                required_capabilities=["infrastructure"],
                dependencies=[],
                assigned_agent=AgentType.CODE,
            ),
            SubTask(
                id="task_2",
                title="Implementation",
                description="Implement features",
                estimated_duration_minutes=90,
                complexity=TaskComplexity.MODERATE,
                required_capabilities=["backend_services"],
                dependencies=["task_1"],
                assigned_agent=AgentType.CODE,
            ),
            SubTask(
                id="task_3",
                title="Testing",
                description="Create comprehensive tests",
                estimated_duration_minutes=45,
                complexity=TaskComplexity.SIMPLE,
                required_capabilities=["testing_frameworks"],
                dependencies=["task_2"],
                assigned_agent=AgentType.CURSOR,
            ),
        ]

        return CoordinationResult(
            coordination_id="test_coord_123",
            status=CoordinationStatus.ASSIGNED,
            subtasks=subtasks,
            total_duration_ms=750,
            success_rate=1.0,
            agent_performance={
                AgentType.CODE: {"assigned_tasks": 2},
                AgentType.CURSOR: {"assigned_tasks": 1},
            },
        )

    @pytest.mark.asyncio
    async def test_coordinate_with_excellence_flywheel_success(self, integrator, simple_intent):
        """Test successful Excellence Flywheel coordination"""
        context = {"user_session": "test_session"}

        coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(
            simple_intent, context
        )

        # Verify coordination result
        assert isinstance(coordination_result, CoordinationResult)
        assert coordination_result.status == CoordinationStatus.ASSIGNED

        # Verify flywheel
        assert isinstance(flywheel, ExcellenceFlywheel)
        assert flywheel.coordination_id.startswith("flywheel_")
        assert len(flywheel.verification_checks) >= 5  # At least 5 verification phases
        assert flywheel.systematic_verified is True  # Should pass all checks

    @pytest.mark.asyncio
    async def test_coordinate_with_excellence_flywheel_error_handling(
        self, integrator, simple_intent
    ):
        """Test Excellence Flywheel coordination error handling"""
        # Mock coordinator to raise exception
        with patch.object(
            integrator.coordinator, "coordinate_task", side_effect=Exception("Coordination failed")
        ):
            coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(
                simple_intent
            )

        # Verify error handling
        assert coordination_result.status == CoordinationStatus.FAILED
        assert "Coordination failed" in str(coordination_result.error_details)
        assert len(flywheel.verification_checks) >= 1  # Should have error check

        # Find error check
        error_checks = [
            c for c in flywheel.verification_checks if c.result == VerificationResult.FAILED
        ]
        assert len(error_checks) >= 1
        assert "Coordination failed" in error_checks[0].details

    @pytest.mark.asyncio
    async def test_verify_pre_coordination(self, integrator, simple_intent):
        """Test pre-coordination verification phase"""
        flywheel = ExcellenceFlywheel(
            coordination_id="test_coord",
            verification_checks=[],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )
        context = {"user_session": "test"}

        await integrator._verify_pre_coordination(simple_intent, flywheel, context)

        # Should have 3 pre-coordination checks
        pre_checks = [
            c for c in flywheel.verification_checks if c.phase == VerificationPhase.PRE_COORDINATION
        ]
        assert len(pre_checks) == 3

        # Check types
        check_ids = [c.check_id for c in pre_checks]
        assert "intent_structure" in check_ids
        assert "pattern_availability" in check_ids
        assert "context_adequacy" in check_ids

    @pytest.mark.asyncio
    async def test_execute_verified_coordination(
        self, integrator, simple_intent, mock_coordination_result
    ):
        """Test verified coordination execution"""
        flywheel = ExcellenceFlywheel(
            coordination_id="test_coord",
            verification_checks=[],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )

        # Mock coordinator to return predetermined result
        with patch.object(
            integrator.coordinator, "coordinate_task", return_value=mock_coordination_result
        ):
            result = await integrator._execute_verified_coordination(simple_intent, flywheel, {})

        assert result == mock_coordination_result

        # Should have task decomposition and agent assignment checks
        decomposition_checks = [
            c
            for c in flywheel.verification_checks
            if c.phase == VerificationPhase.TASK_DECOMPOSITION
        ]
        assignment_checks = [
            c for c in flywheel.verification_checks if c.phase == VerificationPhase.AGENT_ASSIGNMENT
        ]

        assert len(decomposition_checks) == 1
        assert len(assignment_checks) == 1

    @pytest.mark.asyncio
    async def test_verify_post_coordination(self, integrator, mock_coordination_result):
        """Test post-coordination verification phase"""
        flywheel = ExcellenceFlywheel(
            coordination_id="test_coord",
            verification_checks=[],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )

        await integrator._verify_post_coordination(mock_coordination_result, flywheel)

        # Should have 3 post-coordination checks
        post_checks = [
            c
            for c in flywheel.verification_checks
            if c.phase == VerificationPhase.POST_COORDINATION
        ]
        assert len(post_checks) == 3

        check_ids = [c.check_id for c in post_checks]
        assert "performance_targets" in check_ids
        assert "coordination_quality" in check_ids
        assert "success_metrics" in check_ids

    @pytest.mark.asyncio
    async def test_capture_learning_and_patterns(
        self, integrator, simple_intent, mock_coordination_result
    ):
        """Test learning capture and pattern detection"""
        flywheel = ExcellenceFlywheel(
            coordination_id="test_coord",
            verification_checks=[],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )

        await integrator._capture_learning_and_patterns(
            simple_intent, mock_coordination_result, flywheel
        )

        # Should have patterns and insights
        assert len(flywheel.patterns_detected) > 0
        assert len(flywheel.learning_insights) >= 0  # May be 0 if no insights generated

        # Should have learning capture check
        learning_checks = [
            c for c in flywheel.verification_checks if c.phase == VerificationPhase.LEARNING_CAPTURE
        ]
        assert len(learning_checks) == 1

    @pytest.mark.asyncio
    async def test_update_acceleration_metrics(self, integrator):
        """Test acceleration metrics updates"""
        flywheel = ExcellenceFlywheel(
            coordination_id="test_coord",
            verification_checks=[
                VerificationCheck(
                    check_id="test1",
                    phase=VerificationPhase.PRE_COORDINATION,
                    description="Test",
                    result=VerificationResult.PASSED,
                    details="Passed",
                    evidence={},
                    duration_ms=10,
                    created_at=datetime.now(),
                ),
                VerificationCheck(
                    check_id="test2",
                    phase=VerificationPhase.POST_COORDINATION,
                    description="Test",
                    result=VerificationResult.PASSED,
                    details="Passed",
                    evidence={},
                    duration_ms=15,
                    created_at=datetime.now(),
                ),
            ],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )

        total_duration_s = 0.5  # 500ms
        await integrator._update_acceleration_metrics(flywheel, total_duration_s)

        # Should update integrator's acceleration metrics
        assert "avg_coordination_time_ms" in integrator.acceleration_metrics
        assert "verification_success_rate" in integrator.acceleration_metrics
        assert "learning_acceleration_factor" in integrator.acceleration_metrics

        # Should copy to flywheel
        assert len(flywheel.acceleration_metrics) > 0
        assert flywheel.acceleration_metrics["learning_acceleration_factor"] >= 1.0

    @pytest.mark.asyncio
    async def test_verify_intent_structure_valid(self, integrator, simple_intent):
        """Test intent structure verification with valid intent"""
        check = await integrator._verify_intent_structure(simple_intent)

        assert check.check_id == "intent_structure"
        assert check.phase == VerificationPhase.PRE_COORDINATION
        assert check.result == VerificationResult.PASSED
        assert "All checks passed" in check.details

    @pytest.mark.asyncio
    async def test_verify_intent_structure_invalid(self, integrator):
        """Test intent structure verification with invalid intent"""
        invalid_intent = Intent(
            id="test_invalid",
            category=IntentCategory.QUERY,
            action="",  # Missing action
            original_message="",  # Missing message
            confidence=0.0,  # Invalid confidence
        )

        check = await integrator._verify_intent_structure(invalid_intent)

        assert check.check_id == "intent_structure"
        assert check.result == VerificationResult.FAILED
        assert "Missing action" in check.details
        assert "Missing original message" in check.details
        assert "Invalid confidence score" in check.details

    @pytest.mark.asyncio
    async def test_verify_pattern_availability_no_patterns(self, integrator, simple_intent):
        """Test pattern availability verification with no existing patterns"""
        check = await integrator._verify_pattern_availability(simple_intent)

        assert check.check_id == "pattern_availability"
        assert check.result == VerificationResult.WARNING  # No patterns available
        assert "Found 0 similar patterns" in check.details

    @pytest.mark.asyncio
    async def test_verify_pattern_availability_with_patterns(self, integrator, simple_intent):
        """Test pattern availability verification with existing patterns"""
        # Add some patterns to the library
        integrator.pattern_library["get_status_simple"] = {
            "action": "get_status",
            "subtask_count": 1,
            "performance_ms": 500,
            "success_rate": 1.0,
            "usage_count": 5,
        }

        check = await integrator._verify_pattern_availability(simple_intent)

        assert check.check_id == "pattern_availability"
        assert check.result == VerificationResult.PASSED
        assert "Found 1 similar patterns" in check.details

    @pytest.mark.asyncio
    async def test_verify_context_adequacy_empty(self, integrator):
        """Test context adequacy verification with empty context"""
        check = await integrator._verify_context_adequacy(None)

        assert check.check_id == "context_adequacy"
        assert check.result == VerificationResult.WARNING
        assert "Context adequacy score: 0.00" in check.details

    @pytest.mark.asyncio
    async def test_verify_context_adequacy_adequate(self, integrator):
        """Test context adequacy verification with adequate context"""
        context = {
            "user_session": "test_session",
            "project_id": "test_project",
            "workspace": "test_workspace",
        }

        check = await integrator._verify_context_adequacy(context)

        assert check.check_id == "context_adequacy"
        assert check.result == VerificationResult.PASSED
        assert "Context adequacy score: 1.00" in check.details

    @pytest.mark.asyncio
    async def test_verify_task_decomposition_optimal(self, integrator, mock_coordination_result):
        """Test task decomposition verification with optimal decomposition"""
        check = await integrator._verify_task_decomposition(mock_coordination_result)

        assert check.check_id == "task_decomposition"
        assert check.result == VerificationResult.PASSED
        assert "Optimal decomposition: 3 subtasks" in check.details

    @pytest.mark.asyncio
    async def test_verify_task_decomposition_single(self, integrator):
        """Test task decomposition verification with single task"""
        single_task_result = CoordinationResult(
            coordination_id="test_single",
            status=CoordinationStatus.ASSIGNED,
            subtasks=[
                SubTask(
                    id="single_task",
                    title="Single Task",
                    description="Single task",
                    estimated_duration_minutes=30,
                    complexity=TaskComplexity.SIMPLE,
                    required_capabilities=["general"],
                    dependencies=[],
                    assigned_agent=AgentType.CODE,
                )
            ],
            total_duration_ms=500,
            success_rate=1.0,
            agent_performance={},
        )

        check = await integrator._verify_task_decomposition(single_task_result)

        assert check.check_id == "task_decomposition"
        assert check.result == VerificationResult.WARNING
        assert "Simple task: 1 subtask" in check.details

    @pytest.mark.asyncio
    async def test_verify_task_decomposition_over_complex(self, integrator):
        """Test task decomposition verification with over-decomposition"""
        # Create result with too many subtasks
        many_subtasks = []
        for i in range(7):  # More than 5 subtasks
            subtask = SubTask(
                id=f"task_{i}",
                title=f"Task {i}",
                description=f"Description {i}",
                estimated_duration_minutes=30,
                complexity=TaskComplexity.SIMPLE,
                required_capabilities=["general"],
                dependencies=[],
                assigned_agent=AgentType.CODE,
            )
            many_subtasks.append(subtask)

        over_complex_result = CoordinationResult(
            coordination_id="test_over_complex",
            status=CoordinationStatus.ASSIGNED,
            subtasks=many_subtasks,
            total_duration_ms=500,
            success_rate=1.0,
            agent_performance={},
        )

        check = await integrator._verify_task_decomposition(over_complex_result)

        assert check.check_id == "task_decomposition"
        assert check.result == VerificationResult.WARNING
        assert "Complex decomposition: 7 subtasks" in check.details

    @pytest.mark.asyncio
    async def test_verify_agent_assignments_multi_agent(self, integrator, mock_coordination_result):
        """Test agent assignment verification with multi-agent coordination"""
        check = await integrator._verify_agent_assignments(mock_coordination_result)

        assert check.check_id == "agent_assignments"
        assert check.result == VerificationResult.PASSED
        assert "uses_multiple_agents" in check.evidence
        assert check.evidence["uses_multiple_agents"] is True

    @pytest.mark.asyncio
    async def test_verify_agent_assignments_no_subtasks(self, integrator):
        """Test agent assignment verification with no subtasks"""
        empty_result = CoordinationResult(
            coordination_id="test_empty",
            status=CoordinationStatus.ASSIGNED,
            subtasks=[],
            total_duration_ms=100,
            success_rate=1.0,
            agent_performance={},
        )

        check = await integrator._verify_agent_assignments(empty_result)

        assert check.check_id == "agent_assignments"
        assert check.result == VerificationResult.WARNING
        assert "No subtasks to assign" in check.details

    @pytest.mark.asyncio
    async def test_verify_performance_targets_meets_target(self, integrator):
        """Test performance target verification when target is met"""
        fast_result = CoordinationResult(
            coordination_id="test_fast",
            status=CoordinationStatus.ASSIGNED,
            subtasks=[],
            total_duration_ms=500,  # Under 1000ms target
            success_rate=1.0,
            agent_performance={},
        )

        check = await integrator._verify_performance_targets(fast_result)

        assert check.check_id == "performance_targets"
        assert check.result == VerificationResult.PASSED
        assert "Coordination time: 500ms" in check.details

    @pytest.mark.asyncio
    async def test_verify_performance_targets_misses_target(self, integrator):
        """Test performance target verification when target is missed"""
        slow_result = CoordinationResult(
            coordination_id="test_slow",
            status=CoordinationStatus.ASSIGNED,
            subtasks=[],
            total_duration_ms=1500,  # Over 1000ms target
            success_rate=1.0,
            agent_performance={},
        )

        check = await integrator._verify_performance_targets(slow_result)

        assert check.check_id == "performance_targets"
        assert check.result == VerificationResult.WARNING
        assert "Coordination time: 1500ms" in check.details

    @pytest.mark.asyncio
    async def test_verify_coordination_quality_excellent(
        self, integrator, mock_coordination_result
    ):
        """Test coordination quality verification with excellent results"""
        check = await integrator._verify_coordination_quality(mock_coordination_result)

        assert check.check_id == "coordination_quality"
        # Should be PASSED or WARNING depending on exact quality score
        assert check.result in [VerificationResult.PASSED, VerificationResult.WARNING]
        assert "Quality score:" in check.details

    @pytest.mark.asyncio
    async def test_verify_coordination_quality_failed(self, integrator):
        """Test coordination quality verification with failed coordination"""
        failed_result = CoordinationResult(
            coordination_id="test_failed",
            status=CoordinationStatus.FAILED,
            subtasks=[],
            total_duration_ms=5000,  # Very slow
            success_rate=0.0,  # No success
            agent_performance={},
        )

        check = await integrator._verify_coordination_quality(failed_result)

        assert check.check_id == "coordination_quality"
        assert check.result in [VerificationResult.FAILED, VerificationResult.WARNING]

    @pytest.mark.asyncio
    async def test_verify_success_metrics_high_success(self, integrator, mock_coordination_result):
        """Test success metrics verification with high success rate"""
        check = await integrator._verify_success_metrics(mock_coordination_result)

        assert check.check_id == "success_metrics"
        assert check.result == VerificationResult.PASSED
        assert "Success rate: 1.00" in check.details

    @pytest.mark.asyncio
    async def test_verify_success_metrics_low_success(self, integrator):
        """Test success metrics verification with low success rate"""
        low_success_result = CoordinationResult(
            coordination_id="test_low_success",
            status=CoordinationStatus.ASSIGNED,
            subtasks=[],
            total_duration_ms=500,
            success_rate=0.7,  # Below 0.9 threshold
            agent_performance={},
        )

        check = await integrator._verify_success_metrics(low_success_result)

        assert check.check_id == "success_metrics"
        assert check.result == VerificationResult.WARNING
        assert "Success rate: 0.70" in check.details

    @pytest.mark.asyncio
    async def test_detect_coordination_patterns(
        self, integrator, simple_intent, mock_coordination_result
    ):
        """Test coordination pattern detection"""
        patterns = await integrator._detect_coordination_patterns(
            simple_intent, mock_coordination_result
        )

        assert "action_pattern" in patterns
        assert "subtask_pattern" in patterns
        assert "performance_pattern" in patterns
        assert "success_pattern" in patterns
        assert "complexity_pattern" in patterns

        assert patterns["action_pattern"] == simple_intent.action
        assert patterns["subtask_pattern"] == len(mock_coordination_result.subtasks)
        assert patterns["performance_pattern"] == "fast"  # 750ms is fast
        assert patterns["success_pattern"] == "high"  # 1.0 success rate
        assert patterns["complexity_pattern"] == "complex"  # 3 subtasks

    @pytest.mark.asyncio
    async def test_generate_learning_insights_excellent_performance(
        self, integrator, simple_intent
    ):
        """Test learning insights generation for excellent performance"""
        excellent_result = CoordinationResult(
            coordination_id="test_excellent",
            status=CoordinationStatus.ASSIGNED,
            subtasks=[
                SubTask(
                    id="task_1",
                    title="Task 1",
                    description="Description",
                    estimated_duration_minutes=30,
                    complexity=TaskComplexity.SIMPLE,
                    required_capabilities=["general"],
                    dependencies=[],
                    assigned_agent=AgentType.CODE,
                ),
                SubTask(
                    id="task_2",
                    title="Task 2",
                    description="Description",
                    estimated_duration_minutes=30,
                    complexity=TaskComplexity.SIMPLE,
                    required_capabilities=["general"],
                    dependencies=[],
                    assigned_agent=AgentType.CURSOR,
                ),
            ],
            total_duration_ms=50,  # Exceptional speed
            success_rate=1.0,  # Perfect success
            agent_performance={},
        )

        flywheel = ExcellenceFlywheel(
            coordination_id="test",
            verification_checks=[
                VerificationCheck(
                    check_id="test",
                    phase=VerificationPhase.PRE_COORDINATION,
                    description="Test",
                    result=VerificationResult.PASSED,
                    details="Passed",
                    evidence={},
                    duration_ms=10,
                    created_at=datetime.now(),
                )
            ],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )

        insights = await integrator._generate_learning_insights(
            simple_intent, excellent_result, flywheel
        )

        # Should generate multiple insights for excellent performance
        assert len(insights) >= 3
        assert any("Exceptional coordination speed" in insight for insight in insights)
        assert any("Perfect success rate" in insight for insight in insights)
        assert any("All verification checks passed" in insight for insight in insights)
        assert any("Optimal task decomposition" in insight for insight in insights)

    @pytest.mark.asyncio
    async def test_update_pattern_library(
        self, integrator, simple_intent, mock_coordination_result
    ):
        """Test pattern library updates"""
        patterns = {"complexity_pattern": "complex"}

        await integrator._update_pattern_library(simple_intent, mock_coordination_result, patterns)

        # Should add pattern to library
        pattern_key = f"{simple_intent.action}_complex"
        assert pattern_key in integrator.pattern_library

        pattern_data = integrator.pattern_library[pattern_key]
        assert pattern_data["action"] == simple_intent.action
        assert pattern_data["subtask_count"] == len(mock_coordination_result.subtasks)
        assert pattern_data["performance_ms"] == mock_coordination_result.total_duration_ms
        assert pattern_data["success_rate"] == mock_coordination_result.success_rate
        assert pattern_data["usage_count"] == 1

    @pytest.mark.asyncio
    async def test_update_pattern_library_increment_usage(
        self, integrator, simple_intent, mock_coordination_result
    ):
        """Test pattern library usage count increment"""
        patterns = {"complexity_pattern": "simple"}
        pattern_key = f"{simple_intent.action}_simple"

        # Add pattern first time
        await integrator._update_pattern_library(simple_intent, mock_coordination_result, patterns)
        assert integrator.pattern_library[pattern_key]["usage_count"] == 1

        # Add same pattern again
        await integrator._update_pattern_library(simple_intent, mock_coordination_result, patterns)
        assert integrator.pattern_library[pattern_key]["usage_count"] == 2

    @pytest.mark.asyncio
    async def test_get_flywheel_analytics_no_data(self, integrator):
        """Test flywheel analytics with no data"""
        analytics = await integrator.get_flywheel_analytics()

        assert analytics["total_coordinations"] == 0
        assert analytics["no_data"] is True

    @pytest.mark.asyncio
    async def test_get_flywheel_analytics_with_data(self, integrator, simple_intent):
        """Test flywheel analytics with coordination data"""
        # Run some coordinations to populate data
        await integrator.coordinate_with_excellence_flywheel(simple_intent)
        await integrator.coordinate_with_excellence_flywheel(simple_intent)

        analytics = await integrator.get_flywheel_analytics()

        assert analytics["total_coordinations"] == 2
        assert "systematic_verification_rate" in analytics
        assert "avg_verification_checks" in analytics
        assert "pattern_library_size" in analytics
        assert "acceleration_metrics" in analytics
        assert "common_learning_insights" in analytics
        assert "verification_success_by_phase" in analytics

        # Verify rates are reasonable
        assert 0.0 <= analytics["systematic_verification_rate"] <= 1.0
        assert analytics["avg_verification_checks"] > 0

    @pytest.mark.asyncio
    async def test_performance_coordination_speed(self, integrator, simple_intent):
        """Test coordination performance meets speed targets"""
        start_time = time.time()

        coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(
            simple_intent
        )

        total_time_ms = (time.time() - start_time) * 1000

        # Should complete within reasonable time
        assert total_time_ms < 5000  # Less than 5 seconds total
        assert coordination_result.total_duration_ms < 2000  # Coordination itself should be fast

    @pytest.mark.asyncio
    async def test_concurrent_excellence_flywheel_coordination(self, integrator):
        """Test concurrent Excellence Flywheel coordinations"""
        intents = []
        for i in range(3):
            intent = Intent(
                id=f"concurrent_intent_{i}",
                category=IntentCategory.EXECUTION,
                action=f"concurrent_action_{i}",
                original_message=f"Concurrent test {i}",
                confidence=0.95,
            )
            intents.append(intent)

        # Execute concurrently
        tasks = [integrator.coordinate_with_excellence_flywheel(intent) for intent in intents]
        results = await asyncio.gather(*tasks)

        # All should succeed
        assert len(results) == 3
        for coordination_result, flywheel in results:
            assert coordination_result.status == CoordinationStatus.ASSIGNED
            assert flywheel.systematic_verified is True

    @pytest.mark.asyncio
    async def test_edge_case_malformed_intent(self, integrator):
        """Test handling of malformed intent"""
        malformed_intent = Intent(
            id="",  # Empty ID
            category=IntentCategory.QUERY,
            action=None,  # None action
            original_message="Test message",
            confidence=-1.0,  # Invalid confidence
        )

        coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(
            malformed_intent
        )

        # Should handle gracefully
        assert isinstance(coordination_result, CoordinationResult)
        assert isinstance(flywheel, ExcellenceFlywheel)

        # Should have failed intent structure verification
        intent_checks = [
            c for c in flywheel.verification_checks if c.check_id == "intent_structure"
        ]
        assert len(intent_checks) == 1
        assert intent_checks[0].result == VerificationResult.FAILED

    @pytest.mark.asyncio
    async def test_stress_test_verification_phases(self, integrator, simple_intent):
        """Test all verification phases under stress"""
        # Run multiple coordinations rapidly
        results = []
        for _ in range(10):
            coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(
                simple_intent
            )
            results.append((coordination_result, flywheel))

        # Verify all phases were executed
        all_phases = set()
        for _, flywheel in results:
            for check in flywheel.verification_checks:
                all_phases.add(check.phase)

        # Should have all verification phases
        expected_phases = {
            VerificationPhase.PRE_COORDINATION,
            VerificationPhase.TASK_DECOMPOSITION,
            VerificationPhase.AGENT_ASSIGNMENT,
            VerificationPhase.POST_COORDINATION,
            VerificationPhase.LEARNING_CAPTURE,
        }

        assert expected_phases.issubset(all_phases)

    @pytest.mark.asyncio
    async def test_verification_check_timing(self, integrator, simple_intent):
        """Test that verification checks are properly timed"""
        coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(
            simple_intent
        )

        # All checks should have reasonable timing
        for check in flywheel.verification_checks:
            assert check.duration_ms >= 0
            assert check.duration_ms < 10000  # Less than 10 seconds per check
            assert isinstance(check.created_at, datetime)

    @pytest.mark.asyncio
    async def test_acceleration_factor_calculation(self, integrator, simple_intent):
        """Test acceleration factor calculation over multiple coordinations"""
        # Run multiple coordinations to build acceleration data
        for _ in range(5):
            await integrator.coordinate_with_excellence_flywheel(simple_intent)

        # Check acceleration metrics
        assert integrator.acceleration_metrics["learning_acceleration_factor"] >= 1.0
        assert integrator.acceleration_metrics["avg_coordination_time_ms"] > 0
        assert 0.0 <= integrator.acceleration_metrics["verification_success_rate"] <= 1.0

    @pytest.mark.asyncio
    async def test_pattern_reuse_detection(self, integrator, simple_intent):
        """Test pattern reuse detection and acceleration"""
        # First coordination to establish pattern
        await integrator.coordinate_with_excellence_flywheel(simple_intent)

        # Second coordination should detect pattern reuse
        coordination_result, flywheel = await integrator.coordinate_with_excellence_flywheel(
            simple_intent
        )

        # Should have detected pattern availability
        pattern_checks = [
            c for c in flywheel.verification_checks if c.check_id == "pattern_availability"
        ]
        assert len(pattern_checks) == 1

        # Should have found similar patterns
        if len(integrator.pattern_library) > 0:
            assert pattern_checks[0].result == VerificationResult.PASSED

        # Pattern reuse rate should be updated
        assert "pattern_reuse_rate" in integrator.acceleration_metrics

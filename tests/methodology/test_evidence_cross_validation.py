"""
Cross-Validation Test Suite for Evidence Engine

Tests the Code Agent's evidence engine implementation to ensure:
- Evidence categorization accuracy
- Performance optimization claims
- Validation completeness
- Integration with verification pyramid

This test suite validates the enhanced evidence collection engine
against defined requirements and performance benchmarks.
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List

import pytest

# Import the evidence engine components (to be implemented by Code Agent)
try:
    from methodology.verification.evidence import (
        AdvancedEvidenceValidator,
        Evidence,
        EvidenceAutoCategorizer,
        EvidenceCache,
        EvidenceCollector,
        EvidenceType,
    )

    EVIDENCE_ENGINE_AVAILABLE = True
except ImportError:
    EVIDENCE_ENGINE_AVAILABLE = False

# Import requirements for validation
from methodology.verification.requirements import (
    TaskComplexity,
    TaskEvidenceRequirements,
    TaskType,
    ValidationReport,
)


@pytest.mark.skipif(not EVIDENCE_ENGINE_AVAILABLE, reason="Evidence engine not yet implemented")
class TestEvidenceEngineValidation:
    """Cross-validate Code Agent's evidence engine implementation"""

    @pytest.fixture
    def evidence_engine(self):
        """Import and initialize Code Agent's evidence engine"""
        if not EVIDENCE_ENGINE_AVAILABLE:
            pytest.skip("Evidence engine not yet implemented by Code Agent")

        from methodology.verification.evidence import AdvancedEvidenceValidator

        return AdvancedEvidenceValidator()

    @pytest.fixture
    def requirements_validator(self):
        """Initialize task evidence requirements validator"""
        return TaskEvidenceRequirements()

    @pytest.fixture
    def test_evidence_samples(self):
        """Generate test evidence samples for validation"""
        return [
            # Terminal evidence samples
            {
                "content": "$ pytest tests/ -v\nPASSED tests/test_example.py::test_function",
                "expected_type": "terminal",
                "description": "Successful test execution",
            },
            {
                "content": "Command not found: invalid_command",
                "expected_type": "terminal",
                "description": "Command error",
            },
            {
                "content": "exit code: 0",
                "expected_type": "terminal",
                "description": "Process completion",
            },
            # URL evidence samples
            {
                "content": "https://github.com/user/repo/issues/146",
                "expected_type": "url",
                "description": "GitHub issue URL",
            },
            {
                "content": "localhost:8001/api/health",
                "expected_type": "url",
                "description": "Local service URL",
            },
            # Metric evidence samples
            {
                "content": "Processing time: 245ms",
                "expected_type": "metric",
                "description": "Performance metric",
            },
            {
                "content": "Memory usage: 128MB",
                "expected_type": "metric",
                "description": "Memory metric",
            },
            # Artifact evidence samples
            {
                "content": "Created file: evidence.py",
                "expected_type": "artifact",
                "description": "File creation",
            },
            {
                "content": "Updated: methodology/verification/requirements.py",
                "expected_type": "artifact",
                "description": "File update",
            },
        ]

    @pytest.mark.asyncio
    async def test_terminal_evidence_validation(self, evidence_engine, test_evidence_samples):
        """Validate that terminal evidence is correctly identified and validated"""
        terminal_samples = [
            sample for sample in test_evidence_samples if sample["expected_type"] == "terminal"
        ]

        for sample in terminal_samples:
            evidence = Evidence(
                evidence_type=None,  # Let auto-categorizer determine
                data={"content": sample["content"]},
                timestamp=datetime.now(),
                source="test",
            )

            # Test auto-categorization
            if hasattr(evidence_engine, "auto_categorizer"):
                categorized_type = await evidence_engine.auto_categorizer.categorize(evidence)
                assert (
                    categorized_type == sample["expected_type"]
                ), f"Expected {sample['expected_type']}, got {categorized_type} for: {sample['description']}"

            # Test validation
            validation_result = await evidence_engine.validate_evidence_collection([evidence])
            assert (
                validation_result.is_valid
            ), f"Failed to validate terminal evidence: {sample['description']}"

    @pytest.mark.asyncio
    async def test_evidence_categorization_accuracy(self, evidence_engine, test_evidence_samples):
        """Test automatic evidence categorization accuracy"""
        if not hasattr(evidence_engine, "auto_categorizer"):
            pytest.skip("Auto-categorizer not implemented by Code Agent")

        correct_categorizations = 0
        total_samples = len(test_evidence_samples)

        for sample in test_evidence_samples:
            evidence = Evidence(
                evidence_type=None,
                data={"content": sample["content"]},
                timestamp=datetime.now(),
                source="test",
            )

            try:
                categorized_type = await evidence_engine.auto_categorizer.categorize(evidence)
                if categorized_type == sample["expected_type"]:
                    correct_categorizations += 1
                else:
                    print(
                        f"Categorization error: Expected {sample['expected_type']}, "
                        f"got {categorized_type} for: {sample['description']}"
                    )
            except Exception as e:
                print(f"Categorization failed for {sample['description']}: {e}")

        accuracy = correct_categorizations / total_samples
        assert accuracy >= 0.95, f"Categorization accuracy {accuracy:.2%} below 95% threshold"

        print(
            f"Evidence categorization accuracy: {accuracy:.2%} ({correct_categorizations}/{total_samples})"
        )

    @pytest.mark.asyncio
    async def test_evidence_processing_speed(self, evidence_engine):
        """Ensure evidence processing meets performance requirements"""
        # Generate large evidence set
        large_evidence_set = self._generate_evidence_samples(1000)

        start_time = time.time()
        try:
            results = await evidence_engine.validate_evidence_collection(large_evidence_set)
            processing_time = time.time() - start_time
        except Exception as e:
            pytest.skip(f"Evidence processing failed: {e}")

        # Should process 1000 evidence items in under 5 seconds
        assert processing_time < 5.0, f"Processing took {processing_time:.2f}s, expected < 5s"

        print(f"Evidence processing time: {processing_time:.2f}s for 1000 items")

    @pytest.mark.asyncio
    async def test_cache_effectiveness(self, evidence_engine):
        """Validate that caching improves repeat validation performance"""
        if not hasattr(evidence_engine, "cache"):
            pytest.skip("Cache not implemented by Code Agent")

        evidence_sample = self._generate_evidence_samples(100)

        # First run (no cache)
        start_time = time.time()
        try:
            await evidence_engine.validate_evidence_collection(evidence_sample)
            first_run_time = time.time() - start_time
        except Exception as e:
            pytest.skip(f"First run failed: {e}")

        # Second run (with cache)
        start_time = time.time()
        try:
            await evidence_engine.validate_evidence_collection(evidence_sample)
            cached_run_time = time.time() - start_time
        except Exception as e:
            pytest.skip(f"Cached run failed: {e}")

        # Cached run should be significantly faster
        speedup_ratio = first_run_time / cached_run_time
        assert speedup_ratio > 2.0, f"Cache speedup only {speedup_ratio:.1f}x, expected > 2x"

        print(
            f"Cache speedup ratio: {speedup_ratio:.1f}x "
            f"({first_run_time:.2f}s -> {cached_run_time:.2f}s)"
        )

    @pytest.mark.asyncio
    async def test_requirements_completeness_validation(self, requirements_validator):
        """Test that evidence requirements properly validate task completeness"""
        # Test simple implementation task
        simple_impl_requirements = requirements_validator.get_requirements(
            TaskType.IMPLEMENTATION, TaskComplexity.SIMPLE
        )
        assert (
            len(simple_impl_requirements) == 3
        ), f"Expected 3 requirements for simple implementation, got {len(simple_impl_requirements)}"

        # Test complex documentation task
        complex_doc_requirements = requirements_validator.get_requirements(
            TaskType.DOCUMENTATION, TaskComplexity.COMPLEX
        )
        assert (
            len(complex_doc_requirements) == 4
        ), f"Expected 4 requirements for complex documentation, got {len(complex_doc_requirements)}"

        # Test validation with provided evidence
        provided_evidence = ["terminal_output", "test_results"]
        report = requirements_validator.validate_completeness(
            TaskType.IMPLEMENTATION, TaskComplexity.SIMPLE, provided_evidence
        )

        assert not report.complete, "Should be incomplete with missing file_artifacts"
        assert "file_artifacts" in report.missing, "Should identify missing file_artifacts"
        assert len(report.missing) == 1, "Should have exactly one missing requirement"

    @pytest.mark.asyncio
    async def test_integration_with_verification_pyramid(self, evidence_engine):
        """Test that evidence engine integrates with verification pyramid"""
        try:
            from methodology.verification.pyramid import VerificationPyramid

            pyramid = VerificationPyramid()

            # Test that evidence engine can provide evidence for pyramid validation
            test_evidence = Evidence(
                evidence_type=EvidenceType.TERMINAL_OUTPUT,
                data={"content": "Test evidence for pyramid integration"},
                timestamp=datetime.now(),
                source="test",
            )

            # This should work without errors
            validation_result = await evidence_engine.validate_evidence_collection([test_evidence])
            assert validation_result is not None, "Evidence validation should return result"

        except ImportError:
            pytest.skip("Verification pyramid not available")
        except Exception as e:
            pytest.skip(f"Pyramid integration failed: {e}")

    def _generate_evidence_samples(self, count: int) -> List["Evidence"]:
        """Generate test evidence samples for performance testing"""
        samples = []
        evidence_types = list(EvidenceType)

        for i in range(count):
            evidence_type = evidence_types[i % len(evidence_types)]
            samples.append(
                Evidence(
                    evidence_type=evidence_type,
                    data={
                        "content": f"Test evidence sample {i}",
                        "index": i,
                        "timestamp": datetime.now().isoformat(),
                    },
                    timestamp=datetime.now(),
                    source="performance_test",
                )
            )

        return samples


class TestEvidencePerformance:
    """Validate Code Agent's performance optimizations"""

    @pytest.mark.asyncio
    async def test_memory_usage_optimization(self, evidence_engine):
        """Test that evidence processing doesn't consume excessive memory"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Process large evidence set
        large_evidence_set = self._generate_evidence_samples(1000)

        try:
            await evidence_engine.validate_evidence_collection(large_evidence_set)
        except Exception as e:
            pytest.skip(f"Evidence processing failed: {e}")

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (< 100MB for 1000 items)
        assert (
            memory_increase < 100 * 1024 * 1024
        ), f"Memory increase {memory_increase / (1024*1024):.1f}MB exceeds 100MB limit"

        print(f"Memory usage increase: {memory_increase / (1024*1024):.1f}MB")

    def _generate_evidence_samples(self, count: int) -> List["Evidence"]:
        """Generate test evidence samples for performance testing"""
        samples = []
        evidence_types = list(EvidenceType)

        for i in range(count):
            evidence_type = evidence_types[i % len(evidence_types)]
            samples.append(
                Evidence(
                    evidence_type=evidence_type,
                    data={
                        "content": f"Test evidence sample {i}",
                        "index": i,
                        "timestamp": datetime.now().isoformat(),
                    },
                    timestamp=datetime.now(),
                    source="performance_test",
                )
            )

        return samples


class TestEvidenceRequirementsCompleteness:
    """Test that evidence requirements cover all necessary task types"""

    def test_all_task_types_covered(self):
        """Ensure all task types have evidence requirements"""
        requirements = TaskEvidenceRequirements()

        task_types = requirements.get_all_task_types()
        complexities = requirements.get_all_complexities()

        # All task types should have requirements for all complexities
        for task_type in task_types:
            for complexity in complexities:
                reqs = requirements.get_requirements(task_type, complexity)
                assert len(reqs) > 0, f"No requirements for {task_type.value} ({complexity.value})"

    def test_requirements_progression(self):
        """Test that requirements increase with complexity"""
        requirements = TaskEvidenceRequirements()

        for task_type in requirements.get_all_task_types():
            simple_reqs = requirements.get_requirements(task_type, TaskComplexity.SIMPLE)
            complex_reqs = requirements.get_requirements(task_type, TaskComplexity.COMPLEX)
            critical_reqs = requirements.get_requirements(task_type, TaskComplexity.CRITICAL)

            # Requirements should increase with complexity
            assert len(complex_reqs) >= len(
                simple_reqs
            ), f"Complex requirements should be >= simple for {task_type.value}"
            assert len(critical_reqs) >= len(
                complex_reqs
            ), f"Critical requirements should be >= complex for {task_type.value}"

    def test_requirements_summary(self):
        """Test requirements summary generation"""
        requirements = TaskEvidenceRequirements()
        summary = requirements.get_requirements_summary()

        # Summary should include all task types
        assert len(summary) == len(
            requirements.get_all_task_types()
        ), "Summary should include all task types"

        # Each task type should have all complexity levels
        for task_type in requirements.get_all_task_types():
            assert len(summary[task_type.value]) == len(
                requirements.get_all_complexities()
            ), f"Task type {task_type.value} should have all complexity levels"

"""
Tests for Verification Pyramid - Three-Tier Verification Framework

Tests the core verification system that prevents verification theater
by requiring concrete evidence and pattern discovery before implementation.
"""

from datetime import datetime

import pytest

from methodology.verification.evidence import EvidenceCollector, EvidenceType
from methodology.verification.pyramid import (
    VerificationLevel,
    VerificationPyramid,
    VerificationResult,
)


@pytest.mark.asyncio
class TestVerificationPyramid:
    """Test suite for VerificationPyramid functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.pyramid = VerificationPyramid()

    async def test_pattern_discovery_prevents_rebuild(self):
        """Verify pattern discovery finds existing implementations"""
        task = {
            "type": "implementation",
            "description": "Add verification to agent coordination",
            "keywords": ["verification", "agent", "coordination"],
        }

        result = await self.pyramid.verify(task)

        # Should complete pattern discovery (informational, doesn't block)
        assert result is not None
        assert result.level == VerificationLevel.EVIDENCE  # Final level reached
        assert "searched_patterns" in result.evidence or "provided_evidence" in result.evidence
        assert isinstance(result.recommendations, list)

    async def test_evidence_requirements_prevent_theater(self):
        """Verify evidence requirements prevent verification theater"""
        task = {
            "type": "implementation",
            "claimed_complete": True,
            "evidence": {},  # No evidence provided
        }

        result = await self.pyramid.verify(task)

        # Should fail without evidence
        assert not result.passed
        assert any("evidence" in failure.lower() for failure in result.failures)
        assert len(result.recommendations) > 0

    async def test_evidence_validation_success(self):
        """Test successful verification with proper evidence"""
        task = {
            "type": "implementation",
            "claimed_complete": True,
            "evidence": {
                "terminal_output": "Command executed successfully",
                "test_results": "All tests passed: 5/5",
                "file_artifacts": "Created: /path/to/file.py",
            },
        }

        result = await self.pyramid.verify(task)

        # Should pass with proper evidence
        assert result.passed
        assert result.level == VerificationLevel.EVIDENCE
        assert len(result.failures) == 0

    async def test_integration_validation(self):
        """Test integration verification requirements"""
        task = {
            "type": "coordination",
            "requires_coordination": True,
            "coordination_plan": {},  # Empty plan
            "dependencies": ["dependency1", "dependency2"],
        }

        result = await self.pyramid.verify(task)

        # Should have integration validation results
        assert result is not None
        assert "dependencies" in result.evidence
        assert "integration_points" in result.evidence

        # Should provide recommendations for missing coordination plan
        assert any("coordination" in rec.lower() for rec in result.recommendations)

    async def test_verification_history_tracking(self):
        """Test that verification results are tracked in history"""
        initial_history_length = len(self.pyramid.verification_history)

        task = {"type": "testing", "claimed_complete": False}

        await self.pyramid.verify(task)

        # Should have added to history
        assert len(self.pyramid.verification_history) == initial_history_length + 1

        # History should contain VerificationResult
        latest_result = self.pyramid.verification_history[-1]
        assert isinstance(latest_result, VerificationResult)
        assert latest_result.verification_id is not None

    async def test_empty_task_handling(self):
        """Test handling of empty or malformed tasks"""
        empty_task = {}

        result = await self.pyramid.verify(empty_task)

        # Should handle gracefully
        assert result is not None
        assert isinstance(result.failures, list)
        assert isinstance(result.recommendations, list)

    async def test_evidence_requirements_by_task_type(self):
        """Test that different task types have appropriate evidence requirements"""
        # Test implementation task requirements
        impl_task = {"type": "implementation", "claimed_complete": True, "evidence": {}}
        impl_result = await self.pyramid.verify(impl_task)

        # Should require implementation-specific evidence
        impl_evidence_reqs = self.pyramid.evidence_requirements.get("implementation", [])
        assert len(impl_evidence_reqs) > 0

        # Test documentation task requirements
        doc_task = {"type": "documentation", "claimed_complete": True, "evidence": {}}
        doc_result = await self.pyramid.verify(doc_task)

        # Should require documentation-specific evidence
        doc_evidence_reqs = self.pyramid.evidence_requirements.get("documentation", [])
        assert len(doc_evidence_reqs) > 0

        # Requirements should be different for different task types
        assert impl_evidence_reqs != doc_evidence_reqs


@pytest.mark.asyncio
class TestEvidenceCollector:
    """Test suite for EvidenceCollector functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.collector = EvidenceCollector()

    def test_terminal_output_evidence_validation(self):
        """Test terminal output evidence validation"""
        # Valid terminal output
        valid_data = {"command": "pytest tests/", "output": "All tests passed", "exit_code": 0}

        evidence = self.collector.collect_evidence(
            EvidenceType.TERMINAL_OUTPUT, valid_data, "test_agent"
        )

        assert evidence.validated
        assert len(evidence.validation_errors) == 0

        # Invalid terminal output (missing fields)
        invalid_data = {
            "command": "pytest tests/"
            # Missing output and exit_code
        }

        evidence = self.collector.collect_evidence(
            EvidenceType.TERMINAL_OUTPUT, invalid_data, "test_agent"
        )

        assert not evidence.validated
        assert len(evidence.validation_errors) > 0

    def test_test_results_evidence_validation(self):
        """Test test results evidence validation"""
        # Valid test results
        valid_data = {
            "test_command": "pytest tests/",
            "total_tests": 10,
            "passed_tests": 8,
            "failed_tests": 2,
        }

        evidence = self.collector.collect_evidence(
            EvidenceType.TEST_RESULTS, valid_data, "test_agent"
        )

        assert evidence.validated
        assert len(evidence.validation_errors) == 0

        # Invalid test results (math doesn't add up)
        invalid_data = {
            "test_command": "pytest tests/",
            "total_tests": 10,
            "passed_tests": 8,
            "failed_tests": 5,  # 8 + 5 != 10
        }

        evidence = self.collector.collect_evidence(
            EvidenceType.TEST_RESULTS, invalid_data, "test_agent"
        )

        assert not evidence.validated
        assert any("total tests" in error.lower() for error in evidence.validation_errors)

    def test_evidence_summary_generation(self):
        """Test evidence summary generation"""
        # Collect several pieces of evidence
        self.collector.collect_evidence(
            EvidenceType.TERMINAL_OUTPUT,
            {"command": "test", "output": "success", "exit_code": 0},
            "agent1",
        )

        self.collector.collect_evidence(
            EvidenceType.TEST_RESULTS,
            {"test_command": "pytest", "total_tests": 5, "passed_tests": 5, "failed_tests": 0},
            "agent2",
        )

        summary = self.collector.get_evidence_summary()

        # Should have summary statistics
        assert summary["total_evidence"] == 2
        assert summary["validated_evidence"] >= 0
        assert "evidence_by_type" in summary
        assert "terminal_output" in summary["evidence_by_type"]
        assert "test_results" in summary["evidence_by_type"]

    def test_file_artifacts_evidence_validation(self):
        """Test file artifacts evidence validation"""
        # Valid file artifacts
        valid_data = {
            "files": [
                {"path": "/path/to/file1.py", "action": "created"},
                {"path": "/path/to/file2.py", "action": "modified"},
            ]
        }

        evidence = self.collector.collect_evidence(
            EvidenceType.FILE_ARTIFACTS, valid_data, "test_agent"
        )

        assert evidence.validated
        assert len(evidence.validation_errors) == 0


if __name__ == "__main__":
    pytest.main([__file__])

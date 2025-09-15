"""
Enforcement Pattern Validation Tests

Comprehensive tests to validate that Code Agent's enforcement patterns
prevent all bypass attempts and provide clear resolution guidance.
"""

import asyncio
from typing import Any, Dict, List

import pytest

# Import Code Agent's enforcement implementation
try:
    from methodology.coordination.enforcement import (
        EnforcementLevel,
        EnforcementPatterns,
        EnforcementRule,
        VerificationRequired,
    )
    from methodology.coordination.exceptions import HandoffBypassError, HandoffValidationError

    ENFORCEMENT_AVAILABLE = True
except ImportError:
    ENFORCEMENT_AVAILABLE = False


class TestEnforcementPatterns:
    """Test enforcement patterns prevent bypass attempts"""

    @pytest.fixture
    def enforcement(self):
        """Initialize enforcement patterns for testing"""
        if not ENFORCEMENT_AVAILABLE:
            pytest.skip("Enforcement patterns not yet implemented by Code Agent")
        return EnforcementPatterns()

    @pytest.fixture
    def task_without_evidence(self):
        """Create task without evidence for testing"""
        return {
            "type": "implementation",
            "description": "Add feature without evidence",
            "evidence": [],  # No evidence - should be blocked
        }

    @pytest.fixture
    def task_with_evidence(self):
        """Create task with evidence for testing"""
        return {
            "type": "implementation",
            "description": "Add feature with evidence",
            "evidence": [
                {"type": "terminal", "content": "$ pytest tests/ -v\nPASSED tests/test_feature.py"},
                {"type": "url", "content": "https://github.com/user/repo/pull/123"},
            ],
            "handoff_protocol_verified": True,
            "evidence_acknowledged": True,
        }

    @pytest.mark.asyncio
    async def test_mandatory_evidence_enforcement(self, enforcement, task_without_evidence):
        """Test that missing evidence blocks handoff"""

        result = await enforcement.enforce_handoff_requirements(
            task=task_without_evidence, from_agent="agent_a", to_agent="agent_b"
        )

        # Verify enforcement blocks handoff
        assert not result["allowed"], "Handoff should be blocked without evidence"
        assert (
            result["enforcement_level"] == EnforcementLevel.STRICT
        ), "Should be strict enforcement"

        # Verify violations are recorded
        assert len(result["violations"]) > 0, "Should have violations"
        assert any(
            "evidence" in v["message"].lower() for v in result["violations"]
        ), "Should mention evidence"

        # Verify required actions are provided
        assert len(result["required_actions"]) > 0, "Should provide required actions"
        assert any(
            "evidence" in action.lower() for action in result["required_actions"]
        ), "Should mention evidence in actions"

    @pytest.mark.asyncio
    async def test_evidence_acknowledgment_enforcement(self, enforcement):
        """Test that evidence must be acknowledged"""

        task_without_acknowledgment = {
            "type": "implementation",
            "evidence": [{"type": "terminal", "content": "tests passing"}],
            "evidence_acknowledged": False,  # Not acknowledged - should be blocked
        }

        result = await enforcement.enforce_handoff_requirements(
            task=task_without_acknowledgment, from_agent="agent_a", to_agent="agent_b"
        )

        # Verify enforcement blocks handoff
        assert not result["allowed"], "Handoff should be blocked without acknowledgment"
        assert (
            result["enforcement_level"] == EnforcementLevel.STRICT
        ), "Should be strict enforcement"

        # Verify acknowledgment violation is recorded
        assert any(
            "acknowledge" in v["message"].lower() for v in result["violations"]
        ), "Should mention acknowledgment"

    @pytest.mark.asyncio
    async def test_handoff_protocol_bypass_prevention(self, enforcement):
        """Test that direct task assignment bypasses are prevented"""

        task_without_protocol = {
            "type": "implementation",
            "evidence": [{"type": "terminal", "content": "tests passing"}],
            "handoff_protocol_verified": False,  # Not using protocol - should be blocked
        }

        result = await enforcement.enforce_handoff_requirements(
            task=task_without_protocol, from_agent="agent_a", to_agent="agent_b"
        )

        # Verify enforcement blocks handoff
        assert not result["allowed"], "Handoff should be blocked without protocol verification"
        assert (
            result["enforcement_level"] == EnforcementLevel.STRICT
        ), "Should be strict enforcement"

        # Verify protocol violation is recorded
        assert any(
            "protocol" in v["message"].lower() or "bypass" in v["message"].lower()
            for v in result["violations"]
        ), "Should mention protocol or bypass"

    @pytest.mark.asyncio
    async def test_valid_task_passes_enforcement(self, enforcement, task_with_evidence):
        """Test that valid tasks pass enforcement"""

        result = await enforcement.enforce_handoff_requirements(
            task=task_with_evidence, from_agent="agent_a", to_agent="agent_b"
        )

        # Verify enforcement allows handoff
        assert result["allowed"], "Valid task should pass enforcement"
        assert len(result["violations"]) == 0, "Should have no violations"
        assert len(result["required_actions"]) == 0, "Should have no required actions"

    def test_enforcement_prompt_generation(self, enforcement):
        """Test enforcement prompt provides clear guidance"""

        violations = [
            {
                "rule": "mandatory_evidence",
                "message": "Handoff blocked: No evidence provided",
                "level": EnforcementLevel.STRICT,
                "resolution_steps": [
                    "Add terminal output evidence to task",
                    "Include test results or validation proof",
                    "Provide concrete deliverable artifacts",
                    "Run verification pyramid on task before handoff",
                ],
            }
        ]

        prompt = enforcement.generate_enforcement_prompt(violations)

        # Verify prompt structure
        assert "MANDATORY ENFORCEMENT REQUIREMENTS" in prompt, "Should have mandatory header"
        assert "blocked due to" in prompt, "Should mention blocking"
        assert "Add terminal output evidence" in prompt, "Should include resolution steps"
        assert "not optional" in prompt.lower(), "Should emphasize mandatory nature"
        assert "MUST address ALL violations" in prompt, "Should require addressing all violations"

    @pytest.mark.asyncio
    async def test_verification_decorator_enforcement(self, enforcement):
        """Test mandatory verification decorator blocks functions"""

        @EnforcementPatterns.mandatory_verification_decorator
        async def test_function(task):
            return {"status": "completed", "task": task}

        # Should block without evidence
        with pytest.raises(VerificationRequired) as exc_info:
            await test_function({"type": "implementation"})  # No evidence

        # Verify error message and resolution steps
        error_message = str(exc_info.value).lower()
        assert "evidence" in error_message, "Should mention evidence requirement"
        assert len(exc_info.value.resolution_steps) > 0, "Should provide resolution steps"

        # Should proceed with evidence
        result = await test_function({"type": "implementation", "evidence": ["test_output"]})
        assert result["status"] == "completed", "Should complete with evidence"

    @pytest.mark.asyncio
    async def test_enforcement_rule_creation(self, enforcement):
        """Test custom enforcement rule creation"""

        # Create custom rule
        def custom_check(task, from_agent, to_agent):
            return "custom_field" not in task  # Violated if custom_field missing

        custom_rule = EnforcementRule(
            name="custom_validation",
            description="Custom validation rule",
            level=EnforcementLevel.STRICT,
            check_function=custom_check,
            violation_message="Custom field required",
            resolution_steps=["Add custom_field to task"],
        )

        # Add rule
        enforcement.add_rule(custom_rule)

        # Test rule enforcement
        task_without_custom = {"type": "implementation", "evidence": ["test"]}

        result = await enforcement.enforce_handoff_requirements(
            task=task_without_custom, from_agent="agent_a", to_agent="agent_b"
        )

        # Should have custom rule violation
        assert not result["allowed"], "Should be blocked by custom rule"
        assert any(
            "custom" in v["message"].lower() for v in result["violations"]
        ), "Should mention custom rule"

    @pytest.mark.asyncio
    async def test_violation_logging(self, enforcement, task_without_evidence):
        """Test that violations are properly logged"""

        initial_violations = len(enforcement.violation_history)

        # Trigger violation
        await enforcement.enforce_handoff_requirements(
            task=task_without_evidence, from_agent="agent_a", to_agent="agent_b"
        )

        # Verify violation was logged
        assert len(enforcement.violation_history) > initial_violations, "Should log violation"

        # Check violation record structure
        latest_violation = enforcement.violation_history[-1]
        assert "timestamp" in latest_violation, "Should have timestamp"
        assert "from_agent" in latest_violation, "Should have from_agent"
        assert "to_agent" in latest_violation, "Should have to_agent"
        assert "violations" in latest_violation, "Should have violations"
        assert "enforcement_level" in latest_violation, "Should have enforcement level"

    @pytest.mark.asyncio
    async def test_multiple_violations_handling(self, enforcement):
        """Test handling of multiple violations"""

        task_with_multiple_violations = {
            "type": "implementation",
            "evidence": [],  # No evidence
            "evidence_acknowledged": False,  # Not acknowledged
            "handoff_protocol_verified": False,  # Not verified
        }

        result = await enforcement.enforce_handoff_requirements(
            task=task_with_multiple_violations, from_agent="agent_a", to_agent="agent_b"
        )

        # Should have multiple violations
        assert not result["allowed"], "Should be blocked with multiple violations"
        assert len(result["violations"]) > 1, "Should have multiple violations"
        assert len(result["required_actions"]) > 1, "Should have multiple required actions"

        # Verify all violation types are present
        violation_messages = [v["message"].lower() for v in result["violations"]]
        assert any(
            "evidence" in msg for msg in violation_messages
        ), "Should have evidence violation"
        assert any(
            "acknowledge" in msg for msg in violation_messages
        ), "Should have acknowledgment violation"
        assert any(
            "protocol" in msg or "bypass" in msg for msg in violation_messages
        ), "Should have protocol violation"

    def test_enforcement_level_enum(self):
        """Test enforcement level enum completeness"""
        if not ENFORCEMENT_AVAILABLE:
            pytest.skip("Enforcement patterns not yet implemented by Code Agent")

        # Verify all required levels exist
        required_levels = ["STRICT", "PROGRESSIVE", "ADVISORY"]
        for level_name in required_levels:
            assert hasattr(EnforcementLevel, level_name), f"Missing {level_name} level"
            level = getattr(EnforcementLevel, level_name)
            assert level.value == level_name.lower(), f"Level value should be lowercase"

    @pytest.mark.asyncio
    async def test_enforcement_performance(self, enforcement, task_without_evidence):
        """Test enforcement performance is acceptable"""
        import time

        # Measure enforcement time
        start_time = time.time()

        result = await enforcement.enforce_handoff_requirements(
            task=task_without_evidence, from_agent="agent_a", to_agent="agent_b"
        )

        end_time = time.time()
        enforcement_time = end_time - start_time

        # Should complete quickly
        assert (
            enforcement_time < 0.1
        ), f"Enforcement time {enforcement_time:.3f}s exceeds 0.1s threshold"
        assert result is not None, "Should return result"

    @pytest.mark.asyncio
    async def test_concurrent_enforcement(self, enforcement):
        """Test concurrent enforcement handling"""

        # Create multiple concurrent enforcement requests
        tasks = []
        for i in range(5):
            task = enforcement.enforce_handoff_requirements(
                task={"type": "test", "evidence": []},
                from_agent=f"agent_{i}",
                to_agent=f"agent_{i+1}",
            )
            tasks.append(task)

        # Execute concurrently
        results = await asyncio.gather(*tasks)

        # Verify all completed
        assert len(results) == 5, "Should handle all concurrent requests"
        for result in results:
            assert not result["allowed"], "All should be blocked without evidence"
            assert (
                result["enforcement_level"] == EnforcementLevel.STRICT
            ), "Should be strict enforcement"

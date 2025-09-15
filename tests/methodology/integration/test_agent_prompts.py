"""
Agent Prompt Testing

Comprehensive tests to validate agent-specific prompt generation
and coordination capabilities in the AgentCoordinator bridge.
"""

from typing import Any, Dict, List

import pytest

# Import Code Agent's agent bridge implementation (to be implemented)
try:
    from methodology.integration.agent_bridge import (
        AgentCapabilities,
        AgentCoordinator,
        AgentType,
        CoordinationMethod,
        CoordinationTask,
    )

    AGENT_BRIDGE_AVAILABLE = True
except ImportError:
    AGENT_BRIDGE_AVAILABLE = False


class TestAgentPrompts:
    """Test agent-specific prompt generation"""

    @pytest.fixture
    def coordinator(self):
        """Initialize agent coordinator for testing"""
        if not AGENT_BRIDGE_AVAILABLE:
            pytest.skip("Agent bridge not yet implemented by Code Agent")
        return AgentCoordinator()

    @pytest.fixture
    def sample_task(self):
        """Create sample task for testing"""
        return {
            "type": "implementation",
            "description": "Implement feature with TDD approach",
            "complexity": "medium",
        }

    @pytest.fixture
    def evidence_requirements(self):
        """Create evidence requirements for testing"""
        return ["terminal_output", "test_results", "file_artifacts"]

    def test_high_context_agent_prompt(self, coordinator, sample_task, evidence_requirements):
        """Test prompt generation for high-context agents"""

        prompt = coordinator._generate_agent_prompt(
            "code_agent", sample_task, evidence_requirements
        )

        # Verify high-context prompt characteristics
        assert (
            "SYSTEMATIC METHODOLOGY EXECUTION" in prompt
        ), "Should have systematic methodology header"
        assert "Excellence Flywheel methodology" in prompt, "Should mention Excellence Flywheel"
        assert "VERIFICATION FIRST" in prompt, "Should emphasize verification first"
        assert (
            "systematic verification principles" in prompt
        ), "Should mention systematic principles"
        assert (
            "No completion without concrete evidence" in prompt
        ), "Should emphasize evidence requirement"

        # Verify task information is included
        assert sample_task["description"] in prompt, "Should include task description"

        # Verify evidence requirements are formatted
        assert "EVIDENCE REQUIREMENTS" in prompt, "Should have evidence requirements section"
        assert (
            "terminal_output" in prompt.lower() or "terminal command" in prompt.lower()
        ), "Should mention terminal evidence"

    def test_limited_context_agent_prompt(self, coordinator, sample_task, evidence_requirements):
        """Test prompt generation for limited-context agents"""

        prompt = coordinator._generate_agent_prompt(
            "cursor_agent", sample_task, evidence_requirements
        )

        # Verify limited-context prompt characteristics
        assert (
            "MANDATORY VERIFICATION REQUIRED" in prompt
        ), "Should have mandatory verification header"
        assert "STOP CONDITIONS" in prompt, "Should have stop conditions section"
        assert "If assuming configuration" in prompt, "Should warn about assumptions"
        assert "GREP before implementing" in prompt, "Should suggest verification commands"
        assert "Never assume what can be verified" in prompt, "Should emphasize verification"
        assert "ASK rather than assume" in prompt, "Should encourage asking questions"

        # Verify step-by-step structure
        assert "STEP 1:" in prompt, "Should have step-by-step structure"
        assert "STEP 2:" in prompt, "Should have multiple steps"
        assert "STEP 3:" in prompt, "Should have implementation step"

        # Verify task information is included
        assert sample_task["description"] in prompt, "Should include task description"

    def test_unknown_agent_strict_prompt(self, coordinator, sample_task, evidence_requirements):
        """Test strict prompt generation for unknown agents"""

        prompt = coordinator._generate_agent_prompt(
            "unknown_agent", sample_task, evidence_requirements
        )

        # Verify strict prompt characteristics
        assert "STRICT VERIFICATION PROTOCOL" in prompt, "Should have strict protocol header"
        assert "MANDATORY REQUIREMENTS" in prompt, "Should have mandatory requirements"
        assert "This is not optional" in prompt, "Should emphasize non-optional nature"
        assert "Progress blocked without verification" in prompt, "Should mention blocking"

        # Verify verification requirements
        assert (
            "Execute verification commands BEFORE implementation" in prompt
        ), "Should require pre-verification"
        assert "Provide concrete evidence for ALL claims" in prompt, "Should require evidence"
        assert "No assumptions - verify everything" in prompt, "Should prohibit assumptions"
        assert (
            "Terminal output required for validation" in prompt
        ), "Should require terminal evidence"

        # Verify task information is included
        assert sample_task["description"] in prompt, "Should include task description"

    def test_agent_capabilities_registration(self, coordinator):
        """Test agent capabilities registration and retrieval"""

        # Verify known agents are registered
        assert "code_agent" in coordinator.agent_capabilities, "Should have code_agent registered"
        assert (
            "cursor_agent" in coordinator.agent_capabilities
        ), "Should have cursor_agent registered"
        assert (
            "lead_developer" in coordinator.agent_capabilities
        ), "Should have lead_developer registered"

        # Verify agent capabilities structure
        code_capabilities = coordinator.agent_capabilities["code_agent"]
        assert isinstance(
            code_capabilities, AgentCapabilities
        ), "Should be AgentCapabilities instance"
        assert code_capabilities.agent_type == AgentType.CODE, "Should have correct agent type"
        assert code_capabilities.context_level == "HIGH", "Should have high context level"
        assert code_capabilities.methodology_awareness == True, "Should be methodology aware"
        assert (
            len(code_capabilities.verification_requirements) > 0
        ), "Should have verification requirements"
        assert (
            len(code_capabilities.preferred_evidence_types) > 0
        ), "Should have preferred evidence types"

        # Verify cursor agent capabilities
        cursor_capabilities = coordinator.agent_capabilities["cursor_agent"]
        assert cursor_capabilities.context_level == "LIMITED", "Should have limited context level"
        assert cursor_capabilities.methodology_awareness == False, "Should not be methodology aware"
        assert (
            "explicit_verification" in cursor_capabilities.verification_requirements
        ), "Should require explicit verification"

    def test_prompt_adaptation_to_evidence_requirements(self, coordinator, sample_task):
        """Test prompt adaptation based on evidence requirements"""

        # Test with different evidence requirements
        terminal_only = ["terminal_output"]
        comprehensive = ["terminal_output", "test_results", "file_artifacts", "cross_validation"]

        prompt_terminal = coordinator._generate_agent_prompt(
            "code_agent", sample_task, terminal_only
        )
        prompt_comprehensive = coordinator._generate_agent_prompt(
            "code_agent", sample_task, comprehensive
        )

        # Verify prompts are different based on requirements
        assert (
            prompt_terminal != prompt_comprehensive
        ), "Prompts should differ based on evidence requirements"

        # Verify comprehensive prompt includes more evidence types
        assert (
            "cross_validation" in prompt_comprehensive.lower()
            or "validation" in prompt_comprehensive.lower()
        ), "Should mention cross-validation"
        assert (
            "test_results" in prompt_comprehensive.lower() or "test" in prompt_comprehensive.lower()
        ), "Should mention test results"

    def test_prompt_consistency_for_same_agent(
        self, coordinator, sample_task, evidence_requirements
    ):
        """Test prompt consistency for same agent and requirements"""

        # Generate same prompt multiple times
        prompt1 = coordinator._generate_agent_prompt(
            "code_agent", sample_task, evidence_requirements
        )
        prompt2 = coordinator._generate_agent_prompt(
            "code_agent", sample_task, evidence_requirements
        )

        # Should be consistent
        assert prompt1 == prompt2, "Prompts should be consistent for same agent and requirements"

    def test_prompt_differentiation_between_agents(
        self, coordinator, sample_task, evidence_requirements
    ):
        """Test that prompts are differentiated between agent types"""

        code_prompt = coordinator._generate_agent_prompt(
            "code_agent", sample_task, evidence_requirements
        )
        cursor_prompt = coordinator._generate_agent_prompt(
            "cursor_agent", sample_task, evidence_requirements
        )
        unknown_prompt = coordinator._generate_agent_prompt(
            "unknown_agent", sample_task, evidence_requirements
        )

        # All prompts should be different
        assert code_prompt != cursor_prompt, "Code and cursor prompts should differ"
        assert code_prompt != unknown_prompt, "Code and unknown prompts should differ"
        assert cursor_prompt != unknown_prompt, "Cursor and unknown prompts should differ"

        # Verify specific differences
        assert "SYSTEMATIC METHODOLOGY EXECUTION" in code_prompt, "Code prompt should be systematic"
        assert (
            "MANDATORY VERIFICATION REQUIRED" in cursor_prompt
        ), "Cursor prompt should be mandatory"
        assert "STRICT VERIFICATION PROTOCOL" in unknown_prompt, "Unknown prompt should be strict"

    def test_verification_commands_formatting(self, coordinator):
        """Test verification commands formatting"""

        requirements = ["terminal_output", "test_results", "file_artifacts"]
        formatted = coordinator._format_verification_commands(requirements)

        # Verify formatting includes relevant commands
        assert "terminal" in formatted.lower(), "Should mention terminal commands"
        assert (
            "pytest" in formatted.lower() or "test" in formatted.lower()
        ), "Should mention testing"
        assert (
            "file" in formatted.lower() or "artifact" in formatted.lower()
        ), "Should mention file artifacts"

    def test_evidence_requirements_formatting(self, coordinator):
        """Test evidence requirements formatting"""

        requirements = ["terminal_output", "test_results", "file_artifacts"]
        formatted = coordinator._format_evidence_requirements(requirements)

        # Verify formatting includes evidence types
        assert "terminal" in formatted.lower(), "Should mention terminal evidence"
        assert "test" in formatted.lower(), "Should mention test evidence"
        assert "file" in formatted.lower(), "Should mention file evidence"

        # Verify bullet point format
        assert formatted.count("-") >= len(
            requirements
        ), "Should have bullet points for each requirement"

    def test_custom_agent_registration(self, coordinator):
        """Test custom agent registration"""

        # Register custom agent
        custom_capabilities = AgentCapabilities(
            agent_type=AgentType.UNKNOWN,
            context_level="MEDIUM",
            methodology_awareness=True,
            verification_requirements=["custom_verification"],
            preferred_evidence_types=["custom_evidence"],
        )

        coordinator.register_agent_capabilities("custom_agent", custom_capabilities)

        # Verify registration
        assert (
            "custom_agent" in coordinator.agent_capabilities
        ), "Should have custom agent registered"
        assert (
            coordinator.agent_capabilities["custom_agent"] == custom_capabilities
        ), "Should match registered capabilities"

        # Test prompt generation for custom agent
        task = {"description": "Custom agent task"}
        prompt = coordinator._generate_agent_prompt("custom_agent", task, ["custom_verification"])

        # Should generate appropriate prompt based on capabilities
        assert (
            "custom_verification" in prompt.lower() or "verification" in prompt.lower()
        ), "Should include verification requirements"

    def test_prompt_length_and_completeness(self, coordinator, sample_task, evidence_requirements):
        """Test prompt length and completeness"""

        prompt = coordinator._generate_agent_prompt(
            "code_agent", sample_task, evidence_requirements
        )

        # Verify prompt is comprehensive
        assert len(prompt) > 200, "Prompt should be comprehensive (at least 200 characters)"
        assert len(prompt.split("\n")) > 10, "Prompt should have multiple lines"

        # Verify all required sections are present
        required_sections = ["VERIFICATION", "EVIDENCE", "TASK"]
        for section in required_sections:
            assert any(
                section in line for line in prompt.split("\n")
            ), f"Should contain {section} section"

    def test_prompt_error_handling(self, coordinator):
        """Test prompt generation error handling"""

        # Test with None task
        with pytest.raises((AttributeError, TypeError)):
            coordinator._generate_agent_prompt("code_agent", None, ["terminal_output"])

        # Test with empty evidence requirements
        prompt = coordinator._generate_agent_prompt("code_agent", {"description": "test"}, [])
        assert len(prompt) > 0, "Should handle empty evidence requirements gracefully"

        # Test with invalid agent ID
        prompt = coordinator._generate_agent_prompt(
            "invalid_agent", {"description": "test"}, ["terminal_output"]
        )
        assert len(prompt) > 0, "Should handle invalid agent ID gracefully"
        assert "STRICT VERIFICATION PROTOCOL" in prompt, "Should fall back to strict protocol"

"""
Enhanced Orchestration Integration Tests

Test integration between enforcement patterns and orchestration bridge
to ensure existing functionality is preserved while adding enforcement.
"""

import asyncio
from typing import Any, Dict, List

import pytest

# Import Code Agent's enhanced orchestration implementation
try:
    from methodology.coordination.enforcement import EnforcementLevel
    from methodology.integration.orchestration_bridge import EnhancedOrchestrationBridge

    ENHANCED_ORCHESTRATION_AVAILABLE = True
except ImportError:
    ENHANCED_ORCHESTRATION_AVAILABLE = False

# Import existing orchestration components
try:
    from services.orchestration.multi_agent_coordinator import MultiAgentCoordinator

    EXISTING_ORCHESTRATION_AVAILABLE = True
except ImportError:
    EXISTING_ORCHESTRATION_AVAILABLE = False


class TestEnhancedOrchestration:
    """Test orchestration bridge enforcement integration"""

    @pytest.fixture
    def enhanced_bridge(self):
        """Initialize enhanced orchestration bridge for testing"""
        if not ENHANCED_ORCHESTRATION_AVAILABLE:
            pytest.skip("Enhanced orchestration bridge not yet implemented by Code Agent")
        return EnhancedOrchestrationBridge()

    @pytest.fixture
    def invalid_coordination_task(self):
        """Create invalid coordination task for testing"""
        return {
            "agents": ["agent_a", "agent_b"],
            "task": "implementation",
            "evidence": [],  # No evidence - should be blocked
        }

    @pytest.fixture
    def valid_coordination_task(self):
        """Create valid coordination task for testing"""
        return {
            "agents": ["agent_a", "agent_b"],
            "task": "implementation",
            "evidence": [
                {"type": "terminal", "content": "tests passing"},
                {"type": "url", "content": "https://github.com/pr/123"},
            ],
            "handoff_protocol_verified": True,
            "evidence_acknowledged": True,
        }

    @pytest.mark.asyncio
    async def test_enforcement_blocks_invalid_handoffs(
        self, enhanced_bridge, invalid_coordination_task
    ):
        """Test orchestration bridge blocks invalid handoffs"""

        result = await enhanced_bridge.coordinate_with_enforcement(invalid_coordination_task)

        # Verify enforcement blocks handoff
        assert result["status"] == "blocked", "Should block invalid handoff"
        assert "enforcement_violations" in result, "Should have enforcement violations"
        assert "enforcement_prompt" in result, "Should have enforcement prompt"
        assert len(result["required_actions"]) > 0, "Should have required actions"

        # Verify enforcement prompt structure
        prompt = result["enforcement_prompt"]
        assert "MANDATORY ENFORCEMENT REQUIREMENTS" in prompt, "Should have mandatory header"
        assert "blocked due to" in prompt, "Should mention blocking"
        assert "not optional" in prompt.lower(), "Should emphasize mandatory nature"

    @pytest.mark.asyncio
    async def test_valid_handoff_proceeds(self, enhanced_bridge, valid_coordination_task):
        """Test valid handoffs proceed through enforcement"""

        result = await enhanced_bridge.coordinate_with_enforcement(valid_coordination_task)

        # Verify handoff proceeds
        assert result["status"] == "success", "Valid handoff should succeed"
        assert result["verification_enforced"] == True, "Should enforce verification"
        assert result["evidence_count"] > 0, "Should have evidence count"
        assert "handoff_package" in result, "Should have handoff package"

    @pytest.mark.asyncio
    async def test_insufficient_agents_handling(self, enhanced_bridge):
        """Test handling of insufficient agents"""

        insufficient_agents_task = {
            "agents": ["agent_a"],  # Only one agent
            "task": "implementation",
            "evidence": ["test"],
        }

        result = await enhanced_bridge.coordinate_with_enforcement(insufficient_agents_task)

        # Should return error for insufficient agents
        assert result["status"] == "error", "Should return error for insufficient agents"
        assert "Need at least 2 agents" in result["error"], "Should mention agent requirement"

    @pytest.mark.asyncio
    async def test_enforcement_violation_details(self, enhanced_bridge, invalid_coordination_task):
        """Test detailed enforcement violation information"""

        result = await enhanced_bridge.coordinate_with_enforcement(invalid_coordination_task)

        # Verify violation details
        violations = result["enforcement_violations"]
        assert len(violations) > 0, "Should have violations"

        for violation in violations:
            assert "rule" in violation, "Should have rule name"
            assert "message" in violation, "Should have violation message"
            assert "level" in violation, "Should have enforcement level"
            assert "resolution_steps" in violation, "Should have resolution steps"
            assert len(violation["resolution_steps"]) > 0, "Should have actionable steps"

    @pytest.mark.asyncio
    async def test_required_actions_completeness(self, enhanced_bridge, invalid_coordination_task):
        """Test that required actions are complete and actionable"""

        result = await enhanced_bridge.coordinate_with_enforcement(invalid_coordination_task)

        # Verify required actions
        required_actions = result["required_actions"]
        assert len(required_actions) > 0, "Should have required actions"

        # Check for specific action types
        action_text = " ".join(required_actions).lower()
        assert "evidence" in action_text, "Should mention evidence requirements"
        assert (
            "verification" in action_text or "validate" in action_text
        ), "Should mention verification"

        # Verify actions are actionable
        for action in required_actions:
            assert len(action.strip()) > 10, "Actions should be descriptive"
            assert not action.endswith("."), "Actions should not end with periods (imperative mood)"

    @pytest.mark.asyncio
    async def test_enforcement_prompt_quality(self, enhanced_bridge, invalid_coordination_task):
        """Test enforcement prompt provides clear, actionable guidance"""

        result = await enhanced_bridge.coordinate_with_enforcement(invalid_coordination_task)

        prompt = result["enforcement_prompt"]

        # Verify prompt structure and content
        assert len(prompt) > 100, "Prompt should be comprehensive"
        assert "MANDATORY" in prompt, "Should emphasize mandatory nature"
        assert "blocked" in prompt, "Should clearly state blocking"
        assert "MUST" in prompt, "Should use imperative language"
        assert "not optional" in prompt.lower(), "Should emphasize non-optional nature"

        # Verify prompt includes specific guidance
        assert "evidence" in prompt.lower(), "Should mention evidence"
        assert (
            "verification" in prompt.lower() or "validate" in prompt.lower()
        ), "Should mention verification"

        # Verify prompt is actionable
        assert (
            "Add" in prompt or "Include" in prompt or "Provide" in prompt
        ), "Should have actionable verbs"

    @pytest.mark.asyncio
    async def test_multiple_agent_coordination(self, enhanced_bridge):
        """Test coordination with multiple agents"""

        multi_agent_task = {
            "agents": ["agent_a", "agent_b", "agent_c"],
            "task": "implementation",
            "evidence": [
                {"type": "terminal", "content": "tests passing"},
                {"type": "url", "content": "https://github.com/pr/123"},
            ],
            "handoff_protocol_verified": True,
            "evidence_acknowledged": True,
        }

        result = await enhanced_bridge.coordinate_with_enforcement(multi_agent_task)

        # Should handle multiple agents
        assert result["status"] == "success", "Should handle multiple agents"
        assert result["verification_enforced"] == True, "Should enforce verification"
        assert result["evidence_count"] > 0, "Should have evidence count"

    @pytest.mark.asyncio
    async def test_enforcement_performance(self, enhanced_bridge, invalid_coordination_task):
        """Test enforcement performance is acceptable"""
        import time

        # Measure enforcement time
        start_time = time.time()

        result = await enhanced_bridge.coordinate_with_enforcement(invalid_coordination_task)

        end_time = time.time()
        enforcement_time = end_time - start_time

        # Should complete quickly
        assert (
            enforcement_time < 0.2
        ), f"Enforcement time {enforcement_time:.3f}s exceeds 0.2s threshold"
        assert result is not None, "Should return result"

    @pytest.mark.asyncio
    async def test_concurrent_enforcement_handling(self, enhanced_bridge):
        """Test concurrent enforcement handling"""

        # Create multiple concurrent enforcement requests
        tasks = []
        for i in range(3):
            task = enhanced_bridge.coordinate_with_enforcement(
                {
                    "agents": [f"agent_{i}", f"agent_{i+1}"],
                    "task": "implementation",
                    "evidence": [],  # No evidence - should be blocked
                }
            )
            tasks.append(task)

        # Execute concurrently
        results = await asyncio.gather(*tasks)

        # Verify all completed
        assert len(results) == 3, "Should handle all concurrent requests"
        for result in results:
            assert result["status"] == "blocked", "All should be blocked without evidence"
            assert "enforcement_violations" in result, "Should have enforcement violations"

    @pytest.mark.asyncio
    async def test_error_handling_robustness(self, enhanced_bridge):
        """Test error handling robustness"""

        # Test with None task
        with pytest.raises((TypeError, ValueError, AttributeError)):
            await enhanced_bridge.coordinate_with_enforcement(None)

        # Test with empty task
        empty_task = {}
        result = await enhanced_bridge.coordinate_with_enforcement(empty_task)
        assert result["status"] in ["blocked", "error"], "Should handle empty task gracefully"

        # Test with malformed task
        malformed_task = {"agents": "not_a_list", "task": "implementation"}  # Should be list
        result = await enhanced_bridge.coordinate_with_enforcement(malformed_task)
        assert result["status"] in ["blocked", "error"], "Should handle malformed task gracefully"

    @pytest.mark.asyncio
    async def test_existing_functionality_preservation(
        self, enhanced_bridge, valid_coordination_task
    ):
        """Test that existing orchestration functionality is preserved"""

        result = await enhanced_bridge.coordinate_with_enforcement(valid_coordination_task)

        # Verify existing functionality is preserved
        assert result["status"] == "success", "Should maintain success status"
        assert "handoff_package" in result, "Should maintain handoff package"
        assert "verification_enforced" in result, "Should add enforcement indicator"
        assert "evidence_count" in result, "Should add evidence count"

        # Verify handoff package structure
        handoff_package = result["handoff_package"]
        assert handoff_package is not None, "Should have valid handoff package"

    def test_enhanced_bridge_initialization(self):
        """Test enhanced bridge initializes correctly"""
        if not ENHANCED_ORCHESTRATION_AVAILABLE:
            pytest.skip("Enhanced orchestration bridge not yet implemented by Code Agent")

        bridge = EnhancedOrchestrationBridge()

        # Verify components are initialized
        assert hasattr(bridge, "enforcement"), "Should have enforcement component"
        assert hasattr(bridge, "protocol"), "Should have protocol component"
        assert bridge.enforcement is not None, "Enforcement should be initialized"
        assert bridge.protocol is not None, "Protocol should be initialized"


class TestOrchestrationIntegrationCompatibility:
    """Test compatibility with existing orchestration infrastructure"""

    @pytest.mark.asyncio
    async def test_existing_coordinator_compatibility(self):
        """Test compatibility with existing multi-agent coordinator"""
        if not EXISTING_ORCHESTRATION_AVAILABLE:
            pytest.skip("Existing orchestration not available")

        # This test would verify that the enhanced bridge doesn't break
        # existing orchestration functionality
        coordinator = MultiAgentCoordinator()
        assert coordinator is not None, "Should be able to create existing coordinator"

        # Additional compatibility tests would go here
        # depending on the existing coordinator's API

    @pytest.mark.asyncio
    async def test_enforcement_integration_with_existing_patterns(self):
        """Test enforcement integrates with existing orchestration patterns"""
        if not ENHANCED_ORCHESTRATION_AVAILABLE:
            pytest.skip("Enhanced orchestration bridge not yet implemented by Code Agent")

        bridge = EnhancedOrchestrationBridge()

        # Test various existing coordination patterns
        patterns = ["sequential_execution", "parallel_execution", "conditional_execution"]

        for pattern in patterns:
            task = {
                "agents": ["agent_a", "agent_b"],
                "coordination_pattern": pattern,
                "task": "implementation",
                "evidence": [{"type": "terminal", "content": f"{pattern} complete"}],
                "handoff_protocol_verified": True,
                "evidence_acknowledged": True,
            }

            result = await bridge.coordinate_with_enforcement(task)

            # Should handle existing patterns
            assert result["status"] == "success", f"Should handle {pattern} pattern"
            assert result["verification_enforced"] == True, "Should enforce verification"

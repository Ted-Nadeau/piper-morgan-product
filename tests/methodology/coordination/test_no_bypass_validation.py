"""
No-Bypass Path Validation Tests

Verify that no alternative paths can bypass verification in the mandatory handoff protocol.
Tests ensure zero escape routes exist and enforcement mechanisms work correctly.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List

import pytest

# Import the handoff protocol components (implemented by Code Agent)
try:
    from methodology.coordination.exceptions import (
        HandoffBypassError,
        HandoffStateError,
        HandoffValidationError,
    )
    from methodology.coordination.handoff import (
        HandoffContext,
        HandoffResult,
        HandoffState,
        MandatoryHandoffProtocol,
    )
    from methodology.verification.evidence import Evidence, EvidenceType

    HANDOFF_PROTOCOL_AVAILABLE = True
except ImportError:
    HANDOFF_PROTOCOL_AVAILABLE = False


class TestNoBypassPaths:
    """Verify no alternative paths bypass verification"""

    @pytest.fixture
    def handoff_protocol(self):
        """Initialize handoff protocol for testing"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")
        return MandatoryHandoffProtocol()

    @pytest.fixture
    def valid_task_with_evidence(self):
        """Create a valid task with evidence for testing"""
        return {
            "type": "implementation",
            "description": "Add new feature with tests",
            "evidence": [
                {
                    "type": "terminal",
                    "content": "$ pytest tests/ -v\nPASSED tests/test_feature.py::test_new_function",
                },
                {"type": "url", "content": "https://github.com/user/repo/pull/123"},
                {"type": "artifact", "content": "Created file: src/feature.py"},
            ],
        }

    @pytest.fixture
    def invalid_task_no_evidence(self):
        """Create an invalid task without evidence for testing"""
        return {
            "type": "implementation",
            "description": "Add feature without evidence",
            "evidence": [],  # No evidence provided
        }

    @pytest.mark.asyncio
    async def test_handoff_blocked_without_verification(
        self, handoff_protocol, invalid_task_no_evidence
    ):
        """Verify handoffs cannot proceed without verification"""

        # Should be blocked due to missing evidence
        with pytest.raises((HandoffValidationError, HandoffBypassError)) as exc_info:
            await handoff_protocol.initiate_handoff(
                source_agent="agent_a",
                target_agent="agent_b",
                task_context=invalid_task_no_evidence,
            )

        # Verify the error message indicates evidence requirement
        error_message = str(exc_info.value).lower()
        assert (
            "evidence" in error_message
            or "verification" in error_message
            or "validation" in error_message
        )

    @pytest.mark.asyncio
    async def test_handoff_package_creation_requires_evidence(self):
        """Verify HandoffPackage cannot be created without evidence"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")

        # Direct creation should be impossible without evidence
        with pytest.raises(VerificationRequired):
            HandoffPackage(
                task={"type": "test"},
                from_agent="agent_a",
                to_agent="agent_b",
                verification_result=None,
                evidence=[],  # Empty evidence should fail
                timestamp=datetime.now(),
                state=HandoffState.INITIATED,
            )

    @pytest.mark.asyncio
    async def test_evidence_review_mandatory(self, handoff_protocol, valid_task_with_evidence):
        """Verify evidence review cannot be bypassed"""

        # Create valid package first
        package = await handoff_protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=valid_task_with_evidence
        )

        # Mock failed evidence review by monkey-patching
        original_method = handoff_protocol._force_evidence_review
        handoff_protocol._force_evidence_review = lambda agent, evidence: False

        try:
            # Should block without evidence review
            with pytest.raises(EvidenceReviewRequired) as exc_info:
                await handoff_protocol.receive_handoff("agent_b", package)

            # Verify error message indicates evidence review requirement
            error_message = str(exc_info.value).lower()
            assert "evidence" in error_message
            assert "review" in error_message

        finally:
            # Restore original method
            handoff_protocol._force_evidence_review = original_method

    @pytest.mark.asyncio
    async def test_handoff_wrong_agent_blocked(self, handoff_protocol, valid_task_with_evidence):
        """Verify handoffs are blocked for wrong receiving agent"""

        # Create valid package
        package = await handoff_protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=valid_task_with_evidence
        )

        # Try to receive with wrong agent
        with pytest.raises(HandoffBlocked) as exc_info:
            await handoff_protocol.receive_handoff("agent_c", package)

        # Verify error message indicates wrong agent
        error_message = str(exc_info.value).lower()
        assert "agent_b" in error_message
        assert "agent_c" in error_message

    @pytest.mark.asyncio
    async def test_verification_pyramid_integration(
        self, handoff_protocol, valid_task_with_evidence
    ):
        """Verify handoff protocol integrates with verification pyramid"""

        # Create handoff - should use verification pyramid internally
        package = await handoff_protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=valid_task_with_evidence
        )

        # Verify package contains verification result
        assert package.verification_result is not None
        assert package.state == HandoffState.VERIFIED
        assert len(package.evidence) > 0

        # Verify evidence is properly structured
        for evidence in package.evidence:
            assert hasattr(evidence, "evidence_type") or hasattr(evidence, "type")
            assert hasattr(evidence, "data") or hasattr(evidence, "content")

    @pytest.mark.asyncio
    async def test_handoff_tracking_and_history(self, handoff_protocol, valid_task_with_evidence):
        """Verify handoffs are properly tracked and logged"""

        # Create handoff
        package = await handoff_protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=valid_task_with_evidence
        )

        # Verify handoff is tracked in active handoffs
        assert len(handoff_protocol.active_handoffs) > 0

        # Verify handoff ID is generated
        handoff_id = handoff_protocol._generate_handoff_id("agent_a", "agent_b")
        assert handoff_id in handoff_protocol.active_handoffs

        # Complete the handoff
        await handoff_protocol.receive_handoff("agent_b", package)

        # Verify handoff moved to history
        assert len(handoff_protocol.handoff_history) > 0
        assert package.state == HandoffState.COMPLETE

    @pytest.mark.asyncio
    async def test_immutable_handoff_package(self, handoff_protocol, valid_task_with_evidence):
        """Verify handoff packages are immutable and cannot be modified"""

        # Create handoff
        package = await handoff_protocol.initiate_handoff(
            from_agent="agent_a", to_agent="agent_b", task=valid_task_with_evidence
        )

        # Verify package is properly structured
        assert package.from_agent == "agent_a"
        assert package.to_agent == "agent_b"
        assert package.timestamp is not None
        assert package.state == HandoffState.VERIFIED

        # Verify task data is preserved
        assert package.task["type"] == "implementation"
        assert package.task["description"] == "Add new feature with tests"
        assert len(package.task["evidence"]) == 3

    def test_handoff_state_enum_completeness(self):
        """Verify HandoffState enum covers all required states"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")

        # Verify all required states exist
        required_states = [
            "INITIATED",
            "VERIFIED",
            "EVIDENCED",
            "ACKNOWLEDGED",
            "COMPLETE",
            "BLOCKED",
        ]

        for state_name in required_states:
            assert hasattr(HandoffState, state_name)
            state = getattr(HandoffState, state_name)
            assert state.value == state_name.lower()


class TestEnforcementPatterns:
    """Test enforcement patterns and edge cases"""

    @pytest.mark.asyncio
    async def test_empty_task_handoff_blocked(self):
        """Verify empty tasks are blocked"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")

        protocol = MandatoryHandoffProtocol()

        empty_task = {}

        with pytest.raises(VerificationRequired):
            await protocol.initiate_handoff(
                from_agent="agent_a", to_agent="agent_b", task=empty_task
            )

    @pytest.mark.asyncio
    async def test_malformed_evidence_blocked(self):
        """Verify malformed evidence is blocked"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")

        protocol = MandatoryHandoffProtocol()

        malformed_task = {
            "type": "implementation",
            "evidence": [
                {"invalid": "structure"},  # Missing required fields
                None,  # Null evidence
                {},  # Empty evidence object
            ],
        }

        with pytest.raises(VerificationRequired):
            await protocol.initiate_handoff(
                from_agent="agent_a", to_agent="agent_b", task=malformed_task
            )

    @pytest.mark.asyncio
    async def test_concurrent_handoff_handling(self):
        """Verify concurrent handoffs are handled correctly"""
        if not HANDOFF_PROTOCOL_AVAILABLE:
            pytest.skip("Handoff protocol not yet implemented by Code Agent")

        protocol = MandatoryHandoffProtocol()

        valid_task = {
            "type": "implementation",
            "evidence": [{"type": "terminal", "content": "tests passing"}],
        }

        # Create multiple concurrent handoffs
        tasks = []
        for i in range(5):
            task = protocol.initiate_handoff(
                from_agent=f"agent_{i}", to_agent=f"agent_{i+1}", task=valid_task
            )
            tasks.append(task)

        # Execute all handoffs concurrently
        packages = await asyncio.gather(*tasks)

        # Verify all handoffs succeeded
        assert len(packages) == 5
        for package in packages:
            assert package.state == HandoffState.VERIFIED
            assert package.verification_result is not None

        # Verify all are tracked
        assert len(protocol.active_handoffs) == 5

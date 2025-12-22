"""
Test capability discovery scenarios for alpha onboarding.

Issue #487: Tests for discovery-oriented user queries that were failing during
alpha E2E testing. Ensures users can discover Piper's capabilities through
natural language queries.

These tests verify:
1. "What services do you offer?" → IDENTITY (capability list)
2. "Help me setup my projects" → GUIDANCE (not STATUS)
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestCapabilityDiscovery:
    """Test discovery-oriented user queries."""

    # ==========================================================================
    # Issue #487: Message 1 - "What services do you offer?"
    # Should classify as IDENTITY to return capability menu
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            "What services do you offer?",
            "what services do you offer",
            "What services do you have?",
            "what features do you have",
            "What can you do?",
            "what can you do for me",
            "What can you help me with?",
            "what can you help with",
            "Show me your capabilities",
            "List your capabilities",
            "menu of services",
            "your capabilities",
        ],
    )
    def test_services_query_classifies_as_identity(self, message: str):
        """
        Issue #487: Capability discovery queries should classify as IDENTITY.

        These are common ways users ask "what can you do?" during alpha testing.
        Previously returned generic responses; should return capability menu.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.IDENTITY, (
            f"Message '{message}' should classify as IDENTITY, " f"got {intent.category}"
        )
        assert intent.action == "get_identity"

    # ==========================================================================
    # Issue #487: Message 2 - "Help me setup my projects"
    # Should classify as GUIDANCE, not STATUS
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            "Help me setup my projects",
            "help me setup projects",
            "Help me configure my projects",
            "setup my projects",
            "configure my projects",
            "How do I setup my projects?",
            "how do i configure this",
            "help me get started",
            "getting started",
        ],
    )
    def test_setup_query_classifies_as_guidance(self, message: str):
        """
        Issue #487: Setup/configuration queries should classify as GUIDANCE.

        Previously "help me setup my projects" was matching STATUS due to
        "my projects" pattern. Now GUIDANCE patterns are checked first.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.GUIDANCE, (
            f"Message '{message}' should classify as GUIDANCE, " f"got {intent.category}"
        )
        assert intent.action == "get_contextual_guidance"

    # ==========================================================================
    # Regression tests: Ensure STATUS still works for non-setup queries
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            "What am I working on?",
            "my projects",
            "show my projects",
            "what's my current project",
            "project status",
            "my status",
        ],
    )
    def test_status_queries_still_work(self, message: str):
        """
        Regression test: Pure status queries should still classify as STATUS.

        Ensures the GUIDANCE-before-STATUS reordering doesn't break legitimate
        status queries that don't contain setup/configure verbs.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.STATUS, (
            f"Message '{message}' should classify as STATUS, " f"got {intent.category}"
        )

    # ==========================================================================
    # Regression tests: Ensure IDENTITY still works for original patterns
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            "What's your name?",
            "who are you",
            "tell me about yourself",
            "introduce yourself",
        ],
    )
    def test_identity_queries_still_work(self, message: str):
        """
        Regression test: Original IDENTITY queries should still work.

        Ensures adding new patterns doesn't break existing behavior.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.IDENTITY, (
            f"Message '{message}' should classify as IDENTITY, " f"got {intent.category}"
        )

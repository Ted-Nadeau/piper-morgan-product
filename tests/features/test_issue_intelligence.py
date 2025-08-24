"""
Issue Intelligence Canonical Query Extension - Test Suite
TDD Implementation following Excellence Flywheel methodology

Created: 2025-08-23 by Chief Architect 5-step foundation
Tests first, then implementation
"""

import asyncio
import time
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

# These imports will fail initially (TDD approach)
from services.features.issue_intelligence import (
    IssueIntelligenceCanonicalQueryEngine,
    IssueIntelligenceContext,
    IssueIntelligenceResult,
)


@pytest.mark.asyncio
class TestIssueIntelligenceCanonicalQueryEngine:
    """Test suite for IssueIntelligenceCanonicalQueryEngine core functionality"""

    async def test_canonical_query_engine_initialization(self):
        """Test IssueIntelligenceCanonicalQueryEngine initializes with required dependencies"""
        # Mock dependencies
        mock_github_integration = Mock()
        mock_canonical_handlers = Mock()
        mock_session_manager = Mock()

        # Initialize query engine
        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github_integration,
            canonical_handlers=mock_canonical_handlers,
            session_manager=mock_session_manager,
        )

        # Verify initialization
        assert engine.github_integration == mock_github_integration
        assert engine.canonical_handlers == mock_canonical_handlers
        assert engine.session_manager == mock_session_manager
        assert engine.user_id == "xian"  # Default user

    async def test_enhance_canonical_query_with_issue_intelligence(self):
        """Test enhancing canonical query responses with GitHub issue intelligence"""
        # Setup mocks
        mock_github_integration = AsyncMock()
        mock_canonical_handlers = AsyncMock()
        mock_session_manager = AsyncMock()

        # Mock GitHub issue data
        mock_issues = [
            {"number": 126, "title": "Configuration Separation Architecture", "state": "closed"},
            {"number": 127, "title": "Canonical Query Integration", "state": "open"},
            {"number": 128, "title": "FTUX Wizard Implementation", "state": "open"},
        ]
        mock_github_integration.get_recent_issues.return_value = mock_issues

        # Mock canonical response
        mock_canonical_response = {
            "message": "Your top priority today is Enhanced conversational context for daily standups.",
            "intent": {
                "category": "PRIORITY",
                "action": "provide_top_priority",
                "confidence": 1.0,
            },
        }
        mock_canonical_handlers.handle.return_value = mock_canonical_response

        # Initialize engine
        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github_integration,
            canonical_handlers=mock_canonical_handlers,
            session_manager=mock_session_manager,
        )

        # Mock intent
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        mock_intent = Intent(
            category=IntentCategory.PRIORITY,
            action="get_top_priority",
            confidence=0.95,
            original_message="What's my top priority?",
        )

        # Execute enhanced query
        result = await engine.enhance_canonical_query(
            intent=mock_intent, session_id="test_session_123"
        )

        # Verify enhanced response includes issue intelligence
        assert isinstance(result, IssueIntelligenceResult)
        assert result.enhanced_message is not None
        assert result.original_response == mock_canonical_response
        assert result.issue_intelligence is not None
        assert len(result.issue_intelligence["recent_issues"]) == 3
        assert result.issue_intelligence["open_issues_count"] == 2
        assert result.issue_intelligence["closed_issues_count"] == 1

    async def test_issue_intelligence_context_integration(self):
        """Test that issue intelligence context integrates with canonical responses"""
        # Setup mocks
        mock_github_integration = AsyncMock()
        mock_canonical_handlers = AsyncMock()
        mock_session_manager = AsyncMock()

        # Mock active GitHub issues related to current priorities
        mock_priority_issues = [
            {
                "number": 127,
                "title": "Canonical Query Integration",
                "state": "open",
                "labels": ["enhancement", "architecture"],
                "assignee": {"login": "mediajunkie"},
            }
        ]
        mock_github_integration.get_issues_by_priority.return_value = mock_priority_issues

        # Initialize engine
        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github_integration,
            canonical_handlers=mock_canonical_handlers,
            session_manager=mock_session_manager,
        )

        # Test context creation
        context = await engine.create_issue_intelligence_context(priority_level="top")

        # Verify context includes relevant issue data
        assert isinstance(context, IssueIntelligenceContext)
        assert context.priority_issues is not None
        assert len(context.priority_issues) == 1
        assert context.priority_issues[0]["number"] == 127
        assert context.priority_issues[0]["title"] == "Canonical Query Integration"
        assert context.open_issues_count == 1
        assert "mediajunkie" in str(context.assignee_context)

    async def test_canonical_query_enhancement_preserves_original_structure(self):
        """Test that canonical query enhancement preserves original response structure while adding intelligence"""
        # Setup mocks
        mock_github_integration = AsyncMock()
        mock_canonical_handlers = AsyncMock()
        mock_session_manager = AsyncMock()

        # Mock original canonical response structure
        original_response = {
            "message": "Based on your current priorities and the time of day: Right Now: Development work",
            "intent": {
                "category": "GUIDANCE",
                "action": "provide_contextual_guidance",
                "confidence": 1.0,
                "context": {
                    "immediate_focus": "Development work",
                    "daily_goal": "Complete PIPER.md configuration system",
                },
            },
            "requires_clarification": False,
        }
        mock_canonical_handlers.handle.return_value = original_response

        # Mock issue intelligence
        mock_github_integration.get_development_context.return_value = {
            "active_prs": 2,
            "pending_reviews": 1,
            "recent_commits": 3,
        }

        # Initialize engine
        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github_integration,
            canonical_handlers=mock_canonical_handlers,
            session_manager=mock_session_manager,
        )

        # Mock intent
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        mock_intent = Intent(
            category=IntentCategory.GUIDANCE,
            action="get_contextual_guidance",
            confidence=0.92,
            original_message="What should I focus on?",
        )

        # Execute enhancement
        result = await engine.enhance_canonical_query(
            intent=mock_intent, session_id="test_session_456"
        )

        # Verify original structure is preserved
        assert isinstance(result, IssueIntelligenceResult)
        assert result.original_response == original_response
        assert result.original_response["intent"]["category"] == "GUIDANCE"
        assert result.original_response["intent"]["confidence"] == 1.0
        assert result.original_response["requires_clarification"] is False

        # Verify enhancement is additive
        assert result.enhanced_message != result.original_response["message"]
        assert result.issue_intelligence is not None
        assert "active_prs" in result.issue_intelligence
        assert result.issue_intelligence["active_prs"] == 2


@pytest.mark.asyncio
class TestIssueIntelligenceIntegration:
    """Integration tests for issue intelligence with existing canonical handlers"""

    async def test_integration_with_existing_canonical_handlers(self):
        """Test that IssueIntelligenceCanonicalQueryEngine integrates seamlessly with existing CanonicalHandlers"""
        # This test will verify that the new engine works with the existing canonical_handlers.py

        # Mock real CanonicalHandlers
        from services.intent_service.canonical_handlers import CanonicalHandlers

        mock_canonical_handlers = Mock(spec=CanonicalHandlers)

        # Mock realistic response from existing handlers
        realistic_response = {
            "message": "Your top priority today is **Enhanced conversational context for daily standups**.",
            "intent": {
                "category": "PRIORITY",
                "action": "provide_top_priority",
                "confidence": 1.0,
                "context": {
                    "top_priority": "Enhanced conversational context for daily standups",
                    "goal": "Transform standup experience",
                    "timeline": "Complete by 5:00 PM today",
                },
            },
            "requires_clarification": False,
        }
        mock_canonical_handlers.handle = AsyncMock(return_value=realistic_response)

        # Mock GitHub integration
        mock_github_integration = AsyncMock()
        mock_session_manager = AsyncMock()

        # Initialize engine with real canonical handlers mock
        engine = IssueIntelligenceCanonicalQueryEngine(
            github_integration=mock_github_integration,
            canonical_handlers=mock_canonical_handlers,
            session_manager=mock_session_manager,
        )

        # Mock intent that would normally go to CanonicalHandlers
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        mock_intent = Intent(
            category=IntentCategory.PRIORITY,
            action="get_top_priority",
            confidence=0.98,
            original_message="What's my top priority today?",
        )

        # Execute and verify delegation works
        result = await engine.enhance_canonical_query(
            intent=mock_intent, session_id="integration_test_789"
        )

        # Verify CanonicalHandlers was called correctly
        mock_canonical_handlers.handle.assert_called_once_with(mock_intent, "integration_test_789")

        # Verify result structure
        assert isinstance(result, IssueIntelligenceResult)
        assert result.original_response == realistic_response
        assert result.enhanced_message is not None
        assert result.issue_intelligence is not None

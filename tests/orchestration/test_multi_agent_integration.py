"""
Integration tests for Multi-Agent Coordinator
Purpose: Validate end-to-end coordination functionality
"""

import asyncio
import time
from unittest.mock import AsyncMock, Mock

import pytest

from services.domain.models import Intent
from services.orchestration.integration.performance_monitoring import PerformanceMonitor
from services.orchestration.integration.session_integration import SessionIntegration
from services.orchestration.integration.workflow_integration import WorkflowIntegration
from services.shared_types import WorkflowType


class TestMultiAgentIntegration:
    """Test Multi-Agent Coordinator integration"""

    @pytest.fixture
    def workflow_integration(self):
        return WorkflowIntegration()

    @pytest.fixture
    def session_integration(self):
        return SessionIntegration()

    @pytest.fixture
    def performance_monitor(self):
        return PerformanceMonitor()

    @pytest.fixture
    def test_intent(self):
        return Intent(
            id="test_123",
            category="EXECUTION",
            action="test_multi_agent",
            original_message="Test multi-agent coordination",
        )

    @pytest.mark.asyncio
    async def test_workflow_integration_performance(self, workflow_integration, test_intent):
        """Test that workflow creation meets performance targets"""

        start_time = time.time()
        workflow = await workflow_integration.create_multi_agent_workflow(test_intent, {})
        duration_ms = int((time.time() - start_time) * 1000)

        assert duration_ms < 1500, f"Workflow creation took {duration_ms}ms, target is <1500ms"
        assert workflow.type == WorkflowType.MULTI_AGENT
        assert len(workflow.tasks) > 0

    @pytest.mark.asyncio
    async def test_session_integration(self, session_integration, test_intent):
        """Test session-based coordination triggering"""

        session_context = {}
        result = await session_integration.trigger_multi_agent_coordination(
            session_context, test_intent
        )

        assert result["status"] == "initiated"
        assert "workflow_id" in result
        assert "ongoing_coordination" in session_context

    @pytest.mark.asyncio
    async def test_performance_monitoring(self, performance_monitor):
        """Test performance monitoring functionality"""

        health_status = await performance_monitor.check_multi_agent_health()

        assert "status" in health_status
        assert "response_time_ms" in health_status
        assert "target_met" in health_status
        assert health_status["response_time_ms"] < 2000  # Health check should be fast

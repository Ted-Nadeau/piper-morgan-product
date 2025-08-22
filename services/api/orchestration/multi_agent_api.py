"""
Multi-Agent Coordination API
Purpose: REST endpoints for triggering and managing multi-agent coordination
"""

from typing import Any, Dict, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.domain.models import Intent
from services.orchestration.integration.performance_monitoring import PerformanceMonitor
from services.orchestration.integration.session_integration import SessionIntegration
from services.orchestration.integration.workflow_integration import WorkflowIntegration

router = APIRouter(prefix="/api/orchestration", tags=["orchestration"])


# Request/Response models
class MultiAgentRequest(BaseModel):
    message: str
    category: str = "EXECUTION"
    action: str
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None


class MultiAgentResponse(BaseModel):
    status: str
    message: str
    workflow_id: Optional[str] = None
    workflow: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    response_time_ms: int
    target_met: bool
    last_check: str


@router.post("/multi-agent", response_model=MultiAgentResponse)
async def trigger_multi_agent_coordination(request: MultiAgentRequest):
    """Trigger multi-agent coordination for complex tasks"""

    try:
        # Create intent
        intent = Intent(
            id=str(uuid4()),
            category=request.category,
            action=request.action,
            original_message=request.message,
            context=request.context or {},
        )

        # Initialize integrations
        workflow_integration = WorkflowIntegration()
        session_integration = SessionIntegration()

        # Create multi-agent workflow
        workflow = await workflow_integration.create_multi_agent_workflow(
            intent, request.context or {}
        )

        # If session_id provided, integrate with session
        if request.session_id:
            session_context = {"session_id": request.session_id}
            session_result = await session_integration.trigger_multi_agent_coordination(
                session_context, intent
            )

        return MultiAgentResponse(
            status="initiated",
            message=f"Multi-agent coordination initiated for: {intent.action}",
            workflow_id=workflow.id,
            workflow=workflow.__dict__,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate coordination: {str(e)}")


@router.get("/multi-agent/health", response_model=HealthResponse)
async def get_multi_agent_health():
    """Get Multi-Agent Coordinator health status"""

    try:
        monitor = PerformanceMonitor()
        health_status = await monitor.check_multi_agent_health()

        return HealthResponse(
            status=health_status["status"],
            response_time_ms=health_status["response_time_ms"],
            target_met=health_status["target_met"],
            last_check=health_status["last_check"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/multi-agent/metrics")
async def get_multi_agent_metrics():
    """Get comprehensive Multi-Agent performance metrics"""

    try:
        monitor = PerformanceMonitor()
        return monitor.get_performance_metrics()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

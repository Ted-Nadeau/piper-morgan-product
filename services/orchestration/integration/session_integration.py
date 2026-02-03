"""
Session Integration for Multi-Agent Coordinator
Purpose: Connect coordination to conversation sessions
"""

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from services.domain.models import Intent
from services.orchestration.integration.workflow_integration import WorkflowIntegration


class SessionIntegration:
    """Integrates Multi-Agent coordination with conversation sessions"""

    def __init__(self):
        self.workflow_integration = WorkflowIntegration()

    async def trigger_multi_agent_coordination(
        self, session_context: Dict[str, Any], intent: Intent
    ) -> Dict[str, Any]:
        """Trigger multi-agent coordination from conversation session"""

        # Check if this session has ongoing coordination
        if "ongoing_coordination" in session_context:
            return {
                "status": "already_in_progress",
                "message": "Coordination already in progress. Check workflow status.",
                "workflow_id": session_context["ongoing_coordination"]["workflow_id"],
            }

        try:
            # Create multi-agent workflow
            workflow = await self.workflow_integration.create_multi_agent_workflow(
                intent, session_context
            )

            # Track coordination in session
            session_context["ongoing_coordination"] = {
                "workflow_id": workflow.id,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "intent": intent.__dict__,
                "status": "active",
            }

            return {
                "status": "initiated",
                "message": f"Multi-agent coordination started. Workflow ID: {workflow.id}",
                "workflow_id": workflow.id,
                "workflow": workflow.__dict__,
            }

        except Exception as e:
            return {
                "status": "failed",
                "message": f"Failed to initiate coordination: {str(e)}",
                "error": str(e),
            }

    def get_coordination_status(self, session_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get current coordination status for session"""
        return session_context.get("ongoing_coordination")

    def clear_coordination(self, session_context: Dict[str, Any]) -> bool:
        """Clear coordination state from session"""
        if "ongoing_coordination" in session_context:
            del session_context["ongoing_coordination"]
            return True
        return False

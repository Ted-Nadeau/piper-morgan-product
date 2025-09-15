"""
Integration module for bridging methodology and services layers.

Provides concrete integration points between methodology patterns
and existing orchestration infrastructure.
"""

from .agent_bridge import AgentCapabilities, AgentCoordinator, CoordinationMethod, CoordinationTask
from .enhanced_orchestration_bridge import EnhancedOrchestrationBridge
from .orchestration_bridge import OrchestrationBridge
from .testing_interface import VerificationTestingInterface
from .workflow_bridge import WorkflowIntegrationBridge

__all__ = [
    "OrchestrationBridge",
    "EnhancedOrchestrationBridge",
    "AgentCoordinator",
    "CoordinationTask",
    "CoordinationMethod",
    "AgentCapabilities",
    "WorkflowIntegrationBridge",
    "VerificationTestingInterface",
]

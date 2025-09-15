"""
Workflow Integration Bridge for Agent Coordination.

Integrates mandatory verification with existing workflow systems,
providing standard workflow patterns with verification enforcement.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from methodology.integration.agent_bridge import (
    AgentCoordinator,
    AgentType,
    CoordinationMethod,
    CoordinationTask,
)


class WorkflowIntegrationBridge:
    """Integrates mandatory verification with existing workflow systems."""

    def __init__(self):
        self.coordinator = AgentCoordinator()
        self.workflow_templates: Dict[str, Dict[str, Any]] = {}
        self.workflow_execution_history: List[Dict[str, Any]] = []
        self._setup_standard_workflows()

    def _setup_standard_workflows(self):
        """Setup standard workflow patterns with verification."""

        # Dual agent implementation workflow
        self.workflow_templates["dual_agent_implementation"] = {
            "coordination_method": CoordinationMethod.PARALLEL_WITH_CROSS_VALIDATION,
            "default_agents": ["code_agent", "cursor_agent"],
            "evidence_requirements": ["terminal_output", "test_results", "cross_validation"],
            "success_criteria": [
                "Implementation complete with evidence",
                "Cross-validation passed",
                "No bypass paths exist",
            ],
            "timeout_minutes": 120,
            "description": "Dual agent parallel implementation with cross-validation",
        }

        # Sequential handoff workflow
        self.workflow_templates["sequential_handoff"] = {
            "coordination_method": CoordinationMethod.SEQUENTIAL_WITH_HANDOFFS,
            "evidence_requirements": [
                "terminal_output",
                "handoff_evidence",
                "verification_results",
            ],
            "success_criteria": [
                "Each handoff includes required evidence",
                "Evidence reviewed by receiving agent",
                "Verification pyramid validation passed",
            ],
            "timeout_minutes": 90,
            "description": "Sequential handoff with mandatory verification",
        }

        # Architecture review workflow
        self.workflow_templates["architecture_review"] = {
            "coordination_method": CoordinationMethod.REVIEW_BASED,
            "default_agents": ["code_agent", "chief_architect"],
            "evidence_requirements": [
                "architectural_evidence",
                "strategic_analysis",
                "methodology_compliance",
            ],
            "success_criteria": [
                "Architecture review completed",
                "Strategic alignment confirmed",
                "Methodology compliance verified",
            ],
            "timeout_minutes": 60,
            "description": "Architecture review with chief architect oversight",
        }

        # Lead developer oversight workflow
        self.workflow_templates["lead_developer_oversight"] = {
            "coordination_method": CoordinationMethod.REVIEW_BASED,
            "default_agents": ["code_agent", "cursor_agent", "lead_developer"],
            "evidence_requirements": [
                "evidence_review",
                "cross_validation",
                "strategic_assessment",
            ],
            "success_criteria": [
                "Implementation meets strategic requirements",
                "Cross-validation between agents successful",
                "Lead developer approval obtained",
            ],
            "timeout_minutes": 150,
            "description": "Multi-agent coordination with lead developer oversight",
        }

        # Quick verification workflow
        self.workflow_templates["quick_verification"] = {
            "coordination_method": CoordinationMethod.SEQUENTIAL_WITH_HANDOFFS,
            "evidence_requirements": ["terminal_output", "explicit_verification"],
            "success_criteria": [
                "Quick verification completed",
                "Terminal evidence provided",
                "No errors detected",
            ],
            "timeout_minutes": 30,
            "description": "Quick verification with minimal overhead",
        }

        print(f"📋 Initialized {len(self.workflow_templates)} standard workflow templates")

    async def execute_workflow_with_verification(
        self,
        workflow_type: str,
        task: Dict[str, Any],
        agents: List[str] = None,
        custom_evidence_requirements: List[str] = None,
        custom_success_criteria: List[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Execute workflow with mandatory verification."""

        workflow_start = datetime.now()

        template = self.workflow_templates.get(workflow_type)
        if not template:
            return {
                "status": "error",
                "message": f"Unknown workflow type: {workflow_type}",
                "available_workflows": list(self.workflow_templates.keys()),
            }

        try:
            # Create coordination task from template
            coordination_task = CoordinationTask(
                task=task,
                coordination_method=template["coordination_method"],
                agents=agents or template.get("default_agents", []),
                evidence_requirements=custom_evidence_requirements
                or template["evidence_requirements"],
                success_criteria=custom_success_criteria or template["success_criteria"],
                timeout_minutes=kwargs.get("timeout_minutes", template.get("timeout_minutes", 60)),
            )

            # Execute with mandatory verification
            result = await self.coordinator.coordinate_task(coordination_task)

            # Add workflow metadata
            workflow_result = {
                **result,
                "workflow_type": workflow_type,
                "workflow_description": template["description"],
                "workflow_duration": (datetime.now() - workflow_start).total_seconds(),
                "workflow_start": workflow_start.isoformat(),
                "template_used": template,
                "agents_used": coordination_task.agents,
            }

            # Store in workflow history
            self.workflow_execution_history.append(workflow_result)

            return workflow_result

        except Exception as e:
            error_result = {
                "status": "workflow_error",
                "workflow_type": workflow_type,
                "error": str(e),
                "workflow_duration": (datetime.now() - workflow_start).total_seconds(),
                "agents_attempted": agents or template.get("default_agents", []),
            }

            self.workflow_execution_history.append(error_result)
            return error_result

    def create_custom_workflow(
        self,
        workflow_name: str,
        coordination_method: CoordinationMethod,
        evidence_requirements: List[str],
        success_criteria: List[str],
        default_agents: List[str] = None,
        timeout_minutes: int = 60,
        description: str = "Custom workflow",
    ) -> bool:
        """Create custom workflow template."""

        if workflow_name in self.workflow_templates:
            print(f"⚠️ Workflow '{workflow_name}' already exists, will be overwritten")

        self.workflow_templates[workflow_name] = {
            "coordination_method": coordination_method,
            "evidence_requirements": evidence_requirements,
            "success_criteria": success_criteria,
            "default_agents": default_agents or [],
            "timeout_minutes": timeout_minutes,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "custom": True,
        }

        print(f"✅ Created custom workflow: {workflow_name}")
        return True

    def get_available_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Get all available workflow templates with descriptions."""
        workflow_info = {}
        for name, template in self.workflow_templates.items():
            workflow_info[name] = {
                "description": template["description"],
                "coordination_method": template["coordination_method"].value,
                "evidence_requirements": template["evidence_requirements"],
                "success_criteria": template["success_criteria"],
                "default_agents": template.get("default_agents", []),
                "timeout_minutes": template.get("timeout_minutes", 60),
                "custom": template.get("custom", False),
            }
        return workflow_info

    def get_workflow_recommendations(
        self, task_type: str, agents_available: List[str]
    ) -> List[str]:
        """Get workflow recommendations based on task type and available agents."""
        recommendations = []

        # Analyze task type and suggest workflows
        if len(agents_available) == 2:
            if "code_agent" in agents_available and "cursor_agent" in agents_available:
                recommendations.append("dual_agent_implementation")
            recommendations.append("sequential_handoff")
        elif len(agents_available) > 2:
            if "lead_developer" in agents_available:
                recommendations.append("lead_developer_oversight")
            elif "chief_architect" in agents_available:
                recommendations.append("architecture_review")

        # Task type specific recommendations
        if "quick" in task_type.lower() or "verification" in task_type.lower():
            recommendations.append("quick_verification")

        if "architecture" in task_type.lower() or "design" in task_type.lower():
            recommendations.append("architecture_review")

        return list(set(recommendations))  # Remove duplicates

    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get workflow execution statistics."""
        total_workflows = len(self.workflow_execution_history)
        if total_workflows == 0:
            return {
                "total_workflows": 0,
                "successful_workflows": 0,
                "failed_workflows": 0,
                "workflow_success_rate": 0.0,
                "average_workflow_time": 0.0,
                "most_used_workflow": None,
                "available_templates": len(self.workflow_templates),
            }

        successful = sum(1 for w in self.workflow_execution_history if w.get("status") == "success")
        failed = total_workflows - successful

        total_time = sum(w.get("workflow_duration", 0) for w in self.workflow_execution_history)
        avg_time = total_time / total_workflows if total_workflows > 0 else 0

        # Count workflow type usage
        workflow_usage = {}
        for w in self.workflow_execution_history:
            workflow_type = w.get("workflow_type", "unknown")
            workflow_usage[workflow_type] = workflow_usage.get(workflow_type, 0) + 1

        most_used = max(workflow_usage.items(), key=lambda x: x[1]) if workflow_usage else None

        return {
            "total_workflows": total_workflows,
            "successful_workflows": successful,
            "failed_workflows": failed,
            "workflow_success_rate": (
                (successful / total_workflows) * 100 if total_workflows > 0 else 0
            ),
            "average_workflow_time": avg_time,
            "most_used_workflow": most_used[0] if most_used else None,
            "most_used_count": most_used[1] if most_used else 0,
            "available_templates": len(self.workflow_templates),
            "custom_templates": sum(
                1 for t in self.workflow_templates.values() if t.get("custom", False)
            ),
            "workflow_usage": workflow_usage,
        }

    def clear_workflow_history(self):
        """Clear workflow execution history - for testing purposes."""
        self.workflow_execution_history.clear()
        print("🧹 Workflow execution history cleared")

    def export_workflow_template(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Export workflow template for sharing or backup."""
        template = self.workflow_templates.get(workflow_name)
        if not template:
            return None

        return {
            "workflow_name": workflow_name,
            "template": template,
            "exported_at": datetime.now().isoformat(),
        }

    def import_workflow_template(self, workflow_data: Dict[str, Any]) -> bool:
        """Import workflow template from exported data."""
        try:
            workflow_name = workflow_data["workflow_name"]
            template = workflow_data["template"]

            # Validate template structure
            required_fields = ["coordination_method", "evidence_requirements", "success_criteria"]
            for field in required_fields:
                if field not in template:
                    print(f"❌ Invalid template: missing {field}")
                    return False

            # Convert coordination method back to enum
            method_str = template["coordination_method"]
            if isinstance(method_str, str):
                template["coordination_method"] = CoordinationMethod(method_str)

            self.workflow_templates[workflow_name] = template
            print(f"✅ Imported workflow template: {workflow_name}")
            return True

        except Exception as e:
            print(f"❌ Failed to import workflow template: {e}")
            return False

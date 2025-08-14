"""
CI/CD Spatial Intelligence Implementation
Following ADR-013: MCP + Spatial Intelligence Pattern

Mirrors LinearSpatialIntelligence with 8-dimensional spatial analysis for CI/CD pipelines.
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)
from services.mcp.consumer.cicd_adapter import CICDMCPSpatialAdapter

logger = logging.getLogger(__name__)


class CICDSpatialIntelligence:
    """
    CI/CD integration using MCP + Spatial Intelligence pattern.
    Following LinearSpatialIntelligence implementation pattern exactly.

    8 Dimensions:
    1. HIERARCHY - Pipeline → Jobs → Steps → Actions
    2. TEMPORAL - Build times, deployment schedules, execution history
    3. PRIORITY - Critical deployments, release priorities, environment order
    4. COLLABORATIVE - Triggering users, approvers, notification recipients
    5. FLOW - Pipeline states (pending/running/success/failed), deployment status
    6. QUANTITATIVE - Build durations, success rates, deployment frequency
    7. CAUSAL - Triggered by commits, blocks deployments, dependency chains
    8. CONTEXTUAL - Repository, environment, branch, release context
    """

    def __init__(self):
        """Initialize CI/CD spatial intelligence with MCP adapter"""
        self.mcp_adapter = CICDMCPSpatialAdapter()

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_pipeline_hierarchy,
            "TEMPORAL": self.analyze_timeline,
            "PRIORITY": self.analyze_priority_signals,
            "COLLABORATIVE": self.analyze_team_activity,
            "FLOW": self.analyze_workflow_state,
            "QUANTITATIVE": self.analyze_metrics,
            "CAUSAL": self.analyze_dependencies,
            "CONTEXTUAL": self.analyze_project_context,
        }

        logger.info("CICDSpatialIntelligence initialized with 8 dimensions")

    async def initialize(self):
        """Initialize MCP adapter and connections"""
        await self.mcp_adapter.configure_cicd_apis()
        logger.info("CI/CD MCP adapter configured")

    # DIMENSION 1: HIERARCHY
    async def analyze_pipeline_hierarchy(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze pipeline/job hierarchy and relationships"""
        hierarchy = {
            "level": "pipeline",  # pipeline, job, step, action
            "type": pipeline.get("type", "build"),  # build, deploy, test
            "depth": 0,
            "has_children": False,
            "parent_pipeline": None,
            "child_jobs": [],
            "workflow_id": pipeline.get("workflow_id"),
            "run_id": pipeline.get("id"),
        }

        # Check for job hierarchy
        if jobs := pipeline.get("jobs", []):
            hierarchy["has_children"] = True
            hierarchy["child_jobs"] = [job.get("id") for job in jobs]
            hierarchy["depth"] = len(jobs)

        # Check for parent workflow
        if parent := pipeline.get("parent_workflow"):
            hierarchy["level"] = "job"
            hierarchy["depth"] = 1
            hierarchy["parent_pipeline"] = parent.get("id")

        return hierarchy

    # DIMENSION 2: TEMPORAL
    async def analyze_timeline(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal patterns and execution timeline"""
        from datetime import timezone

        now = datetime.now(timezone.utc)
        created = datetime.fromisoformat(
            pipeline.get("created_at", now.isoformat()).replace("Z", "+00:00")
        )
        updated = datetime.fromisoformat(
            pipeline.get("updated_at", now.isoformat()).replace("Z", "+00:00")
        )

        # Calculate execution metrics
        age_minutes = (now - created).total_seconds() / 60
        last_activity_minutes = (now - updated).total_seconds() / 60

        # Determine activity level
        if last_activity_minutes < 5:
            activity_level = "active"
        elif last_activity_minutes < 30:
            activity_level = "recent"
        elif last_activity_minutes < 1440:  # 24 hours
            activity_level = "moderate"
        else:
            activity_level = "stale"

        # Check scheduled deployments
        urgency = "normal"
        if scheduled := pipeline.get("scheduled_at"):
            scheduled_time = datetime.fromisoformat(scheduled.replace("Z", "+00:00"))
            minutes_to_deploy = (scheduled_time - now).total_seconds() / 60
            if minutes_to_deploy <= 30:
                urgency = "high"
            elif minutes_to_deploy <= 120:
                urgency = "medium"

        # Calculate duration
        duration_seconds = None
        if completed_at := pipeline.get("completed_at"):
            completed = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
            duration_seconds = (completed - created).total_seconds()

        return {
            "age_minutes": age_minutes,
            "last_activity_minutes": last_activity_minutes,
            "activity_level": activity_level,
            "urgency": urgency,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
            "scheduled_at": pipeline.get("scheduled_at"),
            "completed_at": pipeline.get("completed_at"),
            "duration_seconds": duration_seconds,
        }

    # DIMENSION 3: PRIORITY
    async def analyze_priority_signals(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze priority signals from pipeline type, environment, branch"""
        environment = pipeline.get("environment", "development")
        branch = pipeline.get("branch", "main")
        pipeline_type = pipeline.get("type", "build")

        # Determine priority level based on environment and type
        priority_level = "normal"
        if environment == "production" or "release" in branch:
            priority_level = "critical"
        elif environment == "staging" or branch == "main":
            priority_level = "high"
        elif environment == "development":
            priority_level = "normal"
        else:
            priority_level = "low"

        # Calculate attention score (0.0 - 1.0)
        attention_score = 0.5  # Base score

        if priority_level == "critical":
            attention_score = 1.0
        elif priority_level == "high":
            attention_score = 0.8
        elif priority_level == "low":
            attention_score = 0.3

        # Boost for deployments
        if pipeline_type == "deploy":
            attention_score = min(1.0, attention_score + 0.2)

        # Boost for production
        if environment == "production":
            attention_score = min(1.0, attention_score + 0.3)

        # Check for tags/labels
        tags = pipeline.get("tags", [])
        is_hotfix = "hotfix" in tags or "emergency" in tags
        is_release = "release" in tags or "release" in branch

        if is_hotfix:
            priority_level = "critical"
            attention_score = 1.0

        return {
            "priority_level": priority_level,
            "environment": environment,
            "branch": branch,
            "pipeline_type": pipeline_type,
            "is_hotfix": is_hotfix,
            "is_release": is_release,
            "is_production": environment == "production",
            "attention_score": attention_score,
            "tags": tags,
        }

    # DIMENSION 4: COLLABORATIVE
    async def analyze_team_activity(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze team collaboration and engagement"""
        # Get triggering user
        triggered_by = (
            pipeline.get("triggered_by", {}).get("login") if pipeline.get("triggered_by") else None
        )

        # Get approvers for deployments
        approvers = []
        if approvals := pipeline.get("approvals", []):
            approvers = [a.get("user", {}).get("login") for a in approvals if a.get("user")]

        # Get committers
        committers = []
        if commits := pipeline.get("commits", []):
            committers = list(
                set([c.get("author", {}).get("login") for c in commits if c.get("author")])
            )

        # Notification recipients
        notification_count = len(pipeline.get("notifications", []))

        # Determine engagement level
        total_participants = (
            len(set([triggered_by] + approvers + committers))
            if triggered_by
            else len(set(approvers + committers))
        )

        if total_participants >= 5:
            engagement_level = "high"
        elif total_participants >= 2:
            engagement_level = "moderate"
        else:
            engagement_level = "low"

        return {
            "triggered_by": triggered_by,
            "approver_count": len(approvers),
            "committer_count": len(committers),
            "notification_count": notification_count,
            "engagement_level": engagement_level,
            "participants": (
                list(set([triggered_by] + approvers + committers))
                if triggered_by
                else list(set(approvers + committers))
            ),
            "approvers": approvers,
            "committers": committers,
        }

    # DIMENSION 5: FLOW
    async def analyze_workflow_state(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow state and progress"""
        status = pipeline.get("status", "pending")
        conclusion = pipeline.get("conclusion", "")

        # Map CI/CD status to workflow stages
        workflow_stage_map = {
            "queued": "pending",
            "in_progress": "running",
            "completed": "completed",
            "waiting": "blocked",
            "pending": "pending",
            "running": "running",
            "success": "completed",
            "failure": "failed",
            "cancelled": "canceled",
            "skipped": "skipped",
        }

        workflow_stage = workflow_stage_map.get(status.lower(), "pending")

        # Check if blocked
        is_blocked = status == "waiting" or "blocked" in pipeline.get("tags", [])

        # Estimate completion percentage based on jobs
        completion = 0
        if jobs := pipeline.get("jobs", []):
            completed_jobs = [j for j in jobs if j.get("status") == "completed"]
            completion = (len(completed_jobs) / len(jobs)) * 100
        elif status == "completed" or conclusion == "success":
            completion = 100
        elif status == "in_progress" or status == "running":
            completion = 50

        return {
            "status": status,
            "conclusion": conclusion,
            "workflow_stage": workflow_stage,
            "is_blocked": is_blocked,
            "completion_percentage": completion,
            "is_failed": conclusion == "failure",
            "is_success": conclusion == "success",
            "can_retry": status in ["failed", "cancelled"],
        }

    # DIMENSION 6: QUANTITATIVE
    async def analyze_metrics(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quantitative metrics and velocities"""
        from datetime import timezone

        created = datetime.fromisoformat(
            pipeline.get("created_at", datetime.now().isoformat()).replace("Z", "+00:00")
        )
        now = datetime.now(timezone.utc)

        # Calculate duration
        duration_seconds = None
        if completed_at := pipeline.get("completed_at"):
            completed = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
            duration_seconds = (completed - created).total_seconds()
        elif status := pipeline.get("status"):
            if status in ["running", "in_progress"]:
                duration_seconds = (now - created).total_seconds()

        # Job metrics
        job_count = len(pipeline.get("jobs", []))
        failed_job_count = len(
            [j for j in pipeline.get("jobs", []) if j.get("conclusion") == "failure"]
        )

        # Calculate success rate
        success_rate = 0
        if job_count > 0:
            success_rate = ((job_count - failed_job_count) / job_count) * 100

        # Complexity estimation
        complexity = "low"
        if job_count > 10 or (duration_seconds and duration_seconds > 1800):  # 30 minutes
            complexity = "high"
        elif job_count > 5 or (duration_seconds and duration_seconds > 600):  # 10 minutes
            complexity = "medium"

        # Deployment frequency (if available from history)
        deployment_frequency = pipeline.get("deployment_frequency", "unknown")

        return {
            "duration_seconds": duration_seconds,
            "job_count": job_count,
            "failed_job_count": failed_job_count,
            "success_rate": success_rate,
            "complexity_estimate": complexity,
            "deployment_frequency": deployment_frequency,
            "retry_count": pipeline.get("retry_count", 0),
        }

    # DIMENSION 7: CAUSAL
    async def analyze_dependencies(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze causal relationships and dependencies"""
        # Get trigger information
        triggered_by_commit = None
        triggered_by_pr = None
        triggered_by_schedule = False
        triggered_by_manual = False

        if trigger := pipeline.get("trigger"):
            trigger_type = trigger.get("type", "")
            if trigger_type == "push":
                triggered_by_commit = trigger.get("commit", {}).get("sha")
            elif trigger_type == "pull_request":
                triggered_by_pr = trigger.get("pull_request", {}).get("number")
            elif trigger_type == "schedule":
                triggered_by_schedule = True
            elif trigger_type == "manual":
                triggered_by_manual = True

        # Dependencies
        depends_on = pipeline.get("depends_on", [])
        blocks = pipeline.get("blocks", [])

        # Deployment chain
        deployment_chain = []
        if next_environment := pipeline.get("next_environment"):
            deployment_chain.append(next_environment)

        dependency_chain_length = len(depends_on) + len(blocks)

        return {
            "triggered_by_commit": triggered_by_commit,
            "triggered_by_pr": triggered_by_pr,
            "triggered_by_schedule": triggered_by_schedule,
            "triggered_by_manual": triggered_by_manual,
            "depends_on": depends_on,
            "blocks": blocks,
            "deployment_chain": deployment_chain,
            "dependency_chain_length": dependency_chain_length,
            "has_dependencies": dependency_chain_length > 0,
        }

    # DIMENSION 8: CONTEXTUAL
    async def analyze_project_context(self, pipeline: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze repository and organizational context"""
        repository = pipeline.get("repository", {}).get("full_name", "unknown")
        organization = pipeline.get("repository", {}).get("owner", {}).get("login", "unknown")

        # CI/CD platform
        platform = "unknown"
        if "github" in pipeline.get("url", "").lower():
            platform = "github_actions"
        elif "gitlab" in pipeline.get("url", "").lower():
            platform = "gitlab_ci"
        elif "circleci" in pipeline.get("url", "").lower():
            platform = "circleci"
        elif "jenkins" in pipeline.get("url", "").lower():
            platform = "jenkins"

        # Determine domain based on pipeline type and repository
        domain = "general"
        pipeline_type = pipeline.get("type", "").lower()
        repo_name = repository.lower()

        if "deploy" in pipeline_type or "release" in pipeline_type:
            domain = "deployment"
        elif "test" in pipeline_type or "qa" in pipeline_type:
            domain = "quality_assurance"
        elif "build" in pipeline_type:
            domain = "build"
        elif "security" in pipeline_type or "scan" in pipeline_type:
            domain = "security"
        elif "docs" in repo_name:
            domain = "documentation"

        # Environment context
        environment = pipeline.get("environment", "development")
        branch = pipeline.get("branch", "main")

        return {
            "repository": repository,
            "organization": organization,
            "platform": platform,
            "domain": domain,
            "environment": environment,
            "branch": branch,
            "full_name": f"{organization}/{repository}",
            "workflow_name": pipeline.get("workflow_name", "unknown"),
        }

    # MAIN SPATIAL CONTEXT CREATION
    async def create_spatial_context(self, pipeline: Dict[str, Any]) -> SpatialContext:
        """Create full 8-dimensional spatial context for CI/CD pipeline"""
        # Run all dimensional analyses in parallel
        dimension_results = await asyncio.gather(
            self.analyze_pipeline_hierarchy(pipeline),
            self.analyze_timeline(pipeline),
            self.analyze_priority_signals(pipeline),
            self.analyze_team_activity(pipeline),
            self.analyze_workflow_state(pipeline),
            self.analyze_metrics(pipeline),
            self.analyze_dependencies(pipeline),
            self.analyze_project_context(pipeline),
        )

        # Unpack results
        hierarchy, temporal, priority, collaborative, flow, quantitative, causal, contextual = (
            dimension_results
        )

        # Determine attention level based on priority and temporal urgency
        if priority["priority_level"] == "critical" or temporal["urgency"] == "high":
            attention_level = "urgent"
        elif priority["priority_level"] == "high" or temporal["activity_level"] == "active":
            attention_level = "high"
        elif temporal["activity_level"] == "stale":
            attention_level = "low"
        else:
            attention_level = "medium"

        # Determine emotional valence
        if flow["is_failed"] or flow["is_blocked"]:
            emotional_valence = "negative"
        elif flow["is_success"]:
            emotional_valence = "positive"
        else:
            emotional_valence = "neutral"

        # Determine navigation intent
        if flow["is_blocked"]:
            navigation_intent = "investigate"
        elif flow["workflow_stage"] == "running":
            navigation_intent = "monitor"
        elif priority["priority_level"] in ["critical", "high"]:
            navigation_intent = "respond"
        else:
            navigation_intent = "explore"

        # Create spatial context
        return SpatialContext(
            territory_id="cicd",
            room_id=contextual["platform"],
            path_id=(
                f"pipelines/{pipeline['id']}"
                if pipeline.get("id")
                else f"pipelines/{pipeline.get('run_id', 'unknown')}"
            ),
            attention_level=attention_level,
            emotional_valence=emotional_valence,
            navigation_intent=navigation_intent,
            external_system="cicd",
            external_id=str(pipeline.get("id", pipeline.get("run_id", "unknown"))),
            external_context={
                "hierarchy": hierarchy,
                "temporal": temporal,
                "priority": priority,
                "collaborative": collaborative,
                "flow": flow,
                "quantitative": quantitative,
                "causal": causal,
                "contextual": contextual,
            },
        )

    # HELPER METHODS FOR INTEGRATION
    async def map_pipeline_to_position(
        self, pipeline_id: str, context: Dict[str, Any]
    ) -> SpatialPosition:
        """Map CI/CD pipeline to spatial position using MCP adapter"""
        return await self.mcp_adapter.map_to_position(pipeline_id, context)

    async def get_pipeline(self, repository: str, pipeline_id: str) -> Dict[str, Any]:
        """Get pipeline data using MCP adapter (backward compatibility)"""
        result = await self.mcp_adapter._call_github_actions_api(
            f"/repos/{repository}/actions/runs/{pipeline_id}"
        )
        return result or {"id": pipeline_id}

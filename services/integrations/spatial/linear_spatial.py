"""
Linear Spatial Intelligence Implementation
Following ADR-013: MCP + Spatial Intelligence Pattern

Mirrors GitHubSpatialIntelligence with 8-dimensional spatial analysis for Linear issues.
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
from services.mcp.consumer.linear_adapter import LinearMCPSpatialAdapter

logger = logging.getLogger(__name__)


class LinearSpatialIntelligence:
    """
    Linear integration using MCP + Spatial Intelligence pattern.
    Following GitHubSpatialIntelligence implementation pattern exactly.

    8 Dimensions:
    1. HIERARCHY - Issue/project relationships, parent-child structures
    2. TEMPORAL - Created/updated patterns, activity timelines
    3. PRIORITY - Priority levels, cycles, milestones
    4. COLLABORATIVE - Assignees, subscribers, comments
    5. FLOW - Status workflows, state transitions
    6. QUANTITATIVE - Counts, sizes, velocities, metrics
    7. CAUSAL - Dependencies, blocked issues, links
    8. CONTEXTUAL - Project, team, workspace context
    """

    def __init__(self):
        """Initialize Linear spatial intelligence with MCP adapter"""
        self.mcp_adapter = LinearMCPSpatialAdapter()

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_issue_hierarchy,
            "TEMPORAL": self.analyze_timeline,
            "PRIORITY": self.analyze_priority_signals,
            "COLLABORATIVE": self.analyze_team_activity,
            "FLOW": self.analyze_workflow_state,
            "QUANTITATIVE": self.analyze_metrics,
            "CAUSAL": self.analyze_dependencies,
            "CONTEXTUAL": self.analyze_project_context,
        }

        logger.info("LinearSpatialIntelligence initialized with 8 dimensions")

    async def initialize(self):
        """Initialize MCP adapter and connections"""
        await self.mcp_adapter.configure_linear_api()
        logger.info("Linear MCP adapter configured")

    # DIMENSION 1: HIERARCHY
    async def analyze_issue_hierarchy(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze issue/project hierarchy and relationships"""
        hierarchy = {
            "level": "root",  # root, child, subtask
            "type": "issue",  # Linear only has issues, no PRs
            "depth": 0,
            "has_children": False,
            "parent_issue": None,
            "child_issues": [],
            "project_id": issue.get("project", {}).get("id"),
            "team_id": issue.get("team", {}).get("id"),
        }

        # Check for parent-child relationships
        if parent := issue.get("parent"):
            hierarchy["level"] = "child"
            hierarchy["depth"] = 1
            hierarchy["parent_issue"] = parent.get("id")

        # Check for child issues
        if children := issue.get("children", {}).get("nodes", []):
            hierarchy["has_children"] = True
            hierarchy["child_issues"] = [child.get("id") for child in children]

        return hierarchy

    # DIMENSION 2: TEMPORAL
    async def analyze_timeline(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal patterns and activity timeline"""
        from datetime import timezone

        now = datetime.now(timezone.utc)
        created = datetime.fromisoformat(issue["createdAt"].replace("Z", "+00:00"))
        updated = datetime.fromisoformat(issue["updatedAt"].replace("Z", "+00:00"))

        age_days = (now - created).days
        last_activity_hours = (now - updated).total_seconds() / 3600

        # Determine activity level
        if last_activity_hours < 24:
            activity_level = "active"
        elif last_activity_hours < 72:
            activity_level = "recent"
        elif last_activity_hours < 168:  # 1 week
            activity_level = "moderate"
        else:
            activity_level = "stale"

        # Check cycle urgency (Linear's equivalent to milestones)
        urgency = "normal"
        if cycle := issue.get("cycle"):
            if end_date := cycle.get("endsAt"):
                due_date = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                days_to_due = (due_date - now).days
                if days_to_due <= 3:
                    urgency = "high"
                elif days_to_due <= 7:
                    urgency = "medium"

        # Check for due date
        if due_date := issue.get("dueDate"):
            due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            days_to_due = (due - now).days
            if days_to_due <= 3:
                urgency = "high"
            elif days_to_due <= 7:
                urgency = "medium"

        return {
            "age_days": age_days,
            "last_activity_hours": last_activity_hours,
            "activity_level": activity_level,
            "urgency": urgency,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
            "cycle_end": issue.get("cycle", {}).get("endsAt"),
            "due_date": issue.get("dueDate"),
        }

    # DIMENSION 3: PRIORITY
    async def analyze_priority_signals(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze priority signals from Linear priority, labels, cycles"""
        # Linear has explicit priority levels (0-4)
        priority_value = issue.get("priority", 0)

        # Map Linear priority to our levels
        if priority_value >= 4:
            priority_level = "critical"
        elif priority_value >= 3:
            priority_level = "high"
        elif priority_value == 2:
            priority_level = "normal"
        else:
            priority_level = "low"

        # Get labels
        labels = []
        if label_nodes := issue.get("labels", {}).get("nodes", []):
            labels = [label.get("name", "") for label in label_nodes]

        # Calculate attention score (0.0 - 1.0)
        attention_score = 0.3 + (priority_value * 0.15)  # Base + priority multiplier

        if priority_level == "critical":
            attention_score = 1.0
        elif priority_level == "high":
            attention_score = 0.8

        # Add cycle boost
        if issue.get("cycle"):
            attention_score = min(1.0, attention_score + 0.2)

        # Add assignee boost
        if issue.get("assignee"):
            attention_score = min(1.0, attention_score + 0.1)

        # Determine issue types from Linear data
        is_bug = any(label.lower() in ["bug", "issue", "error"] for label in labels)
        is_feature = any(
            label.lower() in ["feature", "enhancement", "improvement"] for label in labels
        )

        return {
            "priority_level": priority_level,
            "priority_value": priority_value,
            "has_cycle": bool(issue.get("cycle")),
            "has_due_date": bool(issue.get("dueDate")),
            "is_bug": is_bug,
            "is_feature": is_feature,
            "assigned": bool(issue.get("assignee")),
            "attention_score": attention_score,
            "labels": labels,
        }

    # DIMENSION 4: COLLABORATIVE
    async def analyze_team_activity(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze team collaboration and engagement"""
        # Get assignee
        assignee = issue.get("assignee", {}).get("email") if issue.get("assignee") else None
        assignees = [assignee] if assignee else []

        # Get creator
        creator = issue.get("creator", {}).get("email") if issue.get("creator") else None

        # Comment count (if available)
        comment_count = issue.get("commentCount", 0)

        # Subscriber count (people watching the issue)
        subscriber_count = len(issue.get("subscribers", {}).get("nodes", []))

        # Determine engagement level
        total_engagement = comment_count + subscriber_count
        if total_engagement >= 10:
            engagement_level = "high"
        elif total_engagement >= 5:
            engagement_level = "moderate"
        else:
            engagement_level = "low"

        # Collect participants
        participants = set()
        if assignee:
            participants.add(assignee)
        if creator:
            participants.add(creator)

        return {
            "assignee_count": len(assignees),
            "comment_count": comment_count,
            "subscriber_count": subscriber_count,
            "engagement_level": engagement_level,
            "participants": list(participants),
            "assignees": assignees,
            "creator": creator,
        }

    # DIMENSION 5: FLOW
    async def analyze_workflow_state(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow state and progress"""
        # Get state information
        state = issue.get("state", {})
        state_name = state.get("name", "Unknown") if state else "Unknown"
        state_type = state.get("type", "backlog") if state else "backlog"

        # Map Linear state types to workflow stages
        workflow_stage_map = {
            "backlog": "new",
            "unstarted": "new",
            "started": "in_progress",
            "completed": "completed",
            "canceled": "canceled",
        }

        workflow_stage = workflow_stage_map.get(state_type.lower(), "new")

        # Check if blocked (Linear doesn't have explicit blocked state, infer from labels/status)
        labels = []
        if label_nodes := issue.get("labels", {}).get("nodes", []):
            labels = [label.get("name", "").lower() for label in label_nodes]

        is_blocked = any(label in ["blocked", "waiting", "on-hold"] for label in labels)

        # Estimate completion percentage based on state
        completion_map = {
            "completed": 100,
            "started": 50,
            "unstarted": 0,
            "backlog": 0,
            "canceled": 0,
        }
        completion = completion_map.get(state_type.lower(), 0)

        return {
            "state": state_name,
            "state_type": state_type,
            "workflow_stage": workflow_stage,
            "is_blocked": is_blocked,
            "completion_percentage": completion,
            "is_canceled": state_type.lower() == "canceled",
        }

    # DIMENSION 6: QUANTITATIVE
    async def analyze_metrics(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quantitative metrics and velocities"""
        from datetime import timezone

        created = datetime.fromisoformat(issue["createdAt"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age_days = max(1, (now - created).days)

        comment_count = issue.get("commentCount", 0)
        comment_velocity = comment_count / age_days

        # Engagement score calculation (comments + subscribers)
        subscriber_count = len(issue.get("subscribers", {}).get("nodes", []))
        engagement_score = comment_count + (subscriber_count * 1.5)

        # Complexity estimation based on various factors
        complexity = "low"
        if comment_count > 10 or age_days > 30:
            complexity = "high"
        elif comment_count > 5 or age_days > 14:
            complexity = "medium"

        # Time to cycle end
        time_to_cycle_days = None
        if cycle := issue.get("cycle"):
            if end_date := cycle.get("endsAt"):
                cycle_end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                time_to_cycle_days = (cycle_end - now).days

        # Time to due date
        time_to_due_days = None
        if due_date := issue.get("dueDate"):
            due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            time_to_due_days = (due - now).days

        # Estimate points (Linear uses estimate field)
        estimate = issue.get("estimate", 0)

        return {
            "comment_velocity": comment_velocity,
            "engagement_score": engagement_score,
            "complexity_estimate": complexity,
            "time_to_cycle_days": time_to_cycle_days,
            "time_to_due_days": time_to_due_days,
            "age_days": age_days,
            "comment_count": comment_count,
            "subscriber_count": subscriber_count,
            "estimate": estimate,
        }

    # DIMENSION 7: CAUSAL
    async def analyze_dependencies(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze causal relationships and dependencies"""
        description = issue.get("description", "")

        # Parse common dependency patterns in description
        blocks = []
        blocked_by = []
        related_issues = []

        # Look for Linear issue references (LIN-XXX pattern)
        import re

        # Linear issues are referenced as LIN-123 or team-123
        if "blocks " in description.lower():
            blocks_matches = re.findall(r"blocks (?:LIN-|[A-Z]+-)?(\d+)", description.lower())
            blocks = [int(num) for num in blocks_matches]

        if "blocked by " in description.lower():
            blocked_matches = re.findall(r"blocked by (?:LIN-|[A-Z]+-)?(\d+)", description.lower())
            blocked_by = [int(num) for num in blocked_matches]

        if "related to " in description.lower() or "see " in description.lower():
            related_matches = re.findall(
                r"(?:related to|see) (?:LIN-|[A-Z]+-)?(\d+)", description.lower()
            )
            related_issues = [int(num) for num in related_matches]

        # Linear also has explicit relations (if available in the API response)
        if relations := issue.get("relations", {}).get("nodes", []):
            for relation in relations:
                if relation.get("type") == "blocks":
                    if related_issue := relation.get("relatedIssue"):
                        blocks.append(related_issue.get("number"))
                elif relation.get("type") == "blocked_by":
                    if related_issue := relation.get("relatedIssue"):
                        blocked_by.append(related_issue.get("number"))

        dependency_chain_length = len(blocks) + len(blocked_by)

        return {
            "blocks": blocks,
            "blocked_by": blocked_by,
            "related_issues": related_issues,
            "dependency_chain_length": dependency_chain_length,
            "has_dependencies": dependency_chain_length > 0,
        }

    # DIMENSION 8: CONTEXTUAL
    async def analyze_project_context(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project and organizational context"""
        # Get team information
        team = issue.get("team", {})
        team_name = team.get("name", "unknown")
        team_key = team.get("key", "unknown")

        # Get project information
        project = issue.get("project", {})
        project_name = project.get("name", "unknown") if project else "No Project"

        # Determine domain based on team/project names
        domain = "general"
        context_text = f"{team_name} {project_name}".lower()

        if any(keyword in context_text for keyword in ["product", "pm", "strategy"]):
            domain = "product_management"
        elif any(keyword in context_text for keyword in ["eng", "dev", "backend", "api"]):
            domain = "engineering"
        elif any(keyword in context_text for keyword in ["design", "ui", "ux", "frontend"]):
            domain = "user_interface"
        elif any(keyword in context_text for keyword in ["docs", "documentation"]):
            domain = "documentation"
        elif any(keyword in context_text for keyword in ["qa", "test", "quality"]):
            domain = "quality_assurance"

        # Organization information (if available)
        organization = issue.get("team", {}).get("organization", {}).get("name", "unknown")

        return {
            "team_name": team_name,
            "team_key": team_key,
            "project_name": project_name,
            "organization": organization,
            "domain": domain,
            "full_name": f"{team_key}/{project_name}" if project_name != "No Project" else team_key,
        }

    # MAIN SPATIAL CONTEXT CREATION
    async def create_spatial_context(self, issue: Dict[str, Any]) -> SpatialContext:
        """Create full 8-dimensional spatial context for Linear issue"""
        # Run all dimensional analyses in parallel
        dimension_results = await asyncio.gather(
            self.analyze_issue_hierarchy(issue),
            self.analyze_timeline(issue),
            self.analyze_priority_signals(issue),
            self.analyze_team_activity(issue),
            self.analyze_workflow_state(issue),
            self.analyze_metrics(issue),
            self.analyze_dependencies(issue),
            self.analyze_project_context(issue),
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
        if priority["is_bug"] or flow["is_blocked"]:
            emotional_valence = "negative"
        elif priority["is_feature"]:
            emotional_valence = "positive"
        else:
            emotional_valence = "neutral"

        # Determine navigation intent
        if flow["is_blocked"]:
            navigation_intent = "investigate"
        elif priority["assigned"] and flow["workflow_stage"] == "in_progress":
            navigation_intent = "monitor"
        elif priority["priority_level"] in ["critical", "high"]:
            navigation_intent = "respond"
        else:
            navigation_intent = "explore"

        # Create spatial context
        return SpatialContext(
            territory_id="linear",
            room_id=contextual["team_key"],
            path_id=(
                f"issues/{issue['number']}"
                if issue.get("number")
                else f"issues/{issue.get('id', 'unknown')}"
            ),
            attention_level=attention_level,
            emotional_valence=emotional_valence,
            navigation_intent=navigation_intent,
            external_system="linear",
            external_id=str(issue.get("number", issue.get("id", "unknown"))),
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
    async def map_issue_to_position(
        self, issue_id: str, context: Dict[str, Any]
    ) -> SpatialPosition:
        """Map Linear issue to spatial position using MCP adapter"""
        return await self.mcp_adapter.map_to_position(issue_id, context)

    async def get_issue(self, team_key: str, issue_number: int) -> Dict[str, Any]:
        """Get issue data using MCP adapter (backward compatibility)"""
        result = await self.mcp_adapter._call_linear_api(f"/teams/{team_key}/issues/{issue_number}")
        return result or {"number": issue_number}

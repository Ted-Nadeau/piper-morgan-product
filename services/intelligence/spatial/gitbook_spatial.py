"""
GitBook Spatial Intelligence Implementation
Following ADR-013: MCP + Spatial Intelligence Pattern

Mirrors NotionSpatialIntelligence with 8-dimensional spatial analysis for GitBook
spaces, collections, and pages.
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from services.integrations.mcp.gitbook_adapter import GitBookMCPAdapter
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

logger = logging.getLogger(__name__)


class GitBookSpatialIntelligence:
    """
    GitBook integration using MCP + Spatial Intelligence pattern.
    Following NotionSpatialIntelligence implementation pattern exactly.

    8 Dimensions:
    1. HIERARCHY - Space → Collection → Page hierarchy
    2. TEMPORAL - Content timeline and publishing workflows
    3. PRIORITY - Visibility and access control analysis
    4. COLLABORATIVE - User permissions and activity patterns
    5. FLOW - Content states and approval workflows
    6. QUANTITATIVE - Page counts and engagement metrics
    7. CAUSAL - Parent-child relationships and dependencies
    8. CONTEXTUAL - Space purpose and collection themes
    """

    def __init__(self):
        """Initialize GitBook spatial intelligence with MCP adapter"""
        self.mcp_adapter = GitBookMCPAdapter()

        # Spatial analytics tracking
        self._spatial_analytics = {
            "spaces_analyzed": 0,
            "collections_analyzed": 0,
            "pages_analyzed": 0,
            "spatial_contexts_created": 0,
            "hierarchy_mappings": 0,
            "temporal_patterns": 0,
            "collaborative_insights": 0,
        }

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_space_hierarchy,  # Space → Collection → Page
            "TEMPORAL": self.analyze_content_timeline,  # Last updated, created
            "PRIORITY": self.analyze_visibility_status,  # Public, private, restricted
            "COLLABORATIVE": self.analyze_user_activity,  # Authors, editors, permissions
            "FLOW": self.analyze_content_workflow,  # Content states, publishing
            "QUANTITATIVE": self.analyze_content_metrics,  # Page counts, sizes, engagement
            "CAUSAL": self.analyze_content_relations,  # Parent-child, references
            "CONTEXTUAL": self.analyze_space_context,  # Space context, collections
        }

        logger.info("GitBookSpatialIntelligence initialized with 8 dimensions")

    async def initialize(self):
        """Initialize MCP adapter and connections"""
        await self.mcp_adapter.configure_gitbook_api("")
        logger.info("GitBook MCP adapter configured")

    # DIMENSION 1: HIERARCHY
    async def analyze_space_hierarchy(self, space_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze space hierarchy and structure (HIERARCHY dimension)"""
        hierarchy = {
            "level": "root",  # root, collection, page
            "type": "space",  # GitBook has spaces, collections, pages
            "depth": 0,
            "has_children": False,
            "parent_id": None,
            "child_collections": [],
            "child_pages": [],
            "space_id": space_data.get("id"),
            "space_name": space_data.get("name"),
        }

        # Check for collections and pages
        if collections := space_data.get("collections", []):
            hierarchy["has_children"] = True
            hierarchy["child_collections"] = [col.get("id") for col in collections]

        if pages := space_data.get("pages", []):
            hierarchy["has_children"] = True
            hierarchy["child_pages"] = [page.get("id") for page in pages]

        return hierarchy

    # DIMENSION 2: TEMPORAL
    async def analyze_content_timeline(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal patterns and content timeline (TEMPORAL dimension)"""
        from datetime import timezone

        now = datetime.now(timezone.utc)
        created = datetime.fromisoformat(page_data["createdAt"].replace("Z", "+00:00"))
        updated = datetime.fromisoformat(page_data["updatedAt"].replace("Z", "+00:00"))

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

        # Check for publishing timeline
        publishing_status = "published"
        if page_data.get("visibility") == "private":
            publishing_status = "draft"
        elif page_data.get("visibility") == "restricted":
            publishing_status = "review"

        return {
            "age_days": age_days,
            "last_activity_hours": last_activity_hours,
            "activity_level": activity_level,
            "publishing_status": publishing_status,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
            "content_freshness": (
                "fresh" if age_days < 30 else "established" if age_days < 90 else "legacy"
            ),
        }

    # DIMENSION 3: PRIORITY
    async def analyze_visibility_status(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visibility and access control (PRIORITY dimension)"""
        # GitBook has explicit visibility levels
        visibility = content_data.get("visibility", "public")
        priority_score = 0

        # Map visibility to priority
        if visibility == "public":
            priority_score = 3  # High priority - publicly accessible
        elif visibility == "restricted":
            priority_score = 2  # Medium priority - limited access
        elif visibility == "private":
            priority_score = 1  # Low priority - internal only

        # Check access level
        access_level = "read"
        if content_data.get("permissions", {}).get("write"):
            access_level = "write"
        if content_data.get("permissions", {}).get("admin"):
            access_level = "admin"

        # Determine content status
        content_status = "active"
        if content_data.get("archived"):
            content_status = "archived"
        elif content_data.get("draft"):
            content_status = "draft"

        return {
            "visibility": visibility,
            "priority_score": priority_score,
            "access_level": access_level,
            "content_status": content_status,
            "requires_approval": content_data.get("requiresApproval", False),
            "review_status": content_data.get("reviewStatus", "none"),
        }

    # DIMENSION 4: COLLABORATIVE
    async def analyze_user_activity(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user collaboration patterns (COLLABORATIVE dimension)"""
        # GitBook user roles and permissions
        role = user_data.get("role", "viewer")
        permissions = user_data.get("permissions", [])

        # Map role to collaboration level
        if role == "admin":
            collaboration_level = "full"
        elif role == "editor":
            collaboration_level = "moderate"
        elif role == "viewer":
            collaboration_level = "limited"
        else:
            collaboration_level = "none"

        # Activity patterns
        last_active = user_data.get("lastActive")
        if last_active:
            last_active_dt = datetime.fromisoformat(last_active.replace("Z", "+00:00"))
            hours_since_active = (datetime.now() - last_active_dt).total_seconds() / 3600

            if hours_since_active < 24:
                activity_status = "active"
            elif hours_since_active < 168:  # 1 week
                activity_status = "recent"
            else:
                activity_status = "inactive"
        else:
            activity_status = "unknown"

        return {
            "role": role,
            "collaboration_level": collaboration_level,
            "permissions": permissions,
            "activity_status": activity_status,
            "last_active": last_active,
            "can_edit": "write" in permissions,
            "can_admin": "admin" in permissions,
        }

    # DIMENSION 5: FLOW
    async def analyze_content_workflow(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content workflow states (FLOW dimension)"""
        # GitBook content workflow states
        current_state = content_data.get("state", "published")

        # Map states to workflow stages
        if current_state == "draft":
            workflow_stage = "creation"
        elif current_state == "review":
            workflow_stage = "approval"
        elif current_state == "published":
            workflow_stage = "live"
        elif current_state == "archived":
            workflow_stage = "retired"
        else:
            workflow_stage = "unknown"

        # Check workflow transitions
        workflow_transitions = []
        if content_data.get("draft"):
            workflow_transitions.append("draft_created")
        if content_data.get("reviewStatus") == "pending":
            workflow_transitions.append("review_requested")
        if content_data.get("published"):
            workflow_transitions.append("published")
        if content_data.get("archived"):
            workflow_transitions.append("archived")

        # Determine next action
        next_action = "none"
        if current_state == "draft":
            next_action = "submit_for_review"
        elif current_state == "review":
            next_action = "approve_or_reject"
        elif current_state == "published":
            next_action = "monitor_and_update"

        return {
            "current_state": current_state,
            "workflow_stage": workflow_stage,
            "workflow_transitions": workflow_transitions,
            "next_action": next_action,
            "requires_approval": content_data.get("requiresApproval", False),
            "approval_workflow": content_data.get("approvalWorkflow", "none"),
            "publishing_pipeline": content_data.get("publishingPipeline", "direct"),
        }

    # DIMENSION 6: QUANTITATIVE
    async def analyze_content_metrics(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quantitative content metrics (QUANTITATIVE dimension)"""
        # Page content metrics
        content_length = len(content_data.get("content", ""))
        word_count = len(content_data.get("content", "").split())

        # Estimate content size categories
        if word_count < 100:
            content_size = "small"
        elif word_count < 500:
            content_size = "medium"
        elif word_count < 2000:
            content_size = "large"
        else:
            content_size = "extensive"

        # Engagement metrics (if available)
        view_count = content_data.get("viewCount", 0)
        edit_count = content_data.get("editCount", 0)

        # Calculate engagement score
        engagement_score = 0
        if view_count > 0:
            engagement_score += min(view_count / 100, 5)  # Cap at 5 points
        if edit_count > 0:
            engagement_score += min(edit_count * 2, 5)  # Cap at 5 points

        return {
            "content_length": content_length,
            "word_count": word_count,
            "content_size": content_size,
            "view_count": view_count,
            "edit_count": edit_count,
            "engagement_score": round(engagement_score, 2),
            "media_count": len(content_data.get("media", [])),
            "link_count": len(content_data.get("links", [])),
        }

    # DIMENSION 7: CAUSAL
    async def analyze_content_relations(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content relationships and dependencies (CAUSAL dimension)"""
        # Parent-child relationships
        parent_id = content_data.get("parentId")
        children = content_data.get("children", [])

        # Cross-references and dependencies
        references = content_data.get("references", [])
        dependencies = content_data.get("dependencies", [])

        # Link analysis
        internal_links = [ref for ref in references if ref.get("type") == "internal"]
        external_links = [ref for ref in references if ref.get("type") == "external"]

        # Dependency analysis
        dependency_count = len(dependencies)
        if dependency_count == 0:
            dependency_status = "independent"
        elif dependency_count <= 3:
            dependency_status = "low_dependency"
        elif dependency_count <= 7:
            dependency_status = "medium_dependency"
        else:
            dependency_status = "high_dependency"

        return {
            "parent_id": parent_id,
            "children_count": len(children),
            "children_ids": [child.get("id") for child in children],
            "references_count": len(references),
            "internal_links": len(internal_links),
            "external_links": len(external_links),
            "dependencies_count": dependency_count,
            "dependency_status": dependency_status,
            "is_dependent": bool(parent_id),
            "has_dependents": len(children) > 0,
        }

    # DIMENSION 8: CONTEXTUAL
    async def analyze_space_context(self, space_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze space and collection context (CONTEXTUAL dimension)"""
        # Space purpose and themes
        space_purpose = space_data.get("purpose", "documentation")
        space_theme = space_data.get("theme", "general")

        # Collection analysis
        collections = space_data.get("collections", [])
        collection_themes = [col.get("theme", "general") for col in collections]

        # Organizational context
        organization = space_data.get("organization", {})
        org_name = organization.get("name", "Unknown")
        org_type = organization.get("type", "company")

        # Content organization patterns
        total_pages = sum(col.get("pageCount", 0) for col in collections)
        total_collections = len(collections)

        # Determine organization pattern
        if total_collections == 0:
            org_pattern = "flat"
        elif total_collections <= 3:
            org_pattern = "simple"
        elif total_collections <= 7:
            org_pattern = "moderate"
        else:
            org_pattern = "complex"

        return {
            "space_purpose": space_purpose,
            "space_theme": space_theme,
            "collection_themes": collection_themes,
            "organization_name": org_name,
            "organization_type": org_type,
            "total_pages": total_pages,
            "total_collections": total_collections,
            "organization_pattern": org_pattern,
            "content_focus": space_data.get("contentFocus", "general"),
            "target_audience": space_data.get("targetAudience", "internal"),
        }

    async def create_spatial_context(self, content_data: Dict[str, Any]) -> SpatialContext:
        """Create comprehensive 8-dimensional spatial context for GitBook content"""
        try:
            # Analyze all dimensions
            hierarchy_analysis = await self.analyze_space_hierarchy(content_data)
            temporal_analysis = await self.analyze_content_timeline(content_data)
            priority_analysis = await self.analyze_visibility_status(content_data)
            collaborative_analysis = await self.analyze_user_activity(content_data)
            flow_analysis = await self.analyze_content_workflow(content_data)
            quantitative_analysis = await self.analyze_content_metrics(content_data)
            causal_analysis = await self.analyze_content_relations(content_data)
            contextual_analysis = await self.analyze_space_context(content_data)

            # Determine attention level based on priority and activity
            attention_level = "medium"
            if priority_analysis["priority_score"] >= 3:
                attention_level = "high"
            elif temporal_analysis["activity_level"] == "stale":
                attention_level = "low"

            # Determine emotional valence based on content status
            emotional_valence = "neutral"
            if flow_analysis["current_state"] == "published":
                emotional_valence = "positive"
            elif flow_analysis["current_state"] == "archived":
                emotional_valence = "negative"

            # Determine navigation intent based on content type
            navigation_intent = "explore"
            if content_data.get("type") == "guide":
                navigation_intent = "learn"
            elif content_data.get("type") == "reference":
                navigation_intent = "lookup"

            # Create spatial context
            spatial_context = SpatialContext(
                territory_id="gitbook",
                room_id=content_data.get("spaceId", "unknown"),
                path_id=content_data.get("collectionId"),
                object_position=None,
                attention_level=attention_level,
                emotional_valence=emotional_valence,
                navigation_intent=navigation_intent,
                external_system="gitbook",
                external_id=content_data.get("id"),
                external_context={
                    "hierarchy": hierarchy_analysis,
                    "temporal": temporal_analysis,
                    "priority": priority_analysis,
                    "collaborative": collaborative_analysis,
                    "flow": flow_analysis,
                    "quantitative": quantitative_analysis,
                    "causal": causal_analysis,
                    "contextual": contextual_analysis,
                },
            )

            self._spatial_analytics["spatial_contexts_created"] += 1
            logger.info(f"Created spatial context for GitBook content {content_data.get('id')}")

            return spatial_context

        except Exception as e:
            logger.error(f"Failed to create spatial context for GitBook content: {e}")
            # Return basic context on failure
            return SpatialContext(
                territory_id="gitbook",
                room_id="unknown",
                external_system="gitbook",
                external_id=content_data.get("id", "unknown"),
            )

    async def map_content_to_position(self, content_data: Dict[str, Any]) -> SpatialPosition:
        """Map GitBook content to spatial position using MCP adapter"""
        try:
            # Create spatial context first
            spatial_context = await self.create_spatial_context(content_data)

            # Map to spatial position
            position = await self.mcp_adapter.map_to_position(
                content_data["id"],
                {
                    "space_id": content_data.get("spaceId"),
                    "collection_id": content_data.get("collectionId"),
                    "position": None,
                },
            )

            # Update spatial context with position
            spatial_context.object_position = position.position

            self._spatial_analytics["hierarchy_mappings"] += 1
            logger.info(
                f"Mapped GitBook content {content_data['id']} to position {position.position}"
            )

            return position

        except Exception as e:
            logger.error(f"Failed to map GitBook content to position: {e}")
            # Return default position on failure
            return SpatialPosition(position=0, context={"error": str(e)})

    async def close(self):
        """Close GitBook spatial intelligence and cleanup resources"""
        try:
            await self.mcp_adapter.close()
            logger.info("GitBookSpatialIntelligence closed successfully")
        except Exception as e:
            logger.error(f"Failed to close GitBookSpatialIntelligence: {e}")

    def get_analytics(self) -> Dict[str, Any]:
        """Get spatial analytics for monitoring"""
        return {
            "spaces_analyzed": self._spatial_analytics["spaces_analyzed"],
            "collections_analyzed": self._spatial_analytics["collections_analyzed"],
            "pages_analyzed": self._spatial_analytics["pages_analyzed"],
            "spatial_contexts_created": self._spatial_analytics["spatial_contexts_created"],
            "hierarchy_mappings": self._spatial_analytics["hierarchy_mappings"],
            "temporal_patterns": self._spatial_analytics["temporal_patterns"],
            "collaborative_insights": self._spatial_analytics["collaborative_insights"],
            "dimensions_implemented": len(self.dimensions),
        }

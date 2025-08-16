"""
GitBook Spatial Intelligence Implementation
Following ADR-013: MCP + Spatial Intelligence Pattern

Mirrors LinearSpatialIntelligence with 8-dimensional spatial analysis for GitBook documentation.
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
from services.mcp.consumer.gitbook_adapter import GitBookMCPSpatialAdapter

logger = logging.getLogger(__name__)


class GitBookSpatialIntelligence:
    """
    GitBook integration using MCP + Spatial Intelligence pattern.
    Following LinearSpatialIntelligence implementation pattern exactly.

    8 Dimensions:
    1. HIERARCHY - Space → Collection → Page → Sub-page structure
    2. TEMPORAL - Content creation, updates, publishing timeline
    3. PRIORITY - Content visibility, access levels, publishing status
    4. COLLABORATIVE - Authors, editors, permissions, contribution patterns
    5. FLOW - Content workflow states (draft, review, published, archived)
    6. QUANTITATIVE - Page counts, content sizes, engagement metrics
    7. CAUSAL - Content relationships, dependencies, references
    8. CONTEXTUAL - Space purpose, collection themes, organizational context
    """

    def __init__(self):
        """Initialize GitBook spatial intelligence with MCP adapter"""
        self.mcp_adapter = GitBookMCPSpatialAdapter()

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_space_hierarchy,
            "TEMPORAL": self.analyze_content_timeline,
            "PRIORITY": self.analyze_visibility_status,
            "COLLABORATIVE": self.analyze_user_activity,
            "FLOW": self.analyze_content_workflow,
            "QUANTITATIVE": self.analyze_content_metrics,
            "CAUSAL": self.analyze_content_relations,
            "CONTEXTUAL": self.analyze_space_context,
        }

        logger.info("GitBookSpatialIntelligence initialized with 8 dimensions")

    async def initialize(self):
        """Initialize MCP adapter and connections"""
        await self.mcp_adapter.configure_gitbook_api()
        logger.info("GitBook MCP adapter configured")

    # DIMENSION 1: HIERARCHY
    async def analyze_space_hierarchy(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze GitBook space/collection/page hierarchy"""
        hierarchy = {
            "level": "page",  # space, collection, page, sub-page
            "type": content.get("type", "page"),  # space, collection, page
            "depth": 0,
            "has_children": False,
            "parent_collection": None,
            "child_pages": [],
            "space_id": content.get("space_id"),
            "collection_id": content.get("collection_id"),
        }

        # Check content type and hierarchy level
        if content.get("type") == "space":
            hierarchy["level"] = "space"
            hierarchy["depth"] = 0
            if collections := content.get("collections", []):
                hierarchy["has_children"] = True
                hierarchy["child_pages"] = [col.get("name") for col in collections]

        elif content.get("type") == "collection":
            hierarchy["level"] = "collection"
            hierarchy["depth"] = 1
            if pages := content.get("pages", []):
                hierarchy["has_children"] = True
                hierarchy["child_pages"] = [page.get("title") for page in pages]

        elif content.get("type") == "page":
            hierarchy["level"] = "page"
            hierarchy["depth"] = 2
            if parent := content.get("parent"):
                hierarchy["parent_collection"] = parent.get("title")
            if children := content.get("children", []):
                hierarchy["has_children"] = True
                hierarchy["child_pages"] = [child.get("title") for child in children]
                hierarchy["depth"] = 3  # Has sub-pages

        # Check for sub-page
        if parent_page := content.get("parent_page"):
            hierarchy["level"] = "sub-page"
            hierarchy["depth"] = 3
            hierarchy["parent_collection"] = parent_page.get("title")

        return hierarchy

    # DIMENSION 2: TEMPORAL
    async def analyze_content_timeline(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content temporal patterns and publishing timeline"""
        from datetime import timezone

        now = datetime.now(timezone.utc)
        created = datetime.fromisoformat(
            content.get("created_at", now.isoformat()).replace("Z", "+00:00")
        )
        updated = datetime.fromisoformat(
            content.get("updated_at", now.isoformat()).replace("Z", "+00:00")
        )

        # Calculate content metrics
        age_days = (now - created).total_seconds() / 86400
        last_activity_hours = (now - updated).total_seconds() / 3600

        # Determine activity level
        if last_activity_hours < 1:
            activity_level = "active"
        elif last_activity_hours < 24:
            activity_level = "recent"
        elif last_activity_hours < 168:  # 1 week
            activity_level = "moderate"
        else:
            activity_level = "stale"

        # Check content urgency based on publishing status
        urgency = "normal"
        status = content.get("status", "published")
        if status == "draft" and age_days > 7:
            urgency = "high"  # Draft sitting too long
        elif status == "review" and age_days > 1:
            urgency = "medium"  # In review for a day

        # Check for scheduled publishing
        if publish_at := content.get("publish_at"):
            publish_time = datetime.fromisoformat(publish_at.replace("Z", "+00:00"))
            hours_to_publish = (publish_time - now).total_seconds() / 3600
            if hours_to_publish <= 2:
                urgency = "high"

        # Publishing timeline
        published_at = content.get("published_at")
        first_published = content.get("first_published_at")

        return {
            "age_days": age_days,
            "last_activity_hours": last_activity_hours,
            "activity_level": activity_level,
            "urgency": urgency,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
            "published_at": published_at,
            "first_published_at": first_published,
            "publish_at": content.get("publish_at"),
            "content_freshness": "fresh" if last_activity_hours < 24 else "aging",
        }

    # DIMENSION 3: PRIORITY
    async def analyze_visibility_status(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content visibility, access levels, and publishing priority"""
        visibility = content.get("visibility", "private")
        status = content.get("status", "draft")
        access_level = content.get("access", "restricted")

        # Determine priority level based on visibility and status
        priority_level = "normal"
        if visibility == "public" and status == "published":
            priority_level = "high"
        elif visibility == "public" or status == "published":
            priority_level = "medium"
        elif status == "archived":
            priority_level = "low"
        elif visibility == "private":
            priority_level = "normal"

        # Calculate attention score (0.0 - 1.0)
        attention_score = 0.5  # Base score

        if priority_level == "high":
            attention_score = 0.9
        elif priority_level == "medium":
            attention_score = 0.7
        elif priority_level == "low":
            attention_score = 0.3

        # Boost for public content
        if visibility == "public":
            attention_score = min(1.0, attention_score + 0.2)

        # Boost for featured content
        if content.get("featured"):
            attention_score = min(1.0, attention_score + 0.3)

        # Check for content tags/categories
        tags = content.get("tags", [])
        is_important = "important" in tags or "featured" in tags
        is_documentation = "docs" in tags or "documentation" in tags

        if is_important:
            priority_level = "high"
            attention_score = 1.0

        return {
            "priority_level": priority_level,
            "visibility": visibility,
            "status": status,
            "access_level": access_level,
            "is_public": visibility == "public",
            "is_published": status == "published",
            "is_featured": content.get("featured", False),
            "is_important": is_important,
            "is_documentation": is_documentation,
            "attention_score": attention_score,
            "tags": tags,
        }

    # DIMENSION 4: COLLABORATIVE
    async def analyze_user_activity(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user collaboration and content contribution patterns"""
        # Get creator/author
        author = content.get("created_by", {}).get("name") if content.get("created_by") else None

        # Get contributors and editors
        contributors = []
        if contribs := content.get("contributors", []):
            contributors = [c.get("name") for c in contribs if c.get("name")]

        # Get recent editors
        recent_editors = []
        if editors := content.get("recent_editors", []):
            recent_editors = [e.get("name") for e in editors if e.get("name")]

        # Content edit count
        edit_count = content.get("revision_count", 0)

        # Determine engagement level
        total_participants = len(set(contributors + recent_editors + ([author] if author else [])))

        if total_participants >= 5:
            engagement_level = "high"
        elif total_participants >= 2:
            engagement_level = "moderate"
        else:
            engagement_level = "low"

        # Check for collaborative features
        has_comments = bool(content.get("comments", []))
        has_suggestions = bool(content.get("suggestions", []))

        return {
            "author": author,
            "contributor_count": len(contributors),
            "editor_count": len(recent_editors),
            "edit_count": edit_count,
            "engagement_level": engagement_level,
            "participants": list(set(contributors + recent_editors + ([author] if author else []))),
            "contributors": contributors,
            "recent_editors": recent_editors,
            "has_comments": has_comments,
            "has_suggestions": has_suggestions,
            "comment_count": len(content.get("comments", [])),
        }

    # DIMENSION 5: FLOW
    async def analyze_content_workflow(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content workflow states and publishing progress"""
        status = content.get("status", "draft")
        visibility = content.get("visibility", "private")

        # Map content status to workflow stages
        workflow_stage_map = {
            "draft": "editing",
            "review": "reviewing",
            "published": "published",
            "archived": "archived",
            "scheduled": "scheduled",
        }

        workflow_stage = workflow_stage_map.get(status.lower(), "unknown")

        # Check if blocked or needs attention
        is_blocked = status == "blocked" or content.get("requires_approval", False)

        # Check publishing readiness
        is_ready_to_publish = status == "review" and not content.get("has_issues", False)

        # Estimate content completeness
        completeness = 0
        if title := content.get("title"):
            completeness += 30  # Has title
        if body := content.get("body"):
            completeness += 50  # Has content
            if len(body) > 500:  # Substantial content
                completeness += 20

        # Check for metadata completeness
        if content.get("description"):
            completeness += 10
        if content.get("tags"):
            completeness += 10

        return {
            "status": status,
            "visibility": visibility,
            "workflow_stage": workflow_stage,
            "is_blocked": is_blocked,
            "is_ready_to_publish": is_ready_to_publish,
            "completeness_percentage": min(100, completeness),
            "is_published": status == "published",
            "is_draft": status == "draft",
            "needs_review": status == "review",
            "can_publish": completeness >= 80 and not is_blocked,
        }

    # DIMENSION 6: QUANTITATIVE
    async def analyze_content_metrics(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quantitative content metrics and engagement"""
        from datetime import timezone

        created = datetime.fromisoformat(
            content.get("created_at", datetime.now().isoformat()).replace("Z", "+00:00")
        )
        now = datetime.now(timezone.utc)

        # Content size metrics
        title_length = len(content.get("title", ""))
        body_length = len(content.get("body", ""))
        word_count = len(content.get("body", "").split()) if content.get("body") else 0

        # Engagement metrics
        view_count = content.get("views", 0)
        like_count = content.get("likes", 0)
        share_count = content.get("shares", 0)
        comment_count = len(content.get("comments", []))

        # Calculate pages in collection/space
        page_count = 1  # This page
        if pages := content.get("sibling_pages", []):
            page_count = len(pages) + 1

        # Estimate reading time (words per minute)
        reading_time_minutes = max(1, word_count // 200) if word_count > 0 else 1

        # Content complexity estimation
        complexity = "low"
        if word_count > 5000 or comment_count > 20:
            complexity = "high"
        elif word_count > 1000 or comment_count > 5:
            complexity = "medium"

        # Engagement rate calculation
        engagement_rate = 0
        if view_count > 0:
            engagement_rate = ((like_count + comment_count + share_count) / view_count) * 100

        return {
            "title_length": title_length,
            "body_length": body_length,
            "word_count": word_count,
            "reading_time_minutes": reading_time_minutes,
            "view_count": view_count,
            "like_count": like_count,
            "share_count": share_count,
            "comment_count": comment_count,
            "page_count": page_count,
            "engagement_rate": engagement_rate,
            "complexity_estimate": complexity,
            "has_media": bool(content.get("attachments", [])),
            "attachment_count": len(content.get("attachments", [])),
        }

    # DIMENSION 7: CAUSAL
    async def analyze_content_relations(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content relationships, dependencies, and references"""
        # Get content relationships
        parent_page = content.get("parent")
        child_pages = content.get("children", [])
        related_pages = content.get("related", [])

        # Check for internal links and references
        internal_links = content.get("internal_links", [])
        external_links = content.get("external_links", [])
        backlinks = content.get("backlinks", [])

        # Content prerequisites and dependencies
        prerequisites = content.get("prerequisites", [])
        depends_on = content.get("depends_on", [])

        # Reference chain analysis
        reference_chain_length = len(internal_links) + len(external_links) + len(related_pages)

        # Check for content templates or patterns
        is_template = content.get("is_template", False)
        template_used = content.get("template_id") is not None

        return {
            "parent_page": parent_page.get("title") if parent_page else None,
            "child_page_count": len(child_pages),
            "related_page_count": len(related_pages),
            "internal_link_count": len(internal_links),
            "external_link_count": len(external_links),
            "backlink_count": len(backlinks),
            "prerequisite_count": len(prerequisites),
            "dependency_count": len(depends_on),
            "reference_chain_length": reference_chain_length,
            "has_dependencies": reference_chain_length > 0,
            "is_referenced": len(backlinks) > 0,
            "is_template": is_template,
            "uses_template": template_used,
            "connectivity_score": len(internal_links) + len(backlinks),
        }

    # DIMENSION 8: CONTEXTUAL
    async def analyze_space_context(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze space, collection, and organizational context"""
        # Get space information
        space_name = (
            content.get("space", {}).get("title", "unknown") if content.get("space") else "unknown"
        )
        collection_name = (
            content.get("collection", {}).get("title", "unknown")
            if content.get("collection")
            else "unknown"
        )

        # Content categorization
        content_type = "page"
        if content.get("type") == "space":
            content_type = "space"
        elif content.get("type") == "collection":
            content_type = "collection"
        elif content.get("is_index"):
            content_type = "index"
        elif content.get("is_template"):
            content_type = "template"

        # Determine domain based on content type and tags
        domain = "general"
        tags = content.get("tags", [])
        tag_text = " ".join(tags).lower()
        title_text = content.get("title", "").lower()

        if any(
            keyword in tag_text + title_text
            for keyword in ["api", "technical", "developer", "code"]
        ):
            domain = "technical_documentation"
        elif any(
            keyword in tag_text + title_text for keyword in ["user", "guide", "tutorial", "how-to"]
        ):
            domain = "user_documentation"
        elif any(
            keyword in tag_text + title_text
            for keyword in ["process", "policy", "procedure", "workflow"]
        ):
            domain = "process_documentation"
        elif any(
            keyword in tag_text + title_text for keyword in ["design", "architecture", "system"]
        ):
            domain = "design_documentation"

        # Organization context
        organization = (
            content.get("organization", {}).get("name", "unknown")
            if content.get("organization")
            else "unknown"
        )
        team = content.get("team", {}).get("name", "unknown") if content.get("team") else "unknown"

        return {
            "space_name": space_name,
            "collection_name": collection_name,
            "content_type": content_type,
            "domain": domain,
            "organization": organization,
            "team": team,
            "tags": tags,
            "full_path": (
                f"{space_name}/{collection_name}" if collection_name != "unknown" else space_name
            ),
            "is_public_space": content.get("space", {}).get("visibility") == "public",
        }

    # MAIN SPATIAL CONTEXT CREATION
    async def create_spatial_context(self, content: Dict[str, Any]) -> SpatialContext:
        """Create full 8-dimensional spatial context for GitBook content"""
        # Run all dimensional analyses in parallel
        dimension_results = await asyncio.gather(
            self.analyze_space_hierarchy(content),
            self.analyze_content_timeline(content),
            self.analyze_visibility_status(content),
            self.analyze_user_activity(content),
            self.analyze_content_workflow(content),
            self.analyze_content_metrics(content),
            self.analyze_content_relations(content),
            self.analyze_space_context(content),
        )

        # Unpack results
        hierarchy, temporal, priority, collaborative, flow, quantitative, causal, contextual = (
            dimension_results
        )

        # Determine attention level based on priority and workflow
        if priority["priority_level"] == "high" or flow["is_blocked"]:
            attention_level = "urgent"
        elif priority["priority_level"] == "medium" or flow["needs_review"]:
            attention_level = "high"
        elif temporal["activity_level"] == "stale" or flow["is_draft"]:
            attention_level = "low"
        else:
            attention_level = "medium"

        # Determine emotional valence
        if flow["is_blocked"] or temporal["urgency"] == "high":
            emotional_valence = "negative"
        elif flow["is_published"] and priority["is_public"]:
            emotional_valence = "positive"
        else:
            emotional_valence = "neutral"

        # Determine navigation intent
        if flow["is_blocked"] or temporal["urgency"] == "high":
            navigation_intent = "investigate"
        elif flow["needs_review"] or priority["priority_level"] == "high":
            navigation_intent = "monitor"
        elif flow["is_draft"]:
            navigation_intent = "respond"
        else:
            navigation_intent = "explore"

        # Create spatial context
        return SpatialContext(
            territory_id="gitbook",
            room_id=contextual["space_name"],
            path_id=(
                f"content/{content['title']}"
                if content.get("title")
                else f"content/{content.get('id', 'unknown')}"
            ),
            attention_level=attention_level,
            emotional_valence=emotional_valence,
            navigation_intent=navigation_intent,
            external_system="gitbook",
            external_id=str(content.get("id", content.get("title", "unknown"))),
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
    async def map_content_to_position(
        self, content_id: str, context: Dict[str, Any]
    ) -> SpatialPosition:
        """Map GitBook content to spatial position using MCP adapter"""
        return await self.mcp_adapter.map_to_position(content_id, context)

    async def get_page(self, space_id: str, page_id: str) -> Dict[str, Any]:
        """Get page data using MCP adapter (backward compatibility)"""
        return await self.mcp_adapter.get_page(space_id, page_id)

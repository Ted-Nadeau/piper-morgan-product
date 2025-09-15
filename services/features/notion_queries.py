"""
Notion Knowledge Management Canonical Query Extension
Built on canonical handlers and Notion MCP adapter infrastructure

Following the established pattern from issue_intelligence.py
Extends existing CanonicalHandlers with Notion knowledge intelligence
Performance target: <200ms enhancement, preserves original response structure
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from services.domain.models import Intent
from services.domain.notion_domain_service import NotionDomainService
from services.intelligence.spatial.notion_spatial import NotionSpatialIntelligence
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


@dataclass
class NotionContext:
    """Context object containing Notion knowledge management data"""

    user_id: str
    workspace_id: Optional[str] = None
    relevant_pages: List[Dict[str, Any]] = field(default_factory=list)
    recent_updates: List[Dict[str, Any]] = field(default_factory=list)
    knowledge_areas: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class NotionIntelligenceResult:
    """Result object containing enhanced canonical response with Notion intelligence"""

    original_response: Dict[str, Any]
    enhanced_message: str
    notion_intelligence: Dict[str, Any]
    context_source: str = "notion_mcp_adapter"
    enhancement_time_ms: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)


class NotionCanonicalQueryEngine:
    """
    Notion Knowledge Management Canonical Query Engine

    Enhances existing CanonicalHandlers with Notion knowledge intelligence
    while preserving original response structure and behavior.
    """

    def __init__(
        self,
        canonical_handlers: CanonicalHandlers,
        user_id: str,
    ):
        self.canonical_handlers = canonical_handlers
        self.user_id = user_id

        # Initialize Notion integrations
        self.notion_domain_service = NotionDomainService()
        self.spatial_intelligence = NotionSpatialIntelligence()

        # Performance tracking
        self._query_count = 0
        self._total_enhancement_time = 0.0

    async def enhance_canonical_query(
        self, intent: Intent, session_id: str
    ) -> Optional[NotionIntelligenceResult]:
        """
        Enhance canonical query response with Notion knowledge intelligence.

        Args:
            intent: The original user intent
            session_id: Session identifier for context

        Returns:
            NotionIntelligenceResult with enhanced response and Notion context
        """
        start_time = time.time()

        try:
            # Get original canonical response
            original_response = await self.canonical_handlers.handle_intent(intent, session_id)

            # Check if Notion is configured
            if not self.notion_domain_service.is_configured():
                return NotionIntelligenceResult(
                    original_response=original_response,
                    enhanced_message=original_response.get("message", ""),
                    notion_intelligence={
                        "status": "not_configured",
                        "message": "Notion integration not configured",
                    },
                )

            # Extract knowledge context from intent
            notion_context = await self._extract_notion_context(intent)

            # Enhance response with Notion intelligence
            enhanced_response = await self._enhance_with_notion_intelligence(
                original_response, notion_context, intent
            )

            # Calculate performance metrics
            enhancement_time_ms = int((time.time() - start_time) * 1000)
            self._query_count += 1
            self._total_enhancement_time += enhancement_time_ms

            return NotionIntelligenceResult(
                original_response=original_response,
                enhanced_message=enhanced_response["message"],
                notion_intelligence=enhanced_response["notion_intelligence"],
                enhancement_time_ms=enhancement_time_ms,
            )

        except Exception as e:
            # Graceful degradation - return original response if enhancement fails
            enhancement_time_ms = int((time.time() - start_time) * 1000)

            return NotionIntelligenceResult(
                original_response=original_response if "original_response" in locals() else {},
                enhanced_message=(
                    original_response.get("message", "") if "original_response" in locals() else ""
                ),
                notion_intelligence={
                    "error": str(e),
                    "status": "enhancement_failed",
                    "fallback": True,
                },
                enhancement_time_ms=enhancement_time_ms,
            )

    async def _extract_notion_context(self, intent: Intent) -> NotionContext:
        """Extract relevant Notion context based on user intent."""
        try:
            # Connect to Notion if not already connected
            if not await self.notion_domain_service.connect():
                return NotionContext(user_id=self.user_id)

            # Search for relevant pages based on intent text
            relevant_pages = await self._search_notion_pages(intent.text)

            # Get recent updates in workspace
            recent_updates = await self._get_recent_updates()

            return NotionContext(
                user_id=self.user_id,
                relevant_pages=relevant_pages,
                recent_updates=recent_updates,
                knowledge_areas=self._extract_knowledge_areas(intent.text),
            )

        except Exception as e:
            # Return empty context if extraction fails
            return NotionContext(user_id=self.user_id)

    async def _search_notion_pages(self, query: str) -> List[Dict[str, Any]]:
        """Search Notion pages relevant to the query."""
        try:
            if not self.notion_domain_service._notion_client:
                return []

            # Use Notion search API to find relevant pages
            # This is a placeholder - actual implementation would use notion_client.search()
            # For now, return empty list to maintain graceful degradation
            return []

        except Exception:
            return []

    async def _get_recent_updates(self) -> List[Dict[str, Any]]:
        """Get recent updates from Notion workspace."""
        try:
            # Placeholder for recent updates functionality
            # Would query recent page modifications
            return []

        except Exception:
            return []

    def _extract_knowledge_areas(self, text: str) -> List[str]:
        """Extract knowledge areas from intent text."""
        # Simple keyword-based extraction
        knowledge_keywords = [
            "project",
            "task",
            "meeting",
            "documentation",
            "plan",
            "requirement",
            "specification",
            "design",
            "architecture",
        ]

        text_lower = text.lower()
        return [keyword for keyword in knowledge_keywords if keyword in text_lower]

    async def _enhance_with_notion_intelligence(
        self, original_response: Dict[str, Any], notion_context: NotionContext, intent: Intent
    ) -> Dict[str, Any]:
        """Enhance original response with Notion intelligence."""

        enhanced_message = original_response.get("message", "")
        notion_intelligence = {
            "workspace_connected": self.notion_domain_service.is_configured(),
            "relevant_pages_count": len(notion_context.relevant_pages),
            "recent_updates_count": len(notion_context.recent_updates),
            "knowledge_areas": notion_context.knowledge_areas,
        }

        # Add Notion-specific enhancements based on intent category
        if intent.category == IntentCategory.PROJECT_MANAGEMENT:
            if notion_context.relevant_pages:
                enhanced_message += f"\n\n📋 Found {len(notion_context.relevant_pages)} related pages in Notion workspace."
                notion_intelligence["project_context"] = True

        elif intent.category == IntentCategory.GENERAL_QUESTION:
            if notion_context.knowledge_areas:
                enhanced_message += (
                    f"\n\n🧠 Related knowledge areas: {', '.join(notion_context.knowledge_areas)}"
                )
                notion_intelligence["knowledge_context"] = notion_context.knowledge_areas

        return {"message": enhanced_message, "notion_intelligence": notion_intelligence}

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for Notion query enhancement."""
        avg_time = self._total_enhancement_time / max(self._query_count, 1)

        return {
            "total_queries": self._query_count,
            "average_enhancement_time_ms": avg_time,
            "total_enhancement_time_ms": self._total_enhancement_time,
            "adapter_configured": self.notion_domain_service.is_configured(),
        }


# Utility function for easy integration
async def enhance_with_notion_intelligence(
    intent: Intent, session_id: str, canonical_handlers: CanonicalHandlers, user_id: str = "default"
) -> NotionIntelligenceResult:
    """
    Convenience function to enhance any intent with Notion intelligence.

    Usage:
        result = await enhance_with_notion_intelligence(intent, session_id, handlers)
        enhanced_message = result.enhanced_message
    """
    engine = NotionCanonicalQueryEngine(canonical_handlers, user_id)
    return await engine.enhance_canonical_query(intent, session_id)

"""
Document Memory Canonical Query Extension - Core Implementation
Built on canonical handlers and document infrastructure

Created: 2025-08-25 by Document Memory Integration Sprint
Extends existing CanonicalHandlers with document memory intelligence
Performance target: <200ms enhancement, graceful degradation
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


@dataclass
class DocumentMemoryContext:
    """Context object containing document memory data"""

    user_id: str
    timeframe: str
    relevant_documents: List[Dict[str, Any]] = field(default_factory=list)
    decisions_found: List[Dict[str, Any]] = field(default_factory=list)
    patterns_discovered: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DocumentMemoryResult:
    """Result object containing enhanced canonical response with document memory"""

    original_response: Dict[str, Any]
    enhanced_message: str
    document_memory: Dict[str, Any]
    context_source: str = "document_memory"
    enhancement_time_ms: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)


class DocumentMemoryQueries:
    """
    Document Memory Canonical Query Engine

    Extends canonical query capabilities with document memory intelligence
    while maintaining full compatibility with existing query patterns.

    Architecture:
    - Integrates with existing DocumentService and DocumentAnalyzer
    - Provides canonical queries for document memory retrieval
    - Enables cross-feature integration (Morning Standup, Issue Intelligence)
    - Graceful degradation when document infrastructure unavailable
    """

    def __init__(
        self,
        canonical_handlers: Optional[CanonicalHandlers] = None,
        user_id: str = "default",
    ):
        """Initialize with required dependencies"""
        self.canonical_handlers = canonical_handlers or CanonicalHandlers()
        self.user_id = user_id

        # Initialize document infrastructure with graceful fallback
        self._document_service = None
        self._document_analyzer = None
        self._initialize_document_services()

        # Define canonical document memory queries
        self.canonical_queries = {
            "what_did_we_decide": self.find_decisions,
            "what_context_exists": self.get_relevant_context,
            "what_should_i_review": self.suggest_documents,
            "what_patterns_exist": self.discover_patterns,
            "what_was_learned": self.get_learning_summary,
        }

    def _initialize_document_services(self):
        """Initialize document services with graceful degradation"""
        try:
            from services.knowledge_graph.document_service import get_document_service

            self._document_service = get_document_service()
        except ImportError:
            self._document_service = None

        try:
            from services.analysis.document_analyzer import DocumentAnalyzer

            self._document_analyzer = DocumentAnalyzer()
        except ImportError:
            self._document_analyzer = None

    async def enhance_canonical_query(
        self, intent: Intent, session_id: str
    ) -> DocumentMemoryResult:
        """
        Enhance canonical query responses with document memory intelligence

        Args:
            intent: Intent object from canonical query
            session_id: Session identifier

        Returns:
            DocumentMemoryResult with enhanced response and memory data
        """
        start_time = time.time()

        # Step 1: Get original canonical response (delegate to existing handlers)
        original_response = await self.canonical_handlers.handle(intent, session_id)

        # Step 2: Gather document memory based on query category
        document_memory = await self._gather_document_memory(intent)

        # Step 3: Enhance the message with document context
        enhanced_message = await self._enhance_message_with_documents(
            original_response.get("message", ""), document_memory, intent
        )

        # Step 4: Calculate performance metrics
        enhancement_time_ms = int((time.time() - start_time) * 1000)

        return DocumentMemoryResult(
            original_response=original_response,
            enhanced_message=enhanced_message,
            document_memory=document_memory,
            context_source="document_memory",
            enhancement_time_ms=enhancement_time_ms,
        )

    async def find_decisions(self, topic: str = "", timeframe: str = "last_week") -> Dict[str, Any]:
        """Find previous decisions on topic within timeframe."""
        try:
            # Mock implementation - would integrate with actual document search
            decisions = []

            if topic:
                # Simulate topic-based decision search
                decisions.append(
                    {
                        "topic": topic,
                        "decision": f"Previous decision on {topic}",
                        "date": (datetime.now() - timedelta(days=3)).isoformat(),
                        "context": "Document memory simulation",
                        "confidence": 0.8,
                    }
                )

            return {
                "decisions": decisions,
                "topic": topic,
                "timeframe": timeframe,
                "count": len(decisions),
                "source": "document_memory_mock",
            }
        except Exception as e:
            return {
                "decisions": [],
                "error": f"Decision search unavailable: {str(e)}",
                "fallback_mode": True,
            }

    async def get_relevant_context(self, timeframe: str = "yesterday") -> Dict[str, Any]:
        """Get relevant document context for timeframe."""
        try:
            # Mock implementation - would integrate with actual document retrieval
            context_docs = []

            if timeframe == "yesterday":
                context_docs.append(
                    {
                        "title": "Recent session logs",
                        "summary": "Development progress from yesterday",
                        "relevance": 0.9,
                        "type": "session_log",
                    }
                )
            elif timeframe == "last_week":
                context_docs.extend(
                    [
                        {
                            "title": "Weekly pattern discoveries",
                            "summary": "Patterns discovered in recent development",
                            "relevance": 0.8,
                            "type": "pattern_analysis",
                        },
                        {
                            "title": "Integration learnings",
                            "summary": "Lessons from recent integrations",
                            "relevance": 0.7,
                            "type": "integration_notes",
                        },
                    ]
                )

            return {
                "context_documents": context_docs,
                "timeframe": timeframe,
                "count": len(context_docs),
                "source": "document_memory_mock",
            }
        except Exception as e:
            return {
                "context_documents": [],
                "error": f"Context retrieval unavailable: {str(e)}",
                "fallback_mode": True,
            }

    async def suggest_documents(self, focus_area: str = "") -> Dict[str, Any]:
        """Suggest documents to review based on focus area."""
        try:
            suggestions = []

            if focus_area:
                suggestions.append(
                    {
                        "title": f"Documentation related to {focus_area}",
                        "reason": f"Relevant to your focus on {focus_area}",
                        "priority": "high",
                        "type": "focused_review",
                    }
                )

            # Always suggest pattern review
            suggestions.append(
                {
                    "title": "Pattern catalog updates",
                    "reason": "Check for new patterns from recent work",
                    "priority": "medium",
                    "type": "pattern_review",
                }
            )

            return {
                "suggestions": suggestions,
                "focus_area": focus_area,
                "count": len(suggestions),
                "source": "document_memory_mock",
            }
        except Exception as e:
            return {
                "suggestions": [],
                "error": f"Document suggestions unavailable: {str(e)}",
                "fallback_mode": True,
            }

    async def discover_patterns(self, scope: str = "recent") -> Dict[str, Any]:
        """Discover patterns in documents within scope."""
        try:
            patterns = []

            if scope == "recent":
                patterns.extend(
                    [
                        "Verification-first methodology adoption",
                        "Canonical query extension pattern",
                        "Graceful degradation implementation",
                    ]
                )

            return {
                "patterns": patterns,
                "scope": scope,
                "count": len(patterns),
                "confidence": 0.75,
                "source": "document_memory_mock",
            }
        except Exception as e:
            return {
                "patterns": [],
                "error": f"Pattern discovery unavailable: {str(e)}",
                "fallback_mode": True,
            }

    async def get_learning_summary(self, timeframe: str = "yesterday") -> Dict[str, Any]:
        """Get summary of what was learned in timeframe."""
        try:
            learnings = []

            if timeframe == "yesterday":
                learnings.extend(
                    [
                        "Formal pattern sweep methodology discovered",
                        "Document memory integration architecture planned",
                        "Canonical query extension patterns validated",
                    ]
                )

            return {
                "learnings": learnings,
                "timeframe": timeframe,
                "count": len(learnings),
                "source": "document_memory_mock",
            }
        except Exception as e:
            return {
                "learnings": [],
                "error": f"Learning summary unavailable: {str(e)}",
                "fallback_mode": True,
            }

    async def create_document_memory_context(
        self, timeframe: str = "yesterday"
    ) -> DocumentMemoryContext:
        """
        Create document memory context for canonical query integration

        Args:
            timeframe: Time period for document memory retrieval

        Returns:
            DocumentMemoryContext with relevant document data
        """
        # Get relevant documents and context
        context_data = await self.get_relevant_context(timeframe)
        decisions_data = await self.find_decisions(timeframe=timeframe)
        patterns_data = await self.discover_patterns()

        return DocumentMemoryContext(
            user_id=self.user_id,
            timeframe=timeframe,
            relevant_documents=context_data.get("context_documents", []),
            decisions_found=decisions_data.get("decisions", []),
            patterns_discovered=patterns_data.get("patterns", []),
        )

    async def _gather_document_memory(self, intent: Intent) -> Dict[str, Any]:
        """Gather relevant document memory based on intent category"""

        memory = {}

        try:
            if intent.category == IntentCategory.STATUS:
                # For status queries, get recent context and decisions
                context_data = await self.get_relevant_context("yesterday")
                memory.update(context_data)

            elif intent.category == IntentCategory.GUIDANCE:
                # For guidance queries, get patterns and suggestions
                patterns_data = await self.discover_patterns("recent")
                suggestions_data = await self.suggest_documents()
                memory.update(patterns_data)
                memory.update(suggestions_data)

            elif intent.category == IntentCategory.PRIORITY:
                # For priority queries, get decisions and learning summary
                decisions_data = await self.find_decisions()
                learnings_data = await self.get_learning_summary()
                memory.update(decisions_data)
                memory.update(learnings_data)

            else:
                # Default memory for other categories
                context_data = await self.get_relevant_context("yesterday")
                memory.update(context_data)

        except Exception as e:
            # Graceful degradation - don't break canonical queries
            memory["error"] = f"Document memory temporarily unavailable: {str(e)}"
            memory["fallback_mode"] = True

        return memory

    async def _enhance_message_with_documents(
        self, original_message: str, document_memory: Dict[str, Any], intent: Intent
    ) -> str:
        """Enhance original message with document memory context"""

        if document_memory.get("fallback_mode"):
            # Don't modify message if document memory failed
            return original_message

        enhanced_message = original_message

        # Add document context based on intent category
        if intent.category == IntentCategory.STATUS and "context_documents" in document_memory:
            context_docs = document_memory["context_documents"]
            if context_docs:
                enhanced_message += "\n\n**Recent Document Context:**"
                for doc in context_docs[:2]:  # Top 2 documents
                    enhanced_message += f"\n📄 {doc['title']}: {doc['summary']}"

        elif intent.category == IntentCategory.GUIDANCE and "patterns" in document_memory:
            patterns = document_memory["patterns"]
            if patterns:
                enhanced_message += "\n\n**Discovered Patterns:**"
                for pattern in patterns[:3]:  # Top 3 patterns
                    enhanced_message += f"\n🔍 {pattern}"

        elif intent.category == IntentCategory.PRIORITY and "decisions" in document_memory:
            decisions = document_memory["decisions"]
            if decisions:
                enhanced_message += "\n\n**Recent Decisions:**"
                for decision in decisions[:2]:  # Top 2 decisions
                    enhanced_message += f"\n✅ {decision['topic']}: {decision['decision']}"

        return enhanced_message

"""
Context-relevant memory retrieval for workspace switching.

Part of #661 WORKSPACE-MEMORY (child of #416 MUX-INTERACT-WORKSPACE epic).

This module provides:
- ContextMemory: Memory relevant to a specific context
- get_relevant_memory(): Retrieve memory filtered by isolation rules
- on_context_switch(): Handle context switch with memory retrieval

Integrates with:
- #657 ConversationalMemoryService (working memory)
- #663 UserHistoryService (long-term memory)
- #660 ContextIsolation (boundary filtering)
- #658 ContextSwitch (trigger)
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from services.memory.conversational_memory import (
    ConversationalMemoryEntry,
    ConversationalMemoryService,
)
from services.memory.user_history import ConversationSummary, UserHistoryService
from services.mux.workspace_detection import ContextSwitch, WorkspaceContext
from services.mux.workspace_isolation import CategorizedContext, ContextIsolation

logger = logging.getLogger(__name__)


# =============================================================================
# Domain Models
# =============================================================================


@dataclass
class ContextMemory:
    """
    Memory relevant to a specific context.

    Three layers of memory, filtered by isolation rules:
    - immediate: Current conversation buffer (turns)
    - working: Cross-session, 7-day window (ConversationalMemoryEntry)
    - longterm: User-wide, highly relevant only (ConversationSummary)
    """

    immediate: List[Dict[str, Any]] = field(default_factory=list)
    working: List[ConversationalMemoryEntry] = field(default_factory=list)
    longterm: List[ConversationSummary] = field(default_factory=list)

    def is_empty(self) -> bool:
        """Check if all memory layers are empty."""
        return not (self.immediate or self.working or self.longterm)

    def total_entries(self) -> int:
        """Total count across all layers."""
        return len(self.immediate) + len(self.working) + len(self.longterm)

    @property
    def has_immediate(self) -> bool:
        """Has current conversation context."""
        return len(self.immediate) > 0

    @property
    def has_working(self) -> bool:
        """Has recent cross-session context."""
        return len(self.working) > 0

    @property
    def has_longterm(self) -> bool:
        """Has relevant historical context."""
        return len(self.longterm) > 0


# =============================================================================
# Categorization Bridge
# =============================================================================


def default_workspace_categorizer(ctx: WorkspaceContext) -> CategorizedContext:
    """
    Default categorizer for WorkspaceContext.

    Maps workspace_type to a category for isolation rules:
    - slack → "work" (default, can be overridden)
    - web → "work"
    - cli → "work"
    - api → "work"

    Uses workspace_id as the primary identifier.
    """
    # Default to "work" category - can be enhanced with user preferences
    category = "work"

    # Extract any client/project hints from metadata
    metadata = ctx.metadata or {}
    if "client" in metadata:
        category = f"client:{metadata['client']}"
    elif "project" in metadata:
        category = f"project:{metadata['project']}"

    return CategorizedContext(
        workspace_id=ctx.workspace_id,
        category=category,
        tags=set(),
    )


def default_entry_categorizer(
    entry: ConversationalMemoryEntry,
) -> CategorizedContext:
    """
    Default categorizer for ConversationalMemoryEntry.

    Entries default to "work" category unless they have
    specific markers in their entities.
    """
    # Default category
    category = "work"

    # Check entities for category hints
    entities = entry.entities_mentioned or []
    for entity in entities:
        if entity.startswith("client:"):
            category = entity
            break
        elif entity.startswith("project:"):
            category = entity
            break

    return CategorizedContext(
        workspace_id=entry.conversation_id,
        category=category,
        tags=set(entities),
    )


# =============================================================================
# Memory Retrieval
# =============================================================================


async def get_relevant_memory(
    context: WorkspaceContext,
    user_id: str,
    memory_service: ConversationalMemoryService,
    history_service: Optional[UserHistoryService] = None,
    isolation: Optional[ContextIsolation] = None,
    workspace_categorizer: Optional[Callable[[WorkspaceContext], CategorizedContext]] = None,
    entry_categorizer: Optional[Callable[[ConversationalMemoryEntry], CategorizedContext]] = None,
    immediate_buffer: Optional[List[Dict[str, Any]]] = None,
    longterm_limit: int = 5,
) -> ContextMemory:
    """
    Retrieve memory relevant to current context.

    Pulls from three layers, applying isolation rules:
    1. Immediate: Current conversation buffer
    2. Working: Cross-session memory (7-day window from ConversationalMemoryService)
    3. Long-term: User history (relevance-searched)

    Args:
        context: Current workspace context
        user_id: User to retrieve memory for
        memory_service: Service for conversational memory
        history_service: Service for user history (optional)
        isolation: Isolation rules (uses defaults if None)
        workspace_categorizer: Function to categorize WorkspaceContext
        entry_categorizer: Function to categorize ConversationalMemoryEntry
        immediate_buffer: Current conversation turns (optional)
        longterm_limit: Max long-term entries to retrieve

    Returns:
        ContextMemory with filtered entries from all layers
    """
    # Use defaults if not provided
    isolation = isolation or ContextIsolation()
    workspace_categorizer = workspace_categorizer or default_workspace_categorizer
    entry_categorizer = entry_categorizer or default_entry_categorizer

    # Categorize target context
    target_category = workspace_categorizer(context)

    # Layer 1: Immediate (conversation buffer)
    # For now, just pass through - isolation doesn't apply within conversation
    immediate = immediate_buffer or []

    # Layer 2: Working (cross-session, 7-day window)
    memory_window = await memory_service.get_memory_window(user_id)
    working = []
    for entry in memory_window.entries:
        entry_category = entry_categorizer(entry)
        if isolation.can_cross(entry_category, target_category):
            working.append(entry)

    # Layer 3: Long-term (user history, relevance-searched)
    longterm: List[ConversationSummary] = []
    if history_service:
        # Build search query from context
        search_terms = _build_search_query(context)
        if search_terms:
            results = await history_service.search_history(
                user_id=user_id,
                query=search_terms,
                limit=longterm_limit,
            )
            # Filter by isolation (search results don't include private anyway)
            for result in results:
                # Longterm results are ConversationSummary which don't have full context
                # For now, include all search results (search already excludes private)
                longterm.append(result)

    return ContextMemory(
        immediate=immediate,
        working=working,
        longterm=longterm,
    )


def _build_search_query(context: WorkspaceContext) -> str:
    """
    Build search query from workspace context.

    Uses friendly_name and metadata to construct a search string.
    """
    parts = []

    # Add friendly name if meaningful
    if context.friendly_name and context.friendly_name not in (
        "unknown context",
        "Slack",
        "web chat",
        "terminal",
        "API",
    ):
        # Strip # prefix from channel names
        name = context.friendly_name.lstrip("#")
        parts.append(name)

    # Add metadata hints
    metadata = context.metadata or {}
    if "topic" in metadata:
        parts.append(str(metadata["topic"]))
    if "channel" in metadata:
        parts.append(str(metadata["channel"]))

    return " ".join(parts)


# =============================================================================
# Context Switch Handler
# =============================================================================


async def on_context_switch(
    switch: ContextSwitch,
    user_id: str,
    memory_service: ConversationalMemoryService,
    history_service: Optional[UserHistoryService] = None,
    isolation: Optional[ContextIsolation] = None,
) -> ContextMemory:
    """
    Handle context switch by retrieving relevant memory.

    Called when user switches between workspaces (e.g., Slack → GitHub).
    Retrieves memory appropriate for the new context.

    Args:
        switch: The detected context switch
        user_id: User who switched contexts
        memory_service: Service for conversational memory
        history_service: Service for user history
        isolation: Isolation rules

    Returns:
        ContextMemory populated for the new context
    """
    memory = await get_relevant_memory(
        context=switch.to_context,
        user_id=user_id,
        memory_service=memory_service,
        history_service=history_service,
        isolation=isolation,
    )

    # Log for observability
    logger.info(
        "context_switch_memory_retrieved",
        extra={
            "from_workspace": switch.from_context.workspace_id,
            "to_workspace": switch.to_context.workspace_id,
            "switch_type": switch.switch_type,
            "immediate_count": len(memory.immediate),
            "working_count": len(memory.working),
            "longterm_count": len(memory.longterm),
        },
    )

    return memory

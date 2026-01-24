"""
Workspace isolation and context boundary rules.

Part of #660 WORKSPACE-ISOLATION (child of #416 MUX-INTERACT-WORKSPACE epic).

This module provides:
- BoundaryType: Types of context boundaries (HARD, SOFT, OPEN)
- BoundaryRule: Configurable rule matching context categories
- CategorizedContext: Context with category tags for isolation
- ContextIsolation: Rules engine for boundary enforcement
- filter_for_isolation: Apply isolation rules to any collection

Privacy boundaries are SECURITY boundaries. Hard boundary violations
are security incidents (client A data in client B context).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional, Protocol, Set, TypeVar, runtime_checkable

# =============================================================================
# Boundary Types
# =============================================================================


class BoundaryType(Enum):
    """
    Types of context boundaries.

    HARD: Never cross - data isolation (work↔personal, client A↔client B)
    SOFT: Cross with summarization - lose detail (project A→project B)
    OPEN: Free crossing - same logical space
    """

    HARD = "hard"
    SOFT = "soft"
    OPEN = "open"


# =============================================================================
# Categorized Context
# =============================================================================


@dataclass
class CategorizedContext:
    """
    Context with category tags for isolation rules.

    Categories follow a prefix convention:
    - "work", "personal" - Life domains
    - "client:acme", "client:beta" - Client isolation
    - "org:mycompany" - Organization
    - "project:api", "project:web" - Project within org

    The isolation engine matches on these categories.
    """

    workspace_id: str
    category: str  # Primary category (e.g., "work", "client:acme")
    tags: Set[str] = field(default_factory=set)

    def matches_category(self, pattern: str) -> bool:
        """
        Check if this context matches a category pattern.

        Patterns:
        - Exact: "work" matches "work"
        - Prefix wildcard: "client:*" matches "client:acme", "client:beta"
        """
        if pattern.endswith(":*"):
            prefix = pattern[:-1]  # Remove "*", keep ":"
            return self.category.startswith(prefix)
        return self.category == pattern

    def has_tag(self, tag: str) -> bool:
        """Check if context has a specific tag."""
        return tag in self.tags


# =============================================================================
# Boundary Rules
# =============================================================================


@dataclass
class BoundaryRule:
    """
    A single boundary rule matching context categories.

    Rules are bidirectional: (A, B) means both A→B and B→A.
    """

    category_a: str
    category_b: str
    boundary_type: BoundaryType

    def matches(self, from_ctx: CategorizedContext, to_ctx: CategorizedContext) -> bool:
        """Check if this rule matches the context pair (in either direction)."""
        # A→B direction
        if from_ctx.matches_category(self.category_a) and to_ctx.matches_category(self.category_b):
            return True

        # B→A direction
        if from_ctx.matches_category(self.category_b) and to_ctx.matches_category(self.category_a):
            return True

        return False


# Default boundary rules - sensible defaults for common scenarios
DEFAULT_BOUNDARY_RULES = [
    # Hard boundaries - NEVER cross
    BoundaryRule("work", "personal", BoundaryType.HARD),
    BoundaryRule("client:*", "client:*", BoundaryType.HARD),  # Different clients
    BoundaryRule("org:*", "org:*", BoundaryType.HARD),  # Different orgs
    # Soft boundaries - cross with summarization
    BoundaryRule("project:*", "project:*", BoundaryType.SOFT),  # Different projects
    BoundaryRule("team:*", "team:*", BoundaryType.SOFT),  # Different teams
]


# =============================================================================
# Context Isolation Engine
# =============================================================================


@dataclass
class ContextIsolation:
    """
    Configurable boundary rules engine.

    Evaluates context pairs against rules to determine boundary type.
    Rules are evaluated in order; first match wins.
    """

    rules: List[BoundaryRule] = field(default_factory=lambda: DEFAULT_BOUNDARY_RULES)

    def get_boundary_type(
        self, from_ctx: CategorizedContext, to_ctx: CategorizedContext
    ) -> BoundaryType:
        """
        Determine boundary type between two contexts.

        Evaluates rules in order; first match wins.
        Returns OPEN if no rules match.
        """
        # Same category = same logical space = OPEN
        if from_ctx.category == to_ctx.category:
            return BoundaryType.OPEN

        # Special case: client:* should be HARD when crossing to different client
        # But OPEN when same client (handled above by category equality)

        for rule in self.rules:
            if rule.matches(from_ctx, to_ctx):
                # For wildcard rules, ensure we're not matching same category
                if (
                    rule.category_a.endswith(":*")
                    and rule.category_b.endswith(":*")
                    and from_ctx.category == to_ctx.category
                ):
                    continue  # Same category, skip this rule
                return rule.boundary_type

        return BoundaryType.OPEN

    def can_cross(self, from_ctx: CategorizedContext, to_ctx: CategorizedContext) -> bool:
        """Check if data can cross this boundary at all."""
        return self.get_boundary_type(from_ctx, to_ctx) != BoundaryType.HARD

    def should_summarize(self, from_ctx: CategorizedContext, to_ctx: CategorizedContext) -> bool:
        """Check if crossing requires summarization (lose detail)."""
        return self.get_boundary_type(from_ctx, to_ctx) == BoundaryType.SOFT


# =============================================================================
# Memory Filtering Protocols
# =============================================================================


@runtime_checkable
class HasContext(Protocol):
    """Protocol for items that have an associated context."""

    context: CategorizedContext


@runtime_checkable
class Summarizable(Protocol):
    """Protocol for items that can be summarized."""

    def summarized(self) -> Any: ...


T = TypeVar("T", bound=HasContext)


def filter_for_isolation(
    items: List[T],
    target: CategorizedContext,
    isolation: Optional[ContextIsolation] = None,
) -> List[Any]:
    """
    Filter items based on isolation rules.

    Args:
        items: List of items with .context attribute
        target: Target context we're filtering for
        isolation: Isolation rules (uses defaults if None)

    Returns:
        Filtered list with:
        - HARD boundary items removed entirely
        - SOFT boundary items summarized (if Summarizable)
        - OPEN boundary items included unchanged
    """
    if isolation is None:
        isolation = ContextIsolation()

    result = []
    for item in items:
        boundary = isolation.get_boundary_type(item.context, target)

        if boundary == BoundaryType.HARD:
            # Never include - skip entirely
            continue
        elif boundary == BoundaryType.SOFT:
            # Summarize if possible, include original otherwise
            if isinstance(item, Summarizable):
                result.append(item.summarized())
            else:
                # Include but mark that it should be summarized
                result.append(item)
        else:
            # OPEN - include unchanged
            result.append(item)

    return result


# =============================================================================
# Convenience Functions
# =============================================================================


def create_work_context(workspace_id: str, project: Optional[str] = None) -> CategorizedContext:
    """Create a work-categorized context."""
    tags = {f"project:{project}"} if project else set()
    return CategorizedContext(
        workspace_id=workspace_id,
        category="work",
        tags=tags,
    )


def create_personal_context(workspace_id: str) -> CategorizedContext:
    """Create a personal-categorized context."""
    return CategorizedContext(
        workspace_id=workspace_id,
        category="personal",
        tags=set(),
    )


def create_client_context(workspace_id: str, client_name: str) -> CategorizedContext:
    """Create a client-categorized context."""
    return CategorizedContext(
        workspace_id=workspace_id,
        category=f"client:{client_name}",
        tags=set(),
    )

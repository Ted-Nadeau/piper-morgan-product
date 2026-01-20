"""
MUX Protocol Definitions - Core Grammar Abstractions

This module defines the three substrate protocols for the MUX-VISION object model:
- EntityProtocol: Any actor with identity and agency
- MomentProtocol: Bounded significant occurrence with theatrical unities
- PlaceProtocol: Context where action happens

All protocols are @runtime_checkable to support role fluidity - the same object
can satisfy multiple protocols simultaneously (e.g., a Team is both Entity and Place).

References:
- ADR-045: Object Model Specification
- ADR-038: Spatial Intelligence Patterns
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Protocol, runtime_checkable

if TYPE_CHECKING:
    from .perception import Perception


@runtime_checkable
class EntityProtocol(Protocol):
    """
    Any actor with identity and agency.

    Entities are things that can:
    - Have experiences (perceive Moments)
    - Take action
    - Be affected by events

    Examples: User, Team, Project, Task (when task acts as agent)

    The key insight: Entities EXPERIENCE moments rather than just
    "having data". This framing preserves consciousness.
    """

    id: str

    def experiences(self, moment: "MomentProtocol") -> "Perception":
        """
        Entity experiences a Moment, returning a Perception.

        This is the core "consciousness-preserving" method. Instead of
        returning raw data, it returns how the entity perceives/experiences
        the moment.

        Args:
            moment: The Moment being experienced

        Returns:
            Perception: The entity's perception of the moment
        """
        ...


@runtime_checkable
class MomentProtocol(Protocol):
    """
    Bounded significant occurrence with theatrical unities.

    Moments capture:
    - Time (when) - timestamp
    - Unity of action (what happened)
    - Unity of place (where, implied)
    - Dramatic significance (why it matters)

    Moments have policy, process, people, and outcomes.
    They are experienced by Entities and occur in Places.

    Examples: Meeting, Decision, Commit, Deploy, Standup
    """

    id: str
    timestamp: datetime

    def captures(self) -> Dict[str, Any]:
        """
        Return what this Moment captures.

        Returns a dictionary with keys like:
        - policy: What rules/decisions are in effect
        - process: What procedures are being followed
        - people: Who is involved
        - outcomes: What results emerged

        Returns:
            Dict containing policy, process, people, outcomes
        """
        ...


@runtime_checkable
class PlaceProtocol(Protocol):
    """
    Context where action happens.

    Places have atmosphere - they're not just containers but
    have emotional/social qualities that affect what happens.

    Places contain Entities and Moments. The same object can be
    both an Entity and a Place (role fluidity).

    Examples: Channel (Slack), Repository (GitHub), Project (Notion),
              Team (is also an Entity), Workspace
    """

    id: str
    atmosphere: str  # warm, formal, urgent, creative, etc.

    def contains(self) -> List[Any]:
        """
        Return entities/moments contained in this Place.

        This creates the spatial hierarchy:
        - Workspace contains Teams
        - Team contains Projects
        - Project contains Tasks
        - Channel contains Conversations

        Returns:
            List of contained entities and/or moments
        """
        ...


# Type alias for anything that can be perceived through a lens
Target = EntityProtocol | MomentProtocol | PlaceProtocol

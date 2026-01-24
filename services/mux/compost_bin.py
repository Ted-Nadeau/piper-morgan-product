"""
Compost bin - staging area for objects awaiting decomposition.

Part of #666 COMPOSTING-BIN (child of #436 MUX-TECH-PHASE4-COMPOSTING).

This module provides:
- CompostBinEntry: An object waiting to be composted
- CompostBin: Staging area with add/remove/get_ready operations
- Integration hooks for lifecycle transitions

Objects flow through:
  Lifecycle transition → CompostBin → Pipeline (#667) → InsightJournal
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, List, Optional

from .composting_models import CompostingTrigger

# =============================================================================
# CompostBinEntry
# =============================================================================


@dataclass
class CompostBinEntry:
    """
    An object waiting to be composted.

    Captures both the object reference and the reason it's ready
    for decomposition, enabling appropriate processing later.

    Priority ordering:
    - Higher priority = composted sooner
    - Within same priority, FIFO ordering applies
    - Corrections (CONTRADICTION) get priority boost automatically
    """

    object_id: str
    object_type: str
    trigger: CompostingTrigger
    added_at: datetime = field(default_factory=datetime.now)
    priority: int = 0  # Higher = compost sooner

    # Optional: reference to actual object (may be None if just ID)
    object_ref: Optional[Any] = None

    def __post_init__(self):
        """Boost priority for contradiction triggers."""
        # Contradictions are urgent - they represent outdated understanding
        if self.trigger == CompostingTrigger.CONTRADICTION:
            self.priority = max(self.priority, 10)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "object_id": self.object_id,
            "object_type": self.object_type,
            "trigger": self.trigger.value,
            "added_at": self.added_at.isoformat(),
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CompostBinEntry":
        """Create from dictionary."""
        added_at = data.get("added_at")
        if isinstance(added_at, str):
            added_at = datetime.fromisoformat(added_at)
        elif added_at is None:
            added_at = datetime.now()

        trigger_value = data.get("trigger", "manual")
        trigger = CompostingTrigger(trigger_value)

        return cls(
            object_id=data.get("object_id", ""),
            object_type=data.get("object_type", "unknown"),
            trigger=trigger,
            added_at=added_at,
            priority=data.get("priority", 0),
        )


# =============================================================================
# CompostBin
# =============================================================================


@dataclass
class CompostBin:
    """
    Staging area for objects ready to decompose.

    The CompostBin manages the queue of objects awaiting composting:
    - Collects objects from various triggers (age, irrelevance, manual, etc.)
    - Orders by priority then FIFO
    - Respects processing thresholds
    - Supports "quiet hours" for scheduled composting (2-5 AM)

    Example:
        bin = CompostBin()
        bin.add(old_task, CompostingTrigger.AGE, object_type="task")

        if bin.should_process_now():
            entries = bin.get_ready(limit=10)
            for entry in entries:
                process(entry)
                bin.remove(entry.object_id)
    """

    # Objects awaiting composting
    pending: List[CompostBinEntry] = field(default_factory=list)

    # Processing state
    is_composting: bool = False
    last_composted: Optional[datetime] = None

    # Thresholds
    min_age_days: int = 30  # Minimum age for AGE trigger
    max_pending: int = 100  # Auto-process if this many waiting
    batch_size: int = 10  # Default batch for get_ready()

    # Quiet hours (for SCHEDULED trigger)
    quiet_start_hour: int = 2  # 2 AM
    quiet_end_hour: int = 5  # 5 AM

    def add(
        self,
        obj: Any,
        trigger: CompostingTrigger,
        object_type: Optional[str] = None,
        priority: int = 0,
    ) -> CompostBinEntry:
        """
        Add an object to the compost bin.

        Args:
            obj: The object to compost (or object ID string)
            trigger: Why this object is ready for composting
            object_type: Type name (inferred from obj if not provided)
            priority: Processing priority (higher = sooner)

        Returns:
            The created CompostBinEntry
        """
        # Extract object_id
        if isinstance(obj, str):
            object_id = obj
            object_ref = None
        else:
            object_id = getattr(obj, "id", None) or str(id(obj))
            object_ref = obj

        # Infer object_type
        if object_type is None:
            if object_ref is not None:
                object_type = type(object_ref).__name__
            else:
                object_type = "unknown"

        # Check for duplicates
        existing = self.get_entry(object_id)
        if existing is not None:
            # Update priority if new one is higher
            if priority > existing.priority:
                existing.priority = priority
            return existing

        entry = CompostBinEntry(
            object_id=object_id,
            object_type=object_type,
            trigger=trigger,
            priority=priority,
            object_ref=object_ref,
        )

        self.pending.append(entry)
        return entry

    def remove(self, object_id: str) -> Optional[CompostBinEntry]:
        """
        Remove an object from the bin after processing.

        Args:
            object_id: ID of the object to remove

        Returns:
            The removed entry, or None if not found
        """
        for i, entry in enumerate(self.pending):
            if entry.object_id == object_id:
                return self.pending.pop(i)
        return None

    def get_entry(self, object_id: str) -> Optional[CompostBinEntry]:
        """
        Get an entry by object ID without removing it.

        Args:
            object_id: ID to look up

        Returns:
            The entry if found, None otherwise
        """
        for entry in self.pending:
            if entry.object_id == object_id:
                return entry
        return None

    def get_ready(self, limit: Optional[int] = None) -> List[CompostBinEntry]:
        """
        Get entries ready for composting, ordered by priority.

        Returns entries in priority order (highest first),
        with FIFO ordering within the same priority level.

        Args:
            limit: Maximum entries to return (default: batch_size)

        Returns:
            List of CompostBinEntry objects ready for processing
        """
        limit = limit if limit is not None else self.batch_size

        # Sort by priority (desc), then added_at (asc)
        sorted_entries = sorted(
            self.pending,
            key=lambda e: (-e.priority, e.added_at),
        )

        return sorted_entries[:limit]

    def should_process_now(self, current_time: Optional[datetime] = None) -> bool:
        """
        Determine if we should process the compost bin now.

        Returns True if:
        1. There are pending entries AND
        2. Either:
           a. We have too many entries (>= max_pending), OR
           b. We're in quiet hours (2-5 AM), OR
           c. There are high-priority items (priority >= 10)

        Args:
            current_time: Time to check (default: now)

        Returns:
            True if processing should occur
        """
        if not self.pending:
            return False

        if self.is_composting:
            return False  # Already processing

        current_time = current_time or datetime.now()

        # Too many pending
        if len(self.pending) >= self.max_pending:
            return True

        # Quiet hours
        if self._is_quiet_hours(current_time):
            return True

        # High priority items exist
        if any(e.priority >= 10 for e in self.pending):
            return True

        return False

    def _is_quiet_hours(self, current_time: datetime) -> bool:
        """Check if we're in quiet hours (filing dreams time)."""
        hour = current_time.hour
        return self.quiet_start_hour <= hour < self.quiet_end_hour

    @property
    def count(self) -> int:
        """Number of entries in the bin."""
        return len(self.pending)

    @property
    def has_urgent(self) -> bool:
        """Check if there are urgent (high priority) entries."""
        return any(e.priority >= 10 for e in self.pending)

    def clear(self) -> int:
        """
        Clear all entries from the bin.

        Returns:
            Number of entries cleared
        """
        count = len(self.pending)
        self.pending = []
        return count

    def get_stats(self) -> dict:
        """
        Get statistics about the bin's contents.

        Returns:
            Dictionary with counts by trigger type and other stats
        """
        by_trigger = {}
        by_type = {}
        total_priority = 0

        for entry in self.pending:
            trigger_name = entry.trigger.value
            by_trigger[trigger_name] = by_trigger.get(trigger_name, 0) + 1

            by_type[entry.object_type] = by_type.get(entry.object_type, 0) + 1
            total_priority += entry.priority

        return {
            "total": len(self.pending),
            "by_trigger": by_trigger,
            "by_type": by_type,
            "avg_priority": total_priority / len(self.pending) if self.pending else 0,
            "is_composting": self.is_composting,
            "last_composted": (self.last_composted.isoformat() if self.last_composted else None),
        }


# =============================================================================
# Lifecycle Integration Hooks
# =============================================================================


def meets_composting_criteria(
    obj: Any,
    min_age_days: int = 30,
    check_relevance: Optional[Callable[[Any], bool]] = None,
) -> bool:
    """
    Check if an object meets criteria for composting.

    This is a hook for lifecycle transitions to determine
    if an object should enter the compost bin.

    Args:
        obj: Object to check
        min_age_days: Minimum age for AGE trigger
        check_relevance: Optional callback to check if still referenced

    Returns:
        True if object should be composted
    """
    # Check age if created_at available
    if hasattr(obj, "created_at"):
        created_at = obj.created_at
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        age = datetime.now() - created_at
        if age.days >= min_age_days:
            return True

    # Check relevance if callback provided
    if check_relevance is not None:
        if not check_relevance(obj):
            return True  # Not relevant = should compost

    return False


def determine_trigger(obj: Any) -> CompostingTrigger:
    """
    Determine the appropriate composting trigger for an object.

    Examines object state to infer why it should be composted.

    Args:
        obj: Object to analyze

    Returns:
        Appropriate CompostingTrigger
    """
    # Check for contradiction marker
    if hasattr(obj, "is_contradicted") and obj.is_contradicted:
        return CompostingTrigger.CONTRADICTION

    # Check for age
    if hasattr(obj, "created_at"):
        created_at = obj.created_at
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        age = datetime.now() - created_at
        if age.days >= 30:
            return CompostingTrigger.AGE

    # Check lifecycle state
    if hasattr(obj, "lifecycle_state"):
        from .lifecycle import LifecycleState

        if obj.lifecycle_state in (
            LifecycleState.DEPRECATED,
            LifecycleState.ARCHIVED,
        ):
            return CompostingTrigger.IRRELEVANCE

    # Default to manual
    return CompostingTrigger.MANUAL


async def on_lifecycle_deprecated(
    obj: Any,
    compost_bin: CompostBin,
    force: bool = False,
) -> Optional[CompostBinEntry]:
    """
    Hook for when an object enters DEPRECATED state.

    Called by lifecycle transitions to potentially add
    objects to the compost bin.

    Args:
        obj: The deprecated object
        compost_bin: Bin to add to
        force: If True, add regardless of criteria

    Returns:
        The CompostBinEntry if added, None otherwise
    """
    if force or meets_composting_criteria(obj):
        trigger = determine_trigger(obj)
        return compost_bin.add(obj, trigger)
    return None


async def on_lifecycle_archived(
    obj: Any,
    compost_bin: CompostBin,
) -> CompostBinEntry:
    """
    Hook for when an object enters ARCHIVED state.

    ARCHIVED objects always enter composting - they've
    completed their lifecycle.

    Args:
        obj: The archived object
        compost_bin: Bin to add to

    Returns:
        The created CompostBinEntry
    """
    trigger = determine_trigger(obj)
    return compost_bin.add(obj, trigger)

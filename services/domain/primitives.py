"""
Domain Primitives: Item and List

These are the cognitive primitives for list-making.
All specific list types (todos, shopping, reading) extend these.

Design Decision: Items know their text and position.
Lists know their type and what items they contain.

Note: List primitive already exists in services.domain.models (line 866).
      We import it here for convenient access alongside Item.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Item:
    """Universal list item - the atomic unit of list-making.

    Every item in every list has these properties.
    Specific item types (Todo, ShoppingItem) extend this.

    Examples:
        >>> item = Item(text="Buy milk")
        >>> assert item.text == "Buy milk"
        >>> assert item.position == 0

        >>> # Future (Phase 2):
        >>> # todo = Todo(text="Review PR", priority="high")
        >>> # assert isinstance(todo, Item)  # Todo IS-A Item
        >>> # assert todo.text == "Review PR"

    Attributes:
        id: Unique identifier (auto-generated UUID string)
        text: The universal property - all items have text
        position: Order within the list (0-indexed)
        list_id: Which list contains this item (optional, UUID string)
        created_at: When the item was created
        updated_at: When the item was last modified
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    text: str = ""  # The universal property - all items have text
    position: int = 0  # Order within the list
    list_id: Optional[str] = None  # Which list contains this item
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def move_to_position(self, new_position: int):
        """Items can be reordered.

        Args:
            new_position: New position in the list (0-indexed)
        """
        self.position = new_position
        self.updated_at = datetime.utcnow()

    def update_text(self, new_text: str):
        """Update item text.

        Args:
            new_text: New text content for the item
        """
        self.text = new_text
        self.updated_at = datetime.utcnow()


# Note: List primitive already exists at services.domain.models:866
# It's universal with item_type discriminator and has comprehensive fields.
# We don't import it here to avoid circular dependencies.
# Import List directly from services.domain.models when needed.

__all__ = ["Item"]

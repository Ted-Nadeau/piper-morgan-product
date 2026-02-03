"""
Tests for domain primitives: Item and List.

These tests verify the base classes work correctly before
Todo extends them in Phase 2.

Note: List primitive already exists at services.domain.models:866.
      These tests focus on the new Item primitive.
"""

import time
from datetime import datetime, timezone

import pytest

from services.domain.models import List
from services.domain.primitives import Item


class TestItem:
    """Tests for Item primitive."""

    def test_item_creation_minimal(self):
        """Items can be created with just text."""
        item = Item(text="Buy milk")

        assert item.text == "Buy milk"
        assert item.position == 0
        assert item.list_id is None
        assert isinstance(item.id, str)
        assert len(item.id) == 36  # UUID string format
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)

    def test_item_creation_with_position(self):
        """Items can specify their position."""
        item = Item(text="Second item", position=1)

        assert item.text == "Second item"
        assert item.position == 1

    def test_item_creation_with_list_id(self):
        """Items can be associated with a list."""
        from uuid import uuid4

        list_id = str(uuid4())

        item = Item(text="Task", list_id=list_id)

        assert item.list_id == list_id

    def test_item_creation_empty_text(self):
        """Items can be created with empty text (default)."""
        item = Item()

        assert item.text == ""
        assert item.position == 0

    def test_item_move_to_position(self):
        """Items can be moved to a new position."""
        item = Item(text="Task", position=0)
        original_updated = item.updated_at

        # Small delay to ensure timestamp changes
        time.sleep(0.01)

        item.move_to_position(3)

        assert item.position == 3
        assert item.updated_at > original_updated

    def test_item_update_text(self):
        """Items can update their text."""
        item = Item(text="Original")
        original_updated = item.updated_at

        # Small delay to ensure timestamp changes
        time.sleep(0.01)

        item.update_text("Modified")

        assert item.text == "Modified"
        assert item.updated_at > original_updated

    def test_item_ids_are_unique(self):
        """Each item gets a unique UUID string."""
        item1 = Item(text="First")
        item2 = Item(text="Second")

        assert item1.id != item2.id
        assert isinstance(item1.id, str)
        assert isinstance(item2.id, str)
        assert len(item1.id) == 36
        assert len(item2.id) == 36

    def test_item_timestamps_auto_set(self):
        """Timestamps are automatically set on creation."""
        before = datetime.now(timezone.utc)
        item = Item(text="Task")
        after = datetime.now(timezone.utc)

        assert before <= item.created_at <= after
        assert before <= item.updated_at <= after

    def test_item_position_can_be_zero(self):
        """Position 0 is valid (first item in list)."""
        item = Item(text="First", position=0)

        assert item.position == 0

    def test_item_position_can_be_large(self):
        """Position can be any non-negative integer."""
        item = Item(text="Task", position=1000)

        assert item.position == 1000

    def test_item_text_can_be_long(self):
        """Items can have long text."""
        long_text = "A" * 1000
        item = Item(text=long_text)

        assert item.text == long_text
        assert len(item.text) == 1000

    def test_item_text_can_have_unicode(self):
        """Items support Unicode text."""
        item = Item(text="Buy 🥛 and 🍞")

        assert item.text == "Buy 🥛 and 🍞"

    def test_item_text_can_have_newlines(self):
        """Items can have multi-line text."""
        item = Item(text="Line 1\nLine 2\nLine 3")

        assert "\n" in item.text
        assert item.text.count("\n") == 2


class TestListPrimitive:
    """Tests for List primitive (already exists in models.py)."""

    def test_list_exists(self):
        """List class exists and is importable."""
        assert List is not None

    def test_list_has_item_type_discriminator(self):
        """List has item_type discriminator for polymorphism."""
        todo_list = List(name="Work Tasks", item_type="todo")

        assert hasattr(todo_list, "item_type")
        assert todo_list.item_type == "todo"

    def test_list_supports_different_types(self):
        """List can be created with different item types."""
        todo_list = List(name="Tasks", item_type="todo")
        shopping_list = List(name="Groceries", item_type="shopping")
        reading_list = List(name="Books", item_type="reading")

        assert todo_list.item_type == "todo"
        assert shopping_list.item_type == "shopping"
        assert reading_list.item_type == "reading"

    def test_list_has_name(self):
        """Lists have a name property."""
        lst = List(name="My List", item_type="todo")

        assert lst.name == "My List"

    def test_list_has_id(self):
        """Lists get unique IDs."""
        list1 = List(name="List 1", item_type="todo")
        list2 = List(name="List 2", item_type="todo")

        assert list1.id != list2.id


class TestItemListIntegration:
    """Tests for Item and List working together."""

    def test_item_can_reference_list(self):
        """Items can reference the list they belong to."""
        from uuid import uuid4

        # Create a list (we'll use the ID)
        todo_list = List(name="Work Tasks", item_type="todo")

        # Create item with list_id
        item = Item(text="Review PR", list_id=str(uuid4()))

        assert item.list_id is not None
        assert isinstance(item.list_id, str)
        assert len(item.list_id) == 36

    def test_multiple_items_same_list(self):
        """Multiple items can belong to the same list."""
        from uuid import uuid4

        list_id = str(uuid4())

        item1 = Item(text="Task 1", list_id=list_id, position=0)
        item2 = Item(text="Task 2", list_id=list_id, position=1)
        item3 = Item(text="Task 3", list_id=list_id, position=2)

        assert item1.list_id == item2.list_id == item3.list_id == list_id
        assert item1.position == 0
        assert item2.position == 1
        assert item3.position == 2

    def test_items_can_be_reordered(self):
        """Items in a list can be reordered."""
        from uuid import uuid4

        list_id = str(uuid4())

        item1 = Item(text="First", list_id=list_id, position=0)
        item2 = Item(text="Second", list_id=list_id, position=1)

        # Swap positions
        item1.move_to_position(1)
        item2.move_to_position(0)

        assert item1.position == 1
        assert item2.position == 0


class TestItemInheritanceReadiness:
    """Tests to verify Item is ready for inheritance (Phase 2)."""

    def test_item_is_dataclass(self):
        """Item is a dataclass (supports inheritance)."""
        from dataclasses import is_dataclass

        assert is_dataclass(Item)

    def test_item_has_required_base_fields(self):
        """Item has all fields needed for inheritance."""
        item = Item(text="Test")

        # Required base fields for all items
        assert hasattr(item, "id")
        assert hasattr(item, "text")
        assert hasattr(item, "position")
        assert hasattr(item, "created_at")
        assert hasattr(item, "updated_at")

    def test_item_can_be_instantiated_directly(self):
        """Item can be used standalone (not just as base class)."""
        item = Item(text="Generic task")

        assert isinstance(item, Item)
        assert item.text == "Generic task"

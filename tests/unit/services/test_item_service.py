"""Tests for universal ItemService."""

from uuid import UUID, uuid4

import pytest

from services.domain.primitives import Item
from services.item_service import ItemService


class TestItemService:
    """Tests for ItemService base class."""

    @pytest.fixture
    def service(self):
        """Create service instance."""
        return ItemService()

    @pytest.fixture
    def list_id(self) -> UUID:
        """Create a test list ID."""
        return uuid4()

    @pytest.mark.smoke
    async def test_create_item(self, service, list_id):
        """Can create generic item."""
        item = await service.create_item(text="Test item", list_id=list_id)

        assert isinstance(item, Item)
        assert item.text == "Test item"
        assert item.list_id == str(list_id)
        assert item.position == 0

    @pytest.mark.smoke
    async def test_get_item(self, service, list_id):
        """Can retrieve item by ID."""
        # Create item
        created = await service.create_item(text="Retrieve me", list_id=list_id)

        # Retrieve it
        retrieved = await service.get_item(UUID(created.id))

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.text == "Retrieve me"

    @pytest.mark.smoke
    async def test_update_item_text(self, service, list_id):
        """Can update item text."""
        item = await service.create_item(text="Original", list_id=list_id)

        updated = await service.update_item_text(UUID(item.id), "Updated")

        assert updated.text == "Updated"

    @pytest.mark.smoke
    async def test_reorder_items(self, service, list_id):
        """Can reorder items in list."""
        # Create 3 items
        item1 = await service.create_item(text="First", list_id=list_id)
        item2 = await service.create_item(text="Second", list_id=list_id)
        item3 = await service.create_item(text="Third", list_id=list_id)

        # Reorder: 3, 1, 2
        reordered = await service.reorder_items(
            list_id, [UUID(item3.id), UUID(item1.id), UUID(item2.id)]
        )

        assert reordered[0].text == "Third"
        assert reordered[1].text == "First"
        assert reordered[2].text == "Second"

    @pytest.mark.smoke
    async def test_delete_item(self, service, list_id):
        """Can delete item."""
        item = await service.create_item(text="Delete me", list_id=list_id)

        deleted = await service.delete_item(UUID(item.id))
        assert deleted is True

        # Verify deleted
        retrieved = await service.get_item(UUID(item.id))
        assert retrieved is None

    @pytest.mark.smoke
    async def test_get_items_in_list(self, service, list_id):
        """Can get all items in a list."""
        # Create multiple items
        await service.create_item(text="Item 1", list_id=list_id)
        await service.create_item(text="Item 2", list_id=list_id)
        await service.create_item(text="Item 3", list_id=list_id)

        # Retrieve all
        items = await service.get_items_in_list(list_id)

        assert len(items) == 3
        assert items[0].text == "Item 1"
        assert items[1].text == "Item 2"
        assert items[2].text == "Item 3"

    @pytest.mark.smoke
    async def test_position_auto_assignment(self, service, list_id):
        """Items are auto-assigned sequential positions."""
        item1 = await service.create_item(text="First", list_id=list_id)
        item2 = await service.create_item(text="Second", list_id=list_id)
        item3 = await service.create_item(text="Third", list_id=list_id)

        assert item1.position == 0
        assert item2.position == 1
        assert item3.position == 2

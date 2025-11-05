"""
Integration tests for Item and List primitives.

These tests verify the full stack works:
domain → database → back to domain.

NOTE: We use in-memory SQLite for testing (not PostgreSQL)
because we're testing the ORM layer, not PostgreSQL-specific features.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.database.connection import Base
from services.database.models import ItemDB, ListDB
from services.domain.models import List
from services.domain.primitives import Item


@pytest.fixture
def in_memory_db():
    """Create in-memory database for testing.

    NOTE: We only create ItemDB table because ListDB uses PostgreSQL JSONB types
    that SQLite doesn't support. List functionality is tested separately with
    domain models only (not database persistence in this test file).
    """
    engine = create_engine("sqlite:///:memory:")

    # Create only ItemDB table (ListDB has JSONB fields incompatible with SQLite)
    ItemDB.__table__.create(engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


class TestItemPersistence:
    """Test Item domain ↔ database conversion."""

    def test_item_domain_to_db_to_domain(self, in_memory_db):
        """Item can be saved and retrieved."""
        # Create domain object
        item = Item(text="Test item", position=0)

        # Convert to database model
        item_db = ItemDB.from_domain(item)

        # Save to database
        in_memory_db.add(item_db)
        in_memory_db.commit()

        # Retrieve from database
        retrieved_db = in_memory_db.query(ItemDB).filter_by(id=item.id).first()
        assert retrieved_db is not None

        # Convert back to domain
        retrieved_item = retrieved_db.to_domain()

        # Verify all properties preserved
        assert retrieved_item.id == item.id
        assert retrieved_item.text == item.text
        assert retrieved_item.position == item.position

    def test_item_with_all_fields(self, in_memory_db):
        """Item preserves all fields through save/retrieve cycle."""
        from uuid import uuid4

        list_id = str(uuid4())
        item = Item(
            text="Complete task",
            position=5,
            list_id=list_id,
        )

        # Save and retrieve
        item_db = ItemDB.from_domain(item)
        in_memory_db.add(item_db)
        in_memory_db.commit()

        retrieved_db = in_memory_db.query(ItemDB).filter_by(id=item.id).first()
        retrieved_item = retrieved_db.to_domain()

        # Verify all fields
        assert retrieved_item.text == "Complete task"
        assert retrieved_item.position == 5
        assert retrieved_item.list_id == list_id

    def test_multiple_items_persist(self, in_memory_db):
        """Multiple items can be saved independently."""
        item1 = Item(text="First item", position=0)
        item2 = Item(text="Second item", position=1)
        item3 = Item(text="Third item", position=2)

        # Save all
        in_memory_db.add(ItemDB.from_domain(item1))
        in_memory_db.add(ItemDB.from_domain(item2))
        in_memory_db.add(ItemDB.from_domain(item3))
        in_memory_db.commit()

        # Retrieve all
        all_items = in_memory_db.query(ItemDB).order_by(ItemDB.position).all()

        assert len(all_items) == 3
        assert all_items[0].text == "First item"
        assert all_items[1].text == "Second item"
        assert all_items[2].text == "Third item"

    def test_item_update_persists(self, in_memory_db):
        """Item updates are saved to database."""
        item = Item(text="Original text", position=0)

        # Save initial
        item_db = ItemDB.from_domain(item)
        in_memory_db.add(item_db)
        in_memory_db.commit()

        # Update in database
        item_db.text = "Updated text"
        item_db.position = 10
        in_memory_db.commit()

        # Retrieve and verify
        retrieved_db = in_memory_db.query(ItemDB).filter_by(id=item.id).first()
        assert retrieved_db.text == "Updated text"
        assert retrieved_db.position == 10


class TestListDomain:
    """Test List domain model (without database persistence).

    NOTE: ListDB uses PostgreSQL JSONB types that SQLite doesn't support,
    so we test List domain functionality only (not database persistence).
    """

    def test_list_domain_model_works(self):
        """List domain model can be created and used."""
        todo_list = List(name="Work Tasks", item_type="todo")

        assert todo_list.name == "Work Tasks"
        assert todo_list.item_type == "todo"
        assert todo_list.id is not None

    def test_list_domain_conversion(self):
        """List domain model can convert to dict."""
        todo_list = List(name="Personal Tasks", item_type="todo")

        dict_repr = todo_list.to_dict()

        assert dict_repr["name"] == "Personal Tasks"
        assert dict_repr["item_type"] == "todo"
        assert "id" in dict_repr


class TestItemListRelationship:
    """Test Item-List relationship (items reference list IDs)."""

    def test_items_can_reference_lists(self, in_memory_db):
        """Items can store list_id references."""
        from uuid import uuid4

        list_id = str(uuid4())

        # Create items in list
        item1 = Item(text="Task 1", list_id=list_id, position=0)
        item2 = Item(text="Task 2", list_id=list_id, position=1)

        in_memory_db.add(ItemDB.from_domain(item1))
        in_memory_db.add(ItemDB.from_domain(item2))
        in_memory_db.commit()

        # Retrieve items for list
        items_in_list = (
            in_memory_db.query(ItemDB).filter_by(list_id=list_id).order_by(ItemDB.position).all()
        )

        assert len(items_in_list) == 2
        assert items_in_list[0].text == "Task 1"
        assert items_in_list[1].text == "Task 2"

    def test_items_belong_to_different_lists(self, in_memory_db):
        """Items can belong to different lists and be queried separately."""
        from uuid import uuid4

        # Create items for two different list IDs
        list1_id = str(uuid4())
        list2_id = str(uuid4())

        personal_item = Item(text="Buy milk", list_id=list1_id, position=0)
        work_item = Item(text="Review PR", list_id=list2_id, position=0)

        in_memory_db.add(ItemDB.from_domain(personal_item))
        in_memory_db.add(ItemDB.from_domain(work_item))
        in_memory_db.commit()

        # Query items by list
        list1_items = in_memory_db.query(ItemDB).filter_by(list_id=list1_id).all()
        list2_items = in_memory_db.query(ItemDB).filter_by(list_id=list2_id).all()

        assert len(list1_items) == 1
        assert list1_items[0].text == "Buy milk"

        assert len(list2_items) == 1
        assert list2_items[0].text == "Review PR"

    def test_items_ordered_within_list(self, in_memory_db):
        """Items maintain position order within a list."""
        from uuid import uuid4

        list_id = str(uuid4())

        # Create items in specific order
        items = [
            Item(text="Third", list_id=list_id, position=2),
            Item(text="First", list_id=list_id, position=0),
            Item(text="Second", list_id=list_id, position=1),
        ]

        for item in items:
            in_memory_db.add(ItemDB.from_domain(item))
        in_memory_db.commit()

        # Retrieve ordered by position
        ordered_items = (
            in_memory_db.query(ItemDB).filter_by(list_id=list_id).order_by(ItemDB.position).all()
        )

        assert len(ordered_items) == 3
        assert ordered_items[0].text == "First"
        assert ordered_items[1].text == "Second"
        assert ordered_items[2].text == "Third"

    def test_item_type_discriminator(self, in_memory_db):
        """Items have type discriminator for polymorphism."""
        item = Item(text="Generic item")
        item_db = ItemDB.from_domain(item)

        in_memory_db.add(item_db)
        in_memory_db.commit()

        retrieved = in_memory_db.query(ItemDB).filter_by(id=item.id).first()

        # Base items have item_type="item"
        assert retrieved.item_type == "item"

    def test_orphan_items_allowed(self, in_memory_db):
        """Items can exist without belonging to a list."""
        orphan_item = Item(text="Standalone item", list_id=None)
        item_db = ItemDB.from_domain(orphan_item)

        in_memory_db.add(item_db)
        in_memory_db.commit()

        retrieved = in_memory_db.query(ItemDB).filter_by(id=orphan_item.id).first()

        assert retrieved is not None
        assert retrieved.list_id is None
        assert retrieved.text == "Standalone item"


class TestDataIntegrity:
    """Test data integrity constraints."""

    def test_item_requires_text(self, in_memory_db):
        """Items must have text (can be empty string but not None)."""
        item = Item(text="", position=0)  # Empty string is OK
        item_db = ItemDB.from_domain(item)

        in_memory_db.add(item_db)
        in_memory_db.commit()

        retrieved = in_memory_db.query(ItemDB).filter_by(id=item.id).first()
        assert retrieved.text == ""

    def test_item_timestamps_persist(self, in_memory_db):
        """Item timestamps are saved and retrieved."""
        item = Item(text="Timestamped item")
        item_db = ItemDB.from_domain(item)

        in_memory_db.add(item_db)
        in_memory_db.commit()

        retrieved = in_memory_db.query(ItemDB).filter_by(id=item.id).first()

        assert retrieved.created_at is not None
        assert retrieved.updated_at is not None

# Gameplan: #657 MEM-ADR054-P1 Core Memory Infrastructure

**Issue**: #657
**ADR**: ADR-054 Cross-Session Memory Architecture
**Phase**: Phase 1 - Core Memory Infrastructure
**Blocks**: #416 (MUX-INTERACT-WORKSPACE)

---

## Overview

Implement the foundational Layer 1 (Conversational Memory - 24hr window) from ADR-054. This creates the infrastructure that #416 needs to navigate between contexts.

---

## Phase 1: Domain Models

**Goal**: Create domain models for conversational memory

**File**: `services/memory/conversational_memory.py`

```python
"""
Conversational Memory Service.

Layer 1 of ADR-054 Cross-Session Memory Architecture.
Provides 24-hour memory window for natural continuity references.

Part of #657 MEM-ADR054-P1.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from uuid import UUID
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class ConversationalMemoryEntry:
    """A memorable item from recent conversation."""

    conversation_id: str  # Use str for consistency with ConversationDB.id
    timestamp: datetime
    topic_summary: str  # Brief summary of what was discussed
    entities_mentioned: List[str] = field(default_factory=list)  # Projects, issues, people
    outcome: Optional[str] = None  # What was decided/accomplished
    user_sentiment: Optional[str] = None  # positive/neutral/negative


@dataclass
class ConversationalMemoryWindow:
    """24-hour memory window for a user."""

    user_id: str
    entries: List[ConversationalMemoryEntry] = field(default_factory=list)
    window_start: datetime = field(default_factory=lambda: datetime.now(timezone.utc) - timedelta(hours=24))
    window_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def get_most_recent(self) -> Optional[ConversationalMemoryEntry]:
        """Get most recent conversation in window."""
        return self.entries[0] if self.entries else None

    def get_active_topics(self) -> List[str]:
        """Get topics discussed in window (deduplicated)."""
        return list(set(e.topic_summary for e in self.entries if e.topic_summary))

    def get_active_entities(self) -> List[str]:
        """Get all entities mentioned in window (deduplicated)."""
        entities = []
        for entry in self.entries:
            entities.extend(entry.entities_mentioned)
        return list(set(entities))

    def is_empty(self) -> bool:
        """Check if memory window has no entries."""
        return len(self.entries) == 0
```

**Acceptance Criteria**:
- [ ] `ConversationalMemoryEntry` dataclass with all fields from ADR-054
- [ ] `ConversationalMemoryWindow` dataclass with helper methods
- [ ] Uses `datetime.now(timezone.utc)` (not deprecated `utcnow()`)
- [ ] Uses `str` for IDs (consistency with existing ConversationDB)

---

## Phase 2: Database Model and Migration

**Goal**: Create database table for memory entries

### 2A: Database Model

**File**: `services/database/models.py` (ADD)

```python
class ConversationalMemoryEntryDB(Base):
    """Database model for conversational memory entries (ADR-054 Layer 1)."""

    __tablename__ = "conversational_memory_entries"

    id = Column(String, primary_key=True)  # UUID as string
    user_id = Column(String, nullable=False, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)

    timestamp = Column(DateTime(timezone=True), nullable=False)
    topic_summary = Column(String(500), nullable=False)
    entities_mentioned = Column(postgresql.JSONB, default=list)
    outcome = Column(String(500), nullable=True)
    user_sentiment = Column(String(20), nullable=True)  # positive/neutral/negative

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_cme_user_timestamp", "user_id", "timestamp"),
    )
```

### 2B: Migration

**File**: `alembic/versions/XXXX_add_conversational_memory_entries.py`

```python
"""add conversational memory entries table

Revision ID: XXXX
Revises: [previous]
Create Date: 2026-01-23
"""

def upgrade():
    op.create_table(
        'conversational_memory_entries',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('topic_summary', sa.String(500), nullable=False),
        sa.Column('entities_mentioned', postgresql.JSONB(), server_default='[]'),
        sa.Column('outcome', sa.String(500), nullable=True),
        sa.Column('user_sentiment', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id']),
    )
    op.create_index('idx_cme_user_timestamp', 'conversational_memory_entries', ['user_id', 'timestamp'])

def downgrade():
    op.drop_index('idx_cme_user_timestamp')
    op.drop_table('conversational_memory_entries')
```

**Acceptance Criteria**:
- [ ] `ConversationalMemoryEntryDB` model in database/models.py
- [ ] Alembic migration creates table
- [ ] Index on (user_id, timestamp) for efficient window queries
- [ ] ForeignKey to conversations table
- [ ] Migration runs without error

---

## Phase 3: Repository

**Goal**: Data access layer for memory entries

**File**: `services/repositories/conversational_memory_repository.py`

```python
"""
Repository for conversational memory entries.

Part of #657 MEM-ADR054-P1.
"""

from datetime import datetime, timezone, timedelta
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import ConversationalMemoryEntryDB
from services.memory.conversational_memory import ConversationalMemoryEntry


class ConversationalMemoryRepository:
    """Repository for conversational memory entries."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_entry(self, user_id: str, entry: ConversationalMemoryEntry) -> str:
        """Save a memory entry. Returns entry ID."""
        entry_id = str(uuid4())

        db_entry = ConversationalMemoryEntryDB(
            id=entry_id,
            user_id=user_id,
            conversation_id=entry.conversation_id,
            timestamp=entry.timestamp,
            topic_summary=entry.topic_summary,
            entities_mentioned=entry.entities_mentioned,
            outcome=entry.outcome,
            user_sentiment=entry.user_sentiment,
        )

        self.session.add(db_entry)
        await self.session.commit()

        return entry_id

    async def get_entries_since(
        self,
        user_id: str,
        since: datetime
    ) -> List[ConversationalMemoryEntry]:
        """Get entries for user since given timestamp, ordered most recent first."""
        stmt = (
            select(ConversationalMemoryEntryDB)
            .where(ConversationalMemoryEntryDB.user_id == user_id)
            .where(ConversationalMemoryEntryDB.timestamp >= since)
            .order_by(ConversationalMemoryEntryDB.timestamp.desc())
        )

        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return [self._to_domain(row) for row in rows]

    async def delete_entries_before(self, user_id: str, before: datetime) -> int:
        """Delete entries older than given timestamp. Returns count deleted."""
        stmt = (
            delete(ConversationalMemoryEntryDB)
            .where(ConversationalMemoryEntryDB.user_id == user_id)
            .where(ConversationalMemoryEntryDB.timestamp < before)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.rowcount

    def _to_domain(self, db_entry: ConversationalMemoryEntryDB) -> ConversationalMemoryEntry:
        """Convert database model to domain model."""
        return ConversationalMemoryEntry(
            conversation_id=db_entry.conversation_id,
            timestamp=db_entry.timestamp,
            topic_summary=db_entry.topic_summary,
            entities_mentioned=db_entry.entities_mentioned or [],
            outcome=db_entry.outcome,
            user_sentiment=db_entry.user_sentiment,
        )
```

**Acceptance Criteria**:
- [ ] `save_entry()` persists entry to database
- [ ] `get_entries_since()` retrieves entries in time range
- [ ] `delete_entries_before()` removes old entries
- [ ] Returns domain models, not DB models

---

## Phase 4: Service Implementation

**Goal**: Complete service with repository integration

**File**: `services/memory/conversational_memory.py` (ADD to existing)

```python
class ConversationalMemoryService:
    """
    Manages 24-hour conversational memory (ADR-054 Layer 1).

    Enables natural continuity references like "yesterday we discussed..."
    """

    WINDOW_HOURS = 24

    def __init__(self, repository: "ConversationalMemoryRepository"):
        self.repository = repository

    async def record_conversation_end(
        self,
        user_id: str,
        conversation_id: str,
        summary: str,
        entities: Optional[List[str]] = None,
        outcome: Optional[str] = None,
        sentiment: Optional[str] = None,
    ) -> None:
        """
        Record conversation summary when session ends.

        Args:
            user_id: User ID
            conversation_id: Conversation ID
            summary: Brief topic summary
            entities: Projects, issues, people mentioned
            outcome: What was decided/accomplished
            sentiment: User sentiment (positive/neutral/negative)
        """
        entry = ConversationalMemoryEntry(
            conversation_id=conversation_id,
            timestamp=datetime.now(timezone.utc),
            topic_summary=summary,
            entities_mentioned=entities or [],
            outcome=outcome,
            user_sentiment=sentiment,
        )

        await self.repository.save_entry(user_id, entry)
        await self._prune_old_entries(user_id)

        logger.info(
            "conversation_memory_recorded",
            user_id=user_id,
            conversation_id=conversation_id,
            topic=summary,
        )

    async def get_memory_window(self, user_id: str) -> ConversationalMemoryWindow:
        """
        Get 24-hour memory window for user.

        Returns:
            ConversationalMemoryWindow with recent entries
        """
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(hours=self.WINDOW_HOURS)

        entries = await self.repository.get_entries_since(user_id, window_start)

        return ConversationalMemoryWindow(
            user_id=user_id,
            entries=entries,
            window_start=window_start,
            window_end=now,
        )

    async def _prune_old_entries(self, user_id: str) -> None:
        """Remove entries older than window."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.WINDOW_HOURS)
        deleted = await self.repository.delete_entries_before(user_id, cutoff)

        if deleted > 0:
            logger.debug(
                "conversation_memory_pruned",
                user_id=user_id,
                entries_deleted=deleted,
            )
```

**Acceptance Criteria**:
- [ ] `record_conversation_end()` saves entry and prunes old ones
- [ ] `get_memory_window()` returns entries from last 24 hours
- [ ] `_prune_old_entries()` removes entries older than 24hr
- [ ] Uses structured logging

---

## Phase 5: Module Setup

**Goal**: Create proper Python package structure

### 5A: services/memory/__init__.py

```python
"""
Memory services for cross-session context.

ADR-054: Cross-Session Memory Architecture
"""

from services.memory.conversational_memory import (
    ConversationalMemoryEntry,
    ConversationalMemoryWindow,
    ConversationalMemoryService,
)

__all__ = [
    "ConversationalMemoryEntry",
    "ConversationalMemoryWindow",
    "ConversationalMemoryService",
]
```

### 5B: tests/unit/services/memory/__init__.py

```python
"""Tests for memory services."""
```

**Acceptance Criteria**:
- [ ] `services/memory/__init__.py` exports public API
- [ ] `tests/unit/services/memory/__init__.py` exists

---

## Phase 6: Unit Tests

**Goal**: Comprehensive test coverage

**File**: `tests/unit/services/memory/test_conversational_memory.py`

```python
"""
Tests for ConversationalMemoryService.

Part of #657 MEM-ADR054-P1.
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock

from services.memory.conversational_memory import (
    ConversationalMemoryEntry,
    ConversationalMemoryWindow,
    ConversationalMemoryService,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_repository():
    """Mock repository for testing."""
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    """Service with mocked repository."""
    return ConversationalMemoryService(repository=mock_repository)


def make_entry(
    conversation_id: str = "conv-123",
    topic: str = "Test topic",
    hours_ago: float = 0,
    entities: list = None,
    outcome: str = None,
    sentiment: str = None,
) -> ConversationalMemoryEntry:
    """Helper to create test entries."""
    return ConversationalMemoryEntry(
        conversation_id=conversation_id,
        timestamp=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
        topic_summary=topic,
        entities_mentioned=entities or [],
        outcome=outcome,
        user_sentiment=sentiment,
    )


# =============================================================================
# Test: ConversationalMemoryEntry
# =============================================================================

class TestConversationalMemoryEntry:
    """Tests for the ConversationalMemoryEntry dataclass."""

    def test_creates_with_required_fields(self):
        """Entry can be created with required fields only."""
        entry = ConversationalMemoryEntry(
            conversation_id="conv-1",
            timestamp=datetime.now(timezone.utc),
            topic_summary="Discussed project roadmap",
        )
        assert entry.conversation_id == "conv-1"
        assert entry.topic_summary == "Discussed project roadmap"
        assert entry.entities_mentioned == []
        assert entry.outcome is None
        assert entry.user_sentiment is None

    def test_creates_with_all_fields(self):
        """Entry can be created with all fields."""
        entry = ConversationalMemoryEntry(
            conversation_id="conv-2",
            timestamp=datetime.now(timezone.utc),
            topic_summary="Fixed authentication bug",
            entities_mentioned=["auth-service", "user-api"],
            outcome="Bug resolved",
            user_sentiment="positive",
        )
        assert entry.entities_mentioned == ["auth-service", "user-api"]
        assert entry.outcome == "Bug resolved"
        assert entry.user_sentiment == "positive"


# =============================================================================
# Test: ConversationalMemoryWindow
# =============================================================================

class TestConversationalMemoryWindow:
    """Tests for the ConversationalMemoryWindow dataclass."""

    def test_empty_window(self):
        """Empty window has no entries."""
        window = ConversationalMemoryWindow(user_id="user-1")
        assert window.is_empty()
        assert window.get_most_recent() is None
        assert window.get_active_topics() == []
        assert window.get_active_entities() == []

    def test_get_most_recent(self):
        """Returns first entry (most recent)."""
        entries = [
            make_entry(topic="Recent", hours_ago=1),
            make_entry(topic="Older", hours_ago=5),
        ]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        assert window.get_most_recent().topic_summary == "Recent"

    def test_get_active_topics_deduplicates(self):
        """Topics are deduplicated."""
        entries = [
            make_entry(topic="Topic A"),
            make_entry(topic="Topic B"),
            make_entry(topic="Topic A"),  # Duplicate
        ]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        topics = window.get_active_topics()
        assert len(topics) == 2
        assert "Topic A" in topics
        assert "Topic B" in topics

    def test_get_active_entities_deduplicates(self):
        """Entities are deduplicated across entries."""
        entries = [
            make_entry(entities=["project-A", "user-X"]),
            make_entry(entities=["project-B", "user-X"]),  # user-X is duplicate
        ]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        entities = window.get_active_entities()
        assert len(entities) == 3
        assert "project-A" in entities
        assert "project-B" in entities
        assert "user-X" in entities

    def test_is_empty_false_with_entries(self):
        """is_empty returns False when entries exist."""
        entries = [make_entry()]
        window = ConversationalMemoryWindow(user_id="user-1", entries=entries)
        assert not window.is_empty()


# =============================================================================
# Test: ConversationalMemoryService.record_conversation_end
# =============================================================================

class TestRecordConversationEnd:
    """Tests for recording conversation summaries."""

    @pytest.mark.asyncio
    async def test_saves_entry_with_required_fields(self, service, mock_repository):
        """Records entry with required fields."""
        mock_repository.save_entry = AsyncMock()
        mock_repository.delete_entries_before = AsyncMock(return_value=0)

        await service.record_conversation_end(
            user_id="user-1",
            conversation_id="conv-1",
            summary="Discussed sprint planning",
        )

        mock_repository.save_entry.assert_called_once()
        call_args = mock_repository.save_entry.call_args
        assert call_args[0][0] == "user-1"  # user_id
        entry = call_args[0][1]
        assert entry.conversation_id == "conv-1"
        assert entry.topic_summary == "Discussed sprint planning"

    @pytest.mark.asyncio
    async def test_saves_entry_with_all_fields(self, service, mock_repository):
        """Records entry with all optional fields."""
        mock_repository.save_entry = AsyncMock()
        mock_repository.delete_entries_before = AsyncMock(return_value=0)

        await service.record_conversation_end(
            user_id="user-1",
            conversation_id="conv-2",
            summary="Fixed critical bug",
            entities=["auth-service", "api-gateway"],
            outcome="Deployed fix to production",
            sentiment="positive",
        )

        entry = mock_repository.save_entry.call_args[0][1]
        assert entry.entities_mentioned == ["auth-service", "api-gateway"]
        assert entry.outcome == "Deployed fix to production"
        assert entry.user_sentiment == "positive"

    @pytest.mark.asyncio
    async def test_prunes_old_entries_after_save(self, service, mock_repository):
        """Prunes old entries after saving new one."""
        mock_repository.save_entry = AsyncMock()
        mock_repository.delete_entries_before = AsyncMock(return_value=3)

        await service.record_conversation_end(
            user_id="user-1",
            conversation_id="conv-1",
            summary="Test",
        )

        mock_repository.delete_entries_before.assert_called_once()
        call_args = mock_repository.delete_entries_before.call_args
        assert call_args[0][0] == "user-1"


# =============================================================================
# Test: ConversationalMemoryService.get_memory_window
# =============================================================================

class TestGetMemoryWindow:
    """Tests for retrieving memory window."""

    @pytest.mark.asyncio
    async def test_returns_window_with_entries(self, service, mock_repository):
        """Returns window with entries from repository."""
        entries = [make_entry(topic="Topic 1"), make_entry(topic="Topic 2")]
        mock_repository.get_entries_since = AsyncMock(return_value=entries)

        window = await service.get_memory_window("user-1")

        assert window.user_id == "user-1"
        assert len(window.entries) == 2
        assert not window.is_empty()

    @pytest.mark.asyncio
    async def test_returns_empty_window_for_new_user(self, service, mock_repository):
        """Returns empty window for user with no history."""
        mock_repository.get_entries_since = AsyncMock(return_value=[])

        window = await service.get_memory_window("new-user")

        assert window.user_id == "new-user"
        assert window.is_empty()

    @pytest.mark.asyncio
    async def test_window_uses_24_hour_range(self, service, mock_repository):
        """Window queries for 24-hour range."""
        mock_repository.get_entries_since = AsyncMock(return_value=[])

        await service.get_memory_window("user-1")

        call_args = mock_repository.get_entries_since.call_args
        since_arg = call_args[0][1]

        # Should be approximately 24 hours ago
        now = datetime.now(timezone.utc)
        hours_ago = (now - since_arg).total_seconds() / 3600
        assert 23.9 < hours_ago < 24.1  # Allow small variance


# =============================================================================
# Test: Window Boundary Behavior
# =============================================================================

class TestWindowBoundary:
    """Tests for 24-hour window boundary behavior."""

    def test_window_start_is_24_hours_ago(self):
        """Window start is 24 hours before window end."""
        window = ConversationalMemoryWindow(user_id="user-1")
        duration = window.window_end - window.window_start
        assert 23.9 < duration.total_seconds() / 3600 < 24.1

    @pytest.mark.asyncio
    async def test_23_hour_old_entry_in_window(self, service, mock_repository):
        """Entry 23 hours old should be included."""
        entry = make_entry(hours_ago=23)
        mock_repository.get_entries_since = AsyncMock(return_value=[entry])

        window = await service.get_memory_window("user-1")

        assert len(window.entries) == 1

    @pytest.mark.asyncio
    async def test_25_hour_old_entry_excluded(self, service, mock_repository):
        """Entry 25 hours old should NOT be returned by repository."""
        # Repository filtering handles this - test documents expected behavior
        mock_repository.get_entries_since = AsyncMock(return_value=[])

        window = await service.get_memory_window("user-1")

        assert window.is_empty()


# =============================================================================
# Test: Pruning Behavior
# =============================================================================

class TestPruning:
    """Tests for old entry pruning."""

    @pytest.mark.asyncio
    async def test_prune_deletes_old_entries(self, service, mock_repository):
        """Pruning removes entries older than 24 hours."""
        mock_repository.delete_entries_before = AsyncMock(return_value=5)

        await service._prune_old_entries("user-1")

        mock_repository.delete_entries_before.assert_called_once()
        call_args = mock_repository.delete_entries_before.call_args
        assert call_args[0][0] == "user-1"

        # Cutoff should be ~24 hours ago
        cutoff = call_args[0][1]
        now = datetime.now(timezone.utc)
        hours_ago = (now - cutoff).total_seconds() / 3600
        assert 23.9 < hours_ago < 24.1
```

**Test Count**: 17 tests

**Acceptance Criteria**:
- [ ] All 17 tests pass
- [ ] Tests cover dataclass behavior
- [ ] Tests cover service methods
- [ ] Tests verify 24-hour boundary behavior
- [ ] Tests verify pruning behavior

---

## Completion Matrix

| Phase | Description | Evidence |
|-------|-------------|----------|
| 1 | Domain models | `services/memory/conversational_memory.py` exists with dataclasses |
| 2 | Database model + migration | `alembic upgrade head` succeeds |
| 3 | Repository | `services/repositories/conversational_memory_repository.py` exists |
| 4 | Service implementation | Service methods implemented |
| 5 | Module setup | `__init__.py` files exist |
| 6 | Unit tests | `pytest tests/unit/services/memory/ -v` passes (17 tests) |

---

## Post-Implementation

After #657 completes:
1. Update #657 issue with completion evidence
2. Update #416 description to remove "blocked by infrastructure"
3. Resume #416 gameplan creation

---

## References

- ADR-054: `docs/internal/architecture/current/adrs/adr-054-cross-session-memory-architecture.md`
- Existing pattern: `services/repositories/user_trust_profile_repository.py`
- Blocked issue: #416 MUX-INTERACT-WORKSPACE

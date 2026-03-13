# Gameplan: Fix Performance Test Import Errors

## Problem

Two performance test files have import errors:
- `tests/integration/test_performance_indexes_356.py` - imports `Conversation`, `ConversationTurn` from `services.database.models`
- `tests/integration/test_performance_indexes_532.py` - imports `ConversationTurn` from `services.database.models`

**Root Cause**: DB model classes are missing from `services/database/models.py`, but:
- ✅ Tables exist in database (created by migration `a9ee08bbdf8c`)
- ✅ Indexes exist (created by migrations `a7c3f9e2b1d4` and `b8e4f3c9a2d7`)
- ✅ Domain models exist in `services/domain/models.py`
- ❌ DB model classes missing from `services/database/models.py`

## Solution

Add missing DB model classes to `services/database/models.py`:

### 1. ConversationDB
Based on migration `a9ee08bbdf8c` (lines 27-44):
```python
class ConversationDB(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    title = Column(String, nullable=False, default="")
    context = Column(JSONB, nullable=False, default={})
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())
    last_activity_at = Column(DateTime, nullable=True)

    def to_domain(self) -> Conversation:
        """Convert DB model to domain model"""
        # Implementation
```

### 2. ConversationTurnDB
Based on migration `a9ee08bbdf8c` (lines 47-70):
```python
class ConversationTurnDB(Base):
    __tablename__ = "conversation_turns"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    turn_number = Column(Integer, nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    intent = Column(String, nullable=True)
    entities = Column(JSONB, nullable=False, default=[])
    references = Column(JSONB, nullable=False, default={})
    metadata = Column(JSONB, nullable=False, default={})
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    def to_domain(self) -> ConversationTurn:
        """Convert DB model to domain model"""
        # Implementation
```

## Import Locations

Tests need to import from `services.database.models`:
```python
# Current (broken):
from services.database.models import Conversation, ConversationTurn

# Should be (after fix):
from services.database.models import ConversationDB, ConversationTurnDB
```

But tests might expect the non-DB names, so update imports in tests to use `ConversationDB` and `ConversationTurnDB`.

## Files to Change

1. **services/database/models.py** - Add `ConversationDB` and `ConversationTurnDB` classes
2. **tests/integration/test_performance_indexes_356.py** - Update imports to use DB model names
3. **tests/integration/test_performance_indexes_532.py** - Update imports to use DB model names

## Verification

After fix, these commands should pass:
```bash
python -m pytest tests/integration/test_performance_indexes_356.py -xvs
python -m pytest tests/integration/test_performance_indexes_532.py -xvs
```

## Context

- Issue #356: PERF-INDEX - Composite indexes for conversation queries
- Issue #532: PERF-CONVERSATION-ANALYTICS - Intent-focused conversation indexes
- These tests validate that performance indexes are working correctly in production

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

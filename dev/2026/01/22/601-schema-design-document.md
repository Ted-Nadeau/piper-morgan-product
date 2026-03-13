# Schema Design: #601 MUX-MULTICHAT-PHASE0

## Overview

Design database schema for conversation graph primitives per ADR-050.

**Phase**: 0 (Schema design only - no implementation)
**Parent ADR**: ADR-050 (Conversation-as-Graph Model)
**Parent Epic**: #427 (MUX-IMPLEMENT-CONVERSE-MODEL)

---

## Current State

### ConversationDB Table (`conversations`)

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | String | PK | UUID |
| user_id | String | No | Owner |
| session_id | String | No | Session identifier |
| title | String | No | Default "" |
| context | JSONB | No | Default {} |
| is_active | Boolean | No | Default true |
| created_at | DateTime | No | server_default now() |
| updated_at | DateTime | No | server_default now() |
| last_activity_at | DateTime | Yes | |

**Indexes**:
- `idx_conversations_user_session` (user_id, session_id)
- `idx_conversations_last_activity` (last_activity_at)

### ConversationTurnDB Table (`conversation_turns`)

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | String | PK | UUID |
| conversation_id | String | No | FK → conversations.id |
| turn_number | Integer | No | Sequential within conversation |
| user_message | Text | No | Default "" |
| assistant_response | Text | No | Default "" |
| intent | String | Yes | Classified intent |
| entities | JSONB | No | Default [] |
| references | JSONB | No | Default {} |
| context_used | JSONB | No | Default {} |
| metadata | JSONB | No | Default {} |
| processing_time | Float | Yes | Response time in ms |
| created_at | DateTime | No | server_default now() |
| completed_at | DateTime | Yes | |

**Indexes**:
- `idx_conversation_turns_conversation` (conversation_id, turn_number)
- `idx_conversation_turns_created` (created_at)

**Constraints**:
- FK: conversation_id → conversations.id (ON DELETE CASCADE)

---

## Proposed Changes

### 1. Add `parent_id` to ConversationTurnDB

**Purpose**: Enable simple threading - a turn can be a reply to another turn.

```sql
ALTER TABLE conversation_turns
ADD COLUMN parent_id VARCHAR REFERENCES conversation_turns(id) ON DELETE SET NULL;

CREATE INDEX idx_conversation_turns_parent ON conversation_turns(parent_id);
```

**Design Decisions**:

| Question | Decision | Rationale |
|----------|----------|-----------|
| FK constraint? | Yes, self-referential | Maintains referential integrity |
| ON DELETE? | SET NULL | Preserve child turns if parent deleted |
| Nullable? | Yes | Root-level turns have no parent |
| Index? | Yes | Thread traversal queries |

**Domain Model Update** (services/domain/models.py):
```python
@dataclass
class ConversationTurn:
    # ... existing fields ...
    parent_id: Optional[str] = None  # For threading
```

---

### 2. New `ConversationLink` Table

**Purpose**: Explicit typed relationships between conversation elements.

```sql
CREATE TABLE conversation_links (
    id VARCHAR PRIMARY KEY,
    conversation_id VARCHAR NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    source_id VARCHAR NOT NULL REFERENCES conversation_turns(id) ON DELETE CASCADE,
    target_id VARCHAR NOT NULL REFERENCES conversation_turns(id) ON DELETE CASCADE,
    link_type VARCHAR NOT NULL,  -- ConversationLinkType enum value
    additional_types JSONB DEFAULT '[]',  -- For multi-type links
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by VARCHAR,  -- User or system that created the link

    CONSTRAINT fk_conversation FOREIGN KEY (conversation_id)
        REFERENCES conversations(id) ON DELETE CASCADE,
    CONSTRAINT fk_source FOREIGN KEY (source_id)
        REFERENCES conversation_turns(id) ON DELETE CASCADE,
    CONSTRAINT fk_target FOREIGN KEY (target_id)
        REFERENCES conversation_turns(id) ON DELETE CASCADE,
    CONSTRAINT chk_no_self_link CHECK (source_id != target_id)
);

-- Indexes for common query patterns
CREATE INDEX idx_conversation_links_conversation ON conversation_links(conversation_id);
CREATE INDEX idx_conversation_links_source ON conversation_links(source_id);
CREATE INDEX idx_conversation_links_target ON conversation_links(target_id);
CREATE INDEX idx_conversation_links_type ON conversation_links(link_type);

-- Composite index for "find all links of type X in conversation Y"
CREATE INDEX idx_conversation_links_conv_type ON conversation_links(conversation_id, link_type);
```

**Design Decisions**:

| Question | Decision | Rationale |
|----------|----------|-----------|
| Separate table vs embedded? | Separate table | Links are first-class entities per ADR-050 |
| Include conversation_id? | Yes | Enables efficient per-conversation queries |
| link_type as enum or string? | String | Extensible per Ted's clarification |
| additional_types type? | JSONB array | Supports multi-type links |
| Self-links allowed? | No (CHECK constraint) | Semantic nonsense |
| Duplicate links allowed? | Yes | Same pair can have different types |

**Domain Model** (services/domain/models.py):
```python
class ConversationLinkType(str, Enum):
    """Base link types. Extensible per ADR-050."""
    RELATES_TO = "relates_to"   # Default/generic
    REPLY = "reply"             # Direct response
    REFERENCE = "reference"     # Non-sequential citation
    BLOCKING = "blocking"       # Dependency
    VARIANT_OF = "variant_of"   # Alternative version
    ANNOTATES = "annotates"     # Commentary
    RESOLVES = "resolves"       # Closes/answers

@dataclass
class ConversationLink:
    """Explicit relationship between conversation elements."""
    id: str
    conversation_id: str
    source_id: str
    target_id: str
    link_type: str  # ConversationLinkType value or custom
    additional_types: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[str] = None
```

**Database Model** (services/database/models.py):
```python
class ConversationLinkDB(Base):
    """Database model for conversation links."""

    __tablename__ = "conversation_links"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False)
    source_id = Column(String, nullable=False)
    target_id = Column(String, nullable=False)
    link_type = Column(String, nullable=False)
    additional_types = Column(postgresql.JSONB, nullable=False, default=[])
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    created_by = Column(String, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["source_id"], ["conversation_turns.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["target_id"], ["conversation_turns.id"], ondelete="CASCADE"),
        CheckConstraint("source_id != target_id", name="chk_no_self_link"),
        Index("idx_conversation_links_conversation", "conversation_id"),
        Index("idx_conversation_links_source", "source_id"),
        Index("idx_conversation_links_target", "target_id"),
        Index("idx_conversation_links_type", "link_type"),
        Index("idx_conversation_links_conv_type", "conversation_id", "link_type"),
    )
```

---

## Migration Strategy

### For Existing Conversations

**Approach**: No data migration needed for Phase 0.

1. `parent_id` column added as nullable - existing rows get NULL (root-level)
2. `conversation_links` table created empty - no existing links to migrate
3. Existing linear conversations remain valid - just don't use graph features yet

**Future Considerations** (Phase 1+):
- Slack thread replies could auto-populate `parent_id`
- "reply" intents could auto-create REPLY links
- Manual link creation via UI

### Rollback Strategy

```sql
-- Rollback for parent_id
DROP INDEX IF EXISTS idx_conversation_turns_parent;
ALTER TABLE conversation_turns DROP COLUMN parent_id;

-- Rollback for conversation_links
DROP TABLE IF EXISTS conversation_links;
```

---

## ADR-050 Alignment Verification

| ADR-050 Requirement | Schema Design | Status |
|---------------------|---------------|--------|
| `parent_id` on ConversationTurn | Added as nullable FK | ✅ |
| `ConversationLink` table | Created with all fields | ✅ |
| `source_id`, `target_id` | FK to conversation_turns | ✅ |
| `type` field | `link_type` String (extensible) | ✅ |
| `additional_types` | JSONB array | ✅ |
| Multiple links same pair | Allowed (no unique constraint) | ✅ |
| Thread structure | Via parent_id | ✅ |

---

## Files to Create/Modify

### New Files
1. `alembic/versions/XXXXXX_mux_multichat_phase0_conversation_graph.py` - Migration

### Modified Files
1. `services/domain/models.py` - Add `parent_id` to ConversationTurn, add ConversationLink, add ConversationLinkType enum
2. `services/database/models.py` - Add `parent_id` to ConversationTurnDB, add ConversationLinkDB

---

## Open Questions for Phase 1

1. **Repository pattern**: Should ConversationLink have its own repository or be part of ConversationRepository?
2. **Cascade behavior**: When a turn is deleted, should its outgoing links be deleted or orphaned?
3. **Link validation**: Should we validate that source and target are in the same conversation?
4. **Index tuning**: After usage patterns emerge, may need additional composite indexes

---

## Summary

This Phase 0 design adds:
1. **`parent_id` column** to `conversation_turns` for simple threading
2. **`conversation_links` table** for explicit typed relationships

Both additions are backward-compatible - existing conversations continue to work without modification.

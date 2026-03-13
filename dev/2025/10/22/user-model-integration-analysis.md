# User Model Integration Analysis

**Date**: October 22, 2025, 7:05 AM
**Agent**: Cursor (Chief Architect)
**Issue**: #228 Phase 1A Preparation
**Duration**: 25 minutes

---

## Executive Summary

**Models to Update**: 3 (PersonalityProfile, TokenBlacklist, Feedback)
**Existing Data**: 86 rows across tables (84 PersonalityProfile, 0 TokenBlacklist, 2 Feedback)
**Migration Complexity**: Medium (requires data migration for PersonalityProfile)
**FK Strategy**: PersonalityProfile (NOT NULL), TokenBlacklist (NULLABLE), Feedback (NULLABLE)

**Key Finding**: System uses consistent String(255) user_id pattern with 84 existing user profiles that need User records created during migration.

---

## PersonalityProfile Model

### Current Structure

```python
class PersonalityProfileModel(Base, TimestampMixin):
    """Database model for personality profiles"""

    __tablename__ = "personality_profiles"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    user_id = Column(String(255), nullable=False, unique=True)
    warmth_level = Column(Float, nullable=False, default=0.6)
    confidence_style = Column(String(50), nullable=False, default="contextual")
    action_orientation = Column(String(50), nullable=False, default="medium")
    technical_depth = Column(String(50), nullable=False, default="balanced")
    is_active = Column(Boolean, nullable=False, default=True)

    # Indexes are defined in the migration
    __table_args__ = (
        Index("idx_personality_profiles_user_id", "user_id", unique=True),
        Index("idx_personality_profiles_active", "is_active"),
        Index("idx_personality_profiles_user_active", "user_id", "is_active"),
        Index("idx_personality_profiles_warmth", "warmth_level"),
        Index("idx_personality_profiles_confidence", "confidence_style"),
        Index("idx_personality_profiles_action", "action_orientation"),
        Index("idx_personality_profiles_technical", "technical_depth"),
    )
```

**Table Name**: `personality_profiles`

**Fields**:
| Field Name | Type | Nullable | Default | Notes |
|------------|------|----------|---------|-------|
| id | UUID | No | uuid4() | Primary key |
| user_id | String(255) | No | None | **Currently unique** |
| warmth_level | Float | No | 0.6 | Personality trait |
| confidence_style | String(50) | No | "contextual" | Personality trait |
| action_orientation | String(50) | No | "medium" | Personality trait |
| technical_depth | String(50) | No | "balanced" | Personality trait |
| is_active | Boolean | No | True | Status flag |
| created_at | DateTime | No | utcnow() | From TimestampMixin |
| updated_at | DateTime | No | utcnow() | From TimestampMixin |

**Indexes**:

- `idx_personality_profiles_user_id` (user_id, unique=True) - **CRITICAL UNIQUE INDEX**
- `idx_personality_profiles_active` (is_active)
- `idx_personality_profiles_user_active` (user_id, is_active)
- `idx_personality_profiles_warmth` (warmth_level)
- `idx_personality_profiles_confidence` (confidence_style)
- `idx_personality_profiles_action` (action_orientation)
- `idx_personality_profiles_technical` (technical_depth)

**Constraints**:

- **CRITICAL**: `user_id` has unique constraint (nullable=False, unique=True)
- Primary key on `id` (UUID)

**Relationships**:

- None currently exist

**Existing Data**:

- Row count: **84 rows**
- Sample user_ids: `['concurrent_1', 'concurrent_2', 'concurrent_3', 'concurrent_4', 'concurrent_5']`
- Data pattern: Consistent format with "concurrent_X" pattern

### Required Changes for User FK

**Add to Model**:

```python
# Modify existing user_id column to add FK
user_id = Column(String(255), ForeignKey("users.id"), nullable=False, index=True)

# Add relationship
user = relationship("User", back_populates="personality_profiles")
```

**Migration Considerations**:

- **CRITICAL**: Need to create User records for all 84 existing user_id values BEFORE adding FK
- Must preserve unique constraint on user_id
- All existing user_id values must exist in users table before FK creation
- Cannot have NULL user_id values (FK will be NOT NULL)

---

## TokenBlacklist Model

### Current Structure

```python
class TokenBlacklist(Base):
    """
    Blacklisted JWT tokens (database fallback for Redis)

    Stores revoked tokens for security invalidation when Redis unavailable.
    Redis is primary storage with TTL; this is fallback only.
    """

    __tablename__ = "token_blacklist"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Token identification
    token_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)

    # Blacklist metadata
    reason = Column(String(50), nullable=False)  # logout, security, admin
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Strategic indexes for performance
    __table_args__ = (
        Index("idx_token_blacklist_token_id", "token_id", unique=True),
        Index("idx_token_blacklist_expires", "expires_at"),
        Index("idx_token_blacklist_user_id", "user_id"),
        Index("idx_token_blacklist_user_expires", "user_id", "expires_at"),
    )
```

**Table Name**: `token_blacklist`

**Fields**:
| Field Name | Type | Nullable | Default | Notes |
|------------|------|----------|---------|-------|
| id | Integer | No | autoincrement | Primary key |
| token_id | String(255) | No | None | Unique token identifier |
| user_id | String(255) | **Yes** | None | **Nullable!** |
| reason | String(50) | No | None | Blacklist reason |
| expires_at | DateTime | No | None | Token expiration |
| created_at | DateTime | No | utcnow() | Creation timestamp |

**Indexes**:

- `idx_token_blacklist_token_id` (token_id, unique=True)
- `idx_token_blacklist_expires` (expires_at)
- `idx_token_blacklist_user_id` (user_id)
- `idx_token_blacklist_user_expires` (user_id, expires_at)

**Constraints**:

- Unique constraint on `token_id`
- Primary key on `id`

**Relationships**:

- None currently exist

**Existing Data**:

- Row count: **0 rows**
- Rows with user_id: 0
- Rows without user_id: 0

### Required Changes for User FK

**Add to Model**:

```python
# Modify user_id column to add FK (keep nullable=True)
user_id = Column(String(255), ForeignKey("users.id"), nullable=True, index=True)

# Add relationship
user = relationship("User", back_populates="blacklisted_tokens")
```

**Migration Considerations**:

- FK can be nullable (existing behavior preserved)
- No existing data to migrate
- Rows without user_id can remain (no FK constraint violation)
- FK constraint allows NULL values

---

## Feedback Model

### Current Structure

```python
class FeedbackDB(Base, TimestampMixin):
    """Database model for user feedback tracking - PM-005"""

    __tablename__ = "feedback"

    # Primary key
    id = Column(String, primary_key=True)

    # Core feedback data
    session_id = Column(String, nullable=False, index=True)
    feedback_type = Column(String, nullable=False)  # "bug", "feature", "ux", "general"
    rating = Column(Integer)  # 1-5 rating (optional)
    comment = Column(Text, nullable=False)
    context = Column(JSON, default=dict)  # Additional context data

    # User and session context
    user_id = Column(String, index=True)
    conversation_context = Column(JSON, default=dict)  # Conversation context if available

    # Feedback metadata
    source = Column(String, default="api")  # "api", "ui", "conversation"
    status = Column(String, default="new")  # "new", "reviewed", "addressed", "closed"
    priority = Column(String, default="medium")  # "low", "medium", "high", "critical"

    # Analysis and processing
    sentiment_score = Column(Float)  # -1.0 to 1.0
    categories = Column(JSON, default=list)  # Auto-detected categories
    tags = Column(JSON, default=list)  # User or system tags

    # Strategic indexes for query performance
    __table_args__ = (
        Index("idx_feedback_session_id", "session_id"),
        Index("idx_feedback_type", "feedback_type"),
        Index("idx_feedback_rating", "rating"),
        Index("idx_feedback_status", "status"),
        Index("idx_feedback_created_at", "created_at"),
        Index("idx_feedback_user_id", "user_id"),
        Index("idx_feedback_source", "source"),
    )
```

**Table Name**: `feedback`

**Fields**:
| Field Name | Type | Nullable | Default | Notes |
|------------|------|----------|---------|-------|
| id | String | No | None | Primary key |
| session_id | String | No | None | Session identifier |
| feedback_type | String | No | None | Feedback category |
| rating | Integer | Yes | None | Optional 1-5 rating |
| comment | Text | No | None | Feedback content |
| context | JSON | Yes | dict | Additional context |
| user_id | String | **Yes** | None | **Note: String not String(255)** |
| conversation_context | JSON | Yes | dict | Conversation context |
| source | String | Yes | "api" | Feedback source |
| status | String | Yes | "new" | Processing status |
| priority | String | Yes | "medium" | Priority level |
| sentiment_score | Float | Yes | None | Sentiment analysis |
| categories | JSON | Yes | list | Auto-detected categories |
| tags | JSON | Yes | list | User/system tags |
| created_at | DateTime | No | utcnow() | From TimestampMixin |
| updated_at | DateTime | No | utcnow() | From TimestampMixin |

**Indexes**:

- `idx_feedback_session_id` (session_id)
- `idx_feedback_type` (feedback_type)
- `idx_feedback_rating` (rating)
- `idx_feedback_status` (status)
- `idx_feedback_created_at` (created_at)
- `idx_feedback_user_id` (user_id)
- `idx_feedback_source` (source)

**Constraints**:

- Primary key on `id` (String)

**Relationships**:

- None currently exist

**Existing Data**:

- Row count: **2 rows**

### Required Changes for User FK

**Add to Model**:

```python
# Modify user_id column - CHANGE TYPE to String(255) for consistency AND add FK
user_id = Column(String(255), ForeignKey("users.id"), nullable=True, index=True)

# Add relationship
user = relationship("User", back_populates="feedback")
```

**Migration Considerations**:

- **CRITICAL**: Need to alter column type String → String(255) for consistency
- FK will be nullable (existing behavior)
- Only 2 rows exist, minimal data impact
- Need to check if existing user_id values exist in users table

---

## Migration Strategy

### From Recent JWT Migration

**Pattern Observed**:

```python
# From 68767106bfb6_add_token_blacklist_table_issue_227.py
def upgrade() -> None:
    """Upgrade schema: Create token_blacklist table with strategic indexes."""

    # Create token_blacklist table
    op.create_table(
        'token_blacklist',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('token_id', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=True),
        sa.Column('reason', sa.String(length=50), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create strategic indexes for performance
    op.create_index('idx_token_blacklist_token_id', 'token_blacklist', ['token_id'], unique=True)
    op.create_index('idx_token_blacklist_expires', 'token_blacklist', ['expires_at'], unique=False)
    op.create_index('idx_token_blacklist_user_id', 'token_blacklist', ['user_id'], unique=False)
    op.create_index('idx_token_blacklist_user_expires', 'token_blacklist', ['user_id', 'expires_at'], unique=False)
```

**Naming Conventions**:

- Migration files: `[timestamp]_[description]_issue_[number].py`
- FK names: Not shown in recent migration (no FKs added)
- Index names: `idx_[table]_[column(s)]`

### Recommended Migration Order

**Step 1: Create users table**

```python
def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_users_username', 'users', ['username'], unique=True)
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_active', 'users', ['is_active'], unique=False)
```

**Step 2: Populate users table**

```python
    # Get all distinct user_id values from existing tables
    connection = op.get_bind()

    # Get user_ids from personality_profiles (84 rows)
    result = connection.execute(text("SELECT DISTINCT user_id FROM personality_profiles"))
    personality_user_ids = [row[0] for row in result.fetchall()]

    # Get user_ids from feedback (2 rows, might be NULL)
    result = connection.execute(text("SELECT DISTINCT user_id FROM feedback WHERE user_id IS NOT NULL"))
    feedback_user_ids = [row[0] for row in result.fetchall()]

    # Combine and deduplicate
    all_user_ids = list(set(personality_user_ids + feedback_user_ids))

    # Insert User records
    for user_id in all_user_ids:
        op.execute(
            text("INSERT INTO users (id, username, email, is_active, is_verified, created_at, updated_at) VALUES (:id, :username, :email, :is_active, :is_verified, :created_at, :updated_at)"),
            {
                'id': user_id,
                'username': user_id,  # Use user_id as username initially
                'email': f"{user_id}@example.com",  # Placeholder email
                'is_active': True,
                'is_verified': False,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        )
```

**Step 3: Add FK to personality_profiles**

```python
    # Add FK constraint to personality_profiles
    op.create_foreign_key(
        'fk_personality_profiles_user_id',
        'personality_profiles',
        'users',
        ['user_id'],
        ['id']
    )
```

**Step 4: Add FK to token_blacklist**

```python
    # Add FK constraint to token_blacklist (nullable)
    op.create_foreign_key(
        'fk_token_blacklist_user_id',
        'token_blacklist',
        'users',
        ['user_id'],
        ['id']
    )
```

**Step 5: Alter feedback.user_id and add FK**

```python
    # Alter feedback.user_id column type String -> String(255)
    op.alter_column('feedback', 'user_id', type_=sa.String(255))

    # Add FK constraint to feedback (nullable)
    op.create_foreign_key(
        'fk_feedback_user_id',
        'feedback',
        'users',
        ['user_id'],
        ['id']
    )
```

### Data Migration Requirements

**Existing user_id Values**:

- PersonalityProfile: 84 values (concurrent_1, concurrent_2, concurrent_3, concurrent_4, concurrent_5, ...)
- TokenBlacklist: 0 values (no data)
- Feedback: 2 values (need to check what they are)

**Strategy**:

```python
# In migration upgrade():
# 1. Create users table with indexes
# 2. Get all unique user_id values from personality_profiles and feedback
# 3. Create User records for each unique user_id
# 4. Add FK constraints to all three tables
# 5. Alter feedback.user_id column type if needed
```

**Rollback Strategy**:

```python
# In migration downgrade():
# 1. Drop FK constraints from all tables
# 2. Alter feedback.user_id back to String (if changed)
# 3. Drop users table and all its indexes
# 4. Restore original state
```

---

## User Model Specification

### Recommended Structure

Based on existing patterns and epic needs:

```python
class User(Base):
    """User account model"""
    __tablename__ = "users"

    # Primary key - matches existing user_id pattern
    id = Column(String(255), primary_key=True)

    # Authentication fields
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=True)  # For future password auth

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    personality_profiles = relationship("PersonalityProfileModel", back_populates="user")
    api_keys = relationship("UserAPIKey", back_populates="user", cascade="all, delete-orphan")
    blacklisted_tokens = relationship("TokenBlacklist", back_populates="user")
    feedback = relationship("FeedbackDB", back_populates="user")
    # audit_logs = relationship("AuditLog", back_populates="user")  # For Issue #230

    # Indexes
    __table_args__ = (
        Index("idx_users_username", "username", unique=True),
        Index("idx_users_email", "email", unique=True),
        Index("idx_users_active", "is_active"),
    )
```

**Why This Structure**:

- id as String(255) matches existing pattern
- Includes auth fields for JWT (#227)
- Includes relationships to all 3 models
- Includes api_keys relationship for #228
- Includes audit relationship for future #230
- Standard timestamps
- Proper indexes

---

## Testing Patterns

### From Existing Tests

**Pattern for model tests**: Found in existing codebase

```python
# From tests/domain/test_user_preference_manager.py pattern
# Tests exist for user-related functionality
```

**Pattern for relationship tests**: Need to create new patterns for FK relationships

---

## Summary for Code

**What Code Needs to Create**:

1. **User Model**: Use specification above
2. **Update PersonalityProfileModel**: Add FK and relationship
3. **Update TokenBlacklist**: Add FK and relationship
4. **Update FeedbackDB**: Change user_id type to String(255), add FK and relationship
5. **Migration**: Follow order and strategy documented above
6. **Tests**: Create new tests for User model and relationships

**Critical Details**:

- PersonalityProfileModel.user_id: Has unique constraint, NOT NULL FK required
- TokenBlacklist.user_id: Nullable FK (existing behavior preserved)
- FeedbackDB.user_id: Need type change String → String(255), nullable FK
- Existing data: 84 user_id values in PersonalityProfile need User records created
- Migration naming: `[timestamp]_add_user_model_issue_228.py`

**Data Migration Strategy**:

1. Create users table
2. Extract all unique user_id values from personality_profiles and feedback
3. Create User records with id=user_id, username=user_id, email=user_id@example.com
4. Add FK constraints to all three tables
5. Alter feedback.user_id column type to String(255)

---

## Evidence Checklist

Investigation complete - all items verified:

- [x] PersonalityProfile complete structure documented
- [x] TokenBlacklist complete structure documented
- [x] Feedback complete structure documented
- [x] All constraints documented
- [x] All indexes documented
- [x] All relationships documented (none exist currently)
- [x] Existing data counts obtained (84, 0, 2)
- [x] Recent migration patterns documented
- [x] Migration strategy defined
- [x] Data migration plan created
- [x] User model specification complete

---

**Investigation complete. Code can now write Phase 1A guidance with 95%+ confidence.**

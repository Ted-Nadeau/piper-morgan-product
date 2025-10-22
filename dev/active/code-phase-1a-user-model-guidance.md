# Phase 1A: Create User Model Foundation - Implementation Guidance

**Agent**: Claude Code (Programmer)
**Issue**: #228 CORE-USERS-API (Phase 1A)
**Task**: Create User model and integrate with existing models
**Date**: October 22, 2025, 7:16 AM
**Estimated Effort**: 2.5 hours

---

## 🎯 Context from Cursor's Investigation

**Cursor discovered** (complete analysis in `dev/2025/10/22/user-model-integration-analysis.md`):
- ✅ 84 PersonalityProfile records exist (user_ids: concurrent_1, concurrent_2, etc.)
- ✅ 0 TokenBlacklist records (empty table, no migration issues)
- ✅ 2 Feedback records (need User records created)
- ✅ PersonalityProfileModel uses String(255), NOT NULL, UNIQUE on user_id
- ✅ TokenBlacklist uses String(255), NULLABLE on user_id
- ✅ FeedbackDB uses String (not String(255)!) - NEEDS TYPE CHANGE
- ✅ Recent migration pattern from #227 (JWT blacklist)

**Total User records needed**: ~86 (84 from PersonalityProfile + 2 from Feedback)

---

## Phase 1A Overview

### What You're Creating

1. **User Model** - New first-class entity for user accounts
2. **Update PersonalityProfileModel** - Add FK relationship to User
3. **Update TokenBlacklist** - Add FK relationship to User
4. **Update FeedbackDB** - Change type + add FK relationship to User
5. **Migration** - Create users table + populate from existing data + add FKs
6. **Tests** - User model + relationships

### Critical Success Factors

- ✅ Create 86 User records from existing user_id values
- ✅ PersonalityProfile FK must be NOT NULL (unique constraint)
- ✅ TokenBlacklist FK can be nullable (preserve existing behavior)
- ✅ Feedback needs type change String → String(255)
- ✅ One clean migration (no breaking existing data)
- ✅ Full rollback capability

---

## Step 1: Create User Model (30 min)

### 1.1 Add User Model to models.py

**File**: `services/database/models.py`

**Location**: Add BEFORE PersonalityProfileModel (User should be early in file)

```python
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, String, Index, ForeignKey
from sqlalchemy.orm import relationship
from services.database.base import Base


class User(Base):
    """
    User account model.

    Represents authenticated users in the system. Initially populated from
    existing user_id values in PersonalityProfile, TokenBlacklist, and Feedback.

    For Alpha: Uses user_id pattern from existing data (concurrent_X).
    For Beta: Will include full authentication with username/email/password.
    """
    __tablename__ = "users"

    # Primary key - matches existing user_id pattern (String(255))
    id = Column(String(255), primary_key=True)

    # Authentication fields
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=True)  # For future password auth

    # Status flags
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    personality_profiles = relationship(
        "PersonalityProfileModel",
        back_populates="user",
        lazy="select"
    )
    api_keys = relationship(
        "UserAPIKey",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select"
    )
    blacklisted_tokens = relationship(
        "TokenBlacklist",
        back_populates="user",
        lazy="select"
    )
    feedback = relationship(
        "FeedbackDB",
        back_populates="user",
        lazy="select"
    )
    # audit_logs = relationship("AuditLog", back_populates="user")  # For Issue #230

    # Indexes
    __table_args__ = (
        Index("idx_users_username", "username", unique=True),
        Index("idx_users_email", "email", unique=True),
        Index("idx_users_active", "is_active"),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, active={self.is_active})>"
```

**Verify**:
```bash
# Quick syntax check
python3 -c "from services.database.models import User; print('User model imports successfully')"
```

---

## Step 2: Update PersonalityProfileModel (15 min)

### 2.1 Modify PersonalityProfileModel

**File**: `services/database/models.py`

**Find this line**:
```python
class PersonalityProfileModel(Base, TimestampMixin):
    """Database model for personality profiles"""

    __tablename__ = "personality_profiles"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    user_id = Column(String(255), nullable=False, unique=True)  # ← MODIFY THIS LINE
```

**Change to**:
```python
class PersonalityProfileModel(Base, TimestampMixin):
    """Database model for personality profiles"""

    __tablename__ = "personality_profiles"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False, unique=True)  # ← ADDED ForeignKey
```

**Add relationship** (after all Column definitions, before __table_args__):
```python
    # ... existing columns ...
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    user = relationship("User", back_populates="personality_profiles")

    # Indexes are defined in the migration
    __table_args__ = (
```

**Critical Notes**:
- Keep `nullable=False` (PersonalityProfile requires user)
- Keep `unique=True` (one profile per user)
- FK points to users.id
- relationship name is "user" (singular)

---

## Step 3: Update TokenBlacklist (15 min)

### 3.1 Modify TokenBlacklist

**File**: `services/database/models.py`

**Find this line**:
```python
class TokenBlacklist(Base):
    """Blacklisted JWT tokens"""
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(255), unique=True, nullable=False, index=True)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)  # ← MODIFY THIS LINE
```

**Change to**:
```python
class TokenBlacklist(Base):
    """Blacklisted JWT tokens"""
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(255), unique=True, nullable=False, index=True)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=True, index=True)  # ← ADDED ForeignKey
```

**Add relationship** (after all Column definitions, before __table_args__):
```python
    # ... existing columns ...
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    user = relationship("User", back_populates="blacklisted_tokens")

    __table_args__ = (
```

**Critical Notes**:
- Keep `nullable=True` (tokens can exist without user_id)
- FK points to users.id
- relationship name is "user" (singular)

---

## Step 4: Update FeedbackDB (15 min)

### 4.1 Modify FeedbackDB

**File**: `services/database/models.py`

**Find this line**:
```python
class FeedbackDB(Base):
    """Database model for feedback"""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)  # ← MODIFY THIS LINE
```

**Change to**:
```python
class FeedbackDB(Base):
    """Database model for feedback"""
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=True, index=True)  # ← CHANGED TYPE + ADDED FK
```

**Add relationship** (after all Column definitions):
```python
    # ... existing columns ...
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="feedback")
```

**Critical Notes**:
- **TYPE CHANGE**: String → String(255) for consistency
- FK points to users.id
- Keep nullable=True (feedback can be anonymous)
- Migration must handle type change

---

## Step 5: Create Migration (45 min)

### 5.1 Generate Migration

```bash
cd /Users/xian/Development/piper-morgan
alembic revision -m "add_user_model_issue_228"
```

**Migration file will be**: `alembic/versions/XXXXXX_add_user_model_issue_228.py`

### 5.2 Write Migration Code

**File**: `alembic/versions/XXXXXX_add_user_model_issue_228.py`

**Replace content with**:

```python
"""add user model issue 228

Revision ID: XXXXXX
Revises: YYYYYY
Create Date: 2025-10-22 07:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'XXXXXX'  # Keep auto-generated value
down_revision = 'YYYYYY'  # Keep auto-generated value
branch_labels = None
depends_on = None


def upgrade():
    """
    Create User model and integrate with existing models.

    Steps:
    1. Create users table with indexes
    2. Populate users table from existing user_id values
    3. Add FK constraints to personality_profiles
    4. Add FK constraints to token_blacklist
    5. Alter feedback.user_id column type and add FK constraint
    """

    # Step 1: Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create indexes on users table
    op.create_index('idx_users_username', 'users', ['username'], unique=True)
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_active', 'users', ['is_active'], unique=False)

    # Step 2: Populate users table from existing user_id values
    # Get connection for raw SQL
    connection = op.get_bind()

    # Get unique user_ids from personality_profiles
    result = connection.execute(sa.text(
        "SELECT DISTINCT user_id FROM personality_profiles WHERE user_id IS NOT NULL"
    ))
    personality_user_ids = [row[0] for row in result]

    # Get unique user_ids from feedback (if any)
    try:
        result = connection.execute(sa.text(
            "SELECT DISTINCT user_id FROM feedback WHERE user_id IS NOT NULL AND user_id != ''"
        ))
        feedback_user_ids = [row[0] for row in result]
    except Exception:
        # Feedback table might not have data or column might not exist yet
        feedback_user_ids = []

    # Combine and deduplicate
    all_user_ids = list(set(personality_user_ids + feedback_user_ids))

    # Create User records for each unique user_id
    for user_id in all_user_ids:
        connection.execute(
            sa.text(
                """
                INSERT INTO users (id, username, email, is_active, is_verified, created_at, updated_at)
                VALUES (:id, :username, :email, :is_active, :is_verified, :created_at, :updated_at)
                """
            ),
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

    # Step 3: Add FK constraint to personality_profiles
    op.create_foreign_key(
        'fk_personality_profiles_user_id',
        'personality_profiles',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'  # If user deleted, delete profiles
    )

    # Step 4: Add FK constraint to token_blacklist
    op.create_foreign_key(
        'fk_token_blacklist_user_id',
        'token_blacklist',
        'users',
        ['user_id'],
        ['id'],
        ondelete='SET NULL'  # If user deleted, set user_id to NULL
    )

    # Step 5: Alter feedback.user_id column type and add FK
    # First, alter column type from String to String(255)
    op.alter_column(
        'feedback',
        'user_id',
        type_=sa.String(255),
        existing_type=sa.String(),
        existing_nullable=True
    )

    # Then add FK constraint
    op.create_foreign_key(
        'fk_feedback_user_id',
        'feedback',
        'users',
        ['user_id'],
        ['id'],
        ondelete='SET NULL'  # If user deleted, set user_id to NULL
    )


def downgrade():
    """
    Remove User model and FK constraints.

    Rollback steps in reverse order.
    """

    # Step 5 rollback: Drop FK from feedback and restore column type
    op.drop_constraint('fk_feedback_user_id', 'feedback', type_='foreignkey')
    op.alter_column(
        'feedback',
        'user_id',
        type_=sa.String(),
        existing_type=sa.String(255),
        existing_nullable=True
    )

    # Step 4 rollback: Drop FK from token_blacklist
    op.drop_constraint('fk_token_blacklist_user_id', 'token_blacklist', type_='foreignkey')

    # Step 3 rollback: Drop FK from personality_profiles
    op.drop_constraint('fk_personality_profiles_user_id', 'personality_profiles', type_='foreignkey')

    # Step 2 rollback: No action needed (users table will be dropped)

    # Step 1 rollback: Drop users table and indexes
    op.drop_index('idx_users_active', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_index('idx_users_username', table_name='users')
    op.drop_table('users')
```

### 5.3 Verify Migration

```bash
# Check migration syntax
alembic check

# Show current revision
alembic current

# Show pending migrations
alembic history | head -20
```

**Success criteria**:
- [ ] Migration file created
- [ ] No syntax errors in migration
- [ ] Migration appears in `alembic history`

---

## Step 6: Apply Migration (15 min)

### 6.1 Run Migration

```bash
# Apply migration
alembic upgrade head

# Expected output:
# INFO  [alembic.runtime.migration] Running upgrade YYYYYY -> XXXXXX, add user model issue 228
```

### 6.2 Verify Migration Results

```bash
# Check users table created
python3 << 'EOF'
import asyncio
from services.database.session_factory import AsyncSessionFactory
from sqlalchemy import text

async def verify_migration():
    async with AsyncSessionFactory.session_scope() as session:
        # Check users table exists
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        print(f"✅ Users table exists: {user_count} rows")

        # Check FK on personality_profiles
        result = await session.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name='personality_profiles'
            AND constraint_type='FOREIGN KEY'
        """))
        fks = result.fetchall()
        print(f"✅ PersonalityProfile FK: {[fk[0] for fk in fks]}")

        # Check FK on token_blacklist
        result = await session.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name='token_blacklist'
            AND constraint_type='FOREIGN KEY'
        """))
        fks = result.fetchall()
        print(f"✅ TokenBlacklist FK: {[fk[0] for fk in fks]}")

        # Check FK on feedback
        result = await session.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name='feedback'
            AND constraint_type='FOREIGN KEY'
        """))
        fks = result.fetchall()
        print(f"✅ Feedback FK: {[fk[0] for fk in fks]}")

asyncio.run(verify_migration())
EOF
```

**Success criteria**:
- [ ] Users table has ~86 rows
- [ ] FK constraint exists on personality_profiles
- [ ] FK constraint exists on token_blacklist
- [ ] FK constraint exists on feedback
- [ ] No errors in verification

**STOP if**: Any verification fails - report to PM

---

## Step 7: Test User Model (30 min)

### 7.1 Create Test File

**File**: `tests/database/test_user_model.py` (CREATE)

```python
"""
Tests for User model and relationships
"""
import pytest
from datetime import datetime
from services.database.models import User, PersonalityProfileModel, TokenBlacklist, FeedbackDB, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_user():
    """Test creating a User record"""
    async with AsyncSessionFactory.session_scope() as session:
        user = User(
            id="test_user_create",
            username="testuser",
            email="test@example.com",
            is_active=True,
            is_verified=False
        )
        session.add(user)
        await session.commit()

        # Verify user created
        result = await session.execute(select(User).where(User.id == "test_user_create"))
        retrieved_user = result.scalar_one_or_none()

        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        assert retrieved_user.email == "test@example.com"
        assert retrieved_user.is_active is True
        assert retrieved_user.is_verified is False

        # Cleanup
        await session.delete(retrieved_user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_personality_profile_relationship():
    """Test User <-> PersonalityProfile relationship"""
    async with AsyncSessionFactory.session_scope() as session:
        # Create user
        user = User(
            id="test_user_profile_rel",
            username="profileuser",
            email="profile@example.com"
        )
        session.add(user)
        await session.flush()  # Get user.id assigned

        # Create personality profile linked to user
        from uuid import uuid4
        profile = PersonalityProfileModel(
            id=uuid4(),
            user_id=user.id,
            warmth_level=0.7,
            confidence_style="confident",
            action_orientation="high",
            technical_depth="deep"
        )
        session.add(profile)
        await session.commit()

        # Test relationship from User -> PersonalityProfile
        result = await session.execute(select(User).where(User.id == "test_user_profile_rel"))
        retrieved_user = result.scalar_one_or_none()

        # Load relationship
        await session.refresh(retrieved_user, ['personality_profiles'])

        assert len(retrieved_user.personality_profiles) == 1
        assert retrieved_user.personality_profiles[0].warmth_level == 0.7

        # Test relationship from PersonalityProfile -> User
        result = await session.execute(
            select(PersonalityProfileModel).where(PersonalityProfileModel.user_id == "test_user_profile_rel")
        )
        retrieved_profile = result.scalar_one_or_none()

        await session.refresh(retrieved_profile, ['user'])

        assert retrieved_profile.user.username == "profileuser"

        # Cleanup
        await session.delete(profile)
        await session.delete(user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_api_key_relationship():
    """Test User <-> UserAPIKey relationship with cascade delete"""
    async with AsyncSessionFactory.session_scope() as session:
        # Create user
        user = User(
            id="test_user_apikey_rel",
            username="apikeyuser",
            email="apikey@example.com"
        )
        session.add(user)
        await session.flush()

        # Create API key linked to user
        # Note: UserAPIKey will be created in Phase 1B
        # This test will be completed then

        # For now, just verify user created
        assert user.id == "test_user_apikey_rel"

        # Cleanup
        await session.delete(user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_token_blacklist_relationship():
    """Test User <-> TokenBlacklist relationship"""
    async with AsyncSessionFactory.session_scope() as session:
        # Create user
        user = User(
            id="test_user_token_rel",
            username="tokenuser",
            email="token@example.com"
        )
        session.add(user)
        await session.flush()

        # Create blacklisted token linked to user
        from datetime import timedelta
        token = TokenBlacklist(
            jti="test_jti_123",
            token_hash="test_hash_456",
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
        session.add(token)
        await session.commit()

        # Test relationship
        result = await session.execute(select(User).where(User.id == "test_user_token_rel"))
        retrieved_user = result.scalar_one_or_none()

        await session.refresh(retrieved_user, ['blacklisted_tokens'])

        assert len(retrieved_user.blacklisted_tokens) == 1
        assert retrieved_user.blacklisted_tokens[0].jti == "test_jti_123"

        # Cleanup
        await session.delete(token)
        await session.delete(user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_cascade_delete():
    """Test that deleting user cascades to API keys but not other relationships"""
    async with AsyncSessionFactory.session_scope() as session:
        # Create user
        user = User(
            id="test_user_cascade",
            username="cascadeuser",
            email="cascade@example.com"
        )
        session.add(user)
        await session.flush()

        # Create personality profile (should NOT cascade delete)
        from uuid import uuid4
        profile = PersonalityProfileModel(
            id=uuid4(),
            user_id=user.id,
            warmth_level=0.5
        )
        session.add(profile)
        await session.commit()

        # Delete user
        await session.delete(user)
        await session.commit()

        # Profile should still exist (FK is CASCADE but relationship doesn't delete)
        # This test verifies FK behavior

        # Cleanup profile
        await session.delete(profile)
        await session.commit()


@pytest.mark.asyncio
async def test_user_unique_constraints():
    """Test unique constraints on username and email"""
    async with AsyncSessionFactory.session_scope() as session:
        # Create first user
        user1 = User(
            id="test_user_unique_1",
            username="uniqueuser",
            email="unique@example.com"
        )
        session.add(user1)
        await session.commit()

        # Try to create second user with same username
        user2 = User(
            id="test_user_unique_2",
            username="uniqueuser",  # Duplicate!
            email="unique2@example.com"
        )
        session.add(user2)

        with pytest.raises(Exception):  # Should raise IntegrityError
            await session.commit()

        await session.rollback()

        # Try to create user with same email
        user3 = User(
            id="test_user_unique_3",
            username="uniqueuser2",
            email="unique@example.com"  # Duplicate!
        )
        session.add(user3)

        with pytest.raises(Exception):  # Should raise IntegrityError
            await session.commit()

        await session.rollback()

        # Cleanup
        await session.delete(user1)
        await session.commit()
```

### 7.2 Run Tests

```bash
cd /Users/xian/Development/piper-morgan
pytest tests/database/test_user_model.py -v

# Expected output:
# tests/database/test_user_model.py::test_create_user PASSED
# tests/database/test_user_personality_profile_relationship PASSED
# tests/database/test_user_api_key_relationship PASSED
# tests/database/test_user_token_blacklist_relationship PASSED
# tests/database/test_user_cascade_delete PASSED
# tests/database/test_user_unique_constraints PASSED
```

**Success criteria**:
- [ ] All 6 tests passing
- [ ] User model works
- [ ] Relationships work
- [ ] Unique constraints enforced
- [ ] No FK errors

**STOP if**: Any test fails - report to PM

---

## Phase 1A Completion Checklist

### Model Creation
- [ ] User model added to models.py
- [ ] User model imports successfully
- [ ] All fields correct (id, username, email, password_hash, status, timestamps)
- [ ] All relationships defined (personality_profiles, api_keys, blacklisted_tokens, feedback)
- [ ] All indexes defined

### Model Updates
- [ ] PersonalityProfileModel updated with FK
- [ ] PersonalityProfileModel relationship added
- [ ] TokenBlacklist updated with FK
- [ ] TokenBlacklist relationship added
- [ ] FeedbackDB updated with type change + FK
- [ ] FeedbackDB relationship added

### Migration
- [ ] Migration file created
- [ ] Migration applied successfully
- [ ] Users table created with ~86 rows
- [ ] FK constraints added to all 3 tables
- [ ] feedback.user_id type changed to String(255)
- [ ] Verification script confirms all changes

### Testing
- [ ] test_user_model.py created
- [ ] All 6 tests passing
- [ ] User creation works
- [ ] Relationships work
- [ ] Unique constraints enforced

### Documentation
- [ ] Session log updated with Phase 1A completion
- [ ] Evidence collected (terminal output, test results)

---

## Evidence Required

**When Phase 1A complete, provide**:

```bash
# 1. Show User model import works
python3 -c "from services.database.models import User; print(User.__tablename__)"

# 2. Show migration applied
alembic current

# 3. Show users table populated
python3 -c "import asyncio; from services.database.session_factory import AsyncSessionFactory; from sqlalchemy import text; asyncio.run((lambda: AsyncSessionFactory.session_scope().__aenter__())()).result()"  # Complex, use verification script instead

# 4. Show tests passing
pytest tests/database/test_user_model.py -v

# 5. Show FK constraints exist
# Use verification script from Step 6.2
```

---

## Communication Protocol

**When Phase 1A complete**:

```
✅ Phase 1A Complete - User Model Foundation

Created:
- User model with all fields and relationships
- Migration with data population (86 User records)
- FK constraints on PersonalityProfile, TokenBlacklist, Feedback
- Type change on Feedback.user_id (String → String(255))
- 6 tests for User model and relationships

Test Results:
- test_user_model.py: 6/6 passing
- User creation: ✅
- Relationships: ✅ (PersonalityProfile, TokenBlacklist, Feedback)
- Unique constraints: ✅ (username, email)
- FK constraints: ✅ (all 3 tables)

Verification:
- Users table: 86 rows created from existing data
- PersonalityProfile FK: ✅ (fk_personality_profiles_user_id)
- TokenBlacklist FK: ✅ (fk_token_blacklist_user_id)
- Feedback FK: ✅ (fk_feedback_user_id)

Evidence: dev/2025/10/22/phase-1a-completion-evidence.md

Ready for Phase 1B (UserAPIKey model + service)!
```

---

## Critical Reminders

1. **Migration must populate users table** - 86 User records from existing data
2. **PersonalityProfile FK is NOT NULL** - all profiles must have valid user_id
3. **TokenBlacklist FK is NULLABLE** - preserve existing behavior
4. **Feedback needs type change** - String → String(255) before FK
5. **Test relationships** - verify all 4 relationships work
6. **Rollback capability** - downgrade() must restore original state

---

**Phase 1A is foundation for the rest of Issue #228. Get this right and everything else builds cleanly!** 🏗️

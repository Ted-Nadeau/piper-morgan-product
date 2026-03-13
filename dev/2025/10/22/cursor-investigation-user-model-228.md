# Cursor Investigation Prompt: User Model Integration Analysis

**Agent**: Cursor (Chief Architect)
**Issue**: #228 CORE-USERS-API (Phase 1A preparation)
**Task**: Investigate existing models for User model integration
**Date**: October 22, 2025, 7:05 AM
**Duration**: 15-20 minutes

---

## Mission

**Goal**: Document exact structure of existing models that will integrate with new User model, so Code can create perfect migration on first try.

**Your job is investigation ONLY**:
- ✅ Document exact model structures
- ✅ Identify all constraints and indexes
- ✅ Check for existing data
- ✅ Note migration patterns from recent work
- ✅ Provide complete specifications
- ❌ Do NOT implement anything

---

## Context

**Decision Made**: Create full User model (not string user_id pattern)

**Why Investigation Needed**:
- Code needs to update 3 existing models to reference User
- Need exact field lists, constraints, relationships
- Need to understand data migration requirements
- Need to follow project's migration conventions
- Want to get FK migrations right first time (no constraint errors!)

**Models to Investigate**:
1. PersonalityProfile (has user_id String(255), unique)
2. TokenBlacklist (has user_id String(255), nullable, indexed)
3. Feedback (has user_id String, indexed)

---

## Phase 1: PersonalityProfile Model (5 min)

### 1.1 View Complete Model

```bash
# View PersonalityProfile model
cat services/database/models.py | grep -A 50 "class PersonalityProfile"
```

**Document**:
- All fields (name, type, nullable, defaults)
- All indexes
- All constraints (unique, check, etc.)
- All relationships (if any exist)
- Table name

### 1.2 Check Current Constraints

```bash
# Look for unique constraints on PersonalityProfile
grep -A 30 "class PersonalityProfile" services/database/models.py | grep -E "unique|Unique|__table_args__"
```

**Critical Questions**:
- Is user_id unique by itself?
- Or is it part of a composite unique constraint?
- Are there other unique constraints we need to preserve?

### 1.3 Check for Existing Relationships

```bash
# Check if PersonalityProfile has relationships already
grep -A 30 "class PersonalityProfile" services/database/models.py | grep -i "relationship"
```

**Document**:
- Does it have any relationships to other models?
- Do we need to preserve these?

### 1.4 Check for Existing Data

```bash
# Check if table has data
cd /Users/xian/Development/piper-morgan
python3 << 'EOF'
import asyncio
from services.database.session_factory import AsyncSessionFactory
from sqlalchemy import text

async def check_data():
    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM personality_profiles"))
        count = result.scalar()
        print(f"PersonalityProfile rows: {count}")

        if count > 0:
            result = await session.execute(text("SELECT DISTINCT user_id FROM personality_profiles LIMIT 5"))
            user_ids = result.fetchall()
            print(f"Sample user_ids: {[row[0] for row in user_ids]}")

asyncio.run(check_data())
EOF
```

**Document**:
- How many rows exist?
- What do user_id values look like?
- Are they consistent format?

---

## Phase 2: TokenBlacklist Model (5 min)

### 2.1 View Complete Model

```bash
# View TokenBlacklist model
cat services/database/models.py | grep -A 50 "class TokenBlacklist"
```

**Document**:
- All fields (name, type, nullable, defaults)
- All indexes
- All constraints
- All relationships
- Table name

### 2.2 Check Current Indexes

```bash
# Check TokenBlacklist indexes
grep -A 30 "class TokenBlacklist" services/database/models.py | grep -E "index|Index|__table_args__"
```

**Document**:
- What indexes exist on user_id?
- Are there composite indexes?
- Index names and types

### 2.3 Check Nullable Status

**Critical**: TokenBlacklist.user_id is nullable (from earlier investigation)

**Verify**:
```bash
grep -A 5 "user_id.*Column" services/database/models.py | grep -A 3 "TokenBlacklist" -B 2
```

**Document**:
- Confirm user_id is nullable
- This affects FK constraint (nullable FK is allowed)

### 2.4 Check for Existing Data

```bash
# Check if table has data
python3 << 'EOF'
import asyncio
from services.database.session_factory import AsyncSessionFactory
from sqlalchemy import text

async def check_data():
    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM token_blacklist"))
        count = result.scalar()
        print(f"TokenBlacklist rows: {count}")

        if count > 0:
            result = await session.execute(text("SELECT COUNT(*) FROM token_blacklist WHERE user_id IS NOT NULL"))
            non_null = result.scalar()
            print(f"Rows with user_id: {non_null}")

asyncio.run(check_data())
EOF
```

**Document**:
- How many rows?
- How many have user_id populated?
- Can FK be nullable?

---

## Phase 3: Feedback Model (5 min)

### 3.1 View Complete Model

```bash
# View Feedback model
cat services/database/models.py | grep -A 50 "class Feedback"
```

**Document**:
- All fields (name, type, nullable, defaults)
- All indexes
- All constraints
- All relationships
- Table name

### 3.2 Check User ID Type

**Note**: Earlier investigation showed "String" not "String(255)"

```bash
# Confirm exact type
grep -A 20 "class Feedback" services/database/models.py | grep "user_id"
```

**Document**:
- Exact type (String vs String(255))
- Is it indexed?
- Is it nullable?

### 3.3 Check for Existing Data

```bash
# Check if table has data
python3 << 'EOF'
import asyncio
from services.database.session_factory import AsyncSessionFactory
from sqlalchemy import text

async def check_data():
    async with AsyncSessionFactory.session_scope() as session:
        # Check if feedback table exists
        try:
            result = await session.execute(text("SELECT COUNT(*) FROM feedback"))
            count = result.scalar()
            print(f"Feedback rows: {count}")
        except Exception as e:
            print(f"Feedback table might not exist: {e}")

asyncio.run(check_data())
EOF
```

**Document**:
- Does table exist?
- How many rows?
- Will FK be nullable or not null?

---

## Phase 4: Recent Migration Patterns (5 min)

### 4.1 Examine Recent JWT Migration

```bash
# Look at recent migration structure (from #227)
cat alembic/versions/*token_blacklist*.py | head -100
```

**Document**:
- How are tables created?
- How are indexes created?
- How are FK constraints named?
- What patterns are used?

### 4.2 Check Migration Naming Convention

```bash
# List recent migrations
ls -la alembic/versions/ | tail -5
```

**Document**:
- Naming pattern for migrations
- Timestamp format
- Description format

### 4.3 Check Alembic Configuration

```bash
# Check if there are any special Alembic settings
cat alembic/env.py | grep -A 10 "target_metadata"
```

**Document**:
- How models are imported
- Any special configuration

---

## Discovery Report Format

Create: `dev/2025/10/22/user-model-integration-analysis.md`

### Report Structure

```markdown
# User Model Integration Analysis

**Date**: October 22, 2025, 7:05 AM
**Agent**: Cursor (Chief Architect)
**Issue**: #228 Phase 1A Preparation
**Duration**: [X] minutes

---

## Executive Summary

**Models to Update**: 3 (PersonalityProfile, TokenBlacklist, Feedback)
**Existing Data**: [X rows across tables]
**Migration Complexity**: [Low/Medium/High]
**FK Strategy**: [Nullable/Not Null for each model]

**Key Finding**: [One sentence summary]

---

## PersonalityProfile Model

### Current Structure

```python
class PersonalityProfile(Base):
    __tablename__ = "personality_profiles"

    # PASTE COMPLETE MODEL HERE
    # Include all fields, constraints, relationships
```

**Table Name**: `personality_profiles`

**Fields**:
| Field Name | Type | Nullable | Default | Notes |
|------------|------|----------|---------|-------|
| id | [type] | [Y/N] | [default] | [notes] |
| user_id | String(255) | No | None | Currently unique |
| [field] | [type] | [Y/N] | [default] | [notes] |
| ... | ... | ... | ... | ... |

**Indexes**:
- [List all indexes with names and columns]

**Constraints**:
- [List all constraints - unique, check, etc.]
- **CRITICAL**: Document the unique constraint on user_id exactly

**Relationships**:
- [List any existing relationships]

**Existing Data**:
- Row count: [X]
- Sample user_ids: [list]
- Data pattern: [consistent/varied/etc]

### Required Changes for User FK

**Add to Model**:
```python
# Add FK column (or modify existing user_id)
user_id = Column(String(255), ForeignKey("users.id"), nullable=False, index=True)

# Add relationship
user = relationship("User", back_populates="personality_profiles")
```

**Migration Considerations**:
- Need to create User records first
- Need to ensure all user_id values exist in users table
- [List any other considerations]

---

## TokenBlacklist Model

### Current Structure

```python
class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    # PASTE COMPLETE MODEL HERE
```

**Table Name**: `token_blacklist`

**Fields**:
| Field Name | Type | Nullable | Default | Notes |
|------------|------|----------|---------|-------|
| id | [type] | [Y/N] | [default] | [notes] |
| user_id | String(255) | **Yes** | None | Nullable! |
| [field] | [type] | [Y/N] | [default] | [notes] |
| ... | ... | ... | ... | ... |

**Indexes**:
- [List all indexes]

**Constraints**:
- [List constraints]

**Relationships**:
- [List any existing relationships]

**Existing Data**:
- Row count: [X]
- Rows with user_id: [Y]
- Rows without user_id: [Z]

### Required Changes for User FK

**Add to Model**:
```python
# Modify user_id column
user_id = Column(String(255), ForeignKey("users.id"), nullable=True, index=True)

# Add relationship
user = relationship("User", back_populates="blacklisted_tokens")
```

**Migration Considerations**:
- FK can be nullable (existing behavior)
- Rows without user_id can remain (no FK constraint violation)
- [List any other considerations]

---

## Feedback Model

### Current Structure

```python
class Feedback(Base):
    __tablename__ = "feedback"

    # PASTE COMPLETE MODEL HERE
```

**Table Name**: `feedback`

**Fields**:
| Field Name | Type | Nullable | Default | Notes |
|------------|------|----------|---------|-------|
| id | [type] | [Y/N] | [default] | [notes] |
| user_id | String | [Y/N] | [default] | Note: String not String(255) |
| [field] | [type] | [Y/N] | [default] | [notes] |
| ... | ... | ... | ... | ... |

**Indexes**:
- [List indexes]

**Constraints**:
- [List constraints]

**Relationships**:
- [List relationships]

**Existing Data**:
- Row count: [X] (or table doesn't exist)

### Required Changes for User FK

**Add to Model**:
```python
# Modify user_id column - CHANGE TYPE to String(255) for consistency
user_id = Column(String(255), ForeignKey("users.id"), nullable=[True/False], index=True)

# Add relationship
user = relationship("User", back_populates="feedback")
```

**Migration Considerations**:
- May need to alter column type String → String(255)
- [List any other considerations]

---

## Migration Strategy

### From Recent JWT Migration

**Pattern Observed**:
```python
# PASTE RELEVANT PARTS OF RECENT MIGRATION
# Show how tables/indexes/constraints are created
```

**Naming Conventions**:
- Migration files: `[timestamp]_[description]_issue_[number].py`
- FK names: [pattern]
- Index names: [pattern]

### Recommended Migration Order

**Step 1: Create users table**
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    -- other fields
)
```

**Step 2: Populate users table**
```python
# Get all distinct user_id values from existing tables
# Insert them as User records
```

**Step 3: Add FK to personality_profiles**
```sql
ALTER TABLE personality_profiles
ADD CONSTRAINT fk_personality_profiles_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
```

**Step 4: Add FK to token_blacklist**
```sql
ALTER TABLE token_blacklist
ADD CONSTRAINT fk_token_blacklist_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
```

**Step 5: Add FK to feedback** (if exists)
```sql
-- May need to alter column type first
ALTER TABLE feedback ALTER COLUMN user_id TYPE VARCHAR(255)

ALTER TABLE feedback
ADD CONSTRAINT fk_feedback_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
```

### Data Migration Requirements

**Existing user_id Values**:
- PersonalityProfile: [X values listed]
- TokenBlacklist: [Y values listed]
- Feedback: [Z values listed]

**Strategy**:
```python
# In migration upgrade():
# 1. Get all unique user_id values
# 2. Create User records for each
# 3. Add FK constraints
```

**Rollback Strategy**:
```python
# In migration downgrade():
# 1. Drop FK constraints
# 2. Drop users table
# 3. Restore original state
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
    personality_profiles = relationship("PersonalityProfile", back_populates="user")
    api_keys = relationship("UserAPIKey", back_populates="user", cascade="all, delete-orphan")
    blacklisted_tokens = relationship("TokenBlacklist", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")
    # audit_logs = relationship("AuditLog", back_populates="user")  # For Issue #230

    # Indexes
    __table_args__ = (
        Index("idx_users_username", "username"),
        Index("idx_users_email", "email"),
        Index("idx_users_active", "is_active"),
    )
```

**Why This Structure**:
- id as String(255) matches existing pattern
- Includes auth fields for JWT (#227)
- Includes relationships to all 4 models
- Includes audit relationship for #230
- Standard timestamps
- Proper indexes

---

## Testing Patterns

### From Existing Tests

**Pattern for model tests**:
```python
# PASTE EXAMPLE FROM EXISTING MODEL TESTS
```

**Pattern for relationship tests**:
```python
# PASTE EXAMPLE IF EXISTS
```

---

## Summary for Code

**What Code Needs to Create**:

1. **User Model**: [Use specification above]
2. **Update PersonalityProfile**: [Specific changes documented above]
3. **Update TokenBlacklist**: [Specific changes documented above]
4. **Update Feedback**: [Specific changes documented above]
5. **Migration**: [Follow order and strategy documented above]
6. **Tests**: [Follow patterns documented above]

**Critical Details**:
- PersonalityProfile.user_id: [unique constraint details]
- TokenBlacklist.user_id: Nullable FK (existing behavior)
- Feedback.user_id: May need type change String → String(255)
- Existing data: [X user_id values to migrate]
- Migration naming: `[timestamp]_add_user_model_issue_228.py`

---

## Evidence Checklist

Before finishing investigation, verify:

- [x] PersonalityProfile complete structure documented
- [x] TokenBlacklist complete structure documented
- [x] Feedback complete structure documented
- [x] All constraints documented
- [x] All indexes documented
- [x] All relationships documented
- [x] Existing data counts obtained
- [x] Recent migration patterns documented
- [x] Migration strategy defined
- [x] Data migration plan created
- [x] User model specification complete

---

**Investigation complete. Lead Dev can now write Phase 1A guidance with 95%+ confidence.**
```

---

## Critical Notes

**For Cursor**:

1. **Be Thorough**: Code needs EXACT specifications
2. **Show Code**: Paste actual model code, don't summarize
3. **Check Data**: Run the Python scripts to check for existing rows
4. **Document Patterns**: Look at recent migration to see how FKs are added
5. **Note Everything**: All constraints, indexes, relationships matter

**Key Outputs**:
- Complete model structures (copy/paste from code)
- All constraints and indexes (exact names)
- Existing data status (row counts, sample values)
- Migration patterns (from recent work)
- Clear data migration strategy

**Time Management**:
- Don't rush - accuracy matters
- 15-20 minutes is fine
- Complete investigation better than fast investigation

---

**Ready to investigate! Start with Phase 1 and work systematically through all phases.**

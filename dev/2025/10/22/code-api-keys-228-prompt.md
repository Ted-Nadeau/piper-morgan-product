# Implementation Prompt: CORE-USERS-API - Multi-User API Key Management

**Agent**: Claude Code (Programmer)
**Issue**: #228 CORE-USERS-API
**Task**: Add multi-user key isolation and rotation to existing world-class infrastructure
**Date**: October 22, 2025, 6:35 AM
**Estimated Effort**: Medium (9 hours)

---

## 🎉 AMAZING NEWS: Infrastructure is 85% Complete!

**Cursor's investigation revealed**:
- ✅ KeychainService (234 lines) - OS keychain integration working!
- ✅ LLMConfigService (640 lines) - Keychain-first pattern with validation!
- ✅ 4-provider LLM support (OpenAI, Anthropic, Gemini, Perplexity)
- ✅ Migration tools (scripts/migrate_keys_to_keychain.py)
- ✅ GitHub, Notion, Slack integrations
- ✅ Real API validation (actually calls provider APIs!)

**What you need to add**:
- ❌ Multi-user key isolation (4 hours)
- ❌ Key rotation system (3 hours)
- ❌ Documentation & testing (2 hours)

**Total work**: ~9 hours instead of 16-20 hours!

---

## Essential Context

Read Cursor's complete investigation:
**File**: `dev/2025/10/22/api-key-management-analysis.md`

```bash
cat dev/2025/10/22/api-key-management-analysis.md
```

**Key findings**:
- KeychainService in `services/infrastructure/keychain_service.py` (234 lines)
- LLMConfigService in `services/config/llm_config_service.py` (640 lines)
- Migration script in `scripts/migrate_keys_to_keychain.py`
- All major dependencies installed (keyring==25.6.0, cryptography==45.0.4)

---

## Session Log

Create: `dev/2025/10/22/2025-10-22-HHMM-prog-code-log.md`

Use standard session log template with:
- Issue #228 context
- Reference to Cursor's investigation
- Phase-by-phase progress tracking

---

## Phase 0: Verify Existing Infrastructure (15 min)

### Confirm KeychainService Status

```bash
# Verify KeychainService exists
cat services/infrastructure/keychain_service.py | head -50

# Check LLMConfigService
cat services/config/llm_config_service.py | head -50

# Verify dependencies
pip list | grep -E "keyring|cryptography"

# Check migration script
ls -la scripts/migrate_keys_to_keychain.py
```

### Test Current Key Storage

```bash
# Start Python shell
cd /Users/xian/Development/piper-morgan
python3 << 'EOF'
from services.infrastructure.keychain_service import KeychainService

# Test keychain access
keychain = KeychainService()
print("KeychainService initialized successfully")

# Check backend
import keyring
backend = keyring.get_keyring()
print(f"Keyring backend: {backend}")
EOF
```

**Success criteria**:
- [ ] KeychainService loads without errors
- [ ] LLMConfigService exists and working
- [ ] keyring backend available
- [ ] Migration script present

**STOP if**: Any infrastructure check fails - report to PM

---

## Phase 1: Multi-User Key Isolation (4 hours)

### 1.1 Create UserAPIKey Database Model (45 min)

**File**: `services/database/models.py`

**Add new model** (after User model):

```python
class UserAPIKey(Base):
    """
    User-specific API keys stored securely in OS keychain.

    This model stores metadata about keys; actual keys are in OS keychain
    with references using format: "piper_{user_id}_{provider}"
    """
    __tablename__ = "user_api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False, index=True)
    provider = Column(String(50), nullable=False)  # openai, anthropic, github, etc
    key_reference = Column(String(500), nullable=False)  # keychain identifier

    # Key metadata
    is_active = Column(Boolean, default=True, nullable=False)
    is_validated = Column(Boolean, default=False)
    last_validated_at = Column(DateTime, nullable=True)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=True)

    # Rotation support
    previous_key_reference = Column(String(500), nullable=True)
    rotated_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="api_keys")

    # Constraints
    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_user_provider"),
        Index("idx_user_api_keys_user_id", "user_id"),
        Index("idx_user_api_keys_provider", "provider"),
        Index("idx_user_api_keys_active", "is_active"),
    )

    def __repr__(self):
        return f"<UserAPIKey(user_id={self.user_id}, provider={self.provider}, active={self.is_active})>"
```

**Update User model**:

```python
# In User class, add relationship
class User(Base):
    # ... existing fields ...

    # Add this relationship
    api_keys = relationship(
        "UserAPIKey",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select"
    )
```

### 1.2 Create Database Migration (30 min)

```bash
# Generate migration
cd /Users/xian/Development/piper-morgan
alembic revision --autogenerate -m "add_user_api_keys_table_issue_228"

# Review migration file
# Should be in: alembic/versions/XXXXX_add_user_api_keys_table_issue_228.py
```

**Verify migration includes**:
- user_api_keys table creation
- All columns with correct types
- Foreign key to users table
- Unique constraint on (user_id, provider)
- All indexes

**Apply migration**:
```bash
alembic upgrade head
```

**Test migration**:
```bash
# Verify table exists
python3 << 'EOF'
from services.database.session_factory import AsyncSessionFactory
from services.database.models import UserAPIKey
import asyncio

async def test():
    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute("SELECT COUNT(*) FROM user_api_keys")
        count = result.scalar()
        print(f"user_api_keys table exists, rows: {count}")

asyncio.run(test())
EOF
```

**Success criteria**:
- [ ] Migration generated successfully
- [ ] Migration applied (alembic upgrade head)
- [ ] user_api_keys table exists in database
- [ ] All constraints and indexes created

### 1.3 Create UserAPIKeyService (1.5 hours)

**File**: `services/security/user_api_key_service.py` (CREATE)

```python
"""
User API Key Management Service
Handles per-user API keys with OS keychain storage
"""
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from services.database.models import UserAPIKey
from services.infrastructure.keychain_service import KeychainService
from services.config.llm_config_service import LLMConfigService

logger = logging.getLogger(__name__)


class UserAPIKeyService:
    """Service for managing user-specific API keys with keychain storage"""

    def __init__(self, keychain_service: Optional[KeychainService] = None):
        """
        Initialize user API key service.

        Args:
            keychain_service: Optional keychain service for testing
        """
        self._keychain = keychain_service or KeychainService()
        self._llm_config = LLMConfigService()

    async def store_user_key(
        self,
        session: AsyncSession,
        user_id: str,
        provider: str,
        api_key: str,
        validate: bool = True
    ) -> UserAPIKey:
        """
        Store API key for user in keychain with database metadata.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider (openai, anthropic, github, etc)
            api_key: API key to store
            validate: Whether to validate key with provider API

        Returns:
            UserAPIKey database record

        Raises:
            ValueError: If validation fails or key invalid
        """
        logger.info(f"Storing API key for user {user_id}, provider {provider}")

        # Validate key if requested
        is_valid = False
        if validate:
            try:
                is_valid = await self._llm_config.validate_api_key(provider, api_key)
                if not is_valid:
                    raise ValueError(f"API key validation failed for {provider}")
                logger.info(f"API key validated successfully for {provider}")
            except Exception as e:
                logger.error(f"API key validation error: {e}")
                raise ValueError(f"Failed to validate API key: {e}")

        # Generate keychain reference
        key_reference = self._generate_key_reference(user_id, provider)

        # Store in keychain
        try:
            self._keychain.store_api_key(provider, api_key, username=user_id)
            logger.info(f"Stored key in keychain: {key_reference}")
        except Exception as e:
            logger.error(f"Failed to store key in keychain: {e}")
            raise ValueError(f"Keychain storage failed: {e}")

        # Check if key record exists
        result = await session.execute(
            select(UserAPIKey).where(
                and_(
                    UserAPIKey.user_id == user_id,
                    UserAPIKey.provider == provider
                )
            )
        )
        existing_key = result.scalar_one_or_none()

        if existing_key:
            # Update existing record
            existing_key.key_reference = key_reference
            existing_key.is_active = True
            existing_key.is_validated = is_valid
            existing_key.last_validated_at = datetime.utcnow() if is_valid else None
            existing_key.updated_at = datetime.utcnow()
            await session.commit()
            logger.info(f"Updated existing key record for {user_id}/{provider}")
            return existing_key
        else:
            # Create new record
            user_key = UserAPIKey(
                user_id=user_id,
                provider=provider,
                key_reference=key_reference,
                is_active=True,
                is_validated=is_valid,
                last_validated_at=datetime.utcnow() if is_valid else None,
                created_by=user_id
            )
            session.add(user_key)
            await session.commit()
            logger.info(f"Created new key record for {user_id}/{provider}")
            return user_key

    async def retrieve_user_key(
        self,
        session: AsyncSession,
        user_id: str,
        provider: str
    ) -> Optional[str]:
        """
        Retrieve API key for user from keychain.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider

        Returns:
            API key if found, None otherwise
        """
        # Check database for key metadata
        result = await session.execute(
            select(UserAPIKey).where(
                and_(
                    UserAPIKey.user_id == user_id,
                    UserAPIKey.provider == provider,
                    UserAPIKey.is_active == True
                )
            )
        )
        user_key = result.scalar_one_or_none()

        if not user_key:
            logger.debug(f"No key record found for {user_id}/{provider}")
            return None

        # Retrieve from keychain
        try:
            api_key = self._keychain.get_api_key(provider, username=user_id)
            if api_key:
                logger.debug(f"Retrieved key from keychain for {user_id}/{provider}")
                return api_key
            else:
                logger.warning(f"Key reference exists but keychain returned None: {user_id}/{provider}")
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve key from keychain: {e}")
            return None

    async def delete_user_key(
        self,
        session: AsyncSession,
        user_id: str,
        provider: str
    ) -> bool:
        """
        Delete API key for user from keychain and database.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider

        Returns:
            True if deleted, False if not found
        """
        logger.info(f"Deleting API key for {user_id}/{provider}")

        # Get database record
        result = await session.execute(
            select(UserAPIKey).where(
                and_(
                    UserAPIKey.user_id == user_id,
                    UserAPIKey.provider == provider
                )
            )
        )
        user_key = result.scalar_one_or_none()

        if not user_key:
            logger.debug(f"No key record to delete for {user_id}/{provider}")
            return False

        # Delete from keychain
        try:
            self._keychain.delete_api_key(provider, username=user_id)
            logger.info(f"Deleted key from keychain: {user_id}/{provider}")
        except Exception as e:
            logger.warning(f"Failed to delete from keychain (continuing): {e}")

        # Delete database record
        await session.delete(user_key)
        await session.commit()
        logger.info(f"Deleted key database record for {user_id}/{provider}")

        return True

    async def list_user_keys(
        self,
        session: AsyncSession,
        user_id: str,
        active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """
        List all API keys for user.

        Args:
            session: Database session
            user_id: User identifier
            active_only: Only return active keys

        Returns:
            List of key metadata (no actual keys)
        """
        query = select(UserAPIKey).where(UserAPIKey.user_id == user_id)

        if active_only:
            query = query.where(UserAPIKey.is_active == True)

        result = await session.execute(query)
        user_keys = result.scalars().all()

        return [
            {
                "provider": key.provider,
                "is_active": key.is_active,
                "is_validated": key.is_validated,
                "last_validated_at": key.last_validated_at.isoformat() if key.last_validated_at else None,
                "created_at": key.created_at.isoformat(),
                "rotated_at": key.rotated_at.isoformat() if key.rotated_at else None,
            }
            for key in user_keys
        ]

    async def validate_user_key(
        self,
        session: AsyncSession,
        user_id: str,
        provider: str
    ) -> bool:
        """
        Validate user's API key by testing with provider API.

        Args:
            session: Database session
            user_id: User identifier
            provider: Service provider

        Returns:
            True if valid, False otherwise
        """
        # Retrieve key
        api_key = await self.retrieve_user_key(session, user_id, provider)
        if not api_key:
            logger.warning(f"No key found to validate for {user_id}/{provider}")
            return False

        # Validate with provider
        try:
            is_valid = await self._llm_config.validate_api_key(provider, api_key)

            # Update validation status in database
            result = await session.execute(
                select(UserAPIKey).where(
                    and_(
                        UserAPIKey.user_id == user_id,
                        UserAPIKey.provider == provider
                    )
                )
            )
            user_key = result.scalar_one_or_none()

            if user_key:
                user_key.is_validated = is_valid
                user_key.last_validated_at = datetime.utcnow()
                await session.commit()

            return is_valid

        except Exception as e:
            logger.error(f"Validation failed for {user_id}/{provider}: {e}")
            return False

    def _generate_key_reference(self, user_id: str, provider: str) -> str:
        """Generate keychain reference identifier"""
        return f"piper_{user_id}_{provider}"
```

### 1.4 Update KeychainService for Multi-User (30 min)

**File**: `services/infrastructure/keychain_service.py`

**Modify methods to support username parameter**:

```python
# Find store_api_key method and ensure it accepts username
def store_api_key(self, provider: str, key: str, username: Optional[str] = None) -> bool:
    """
    Store API key in OS keychain.

    Args:
        provider: Service provider name
        key: API key to store
        username: Optional username for multi-user support (uses provider as default)
    """
    account = username if username else provider
    # ... rest of implementation

# Find get_api_key method and ensure it accepts username
def get_api_key(self, provider: str, username: Optional[str] = None) -> Optional[str]:
    """
    Retrieve API key from OS keychain.

    Args:
        provider: Service provider name
        username: Optional username for multi-user support (uses provider as default)
    """
    account = username if username else provider
    # ... rest of implementation

# Find delete_api_key method and ensure it accepts username
def delete_api_key(self, provider: str, username: Optional[str] = None) -> bool:
    """
    Delete API key from OS keychain.

    Args:
        provider: Service provider name
        username: Optional username for multi-user support (uses provider as default)
    """
    account = username if username else provider
    # ... rest of implementation
```

**Note**: KeychainService might already support this! Check first before modifying.

### 1.5 Test Multi-User Key Isolation (45 min)

**File**: `tests/security/test_user_api_key_service.py` (CREATE)

```python
"""
Tests for UserAPIKeyService - Multi-user key isolation
"""
import pytest
from datetime import datetime
from services.security.user_api_key_service import UserAPIKeyService
from services.database.models import UserAPIKey, User
from services.database.session_factory import AsyncSessionFactory


@pytest.mark.asyncio
async def test_store_user_key():
    """Test storing user API key"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Store key (skip validation for test)
        user_key = await service.store_user_key(
            session,
            user_id="test_user_1",
            provider="openai",
            api_key="sk-test-key-123",
            validate=False
        )

        assert user_key.user_id == "test_user_1"
        assert user_key.provider == "openai"
        assert user_key.is_active is True


@pytest.mark.asyncio
async def test_retrieve_user_key():
    """Test retrieving user API key"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Store key
        await service.store_user_key(
            session,
            user_id="test_user_2",
            provider="anthropic",
            api_key="sk-ant-test-key-456",
            validate=False
        )

        # Retrieve key
        retrieved_key = await service.retrieve_user_key(
            session,
            user_id="test_user_2",
            provider="anthropic"
        )

        assert retrieved_key == "sk-ant-test-key-456"


@pytest.mark.asyncio
async def test_multi_user_isolation():
    """Test that users' keys are isolated from each other"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Store keys for two different users
        await service.store_user_key(
            session,
            user_id="alice",
            provider="openai",
            api_key="alice-key",
            validate=False
        )

        await service.store_user_key(
            session,
            user_id="bob",
            provider="openai",
            api_key="bob-key",
            validate=False
        )

        # Verify Alice gets her key
        alice_key = await service.retrieve_user_key(session, "alice", "openai")
        assert alice_key == "alice-key"

        # Verify Bob gets his key
        bob_key = await service.retrieve_user_key(session, "bob", "openai")
        assert bob_key == "bob-key"

        # Verify they're different
        assert alice_key != bob_key


@pytest.mark.asyncio
async def test_delete_user_key():
    """Test deleting user API key"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Store and delete key
        await service.store_user_key(
            session,
            user_id="test_user_3",
            provider="github",
            api_key="ghp_test",
            validate=False
        )

        deleted = await service.delete_user_key(session, "test_user_3", "github")
        assert deleted is True

        # Verify key is gone
        key = await service.retrieve_user_key(session, "test_user_3", "github")
        assert key is None


@pytest.mark.asyncio
async def test_list_user_keys():
    """Test listing all keys for a user"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Store multiple keys for one user
        await service.store_user_key(session, "test_user_4", "openai", "key1", validate=False)
        await service.store_user_key(session, "test_user_4", "anthropic", "key2", validate=False)
        await service.store_user_key(session, "test_user_4", "github", "key3", validate=False)

        # List keys
        keys = await service.list_user_keys(session, "test_user_4")

        assert len(keys) == 3
        providers = {k["provider"] for k in keys}
        assert providers == {"openai", "anthropic", "github"}
```

**Run tests**:
```bash
pytest tests/security/test_user_api_key_service.py -v
```

**Success criteria**:
- [ ] All 5 tests passing
- [ ] Multi-user isolation verified
- [ ] Keys stored in keychain with user context
- [ ] Retrieval works per-user
- [ ] Deletion works per-user

**Evidence required**:
```bash
# Show test results
[paste pytest output]
```

---

## Phase 2: Key Rotation System (3 hours)

### 2.1 Add Rotation Methods to UserAPIKeyService (1.5 hours)

**File**: `services/security/user_api_key_service.py` (MODIFY)

**Add rotation method**:

```python
async def rotate_user_key(
    self,
    session: AsyncSession,
    user_id: str,
    provider: str,
    new_api_key: str,
    validate: bool = True
) -> UserAPIKey:
    """
    Rotate user's API key with zero-downtime.

    Process:
    1. Validate new key
    2. Store new key in keychain
    3. Update database with new key reference
    4. Mark old key for cleanup
    5. Delete old key from keychain after grace period

    Args:
        session: Database session
        user_id: User identifier
        provider: Service provider
        new_api_key: New API key
        validate: Whether to validate new key

    Returns:
        Updated UserAPIKey record

    Raises:
        ValueError: If validation fails or rotation error
    """
    logger.info(f"Rotating API key for {user_id}/{provider}")

    # Get existing key record
    result = await session.execute(
        select(UserAPIKey).where(
            and_(
                UserAPIKey.user_id == user_id,
                UserAPIKey.provider == provider,
                UserAPIKey.is_active == True
            )
        )
    )
    existing_key = result.scalar_one_or_none()

    if not existing_key:
        logger.warning(f"No existing key found for {user_id}/{provider}, treating as new key")
        return await self.store_user_key(session, user_id, provider, new_api_key, validate)

    # Validate new key if requested
    if validate:
        try:
            is_valid = await self._llm_config.validate_api_key(provider, new_api_key)
            if not is_valid:
                raise ValueError(f"New API key validation failed for {provider}")
            logger.info(f"New API key validated successfully for {provider}")
        except Exception as e:
            logger.error(f"New API key validation error: {e}")
            raise ValueError(f"Failed to validate new API key: {e}")

    # Save old key reference for cleanup
    old_key_reference = existing_key.key_reference

    # Generate new key reference
    new_key_reference = self._generate_key_reference(user_id, provider, version="v2")

    # Store new key in keychain
    try:
        self._keychain.store_api_key(provider, new_api_key, username=f"{user_id}_v2")
        logger.info(f"Stored new key in keychain: {new_key_reference}")
    except Exception as e:
        logger.error(f"Failed to store new key in keychain: {e}")
        raise ValueError(f"Keychain storage failed: {e}")

    # Update database record
    existing_key.previous_key_reference = old_key_reference
    existing_key.key_reference = new_key_reference
    existing_key.rotated_at = datetime.utcnow()
    existing_key.is_validated = validate
    existing_key.last_validated_at = datetime.utcnow() if validate else None
    existing_key.updated_at = datetime.utcnow()

    await session.commit()

    # Delete old key from keychain (immediate cleanup)
    try:
        self._keychain.delete_api_key(provider, username=user_id)
        logger.info(f"Deleted old key from keychain: {old_key_reference}")
    except Exception as e:
        logger.warning(f"Failed to delete old key from keychain: {e}")

    logger.info(f"Key rotation completed successfully for {user_id}/{provider}")
    return existing_key

def _generate_key_reference(
    self,
    user_id: str,
    provider: str,
    version: str = "v1"
) -> str:
    """Generate keychain reference identifier with version"""
    return f"piper_{user_id}_{provider}_{version}"
```

### 2.2 Add Rotation API Endpoint (45 min)

**File**: `web/api/routes/api_keys.py` (CREATE)

```python
"""
API Key Management Routes
User-specific API key operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any

from services.security.user_api_key_service import UserAPIKeyService
from services.database.session_factory import AsyncSessionFactory
from web.api.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/keys", tags=["api-keys"])


class StoreKeyRequest(BaseModel):
    provider: str
    api_key: str
    validate: bool = True


class RotateKeyRequest(BaseModel):
    provider: str
    new_api_key: str
    validate: bool = True


@router.post("/store")
async def store_api_key(
    request: StoreKeyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Store API key for current user"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        try:
            user_key = await service.store_user_key(
                session,
                user_id=current_user["user_id"],
                provider=request.provider,
                api_key=request.api_key,
                validate=request.validate
            )

            return {
                "message": f"API key stored successfully for {request.provider}",
                "provider": user_key.provider,
                "is_validated": user_key.is_validated,
                "created_at": user_key.created_at.isoformat()
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/rotate")
async def rotate_api_key(
    request: RotateKeyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Rotate API key for current user"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        try:
            user_key = await service.rotate_user_key(
                session,
                user_id=current_user["user_id"],
                provider=request.provider,
                new_api_key=request.new_api_key,
                validate=request.validate
            )

            return {
                "message": f"API key rotated successfully for {request.provider}",
                "provider": user_key.provider,
                "rotated_at": user_key.rotated_at.isoformat() if user_key.rotated_at else None,
                "is_validated": user_key.is_validated
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/list")
async def list_api_keys(current_user: dict = Depends(get_current_user)):
    """List all API keys for current user (metadata only, no actual keys)"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        keys = await service.list_user_keys(session, current_user["user_id"])
        return {"keys": keys}


@router.delete("/{provider}")
async def delete_api_key(
    provider: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete API key for current user"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        deleted = await service.delete_user_key(
            session,
            user_id=current_user["user_id"],
            provider=provider
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No API key found for provider: {provider}"
            )

        return {"message": f"API key deleted for {provider}"}


@router.post("/validate/{provider}")
async def validate_api_key(
    provider: str,
    current_user: dict = Depends(get_current_user)
):
    """Validate API key for current user"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        is_valid = await service.validate_user_key(
            session,
            user_id=current_user["user_id"],
            provider=provider
        )

        return {
            "provider": provider,
            "is_valid": is_valid,
            "validated_at": datetime.utcnow().isoformat()
        }
```

**Mount router in web/app.py**:

```python
from web.api.routes import api_keys

# Add to router mounting section
app.include_router(api_keys.router)
```

### 2.3 Test Key Rotation (45 min)

**File**: `tests/security/test_key_rotation.py` (CREATE)

```python
"""
Tests for API Key Rotation
"""
import pytest
from services.security.user_api_key_service import UserAPIKeyService
from services.database.session_factory import AsyncSessionFactory


@pytest.mark.asyncio
async def test_rotate_key():
    """Test basic key rotation"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Store initial key
        user_key = await service.store_user_key(
            session,
            user_id="rotation_test_1",
            provider="openai",
            api_key="old-key-123",
            validate=False
        )

        old_reference = user_key.key_reference

        # Rotate to new key
        rotated_key = await service.rotate_user_key(
            session,
            user_id="rotation_test_1",
            provider="openai",
            new_api_key="new-key-456",
            validate=False
        )

        # Verify rotation
        assert rotated_key.previous_key_reference == old_reference
        assert rotated_key.key_reference != old_reference
        assert rotated_key.rotated_at is not None

        # Verify new key is retrieved
        retrieved_key = await service.retrieve_user_key(
            session,
            user_id="rotation_test_1",
            provider="openai"
        )
        assert retrieved_key == "new-key-456"


@pytest.mark.asyncio
async def test_rotation_without_existing_key():
    """Test rotation when no existing key (should create new)"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Rotate without existing key (should work like store)
        rotated_key = await service.rotate_user_key(
            session,
            user_id="rotation_test_2",
            provider="anthropic",
            new_api_key="first-key-789",
            validate=False
        )

        assert rotated_key.provider == "anthropic"
        assert rotated_key.is_active is True


@pytest.mark.asyncio
async def test_multiple_rotations():
    """Test rotating key multiple times"""
    service = UserAPIKeyService()

    async with AsyncSessionFactory.session_scope() as session:
        # Store initial key
        await service.store_user_key(
            session, "rotation_test_3", "github", "key-v1", validate=False
        )

        # Rotate to v2
        key_v2 = await service.rotate_user_key(
            session, "rotation_test_3", "github", "key-v2", validate=False
        )
        first_rotation = key_v2.rotated_at

        # Rotate to v3
        key_v3 = await service.rotate_user_key(
            session, "rotation_test_3", "github", "key-v3", validate=False
        )

        # Verify v3 is active
        retrieved = await service.retrieve_user_key(session, "rotation_test_3", "github")
        assert retrieved == "key-v3"

        # Verify rotation timestamps
        assert key_v3.rotated_at > first_rotation
```

**Run rotation tests**:
```bash
pytest tests/security/test_key_rotation.py -v
```

**Success criteria**:
- [ ] All 3 rotation tests passing
- [ ] Old key deleted from keychain
- [ ] New key accessible
- [ ] Multiple rotations supported
- [ ] Rotation without existing key works

---

## Phase 3: Documentation & Testing (2 hours)

### 3.1 Create API Key Management Guide (45 min)

**File**: `docs/api-key-management.md` (CREATE)

```markdown
# API Key Management Guide

**Last Updated**: October 22, 2025

---

## Overview

Piper Morgan provides secure, per-user API key management with OS keychain integration and zero-downtime rotation.

**Features**:
- OS-level encryption (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- Per-user key isolation
- Real API validation
- Zero-downtime key rotation
- Support for 4+ LLM providers

---

## Quick Start

### Store Your First API Key

```bash
# Via API
POST /api/v1/keys/store
{
  "provider": "openai",
  "api_key": "sk-...",
  "validate": true
}
```

### List Your Keys

```bash
GET /api/v1/keys/list
```

### Rotate a Key

```bash
POST /api/v1/keys/rotate
{
  "provider": "openai",
  "new_api_key": "sk-new-...",
  "validate": true
}
```

---

## Supported Providers

**LLM Services**:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Gemini (Google)
- Perplexity

**Integration Services**:
- GitHub (tokens)
- Notion (API keys)
- Slack (workspace tokens)

---

## Security Architecture

### OS Keychain Integration

**Storage**:
```
macOS: Keychain.app
Linux: Secret Service (GNOME Keyring, KWallet)
Windows: Credential Manager
```

**Encryption**: OS-level secure storage (256-bit AES or better)

### Multi-User Isolation

Each user's keys are stored with unique identifiers:
```
Keychain account: {user_id}
Service: piper_morgan_{provider}
```

**Users cannot access each other's keys** - enforced at both application and OS level.

---

## Key Rotation

### Zero-Downtime Process

1. Validate new key with provider API
2. Store new key in keychain
3. Update database reference
4. Switch to new key (atomic)
5. Delete old key from keychain

**No service interruption during rotation!**

### Rotation Best Practices

**When to rotate**:
- Every 90 days (recommended)
- On security incident
- On team member departure
- On key compromise

**How to rotate**:
```python
from services.security.user_api_key_service import UserAPIKeyService

service = UserAPIKeyService()

async with session_scope() as session:
    await service.rotate_user_key(
        session,
        user_id="user_123",
        provider="openai",
        new_api_key="sk-new-...",
        validate=True
    )
```

---

## API Endpoints

### POST /api/v1/keys/store

Store API key for current user.

**Request**:
```json
{
  "provider": "openai",
  "api_key": "sk-...",
  "validate": true
}
```

**Response**:
```json
{
  "message": "API key stored successfully for openai",
  "provider": "openai",
  "is_validated": true,
  "created_at": "2025-10-22T06:00:00Z"
}
```

### POST /api/v1/keys/rotate

Rotate API key for current user.

**Request**:
```json
{
  "provider": "anthropic",
  "new_api_key": "sk-ant-...",
  "validate": true
}
```

**Response**:
```json
{
  "message": "API key rotated successfully for anthropic",
  "provider": "anthropic",
  "rotated_at": "2025-10-22T06:05:00Z",
  "is_validated": true
}
```

### GET /api/v1/keys/list

List all API keys for current user (metadata only).

**Response**:
```json
{
  "keys": [
    {
      "provider": "openai",
      "is_active": true,
      "is_validated": true,
      "last_validated_at": "2025-10-22T06:00:00Z",
      "created_at": "2025-10-20T10:00:00Z",
      "rotated_at": null
    }
  ]
}
```

### DELETE /api/v1/keys/{provider}

Delete API key for current user.

**Response**:
```json
{
  "message": "API key deleted for openai"
}
```

### POST /api/v1/keys/validate/{provider}

Validate API key by testing with provider API.

**Response**:
```json
{
  "provider": "openai",
  "is_valid": true,
  "validated_at": "2025-10-22T06:10:00Z"
}
```

---

## Troubleshooting

### Keychain Access Denied

**macOS**: Grant Keychain access in System Preferences → Security & Privacy
**Linux**: Install gnome-keyring or kwallet
**Windows**: Run as administrator for first access

### Key Validation Fails

1. Verify key format correct for provider
2. Check key has required permissions
3. Verify network connectivity
4. Check provider service status

### Key Not Found

1. Verify key was stored for current user
2. Check provider spelling exact match
3. Verify keychain accessible
4. Check database record exists

---

## Migration from Environment Variables

Use the migration script to move from .env to keychain:

```bash
python scripts/migrate_keys_to_keychain.py --user-id your_user_id
```

**Dry run** (preview only):
```bash
python scripts/migrate_keys_to_keychain.py --user-id your_user_id --dry-run
```

---

*For developer integration, see services/security/user_api_key_service.py*
```

### 3.2 Integration Testing (45 min)

**File**: `tests/integration/test_api_key_workflow.py` (CREATE)

```python
"""
Integration tests for complete API key workflow
"""
import pytest
from fastapi.testclient import TestClient
from web.app import app
from services.database.session_factory import AsyncSessionFactory


client = TestClient(app)


@pytest.mark.integration
def test_complete_api_key_workflow():
    """Test complete workflow: store, list, rotate, validate, delete"""

    # Mock authentication (replace with actual auth token)
    headers = {"Authorization": "Bearer test_token"}

    # 1. Store key
    response = client.post(
        "/api/v1/keys/store",
        json={
            "provider": "openai",
            "api_key": "sk-test-key-123",
            "validate": False
        },
        headers=headers
    )
    assert response.status_code == 200
    assert "stored successfully" in response.json()["message"]

    # 2. List keys
    response = client.get("/api/v1/keys/list", headers=headers)
    assert response.status_code == 200
    keys = response.json()["keys"]
    assert len(keys) >= 1
    assert any(k["provider"] == "openai" for k in keys)

    # 3. Rotate key
    response = client.post(
        "/api/v1/keys/rotate",
        json={
            "provider": "openai",
            "new_api_key": "sk-test-key-456",
            "validate": False
        },
        headers=headers
    )
    assert response.status_code == 200
    assert "rotated successfully" in response.json()["message"]

    # 4. Validate key
    response = client.post(
        "/api/v1/keys/validate/openai",
        headers=headers
    )
    # May fail validation with test key, but endpoint should work
    assert response.status_code == 200

    # 5. Delete key
    response = client.delete("/api/v1/keys/openai", headers=headers)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    # 6. Verify deleted
    response = client.get("/api/v1/keys/list", headers=headers)
    keys = response.json()["keys"]
    assert not any(k["provider"] == "openai" for k in keys)
```

### 3.3 Update .env.example (15 min)

**File**: `.env.example` (UPDATE)

Add documentation about keychain usage:

```bash
# API Key Management
# ==================
# Piper Morgan stores API keys securely in OS keychain per user.
# For initial setup, you can use environment variables which will be
# migrated to keychain on first use.

# LLM Providers (will be migrated to keychain)
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GEMINI_API_KEY=your-gemini-key
PERPLEXITY_API_KEY=pplx-your-key

# Integration Services (will be migrated to keychain)
GITHUB_TOKEN=ghp_your-github-token
NOTION_API_KEY=secret_your-notion-key
SLACK_BOT_TOKEN=xoxb-your-slack-token

# Multi-User Key Management
# Keys are automatically isolated per user via keychain
# No additional configuration needed
```

### 3.4 Final Verification (15 min)

```bash
# Run all API key tests
pytest tests/security/ -v

# Run integration test
pytest tests/integration/test_api_key_workflow.py -v

# Verify endpoints
curl http://localhost:8001/api/v1/keys/list \
  -H "Authorization: Bearer test_token"
```

**Success criteria**:
- [ ] All unit tests passing (user key service + rotation)
- [ ] Integration test passing (complete workflow)
- [ ] Documentation complete and clear
- [ ] API endpoints responding
- [ ] .env.example updated

---

## Success Criteria

All phases complete when:

- [x] Phase 0: Infrastructure verified (existing 85%)
- [x] Phase 1: Multi-user key isolation working (4 hours)
  - [ ] UserAPIKey model created
  - [ ] Database migration applied
  - [ ] UserAPIKeyService implemented
  - [ ] Tests passing (multi-user isolation verified)
- [x] Phase 2: Key rotation implemented (3 hours)
  - [ ] Rotation methods added
  - [ ] API endpoints created
  - [ ] Tests passing (zero-downtime verified)
- [x] Phase 3: Documentation complete (2 hours)
  - [ ] API key management guide created
  - [ ] Integration tests passing
  - [ ] .env.example updated
- [x] NO breaking changes to existing infrastructure
- [x] All existing LLM integrations still working

---

## Critical Reminders

### 1. Infrastructure is 85% DONE

Don't rebuild what exists! The KeychainService and LLMConfigService are world-class.

### 2. Build ON TOP of Existing Work

- KeychainService: Already handles OS keychain
- LLMConfigService: Already validates and manages keys
- Migration scripts: Already exist and work

### 3. Multi-User is the Key Addition

The main work is adding per-user isolation, not rebuilding key management.

### 4. STOP Conditions

If ANY of these occur, STOP and ask PM:
- KeychainService doesn't work as documented
- LLMConfigService validation fails
- Cannot create UserAPIKey model
- Migration fails
- Tests fail unexpectedly
- Rotation causes service interruption

---

## Communication Protocol

**When phase complete**:
```
✅ Phase X Complete

Added: [what was added]
Tests: [X/Y passing]
Evidence: [terminal output]

Ready for Phase Y.
```

**When all complete**:
```
✅ ALL PHASES COMPLETE

Summary:
- Multi-user key isolation: ✅ (UserAPIKey model + service)
- Key rotation: ✅ (Zero-downtime rotation + API endpoints)
- Documentation: ✅ (API guide + integration tests)

Test Results:
- Unit tests: X/X passing
- Integration tests: Y/Y passing
- API endpoints: All responding

Existing Infrastructure Preserved:
- KeychainService: ✅ Working
- LLMConfigService: ✅ Working
- 4-provider LLM support: ✅ Working
- Migration tools: ✅ Available

Evidence document: dev/2025/10/22/api-key-management-completion-summary.md

Ready for PM review!
```

---

**This is enhancement work, not infrastructure building! 85% is already done - just adding multi-user support and rotation to world-class existing code.** 🚀

"""
Tests for UserAPIKeyService - Multi-User API Key Isolation

Tests verify that:
1. Different users can store keys for the same provider
2. Keys are isolated per user (user A can't access user B's keys)
3. Store/retrieve/delete operations work correctly per user
4. Key validation works per user
5. List operations show only user-specific keys

Issue #228 CORE-USERS-API Phase 1E
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import select

from services.database.models import User, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService


# Test fixtures
@pytest.fixture
async def test_users():
    """Create test users for isolation testing"""
    async with AsyncSessionFactory.session_scope() as session:
        # Create user A
        user_a = User(
            id="test_user_a_isolation",
            username="user_a",
            email="user_a@example.com",
            is_active=True,
        )
        # Create user B
        user_b = User(
            id="test_user_b_isolation",
            username="user_b",
            email="user_b@example.com",
            is_active=True,
        )
        session.add(user_a)
        session.add(user_b)
        await session.commit()

        yield user_a, user_b

        # Cleanup
        await session.delete(user_a)
        await session.delete(user_b)
        await session.commit()


@pytest.fixture
def mock_keychain():
    """Mock keychain service for testing"""
    keychain = MagicMock()
    keychain._storage = {}  # In-memory storage for testing

    def store_key(provider, api_key, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        keychain._storage[key_name] = api_key

    def get_key(provider, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        return keychain._storage.get(key_name)

    def delete_key(provider, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        if key_name in keychain._storage:
            del keychain._storage[key_name]

    keychain.store_api_key = MagicMock(side_effect=store_key)
    keychain.get_api_key = MagicMock(side_effect=get_key)
    keychain.delete_api_key = MagicMock(side_effect=delete_key)

    return keychain


@pytest.mark.asyncio
async def test_multi_user_key_isolation(test_users, mock_keychain):
    """
    Test that different users can store keys for the same provider
    without interfering with each other.

    Issue #228 CORE-USERS-API - Multi-user key isolation
    """
    user_a, user_b = test_users

    # Create service with mock keychain (skip validation)
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope() as session:
        # User A stores OpenAI key
        with patch.object(service._llm_config, "validate_api_key", return_value=True):
            key_a = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key="sk-userA-key-123",
                validate=False,  # Skip validation for speed
            )

        # User B stores OpenAI key (same provider, different key!)
        with patch.object(service._llm_config, "validate_api_key", return_value=True):
            key_b = await service.store_user_key(
                session=session,
                user_id=user_b.id,
                provider="openai",
                api_key="sk-userB-key-456",
                validate=False,  # Skip validation for speed
            )

        # Verify both keys stored in database
        assert key_a is not None
        assert key_b is not None
        assert key_a.user_id == user_a.id
        assert key_b.user_id == user_b.id
        assert key_a.provider == "openai"
        assert key_b.provider == "openai"

        # Verify keys stored in keychain with different references
        assert key_a.key_reference == f"piper_{user_a.id}_openai"
        assert key_b.key_reference == f"piper_{user_b.id}_openai"

        # Retrieve user A's key - should get user A's key only
        retrieved_key_a = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="openai"
        )
        assert retrieved_key_a == "sk-userA-key-123"

        # Retrieve user B's key - should get user B's key only
        retrieved_key_b = await service.retrieve_user_key(
            session=session, user_id=user_b.id, provider="openai"
        )
        assert retrieved_key_b == "sk-userB-key-456"

        # Verify keychain was called with correct username parameter
        mock_keychain.get_api_key.assert_any_call("openai", username=user_a.id)
        mock_keychain.get_api_key.assert_any_call("openai", username=user_b.id)

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")
        await service.delete_user_key(session, user_b.id, "openai")


@pytest.mark.asyncio
async def test_delete_user_key_isolation(test_users, mock_keychain):
    """
    Test that deleting user A's key doesn't affect user B's key
    for the same provider.

    Issue #228 CORE-USERS-API - Delete isolation
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope() as session:
        # Store keys for both users
        await service.store_user_key(
            session=session,
            user_id=user_a.id,
            provider="anthropic",
            api_key="sk-userA-anthropic-123",
            validate=False,
        )

        await service.store_user_key(
            session=session,
            user_id=user_b.id,
            provider="anthropic",
            api_key="sk-userB-anthropic-456",
            validate=False,
        )

        # Delete user A's key
        deleted = await service.delete_user_key(
            session=session, user_id=user_a.id, provider="anthropic"
        )
        assert deleted is True

        # Verify user A's key is gone
        key_a = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="anthropic"
        )
        assert key_a is None

        # Verify user B's key still exists
        key_b = await service.retrieve_user_key(
            session=session, user_id=user_b.id, provider="anthropic"
        )
        assert key_b == "sk-userB-anthropic-456"

        # Cleanup
        await service.delete_user_key(session, user_b.id, "anthropic")


@pytest.mark.asyncio
async def test_list_user_keys_isolation(test_users, mock_keychain):
    """
    Test that list_user_keys only returns keys for the specified user.

    Issue #228 CORE-USERS-API - List isolation
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope() as session:
        # User A stores 2 keys
        await service.store_user_key(
            session=session,
            user_id=user_a.id,
            provider="openai",
            api_key="sk-userA-openai-123",
            validate=False,
        )
        await service.store_user_key(
            session=session,
            user_id=user_a.id,
            provider="anthropic",
            api_key="sk-userA-anthropic-456",
            validate=False,
        )

        # User B stores 1 key
        await service.store_user_key(
            session=session,
            user_id=user_b.id,
            provider="openai",
            api_key="sk-userB-openai-789",
            validate=False,
        )

        # List user A's keys - should see 2 keys
        keys_a = await service.list_user_keys(session=session, user_id=user_a.id, active_only=True)
        assert len(keys_a) == 2
        providers_a = {key["provider"] for key in keys_a}
        assert providers_a == {"openai", "anthropic"}

        # List user B's keys - should see 1 key
        keys_b = await service.list_user_keys(session=session, user_id=user_b.id, active_only=True)
        assert len(keys_b) == 1
        assert keys_b[0]["provider"] == "openai"

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")
        await service.delete_user_key(session, user_a.id, "anthropic")
        await service.delete_user_key(session, user_b.id, "openai")


@pytest.mark.asyncio
async def test_store_user_key_update_existing(test_users, mock_keychain):
    """
    Test that storing a key for an existing (user_id, provider) updates
    the record rather than creating a duplicate.

    Issue #228 CORE-USERS-API - Update behavior
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope() as session:
        # Store initial key
        key1 = await service.store_user_key(
            session=session,
            user_id=user_a.id,
            provider="openai",
            api_key="sk-old-key-123",
            validate=False,
        )
        initial_id = key1.id

        # Store new key (should update, not create new)
        key2 = await service.store_user_key(
            session=session,
            user_id=user_a.id,
            provider="openai",
            api_key="sk-new-key-456",
            validate=False,
        )

        # Verify same record updated (same ID)
        assert key2.id == initial_id

        # Verify only one record exists
        result = await session.execute(
            select(UserAPIKey).where(
                UserAPIKey.user_id == user_a.id, UserAPIKey.provider == "openai"
            )
        )
        all_keys = result.scalars().all()
        assert len(all_keys) == 1

        # Verify new key retrieved
        retrieved_key = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="openai"
        )
        assert retrieved_key == "sk-new-key-456"

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")


@pytest.mark.asyncio
async def test_validate_user_key_per_user(test_users, mock_keychain):
    """
    Test that key validation works per user.

    Issue #228 CORE-USERS-API - Validation per user
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope() as session:
        # Store keys for both users (skip initial validation)
        await service.store_user_key(
            session=session,
            user_id=user_a.id,
            provider="openai",
            api_key="sk-valid-key-123",
            validate=False,
        )

        await service.store_user_key(
            session=session,
            user_id=user_b.id,
            provider="openai",
            api_key="sk-invalid-key-456",
            validate=False,
        )

        # Mock validation - user A's key is valid, user B's is invalid
        async def mock_validate(provider, api_key):
            if api_key == "sk-valid-key-123":
                return True
            return False

        with patch.object(service._llm_config, "validate_api_key", side_effect=mock_validate):
            # Validate user A's key
            is_valid_a = await service.validate_user_key(
                session=session, user_id=user_a.id, provider="openai"
            )
            assert is_valid_a is True

            # Validate user B's key
            is_valid_b = await service.validate_user_key(
                session=session, user_id=user_b.id, provider="openai"
            )
            assert is_valid_b is False

        # Verify validation status in database
        result_a = await session.execute(
            select(UserAPIKey).where(
                UserAPIKey.user_id == user_a.id, UserAPIKey.provider == "openai"
            )
        )
        key_a = result_a.scalar_one()
        assert key_a.is_validated is True
        assert key_a.last_validated_at is not None

        result_b = await session.execute(
            select(UserAPIKey).where(
                UserAPIKey.user_id == user_b.id, UserAPIKey.provider == "openai"
            )
        )
        key_b = result_b.scalar_one()
        assert key_b.is_validated is False

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")
        await service.delete_user_key(session, user_b.id, "openai")


@pytest.mark.asyncio
async def test_keychain_reference_format(test_users, mock_keychain):
    """
    Test that keychain references follow the correct format:
    piper_{user_id}_{provider}

    Issue #228 CORE-USERS-API - Reference format
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope() as session:
        # Store key for user A
        key = await service.store_user_key(
            session=session,
            user_id=user_a.id,
            provider="github",
            api_key="ghp_test123",
            validate=False,
        )

        # Verify reference format
        expected_reference = f"piper_{user_a.id}_github"
        assert key.key_reference == expected_reference

        # Verify keychain was called with correct username
        mock_keychain.store_api_key.assert_called_with("github", "ghp_test123", username=user_a.id)

        # Cleanup
        await service.delete_user_key(session, user_a.id, "github")


@pytest.mark.asyncio
async def test_retrieve_nonexistent_key_returns_none(test_users, mock_keychain):
    """
    Test that retrieving a non-existent key returns None without error.

    Issue #228 CORE-USERS-API - Error handling
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope() as session:
        # Try to retrieve key that doesn't exist
        key = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="nonexistent"
        )

        assert key is None

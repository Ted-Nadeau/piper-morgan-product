"""
Tests for User model and relationships

Issue #228 CORE-USERS-API Phase 1A
Issue #262 - Updated for UUID migration
"""

from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from services.database.models import FeedbackDB, PersonalityProfileModel, TokenBlacklist, User
from services.database.session_factory import AsyncSessionFactory

# Import test UUIDs from conftest
from tests.conftest import TEST_USER_ID, TEST_USER_ID_2


@pytest.mark.asyncio
async def test_create_user():
    """Test creating a User record

    Note: Uses unique email to avoid duplicate key errors from multiple test runs.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        unique_id = uuid4()
        user = User(
            id=unique_id,  # Issue #262 - UUID instead of string
            username=f"testuser_{unique_id.hex[:8]}",
            email=f"test_{unique_id.hex[:8]}@example.com",
            is_active=True,
            is_verified=False,
        )
        session.add(user)
        await session.commit()

        # Verify user created
        result = await session.execute(select(User).where(User.id == user.id))
        retrieved_user = result.scalar_one_or_none()

        assert retrieved_user is not None
        assert retrieved_user.username == f"testuser_{unique_id.hex[:8]}"
        assert retrieved_user.email == f"test_{unique_id.hex[:8]}@example.com"
        assert retrieved_user.is_active is True
        assert retrieved_user.is_verified is False

        # Cleanup
        await session.delete(retrieved_user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_personality_profile_relationship():
    """Test User <-> PersonalityProfile relationship

    Note: Uses unique identifiers to avoid duplicate key errors from multiple test runs.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create user with unique identifiers
        unique_id = uuid4()
        user = User(
            id=unique_id,
            username=f"profileuser_{unique_id.hex[:8]}",
            email=f"profile_{unique_id.hex[:8]}@example.com",
        )
        session.add(user)
        await session.flush()  # Get user.id assigned

        # Create personality profile linked to user
        profile = PersonalityProfileModel(
            id=uuid4(),
            user_id=user.id,
            warmth_level=0.7,
            confidence_style="confident",
            action_orientation="high",
            technical_depth="deep",
        )
        session.add(profile)
        await session.commit()

        # Test relationship from User -> PersonalityProfile
        result = await session.execute(select(User).where(User.id == unique_id))
        retrieved_user = result.scalar_one_or_none()

        # Load relationship
        await session.refresh(retrieved_user, ["personality_profiles"])

        assert len(retrieved_user.personality_profiles) == 1
        assert retrieved_user.personality_profiles[0].warmth_level == 0.7

        # Test relationship from PersonalityProfile -> User
        result = await session.execute(
            select(PersonalityProfileModel).where(PersonalityProfileModel.user_id == unique_id)
        )
        retrieved_profile = result.scalar_one_or_none()

        await session.refresh(retrieved_profile, ["user"])

        assert retrieved_profile.user.username == f"profileuser_{unique_id.hex[:8]}"

        # Cleanup
        await session.delete(profile)
        await session.delete(user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_token_blacklist_relationship():
    """Test User <-> TokenBlacklist relationship

    Note: Uses unique identifiers to avoid duplicate key errors from multiple test runs.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create user with unique identifiers
        unique_id = uuid4()
        user = User(
            id=unique_id,
            username=f"tokenuser_{unique_id.hex[:8]}",
            email=f"token_{unique_id.hex[:8]}@example.com",
        )
        session.add(user)
        await session.flush()

        # Create blacklisted token linked to user
        token = TokenBlacklist(
            token_id=str(uuid4()),
            user_id=user.id,
            reason="test",
            expires_at=datetime.utcnow() + timedelta(days=1),
            created_at=datetime.utcnow(),
        )
        session.add(token)
        await session.commit()

        # Test relationship
        result = await session.execute(select(User).where(User.id == unique_id))
        retrieved_user = result.scalar_one_or_none()

        await session.refresh(retrieved_user, ["blacklisted_tokens"])

        assert len(retrieved_user.blacklisted_tokens) == 1
        assert retrieved_user.blacklisted_tokens[0].reason == "test"

        # Cleanup
        await session.delete(token)
        await session.delete(user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_feedback_relationship():
    """Test User <-> Feedback relationship

    Note: Uses unique identifiers to avoid duplicate key errors from multiple test runs.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create user with unique identifiers
        unique_id = uuid4()
        user = User(
            id=unique_id,
            username=f"feedbackuser_{unique_id.hex[:8]}",
            email=f"feedback_{unique_id.hex[:8]}@example.com",
        )
        session.add(user)
        await session.flush()

        # Create feedback linked to user
        feedback = FeedbackDB(
            id=str(uuid4()),
            session_id=str(uuid4()),
            feedback_type="bug",
            comment="Test feedback",
            user_id=user.id,
        )
        session.add(feedback)
        await session.commit()

        # Test relationship
        result = await session.execute(select(User).where(User.id == unique_id))
        retrieved_user = result.scalar_one_or_none()

        await session.refresh(retrieved_user, ["feedback"])

        assert len(retrieved_user.feedback) == 1
        assert retrieved_user.feedback[0].comment == "Test feedback"

        # Cleanup
        await session.delete(feedback)
        await session.delete(user)
        await session.commit()


@pytest.mark.asyncio
async def test_user_unique_constraints():
    """Test unique constraints on username and email

    Note: Uses unique identifiers to avoid duplicate key errors from multiple test runs.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create first user with unique email
        unique_id = uuid4()
        user1_id = uuid4()
        user1 = User(
            id=user1_id,
            username=f"uniqueuser_{unique_id.hex[:8]}",
            email=f"unique_{unique_id.hex[:8]}@example.com",
        )
        session.add(user1)
        await session.commit()

        # Try to create second user with same username
        user2 = User(
            id=uuid4(),
            username=f"uniqueuser_{unique_id.hex[:8]}",  # Duplicate!
            email=f"unique2_{unique_id.hex[:8]}@example.com",
        )
        session.add(user2)

        with pytest.raises(Exception):  # Should raise IntegrityError
            await session.commit()

        await session.rollback()

        # Try to create user with same email
        user3 = User(
            id=uuid4(),
            username=f"uniqueuser2_{unique_id.hex[:8]}",
            email=f"unique_{unique_id.hex[:8]}@example.com",  # Duplicate!
        )
        session.add(user3)

        with pytest.raises(Exception):  # Should raise IntegrityError
            await session.commit()

        await session.rollback()

        # Cleanup
        result = await session.execute(select(User).where(User.id == user1_id))
        user_to_delete = result.scalar_one_or_none()
        if user_to_delete:
            await session.delete(user_to_delete)
            await session.commit()


@pytest.mark.asyncio
async def test_user_timestamps():
    """Test that timestamps are set correctly"""
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create user
        user = User(id=uuid4(), username="timestampuser", email="timestamp@example.com")
        session.add(user)
        await session.commit()

        # Verify timestamps
        result = await session.execute(select(User).where(User.id == user.id))
        retrieved_user = result.scalar_one_or_none()

        assert retrieved_user.created_at is not None
        assert retrieved_user.updated_at is not None
        assert retrieved_user.last_login_at is None  # Should be None initially

        # Cleanup
        await session.delete(retrieved_user)
        await session.commit()

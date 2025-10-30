"""
End-to-End Test for Alpha User Onboarding Flow

When this test passes, we can invite Beatrice as alpha tester #2!

Tests the complete happy path:
1. Setup wizard creates alpha user account
2. User can check system status
3. User sets preferences via questionnaire
4. Final status shows configured state

Issue #259: CORE-USER-ALPHA-TABLE (Alpha/production data separation)
Issue #218: CORE-USERS-ONBOARD (Setup wizard)
"""

import asyncio
import uuid
from datetime import datetime
from typing import Optional

import pytest
import sqlalchemy
from sqlalchemy import select, text

from services.database.models import AlphaUser, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService


class TestAlphaOnboardingE2E:
    """End-to-end tests for alpha user onboarding flow."""

    @pytest.fixture
    async def clean_test_user(self):
        """Clean up test user before and after test."""
        test_username = f"test_alpha_{uuid.uuid4().hex[:8]}"

        yield test_username

        # Cleanup: Remove test user if it exists
        try:
            async with AsyncSessionFactory.session_scope() as session:
                result = await session.execute(
                    select(AlphaUser).where(AlphaUser.username == test_username)
                )
                user = result.scalar_one_or_none()
                if user:
                    await session.delete(user)
                    await session.commit()
        except Exception:
            pass  # User may not exist

    async def test_alpha_user_creation(self, clean_test_user):
        """
        Test Step 1: Setup wizard creates alpha user account

        Verifies:
        - AlphaUser record created in alpha_users table
        - UUID primary key assigned
        - Username and email stored
        - Alpha wave set to 1
        - Timestamps created
        """
        username = clean_test_user
        email = f"{username}@test.com"

        # Simulate what setup_wizard.create_user_account() does
        user = AlphaUser(
            id=uuid.uuid4(),
            username=username,
            email=email,
            alpha_wave=1,  # First wave of alpha testing
            test_start_date=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        async with AsyncSessionFactory.session_scope() as session:
            session.add(user)
            await session.commit()

            # Verify user was created
            result = await session.execute(select(AlphaUser).where(AlphaUser.username == username))
            created_user = result.scalar_one()

            assert created_user is not None
            assert created_user.username == username
            assert created_user.email == email
            assert created_user.alpha_wave == 1
            assert isinstance(created_user.id, uuid.UUID)
            assert created_user.created_at is not None
            assert created_user.migrated_to_prod is False

    async def test_system_status_check(self, clean_test_user):
        """
        Test Step 2: Check system status

        Verifies:
        - Database connectivity works
        - Can query alpha_users table
        - Can retrieve user by ID
        - Status checker finds the user
        """
        # Create user first
        username = clean_test_user
        user_id = uuid.uuid4()

        # Create user in first session
        async with AsyncSessionFactory.session_scope() as session:
            user = AlphaUser(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                alpha_wave=1,
                test_start_date=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(user)
            await session.commit()

        # Verify in separate session
        async with AsyncSessionFactory.session_scope() as session:
            # Simulate what status_checker.check_database() does
            result = await session.execute(text("SELECT 1"))
            assert result.scalar_one() == 1

            # Count alpha users
            count_result = await session.execute(text("SELECT COUNT(*) FROM alpha_users"))
            user_count = count_result.scalar_one()
            assert user_count >= 1

            # Retrieve most recent user (what status_checker does)
            user_result = await session.execute(
                text("SELECT id, username FROM alpha_users ORDER BY created_at DESC LIMIT 1")
            )
            retrieved_user = user_result.first()
            assert retrieved_user is not None
            assert retrieved_user[1] == username

    async def test_preferences_storage(self, clean_test_user):
        """
        Test Step 3: Store and retrieve preferences

        Verifies:
        - Preferences saved to alpha_users.preferences JSONB column
        - All 5 preference types stored correctly
        - Can retrieve preferences
        - Timestamp added to preferences
        """
        import json

        username = clean_test_user
        user_id = uuid.uuid4()

        # Create user
        async with AsyncSessionFactory.session_scope() as session:
            user = AlphaUser(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                alpha_wave=1,
                test_start_date=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(user)
            await session.commit()

        # Store preferences (simulating questionnaire)
        preferences = {
            "communication_style": "balanced",
            "work_style": "flexible",
            "decision_making": "collaborative",
            "learning_style": "explanations",
            "feedback_level": "moderate",
            "configured_at": datetime.utcnow().isoformat(),
        }

        async with AsyncSessionFactory.session_scope() as session:
            # Simulate what store_user_preferences() does
            await session.execute(
                text(
                    """
                    UPDATE alpha_users
                    SET preferences = CAST(:prefs AS jsonb)
                    WHERE id = :user_id
                """
                ),
                {
                    "prefs": json.dumps(preferences),
                    "user_id": user_id,
                },
            )
            await session.commit()

        # Verify preferences were stored in separate session
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                text("SELECT preferences FROM alpha_users WHERE id = :user_id"),
                {"user_id": user_id},
            )
            row = result.fetchone()
            assert row is not None
            stored_prefs = row[0]

            # JSONB column returns dict
            assert isinstance(stored_prefs, dict)
            assert stored_prefs["communication_style"] == "balanced"
            assert stored_prefs["work_style"] == "flexible"
            assert stored_prefs["decision_making"] == "collaborative"
            assert stored_prefs["learning_style"] == "explanations"
            assert stored_prefs["feedback_level"] == "moderate"
            assert "configured_at" in stored_prefs

    async def test_api_key_storage_with_user(self, clean_test_user):
        """
        Test Step 4: API key storage (integration with alpha user)

        Verifies:
        - API keys can be stored for alpha users
        - UUID to string conversion works
        - No FK violations after migration 648730a3238d
        - UserAPIKey properly linked to alpha user
        """
        username = clean_test_user
        user_id = uuid.uuid4()
        test_key = "sk-proj-test123abc456def789"

        # Create user
        async with AsyncSessionFactory.session_scope() as session:
            user = AlphaUser(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                alpha_wave=1,
                test_start_date=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(user)
            await session.commit()

        # Store API key (user_id converted to string for compatibility)
        service = UserAPIKeyService()
        async with AsyncSessionFactory.session_scope() as session:
            try:
                # This is what wizard does: convert UUID to string
                user_id_str = str(user_id)

                # Store key using service
                result = await service.store_user_key(
                    session=session,
                    user_id=user_id_str,
                    provider="openai",
                    api_key=test_key,
                )

                assert result is not None, "API key storage should return UserAPIKey"
                assert result.provider == "openai"

                # Verify key was stored
                retrieved_key = await service.retrieve_user_key(
                    session=session,
                    user_id=user_id_str,
                    provider="openai",
                )
                assert retrieved_key == test_key

            except sqlalchemy.exc.IntegrityError as e:
                pytest.fail(
                    f"FK constraint violation (should be fixed by migration 648730a3238d): {e}"
                )

    async def test_complete_onboarding_happy_path(self, clean_test_user):
        """
        Test Complete Happy Path: wizard → status → preferences → final status

        This is the "birthday success" test!
        Verifies the complete end-to-end flow works:
        1. User created
        2. System status checks pass
        3. Preferences configured
        4. Final status shows configured
        """
        import json

        username = clean_test_user
        user_id = uuid.uuid4()

        # STEP 1: Create user (setup wizard)
        async with AsyncSessionFactory.session_scope() as session:
            user = AlphaUser(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                alpha_wave=1,
                test_start_date=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(user)
            await session.commit()

        # STEP 2: Check status (should find user) - in new session
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                text("SELECT id, username FROM alpha_users ORDER BY created_at DESC LIMIT 1")
            )
            retrieved = result.first()
            assert retrieved is not None
            assert retrieved[1] == username

        # STEP 3: Configure preferences - in new session
        preferences = {
            "communication_style": "balanced",
            "work_style": "flexible",
            "decision_making": "collaborative",
            "learning_style": "explanations",
            "feedback_level": "moderate",
            "configured_at": datetime.utcnow().isoformat(),
        }

        async with AsyncSessionFactory.session_scope() as session:
            await session.execute(
                text(
                    """
                    UPDATE alpha_users
                    SET preferences = CAST(:prefs AS jsonb)
                    WHERE id = :user_id
                """
                ),
                {
                    "prefs": json.dumps(preferences),
                    "user_id": user_id,
                },
            )
            await session.commit()

        # STEP 4: Verify final state - in new session
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(select(AlphaUser).where(AlphaUser.id == user_id))
            final_user = result.scalar_one()

            assert final_user.username == username
            assert final_user.preferences is not None
            assert final_user.preferences["communication_style"] == "balanced"
            assert final_user.alpha_wave == 1
            assert final_user.migrated_to_prod is False

        # 🎉 Success!


# Async test support (use pytest-asyncio)
pytestmark = pytest.mark.asyncio

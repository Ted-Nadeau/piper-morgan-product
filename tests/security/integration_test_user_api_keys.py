"""
Standalone Integration Test for Multi-User API Key Isolation

Bypasses pytest-asyncio fixtures to avoid event loop issues.
Proves functionality works end-to-end without test framework complications.

Issue #228 CORE-USERS-API Phase 1E
"""

import asyncio
import sys
from datetime import datetime

# Add project root to path
from uuid import UUID, uuid4

sys.path.insert(0, "/Users/xian/Development/piper-morgan")

from sqlalchemy import select

from services.database.models import User, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService


async def main():
    """Run integration tests"""
    print("=" * 80)
    print("Multi-User API Key Isolation - Standalone Integration Test")
    print("=" * 80)
    print()

    service = UserAPIKeyService()

    # Test users
    user_a_id = "integration_test_user_a"
    user_b_id = "integration_test_user_b"

    try:
        # ====================================================================
        # Test 1: Create Test Users
        # ====================================================================
        print("Test 1: Creating test users...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Clean up any existing test users first
            result = await session.execute(select(User).where(User.id.in_([user_a_id, user_b_id])))
            existing_users = result.scalars().all()
            for user in existing_users:
                await session.delete(user)
            await session.commit()

            # Create fresh test users
            user_a = User(
                id=user_a_id,
                username="integration_user_a",
                email="integration_a@example.com",
                is_active=True,
            )
            user_b = User(
                id=user_b_id,
                username="integration_user_b",
                email="integration_b@example.com",
                is_active=True,
            )
            session.add(user_a)
            session.add(user_b)
            await session.commit()
            print(f"✅ Created users: {user_a_id}, {user_b_id}")

        # ====================================================================
        # Test 2: Store Keys for Both Users (Same Provider)
        # ====================================================================
        print("\nTest 2: Storing keys for both users (same provider: github)...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # User A stores GitHub key
            key_a = await service.store_user_key(
                session=session,
                user_id=user_a_id,
                provider="github",
                api_key="ghp_integration_test_user_a_key_123",
                validate=False,  # Skip validation for speed
            )
            print(f"✅ User A stored GitHub key: {key_a.key_reference}")

            # User B stores GitHub key (same provider!)
            key_b = await service.store_user_key(
                session=session,
                user_id=user_b_id,
                provider="github",
                api_key="ghp_integration_test_user_b_key_456",
                validate=False,  # Skip validation for speed
            )
            print(f"✅ User B stored GitHub key: {key_b.key_reference}")

            # Verify different key references
            assert key_a.key_reference != key_b.key_reference, "Key references should be different!"
            print(f"✅ Verified: Key references are different")
            print(f"   User A: {key_a.key_reference}")
            print(f"   User B: {key_b.key_reference}")

        # ====================================================================
        # Test 3: Retrieve Keys (Verify Isolation)
        # ====================================================================
        print("\nTest 3: Retrieving keys (verify isolation)...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Retrieve user A's key
            retrieved_key_a = await service.retrieve_user_key(
                session=session, user_id=user_a_id, provider="github"
            )
            assert (
                retrieved_key_a == "ghp_integration_test_user_a_key_123"
            ), f"User A key mismatch! Expected user A's key, got: {retrieved_key_a}"
            print(f"✅ User A retrieved correct key: ghp_integration_test_user_a_key_123")

            # Retrieve user B's key
            retrieved_key_b = await service.retrieve_user_key(
                session=session, user_id=user_b_id, provider="github"
            )
            assert (
                retrieved_key_b == "ghp_integration_test_user_b_key_456"
            ), f"User B key mismatch! Expected user B's key, got: {retrieved_key_b}"
            print(f"✅ User B retrieved correct key: ghp_integration_test_user_b_key_456")

            print(f"✅ Verified: Multi-user isolation works! Each user gets their own key")

        # ====================================================================
        # Test 4: List Keys (Verify User-Specific Lists)
        # ====================================================================
        print("\nTest 4: Listing keys (verify user-specific lists)...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Store additional key for user A
            await service.store_user_key(
                session=session,
                user_id=user_a_id,
                provider="openai",
                api_key="sk_integration_test_user_a_openai",
                validate=False,
            )
            print(f"✅ User A stored additional OpenAI key")

            # List user A's keys
            keys_a = await service.list_user_keys(
                session=session, user_id=user_a_id, active_only=True
            )
            providers_a = {key["provider"] for key in keys_a}
            assert providers_a == {
                "github",
                "openai",
            }, f"User A should have 2 providers, got: {providers_a}"
            print(f"✅ User A has 2 keys: {providers_a}")

            # List user B's keys
            keys_b = await service.list_user_keys(
                session=session, user_id=user_b_id, active_only=True
            )
            providers_b = {key["provider"] for key in keys_b}
            assert providers_b == {"github"}, f"User B should have 1 provider, got: {providers_b}"
            print(f"✅ User B has 1 key: {providers_b}")

            print(f"✅ Verified: List keys returns only user-specific keys")

        # ====================================================================
        # Test 5: Delete Key (Verify Isolation)
        # ====================================================================
        print("\nTest 5: Deleting key (verify deletion doesn't affect other user)...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Delete user A's GitHub key
            deleted = await service.delete_user_key(
                session=session, user_id=user_a_id, provider="github"
            )
            assert deleted is True, "Delete should return True"
            print(f"✅ User A's GitHub key deleted")

            # Verify user A's key is gone
            key_a = await service.retrieve_user_key(
                session=session, user_id=user_a_id, provider="github"
            )
            assert key_a is None, "User A's GitHub key should be gone"
            print(f"✅ Verified: User A's GitHub key no longer exists")

            # Verify user B's key still exists
            key_b = await service.retrieve_user_key(
                session=session, user_id=user_b_id, provider="github"
            )
            assert (
                key_b == "ghp_integration_test_user_b_key_456"
            ), "User B's GitHub key should still exist"
            print(f"✅ Verified: User B's GitHub key still exists and is correct")

            print(f"✅ Verified: Deleting user A's key doesn't affect user B")

        # ====================================================================
        # Test 6: Update Existing Key (Verify Update, Not Create)
        # ====================================================================
        print("\nTest 6: Updating existing key (verify update behavior)...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Get current count
            result = await session.execute(
                select(UserAPIKey).where(
                    UserAPIKey.user_id == user_b_id, UserAPIKey.provider == "github"
                )
            )
            keys_before = result.scalars().all()
            count_before = len(keys_before)
            print(f"   Before update: {count_before} GitHub key(s) for user B")

            # Store new key (should update, not create)
            await service.store_user_key(
                session=session,
                user_id=user_b_id,
                provider="github",
                api_key="ghp_integration_test_user_b_key_789_updated",
                validate=False,
            )
            print(f"✅ Stored new GitHub key for user B")

            # Verify still only one record
            result = await session.execute(
                select(UserAPIKey).where(
                    UserAPIKey.user_id == user_b_id, UserAPIKey.provider == "github"
                )
            )
            keys_after = result.scalars().all()
            count_after = len(keys_after)
            print(f"   After update: {count_after} GitHub key(s) for user B")

            assert count_after == 1, f"Should have 1 key, got {count_after}"
            print(f"✅ Verified: Update doesn't create duplicate (still 1 record)")

            # Verify new key is retrieved
            retrieved_key = await service.retrieve_user_key(
                session=session, user_id=user_b_id, provider="github"
            )
            assert (
                retrieved_key == "ghp_integration_test_user_b_key_789_updated"
            ), "Should retrieve updated key"
            print(f"✅ Verified: Retrieved key is the updated one")

        # ====================================================================
        # Test 7: Key Rotation (Zero-Downtime)
        # ====================================================================
        print("\nTest 7: Key rotation (zero-downtime strategy)...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Store initial key for user A
            await service.store_user_key(
                session=session,
                user_id=user_a_id,
                provider="github",
                api_key="ghp_original_key_abc123",
                validate=False,
            )
            print(f"✅ User A stored original GitHub key")

            # Get initial key metadata
            result = await session.execute(
                select(UserAPIKey).where(
                    UserAPIKey.user_id == user_a_id, UserAPIKey.provider == "github"
                )
            )
            key_before = result.scalar_one()
            initial_key_reference = key_before.key_reference
            assert key_before.rotated_at is None, "rotated_at should be None initially"
            assert (
                key_before.previous_key_reference is None
            ), "previous_key_reference should be None initially"
            print(f"   Initial key_reference: {initial_key_reference}")
            print(f"   rotated_at: {key_before.rotated_at}")

            # Rotate the key
            rotated_key = await service.rotate_user_key(
                session=session,
                user_id=user_a_id,
                provider="github",
                new_api_key="ghp_rotated_key_xyz789",
                validate=False,
            )
            print(f"✅ User A rotated GitHub key")

            # Verify rotation metadata
            assert (
                rotated_key.previous_key_reference == initial_key_reference
            ), "previous_key_reference should be the old reference"
            assert rotated_key.rotated_at is not None, "rotated_at should be set"
            assert (
                rotated_key.key_reference == initial_key_reference
            ), "key_reference format should remain the same"
            print(f"   New key_reference: {rotated_key.key_reference}")
            print(f"   previous_key_reference: {rotated_key.previous_key_reference}")
            print(f"   rotated_at: {rotated_key.rotated_at.isoformat()}")

            # Verify only one record exists (not duplicate)
            result = await session.execute(
                select(UserAPIKey).where(
                    UserAPIKey.user_id == user_a_id, UserAPIKey.provider == "github"
                )
            )
            all_keys = result.scalars().all()
            assert len(all_keys) == 1, f"Should have 1 key, got {len(all_keys)}"
            print(f"✅ Verified: Still only 1 key record (no duplicate created)")

            # Verify new key is retrieved
            retrieved_key = await service.retrieve_user_key(
                session=session, user_id=user_a_id, provider="github"
            )
            assert retrieved_key == "ghp_rotated_key_xyz789", "Should retrieve new rotated key"
            print(f"✅ Verified: Retrieved key is the new rotated key")

            # Cleanup
            await service.delete_user_key(session, user_a_id, "github")

        # ====================================================================
        # Test 8: Rotate Non-Existent Key (Error Handling)
        # ====================================================================
        print("\nTest 8: Rotate non-existent key (error handling)...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Try to rotate key that doesn't exist
            try:
                await service.rotate_user_key(
                    session=session,
                    user_id=user_a_id,
                    provider="nonexistent",
                    new_api_key="should_fail",
                    validate=False,
                )
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "No existing key found" in str(e)
                print(f"✅ Correctly raised ValueError: {e}")

        print("\n" + "=" * 80)
        print("✅ ALL INTEGRATION TESTS PASSED (Including Key Rotation!)")
        print("=" * 80)
        print()
        print("Summary:")
        print("  ✅ Multi-user key isolation works correctly")
        print("  ✅ Different users can store keys for same provider")
        print("  ✅ Keys retrieved correctly per user")
        print("  ✅ List operations show only user-specific keys")
        print("  ✅ Delete operations don't affect other users")
        print("  ✅ Update operations don't create duplicates")
        print("  ✅ Key rotation works with zero-downtime strategy")
        print("  ✅ Rotation metadata tracked correctly")
        print("  ✅ Error handling works (non-existent key rotation)")
        print()
        print("Phase 1E + 2C functionality CONFIRMED WORKING! 🎉")
        print()

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    finally:
        # Cleanup
        print("Cleaning up test data...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Delete all test keys
            result = await session.execute(
                select(UserAPIKey).where(UserAPIKey.user_id.in_([user_a_id, user_b_id]))
            )
            keys = result.scalars().all()
            for key in keys:
                await session.delete(key)

            # Delete test users
            result = await session.execute(select(User).where(User.id.in_([user_a_id, user_b_id])))
            users = result.scalars().all()
            for user in users:
                await session.delete(user)

            await session.commit()
            print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(main())

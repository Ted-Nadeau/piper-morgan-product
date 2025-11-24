#!/usr/bin/env python3
"""
Phase 5 Manual Verification Tests
Issue #262 UUID Migration + Issue #291 Token Blacklist FK

These tests manually verify:
1. User creation with UUID
2. JWT token generation with UUID
3. Token blacklist CASCADE delete (Issue #291)
4. FK constraint enforcement
"""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from services.auth.jwt_service import JWTService
from services.database.models import TokenBlacklist, User
from services.database.session_factory import AsyncSessionFactory


async def test_1_user_creation_and_auth():
    """Test 1: User Creation & Auth with UUID"""
    print("=" * 80)
    print("TEST 1: User Creation & Auth with UUID")
    print("=" * 80)

    jwt_service = JWTService()

    async with AsyncSessionFactory.session_scope() as session:
        # Create user with UUID
        user_id = uuid4()
        user = User(
            id=user_id,
            username=f"test_e2e_{user_id.hex[:8]}",
            email=f"test_e2e_{user_id.hex[:8]}@example.com",
            is_active=True,
            is_verified=True,
        )
        session.add(user)
        await session.commit()
        print(f"✅ Created user with UUID: {user_id}")

        # Generate JWT token
        token = jwt_service.generate_access_token(
            user_id=user.id, user_email=user.email, scopes=["user"]
        )
        print(f"✅ Generated JWT token: {token[:50]}...")

        # Decode token to verify it contains UUID (without verification for testing)
        import jwt as pyjwt

        payload = pyjwt.decode(token, options={"verify_signature": False})
        assert "user_id" in payload
        assert payload["user_id"] == str(user.id)
        print(f"✅ Token contains correct UUID: {payload['user_id']}")

        # Cleanup
        await session.delete(user)
        await session.commit()
        print("✅ Cleanup complete\n")

        return True


async def test_2_token_blacklist_cascade():
    """Test 2: Token Blacklist CASCADE Delete (Issue #291)"""
    print("=" * 80)
    print("TEST 2: Token Blacklist CASCADE Delete (Issue #291)")
    print("=" * 80)

    async with AsyncSessionFactory.session_scope() as session:
        # Create user
        user_id = uuid4()
        user = User(
            id=user_id,
            username=f"test_cascade_{user_id.hex[:8]}",
            email=f"test_cascade_{user_id.hex[:8]}@example.com",
            is_active=True,
            is_verified=True,
        )
        session.add(user)
        await session.commit()
        print(f"✅ Created test user: {user_id}")

        # Create blacklisted token
        token_id = str(uuid4())
        token = TokenBlacklist(
            token_id=token_id,
            user_id=user.id,
            reason="test_cascade",
            expires_at=datetime.utcnow() + timedelta(days=1),
        )
        session.add(token)
        await session.commit()
        print(f"✅ Created blacklist entry: {token_id}")

        # Verify relationship works
        await session.refresh(token)
        assert token.user_id == user.id
        print(f"✅ Token linked to user via FK")

        # Verify token exists before delete
        result = await session.execute(
            select(TokenBlacklist).where(TokenBlacklist.token_id == token_id)
        )
        token_before = result.scalar_one_or_none()
        assert token_before is not None
        print(f"✅ Token exists in database before user delete")

        # Delete user (should CASCADE delete token)
        await session.delete(user)
        await session.commit()
        print(f"✅ Deleted user")

        # Verify token was CASCADE deleted
        result = await session.execute(
            select(TokenBlacklist).where(TokenBlacklist.token_id == token_id)
        )
        token_after = result.scalar_one_or_none()
        assert token_after is None, "Token should be CASCADE deleted!"
        print(f"✅ Token CASCADE deleted successfully!")
        print(f"\n🎉 ISSUE #291 CASCADE DELETE VERIFIED!\n")

        return True


async def test_3_fk_constraint_enforcement():
    """Test 3: FK Constraint Prevents Orphaned Tokens"""
    print("=" * 80)
    print("TEST 3: FK Constraint Enforcement")
    print("=" * 80)

    async with AsyncSessionFactory.session_scope() as session:
        # Try to create token with non-existent user
        fake_user_id = uuid4()
        token = TokenBlacklist(
            token_id=str(uuid4()),
            user_id=fake_user_id,  # Doesn't exist in users table
            reason="test_orphan",
            expires_at=datetime.utcnow() + timedelta(days=1),
        )
        session.add(token)

        # Should raise FK constraint error
        try:
            await session.commit()
            print("❌ FAILED - Should have raised IntegrityError!")
            return False
        except IntegrityError as e:
            await session.rollback()
            print(f"✅ FK constraint prevented orphaned entry")
            print(f"✅ Error (expected): {str(e)[:100]}...")
            print(f"\n🎉 ISSUE #291 FK ENFORCEMENT VERIFIED!\n")
            return True


async def test_4_performance():
    """Test 4: UUID Performance Testing"""
    print("=" * 80)
    print("TEST 4: UUID Performance Testing")
    print("=" * 80)

    import time

    async with AsyncSessionFactory.session_scope() as session:
        # Test xian's UUID lookup
        start = time.time()
        from uuid import UUID

        xian_id = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")
        result = await session.execute(select(User).where(User.id == xian_id))
        user = result.scalar_one_or_none()
        end = time.time()

        lookup_time = (end - start) * 1000  # Convert to ms
        print(f"✅ UUID lookup time: {lookup_time:.2f}ms")
        print(f"✅ User found: {user.username if user else 'None'}")

        # Verify acceptable performance (<50ms)
        if lookup_time < 50:
            print(f"✅ Performance acceptable (<50ms)\n")
            return True
        else:
            print(f"⚠️ Performance slower than expected (>50ms)\n")
            return False


async def main():
    """Run all Phase 5 manual verification tests"""
    print("\n" + "=" * 80)
    print("PHASE 5 MANUAL VERIFICATION - Issue #262 + #291")
    print("=" * 80)
    print()

    results = {}

    try:
        results["test_1"] = await test_1_user_creation_and_auth()
        results["test_2"] = await test_2_token_blacklist_cascade()
        results["test_3"] = await test_3_fk_constraint_enforcement()
        results["test_4"] = await test_4_performance()

        print("=" * 80)
        print("VERIFICATION RESULTS")
        print("=" * 80)
        print(f"Test 1 - User Creation & Auth: {'✅ PASS' if results['test_1'] else '❌ FAIL'}")
        print(f"Test 2 - CASCADE Delete (#291): {'✅ PASS' if results['test_2'] else '❌ FAIL'}")
        print(f"Test 3 - FK Enforcement (#291): {'✅ PASS' if results['test_3'] else '❌ FAIL'}")
        print(f"Test 4 - Performance: {'✅ PASS' if results['test_4'] else '❌ FAIL'}")
        print()

        all_passed = all(results.values())
        if all_passed:
            print("🎉 ALL MANUAL TESTS PASSED!")
            print("✅ Issue #262: UUID migration working")
            print("✅ Issue #291: Token blacklist FK with CASCADE working")
        else:
            print("⚠️ Some tests failed - see above for details")

        return all_passed

    except Exception as e:
        print(f"\n❌ ERROR during verification: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)

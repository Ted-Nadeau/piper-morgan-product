"""
Standalone Integration Test for JWT Audit Logging

Tests audit logging integration with JWT service (token revocation and refresh).
Bypasses pytest-asyncio fixtures to avoid event loop issues.

Issue #249 CORE-AUDIT-LOGGING Phase 2B
"""

import asyncio
import sys
from datetime import datetime
from uuid import UUID, uuid4

# Add project root to path
sys.path.insert(0, "/Users/xian/Development/piper-morgan")

from sqlalchemy import select

from services.auth.jwt_service import JWTService
from services.database.models import AuditLog, User
from services.database.session_factory import AsyncSessionFactory
from services.security.audit_logger import Action, EventType, Severity


async def main():
    """Run JWT audit logging integration tests"""
    print("=" * 80)
    print("JWT Audit Logging - Standalone Integration Test")
    print("=" * 80)
    print()

    # Test user
    test_user_id = uuid4()
    test_user_email = "jwt_audit@example.com"

    # Mock token blacklist for testing
    class MockBlacklist:
        def __init__(self):
            self.blacklisted_tokens = set()

        async def add(self, token_id: str, reason: str, expires_at, user_id: UUID):
            self.blacklisted_tokens.add(token_id)
            return True

        async def is_blacklisted(self, token_id: str):
            return token_id in self.blacklisted_tokens

    try:
        # ====================================================================
        # Test 1: Create Test User
        # ====================================================================
        print("Test 1: Creating test user...")
        async with AsyncSessionFactory.session_scope() as session:
            # Clean up any existing test user first
            result = await session.execute(select(User).where(User.id == test_user_id))
            existing_user = result.scalar_one_or_none()
            if existing_user:
                await session.delete(existing_user)
            await session.commit()

            # Create fresh test user
            test_user = User(
                id=test_user_id,
                username="jwt_audit_user",
                email=test_user_email,
                is_active=True,
            )
            session.add(test_user)
            await session.commit()
            print(f"✅ Created user: {test_user_id}")

        # ====================================================================
        # Test 2: JWT Token Revocation with Audit Logging
        # ====================================================================
        print("\nTest 2: Testing JWT token revocation audit logging...")

        # Create JWT service with mock blacklist
        mock_blacklist = MockBlacklist()
        jwt_service = JWTService(blacklist=mock_blacklist)

        # Generate access token
        access_token = jwt_service.generate_access_token(
            user_id=test_user_id,
            user_email=test_user_email,
            scopes=["read", "write"],
            session_id="jwt_test_session_123",
        )
        print(f"✅ Generated access token")

        # Revoke token WITH audit logging
        async with AsyncSessionFactory.session_scope() as session:
            success = await jwt_service.revoke_token(
                token=access_token,
                reason="logout",
                user_id=test_user_id,
                session=session,  # Enable audit logging
                audit_context={
                    "ip_address": "192.168.1.100",
                    "user_agent": "Test-Agent/1.0",
                    "request_id": "req_jwt_test_001",
                    "request_path": "/api/v1/auth/logout",
                },
            )
            await session.commit()

            print(f"✅ Token revoked: {success}")
            assert success, "Token revocation should succeed"

            # Verify audit log was created
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.event_type == EventType.AUTH,
                    AuditLog.action == Action.TOKEN_REVOKED,
                    AuditLog.user_id == test_user_id,
                )
            )
            revoke_log = result.scalar_one()

            print(f"✅ Found audit log: {revoke_log.id}")
            print(f"   Event Type: {revoke_log.event_type}")
            print(f"   Action: {revoke_log.action}")
            print(f"   Status: {revoke_log.status}")
            print(f"   Severity: {revoke_log.severity}")
            print(f"   Message: {revoke_log.message}")
            print(f"   IP: {revoke_log.ip_address}")
            print(f"   Details: {revoke_log.details}")

            # Assertions
            assert revoke_log.event_type == EventType.AUTH
            assert revoke_log.action == Action.TOKEN_REVOKED
            assert revoke_log.status == "success"
            assert revoke_log.severity == Severity.INFO
            assert revoke_log.user_id == test_user_id
            assert revoke_log.ip_address == "192.168.1.100"
            assert revoke_log.user_agent == "Test-Agent/1.0"
            assert revoke_log.request_id == "req_jwt_test_001"
            assert revoke_log.request_path == "/api/v1/auth/logout"
            assert revoke_log.details["reason"] == "logout"
            assert "token_id" in revoke_log.details
            assert "expires_at" in revoke_log.details
            print(f"✅ Verified: Token revocation audit log complete")

        # ====================================================================
        # Test 3: JWT Token Refresh with Audit Logging
        # ====================================================================
        print("\nTest 3: Testing JWT token refresh audit logging...")

        # Generate refresh token
        refresh_token = jwt_service.generate_refresh_token(
            user_id=test_user_id,
            user_email=test_user_email,
            session_id="jwt_test_session_456",
        )
        print(f"✅ Generated refresh token")

        # Refresh token WITH audit logging
        async with AsyncSessionFactory.session_scope() as session:
            new_access_token = await jwt_service.refresh_access_token(
                refresh_token=refresh_token,
                session=session,  # Enable audit logging
                audit_context={
                    "ip_address": "192.168.1.101",
                    "user_agent": "Test-Agent/2.0",
                    "request_id": "req_jwt_test_002",
                    "request_path": "/api/v1/auth/refresh",
                },
            )
            await session.commit()

            print(f"✅ Token refreshed: {new_access_token is not None}")
            assert new_access_token is not None, "Token refresh should succeed"

            # Verify audit log was created
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.event_type == EventType.AUTH,
                    AuditLog.action == Action.TOKEN_REFRESHED,
                    AuditLog.user_id == test_user_id,
                )
            )
            refresh_log = result.scalar_one()

            print(f"✅ Found audit log: {refresh_log.id}")
            print(f"   Event Type: {refresh_log.event_type}")
            print(f"   Action: {refresh_log.action}")
            print(f"   Status: {refresh_log.status}")
            print(f"   Session ID: {refresh_log.session_id}")
            print(f"   IP: {refresh_log.ip_address}")
            print(f"   Details: {refresh_log.details}")

            # Assertions
            assert refresh_log.event_type == EventType.AUTH
            assert refresh_log.action == Action.TOKEN_REFRESHED
            assert refresh_log.status == "success"
            assert refresh_log.severity == Severity.INFO
            assert refresh_log.user_id == test_user_id
            assert refresh_log.session_id == "jwt_test_session_456"
            assert refresh_log.ip_address == "192.168.1.101"
            assert refresh_log.user_agent == "Test-Agent/2.0"
            assert refresh_log.request_id == "req_jwt_test_002"
            assert refresh_log.request_path == "/api/v1/auth/refresh"
            assert "refresh_token_id" in refresh_log.details
            assert "scopes" in refresh_log.details
            print(f"✅ Verified: Token refresh audit log complete")

        # ====================================================================
        # Test 4: Token Revocation WITHOUT Audit Logging (Backward Compat)
        # ====================================================================
        print("\nTest 4: Testing backward compatibility (no audit logging)...")

        # Generate another access token
        access_token2 = jwt_service.generate_access_token(
            user_id=test_user_id,
            user_email=test_user_email,
            scopes=["read"],
        )

        # Revoke WITHOUT session (backward compatible - no audit logging)
        success = await jwt_service.revoke_token(
            token=access_token2,
            reason="security",
            user_id=test_user_id,
            # NO session parameter - audit logging should NOT occur
        )

        print(f"✅ Token revoked without audit: {success}")
        assert success, "Token revocation without audit should still work"

        # Verify no new audit log was created for this revocation
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.event_type == EventType.AUTH,
                    AuditLog.action == Action.TOKEN_REVOKED,
                    AuditLog.user_id == test_user_id,
                )
            )
            revoke_logs = result.scalars().all()

            # Should still only have 1 revocation log (from Test 2)
            assert len(revoke_logs) == 1, f"Expected 1 revoke log, found {len(revoke_logs)}"
            print(f"✅ Verified: No audit log created without session (backward compatible)")

        # ====================================================================
        # Test 5: Query All JWT Audit Logs
        # ====================================================================
        print("\nTest 5: Querying all JWT audit logs for user...")
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(AuditLog)
                .where(
                    AuditLog.user_id == test_user_id,
                    AuditLog.event_type == EventType.AUTH,
                )
                .order_by(AuditLog.created_at)
            )
            jwt_logs = result.scalars().all()

            print(f"✅ Found {len(jwt_logs)} JWT audit logs for user")
            for log in jwt_logs:
                print(f"   - {log.event_type}.{log.action}: {log.message}")

            # Should have 2 logs: TOKEN_REVOKED (Test 2) and TOKEN_REFRESHED (Test 3)
            assert len(jwt_logs) == 2
            actions = {log.action for log in jwt_logs}
            assert Action.TOKEN_REVOKED in actions
            assert Action.TOKEN_REFRESHED in actions
            print(f"✅ Verified: Both revocation and refresh logged correctly")

        print("\n" + "=" * 80)
        print("✅ ALL JWT AUDIT LOGGING TESTS PASSED (5/5 = 100%)")
        print("=" * 80)
        print()
        print("Summary:")
        print("  ✅ Token revocation audit logging works")
        print("  ✅ Token refresh audit logging works")
        print("  ✅ Audit context captured correctly (IP, user_agent, request_id, path)")
        print("  ✅ Backward compatibility maintained (no session = no audit)")
        print("  ✅ All JWT audit events queryable by user_id")
        print()
        print("Phase 2 (JWT Integration) functionality CONFIRMED WORKING! 🎉")
        print()

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    finally:
        # Cleanup
        print("Cleaning up test data...")
        async with AsyncSessionFactory.session_scope() as session:
            # Delete JWT audit logs
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.user_id == test_user_id,
                    AuditLog.event_type == EventType.AUTH,
                )
            )
            logs = result.scalars().all()
            for log in logs:
                await session.delete(log)

            # Delete test user
            result = await session.execute(select(User).where(User.id == test_user_id))
            user = result.scalar_one_or_none()
            if user:
                await session.delete(user)

            await session.commit()
            print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(main())

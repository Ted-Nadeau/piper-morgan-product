"""
Issue #490: TRUE End-to-End HTTP Tests for Portfolio Onboarding

These tests hit the REAL HTTP endpoints with REAL services.
No mocking of business logic - only database session isolation.

Pattern-045 Compliance:
- Tests the actual user experience, not mocked components
- If these tests pass, the feature works for users
- If these tests fail, users will see broken behavior

Test Flow (matches manual testing):
1. Create user with 0 projects
2. Login via /auth/login
3. Say "Hello" via /api/v1/intent
4. Expect onboarding prompt (not normal greeting)
5. Say "My project is X"
6. Expect acknowledgment (not echo, not identity response)
"""

from datetime import datetime, timezone
from uuid import uuid4

import httpx
import pytest
from sqlalchemy import delete as sql_delete
from sqlalchemy import select, text

from services.database.models import User


@pytest.fixture
async def e2e_db_session():
    """
    Create database session for E2E tests.
    Commits are real but we clean up after ourselves.
    """
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

    # Use same database as app (real integration)
    db_url = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
    engine = create_async_engine(db_url, echo=False)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def e2e_test_user(e2e_db_session):
    """
    Create a test user with NO projects for onboarding testing.
    Returns (user_id, username, password) tuple.
    Cleans up after test.
    """
    user_id = str(uuid4())
    username = f"e2e_onboard_{user_id[:8]}"
    email = f"{username}@test.example.com"
    password = "testpass123"

    # Hash password
    from services.auth.password_service import PasswordService

    ps = PasswordService()
    password_hash = ps.hash_password(password)

    # Insert user directly and COMMIT so auth route can see it
    await e2e_db_session.execute(
        text(
            """
            INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                               created_at, updated_at, role, is_alpha)
            VALUES (:id, :username, :email, :password_hash, true, true, :now, :now, 'user', true)
        """
        ),
        {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "now": datetime.now(timezone.utc),
        },
    )
    await e2e_db_session.commit()

    # Verify user has NO projects
    result = await e2e_db_session.execute(
        text("SELECT COUNT(*) FROM projects WHERE owner_id = :user_id"),
        {"user_id": user_id},
    )
    project_count = result.scalar()
    assert project_count == 0, f"Test user should have 0 projects, has {project_count}"

    yield user_id, username, password

    # Cleanup: Delete test user after test
    await e2e_db_session.execute(
        text("DELETE FROM users WHERE id = :user_id"),
        {"user_id": user_id},
    )
    await e2e_db_session.commit()


@pytest.fixture
async def e2e_client():
    """
    HTTP client that uses the REAL app with full startup lifecycle.

    This is a TRUE E2E client - it boots the real FastAPI app with all
    middleware, routes, services, and database connections exactly as
    they would be in production.

    Uses lifespan context manager to trigger startup/shutdown events.
    """
    from contextlib import asynccontextmanager

    from httpx import ASGITransport

    from web.app import app

    # Trigger the lifespan startup events
    @asynccontextmanager
    async def lifespan_wrapper():
        async with app.router.lifespan_context(app):
            yield

    async with lifespan_wrapper():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


class TestOnboardingHTTPE2E:
    """
    TRUE E2E tests for portfolio onboarding.

    These tests reproduce the exact manual testing flow:
    1. Login
    2. Send greeting
    3. Send project info
    4. Verify responses
    """

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_new_user_greeting_triggers_onboarding(
        self, e2e_client, e2e_test_user, e2e_db_session
    ):
        """
        Issue #490: New user saying 'Hello' should trigger onboarding.

        This is the FIRST manual test that kept failing.
        If this passes, the greeting->onboarding path works.
        """
        user_id, username, password = e2e_test_user

        # Step 1: Login
        login_response = await e2e_client.post(
            "/auth/login",
            data={"username": username, "password": password},
        )
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"

        # Get auth cookie
        cookies = login_response.cookies

        # Step 2: Send greeting via /api/v1/intent
        intent_response = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hello", "session_id": "test-session"},
            cookies=cookies,
        )

        assert intent_response.status_code == 200, f"Intent failed: {intent_response.text}"
        result = intent_response.json()

        # Step 3: Verify onboarding is triggered
        # The response message should contain onboarding prompt
        message = result.get("message", "").lower()

        # MUST contain onboarding indicators
        assert any(
            phrase in message
            for phrase in ["project portfolio", "projects you're working on", "set up"]
        ), f"Expected onboarding prompt, got: {result.get('message')}"

        # MUST NOT be the identity response
        assert (
            "i'm piper morgan" not in message or "portfolio" in message
        ), f"Got identity response instead of onboarding: {result.get('message')}"

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_project_info_not_echoed(self, e2e_client, e2e_test_user, e2e_db_session):
        """
        Issue #560: User providing project info should NOT be echoed back.

        This catches the echo bug that was found via manual testing.
        """
        user_id, username, password = e2e_test_user

        # Login
        login_response = await e2e_client.post(
            "/auth/login",
            data={"username": username, "password": password},
        )
        cookies = login_response.cookies

        # Send greeting first (to trigger onboarding)
        await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hello", "session_id": "test-session"},
            cookies=cookies,
        )

        # Now send project info
        project_message = "My main project is called Piper Morgan"
        intent_response = await e2e_client.post(
            "/api/v1/intent",
            json={"message": project_message, "session_id": "test-session"},
            cookies=cookies,
        )

        assert intent_response.status_code == 200
        result = intent_response.json()
        response_message = result.get("message", "")

        # CRITICAL: Response should NOT echo user's exact input
        assert (
            response_message.lower() != project_message.lower()
        ), f"ECHO BUG: Response echoed user input verbatim: {response_message}"

        # Response should NOT be the identity response
        assert (
            "i'm piper morgan, your ai product management" not in response_message.lower()
        ), f"Got identity response instead of onboarding continuation: {response_message}"

        # Response should acknowledge the project (ideal case)
        # Or at least be a reasonable response (not echo, not error)
        assert len(response_message) > 10, f"Response too short: {response_message}"

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_full_onboarding_flow(self, e2e_client, e2e_test_user, e2e_db_session):
        """
        Issue #490: Complete onboarding flow from greeting to project capture.

        This is the full happy path that users should experience.
        """
        user_id, username, password = e2e_test_user

        # Login
        login_response = await e2e_client.post(
            "/auth/login",
            data={"username": username, "password": password},
        )
        cookies = login_response.cookies
        session_id = f"e2e-{uuid4()}"

        # Turn 1: Greeting -> Onboarding prompt
        response1 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hi there!", "session_id": session_id},
            cookies=cookies,
        )
        result1 = response1.json()
        msg1 = result1.get("message", "").lower()

        assert (
            "portfolio" in msg1 or "project" in msg1
        ), f"Turn 1: Expected onboarding, got: {result1.get('message')}"

        # Turn 2: User accepts -> Should ask for project
        response2 = await e2e_client.post(
            "/api/v1/intent",
            json={
                "message": "Yes, I'd like to tell you about my projects",
                "session_id": session_id,
            },
            cookies=cookies,
        )
        result2 = response2.json()
        msg2 = result2.get("message", "")

        # Should NOT echo
        assert "yes, i'd like" not in msg2.lower(), f"Turn 2: Echo detected: {msg2}"
        # Should NOT be identity
        assert "i'm piper morgan, your ai" not in msg2.lower(), f"Turn 2: Wrong response: {msg2}"

        # Turn 3: User provides project info
        response3 = await e2e_client.post(
            "/api/v1/intent",
            json={
                "message": "The main one is Piper Morgan, a PM assistant",
                "session_id": session_id,
            },
            cookies=cookies,
        )
        result3 = response3.json()
        msg3 = result3.get("message", "")

        # Should NOT be verbatim echo (exact message returned)
        # Note: The handler may include project name in acknowledgment - that's OK
        assert (
            msg3.lower() != "the main one is piper morgan, a pm assistant"
        ), f"Turn 3: Verbatim echo detected: {msg3}"
        # Should NOT be identity response
        assert (
            "i'm piper morgan, your ai" not in msg3.lower()
        ), f"Turn 3: Got identity response instead of onboarding: {msg3}"
        # Should acknowledge project (start with "Got it" or similar)
        assert msg3.lower().startswith(
            "got it"
        ), f"Turn 3: Expected project acknowledgment, got: {msg3}"


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_degradation_response_not_echo(e2e_client):
    """
    Issue #560: Even error responses should NOT echo user input.

    When services fail, the degradation message should be shown,
    not the user's original message.
    """
    # Send request without auth (will trigger some error path)
    response = await e2e_client.post(
        "/api/v1/intent",
        json={"message": "Test message that should not be echoed", "session_id": "test"},
    )

    result = response.json()
    message = result.get("message", "")

    # Even if it errors, should NOT echo
    assert (
        message != "Test message that should not be echoed"
    ), f"Error response echoed user input: {message}"

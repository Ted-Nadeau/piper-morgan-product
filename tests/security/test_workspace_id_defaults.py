"""Workspace ID default value tests.

Issue #734: SEC-MULTITENANCY - Verify workspace_id has sensible defaults
for single-tenant deployments while supporting future multi-tenant use.
"""

from uuid import UUID

import pytest

from services.auth.jwt_service import JWTClaims
from services.domain.models import DEFAULT_WORKSPACE_ID, RequestContext


def make_jwt_claims(
    sub: str = None,
    user_email: str = "test@example.com",
    workspace_id: str = None,
) -> JWTClaims:
    """Helper to create JWTClaims with all required fields."""
    from datetime import datetime, timezone
    from uuid import uuid4

    user_id = str(uuid4())
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub=sub or user_id,  # Must be valid UUID string
        iat=datetime.now(timezone.utc),
        exp=datetime.now(timezone.utc),
        jti=str(uuid4()),
        user_email=user_email,
        username="testuser",
        user_id=user_id,
        token_type="access",
        scopes=["user"],
        session_id=str(uuid4()),
        workspace_id=workspace_id,
    )


class TestDefaultWorkspaceId:
    """Verify DEFAULT_WORKSPACE_ID constant exists and is valid."""

    def test_default_workspace_id_exists(self):
        """DEFAULT_WORKSPACE_ID constant should be defined."""
        assert DEFAULT_WORKSPACE_ID is not None

    def test_default_workspace_id_is_uuid(self):
        """DEFAULT_WORKSPACE_ID should be a valid UUID."""
        assert isinstance(DEFAULT_WORKSPACE_ID, UUID)

    def test_default_workspace_id_is_deterministic(self):
        """DEFAULT_WORKSPACE_ID should be the same across imports."""
        from services.domain.models import DEFAULT_WORKSPACE_ID as ws1
        from services.domain.models import DEFAULT_WORKSPACE_ID as ws2

        assert ws1 == ws2


class TestRequestContextWorkspaceDefaults:
    """Verify RequestContext uses default workspace when not provided."""

    def test_context_uses_default_workspace_when_none(self):
        """RequestContext should use DEFAULT_WORKSPACE_ID when claims.workspace_id is None."""
        claims = make_jwt_claims(workspace_id=None)
        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=str(UUID("11111111-1111-1111-1111-111111111111")),
        )
        assert ctx.workspace_id == DEFAULT_WORKSPACE_ID

    def test_context_uses_provided_workspace_when_present(self):
        """RequestContext should use provided workspace_id from claims."""
        custom_workspace = "22222222-2222-2222-2222-222222222222"
        claims = make_jwt_claims(workspace_id=custom_workspace)
        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=str(UUID("11111111-1111-1111-1111-111111111111")),
        )
        assert ctx.workspace_id == UUID(custom_workspace)

    def test_context_workspace_is_never_none(self):
        """RequestContext.workspace_id should never be None after construction."""
        claims = make_jwt_claims(workspace_id=None)
        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=str(UUID("11111111-1111-1111-1111-111111111111")),
        )
        assert ctx.workspace_id is not None


class TestWorkspaceIdForMultiTenancy:
    """Verify workspace_id properly isolates data for multi-tenant scenarios."""

    def test_different_workspaces_have_different_ids(self):
        """Different workspace_id values should create different contexts."""
        workspace_a = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        workspace_b = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"

        claims_a = make_jwt_claims(workspace_id=workspace_a)
        claims_b = make_jwt_claims(workspace_id=workspace_b)

        ctx_a = RequestContext.from_jwt_and_request(
            claims=claims_a,
            conversation_id=str(UUID("11111111-1111-1111-1111-111111111111")),
        )
        ctx_b = RequestContext.from_jwt_and_request(
            claims=claims_b,
            conversation_id=str(UUID("11111111-1111-1111-1111-111111111111")),
        )

        assert ctx_a.workspace_id != ctx_b.workspace_id
        assert ctx_a.workspace_id == UUID(workspace_a)
        assert ctx_b.workspace_id == UUID(workspace_b)

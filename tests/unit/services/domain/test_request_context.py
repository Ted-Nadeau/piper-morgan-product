"""
Unit tests for RequestContext - ADR-051: Unified User Session Context

Tests verify the RequestContext model:
- Creation via constructor
- Creation via factory method
- Immutability (frozen dataclass)
- Validation in factory
- String representation
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from services.domain.models import RequestContext


class TestRequestContextCreation:
    """Tests for RequestContext creation and basic functionality."""

    def test_create_request_context_with_all_fields(self):
        """RequestContext can be created with all required fields."""
        user_id = uuid4()
        conversation_id = uuid4()
        request_id = uuid4()
        timestamp = datetime.now(timezone.utc)

        ctx = RequestContext(
            user_id=user_id,
            conversation_id=conversation_id,
            request_id=request_id,
            user_email="test@example.com",
            timestamp=timestamp,
        )

        assert ctx.user_id == user_id
        assert ctx.conversation_id == conversation_id
        assert ctx.request_id == request_id
        assert ctx.user_email == "test@example.com"
        assert ctx.timestamp == timestamp
        assert ctx.workspace_id is None  # Optional, defaults to None

    def test_create_request_context_with_workspace_id(self):
        """RequestContext can include optional workspace_id."""
        workspace_id = uuid4()

        ctx = RequestContext(
            user_id=uuid4(),
            conversation_id=uuid4(),
            request_id=uuid4(),
            user_email="test@example.com",
            timestamp=datetime.now(timezone.utc),
            workspace_id=workspace_id,
        )

        assert ctx.workspace_id == workspace_id

    def test_request_context_is_immutable(self):
        """RequestContext is frozen (immutable) - cannot modify after creation."""
        ctx = RequestContext(
            user_id=uuid4(),
            conversation_id=uuid4(),
            request_id=uuid4(),
            user_email="test@example.com",
            timestamp=datetime.now(timezone.utc),
        )

        # Attempting to modify should raise FrozenInstanceError
        with pytest.raises(Exception):  # FrozenInstanceError is a subclass
            ctx.user_id = uuid4()

    def test_request_context_str_representation(self):
        """RequestContext has useful string representation for logging."""
        user_id = uuid4()
        conversation_id = uuid4()
        request_id = uuid4()

        ctx = RequestContext(
            user_id=user_id,
            conversation_id=conversation_id,
            request_id=request_id,
            user_email="test@example.com",
            timestamp=datetime.now(timezone.utc),
        )

        str_repr = str(ctx)
        assert "RequestContext" in str_repr
        assert str(user_id) in str_repr
        assert str(conversation_id) in str_repr
        assert str(request_id) in str_repr


class TestRequestContextFactory:
    """Tests for RequestContext.from_jwt_and_request factory method."""

    def _mock_jwt_claims(
        self,
        sub: str = None,
        user_email: str = "test@example.com",
        workspace_id: str = None,
    ) -> MagicMock:
        """Create a mock JWTClaims object."""
        claims = MagicMock()
        # Use explicit None check - empty string should pass through for validation tests
        claims.sub = str(uuid4()) if sub is None else sub
        claims.user_email = user_email
        claims.workspace_id = workspace_id
        return claims

    def test_from_jwt_and_request_creates_context(self):
        """Factory method creates RequestContext from JWT claims."""
        claims = self._mock_jwt_claims()
        conversation_id = str(uuid4())

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=conversation_id,
        )

        assert ctx.user_id == UUID(claims.sub)
        assert ctx.conversation_id == UUID(conversation_id)
        assert ctx.user_email == claims.user_email
        assert ctx.request_id is not None  # Auto-generated
        assert ctx.timestamp is not None

    def test_from_jwt_and_request_with_explicit_request_id(self):
        """Factory method can accept explicit request_id."""
        claims = self._mock_jwt_claims()
        conversation_id = str(uuid4())
        request_id = uuid4()

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=conversation_id,
            request_id=request_id,
        )

        assert ctx.request_id == request_id

    def test_from_jwt_and_request_with_workspace_id(self):
        """Factory method handles workspace_id from claims."""
        workspace_id = str(uuid4())
        claims = self._mock_jwt_claims(workspace_id=workspace_id)
        conversation_id = str(uuid4())

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=conversation_id,
        )

        assert ctx.workspace_id == UUID(workspace_id)

    def test_from_jwt_and_request_validates_sub(self):
        """Factory method fails fast if claims.sub is missing."""
        claims = self._mock_jwt_claims(sub="")  # Empty string
        conversation_id = str(uuid4())

        with pytest.raises(ValueError, match="JWT claims missing 'sub' field"):
            RequestContext.from_jwt_and_request(
                claims=claims,
                conversation_id=conversation_id,
            )

    def test_from_jwt_and_request_validates_conversation_id(self):
        """Factory method fails fast if conversation_id is missing."""
        claims = self._mock_jwt_claims()

        with pytest.raises(ValueError, match="conversation_id is required"):
            RequestContext.from_jwt_and_request(
                claims=claims,
                conversation_id="",  # Empty string
            )

    def test_from_jwt_and_request_converts_str_to_uuid(self):
        """Factory method converts string IDs to UUID at boundary."""
        user_id_str = str(uuid4())
        conversation_id_str = str(uuid4())

        claims = self._mock_jwt_claims(sub=user_id_str)

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=conversation_id_str,
        )

        # Verify types are UUID, not str
        assert isinstance(ctx.user_id, UUID)
        assert isinstance(ctx.conversation_id, UUID)
        assert isinstance(ctx.request_id, UUID)


class TestRequestContextTypeConsistency:
    """Tests for type consistency as defined in ADR-051."""

    def test_all_ids_are_uuid_type(self):
        """All ID fields should be UUID type internally."""
        ctx = RequestContext(
            user_id=uuid4(),
            conversation_id=uuid4(),
            request_id=uuid4(),
            user_email="test@example.com",
            timestamp=datetime.now(timezone.utc),
            workspace_id=uuid4(),
        )

        assert isinstance(ctx.user_id, UUID)
        assert isinstance(ctx.conversation_id, UUID)
        assert isinstance(ctx.request_id, UUID)
        assert isinstance(ctx.workspace_id, UUID)

    def test_timestamp_is_timezone_aware(self):
        """Timestamp should be timezone-aware (UTC)."""
        claims = MagicMock()
        claims.sub = str(uuid4())
        claims.user_email = "test@example.com"
        claims.workspace_id = None

        ctx = RequestContext.from_jwt_and_request(
            claims=claims,
            conversation_id=str(uuid4()),
        )

        # Timestamp should have tzinfo set
        assert ctx.timestamp.tzinfo is not None

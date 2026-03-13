# Code Implementation Prompt: Comprehensive Audit Logging System

**Agent**: Code (Lead Developer)
**Issue**: #249 CORE-AUDIT-LOGGING
**Task**: Implement comprehensive audit trail system for security and compliance
**Date**: October 22, 2025, 9:27 AM
**Estimated Duration**: 15 hours → Target 2-3 hours actual

---

## Mission

**Goal**: Implement production-ready audit logging system with complete integration into JWT authentication and API key management.

**Your responsibilities**:
- ✅ Create AuditLog model and migration
- ✅ Implement AuditLogger service
- ✅ Integrate with JWT authentication service
- ✅ Integrate with UserAPIKeyService
- ✅ Create REST API endpoints for log queries
- ✅ Write comprehensive tests
- ✅ Document all integrations

---

## Context from Cursor's Investigation

**Infrastructure Analysis**: `dev/2025/10/22/audit-logging-infrastructure-analysis.md` (876 lines)

**Key Findings**:
1. ✅ User model already prepared with commented audit_logs relationship
2. ✅ JWT service has perfect token lifecycle methods
3. ✅ UserAPIKeyService has all integration points
4. ✅ Consistent patterns: String(255) PKs, TimestampMixin, JSON columns
5. ✅ FastAPI provides request context (IP, user_agent, path)

**Integration Strategy**: Explicit context passing from routes → services → audit

---

## Phase 1: Core Infrastructure (3 hours)

### 1.1 Add AuditLog Model to services/database/models.py

**Location**: Add to existing `services/database/models.py`

**Model Specification** (from Cursor's analysis):

```python
from sqlalchemy import Column, String, DateTime, Text, Index, ForeignKey, JSON
from datetime import datetime
import uuid

class AuditLog(Base, TimestampMixin):
    """Comprehensive audit trail for security and compliance

    Tracks all security-relevant events including:
    - Authentication (login, logout, token operations)
    - API key management (store, retrieve, delete, rotate)
    - Data modifications
    - Security events
    """
    __tablename__ = "audit_logs"

    # Identity (follow User model pattern - String primary key)
    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(String(255), nullable=True, index=True)

    # Event classification
    event_type = Column(String(50), nullable=False, index=True)  # auth, api_key, data, system
    action = Column(String(100), nullable=False, index=True)     # login, logout, store_key, etc
    resource_type = Column(String(50), nullable=True, index=True)  # user, api_key, token, etc
    resource_id = Column(String(255), nullable=True, index=True)   # Specific resource identifier

    # Event details
    status = Column(String(20), nullable=False, index=True)      # success, failed, error
    severity = Column(String(20), nullable=False, index=True)    # info, warning, error, critical
    message = Column(Text, nullable=False)                       # Human-readable description
    details = Column(JSON, nullable=True)                        # Additional structured data

    # Request context
    ip_address = Column(String(45), nullable=True, index=True)   # IPv4/IPv6 support
    user_agent = Column(String(500), nullable=True)             # Browser/client info
    request_id = Column(String(255), nullable=True, index=True) # Request correlation
    request_path = Column(String(500), nullable=True)           # API endpoint called

    # Change tracking
    old_value = Column(JSON, nullable=True)                      # Previous state
    new_value = Column(JSON, nullable=True)                      # New state

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    # Strategic indexes for query performance
    __table_args__ = (
        Index("idx_audit_user_date", "user_id", "created_at"),
        Index("idx_audit_event_type", "event_type"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_severity", "severity"),
        Index("idx_audit_status", "status"),
        Index("idx_audit_ip", "ip_address"),
        Index("idx_audit_session", "session_id"),
        Index("idx_audit_request", "request_id"),
    )

    def __repr__(self):
        return (
            f"<AuditLog(id={self.id}, event_type={self.event_type}, "
            f"action={self.action}, user_id={self.user_id}, status={self.status})>"
        )
```

**Also update User model**:
```python
# In User model, uncomment the relationship:
audit_logs = relationship("AuditLog", back_populates="user")
```

### 1.2 Create Migration

**File**: `alembic/versions/[timestamp]_add_audit_logging_issue_249.py`

**Migration Content**:
```python
"""Add audit logging for Issue #249

Revision ID: [auto-generated]
Revises: [previous_revision]
Create Date: 2025-10-22 09:27:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '[auto-generated]'
down_revision = '[previous_revision]'
branch_labels = None
depends_on = None


def upgrade():
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=True),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=True),
        sa.Column('resource_id', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('request_id', sa.String(length=255), nullable=True),
        sa.Column('request_path', sa.String(length=500), nullable=True),
        sa.Column('old_value', sa.JSON(), nullable=True),
        sa.Column('new_value', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_audit_user_date', 'audit_logs', ['user_id', 'created_at'])
    op.create_index('idx_audit_event_type', 'audit_logs', ['event_type'])
    op.create_index('idx_audit_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_resource', 'audit_logs', ['resource_type', 'resource_id'])
    op.create_index('idx_audit_severity', 'audit_logs', ['severity'])
    op.create_index('idx_audit_status', 'audit_logs', ['status'])
    op.create_index('idx_audit_ip', 'audit_logs', ['ip_address'])
    op.create_index('idx_audit_session', 'audit_logs', ['session_id'])
    op.create_index('idx_audit_request', 'audit_logs', ['request_id'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_audit_request', table_name='audit_logs')
    op.drop_index('idx_audit_session', table_name='audit_logs')
    op.drop_index('idx_audit_ip', table_name='audit_logs')
    op.drop_index('idx_audit_status', table_name='audit_logs')
    op.drop_index('idx_audit_severity', table_name='audit_logs')
    op.drop_index('idx_audit_resource', table_name='audit_logs')
    op.drop_index('idx_audit_action', table_name='audit_logs')
    op.drop_index('idx_audit_event_type', table_name='audit_logs')
    op.drop_index('idx_audit_user_date', table_name='audit_logs')

    # Drop table
    op.drop_table('audit_logs')
```

### 1.3 Create AuditLogger Service

**File**: `services/security/audit_logger.py` (NEW)

```python
"""Audit logging service for security and compliance tracking

Provides comprehensive audit trail for:
- Authentication events (login, logout, token operations)
- API key management (store, retrieve, delete, rotate)
- Data modifications
- Security events

Usage:
    from services.security.audit_logger import audit_logger, EventType, Action, Severity

    # Log authentication event
    await audit_logger.log_auth_event(
        action=Action.LOGIN,
        user_id="user123",
        status="success",
        session=session,
        audit_context={"ip_address": "192.168.1.1", "user_agent": "Mozilla..."}
    )

    # Log API key event
    await audit_logger.log_api_key_event(
        action=Action.KEY_STORED,
        user_id="user123",
        provider="openai",
        status="success",
        session=session,
        audit_context=request_context
    )
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from services.database.models import AuditLog

logger = logging.getLogger(__name__)


class EventType:
    """Audit event type constants"""
    AUTH = "auth"              # Authentication events
    API_KEY = "api_key"        # API key operations
    DATA = "data"              # Data modifications
    SYSTEM = "system"          # System events
    SECURITY = "security"      # Security events


class Action:
    """Audit action constants"""
    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    TOKEN_ISSUED = "token_issued"
    TOKEN_REVOKED = "token_revoked"
    TOKEN_REFRESHED = "token_refreshed"

    # API Keys
    KEY_STORED = "key_stored"
    KEY_RETRIEVED = "key_retrieved"
    KEY_DELETED = "key_deleted"
    KEY_ROTATED = "key_rotated"
    KEY_VALIDATED = "key_validated"

    # Data Operations
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    EXPORTED = "exported"

    # Security Events
    PERMISSION_DENIED = "permission_denied"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"


class Severity:
    """Audit severity levels"""
    INFO = "info"        # Normal operations
    WARNING = "warning"  # Potential issues
    ERROR = "error"      # Errors that need attention
    CRITICAL = "critical"  # Critical security/system events


class AuditLogger:
    """Centralized audit logging service"""

    async def log_event(
        self,
        event_type: str,
        action: str,
        status: str,
        severity: str,
        message: str,
        session: AsyncSession,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log a comprehensive audit event

        Args:
            event_type: Type of event (auth, api_key, data, system, security)
            action: Specific action (login, key_stored, etc)
            status: Event status (success, failed, error)
            severity: Event severity (info, warning, error, critical)
            message: Human-readable message
            session: Database session
            user_id: User ID if applicable
            session_id: Session ID if applicable
            resource_type: Resource type being acted upon
            resource_id: Specific resource identifier
            details: Additional structured data
            old_value: Previous state for modifications
            new_value: New state for modifications
            audit_context: Request context (ip_address, user_agent, etc)

        Returns:
            Created AuditLog instance
        """
        # Extract request context
        context = audit_context or {}

        # Create audit log entry
        log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            event_type=event_type,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            severity=severity,
            message=message,
            details=details,
            old_value=old_value,
            new_value=new_value,
            ip_address=context.get("ip_address"),
            user_agent=context.get("user_agent"),
            request_id=context.get("request_id"),
            request_path=context.get("request_path")
        )

        # Store in database
        session.add(log)
        await session.flush()  # Don't commit - let caller handle transaction

        # Log to application logs as well
        logger.info(
            f"AUDIT: {event_type}.{action} | user={user_id} | status={status} | "
            f"message={message}",
            extra={
                "audit_log_id": log.id,
                "event_type": event_type,
                "action": action,
                "user_id": user_id,
                "status": status,
                "severity": severity
            }
        )

        return log

    async def log_auth_event(
        self,
        action: str,
        status: str,
        message: str,
        session: AsyncSession,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Convenience method for authentication events

        Args:
            action: Auth action (login, logout, token_issued, etc)
            status: Event status (success, failed)
            message: Human-readable message
            session: Database session
            user_id: User ID
            session_id: Session ID if applicable
            details: Additional data (username, reason, etc)
            audit_context: Request context

        Returns:
            Created AuditLog instance
        """
        severity = Severity.WARNING if status == "failed" else Severity.INFO

        return await self.log_event(
            event_type=EventType.AUTH,
            action=action,
            status=status,
            severity=severity,
            message=message,
            session=session,
            user_id=user_id,
            session_id=session_id,
            resource_type="auth",
            details=details,
            audit_context=audit_context
        )

    async def log_api_key_event(
        self,
        action: str,
        provider: str,
        status: str,
        message: str,
        session: AsyncSession,
        user_id: str,
        details: Optional[Dict[str, Any]] = None,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Convenience method for API key events

        Args:
            action: API key action (key_stored, key_rotated, etc)
            provider: Provider name (openai, anthropic, etc)
            status: Event status (success, failed)
            message: Human-readable message
            session: Database session
            user_id: User ID
            details: Additional data (keychain_ref, validation result, etc)
            old_value: Previous state for rotations
            new_value: New state for rotations
            audit_context: Request context

        Returns:
            Created AuditLog instance
        """
        # Add provider to details
        event_details = details or {}
        event_details["provider"] = provider

        return await self.log_event(
            event_type=EventType.API_KEY,
            action=action,
            status=status,
            severity=Severity.INFO,
            message=message,
            session=session,
            user_id=user_id,
            resource_type="api_key",
            resource_id=provider,
            details=event_details,
            old_value=old_value,
            new_value=new_value,
            audit_context=audit_context
        )

    async def log_security_event(
        self,
        action: str,
        severity: str,
        message: str,
        session: AsyncSession,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        audit_context: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Convenience method for security events

        Args:
            action: Security action (permission_denied, suspicious_activity, etc)
            severity: Event severity (warning, error, critical)
            message: Human-readable message
            session: Database session
            user_id: User ID if applicable
            details: Additional data (attempted action, detection reason, etc)
            audit_context: Request context

        Returns:
            Created AuditLog instance
        """
        return await self.log_event(
            event_type=EventType.SECURITY,
            action=action,
            status="detected",
            severity=severity,
            message=message,
            session=session,
            user_id=user_id,
            resource_type="security",
            details=details,
            audit_context=audit_context
        )


# Global instance
audit_logger = AuditLogger()
```

### 1.4 Unit Tests

**File**: `tests/security/test_audit_logger.py` (NEW)

```python
"""Unit tests for audit logger"""

import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from services.security.audit_logger import (
    audit_logger,
    EventType,
    Action,
    Severity
)
from services.database.models import AuditLog


class TestAuditLogger:
    """Test audit logging functionality"""

    @pytest.mark.asyncio
    async def test_log_auth_event_success(self, async_session: AsyncSession):
        """Test successful authentication event logging"""
        result = await audit_logger.log_auth_event(
            action=Action.LOGIN,
            status="success",
            message="User logged in successfully",
            session=async_session,
            user_id="test_user",
            session_id="test_session",
            details={"username": "testuser"},
            audit_context={
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0",
                "request_id": "req_123",
                "request_path": "/api/v1/auth/login"
            }
        )

        assert result.event_type == EventType.AUTH
        assert result.action == Action.LOGIN
        assert result.user_id == "test_user"
        assert result.session_id == "test_session"
        assert result.status == "success"
        assert result.severity == Severity.INFO
        assert result.message == "User logged in successfully"
        assert result.details["username"] == "testuser"
        assert result.ip_address == "192.168.1.1"
        assert result.user_agent == "Mozilla/5.0"
        assert result.request_id == "req_123"
        assert result.request_path == "/api/v1/auth/login"
        assert result.created_at is not None

    @pytest.mark.asyncio
    async def test_log_auth_event_failure(self, async_session: AsyncSession):
        """Test failed authentication event logging"""
        result = await audit_logger.log_auth_event(
            action=Action.LOGIN_FAILED,
            status="failed",
            message="Invalid credentials",
            session=async_session,
            user_id=None,  # No user_id for failed login
            details={"username": "testuser", "reason": "invalid_password"},
            audit_context={"ip_address": "192.168.1.1"}
        )

        assert result.event_type == EventType.AUTH
        assert result.action == Action.LOGIN_FAILED
        assert result.user_id is None
        assert result.status == "failed"
        assert result.severity == Severity.WARNING
        assert result.details["reason"] == "invalid_password"

    @pytest.mark.asyncio
    async def test_log_api_key_event(self, async_session: AsyncSession):
        """Test API key event logging"""
        result = await audit_logger.log_api_key_event(
            action=Action.KEY_STORED,
            provider="openai",
            status="success",
            message="API key stored successfully",
            session=async_session,
            user_id="test_user",
            details={"keychain_ref": "test_user_openai_api_key"},
            audit_context={"ip_address": "192.168.1.1"}
        )

        assert result.event_type == EventType.API_KEY
        assert result.action == Action.KEY_STORED
        assert result.resource_type == "api_key"
        assert result.resource_id == "openai"
        assert result.details["provider"] == "openai"
        assert result.details["keychain_ref"] == "test_user_openai_api_key"

    @pytest.mark.asyncio
    async def test_log_api_key_rotation(self, async_session: AsyncSession):
        """Test API key rotation with old/new values"""
        result = await audit_logger.log_api_key_event(
            action=Action.KEY_ROTATED,
            provider="openai",
            status="success",
            message="API key rotated successfully",
            session=async_session,
            user_id="test_user",
            old_value={"keychain_ref": "old_ref", "rotated_at": "2025-07-22T00:00:00Z"},
            new_value={"keychain_ref": "new_ref", "rotated_at": "2025-10-22T09:27:00Z"},
            audit_context={"ip_address": "192.168.1.1"}
        )

        assert result.action == Action.KEY_ROTATED
        assert result.old_value["keychain_ref"] == "old_ref"
        assert result.new_value["keychain_ref"] == "new_ref"

    @pytest.mark.asyncio
    async def test_log_security_event(self, async_session: AsyncSession):
        """Test security event logging"""
        result = await audit_logger.log_security_event(
            action=Action.SUSPICIOUS_ACTIVITY,
            severity=Severity.CRITICAL,
            message="Multiple failed login attempts detected",
            session=async_session,
            user_id="test_user",
            details={
                "failed_attempts": 5,
                "time_window": "5_minutes",
                "ip_addresses": ["192.168.1.1", "10.0.0.1"]
            },
            audit_context={"ip_address": "192.168.1.1"}
        )

        assert result.event_type == EventType.SECURITY
        assert result.action == Action.SUSPICIOUS_ACTIVITY
        assert result.severity == Severity.CRITICAL
        assert result.details["failed_attempts"] == 5
```

---

## Phase 2: Authentication Integration (2 hours)

### 2.1 Integrate with JWT Service

**File**: `services/auth/jwt_service.py`

**Add audit logging to token lifecycle methods:**

```python
from services.security.audit_logger import audit_logger, Action

# Add to create_token method
async def create_token(
    self,
    user_id: str,
    token_type: TokenType,
    session: Optional[AsyncSession] = None,
    audit_context: Optional[Dict[str, Any]] = None
) -> str:
    """Create JWT token with audit logging"""
    # Existing token creation logic...
    token = await self._generate_token(...)

    # Audit log
    if session:
        await audit_logger.log_auth_event(
            action=Action.TOKEN_ISSUED,
            status="success",
            message=f"{token_type.value} token issued for user {user_id}",
            session=session,
            user_id=user_id,
            details={
                "token_type": token_type.value,
                "token_id": claims.jti,
                "expires_at": claims.exp.isoformat()
            },
            audit_context=audit_context
        )

    return token

# Add to revoke_token method
async def revoke_token(
    self,
    token_id: str,
    reason: str,
    session: AsyncSession,
    audit_context: Optional[Dict[str, Any]] = None
) -> bool:
    """Revoke token with audit logging"""
    # Get token info before revoking
    claims = await self.validate_token(token_id)

    # Existing revocation logic...
    success = await self._revoke_token_internal(...)

    # Audit log
    await audit_logger.log_auth_event(
        action=Action.TOKEN_REVOKED,
        status="success" if success else "failed",
        message=f"Token revoked: {reason}",
        session=session,
        user_id=claims.user_id if claims else None,
        details={
            "token_id": token_id,
            "reason": reason
        },
        audit_context=audit_context
    )

    return success
```

### 2.2 Integration Tests for Auth Auditing

**File**: `tests/security/integration_test_audit_auth.py` (NEW)

```python
"""Integration tests for authentication audit logging"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.jwt_service import JWTService, TokenType
from services.security.audit_logger import Action, EventType
from services.database.models import AuditLog


class TestAuthAudit:
    """Test authentication audit trail"""

    @pytest.mark.asyncio
    async def test_token_creation_audited(self, async_session: AsyncSession):
        """Test that token creation is audited"""
        jwt_service = JWTService()

        audit_context = {
            "ip_address": "192.168.1.1",
            "user_agent": "test_client",
            "request_id": "req_123"
        }

        # Create token (should trigger audit)
        token = await jwt_service.create_token(
            user_id="test_user",
            token_type=TokenType.ACCESS,
            session=async_session,
            audit_context=audit_context
        )

        await async_session.commit()

        # Verify audit log was created
        result = await async_session.execute(
            select(AuditLog).where(
                AuditLog.event_type == EventType.AUTH,
                AuditLog.action == Action.TOKEN_ISSUED,
                AuditLog.user_id == "test_user"
            )
        )
        log = result.scalar_one()

        assert log.status == "success"
        assert log.details["token_type"] == "access"
        assert log.ip_address == "192.168.1.1"

    @pytest.mark.asyncio
    async def test_token_revocation_audited(self, async_session: AsyncSession):
        """Test that token revocation is audited"""
        jwt_service = JWTService()

        # Create and revoke token
        token = await jwt_service.create_token(
            user_id="test_user",
            token_type=TokenType.ACCESS,
            session=async_session
        )

        claims = await jwt_service.validate_token(token)

        await jwt_service.revoke_token(
            token_id=claims.jti,
            reason="logout",
            session=async_session,
            audit_context={"ip_address": "192.168.1.1"}
        )

        await async_session.commit()

        # Verify revocation was audited
        result = await async_session.execute(
            select(AuditLog).where(
                AuditLog.action == Action.TOKEN_REVOKED,
                AuditLog.user_id == "test_user"
            )
        )
        log = result.scalar_one()

        assert log.status == "success"
        assert log.details["reason"] == "logout"
```

---

## Phase 3: API Key Service Integration (3 hours)

### 3.1 Integrate with UserAPIKeyService

**File**: `services/security/user_api_key_service.py`

**Add audit logging to all CRUD methods:**

```python
from services.security.audit_logger import audit_logger, Action

# In store_user_key method
async def store_user_key(
    self,
    user_id: str,
    provider: str,
    api_key: str,
    session: Optional[AsyncSession] = None,
    audit_context: Optional[Dict[str, Any]] = None
) -> UserAPIKey:
    """Store API key with audit logging"""
    # Existing storage logic...
    result = await self._store_key_internal(...)

    # Audit log
    if session:
        await audit_logger.log_api_key_event(
            action=Action.KEY_STORED,
            provider=provider,
            status="success",
            message=f"API key stored for {provider}",
            session=session,
            user_id=user_id,
            details={
                "keychain_ref": result.encrypted_key_ref,
                "validated": True
            },
            audit_context=audit_context
        )

    return result

# In rotate_user_key method
async def rotate_user_key(
    self,
    user_id: str,
    provider: str,
    new_api_key: str,
    session: Optional[AsyncSession] = None,
    audit_context: Optional[Dict[str, Any]] = None
) -> UserAPIKey:
    """Rotate API key with audit logging"""
    # Get old key info
    old_key = await self.retrieve_user_key(user_id, provider, session)
    old_ref = old_key.encrypted_key_ref if old_key else None

    # Existing rotation logic...
    result = await self._rotate_key_internal(...)

    # Audit log
    if session:
        await audit_logger.log_api_key_event(
            action=Action.KEY_ROTATED,
            provider=provider,
            status="success",
            message=f"API key rotated for {provider}",
            session=session,
            user_id=user_id,
            old_value={"keychain_ref": old_ref, "rotated_at": old_key.rotated_at.isoformat() if old_key else None},
            new_value={"keychain_ref": result.encrypted_key_ref, "rotated_at": result.rotated_at.isoformat()},
            details={"zero_downtime": True},
            audit_context=audit_context
        )

    return result

# In delete_user_key method
async def delete_user_key(
    self,
    user_id: str,
    provider: str,
    session: Optional[AsyncSession] = None,
    audit_context: Optional[Dict[str, Any]] = None
) -> bool:
    """Delete API key with audit logging"""
    # Get key info before deletion
    key = await self.retrieve_user_key(user_id, provider, session)

    # Existing deletion logic...
    success = await self._delete_key_internal(...)

    # Audit log
    if session:
        await audit_logger.log_api_key_event(
            action=Action.KEY_DELETED,
            provider=provider,
            status="success" if success else "failed",
            message=f"API key deleted for {provider}",
            session=session,
            user_id=user_id,
            old_value={"keychain_ref": key.encrypted_key_ref if key else None},
            audit_context=audit_context
        )

    return success
```

### 3.2 Integration Tests for API Key Auditing

**File**: `tests/security/integration_test_audit_api_keys.py` (NEW)

```python
"""Integration tests for API key audit logging"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from services.security.user_api_key_service import UserAPIKeyService
from services.security.audit_logger import Action, EventType
from services.database.models import AuditLog


class TestAPIKeyAudit:
    """Test API key management audit trail"""

    @pytest.mark.asyncio
    async def test_key_storage_audited(self, async_session: AsyncSession):
        """Test that key storage is audited"""
        service = UserAPIKeyService()

        audit_context = {"ip_address": "192.168.1.1"}

        # Store key (should trigger audit)
        result = await service.store_user_key(
            user_id="test_user",
            provider="openai",
            api_key="sk-test123",
            session=async_session,
            audit_context=audit_context
        )

        await async_session.commit()

        # Verify audit log
        result = await async_session.execute(
            select(AuditLog).where(
                AuditLog.event_type == EventType.API_KEY,
                AuditLog.action == Action.KEY_STORED,
                AuditLog.resource_id == "openai"
            )
        )
        log = result.scalar_one()

        assert log.status == "success"
        assert log.details["provider"] == "openai"
        assert log.ip_address == "192.168.1.1"

    @pytest.mark.asyncio
    async def test_key_rotation_audited(self, async_session: AsyncSession):
        """Test that key rotation is audited with old/new values"""
        service = UserAPIKeyService()

        # Store initial key
        await service.store_user_key(
            user_id="test_user",
            provider="openai",
            api_key="sk-old123",
            session=async_session
        )

        # Rotate key
        await service.rotate_user_key(
            user_id="test_user",
            provider="openai",
            new_api_key="sk-new456",
            session=async_session,
            audit_context={"ip_address": "192.168.1.1"}
        )

        await async_session.commit()

        # Verify rotation audit
        result = await async_session.execute(
            select(AuditLog).where(
                AuditLog.action == Action.KEY_ROTATED
            )
        )
        log = result.scalar_one()

        assert log.status == "success"
        assert log.old_value is not None
        assert log.new_value is not None
        assert log.details["zero_downtime"] == True
```

---

## Phase 4: REST API & Query (4 hours)

### 4.1 Create Query Service

**File**: `services/security/audit_query_service.py` (NEW)

```python
"""Audit log query service for retrieving and filtering audit logs"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import AuditLog
from services.security.audit_logger import EventType, Action, Severity


class AuditQueryService:
    """Service for querying audit logs"""

    async def get_logs(
        self,
        session: AsyncSession,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None,
        action: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """Query audit logs with filters

        Args:
            session: Database session
            user_id: Filter by user
            event_type: Filter by event type (auth, api_key, etc)
            action: Filter by action (login, key_stored, etc)
            severity: Filter by severity (info, warning, error, critical)
            status: Filter by status (success, failed, error)
            start_date: Filter logs after this date
            end_date: Filter logs before this date
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of matching AuditLog entries
        """
        # Build query
        query = select(AuditLog)

        # Apply filters
        filters = []
        if user_id:
            filters.append(AuditLog.user_id == user_id)
        if event_type:
            filters.append(AuditLog.event_type == event_type)
        if action:
            filters.append(AuditLog.action == action)
        if severity:
            filters.append(AuditLog.severity == severity)
        if status:
            filters.append(AuditLog.status == status)
        if start_date:
            filters.append(AuditLog.created_at >= start_date)
        if end_date:
            filters.append(AuditLog.created_at <= end_date)

        if filters:
            query = query.where(and_(*filters))

        # Order by date descending (most recent first)
        query = query.order_by(desc(AuditLog.created_at))

        # Pagination
        query = query.limit(limit).offset(offset)

        # Execute
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_activity(
        self,
        user_id: str,
        session: AsyncSession,
        days: int = 7
    ) -> List[AuditLog]:
        """Get recent activity for a user

        Args:
            user_id: User ID
            session: Database session
            days: Number of days to look back

        Returns:
            List of user's audit logs
        """
        start_date = datetime.utcnow() - timedelta(days=days)

        return await self.get_logs(
            session=session,
            user_id=user_id,
            start_date=start_date,
            limit=1000
        )

    async def get_security_events(
        self,
        session: AsyncSession,
        severity: Optional[str] = None,
        hours: int = 24
    ) -> List[AuditLog]:
        """Get recent security events

        Args:
            session: Database session
            severity: Filter by severity (warning, error, critical)
            hours: Number of hours to look back

        Returns:
            List of security events
        """
        start_date = datetime.utcnow() - timedelta(hours=hours)

        return await self.get_logs(
            session=session,
            event_type=EventType.SECURITY,
            severity=severity,
            start_date=start_date,
            limit=1000
        )


# Global instance
audit_query_service = AuditQueryService()
```

### 4.2 Create REST API Endpoints

**File**: `web/api/audit_routes.py` (NEW)

```python
"""REST API endpoints for audit log queries"""

from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

from services.database.session_factory import get_async_session
from services.security.audit_query_service import audit_query_service
from web.auth import require_auth


router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


class AuditLogResponse(BaseModel):
    """Audit log API response"""
    id: str
    user_id: Optional[str]
    event_type: str
    action: str
    status: str
    severity: str
    message: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    action: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    session = Depends(get_async_session),
    current_user = Depends(require_auth)
):
    """Query audit logs with filters

    Requires authentication. Users can only see their own logs unless admin.
    """
    # Non-admin users can only see their own logs
    if not current_user.is_admin:
        user_id = current_user.id

    logs = await audit_query_service.get_logs(
        session=session,
        user_id=user_id,
        event_type=event_type,
        action=action,
        severity=severity,
        status=status,
        limit=limit,
        offset=offset
    )

    return logs


@router.get("/logs/me", response_model=List[AuditLogResponse])
async def get_my_activity(
    days: int = Query(7, ge=1, le=90),
    session = Depends(get_async_session),
    current_user = Depends(require_auth)
):
    """Get current user's recent activity"""
    logs = await audit_query_service.get_user_activity(
        user_id=current_user.id,
        session=session,
        days=days
    )

    return logs


@router.get("/security", response_model=List[AuditLogResponse])
async def get_security_events(
    severity: Optional[str] = None,
    hours: int = Query(24, ge=1, le=168),
    session = Depends(get_async_session),
    current_user = Depends(require_auth)
):
    """Get recent security events (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    logs = await audit_query_service.get_security_events(
        session=session,
        severity=severity,
        hours=hours
    )

    return logs
```

**Add to main app** (`web/app.py`):
```python
from web.api.audit_routes import router as audit_router

app.include_router(audit_router)
```

---

## Testing Requirements

### Run All Tests
```bash
# Unit tests
pytest tests/security/test_audit_logger.py -v

# Integration tests
pytest tests/security/integration_test_audit_auth.py -v
pytest tests/security/integration_test_audit_api_keys.py -v

# All audit tests
pytest tests/security/ -v -k audit
```

### Run Migration
```bash
alembic upgrade head
```

### Verify Database
```bash
# Check table exists
psql -d piper_db -c "\dt audit_logs"

# Check indexes
psql -d piper_db -c "\di audit_logs*"

# Count logs
psql -d piper_db -c "SELECT COUNT(*) FROM audit_logs;"
```

---

## Documentation Requirements

### Update API Documentation

**File**: `docs/api-audit-logging.md` (NEW)

Include:
- API endpoint reference
- Query parameter descriptions
- Response examples
- Authentication requirements
- Rate limiting (if applicable)

### Update Architecture Documentation

**File**: `docs/architecture/audit-logging.md` (NEW)

Include:
- Audit system overview
- Event types and actions
- Integration points
- Security considerations
- Compliance features

---

## Acceptance Criteria

Before marking complete, verify:

### Core Functionality
- [x] AuditLog model created with all fields
- [x] Migration creates table and indexes successfully
- [x] AuditLogger service implements all convenience methods
- [x] Unit tests pass (100% coverage)

### Authentication Integration
- [x] JWT token creation audited
- [x] JWT token revocation audited
- [x] Failed login attempts audited
- [x] Integration tests pass

### API Key Integration
- [x] Key storage audited
- [x] Key retrieval audited (if tracking access)
- [x] Key deletion audited
- [x] Key rotation audited with old/new values
- [x] Integration tests pass

### Query & API
- [x] Query service supports all filters
- [x] REST API endpoints functional
- [x] Authentication enforced
- [x] Users can only see own logs (unless admin)

### Quality
- [x] All tests passing
- [x] Migration runs successfully
- [x] Documentation complete
- [x] Code follows existing patterns

---

## Session Log Requirements

**File**: `dev/2025/10/22/2025-10-22-0927-lead-dev-code-log.md`

Include:
- Start time (9:27 AM)
- Issue number (#249)
- Phases completed
- Test results
- Migration results
- Any issues encountered
- Total time taken
- End time

---

## Critical Notes

1. **Follow Existing Patterns**: String(255) PKs, TimestampMixin, JSON (not JSONB)
2. **Explicit Context**: Pass audit_context from routes → services
3. **Transaction Management**: Use flush(), let caller handle commit()
4. **Security**: Never log actual API keys, only keychain references
5. **Performance**: Indexes on all query fields
6. **Testing**: Integration tests verify end-to-end flow

---

## Success Criteria

**Issue #249 is complete when**:
1. All Phases 1-3 implemented (infrastructure + integrations)
2. All tests passing (unit + integration)
3. Migration successful
4. Documentation complete
5. Code review ready

**Phases 4-5** (dashboard + security alerts) are optional/future enhancements.

---

**Ready to implement! Start with Phase 1 and work systematically through each phase.**

**Target**: Complete Phases 1-3 in 2-3 hours (if pattern holds!) 🚀

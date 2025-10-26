# Audit Logging Infrastructure Analysis

**Date**: October 22, 2025, 8:48 AM
**Agent**: Cursor (Chief Architect)
**Issue**: #249 Audit Logging
**Duration**: 35 minutes

---

## Executive Summary

**Existing Infrastructure**: Distributed logging with structlog, no centralized audit system
**Integration Readiness**: High - excellent integration points with JWT, UserAPIKey services
**Key Findings**: Perfect foundation exists with User model, JWT auth, and consistent patterns. Ready for comprehensive audit system implementation.

---

## Existing Logging Infrastructure

### Current Logging Setup

**Location**: Distributed across services using Python's `logging` module
**Format**: Structured logging with `structlog` in some services
**Destination**: Standard output/files (no centralized collection)
**Centralized**: No - each service handles its own logging

**Current Logging Code**:

```python
# From services/auth/jwt_service.py
import structlog
logger = structlog.get_logger(__name__)

# From services/security/user_api_key_service.py
import logging
logger = logging.getLogger(__name__)
```

**Assessment**: Current logging is basic but structured. Good foundation for audit system, but needs centralized audit-specific logging.

### Existing Audit-Related Tables

**Tables Found**: None currently exist, but User model has prepared relationship

```python
# From services/database/models.py (User model)
# audit_logs = relationship("AuditLog", back_populates="user")  # For Issue #230
```

**Can We Use These?**: Perfect - the User model is already prepared for audit log relationships. Issue #230 was likely the original audit logging issue.

---

## Authentication Integration Points

### JWT Service Structure

**Location**: `services/auth/jwt_service.py`

**Key Methods to Audit**:

```python
# JWT token lifecycle methods (inferred from service structure)
async def create_token(user_id: str, token_type: TokenType) -> str
async def validate_token(token: str) -> JWTClaims
async def revoke_token(token_id: str, reason: str) -> bool
async def refresh_token(refresh_token: str) -> str
```

**Available Context**:

- user_id: Available in JWTClaims.user_id and JWTClaims.sub
- session_id: Available in JWTClaims.session_id (optional)
- token_id: Available in JWTClaims.jti (JWT ID)
- scopes: Available in JWTClaims.scopes

**Current Logging**: Basic structlog usage, logs authentication events but not audit-level detail

### Token Blacklist Integration

**Model**:

```python
class TokenBlacklist(Base):
    """Blacklisted JWT tokens (database fallback for Redis)"""
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=True, index=True)
    reason = Column(String(50), nullable=False)  # logout, security, admin
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
```

**Audit Needs**:

- Token revocation events (who, when, why)
- Token blacklist additions/removals
- Security-related token invalidations

---

## API Key Service Integration

### UserAPIKeyService Structure

**Location**: services/security/user_api_key_service.py

**Methods to Audit**:

```python
async def store_user_key(self, session, user_id, provider, api_key, validate=True) -> UserAPIKey
async def retrieve_user_key(self, session, user_id, provider) -> Optional[str]
async def delete_user_key(self, session, user_id, provider) -> bool
async def rotate_user_key(self, session, user_id, provider, new_key) -> UserAPIKey  # Inferred
async def validate_user_key(self, session, user_id, provider) -> bool  # Inferred
```

**Available Context in Methods**:

- user_id: Always available as method parameter
- provider: Always available (openai, anthropic, github, etc.)
- session context: AsyncSession available for database operations

**Integration Strategy**:

```python
# Example integration point
async def store_user_key(self, session, user_id, provider, api_key, validate=True):
    # Store key (existing logic)
    result = await self._store_key_logic(...)

    # INSERT AUDIT LOG HERE
    await audit_logger.log_api_key_event(
        user_id=user_id,
        action="store_key",
        provider=provider,
        status="success" if result else "failed",
        session=session
    )

    return result
```

### KeychainService Integration

**Critical Events**:

- API key storage in OS keychain
- API key retrieval from keychain
- Keychain access failures or security events
- Key validation successes/failures

---

## Session & Request Context

### Session Management

**How Sessions Work**:

```python
# Multiple session management systems found:
# 1. services/session/session_manager.py - ConversationSession
# 2. services/database/session_factory.py - AsyncSessionFactory
# 3. services/orchestration/session_persistence.py - SessionPersistenceManager
```

**Session Context Available**:

- session_id: Yes - available in ConversationSession and persistence systems
- user_id: Yes - tracked in session context and JWT claims

### Request Context

**Web App Structure**:

```python
# From web/app.py
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse

# FastAPI Request object provides:
# - request.client.host (IP address)
# - request.headers.get("user-agent") (User agent)
# - request.url.path (Request path)
```

**Request Context Available**:

- IP address: `request.client.host` in FastAPI
- user_agent: `request.headers.get("user-agent")`
- request_id: Not currently generated, but can be added via middleware

**Middleware Needed**: Yes - need audit context middleware to capture and pass request context to services

---

## Database Schema Patterns

### Standard Model Patterns

**Primary Key Pattern**:

```python
# Mixed patterns found:
# UUID for some models (PersonalityProfile)
id = Column(postgresql.UUID(as_uuid=True), primary_key=True)

# String for others (User, Task)
id = Column(String(255), primary_key=True)

# Integer for others (TokenBlacklist, UserAPIKey)
id = Column(Integer, primary_key=True, autoincrement=True)
```

**Timestamp Pattern**:

```python
# TimestampMixin available and widely used
class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models"""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**User Reference Pattern**:

```python
# Consistent ForeignKey pattern
user_id = Column(String(255), ForeignKey("users.id"), nullable=False, index=True)
```

**Index Naming Convention**:

```python
# Consistent pattern: idx_[table]_[field(s)]
Index("idx_users_username", "username", unique=True)
Index("idx_token_blacklist_user_id", "user_id")
Index("idx_personality_profiles_user_active", "user_id", "is_active")
```

### JSONB Support

**Is JSONB Available?**: No - but JSON is extensively used

**Example Usage**:

```python
# JSON columns are common throughout the codebase
context = Column(JSON, default=dict)  # Additional context data
conversation_context = Column(JSON, default=dict)
categories = Column(JSON, default=list)  # Auto-detected categories
tags = Column(JSON, default=list)  # User or system tags
```

**Import Pattern**:

```python
from sqlalchemy import JSON  # Standard JSON, not PostgreSQL JSONB
```

---

## Recommended AuditLog Model

Based on existing patterns:

```python
from sqlalchemy import Column, String, Integer, DateTime, Text, Index, ForeignKey, JSON
from datetime import datetime
import uuid

class AuditLog(Base, TimestampMixin):
    """Comprehensive audit trail for security and compliance"""
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
```

**Why This Structure**:

- Follows existing String(255) primary key pattern (like User model)
- Uses TimestampMixin for consistent timestamp handling
- Uses JSON columns (not JSONB) to match existing patterns
- Follows idx*[table]*[field] naming convention
- Includes comprehensive context capture for security analysis
- Supports both authentication and data modification auditing

---

## Integration Points Summary

### Priority 1: Authentication Events

**Where**: `services/auth/jwt_service.py`
**Methods**: `create_token`, `validate_token`, `revoke_token`, `refresh_token`
**Complexity**: Low - clear integration points
**Estimated Time**: 2 hours

**Integration Pattern**:

```python
# In JWT service methods
async def create_token(self, user_id: str, token_type: TokenType) -> str:
    # Generate token (existing logic)
    token = await self._generate_token(...)

    # Audit log
    await self.audit_logger.log_event(
        user_id=user_id,
        event_type="auth",
        action="token_created",
        resource_type="jwt_token",
        resource_id=token_id,
        status="success",
        severity="info",
        message=f"JWT token created for user {user_id}",
        details={"token_type": token_type.value, "expires_at": expires_at}
    )

    return token
```

### Priority 2: API Key Events

**Where**: `services/security/user_api_key_service.py`
**Methods**: `store_user_key`, `retrieve_user_key`, `delete_user_key`
**Complexity**: Low - session context already available
**Estimated Time**: 3 hours

**Integration Pattern**:

```python
# In UserAPIKeyService methods
async def store_user_key(self, session, user_id, provider, api_key, validate=True):
    try:
        # Store key (existing logic)
        result = await self._store_key_logic(...)

        # Audit success
        await self.audit_logger.log_event(
            user_id=user_id,
            event_type="api_key",
            action="store_key",
            resource_type="api_key",
            resource_id=f"{user_id}:{provider}",
            status="success",
            severity="info",
            message=f"API key stored for {provider}",
            details={"provider": provider, "validated": validate},
            session=session
        )

        return result
    except Exception as e:
        # Audit failure
        await self.audit_logger.log_event(
            user_id=user_id,
            event_type="api_key",
            action="store_key",
            resource_type="api_key",
            resource_id=f"{user_id}:{provider}",
            status="failed",
            severity="error",
            message=f"Failed to store API key for {provider}: {str(e)}",
            details={"provider": provider, "error": str(e)},
            session=session
        )
        raise
```

### Priority 3: Data Modification Events

**Where**: Multiple locations (User, PersonalityProfile, etc.)
**Approach**: Decorator pattern or service layer integration
**Complexity**: Medium - requires systematic integration
**Estimated Time**: 4 hours

---

## Migration Strategy

### Migration File Structure

**Based on Recent Migrations**:

```python
# Following pattern from 6d503d8783d2_add_user_model_issue_228.py

def upgrade() -> None:
    """Create audit_logs table with comprehensive indexing"""

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(255), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=True),
        sa.Column('session_id', sa.String(255), nullable=True),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=True),
        sa.Column('resource_id', sa.String(255), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('request_id', sa.String(255), nullable=True),
        sa.Column('request_path', sa.String(500), nullable=True),
        sa.Column('old_value', sa.JSON(), nullable=True),
        sa.Column('new_value', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create strategic indexes
    op.create_index('idx_audit_user_date', 'audit_logs', ['user_id', 'created_at'])
    op.create_index('idx_audit_event_type', 'audit_logs', ['event_type'])
    op.create_index('idx_audit_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_resource', 'audit_logs', ['resource_type', 'resource_id'])
    op.create_index('idx_audit_severity', 'audit_logs', ['severity'])
    op.create_index('idx_audit_status', 'audit_logs', ['status'])
    op.create_index('idx_audit_ip', 'audit_logs', ['ip_address'])
    op.create_index('idx_audit_session', 'audit_logs', ['session_id'])
    op.create_index('idx_audit_request', 'audit_logs', ['request_id'])

    # Add foreign key constraint
    op.create_foreign_key('fk_audit_logs_user_id', 'audit_logs', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    """Drop audit_logs table and indexes"""
    op.drop_constraint('fk_audit_logs_user_id', 'audit_logs', type_='foreignkey')
    op.drop_table('audit_logs')
```

**Naming Convention**: `[timestamp]_add_audit_logging_issue_249.py`

---

## AuditLogger Service Specification

Based on existing service patterns:

```python
# Location: services/security/audit_logger.py

import logging
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from services.database.models import AuditLog
from services.database.session_factory import AsyncSessionFactory

logger = logging.getLogger(__name__)

class AuditLogger:
    """Centralized audit logging service for security and compliance"""

    def __init__(self, session_factory: Optional[AsyncSessionFactory] = None):
        """Initialize audit logger with session factory"""
        self.session_factory = session_factory or AsyncSessionFactory()

    async def log_event(
        self,
        event_type: str,
        action: str,
        status: str,
        severity: str,
        message: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_id: Optional[str] = None,
        request_path: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
        session: Optional[AsyncSession] = None
    ) -> AuditLog:
        """
        Log audit event to database

        Args:
            event_type: Type of event (auth, api_key, data, system)
            action: Specific action (login, logout, store_key, etc)
            status: Event status (success, failed, error)
            severity: Event severity (info, warning, error, critical)
            message: Human-readable description
            user_id: User who performed the action
            session_id: Session identifier
            resource_type: Type of resource affected
            resource_id: Specific resource identifier
            ip_address: Client IP address
            user_agent: Client user agent
            request_id: Request correlation ID
            request_path: API endpoint path
            details: Additional structured data
            old_value: Previous state (for modifications)
            new_value: New state (for modifications)
            session: Existing database session (optional)

        Returns:
            Created AuditLog record
        """
        audit_log = AuditLog(
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
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            request_path=request_path,
            old_value=old_value,
            new_value=new_value
        )

        # Use provided session or create new one
        if session:
            session.add(audit_log)
            await session.flush()  # Don't commit, let caller handle transaction
        else:
            async with self.session_factory.session_scope() as new_session:
                new_session.add(audit_log)
                await new_session.commit()

        logger.info(f"Audit event logged: {event_type}.{action} for user {user_id}")
        return audit_log

    # Convenience methods for common event types
    async def log_auth_event(
        self,
        action: str,
        user_id: str,
        status: str = "success",
        severity: str = "info",
        **kwargs
    ) -> AuditLog:
        """Log authentication event"""
        return await self.log_event(
            event_type="auth",
            action=action,
            user_id=user_id,
            status=status,
            severity=severity,
            message=f"Authentication {action} for user {user_id}",
            **kwargs
        )

    async def log_api_key_event(
        self,
        action: str,
        user_id: str,
        provider: str,
        status: str = "success",
        severity: str = "info",
        **kwargs
    ) -> AuditLog:
        """Log API key management event"""
        return await self.log_event(
            event_type="api_key",
            action=action,
            user_id=user_id,
            resource_type="api_key",
            resource_id=f"{user_id}:{provider}",
            status=status,
            severity=severity,
            message=f"API key {action} for {provider}",
            details={"provider": provider},
            **kwargs
        )

    async def log_data_event(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        user_id: Optional[str] = None,
        status: str = "success",
        severity: str = "info",
        **kwargs
    ) -> AuditLog:
        """Log data modification event"""
        return await self.log_event(
            event_type="data",
            action=action,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            severity=severity,
            message=f"Data {action} on {resource_type} {resource_id}",
            **kwargs
        )
```

---

## Request Context Capture

### Challenge

How to capture IP, user_agent, request_id in service layer when services are called from FastAPI routes?

### Options

**Option 1: Pass context explicitly** (Recommended)

```python
# In FastAPI route
@router.post("/api/keys")
async def store_key(
    request: Request,
    user_id: str,
    provider: str,
    api_key: str,
    service: UserAPIKeyService = Depends(get_api_key_service)
):
    # Capture request context
    context = {
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "request_path": str(request.url.path),
        "request_id": str(uuid.uuid4())  # Generate correlation ID
    }

    # Pass to service
    result = await service.store_user_key(
        user_id=user_id,
        provider=provider,
        api_key=api_key,
        audit_context=context
    )
```

**Option 2: Middleware injection**

```python
# Add audit context middleware
class AuditContextMiddleware:
    async def __call__(self, request: Request, call_next):
        # Generate request ID and capture context
        request_id = str(uuid.uuid4())
        audit_context = {
            "ip_address": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "request_path": str(request.url.path),
            "request_id": request_id
        }

        # Store in request state
        request.state.audit_context = audit_context

        response = await call_next(request)
        return response

# In services, access via dependency injection
async def get_audit_context(request: Request) -> Dict[str, Any]:
    return getattr(request.state, "audit_context", {})
```

**Recommendation**: Option 1 (explicit context passing) fits best with existing architecture patterns and provides clear data flow.

---

## Testing Strategy

### Test Requirements

**Unit Tests**:

- AuditLog model creation and validation
- AuditLogger service methods
- Context capture and serialization
- JSON field handling

**Integration Tests**:

- Auth event logging (login, logout, token operations)
- API key event logging (store, retrieve, delete, rotate)
- Database transaction handling
- Query and filter operations

**Test Location**: `tests/security/test_audit_logger.py`

**Test Pattern** (based on existing patterns):

```python
# Following pattern from existing tests
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from services.security.audit_logger import AuditLogger
from services.database.models import AuditLog

class TestAuditLogger:
    """Test audit logging functionality"""

    async def test_log_auth_event(self, async_session: AsyncSession):
        """Test authentication event logging"""
        audit_logger = AuditLogger()

        result = await audit_logger.log_auth_event(
            action="login",
            user_id="test_user",
            status="success",
            session=async_session
        )

        assert result.event_type == "auth"
        assert result.action == "login"
        assert result.user_id == "test_user"
        assert result.status == "success"

    async def test_log_api_key_event(self, async_session: AsyncSession):
        """Test API key event logging"""
        audit_logger = AuditLogger()

        result = await audit_logger.log_api_key_event(
            action="store_key",
            user_id="test_user",
            provider="openai",
            status="success",
            session=async_session
        )

        assert result.event_type == "api_key"
        assert result.resource_type == "api_key"
        assert result.details["provider"] == "openai"
```

---

## Summary for Code

### What Code Needs to Create

**Phase 1: Infrastructure** (3 hours estimated)

1. AuditLog model in `services/database/models.py`
2. Migration `[timestamp]_add_audit_logging_issue_249.py`
3. AuditLogger service in `services/security/audit_logger.py`
4. Basic unit tests in `tests/security/test_audit_logger.py`

**Phase 2: Authentication Integration** (2 hours)

1. Integrate with JWT service login/logout/token events
2. Integrate with token blacklist operations
3. Add audit context to auth middleware
4. Test authentication audit trail

**Phase 3: API Key Integration** (3 hours)

1. Integrate with UserAPIKeyService methods
2. Add audit logging to keychain operations
3. Test API key management audit trail
4. Add error case audit logging

**Phase 4: Query & Dashboard** (4 hours)

1. Query service for audit logs with filtering
2. REST API endpoints for audit log access
3. Basic dashboard UI for audit review
4. Export capabilities for compliance

**Phase 5: Security Alerts** (3 hours)

1. Detect suspicious patterns (multiple failed logins, etc.)
2. Alert on critical events (admin actions, security failures)
3. Rate limiting based on audit logs
4. Automated security response

**Total**: 15 hours estimated

### Critical Details

**Model Location**: `services/database/models.py` (add AuditLog class)
**Service Location**: `services/security/audit_logger.py` (new file)
**Migration Naming**: `[timestamp]_add_audit_logging_issue_249.py`

**Existing Patterns to Follow**:

- String(255) primary keys (like User model)
- TimestampMixin for created_at/updated_at
- JSON columns (not JSONB) for structured data
- Index naming: `idx_[table]_[field(s)]`
- ForeignKey pattern: `ForeignKey("users.id")`

**Integration Points**:

- `services/auth/jwt_service.py` - token lifecycle methods
- `services/security/user_api_key_service.py` - all CRUD methods
- `services/auth/auth_middleware.py` - request context capture
- `web/app.py` - FastAPI route integration

**Context Capture Strategy**:

- Explicit context passing from FastAPI routes to services
- Generate request_id in routes for correlation
- Capture IP, user_agent, request_path from FastAPI Request object
- Pass audit_context parameter to service methods

---

## Evidence Checklist

Investigation complete:

- [x] Existing logging infrastructure documented (structlog + logging)
- [x] Authentication service structure documented (JWT + TokenBlacklist)
- [x] API key service integration points identified (UserAPIKeyService methods)
- [x] Session/request context capture strategy defined (explicit passing)
- [x] Database schema patterns documented (String PK, TimestampMixin, JSON)
- [x] Migration strategy defined (following recent patterns)
- [x] AuditLog model specification complete (matches existing patterns)
- [x] AuditLogger service specification complete (async/await pattern)
- [x] Integration examples provided (auth + API key events)
- [x] Testing strategy defined (unit + integration tests)

---

**Investigation complete. Code can now implement audit logging with high confidence and excellent integration with existing infrastructure.**

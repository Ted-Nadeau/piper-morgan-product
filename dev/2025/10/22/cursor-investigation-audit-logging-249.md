# Cursor Investigation Prompt: Audit Logging Infrastructure Analysis

**Agent**: Cursor (Chief Architect)
**Issue**: #249 CORE-AUDIT-LOGGING
**Task**: Investigate existing logging infrastructure and prepare for audit system implementation
**Date**: October 22, 2025, 8:48 AM
**Duration**: 20-30 minutes

---

## Mission

**Goal**: Document existing logging infrastructure and patterns to build comprehensive audit logging system on solid foundations.

**Your job is investigation ONLY**:
- ✅ Document existing logging patterns
- ✅ Identify database integration points
- ✅ Check authentication/API key services for hook points
- ✅ Review session management for context capture
- ✅ Provide complete specifications
- ❌ Do NOT implement anything

---

## Context

**What We're Building**: Comprehensive audit trail system for security, compliance, and debugging.

**Why Investigation Needed**:
- Need to understand existing logging infrastructure
- Need to identify integration points (auth, API keys, data ops)
- Need to see what context is already captured (user_id, session_id, IP, etc.)
- Want consistent patterns across the codebase
- Need to avoid duplicating existing logging

**Key Integration Points**:
1. JWT Authentication (#227) - login, logout, token events
2. UserAPIKeyService (#228) - key storage, retrieval, rotation
3. Database operations - data modifications
4. Session management - user context

---

## Phase 1: Existing Logging Infrastructure (10 min)

### 1.1 Check for Existing Logging Setup

```bash
# Find logging configuration
find /Users/xian/Development/piper-morgan -name "*.py" -type f | xargs grep -l "import logging" | head -20

# Check for centralized logger
cat services/utils/logger.py 2>/dev/null || echo "No central logger found"

# Check logging config
cat config/logging.yaml 2>/dev/null || cat config/logging.json 2>/dev/null || echo "No logging config found"
```

**Document**:
- Is there centralized logging?
- What format is used? (JSON, text, etc.)
- What's logged currently?
- Where are logs stored?
- Any existing patterns we should follow?

### 1.2 Check Database Models for Audit-Related Tables

```bash
# Check if audit tables already exist
grep -r "audit" services/database/models.py
grep -r "log" services/database/models.py | grep "class.*Log"

# Check migrations for audit-related changes
ls -la alembic/versions/ | grep -i audit
ls -la alembic/versions/ | grep -i log
```

**Document**:
- Do any audit-related tables exist?
- Are there any log models?
- What patterns are used for timestamps, user IDs?

---

## Phase 2: Authentication Integration Points (8 min)

### 2.1 Examine JWT Authentication Service

```bash
# Find JWT authentication service
find services -name "*auth*" -o -name "*jwt*" | grep -v __pycache__

# View JWT service structure
cat services/security/jwt_service.py 2>/dev/null | head -100

# Check for existing auth logging
grep -A 10 "login\|authenticate" services/security/*.py | head -50
```

**Document**:
- Where is user authentication handled?
- What events should be audited? (login, logout, token issue, token revoke)
- What context is available? (user_id, IP, user_agent)
- Are there any existing hooks we can use?

### 2.2 Check Token Blacklist for Audit Patterns

```bash
# TokenBlacklist was added in #227
grep -A 20 "class TokenBlacklist" services/database/models.py

# Check if token operations are logged anywhere
grep -r "blacklist" services/security/*.py | grep -v "^Binary"
```

**Document**:
- How are tokens tracked?
- Is token revocation logged?
- What fields are captured?

---

## Phase 3: API Key Service Integration (8 min)

### 3.1 Review UserAPIKeyService

```bash
# UserAPIKeyService from #228
cat services/security/user_api_key_service.py | head -150

# Check what context is captured
grep -A 5 "store_user_key\|retrieve_user_key\|rotate_user_key" services/security/user_api_key_service.py
```

**Document**:
- What methods need audit logging?
  - store_user_key()
  - retrieve_user_key()
  - delete_user_key()
  - rotate_user_key()
  - validate_user_key()
- What context is available in these methods?
- Are there any existing logging statements?

### 3.2 Check KeychainService

```bash
# KeychainService integration
cat services/keychain/keychain_service.py | head -100

# Check for any security logging
grep -i "log\|audit" services/keychain/keychain_service.py
```

**Document**:
- Should keychain operations be audited?
- What security events are critical?

---

## Phase 4: Session & Context Management (5 min)

### 4.1 Check Session Management

```bash
# Find session management
find services -name "*session*" | grep -v __pycache__

# Check SessionFactory
cat services/database/session_factory.py 2>/dev/null | head -80
```

**Document**:
- How are sessions managed?
- Is session_id tracked?
- What user context is available?

### 4.2 Check Request Context Handling

```bash
# Check for request context in web app
cat web/app.py | head -100

# Check for middleware that captures context
grep -r "ip_address\|user_agent\|request_id" web/*.py | head -30
```

**Document**:
- Is IP address captured?
- Is user_agent tracked?
- Is request_id available?
- How can we access request context from services?

---

## Phase 5: Database Schema Patterns (5 min)

### 5.1 Review Existing Model Patterns

```bash
# Look at User model for patterns
grep -A 30 "class User" services/database/models.py

# Look at UserAPIKey for patterns
grep -A 30 "class UserAPIKey" services/database/models.py

# Check TimestampMixin
grep -A 10 "class.*Mixin" services/database/models.py
```

**Document**:
- What's the standard pattern for:
  - Primary keys (UUID? Integer? String?)
  - Timestamps (created_at, updated_at)
  - User references (ForeignKey pattern)
  - Indexes (naming convention)
- Is there a TimestampMixin?
- Are there other mixins we should use?

### 5.2 Check PostgreSQL JSONB Support

```bash
# Check if JSONB is used anywhere
grep -r "JSONB\|JSON" services/database/models.py

# Check SQLAlchemy imports
grep "from sqlalchemy" services/database/models.py | head -20
```

**Document**:
- Is JSONB used for flexible data?
- What's imported from SQLAlchemy?
- Are there examples of JSONB columns?

---

## Phase 6: Migration Patterns (5 min)

### 6.1 Review Recent Migrations

```bash
# Look at recent migration structure
ls -lt alembic/versions/ | head -5

# Examine most recent migration
cat alembic/versions/$(ls -t alembic/versions/*.py | head -1) | head -100
```

**Document**:
- What's the migration pattern?
- How are indexes created?
- How are tables created?
- Any special patterns for audit-related fields?

---

## Discovery Report Format

Create: `dev/2025/10/22/audit-logging-infrastructure-analysis.md`

### Report Structure

```markdown
# Audit Logging Infrastructure Analysis

**Date**: October 22, 2025, 8:48 AM
**Agent**: Cursor (Chief Architect)
**Issue**: #249 Audit Logging
**Duration**: [X] minutes

---

## Executive Summary

**Existing Infrastructure**: [High-level summary]
**Integration Readiness**: [Ready/Needs work/Unknown]
**Key Findings**: [1-2 sentence summary]

---

## Existing Logging Infrastructure

### Current Logging Setup

**Location**: [Where logging is configured]
**Format**: [JSON/text/structured]
**Destination**: [Files/stdout/database]
**Centralized**: [Yes/No]

**Current Logging Code**:
```python
# PASTE EXAMPLE IF EXISTS
```

**Assessment**: [Is current logging sufficient as base?]

### Existing Audit-Related Tables

**Tables Found**: [List any audit/log tables]

```python
# PASTE MODEL CODE IF EXISTS
```

**Can We Use These?**: [Yes/No and why]

---

## Authentication Integration Points

### JWT Service Structure

**Location**: [File path]

**Key Methods to Audit**:
```python
# PASTE RELEVANT METHOD SIGNATURES
async def login(...): ...
async def logout(...): ...
async def revoke_token(...): ...
```

**Available Context**:
- user_id: [How accessed]
- session_id: [How accessed]
- IP address: [How accessed]
- user_agent: [How accessed]

**Current Logging**: [Describe what's already logged]

### Token Blacklist Integration

**Model**:
```python
# PASTE TokenBlacklist model
```

**Audit Needs**:
- [List what should be audited]

---

## API Key Service Integration

### UserAPIKeyService Structure

**Location**: services/security/user_api_key_service.py

**Methods to Audit**:
```python
# PASTE METHOD SIGNATURES
async def store_user_key(...): ...
async def retrieve_user_key(...): ...
async def delete_user_key(...): ...
async def rotate_user_key(...): ...
async def validate_user_key(...): ...
```

**Available Context in Methods**:
- user_id: [Always available? How?]
- provider: [Always available?]
- session context: [How to access?]

**Integration Strategy**:
```python
# Example integration point
async def store_user_key(self, user_id, provider, api_key):
    # Store key
    result = await self._store(...)

    # INSERT AUDIT LOG HERE
    await audit_logger.log_api_key_event(...)

    return result
```

### KeychainService Integration

**Critical Events**:
- [List what should be audited from keychain operations]

---

## Session & Request Context

### Session Management

**How Sessions Work**:
```python
# PASTE RELEVANT CODE
```

**Session Context Available**:
- session_id: [Yes/No - How to access]
- user_id: [Yes/No - How to access]

### Request Context

**Web App Structure**:
```python
# PASTE RELEVANT CODE FROM web/app.py
```

**Request Context Available**:
- IP address: [How to capture]
- user_agent: [How to capture]
- request_id: [Generated? How?]

**Middleware Needed**: [Yes/No - What kind?]

---

## Database Schema Patterns

### Standard Model Patterns

**Primary Key Pattern**:
```python
# UUID, Integer, or String?
id = Column(...)
```

**Timestamp Pattern**:
```python
# TimestampMixin? Manual fields?
created_at = Column(...)
updated_at = Column(...)
```

**User Reference Pattern**:
```python
# ForeignKey pattern
user_id = Column(..., ForeignKey("users.id"))
```

**Index Naming Convention**:
```python
# What's the pattern?
Index("idx_table_field", "field")
```

### JSONB Support

**Is JSONB Available?**: [Yes/No]

**Example Usage**:
```python
# PASTE EXAMPLE IF EXISTS
details = Column(JSONB, nullable=True)
```

**Import Pattern**:
```python
from sqlalchemy.dialects.postgresql import JSONB
```

---

## Recommended AuditLog Model

Based on existing patterns:

```python
from sqlalchemy import Column, String, Integer, DateTime, Text, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from uuid import uuid4

class AuditLog(Base):
    """Comprehensive audit trail"""
    __tablename__ = "audit_logs"

    # Identity (follow existing pattern)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(255), nullable=True)

    # Event classification
    event_type = Column(String(50), nullable=False, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(String(255), nullable=True)

    # Event details
    status = Column(String(20), nullable=False)
    severity = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSONB, nullable=True)  # IF JSONB AVAILABLE

    # Context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    request_id = Column(String(255), nullable=True)

    # Changes
    old_value = Column(JSONB, nullable=True)
    new_value = Column(JSONB, nullable=True)

    # Timestamp (follow existing pattern)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Indexes (follow existing naming convention)
    __table_args__ = (
        Index("idx_audit_user_date", "user_id", "created_at"),
        Index("idx_audit_event_type", "event_type"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_severity", "severity"),
        Index("idx_audit_status", "status"),
    )
```

**Why This Structure**:
- [Explain how it follows existing patterns]
- [Note any deviations and why]

---

## Integration Points Summary

### Priority 1: Authentication Events

**Where**: [Service/file]
**Methods**: [List methods]
**Complexity**: [Low/Medium/High]
**Estimated Time**: [X hours]

**Integration Pattern**:
```python
# SHOW SPECIFIC EXAMPLE
```

### Priority 2: API Key Events

**Where**: [Service/file]
**Methods**: [List methods]
**Complexity**: [Low/Medium/High]
**Estimated Time**: [X hours]

**Integration Pattern**:
```python
# SHOW SPECIFIC EXAMPLE
```

### Priority 3: Data Modification Events

**Where**: [Multiple locations]
**Approach**: [Decorator? Mixin? Manual?]
**Complexity**: [Low/Medium/High]
**Estimated Time**: [X hours]

---

## Migration Strategy

### Migration File Structure

**Based on Recent Migrations**:
```python
# PASTE EXAMPLE FROM RECENT MIGRATION

def upgrade():
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column(...),
        ...
    )

    # Create indexes
    op.create_index(...)
```

**Naming Convention**: `[timestamp]_add_audit_logging_issue_249.py`

---

## AuditLogger Service Specification

Based on existing service patterns:

```python
# Location: services/security/audit_logger.py

class AuditLogger:
    """Centralized audit logging service"""

    def __init__(self, session_factory: AsyncSessionFactory):
        self.session_factory = session_factory

    async def log_event(
        self,
        user_id: str = None,
        event_type: str,
        action: str,
        status: str,
        severity: str,
        message: str,
        **kwargs  # Additional context
    ):
        """Log audit event"""
        async with self.session_factory.session_scope() as session:
            log = AuditLog(
                user_id=user_id,
                event_type=event_type,
                action=action,
                status=status,
                severity=severity,
                message=message,
                # Extract kwargs
                session_id=kwargs.get("session_id"),
                ip_address=kwargs.get("ip_address"),
                user_agent=kwargs.get("user_agent"),
                details=kwargs.get("details"),
                # etc.
            )
            session.add(log)
            await session.commit()

    # Convenience methods
    async def log_auth_event(...):
        """Log authentication event"""

    async def log_api_key_event(...):
        """Log API key event"""
```

---

## Request Context Capture

### Challenge

How to capture IP, user_agent, request_id in service layer?

### Options

**Option 1: Pass context explicitly**
```python
await service.store_key(user_id, provider, key, request_context=request.context)
```

**Option 2: Thread-local storage (if available)**
```python
# Set context in middleware
request_context.set(ip=request.ip, user_agent=request.user_agent)

# Access in service
context = request_context.get()
```

**Option 3: Middleware injection**
```python
# Service receives context from dependency injection
```

**Recommendation**: [Which option fits best with existing architecture?]

---

## Testing Strategy

### Test Requirements

**Unit Tests**:
- AuditLog model creation
- AuditLogger service methods
- Context capture

**Integration Tests**:
- Auth event logging (login, logout)
- API key event logging (store, rotate, delete)
- Query/filter logs

**Test Location**: `tests/security/test_audit_logger.py`

**Test Pattern** (based on existing tests):
```python
# PASTE EXAMPLE FROM EXISTING TEST IF AVAILABLE
```

---

## Summary for Code

### What Code Needs to Create

**Phase 1: Infrastructure** (3 hours estimated)
1. AuditLog model in models.py
2. Migration for audit_logs table
3. AuditLogger service
4. Basic unit tests

**Phase 2: Authentication Integration** (2 hours)
1. Log login events
2. Log logout events
3. Log token issuance
4. Log token revocation

**Phase 3: API Key Integration** (3 hours)
1. Log key storage
2. Log key retrieval
3. Log key deletion
4. Log key rotation
5. Log key validation

**Phase 4: Query & Dashboard** (4 hours)
1. Query service for logs
2. Filter by user/event/date
3. Basic dashboard UI
4. Export capabilities

**Phase 5: Security Alerts** (3 hours)
1. Detect suspicious patterns
2. Alert on critical events
3. Rate limiting based on logs

**Total**: 15 hours estimated

### Critical Details

**Model Location**: `services/database/models.py`
**Service Location**: `services/security/audit_logger.py`
**Migration Naming**: `[timestamp]_add_audit_logging_issue_249.py`

**Existing Patterns to Follow**:
- [List specific patterns from investigation]

**Integration Points**:
- [List specific files/methods with line numbers if possible]

**Context Capture Strategy**:
- [Specific approach based on investigation]

---

## Evidence Checklist

Before finishing investigation:

- [x] Existing logging infrastructure documented
- [x] Authentication service structure documented
- [x] API key service integration points identified
- [x] Session/request context capture strategy defined
- [x] Database schema patterns documented
- [x] Migration strategy defined
- [x] AuditLog model specification complete
- [x] AuditLogger service specification complete
- [x] Integration examples provided
- [x] Testing strategy defined

---

**Investigation complete. Code can now implement audit logging with high confidence.**
```

---

## Critical Notes

**For Cursor**:

1. **Focus on Integration Points**: This is about connecting audit logging to existing systems
2. **Follow Existing Patterns**: Don't invent new patterns, use what's there
3. **Be Specific**: Provide actual code examples, file paths, line numbers
4. **Context Capture is Key**: How to get IP, user_agent, session_id in service layer?
5. **Test Patterns**: Show how tests are structured in this project

**Key Outputs**:
- Complete AuditLog model (matching existing patterns)
- AuditLogger service specification
- Specific integration points (file paths, methods)
- Context capture strategy
- Migration strategy

**Time Management**:
- 20-30 minutes is fine
- Thoroughness matters more than speed
- Specific examples are gold

---

**Ready to investigate! Start with Phase 1 and work systematically.**

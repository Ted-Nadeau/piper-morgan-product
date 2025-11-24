# CORE-AUDIT-LOGGING: Comprehensive Audit Trail System

## Context

Production systems require comprehensive audit trails for security, compliance, and debugging. All user actions, security events, and system changes must be logged with complete traceability.

**Sprint**: A6
**Priority**: High (security & compliance requirement)
**Complexity**: Medium

---

## Problem Statement

**Current State**:
- No centralized audit logging
- Security events not tracked
- User actions not logged
- API key access unaudited
- No compliance trail
- Debugging requires log diving

**Risks Without Audit Logging**:
- **Security**: Can't detect unauthorized access or suspicious activity
- **Compliance**: Can't prove GDPR/SOC2/HIPAA compliance
- **Debugging**: Can't trace user actions when issues occur
- **Forensics**: Can't investigate security incidents
- **Support**: Can't see what user did before error

---

## Proposed Solution

### 1. Audit Log Model
```python
class AuditLog(Base):
    """Comprehensive audit trail"""
    __tablename__ = "audit_logs"

    # Identity
    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(255), nullable=True)

    # Event classification
    event_type = Column(String(50), nullable=False)  # auth, api_key, data, system
    action = Column(String(100), nullable=False)     # login, store_key, delete, etc.
    resource_type = Column(String(50), nullable=True)  # user, api_key, conversation
    resource_id = Column(String(255), nullable=True)

    # Event details
    status = Column(String(20), nullable=False)  # success, failure, error
    severity = Column(String(20), nullable=False)  # info, warning, error, critical
    message = Column(Text, nullable=False)
    details = Column(JSONB, nullable=True)  # Structured event data

    # Context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    request_id = Column(String(255), nullable=True)

    # Changes (for data modifications)
    old_value = Column(JSONB, nullable=True)  # Before state
    new_value = Column(JSONB, nullable=True)  # After state

    # Timestamp
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Indexes
    __table_args__ = (
        Index("idx_audit_user_date", "user_id", "created_at"),
        Index("idx_audit_event_type", "event_type"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_severity", "severity"),
        Index("idx_audit_status", "status"),
    )
```

### 2. Event Types & Actions
```python
class EventType:
    """Categorize audit events"""

    AUTH = "auth"              # Authentication events
    API_KEY = "api_key"        # API key operations
    DATA = "data"              # Data modifications
    SYSTEM = "system"          # System events
    SECURITY = "security"      # Security events
    COMPLIANCE = "compliance"  # Compliance events

class Action:
    """Specific actions to audit"""

    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    TOKEN_ISSUED = "token_issued"
    TOKEN_REVOKED = "token_revoked"

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
    """Event severity levels"""

    INFO = "info"        # Normal operations
    WARNING = "warning"  # Potential issues
    ERROR = "error"      # Errors that need attention
    CRITICAL = "critical"  # Critical security/system events
```

### 3. Audit Logger Service
```python
class AuditLogger:
    """Centralized audit logging service"""

    async def log_event(
        self,
        user_id: str = None,
        event_type: str,
        action: str,
        status: str,
        severity: str,
        message: str,
        resource_type: str = None,
        resource_id: str = None,
        details: dict = None,
        old_value: dict = None,
        new_value: dict = None,
        request_context: dict = None
    ):
        """Log audit event"""

        log = AuditLog(
            user_id=user_id,
            session_id=request_context.get("session_id") if request_context else None,
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
            ip_address=request_context.get("ip_address") if request_context else None,
            user_agent=request_context.get("user_agent") if request_context else None,
            request_id=request_context.get("request_id") if request_context else None
        )

        await self._store_log(log)
        await self._check_security_alerts(log)

    async def log_auth_event(
        self,
        user_id: str,
        action: str,
        status: str,
        message: str,
        **kwargs
    ):
        """Convenience method for auth events"""
        await self.log_event(
            user_id=user_id,
            event_type=EventType.AUTH,
            action=action,
            status=status,
            severity=Severity.INFO if status == "success" else Severity.WARNING,
            message=message,
            **kwargs
        )

    async def log_api_key_event(
        self,
        user_id: str,
        action: str,
        provider: str,
        status: str,
        **kwargs
    ):
        """Convenience method for API key events"""
        await self.log_event(
            user_id=user_id,
            event_type=EventType.API_KEY,
            action=action,
            resource_type="api_key",
            resource_id=provider,
            status=status,
            severity=Severity.INFO,
            message=f"API key {action} for {provider}",
            **kwargs
        )
```

### 4. Integration Points
```python
# In JWT authentication
async def login(username: str, password: str):
    try:
        user = await authenticate(username, password)
        token = create_jwt_token(user)

        # Audit successful login
        await audit_logger.log_auth_event(
            user_id=user.id,
            action=Action.LOGIN,
            status="success",
            message=f"User {username} logged in successfully"
        )

        return token
    except AuthenticationError:
        # Audit failed login
        await audit_logger.log_auth_event(
            user_id=None,
            action=Action.LOGIN_FAILED,
            status="failure",
            message=f"Failed login attempt for {username}",
            details={"username": username}
        )
        raise

# In UserAPIKeyService
async def store_user_key(self, user_id: str, provider: str, api_key: str):
    # Store key
    result = await self._store_key(user_id, provider, api_key)

    # Audit key storage
    await audit_logger.log_api_key_event(
        user_id=user_id,
        action=Action.KEY_STORED,
        provider=provider,
        status="success",
        details={"keychain_ref": result.keychain_ref}
    )

    return result

# In UserAPIKeyService rotation
async def rotate_user_key(self, user_id: str, provider: str, new_api_key: str):
    old_ref = await self._get_current_key_ref(user_id, provider)

    # Rotate key
    result = await self._rotate_key(user_id, provider, new_api_key)

    # Audit rotation
    await audit_logger.log_api_key_event(
        user_id=user_id,
        action=Action.KEY_ROTATED,
        provider=provider,
        status="success",
        old_value={"keychain_ref": old_ref},
        new_value={"keychain_ref": result.new_ref}
    )

    return result
```

---

## Implementation Phases

### Phase 1: Audit Log Infrastructure (3 hours)
- Create AuditLog model
- Create database migration
- Create AuditLogger service
- Add convenience methods for common events

### Phase 2: Authentication Auditing (2 hours)
- Log all login attempts (success/failure)
- Log JWT token issuance
- Log JWT token revocation
- Log logout events

### Phase 3: API Key Auditing (3 hours)
- Log key storage
- Log key retrieval (when accessed)
- Log key deletion
- Log key rotation
- Log key validation

### Phase 4: Query & Dashboard (4 hours)
- Query API for audit logs
- Filter by user, event type, date range
- Dashboard UI for viewing logs
- Export capabilities

### Phase 5: Security Alerts (3 hours)
- Detect suspicious patterns
- Alert on security events
- Rate limiting based on audit logs
- Automated responses to threats

---

## Acceptance Criteria

### Core Functionality
- [ ] All authentication events logged
- [ ] All API key operations logged
- [ ] All data modifications logged
- [ ] Logs include complete context (user, IP, timestamp, etc.)
- [ ] Logs stored with proper indexing

### Query Capabilities
- [ ] Query logs by user
- [ ] Query logs by event type
- [ ] Query logs by date range
- [ ] Query logs by resource
- [ ] Query logs by severity

### Security
- [ ] Logs are tamper-evident
- [ ] Logs don't contain sensitive data (passwords, keys)
- [ ] Logs retained per compliance requirements
- [ ] Access to logs is audited

### User Experience
- [ ] Dashboard for viewing own activity
- [ ] Clear explanations of logged events
- [ ] Export logs to CSV/JSON
- [ ] Search and filter capabilities

### Performance
- [ ] Logging doesn't slow down operations (<10ms overhead)
- [ ] Efficient queries on large log volumes
- [ ] Automatic log rotation/archival
- [ ] Supports millions of log entries

---

## Example Audit Events

### Authentication Success
```json
{
  "user_id": "alice",
  "event_type": "auth",
  "action": "login",
  "status": "success",
  "severity": "info",
  "message": "User alice logged in successfully",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "created_at": "2025-10-22T08:15:30Z"
}
```

### Authentication Failure
```json
{
  "user_id": null,
  "event_type": "auth",
  "action": "login_failed",
  "status": "failure",
  "severity": "warning",
  "message": "Failed login attempt for alice",
  "details": {
    "username": "alice",
    "reason": "invalid_password",
    "attempt_count": 3
  },
  "ip_address": "192.168.1.100",
  "created_at": "2025-10-22T08:14:15Z"
}
```

### API Key Storage
```json
{
  "user_id": "alice",
  "event_type": "api_key",
  "action": "key_stored",
  "resource_type": "api_key",
  "resource_id": "openai",
  "status": "success",
  "severity": "info",
  "message": "API key key_stored for openai",
  "details": {
    "provider": "openai",
    "keychain_ref": "alice_openai_api_key",
    "validated": true
  },
  "created_at": "2025-10-22T08:16:00Z"
}
```

### API Key Rotation
```json
{
  "user_id": "alice",
  "event_type": "api_key",
  "action": "key_rotated",
  "resource_type": "api_key",
  "resource_id": "openai",
  "status": "success",
  "severity": "info",
  "message": "API key key_rotated for openai",
  "old_value": {
    "keychain_ref": "alice_openai_api_key",
    "rotated_at": "2025-07-22T08:16:00Z"
  },
  "new_value": {
    "keychain_ref": "alice_openai_api_key",
    "rotated_at": "2025-10-22T09:30:00Z"
  },
  "created_at": "2025-10-22T09:30:00Z"
}
```

### Suspicious Activity
```json
{
  "user_id": "alice",
  "event_type": "security",
  "action": "suspicious_activity",
  "status": "detected",
  "severity": "critical",
  "message": "Multiple failed login attempts from different IPs",
  "details": {
    "failed_attempts": 5,
    "ip_addresses": ["192.168.1.100", "10.0.0.50", "172.16.0.200"],
    "time_window": "5_minutes"
  },
  "created_at": "2025-10-22T10:15:00Z"
}
```

---

## User Flows

### Flow 1: View Personal Activity
```bash
$ piper audit logs --me

Your Recent Activity (Last 7 days)

Oct 22, 2025:
09:30 AM - Rotated OpenAI API key ✓
08:16 AM - Stored OpenAI API key ✓
08:15 AM - Logged in ✓

Oct 21, 2025:
02:45 PM - Exported conversation data ✓
11:23 AM - Updated personality profile ✓
09:15 AM - Logged in ✓

[Show More] [Export CSV]
```

### Flow 2: Security Dashboard (Admin)
```bash
$ piper audit security --critical

Critical Security Events (Last 24 hours)

⚠️  3 suspicious activity detections
├─ User: alice | Multiple failed logins | 10:15 AM
├─ User: bob   | Unusual IP address     | 03:22 PM
└─ User: charlie | Rate limit exceeded | 08:45 PM

⚠️  2 permission denied events
├─ User: alice | Attempted to access admin area | 11:30 AM
└─ User: bob   | Attempted to delete system config | 04:15 PM

✓ All events reviewed and resolved
```

### Flow 3: Compliance Report
```bash
$ piper audit report --compliance --month october

Compliance Audit Report - October 2025

Authentication Events:
- Successful logins: 1,234
- Failed logins: 45 (3.6% failure rate)
- Average session duration: 2.3 hours
- MFA usage: 98.5% (target: >95%) ✓

API Key Operations:
- Keys stored: 34
- Keys retrieved: 4,567
- Keys rotated: 12
- Keys deleted: 5
- All operations validated ✓

Data Access:
- User data accessed: 1,234 times
- Exports: 23
- Deletions: 5 (all with user consent) ✓
- GDPR compliance: 100% ✓

Security Events:
- Suspicious activities: 3 (all investigated) ✓
- Permission denials: 2 (expected behavior) ✓
- Zero security breaches ✓

Report generated: October 22, 2025
Compliance status: PASS ✓
```

---

## Success Metrics

### Coverage
- **Target**: 100% of security-relevant actions logged
- **Measure**: Coverage checklist
- **Success**: All auth, API key, data ops logged

### Performance
- **Target**: <10ms logging overhead
- **Measure**: P95 latency with/without audit
- **Success**: No noticeable performance impact

### Retention
- **Target**: 90 days minimum (compliance)
- **Measure**: Oldest log entry
- **Success**: Can query 90+ day old logs

### Usability
- **Target**: 80% of users find logs helpful
- **Measure**: User survey
- **Success**: >80% positive feedback

---

## Dependencies

**Required**:
- ✅ #228: API Key Management (API key events)
- ✅ #227: JWT Authentication (auth events)
- ✅ User model (user context)
- ❌ Audit log infrastructure (new)

**Enables**:
- Future: Security alerting system
- Future: Compliance reporting
- Future: Forensic investigation
- Future: User activity insights

---

## Time Estimate

**Total**: 15 hours (~2 days)

**Breakdown**:
- Audit log infrastructure: 3 hours
- Authentication auditing: 2 hours
- API key auditing: 3 hours
- Query & dashboard: 4 hours
- Security alerts: 3 hours

---

## Priority & Sprint

**Priority**: High (security & compliance)
**Sprint**: A6 (core security infrastructure)
**Milestone**: Alpha

**Rationale**: Core security requirement for production. Must have before alpha launch for compliance and incident response.

---

## Related Issues

- #227: JWT Authentication (auth events to audit)
- #228: API Key Management (API key events to audit)
- Future: Enhanced rotation reminders (uses audit data)
- Future: Cost tracking (uses audit data)
- Future: Security alerting (uses audit data)

**Epic**: CORE-USERS (Multi-user & Security)
**Labels**: security, compliance, component: security, priority: high, sprint: a6

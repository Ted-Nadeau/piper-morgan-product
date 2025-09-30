# Webhook Security Architecture

**Document Status**: Operational Guide
**Last Updated**: September 30, 2025
**Source**: CORE-GREAT-2C Phase 3 (TBD-SECURITY-02 Resolution)

## Overview

Piper Morgan implements a **graceful degradation security pattern** for webhook endpoints, providing developer-friendly defaults while maintaining production security. This design enables seamless local development without sacrificing security in production environments.

## Security Philosophy

**Developer Experience First, Security Always**

The webhook security system follows these principles:

1. **Works Out of the Box**: No configuration required for local development
2. **Production Secure**: Full verification when signing secrets configured
3. **Graceful Degradation**: No hard failures on missing configuration
4. **Standard Compliance**: Follows platform specifications (Slack HMAC-SHA256)
5. **Clear Feedback**: Logs warnings when security is degraded

---

## Security Design Pattern

### Development Mode (Default Behavior)

**Trigger**: No signing secret configured (`SLACK_SIGNING_SECRET` not set)

**Behavior**:
```python
if not signing_secret:
    logger.warning("No Slack signing secret configured, skipping signature verification")
    return True  # Allow request to proceed
```

**Characteristics**:
- Webhook endpoints return `200 OK` for all requests
- No signature verification required
- Allows local development and testing without Slack workspace access
- Warning logged for visibility (not error)
- Graceful fallback preserves functionality

**Use Cases**:
- Local development on developer machines
- Testing webhook handlers without external dependencies
- CI/CD pipelines without production credentials
- Prototyping and experimentation

**Security Level**: ⚠️ **Development Only** - Not suitable for production

---

### Production Mode (Configured Security)

**Trigger**: Signing secret configured (`SLACK_SIGNING_SECRET` environment variable set)

**Behavior**:
```python
# Validate timestamp (prevent replay attacks)
current_time = int(time.time())
if abs(current_time - int(timestamp)) > 300:
    logger.warning("Slack request timestamp too old")
    return False

# Compute expected signature using HMAC-SHA256
sig_basestring = f"v0:{timestamp}:{body.decode()}"
expected_signature = "v0=" + hmac.new(
    signing_secret.encode(),
    sig_basestring.encode(),
    hashlib.sha256
).hexdigest()

# Timing-safe comparison
return hmac.compare_digest(signature, expected_signature)
```

**Characteristics**:
- Full HMAC-SHA256 signature verification
- Timestamp validation (5-minute tolerance window)
- Invalid signatures return `401 Unauthorized`
- Replay attack prevention (timestamp must be recent)
- Timing-safe signature comparison (prevents timing attacks)

**Use Cases**:
- Production deployments with real Slack workspace
- Staging environments with workspace integration
- Any environment accepting external webhook requests

**Security Level**: 🔒 **Production Grade** - Industry standard security

---

## Implementation Details

### Verification Method

**Location**: `services/integrations/slack/webhook_router.py`

**Method**: `_verify_slack_signature(self, request: Request) -> bool`

**Implementation** (lines 442-487):
```python
async def _verify_slack_signature(self, request: Request) -> bool:
    """
    Verify Slack request signature for security.

    Implements Slack's signature verification protocol:
    1. Extract timestamp and signature from headers
    2. Validate timestamp (prevent replay attacks)
    3. Compute expected signature using HMAC-SHA256
    4. Compare signatures using timing-safe comparison

    Returns:
        True if signature valid or development mode (no signing secret)
        False if signature invalid or missing required headers
    """
    try:
        # Get signing secret from configuration
        config = self.config_service.get_config()
        signing_secret = config.signing_secret

        # Development mode: Allow requests without signing secret
        if not signing_secret:
            logger.warning("No Slack signing secret configured, skipping signature verification")
            return True  # Graceful degradation

        # Extract required headers
        timestamp = request.headers.get("X-Slack-Request-Timestamp")
        signature = request.headers.get("X-Slack-Signature")

        # Validate headers present
        if not timestamp or not signature:
            logger.warning("Missing timestamp or signature in Slack request")
            return False

        # Validate timestamp (prevent replay attacks - 5 minute window)
        current_time = int(time.time())
        if abs(current_time - int(timestamp)) > 300:
            logger.warning("Slack request timestamp too old")
            return False

        # Get request body
        body = await request.body()

        # Compute expected signature (Slack protocol)
        sig_basestring = f"v0:{timestamp}:{body.decode()}"
        expected_signature = (
            "v0=" + hmac.new(
                signing_secret.encode(),
                sig_basestring.encode(),
                hashlib.sha256
            ).hexdigest()
        )

        # Timing-safe comparison (prevents timing attacks)
        return hmac.compare_digest(signature, expected_signature)

    except Exception as e:
        logger.error(f"Error verifying Slack signature: {e}")
        return False
```

---

### Endpoint Protection

**All webhook endpoints call verification** before processing requests:

#### 1. Events Webhook
**Endpoint**: `/slack/webhooks/events`
**Method**: `_handle_events_webhook` (line 180)
**Protection** (lines 184-188):
```python
# Verify request signature
if not await self._verify_slack_signature(request):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid request signature"
    )
```

**Status**: ✅ Protected (enabled in Phase 3)

#### 2. Interactive Components
**Endpoint**: `/slack/webhooks/interactive`
**Method**: `_handle_interactive_webhook` (line 311)
**Protection** (lines 315-319):
```python
# Verify request signature
if not await self._verify_slack_signature(request):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid request signature"
    )
```

**Status**: ✅ Protected (previously enabled)

#### 3. Slash Commands
**Endpoint**: `/slack/webhooks/commands`
**Method**: `_handle_commands_webhook` (line 350)
**Protection** (lines 354-358):
```python
# Verify request signature
if not await self._verify_slack_signature(request):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid request signature"
    )
```

**Status**: ✅ Protected (previously enabled)

**Protection Coverage**: **100%** (3/3 webhook endpoints protected)

---

## Security Features

### 1. HMAC-SHA256 Signature Verification

**Standard**: Slack Web API specification
**Algorithm**: HMAC with SHA-256 hash function
**Key Material**: Slack signing secret (from workspace settings)

**Process**:
1. Concatenate version (`v0`), timestamp, and request body
2. Compute HMAC-SHA256 hash using signing secret
3. Compare with signature from `X-Slack-Signature` header

**Security Benefit**: Ensures request originated from Slack and wasn't tampered with

### 2. Replay Attack Protection

**Mechanism**: Timestamp validation with tolerance window
**Tolerance**: 5 minutes (300 seconds)
**Header**: `X-Slack-Request-Timestamp`

**Process**:
1. Extract timestamp from request header
2. Compare with current server time
3. Reject if difference exceeds 5 minutes

**Security Benefit**: Prevents attackers from replaying captured valid requests

### 3. Timing-Safe Comparison

**Function**: `hmac.compare_digest(signature, expected_signature)`
**Purpose**: Prevent timing attacks

**Process**:
1. Compare signatures character-by-character
2. Always compare full strings (don't short-circuit)
3. Return result after constant-time comparison

**Security Benefit**: Prevents attackers from using response time to guess valid signatures

### 4. Header Validation

**Required Headers**:
- `X-Slack-Request-Timestamp` - Request timestamp (Unix epoch)
- `X-Slack-Signature` - HMAC-SHA256 signature with version prefix

**Validation**:
1. Check both headers present
2. Validate timestamp format (parseable integer)
3. Validate signature format (starts with `v0=`)

**Security Benefit**: Ensures request has required security metadata

### 5. Error Handling

**Philosophy**: Fail closed (reject on error)

**Behavior**:
```python
except Exception as e:
    logger.error(f"Error verifying Slack signature: {e}")
    return False  # Reject request on any error
```

**Security Benefit**: Errors don't create security vulnerabilities

### 6. Logging and Observability

**Warnings**:
- No signing secret configured (development mode)
- Missing headers in request
- Timestamp too old (replay attack)

**Errors**:
- Exception during verification process

**Security Benefit**: Visibility into security events for monitoring and debugging

---

## Configuration

### Development Environment

**No configuration required** - webhook endpoints work immediately.

**Behavior**: All requests accepted (graceful degradation)

### Production Environment

**Required**: Set `SLACK_SIGNING_SECRET` environment variable

**How to Get Signing Secret**:
1. Open Slack App settings
2. Navigate to "Basic Information"
3. Scroll to "App Credentials"
4. Copy "Signing Secret"

**Configuration**:
```bash
# Set environment variable
export SLACK_SIGNING_SECRET=your_signing_secret_here

# Or in .env file
SLACK_SIGNING_SECRET=your_signing_secret_here

# Restart server to activate
./stop-piper.sh && ./start-piper.sh
```

**Verification**: Check logs for absence of warnings:
```
# Should NOT see this in production:
WARNING: No Slack signing secret configured, skipping signature verification
```

---

## Testing

### Development Mode Testing

**Test**: Webhook accepts requests without signatures

```bash
# Send request without signature
curl -X POST http://localhost:8001/slack/webhooks/events \
  -H "Content-Type: application/json" \
  -d '{"type": "url_verification", "challenge": "test123"}'

# Expected: 200 OK (development mode allows)
# Expected log: WARNING: No Slack signing secret configured
```

**Result**: ✅ Works in development (graceful degradation)

### Production Mode Testing

**Test 1**: Valid signature accepted

```bash
# Generate valid signature using signing secret
TIMESTAMP=$(date +%s)
BODY='{"type":"url_verification","challenge":"test123"}'
SIG_BASE="v0:${TIMESTAMP}:${BODY}"
SIGNATURE="v0=$(echo -n "$SIG_BASE" | openssl dgst -sha256 -hmac "$SLACK_SIGNING_SECRET" | cut -d' ' -f2)"

# Send request with valid signature
curl -X POST https://production.app/slack/webhooks/events \
  -H "Content-Type: application/json" \
  -H "X-Slack-Request-Timestamp: $TIMESTAMP" \
  -H "X-Slack-Signature: $SIGNATURE" \
  -d "$BODY"

# Expected: 200 OK (valid signature)
```

**Test 2**: Invalid signature rejected

```bash
# Send request with invalid signature
curl -X POST https://production.app/slack/webhooks/events \
  -H "Content-Type: application/json" \
  -H "X-Slack-Request-Timestamp: $(date +%s)" \
  -H "X-Slack-Signature: v0=invalid_signature" \
  -d '{"type":"url_verification","challenge":"test123"}'

# Expected: 401 Unauthorized (invalid signature)
```

**Test 3**: Old timestamp rejected (replay attack)

```bash
# Send request with old timestamp (> 5 minutes ago)
OLD_TIMESTAMP=$(($(date +%s) - 400))

curl -X POST https://production.app/slack/webhooks/events \
  -H "Content-Type: application/json" \
  -H "X-Slack-Request-Timestamp: $OLD_TIMESTAMP" \
  -H "X-Slack-Signature: v0=some_signature" \
  -d '{"type":"url_verification","challenge":"test123"}'

# Expected: 401 Unauthorized (timestamp too old)
```

---

## Security Audit History

### TBD-SECURITY-02 (Resolved September 30, 2025)

**Issue**: Events webhook (`/slack/webhooks/events`) had signature verification disabled

**Root Cause**: Lines 184-189 in `webhook_router.py` were commented out with note "disabled for integration testing"

**Resolution**:
- Uncommented verification code (Phase 3 of GREAT-2C)
- Restored signature verification call
- Removed TODO comment

**Impact**:
- Before: 2/3 endpoints protected (67%)
- After: 3/3 endpoints protected (100%)
- Security coverage: 100%

**Files Modified**:
- `services/integrations/slack/webhook_router.py` (lines 184-188)

**Verification**:
- ✅ All 3 endpoints now call `_verify_slack_signature`
- ✅ Invalid signatures return 401 Unauthorized
- ✅ Development mode still works (graceful degradation)
- ✅ Spatial systems unaffected (zero breaking changes)

---

## Best Practices

### For Developers

1. **Local Development**: Use default configuration (no signing secret)
2. **Test Changes**: Verify webhook handlers work without signatures
3. **Production Testing**: Always test with valid signatures before deploying
4. **Error Handling**: Don't bypass security checks in error handlers

### For Operations

1. **Signing Secret**: Rotate periodically (every 90 days recommended)
2. **Monitoring**: Alert on signature verification failures
3. **Logging**: Review security warnings in logs
4. **Deployment**: Ensure signing secret set before production deployment

### For Security

1. **Secret Storage**: Never commit signing secrets to version control
2. **Access Control**: Limit who can view/modify signing secrets
3. **Rotation**: Have procedure for emergency secret rotation
4. **Auditing**: Log all signature verification attempts

---

## Troubleshooting

### Issue: Webhooks rejected in production (401 Unauthorized)

**Cause**: Invalid signature verification

**Solutions**:
1. Verify `SLACK_SIGNING_SECRET` is set correctly
2. Check signing secret matches Slack workspace settings
3. Ensure timestamp is current (within 5 minutes)
4. Verify request format matches Slack specification

### Issue: Webhooks accepted when they shouldn't be

**Cause**: No signing secret configured (development mode)

**Solutions**:
1. Set `SLACK_SIGNING_SECRET` environment variable
2. Restart server to activate production mode
3. Verify logs don't show "skipping signature verification" warning

### Issue: Intermittent 401 errors

**Cause**: Timestamp validation failing (clock skew)

**Solutions**:
1. Synchronize server clock with NTP
2. Check for clock drift
3. Ensure timestamp header is recent (< 5 minutes)

---

## Future Considerations

### Potential Enhancements

1. **Configurable Tolerance**: Make timestamp tolerance configurable (currently 300s)
2. **Metrics**: Add Prometheus metrics for signature verification (success/failure rates)
3. **Rate Limiting**: Add rate limiting to prevent brute force attacks
4. **Signature Caching**: Cache valid signatures briefly to reduce computation
5. **Multiple Secrets**: Support key rotation with multiple valid secrets

### Security Roadmap

- [ ] Add signature verification metrics
- [ ] Implement configurable timestamp tolerance
- [ ] Add rate limiting per IP/endpoint
- [ ] Create security monitoring dashboard
- [ ] Document secret rotation procedure

---

## Compliance

**Standards Followed**:
- Slack Web API Signature Verification Specification
- HMAC-SHA256 (RFC 2104)
- FastAPI HTTP Exception Standards (401 Unauthorized)

**Security Properties**:
- ✅ Authentication (verifies request origin)
- ✅ Integrity (detects tampering)
- ✅ Replay attack prevention
- ✅ Timing attack resistance
- ✅ Graceful degradation

---

## Conclusion

Piper Morgan's webhook security architecture successfully balances **developer experience** with **production security** through graceful degradation. The system:

- Works immediately for local development (no configuration)
- Provides industry-standard security in production (HMAC-SHA256)
- Prevents common attacks (replay, timing, tampering)
- Maintains observability (logging, error handling)
- Follows platform specifications (Slack API compliance)

**Key Insight**: Security doesn't have to hurt developer experience when designed thoughtfully.

---

**See Also**:
- [Spatial Intelligence Patterns](spatial-intelligence-patterns.md) - Spatial architecture
- [ADR-038: Spatial Intelligence Patterns](../internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md) - Architectural decision
- [Slack API Documentation](https://api.slack.com/authentication/verifying-requests-from-slack) - Official Slack verification spec

**Maintained by**: Piper Morgan Core Team
**Questions**: Create a GitHub issue with label `security`

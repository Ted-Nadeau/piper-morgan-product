# Health Endpoint Should Return UTC Timestamps with Timezone Marker

**Type**: Tech Debt
**Priority**: Low
**Labels**: tech-debt, api, standards-compliance
**Estimated Effort**: 5 minutes
**Discovered**: October 20, 2025 (Task 7 - Integration Testing)

---

## Problem

The health endpoint (`/api/v1/standup/health`) currently returns timestamps in local time without timezone markers:

```json
{
  "status": "healthy",
  "timestamp": "2025-10-20T07:06:43"  // Local PDT, no timezone
}
```

This violates ISO 8601 best practices and can cause confusion in multi-timezone deployments.

---

## Expected Behavior

Health endpoint should return UTC timestamps with explicit timezone markers:

```json
{
  "status": "healthy",
  "timestamp": "2025-10-20T14:06:43Z"  // UTC with 'Z' suffix
}
```

---

## Impact

**Current**:
- 7-hour offset observed between endpoint and UTC (PDT = UTC-7)
- Tests had to account for timezone ambiguity
- Potential confusion in production deployments
- Non-standard timestamp format

**Risk Level**: Low
- Doesn't affect functionality
- Workarounds exist
- Only affects health endpoint

---

## Discovery Context

Found during Task 7 (Integration Testing) of Issue #162:
- Integration tests compared server timestamp to `datetime.now(timezone.utc)`
- Discovered 7-hour difference (PDT offset)
- Code correctly worked around the issue for testing
- But highlighted the underlying bug in health endpoint

**Evidence**:
- `tests/integration/test_standup_integration.py`
- Task 7 session log: `dev/2025/10/20/2025-10-20-0654-prog-code-log.md`

---

## Recommended Fix

**File to change**: `web/api/routes/standup.py` (or wherever health endpoint is)

**Current code** (likely):
```python
@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()  # Local time
    }
```

**Fixed code**:
```python
from datetime import datetime, timezone

@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()  # UTC with 'Z'
    }
```

**That's it!** One-line change: add `timezone.utc` parameter.

---

## Testing

**Update integration test** to verify UTC format:

```python
def test_health_endpoint_returns_utc_timestamp(api_client, base_url):
    """Verify health endpoint returns UTC timestamp"""
    response = api_client.get(f"{base_url}/api/v1/standup/health")
    assert response.status_code == 200

    data = response.json()
    timestamp = data["timestamp"]

    # Should end with 'Z' (UTC indicator)
    assert timestamp.endswith('Z'), "Timestamp should be UTC with 'Z' suffix"

    # Should parse as UTC
    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    assert parsed.tzinfo is not None, "Timestamp should include timezone"
```

---

## Benefits of Fixing

**Standards Compliance**:
- ✅ ISO 8601 compliant
- ✅ Explicit timezone indication
- ✅ No ambiguity

**Multi-Timezone Deployments**:
- ✅ Works correctly across timezones
- ✅ No confusion for international users
- ✅ Consistent with API best practices

**Testing**:
- ✅ Simpler test assertions
- ✅ No timezone offset calculations needed
- ✅ More reliable integration tests

---

## Acceptance Criteria

- [ ] Health endpoint returns timestamps in UTC
- [ ] Timestamps include explicit 'Z' timezone marker
- [ ] Timestamp format: `YYYY-MM-DDTHH:MM:SSZ`
- [ ] Integration test updated to verify UTC format
- [ ] All existing tests still pass

---

## Related Issues

- **Discovered in**: #162 (CORE-STAND-MODES-API) Task 7
- **Related pattern**: All API endpoints should use UTC timestamps

---

## Notes

**Why Low Priority**:
- Doesn't affect functionality
- Only affects health endpoint
- Easy workaround exists
- Not user-facing feature

**Why Still Worth Fixing**:
- Standards compliance
- Future multi-timezone deployments
- Good API hygiene
- 5-minute fix

**Could be combined with**:
- Audit all API endpoints for UTC timestamp usage
- Create standard timestamp utility function
- Add timezone handling to API documentation

---

*Created: October 20, 2025*
*Discovered by: Claude Code during Task 7 Integration Testing*
*Estimated fix time: 5 minutes*

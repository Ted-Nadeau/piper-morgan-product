# API Error Handling

**Status**: ✅ Active
**Effective**: October 16, 2025
**Pattern**: Pattern 034 - REST-Compliant Error Handling

---

## Overview

Piper Morgan API follows REST principles for error handling. All errors return appropriate HTTP status codes along with a structured JSON response.

**Key Principle**: The HTTP status code tells you **what happened**, the response body tells you **why**.

---

## HTTP Status Codes

### 200 OK ✅
**Meaning**: Request succeeded
**When**: Valid request, successful operation
**Response**:
```json
{
  "status": "success",
  "data": { ... }
}
```

**Example**:
```bash
curl -X POST /api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "show me the standup"}'
# → HTTP 200
```

---

### 422 Unprocessable Entity ⚠️
**Meaning**: Request syntax valid, but semantically invalid
**When**:
- Empty required fields
- Invalid field values
- Business rule violations
- Type mismatches

**Response**:
```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "User-friendly error message",
  "details": {
    "field": "intent",
    "issue": "Cannot be empty"
  }
}
```

**Example**:
```bash
curl -X POST /api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
# → HTTP 422
# {
#   "status": "error",
#   "code": "VALIDATION_ERROR",
#   "message": "Validation failed",
#   "details": {"field": "message", "issue": "Cannot be empty"}
# }
```

---

### 404 Not Found 🔍
**Meaning**: Requested resource doesn't exist
**When**:
- Workflow ID not found
- User ID not found
- Invalid endpoint

**Response**:
```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "Resource not found",
  "details": {
    "resource": "workflow",
    "id": "12345"
  }
}
```

**Example**:
```bash
curl -X GET /api/v1/workflows/nonexistent-id
# → HTTP 404
```

---

### 500 Internal Server Error ⚡
**Meaning**: Unexpected server error
**When**: Unhandled exceptions, service failures

**Response**:
```json
{
  "status": "error",
  "code": "INTERNAL_ERROR",
  "message": "An unexpected error occurred",
  "details": {
    "error_id": "uuid-for-log-correlation"
  }
}
```

**Security**: Internal details never exposed in production
**Debugging**: Use `error_id` to correlate with server logs

---

## Error Response Format

All errors follow this structure:

```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "User-friendly message",
  "details": {
    // Optional additional context
  }
}
```

### Fields

**status** (string, required)
- Always `"error"` for error responses
- Backward compatible with old API

**code** (string, required)
- One of: `VALIDATION_ERROR`, `NOT_FOUND`, `INTERNAL_ERROR`, `BAD_REQUEST`
- Use for programmatic error handling

**message** (string, required)
- Human-readable error description
- Safe to display to users

**details** (object, optional)
- Additional context about the error
- Field-specific information
- Never includes sensitive data

---

## Client Implementation Guide

### Recommended Approach

```python
import requests

response = requests.post(
    "https://api.piper-morgan.ai/api/v1/intent",
    json={"message": "show me standup"}
)

# Check HTTP status code FIRST
if response.status_code == 200:
    # Success
    data = response.json()
    print(data["data"])

elif response.status_code == 422:
    # Validation error
    error = response.json()
    print(f"Validation failed: {error['message']}")
    if "details" in error:
        print(f"Field: {error['details'].get('field')}")

elif response.status_code == 404:
    # Not found
    error = response.json()
    print(f"Resource not found: {error['message']}")

elif response.status_code == 500:
    # Internal error
    error = response.json()
    error_id = error.get("details", {}).get("error_id")
    print(f"Server error (ID: {error_id})")

else:
    # Other errors
    print(f"Unexpected status: {response.status_code}")
```

### JavaScript/TypeScript

```typescript
try {
  const response = await fetch('/api/v1/intent', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'show me standup'})
  });

  const data = await response.json();

  if (response.ok) {
    // Success (200-299)
    console.log(data.data);
  } else if (response.status === 422) {
    // Validation error
    console.error('Validation:', data.message);
  } else if (response.status === 404) {
    // Not found
    console.error('Not found:', data.message);
  } else if (response.status === 500) {
    // Internal error
    console.error('Server error:', data.details.error_id);
  }
} catch (error) {
  console.error('Request failed:', error);
}
```

---

## Best Practices

### DO ✅

- Check HTTP status code before parsing response
- Use `code` field for programmatic error handling
- Display `message` field to users
- Log `error_id` for 500 errors (support correlation)
- Handle all error status codes (422, 404, 500)

### DON'T ❌

- Rely only on response body `status` field
- Ignore HTTP status codes
- Expose `error_id` to end users (internal use only)
- Assume all errors are 200 with error body

---

## Common Patterns

### Validation Errors

```bash
# Empty field
POST /api/v1/intent {"message": ""}
→ 422 {"code": "VALIDATION_ERROR", "details": {"field": "message"}}

# Invalid type
POST /api/v1/workflows {"name": 123}
→ 422 {"code": "VALIDATION_ERROR", "details": {"field": "name", "issue": "Must be string"}}
```

### Not Found Errors

```bash
# Invalid ID
GET /api/v1/workflows/invalid-id
→ 404 {"code": "NOT_FOUND", "details": {"resource": "workflow", "id": "invalid-id"}}
```

### Internal Errors

```bash
# Service unavailable
POST /api/v1/intent {"message": "test"}
→ 500 {"code": "INTERNAL_ERROR", "details": {"error_id": "abc-123"}}
```

---

## Backward Compatibility

### What Changed

**Before** (deprecated):
```json
HTTP 200
{"status": "error", "error": "Intent required"}
```

**After** (current):
```json
HTTP 422
{"status": "error", "code": "VALIDATION_ERROR", "message": "Intent required"}
```

### Migration Impact

**Breaking Changes**:
- HTTP status codes now correct (not always 200)
- Clients must check `response.status_code`

**Backward Compatible**:
- Response format still has `status` field
- Can still check `response.json()["status"] == "error"`
- Added `code` field (doesn't break existing clients)

**Recommended**: Update clients to use HTTP status codes

---

## Support

**Questions?** Contact the API team or file an issue on GitHub.

**Bug Reports**: Include `error_id` for 500 errors.

---

*Last Updated: October 16, 2025*
*Pattern: 034 - REST-Compliant Error Handling*

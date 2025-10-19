# Code Agent Prompt: Phase 4 - Documentation

**Date**: October 16, 2025, 2:00 PM
**Sprint**: A2 - Notion & Errors (Day 2)
**Issue**: CORE-ERROR-STANDARDS #215
**Phase**: Phase 4 - Documentation
**Duration**: 30-45 minutes
**Agent**: Claude Code

---

## Mission

Create comprehensive documentation for the REST-compliant error handling (Pattern 034) implemented in Phases 0-3. External developers need to understand the new error responses, and internal team needs migration guidance.

**Context**: All endpoints now return proper HTTP status codes. Need to document this for API consumers and provide migration guide for breaking changes.

**Philosophy**: "Good documentation prevents a thousand support tickets."

---

## What We've Accomplished

### Phases 0-3 Complete! ✅
- **Phase 0**: Error utilities + Pattern 034 specification
- **Phase 1**: Intent endpoint REST-compliant
- **Phase 1.5**: DDD Service Container
- **Phase 1.6**: ServiceRegistry cleanup
- **Phase 2**: All endpoints REST-compliant (15+ endpoints)
- **Phase 3**: Tests verified (no updates needed!)

### Phase 4 ← **WE ARE HERE**
- Document error handling for external developers
- Create migration guide for API clients
- Update README with new startup and error info
- Complete Pattern 034 reference

---

## Step 1: API Error Handling Guide (15 min)

**For**: External developers using Piper Morgan API

**File**: `docs/public/api/error-handling.md`

```markdown
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
  -d '{"intent": "show me the standup"}'
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
  -d '{"intent": ""}'
# → HTTP 422
# {
#   "status": "error",
#   "code": "VALIDATION_ERROR",
#   "message": "Validation failed",
#   "details": {"field": "intent", "issue": "Cannot be empty"}
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
    json={"intent": "show me standup"}
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
    body: JSON.stringify({intent: 'show me standup'})
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
POST /api/v1/intent {"intent": ""}
→ 422 {"code": "VALIDATION_ERROR", "details": {"field": "intent"}}

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
POST /api/v1/intent {"intent": "test"}
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
```

---

## Step 2: Migration Guide (10 min)

**For**: Teams with existing API clients

**File**: `docs/public/migration/error-handling-migration.md`

```markdown
# Error Handling Migration Guide

**Effective Date**: October 16, 2025
**Breaking Changes**: Yes (HTTP status codes)
**Migration Effort**: Low to Medium
**Pattern**: Pattern 034

---

## Summary of Changes

Piper Morgan API now returns proper HTTP status codes for errors instead of always returning 200.

**Before**: All errors returned HTTP 200 with error body
**After**: Errors return 422/404/500 with structured error body

---

## Breaking Changes

### HTTP Status Codes

| Scenario | Before | After |
|----------|--------|-------|
| Validation error | 200 | 422 |
| Not found | 200 | 404 |
| Internal error | 200 | 500 |
| Success | 200 | 200 |

### Response Format

**Before**:
```json
{
  "status": "error",
  "error": "Error message string"
}
```

**After**:
```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "Error message string",
  "details": { ... }
}
```

---

## Migration Steps

### Step 1: Update Error Handling

**Old Code** (will break):
```python
response = requests.post("/api/v1/intent", json=data)
result = response.json()

if result["status"] == "error":
    # This won't catch 422/404/500 properly anymore
    print(result["error"])
```

**New Code** (correct):
```python
response = requests.post("/api/v1/intent", json=data)

if response.status_code == 200:
    result = response.json()
    # Handle success
elif response.status_code == 422:
    error = response.json()
    print(f"Validation error: {error['message']}")
elif response.status_code == 404:
    error = response.json()
    print(f"Not found: {error['message']}")
elif response.status_code == 500:
    error = response.json()
    print(f"Server error: {error['details']['error_id']}")
```

### Step 2: Update Field Names

Change `error` field to `message`:

```python
# Old
error_text = response.json()["error"]

# New
error_text = response.json()["message"]
```

### Step 3: Add Status Code Checking

```python
# Add before parsing JSON
if not response.ok:  # Checks status_code >= 400
    error = response.json()
    # Handle error based on status_code
```

---

## Timeline

**Phase 1**: October 16, 2025 (Complete)
- All endpoints updated
- Pattern 034 active

**Recommended**: Update clients within 30 days

**Support**: Old error format still present (`status` field), but use HTTP codes

---

## Testing Your Migration

### Test Cases

```bash
# 1. Valid request (should return 200)
curl -X POST /api/v1/intent \
  -d '{"intent": "show me standup"}' \
  -w "\n%{http_code}\n"

# 2. Invalid request (should return 422)
curl -X POST /api/v1/intent \
  -d '{"intent": ""}' \
  -w "\n%{http_code}\n"

# 3. Not found (should return 404)
curl -X GET /api/v1/workflows/invalid \
  -w "\n%{http_code}\n"
```

---

## Need Help?

Contact API team or file migration issues on GitHub.

---

*Last Updated: October 16, 2025*
```

---

## Step 3: Update README (10 min)

**File**: `README.md`

**Add/Update these sections**:

### Startup Instructions

```markdown
## Getting Started

### Starting the Server

```bash
# Recommended: Use main.py (initializes services)
python main.py

# Server will start on http://127.0.0.1:8001
```

**Note**: Use `python main.py` instead of `uvicorn` directly. This ensures proper service initialization.

### Health Check

```bash
curl http://localhost:8001/health
```
```

### Error Handling Section

```markdown
## API Error Handling

Piper Morgan follows REST principles for error responses:

- **200**: Success
- **422**: Validation error (invalid input)
- **404**: Resource not found
- **500**: Internal server error

See [API Error Handling Guide](docs/public/api/error-handling.md) for details.

### Example

```python
response = requests.post("/api/v1/intent", json={"intent": "test"})

if response.status_code == 200:
    # Success
    data = response.json()
elif response.status_code == 422:
    # Validation error
    error = response.json()
    print(error["message"])
```

For complete documentation, see:
- [Error Handling Guide](docs/public/api/error-handling.md)
- [Migration Guide](docs/public/migration/error-handling-migration.md)
- [Pattern 034 Reference](docs/internal/architecture/current/patterns/pattern-034-error-handling-standards.md)
```

---

## Step 4: Verify Pattern 034 Reference (5 min)

**File**: `docs/internal/architecture/current/patterns/pattern-034-error-handling-standards.md`

**Check that it's complete** (should be from Phase 0):
- ✅ HTTP status code standards
- ✅ Error response format
- ✅ Usage examples
- ✅ Migration guidance

**If missing anything**, add it. Otherwise, just verify it's good.

---

## Step 5: Create Documentation Index (5 min)

**File**: `docs/public/api/README.md` (if doesn't exist)

```markdown
# Piper Morgan API Documentation

## Getting Started

- [Error Handling](error-handling.md) - How errors work
- [Migration Guide](../migration/error-handling-migration.md) - Updating your code

## Reference

- [Pattern 034](../../internal/architecture/current/patterns/pattern-034-error-handling-standards.md) - Complete specification

## Support

Questions? File an issue on GitHub or contact the API team.
```

---

## Step 6: Commit Documentation (5 min)

```bash
./scripts/commit.sh "docs(#215): Phase 4 - comprehensive error handling documentation

Created Documentation:
- docs/public/api/error-handling.md (comprehensive API guide)
- docs/public/migration/error-handling-migration.md (migration guide)
- docs/public/api/README.md (documentation index)
- README.md (updated startup + error handling sections)

Documentation Includes:
- HTTP status code meanings
- Error response format
- Client implementation examples (Python, JavaScript)
- Best practices
- Migration steps
- Testing guide

Audience:
- External developers using API
- Internal teams with existing clients
- New developers onboarding

Part of: #215 Phase 4, Sprint A2
Duration: [actual time]"
```

---

## Deliverables Phase 4

When complete, you should have:

- [ ] API Error Handling Guide created (docs/public/api/error-handling.md)
- [ ] Migration Guide created (docs/public/migration/error-handling-migration.md)
- [ ] README updated (startup + error handling sections)
- [ ] Pattern 034 verified complete
- [ ] Documentation index created
- [ ] Changes committed

---

## Success Criteria

**Phase 4 is complete when**:

- ✅ External developers can understand error responses
- ✅ Teams know how to migrate existing clients
- ✅ README has clear startup and error info
- ✅ All documentation linked properly
- ✅ Examples in multiple languages
- ✅ Changes committed

---

## Time Budget

**Target**: 30-45 minutes

- API guide: 15 min
- Migration guide: 10 min
- README updates: 10 min
- Pattern verification: 5 min
- Doc index: 5 min
- Commit: 5 min

**Total**: ~50 minutes (with buffer)

---

## What NOT to Do

- ❌ Don't skip examples (developers need them!)
- ❌ Don't forget migration guide (breaking changes!)
- ❌ Don't leave links broken
- ❌ Don't forget README updates

## What TO Do

- ✅ Clear examples in multiple languages
- ✅ Comprehensive migration steps
- ✅ Link all docs together
- ✅ Update README prominently
- ✅ Verify Pattern 034 complete

---

**Phase 4 Start**: 2:05 PM
**Expected Done**: ~2:45 PM (40 min)
**Status**: Ready to document everything!

**LET'S FINISH THE DOCUMENTATION!** 📝

---

*"Good documentation is code for humans."*
*- Phase 4 Philosophy*

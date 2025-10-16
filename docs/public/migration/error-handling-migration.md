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
  -H "Content-Type: application/json" \
  -d '{"intent": "show me standup"}' \
  -w "\n%{http_code}\n"

# 2. Invalid request (should return 422)
curl -X POST /api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": ""}' \
  -w "\n%{http_code}\n"

# 3. Not found (should return 404)
curl -X GET /api/v1/workflows/invalid \
  -w "\n%{http_code}\n"
```

---

## Language-Specific Examples

### Python (requests)

```python
import requests

def call_api(endpoint, data):
    """Example API call with proper error handling."""
    try:
        response = requests.post(
            f"http://localhost:8001/api/v1/{endpoint}",
            json=data,
            timeout=10
        )

        # Check status code first
        if response.status_code == 200:
            return response.json()

        # Parse error response
        error = response.json()

        if response.status_code == 422:
            raise ValidationError(error['message'], error.get('details'))
        elif response.status_code == 404:
            raise NotFoundError(error['message'])
        elif response.status_code == 500:
            error_id = error.get('details', {}).get('error_id')
            raise ServerError(error['message'], error_id)
        else:
            raise APIError(f"Unexpected status: {response.status_code}")

    except requests.RequestException as e:
        raise NetworkError(f"Request failed: {e}")
```

### JavaScript/TypeScript

```typescript
interface ApiError {
  status: 'error';
  code: string;
  message: string;
  details?: Record<string, any>;
}

async function callApi(endpoint: string, data: any): Promise<any> {
  try {
    const response = await fetch(`/api/v1/${endpoint}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
      return result;
    }

    // Handle errors based on status code
    const error = result as ApiError;

    switch (response.status) {
      case 422:
        throw new ValidationError(error.message, error.details);
      case 404:
        throw new NotFoundError(error.message);
      case 500:
        throw new ServerError(error.message, error.details?.error_id);
      default:
        throw new Error(`Unexpected status: ${response.status}`);
    }
  } catch (error) {
    if (error instanceof TypeError) {
      throw new NetworkError('Network request failed');
    }
    throw error;
  }
}
```

---

## Common Migration Issues

### Issue 1: Always Checking JSON First

**Problem**:
```python
# This fails if status code is 500
data = response.json()
if data["status"] == "error":
    handle_error()
```

**Solution**:
```python
# Check status code first
if response.status_code != 200:
    error = response.json()
    handle_error(error)
```

### Issue 2: Not Handling All Status Codes

**Problem**:
```python
if response.status_code == 200:
    return response.json()
# Missing 422, 404, 500 handling
```

**Solution**:
```python
if response.status_code == 200:
    return response.json()
elif response.status_code == 422:
    handle_validation_error()
elif response.status_code == 404:
    handle_not_found()
elif response.status_code == 500:
    handle_server_error()
```

### Issue 3: Using Old Field Names

**Problem**:
```python
error_msg = response.json()["error"]  # Field doesn't exist
```

**Solution**:
```python
error_msg = response.json()["message"]  # New field name
```

---

## Validation Checklist

Before deploying your migrated code:

- [ ] Check `response.status_code` before parsing JSON
- [ ] Handle all status codes (200, 422, 404, 500)
- [ ] Use `message` field instead of `error` field
- [ ] Log `error_id` for 500 errors
- [ ] Test with all error scenarios
- [ ] Update error messages shown to users
- [ ] Add retry logic for 500 errors (optional)

---

## Affected Endpoints

All endpoints now follow Pattern 034:

### Core API
- POST /api/v1/intent
- GET /api/v1/workflows/{workflow_id}

### Personality
- GET /api/personality/profile/{user_id}
- PUT /api/personality/profile/{user_id}
- POST /api/personality/enhance

### Admin
- GET /api/standup
- All admin endpoints (/api/admin/*)

---

## Need Help?

**Questions**: File an issue on GitHub or contact the API team

**Migration Support**: Include your current code and error messages

**Bug Reports**: Include `error_id` for 500 errors

---

*Last Updated: October 16, 2025*
*Pattern: 034 - REST-Compliant Error Handling*

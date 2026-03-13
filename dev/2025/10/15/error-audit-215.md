# Error Audit Report - Issue #215

**Date**: October 15, 2025, 6:02 PM
**File**: web/app.py
**Total Endpoints**: 20
**Lines**: 653 total

---

## Summary

**Error Returns Found**: 8 distinct error return patterns
**Try/Except Blocks**: 11 total
**HTTPException Usage**: 0 (none found)
**Current Behavior**: All errors return 200 with {"status": "error", ...}

**CRITICAL**: All error responses violate REST principles by returning 200 status code.

---

## Detailed Findings by Endpoint

### 1. POST /api/v1/intent (Lines 426-486)
**Status**: CRITICAL - Main API endpoint

**Error Pattern 1** (Lines 447-451):
```python
if intent_service is None:
    return {
        "status": "error",
        "error": "IntentService not available - initialization failed",
        "detail": "Service not found in app.state",
    }
```
- **Current**: Returns 200
- **Should Return**: 500 (Internal Server Error - service unavailable)
- **Reason**: Server configuration/initialization failure

**Error Pattern 2** (Lines 466-470):
```python
if result.error:
    response["status"] = "error"
    response["error"] = result.error
    if result.error_type:
        response["error_type"] = result.error_type
```
- **Current**: Returns 200
- **Should Return**: 422 (Validation Error - semantic issue)
- **Reason**: Business logic validation failure

**Error Pattern 3** (Lines 474-486):
```python
except Exception as e:
    logger.error(f"Intent route error: {str(e)}")
    return {
        "status": "error",
        "error": f"Intent processing failed: {str(e)}",
        "metadata": {...}
    }
```
- **Current**: Returns 200
- **Should Return**: 500 (Internal Server Error)
- **Reason**: Unexpected exception

---

### 2. GET /api/v1/workflows/{workflow_id} (Lines 300-326)
**Status**: HIGH PRIORITY

**Error Pattern** (Lines 308-312, 326):
```python
if orchestration_engine is None:
    return {
        "status": "error",
        "error": "OrchestrationEngine not available",
        "workflow_id": workflow_id,
    }

except Exception as e:
    return {"status": "error", "error": str(e), "workflow_id": workflow_id}
```
- **Current**: Returns 200
- **Should Return**:
  - 500 for service unavailable
  - 404 if workflow not found (future enhancement)
- **Reason**: Service unavailable or workflow not found

---

### 3. GET /api/personality/profile/{user_id} (Lines 330-337)
**Status**: MEDIUM PRIORITY

**Error Pattern** (Lines 336-337):
```python
except Exception as e:
    return {"status": "error", "error": str(e), "user_id": user_id}
```
- **Current**: Returns 200
- **Should Return**: 404 (Not Found) or 500 (Internal Error)
- **Reason**: User profile doesn't exist or load failure

---

### 4. PUT /api/personality/profile/{user_id} (Lines 340-363)
**Status**: MEDIUM PRIORITY

**Error Pattern 1** (Lines 357-361):
```python
return {
    "status": "error",
    "error": "Failed to save personality configuration",
    "user_id": user_id,
}
```
- **Current**: Returns 200
- **Should Return**: 500 (Internal Server Error)
- **Reason**: Save operation failed

**Error Pattern 2** (Lines 362-363):
```python
except Exception as e:
    return {"status": "error", "error": str(e), "user_id": user_id}
```
- **Current**: Returns 200
- **Should Return**: 422 (Validation Error) or 500 (Internal Error)
- **Reason**: Invalid data or save failure

---

### 5. POST /api/personality/enhance (Lines 366-391)
**Status**: MEDIUM PRIORITY

**Error Pattern** (Lines 390-391):
```python
except Exception as e:
    return {"status": "error", "error": str(e)}
```
- **Current**: Returns 200
- **Should Return**: 422 (Validation Error) or 500 (Internal Error)
- **Reason**: Enhancement failure (validation or processing)

---

### 6. GET /api/standup (Lines 394-423)
**Status**: MEDIUM PRIORITY (Proxy endpoint)

**Error Pattern** (Lines 408-423):
```python
except Exception as e:
    return {
        "status": "error",
        "error": f"Backend API unavailable: {str(e)}",
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source": "web-proxy",
            "version": "1.0",
            "error_type": "ProxyError",
            "recovery_suggestions": [...]
        },
    }
```
- **Current**: Returns 200
- **Should Return**: 502 (Bad Gateway) or 503 (Service Unavailable)
- **Reason**: Backend service unavailable

---

### 7. Health/Admin Endpoints (No Errors Found)
**Status**: ✅ COMPLIANT

The following endpoints have NO error handling issues:
- GET /health/config (Lines 505-527)
- GET /api/admin/intent-monitoring (Lines 527-538)
- GET /api/admin/intent-cache-metrics (Lines 538-557)
- POST /api/admin/intent-cache-clear (Lines 557-576)
- GET /api/admin/piper-config-cache-metrics (Lines 576-590)
- POST /api/admin/piper-config-cache-clear (Lines 590-604)
- GET /api/admin/user-context-cache-metrics (Lines 604-618)
- POST /api/admin/user-context-cache-clear (Lines 618-632)
- GET /health (Lines 632-647)
- POST /api/admin/user-context-cache-invalidate/{session_id} (Lines 647-653)

These return success responses only (no error paths).

---

### 8. UI Endpoints (No Errors Found)
**Status**: ✅ COMPLIANT

- GET / (Lines 293-296) - Template rendering
- GET /standup (Lines 489-490) - Template rendering
- GET /personality-preferences (Lines 495-505) - Static file serving
- GET /debug-markdown (Lines 232-290) - Debug page

No error handling needed (templates/static files).

---

## Error Patterns by Type

### Pattern 1: Try/Except with Generic Error Return
**Count**: 8 occurrences
**Lines**: 326, 337, 363, 391, 408, 447, 467, 474
**Current**:
```python
try:
    # operation
except Exception as e:
    return {"status": "error", "error": str(e)}  # Returns 200!
```
**Fix**: Use validation_error() for semantic errors, internal_error() for unexpected

### Pattern 2: Conditional Error Return (No Exception)
**Count**: 2 occurrences
**Lines**: 308-312 (service unavailable), 357-361 (save failed)
**Current**:
```python
if condition_failed:
    return {"status": "error", "error": "..."}  # Returns 200!
```
**Fix**: Use appropriate error utility based on failure type

### Pattern 3: Service Result Error Passthrough
**Count**: 1 occurrence
**Lines**: 466-470 (intent endpoint)
**Current**:
```python
if result.error:
    response["status"] = "error"
    response["error"] = result.error  # Returns 200!
```
**Fix**: Map service errors to appropriate HTTP status codes

---

## Endpoints Requiring Updates

### High Priority (Core Functionality)
1. **POST /api/v1/intent** (Lines 426-486)
   - Reason: Main API endpoint, most critical
   - Errors: 3 different error patterns
   - Impact: All API consumers affected

2. **GET /api/v1/workflows/{workflow_id}** (Lines 300-326)
   - Reason: Workflow status polling (Bug #166 fix)
   - Errors: 2 error patterns
   - Impact: UI polling functionality

### Medium Priority (Feature Endpoints)
3. **GET /api/personality/profile/{user_id}** (Lines 330-337)
4. **PUT /api/personality/profile/{user_id}** (Lines 340-363)
5. **POST /api/personality/enhance** (Lines 366-391)
6. **GET /api/standup** (Lines 394-423)

### Low Priority (Admin/Debug)
- None with errors

---

## HTTP Status Code Mapping

| Current Behavior | Correct Status Code | Error Type |
|-----------------|--------------------|-----------|
| 200 + error JSON | 422 | Validation/semantic errors |
| 200 + error JSON | 500 | Unexpected exceptions |
| 200 + error JSON | 502/503 | Backend unavailable |
| 200 + error JSON | 404 | Resource not found |

---

## Impact Analysis

### Breaking Changes
- **YES**: HTTP status codes will change from 200 to appropriate error codes
- **Mitigation**: Response JSON format remains same (`{"status": "error", ...}`)
- **Client Impact**: Clients must check `response.status_code` not just JSON

### Backward Compatibility
- **Response Format**: ✅ PRESERVED - `{"status": "error", ...}` unchanged
- **Status Codes**: ❌ BREAKING - 200 → proper codes (422, 500, etc.)
- **Migration Path**: Clear - check status code instead of JSON field first

---

## Recommendations

### Implementation Order
1. **Phase 1**: Fix intent endpoint (most critical, most errors)
2. **Phase 2**: Fix workflow endpoint (UI polling)
3. **Phase 3**: Fix personality endpoints (3 endpoints)
4. **Phase 4**: Fix standup proxy (backend connectivity)

### Estimated Effort
- **Original estimate**: 8-12 hours
- **Revised estimate**: 4-5 hours
  - Error utility: 30 min (Phase 0)
  - Intent endpoint: 45 min (Phase 1)
  - Other endpoints: 2 hours (Phase 2)
  - Test updates: 1.5 hours (Phase 3)
  - Documentation: 30 min (Phase 4)

### Test Coverage
- **Existing tests**: Need updates to expect new status codes
- **New tests**: Error utility tests (Phase 0)
- **Integration tests**: Test each endpoint's error paths

---

## Key Insights

1. **Consistent Pattern**: All errors use same JSON format (easy to standardize)
2. **No Existing Utilities**: Clean slate for error_responses.py
3. **Limited Scope**: Only 6 endpoints need updates (not 20)
4. **Clear Mapping**: Error types map clearly to HTTP status codes

---

## Next Steps (Phase 0 → Phase 1)

**Phase 0 Complete**:
- ✅ Audit complete
- ✅ All error patterns documented
- ✅ Priorities identified
- 🔜 Create error utility module
- 🔜 Write utility tests

**Phase 1 Ready**:
- Target: POST /api/v1/intent endpoint
- Complexity: 3 error patterns to fix
- Estimated time: 45-60 minutes
- Blocker: None (utility module first)

---

**Audit Complete**: 6:02 PM
**Duration**: 13 minutes
**Next Step**: Create error standards document (Step 2)

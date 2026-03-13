# Phase 2 - Endpoints to Update

**Source**: Phase 0 audit from October 15 (error-audit-215.md)
**Date**: October 16, 2025, 12:47 PM
**Phase**: 2 of 4

---

## Endpoints Already Done

1. ✅ **POST /api/v1/intent** (Lines 426-486) - Phase 1 COMPLETE
   - Returns 422 for validation errors
   - Returns 500 for service unavailable/unexpected
   - Returns 200 for success
   - Tested and validated

---

## Endpoints Remaining

### Batch 1: Workflow Endpoints (HIGH PRIORITY)

2. **GET /api/v1/workflows/{workflow_id}** (Lines 300-326)
   - Current: Returns 200 for all errors
   - Fix needed:
     - Service unavailable → 500 (internal_error)
     - Workflow not found → 404 (not_found_error)
     - Unexpected errors → 500 (internal_error)
   - Status: ⏳ TODO

---

### Batch 2: Personality & Proxy Endpoints (MEDIUM PRIORITY)

3. **GET /api/personality/profile/{user_id}** (Lines 330-337)
   - Current: Returns 200 for all errors
   - Fix needed:
     - Profile not found → 404 (not_found_error)
     - Load failure → 500 (internal_error)
   - Status: ⏳ TODO

4. **PUT /api/personality/profile/{user_id}** (Lines 340-363)
   - Current: Returns 200 for all errors
   - Fix needed:
     - Save failed → 500 (internal_error)
     - Invalid data → 422 (validation_error)
     - Unexpected → 500 (internal_error)
   - Status: ⏳ TODO

5. **POST /api/personality/enhance** (Lines 366-391)
   - Current: Returns 200 for all errors
   - Fix needed:
     - Validation errors → 422 (validation_error)
     - Processing errors → 500 (internal_error)
   - Status: ⏳ TODO

6. **GET /api/standup** (Lines 394-423)
   - Current: Returns 200 for all errors
   - Fix needed:
     - Backend unavailable → 502 (bad_gateway_error) or 503 (service_unavailable_error)
     - Unexpected → 500 (internal_error)
   - Status: ⏳ TODO

---

### Batch 3: Admin/Debug Endpoints (LOW PRIORITY)

**Status**: ✅ ALL COMPLIANT

From audit - these endpoints already compliant (no error paths or return success only):
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

**Action**: Verify these still work, no changes needed.

---

## UI Endpoints (No Action Needed)

**Status**: ✅ COMPLIANT

From audit - template/static rendering only (no error handling needed):
- GET / (Lines 293-296)
- GET /standup (Lines 489-490)
- GET /personality-preferences (Lines 495-505)
- GET /debug-markdown (Lines 232-290)

---

## Total Remaining: 5 endpoints

**Batch 1**: 1 endpoint (workflow)
**Batch 2**: 4 endpoints (personality x3 + standup proxy)
**Batch 3**: 0 endpoints (verify only)

---

## Error Utility Functions (from web/app.py)

Available functions for use:
```python
from web.error_responses import (
    validation_error,       # 422 - semantic/validation errors
    not_found_error,        # 404 - resource doesn't exist
    internal_error,         # 500 - unexpected errors
    service_unavailable,    # 503 - service down (optional)
    bad_gateway_error,      # 502 - backend service error (optional)
)
```

---

## Status Summary

- **Already Done**: 1 endpoint (intent)
- **To Update**: 5 endpoints
- **No Changes**: 10+ admin/UI endpoints
- **Total in web/app.py**: 20 endpoints

---

**Phase 2 Ready**: Let's update these 5 endpoints! 🎯

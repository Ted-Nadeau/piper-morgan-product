# Issue #4 Investigation: Standup Generation Button Hangs

**Date**: November 23, 2025
**Investigator**: Code Agent
**Duration**: 12 minutes
**Status**: Complete

---

## Summary

The "Generate Standup" button hangs indefinitely because the proxy endpoint `/api/standup` calls itself, creating an infinite loop or timeout. Additionally, the proxy uses HTTP GET but the backend endpoint requires POST. This is a **Type A: Quick Fix** - two line changes in the proxy endpoint.

---

## Frontend Analysis

**Button Location**: `templates/standup.html:129`

```html
<button onclick="loadStandup()" id="loadBtn">Generate Standup</button>
```

**JavaScript Handler**: `templates/standup.html:136-241`

**Function Name**: `loadStandup()`

**Status**: ✅ Exists and wired correctly

**API Call**: Line 147
```javascript
const response = await fetch("/api/standup?format=human-readable");
```

**Frontend Implementation**:
- ✅ Button exists and is wired
- ✅ Click handler calls `loadStandup()`
- ✅ Shows loading spinner while waiting
- ✅ Handles response parsing (success/error paths)
- ✅ Displays metrics and results
- ✅ Error handling with try/catch

**Status**: Frontend is 100% complete and correctly implemented

---

## Backend Analysis

**Frontend Proxy Endpoint**: `/api/standup` (web/app.py:891-912)

```python
@app.get("/api/standup")
async def standup_proxy(
    format: str = Query("raw", description="Response format"),
    personality: bool = Query(False)
):
    """Proxy standup requests to backend API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/api/standup",  # <-- PROBLEM: Calls itself!
            params={"format": format, "personality": personality}
        )
        return response.json()
```

**Actual Standup Router**: `/api/v1/standup` (web/api/routes/standup.py)

- ✅ Router exists and is mounted at `/api/v1/standup`
- ✅ POST `/api/v1/standup/generate` endpoint exists (line 529)
- ✅ Endpoint is fully implemented with proper authentication and modes
- ✅ Takes `StandupRequest` with mode and format parameters
- ✅ Returns properly formatted `StandupResponse`

**Status**: ✅ Backend endpoint exists, but proxy is calling wrong endpoint

---

## Root Cause

**Classification**: **Type A (Quick Fix)**

**The Issues**:

1. **Wrong Endpoint Path**: Proxy at `/api/standup` calls `{API_BASE_URL}/api/standup`
   - This is **itself** (infinite loop)
   - Should call `/api/v1/standup/generate` instead
   - `API_BASE_URL` = `http://localhost:8001` (from port configuration)
   - Actual call: `http://localhost:8001/api/standup` (the proxy itself)

2. **Wrong HTTP Method**: Proxy uses GET but backend endpoint is POST
   - Frontend calls GET `/api/standup`
   - Proxy calls GET to backend
   - Backend endpoint is POST `/api/v1/standup/generate`
   - Mismatch causes request to fail or timeout

**Why This Happened**:
The proxy was added as a compatibility layer but references the wrong backend endpoint. The standup router was moved to `/api/v1/` but the proxy wasn't updated. This is 75% complete code - proxy exists but calls wrong endpoint.

---

## Manual Testing Evidence

**Frontend Behavior**:
- Click "Generate Standup" button
- Shows: "⏱️ Generating your morning standup..."
- Spinner shows indefinitely (never completes)
- Loading state never clears
- Button stays disabled
- No error shown to user

**Root Cause**:
- Proxy tries to call itself
- Creates infinite loop or timeout (likely httpx timeout after 30+ seconds)
- User sees spinner forever

---

## Fix Estimate

**Effort**: 2-5 minutes (Type A)

**What Needs to Happen**:

1. **Change proxy endpoint** (line 901-902 in web/app.py):
   - FROM: `f"{API_BASE_URL}/api/standup"`
   - TO: `f"{API_BASE_URL}/api/v1/standup/generate"`

2. **Change HTTP method** (line 901 in web/app.py):
   - FROM: `client.get(`
   - TO: `client.post(`

3. **Add mode parameter** (optional but recommended):
   - Frontend sends `format=human-readable`
   - Backend also expects `mode=standard` (or other mode)
   - Could default to `mode=standard` if not provided

**Complexity**: Very Simple (straightforward endpoint path fix)

---

## Recommendation

**Action**: **FIX NOW** (Type A - Quick fix, blocks core functionality)

**Reasoning**:
1. Frontend is 100% complete
2. Backend is 100% complete
3. Only issue is proxy calling wrong endpoint
4. One-line fix (change endpoint path)
5. Blocks core standup feature (high priority for alpha)
6. No architectural changes needed
7. Very low risk of regression

**Implementation**:
1. Fix proxy endpoint path
2. Change GET to POST
3. Test button clicks and generates standup
4. Test with different format parameters

---

## Evidence

**Frontend Button**: templates/standup.html:129
**JavaScript Handler**: templates/standup.html:136-241
**API Call**: templates/standup.html:147
**Proxy Endpoint**: web/app.py:891-912 (lines 901-902 - THE PROBLEM)
**Backend Router**: web/api/routes/standup.py:529-570+
**Root Cause**: Proxy calls `{API_BASE_URL}/api/standup` (itself) instead of `{API_BASE_URL}/api/v1/standup/generate`

---

## Next Steps

1. Fix the proxy endpoint path and HTTP method
2. Test button in browser (should generate standup with metrics)
3. Verify spinner clears and results display
4. Test with different format parameters if supported

---

## Git History

**Proxy Endpoint Created**: Appears to be from Option B work (based on commit messages)
**Last Modified**: Not recently (stable code with bug)
**Context**: This is working code with a typo/wrong endpoint reference

---

**Priority**: FIX NOW - Quick win that unblocks core feature

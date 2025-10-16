# Gameplan: CORE-ERROR-STANDARDS #215
**Standardize Error Handling Across All Endpoints**

**Date**: October 15, 2025, 5:35 PM  
**Sprint**: A2 - Notion & Errors  
**Issue**: #215  
**Estimated Duration**: 8-12 hours (1 focused day)  
**Chief Architect**: Lead Developer Sonnet

---

## Phase -1: Infrastructure Verification (MANDATORY)

### Current Understanding (Based on Architecture Docs)

**Web Framework**: FastAPI
- Location: `web/app.py` (single file, not routes/)
- Port: 8001
- Current behavior: Returns 200 with error JSON for validation errors

**Endpoint Types**:
- Intent endpoints: `/api/v1/intent`
- API endpoints: Various under `/api/v1/`
- Health checks: `/health`, `/ready`
- Admin endpoints: (need to verify)
- Plugin endpoints: (need to verify)

**Current Error Patterns** (from issue):
- Invalid JSON → 200 with `{"status": "error", ...}`
- Some endpoints → 422 for validation
- Some endpoints → 400 for bad requests
- Inconsistent across system

**Testing**:
- Framework: pytest
- Location: `tests/` directory
- Need to update test expectations

### PM Verification Required

**Please verify by running**:

```bash
# 1. Confirm web framework and structure
ls -la web/
cat web/app.py | head -50

# 2. Find all endpoints
grep -r "@app\." web/ --include="*.py" | grep -E "(get|post|put|delete)" | head -20

# 3. Find current error handling patterns
grep -r "return.*error\|raise.*Error" web/ services/ --include="*.py" -B 2 -A 2 | head -40

# 4. Check existing error responses
grep -r "status.*error\|HTTPException" web/ --include="*.py" -B 2 -A 2 | head -30

# 5. Find test files that check error codes
find tests/ -name "*.py" -exec grep -l "status_code\|assert.*200\|assert.*422\|assert.*400" {} \; | head -10
```

**Questions**:
1. Are there admin or plugin-specific endpoints beyond main API?
2. Any middleware handling errors globally?
3. Are there existing error handler decorators/utilities?
4. What's the current test pass rate for error-related tests?

### Proceed/Revise Decision
- [ ] **PROCEED** - Understanding correct, continue with gameplan
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: __________

---

## Phase 0: Initial Bookending - Audit & Standards Definition

### Duration: 2-3 hours

### Objectives
1. Document ALL current error patterns
2. Define REST-compliant error standards
3. Create error response utility
4. List all endpoints to update

### Tasks

#### Task 1: Complete Error Audit (60 min)

**Find all error responses**:
```bash
# Document in /tmp/error-audit.md

# 1. All API endpoints
grep -r "@app\." web/ --include="*.py" > /tmp/all-endpoints.txt

# 2. All error returns
grep -r "return.*{.*error" web/ services/ --include="*.py" -B 3 -A 3 > /tmp/error-returns.txt

# 3. All HTTPExceptions
grep -r "HTTPException\|raise.*Error" web/ services/ --include="*.py" -B 3 -A 3 > /tmp/exceptions.txt

# 4. All status codes
grep -r "status_code.*=\|return.*[0-9]{3}" web/ --include="*.py" > /tmp/status-codes.txt
```

**Create audit report**:
```markdown
# Error Audit Report

## Endpoints by Category
### Intent Endpoints
- POST /api/v1/intent
  - Current: Returns 200 with error JSON
  - Should be: 422 for validation errors

### API Endpoints
[List each endpoint with current behavior]

### Health/Admin Endpoints
[List each endpoint with current behavior]

## Current Error Patterns Found
1. Pattern: Return 200 with error JSON
   - Used in: [list files/functions]
   - Count: X occurrences

2. Pattern: HTTPException with 422
   - Used in: [list files/functions]
   - Count: Y occurrences

3. Pattern: HTTPException with 400
   - Used in: [list files/functions]
   - Count: Z occurrences

## Summary
- Total endpoints: [count]
- Need update: [count]
- Already correct: [count]
```

#### Task 2: Define Error Standards (30 min)

**Create ADR or pattern document**:

Location: `docs/internal/architecture/current/patterns/error-handling-standards.md`

```markdown
# Error Handling Standards

## HTTP Status Codes

### 200 OK
**Use for**: Successful requests only
**Response format**:
```json
{
    "status": "success",
    "data": { ... }
}
```

### 400 Bad Request
**Use for**: Malformed request syntax
**Examples**:
- Invalid JSON syntax
- Missing required headers
- Malformed URL parameters

**Response format**:
```json
{
    "status": "error",
    "code": "BAD_REQUEST",
    "message": "Request syntax is malformed",
    "details": {
        "issue": "Invalid JSON: unexpected token at line 5"
    }
}
```

### 422 Unprocessable Entity
**Use for**: Valid syntax but semantic errors
**Examples**:
- Invalid field values
- Business rule violations
- Missing required fields

**Response format**:
```json
{
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
        "field": "intent",
        "issue": "Intent cannot be empty"
    }
}
```

### 404 Not Found
**Use for**: Resource doesn't exist
**Response format**:
```json
{
    "status": "error",
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": {
        "resource": "user",
        "id": "12345"
    }
}
```

### 500 Internal Server Error
**Use for**: Unexpected server errors
**Response format**:
```json
{
    "status": "error",
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "details": {
        "error_id": "uuid-for-tracking"
    }
}
```

**CRITICAL**: Never expose stack traces or internal details in 500 errors.

## Error Codes Enumeration
```python
class ErrorCode(str, Enum):
    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    # Add more as needed
```

## Implementation Guidelines
1. Use error utility functions (see below)
2. Log all errors with appropriate level
3. Include request_id for tracing
4. Sanitize error details for production
```

#### Task 3: Create Error Utility (30 min)

**File**: `web/utils/error_responses.py` (or appropriate location)

```python
"""
Standard error response utilities for REST API compliance.
"""
from enum import Enum
from typing import Dict, Optional, Any
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class ErrorCode(str, Enum):
    """Standard error codes for API responses."""
    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"

def error_response(
    status_code: int,
    code: ErrorCode,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create standardized error response.
    
    Args:
        status_code: HTTP status code
        code: Error code from ErrorCode enum
        message: User-friendly error message
        details: Optional additional error details
        
    Returns:
        JSONResponse with standardized error format
    """
    response_body = {
        "status": "error",
        "code": code.value,
        "message": message
    }
    
    if details:
        response_body["details"] = details
        
    return JSONResponse(
        status_code=status_code,
        content=response_body
    )

def bad_request_error(message: str, details: Optional[Dict[str, Any]] = None) -> JSONResponse:
    """Return 400 Bad Request error."""
    return error_response(400, ErrorCode.BAD_REQUEST, message, details)

def validation_error(message: str, details: Optional[Dict[str, Any]] = None) -> JSONResponse:
    """Return 422 Validation Error."""
    return error_response(422, ErrorCode.VALIDATION_ERROR, message, details)

def not_found_error(message: str, details: Optional[Dict[str, Any]] = None) -> JSONResponse:
    """Return 404 Not Found error."""
    return error_response(404, ErrorCode.NOT_FOUND, message, details)

def internal_error(message: str = "An unexpected error occurred") -> JSONResponse:
    """
    Return 500 Internal Server Error.
    Never include sensitive details in production.
    """
    return error_response(
        500,
        ErrorCode.INTERNAL_ERROR,
        message,
        details={"error_id": str(uuid.uuid4())}  # For log correlation
    )
```

#### Task 4: Test Error Utility (30 min)

**File**: `tests/utils/test_error_responses.py`

```python
"""Tests for standardized error responses."""
import pytest
from web.utils.error_responses import (
    bad_request_error,
    validation_error,
    not_found_error,
    internal_error,
    ErrorCode
)

def test_bad_request_error():
    """Test 400 error response format."""
    response = bad_request_error("Invalid JSON", {"issue": "Syntax error"})
    assert response.status_code == 400
    body = json.loads(response.body)
    assert body["status"] == "error"
    assert body["code"] == "BAD_REQUEST"
    assert body["message"] == "Invalid JSON"
    assert body["details"]["issue"] == "Syntax error"

def test_validation_error():
    """Test 422 error response format."""
    response = validation_error(
        "Validation failed",
        {"field": "intent", "issue": "Cannot be empty"}
    )
    assert response.status_code == 422
    body = json.loads(response.body)
    assert body["code"] == "VALIDATION_ERROR"

# More tests...
```

### Deliverables Phase 0
- [ ] Complete error audit report (`/tmp/error-audit.md`)
- [ ] Error standards document created
- [ ] Error utility module created
- [ ] Error utility tests written and passing
- [ ] List of endpoints to update identified

### Evidence Required
- Terminal output of audit commands
- Test output showing error utility tests pass
- Count of endpoints needing update

---

## Phase 1: Update Intent Endpoint (Critical Path)

### Duration: 1-2 hours

### Objective
Fix the primary issue discovered in GREAT-5: Intent endpoint returning 200 for errors

### Current Behavior
```python
# web/app.py (or similar)
@app.post("/api/v1/intent")
async def process_intent(request: dict):
    if not request.get("intent"):
        return {"status": "error", "error": "Intent required"}  # Returns 200!
```

### Target Behavior
```python
@app.post("/api/v1/intent")
async def process_intent(request: dict):
    if not request.get("intent"):
        return validation_error(
            "Intent required",
            {"field": "intent", "issue": "Cannot be empty"}
        )  # Returns 422!
```

### Tasks

#### Task 1: Update Intent Endpoint (30 min)
```bash
# Find and update intent endpoint
grep -n "def.*intent" web/app.py

# Update to use error utility
# Replace all error returns with proper status codes
```

#### Task 2: Update Intent Tests (30 min)
```bash
# Find intent tests
find tests/ -name "*intent*"

# Update test expectations
# Old: assert response.status_code == 200 and "error" in response.json()
# New: assert response.status_code == 422
```

#### Task 3: Validate Intent Endpoint (30 min)
```bash
# Start server
python main.py

# Test invalid request
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"invalid": "structure"}'

# Should return:
# HTTP/1.1 422 Unprocessable Entity
# {"status":"error","code":"VALIDATION_ERROR",...}

# Test valid request (should still work)
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "test intent"}'

# Should return 200 with success
```

### Deliverables Phase 1
- [ ] Intent endpoint updated
- [ ] Intent tests updated
- [ ] Real API validation complete
- [ ] No regressions in valid requests

### Evidence Required
- Diff showing code changes
- Test output showing updated tests pass
- curl output showing correct status codes

---

## Phase 2: Update All API Endpoints

### Duration: 3-4 hours

### Objective
Apply error standards to all remaining endpoints

### Approach
Work through endpoint list from Phase 0 audit, updating each one:

#### Template for Each Endpoint

**Before**:
```python
@app.post("/api/v1/some-endpoint")
async def some_endpoint(data: dict):
    if not data.get("required_field"):
        return {"status": "error", "error": "Field required"}
```

**After**:
```python
@app.post("/api/v1/some-endpoint")
async def some_endpoint(data: dict):
    if not data.get("required_field"):
        return validation_error(
            "Validation failed",
            {"field": "required_field", "issue": "Field is required"}
        )
```

### Tasks

#### Task 1: Update Health/Admin Endpoints (60 min)
```bash
# Find health endpoints
grep -n "health\|ready" web/app.py

# Update error handling
# Health checks should return appropriate status codes
```

#### Task 2: Update Plugin Endpoints (60 min)
```bash
# Find plugin endpoints
grep -r "plugin" web/ --include="*.py"

# Update to use error utility
```

#### Task 3: Update Remaining API Endpoints (60 min)
```bash
# Work through list from Phase 0 audit
# Update each endpoint systematically
```

#### Task 4: Add Global Error Handler (30 min)
```python
# Add to web/app.py
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Catch all unhandled exceptions and return 500."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return internal_error()  # Never expose stack trace

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Convert ValueError to 400."""
    return bad_request_error(str(exc))
```

### Deliverables Phase 2
- [ ] All endpoints updated
- [ ] Global error handlers added
- [ ] No stack traces in responses
- [ ] All endpoints follow standards

### Evidence Required
- List of updated endpoints with file:line references
- Sample responses from each endpoint type
- Confirmation no stack traces leak

---

## Phase 3: Update All Tests

### Duration: 2-3 hours

### Objective
Update test expectations to match new error behavior

### Strategy
1. Find all tests checking error responses
2. Update status code assertions
3. Update response format assertions
4. Verify no regressions

### Tasks

#### Task 1: Find All Error Tests (30 min)
```bash
# Create comprehensive list
grep -r "status_code.*200.*error\|assert.*error" tests/ --include="*.py" > /tmp/error-tests.txt

# Count tests to update
wc -l /tmp/error-tests.txt
```

#### Task 2: Update Test Expectations (90 min)
```python
# Old pattern:
response = client.post("/api/v1/intent", json={"invalid": "data"})
assert response.status_code == 200
assert "error" in response.json()

# New pattern:
response = client.post("/api/v1/intent", json={"invalid": "data"})
assert response.status_code == 422
assert response.json()["code"] == "VALIDATION_ERROR"
assert response.json()["status"] == "error"
```

#### Task 3: Run Full Test Suite (30 min)
```bash
# Run all tests
pytest tests/ -v

# Check pass rate
pytest tests/ --tb=short -q

# Expected: All tests pass
```

#### Task 4: Add New Error Standard Tests (30 min)
```python
# tests/test_error_standards.py
"""Comprehensive error standard compliance tests."""

def test_all_endpoints_return_correct_status_codes():
    """Verify no endpoint returns 200 for errors."""
    # Test each endpoint with invalid input
    # Assert proper status codes

def test_error_response_format():
    """Verify all errors follow standard format."""
    # Check required fields: status, code, message

def test_no_stack_traces_in_errors():
    """Verify 500 errors don't leak internals."""
    # Trigger internal errors
    # Assert no stack traces in response
```

### Deliverables Phase 3
- [ ] All tests updated
- [ ] New error standard tests added
- [ ] Full test suite passing
- [ ] Test coverage maintained

### Evidence Required
- pytest output showing all tests pass
- Count of tests updated
- New test coverage report

---

## Phase 4: Documentation & Migration

### Duration: 1-2 hours

### Objective
Document changes and provide migration guidance

### Tasks

#### Task 1: Update API Documentation (30 min)
```markdown
# docs/public/api/error-handling.md

# Error Handling

## Standard Error Responses

All API endpoints return errors with proper HTTP status codes:

### 400 Bad Request
Returned when request syntax is malformed.

Example:
```bash
curl -X POST /api/v1/intent -d 'invalid json'
```

Response:
```json
{
  "status": "error",
  "code": "BAD_REQUEST",
  "message": "Invalid JSON syntax",
  "details": {
    "issue": "Unexpected token at line 1"
  }
}
```

### 422 Unprocessable Entity
Returned when request is syntactically correct but semantically invalid.

[Document all error types]

## Breaking Changes

**If you're consuming the API**:
- Check `status_code` instead of `response.json()["status"]`
- Handle 422 for validation errors (previously 200)
- Handle 400 for malformed requests
- Error format remains same (`{"status":"error",...}`)
```

#### Task 2: Update Client Documentation (30 min)
```markdown
# docs/public/user-guides/api-clients.md

# API Client Guide

## Error Handling

Handle errors by checking HTTP status code:

```python
response = requests.post("http://localhost:8001/api/v1/intent", json=data)

if response.status_code == 200:
    # Success
    result = response.json()
elif response.status_code == 422:
    # Validation error
    error = response.json()
    print(f"Validation failed: {error['message']}")
elif response.status_code == 500:
    # Server error
    print("Internal error occurred")
```

## Migration from 200-with-error Pattern

**Old code**:
```python
response = requests.post(url, json=data)
if response.json().get("status") == "error":
    handle_error()
```

**New code**:
```python
response = requests.post(url, json=data)
if response.status_code != 200:
    handle_error()
```
```

#### Task 3: Create Migration Checklist (30 min)
```markdown
# Migration Checklist for API Consumers

If you're consuming Piper Morgan's API, follow this checklist:

- [ ] Update error checking to use `response.status_code`
- [ ] Handle 422 for validation errors
- [ ] Handle 400 for bad requests
- [ ] Handle 404 for not found
- [ ] Handle 500 for server errors
- [ ] Update tests to expect new status codes
- [ ] Verify error response format still works

## Backward Compatibility

The error response format remains the same:
```json
{"status": "error", "code": "...", "message": "...", "details": {...}}
```

Only the HTTP status code changed from 200 to proper codes.
```

### Deliverables Phase 4
- [ ] API documentation updated
- [ ] Client guide updated
- [ ] Migration checklist created
- [ ] Breaking changes documented

### Evidence Required
- Documentation files created/updated
- Clear migration path documented

---

## Phase Z: Final Bookending & Handoff

### Duration: 30-45 minutes

### Objective
Ensure issue is complete and ready for PM approval

### Tasks

#### Task 1: Issue Verification Checklist

Go through EVERY acceptance criterion:

```markdown
## Acceptance Criteria Verification

- [ ] Error standards documented in ADR/pattern
  - Location: docs/internal/architecture/current/patterns/error-handling-standards.md
  - Evidence: [file path]

- [ ] All endpoints audited and listed
  - Report: /tmp/error-audit.md
  - Total endpoints: [count]
  - Updated: [count]

- [ ] All endpoints follow standards
  - Evidence: [grep output showing proper status codes]
  - Tested: [curl commands showing correct behavior]

- [ ] Tests updated for new behavior
  - Tests updated: [count]
  - All passing: [pytest output]

- [ ] No 500 errors leak stack traces
  - Global handler: [code location]
  - Tested: [curl command triggering 500]
  - Evidence: [response showing no stack trace]

- [ ] Client documentation updated
  - API docs: [file path]
  - Migration guide: [file path]
  - Breaking changes: [documented where]
```

#### Task 2: Run Complete Validation

```bash
# Full test suite
pytest tests/ -v > /tmp/final-test-output.txt

# Test error responses manually
./scripts/test_error_standards.sh

# Security check for stack traces
./scripts/security_check.sh

# Document results
cat /tmp/final-test-output.txt >> session-log.md
```

#### Task 3: Update GitHub Issue

```bash
# Update issue with all evidence
gh issue edit 215 --body "$(cat updated-issue-description.md)"

# Add comment with completion evidence
gh issue comment 215 --body "All acceptance criteria met. See session log for evidence."
```

#### Task 4: Documentation Updates

```markdown
## Documentation Checklist

- [ ] Error handling pattern documented
- [ ] ADR updated (if created new)
- [ ] architecture.md updated (if flow changed)
- [ ] CURRENT-STATE.md updated
- [ ] API documentation comprehensive
- [ ] Migration guide clear
```

#### Task 5: PM Approval Request

```markdown
@PM - Issue #215 complete and ready for review:

**Completed**:
- ✅ Error standards defined and documented
- ✅ All [count] endpoints audited
- ✅ All endpoints updated to REST compliance
- ✅ [count] tests updated and passing
- ✅ Global error handler prevents stack trace leaks
- ✅ Documentation comprehensive
- ✅ Migration guide created

**Evidence**:
- Session log: dev/2025/10/15/[session-log-name].md
- Error standards: docs/internal/architecture/current/patterns/error-handling-standards.md
- Audit report: /tmp/error-audit.md
- Test output: All [count] tests passing

**Breaking Changes**:
- HTTP status codes now REST-compliant
- Migration path documented for API consumers
- Error response format unchanged (backward compatible)

**Validation**:
```bash
# Test various error conditions
curl -X POST http://localhost:8001/api/v1/intent -d '{"invalid": "json"}'
# Returns 422 ✅

# All tests pass
pytest tests/ -v
# [count] passed ✅
```

Please review and close if satisfied.
```

### Deliverables Phase Z
- [ ] All acceptance criteria verified
- [ ] Complete validation run
- [ ] GitHub issue updated
- [ ] Documentation complete
- [ ] PM approval requested

### Evidence Required
- Complete session log
- Full test output
- Manual validation results
- GitHub issue updated

---

## STOP Conditions

Stop immediately and escalate if:

1. **Breaking Changes Too Severe**
   - Existing clients break badly
   - Tests fail catastrophically
   - Need API versioning discussion

2. **Performance Issues**
   - Error handling adds noticeable latency
   - Memory leaks discovered
   - Global handler causes problems

3. **Security Concerns**
   - Stack traces still leaking
   - Sensitive data in errors
   - Error messages reveal internals

4. **Infrastructure Different**
   - Not using FastAPI as expected
   - Error handling already standardized
   - Different error utility exists

---

## Success Metrics

### Must Have (Minimum)
- ✅ Intent endpoint returns 422 (not 200) for errors
- ✅ All endpoints use proper HTTP status codes
- ✅ All tests passing
- ✅ No stack traces in production errors

### Should Have (Target)
- ✅ All above
- ✅ Global error handlers working
- ✅ Documentation comprehensive
- ✅ Migration path clear

### Nice to Have (Ideal)
- ✅ All above
- ✅ Error utility reusable
- ✅ Error codes enumerated
- ✅ Client examples provided

---

## Time Breakdown

| Phase | Task | Duration | Total |
|-------|------|----------|-------|
| -1 | Infrastructure Verification | 15 min | 15 min |
| 0 | Audit & Standards | 2-3 hours | 2-3 hours |
| 1 | Intent Endpoint | 1-2 hours | 1-2 hours |
| 2 | All Endpoints | 3-4 hours | 3-4 hours |
| 3 | Update Tests | 2-3 hours | 2-3 hours |
| 4 | Documentation | 1-2 hours | 1-2 hours |
| Z | Final Bookending | 30-45 min | 30-45 min |

**Total**: 8-12 hours (1 focused day)

---

## Agent Coordination

**Single Agent**: Claude Code (Lead Developer)
- Full-stack ownership
- API changes + tests
- Documentation updates

**Rationale**: Straightforward refactoring, no complex coordination needed

**Cross-validation**: After Phase 2 (endpoints updated)
- Verify no regressions
- Test all error paths
- Confirm standards consistent

---

## Notes

- Keep error response format same (backward compatible)
- Only HTTP status codes changing
- Document all breaking changes clearly
- Test extensively before merging
- Consider API versioning if changes too breaking

---

**Gameplan Status**: Ready for PM approval after Phase -1 verification

**Next Steps**: PM runs verification commands, confirms/corrects understanding

---

*"Standardize errors for clarity, not complexity."*  
*- REST API Philosophy*

# Code Agent Prompt: CORE-ERROR-STANDARDS #215 - Phase 0

**Date**: October 15, 2025, 6:48 PM
**Sprint**: A2 - Notion & Errors
**Issue**: #215
**Phase**: Phase 0 - Audit & Standards Definition
**Duration**: 60-90 minutes
**Agent**: Claude Code

---

## Mission

Complete error audit of all endpoints, define REST-compliant standards, create error utility module, and write tests. This sets the foundation for standardizing error handling across the entire API.

**Context**: Phase -1 verified infrastructure - single `web/app.py` with 20 endpoints, all returning 200 with error JSON. Need to establish REST-compliant standards.

**Philosophy**: "Measure twice, cut once" - comprehensive audit now prevents mistakes later.

---

## Phase -1 Verification Results

**Infrastructure Confirmed**:
- ✅ Single file: `web/app.py` (23,868 bytes)
- ✅ Framework: FastAPI
- ✅ Endpoints: 20 total
- ✅ Error pattern: `return {"status": "error", "error": str(e)}`
- ✅ No existing error utilities

**Proceed with confidence!**

---

## Step 1: Complete Error Audit (30 minutes)

### Task: Find ALL Error Returns

**Search for error patterns**:
```bash
# Find all error returns in web/app.py
grep -n "return.*error" web/app.py

# Find all try/except blocks
grep -n "except" web/app.py -B 3 -A 3

# Find all error responses
grep -n '{"status": "error"' web/app.py

# Find HTTPException usage
grep -n "HTTPException" web/app.py
```

**Document in**: `/tmp/error-audit-215.md`

### Audit Report Template

```markdown
# Error Audit Report - Issue #215

**Date**: October 15, 2025, 6:50 PM
**File**: web/app.py
**Total Endpoints**: 20

---

## Summary

**Error Returns Found**: [count]
**Try/Except Blocks**: [count]
**HTTPException Usage**: [count]
**Current Behavior**: All errors return 200 with JSON

---

## Detailed Findings

### Endpoint 1: [endpoint_name]
- **Line**: [number]
- **Current Code**:
```python
[paste actual code]
```
- **Current Behavior**: Returns 200 with error JSON
- **Should Return**: 422 (or appropriate code)
- **Reason**: [why this status code]

### Endpoint 2: [endpoint_name]
[repeat for each endpoint with error handling]

---

## Error Patterns by Type

### Pattern 1: Try/Except with Generic Error
**Count**: [X]
**Example**:
```python
try:
    # operation
except Exception as e:
    return {"status": "error", "error": str(e)}
```
**Fix**: Use validation_error() for semantic errors, internal_error() for unexpected

### Pattern 2: Validation Errors
**Count**: [Y]
**Example**:
```python
if not data.get("field"):
    return {"status": "error", "error": "Field required"}
```
**Fix**: Use validation_error() with proper field details

[Document all patterns found]

---

## Endpoints Requiring Updates

### High Priority (Core Functionality)
1. POST /api/v1/intent - [reason]
2. [other critical endpoints]

### Medium Priority
[list medium priority endpoints]

### Low Priority (Admin/Debug)
[list low priority endpoints]

---

## Recommendations

1. **Order of updates**: Start with intent endpoint (core functionality)
2. **Estimated effort**: [based on findings]
3. **Breaking changes**: [list any concerns]
4. **Test coverage**: [what needs testing]

---

**Audit Complete**: [time]
**Next Steps**: Create error standards and utility
```

**Save audit to**: `/tmp/error-audit-215.md`

---

## Step 2: Create Error Standards Document (15 minutes)

### Task: Define REST-Compliant Standards

**Create**: `docs/internal/architecture/current/patterns/error-handling-standards.md`

### Standards Document Template

```markdown
# Error Handling Standards

**Status**: ✅ Active
**Applies To**: All API endpoints
**Effective**: October 16, 2025
**Related Issue**: #215

---

## Overview

All API endpoints MUST return appropriate HTTP status codes for errors. The response body format remains consistent for backward compatibility.

---

## HTTP Status Code Standards

### 200 OK ✅ Success Only
**Use For**: Successful operations only
**Response Format**:
```json
{
    "status": "success",
    "data": { ... }
}
```

**Never use 200 for errors** - this violates REST principles.

---

### 400 Bad Request
**Use For**: Malformed request syntax
**Examples**:
- Invalid JSON syntax
- Missing required headers
- Malformed URL parameters
- Wrong content-type

**Response Format**:
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

---

### 422 Unprocessable Entity
**Use For**: Syntactically valid but semantically invalid
**Examples**:
- Empty required fields
- Invalid field values
- Business rule violations
- Type mismatches

**Response Format**:
```json
{
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
        "field": "intent",
        "issue": "Cannot be empty"
    }
}
```

---

### 404 Not Found
**Use For**: Resource doesn't exist
**Examples**:
- Workflow ID not found
- User ID not found
- Unknown endpoint

**Response Format**:
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

---

### 500 Internal Server Error
**Use For**: Unexpected server errors
**Examples**:
- Unhandled exceptions
- Service failures
- Database errors

**Response Format**:
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

**CRITICAL**: Never expose stack traces or internal details in production.

---

## Error Codes Enumeration

```python
from enum import Enum

class ErrorCode(str, Enum):
    """Standard error codes for API responses."""
    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

---

## Implementation Guidelines

### Using Error Utilities

```python
from web.utils.error_responses import validation_error, bad_request_error

@app.post("/api/v1/intent")
async def process_intent(request: dict):
    if not request.get("intent"):
        return validation_error(
            "Validation failed",
            {"field": "intent", "issue": "Cannot be empty"}
        )
    # ... process intent
```

### Logging Errors

```python
import logging
logger = logging.getLogger(__name__)

try:
    # operation
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return internal_error()  # Don't expose details to client
```

### Error Response Consistency

All error responses include:
- `status`: Always "error"
- `code`: Error code from ErrorCode enum
- `message`: User-friendly message
- `details`: Optional additional information

---

## Migration from 200-with-error Pattern

### Old Pattern (Deprecated)
```python
try:
    result = operation()
    return result
except Exception as e:
    return {"status": "error", "error": str(e)}  # Returns 200!
```

### New Pattern (Required)
```python
try:
    result = operation()
    return result
except ValueError as e:
    return validation_error(str(e))  # Returns 422
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return internal_error()  # Returns 500
```

---

## Backward Compatibility

**Response Format**: Unchanged - `{"status": "error", ...}` maintained
**Breaking Change**: HTTP status codes now correct (not always 200)

**Impact on Clients**:
- Must check `response.status_code` not just `response.json()["status"]`
- Most HTTP clients handle this automatically
- Update client tests to expect proper status codes

---

**Document Owner**: Lead Developer
**Last Updated**: October 15, 2025
**Review Date**: Sprint A3
```

**Save to**: `docs/internal/architecture/current/patterns/error-handling-standards.md`

---

## Step 3: Create Error Utility Module (25 minutes)

### Task: Build Reusable Error Functions

**Create**: `web/utils/error_responses.py`

### Error Utility Code

```python
"""
Standard error response utilities for REST API compliance.

This module provides utility functions for creating standardized error
responses with proper HTTP status codes.

Usage:
    from web.utils.error_responses import validation_error

    if not data:
        return validation_error("Data required", {"field": "data"})
"""

import uuid
import logging
from enum import Enum
from typing import Dict, Optional, Any
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


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
        status_code: HTTP status code (400, 422, 404, 500)
        code: Error code from ErrorCode enum
        message: User-friendly error message
        details: Optional additional error details

    Returns:
        JSONResponse with standardized error format

    Example:
        return error_response(422, ErrorCode.VALIDATION_ERROR, "Invalid input")
    """
    response_body = {
        "status": "error",
        "code": code.value,
        "message": message
    }

    if details:
        response_body["details"] = details

    logger.warning(
        f"Error response: {status_code} - {code.value} - {message}",
        extra={"details": details}
    )

    return JSONResponse(
        status_code=status_code,
        content=response_body
    )


def bad_request_error(
    message: str = "Request syntax is malformed",
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Return 400 Bad Request error.

    Use for malformed request syntax (invalid JSON, missing headers, etc.)

    Args:
        message: User-friendly error message
        details: Optional additional error details

    Returns:
        JSONResponse with 400 status code

    Example:
        return bad_request_error("Invalid JSON", {"issue": "Syntax error at line 5"})
    """
    return error_response(400, ErrorCode.BAD_REQUEST, message, details)


def validation_error(
    message: str = "Validation failed",
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Return 422 Validation Error.

    Use for syntactically valid but semantically invalid requests.

    Args:
        message: User-friendly error message
        details: Optional field-specific error details

    Returns:
        JSONResponse with 422 status code

    Example:
        return validation_error(
            "Required field missing",
            {"field": "intent", "issue": "Cannot be empty"}
        )
    """
    return error_response(422, ErrorCode.VALIDATION_ERROR, message, details)


def not_found_error(
    message: str = "Resource not found",
    details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Return 404 Not Found error.

    Use when requested resource doesn't exist.

    Args:
        message: User-friendly error message
        details: Optional resource identification details

    Returns:
        JSONResponse with 404 status code

    Example:
        return not_found_error(
            "Workflow not found",
            {"resource": "workflow", "id": "12345"}
        )
    """
    return error_response(404, ErrorCode.NOT_FOUND, message, details)


def internal_error(
    message: str = "An unexpected error occurred",
    error_id: Optional[str] = None
) -> JSONResponse:
    """
    Return 500 Internal Server Error.

    Use for unexpected server errors. Never exposes sensitive details.

    Args:
        message: Generic user-friendly error message
        error_id: Optional error ID for log correlation

    Returns:
        JSONResponse with 500 status code

    Example:
        try:
            # operation
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return internal_error()
    """
    if not error_id:
        error_id = str(uuid.uuid4())

    logger.error(
        f"Internal error (ID: {error_id})",
        extra={"error_id": error_id}
    )

    return error_response(
        500,
        ErrorCode.INTERNAL_ERROR,
        message,
        {"error_id": error_id}
    )
```

**Save to**: `web/utils/error_responses.py`

**Also create**: `web/utils/__init__.py` (empty file if doesn't exist)

---

## Step 4: Write Utility Tests (20 minutes)

### Task: Test Error Utility Functions

**Create**: `tests/web/utils/test_error_responses.py`

### Test Code

```python
"""Tests for standardized error responses."""

import json
import pytest
from web.utils.error_responses import (
    bad_request_error,
    validation_error,
    not_found_error,
    internal_error,
    ErrorCode
)


def test_bad_request_error_basic():
    """Test 400 error response basic format."""
    response = bad_request_error("Invalid JSON")

    assert response.status_code == 400
    body = json.loads(response.body)
    assert body["status"] == "error"
    assert body["code"] == "BAD_REQUEST"
    assert body["message"] == "Invalid JSON"


def test_bad_request_error_with_details():
    """Test 400 error response with details."""
    response = bad_request_error(
        "Invalid JSON",
        {"issue": "Syntax error at line 5"}
    )

    assert response.status_code == 400
    body = json.loads(response.body)
    assert body["details"]["issue"] == "Syntax error at line 5"


def test_validation_error_basic():
    """Test 422 error response basic format."""
    response = validation_error("Validation failed")

    assert response.status_code == 422
    body = json.loads(response.body)
    assert body["status"] == "error"
    assert body["code"] == "VALIDATION_ERROR"
    assert body["message"] == "Validation failed"


def test_validation_error_with_field_details():
    """Test 422 error response with field details."""
    response = validation_error(
        "Required field missing",
        {"field": "intent", "issue": "Cannot be empty"}
    )

    assert response.status_code == 422
    body = json.loads(response.body)
    assert body["details"]["field"] == "intent"
    assert body["details"]["issue"] == "Cannot be empty"


def test_not_found_error_basic():
    """Test 404 error response basic format."""
    response = not_found_error("Resource not found")

    assert response.status_code == 404
    body = json.loads(response.body)
    assert body["status"] == "error"
    assert body["code"] == "NOT_FOUND"
    assert body["message"] == "Resource not found"


def test_not_found_error_with_resource_details():
    """Test 404 error response with resource details."""
    response = not_found_error(
        "Workflow not found",
        {"resource": "workflow", "id": "12345"}
    )

    assert response.status_code == 404
    body = json.loads(response.body)
    assert body["details"]["resource"] == "workflow"
    assert body["details"]["id"] == "12345"


def test_internal_error_basic():
    """Test 500 error response basic format."""
    response = internal_error()

    assert response.status_code == 500
    body = json.loads(response.body)
    assert body["status"] == "error"
    assert body["code"] == "INTERNAL_ERROR"
    assert body["message"] == "An unexpected error occurred"
    assert "error_id" in body["details"]


def test_internal_error_with_custom_message():
    """Test 500 error response with custom message."""
    response = internal_error("Database connection failed")

    assert response.status_code == 500
    body = json.loads(response.body)
    assert body["message"] == "Database connection failed"


def test_internal_error_with_custom_error_id():
    """Test 500 error response with custom error ID."""
    response = internal_error(error_id="test-error-123")

    body = json.loads(response.body)
    assert body["details"]["error_id"] == "test-error-123"


def test_error_response_format_consistency():
    """Test all error responses have consistent format."""
    responses = [
        bad_request_error("Test"),
        validation_error("Test"),
        not_found_error("Test"),
        internal_error("Test")
    ]

    for response in responses:
        body = json.loads(response.body)
        # All must have these fields
        assert "status" in body
        assert "code" in body
        assert "message" in body
        # Status must always be "error"
        assert body["status"] == "error"


def test_error_codes_enum():
    """Test ErrorCode enum values."""
    assert ErrorCode.BAD_REQUEST.value == "BAD_REQUEST"
    assert ErrorCode.VALIDATION_ERROR.value == "VALIDATION_ERROR"
    assert ErrorCode.NOT_FOUND.value == "NOT_FOUND"
    assert ErrorCode.INTERNAL_ERROR.value == "INTERNAL_ERROR"
```

**Save to**: `tests/web/utils/test_error_responses.py`

**Also create**: `tests/web/__init__.py` and `tests/web/utils/__init__.py` (if needed)

---

## Step 5: Run Tests (5 minutes)

### Task: Verify Utility Works

```bash
# Run just the new tests
pytest tests/web/utils/test_error_responses.py -v

# Expected: All 12 tests pass

# Run with coverage
pytest tests/web/utils/test_error_responses.py --cov=web.utils.error_responses --cov-report=term-missing

# Expected: 100% coverage
```

**Document results** in session log

---

## Step 6: Update Session Log (5 minutes)

### Task: Document Phase 0 Completion

Add to session log:

```markdown
## Phase 0: Audit & Standards Definition - COMPLETE

**Duration**: [actual time]
**Started**: 6:50 PM
**Completed**: [time]

### Deliverables

1. ✅ **Error Audit Report**
   - Location: /tmp/error-audit-215.md
   - Endpoints audited: 20
   - Error patterns found: [count]
   - Recommendations documented

2. ✅ **Error Standards Document**
   - Location: docs/internal/architecture/current/patterns/error-handling-standards.md
   - Standards defined for all error types
   - Migration guidance provided

3. ✅ **Error Utility Module**
   - Location: web/utils/error_responses.py
   - Functions: 4 utility functions + 1 base function
   - Error codes: 4 enum values
   - Lines: ~200

4. ✅ **Utility Tests**
   - Location: tests/web/utils/test_error_responses.py
   - Tests: 12 comprehensive tests
   - Coverage: 100%
   - All passing: ✅

### Key Findings

- All errors currently return 200 (incorrect)
- [X] endpoints need updating
- Pattern is consistent (easy to fix)
- No existing error utilities (clean implementation)

### Next Steps

**Tomorrow - Phase 1**: Update intent endpoint
**Tomorrow - Phase 2**: Update all endpoints
**Tomorrow - Phase 3**: Update tests
**Tomorrow - Phase 4**: Documentation

**Estimated remaining**: 4-5 hours (not 8-12!)

---

**Phase 0 Status**: ✅ COMPLETE
```

---

## Deliverables Phase 0

When complete, you should have:

- [ ] Error audit report (`/tmp/error-audit-215.md`)
- [ ] Error standards document (`docs/internal/architecture/current/patterns/error-handling-standards.md`)
- [ ] Error utility module (`web/utils/error_responses.py`)
- [ ] Error utility tests (`tests/web/utils/test_error_responses.py`)
- [ ] All tests passing (12/12)
- [ ] Session log updated

---

## Success Criteria

**Phase 0 is complete when**:
- ✅ Every error return in app.py documented
- ✅ Standards clearly defined
- ✅ Utility module working
- ✅ Tests 100% passing
- ✅ Foundation ready for implementation

---

## Time Budget

**Target**: 60-90 minutes

- Error audit: 30 min
- Standards doc: 15 min
- Utility module: 25 min
- Tests: 20 min
- Session log: 5 min

**Total**: ~95 minutes (buffer included)

---

## What NOT to Do

- ❌ Don't update endpoints yet (that's Phase 1+)
- ❌ Don't update existing tests yet (that's Phase 3)
- ❌ Don't write documentation yet (that's Phase 4)
- ❌ Don't skip the audit (foundation is critical)

## What TO Do

- ✅ Thorough audit (find EVERY error)
- ✅ Clear standards (REST-compliant)
- ✅ Tested utility (100% coverage)
- ✅ Clean documentation (for tomorrow)

---

**Phase 0 Start**: 6:50 PM
**Expected Done**: ~8:15 PM (85 minutes)
**Status**: Ready to execute

**LET'S BUILD THE FOUNDATION!** 🏗️

---

*"A solid foundation makes the rest easy."*
*- Phase 0 Philosophy*

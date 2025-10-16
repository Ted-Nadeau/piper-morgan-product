#!/usr/bin/env python
"""
Manual test script for error_responses module.
This bypasses pytest to verify functionality directly.
"""
import sys
import json
sys.path.insert(0, '/Users/xian/Development/piper-morgan')

from web.utils.error_responses import (
    ErrorCode,
    bad_request_error,
    validation_error,
    not_found_error,
    internal_error,
)

def test_error_code_values():
    """Test ErrorCode enum."""
    assert ErrorCode.BAD_REQUEST.value == "BAD_REQUEST"
    assert ErrorCode.VALIDATION_ERROR.value == "VALIDATION_ERROR"
    assert ErrorCode.NOT_FOUND.value == "NOT_FOUND"
    assert ErrorCode.INTERNAL_ERROR.value == "INTERNAL_ERROR"
    print("✅ ErrorCode enum values correct")

def test_bad_request_error():
    """Test bad_request_error function."""
    response = bad_request_error("Test error", {"detail": "test"})
    assert response.status_code == 400
    body = json.loads(response.body.decode())
    assert body["status"] == "error"
    assert body["code"] == "BAD_REQUEST"
    assert body["message"] == "Test error"
    assert body["details"]["detail"] == "test"
    print("✅ bad_request_error works correctly")

def test_validation_error():
    """Test validation_error function."""
    response = validation_error("Validation failed", {"field": "test"})
    assert response.status_code == 422
    body = json.loads(response.body.decode())
    assert body["status"] == "error"
    assert body["code"] == "VALIDATION_ERROR"
    assert body["message"] == "Validation failed"
    assert body["details"]["field"] == "test"
    print("✅ validation_error works correctly")

def test_not_found_error():
    """Test not_found_error function."""
    response = not_found_error("Not found", {"resource": "test", "id": "123"})
    assert response.status_code == 404
    body = json.loads(response.body.decode())
    assert body["status"] == "error"
    assert body["code"] == "NOT_FOUND"
    assert body["message"] == "Not found"
    assert body["details"]["resource"] == "test"
    print("✅ not_found_error works correctly")

def test_internal_error():
    """Test internal_error function."""
    response = internal_error("Server error")
    assert response.status_code == 500
    body = json.loads(response.body.decode())
    assert body["status"] == "error"
    assert body["code"] == "INTERNAL_ERROR"
    assert body["message"] == "Server error"
    assert "error_id" in body["details"]
    print("✅ internal_error works correctly")

def test_error_structure():
    """Test all errors have consistent structure."""
    errors = [
        bad_request_error(),
        validation_error(),
        not_found_error(),
        internal_error(),
    ]
    for response in errors:
        body = json.loads(response.body.decode())
        assert body["status"] == "error"
        assert "code" in body
        assert "message" in body
    print("✅ Error structure consistent across all functions")

if __name__ == "__main__":
    print("Testing error_responses module...")
    print()

    test_error_code_values()
    test_bad_request_error()
    test_validation_error()
    test_not_found_error()
    test_internal_error()
    test_error_structure()

    print()
    print("=" * 60)
    print("✅ ALL TESTS PASSED - error_responses module is functional!")
    print("=" * 60)

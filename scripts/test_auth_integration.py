#!/usr/bin/env python3
"""Test authentication integration for standup API

Tests all auth flows for Task 3 (Authentication Integration):
1. Unauthorized access (no token) → 401
2. Invalid token → 401
3. Valid token → 200
4. All 5 modes with auth → 200
5. Public endpoints without auth → 200

Usage:
    1. Start server: uvicorn web.app:app --port 8001
    2. Run tests: python scripts/test_auth_integration.py
"""

import os
import sys

import requests

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.auth.jwt_service import JWTService

BASE_URL = "http://localhost:8001"
API_URL = f"{BASE_URL}/api/v1/standup"


def generate_test_token(user_id="test_user"):
    """Generate a test JWT token"""
    jwt_service = JWTService()
    token = jwt_service.generate_access_token(
        user_id=user_id, user_email=f"{user_id}@example.com", scopes=["read", "write"]
    )
    return token


def test_unauthorized_access():
    """Test: No token should return 401"""
    print("\n1. Testing unauthorized access (no token)...")

    response = requests.post(f"{API_URL}/generate", json={"mode": "standard", "format": "json"})

    if response.status_code == 401:
        print("   ✅ PASS: Returns 401 Unauthorized")
        print(f"   Response: {response.json()}")
        return True
    else:
        print(f"   ❌ FAIL: Expected 401, got {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_invalid_token():
    """Test: Invalid token should return 401"""
    print("\n2. Testing invalid token...")

    response = requests.post(
        f"{API_URL}/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": "Bearer invalid_token_12345"},
    )

    if response.status_code == 401:
        print("   ✅ PASS: Returns 401 Unauthorized")
        print(f"   Response: {response.json()}")
        return True
    else:
        print(f"   ❌ FAIL: Expected 401, got {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_valid_token():
    """Test: Valid token should return 200 and data"""
    print("\n3. Testing valid token...")

    token = generate_test_token()
    print(f"   Generated token: {token[:50]}...")

    response = requests.post(
        f"{API_URL}/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print("   ✅ PASS: Returns 200 OK with success=true")
            print(f"   User ID: {data.get('metadata', {}).get('user_id')}")
            print(
                f"   Performance: {data.get('performance_metrics', {}).get('generation_time_ms')}ms"
            )
            return True
        else:
            print(f"   ❌ FAIL: Got 200 but success={data.get('success')}")
            return False
    else:
        print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_all_modes_with_auth():
    """Test: All 5 modes work with valid auth"""
    print("\n4. Testing all 5 modes with valid auth...")

    token = generate_test_token()
    modes = ["standard", "issues", "documents", "calendar", "trifecta"]
    results = []

    for mode in modes:
        response = requests.post(
            f"{API_URL}/generate",
            json={"mode": mode, "format": "json"},
            headers={"Authorization": f"Bearer {token}"},
        )

        if response.status_code == 200 and response.json().get("success"):
            perf = response.json().get("performance_metrics", {}).get("generation_time_ms", "N/A")
            print(f"   ✅ {mode}: 200 OK ({perf}ms)")
            results.append(True)
        else:
            print(f"   ❌ {mode}: {response.status_code}")
            results.append(False)

    if all(results):
        print(f"   ✅ PASS: All {len(modes)} modes work with auth")
        return True
    else:
        print(f"   ❌ FAIL: {sum(results)}/{len(modes)} modes passed")
        return False


def test_public_endpoints():
    """Test: Public endpoints don't require auth"""
    print("\n5. Testing public endpoints (no auth needed)...")

    endpoints = [
        ("/health", "Health check"),
        ("/modes", "List modes"),
        ("/formats", "List formats"),
    ]

    results = []
    for path, description in endpoints:
        response = requests.get(f"{API_URL}{path}")

        if response.status_code == 200:
            print(f"   ✅ {description}: 200 OK (public)")
            results.append(True)
        else:
            print(f"   ❌ {description}: {response.status_code}")
            results.append(False)

    if all(results):
        print(f"   ✅ PASS: All {len(endpoints)} public endpoints work")
        return True
    else:
        print(f"   ❌ FAIL: {sum(results)}/{len(endpoints)} endpoints passed")
        return False


def check_server_running():
    """Check if API server is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def main():
    """Run all auth integration tests"""
    print("=" * 70)
    print("Authentication Integration Test Suite - Task 3")
    print("=" * 70)

    # Check server is running
    print("\nChecking if API server is running...")
    if not check_server_running():
        print("❌ ERROR: API server not running at http://localhost:8001")
        print("\nPlease start the server first:")
        print("  export REQUIRE_AUTH=true")
        print("  uvicorn web.app:app --port 8001")
        print("\nThen run this script again.")
        sys.exit(1)

    print("✅ API server is running")

    # Run all tests
    tests = [
        test_unauthorized_access,
        test_invalid_token,
        test_valid_token,
        test_all_modes_with_auth,
        test_public_endpoints,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"\nTests passed: {passed}/{total}")

    if all(results):
        print("\n✅ ALL TESTS PASSED - Authentication integration complete!")
        print("\nAuth Flow Enumeration:")
        print("  1. Unauthorized (no token): 401 ✅")
        print("  2. Invalid token: 401 ✅")
        print("  3. Valid token: 200 ✅")
        print("  = 3/3 auth flows verified (100%)")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} test(s) failed - please review output above")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Guidance: Server Testing Approach

**Date**: October 19, 2025, 4:20 PM
**Issue**: Bash complexity blocking auth testing
**Solution**: Use Python test script instead of complex bash

---

## Great Progress! 🎯

**You completed the hard part in 11 minutes**:
- ✅ JWT bug fixed
- ✅ Token generation script created
- ✅ REQUIRE_AUTH=true enabled
- ✅ Auth code properly implemented

**Only testing remains** - and we can make that easier!

---

## The Bash Problem

**You're hitting known issues**:
- Complex bash in tools is hard (multiline, variables, backgrounding)
- May be zsh vs bash differences
- Shell escaping is tricky
- Background server + curl testing = complexity

**Don't fight bash - use Python instead!** 🐍

---

## Recommended Approach: Python Test Script

**Create a simple Python script to test everything**:

### Step 1: Create Test Script

```python
# scripts/test_auth_integration.py
"""Test authentication integration for standup API"""

import requests
import subprocess
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.auth.jwt_service import JWTService

BASE_URL = "http://localhost:8001"
API_URL = f"{BASE_URL}/api/standup"

def generate_test_token(user_id="test_user"):
    """Generate a test JWT token"""
    jwt_service = JWTService()
    token = jwt_service.create_token({"sub": user_id})
    return token

def test_unauthorized_access():
    """Test: No token should return 401"""
    print("\n1. Testing unauthorized access (no token)...")

    response = requests.post(
        f"{API_URL}/generate",
        json={"mode": "standard", "format": "json"}
    )

    if response.status_code == 401:
        print("   ✅ PASS: Returns 401 Unauthorized")
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
        headers={"Authorization": "Bearer invalid_token_12345"}
    )

    if response.status_code == 401:
        print("   ✅ PASS: Returns 401 Unauthorized")
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
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print("   ✅ PASS: Returns 200 OK with success=true")
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
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 200 and response.json().get("success"):
            print(f"   ✅ {mode}: 200 OK")
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
        ("/formats", "List formats")
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
    print("=" * 60)
    print("Authentication Integration Test Suite")
    print("=" * 60)

    # Check server is running
    print("\nChecking if API server is running...")
    if not check_server_running():
        print("❌ ERROR: API server not running at http://localhost:8001")
        print("\nPlease start the server first:")
        print("  uvicorn main:app --reload --port 8001")
        print("\nThen run this script again.")
        sys.exit(1)

    print("✅ API server is running")

    # Run all tests
    tests = [
        test_unauthorized_access,
        test_invalid_token,
        test_valid_token,
        test_all_modes_with_auth,
        test_public_endpoints
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"\nTests passed: {passed}/{total}")

    if all(results):
        print("\n✅ ALL TESTS PASSED - Authentication integration complete!")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} test(s) failed - please review output above")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

### Step 2: How to Use

**Start server in one terminal**:
```bash
# Terminal 1 - Start API server
export REQUIRE_AUTH=true  # Make sure auth is enabled
uvicorn main:app --reload --port 8001
```

**Run tests in another terminal**:
```bash
# Terminal 2 - Run auth tests
python scripts/test_auth_integration.py
```

---

### Step 3: Expected Output

```
============================================================
Authentication Integration Test Suite
============================================================

Checking if API server is running...
✅ API server is running

1. Testing unauthorized access (no token)...
   ✅ PASS: Returns 401 Unauthorized

2. Testing invalid token...
   ✅ PASS: Returns 401 Unauthorized

3. Testing valid token...
   Generated token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ✅ PASS: Returns 200 OK with success=true

4. Testing all 5 modes with valid auth...
   ✅ standard: 200 OK
   ✅ issues: 200 OK
   ✅ documents: 200 OK
   ✅ calendar: 200 OK
   ✅ trifecta: 200 OK
   ✅ PASS: All 5 modes work with auth

5. Testing public endpoints (no auth needed)...
   ✅ Health check: 200 OK (public)
   ✅ List modes: 200 OK (public)
   ✅ List formats: 200 OK (public)
   ✅ PASS: All 3 public endpoints work

============================================================
SUMMARY
============================================================

Tests passed: 5/5

✅ ALL TESTS PASSED - Authentication integration complete!
```

---

## Why This Approach Is Better

**Advantages**:
1. ✅ No complex bash escaping
2. ✅ No background process management
3. ✅ Clear pass/fail for each test
4. ✅ Easy to debug (Python errors are clear)
5. ✅ Reusable script for future testing
6. ✅ Works same on zsh/bash/whatever

**Simplicity**:
- Start server manually (see it running)
- Run Python script (see test results)
- Clear evidence of what works/doesn't

---

## Your Task

### 1. Create the Test Script

Save the Python code above as `scripts/test_auth_integration.py`

### 2. Start the Server Manually

In your main terminal:
```bash
export REQUIRE_AUTH=true
uvicorn main:app --reload --port 8001
```

Leave this running. You'll see startup messages.

### 3. Run the Test Script

In the Claude Code tool (or another terminal):
```bash
python scripts/test_auth_integration.py
```

### 4. Capture the Output

Show us the complete output. This is your evidence.

### 5. Success Criteria

**Pass = All 5 tests green**:
- ✅ Unauthorized access rejected (401)
- ✅ Invalid token rejected (401)
- ✅ Valid token accepted (200)
- ✅ All 5 modes work with auth
- ✅ Public endpoints work without auth

---

## If Tests Fail

**The script will show you exactly what failed**:
- Which test
- What status code was returned
- What the response was

Then you can fix the specific issue and re-run.

---

## Alternative: Even Simpler

If you still have issues, we can do **manual verification**:

1. You start the server
2. You tell me "server running"
3. I give you exact curl commands
4. You paste them one at a time
5. You show me the output

But the Python script is cleaner and more professional.

---

## Summary

**Don't fight bash** - use Python:
- ✅ Create `scripts/test_auth_integration.py`
- ✅ Start server manually (one terminal)
- ✅ Run test script (Claude Code tool)
- ✅ Show complete output
- ✅ All tests should pass

**This is easier, clearer, and better evidence.** 🎯

---

**Let me know when you've created the script and I'll help you run it!**

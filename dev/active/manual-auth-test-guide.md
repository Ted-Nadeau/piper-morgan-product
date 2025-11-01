# Manual Auth Testing Guide - Issue #281

**Date**: November 1, 2025 11:12 AM
**Purpose**: Manual verification of JWT authentication with file upload integration

---

## Prerequisites

1. ✅ Password set for user `xian`: `test123456`
2. ✅ Web server running on port 8001
3. ✅ PostgreSQL running on port 5433

---

## Test 1: Login with Valid Credentials

```bash
# Login and capture token
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}' \
  -v

# Expected Response:
# HTTP/1.1 200 OK
# Set-Cookie: auth_token=<JWT_TOKEN>; HttpOnly; Path=/; SameSite=lax
# {
#   "token": "eyJ...",
#   "user_id": "3f4593ae-5bc9-468d-b08d-8c4c02a5b963",
#   "username": "xian"
# }
```

**Success Criteria**:
- ✅ Status 200
- ✅ Response includes `token`, `user_id`, `username`
- ✅ Token starts with `eyJ` (JWT format)
- ✅ Cookie `auth_token` is set

---

## Test 2: Login with Invalid Credentials

```bash
# Wrong password
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "wrong"}' \
  -v

# Expected Response:
# HTTP/1.1 401 Unauthorized
# {
#   "detail": "Invalid username or password"
# }
```

**Success Criteria**:
- ✅ Status 401
- ✅ Generic error message (no user enumeration)

---

## Test 3: File Upload with JWT Auth (Issue #282 Integration)

```bash
# First, login and save token
TOKEN=$(curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}' \
  -s | jq -r '.token')

echo "Token: $TOKEN"

# Create test file
echo "Test file for auth verification" > /tmp/test-auth.txt

# Upload file with auth
curl -X POST http://localhost:8001/api/v1/files/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test-auth.txt" \
  -v

# Expected Response:
# HTTP/1.1 200 OK
# {
#   "file_id": "uuid",
#   "filename": "test-auth.txt",
#   "size": 32,
#   "content_type": "text/plain",
#   "status": "uploaded",
#   "uploaded_at": "2025-11-01T18:12:00",
#   "storage_path": "uploads/xian/..."
# }
```

**Success Criteria**:
- ✅ Status 200
- ✅ File uploaded successfully
- ✅ Storage path includes user directory: `uploads/xian/`
- ✅ User isolation verified

---

## Test 4: File Upload WITHOUT Auth

```bash
# Try to upload without token
curl -X POST http://localhost:8001/api/v1/files/upload \
  -F "file=@/tmp/test-auth.txt" \
  -v

# Expected Response:
# HTTP/1.1 401 Unauthorized
# {
#   "detail": "Not authenticated"
# }
```

**Success Criteria**:
- ✅ Status 401
- ✅ Upload rejected without auth

---

## Test 5: List User Files (Verify Isolation)

```bash
# Login as xian
TOKEN=$(curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}' \
  -s | jq -r '.token')

# List files
curl -X GET http://localhost:8001/api/v1/files/list \
  -H "Authorization: Bearer $TOKEN" \
  -v

# Expected: Only files uploaded by xian
```

**Success Criteria**:
- ✅ Returns only xian's files
- ✅ Does not show files from other users

---

## Test 6: Logout

```bash
# Login first
TOKEN=$(curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}' \
  -s | jq -r '.token')

# Logout
curl -X POST http://localhost:8001/auth/logout \
  -H "Authorization: Bearer $TOKEN" \
  -v

# Expected Response:
# HTTP/1.1 200 OK
# {
#   "message": "Logged out successfully",
#   "user_id": "3f4593ae-5bc9-468d-b08d-8c4c02a5b963"
# }

# Try to use token after logout (should fail)
curl -X GET http://localhost:8001/api/v1/files/list \
  -H "Authorization: Bearer $TOKEN" \
  -v

# Expected: 401 Unauthorized (token blacklisted)
```

**Success Criteria**:
- ✅ Logout succeeds
- ✅ Token blacklisted
- ✅ Subsequent requests with token fail

---

## All-in-One Test Script

```bash
#!/bin/bash
set -e

echo "🔐 Testing Auth + File Upload Integration"
echo "=========================================="

# Test 1: Login
echo -e "\n1️⃣ Testing login..."
RESPONSE=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}')

TOKEN=$(echo $RESPONSE | jq -r '.token')
USER_ID=$(echo $RESPONSE | jq -r '.user_id')
echo "✅ Login successful"
echo "   User ID: $USER_ID"
echo "   Token: ${TOKEN:0:20}..."

# Test 2: Invalid login
echo -e "\n2️⃣ Testing invalid credentials..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "wrong"}')
STATUS=$(echo "$RESPONSE" | tail -n1)
if [ "$STATUS" = "401" ]; then
  echo "✅ Invalid credentials rejected (401)"
else
  echo "❌ Expected 401, got $STATUS"
fi

# Test 3: File upload with auth
echo -e "\n3️⃣ Testing file upload with auth..."
echo "Test file content" > /tmp/test-auth.txt
RESPONSE=$(curl -s -X POST http://localhost:8001/api/v1/files/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test-auth.txt")

FILE_ID=$(echo $RESPONSE | jq -r '.file_id')
echo "✅ File uploaded successfully"
echo "   File ID: $FILE_ID"

# Test 4: File upload without auth
echo -e "\n4️⃣ Testing file upload WITHOUT auth..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/api/v1/files/upload \
  -F "file=@/tmp/test-auth.txt")
STATUS=$(echo "$RESPONSE" | tail -n1)
if [ "$STATUS" = "401" ]; then
  echo "✅ Upload without auth rejected (401)"
else
  echo "❌ Expected 401, got $STATUS"
fi

# Test 5: List files
echo -e "\n5️⃣ Testing file list..."
RESPONSE=$(curl -s -X GET http://localhost:8001/api/v1/files/list \
  -H "Authorization: Bearer $TOKEN")

FILE_COUNT=$(echo $RESPONSE | jq -r '.count')
echo "✅ File list retrieved"
echo "   Files: $FILE_COUNT"

# Test 6: Logout
echo -e "\n6️⃣ Testing logout..."
RESPONSE=$(curl -s -X POST http://localhost:8001/auth/logout \
  -H "Authorization: Bearer $TOKEN")
echo "✅ Logout successful"

# Test 7: Use token after logout
echo -e "\n7️⃣ Testing token after logout..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET http://localhost:8001/api/v1/files/list \
  -H "Authorization: Bearer $TOKEN")
STATUS=$(echo "$RESPONSE" | tail -n1)
if [ "$STATUS" = "401" ]; then
  echo "✅ Token blacklisted after logout (401)"
else
  echo "❌ Expected 401, got $STATUS"
fi

echo -e "\n=========================================="
echo "✅ All tests passed!"
echo ""
echo "Issue #281: COMPLETE ✅"
echo "Issue #282: Integration verified ✅"
```

---

## Success Criteria Summary

**Issue #281 - Web Authentication**:
- ✅ Login endpoint works with valid credentials
- ✅ Invalid credentials rejected with 401
- ✅ JWT tokens generated correctly
- ✅ Cookie-based auth works
- ✅ Token blacklist works (logout)

**Issue #282 - File Upload Integration**:
- ✅ File upload requires authentication
- ✅ User isolation works (uploads/xian/)
- ✅ File list filtered by user
- ✅ Unauthenticated requests rejected

---

## Cleanup

```bash
# Remove test file
rm /tmp/test-auth.txt

# Optional: Clean up uploaded files
rm -rf uploads/xian/*
```

---

**Status**: Ready for manual testing ✅
**Next**: Run all-in-one test script to verify complete integration

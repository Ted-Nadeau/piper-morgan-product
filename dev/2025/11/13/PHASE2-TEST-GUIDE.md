# Phase 2 Manual Test Guide

**Issue**: #300 Phase 2 - User Controls API
**Test Status**: All tests passing (21/21 - 100%)
**Last Updated**: 2025-11-13

## Prerequisites

### 1. Server Running
```bash
cd /Users/xian/Development/piper-morgan
source venv/bin/activate
uvicorn web.app:app --port 8001 --host 127.0.0.1 --reload
```

### 2. Database Ready
```bash
# Check database is running
docker ps | grep piper-postgres

# Verify migrations applied
alembic current
# Should show: 3242bdd246f1 (head)
```

### 3. Test Patterns Exist
```bash
# Create test patterns (if needed)
python3 dev/2025/11/13/test_phase2_patterns.py
```

---

## Quick Test Suite

### Run All Security Tests (Recommended)
```bash
python3 dev/2025/11/13/test_phase2_security.py
```

**Expected Output**:
```
======================================================================
PHASE 2.3 SECURITY & ERROR HANDLING TESTS
======================================================================

TEST 1: Pattern Ownership Verification
  ✅ Found 2 patterns
  ✅ Can access own pattern
  ✅ Cannot access non-existent pattern (404)
  ✅ Cannot delete non-existent pattern (404)
  ✅ Cannot disable non-existent pattern (404)
  ✅ ALL OWNERSHIP TESTS PASSED!

TEST 2: Settings Validation
  ✅ Rejects threshold > 1.0 (422)
  ✅ Rejects threshold < 0.0 (422)
  ✅ Accepts valid threshold (200)
  ✅ Setting persisted correctly
  ✅ ALL VALIDATION TESTS PASSED!

TEST 3: Error Handling
  ✅ Invalid UUID format returns 422
  ✅ Non-existent pattern returns 404
  ✅ Invalid JSON returns 422
  ✅ Invalid field type returns 422
  ✅ ALL ERROR HANDLING TESTS PASSED!

🎉 ALL SECURITY TESTS PASSED!
```

---

## Manual Test Sequence (Step-by-Step)

### Test 1: List Patterns
```bash
curl -s http://localhost:8001/api/v1/learning/patterns | python3 -m json.tool
```

**Expected**:
- Status: 200 OK
- Response contains `patterns` array and `count` field
- Each pattern has all required fields (id, pattern_type, confidence, etc.)
- Patterns ordered by `last_used_at` DESC

---

### Test 2: Get Pattern Details
```bash
# Get first pattern ID (save to variable)
PATTERN_ID=$(curl -s http://localhost:8001/api/v1/learning/patterns | python3 -c "import sys, json; print(json.load(sys.stdin)['patterns'][0]['id'])")

echo "Testing pattern: $PATTERN_ID"

# Get pattern details
curl -s http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID | python3 -m json.tool
```

**Expected**:
- Status: 200 OK
- Response contains full pattern object
- All fields match the pattern from list endpoint

---

### Test 3: Disable Pattern
```bash
curl -s -X POST http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID/disable | python3 -m json.tool
```

**Expected**:
```json
{
  "success": true,
  "message": "Pattern disabled successfully",
  "pattern": {
    "id": "...",
    "enabled": false
  }
}
```

**Verify**:
```bash
curl -s http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID | python3 -c "import sys, json; p=json.load(sys.stdin); print(f'Enabled: {p[\"enabled\"]}')"
# Should print: Enabled: False
```

---

### Test 4: Enable Pattern
```bash
curl -s -X POST http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID/enable | python3 -m json.tool
```

**Expected**:
```json
{
  "success": true,
  "message": "Pattern enabled successfully",
  "pattern": {
    "id": "...",
    "enabled": true
  }
}
```

**Verify**:
```bash
curl -s http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID | python3 -c "import sys, json; p=json.load(sys.stdin); print(f'Enabled: {p[\"enabled\"]}')"
# Should print: Enabled: True
```

---

### Test 5: Delete Pattern
```bash
# Get pattern to delete (use second pattern if available)
DELETE_ID=$(curl -s http://localhost:8001/api/v1/learning/patterns | python3 -c "import sys, json; patterns=json.load(sys.stdin)['patterns']; print(patterns[1]['id'] if len(patterns) > 1 else patterns[0]['id'])")

echo "Deleting pattern: $DELETE_ID"

curl -s -X DELETE http://localhost:8001/api/v1/learning/patterns/$DELETE_ID | python3 -m json.tool
```

**Expected**:
```json
{
  "success": true,
  "message": "Pattern deleted successfully",
  "pattern_id": "..."
}
```

**Verify deletion**:
```bash
curl -s http://localhost:8001/api/v1/learning/patterns/$DELETE_ID | python3 -m json.tool
# Should return 404 error
```

---

### Test 6: Get Settings (Default)
```bash
curl -s http://localhost:8001/api/v1/learning/settings | python3 -m json.tool
```

**Expected (if not configured)**:
```json
{
  "settings": {
    "learning_enabled": true,
    "suggestion_threshold": 0.7,
    "automation_threshold": 0.9,
    "auto_apply_enabled": false,
    "notification_enabled": true
  },
  "configured": false
}
```

**Expected (if configured)**:
```json
{
  "settings": {
    "learning_enabled": true,
    "suggestion_threshold": 0.7,
    ...
    "created_at": "2025-11-13T22:51:34.859277",
    "updated_at": "2025-11-13T22:51:34.859277"
  },
  "configured": true
}
```

---

### Test 7: Update Settings (Partial)
```bash
curl -s -X PUT http://localhost:8001/api/v1/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"learning_enabled": false, "suggestion_threshold": 0.8}' | python3 -m json.tool
```

**Expected**:
```json
{
  "success": true,
  "message": "Settings updated successfully",
  "settings": {
    "learning_enabled": false,
    "suggestion_threshold": 0.8,
    "automation_threshold": 0.9,  // unchanged
    "auto_apply_enabled": false,   // unchanged
    "notification_enabled": true   // unchanged
  }
}
```

**Verify persistence**:
```bash
curl -s http://localhost:8001/api/v1/learning/settings | python3 -m json.tool
# Should show configured: true with updated values
```

---

### Test 8: Update Settings (All Fields)
```bash
curl -s -X PUT http://localhost:8001/api/v1/learning/settings \
  -H "Content-Type: application/json" \
  -d '{
    "learning_enabled": true,
    "suggestion_threshold": 0.75,
    "automation_threshold": 0.95,
    "auto_apply_enabled": true,
    "notification_enabled": false
  }' | python3 -m json.tool
```

**Expected**:
```json
{
  "success": true,
  "message": "Settings updated successfully",
  "settings": {
    "learning_enabled": true,
    "suggestion_threshold": 0.75,
    "automation_threshold": 0.95,
    "auto_apply_enabled": true,
    "notification_enabled": false
  }
}
```

---

## Error Handling Tests

### Test 9: Invalid UUID Format
```bash
curl -s http://localhost:8001/api/v1/learning/patterns/not-a-uuid | python3 -m json.tool
```

**Expected**:
- Status: 422 Unprocessable Entity
- FastAPI validation error with detail about UUID format

---

### Test 10: Non-Existent Pattern
```bash
curl -s http://localhost:8001/api/v1/learning/patterns/00000000-0000-0000-0000-000000000000 | python3 -m json.tool
```

**Expected**:
```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "Pattern 00000000-0000-0000-0000-000000000000 not found",
  "details": {
    "error_id": "PATTERN_NOT_FOUND",
    "pattern_id": "00000000-0000-0000-0000-000000000000"
  }
}
```

---

### Test 11: Invalid Threshold (Too High)
```bash
curl -s -X PUT http://localhost:8001/api/v1/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"suggestion_threshold": 1.5}' | python3 -m json.tool
```

**Expected**:
- Status: 422 Unprocessable Entity
- Pydantic validation error about threshold range

---

### Test 12: Invalid Threshold (Negative)
```bash
curl -s -X PUT http://localhost:8001/api/v1/learning/settings \
  -H "Content-Type: application/json" \
  -d '{"automation_threshold": -0.1}' | python3 -m json.tool
```

**Expected**:
- Status: 422 Unprocessable Entity
- Pydantic validation error about threshold range

---

### Test 13: Invalid JSON
```bash
curl -s -X PUT http://localhost:8001/api/v1/learning/settings \
  -H "Content-Type: application/json" \
  -d 'not valid json' | python3 -m json.tool
```

**Expected**:
- Status: 422 Unprocessable Entity
- JSON decode error

---

## Database Verification

### Check Patterns in Database
```bash
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "
  SELECT id, pattern_type, enabled, confidence, usage_count
  FROM learned_patterns
  WHERE user_id = '3f4593ae-5bc9-468d-b08d-8c4c02a5b963'
  ORDER BY last_used_at DESC;
"
```

### Check Settings in Database
```bash
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "
  SELECT learning_enabled, suggestion_threshold, automation_threshold,
         auto_apply_enabled, notification_enabled, created_at, updated_at
  FROM learning_settings
  WHERE user_id = '3f4593ae-5bc9-468d-b08d-8c4c02a5b963';
"
```

---

## Performance Testing

### Response Times
All endpoints should respond in < 100ms for single pattern operations.

```bash
# Test pattern list performance
time curl -s http://localhost:8001/api/v1/learning/patterns > /dev/null
# Should be < 0.1s

# Test settings performance
time curl -s http://localhost:8001/api/v1/learning/settings > /dev/null
# Should be < 0.1s
```

### Concurrent Updates
```bash
# Test concurrent enable/disable (requires GNU parallel or similar)
# This tests SELECT FOR UPDATE row locking

PATTERN_ID="your-pattern-id"

# Attempt concurrent updates
curl -s -X POST http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID/disable &
curl -s -X POST http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID/enable &
wait

# Check final state - should be consistent
curl -s http://localhost:8001/api/v1/learning/patterns/$PATTERN_ID | python3 -c "import sys, json; print(json.load(sys.stdin)['enabled'])"
```

---

## Test Evidence

**Test Files**:
- `dev/2025/11/13/test_phase2_patterns.py` - Pattern creation script
- `dev/2025/11/13/test_phase2_security.py` - Comprehensive security tests
- `dev/2025/11/13/PHASE2.1-TEST-EVIDENCE.md` - Pattern endpoint test evidence

**Session Logs**:
- `dev/2025/11/13/2025-11-13-0706-prog-code-log.md` - Complete session log

**Test Results**:
- Phase 2.1: 8/8 tests passed (Pattern Management)
- Phase 2.2: 4/4 tests passed (Settings API)
- Phase 2.3: 13/13 tests passed (Security & Error Handling)
- **Total: 21/21 tests passed (100%)**

---

## Troubleshooting

### Server Not Running
```bash
# Check if port 8001 is in use
lsof -i :8001

# Kill process if needed
kill -9 <PID>

# Restart server
uvicorn web.app:app --port 8001 --host 127.0.0.1 --reload
```

### Database Connection Issues
```bash
# Check database is running
docker ps | grep piper-postgres

# Restart database if needed
docker start piper-postgres

# Verify connection
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "SELECT 1;"
```

### No Test Patterns
```bash
# Create test patterns
python3 dev/2025/11/13/test_phase2_patterns.py
```

### Migrations Not Applied
```bash
# Check current migration
alembic current

# Apply migrations
alembic upgrade head

# Verify tables exist
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\dt learned_patterns learning_settings"
```

---

## Next Steps

After completing manual tests:
1. Verify all 21 tests pass
2. Document any issues found
3. Update GitHub issue #300 with test results
4. Prepare for Phase 3 (Pattern Suggestions)

For Phase 5 (Automated Testing):
- Convert manual tests to pytest fixtures
- Add unit tests for each endpoint
- Add integration tests with test database
- Configure CI/CD pipeline

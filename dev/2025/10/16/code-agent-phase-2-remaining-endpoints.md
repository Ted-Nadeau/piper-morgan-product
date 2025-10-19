# Code Agent Prompt: Phase 2 - Update Remaining Endpoints

**Date**: October 16, 2025, 12:43 PM
**Sprint**: A2 - Notion & Errors (Day 2)
**Issue**: CORE-ERROR-STANDARDS #215
**Phase**: Phase 2 - Remaining Endpoints
**Duration**: 1.5-2 hours
**Agent**: Claude Code

---

## Mission

Apply REST-compliant error handling (Pattern 034) to all remaining endpoints. Now that the DDD service layer is solid (Phases 1.5-1.6), we can properly test and validate the error handling changes.

**Context**: Phase 0 created error utilities. Phase 1 fixed intent endpoint. Phases 1.5-1.6 fixed service layer. NOW we can complete the remaining endpoints with confidence!

**Philosophy**: "With solid foundation, build with confidence."

---

## What We've Accomplished

### Phase 0 ✅
- Error audit complete
- Pattern 034 defined
- Error utility module created
- All utilities tested

### Phase 1 ✅
- Intent endpoint updated
- Error utilities validated (returns 422 for invalid)

### Phases 1.5-1.6 ✅
- DDD ServiceContainer implemented
- ServiceRegistry anti-pattern eliminated
- Intent endpoint now functional (returns 200 for valid!)
- Foundation solid

### Phase 2 ← **WE ARE HERE**
- Update remaining endpoints
- Test each one properly
- Validate with working system

---

## Step 1: Review Phase 0 Audit (5 min)

**Find the audit report**:
```bash
# Phase 0 audit should be in dev/2025/10/15/
find dev/2025/10/15/ -name "*audit*" -o -name "*error*" | grep -i audit
```

**What we need from audit**:
- List of all endpoints with errors
- Current error patterns
- Recommended status codes

**Create summary** in `dev/active/phase-2-endpoints-list.md`:

```markdown
# Phase 2 - Endpoints to Update

**Source**: Phase 0 audit from October 15

---

## Endpoints Already Done

1. ✅ POST /api/v1/intent - Phase 1 (returns 422/500)

---

## Endpoints Remaining

### High Priority (Core API)
2. [ ] GET /api/v1/workflows/{workflow_id}
3. [ ] POST /api/v1/workflows
4. [ ] [other workflow endpoints]

### Medium Priority (Personality)
5. [ ] GET /api/personality/profile/{user_id}
6. [ ] PUT /api/personality/profile/{user_id}
7. [ ] POST /api/personality/enhance
8. [ ] [other personality endpoints]

### Lower Priority (Admin/Debug)
9. [ ] [admin endpoints from audit]

---

**Total Remaining**: [count]
```

---

## Step 2: Update Endpoints in Batches (90 min)

### Strategy: Small Batches + Test

**Approach**:
1. Update 2-3 endpoints at a time
2. Start server and test each batch
3. Verify error codes correct
4. Commit batch before moving to next

**This prevents**: Breaking everything at once
**This enables**: Quick rollback if needed

---

### Batch 1: Workflow Endpoints (30 min)

#### Find workflow endpoints in web/app.py

```bash
grep -n "workflow" web/app.py | grep -E "@app\.(get|post|put|delete)"
```

#### Update pattern for each endpoint

**Current pattern**:
```python
@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    try:
        # ... workflow logic ...
        return result
    except Exception as e:
        return {"status": "error", "error": str(e)}  # ❌ Returns 200!
```

**Updated pattern**:
```python
@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    try:
        # Validate workflow_id
        if not workflow_id or not workflow_id.strip():
            return validation_error(
                "Workflow ID required",
                {"field": "workflow_id", "issue": "Cannot be empty"}
            )

        # ... workflow logic ...

        # If workflow not found
        if not workflow:
            return not_found_error(
                "Workflow not found",
                {"resource": "workflow", "id": workflow_id}
            )

        return result

    except ValueError as e:
        # Known validation errors
        return validation_error(str(e))
    except Exception as e:
        # Unexpected errors
        logger.error(f"Error getting workflow {workflow_id}: {e}", exc_info=True)
        return internal_error()
```

**Key changes**:
1. ✅ Empty/invalid input → `validation_error()` (422)
2. ✅ Resource not found → `not_found_error()` (404)
3. ✅ Known errors → `validation_error()` (422)
4. ✅ Unexpected → `internal_error()` with logging (500)

#### Test Batch 1

```bash
# Start server
pkill -f "python main.py" 2>/dev/null || true
python main.py &
sleep 5

# Test workflow endpoint - invalid ID
curl -X GET http://localhost:8001/api/v1/workflows/ \
  -w "\nHTTP: %{http_code}\n"
# Expected: 404 or 422

# Test workflow endpoint - valid ID (if you have one)
curl -X GET http://localhost:8001/api/v1/workflows/test-123 \
  -w "\nHTTP: %{http_code}\n"
# Expected: 200 (if exists) or 404 (if not)

# Document results
echo "Batch 1 results..." >> dev/active/phase-2-test-results.md
```

#### Commit Batch 1

```bash
./scripts/commit.sh "feat(#215): Phase 2 Batch 1 - workflow endpoints REST-compliant

Updated endpoints:
- GET /api/v1/workflows/{workflow_id}
- POST /api/v1/workflows
- [others]

Changes:
- Empty/invalid input → 422 validation error
- Not found → 404 not found error
- Unexpected → 500 internal error with logging

Testing:
- Manual curl tests performed
- Error codes validated

Part of: #215 Phase 2, Sprint A2"
```

---

### Batch 2: Personality Endpoints (30 min)

#### Find personality endpoints

```bash
grep -n "personality" web/app.py | grep -E "@app\.(get|post|put|delete)"
```

#### Apply same pattern

**For each personality endpoint**:
1. Add validation for required fields → `validation_error()` (422)
2. Handle not found cases → `not_found_error()` (404)
3. Catch validation errors → `validation_error()` (422)
4. Catch unexpected → `internal_error()` with logging (500)

#### Test Batch 2

```bash
# Test personality endpoints
curl -X GET http://localhost:8001/api/personality/profile/ \
  -w "\nHTTP: %{http_code}\n"

# Test with valid user_id (if you have one)
curl -X GET http://localhost:8001/api/personality/profile/test-user \
  -w "\nHTTP: %{http_code}\n"

# Document results
echo "Batch 2 results..." >> dev/active/phase-2-test-results.md
```

#### Commit Batch 2

```bash
./scripts/commit.sh "feat(#215): Phase 2 Batch 2 - personality endpoints REST-compliant

Updated endpoints:
- GET /api/personality/profile/{user_id}
- PUT /api/personality/profile/{user_id}
- POST /api/personality/enhance
- [others]

Testing: Manual validation complete

Part of: #215 Phase 2, Sprint A2"
```

---

### Batch 3: Admin/Debug Endpoints (30 min)

#### Find admin endpoints

```bash
grep -n "admin\|debug\|health" web/app.py | grep -E "@app\.(get|post|put|delete)"
```

#### Apply same pattern

**Note**: Admin endpoints may be simpler (fewer validation needs)

**Common pattern**:
```python
@app.get("/api/admin/stats")
async def get_stats():
    try:
        # ... get stats ...
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}", exc_info=True)
        return internal_error()
```

#### Test Batch 3

```bash
# Test admin endpoints
curl -X GET http://localhost:8001/api/admin/stats \
  -w "\nHTTP: %{http_code}\n"

# Test health (should stay simple)
curl -X GET http://localhost:8001/health \
  -w "\nHTTP: %{http_code}\n"
# Expected: 200 (always)

# Document results
echo "Batch 3 results..." >> dev/active/phase-2-test-results.md
```

#### Commit Batch 3

```bash
./scripts/commit.sh "feat(#215): Phase 2 Batch 3 - admin/debug endpoints REST-compliant

Updated endpoints:
- [list admin endpoints]

Testing: Manual validation complete

Part of: #215 Phase 2, Sprint A2"
```

---

## Step 3: Comprehensive Testing (15 min)

### Test ALL endpoints systematically

**Create test script** (if helpful):

**File**: `scripts/test-all-endpoints.sh`

```bash
#!/bin/bash
# Test all endpoints for proper error codes

BASE_URL="http://localhost:8001"

echo "Testing all endpoints..."
echo ""

# Intent endpoint
echo "1. POST /api/v1/intent (empty)"
curl -s -X POST $BASE_URL/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": ""}' \
  -w "\nHTTP: %{http_code}\n" | tail -1
# Expected: 422

echo ""
echo "2. POST /api/v1/intent (valid)"
curl -s -X POST $BASE_URL/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "show me the standup"}' \
  -w "\nHTTP: %{http_code}\n" | tail -1
# Expected: 200

echo ""
echo "3. GET /api/v1/workflows/{invalid}"
curl -s -X GET $BASE_URL/api/v1/workflows/invalid-id \
  -w "\nHTTP: %{http_code}\n" | tail -1
# Expected: 404

# Add more endpoints...

echo ""
echo "Testing complete!"
```

**Run comprehensive tests**:
```bash
chmod +x scripts/test-all-endpoints.sh
./scripts/test-all-endpoints.sh | tee dev/active/comprehensive-test-results.txt
```

---

## Step 4: Document Results (10 min)

### Create final validation report

**File**: `dev/active/phase-2-validation-report.md`

```markdown
# Phase 2 Validation Report

**Date**: October 16, 2025
**Time**: [completion time]
**Duration**: [actual time]

---

## Summary

**Endpoints Updated**: [count]
**Batches Completed**: 3
**Test Results**: [summary]

---

## Endpoints by Status Code

### 200 OK (Success)
- POST /api/v1/intent (valid request)
- GET /api/v1/workflows/{id} (when exists)
- [others]

### 422 Validation Error
- POST /api/v1/intent (empty intent)
- GET /api/v1/workflows/ (missing ID)
- [others]

### 404 Not Found
- GET /api/v1/workflows/{invalid-id}
- GET /api/personality/profile/{invalid-user}
- [others]

### 500 Internal Error
- Any unexpected server errors (logged)

---

## Pattern Compliance

**Before Phase 2**: All errors returned 200 ❌
**After Phase 2**: Proper HTTP status codes ✅

**Pattern 034 Adherence**: ✅ 100%

---

## Test Results

**Manual Tests**: [X] endpoints tested
**Passing**: [X] / [X]
**Issues Found**: [count]

### Test Details

[Paste comprehensive test results]

---

## Commits

1. Batch 1: Workflow endpoints - [commit hash]
2. Batch 2: Personality endpoints - [commit hash]
3. Batch 3: Admin endpoints - [commit hash]

---

## Ready for Phase 3

**Status**: ✅ YES / ❌ NO
**Blockers**: [if any]

---

**Phase 2 Complete**: [time]
```

---

## Step 5: Final Commit (5 min)

### Summary commit (if needed)

```bash
./scripts/commit.sh "feat(#215): Phase 2 complete - all endpoints REST-compliant

Summary:
- Updated [X] endpoints total
- Applied Pattern 034 consistently
- Validation errors → 422
- Not found → 404
- Internal errors → 500

Testing:
- All endpoints manually validated
- Comprehensive test results documented

Batches:
1. Workflow endpoints
2. Personality endpoints
3. Admin/debug endpoints

Part of: #215 Error Standardization, Sprint A2
Duration: [actual time]"
```

---

## Deliverables Phase 2

When complete, you should have:

- [ ] Phase 0 audit reviewed
- [ ] Endpoints list created
- [ ] Batch 1 (workflows) updated & committed
- [ ] Batch 2 (personality) updated & committed
- [ ] Batch 3 (admin) updated & committed
- [ ] Comprehensive testing complete
- [ ] All endpoints returning proper status codes
- [ ] Validation report documented
- [ ] Changes committed

---

## Success Criteria

**Phase 2 is complete when**:

- ✅ All endpoints follow Pattern 034
- ✅ Validation errors return 422
- ✅ Not found returns 404
- ✅ Internal errors return 500
- ✅ Valid requests return 200
- ✅ All endpoints tested manually
- ✅ Results documented
- ✅ Changes committed

---

## Time Budget

**Target**: 1.5-2 hours

- Review audit: 5 min
- Batch 1 (workflows): 30 min
- Batch 2 (personality): 30 min
- Batch 3 (admin): 30 min
- Comprehensive testing: 15 min
- Documentation: 10 min
- Final commit: 5 min

**Total**: ~2 hours

---

## What NOT to Do

- ❌ Don't update all at once (batch approach is safer)
- ❌ Don't skip testing between batches
- ❌ Don't forget to commit each batch
- ❌ Don't break existing functionality

## What TO Do

- ✅ Work in small batches
- ✅ Test after each batch
- ✅ Commit frequently
- ✅ Document results
- ✅ Verify proper status codes

---

## STOP Conditions

Stop and escalate if:

- Endpoints breaking unexpectedly
- Can't determine proper status codes
- Tests failing across the board
- Working functionality regressing

---

**Phase 2 Start**: 12:45 PM
**Expected Done**: ~2:45 PM (2 hours)
**Status**: Ready to complete error standardization!

**LET'S FINISH THE ENDPOINTS!** 🎯

---

*"Small batches, frequent commits, continuous validation."*
*- Phase 2 Philosophy*

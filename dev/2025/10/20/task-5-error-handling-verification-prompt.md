# Task 5: Error Handling Verification - Standup API

**Agent**: Claude Code (Programmer)
**Issue**: #162 (CORE-STAND-MODES-API)
**Task**: 5 of 7 - Error Handling Verification
**Sprint**: A4 "Standup Epic"
**Date**: October 19, 2025, 5:20 PM
**Estimated Effort**: Small (30-45 minutes)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

**This is critical**. After compaction, get your bearings first.

---

## Mission

Verify that all standup API endpoints have comprehensive error handling following Pattern-034 (Error Handling Standards), test all error scenarios, and ensure consistent, user-friendly error responses with proper HTTP status codes.

**Scope**:
- Verify Pattern-034 compliance
- Test all error scenarios per endpoint
- Verify HTTP status codes correct
- Verify error response format consistent
- Test error messages user-friendly
- Verify logging integrated

**NOT in scope**:
- Changing error handling architecture
- Creating new error patterns
- Comprehensive testing (Task 6)
- Integration testing (Task 7)

---

## Context

- **GitHub Issue**: #162 (CORE-STAND-MODES-API) - Multi-modal API
- **Current State**:
  - ✅ REST API endpoints created (Task 1)
  - ✅ Service integration complete (Task 2)
  - ✅ Authentication working (Task 3)
  - ✅ OpenAPI docs verified (Task 4)
  - ✅ Error handling utilities exist (web/utils/error_responses.py)
  - ❓ Error scenarios need testing
- **Target State**:
  - All error scenarios tested
  - Pattern-034 compliance verified
  - Consistent error responses
  - User-friendly error messages
- **Dependencies**:
  - Pattern-034: Error Handling Standards
  - web/utils/error_responses.py utilities
  - FastAPI HTTPException handling
- **User Data Risk**: None - testing only
- **Infrastructure Verified**: Yes - error utilities exist

---

## STOP Conditions (EXPANDED TO 17)

If ANY of these occur, STOP and escalate to PM immediately:

1. **Infrastructure doesn't match gameplan** - Error utilities not where expected
2. **Method implementation <100% complete** - All error scenarios must be tested
3. **Pattern already exists in catalog** - Using Pattern-034
4. **Tests fail for any reason** - Error handling must work correctly
5. **Configuration assumptions needed** - Don't guess error behavior
6. **GitHub issue missing or unassigned** - Verify #162 still assigned
7. **Can't provide verification evidence** - Must show errors working
8. **ADR conflicts with approach** - Check for error handling ADRs
9. **Resource not found after searching** - Pattern-034 must exist
10. **User data at risk** - N/A for error testing
11. **Completion bias detected** - Must test ALL error scenarios
12. **Rationalizing gaps as "minor"** - All error paths critical
13. **GitHub tracking not working** - Issue updates must work
14. **Single agent seems sufficient** - This IS single agent task
15. **Git operations failing** - Commits needed only if gaps found
16. **Server state unexpected** - Verify error responses
17. **UI behavior can't be visually confirmed** - Use curl to test errors

**Remember**: STOP means STOP. Don't try to work around it. Ask PM.

---

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:

- **"Error handling follows Pattern-034"** → Show pattern compliance
- **"Error scenario X works"** → Show curl output with error response
- **"Status code correct"** → Show HTTP status in response
- **"Error message user-friendly"** → Show actual message text
- **"All scenarios tested"** → Show test output for each scenario
- **"Logging works"** → Show log entries for errors

### Completion Bias Prevention (CRITICAL):

- **Never guess! Always verify first!**
- **NO "should handle errors"** - only "here's proof it handles errors"
- **NO "probably works"** - only "here's evidence it works"
- **NO assumptions** - only verified facts with curl outputs
- **NO rushing to claim done** - test ALL error scenarios

### Working Files Location:

**NEVER use /tmp for important files**:
- ❌ /tmp - Can be lost between sessions
- ✅ dev/active/ - For working files, evidence, analysis
- ✅ outputs/ - For final deliverables

**Save test results to**: dev/active/error-handling-test-results.txt

---

## Related Documentation

- **resource-map.md** - ALWAYS CHECK FIRST for pattern locations
- **stop-conditions.md** - When to stop and ask for help
- **anti-80-pattern.md** - Understanding completion bias prevention
- **Pattern-034** - Error Handling Standards (FOLLOW THIS)
- **web/utils/error_responses.py** - Error utilities

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:

1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. **Checking what exists NEXT** (Pattern-034 already implemented)
4. **Preserving user data ALWAYS** (N/A for error testing)
5. **Checking resource-map.md FIRST** (for pattern locations)
6. **Following ALL verification requirements**
7. **Providing evidence for EVERY claim**
8. **Creating error scenario enumeration** (test all paths)
9. **Stopping when assumptions are needed**
10. **Maintaining architectural integrity**
11. **Updating GitHub with progress** (in descriptions!)
12. **Creating session logs in .md format**
13. **Verifying git commits with log output** (if changes made)
14. **Checking actual error responses**
15. **Providing curl output evidence**
16. **Never guessing - always verifying first!**
17. **Never rationalizing incompleteness!**

**Poor error handling = poor user experience. Evidence is mandatory.**

---

## Task Requirements

### 1. Review Pattern-034 (Error Handling Standards)

**Locate and review the pattern**:

```bash
# Find Pattern-034
find docs/internal/architecture/current/patterns -name "*034*" -o -name "*error*" | grep -i pattern

# Or check pattern catalog
grep -i "error" docs/internal/architecture/current/patterns/README.md

# Review the pattern
cat [pattern-file-path]
```

**Document Pattern-034 requirements**:
- Required HTTP status codes
- Error response format
- Required fields
- User-friendly message guidelines
- Logging requirements

**If not found**: STOP (condition #9)

---

### 2. Review Error Handling Implementation

**Check existing utilities**:

```bash
# Review error response utilities
cat web/utils/error_responses.py

# Check how endpoints use them
grep -A 5 "HTTPException\|error_response" web/api/routes/standup.py
```

**Document**:
- What utilities exist
- How they're used
- What HTTP status codes are used
- Error response format
- Whether Pattern-034 compliant

---

### 3. Identify All Error Scenarios

**For /api/v1/standup/generate endpoint**:

| Error Scenario | Expected Status | Expected Message Pattern |
|----------------|-----------------|--------------------------|
| No authentication | 401 | "Authentication required" |
| Invalid token | 401 | "Invalid or expired token" |
| Invalid mode | 422 | "Invalid mode: X" |
| Invalid format | 422 | "Invalid format: X" |
| Missing required field | 422 | Pydantic validation error |
| Service unavailable | 503 | User-friendly message |
| Unexpected error | 500 | Generic error message |
| User not found | 404 | "User not found" (if applicable) |

**For other endpoints**:
- /health - Should not error (always 200)
- /modes - Should not error (always 200)
- /formats - Should not error (always 200)

**Total error scenarios**: ~7-8 for /generate endpoint

---

### 4. Test Each Error Scenario

**Test systematically**:

```bash
# Save results for evidence
touch dev/active/error-handling-test-results.txt

# 1. No authentication
echo "=== Test 1: No Authentication ===" >> dev/active/error-handling-test-results.txt
curl -v -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode":"standard"}' 2>&1 | tee -a dev/active/error-handling-test-results.txt

# 2. Invalid token
echo "=== Test 2: Invalid Token ===" >> dev/active/error-handling-test-results.txt
curl -v -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token_123" \
  -d '{"mode":"standard"}' 2>&1 | tee -a dev/active/error-handling-test-results.txt

# 3. Invalid mode
echo "=== Test 3: Invalid Mode ===" >> dev/active/error-handling-test-results.txt
TOKEN=$(python scripts/generate_test_token.py)
curl -v -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mode":"invalid_mode"}' 2>&1 | tee -a dev/active/error-handling-test-results.txt

# 4. Invalid format
echo "=== Test 4: Invalid Format ===" >> dev/active/error-handling-test-results.txt
curl -v -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mode":"standard","format":"invalid"}' 2>&1 | tee -a dev/active/error-handling-test-results.txt

# 5. Missing Content-Type
echo "=== Test 5: Missing Content-Type ===" >> dev/active/error-handling-test-results.txt
curl -v -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mode":"standard"}' 2>&1 | tee -a dev/active/error-handling-test-results.txt

# 6. Malformed JSON
echo "=== Test 6: Malformed JSON ===" >> dev/active/error-handling-test-results.txt
curl -v -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{invalid json}' 2>&1 | tee -a dev/active/error-handling-test-results.txt

# 7. Empty request body
echo "=== Test 7: Empty Request Body ===" >> dev/active/error-handling-test-results.txt
curl -v -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{}' 2>&1 | tee -a dev/active/error-handling-test-results.txt
```

**Evidence**: Show complete test results file

---

### 5. Verify Error Response Format

**Check each error response follows pattern**:

```json
// Expected error response format (Pattern-034)
{
  "detail": "User-friendly error message",
  "error_code": "ERROR_TYPE", // Optional
  "field_errors": [...],  // For 422 validation errors
  "timestamp": "2025-10-19T17:30:00Z"  // Optional
}
```

**Verify**:
- Consistent format across all errors
- User-friendly messages (no stack traces)
- Appropriate detail level
- Field errors for validation issues

---

### 6. Verify HTTP Status Codes

**Create verification table**:

| Error Scenario | Expected | Actual | Match? |
|----------------|----------|--------|--------|
| No auth | 401 | 401 | ✅ |
| Invalid token | 401 | 401 | ✅ |
| Invalid mode | 422 | ??? | ☐ |
| Invalid format | 422 | ??? | ☐ |
| Malformed JSON | 422 | ??? | ☐ |
| Service error | 500 | ??? | ☐ |

**Target**: All match expectations ✅

---

### 7. Verify User-Friendly Messages

**Check messages are helpful**:

✅ **Good**: "Invalid mode 'xyz'. Valid modes: standard, issues, documents, calendar, trifecta"

❌ **Bad**: "ValueError: mode not in enum"

✅ **Good**: "Authentication required. Please provide a valid JWT token."

❌ **Bad**: "401 Unauthorized"

**Review each error message** for:
- Clear explanation of what went wrong
- Guidance on how to fix (when appropriate)
- No technical jargon or stack traces
- Professional tone

---

### 8. Check Logging Integration

**Verify errors are logged**:

```bash
# Start server with visible logs
uvicorn main:app --reload --port 8001 --log-level debug

# Trigger an error
curl -X POST http://localhost:8001/api/v1/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode":"invalid"}'

# Check server logs show the error
# Should see log entry with:
# - Timestamp
# - Error level (ERROR or WARNING)
# - Error message
# - Request context
```

**Verify**:
- Errors logged at appropriate level
- Includes context (endpoint, user, etc.)
- No sensitive data in logs (no tokens!)

---

## Verification Steps

### Step 1: Start API Server

```bash
# Start with logging visible
uvicorn main:app --reload --port 8001 --log-level info

# Keep this running for all tests
```

---

### Step 2: Run All Error Scenario Tests

```bash
# Run systematic test suite (from step 4)
# This will create dev/active/error-handling-test-results.txt

# Review results
cat dev/active/error-handling-test-results.txt

# Count successes
grep "< HTTP" dev/active/error-handling-test-results.txt | sort | uniq -c
```

**Expected**: All error responses working correctly

---

### Step 3: Analyze Error Response Format

```bash
# Extract just the JSON responses
grep "^{" dev/active/error-handling-test-results.txt | jq '.'

# Verify format consistency
# All should have "detail" field
# Validation errors should have "field_errors" or similar
```

**Expected**: Consistent format following Pattern-034

---

### Step 4: Verify Status Codes

```bash
# Extract HTTP status codes
grep "< HTTP/1.1" dev/active/error-handling-test-results.txt

# Should see:
# - HTTP/1.1 401 for auth errors
# - HTTP/1.1 422 for validation errors
# - HTTP/1.1 500 for server errors (if any)
```

**Expected**: Correct status codes for each scenario

---

### Step 5: Review Server Logs

Check server terminal for:
- Error log entries
- Appropriate log levels
- Context information
- No sensitive data exposed

**Evidence**: Sample log entries showing error logging

---

## Success Criteria

Task 5 is complete when:

- [ ] Pattern-034 located and reviewed
- [ ] Error handling implementation reviewed
- [ ] All error scenarios identified (~7-8 scenarios)
- [ ] All error scenarios tested (evidence in file)
- [ ] Error response format verified (Pattern-034 compliant)
- [ ] HTTP status codes correct for all scenarios
- [ ] Error messages user-friendly (no technical jargon)
- [ ] Logging integration verified
- [ ] Test results saved to dev/active/ (not /tmp!)
- [ ] Error scenario enumeration complete (X/X = 100%)
- [ ] Any gaps identified and documented
- [ ] Code changes committed if gaps fixed
- [ ] Session log updated in .md format
- [ ] No error handling shortcuts
- [ ] All error paths tested

---

## Self-Check Before Claiming Complete

### Ask Yourself:

1. **Did I actually test all error scenarios?** (Not just assume they work)
2. **Do I have curl output for each scenario?** (Actual evidence)
3. **Are status codes correct for all errors?** (401, 422, 500, etc.)
4. **Are error messages user-friendly?** (Reviewed each one)
5. **Did I check error response format?** (Pattern-034 compliance)
6. **Did I verify logging works?** (Checked server logs)
7. **Did I save results to dev/active/?** (Not /tmp!)
8. **Is there a gap between claims and reality?** (Evidence matches)
9. **Am I rationalizing any missing tests?** (No "probably works")
10. **Did I test negative cases?** (Not just happy paths)
11. **Are error messages helpful?** (Not just technically correct)
12. **Did I document all scenarios?** (Complete enumeration)
13. **Am I guessing or do I have evidence?** (Evidence for everything)

### If Uncertain About Anything:

- Run the tests yourself
- Show actual curl outputs
- Review server logs
- Check against Pattern-034
- Ask for help if stuck
- **Never assume error handling works - test it!**

---

## Files to Review

### Primary Files

- `docs/internal/architecture/current/patterns/pattern-034*` - Error handling pattern
- `web/utils/error_responses.py` - Error utilities
- `web/api/routes/standup.py` - Endpoint error handling

### Evidence Files

- `dev/active/error-handling-test-results.txt` - Test outputs (created by you)

### Session Log

- `dev/2025/10/19/HHMM-prog-code-log.md` - Your session log

---

## Deliverables

### 1. Pattern-034 Compliance Report

**Pattern requirements**:
- Required status codes: [list]
- Error format: [describe]
- Message guidelines: [describe]

**Implementation review**:
- ✅ Follows pattern requirements
- ❌ Gap identified: [describe]

### 2. Error Scenario Enumeration

**Table**:

| Scenario | Status | Message | Format OK | Logged | Tested | Status |
|----------|--------|---------|-----------|--------|--------|--------|
| No auth | 401 | "Authentication required" | ✅ | ✅ | ✅ | ✅ |
| Invalid token | 401 | "Invalid or expired token" | ✅ | ✅ | ✅ | ✅ |
| Invalid mode | 422 | Clear enum error | ✅ | ✅ | ✅ | ✅ |
| Invalid format | 422 | Clear enum error | ✅ | ✅ | ✅ | ✅ |
| Malformed JSON | 422 | Validation error | ✅ | ✅ | ✅ | ✅ |
| Empty body | 422 | Uses defaults | ✅ | ✅ | ✅ | ✅ |
| Service error | 500 | Generic message | ✅ | ✅ | ☐ | ☐ |

**Target**: X/X = 100% ✅

### 3. Test Results File

**Location**: dev/active/error-handling-test-results.txt

**Contents**:
- All curl commands
- All HTTP responses
- All status codes
- All error messages

**Evidence**: Show file exists and is complete

### 4. Gap Analysis

**Any issues found**:
- Gap 1: [description] → [fix applied]
- Gap 2: [description] → [fix applied]

**If no gaps**: "No issues found - error handling complete"

### 5. Session Log

**In dev/2025/10/19/HHMM-prog-code-log.md**:
- Pattern-034 review
- Error scenario identification
- Test results summary
- Status code verification
- Message quality assessment
- Logging verification
- Any gaps found/fixed
- Time spent

---

## Remember

- **Test ALL error scenarios** - Not just some
- **User-friendly messages matter** - Users read these
- **Consistent format is key** - Pattern-034 compliance
- **Logging helps debugging** - Verify it works
- **Save to dev/active/** - Not /tmp!
- **100% means 100%** - All error paths tested

**Good error handling = professional API!** 🛡️

---

*Template Version: 8.0*
*Based on: agent-prompt-template.md*
*All methodology sections included*
*Post-compaction protocol added*
*Working files location guidance added*
*Task-specific sections customized*
*Ready for deployment*

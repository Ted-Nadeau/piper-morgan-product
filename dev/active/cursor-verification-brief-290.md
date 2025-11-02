# Cursor Verification Brief: Issue #290 Document Processing Integration

**Date**: November 1, 2025, 3:45 PM PT
**Role**: Test Engineer / Cross-Validator
**Task**: Verify document processing integration (Tests 19-24)
**Issue**: #290 - CORE-ALPHA-DOC-PROCESSING

---

## Mission

Verify that Code Agent successfully **wired existing document services** into the web/chat interface. This is integration work, not new feature development.

**Key Distinction**: 75% of services already exist (DocumentService, DocumentAnalyzer, ChromaDB). Code is wiring them, not building them.

---

## What to Verify

### 1. Integration Quality (Primary Focus)

**Verify Code REUSED existing services** (not rebuilt):

```bash
# Should call existing DocumentService methods
grep -n "DocumentService" services/intent_service/document_handlers.py
# Expected: Multiple references to upload_pdf, find_decisions, etc.

# Should call existing DocumentAnalyzer
grep -n "DocumentAnalyzer" services/intent_service/document_handlers.py
# Expected: analyze() method called

# Should use existing ChromaDB
grep -n "chromadb" services/intent_service/document_handlers.py
# Expected: No new ChromaDB initialization (uses existing)
```

**Red Flag**: If Code created new DocumentService, DocumentAnalyzer, or ChromaDB integration → **WRONG APPROACH**

---

### 2. Test Coverage (All 6 Must Pass)

**Verify Tests 19-24** implemented and passing:

```bash
pytest tests/integration/test_document_processing.py -v
```

**Expected Output**:
```
test_19_analyze_uploaded_document ✅ PASSED
test_20_question_document ✅ PASSED
test_21_reference_in_conversation ✅ PASSED
test_22_summarize_document ✅ PASSED
test_23_compare_documents ✅ PASSED
test_24_search_documents ✅ PASSED

6 passed in XX seconds
```

**Failure Cases to Check**:
- ❌ 5/6 tests passing → NOT COMPLETE
- ❌ Tests skipped → NOT COMPLETE
- ❌ "Works but Test X has issue" → NOT COMPLETE

---

### 3. Security Verification

**JWT Authentication** (from #281 integration):

```bash
# All endpoints should require auth
grep -n "Depends(get_current_user)" web/api/routes/files.py
# OR
grep -n "Depends(get_current_user)" web/api/routes/documents.py

# Expected: ALL document endpoints protected
```

**User Isolation**:
```bash
# Should use current_user.user_id for isolation
grep -n "current_user\[\"user_id\"\]" services/intent_service/document_handlers.py
# OR
grep -n "current_user.user_id" services/intent_service/document_handlers.py

# Expected: Document operations scoped to user
```

**Test Security**:
```python
# Try to access another user's document
# Expected: 403 Forbidden or 404 Not Found
```

---

### 4. API Endpoint Verification

**Check all 5 endpoints exist**:

```bash
# Start server
python main.py

# Check OpenAPI spec
curl http://localhost:8001/docs
# Look for:
# POST /api/v1/documents/{file_id}/analyze
# POST /api/v1/documents/{file_id}/question
# POST /api/v1/documents/compare
# GET  /api/v1/documents/search
# POST /api/v1/documents/{file_id}/summarize
```

**Manual Testing**:
```bash
# 1. Login and get token
TOKEN=$(curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xian", "password": "test123456"}' \
  | jq -r '.token')

# 2. Upload document
FILE_ID=$(curl -X POST http://localhost:8001/api/v1/files/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf" | jq -r '.file_id')

# 3. Test analyze endpoint
curl -X POST http://localhost:8001/api/v1/documents/$FILE_ID/analyze \
  -H "Authorization: Bearer $TOKEN"
# Expected: JSON with summary, key_findings

# 4. Test question endpoint
curl -X POST "http://localhost:8001/api/v1/documents/$FILE_ID/question" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
# Expected: JSON with answer

# 5. Test search endpoint
curl -X GET "http://localhost:8001/api/v1/documents/search?q=testing" \
  -H "Authorization: Bearer $TOKEN"
# Expected: JSON with search results
```

---

### 5. ChromaDB Integration

**Verify ChromaDB used correctly**:

```bash
# Check ChromaDB data directory exists
ls -la data/chromadb/
# Expected: ChromaDB files present

# Verify embeddings configured
grep -n "OpenAIEmbeddingFunction" services/knowledge_graph/ingestion.py
# Expected: OpenAI embeddings configured

# Check search uses ChromaDB
grep -n "find_decisions" services/intent_service/document_handlers.py
# Expected: Calls DocumentService.find_decisions (which uses ChromaDB)
```

---

### 6. Performance Check

**Document operations should be reasonably fast**:

```bash
# Time analysis operation
time curl -X POST http://localhost:8001/api/v1/documents/$FILE_ID/analyze \
  -H "Authorization: Bearer $TOKEN"
# Expected: < 10 seconds for typical document

# Time search operation
time curl -X GET "http://localhost:8001/api/v1/documents/search?q=test" \
  -H "Authorization: Bearer $TOKEN"
# Expected: < 5 seconds
```

**If slow**: Check for:
- N+1 query problems
- Missing ChromaDB indexes
- Inefficient document retrieval

---

### 7. Error Handling

**Test error scenarios**:

```bash
# 1. Document doesn't exist
curl -X POST http://localhost:8001/api/v1/documents/fake-id/analyze \
  -H "Authorization: Bearer $TOKEN"
# Expected: 404 with clear error message

# 2. No auth token
curl -X POST http://localhost:8001/api/v1/documents/$FILE_ID/analyze
# Expected: 401 Unauthorized

# 3. Invalid question format
curl -X POST http://localhost:8001/api/v1/documents/$FILE_ID/question \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"invalid": "format"}'
# Expected: 422 Validation Error

# 4. Empty search query
curl -X GET "http://localhost:8001/api/v1/documents/search?q=" \
  -H "Authorization: Bearer $TOKEN"
# Expected: 400 Bad Request or empty results (not crash)
```

---

## Verification Checklist

### ✅ Integration Quality
- [ ] DocumentService methods reused (not reimplemented)
- [ ] DocumentAnalyzer called correctly
- [ ] ChromaDB integration uses existing config
- [ ] No duplicate service implementations
- [ ] Intent handlers properly wired

### ✅ Test Coverage
- [ ] Test 19: Analyze document passing
- [ ] Test 20: Question document passing
- [ ] Test 21: Reference in conversation passing
- [ ] Test 22: Summarize document passing
- [ ] Test 23: Compare documents passing
- [ ] Test 24: Search documents passing
- [ ] ALL 6/6 tests passing (not 5/6 or "has issue")

### ✅ Security
- [ ] All endpoints require JWT auth
- [ ] User isolation enforced (can't access others' docs)
- [ ] Auth errors return 401 (not crash)
- [ ] Permission errors return 403 (not crash)

### ✅ API Quality
- [ ] All 5 endpoints exist in OpenAPI spec
- [ ] Endpoints return valid JSON
- [ ] Error responses are clear and helpful
- [ ] HTTP status codes correct

### ✅ Performance
- [ ] Analysis completes in reasonable time (<10s)
- [ ] Search completes quickly (<5s)
- [ ] No obvious performance issues
- [ ] Large documents handled (10+ pages)

### ✅ Error Handling
- [ ] Missing document returns 404
- [ ] Missing auth returns 401
- [ ] Invalid input returns 422
- [ ] Error messages are clear

---

## Red Flags to Watch For

### 🚩 Integration Issues
- Code rebuilt DocumentService instead of reusing
- Code created new ChromaDB client instead of using existing
- Code reimplemented PDF extraction
- Duplicate service implementations

### 🚩 Test Issues
- Only 5/6 tests passing ("one has issue")
- Tests skipped
- "Works but needs fixing"
- Mocked services instead of real integration

### 🚩 Security Issues
- Endpoints missing auth
- User isolation not enforced
- Can access other users' documents
- Passwords or tokens in logs

### 🚩 Quality Issues
- Poor error messages
- Slow operations (>30s)
- Crashes on invalid input
- Missing acceptance criteria

---

## Comparison with #281

**Similar to #281**:
- Integration work (wiring services)
- JWT auth required
- User isolation critical
- Tests must ALL pass

**Different from #281**:
- **#281**: Built new services (PasswordService, JWT)
- **#290**: Wire existing services (DocumentService already works)
- Focus on **integration quality** not **new implementation**

---

## Expected Architecture

**Correct Flow**:
```
User Chat Message
    ↓
Intent Classifier (recognizes "analyze")
    ↓
Document Handler (new)
    ↓
DocumentService (existing)
    ↓
DocumentAnalyzer (existing)
    ↓
ChromaDB (existing)
    ↓
Return result
```

**Wrong Flow** (red flag):
```
User Chat Message
    ↓
Document Handler (new)
    ↓
NEW DocumentAnalyzer (wrong!)
    ↓
NEW ChromaDB client (wrong!)
```

---

## Evidence Required from Code

**Code should provide**:
1. All 6 tests passing (full pytest output)
2. Manual verification (curl commands + responses)
3. Git diff showing integration (not new services)
4. Proof existing services reused (grep output)

**You should verify**:
1. Tests actually pass when you run them
2. Manual tests work when you try them
3. Integration is clean (no duplication)
4. Security works (auth, user isolation)

---

## Success Criteria

**PASS** if:
- ✅ ALL 6 tests passing
- ✅ Existing services reused
- ✅ Auth integration working
- ✅ User isolation enforced
- ✅ No red flags

**FAIL** if:
- ❌ Any test failing or skipped
- ❌ Services rebuilt instead of reused
- ❌ Security issues found
- ❌ Performance problems
- ❌ Missing acceptance criteria

---

## Verification Report Format

**Provide concise report**:

```markdown
# Issue #290 Cross-Validation Report

**Status**: ✅ PASS / ❌ FAIL

## Test Results
- Test 19: ✅ PASSED
- Test 20: ✅ PASSED
- Test 21: ✅ PASSED
- Test 22: ✅ PASSED
- Test 23: ✅ PASSED
- Test 24: ✅ PASSED

## Integration Quality
- ✅ Existing services reused (not rebuilt)
- ✅ DocumentService calls verified
- ✅ DocumentAnalyzer integration correct
- ✅ ChromaDB existing config used

## Security
- ✅ JWT auth on all endpoints
- ✅ User isolation enforced
- ✅ Auth errors handled correctly

## Issues Found
- [None] or [List issues]

## Verdict
✅ READY FOR ALPHA / ❌ NEEDS FIXES
```

---

## Questions for PM (if issues found)

**If integration unclear**:
- Should services be rebuilt or reused?
- Any missing infrastructure?

**If tests failing**:
- Are acceptance criteria correct?
- Any infrastructure issues?

**If security concerns**:
- User isolation pattern correct?
- Auth requirements met?

---

**Primary Focus**: Verify Code wired existing services correctly, not rebuilt them.

**Secondary Focus**: All 6 tests passing, security working.

**Success Definition**: Integration complete, clean, and tested.

---

Good luck! This is about verifying clean integration of proven services, not validating new implementations. 🏰

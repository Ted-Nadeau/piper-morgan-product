# Claude Code Prompt: CORE-ALPHA-DOC-PROCESSING (#290)

**Date**: November 1, 2025, 3:40 PM PT
**Mission**: Wire document processing services into chat/web interface
**Issue**: #290 - Implement Document Analysis Workflows (Tests 19-24)
**GitHub**: https://github.com/mediajunkie/piper-morgan-product/issues/290

---

## Your Identity

You are Claude Code, implementing document analysis workflows by wiring existing services into the chat/web interface. You follow systematic methodology and provide evidence at each checkpoint.

---

## Essential Context

**Read Issue #290** on GitHub for complete requirements: Tests 19-24 from manual testing checklist.

**Key Finding** (Archaeological Investigation):
- 75% of document processing **already exists and works via CLI**
- DocumentService, DocumentAnalyzer, ChromaDB all functional
- We just need to wire them into chat/web interface

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Before Writing ANY Code

**Verify the 75% claim** by checking that services exist:

```bash
# 1. Verify DocumentService exists
ls -la services/knowledge_graph/document_service.py
grep -n "class DocumentService" services/knowledge_graph/document_service.py

# 2. Verify DocumentAnalyzer exists
ls -la services/analysis/document_analyzer.py
grep -n "class DocumentAnalyzer" services/analysis/document_analyzer.py

# 3. Verify ChromaDB configured
ls -la data/chromadb/
grep -n "chromadb" services/knowledge_graph/ingestion.py

# 4. Verify CLI commands work
ls -la cli/commands/documents.py
python -m cli documents --help

# 5. Check what intent patterns already exist
grep -n "search_documents" services/intent_service/classifier.py
```

**Report findings** with evidence before proceeding.

**If ANY service missing or different than described**: STOP and report mismatch.

---

## 🎯 ANTI-80% COMPLETION SAFEGUARDS

### MANDATORY: Test Enumeration FIRST

Before implementing, create comparison table:

```
Test Number | Requirement | Implemented | Status
----------- | ----------- | ----------- | ------
Test 19     | Analyze doc | ❌          | MISSING
Test 20     | Question    | ❌          | MISSING
Test 21     | Reference   | ❌          | MISSING
Test 22     | Summarize   | ❌          | MISSING
Test 23     | Compare     | ❌          | MISSING
Test 24     | Search      | ❌          | MISSING
TOTAL: 0/6 = NOT STARTED
```

**Track this table** through implementation. Update after each checkpoint.

### Completion Definition

**COMPLETE means**:
- ✅ ALL 6 tests (19-24) implemented
- ✅ ALL tests passing
- ✅ ALL acceptance criteria checked
- ✅ Evidence provided (test output)

**NOT complete means**:
- ❌ "5/6 tests done, one has issue"
- ❌ "Works but Test X needs fixing"
- ❌ "Core done, Test Y optional"

---

## Mission Breakdown

### What We're Building

**Wire existing services into chat/web**:
1. Add intent patterns (so chat recognizes document commands)
2. Create handlers (call existing DocumentService methods)
3. Add API routes (with JWT auth from #281)
4. Create prompts (for LLM Q&A, comparison)
5. Implement Tests 19-24 (validate end-to-end)

**What We're NOT Building**:
- ❌ New document processing (already exists)
- ❌ New ChromaDB integration (already configured)
- ❌ New PDF extraction (already working)

**This is integration work** (~350 lines), not new feature development.

---

## Implementation Checkpoints

### Checkpoint 1: Verify Infrastructure (Mandatory First)

**Run verification commands** above.

**Expected findings**:
- ✅ DocumentService has methods: upload_pdf, find_decisions, get_relevant_context, suggest_documents
- ✅ DocumentAnalyzer has analyze() method
- ✅ ChromaDB configured with OpenAI embeddings
- ✅ CLI commands work: `python -m cli documents --help`

**Provide evidence**:
```bash
# Show that services exist
ls -lh services/knowledge_graph/document_service.py
ls -lh services/analysis/document_analyzer.py

# Show key methods
grep -A 5 "async def upload_pdf" services/knowledge_graph/document_service.py
grep -A 5 "async def analyze" services/analysis/document_analyzer.py
```

**If mismatch found**: STOP and report to PM.

---

### Checkpoint 2: Extend Intent Classifier

**Goal**: Add intent patterns for document operations.

**File**: `services/intent_service/classifier.py`

**Add patterns** (around line 195 where search_documents exists):
```python
# Document analysis intents
"analyze": "analyze_document",
"summarize": "summarize_document",
"what does": "question_document",
"compare": "compare_documents",
# search_documents already exists ✅
```

**File**: `shared_types.py`

**Add TaskTypes**:
```python
ANALYZE_DOCUMENT = "analyze_document"
QUESTION_ANSWER_DOCUMENT = "qa_document"
COMPARE_DOCUMENTS = "compare_documents"
SUMMARIZE_DOCUMENT = "summarize_document"
```

**Test**:
```bash
# Verify intent patterns added
grep -n "analyze_document" services/intent_service/classifier.py
grep -n "ANALYZE_DOCUMENT" shared_types.py
```

**Evidence**: Show git diff with new patterns.

**Update progress table**:
```
Checkpoint 1: Infrastructure ✅ VERIFIED
Checkpoint 2: Intent patterns ⏳ IN PROGRESS
```

---

### Checkpoint 3: Create Document Handlers

**Goal**: Create handlers that call existing DocumentService methods.

**Create**: `services/intent_service/document_handlers.py`

**Implement 5 handlers**:
```python
from services.knowledge_graph.document_service import DocumentService
from services.analysis.document_analyzer import DocumentAnalyzer

async def _handle_analyze_document_intent(intent, file_id) -> IntentResult:
    """Call DocumentAnalyzer.analyze() on uploaded file"""
    # 1. Retrieve file from UploadedFileDB
    # 2. Call DocumentAnalyzer.analyze(file_content)
    # 3. Return formatted result
    pass

async def _handle_question_document_intent(intent, file_id, question) -> IntentResult:
    """Answer question about document using LLM + doc context"""
    # 1. Retrieve document content
    # 2. Build Q&A prompt with get_document_qa_prompt()
    # 3. Call LLM with document context
    # 4. Return answer
    pass

async def _handle_summarize_document_intent(intent, file_id) -> IntentResult:
    """Summarize document (reuse DocumentAnalyzer)"""
    # Same as analyze but format as summary
    pass

async def _handle_compare_documents_intent(intent, file_ids) -> IntentResult:
    """Compare multiple documents"""
    # 1. Retrieve all documents
    # 2. Build comparison prompt
    # 3. Call LLM
    # 4. Return structured comparison
    pass

async def _handle_search_documents_intent(intent, query) -> IntentResult:
    """Search user's documents (reuse DocumentService.find_decisions)"""
    # 1. Call DocumentService.find_decisions(query)
    # 2. Format results
    # 3. Return with context
    pass
```

**Wire into intent router** (follow existing pattern from #281).

**Test**:
```bash
# Verify handlers created
ls -lh services/intent_service/document_handlers.py
wc -l services/intent_service/document_handlers.py
# Expected: ~150 lines

# Verify imports work
python -c "from services.intent_service.document_handlers import _handle_analyze_document_intent"
```

**Evidence**: Show file created, line count, test imports.

**Update progress**:
```
Checkpoint 2: Intent patterns ✅ COMPLETE
Checkpoint 3: Document handlers ⏳ IN PROGRESS
```

---

### Checkpoint 4: Add API Routes

**Goal**: Create REST endpoints with JWT auth.

**Extend**: `web/api/routes/files.py` (or create separate `documents.py`)

**Add 5 endpoints** (all require JWT auth):
```python
from fastapi import APIRouter, Depends
from services.auth.auth_middleware import get_current_user

router = APIRouter()

@router.post("/api/v1/documents/{file_id}/analyze")
async def analyze_document(
    file_id: str,
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Analyze uploaded document"""
    # Call _handle_analyze_document_intent
    pass

@router.post("/api/v1/documents/{file_id}/question")
async def ask_question(
    file_id: str,
    question: str,
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Answer question about document"""
    # Call _handle_question_document_intent
    pass

@router.post("/api/v1/documents/compare")
async def compare_documents(
    file_ids: List[str],
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Compare multiple documents"""
    # Call _handle_compare_documents_intent
    pass

@router.get("/api/v1/documents/search")
async def search_documents(
    q: str,
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Search across user's documents"""
    # Call _handle_search_documents_intent
    pass

@router.post("/api/v1/documents/{file_id}/summarize")
async def summarize_document(
    file_id: str,
    format: str = "bullet",
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Summarize document"""
    # Call _handle_summarize_document_intent
    pass
```

**Mount in**: `web/app.py` (follow pattern from files routes in #282)

**Test**:
```bash
# Start server
python main.py &

# Test endpoints (after implementing)
curl -X POST http://localhost:8001/api/v1/documents/{file_id}/analyze \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 or 401 (needs auth)
```

**Evidence**: Show routes registered, OpenAPI spec updated.

**Update progress**:
```
Checkpoint 3: Document handlers ✅ COMPLETE
Checkpoint 4: API routes ⏳ IN PROGRESS
```

---

### Checkpoint 5: Create Document Prompts

**Goal**: Add prompts for Q&A, comparison, extraction.

**Add to**: `services/prompts.py`

**Create 3 prompts**:
```python
def get_document_qa_prompt(document_text: str, question: str) -> str:
    """Generate Q&A prompt with document context"""
    return f"""
You are answering a question about a document.

Document content:
{document_text}

User question: {question}

Answer based ONLY on the document content above.
Cite specific sections when possible.
If the answer is not in the document, say so clearly.
"""

def get_document_comparison_prompt(doc1_text: str, doc2_text: str) -> str:
    """Generate comparison prompt"""
    return f"""
Compare these two documents:

Document 1:
{doc1_text}

Document 2:
{doc2_text}

Provide a structured comparison:
1. Key similarities
2. Key differences
3. Complementary information
4. Conflicting information (if any)
"""

def get_entity_extraction_prompt(document_text: str, entity_type: str) -> str:
    """Extract entities from document"""
    return f"""
Extract {entity_type} from this document:

{document_text}

Return as structured list.
"""
```

**Reuse**: `get_json_summary_prompt()` already exists for summarization.

**Test**:
```bash
# Verify prompts added
grep -n "get_document_qa_prompt" services/prompts.py
grep -n "get_document_comparison_prompt" services/prompts.py
```

**Evidence**: Show prompts added.

**Update progress**:
```
Checkpoint 4: API routes ✅ COMPLETE
Checkpoint 5: Document prompts ⏳ IN PROGRESS
```

---

### Checkpoint 6: Implement Tests 19-24

**Goal**: Validate each user scenario end-to-end.

**Create**: `tests/integration/test_document_processing.py`

**Implement 6 tests**:
```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
class TestDocumentProcessing:

    async def test_19_analyze_uploaded_document(self, async_client, test_user):
        """Test 19: Can you analyze the document I just uploaded?"""
        # 1. Upload PDF via API
        # 2. Call /api/v1/documents/{file_id}/analyze
        # 3. Verify: summary, key_findings present
        # 4. Assert: HTTP 200, valid JSON response
        pass

    async def test_20_question_document(self, async_client, test_user):
        """Test 20: What are the key decision points in this document?"""
        # 1. Upload document with known content
        # 2. Call /api/v1/documents/{file_id}/question
        # 3. Verify: Answer contains expected information
        # 4. Assert: Response references document
        pass

    async def test_21_reference_in_conversation(self, async_client, test_user):
        """Test 21: Based on doc and discussion, what should I prioritize?"""
        # 1. Upload document
        # 2. Send chat message referencing doc
        # 3. Verify: Response includes document context
        # 4. Assert: Natural integration
        pass

    async def test_22_summarize_document(self, async_client, test_user):
        """Test 22: Summarize the research paper in 3 key points"""
        # 1. Upload multi-page PDF
        # 2. Call /api/v1/documents/{file_id}/summarize
        # 3. Verify: 3-5 key points returned
        # 4. Assert: Concise, accurate summary
        pass

    async def test_23_compare_documents(self, async_client, test_user):
        """Test 23: Compare these and highlight differences"""
        # 1. Upload two related documents
        # 2. Call /api/v1/documents/compare
        # 3. Verify: Similarities, differences identified
        # 4. Assert: Structured comparison output
        pass

    async def test_24_search_documents(self, async_client, test_user):
        """Test 24: Find section about testing methodology"""
        # 1. Upload 3+ documents
        # 2. Call /api/v1/documents/search?q=testing
        # 3. Verify: Relevant results returned
        # 4. Assert: Results ranked by relevance
        pass
```

**Run tests**:
```bash
pytest tests/integration/test_document_processing.py -v
# Expected: 6 passed
```

**Evidence**: Show ALL 6 tests passing with output.

**Update progress**:
```
Checkpoint 5: Document prompts ✅ COMPLETE
Checkpoint 6: Tests 19-24 ⏳ IN PROGRESS
```

---

## Testing & Verification

### Automated Tests

**Run full test suite**:
```bash
# Integration tests
pytest tests/integration/test_document_processing.py -v
# Expected: 6/6 passing (Tests 19-24)

# Unit tests (if created)
pytest tests/services/intent_service/test_document_handlers.py -v
```

**Evidence required**:
- Full pytest output showing all tests passing
- No failures, no skipped tests

### Manual Testing

**Test via web interface**:
```bash
# 1. Start server
python main.py

# 2. Login
curl -X POST http://localhost:8001/auth/login \
  -d '{"username": "xian", "password": "test"}'

# 3. Upload document
curl -X POST http://localhost:8001/api/v1/files/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf"

# 4. Analyze document
curl -X POST http://localhost:8001/api/v1/documents/{file_id}/analyze \
  -H "Authorization: Bearer $TOKEN"
# Expected: Analysis result

# 5. Question document
curl -X POST "http://localhost:8001/api/v1/documents/{file_id}/question?question=What%20is%20the%20main%20topic?" \
  -H "Authorization: Bearer $TOKEN"
# Expected: Answer

# 6. Search documents
curl -X GET "http://localhost:8001/api/v1/documents/search?q=architecture" \
  -H "Authorization: Bearer $TOKEN"
# Expected: Search results
```

**Evidence**: Show curl outputs proving endpoints work.

---

## Success Criteria

**Verify ALL before claiming complete**:

### Implementation Complete
- [ ] Intent patterns added (classifier.py modified)
- [ ] TaskTypes added (shared_types.py modified)
- [ ] Document handlers created (document_handlers.py)
- [ ] API routes added (files.py or documents.py)
- [ ] Routes mounted (web/app.py)
- [ ] Prompts created (prompts.py)

### Tests Complete
- [ ] Test 19 implemented and passing
- [ ] Test 20 implemented and passing
- [ ] Test 21 implemented and passing
- [ ] Test 22 implemented and passing
- [ ] Test 23 implemented and passing
- [ ] Test 24 implemented and passing

### Quality Complete
- [ ] All endpoints require JWT auth
- [ ] User isolation enforced (can't access others' docs)
- [ ] Error handling for missing files
- [ ] ChromaDB search working
- [ ] DocumentService methods called correctly
- [ ] DocumentAnalyzer integration working

### Evidence Complete
- [ ] All test output provided
- [ ] Manual verification provided
- [ ] Git status clean (committed)
- [ ] No "works but X has issue"

---

## Evidence Format

**Provide complete proof**:

### 1. Files Created/Modified
```bash
git status
git diff --stat main

# Expected:
# M services/intent_service/classifier.py
# M shared_types.py
# M services/prompts.py
# M web/api/routes/files.py (or new documents.py)
# M web/app.py
# A services/intent_service/document_handlers.py
# A tests/integration/test_document_processing.py
```

### 2. All Test Outputs
```bash
pytest tests/integration/test_document_processing.py -v
# Show FULL output with 6/6 passing
```

### 3. Manual Verification
```bash
# Show curl commands and responses for:
# - Analyze document
# - Question document
# - Search documents
```

### 4. Integration Proof
```bash
# Show that existing services were reused:
grep -n "DocumentService" services/intent_service/document_handlers.py
grep -n "DocumentAnalyzer" services/intent_service/document_handlers.py
```

---

## Completion Verification Table

**Before claiming done, verify**:

```
Test | Implemented | Tested | Evidence | Status
---- | ----------- | ------ | -------- | ------
19   | ✅          | ✅     | ✅       | ✅ DONE
20   | ✅          | ✅     | ✅       | ✅ DONE
21   | ✅          | ✅     | ✅       | ✅ DONE
22   | ✅          | ✅     | ✅       | ✅ DONE
23   | ✅          | ✅     | ✅       | ✅ DONE
24   | ✅          | ✅     | ✅       | ✅ DONE
```

**Only then** claim complete.

---

## Questions for PM (if needed)

**If infrastructure doesn't match**:
- DocumentService methods different than described?
- ChromaDB not configured?
- CLI commands don't work?

**If design uncertainty**:
- Should routes be in files.py or separate documents.py?
- Any specific prompt formats needed?
- Any specific response schemas needed?

**Always ask rather than assume!**

---

## What's NOT in Scope

Remember, you're NOT implementing:
- ❌ New document processing (exists)
- ❌ New ChromaDB integration (configured)
- ❌ New PDF extraction (works)
- ❌ New LLM integration (exists)

You're **wiring existing services** into web/chat interface.

---

## Time Lord Reminder

**No time pressure**. Complete means:
- ✅ ALL 6 tests passing
- ✅ ALL acceptance criteria met
- ✅ ALL evidence provided

**Do NOT**:
- ❌ Skip tests because "almost done"
- ❌ Call "complete" with 5/6 tests
- ❌ Say "works but has issue X"

**Quality over speed**. Finish properly.

---

Good luck! This is integration work with proven services. Take it checkpoint by checkpoint, provide evidence at each stage, and you'll get there. 🏰

**First action**: Run infrastructure verification commands and report findings.

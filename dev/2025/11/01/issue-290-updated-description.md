# CORE-ALPHA-DOC-PROCESSING - Implement Document Analysis Workflows (Tests 19-24)

**Priority**: P1 (Medium - post-alpha, required for beta)
**Labels**: `enhancement`, `document-processing`, `alpha-feature`, `tests-19-24`
**Milestone**: Sprint A9 or A10 (post-#281)
**Effort**: Medium (integration work, ~350 lines of wiring code)
**Related Issues**: #282 (upload infrastructure complete), #281 (auth complete)

---

## Problem Statement

File upload infrastructure is complete (#282), but users cannot **analyze, summarize, or search** uploaded documents. Tests 19-24 from the manual testing checklist are not implemented.

**What Users Can Do** ✅:
- Upload files (txt, pdf, docx, md, json)
- Files stored securely with user isolation
- Progress indication and validation

**What Users Cannot Do** ❌:
- Analyze uploaded documents
- Ask questions about document content
- Reference documents in conversation
- Generate summaries
- Compare multiple documents
- Search across their document library

---

## Archaeological Findings (The 75% Pattern)

**Investigation Date**: 2025-11-01
**Investigator**: Code Agent
**Finding**: 70-75% of document processing infrastructure **already exists but is disconnected from chat**

### What Already Works 🎉

| Component | Completeness | Location | Status |
|-----------|-------------|----------|--------|
| PDF Extraction | 100% ✅ | `services/knowledge_graph/ingestion.py` | Production-ready |
| ChromaDB Semantic Search | 90% ✅ | Fully configured with OpenAI embeddings | Works via CLI |
| DocumentAnalyzer | 90% ✅ | `services/analysis/document_analyzer.py` | Summarization functional |
| Document Metadata Analysis | 95% ✅ | Ingester extracts concepts, hierarchy | Enhanced metadata |
| CLI Commands | 80% ✅ | `cli/commands/documents.py` | All operations work |

**Key Services That Exist**:
- `DocumentService.upload_pdf()` - Validates, ingests, indexes PDFs
- `DocumentService.find_decisions()` - Semantic search + metadata filters
- `DocumentService.get_relevant_context()` - Retrieves by timeframe
- `DocumentService.suggest_documents()` - Relevance scoring
- `DocumentIngester.ingest_pdf()` - Chunks, embeds, stores in ChromaDB
- `DocumentAnalyzer.analyze()` - LLM-powered summarization

**Evidence**: All methods tested and working via CLI commands

---

## What's Missing (Integration Work)

### Gap Analysis

| Component | Status | Impact | Scope |
|-----------|--------|--------|-------|
| Document intent handlers | ❌ Missing | Can't call analysis from chat | Medium |
| API routes for operations | ❌ Missing | Web UI can't access analysis | Small |
| Document-specific prompts | ❌ Missing | Need Q&A, comparison prompts | Small |
| Intent classifier patterns | ⚠️ Partial | Chat doesn't recognize doc commands | Small |
| Tests 19-24 | ❌ Missing | No end-to-end validation | Medium |

**Total Work**: ~350 lines of wiring code (mostly integration, not new features)

---

## Requirements (From Manual Testing Checklist)

### Test 18: File Upload ✅ **COMPLETE** (#282)
**Status**: Implemented
**What works**: Upload files, progress indication, user isolation

---

### Test 19: Document Analysis Request ❌ **TO IMPLEMENT**
**User Action**: "Can you analyze the document I just uploaded?"

**Requirements**:
- Retrieve uploaded file by reference
- Call `DocumentAnalyzer.analyze()` with file content
- Return structured insights (summary + key findings)
- Handle errors gracefully

**Implementation**:
- Intent: `ANALYZE_DOCUMENT`
- Handler: `_handle_analyze_document_intent()`
- API Route: `POST /api/v1/documents/{file_id}/analyze`

---

### Test 20: Specific Analysis Query ❌ **TO IMPLEMENT**
**User Action**: "What are the key decision points in this document?"

**Requirements**:
- Parse question from user message
- Retrieve document content
- Use LLM Q&A with document context
- Format response with specific answers

**Implementation**:
- Intent: `QUESTION_DOCUMENT`
- Handler: `_handle_question_document_intent(question, file_id)`
- API Route: `POST /api/v1/documents/{file_id}/question`
- Prompt: `get_document_qa_prompt(doc_text, question)`

---

### Test 21: Reference in Conversation ❌ **TO IMPLEMENT**
**User Action**: "Based on what we discussed and the uploaded doc, what should I prioritize?"

**Requirements**:
- Detect document reference in message
- Merge conversation history + document context
- LLM synthesis of multiple sources
- Natural attribution to sources

**Implementation**:
- Session context: Track recent uploads
- File resolver: Match "uploaded doc" → file_id
- Context enrichment: Add doc content to prompt

---

### Test 22: Document Summary ❌ **TO IMPLEMENT**
**User Action**: "Summarize the uploaded research paper in 3 key points"

**Requirements**:
- Retrieve document by reference
- Call summarization with constraints
- Structured output (bullet points)
- Respect user's format request

**Implementation**:
- Intent: `SUMMARIZE_DOCUMENT`
- Handler: `_handle_summarize_document_intent(file_id, format)`
- Reuse: `DocumentAnalyzer.analyze()` (already works)

---

### Test 23: Multi-Document Comparison ❌ **TO IMPLEMENT**
**User Action**: Upload 2+ documents, ask "Compare these and highlight differences"

**Requirements**:
- Multi-document retrieval
- Parallel content extraction
- LLM comparative analysis
- Structured difference highlighting

**Implementation**:
- Intent: `COMPARE_DOCUMENTS`
- Handler: `_handle_compare_documents_intent(file_ids)`
- API Route: `POST /api/v1/documents/compare`
- Prompt: `get_document_comparison_prompt(doc1, doc2)`

---

### Test 24: Document Search ❌ **TO IMPLEMENT**
**User Action**: "Find the section about testing methodology in my uploaded docs"

**Requirements**:
- Full-text + semantic search
- User-scoped results
- Context extraction around matches
- Relevance ranking

**Implementation**:
- Intent: `SEARCH_DOCUMENTS` (already recognized!)
- Handler: `_handle_search_documents_intent(query)`
- Reuse: `DocumentService.find_decisions()` (works via CLI)
- API Route: `GET /api/v1/documents/search?q={query}`

---

## Implementation Plan

### Phase 1: Extend Intent Classifier

**File**: `services/intent_service/classifier.py`

**Add patterns**:
```python
# Document analysis intents
"analyze": "analyze_document",
"summarize": "summarize_document",
"what does": "question_document",
"compare": "compare_documents",
# search_documents already exists ✅
```

**Add TaskTypes** to `shared_types.py`:
```python
ANALYZE_DOCUMENT = "analyze_document"
QUESTION_ANSWER_DOCUMENT = "qa_document"
COMPARE_DOCUMENTS = "compare_documents"
SUMMARIZE_DOCUMENT = "summarize_document"
```

**Evidence**: Intent patterns already exist for `search_documents` (line 195)

---

### Phase 2: Create Document Handlers

**Create**: `services/intent_service/document_handlers.py`

**Implement handlers** for each document operation:
```python
async def _handle_analyze_document_intent(intent, file_id) -> IntentResult
    # Retrieve file from UploadedFileDB
    # Call DocumentAnalyzer.analyze()
    # Return formatted result

async def _handle_question_document_intent(intent, file_id, question) -> IntentResult
    # Retrieve document content
    # Build Q&A prompt
    # Call LLM with document context
    # Return answer

async def _handle_summarize_document_intent(intent, file_id) -> IntentResult
    # Reuse DocumentAnalyzer (already works)
    # Format as structured summary
    # Return key points

async def _handle_compare_documents_intent(intent, file_ids) -> IntentResult
    # Retrieve multiple documents
    # Build comparison prompt
    # Call LLM for analysis
    # Return structured comparison

async def _handle_search_documents_intent(intent, query) -> IntentResult
    # Call DocumentService.find_decisions()
    # Format search results
    # Return with context
```

**Wire into**: Intent router (existing pattern from #281, #282)

---

### Phase 3: Add Document API Routes

**Extend**: `web/api/routes/files.py` (or create `documents.py`)

**Add endpoints** (all require JWT auth via `get_current_user`):
```python
@router.post("/api/v1/documents/{file_id}/analyze")
async def analyze_document(
    file_id: str,
    current_user: dict = Depends(get_current_user)
) -> AnalysisResult

@router.post("/api/v1/documents/{file_id}/question")
async def ask_question(
    file_id: str,
    question: str,
    current_user: dict = Depends(get_current_user)
) -> dict

@router.post("/api/v1/documents/compare")
async def compare_documents(
    file_ids: List[str],
    current_user: dict = Depends(get_current_user)
) -> ComparisonResult

@router.get("/api/v1/documents/search")
async def search_documents(
    q: str,
    current_user: dict = Depends(get_current_user)
) -> List[SearchResult]

@router.post("/api/v1/documents/{file_id}/summarize")
async def summarize_document(
    file_id: str,
    format: str = "bullet",
    current_user: dict = Depends(get_current_user)
) -> SummaryResult
```

**Mount**: In `web/app.py` lifespan (existing pattern from files routes)

---

### Phase 4: Document-Specific Prompts

**Add to**: `services/prompts.py`

**Create prompts** for:
```python
def get_document_qa_prompt(document_text: str, question: str) -> str:
    """Generate Q&A prompt with document context"""

def get_document_comparison_prompt(doc1_text: str, doc2_text: str) -> str:
    """Generate comparison prompt"""

def get_entity_extraction_prompt(document_text: str, entity_type: str) -> str:
    """Extract entities from document"""
```

**Reuse**: `get_json_summary_prompt()` already exists for summarization

---

### Phase 5: Implement Tests 19-24

**Create**: `tests/integration/test_document_processing.py`

**Test each user scenario**:
```python
async def test_19_analyze_uploaded_document():
    # Upload PDF via API
    # Call analyze endpoint
    # Verify: summary, key_findings present

async def test_20_question_document():
    # Upload document with known content
    # Ask specific question
    # Verify: Answer contains expected information

async def test_21_reference_in_conversation():
    # Upload document
    # Send message referencing doc
    # Verify: Response includes document context

async def test_22_summarize_document():
    # Upload multi-page PDF
    # Request summary
    # Verify: Key points returned

async def test_23_compare_documents():
    # Upload two related documents
    # Request comparison
    # Verify: Similarities, differences identified

async def test_24_search_documents():
    # Upload 3+ documents
    # Search for specific term
    # Verify: Relevant results returned
```

**Use**: Existing test infrastructure patterns from #281

---

## Acceptance Criteria

### Core Functionality
- [ ] Test 19: Users can analyze uploaded documents via chat
- [ ] Test 20: Users can ask questions about document content
- [ ] Test 21: Documents referenced naturally in conversation
- [ ] Test 22: Document summaries generated on request
- [ ] Test 23: Multiple documents compared successfully
- [ ] Test 24: Semantic search across user's documents works

### Technical Requirements
- [ ] Intent classifier recognizes all document operations
- [ ] Document handlers implemented and wired
- [ ] API routes secured with JWT authentication
- [ ] ChromaDB search integrated with user isolation
- [ ] Prompts generate high-quality responses
- [ ] All 6 tests (19-24) passing

### Quality Standards
- [ ] Error handling for missing files
- [ ] User isolation enforced (can't access others' docs)
- [ ] Response times acceptable (<5s for analysis)
- [ ] Large documents handled (chunking works)
- [ ] Clear error messages for failures

---

## Dependencies

### ✅ Complete (Ready to Use)
- ✅ File upload infrastructure (#282)
- ✅ JWT authentication (#281)
- ✅ DocumentService with all methods
- ✅ DocumentAnalyzer with LLM integration
- ✅ ChromaDB with OpenAI embeddings
- ✅ PDF extraction (PyPDF2)
- ✅ CLI commands (patterns to follow)

### 📦 No Additional Libraries Needed
- All dependencies already installed
- ChromaDB configured and working
- OpenAI embeddings active

---

## Risk Assessment

### Low Risk ✅
- All processing components proven (work via CLI)
- DocumentService methods tested with real PDFs
- ChromaDB stable and configured
- No database schema changes needed
- Following existing patterns (intent handlers, API routes from #281, #282)

### Medium Risk ⚠️
- Intent handler complexity (file context passing)
- Session state management (tracking recent uploads)
- Response formatting (multiple document types)

### Mitigation Strategies
- Use existing intent handler patterns
- Test with simple cases first (single document)
- Reuse DocumentService methods (already tested)
- Follow #282 patterns for user isolation
- Follow #281 patterns for auth integration

---

## Evidence (From Investigation)

### Services That Exist
```bash
# DocumentService methods
$ grep -n "async def" services/knowledge_graph/document_service.py
27:    async def upload_pdf(self, file: UploadFile, metadata: Dict)
70:    async def find_decisions(self, topic: str, timeframe: str)
176:   async def get_relevant_context(self, timeframe: str)
259:   async def suggest_documents(self, focus_area: str)

# DocumentAnalyzer
$ grep -n "class DocumentAnalyzer" services/analysis/document_analyzer.py
12:class DocumentAnalyzer(BaseAnalyzer):

# ChromaDB configuration
$ grep -n "chromadb" services/knowledge_graph/ingestion.py
34:    self.client = chromadb.PersistentClient(path="./data/chromadb")
41:    embedding_functions.OpenAIEmbeddingFunction(...)
```

### CLI Evidence (Working Commands)
```bash
# These all work via CLI - just need web/chat integration
$ python -m cli documents decide --topic "architecture"
$ python -m cli documents context --timeframe "last_week"
$ python -m cli documents add --file report.pdf
$ python -m cli documents review --focus-area "testing"
```

**Conclusion**: Services exist and work. Need to wire them into web/chat interface.

---

## Files to Create/Modify

### Create (New Files)
```
services/intent_service/document_handlers.py  (~150 lines)
tests/integration/test_document_processing.py (~200 lines)
```

### Modify (Existing Files)
```
services/intent_service/classifier.py         +30 lines (intents)
shared_types.py                               +5 lines (TaskTypes)
services/prompts.py                           +60 lines (prompts)
web/api/routes/files.py (or documents.py)    +100 lines (routes)
web/app.py                                    +5 lines (mount routes)
```

**Total New Code**: ~350 lines (mostly wiring, not new features)

---

## Success Metrics

### Functional
- All Tests 19-24 passing
- Document operations work via chat
- Response quality high (accurate summaries, good answers)
- Search returns relevant results

### Performance
- Analysis completes in reasonable time
- Search returns quickly
- Large PDFs handled (10+ pages)
- Multiple documents compared efficiently

### User Experience
- Natural language references work ("the doc I uploaded")
- Error messages helpful and clear
- Progress indication for long operations
- Results well-formatted

---

## Post-Implementation

### Alpha Testing
- Validate with 5-10 alpha testers
- Gather feedback on document workflows
- Measure usage patterns
- Identify edge cases

### Enhancements (Defer to Beta)
- Document versioning
- Collaborative annotations
- Advanced chunking strategies
- Multi-document summarization
- Document clustering/organization

---

## Related Documentation

**Investigation Report**: `dev/2025/11/01/investigation-document-processing-pipeline-282.md`

**Manual Testing Checklist**: `dev/2025/10/27/phase-2-manual-testing-checklist.md` (Tests 19-24, lines 404-543)

**Issue #282**: File upload infrastructure (complete)

**Issue #281**: Web authentication (complete)

---

## Completion Criteria

**COMPLETE means**:
- ✅ ALL 6 tests (19-24) passing
- ✅ ALL acceptance criteria checked
- ✅ ALL document handlers implemented
- ✅ ALL API routes working with auth
- ✅ Evidence provided (test output, manual verification)
- ✅ Zero known issues

**NOT complete means**:
- ❌ "Works but Test X has issue"
- ❌ "5/6 tests passing"
- ❌ "Core done, extras optional"

See: `anti-80-percent-completion-protocol.md` for completion standards.

---

**Priority**: P1 (Medium - implement in Sprint A9 or A10)
**Effort**: Medium (integration work, ~350 lines)
**Ready to Start**: After #281 complete ✅
**Confidence**: High (90%) - infrastructure exists and proven via CLI

---

*This issue represents the final 25% of work to complete document processing. The archaeological investigation confirmed that 75% already exists and works via CLI - we just need to wire it into chat and web.*

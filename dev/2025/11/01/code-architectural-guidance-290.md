# Architectural Guidance: Issue #290 Document Handlers

**Date**: November 1, 2025, 4:18 PM PT
**Context**: Code discovered IntentService is 4974 lines and asked about approach
**Decision**: Use proper separation of concerns with separate handlers file

---

## TL;DR

**Use Option C: Both handlers AND routes, properly separated**

Create **NEW FILE** `services/intent_service/document_handlers.py` (don't bloat IntentService), then wire it in minimally. Also create REST routes. Both can call the same DocumentService methods.

---

## Why Code is Confused

Code correctly identified that IntentService is large (4974 lines) and adding more handlers directly would create technical debt. This is good architectural thinking!

**The solution is already in Issue #290** - just needs clarification.

---

## The Right Pattern (From Issue #290)

Looking at Phase 2 from the issue:

```markdown
Phase 2: Create Document Handlers

**Create**: `services/intent_service/document_handlers.py`  <-- NEW FILE (separate)
```

**Key**: Issue says "Create document_handlers.py" NOT "add to IntentService"

This follows **separation of concerns** principle:
- Keep handler logic isolated
- Don't bloat existing large files
- Easy to test independently
- Clear responsibility boundaries

---

## Step-by-Step Implementation

### Step 1: Research Existing Patterns (Use Serena)

**Before writing any code**, understand how handlers are currently structured:

```python
# 1. See what's in intent_service directory
serena.list_dir("services/intent_service")

# 2. How is IntentService structured?
serena.find_symbol("IntentService")
serena.view_file("services/intent_service/intent_service.py", view_range=[1, 100])

# 3. Are there existing handler files?
serena.list_dir("services/intent_service")
# Look for patterns like *_handlers.py or *_handler.py

# 4. How do routes work?
serena.view_file("web/api/routes/files.py", view_range=[1, 50])

# 5. How are intents classified and routed?
serena.find_symbol("classify_intent")
serena.find_symbol("route_intent")
```

**Report what you find** before implementing. Pattern may already exist!

---

### Step 2: Create Document Handlers (NEW FILE)

**Create**: `services/intent_service/document_handlers.py`

```python
"""
Document operation handlers for Issue #290.

These handlers wire existing DocumentService and DocumentAnalyzer
into the chat/intent system.
"""

from typing import Dict, List
from services.knowledge_graph.document_service import DocumentService
from services.analysis.document_analyzer import DocumentAnalyzer
from services.prompts import (
    get_document_qa_prompt,
    get_document_comparison_prompt
)

# Initialize services (or use dependency injection pattern if exists)
doc_service = DocumentService()
doc_analyzer = DocumentAnalyzer()


async def handle_analyze_document(
    file_id: str,
    user_id: str
) -> Dict:
    """
    Test 19: Analyze uploaded document.

    Calls existing DocumentAnalyzer.analyze() method.
    """
    # 1. Retrieve file (use existing UploadedFileDB or DocumentService)
    file = await doc_service.get_file(file_id, user_id)

    # 2. Call existing analyzer
    analysis = await doc_analyzer.analyze(file.content)

    # 3. Return formatted result
    return {
        "summary": analysis.summary,
        "key_findings": analysis.key_findings
    }


async def handle_question_document(
    file_id: str,
    question: str,
    user_id: str
) -> Dict:
    """
    Test 20: Answer question about document.

    Uses existing DocumentService + LLM Q&A prompt.
    """
    # 1. Retrieve document
    file = await doc_service.get_file(file_id, user_id)

    # 2. Build Q&A prompt
    prompt = get_document_qa_prompt(file.content, question)

    # 3. Call LLM (use existing LLM service)
    answer = await llm_service.complete(prompt)

    return {
        "answer": answer,
        "question": question,
        "file_id": file_id
    }


async def handle_summarize_document(
    file_id: str,
    format: str,
    user_id: str
) -> Dict:
    """
    Test 22: Summarize document.

    Reuses DocumentAnalyzer.analyze() (same as analyze but formatted differently).
    """
    # Similar to handle_analyze_document but format output
    pass


async def handle_compare_documents(
    file_ids: List[str],
    user_id: str
) -> Dict:
    """
    Test 23: Compare multiple documents.

    Uses existing DocumentService + comparison prompt.
    """
    # 1. Retrieve all documents
    files = [await doc_service.get_file(fid, user_id) for fid in file_ids]

    # 2. Build comparison prompt
    prompt = get_document_comparison_prompt(files[0].content, files[1].content)

    # 3. Call LLM
    comparison = await llm_service.complete(prompt)

    return comparison


async def handle_search_documents(
    query: str,
    user_id: str
) -> Dict:
    """
    Test 24: Search across user's documents.

    Calls existing DocumentService.find_decisions() (uses ChromaDB).
    """
    # Call existing search method
    results = await doc_service.find_decisions(query, user_id=user_id)

    return {
        "query": query,
        "results": results
    }
```

**Key Points**:
- Each handler is standalone function
- All handlers call EXISTING services (DocumentService, DocumentAnalyzer)
- User isolation via user_id parameter
- Clear docstrings reference test numbers

---

### Step 3: Wire Handlers into IntentService (MINIMAL CHANGES)

**Find where intents are routed** (use Serena to locate):
```python
serena.find_symbol("route_intent")
# OR
serena.find_symbol("handle_intent")
```

**Add routing logic** (minimal addition):
```python
# In intent_service.py or routing module
from services.intent_service.document_handlers import (
    handle_analyze_document,
    handle_question_document,
    handle_summarize_document,
    handle_compare_documents,
    handle_search_documents
)

# In routing method (wherever intent routing happens)
async def route_intent(intent_type: str, params: Dict, user_id: str):
    if intent_type == "analyze_document":
        return await handle_analyze_document(
            file_id=params["file_id"],
            user_id=user_id
        )

    elif intent_type == "question_document":
        return await handle_question_document(
            file_id=params["file_id"],
            question=params["question"],
            user_id=user_id
        )

    elif intent_type == "summarize_document":
        return await handle_summarize_document(
            file_id=params["file_id"],
            format=params.get("format", "bullet"),
            user_id=user_id
        )

    elif intent_type == "compare_documents":
        return await handle_compare_documents(
            file_ids=params["file_ids"],
            user_id=user_id
        )

    elif intent_type == "search_documents":
        return await handle_search_documents(
            query=params["query"],
            user_id=user_id
        )

    # ... existing routing logic
```

**Only add routing logic** - don't bloat IntentService with handler implementations.

---

### Step 4: Create API Routes (Separate Layer)

**Create**: `web/api/routes/documents.py`

```python
"""
Document analysis REST API endpoints for Issue #290.

These routes provide direct API access to document operations,
following the pattern from files.py (#282).
"""

from fastapi import APIRouter, Depends, HTTPException
from services.auth.auth_middleware import get_current_user
from services.intent_service.document_handlers import (
    handle_analyze_document,
    handle_question_document,
    handle_summarize_document,
    handle_compare_documents,
    handle_search_documents
)

router = APIRouter()


@router.post("/api/v1/documents/{file_id}/analyze")
async def analyze_document(
    file_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Test 19: Analyze uploaded document"""
    try:
        result = await handle_analyze_document(
            file_id=file_id,
            user_id=current_user["user_id"]
        )
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")


@router.post("/api/v1/documents/{file_id}/question")
async def ask_question(
    file_id: str,
    question: str,
    current_user: dict = Depends(get_current_user)
):
    """Test 20: Question about document"""
    result = await handle_question_document(
        file_id=file_id,
        question=question,
        user_id=current_user["user_id"]
    )
    return result


# ... similar for other endpoints
```

**Mount in** `web/app.py`:
```python
from web.api.routes.documents import router as documents_router

app.include_router(documents_router, tags=["documents"])
```

---

## Why Both Handlers AND Routes?

**Handlers** (`document_handlers.py`):
- Used by chat ("analyze this doc")
- Intent-driven workflow
- Conversational integration

**Routes** (`documents.py`):
- Used by API clients
- Direct HTTP access
- Testing and development
- Follows REST patterns

**Both call the same DocumentService methods** - no duplication.

---

## Architecture Diagram

```
Chat Message: "analyze this doc"
    ↓
Intent Classifier (recognizes "analyze_document")
    ↓
document_handlers.handle_analyze_document()
    ↓
DocumentService.get_file() + DocumentAnalyzer.analyze()
    ↓
Return result

API Request: POST /api/v1/documents/123/analyze
    ↓
documents.py:analyze_document()
    ↓
document_handlers.handle_analyze_document()
    ↓
DocumentService.get_file() + DocumentAnalyzer.analyze()
    ↓
Return result
```

**Key**: Single path to DocumentService (no duplication)

---

## What This Achieves

### ✅ Separation of Concerns
- Handlers isolated in separate file
- IntentService stays focused on routing
- Routes stay focused on HTTP

### ✅ Follows Existing Patterns
- Similar to how file upload (#282) structured
- Similar to how auth (#281) structured
- Domain-driven design principles

### ✅ Maintainable
- Easy to find handler logic (one file)
- Easy to test handlers independently
- Clear responsibility boundaries

### ✅ No Technical Debt
- Not bloating large files
- Not duplicating service implementations
- Following established patterns

---

## Testing Strategy

**Test handlers directly**:
```python
# Unit test
async def test_handle_analyze_document():
    result = await handle_analyze_document(
        file_id="test-file",
        user_id="test-user"
    )
    assert "summary" in result
```

**Test routes**:
```python
# Integration test
async def test_analyze_endpoint(async_client):
    response = await async_client.post(
        "/api/v1/documents/test-file/analyze",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

**Test via chat** (Tests 19-24):
```python
# End-to-end test
async def test_19_analyze_via_chat():
    # Send chat message "analyze document"
    # Verify intent classified
    # Verify handler called
    # Verify result returned
```

---

## Verification Checklist

Before claiming complete:
- [ ] `document_handlers.py` created (not added to IntentService)
- [ ] Handlers call existing DocumentService methods (verified)
- [ ] Handlers wired into IntentService (minimal changes)
- [ ] API routes created in separate file
- [ ] Routes mounted in app.py
- [ ] All 6 handlers implemented
- [ ] All 6 routes implemented
- [ ] Tests 19-24 passing

---

## Summary

**Do This**:
✅ Create separate `document_handlers.py`
✅ Research existing patterns with Serena first
✅ Wire handlers minimally into IntentService
✅ Create separate `documents.py` for routes
✅ Both layers call same DocumentService methods

**Don't Do This**:
❌ Add handlers directly to large IntentService
❌ Duplicate DocumentService functionality
❌ Skip researching existing patterns
❌ Create new document processing (already exists)

---

**The issue description already specified this pattern** - you just need to follow it systematically.

**First action**: Use Serena to research existing handler patterns, then implement following those patterns.

Good luck! 🏰

# Gameplan: Issue #522 - Query #40: Update Document

**GitHub Issue**: #522
**Date**: December 27, 2025
**Lead Developer**: Opus 4.5
**Status**: READY FOR APPROVAL

---

## Query in Scope

| Query # | User Query          | What's Needed                              |
| ------- | ------------------- | ------------------------------------------ |
| #40     | "Update the X document" | Search document by name → get page ID → update via router |

---

## Phase 0: Infrastructure Verification

### Current State (Verified)

| Component                | Status         | Location                                                   |
| ------------------------ | -------------- | ---------------------------------------------------------- |
| NotionIntegrationRouter  | ✅ Exists      | `services/integrations/notion/notion_integration_router.py` |
| `update_page()`          | ✅ Exists      | Lines 382-403                                              |
| `search_notion()`        | ✅ Exists      | Lines 460-484                                              |
| `is_configured()`        | ✅ Exists      | Lines 155-172                                              |
| Document search handler  | ✅ Exists      | `_handle_search_documents_notion()` - Query #20            |
| Document update handler  | ❌ **Missing** | Needs to be added                                          |

### Architecture Understanding

```
Router Pattern (same as Query #20):
IntentService._handle_update_document_notion()
    → NotionIntegrationRouter.search_notion(doc_name)  # Find page by name
    → NotionIntegrationRouter.update_page(page_id, properties)  # Update it
```

**Key Finding**: The `_handle_search_documents_notion()` handler (lines 677-809) shows the exact pattern:
1. Initialize NotionIntegrationRouter
2. Check `is_configured()` for graceful degradation
3. Call `search_notion()` to find pages
4. Extract page ID from results
5. Return formatted response

### What Needs to Be Added

1. **Intent Handler** (`intent_service.py`):
   - Add `_handle_update_document_notion()` handler
   - Parse document name and update content from query
   - Search for document by name using `search_notion()`
   - Update document using `update_page()`
   - Handle ambiguity (multiple matches) with clarification

2. **Intent Routing** (`intent_service.py`):
   - Add routing logic for update_document action

3. **Pre-Classifier** (`pre_classifier.py`):
   - Add DOCUMENT_QUERY_PATTERNS for update queries

---

## Phase 1: Intent Handler Implementation

### 1.1 Add Handler

**File**: `services/intent/intent_service.py`

Follow pattern from `_handle_search_documents_notion()`:

```python
async def _handle_update_document_notion(
    self, intent: Intent, workflow_id: str, session_id: str
) -> IntentProcessingResult:
    """
    Handle document update via Notion integration.

    Issue #522: Canonical Query #40 - "Update the X document"
    Uses NotionIntegrationRouter.search_notion() to find document,
    then update_page() to modify it.

    Flow:
    1. Extract document name and update content from query
    2. Search for document by name
    3. Handle ambiguity (0 matches, 1 match, multiple matches)
    4. Update document properties
    5. Return confirmation

    Args:
        intent: The classified intent with document name in context
        workflow_id: Current workflow ID
        session_id: User session ID

    Returns:
        IntentProcessingResult with update confirmation or clarification
    """
```

### 1.2 Key Implementation Details

**Query Parsing**:
- "Update the README document" → doc_name="README"
- "Update project plan with new deadline" → doc_name="project plan", content="new deadline"
- "Add notes to meeting doc" → doc_name="meeting doc", action="add"

**Ambiguity Handling** (same as existing patterns):
- 0 matches: "No document found matching 'X'. Try a more specific name."
- 1 match: Proceed with update
- Multiple matches: "Found N documents matching 'X': [list]. Which one do you mean?"

**Update Properties** (Notion API format):
```python
properties = {
    "description": {  # Or appropriate property
        "rich_text": [{"text": {"content": update_content}}]
    }
}
```

### 1.3 Add Pre-Classifier Patterns

**File**: `services/intent_service/pre_classifier.py`

Add to pattern groups:

```python
DOCUMENT_QUERY_PATTERNS = [
    r"\bupdate\s+(?:the\s+)?(?:\w+\s+)?doc(?:ument)?\b",
    r"\bedit\s+(?:the\s+)?(?:\w+\s+)?doc(?:ument)?\b",
    r"\bmodify\s+(?:the\s+)?(?:\w+\s+)?doc(?:ument)?\b",
    r"\badd\s+(?:to\s+)?(?:the\s+)?(?:\w+\s+)?doc(?:ument)?\b",
    r"\bupdate\s+(?:the\s+)?\w+(?:\s+with\b|\s+to\b)",
]
```

---

## Phase 2: Tests (Following Issue #521 Discipline)

### 2.1 Routing Integration Tests (CRITICAL per Issue #521 learning)

**File**: `tests/unit/services/intent_service/test_document_query_handlers.py` (NEW)

```python
class TestPreClassifierDocumentRouting:
    """Test pre-classifier routes document update queries correctly."""

    @pytest.mark.parametrize("query", [
        "update the README document",
        "edit the project plan doc",
        "modify the meeting notes document",
        "add to the status document",
        "update project plan with new deadline",
    ])
    def test_document_update_queries_route_correctly(self, query):
        """Verify document update queries reach correct classification."""
        pre_classifier = PreClassifier()
        intent = pre_classifier.pre_classify(query)
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "update_document"  # Or appropriate action
```

### 2.2 Handler Tests

**File**: `tests/unit/services/intent_service/test_document_query_handlers.py`

Tests required:
1. `test_update_document_not_configured` - graceful degradation
2. `test_update_document_not_found` - no matches
3. `test_update_document_multiple_matches` - clarification required
4. `test_update_document_success` - happy path
5. `test_update_document_parse_query` - query parsing

### 2.3 Test Count Target

| Category | Tests |
|----------|-------|
| Routing Integration | 5 |
| Handler Logic | 5 |
| **Total** | 10 |

---

## Phase 3: Verification Gates

- [ ] Phase 1: Handler added and compiles
- [ ] Phase 2: Routing integration tests pass
- [ ] Phase 2a: Handler unit tests pass
- [ ] Full suite: `pytest tests/unit/services/intent_service/ -v` passes
- [ ] No regressions

---

## Acceptance Criteria

- [ ] `_handle_update_document_notion()` handler implemented
- [ ] Pre-classifier patterns added for update queries
- [ ] Routing wired in `_process_query_intent()`
- [ ] 10+ tests added (routing + handler)
- [ ] All tests passing
- [ ] No regressions
- [ ] Graceful degradation when Notion not configured

---

## STOP Conditions

- Notion router `update_page()` signature different than expected → STOP
- Search returns different structure than Query #20 pattern → STOP
- Notion property format unclear → escalate

---

## Manual Testing Note

⚠️ **Blocker**: Same as other integration queries - needs Notion connection configured in setup UI. Document in issue for future testing.

---

## Estimated Effort

| Component           | Lines | Complexity |
| ------------------- | ----- | ---------- |
| Intent handler      | ~150  | Medium     |
| Query parsing       | ~30   | Low        |
| Pre-classifier      | ~10   | Low        |
| Intent routing      | ~5    | Low        |
| Tests               | ~200  | Medium     |
| **Total**           | ~395  | Medium     |

---

## Comparison to Issue #519 (GitHub Ops)

| Aspect | Issue #519 | Issue #522 |
|--------|------------|------------|
| Router exists | ✅ | ✅ |
| Method exists | ✅ (3 methods) | ✅ (2 methods) |
| Handler pattern | New handlers | Follow Query #20 pattern |
| POST capability | Added | Not needed |
| Name resolution | Issue number | Document search |

Issue #522 is simpler than #519 because:
1. All router methods exist
2. Search + update pattern already exists (Query #20)
3. No new adapter methods needed

---

**Status**: READY FOR APPROVAL

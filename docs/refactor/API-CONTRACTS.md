# API Contracts - Must Maintain During Refactoring

**Created**: 2025-11-03 16:32 PM PT
**Purpose**: Document API contracts that MUST remain backward compatible
**Context**: title → text field rename requires careful handling

---

## Executive Summary

**Critical Change**: Todo domain model changing from `.title` to `.text` (Item base property)

**API Impact**: TodoCreateRequest and TodoResponse currently use `title` field

**Backward Compatibility Strategy**: Support BOTH `title` and `text` during transition

---

## Current API Contracts

### Todo Creation Endpoint

**Endpoint**: `POST /api/v1/todos`

**Current Request Schema**:
```json
{
  "title": "string",              // REQUIRED - will rename to "text"
  "description": "string",         // optional
  "priority": "string",            // optional, default: "medium"
  "due_date": "datetime",          // optional
  "tags": ["string"],              // optional, default: []
  "list_id": "string",             // optional
  "assignee_id": "string",         // optional
  "metadata": {}                   // optional, default: {}
}
```

**Field Constraints**:
- `title`: min_length=1, max_length=200, REQUIRED
- `priority`: Values: "low", "medium", "high", "urgent"

**Current Response Schema**:
```json
{
  "id": "string",
  "title": "string",               // Will rename to "text"
  "description": "string",
  "priority": "string",
  "status": "string",              // "pending", "in_progress", "completed", "cancelled"
  "due_date": "datetime",
  "tags": ["string"],
  "list_id": "string",
  "assignee_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "completed_at": "datetime",
  "metadata": {}
}
```

---

### Todo Update Endpoint

**Endpoint**: `PUT /api/v1/todos/{todo_id}` or `PATCH /api/v1/todos/{todo_id}`

**Current Request Schema**:
```json
{
  "title": "string",               // Optional - will rename to "text"
  "description": "string",         // optional
  "priority": "string",            // optional
  "due_date": "datetime",          // optional
  "tags": ["string"],              // optional
  "status": "string",              // optional
  "assignee_id": "string",         // optional
  "metadata": {}                   // optional
}
```

**All fields optional** (partial update)

---

### Todo Retrieval Endpoint

**Endpoint**: `GET /api/v1/todos/{todo_id}`

**Response**: Same as TodoResponse above

---

### Todo List Endpoint

**Endpoint**: `GET /api/v1/todos`

**Query Parameters**:
- `status`: Filter by status
- `priority`: Filter by priority
- `assignee_id`: Filter by assignee
- `list_id`: Filter by list

**Response**:
```json
{
  "todos": [
    {
      // TodoResponse schema
    }
  ],
  "total": 0,
  "page": 1,
  "page_size": 50
}
```

---

### Todo Delete Endpoint

**Endpoint**: `DELETE /api/v1/todos/{todo_id}`

**Response**: 204 No Content (or success confirmation)

---

## Breaking Changes to Manage

### Primary Breaking Change: `title` → `text`

**Impact**:
1. **Request field rename**: Clients sending `{"title": "..."}` must work
2. **Response field rename**: Clients expecting `{"title": "..."}` must work
3. **Update requests**: Clients updating `title` field must work

**Mitigation Strategy**:

### Phase 2: Transition Period (Support Both)

**Request Handling** (in API layer):
```python
class TodoCreateRequest(BaseModel):
    # Accept BOTH fields
    title: Optional[str] = Field(None, description="DEPRECATED: Use 'text' instead")
    text: Optional[str] = Field(None, description="Todo text content")

    @validator('text', always=True)
    def set_text_from_title(cls, v, values):
        """Support legacy 'title' field during transition"""
        if v is None and 'title' in values and values['title']:
            return values['title']
        return v

    @root_validator
    def check_text_or_title(cls, values):
        """Ensure either text or title is provided"""
        if not values.get('text') and not values.get('title'):
            raise ValueError("Either 'text' or 'title' must be provided")
        return values
```

**Response Handling** (in API layer):
```python
class TodoResponse(BaseModel):
    text: str                        # NEW: Primary field
    title: Optional[str] = None      # DEPRECATED: Alias for backward compatibility

    @root_validator
    def set_title_alias(cls, values):
        """Provide 'title' alias for backward compatibility"""
        if 'text' in values and values['text']:
            values['title'] = values['text']
        return values
```

**Result**: Clients can use EITHER field, both work

### Phase 3: Deprecation Period

**Add deprecation warnings**:
```python
@deprecated(version="2.0", reason="Use 'text' field instead")
title: Optional[str] = None
```

**Document in API response**:
```json
{
  "_deprecation_warnings": [
    "Field 'title' is deprecated. Use 'text' instead. Support will be removed in v3.0"
  ],
  "text": "Buy milk",
  "title": "Buy milk"  // Still present but marked deprecated
}
```

### Phase 4: Final Transition (Future)

**Eventually remove `title` completely**:
- Major version bump (v2.0 → v3.0)
- Clear migration guide
- Only `text` field remains

---

## Backward Compatibility Strategy

### Recommended Approach: **Accept Both, Prefer Text**

**Advantages**:
- ✅ Zero breaking changes for existing clients
- ✅ New clients can use `text` immediately
- ✅ Clear migration path
- ✅ Can deprecate `title` gradually

**Implementation Timeline**:
1. **Phase 2** (Now): Support both fields
2. **Phase 2+1 month**: Add deprecation warnings
3. **Phase 2+3 months**: Document migration guide
4. **Phase 3 (v2.0)**: Remove `title` support

### Alternative Approaches Considered

**Option A**: Version the API (`/api/v1` vs `/api/v2`)
- ❌ More complex
- ❌ Maintains two codebases
- ✅ Clean separation

**Option B**: Use field aliasing in Pydantic
- ✅ Simple implementation
- ✅ Transparent to domain layer
- ❌ Less clear to API consumers

**Option C**: Accept both but only return `text`
- ❌ Breaking change for clients expecting `title` in response
- ❌ Inconsistent (accept title, return text)

**Decision**: Recommend primary approach (accept both, return both with deprecation)

---

## Testing Strategy for Compatibility

### Required Tests

**Test 1: Legacy client using `title`**:
```python
async def test_legacy_title_field_still_works():
    # Client sends old format
    response = await client.post("/api/v1/todos", json={
        "title": "Buy milk",  # Old field name
        "priority": "high"
    })

    assert response.status_code == 200
    assert response.json()["text"] == "Buy milk"      # New field
    assert response.json()["title"] == "Buy milk"     # Legacy alias
```

**Test 2: New client using `text`**:
```python
async def test_new_text_field_works():
    # Client sends new format
    response = await client.post("/api/v1/todos", json={
        "text": "Buy milk",   # New field name
        "priority": "high"
    })

    assert response.status_code == 200
    assert response.json()["text"] == "Buy milk"
```

**Test 3: Both fields provided (text takes precedence)**:
```python
async def test_text_takes_precedence_over_title():
    # Client sends both (shouldn't happen, but handle it)
    response = await client.post("/api/v1/todos", json={
        "title": "Old value",
        "text": "New value",
        "priority": "high"
    })

    assert response.status_code == 200
    assert response.json()["text"] == "New value"  # text wins
```

**Test 4: Update with legacy field**:
```python
async def test_update_with_legacy_title():
    # Update using old field name
    response = await client.put("/api/v1/todos/123", json={
        "title": "Updated title"
    })

    assert response.status_code == 200
    assert response.json()["text"] == "Updated title"
```

---

## Migration Guide for API Consumers

**Document for clients**:

```markdown
# Todo API Migration: title → text

## Change Summary
The `title` field is being renamed to `text` to align with universal Item primitive.

## Timeline
- **Now**: Both `title` and `text` fields supported
- **+1 month**: `title` field deprecated (warnings added)
- **+3 months**: Migration guide published
- **v2.0** (TBD): `title` field removed

## How to Migrate

### Before (using title):
```json
POST /api/v1/todos
{
  "title": "Buy milk",
  "priority": "high"
}
```

### After (using text):
```json
POST /api/v1/todos
{
  "text": "Buy milk",
  "priority": "high"
}
```

### Transition Period (both work):
```json
// Either field works:
{"title": "Buy milk"}  // ✓ Works (legacy)
{"text": "Buy milk"}   // ✓ Works (recommended)
```

## Response Changes
Responses now include BOTH fields (same value):
```json
{
  "text": "Buy milk",   // Primary field
  "title": "Buy milk"   // Deprecated alias
}
```

## Action Required
Update your code to use `text` instead of `title` at your convenience.
No immediate action required (backward compatible).
```

---

## Validation Requirements

**Before releasing Phase 2**:
- [ ] All 4 compatibility tests pass
- [ ] Legacy clients tested (if available)
- [ ] API documentation updated
- [ ] Migration guide published
- [ ] Deprecation warnings implemented
- [ ] Response includes both fields
- [ ] Request accepts both fields

---

## Notes

**Key Insight**: The refactoring is internal (domain model), API can remain compatible with careful handling.

**Success Metric**: Zero breaking changes for existing API consumers while enabling new functionality.

**Future**: This pattern can be reused for other field migrations (if needed).

---

*API contracts documented. Backward compatibility strategy defined.*

# Issue #282 Investigation Report: CORE-ALPHA-FILE-UPLOAD

**Date**: November 1, 2025, 8:40 AM PT
**Status**: Investigation Complete ✅
**Effort**: Small-Medium (2-4 hours)

---

## Executive Summary

**Finding**: File upload functionality is **95% complete but disconnected**. All infrastructure exists in the codebase but the FastAPI endpoint and frontend UI are missing. This is a textbook case of DDD refactoring breaking integration.

**Root Cause**: Past working implementation (`Jun 20, 2025` - commit `031a7850`) had:
- ✅ Backend endpoint: `@app.post("/api/v1/knowledge/upload")`
- ✅ Frontend UI: Upload form with progress tracking
- ✅ Integration: DocumentService.upload_pdf()

Current state has all the pieces but **the glue is missing**:
- ✅ Database model: `UploadedFileDB` (proper schema)
- ✅ Storage service: `save_file_to_storage()` (complete)
- ✅ Document service: `DocumentService.upload_pdf()` (complete)
- ❌ **FastAPI endpoint**: MISSING
- ❌ **Frontend component**: MISSING

---

## Archaeological Findings

### Past Working Implementation (Jun 20-24, 2025)

**Commits showing working upload**:
- `031a7850` - PM-011: Implement basic web chat interface with file upload
- `14948675` - Fix: File upload working - corrected endpoint URLs
- `0d2dc9ea` - feat: Complete file upload and analysis slice working
- `6861995b` - feat: Complete PM-011 file analysis slice working end-to-end

**Working Endpoint**:
```python
@app.post("/api/v1/knowledge/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    source_type: Optional[str] = Form("reference"),
    knowledge_domain: Optional[str] = Form("pm_fundamentals")
):
    # Validate knowledge domain
    # Use document_service.upload_pdf()
    # Emit event to learning system
    # Return metadata
```

**Working Frontend**:
```javascript
const response = await fetch(`${API_BASE_URL}/api/v1/knowledge/upload`, {
    method: 'POST',
    body: formData,
    credentials: 'include'
});
```

---

## Current State Analysis

### ✅ What EXISTS - Ready to Use

#### 1. Database Model (`services/database/models.py`)
```python
class UploadedFileDB(Base):
    __tablename__ = "uploaded_files"
    id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    filename = Column(String(500), nullable=False)
    file_type = Column(String(255))
    file_size = Column(Integer)
    storage_path = Column(String(1000))
    upload_time = Column(DateTime, default=datetime.utcnow)
    last_referenced = Column(DateTime, nullable=True)
    reference_count = Column(Integer, default=0)
    file_metadata = Column(JSON, default=dict)
    item_metadata = Column(JSON, default=dict)
```
**Status**: ✅ Complete, has proper indexes, converts to domain model

#### 2. Storage Service (`services/file_context/storage.py`)
```python
async def save_file_to_storage(
    file: Union[UploadFile, bytes],
    filename: Optional[str] = None
) -> str
```
**Status**: ✅ Complete, handles both UploadFile and bytes

Functions available:
- `save_file_to_storage()` - saves and returns path
- `delete_file_from_storage()` - deletes file
- `get_file_size()` - gets file size
- `generate_session_id()` - generates session IDs

#### 3. Document Service (`services/knowledge_graph/document_service.py`)
```python
class DocumentService:
    async def upload_pdf(self, file: UploadFile, metadata: Dict) -> Dict
```
**Status**: ✅ Complete, validates file type, uses ingester

Functions available:
- `upload_pdf()` - handles PDF upload with metadata
- `find_decisions()` - search uploaded documents
- Other knowledge base operations

#### 4. File Infrastructure
```
uploads/                          # ✅ Exists (empty)
services/file_context/
  ├── storage.py                  # ✅ Complete
  ├── file_resolver.py            # ✅ Resolves file references
  └── ... (other file services)
services/database/models.py       # ✅ UploadedFileDB model
services/knowledge_graph/
  └── document_service.py         # ✅ DocumentService
```

---

### ❌ What's MISSING - Need to Build

#### 1. FastAPI Endpoint in `main.py`
- No `/upload` endpoint
- No `/api/v1/files/upload` endpoint
- No `/api/v1/knowledge/upload` endpoint

**What we need**:
```python
@app.post("/upload")  # Simple endpoint matching current architecture
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_auth)  # From Issue #281
) -> dict
```

#### 2. Frontend Upload UI in `web/app.py`
- No upload section in HTML
- No upload JavaScript
- No progress indication
- No success/error messages

**What we need**:
- File input element
- Upload button
- Progress bar
- Status messages (success/error)
- File type validation on client

#### 3. User Isolation in Storage
- Current `save_file_to_storage()` doesn't use session_id/user_id
- Need to update storage function OR create wrapper

**Current behavior**:
```python
# Current: save_file_to_storage(file, filename)
# Saves to: uploads/20251101_123456_filename.txt
# Problem: Mixed for all users!

# Needed: User-isolated paths
# uploads/user_id_or_session/20251101_123456_filename.txt
```

---

## Implementation Strategy

### Phase 1: Backend Endpoint (1.5 hours)
**Goal**: Create `/upload` endpoint in `main.py`

**Approach**:
1. Add import: `from fastapi import UploadFile, File, Depends, HTTPException`
2. Create endpoint:
   - Validate file (size, type)
   - Get current user from auth (use stub if #281 not done)
   - Create user upload directory
   - Save file via `save_file_to_storage()`
   - Store metadata in database (UploadedFileDB)
   - Return file_id + metadata

**Dependencies**:
- Needs `require_auth` from Issue #281
- **Fallback**: Create stub that returns `{"user_id": "demo"}`

### Phase 2: Frontend Component (1 hour)
**Goal**: Add upload UI to `web/app.py` HTML

**Approach**:
1. Add HTML form with file input
2. Add CSS for styling (dashed border, progress bar)
3. Add JavaScript handler:
   - Validate file on client
   - Send POST to `/upload`
   - Show progress
   - Display success/error

### Phase 3: Testing (1 hour)
**Goal**: Verify end-to-end functionality

**Test cases**:
1. File size validation (reject >10MB)
2. File type validation (allow txt, pdf, docx, md, json)
3. User isolation (different users see different files)
4. Progress indication works
5. Error messages are helpful

### Phase 4: Cleanup (30 min)
**Goal**: Ensure code quality

- Remove test files
- Update comments
- Run linter
- Commit and push

---

## DDD Violation Assessment

**What violated DDD** (in past implementation):
- Mixed concern: upload endpoint + PDF processing + knowledge ingestion
- Tight coupling to DocumentService

**How to fix** (recommended approach):
- Keep endpoint simple: just save file + metadata
- Let DocumentService handle complex processing (async later)
- Separate concerns: upload vs. processing

**Recommendation**:
```python
# Endpoint does: Save uploaded file
@app.post("/upload")
async def upload_file(file: UploadFile, user: dict) -> dict:
    # Just save the file and metadata
    # Return file_id
    # Don't process yet

# Later: Async job processes file
# document_service.process_file(file_id)
```

---

## Success Criteria

- [ ] `/upload` endpoint exists and handles POST requests
- [ ] File size limits enforced (10MB max)
- [ ] File type validation working
- [ ] Files saved in user-isolated directories
- [ ] Frontend upload component functional
- [ ] Progress indication displayed
- [ ] Error messages are helpful and clear
- [ ] Database records created for uploads
- [ ] All tests pass
- [ ] Code committed and pushed

---

## Risk Assessment

**Low Risk**: All infrastructure exists, just needs to be wired together

**Potential Issues**:
1. Auth dependency (#281) not complete
   - **Mitigation**: Use auth stub for testing
2. Database session management
   - **Mitigation**: Use existing db patterns in codebase
3. File path isolation
   - **Mitigation**: Use user_id from session

---

## Next Steps

1. ✅ Investigation complete
2. → Phase 1: Create backend endpoint (next)
3. → Phase 2: Create frontend component
4. → Phase 3: Test end-to-end
5. → Phase 4: Commit and push

---

**Investigation Status**: COMPLETE ✅
**Ready to Proceed**: YES ✅

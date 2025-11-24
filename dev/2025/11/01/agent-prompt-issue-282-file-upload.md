# Claude Code Prompt: CORE-ALPHA-FILE-UPLOAD (#282)

**Date**: November 1, 2025, 7:00 AM PT
**Mission**: Fix file upload functionality for document processing
**Effort**: Small-Medium (2-4 hours)
**GitHub Issue**: #282
**Depends On**: Issue #281 (auth) for `require_auth` dependency

---

## Your Identity

You are Claude Code, investigating and fixing broken file upload functionality. Follow systematic discovery and provide evidence.

---

## CRITICAL FIRST ACTION: Use Serena MCP

**Investigate current state with Serena**:

```python
# Find upload-related code
serena.find_symbol("upload")
serena.find_symbol("UploadFile")
serena.find_referencing_symbols("upload")

# Check web routes
serena.view_file("web/app.py")

# Check frontend
serena.list_dir("web/static")
serena.view_file("web/static/index.html")

# Check for document service
serena.find_symbol("DocumentService")
serena.find_symbol("document_processor")
```

**Report your findings** before starting work.

---

## Cathedral Context

**Read this gameplan section for full context**:
- `/mnt/user-data/uploads/gameplan-p0-alpha-blockers-v2.md` (Issue #2 section)

**The Problem**:
File upload is completely broken - users can't upload documents for analysis. This blocks core PM workflows.

**The Solution**:
1. Investigate what exists vs what's missing
2. Fix or create upload endpoint with validation
3. Fix or create frontend upload component
4. Implement user-isolated file storage
5. Connect to document processor
6. Test end-to-end

---

## Mission

Fix file upload functionality to enable users to upload documents (text, PDF, Word, etc.) for analysis and processing, with proper security validation and user isolation.

---

## Phase -1: Investigation (30 minutes)

### Questions to Answer

Use Serena and filesystem exploration:

1. **Does `/upload` endpoint exist?**
   ```python
   serena.find_symbol("upload_file")
   serena.view_file("web/app.py")
   # Look for @app.post("/upload")
   ```

2. **Is frontend component wired up?**
   ```bash
   grep -r "upload" web/static/index.html
   grep -r "fileInput" web/static/
   ```

3. **Does upload directory exist?**
   ```bash
   ls -la uploads/ 2>/dev/null || echo "uploads/ does not exist"
   ```

4. **Is document service available?**
   ```python
   serena.find_symbol("DocumentService")
   ```

**Create investigation report** before proceeding.

Example format:
```
Investigation Results:
1. /upload endpoint: [EXISTS / MISSING / BROKEN]
2. Frontend component: [EXISTS / MISSING / BROKEN]
3. Upload directory: [EXISTS / MISSING]
4. Document service: [EXISTS / MISSING]

Root Cause: [Your assessment]
Fix Strategy: [Your plan]
```

---

## Implementation Plan

### Phase 0: Create Upload Infrastructure (20 minutes)

**If upload directory missing**:
```bash
mkdir -p uploads
echo "*" > uploads/.gitignore  # Don't commit uploads
echo "!.gitignore" >> uploads/.gitignore
```

**If document service missing**, create basic version:
```python
# services/document_service.py
class DocumentService:
    def __init__(self, db_session):
        self.db = db_session

    async def store_document_metadata(
        self,
        user_id: str,
        file_id: str,
        filename: str,
        path: str,
        content_type: str,
        size: int
    ) -> str:
        """Store document metadata - implement based on your models"""
        # TODO: Implement based on actual UploadedFile model
        pass

    async def index_document(
        self,
        document_id: str,
        content: str
    ):
        """Index document for search - basic implementation"""
        # TODO: Implement based on actual knowledge base
        pass
```

### Phase 1: Backend Endpoint (1.5 hours)

**Create or fix `/upload` endpoint in `web/app.py`**:

```python
from fastapi import UploadFile, File, HTTPException, Depends
from web.middleware.auth import require_auth  # From Issue #281
import aiofiles
import uuid
from pathlib import Path

# Ensure upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_auth)
):
    """
    Handle file upload with validation and user isolation.

    Security:
    - Max 10MB file size
    - Allowed types: text, PDF, Word, Markdown, JSON
    - User-isolated storage
    - Proper error handling
    """
    # 1. Read and validate file
    file_content = await file.read()

    # Size check
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    if len(file_content) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large: {len(file_content)} bytes (max {MAX_SIZE})"
        )

    # Type check
    ALLOWED_TYPES = {
        'text/plain',
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/markdown',
        'application/json'
    }

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}"
        )

    # 2. Save with user isolation
    file_id = str(uuid.uuid4())
    user_dir = UPLOAD_DIR / current_user['user_id']
    user_dir.mkdir(exist_ok=True)

    file_path = user_dir / f"{file_id}_{file.filename}"

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)

    # 3. Store metadata (adapt to your models)
    try:
        from services.document_service import DocumentService
        doc_service = DocumentService(db)  # Get db from dependency

        doc_id = await doc_service.store_document_metadata(
            user_id=current_user['user_id'],
            file_id=file_id,
            filename=file.filename,
            path=str(file_path),
            content_type=file.content_type,
            size=len(file_content)
        )
    except Exception as e:
        # If metadata storage fails, still return success
        # But log the error
        print(f"Warning: Failed to store metadata: {e}")
        doc_id = file_id

    # 4. Process text files
    indexed = False
    if file.content_type == 'text/plain':
        try:
            text_content = file_content.decode('utf-8')
            await doc_service.index_document(
                document_id=doc_id,
                content=text_content
            )
            indexed = True
        except Exception as e:
            print(f"Warning: Failed to index document: {e}")

    return {
        "file_id": file_id,
        "document_id": doc_id,
        "filename": file.filename,
        "size": len(file_content),
        "content_type": file.content_type,
        "status": "uploaded",
        "indexed": indexed
    }
```

**Evidence Required**:
- Show endpoint added to web/app.py
- Show line numbers where it was added
- Test with curl (provide command + output)

### Phase 2: Frontend Component (1 hour)

**Add upload section to `web/static/index.html`**:

Find appropriate location in HTML (after chat interface) and add:

```html
<!-- File Upload Section -->
<div class="upload-section">
    <h3>📎 Upload Document</h3>
    <div class="upload-controls">
        <input
            type="file"
            id="fileInput"
            accept=".txt,.pdf,.docx,.md,.json"
            class="file-input"
        >
        <button onclick="uploadFile()" class="btn-upload">
            Upload
        </button>
    </div>
    <div id="uploadStatus" class="upload-status"></div>
    <div id="uploadProgress" class="progress-bar" style="display: none;">
        <div id="progressFill" class="progress-fill"></div>
    </div>
</div>

<style>
.upload-section {
    margin: 20px 0;
    padding: 20px;
    border: 2px dashed #ccc;
    border-radius: 8px;
    background: #fafafa;
}

.upload-controls {
    display: flex;
    gap: 10px;
    align-items: center;
}

.file-input {
    flex: 1;
    padding: 8px;
}

.btn-upload {
    padding: 10px 20px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn-upload:hover {
    background: #45a049;
}

.upload-status {
    margin-top: 10px;
    padding: 10px;
    border-radius: 4px;
}

.status-success {
    background: #d4edda;
    color: #155724;
}

.status-error {
    background: #f8d7da;
    color: #721c24;
}

.progress-bar {
    width: 100%;
    height: 20px;
    background: #f0f0f0;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #8BC34A);
    width: 0%;
    transition: width 0.3s ease;
}
</style>

<script>
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        showUploadStatus('Please select a file', 'error');
        return;
    }

    const statusDiv = document.getElementById('uploadStatus');
    const progressDiv = document.getElementById('uploadProgress');
    const progressFill = document.getElementById('progressFill');

    // Show progress
    statusDiv.textContent = 'Uploading...';
    statusDiv.className = 'upload-status';
    progressDiv.style.display = 'block';
    progressFill.style.width = '0%';

    const formData = new FormData();
    formData.append('file', file);

    try {
        // Simulate progress
        progressFill.style.width = '30%';

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
            credentials: 'include'  // Include auth cookie
        });

        progressFill.style.width = '100%';

        if (response.ok) {
            const result = await response.json();
            showUploadStatus(
                `✅ Uploaded: ${result.filename} (${formatBytes(result.size)})`,
                'success'
            );

            // Clear input
            fileInput.value = '';

            // Hide progress after delay
            setTimeout(() => {
                progressDiv.style.display = 'none';
                progressFill.style.width = '0%';
            }, 2000);
        } else {
            const error = await response.json();
            showUploadStatus(error.detail || 'Upload failed', 'error');
            progressDiv.style.display = 'none';
        }
    } catch (error) {
        console.error('Upload error:', error);
        showUploadStatus('Upload failed - please try again', 'error');
        progressDiv.style.display = 'none';
    }
}

function showUploadStatus(message, type) {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.textContent = message;
    statusDiv.className = `upload-status status-${type}`;
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
</script>
```

**Evidence Required**:
- Show where you added the HTML section
- Show line numbers
- Describe how it integrates with existing UI

---

## Testing (1 hour)

### Test 1: Backend endpoint with curl
```bash
# Create test file
echo "Test document content" > test.txt

# Upload (replace TOKEN with actual JWT)
curl -X POST http://localhost:8001/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@test.txt"

# Expected: JSON response with file_id
```

### Test 2: File size validation
```bash
# Create large file
dd if=/dev/zero of=large.txt bs=1M count=20

# Try upload (should reject)
curl -X POST http://localhost:8001/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@large.txt"

# Expected: 413 File too large
```

### Test 3: File type validation
```bash
# Create executable (not allowed)
echo "#!/bin/bash" > test.sh

# Try upload (should reject)
curl -X POST http://localhost:8001/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@test.sh"

# Expected: 415 Unsupported file type
```

### Test 4: Web UI
```
1. Open browser to http://localhost:8001
2. Login (if auth is working)
3. Find upload section
4. Select test.txt file
5. Click Upload button
6. Verify success message appears
7. Check uploads/[user_id]/ directory has file
```

### Test 5: User isolation
```bash
# Login as user 1, upload file
# Login as user 2 (different browser)
# Verify user 2 can't see user 1's files

ls -R uploads/
# Should show separate directories per user
```

---

## Success Criteria

**Check all before claiming complete**:
- [ ] `/upload` endpoint exists and works
- [ ] File size limits enforced (10MB)
- [ ] File type validation works
- [ ] Files saved in user-isolated directories
- [ ] Frontend upload component functional
- [ ] Progress indication works
- [ ] Error messages are helpful
- [ ] Files can be referenced (if document service exists)
- [ ] All tests pass
- [ ] Changes committed to git

---

## Evidence Format

**Provide**:

1. **Files Modified/Created**:
   ```
   web/app.py: +X lines (upload endpoint)
   web/static/index.html: +Y lines (upload UI)
   services/document_service.py: Created/Modified
   ```

2. **Test Results**:
   - All 5 tests with full terminal output
   - Screenshots of web UI working (optional but nice)

3. **File Structure**:
   ```bash
   ls -R uploads/
   ```

4. **Git Status**:
   ```bash
   git status
   git log --oneline -2
   ```

---

## Dependency Note

This issue depends on Issue #281 (auth) for the `require_auth` middleware. If auth isn't done yet:

**Option A**: Wait for auth to complete
**Option B**: Create temporary stub:
```python
async def require_auth_stub():
    return {"user_id": "test-user", "username": "test"}
```

Use stub for testing, replace with real auth later.

---

## Questions for PM (if needed)

- If document service doesn't exist, should I create basic version or skip indexing?
- If upload directory should be elsewhere (not `uploads/`)?
- If additional file types should be supported?
- If there's existing file storage infrastructure I should use?

---

Good luck! This should be straightforward - mostly plumbing to connect upload to storage. The hard part is making sure security validation is solid.

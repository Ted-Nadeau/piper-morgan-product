# Code Agent Prompt: UI Quick Fixes - Phase 4 Implementation

**Date**: November 23, 2025, 4:47 PM
**Estimated Duration**: 50-65 minutes
**Phase**: Implementation (all 3 issues from Phase 3)

---

## Your Mission

Implement fixes for all 3 Phase 3 issues:
1. **Issue #4**: Quick fix (2-5 min) - Standup proxy endpoint
2. **Issue #13**: Quick fix (2-3 min) - Integrations page route
3. **Issue #8**: Build Files UI (45-60 min) - Frontend for complete backend

**Order**: #4 → #13 → #8 (quick wins first, then substantial work)

---

## Context From Phase 3 Investigation

### Issue #4: Standup Button Hangs
- **Root Cause**: Proxy calls itself instead of backend, creates infinite loop
- **Fix Location**: web/app.py:901-902
- **What to Change**:
  - Line 901: `client.get(` → `client.post(`
  - Line 902: `f"{API_BASE_URL}/api/standup"` → `f"{API_BASE_URL}/api/v1/standup/generate"`

### Issue #13: Integrations Page 404
- **Root Cause**: Settings card links to `/settings/integrations` but no route exists
- **Fix Needed**: Create route handler + template with "coming soon" placeholder
- **Pattern**: Copy from files.html, advanced-settings.html

### Issue #8: Files UI Missing
- **Backend Status**: 100% complete - POST /upload, GET /list, DELETE /id all working
- **Frontend Status**: 0% - just placeholder page
- **Pattern Reuse**: Copy from Lists/Todos/Projects pages built today (Option B)
- **Endpoints Ready**:
  - POST `/api/v1/files/upload` - Upload with validation
  - GET `/api/v1/files/list` - List user's files
  - DELETE `/api/v1/files/{file_id}` - Delete files

---

## MANDATORY EXECUTION ORDER

### Step 1: Issue #4 - Standup Proxy Fix (2-5 min)

**File**: `web/app.py`

**Current Code** (lines 901-902):
```python
async with httpx.AsyncClient(timeout=timeout) as client:
    response = await client.get(
        f"{API_BASE_URL}/api/standup",
        headers={"Authorization": f"Bearer {token}"}
    )
```

**Change to**:
```python
async with httpx.AsyncClient(timeout=timeout) as client:
    response = await client.post(  # CHANGED: get → post
        f"{API_BASE_URL}/api/v1/standup/generate",  # CHANGED: /api/standup → /api/v1/standup/generate
        headers={"Authorization": f"Bearer {token}"}
    )
```

**Testing**:
1. Navigate to http://localhost:8001/standup
2. Click "Generate Standup" button
3. Should complete within 2-3 seconds (not hang forever)
4. Should return standup data

**Commit Message**:
```
fix(#379): Correct standup proxy endpoint and HTTP method

- Change proxy from GET /api/standup to POST /api/v1/standup/generate
- Fixes infinite loop causing button to hang
- Issue #4 investigation: web/app.py:901-902
```

---

### Step 2: Issue #13 - Integrations Page Route (2-3 min)

**A. Create Template** - `templates/integrations.html`

```html
{% extends "layout.html" %}

{% block content %}
<div class="coming-soon-container">
  <div class="coming-soon-icon">🔗</div>
  <h1>Integrations</h1>
  <p class="coming-soon-description">
    Connect and manage your integrations with Slack, GitHub, Notion, Calendar, and more.
    Full integration management UI coming soon!
  </p>
  <p class="coming-soon-hint">
    Current integrations can be configured via the conversational interface.
  </p>
  <a href="/settings" class="back-link">← Back to Settings</a>
</div>
{% endblock %}
```

**B. Add Route Handler** - `web/app.py` (add after line 1027)

```python
@app.get("/settings/integrations", response_class=HTMLResponse)
async def integrations_page(request: Request):
    """Integrations management page - Coming soon"""
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "integrations.html",
        {"request": request, "user": user_context}
    )
```

**Testing**:
1. Navigate to http://localhost:8001/settings
2. Click "Integrations" card (should not be disabled anymore)
3. Should show "coming soon" page (not 404)

**Commit Message**:
```
fix(#379): Add integrations page route handler

- Create templates/integrations.html with "coming soon" placeholder
- Add GET /settings/integrations route handler
- Prevents 404 error when clicking Integrations card
- Issue #13 investigation: settings-index.html:212
```

---

### Step 3: Issue #8 - Files UI Implementation (45-60 min)

**Pattern Reuse Strategy**:
- Copy structure from `templates/lists.html` (built today in Option B)
- Replace "list" with "file" throughout
- Use existing dialog.js and toast.js utilities
- Follow same permission-aware button pattern

**A. Replace templates/files.html**

```html
{% extends "layout.html" %}

{% block content %}
<script src="/static/js/permissions.js"></script>
<script src="/static/js/dialog.js"></script>
<script src="/static/js/toast.js"></script>

<div class="page-container">
  <div class="page-header">
    <h1>📄 Files</h1>
    <button id="uploadFileBtn" class="btn btn-primary">
      Upload File
    </button>
  </div>

  <div id="filesContainer" class="resource-list">
    <!-- Files will be rendered here -->
  </div>

  <div id="emptyState" class="empty-state" style="display: none;">
    <div class="empty-state-icon">📄</div>
    <h2>No Files Yet</h2>
    <p>Upload your first file to get started</p>
    <button class="btn btn-primary" onclick="document.getElementById('uploadFileBtn').click()">
      Upload File
    </button>
  </div>
</div>

<script>
window.currentUser = {
  username: "{{ user.username }}",
  user_id: "{{ user.user_id }}",
  is_admin: {{ 'true' if user.is_admin else 'false' }}
};

// Load files on page load
document.addEventListener('DOMContentLoaded', loadFiles);

async function loadFiles() {
  try {
    const response = await fetch('/api/v1/files/list');
    if (!response.ok) throw new Error('Failed to fetch files');

    const files = await response.json();
    renderFiles(files);
  } catch (error) {
    console.error('Error loading files:', error);
    showToast('Failed to load files', 'error');
  }
}

function renderFiles(files) {
  const container = document.getElementById('filesContainer');
  const emptyState = document.getElementById('emptyState');

  if (!files || files.length === 0) {
    container.style.display = 'none';
    emptyState.style.display = 'block';
    return;
  }

  container.style.display = 'grid';
  emptyState.style.display = 'none';

  container.innerHTML = files.map(file => `
    <div class="resource-card" data-file-id="${file.id}">
      <div class="resource-header">
        <h3 class="resource-title">${escapeHtml(file.filename)}</h3>
        <div class="resource-actions">
          <button class="btn-icon" onclick="downloadFile('${file.id}')" title="Download">
            ⬇️
          </button>
          ${canDeleteFile(file) ? `
            <button class="btn-icon btn-danger" onclick="deleteFile('${file.id}')" title="Delete">
              🗑️
            </button>
          ` : ''}
        </div>
      </div>
      <div class="resource-metadata">
        <span class="metadata-item">📦 ${formatFileSize(file.file_size)}</span>
        <span class="metadata-item">📅 ${formatDate(file.uploaded_at)}</span>
        <span class="metadata-item">📋 ${file.content_type}</span>
      </div>
      ${file.owner_id !== window.currentUser.user_id ? `
        <div class="resource-owner">
          Uploaded by: ${file.owner_id}
        </div>
      ` : ''}
    </div>
  `).join('');
}

// Permission check: Only owner or admin can delete
function canDeleteFile(file) {
  if (!window.currentUser) return false;
  if (window.currentUser.is_admin) return true;
  return file.owner_id === window.currentUser.user_id;
}

// Upload file dialog
document.getElementById('uploadFileBtn').addEventListener('click', () => {
  showDialog({
    title: 'Upload File',
    content: `
      <form id="uploadFileForm">
        <div class="form-group">
          <label for="fileInput">Select File</label>
          <input type="file" id="fileInput" name="file" required
                 accept=".txt,.pdf,.doc,.docx,.md,.json">
          <small class="form-hint">Max size: 10MB. Allowed: Text, PDF, Word, Markdown, JSON</small>
        </div>
      </form>
    `,
    confirmText: 'Upload',
    onConfirm: uploadFile
  });
});

async function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];

  if (!file) {
    showToast('Please select a file', 'error');
    return;
  }

  // Validate file size (10MB)
  if (file.size > 10 * 1024 * 1024) {
    showToast('File too large. Max size: 10MB', 'error');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/v1/files/upload', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    showToast('File uploaded successfully', 'success');
    closeDialog();
    loadFiles(); // Reload file list
  } catch (error) {
    console.error('Upload error:', error);
    showToast(error.message || 'Failed to upload file', 'error');
  }
}

async function downloadFile(fileId) {
  try {
    const response = await fetch(`/api/v1/files/${fileId}`);
    if (!response.ok) throw new Error('Download failed');

    const fileData = await response.json();
    // Construct download URL
    window.location.href = `/api/v1/files/${fileId}/download`;
  } catch (error) {
    console.error('Download error:', error);
    showToast('Failed to download file', 'error');
  }
}

async function deleteFile(fileId) {
  showDialog({
    title: 'Delete File',
    content: '<p>Are you sure you want to delete this file? This action cannot be undone.</p>',
    confirmText: 'Delete',
    confirmClass: 'btn-danger',
    onConfirm: async () => {
      try {
        const response = await fetch(`/api/v1/files/${fileId}`, {
          method: 'DELETE'
        });

        if (!response.ok) throw new Error('Delete failed');

        showToast('File deleted successfully', 'success');
        closeDialog();
        loadFiles(); // Reload file list
      } catch (error) {
        console.error('Delete error:', error);
        showToast('Failed to delete file', 'error');
      }
    }
  });
}

// Utility functions
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}
</script>
{% endblock %}
```

**B. Add Download Endpoint** (if not already exists)

Check if `GET /api/v1/files/{file_id}/download` exists in web/api/routes/files.py.

If missing, add:
```python
@router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    request: Request,
    session: AsyncSession = Depends(get_db_session)
):
    """Download file content"""
    user_id = request.state.user_id
    is_admin = getattr(request.state, "is_admin", False)

    # Get file metadata
    result = await session.execute(
        select(UploadedFileDB).where(UploadedFileDB.id == file_id)
    )
    file_record = result.scalar_one_or_none()

    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Check ownership
    if not is_admin and file_record.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to download this file")

    # Construct file path
    file_path = Path("uploads") / file_record.owner_id / file_record.filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=file_path,
        filename=file_record.filename,
        media_type=file_record.content_type
    )
```

**Testing**:
1. Navigate to http://localhost:8001/files
2. Click "Upload File" button
3. Select a file (< 10MB, allowed type)
4. Verify file appears in list
5. Click download icon - file downloads
6. Click delete icon - confirmation dialog, then file deleted
7. Verify empty state shows when no files

**Commit Message**:
```
feat(#379): Build Files UI with upload/list/delete functionality

- Replace templates/files.html placeholder with full file management UI
- Add file upload form with drag-and-drop support
- Add file list display with metadata (filename, size, date, type)
- Add download and delete functionality
- Integrate with existing backend API (POST /upload, GET /list, DELETE)
- Follow permission-aware pattern from Lists/Todos/Projects
- Use existing dialog.js and toast.js utilities
- Issue #8 investigation: Backend 100% ready, frontend was deferred

Backend endpoints used:
- POST /api/v1/files/upload
- GET /api/v1/files/list
- GET /api/v1/files/{id}
- DELETE /api/v1/files/{id}
```

---

## Pre-commit Hook Compliance

**BEFORE EVERY COMMIT**:
```bash
# Fix newlines
./scripts/fix-newlines.sh

# Then commit
git add .
git commit -m "your message"
```

---

## Testing Checklist

### Issue #4 Testing
- [ ] Navigate to /standup
- [ ] Click "Generate Standup" button
- [ ] Completes within 2-3 seconds (not hanging)
- [ ] Returns standup data
- [ ] No console errors

### Issue #13 Testing
- [ ] Navigate to /settings
- [ ] Click "Integrations" card
- [ ] Shows "coming soon" page (not 404)
- [ ] Back link returns to /settings
- [ ] No console errors

### Issue #8 Testing
- [ ] Navigate to /files
- [ ] See empty state if no files
- [ ] Click "Upload File" button
- [ ] Upload form appears with file input
- [ ] Select valid file (< 10MB)
- [ ] Click "Upload" button
- [ ] File appears in list with metadata
- [ ] Click download icon - file downloads
- [ ] Click delete icon - confirmation appears
- [ ] Confirm delete - file removed from list
- [ ] No console errors
- [ ] Network tab shows 200 responses

### Permission Testing (Issue #8)
- [ ] Admin can delete any file
- [ ] Owner can delete their own files
- [ ] Non-owner cannot see delete button for others' files

---

## Success Criteria

**All Three Issues Complete When**:
1. ✅ All commits pushed to feature branch
2. ✅ All pre-commit hooks passed
3. ✅ Manual testing completed (all checkboxes above)
4. ✅ No console errors
5. ✅ No regressions in other features

---

## Validation Protocol

### After Each Fix
1. Test the specific feature
2. Check browser console for errors
3. Verify Network tab shows expected requests
4. Run pre-commit checks
5. Commit with proper message

### After All Fixes
1. Test all three features end-to-end
2. Verify no regressions in Phase 2 fixes (#6, #7, #14)
3. Check that permission system still works
4. Create completion report

---

## Completion Report Template

Save as: `dev/2025/11/23/phase-4-completion-report.md`

```markdown
# Phase 4 Implementation Report

**Date**: November 23, 2025
**Duration**: [start time] - [end time] = [X minutes]
**Status**: ✅ Complete

## Fixes Implemented

### Issue #4: Standup Proxy Fix
- **Commit**: [hash]
- **Changes**: web/app.py:901-902
- **Testing**: ✅ Button completes within 2-3 seconds
- **Evidence**: [paste browser console or response]

### Issue #13: Integrations Page Route
- **Commit**: [hash]
- **Changes**: templates/integrations.html (new), web/app.py (route)
- **Testing**: ✅ No more 404 errors
- **Evidence**: [screenshot or response]

### Issue #8: Files UI Implementation
- **Commit**: [hash]
- **Changes**: templates/files.html (replaced), web/api/routes/files.py (download endpoint if added)
- **Testing**: ✅ Upload/list/download/delete all working
- **Evidence**:
  - Uploaded test file successfully
  - File list displays correctly
  - Download works
  - Delete works with confirmation

## Total Time

- Issue #4: [X minutes]
- Issue #13: [X minutes]
- Issue #8: [X minutes]
- **Total**: [X minutes] (vs 50-65 min estimate)

## Pattern Reuse Success

Files UI reused patterns from:
- Lists/Todos/Projects structure (Option B)
- dialog.js and toast.js utilities
- Permission-aware button pattern
- Empty state pattern

Result: [X]% time savings vs building from scratch

## Pre-commit Status

- ✅ All commits passed pre-commit hooks
- ✅ ./scripts/fix-newlines.sh run before each commit
- ✅ No linting errors

## Commits

1. [hash] - fix(#379): Correct standup proxy endpoint
2. [hash] - fix(#379): Add integrations page route
3. [hash] - feat(#379): Build Files UI

## Next Steps

- PM manual testing validation
- Update Issue #379 with completion evidence
- Decide on remaining medium/low priority issues
```

---

## STOP Conditions

**STOP immediately if**:
- Pre-commit hooks fail
- Any test fails
- File upload backend missing download endpoint and you can't add it
- Console errors during testing
- Permission checks don't work

**When stopped**: Document the issue, commit what's working, report to PM

---

**Remember**:
- Implement in order: #4 → #13 → #8
- Test after EACH fix
- Run ./scripts/fix-newlines.sh before EACH commit
- Pattern reuse from today's Lists/Todos/Projects work
- Backend is 100% ready for Issue #8
- Michelle's alpha is tomorrow - this unlocks file upload testing!

---

*Prompt prepared by: Lead Developer*
*Date: November 23, 2025, 4:47 PM*
*Based on Phase 3 investigation findings*
*Backend API ready, just needs frontend wiring*

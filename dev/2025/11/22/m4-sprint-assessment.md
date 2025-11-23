# M4 Sprint Assessment - November 22, 2025

**Date**: 1:09 PM
**Sprint**: M4 (Convergence - Week 5-6)
**Issues**: #302, #313, #314, #355
**Assessment**: HAIRY - Multiple interdependencies, foundational work required

---

## Quick Summary

All four M4 issues have significant complexity and **multiple interdependencies**:

| Issue | Title | Size | Status | Ripeness | Risk |
|-------|-------|------|--------|----------|------|
| **#302** | CONV-MCP-DOCS | Large | Open | ⚠️ Medium (3/10) | High - Depends on #313, skill framework |
| **#313** | CONV-UX-DOCS | Large | Open | ⚠️ Low (2/10) | High - UI complex, no existing components |
| **#314** | CONV-UX-PERSIST | Medium | Open | ⚠️ Low (2/10) | High - DB schema, cross-channel sync |
| **#355** | DOCS-STOPGAP | Medium | Open | ✅ Medium (5/10) | Medium - Quick win, but blocks #313 |

**Recommendation**: All are "hairy" as expected. No quick wins. Choose based on strategic priority, not ripeness.

---

## Issue #302: CONV-MCP-DOCS (Document Analysis Skill)

### Overview
Create `DocumentAnalysisSkill` - unified document processing with 90%+ token reduction.

### Current State
- ✅ File upload infrastructure exists (`web/api/routes/files.py`)
- ✅ File repository exists (`services/repositories/file_repository.py`)
- ✅ Document analyzer exists (`services/analysis/document_analyzer.py`)
- ❌ DocumentAnalysisSkill doesn't exist
- ❌ Sandbox execution environment not implemented

### What's Needed
1. Create `DocumentAnalysisSkill` class (extends BaseSkill)
2. Implement `load_documents()` - fetch from file repo
3. Implement `analyze_in_sandbox()` - process in execution env (not passed to model)
4. Implement `generate_summary()` - token-efficient output
5. Integrate with file browser UI (#313)

### Dependencies
- **Blocks**: #313 (file browser needs skill output)
- **Depends on**:
  - Existing file repo ✅
  - Existing document analyzer ✅
  - BaseSkill pattern ✅ (just completed)
  - Sandbox execution framework ❓ (may not exist)

### Complexity Factors
- **Sandbox execution**: How does skill run code without model context? Unclear implementation.
- **Token measurement**: Need baseline comparison (existing vs new)
- **File format handling**: Multiple format support (PDF, DOCX, JSON, Markdown)
- **Memory efficiency**: 150K tokens → <15K tokens (90%+ reduction)

### Ripeness: ⚠️ **2/10** (Not ripe)
- Sandbox framework unclear
- Design decisions about execution not documented
- Dependency on #313 complicates validation

---

## Issue #313: CONV-UX-DOCS (File Browser UI)

### Overview
Build file browser UI with upload, download, preview, delete, search capabilities.

### Current State
- ✅ File upload route exists (`web/api/routes/files.py`)
- ✅ Database models for files exist
- ❌ File browser UI doesn't exist
- ❌ File retrieval endpoints incomplete
- ❌ Preview functionality missing
- ❌ Search not implemented

### What's Needed
1. Create `/files` route (page handler)
2. Create file browser template with:
   - File list view (uploaded files + artifacts)
   - Drag & drop upload zone
   - Search/filter controls
   - Download/delete buttons
   - Preview modal (for supported types)
3. API endpoints:
   - GET `/api/v1/files` - list files
   - GET `/api/v1/files/{id}/download` - download
   - DELETE `/api/v1/files/{id}` - delete
   - GET `/api/v1/files/search` - search
4. Frontend JavaScript:
   - Drag & drop handler
   - Progress indicator
   - File preview logic

### Dependencies
- **Blocks**: #355 (save as artifact feature)
- **Depends on**:
  - Existing file upload ✅
  - File metadata DB models ✅
  - #302 (document analysis integration) - for preview
  - #355 (artifact persistence) - for artifact display

### Complexity Factors
- **UI complexity**: Multiple views, drag-drop, preview, search
- **Frontend state**: Managing file list, filters, uploads in real-time
- **File preview**: Different handling for PDF, Markdown, JSON, etc.
- **Search**: Across large file collections efficiently
- **Integration**: Needs to work with skill output from #302

### Ripeness: ⚠️ **1/10** (Not ripe - most complex)
- Multiple UI components to build from scratch
- No existing file browser in codebase
- Heavy frontend/backend coordination needed
- Largest scope in M4

---

## Issue #314: CONV-UX-PERSIST (Conversation Persistence)

### Overview
Implement conversation history and session persistence across refreshes/channels.

### Current State
- ✅ Conversation storage likely exists (implied by chat system)
- ❌ Conversation history view not implemented
- ❌ Session restoration not implemented
- ❌ Cross-channel sync not implemented
- ❌ Conversation ID system may be incomplete

### What's Needed
1. Database schema:
   - Conversation table (if not exists)
   - Message history storage
   - Session metadata (timestamps, user, channel)
2. API endpoints:
   - GET `/api/v1/conversations` - list
   - GET `/api/v1/conversations/{id}` - resume
   - GET `/api/v1/conversations/{id}/messages` - history
   - POST `/api/v1/conversations/{id}/restore` - restore state
   - DELETE `/api/v1/conversations/{id}` - delete
3. Frontend:
   - History sidebar component
   - "Continue where you left off" modal
   - Auto-restore logic on page load
4. Cross-channel foundation:
   - Unified conversation ID across web/CLI/Slack
   - State sync mechanism

### Dependencies
- **Blocks**: Cross-channel features (Slack integration, CLI continuity)
- **Depends on**:
  - Existing chat system ✅
  - Database models (may need expansion)
  - Session management system (partially exists)

### Complexity Factors
- **Database design**: Need flexible schema for multi-channel conversations
- **Real-time sync**: State must sync across channels in real-time
- **Privacy**: Conversations must respect user permissions across channels
- **Performance**: History search/filter must be fast
- **Cross-channel ID**: Complex ID system for web/CLI/Slack parity

### Ripeness: ⚠️ **2/10** (Not ripe)
- Core chat system exists but history not implemented
- Cross-channel sync architecture unclear
- Database schema decisions needed first

---

## Issue #355: DOCS-STOPGAP (Basic Artifact Persistence)

### Overview
Quick stopgap (not full domain model) to save/retrieve generated artifacts.

### Current State
- ✅ File upload exists
- ✅ File browser route framework exists
- ✅ File storage works
- ❌ "Save as artifact" button not on chat outputs
- ❌ Artifact-specific handling missing
- ❌ Filename editing missing

### What's Needed
1. Chat output enhancement:
   - Show "Save as artifact" button for outputs >500 chars
   - Trigger artifact save modal
2. Artifact save handler:
   - POST endpoint to save output as file
   - Auto-generate filename (or let user customize)
   - Tag as "artifact" type
3. File browser:
   - Filter "generated artifacts" vs "uploaded files"
   - Show creation date, size
   - Download/delete actions
4. Persistence:
   - Store in existing file repository
   - Metadata (type: "artifact", source: conversation ID)

### Dependencies
- **Blocks**: None (independent)
- **Depends on**:
  - Existing file upload ✅
  - Basic file storage ✅
  - File metadata DB ✅

### Complexity Factors
- **Chat integration**: Where/how to add button? (Depends on chat UI architecture)
- **Filename generation**: Smart default names from content
- **File size**: Large generated content may hit limits

### Ripeness: ✅ **5/10** (Most ripe of M4)
- Uses existing infrastructure
- Defined scope (out of scope: folders, versioning, search)
- Smaller effort than #313/#314
- **HOWEVER**: Blocked by #313 (file browser UI) for display

### Effort: **20-30 hours**
- Save button: 4h
- Artifact endpoint: 3h
- File browser list view: 12h
- Testing: 4h

---

## Interdependency Graph

```
#355 (DOCS-STOPGAP)
    ↓ blocks display
    └→ #313 (CONV-UX-DOCS) ← File Browser UI
            ↓ needs document preview
            └→ #302 (CONV-MCP-DOCS) ← Document Analysis

#314 (CONV-UX-PERSIST)
    (independent for MVP - can be done in parallel)
```

**Critical Path**: #302 → #313 → #355

---

## Ripeness Comparison

### Why All "Hairy"?

1. **Infrastructure incomplete**: None have complete infrastructure
   - #302: No sandbox framework
   - #313: No UI components
   - #314: Cross-channel architecture unclear
   - #355: Depends on #313 being complete

2. **Database decisions**: Multiple need schema/design decisions
   - #302: How to handle large documents?
   - #313: File metadata, artifact types
   - #314: Conversation schema, session format
   - #355: Artifact-specific metadata

3. **Cross-system integration**: All touch multiple systems
   - #302: Files + skills + models
   - #313: Frontend + API + DB
   - #314: Chat + DB + Auth + Channels
   - #355: Chat + Files + DB

4. **UI complexity**: #313 and #314 both have significant frontend work
   - Building new pages/components from scratch
   - Real-time state management
   - Drag-drop, search, filtering

---

## Strategic Options

### Option A: Tackle Critical Path (#302 → #313 → #355)
**Timeline**: 3-4 weeks
**Benefit**: Complete document workflow
**Risk**: Long chain, #313 bottleneck for #355
**Blocker**: #302 sandbox architecture needs design

### Option B: Do Quick Stopgap (#355 only)
**Timeline**: 1-2 weeks
**Benefit**: Users can save artifacts immediately
**Risk**: Incomplete without file browser (#313)
**Blocker**: Still need basic #313 for display

### Option C: Focus on Persistence (#314) + Parallel Work
**Timeline**: 2-3 weeks
**Benefit**: Fixes conversation loss (major UX pain)
**Risk**: Doesn't address document management
**Blocker**: Cross-channel architecture needs design

### Option D: Skip M4, Focus on Bug Fixes
**Timeline**: Depends
**Benefit**: Stabilize core features
**Risk**: Delays document/persistence work
**User Impact**: Addresses immediate pain points

---

## My Assessment

**All four issues are legitimately "hairy":**

1. **#302** - Depends on undefined sandbox architecture
2. **#313** - Largest UI scope (most complex)
3. **#314** - Cross-channel architecture not finalized
4. **#355** - Quick win but needs #313 for full value

**Quick recommendations:**

- **If focusing on document story**: Start with #302 + #313 (define sandbox architecture first)
- **If focusing on UX stability**: Start with #314 (conversation continuity fixes frustration)
- **If wanting quick win**: Do #355 + minimal #313 (basic file list only)
- **If wanting foundational work**: Define #302 architecture + #314 cross-channel design (no code yet)

**None are ready to start immediately without design/planning work first.**

---

## Next Steps (For PM Discussion)

1. **Strategic choice**: Which problem to solve first? (Documents? Persistence? Stability?)
2. **Architecture decisions**:
   - #302: How should sandbox execution work?
   - #314: What's cross-channel ID system?
3. **Scope clarification**:
   - #313: Full file browser or minimal list view?
   - #355: Just save button or full artifact management?

Once decisions made → can estimate effort per issue → plan sprint allocation.

**Current recommendation**: Don't start new work yet. Do lightweight architecture planning sessions for #302 and #314 first. They're too complex for improvisation.

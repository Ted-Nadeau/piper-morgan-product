# Phase 4 Addendum: Document & Artifact Management Domain
**UX Investigation - Piper Morgan**
**Date**: November 14, 2025, 2:30 PM PT
**Investigator**: Claude Code (UXR)
**Type**: Critical Domain Addition

---

## Executive Summary

This addendum addresses a **critical blind spot** in the original UX audit: **document and artifact management**. The initial investigation (Phases 1-4) focused on conversational UX, settings, and cross-channel integration but **did not audit file/document workflows**.

**Impact**: This gap affects **product value proposition** and **alpha UX** directly.

**Scope Decision**: Implementing **Option A (Lightweight)** for alpha - basic file browser without formal domain model. Defer deep taxonomy to Beta.

---

## What Was Missed

### Original Audit Scope (Phases 1-4)

✅ **Covered**:
- Chat conversations
- Standup reports
- Settings/preferences
- Cross-channel integration (web/CLI/Slack)
- Learning system UX
- Authentication flow

❌ **Missed**:
- **Uploaded document management** (can upload, but can't browse/retrieve)
- **Created artifact management** (Piper generates PRDs/specs, but output only goes to chat)
- **Document persistence** (no artifact history)
- **Document domain model** (Piper doesn't understand PRD vs spec vs report)
- **File organization** (no folders, tags, search)

### Why This Matters

From Chief of Staff discussion:

> "Document/Artifact Domain Model: Formal structure for how Piper understands and stores different document types. Current state: Learning system stores patterns, but no formal document taxonomy."

> "File Creation & Management Strategy ⭐ CRITICAL: Can upload files ✅, Can analyze/summarize ✅, No browsing interface for uploaded files ❌, No browsing interface for created files ❌, Output only goes to chat ❌"

**Strategic Question**: Need explicit domain model for documents (PRDs, specs, reports) or keep fluid?

**Answer for Alpha**: Keep fluid (Option A), establish foundation for Beta evolution.

---

## New Journey: Document Workflow

### Journey 6: Document Creation & Retrieval (MISSING FROM PHASE 2)

**Persona**: Sam - Documentation-Focused PM
- Role: PM who works with structured documents (PRDs, specs, reports)
- Context: Needs to upload template, ask Piper to draft PRD, retrieve it later for editing
- Motivation: "I want Piper to help me write docs, not just chat"

### Journey Map (Abbreviated)

| Step | Touchpoint | User Goal | Emotion | Pain Point | Gap |
|------|------------|-----------|---------|------------|-----|
| 1. Upload PRD template | Web | Provide example structure | 😊 Hopeful | Upload works | ✅ |
| 2. Ask Piper to draft PRD | Web Chat | Generate PRD from template | 😊 Excited | Piper generates good output | ✅ |
| 3. Review PRD in chat | Web Chat | Read generated PRD | 😊 Satisfied | Long output in chat window | ⚠️ |
| 4. Want to save PRD | Web Chat | Persist PRD for later | 😤 Frustrated | **No save button** | ❌ G65 |
| 5. Close browser | - | End session | 😐 | - | - |
| 6. Next day: need PRD | Web | Retrieve yesterday's PRD | 😤 Frustrated | **Can't find it** | ❌ G64 |
| 7. Search chat history | Web Chat | Scroll through messages | 😤 Annoyed | **Ephemeral, hard to find** | ❌ G35 |
| 8. Want to see uploads | Web | Check what files uploaded | 😤 Confused | **No file browser** | ❌ G63 |
| 9. Re-ask Piper | Web Chat | "Can you generate that PRD again?" | 😤 Resigned | **Lost work** | ❌ |

**Current Experience**: **2/10** (generates well, but no persistence)
**After Fixes**: **8/10** (can save, browse, retrieve artifacts)

---

## New Gaps Identified

### Category 12: Document & Artifact Management (NEW)

| ID | Gap | Impact | Freq | Effort | Score | Priority | Journey |
|----|-----|--------|------|--------|-------|----------|---------|
| **G63** | No file browser for uploaded documents | 9 | 7 | 5 | **315** | 🟡 Medium | 6 |
| **G64** | No artifact browser for created files (PRDs, specs) | 9 | 8 | 5 | **360** | 🟡 Medium | 6 |
| **G65** | Output only goes to chat (no persistence beyond history) | 10 | 9 | 4 | **360** | 🟡 Medium | 6 |
| **G66** | No document domain model (PRD structure unknown to Piper) | 8 | 6 | 3 | **144** | 🟠 Long-term | 6 |
| **G67** | No file organization (folders/tags/search) | 7 | 6 | 4 | **168** | 🟠 Long-term | 6 |
| **G68** | No document templates (PRD, spec, user story formats) | 7 | 5 | 5 | **175** | 🟠 Long-term | 6 |

**Category Total**: 6 new gaps

### Updated Priority Ranking (Top 25)

Original top 20 + new document gaps:

| Rank | ID | Gap | Score | Priority |
|------|----|-----|-------|----------|
| 1 | G1 | No global navigation menu | 700 | 🟢 Quick Win |
| 2 | G50 | No clear server startup message | 700 | 🟢 Quick Win |
| 3 | G8 | No logged-in user indicator | 630 | 🟢 Quick Win |
| 4 | G2 | No settings menu | 576 | 🟢 Quick Win |
| 5 | G3 | No breadcrumbs | 504 | 🟢 Quick Win |
| 6 | G33 | No "copy to clipboard" button | 480 | 🟢 Quick Win |
| 7 | G57 | No ARIA labels | 480 | 🟢 Quick Win |
| 8 | G21 | Inconsistent button styles | 441 | 🟢 Quick Win |
| 9 | G34 | No standup history | 432 | 🟢 Quick Win |
| 10 | G60 | Color contrast not validated | 420 | 🟢 Quick Win |
| 11 | G51 | Manual browser URL entry | 400 | 🟢 Quick Win |
| 12 | G40 | Settings scope unclear | 384 | 🟡 Medium |
| 13 | G4 | Non-intuitive URLs | 378 | 🟢 Quick Win |
| **14** | **G64** | **No artifact browser** | **360** | **🟡 Medium** ⭐ NEW |
| **15** | **G65** | **Output only to chat** | **360** | **🟡 Medium** ⭐ NEW |
| 16 | G13 | Theme inconsistency | 360 | 🟡 Medium |
| 17 | G62 | No skip-to-content links | 360 | 🟡 Medium |
| 18 | G23 | Inconsistent error displays | 343 | 🟡 Medium |
| 19 | G6 | No in-app help | 336 | 🟡 Medium |
| 20 | G16 | Inconsistent color palettes | 336 | 🟡 Medium |
| 21 | G22 | Inconsistent loading patterns | 336 | 🟡 Medium |
| 22 | G59 | No focus management | 336 | 🟡 Medium |
| **23** | **G63** | **No file browser** | **315** | **🟡 Medium** ⭐ NEW |
| 24 | G5 | No feature discovery | 315 | 🟡 Medium |
| 25 | G31 | No success confirmations | 315 | 🟡 Medium |

**G64 and G65 rank #14-15** - between accessibility (G62) and theme work (G13). **Higher priority than most design system work.**

---

## Implementation: Sprint 5.5 (NEW)

### Sprint 5.5: Document Management Foundation
**Week**: 5.5 (insert between current Sprint 5 and Sprint 6)
**Theme**: File persistence and retrieval
**Duration**: 1 week (5 days)

**Goals**:
- ✅ Users can browse uploaded files
- ✅ Users can browse Piper-created artifacts
- ✅ Files persist beyond chat history
- ✅ Foundation for future document domain model

**Backlog**:

#### 1. G63: File Browser for Uploads (3 days)

**Create `/files/uploads` page**:

```html
<!-- New page: web/templates/files_uploads.html -->
<h1>Uploaded Files</h1>
<div class="file-list">
  <!-- For each uploaded file: -->
  <div class="file-card">
    <div class="file-icon">📄</div>
    <div class="file-info">
      <div class="file-name">product-requirements.pdf</div>
      <div class="file-meta">
        <span>Uploaded: 2025-11-10</span>
        <span>Size: 2.4 MB</span>
        <span>Type: PDF</span>
      </div>
    </div>
    <div class="file-actions">
      <button onclick="downloadFile(id)">⬇ Download</button>
      <button onclick="deleteFile(id)" class="danger">🗑 Delete</button>
    </div>
  </div>
</div>
```

**API Endpoints** (new):
- `GET /api/v1/files/uploads` - List all uploaded files
- `GET /api/v1/files/uploads/:id/download` - Download file
- `DELETE /api/v1/files/uploads/:id` - Delete file

**Database**: Existing `file_uploads` table (verify schema has: id, user_id, filename, filepath, filesize, filetype, uploaded_at)

**Acceptance Criteria**:
- [ ] `/files/uploads` page shows list of uploaded files
- [ ] Files sortable by date (newest first)
- [ ] Download button works
- [ ] Delete button requires confirmation

---

#### 2. G64: Artifact Browser for Created Files (3 days)

**Create `/files/artifacts` page**:

```html
<!-- New page: web/templates/files_artifacts.html -->
<h1>Created Artifacts</h1>
<div class="artifact-list">
  <!-- For each artifact: -->
  <div class="artifact-card">
    <div class="artifact-icon">📋</div> <!-- Different icon than uploads -->
    <div class="artifact-info">
      <div class="artifact-name">Q4 Product Requirements Document</div>
      <div class="artifact-preview">
        Problem: Users need a way to...
      </div>
      <div class="artifact-meta">
        <span>Created: 2025-11-10 3:45 PM</span>
        <span>Type: Document</span> <!-- Generic for now, not "PRD" -->
        <span>From: <a href="/chat#conv-123">Chat conversation</a></span>
      </div>
    </div>
    <div class="artifact-actions">
      <button onclick="viewArtifact(id)">👁 View</button>
      <button onclick="downloadArtifact(id)">⬇ Download</button>
      <button onclick="deleteArtifact(id)" class="danger">🗑 Delete</button>
    </div>
  </div>
</div>
```

**API Endpoints** (new):
- `GET /api/v1/files/artifacts` - List all artifacts
- `GET /api/v1/files/artifacts/:id` - Get artifact content
- `POST /api/v1/files/artifacts` - Create artifact from chat message
- `DELETE /api/v1/files/artifacts/:id` - Delete artifact

**Database** (new table):
```sql
CREATE TABLE artifacts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  artifact_type VARCHAR(50) DEFAULT 'document', -- Generic for alpha
  conversation_id UUID, -- Link back to chat
  message_id UUID, -- Specific message
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_artifacts_user_id ON artifacts(user_id);
CREATE INDEX idx_artifacts_created_at ON artifacts(created_at DESC);
```

**Acceptance Criteria**:
- [ ] `/files/artifacts` page shows list of created artifacts
- [ ] Artifacts display preview (first 100 chars)
- [ ] Artifacts link back to originating chat conversation
- [ ] View button shows full artifact in modal/new page

---

#### 3. G65: Artifact Persistence from Chat (2 days)

**Add "Save as Artifact" button to chat interface**:

```html
<!-- In templates/home.html, add to bot messages: -->
<div class="message bot-message">
  <div class="message-content">
    <!-- Piper's response with markdown -->
  </div>
  <div class="message-actions">
    <button onclick="saveAsArtifact(messageId)" class="btn-secondary">
      💾 Save as artifact
    </button>
  </div>
</div>
```

**Workflow**:
1. User asks Piper to generate PRD
2. Piper responds with generated PRD in chat
3. User clicks "💾 Save as artifact"
4. Modal appears: "Name this artifact: [Q4 Product Requirements]"
5. User confirms → artifact saved to `artifacts` table
6. Success toast: "✅ Artifact saved! [View in Files](/files/artifacts)"

**API Endpoint**:
- `POST /api/v1/files/artifacts/from-message`
  - Body: `{ message_id: UUID, name: string }`
  - Creates artifact from message content

**Acceptance Criteria**:
- [ ] "Save as artifact" button appears on all bot messages >100 chars
- [ ] Clicking button prompts for artifact name (pre-filled with smart default)
- [ ] Artifact created and linked to message
- [ ] User redirected to artifact browser

---

#### 4. Unified Files Navigation (1 day)

**Create `/files` landing page with tabs**:

```html
<!-- New page: web/templates/files.html -->
<div class="files-container">
  <h1>Files & Artifacts</h1>

  <div class="tabs">
    <button class="tab active" data-tab="uploads">📤 Uploads (3)</button>
    <button class="tab" data-tab="artifacts">📋 Artifacts (7)</button>
  </div>

  <div id="uploads-tab" class="tab-content active">
    <!-- Load web/templates/files_uploads.html content here -->
  </div>

  <div id="artifacts-tab" class="tab-content" hidden>
    <!-- Load web/templates/files_artifacts.html content here -->
  </div>
</div>
```

**Add to Navigation Menu** (from Sprint 1):
```html
<nav>
  <a href="/">Home</a>
  <a href="/standup">Standup</a>
  <a href="/files">Files</a> <!-- NEW -->
  <a href="/learning">Learning</a>
  <a href="/settings">Settings</a>
</nav>
```

**Acceptance Criteria**:
- [ ] `/files` page has two tabs: Uploads | Artifacts
- [ ] Tab counts show number of items
- [ ] Navigation menu includes "Files" link
- [ ] URL routing: `/files` (default to uploads), `/files?tab=artifacts`

---

### Sprint 5.5 Dependencies

**Required Before Sprint 5.5**:
- Sprint 1 (Navigation menu) - need menu to add "Files" link
- Sprint 4 (Standup history) - pattern established for history/persistence

**Enables After Sprint 5.5**:
- Journey 6 (Document Workflow) now functional
- Foundation for Sprint 8+ document domain model work

---

## Deferred to Beta (Option B/C)

The following are **out of scope for Alpha** but documented for future work:

### G66: Document Domain Model (Score: 144)

**What**: Piper understands PRD structure (problem, solution, metrics, success criteria)

**Why Deferred**:
- Requires defining "canonical PM document" structure in shifting landscape
- PRD/spec formats vary by organization
- ChatPRD integration needs evaluation

**Beta Milestone**:
1. Define generic document structure: `{ title, sections[], metadata }`
2. PRD template: `{ problem, solution, metrics, success_criteria }`
3. Spec template: `{ overview, requirements, api_spec, test_plan }`
4. User story template: `{ as_a, i_want, so_that, acceptance_criteria[] }`
5. Piper recognizes document type from content

---

### G67: File Organization (Score: 168)

**What**: Folders, tags, search for files/artifacts

**Why Deferred**:
- Alpha volume too low to need organization (< 50 artifacts expected)
- Search requires full-text indexing
- Tagging UX requires design

**Beta Milestone**:
1. Folders: Simple hierarchy (`/personal`, `/project-x`)
2. Tags: Multi-select tagging (`PRD`, `Q4`, `draft`)
3. Search: Full-text search across artifact content
4. Filters: By type, date range, conversation

---

### G68: Document Templates (Score: 175)

**What**: PRD templates, spec formats, user story templates built into Piper

**Why Deferred**:
- Templates are organization-specific
- Let users upload their own templates in Alpha
- Observe usage patterns before creating canonical templates

**Beta Milestone**:
1. Template library: 5-10 common PM document templates
2. Custom templates: Users can save their own
3. Template variables: `{{project_name}}`, `{{quarter}}`
4. Piper auto-fills templates from conversation context

---

## Updated Phase 4 Summary Statistics

### Original Phase 4 Stats:
- Total Gaps: 62
- Quick Wins: 15 (24%)
- Medium Priority: 26 (42%)
- Long-term: 12 (19%)
- Major Refactor: 9 (15%)

### Updated Stats (with Document Management):
- **Total Gaps**: **68** (+6)
- **Quick Wins**: 15 (22%)
- **Medium Priority**: **29** (43%) ← +3 from document management
- **Long-term**: **15** (22%) ← +3 from document management
- **Major Refactor**: 9 (13%)

### Roadmap Impact

**Original Roadmap**: 7 sprints (Weeks 1-12)
**Updated Roadmap**: 8 sprints (Weeks 1-13)

**New Sprint Inserted**:
- Sprint 5.5 (Week 5.5): Document Management Foundation (NEW)
  - Follows: Sprint 5 (History & Persistence)
  - Precedes: Sprint 6 (Feedback & Communication)

**Total Implementation Time**:
- Original: ~12 weeks
- Updated: ~13 weeks (+1 week for document management)

---

## Success Metrics (Document Management)

After Sprint 5.5 implementation, track:

### Quantitative Metrics

1. **File Upload Retention**:
   - % of uploaded files viewed again (Goal: >30%)
   - Avg time between upload and first re-access (Goal: <3 days)

2. **Artifact Creation**:
   - % of long bot messages (>500 chars) saved as artifacts (Goal: >40%)
   - Avg artifacts created per user per week (Goal: 2+)

3. **Artifact Retrieval**:
   - % of artifacts viewed >1 time (Goal: >60%)
   - Avg time to find artifact via browser (Goal: <20 seconds)

### Qualitative Metrics (User Interviews)

1. **Persistence Satisfaction**: "Can you find documents Piper created for you?" (Goal: 90% yes)
2. **Value Perception**: "Does Piper help with document creation?" (Goal: 8/10)
3. **Organization Need**: "Do you need folders/tags?" (Informs Beta priority)

---

## Recommendations

### For Alpha (Immediate)

1. **Implement Sprint 5.5** (Document Management Foundation) - 1 week
   - High ROI: G64 (360), G65 (360), G63 (315) all in top 25 priorities
   - Enables core product value: "Piper helps with PM documents"
   - Foundation for Beta domain model work

2. **Update Navigation Menu** (Sprint 1) to include "Files" link
   - Users need discoverability for file browser

3. **Monitor Artifact Usage Patterns** in Alpha
   - What document types do users create most?
   - Do they upload templates? What formats?
   - Informs Beta domain model decisions

### For Beta (Post-Alpha)

1. **Observe Before Canonizing**:
   - Don't force "PRD template" if users have their own
   - Watch for organic patterns in artifact types
   - User interviews: "What document scaffolding would help?"

2. **Evaluate ChatPRD Integration**:
   - If users consistently create PRDs, consider plugin
   - If diverse document types, keep generic

3. **Organization Features** (Folders/Tags/Search):
   - Only if Alpha shows >50 artifacts per user
   - Design based on observed user mental models

---

## Alignment Verification

### Strategic Questions Answered

✅ **Q: Should Piper know typical product doc structures?**
- **Alpha Answer**: No, keep generic. Observe usage patterns first.
- **Beta Decision Point**: After 3 months of Alpha, evaluate if canonical structures add value.

✅ **Q: Need formal domain model for PRDs?**
- **Alpha Answer**: No, store as generic `artifact_type='document'`.
- **Beta Evolution**: If 70%+ of artifacts are PRDs, add structured PRD fields.

✅ **Q: Need file browser UI?**
- **Alpha Answer**: Yes, Sprint 5.5. Basic tabs: Uploads | Artifacts.
- **Enhancement**: Add folders/tags in Beta if needed.

✅ **Q: Upload + created files in one view?**
- **Alpha Answer**: Yes, unified `/files` page with tabs.
- **Rationale**: Users conceptually group "files I have" regardless of source.

✅ **Q: MCP Server timing?**
- **Alpha Answer**: Defer to Post-Sprint 7 (after accessibility).
- **Rationale**: File management API must be stable first, then expose via MCP.

---

## Integration with Existing Phases

### Phase 1 (Touchpoint Inventory)
**Add**: Section 11 - File & Artifact Management touchpoint

### Phase 2 (Journey Mapping)
**Add**: Journey 6 - Document Creation & Retrieval (detailed in this addendum)

### Phase 3 (Design System)
**No Changes**: Design system applies to file browser UI (use same tokens)

### Phase 4 (Gap Analysis)
**Add**: Category 12 - Document Management (6 new gaps: G63-G68)
**Update**: Priority ranking (G64, G65 in top 15)
**Add**: Sprint 5.5 to roadmap

### Phase 5 (Strategic Recommendations) - Next
**Add**: Document management as strategic pillar
**Add**: Decision framework for domain model evolution (Alpha → Beta → MVP)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-14 2:30 PM PT
**Status**: Approved for Alpha Implementation (Option A)
**Next Action**: Proceed to Phase 5 with document management integrated

# Gameplan: #422 MUX-IMPLEMENT-DOCS-ACCESS

**Issue**: #422 MUX-IMPLEMENT-DOCS-ACCESS: Document Retrieval UI
**Date**: 2026-01-25
**Author**: Lead Developer (Claude Opus)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL on port 5433
- [x] Testing framework: pytest
- [x] Document endpoints: `/api/v1/documents/*` (6 endpoints exist)
- [x] Place window pattern: `templates/components/place_window.html` (from #684)
- [x] Trust-gating pattern: CSS classes + JavaScript (from #684)

**My understanding of the task**:
- Create UI for browsing documents following Place window pattern from #684
- Documents are DOCUMENTATION-type Places with SOFT hardness (Stage 4+)
- Backend API already exists - this is UI only
- Follow atmosphere styling established in #684

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**
- [ ] Multiple agents in parallel - No, single sequential work
- [ ] Task duration >30 min - Yes
- [x] Multi-component work - No, single agent
- [ ] Exploratory/risky - No, following established pattern

**Assessment**: [ ] SKIP WORKTREE
**Rationale**: Single agent, follows established #684 patterns, low risk

### Part B: PM Verification Required

**What actually exists**:
```
templates/components/place_window.html - Place window component (from #684)
web/api/routes/documents.py - 6 API endpoints
services/repositories/file_repository.py - Data access
web/api/routes/ui.py - UI routes (needs /documents added)
```

**Recent work**: #684 completed - Place window pattern established
**Actual task**: Add UI components using existing patterns

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Patterns established, infrastructure verified

---

## Phase 0: Initial Bookending

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 422
   ```

2. **Infrastructure Verification**
   ```bash
   # Verify document API endpoints
   curl -s http://localhost:8001/api/v1/documents/ | head -20

   # Verify place_window.html exists
   ls templates/components/place_window.html

   # Verify UI routes file
   ls web/api/routes/ui.py
   ```

3. **Update GitHub Issue**
   - Mark Phase 0 checkboxes complete
   - Document any discoveries

### STOP Conditions
- Document API not responding
- Place window component missing
- Trust-gating pattern changed since #684

---

## Phase 0.5: Frontend-Backend Contract Verification

### Endpoint Verification

| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| list documents | /documents | /api/v1 | /api/v1/documents |
| search | /documents/search | /api/v1 | /api/v1/documents/search |
| analyze | /documents/{id}/analyze | /api/v1 | /api/v1/documents/{id}/analyze |
| question | /documents/{id}/question | /api/v1 | /api/v1/documents/{id}/question |
| summarize | /documents/{id}/summarize | /api/v1 | /api/v1/documents/{id}/summarize |
| compare | /documents/compare | /api/v1 | /api/v1/documents/compare |

### Static File Verification
```bash
# Verify static file serving
grep -n "StaticFiles" web/app.py
ls -la web/static/js/
```

---

## Phase 1: Document Window Component

### Objective
Create reusable document window component following Place window pattern from #684.

### Agent Instructions

```markdown
## Task: Create Document Window Component

**Issue**: #422 (Document Retrieval UI)

### Context
- Follow `templates/components/place_window.html` pattern exactly
- PlaceType.DOCUMENTATION = purple atmosphere (#ddd6fe gradient)
- SOFT hardness = Stage 4+ visibility
- Must pass contractor test ("Would a colleague say this naturally?")

### Files to Create
- `templates/components/document_window.html`

### Acceptance Criteria
- [ ] Component has data attributes (document-id, confidence, hardness, source-url)
- [ ] Documentation atmosphere styling (purple/reference gradient)
- [ ] Trust-gating CSS classes (trust-visibility, data-min-stage="4")
- [ ] ARIA labels for accessibility
- [ ] Piper's voice in summary ("I see...", "This document...")
- [ ] JavaScript API (DocumentWindow.create(), render())

### Test Requirements
- 10+ unit tests in `tests/unit/templates/test_document_window.py`
- Test data attributes
- Test atmosphere styling
- Test trust visibility classes
- Test ARIA labels

### Evidence Required
- Component file created
- Test output showing all tests pass
- Full test suite still passing

### STOP Conditions
- Atmosphere styling conflicts with place_window.html
- Trust-gating pattern differs from #684
```

### Deliverables
- `templates/components/document_window.html`
- `tests/unit/templates/test_document_window.py` (10+ tests)

---

## Phase 2: Document Collection View

### Objective
Create browsable document page with search integration.

### Agent Instructions

```markdown
## Task: Create Document Collection Page

**Issue**: #422 (Document Retrieval UI)

### Context
- Route: `/documents`
- Uses document_window.html from Phase 1
- Integrates with `/api/v1/documents/search` API
- Trust-gated: Stage 4+ only (SOFT hardness)

### Files to Create/Modify
- `templates/documents.html` (NEW)
- `web/api/routes/ui.py` (add /documents route)

### Acceptance Criteria
- [ ] Page renders at /documents
- [ ] Search input filters documents (debounced)
- [ ] Documents rendered in responsive grid
- [ ] Trust-gated: data-min-stage="4"
- [ ] Empty state: "No documents yet" (with personality)
- [ ] Loading state during API fetch

### Test Requirements
- 5+ unit tests in `tests/unit/templates/test_documents_page.py`
- Test route exists
- Test trust-gating
- Test empty state
- Test document grid rendering

### Evidence Required
- Page accessible at /documents
- Search filters correctly
- Test output
- Full test suite passing

### STOP Conditions
- Trust-gating inconsistent with #684
- Search API not responding
```

### Deliverables
- `templates/documents.html`
- Route in `web/api/routes/ui.py`
- `tests/unit/templates/test_documents_page.py` (5+ tests)

---

## Phase 3: Document Detail Modal

### Objective
Expanded view with Q&A capability.

### Agent Instructions

```markdown
## Task: Create Document Detail Modal

**Issue**: #422 (Document Retrieval UI)

### Context
- Modal for expanded document view
- Integrates with analyze/question APIs
- Shows Piper's summary, allows Q&A

### Files to Modify
- `templates/components/document_window.html` (add modal)
- OR create `templates/components/document_detail_modal.html`

### Acceptance Criteria
- [ ] Modal opens on document click/expand
- [ ] Shows summary from /analyze endpoint
- [ ] Q&A input field sends to /question endpoint
- [ ] Compare action links to /compare
- [ ] "Open original" link works
- [ ] Escape key closes modal
- [ ] Focus trap for accessibility

### Test Requirements
- 5+ integration tests
- Test modal open/close
- Test API integration
- Test keyboard navigation

### Evidence Required
- Modal opens and closes correctly
- Q&A works with real API
- Test output

### STOP Conditions
- API integration failing
- Modal accessibility issues
```

### Deliverables
- Modal component
- `tests/unit/templates/test_document_modal.py` (5+ tests)

---

## Phase 4: Navigation Integration

### Objective
Add Documents to navigation and command palette.

### Agent Instructions

```markdown
## Task: Integrate Documents into Navigation

**Issue**: #422 (Document Retrieval UI)

### Context
- Add "Documents" nav item (SOFT hardness = Stage 4+)
- Add command palette command "View documents"
- Follows patterns from #420 and #421

### Files to Modify
- `templates/components/navigation.html`
- `templates/components/command_palette.html`

### Acceptance Criteria
- [ ] Nav item "Documents" visible at Stage 4+
- [ ] Command palette command "View documents" works
- [ ] Keyboard shortcut optional
- [ ] Trust-gating consistent with existing nav items

### Test Requirements
- 3+ tests
- Test nav item visibility
- Test command execution

### Evidence Required
- Nav shows Documents at Stage 4+
- Command palette command works
- Test output

### STOP Conditions
- Trust-gating inconsistent with existing nav
```

### Deliverables
- Updated navigation.html
- Updated command_palette.html
- Tests added to existing test files

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **Evidence Compilation**
   ```bash
   # Run all #422-specific tests
   pytest tests/unit/templates/test_document_window.py tests/unit/templates/test_documents_page.py tests/unit/templates/test_document_modal.py -v

   # Run full test suite
   pytest tests/unit/ -v --tb=short
   ```

2. **GitHub Issue Update**
   - Fill completion matrix with evidence
   - Mark all acceptance criteria
   - Update status to "Complete - Awaiting PM Review"

3. **Session Log Update**
   - Document all files created/modified
   - Include test counts
   - Note any discoveries or issues

### Success Criteria
- [ ] All acceptance criteria met
- [ ] 20+ tests passing
- [ ] No regressions
- [ ] Evidence provided
- [ ] Session log complete

---

## Multi-Agent Coordination

### Deployment Map

| Phase | Type | Work | Evidence |
|-------|------|------|----------|
| 1 | Sequential | Document window component | 10+ tests |
| 2 | Sequential | Collection page | 5+ tests |
| 3 | Sequential | Detail modal | 5+ tests |
| 4 | Sequential | Nav integration | 3+ tests |
| Z | Sequential | Final verification | Full suite |

**Note**: Single agent sequential work - no parallel deployment needed.

---

## Verification Gates

- [ ] Phase 1: Document window component tests passing
- [ ] Phase 2: Collection page tests passing
- [ ] Phase 3: Modal tests passing
- [ ] Phase 4: Navigation tests passing
- [ ] Phase Z: Full suite 0 regressions

---

## STOP Conditions (Apply Throughout)

- Document API endpoints not responding
- Place window pattern changed since #684
- Trust-gating inconsistent
- Atmosphere styling conflicts
- Tests fail for any reason

---

## Cross-References

- **#684**: Place window pattern source
- **#420**: Navigation vocabulary pattern
- **#421**: Command palette pattern
- **#423**: Will use document lifecycle indicator (dependency)
- **#424**: May integrate with Insight Journal (future)

---

## Audit Notes

This gameplan follows gameplan-template.md v9.3:
- [x] Phase -1 Infrastructure Verification
- [x] Phase 0 Initial Bookending
- [x] Phase 0.5 Frontend-Backend Contract
- [x] Phases 1-4 Development Work
- [x] Phase Z Final Bookending
- [x] Multi-Agent Coordination
- [x] STOP Conditions
- [x] Evidence Requirements

---

_Gameplan created: 2026-01-25_

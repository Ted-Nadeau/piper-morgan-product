# STOP-GAP-DOCS: Basic Artifact Persistence
**Priority**: P2
**Labels**: `ux`, `documents`, `stop-gap`
**Effort**: 3 days
**Sprint**: A10 (Post-TEST)

---

## Problem Statement

Users generate valuable artifacts (PRDs, specs, reports) in chat that vanish into conversation history. No way to save, browse, or retrieve these artifacts later. Current experience: 2/10.

## Goal

Quick stop-gap solution (not full domain model) to let users save and retrieve artifacts. Target: 6/10 experience.

## Scope

**In Scope**:
- "Save as file" button on long chat outputs
- Basic file browser at `/files`
- Simple list view of saved artifacts
- Download capability
- Delete capability

**Out of Scope**:
- Document domain model (PRD vs Spec types)
- Folders/organization
- Version history
- Collaborative editing
- Search (beyond filename)

## Acceptance Criteria

- [ ] Chat outputs > 500 chars show "Save as artifact" button
- [ ] Saved artifacts appear in `/files` browser
- [ ] Files show: name, date, size, actions (download/delete)
- [ ] Artifacts persist across sessions
- [ ] Basic filename editing capability
- [ ] Downloaded files are valid markdown/text

## Implementation Notes

- Store in database or filesystem (PM decision)
- No complex taxonomy - just "artifacts" table/folder
- Reuse existing UI patterns from Tranches 1-2
- Keep it simple - this is a stop-gap

## Success Metrics

- User can save a generated PRD and retrieve it next day
- Experience improves from 2/10 to 6/10
- Sets foundation for future domain model decisions

---

*This is intentionally minimal. Full document management is post-MVP.*

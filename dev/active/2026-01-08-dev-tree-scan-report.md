# Dev Tree Retroactive Scan Report

**Date**: 2026-01-08
**Prepared by**: Documentation Manager (Haiku)
**Scope**: dev/active/ and dev/2025/ trees

---

## Summary

Scanned dev/ tree for working documents that should be moved to docs/ for permanent storage and access. Found 57 files in dev/active/ and 177+ files in dev/2025/12/ alone.

---

## Recommended Moves

### HIGH PRIORITY: Briefings → knowledge/

| Current Location | Recommended Location | Action |
|-----------------|---------------------|--------|
| `dev/active/BRIEFING-ESSENTIAL-CXO.md` | `knowledge/BRIEFING-ESSENTIAL-CXO.md` | Move |
| `dev/active/BRIEFING-ESSENTIAL-CXO-v2-draft.md` | (evaluate if final) | PM Decision |
| `dev/active/BRIEFING-ESSENTIAL-CXO (1).md` | DELETE (duplicate) | Delete |

### HIGH PRIORITY: PDRs → docs/internal/pdr/

Currently no dedicated PDR directory exists. Recommend creating `docs/internal/pdr/`.

| Current Location | Recommended Location |
|-----------------|---------------------|
| `dev/active/PDR-001-ftux-as-first-recognition-v3.md` | `docs/internal/pdr/PDR-001-ftux-recognition-v3.md` |
| `dev/active/PDR-002-conversational-glue.md` | `docs/internal/pdr/PDR-002-conversational-glue.md` |
| `dev/active/PDR-101-multi-entity-conversation.md` | `docs/internal/pdr/PDR-101-multi-entity-conversation.md` |
| `dev/active/PDRs-README.md` | `docs/internal/pdr/README.md` |

### MEDIUM PRIORITY: UX Specs → docs/internal/design/

Currently no dedicated design specs directory. Recommend creating `docs/internal/design/specs/`.

| Current Location | Recommended Location |
|-----------------|---------------------|
| `dev/active/contextual-hint-ux-spec-v1.md` | `docs/internal/design/specs/contextual-hint-ux-spec-v1.md` |
| `dev/active/cross-session-greeting-ux-spec-v1.md` | `docs/internal/design/specs/cross-session-greeting-ux-spec-v1.md` |
| `dev/active/empty-state-voice-guide-v1.md` | `docs/internal/design/specs/empty-state-voice-guide-v1.md` |
| `dev/active/multi-entry-ftux-exploration-v1.md` | `docs/internal/design/specs/multi-entry-ftux-exploration-v1.md` |
| `dev/active/b1-quality-rubric-v1.md` | `docs/internal/design/specs/b1-quality-rubric-v1.md` |
| `dev/active/conversational-glue-design-brief.md` | `docs/internal/design/briefs/conversational-glue.md` |
| `dev/active/cxo-brief-discovery-ux-strategy.md` | `docs/internal/design/briefs/discovery-ux-strategy.md` |

### MEDIUM PRIORITY: Operations → docs/internal/operations/

| Current Location | Recommended Location |
|-----------------|---------------------|
| `dev/active/staggered-audit-calendar-2026.md` | `docs/internal/operations/audit-calendar-2026.md` |

### LOW PRIORITY: Testing/Analysis → docs/internal/testing/

| Current Location | Recommended Location |
|-----------------|---------------------|
| `dev/active/ftux-gap-analysis-report.md` | `docs/internal/testing/ftux-gap-analysis-report.md` |
| `dev/active/canonical-queries-v2.md` | `docs/internal/testing/canonical-queries-v2.md` |
| `dev/active/canonical-query-test-matrix-v2.md` | `docs/internal/testing/canonical-query-test-matrix-v2.md` |

### LOW PRIORITY: Scripts → scripts/

| Current Location | Recommended Location |
|-----------------|---------------------|
| `dev/active/validate_322_multiworker.py` | `scripts/validate_322_multiworker.py` |

### ARCHIVE: Historical Artifacts in dev/2025/

Found in dev/2025/12/04/:
- `wardley-map-piper-morgan-v1.md` - Unique strategic artifact
- `wardley-map-piper-morgan-visual.html` - Visual companion
- `codebase-component-inventory.md` - Architectural snapshot

**Recommendation**: Move to `docs/internal/architecture/artifacts/` for permanent access.

---

## Files That Should Stay in dev/

### Session Logs (Correctly Placed)
All `*-log.md` files should remain in dev/YYYY/MM/DD/ structure.

### Working Documents (Active)
- `gameplan-*.md` - Active gameplans
- `agent-prompt-*.md` - Agent prompts
- `memo-*.md` - Inter-agent memos (archive after action)
- `issue-*.md` - Issue working docs
- `report-*.md` - Reports (move to docs/ when finalized)

### Screenshots
- `.png` files are working artifacts, can stay in dev/

---

## New Directory Structure Needed

```
docs/internal/
├── pdr/                    # NEW - Product Decision Records
│   ├── README.md
│   ├── PDR-001-*.md
│   └── PDR-002-*.md
├── design/                 # NEW - Design documentation
│   ├── specs/             # UX specifications
│   └── briefs/            # Design briefs
└── architecture/
    └── artifacts/          # NEW - Point-in-time artifacts (Wardley, inventories)
```

---

## Counts

| Category | Count | Action |
|----------|-------|--------|
| Briefings | 3 | Move to knowledge/ |
| PDRs | 4 | Move to new docs/internal/pdr/ |
| UX Specs | 7 | Move to new docs/internal/design/specs/ |
| Operations | 1 | Move to docs/internal/operations/ |
| Testing | 3 | Move to docs/internal/testing/ |
| Scripts | 1 | Move to scripts/ |
| Historical Artifacts | 3 | Move to docs/internal/architecture/artifacts/ |
| **Total to move** | **22** | |

---

## PM Decision Points

1. **Create docs/internal/pdr/?** - PDRs need a permanent home
2. **Create docs/internal/design/?** - UX specs need organization
3. **CXO Briefing version** - Which version is canonical? v1 or v2-draft?
4. **Historical artifacts** - Worth preserving Wardley map and inventory?
5. **Memos** - Should completed memos be archived? Where?

---

**Next Steps**:
1. PM reviews and approves directory structure
2. Execute moves (can be scripted)
3. Update NAVIGATION.md with new sections
4. Verify no broken references

---

*End of Report*

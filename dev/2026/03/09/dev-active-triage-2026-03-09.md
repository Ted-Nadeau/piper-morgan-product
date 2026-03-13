# dev/active/ Folder Triage

**Date**: March 9, 2026
**Total files**: 55 (including .DS_Store and 5 binary/image files)
**Prepared by**: Documentation Management Specialist

---

## Category 1: DELETE — Confirmed Duplicates (4 files)

| File | Why |
|------|-----|
| `pattern-062-assembly-assumption.md` | Identical to `docs/internal/architecture/current/patterns/pattern-062-assembly-assumption.md` |
| `ppm-workstream-ship031-2026-02-21 (1).md` | Byte-for-byte duplicate of the non-(1) version (browser re-download artifact) |
| `PDR-002-appendix-layer-2-vision-template.md` | Scaffolding artifact; real doc is in `docs/internal/product/pdr/` |
| `PDR-002-appendix-layer-2-vision.md` | Near-duplicate of docs/ version (trailing whitespace only) |

---

## Category 2: FILE TO docs/ — Orphaned Originals That Need a Home (4 files)

| File | Destination | Why |
|------|-------------|-----|
| `PDR-003-entity-concept-model.md` | `docs/internal/product/pdr/` | Only copy; Architect just approved it (Mar 8). Status should be changed from DRAFT to APPROVED. |
| `human-collaborator-profile-template.md` | `docs/operations/alpha-onboarding/` | Template used to create profiles already in that directory. Should live alongside them. |
| `skill-narrative-verification-v1.md` | `.claude/skills/narrative-verification/SKILL.md` | Process doc that should be formalized as a skill. Referenced as "applied" in Ship #030. |
| `sprint-gate-template-v1.md` | `docs/internal/development/` or `.claude/skills/sprint-gate/SKILL.md` | Template used for #779 (M0 gate). Needed for future sprints. |

**NAVIGATION.md impact**: PDR-003 and the collaborator template should be added. The skills would be auto-discovered.

---

## Category 3: KEEP IN dev/active/ — Currently Active Working Documents (8 files)

| File | Why Active |
|------|-----------|
| `ia-conference-talk-groundwork-2026-02-08.md` | Conference is April 17, 2026 — source material for talk |
| `ia-conference-talk-outline-2026-04-17.md` | Primary working document for upcoming talk |
| `ia-conference-talk-outline-2026-04-17.md.pdf` | PDF export for sharing with conference organizers |
| `memo-hosr-workstreams-ship033-2026-03-08.md` | Ship #033 input — actively in use (created yesterday) |
| `ppm-workstream-ship032-2026-03-01.md` | Ship #032 input — may still be referenced |
| `agent-360-questionnaire-draft-v0.1.md` | PM to review (created yesterday) |
| `pipermorgan-ai-sitemap-v2-2026-02-16.md` | Current website IA reference — not superseded |
| `tug-piper-framework-mapping.md` | Strategic research doc relevant to IA Conference talk |

---

## Category 4: ARCHIVE TO dev/YYYY/MM/DD/ — Historical Working Documents (28 files)

These are dated documents whose purpose has been fulfilled (ships published, decisions made, sprints closed). They have historical value but are no longer active.

### Ship #030 inputs (published ~Feb 14)
| File | Archive To |
|------|-----------|
| `memo-from-arch-weekly-summary-2026-02-13.md` | `dev/2026/02/13/` |
| `memo-arch-comments-ship-030-2026-02-13.md` | `dev/2026/02/13/` |
| `ship-030-workstream-draft.md` | `dev/2026/02/13/` |

### Ship #031 inputs (published ~Feb 22)
| File | Archive To |
|------|-----------|
| `memo-arch-weekly-summary-feb13-19-2026.md` | `dev/2026/02/21/` |
| `memo-comms-weekly-summary-feb13-19-2026.md` | `dev/2026/02/22/` |
| `memo-cio-to-exec-weekly-2026-02-20.md` | `dev/2026/02/20/` |
| `cxo-weekly-summary-2026-02-13-19.md` | `dev/2026/02/22/` |
| `ppm-workstream-ship031-2026-02-21.md` | `dev/2026/02/21/` |
| `ship-031-workstream-draft.md` | `dev/2026/02/22/` |

### Ship #032 inputs (published ~Mar 4)
| File | Archive To |
|------|-----------|
| `memo-arch-weekly-summary-feb20-27-2026.md` | `dev/2026/03/01/` |
| `memo-comms-workstream-feb20-26-2026.md` | `dev/2026/03/01/` |
| `memo-cio-to-exec-weekly-2026-03-01.md` | `dev/2026/03/01/` |
| `cxo-workstream-summary-feb20-26-2026.md` | `dev/2026/03/01/` |
| `memo-ppm-distribution-post-m0-response-2026-02-20.md` | `dev/2026/02/20/` |

### Website copy chain (website deployed, copy approved)
| File | Archive To |
|------|-----------|
| `cxo-copy-guidance-summary-2026-02-08.md` | `dev/2026/02/08/` |
| `website-copy-exploration-2026-02-08.md` | `dev/2026/02/08/` |
| `website-copy-exploration-v2-2026-02-08.md` | `dev/2026/02/08/` |
| `website-pages-full-draft-2026-02-08.md` | `dev/2026/02/08/` |
| `pipermorgan-ai-sitemap-sketch-2026-02-08.md` | `dev/2026/02/08/` (superseded by v2) |

### Domain model proposal (implemented)
| File | Archive To |
|------|-----------|
| `domain-models-proposed-updates-2026-02-26.md` | `dev/2026/02/26/` |

### Pattern analysis batch (Feb 3 snapshot, superseded)
| File | Archive To |
|------|-----------|
| `pattern-evolution-report.md` | `dev/2026/02/03/` |
| `pattern-library-index.json` | `dev/2026/02/03/` |
| `pattern-meta-synthesis.md` | `dev/2026/02/03/` |
| `pattern-novelty-candidates.md` | `dev/2026/02/03/` |
| `pattern-usage-analysis.md` | `dev/2026/02/03/` |

### Misc historical
| File | Archive To |
|------|-----------|
| `ted-nadeau-windows-issues-2026-02-07.md` | `dev/2026/02/07/` |
| `unpublished-insights-summary-index.md` | `dev/2026/02/12/` |
| `Glue-issues.tsv` | `dev/2026/02/22/` (M0 planning artifact) |

---

## Category 5: ARCHIVE — Content Drafts (2 files)

| File | Archive To | Notes |
|------|-----------|-------|
| `draft-feb-10-12-cathedral-in-winter-v1.md` | `dev/2026/02/12/` | Published Feb 24; this is the working draft with PM placeholders |
| `draft-feb-5-9-narrative-v1.md` | `dev/2026/02/09/` | Working draft; check if published |

---

## Category 6: ARCHIVE — Log Index Experiments (3 files)

| File | Archive To | Notes |
|------|-----------|-------|
| `log-index-example.csv` | `dev/2026/02/28/` | Format example, superseded |
| `log-index-feb-8-27.csv` | `dev/2026/02/28/` | Canonical index for that period |
| `PM agent logs index - example.csv` | `dev/2026/02/28/` | Longer format example |

---

## Category 7: NEEDS PM DECISION — Binary/RTF Files (5 files, ~10.4 MB)

| File | Size | Notes |
|------|------|-------|
| `Narrative_Arc_Episode 2.docx.rtf` | 437 KB | RTF file — likely Cindy podcast episode 2 narrative arc. Unusual format for repo. |
| `privacy-first-metadata.png` | 2.0 MB | Image asset — possibly for website or blog. No markdown references it. |
| `robot-jig.png` | 2.4 MB | Image — likely Ship #031 illustration |
| `robot-upstream.png` | 2.8 MB | Image — likely Ship #032 illustration |
| `ship-029.png` | 2.7 MB | Image — Ship #029 illustration |

**Recommendation**: These are large binary files that bloat the gitignored dev/ directory. Consider:
- If published: originals likely exist on the blog platform. Safe to delete from dev/.
- If needed for reference: move to a dedicated `dev/assets/` or `dev/images/` folder.

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Delete (duplicates) | 4 | Safe to remove immediately |
| File to docs/ | 4 | Need proper filing + NAVIGATION.md update |
| Keep active | 8 | Leave in dev/active/ |
| Archive to dev/YYYY/MM/DD/ | 33 | Move to dated directories |
| PM decision (binaries) | 5 | Need direction on image/RTF handling |
| .DS_Store | 1 | Delete |
| **Total** | **55** | |

After cleanup, dev/active/ would contain only 8 actively relevant files.

---

*Prepared by Documentation Management Specialist, March 9, 2026*

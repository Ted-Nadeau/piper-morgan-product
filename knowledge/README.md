# Knowledge Base Staging Area

**Purpose**: Staging area for claude.ai project knowledge base files
**Last Updated**: October 17, 2025

---

## Overview

This directory contains files that exist in (or are staged for) the claude.ai project knowledge base. The project knowledge base is a **flat file collection** accessed via RAG search, not a hierarchical file system.

---

## Naming Convention

Files use the `BRIEFING-` prefix to provide context in RAG search results, since the knowledge base doesn't preserve directory hierarchy.

**Examples**:
- `BRIEFING-CURRENT-STATE.md` - Current sprint/epic position
- `BRIEFING-ESSENTIAL-LEAD-DEV.md` - Lead Developer role briefing
- `BRIEFING-ESSENTIAL-ARCHITECT.md` - Chief Architect role briefing

---

## File Categories

### 1. Canonical Files (Authoritative Source Here)

**BRIEFING-ESSENTIAL-* files** - Role-based briefings optimized for RAG:
- `BRIEFING-ESSENTIAL-LEAD-DEV.md` - Lead Developer briefing (2.5K tokens)
- `BRIEFING-ESSENTIAL-ARCHITECT.md` - Chief Architect briefing (2.5K tokens)
- `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` - Chief of Staff briefing (2.5K tokens)
- `BRIEFING-ESSENTIAL-COMMS.md` - Communications briefing (2.5K tokens)
- `BRIEFING-ESSENTIAL-AGENT.md` - Coding Agent briefing (2K tokens)
- `BRIEFING-ESSENTIAL-LLM.md` - LLM Lead briefing

**Status**: These files are unique to knowledge/ (may have equivalents in docs/briefing/ but knowledge/ versions are authoritative for claude.ai)

### 2. Symlinked Files (Canonical Source in docs/briefing/)

**All BRIEFING-* files are now symlinks** ✅ (Phase 2 complete Oct 17, 2025):
- `BRIEFING-CURRENT-STATE.md` → `../docs/briefing/BRIEFING-CURRENT-STATE.md`
- `BRIEFING-ESSENTIAL-LEAD-DEV.md` → `../docs/briefing/BRIEFING-ESSENTIAL-LEAD-DEV.md`
- `BRIEFING-ESSENTIAL-ARCHITECT.md` → `../docs/briefing/BRIEFING-ESSENTIAL-ARCHITECT.md`
- `BRIEFING-ESSENTIAL-AGENT.md` → `../docs/briefing/BRIEFING-ESSENTIAL-AGENT.md`
- `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` → `../docs/briefing/BRIEFING-ESSENTIAL-CHIEF-STAFF.md`
- `BRIEFING-ESSENTIAL-COMMS.md` → `../docs/briefing/BRIEFING-ESSENTIAL-COMMS.md`
- `BRIEFING-ESSENTIAL-LLM.md` → `../docs/briefing/BRIEFING-ESSENTIAL-LLM.md`

**Benefits**: Zero duplication, impossible to drift, one edit updates both locations

### 3. Temporary Staging Files

**Purpose**: Files copied from elsewhere in the repository for staging before adding to claude.ai project knowledge

**Lifecycle**:
1. Copy file from docs/ to knowledge/ for staging
2. PM adds to claude.ai project knowledge
3. **Clean up**: Remove temporary file after sync (to avoid duplication)

**Maintenance**: Check weekly docs audit for temporary files needing cleanup

---

## Workflow

### For Developers/Agents

1. **Update BRIEFING-* files** in their canonical location:
   - **All BRIEFING-* files**: Update in `docs/briefing/` (symlinks auto-sync to knowledge/) ✅
   - Changes immediately appear in both locations via symlinks
   - Impossible to have stale copies or drift

2. **Reference BRIEFING-CURRENT-STATE.md** for current sprint position (don't duplicate in role briefings)

3. **Use Serena symbolic queries** for live system state (see serena-briefing-queries.md)

### For PM (Briefing Updates)

**Automated Updates** (Phase 3 ✅):
```bash
# At end of session - updates position and timestamp automatically
./scripts/update-briefing.sh

# Or use auto mode (suggested position)
./scripts/update-briefing.sh --auto

# Specific position
./scripts/update-briefing.sh --position 2.3.5
```

**Manual Knowledge Base Sync**:
1. **After script runs**: Changes in docs/briefing/ auto-sync to knowledge/ via symlinks
2. **Update claude.ai**: Manually update project knowledge from docs/briefing/ files
3. **Weekly audit**: Verify symlinks working (`ls -lah knowledge/BRIEFING-*.md`)

**Benefits**:
- ✅ No manual editing of position/timestamp
- ✅ Consistent formatting (script handles it)
- ✅ Shows diff before applying
- ✅ Creates backup automatically
- ✅ "Auto more reliable than ol' monkey-mind" 😄

---

## Related Documentation

- **docs/briefing/** - Repository briefing documentation (hierarchical structure)
- **docs/NAVIGATION.md** - Complete documentation navigation
- **serena-briefing-queries.md** - Symbolic queries for live system state
- **.github/workflows/weekly-docs-audit.yml** - Automated weekly checks

---

## File Status (As of Oct 17, 2025)

| File | Status | Last Updated | Canonical Source |
|------|--------|--------------|------------------|
| BRIEFING-CURRENT-STATE.md | ✅ Current | Oct 17, 2025 | knowledge/ (will become symlink) |
| BRIEFING-ESSENTIAL-LEAD-DEV.md | ✅ Current | Oct 17, 2025 | knowledge/ |
| BRIEFING-ESSENTIAL-ARCHITECT.md | ✅ Current | Oct 17, 2025 | knowledge/ |
| BRIEFING-ESSENTIAL-AGENT.md | ✅ Current | Oct 17, 2025 | knowledge/ |
| BRIEFING-ESSENTIAL-CHIEF-STAFF.md | ⚠️ Needs Update | Oct 6, 2025 | knowledge/ |
| BRIEFING-ESSENTIAL-COMMS.md | ⚠️ Needs Update | Oct 6, 2025 | knowledge/ |
| BRIEFING-ESSENTIAL-LLM.md | ⚠️ Needs Update | Oct 6, 2025 | knowledge/ |
| CLAUDE.md | ✅ Current | Oct 3, 2025 | knowledge/ |
| serena-briefing-queries.md | ✅ Current | Oct 10, 2025 | knowledge/ |

---

## Weekly Maintenance Checklist

- [ ] Verify no duplicate files between knowledge/ and docs/briefing/
- [ ] Check for temporary staging files (clean up if found)
- [ ] Confirm all BRIEFING-ESSENTIAL-* files are current
- [ ] Verify symlinks are working (when implemented)
- [ ] Update claude.ai project knowledge with any changes

---

## Phase 2 Goals ✅ COMPLETE (Oct 17, 2025)

1. ✅ Document knowledge/ purpose (this README)
2. ✅ Create symlinks for all BRIEFING-* files (zero duplication achieved!)
3. ✅ Update NAVIGATION.md to include knowledge/ section
4. ✅ Update weekly docs audit workflow
5. ✅ All BRIEFING-* files current with Sprint A3 (position 2.3.4)

**Result**: Zero-drift knowledge base ready for Lead Developer onboarding!

## Phase 3 Goals ✅ COMPLETE (Oct 17, 2025)

1. ✅ Create automated update script (`scripts/update-briefing.sh`)
2. ✅ Smart defaults (auto-increment position, derive sprint, timestamp)
3. ✅ Interactive + auto modes for flexibility
4. ✅ Safety features (backup, diff preview, revert instructions)
5. ✅ Documentation (scripts/README.md, knowledge/README.md)

**Result**: "Auto more reliable than ol' monkey-mind" - PM can update with one command!

---

**Note**: This directory structure is evolving. See `dev/2025/10/17/phase-2-briefing-refactor-plan.md` for detailed refactor plan.

# Phase 2: Briefing System Refactor - Complete Plan

**Date**: October 17, 2025, 11:12 AM
**Context**: Lead Developer onboarding preparation
**Phase**: 2 of 3 (Structure Refactoring)

---

## Current State Analysis

### File Duplication Discovered

**knowledge/ folder** (7 files):
- `BRIEFING-CURRENT-STATE.md` ✅ Updated Oct 17
- `BRIEFING-ESSENTIAL-AGENT.md` ✅ Updated Oct 17
- `BRIEFING-ESSENTIAL-ARCHITECT.md` ✅ Updated Oct 17
- `BRIEFING-ESSENTIAL-CHIEF-STAFF.md` (stale)
- `BRIEFING-ESSENTIAL-COMMS.md` (stale)
- `BRIEFING-ESSENTIAL-LEAD-DEV.md` ✅ Updated Oct 17
- `BRIEFING-ESSENTIAL-LLM.md` (stale)

**docs/briefing/ folder** (different structure):
- `BRIEFING-CURRENT-STATE.md` (STALE - Oct 16)
- `ESSENTIAL-AGENT.md` (different from knowledge/ version)
- `METHODOLOGY.md`
- `PROJECT.md`
- `README.md`
- `roles/ARCHITECT.md`
- `roles/LEAD-DEV.md`
- `roles/PROGRAMMER.md`
- `roles/ESSENTIAL-LLM-LEAD.md`

### Key Insights

1. **Naming Convention**: knowledge/ uses `BRIEFING-` prefix for flat RAG search
2. **Purpose Difference**:
   - `knowledge/` = Staging for claude.ai project knowledge (flat namespace)
   - `docs/briefing/` = Repository documentation (hierarchical)
3. **Duplication Pattern**: BRIEFING-CURRENT-STATE exists in both places
4. **Workflow**: PM manually updates claude.ai project knowledge after repo changes

---

## Problems Identified

### P1: File Duplication (High Priority)
- `BRIEFING-CURRENT-STATE.md` exists in both locations
- Versions diverge over time (knowledge/ updated Oct 17, docs/briefing/ stale Oct 16)
- Manual sync required creates drift risk
- No automated sync mechanism

### P2: Inconsistent Naming (Medium Priority)
- knowledge/ uses `BRIEFING-ESSENTIAL-*` prefix
- docs/briefing/ uses plain names (`ESSENTIAL-AGENT.md`) or nested (`roles/ARCHITECT.md`)
- Makes it unclear which is authoritative

### P3: Unclear Purpose (Medium Priority)
- No README.md in knowledge/ explaining its purpose
- NAVIGATION.md doesn't mention knowledge/ folder
- Weekly docs audit doesn't explicitly check knowledge/ sync

### P4: Workflow Efficiency (Low Priority)
- Manual updates to claude.ai project knowledge
- No automated copy/sync process
- Relies on weekly docs sweep to catch drift

---

## Recommended Solutions

### Solution 1: Single Source of Truth with Symlinks ⭐ **RECOMMENDED**

**Approach**: Make knowledge/ files symlinks to docs/briefing/ files

**Implementation**:
```bash
# Remove duplicates from knowledge/
rm knowledge/BRIEFING-CURRENT-STATE.md

# Create symlink to canonical source
ln -s ../docs/briefing/BRIEFING-CURRENT-STATE.md knowledge/BRIEFING-CURRENT-STATE.md

# Git will track the symlink, not duplicate the content
```

**Pros**:
- ✅ Zero duplication - impossible to have stale copies
- ✅ One edit updates both locations
- ✅ Git tracks symlinks properly
- ✅ Preserves flat namespace for RAG (knowledge/ structure maintained)
- ✅ Clear canonical source (docs/briefing/)

**Cons**:
- ⚠️ Symlinks might confuse some tools (though Git handles them well)
- ⚠️ PM would need to update files in docs/briefing/ then sync to claude.ai

**Files to Symlink**:
1. `knowledge/BRIEFING-CURRENT-STATE.md` → `docs/briefing/BRIEFING-CURRENT-STATE.md`

**Files That DON'T Need Symlinks** (knowledge/ has different/better versions):
- `BRIEFING-ESSENTIAL-*` files (these are already better in knowledge/)

### Solution 2: Documentation + Manual Workflow (Alternative)

**Approach**: Keep separate files, document the sync workflow clearly

**Implementation**:
- Create `knowledge/README.md` explaining purpose
- Update `NAVIGATION.md` with knowledge/ section
- Enhance weekly docs audit checklist
- Document in PM workflow docs

**Pros**:
- ✅ Simple - no file system changes
- ✅ Flexible - can diverge if needed
- ✅ Clear documentation of purpose

**Cons**:
- ❌ Still requires manual sync
- ❌ Risk of drift remains
- ❌ Duplication continues

### Solution 3: Automated Sync Script (Future Enhancement)

**Approach**: Script to sync docs/briefing/ → knowledge/ automatically

**Implementation**:
```bash
# scripts/sync-briefing-to-knowledge.sh
cp docs/briefing/BRIEFING-CURRENT-STATE.md knowledge/BRIEFING-CURRENT-STATE.md
# Add other syncs as needed
```

**When to Use**: Phase 3 automation (if symlinks don't work for some reason)

---

## Phase 2 Implementation Plan

### Step 1: Document Current State (30 min)

**Create `knowledge/README.md`**:
```markdown
# Knowledge Base Staging Area

## Purpose
This directory contains files staged for the claude.ai project knowledge base.

## Naming Convention
Files use `BRIEFING-` prefix for flat RAG search (project knowledge is non-hierarchical).

## Workflow
1. Update canonical files in repository (usually in docs/)
2. Sync or symlink to this directory
3. PM manually updates claude.ai project knowledge from these files
4. Weekly docs audit verifies sync status

## File Status

### Symlinked to Canonical Sources
- `BRIEFING-CURRENT-STATE.md` → `../docs/briefing/BRIEFING-CURRENT-STATE.md`

### Canonical in This Directory
- `BRIEFING-ESSENTIAL-*.md` files (optimized for RAG, unique to knowledge base)

### Temporary Staging (Clean Up Regularly)
- Files copied from docs/ for staging before knowledge base update
- Should be removed after sync to avoid duplication

## Weekly Maintenance
- Check for stale temporary files
- Verify symlinks are working
- Confirm knowledge base is in sync with repository
```

**Update `docs/NAVIGATION.md`** - Add section:
```markdown
### 📚 Knowledge Base (`knowledge/`)

**Staging area for claude.ai project knowledge**

- Essential briefings optimized for RAG search (flat namespace)
- Symlinked canonical files from docs/briefing/
- Temporary staging for docs before knowledge base updates
- See `knowledge/README.md` for workflow details
```

### Step 2: Create Symlinks (15 min)

```bash
# Backup current file
cp knowledge/BRIEFING-CURRENT-STATE.md knowledge/BRIEFING-CURRENT-STATE.md.backup

# Remove duplicate
rm knowledge/BRIEFING-CURRENT-STATE.md

# Create symlink to canonical source
ln -s ../docs/briefing/BRIEFING-CURRENT-STATE.md knowledge/BRIEFING-CURRENT-STATE.md

# Verify symlink works
cat knowledge/BRIEFING-CURRENT-STATE.md  # Should show current content

# Update docs/briefing/ version to match knowledge/ (which we just updated)
cp knowledge/BRIEFING-CURRENT-STATE.md.backup docs/briefing/BRIEFING-CURRENT-STATE.md

# Remove backup
rm knowledge/BRIEFING-CURRENT-STATE.md.backup
```

### Step 3: Update Weekly Docs Audit (15 min)

**Add to `.github/workflows/weekly-docs-audit.yml`**:

After line 72 (knowledge base section), add:
```yaml
- [ ] Verify knowledge/ symlinks are working: `ls -la knowledge/BRIEFING-*.md`
- [ ] Check for temporary staging files in knowledge/ (should be cleaned up after sync)
- [ ] Confirm no duplicate content between knowledge/ and docs/briefing/
```

### Step 4: Update Other Stale Files (15 min)

**Files needing update** (same pattern as Phase 1):
- `knowledge/BRIEFING-ESSENTIAL-CHIEF-STAFF.md`
- `knowledge/BRIEFING-ESSENTIAL-COMMS.md`
- `knowledge/BRIEFING-ESSENTIAL-LLM.md`

Apply same refactor: reference BRIEFING-CURRENT-STATE.md for current position.

### Step 5: Test and Validate (15 min)

```bash
# Test symlink
cat knowledge/BRIEFING-CURRENT-STATE.md

# Update via docs/briefing/
echo "test" >> docs/briefing/BRIEFING-CURRENT-STATE.md

# Verify change appears in knowledge/
tail knowledge/BRIEFING-CURRENT-STATE.md

# Remove test line
git checkout docs/briefing/BRIEFING-CURRENT-STATE.md

# Verify git sees symlink correctly
git status knowledge/
```

---

## Estimated Time

- **Step 1** (Documentation): 30 min
- **Step 2** (Symlinks): 15 min
- **Step 3** (Workflow update): 15 min
- **Step 4** (Stale files): 15 min
- **Step 5** (Testing): 15 min

**Total**: 90 minutes (1.5 hours)

---

## Success Criteria

✅ **Zero Duplication**: BRIEFING-CURRENT-STATE exists only once (in docs/briefing/)
✅ **Working Symlink**: knowledge/ version is symlink that works correctly
✅ **Documentation**: README.md explains knowledge/ purpose clearly
✅ **Navigation**: NAVIGATION.md includes knowledge/ section
✅ **Workflow**: Weekly audit checks knowledge/ sync status
✅ **All Files Current**: Remaining BRIEFING-ESSENTIAL-* files updated to Sprint A3

---

## Future Enhancements (Phase 3)

1. **Automated Sync Script**: `scripts/update-briefing-current-state.sh` for PM to run at session end
2. **Git Hook Option**: Auto-update on session log commits
3. **Consider**: Should other BRIEFING-ESSENTIAL-* files also be symlinked? Or are they unique to knowledge/?

---

## Questions for PM

1. **Symlink Approach**: OK to use symlinks for BRIEFING-CURRENT-STATE.md?
2. **Other Files**: Should BRIEFING-ESSENTIAL-* files also be symlinked, or are they unique to knowledge/?
3. **docs/briefing/ Structure**: Should we consolidate docs/briefing/roles/* into flat structure to match knowledge/?
4. **Workflow Preference**: Manual update workflow OK, or want automation in Phase 3?

---

**Created**: October 17, 2025, 11:20 AM
**Next**: Await PM approval before executing Phase 2

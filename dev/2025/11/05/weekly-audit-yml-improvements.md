# Improvements to weekly-docs-audit.yml

**Date**: November 5, 2025, 4:15 PM
**Based on**: Lessons from issue #293 (Nov 5 audit)
**Purpose**: Provide better context for future audit agents

---

## 🎯 Key Improvements Needed

### 1. Add File Location Guidance (CRITICAL)

**Problem**: Agent checked for roadmap.md in project root instead of actual location
**Root Cause**: Workflow didn't specify to consult docs/NAVIGATION.md first

**Add this section** after line 60 (before "### 📚 Claude Project Knowledge Updates"):

```yaml
              ### 🗺️ **IMPORTANT: File Location Reference**

              **Before reporting any file as "missing", consult [docs/NAVIGATION.md](../docs/NAVIGATION.md) for actual locations.**

              **Common File Locations** (not in project root):
              - **roadmap.md**: `docs/internal/planning/roadmap/roadmap.md`
              - **Pattern catalog**: `docs/internal/architecture/current/patterns/README.md`
              - **ADRs**: `docs/internal/architecture/current/adrs/`
              - **Session logs**: `dev/2025/MM/DD/` structure
              - **User config**: `config/PIPER.md` (generic), `config/PIPER.user.md` (user-specific)

              **Agent instructions**:
              1. Read docs/NAVIGATION.md FIRST before searching for files
              2. Use NAVIGATION.md as source of truth for directory structure
              3. Only report files as "missing" if not found at documented location
              4. Document actual location if found elsewhere
```

### 2. Clarify Config File Expectations

**Problem**: Confusion between PIPER.md and PIPER.user.md (two different files)

**Update line 112** from:
```yaml
- [ ] Update sprint goals in PIPER.user.md if new sprint started
```

To:
```yaml
- [ ] Update sprint goals in config/PIPER.user.md if new sprint started
  - **Note**: `config/PIPER.md` = generic system config (always exists)
  - **Note**: `config/PIPER.user.md` = user-specific config (may not exist if using database config)
  - These are TWO DIFFERENT FILES with different purposes
```

**Update line 71** from:
```yaml
- [ ] roadmap.md and backlog.md (if modified)
```

To:
```yaml
- [ ] docs/internal/planning/roadmap/roadmap.md (if modified)
- [ ] backlog.md (DEPRECATED - moved to trash)
```

### 3. Update Pattern Count

**Problem**: Checklist says "33 total patterns" but actual count is 38+ patterns

**Update line 125** from:
```yaml
- [ ] New patterns discovered this week (33 total patterns in 5 categories)
```

To:
```yaml
- [ ] New patterns discovered this week (38 total patterns as of Nov 5, 2025)
  - Check `docs/internal/architecture/current/patterns/README.md` for current count
  - Verify README.md count matches actual pattern-*.md files in directory
  - Update README.md if new patterns (036-038+) not yet documented
```

### 4. Add README.md Review Guidance

**Problem**: Line 150 says "Review root README.md" but doesn't specify what to look for

**Enhance lines 150-154** with specific guidance:

```yaml
- [ ] **Review root README.md (repository view)** - Agent should perform review:
  - [ ] Check for outdated "new" claims (>2 weeks old features should not say "NEW:")
  - [ ] Verify external links are current and working (especially pmorgan.tech)
  - [ ] Ensure code examples are still accurate
  - [ ] Check setup instructions match current process (PIPER.user.md vs database config)
  - [ ] Ensure content is brief and evergreen
  - [ ] Remove any accidental test content or markdown artifacts
  - [ ] **Create review document**: Save findings to `dev/2025/MM/DD/root-readme-review.md`
  - [ ] Note: This is separate from docs/README.md (pmorgan.tech homepage)
```

### 5. Add Context for Pattern Count Verification

**Add new item** in "Pattern & Knowledge Capture" section after line 125:

```yaml
- [ ] **Verify pattern count accuracy**:
  - Run: `ls -1 docs/internal/architecture/current/patterns/pattern-*.md | wc -l`
  - Compare actual file count to README.md documented count
  - Investigate discrepancy if counts don't match
  - Update README.md to document any undocumented patterns
  - Common cause: Recent pattern sweep work may add patterns without updating README
```

### 6. Add Roadmap Location Check

**Add new item** in "Sprint & Roadmap Alignment" section after line 108:

```yaml
- [ ] **Verify roadmap.md location** (common error):
  - Location: `docs/internal/planning/roadmap/roadmap.md` (NOT project root)
  - Check last update: `git log -1 --format="%ai" -- docs/internal/planning/roadmap/roadmap.md`
  - If not found, consult docs/NAVIGATION.md before reporting as missing
```

### 7. Clarify Automated Audit Approach

**Problem**: Lines 77-85 suggest using `/agent` commands but agent may prefer manual checks

**Update line 77** from:
```yaml
### 🔍 Automated Audits (Claude Code /agent)
```

To:
```yaml
### 🔍 Automated Audits (Claude Code /agent or manual verification)

**Note**: Agent may choose manual verification instead of launching subagents.
Both approaches are acceptable as long as evidence is provided.
```

### 8. Add Lessons Learned Section

**Add new section** at end (after line 188, before labels):

```yaml
              ### 📖 Lessons Learned from Previous Audits

              **Nov 5, 2025 (#293) - Key Findings**:
              1. ✅ **Always check docs/NAVIGATION.md first** before reporting files missing
              2. ✅ **PIPER.md ≠ PIPER.user.md** - Two different files (generic vs user-specific)
              3. ✅ **Pattern count discrepancy** - New patterns from pattern sweep may not be in README yet
              4. ✅ **roadmap.md location** - Lives at `docs/internal/planning/roadmap/roadmap.md`, not root
              5. ✅ **Root README.md review** - Agent should perform review, create findings document

              **Agent Guidelines**:
              - Provide evidence for all claims (command outputs, file paths, line numbers)
              - Explain any items that couldn't be completed (don't just skip)
              - Create separate review documents for complex analyses
              - Update this "Lessons Learned" section if new patterns discovered
```

### 9. Update Roadmap File Location in Action

**Update line 218** from:
```yaml
if [ -f "docs/planning/roadmap.md" ]; then
```

To:
```yaml
if [ -f "docs/internal/planning/roadmap/roadmap.md" ]; then
```

**And update line 219** from:
```yaml
POSITION=$(grep -i "current position\|position:" docs/planning/roadmap.md | head -1 | cut -d: -f2 | xargs)
```

To:
```yaml
POSITION=$(grep -i "current position\|position:" docs/internal/planning/roadmap/roadmap.md | head -1 | cut -d: -f2 | xargs)
```

---

## 📊 Summary of Changes

### Critical Changes (Prevent Future Errors)
1. ✅ Add docs/NAVIGATION.md guidance section
2. ✅ Fix roadmap.md path in automation script (lines 218-219)
3. ✅ Update pattern count (33 → 38+)
4. ✅ Clarify PIPER.md vs PIPER.user.md distinction

### Enhancement Changes (Better Context)
5. ✅ Add specific README.md review guidance
6. ✅ Add pattern count verification step
7. ✅ Add roadmap location verification
8. ✅ Add "Lessons Learned" section

### Clarification Changes (Reduce Ambiguity)
9. ✅ Clarify automated vs manual audit approaches
10. ✅ Specify file paths (not just filenames)
11. ✅ Add examples of expected outputs

---

## 🎯 Expected Impact

**Before improvements**:
- ❌ Agent checks project root for roadmap.md (wrong location)
- ❌ Agent confused about PIPER.md vs PIPER.user.md
- ❌ Agent reports outdated pattern count (33 instead of 38)
- ❌ Agent unsure what to check in root README.md

**After improvements**:
- ✅ Agent consults docs/NAVIGATION.md first (correct approach)
- ✅ Agent understands config file distinctions
- ✅ Agent verifies pattern count accuracy
- ✅ Agent performs detailed README.md review with findings doc
- ✅ Agent learns from previous audit lessons

---

## 📝 Implementation Notes

**File to modify**: `.github/workflows/weekly-docs-audit.yml`

**Sections to update**:
- Lines 60+ (add NAVIGATION.md guidance)
- Line 71 (fix roadmap.md path)
- Line 112 (clarify PIPER files)
- Line 125 (update pattern count)
- Lines 150-154 (enhance README review)
- Line 188+ (add Lessons Learned)
- Lines 218-219 (fix roadmap path in script)

**Testing**:
- Manual trigger: `gh workflow run weekly-docs-audit.yml`
- Verify issue creation with updated checklist
- Confirm roadmap path fix in automation job

---

**Created by**: prog-code (Claude Code / Sonnet 4.5)
**Date**: November 5, 2025, 4:15 PM
**Based on**: Issue #293 audit learnings

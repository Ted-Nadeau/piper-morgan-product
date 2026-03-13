# Directory Name Audit: `cd piper-morgan` vs `cd piper-morgan-product`
## Date: November 18, 2025, 11:21 AM PT
## Issue: Documentation uses wrong directory name for git clone

---

## Problem Statement

Repository name: `piper-morgan-product`
Git clone creates: `piper-morgan-product/` directory
Docs incorrectly say: `cd piper-morgan`

**Impact**: Alpha testers hit immediate blocker after clone.

---

## Search Results: `cd piper-morgan`

Found **15 files** with directory name issues:

### ✅ FIXED (Alpha Blockers)

1. **docs/ALPHA_QUICKSTART.md** line 27
   - Status: ✅ Fixed to `cd piper-morgan-product`
   - Also fixed: Python version spec added

2. **docs/ALPHA_TESTING_GUIDE.md** line 75
   - Status: ✅ Fixed to `cd piper-morgan-product`
   - Also fixed: Python version spec added

3. **README.md** line 25
   - Status: ✅ Already correct (`cd piper-morgan-product`)

### ⚠️ NEEDS REVIEW (Medium Priority - Developer Docs)

4. **docs/TECHNICAL-DEVELOPERS.md** line 32
   - Content: `cd piper-morgan-product`
   - Status: ⚠️ Need to verify context

5. **docs/HOME.md** lines 60, 399
   - Content: `cd piper-morgan-product`
   - Status: ⚠️ Need to verify (appears correct)

6. **docs/README.md** lines 80, 441
   - Content: `cd piper-morgan-product`
   - Status: ⚠️ Need to verify (appears correct)

7. **docs/public/getting-started/legacy-getting-started/developers.md** line 27
   - Content: `cd piper-morgan-product`
   - Status: ⚠️ Legacy doc, verify needed

8. **docs/installation/PREREQUISITES-COMPREHENSIVE.md** line 228
   - Content: `cd piper-morgan-product`
   - Status: ✅ Correct (verified from earlier audit)

### 🔴 WRONG DIRECTORY NAME (Needs Fix)

9. **docs/installation/quick-reference.md**
   - Line 22: `cd piper-morgan-workspace` (parent directory)
   - Line 26: `cd piper-morgan` ← WRONG
   - Fix: Change line 26 to `cd piper-morgan-product`

10. **docs/installation/step-by-step-installation.md**
    - Line 58: `cd piper-morgan-workspace` (parent directory)
    - Line 65: Text mentions `cd piper-morgan-workspace`
    - Status: ⚠️ Unclear if `piper-morgan` subdirectory mentioned

11. **docs/internal/planning/roadmap/CORE/USERS/CORE-USERS-ONBOARD.md** line 47
    - Content: `cd piper-morgan` ← WRONG
    - Priority: Low (internal planning doc)

### 📁 CONTEXT UNCLEAR (Needs Investigation)

12. **docs/processes/environment-sync-procedure.md**
    - Lines 72, 75: `ssh staging "cd piper-morgan && alembic current"`
    - Context: Production/staging server paths (may be intentionally different)
    - Action: Verify server deployment paths

13. **docs/internal/development/tools/quick-start.md** line 21
    - Content: `cd piper-morgan-platform` (different repo?)
    - Action: Verify if this is a different project

14. **docs/internal/development/tools/onboarding.md** line 20
    - Content: `cd piper-morgan-platform` (different repo?)
    - Action: Verify if this is a different project

### 📝 LEGACY/OMNIBUS (Already Documented)

15. **docs/omnibus-logs/2025-10-28-omnibus-log.md**
    - Lines 57, 240-241: Documents this exact issue!
    - Text: "⚠️ **Issue**: Guide says `cd piper-morgan`"
    - Text: "Was: `cd piper-morgan`, Now: `cd piper-morgan-product`"
    - **This was already caught and supposedly fixed on Oct 28!**

---

## Absolute Path Issues: `/piper-morgan/`

Found **127 instances** of absolute paths that will break for other users:

### Categories

**Developer Machine Paths** (~80 instances):
- `/Users/xian/Development/piper-morgan/...`
- Used in: session logs, investigation reports, handoff docs
- Impact: Examples in docs won't work for other users
- Fix: Replace with relative paths or `~/Development/piper-morgan/`

**Placeholder GitHub URLs** (~15 instances):
- `https://github.com/your-org/piper-morgan/issues`
- Used in: API docs, feature docs
- Impact: Broken links
- Fix: Replace with actual repo URL or make relative

**Production/Staging Paths** (~5 instances):
- `/var/log/piper-morgan/app.log`
- Context: Server deployment configuration
- Impact: May be intentional
- Action: Verify with PM

**Working Directory Paths** (~27 instances):
- Session logs, beads files, investigation docs
- Pattern: Internal working documents with full paths
- Impact: Low (internal only)
- Action: Acceptable for dev logs, problematic in published docs

---

## Root Cause Analysis

**How this happened**:
1. Oct 28, 2025: Issue discovered and "fixed" (see omnibus log)
2. Nov 11, 2025: ALPHA docs created/updated (ALPHA_QUICKSTART last updated)
3. Alpha docs created WITHOUT referencing omnibus findings
4. Same bug reintroduced

**Why it persisted**:
- No checklist for "must-verify" in new docs
- Omnibus findings not referenced during doc creation
- No automated check for `cd piper-morgan` vs `cd piper-morgan-product`

---

## Priority Fix List

### Immediate (Alpha Blocker)
- ✅ docs/ALPHA_QUICKSTART.md
- ✅ docs/ALPHA_TESTING_GUIDE.md

### High Priority (Developer Onboarding)
- 🔴 docs/installation/quick-reference.md line 26
- ⚠️ docs/installation/step-by-step-installation.md (verify)

### Medium Priority (Internal Planning)
- 🔴 docs/internal/planning/roadmap/CORE/USERS/CORE-USERS-ONBOARD.md line 47

### Needs Investigation
- docs/processes/environment-sync-procedure.md (server paths)
- docs/internal/development/tools/quick-start.md (different repo?)
- docs/internal/development/tools/onboarding.md (different repo?)

### Low Priority (Legacy Docs)
- docs/public/getting-started/legacy-getting-started/* (already marked legacy)

---

## Recommendations

### Immediate Actions
1. ✅ Fix alpha blockers (DONE)
2. Fix docs/installation/quick-reference.md
3. Verify docs/installation/step-by-step-installation.md

### Process Improvements
1. **Pre-commit hook**: Check for `cd piper-morgan[^-]` pattern
2. **Doc template**: Include "Verified Paths Checklist"
3. **Reference omnibus logs**: Before creating new install docs
4. **Automated link checker**: Flag `/Users/xian/` in published docs

### Prevention
```bash
# Add to .pre-commit-config.yaml or git hooks
# Block commits with wrong directory name in public docs
grep -r "cd piper-morgan[^-]" docs/ALPHA*.md docs/installation/ docs/README.md
# Exit 1 if found
```

---

## Evidence of Previous Fix

From `docs/omnibus-logs/2025-10-28-omnibus-log.md`:
```markdown
⚠️ **Issue**: Guide says `cd piper-morgan`
...
Was: `cd piper-morgan`
Now: `cd piper-morgan-product`
```

**This proves**:
- Issue was known and fixed on Oct 28
- Regression occurred when ALPHA docs created Nov 11
- Need better process to prevent regressions

---

**Status**: Alpha blockers fixed, comprehensive audit complete
**Next**: Investigate database schema issue (`is_alpha` column missing)

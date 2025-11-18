# Alpha Documentation Audit Report
## Date: November 18, 2025, 11:00 AM PT
## Auditor: Claude Code (Sonnet 4.5)
## Trigger: PM reported "sloppy documentation" during alpha testing

---

## Executive Summary

**Finding**: Significant documentation regression between Oct 29 and current state

**Impact**: Alpha testers hitting preventable blockers:
1. Python version ambiguity → pip install failures
2. Model naming mismatch → setup wizard crashes
3. README Quick Start missing critical details present in full guides

**Root Cause**: README.md simplified without maintaining critical requirements

---

## Comparison: Good Docs (Oct 29) vs Current Quick Start

### ✅ GOOD: `docs/installation/PREREQUISITES-COMPREHENSIVE.md` (Oct 29)

**Python Version Spec** (Lines 26-32):
```markdown
### 1. Python 3.12 (REQUIRED)

**Why**: Piper Morgan requires Python 3.12.x specifically

- Python 3.13+ lack pre-built wheels for scipy, onnxruntime, pillow
- Python 3.11 works but 3.12 is recommended
- Python 3.9/3.10 are too old
```

**Clarity**:
- ✅ Explicit version requirement
- ✅ Explains why (dependency compatibility)
- ✅ Specifies what doesn't work (3.9/3.10 too old, 3.13+ missing wheels)
- ✅ Provides verification command: `python3.12 --version`

### ❌ REGRESSION: `README.md` (Current)

**Python Version Spec** (Line 26):
```bash
python -m venv venv && source venv/bin/activate
```

**Problems**:
- ❌ No version specified
- ❌ Uses ambiguous `python` (could be 3.9, 3.11, 3.12, 3.13 depending on system)
- ❌ No explanation of requirements
- ❌ No troubleshooting guidance

**Impact on Alpha Testers**:
```
User with Python 3.12 system → `python` points to 3.9
→ Creates 3.9 venv
→ pip install fails on `future==0.18.2` with setuptools error
→ Blocker, no obvious fix in docs
```

---

## Evidence from Today's Alpha Test

### Issue 1: Python Version Mismatch

**User's Environment**:
- System has Python 3.12 (old install used this successfully)
- `python` command points to Python 3.9
- README says: `python -m venv venv` (no version spec)

**Result**:
```
ERROR: Could not find a version that satisfies the requirement future==0.18.2
ImportError: cannot import name 'SetuptoolsDeprecationWarning' from partially initialized module 'setuptools'
```

**Fix Applied**:
```bash
# What PM had to do (not in Quick Start)
rm -rf venv
python3.12 -m venv venv  # Explicitly use 3.12
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Should Have Been in Quick Start**:
```bash
# What it should say
python3.12 -m venv venv && source venv/bin/activate
# Or at minimum:
# Requires Python 3.11 or 3.12 - verify with: python --version
```

### Issue 2: AlphaUser Model Mismatch

**User's Error**:
```python
ImportError: cannot import name 'AlphaUser' from 'services.database.models'
```

**Root Cause**:
- Model renamed `AlphaUser` → `User` at some point
- `scripts/setup_wizard.py` line 479 not updated

**Fix Applied**:
```python
# Changed:
from services.database.models import AlphaUser, UserAPIKey

# To:
from services.database.models import User as AlphaUser, UserAPIKey
```

**How This Was Missed**:
- No end-to-end testing of fresh install
- Existing installations already had the schema
- Setup wizard not run in CI/CD

---

## Documentation Inventory

### Quality Docs (Keep as Reference)

1. **`docs/installation/PREREQUISITES-COMPREHENSIVE.md`** (Oct 29)
   - ✅ Python 3.12 requirement explicit
   - ✅ Explains why specific versions
   - ✅ Docker setup detailed
   - ✅ Verification commands provided

2. **`docs/installation/step-by-step-installation.md`** (Oct 29)
   - ✅ Beginner-friendly language
   - ✅ Screenshots/visual guidance
   - ✅ Step-by-step terminal commands
   - ✅ Troubleshooting sections

3. **`docs/installation/troubleshooting.md`** (Oct 28)
   - ✅ Common error scenarios
   - ✅ Port conflict resolution
   - ✅ Docker issues
   - ✅ Permission problems

### Regression Docs (Need Fixing)

1. **`README.md`** (Current - Last modified unknown)
   - ❌ Python version ambiguous
   - ❌ Oversimplified Quick Start
   - ❌ No troubleshooting links
   - ❌ Assumes too much knowledge

2. **.python-version** (Shows `3.11`)
   - ⚠️ Conflicts with PREREQUISITES (says 3.12)
   - ⚠️ Not enforced/explained anywhere
   - ⚠️ Ignored by README Quick Start

### Unknown/Unverified

1. **Alpha Quick Start at pmorgan.tech**
   - ❓ Can't access externally hosted docs
   - ❓ May have same regressions as README
   - ❓ PM testing this today (will surface issues)

---

## Root Cause Analysis

### How Did This Regress?

**Hypothesis**: Someone simplified README.md without cross-checking comprehensive guides

**Evidence**:
1. Good docs exist (Oct 29) with all details
2. README missing those details (date unknown)
3. No review process caught it
4. No fresh install testing validated README

**Contributing Factors**:
1. **No Doc Review Checklist**
   - Critical requirements not flagged
   - No "must include" list for Quick Starts
   - No comparison to canonical docs

2. **No Fresh Install CI/CD**
   - Setup wizard not run in tests
   - Assumes existing environment
   - Model changes not validated against wizard

3. **Multiple Sources of Truth**
   - README.md Quick Start
   - docs/installation/ guides
   - pmorgan.tech alpha docs
   - .python-version file
   - All say different things

---

## Recommendations

### Immediate Fixes (Today)

1. **Update README.md Quick Start**
   ```diff
   - python -m venv venv && source venv/bin/activate
   + python3.12 -m venv venv && source venv/bin/activate
   + # Requires Python 3.11 or 3.12 - check: python3.12 --version
   ```

2. **Add Troubleshooting Section to README**
   ```markdown
   ### Troubleshooting Installation

   **Python version errors?**
   - Ensure Python 3.11 or 3.12 installed
   - See: docs/installation/PREREQUISITES-COMPREHENSIVE.md

   **pip install failing?**
   - Upgrade pip: `pip install --upgrade pip setuptools wheel`
   - See: docs/installation/troubleshooting.md
   ```

3. **Fix .python-version Alignment**
   - Decide: 3.11 or 3.12?
   - Update all docs to match
   - Add explanation in README

4. **Add Fresh Install Test**
   - CI/CD job: clone → setup → validate
   - Runs setup_wizard.py
   - Catches model mismatches

### Process Improvements

1. **Documentation Review Checklist**
   ```
   Before publishing any Quick Start:
   [ ] Python version explicitly specified
   [ ] Links to troubleshooting docs
   [ ] Matches canonical installation guide
   [ ] Tested on fresh machine/VM
   [ ] All commands have verification steps
   ```

2. **Single Source of Truth Policy**
   - Canonical: `docs/installation/PREREQUISITES-COMPREHENSIVE.md`
   - All other docs MUST reference it
   - README Quick Start = abbreviated version WITH LINKS

3. **Alpha Testing Protocol**
   - Fresh laptop/VM required
   - Follow README.md only (no cheating with knowledge)
   - Document every blocker/confusion
   - Update docs before closing alpha sprint

---

## Files Needing Updates

### High Priority (Blocking Alpha)

1. **README.md**
   - Line 26: Add python version spec
   - Add troubleshooting section
   - Link to comprehensive guides

2. **.python-version**
   - Align with PREREQUISITES (3.12 vs 3.11 decision)
   - Document purpose/usage

3. **scripts/setup_wizard.py**
   - ✅ FIXED: AlphaUser import (commit 7ce48ec4)

### Medium Priority (Improve Alpha Experience)

4. **docs/installation/quick-reference.md**
   - Verify Python version consistency
   - Add common error scenarios

5. **requirements.txt**
   - Consider removing `future==0.18.2` if unused
   - Or document why Python 3.9 incompatible

### Low Priority (Post-Alpha)

6. **pmorgan.tech alpha docs** (external)
   - Audit for same regressions
   - Sync with canonical docs

---

## Next Steps

**For PM (xian)**:
1. Continue alpha testing - report next blocker
2. Decide: Python 3.11 or 3.12 as canonical version?
3. Approve documentation fix priority

**For Agent (me)**:
1. Wait for next alpha blocker OR
2. If no blocker: Begin README.md fixes
3. Create fresh install validation test

**Evidence Collection**:
- This audit report
- Session log: `dev/active/2025-11-18-1026-prog-code-log.md`
- Commits: 7ce48ec4 (AlphaUser fix)

---

## Lessons Learned

1. **"Simplification" ≠ "Improvement"**
   - Removing details ≠ making easier
   - Must maintain critical requirements

2. **Multiple Docs = Multiple Truths**
   - Need canonical source
   - All others reference it
   - Regular consistency audits

3. **Fresh Eyes Find Issues**
   - Alpha testing on new laptop = best validation
   - Developer laptops hide setup issues
   - Need clean room testing

4. **Documentation is Code**
   - Needs version control
   - Needs testing
   - Needs review process

---

**Status**: Audit Complete
**Next**: Awaiting PM guidance on fixes + next alpha blocker

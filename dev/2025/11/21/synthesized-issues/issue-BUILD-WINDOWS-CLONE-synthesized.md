# BUILD-WINDOWS-CLONE - Fix Windows Git Clone Failure (Illegal Filename Characters)

**Priority**: P0 (Blocks Windows developers)
**Labels**: `bug`, `Windows`, `critical`, `priority: highest`
**Milestone**: MVP (Blocking)
**Epic**: Cross-Platform Compatibility
**Related**: Ted Nadeau architectural review (Nov 19, 2025)

---

## Problem Statement

### Current State
Windows users cannot clone the repository due to illegal colon (`:`) character in filename:

```
error: invalid path 'archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md'
fatal: unable to checkout working tree
```

**Root Cause**: Colons are illegal in Windows filenames (MS-DOS legacy restriction). On macOS/Linux they're valid, but Windows blocks them.

**Discovered By**: Ted Nadeau during architectural review (Nov 19, 2025)

### Current Implementation
**Problematic file**:
- `archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md`
  - Contains colon (`:`) in directory name `claude docs 5:30`
  - Valid on macOS/Linux
  - Invalid on Windows (can't checkout)

### Impact
- **Blocks Windows developers**: Cannot clone repository at all
- **Blocks Windows testing**: Cannot run tests on Windows VM
- **Blocks Windows contributors**: Windows users can't participate
- **Violates cross-platform goal**: Repository should work everywhere
- **Support burden**: New Windows developers encounter immediate blocker

### Windows Illegal Characters
The following characters are illegal in Windows filenames:
- `:` (colon) - **PRIMARY ISSUE**
- `<` (less than)
- `>` (greater than)
- `"` (double quote)
- `/` (forward slash, path separator)
- `\` (backslash, path separator)
- `|` (pipe)
- `?` (question mark)
- `*` (asterisk)

---

## Goal

**Primary Objective**: Make repository cloneable and usable on Windows 10/11 by removing all illegal filename characters, preventing future violations, and validating cross-platform compatibility.

**Expected Outcome**:
```
Before:
❌ Windows user tries to clone → Error: invalid path
❌ Cannot checkout working tree
❌ Clone fails, no repository

After:
✅ Windows user clones successfully
✅ All files checked out without errors
✅ Repository fully functional on Windows
✅ Future commits validated for Windows compatibility
```

**Not In Scope** (explicitly):
- ❌ Full Windows compatibility testing (GUI, performance)
- ❌ Windows-specific features (registry, shortcuts)
- ❌ WSL vs native Windows differences (both should work)
- ❌ Git client-specific issues (recommend standard clients)

---

## What Already Exists

### Infrastructure ✅
- Repository on GitHub (public, cloneable)
- Git LFS configured (if needed)
- CI/CD pipeline (GitHub Actions)
- Pre-commit hooks framework (.pre-commit-config.yaml)

### What's Missing ❌
- Removal of illegal Windows filename characters
- Pre-commit hook to prevent future illegal filenames
- Windows clone testing (manual or CI)
- Documentation for Windows developers

---

## Requirements

### Phase 1: Identify All Illegal Filenames
**Objective**: Find all files with Windows-illegal characters

**Tasks**:
- [ ] Search repository for all files containing: `:`, `<`, `>`, `"`, `|`, `?`, `*`
- [ ] Primary search pattern: Look for colons in filenames
- [ ] Document each problematic file with:
  - Current path
  - Illegal character(s)
  - Suggested new name
- [ ] Create list of ALL files to rename
- [ ] Prioritize: Some may be in `.git` history (harder to fix)

**Deliverables**:
- Complete list of problematic files
- Suggested new names for each
- Assessment: Which files are in history vs committed

### Phase 2: Rename Problematic Files
**Objective**: Remove illegal characters from all filenames

**Tasks**:
- [ ] For each problematic file:
  - **Option A** (preferred): Rename using `git mv`:
    ```bash
    git mv "archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md" \
           "archive/piper-morgan-0.1.1/docs/claude-docs-0530/conversational_refactor.md"
    ```
  - **Option B** (if in history): Remove from archive if no longer needed
- [ ] Replace `:` with `-` (dash) in directory/file names
- [ ] Verify renamed files are properly tracked in git
- [ ] Test git status shows changes properly
- [ ] Create commit with all renames

**Deliverables**:
- All files renamed
- Git commit with all changes
- List of renamed files with mappings

### Phase 3: Add Pre-Commit Hook
**Objective**: Prevent future Windows-illegal filenames

**Tasks**:
- [ ] Create `.githooks/pre-commit` script:
  ```bash
  #!/bin/bash
  # Check for Windows-illegal characters in filenames
  # Exit with error if found
  ```
  - Check staged files for: `:`, `<`, `>`, `"`, `|`, `?`, `*`
  - Print error message with file name and illegal character
  - Suggest fix (which character to replace)
  - Exit code 1 (prevent commit)

- [ ] Alternative: Create `scripts/check-windows-filenames.py`:
  - More robust than shell script
  - Better error messages
  - Easier to maintain

- [ ] Update `.pre-commit-config.yaml`:
  ```yaml
  - id: check-windows-filenames
    name: Check for Windows-incompatible filenames
    entry: python scripts/check-windows-filenames.py
    language: python
    stages: [commit]
  ```

- [ ] Test pre-commit hook works:
  - Try to stage file with colon → should fail
  - Error message should be clear
  - Fix name and retry → should succeed

**Deliverables**:
- Pre-commit hook script
- Hook integrated into `.pre-commit-config.yaml`
- Documentation for developers
- Test cases verifying hook works

### Phase 4: Windows Testing
**Objective**: Verify repository works on Windows 10/11

**Tasks**:
- [ ] **Option A** (Recommended): Use GitHub Actions with Windows runner
  - Add Windows job to CI/CD: `windows-latest`
  - Run: `git clone <repo>`
  - Verify: No errors, all files present
  - Run tests on Windows

- [ ] **Option B**: Manual testing on Windows VM
  - Use VirtualBox/VMware with Windows 10/11
  - Clone repository
  - Verify all files present
  - Try to run tests/build

- [ ] Test with different Git clients:
  - Git Bash (Windows)
  - Git for Windows (native)
  - WSL (Windows Subsystem for Linux)

- [ ] Test clone success on:
  - Windows 10 Pro
  - Windows 11
  - Both NTFS and WSL2 filesystems

**Deliverables**:
- CI/CD workflow for Windows testing
- Evidence of successful clone on Windows
- Test results showing all files checkout

### Phase 5: Documentation Updates
**Objective**: Document Windows compatibility and workarounds

**Tasks**:
- [ ] Update `CONTRIBUTING.md`:
  - Add Windows developer setup section
  - Document recommended Git client
  - Mention WSL option (easier, full Linux support)
  - Link to troubleshooting guide

- [ ] Create/update Windows troubleshooting guide:
  - "I can't clone on Windows" → Solutions
  - Pre-commit hook errors → How to fix
  - WSL recommendation if native Windows has issues

- [ ] Add to onboarding documentation:
  - "Supported platforms: macOS, Linux, Windows"
  - "Windows users: See WINDOWS.md for setup"

**Deliverables**:
- Updated CONTRIBUTING.md
- Windows-specific documentation
- Troubleshooting guide
- Setup instructions for Windows developers

### Phase Z: Completion & Validation
- [ ] All illegal filenames renamed
- [ ] Pre-commit hook working
- [ ] Windows clone test passing
- [ ] CI/CD includes Windows test job
- [ ] Documentation updated
- [ ] GitHub issue closed with evidence

---

## Acceptance Criteria

### Phase 1: File Identification
- [ ] All files with Windows-illegal characters identified
- [ ] Complete list documented with:
  - Current path
  - Illegal character(s)
  - Suggested new name
  - Location in history (if applicable)
- [ ] No files with `:`, `<`, `>`, `"`, `|`, `?`, `*` remain in repository

### Phase 2: File Renaming
- [ ] All identified files renamed
- [ ] No `:` characters in any filename
- [ ] No `<`, `>`, `"`, `|`, `?`, `*` characters in filenames
- [ ] All renames tracked in git (use `git mv`)
- [ ] Single commit with all renames or separate commits per file
- [ ] Commit message documents issue fixed

### Phase 3: Pre-Commit Hook
- [ ] `scripts/check-windows-filenames.py` created and working
- [ ] Pre-commit hook configured in `.pre-commit-config.yaml`
- [ ] Hook prevents commits with illegal filenames
- [ ] Error message is clear and helpful:
  - Shows filename
  - Shows illegal character
  - Suggests replacement
- [ ] Hook can be bypassed (for emergencies): `git commit --no-verify`
- [ ] Test case: Create file with `:` → hook blocks commit

### Phase 4: Windows Testing
- [ ] Repository clones successfully on Windows 10
- [ ] Repository clones successfully on Windows 11
- [ ] All files present after clone (no missing files)
- [ ] No permission errors on Windows
- [ ] No encoding issues (UTF-8 handling)
- [ ] Tests run on Windows (if applicable)
- [ ] CI/CD Windows job passing

### Phase 5: Documentation
- [ ] CONTRIBUTING.md includes Windows section
- [ ] Windows-specific documentation created
- [ ] Troubleshooting guide covers common issues
- [ ] Onboarding docs mention Windows support
- [ ] All documentation links valid

### Cross-Platform Validation
- [ ] Clone works on macOS
- [ ] Clone works on Linux
- [ ] Clone works on Windows
- [ ] No regressions on existing platforms
- [ ] File permissions preserved

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Illegal files identified | ❌ | [file list] |
| Files renamed | ❌ | [git commit] |
| Pre-commit hook created | ❌ | [script] |
| Hook configured | ❌ | [.pre-commit-config.yaml] |
| Windows 10 clone test | ❌ | [test log] |
| Windows 11 clone test | ❌ | [test log] |
| CI/CD Windows job | ❌ | [workflow file] |
| Documentation updated | ❌ | [doc files] |

**Definition of COMPLETE**:
- ✅ All illegal filenames removed from repository
- ✅ Pre-commit hook prevents future violations
- ✅ Repository successfully clones on Windows 10 and 11
- ✅ CI/CD validates Windows compatibility
- ✅ Documentation updated for Windows developers

---

## Testing Strategy

### Unit Tests: Pre-Commit Hook
```python
# tests/test_windows_filenames.py
import subprocess
import tempfile
from pathlib import Path

def test_hook_rejects_colon_in_filename():
    """Pre-commit hook should reject filenames with colon"""
    with tempfile.NamedTemporaryFile(suffix=":invalid.txt") as f:
        # Run pre-commit hook
        result = subprocess.run(
            ["python", "scripts/check-windows-filenames.py", f.name],
            capture_output=True
        )
        assert result.returncode != 0, "Hook should reject colon"
        assert "colon" in result.stderr.lower()

def test_hook_accepts_valid_filename():
    """Pre-commit hook should accept valid filenames"""
    with tempfile.NamedTemporaryFile(suffix="-valid.txt") as f:
        result = subprocess.run(
            ["python", "scripts/check-windows-filenames.py", f.name],
            capture_output=True
        )
        assert result.returncode == 0, "Hook should accept dash"
```

### Integration Test: Windows Clone
```bash
#!/bin/bash
# tests/integration/test-windows-clone.sh

# Run on Windows VM or GitHub Actions Windows runner
set -e

echo "Testing Windows clone..."
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Clone repository
git clone https://github.com/anthropics/piper-morgan.git
cd piper-morgan

# Verify all files present
echo "Checking for Windows-illegal characters..."
if find . -name "*:*" -o -name "*<*" -o -name "*>*" -o -name "*\"*" -o -name "*|*" -o -name "*?*" -o -name "***"; then
    echo "❌ Found Windows-illegal characters"
    exit 1
fi

echo "✅ All files cloned successfully"
echo "✅ No Windows-illegal characters found"
```

### Cross-Platform Testing
- **macOS**: `git clone && ls -la` (verify all files)
- **Linux**: `git clone && find . -type f` (enumerate files)
- **Windows**: `git clone && dir /s` (verify files present)

---

## Success Metrics

### Quantitative
- Zero illegal filename characters in repository: 100%
- Windows clone success rate: 100%
- Pre-commit hook blocking illegal files: 100%
- CI/CD Windows job pass rate: 100%
- All tests passing on all platforms: 100%

### Qualitative
- Windows developers can clone without errors
- Pre-commit hook error messages are clear and helpful
- Documentation covers Windows setup adequately
- No platform-specific complaints from team

---

## STOP Conditions

**STOP immediately and escalate if**:
- Illegal character files found in Git history (require `git filter-branch`)
  - (Use tool to rewrite history if critical)
- Windows test environment unavailable (use GitHub Actions instead)
- Pre-commit hook conflicts with existing hooks (debug and integrate)
- Renames break any internal scripts (update scripts to match new paths)
- Test framework incompatible with Windows (fix/adapt tests)

**When stopped**: Document the issue, propose workaround, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Small

**Breakdown by Phase**:
- Phase 1 (Identify files): 1 hour
  - Search for illegal characters
  - Document problematic files

- Phase 2 (Rename files): 2-3 hours
  - Rename each file with `git mv`
  - Verify changes
  - Create commit

- Phase 3 (Pre-commit hook): 2-3 hours
  - Write/adapt hook script
  - Test hook functionality
  - Configure in `.pre-commit-config.yaml`

- Phase 4 (Windows testing): 2-4 hours
  - Set up Windows test environment (or use GitHub Actions)
  - Clone and test repository
  - Document results

- Phase 5 (Documentation): 1-2 hours
  - Update CONTRIBUTING.md
  - Create Windows guide
  - Update onboarding docs

**Total**: 8-13 hours (~1 day for single developer)

**Complexity Notes**:
- Low-medium complexity
- Straightforward file renames
- Hook implementation is simple
- Windows testing may require VM setup (use GitHub Actions to simplify)
- No code changes needed, only file operations

---

## Dependencies

### Required (Must be complete first)
- [ ] Repository must be cloned locally
- [ ] Git installed with Linux-like tools (Git Bash on Windows)
- [ ] Python 3.9+ for pre-commit hook
- [ ] Access to repository (to push commits)

### Optional (Nice to have)
- [ ] Windows VM for manual testing (use GitHub Actions instead)
- [ ] GitHub Actions setup (for CI/CD Windows job)

---

## Related Documentation

- **Issue Discovery**: Ted Nadeau architectural review (Nov 19, 2025)
- **Issue Records**:
  - `dev/active/2025-11-19-1259-research-code-log.md`
  - GitHub issue #353 (Windows clone failure)

- **Windows Development Resources**:
  - Git for Windows: https://gitforwindows.org/
  - WSL (Windows Subsystem for Linux): https://learn.microsoft.com/en-us/windows/wsl/
  - GitHub Actions Windows runners: https://github.com/actions/runner-images

---

## Workarounds (For Users Hitting This Now)

**For Windows developers unable to clone**:

1. **Use WSL (Recommended)**:
   ```bash
   # Install WSL2 on Windows 10/11
   wsl --install
   # Inside WSL:
   git clone https://github.com/anthropics/piper-morgan.git
   ```
   - Full Linux support
   - No NTFS restrictions
   - Easier development experience

2. **Use Git config (Risky)**:
   ```bash
   git config --global core.protectNTFS false
   git clone https://github.com/anthropics/piper-morgan.git
   ```
   - May cause issues with other repositories
   - Not recommended as permanent solution

3. **Clone without problematic directory**:
   ```bash
   git clone --sparse https://github.com/anthropics/piper-morgan.git
   # Then configure sparse checkout to exclude archive/
   ```

**Best practice**: Recommend WSL for Windows development

---

## Evidence Section

[This section is filled in during/after implementation]

### Phase 1 Results
```
Files with illegal characters:
- archive/piper-morgan-0.1.1/docs/claude docs 5:30/conversational_refactor.md
  - Illegal char: `:` (colon)
  - Suggested: claude-docs-0530

Total files to rename: 1
```

### Phase 2 Results
```
Renamed files:
✅ archive/piper-morgan-0.1.1/docs/claude docs 5:30/
  → archive/piper-morgan-0.1.1/docs/claude-docs-0530/

Commit: abc1234 "fix: remove Windows-illegal colon from filename"
```

### Phase 4 Results
```
Windows Clone Test:
✅ Windows 10 clone: SUCCESS
✅ Windows 11 clone: SUCCESS
✅ All files present
✅ No errors during checkout

CI/CD Windows Job:
✅ Passing on windows-latest runner
```

---

## Completion Checklist

Before requesting PM review:
- [ ] All illegal filenames identified ✅
- [ ] All files renamed with `git mv` ✅
- [ ] Pre-commit hook created and tested ✅
- [ ] Hook configured in `.pre-commit-config.yaml` ✅
- [ ] Windows clone test passing ✅
- [ ] CI/CD Windows job passing ✅
- [ ] CONTRIBUTING.md updated ✅
- [ ] Windows documentation created ✅
- [ ] All tests passing ✅
- [ ] GitHub issue closed ✅

**Status**: Not Started

---

## Notes for Implementation

**From synthesized issues #319 + #353**:
- Both issues identified same problem: colon in `claude docs 5:30` directory
- Both recommended same solution: rename files, add pre-commit hook, test Windows
- #353 is more formally structured with clear acceptance criteria
- Synthesized to include Windows testing via GitHub Actions (avoid needing VM)

**Key Decisions**:
- Use `git mv` for renames (preserves git history)
- Create Python script for pre-commit hook (more robust than bash)
- Use GitHub Actions with Windows runner for testing (no VM needed)
- Recommend WSL for Windows developers (best experience)

**Priority**: P0 because Windows developers can't work without this fix. Blocks:
- Windows development
- Windows testing
- Windows CI/CD
- New Windows contributors

**Timeline**: Should be completed immediately to unblock Windows developers.

---

**Remember**:
- Windows filename restrictions are real and unavoidable
- Pre-commit hook prevents future violations
- WSL is recommended for Windows developers
- GitHub Actions Windows runners help catch issues early
- This is a cross-platform support issue, not optional

---

_Issue synthesized: November 20, 2025_
_Synthesized from: #319 + #353_
_Canonical name: BUILD-WINDOWS-CLONE_
_Priority: P0 (Critical blocker)_

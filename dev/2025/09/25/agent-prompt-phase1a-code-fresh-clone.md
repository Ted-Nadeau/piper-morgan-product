# Claude Code Agent Prompt: Fresh Clone Environment Preparation

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
**Before doing ANYTHING else, verify infrastructure matches gameplan**:

```bash
# What the gameplan assumes exists:
# - Setup documentation: docs/guides/orchestration-setup-guide.md
# - Performance docs: Multiple locations found
# - Git repository: Standard GitHub structure

# Verify reality:
ls -la docs/guides/orchestration-setup-guide.md
find docs/ -name "*performance*" -o -name "*benchmark*"
git status
git remote -v
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

## Session Log Management (CRITICAL)

**Create fresh session log for this verification task**:
- Create one at: `dev/2025/09/25/2025-09-25-1720-prog-code-log.md`
- Update throughout work with evidence and progress
- Format: Use markdown (.md extension)

## MANDATORY FIRST ACTIONS

### 1. Check What Already Exists
**After infrastructure verification**:
```bash
# Check current project state
pwd
git status
git log --oneline -5

# Check if already in project directory
ls -la README.md main.py requirements.txt

# Verify we're in the main project, not a fresh clone location
```

## Mission
**Create completely fresh environment for setup verification testing**

**Scope Boundaries**:
- This prompt covers ONLY: Fresh clone environment preparation in /tmp
- NOT in scope: Following setup documentation (that's Cursor's job)
- Separate prompts handle: Setup documentation execution

## Context
- **GitHub Issue**: GREAT-1C (#187) - Verification Phase
- **Current State**: Working project with documentation created today
- **Target State**: Clean /tmp environment with fresh clone for testing
- **Dependencies**: Access to GitHub repository
- **User Data Risk**: None - working in isolated /tmp space
- **Infrastructure Verified**: [Verify first per above]

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:
- **"Created directory X"** → Provide `ls -la` showing it exists
- **"Cloned repository"** → Show git log and directory structure
- **"Environment clean"** → Show no existing venv, configs, or dependencies
- **"Repository accessible"** → Show git remote and clone success
- **"Directory ready"** → Show clean workspace structure

### Completion Bias Prevention (CRITICAL):
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- **NO assumptions** - only verified facts
- **NO rushing to claim done** - evidence first, claims second

## Constraints & Requirements

### For This Agent
1. **Work in isolation**: Use /tmp directory, not current project space
2. **Fresh environment only**: No existing configs, venvs, or dependencies
3. **Evidence collection**: Document every step with terminal output
4. **No setup execution**: Only environment preparation, not following setup docs

## Phase 1A Specific Instructions

### Step 1: Create Fresh Environment
```bash
# Move to completely clean space
cd /tmp
mkdir fresh-clone-verification-$(date +%Y%m%d-%H%M)
cd fresh-clone-verification-*

# Document clean state
pwd
ls -la  # Should show empty directory
echo $VIRTUAL_ENV  # Should show nothing
which python3
python3 --version
```

### Step 2: Clone Repository Fresh
```bash
# Clone the repository
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# Verify fresh clone state
git log --oneline -3
git status
ls -la
```

### Step 3: Document Initial State
```bash
# Document what exists in fresh clone
ls -la  # Show all files
cat README.md | head -10  # Show it's the right repo
ls -la docs/guides/  # Show setup guide exists
ls -la requirements.txt  # Show dependencies file
```

### Step 4: Verify No Existing Setup
```bash
# Confirm clean environment
echo $VIRTUAL_ENV  # Should be empty
ls -la venv/  # Should not exist
ls -la .env  # Should not exist
ls -la config/PIPER.user.md  # May or may not exist
```

## Expected Outcomes

### Success Criteria
- [ ] Clean /tmp directory created with timestamp
- [ ] Repository cloned successfully from GitHub
- [ ] All expected files present (README, main.py, requirements.txt, docs/)
- [ ] No existing Python environment or configuration
- [ ] Setup guide documentation confirmed present
- [ ] Terminal output evidence for every step

### Evidence Package to Provide
1. **Directory creation proof**: `ls -la /tmp/fresh-clone-verification-*`
2. **Clone success proof**: `git log --oneline -3` from fresh repo
3. **Clean environment proof**: No venv, .env, or existing config
4. **Documentation presence proof**: `ls -la docs/guides/orchestration-setup-guide.md`

## Handoff to Cursor Agent
Once environment prepared, provide Cursor with:
- **Clean clone location**: Full path to /tmp/fresh-clone-verification-*/piper-morgan-product/
- **Repository state**: Confirmed fresh with no setup artifacts
- **Documentation confirmed**: Setup guide exists and accessible
- **Environment baseline**: Clean Python 3 with no virtual environment

## STOP Conditions
- If repository cannot be cloned
- If setup documentation missing from fresh clone
- If /tmp directory unavailable
- If clean environment cannot be established

---

**Mission**: Prepare isolated fresh environment for setup verification testing. Do NOT execute setup - only prepare clean workspace for Cursor to test documentation.

**Evidence Standard**: Terminal output for every command, verified clean state, successful fresh clone.

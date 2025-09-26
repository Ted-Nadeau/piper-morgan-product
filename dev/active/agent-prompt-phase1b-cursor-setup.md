# Cursor Agent Prompt: Setup Documentation Following

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

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
# - Fresh clone environment prepared by Code agent
# - Setup documentation: docs/guides/orchestration-setup-guide.md
# - Clean environment with no existing setup

# Will verify Code agent's prepared environment:
# - /tmp/fresh-clone-verification-*/piper-morgan-product/ exists
# - No venv, .env, or config files present
# - Setup guide accessible
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

## Session Log Management (CRITICAL)

**Create fresh session log for this verification task**:
- Create one at: `dev/2025/09/25/2025-09-25-1720-prog-cursor-log.md`
- Update throughout work with evidence and progress
- Format: Use markdown (.md extension)

## MANDATORY FIRST ACTIONS

### 1. Verify Code Agent's Prepared Environment
```bash
# Check if Code agent completed environment preparation
ls -la /tmp/fresh-clone-verification-*/
cd /tmp/fresh-clone-verification-*/piper-morgan-product/

# Verify clean state
echo $VIRTUAL_ENV  # Should be empty
ls -la venv/  # Should not exist
ls -la .env   # Should not exist
ls -la docs/guides/orchestration-setup-guide.md  # Should exist
```

### 2. Assess System Context
**This is a CLEAN ENVIRONMENT for testing**:
- [ ] Confirm no existing user configuration
- [ ] Verify no running processes
- [ ] Confirm clean Python environment
- [ ] Document baseline state

## Mission
**Follow ONLY the setup documentation to reach operational state**

**Scope Boundaries**:
- This prompt covers ONLY: Executing documented setup procedures
- NOT in scope: Using prior knowledge or shortcuts
- Documentation source: docs/guides/orchestration-setup-guide.md exclusively

## Context
- **GitHub Issue**: GREAT-1C (#187) - Verification Phase
- **Current State**: Fresh clone prepared by Code agent
- **Target State**: Operational Piper Morgan following only documentation
- **Dependencies**: Code agent's prepared environment
- **User Data Risk**: None - isolated test environment
- **Infrastructure Verified**: [Verify Code's work per above]

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:
- **"Followed step X"** → Show exact command run and output
- **"Created venv"** → Show `ls -la venv/` and activation proof
- **"Installed dependencies"** → Show pip install output with package counts
- **"Configuration complete"** → Show config file contents
- **"Server started"** → Show server startup logs and port binding
- **"Tests passed"** → Show pytest output with pass counts
- **"Setup successful"** → Show end-to-end functionality test

### Completion Bias Prevention (CRITICAL):
- **Never guess! Always verify first!**
- **Follow docs literally** - don't add steps or skip steps
- **Document gaps** - note missing or unclear instructions
- **Time everything** - track how long each major step takes
- **NO shortcuts** - only what's documented

### Git Workflow Discipline:
No git changes expected in this verification test.

### Documentation Compliance:
```bash
# Track adherence to documentation
# Before each major step, show:
cat docs/guides/orchestration-setup-guide.md | grep -A 5 "Step X"

# After each step, verify:
echo "Step X completed at $(date)"
```

## Constraints & Requirements

### For This Agent
1. **Documentation only**: Use ONLY docs/guides/orchestration-setup-guide.md
2. **No prior knowledge**: Don't fill gaps with assumptions
3. **Document issues**: Note unclear or missing instructions
4. **Time tracking**: Measure setup duration for new developers
5. **Evidence collection**: Terminal output for every command

## Phase 1B Specific Instructions

### Step 1: Navigate to Prepared Environment
```bash
# Move to Code agent's prepared directory
cd /tmp/fresh-clone-verification-*/piper-morgan-product/
pwd
ls -la

# Document starting state
echo "=== STARTING STATE ==="
echo "Virtual env: $VIRTUAL_ENV"
echo "Python version: $(python3 --version)"
echo "Pip version: $(pip3 --version)"
ls -la venv/ || echo "No venv directory (expected)"
ls -la .env || echo "No .env file (expected)"
```

### Step 2: Read Setup Documentation
```bash
# Display the setup guide
cat docs/guides/orchestration-setup-guide.md

# Document guide structure
echo "=== SETUP GUIDE STRUCTURE ==="
grep "^#" docs/guides/orchestration-setup-guide.md
```

### Step 3: Follow Documentation Step-by-Step
**Follow EXACTLY what the documentation says**:

```bash
# Start timer
SETUP_START_TIME=$(date +%s)

# Execute each documented step
# (Will adapt based on actual documentation content)
# Document every command and its output

# Example expected steps (verify against actual docs):
# 1. Python environment setup
# 2. Dependency installation  
# 3. Configuration creation
# 4. Database setup (if needed)
# 5. Verification steps
```

### Step 4: Document Missing Instructions
```bash
# Track any gaps found
echo "=== DOCUMENTATION GAPS FOUND ==="
# Note any steps that were unclear
# Note any missing dependencies
# Note any assumed knowledge
```

### Step 5: Verify Operational State
```bash
# Test that setup actually works
# Based on what documentation says to test

# Example tests (adapt to actual documentation):
python3 main.py --version
python3 -c "import services.orchestration.engine; print('Import successful')"

# End timer
SETUP_END_TIME=$(date +%s)
SETUP_DURATION=$((SETUP_END_TIME - SETUP_START_TIME))
echo "Total setup time: ${SETUP_DURATION} seconds"
```

## Expected Outcomes

### Success Criteria
- [ ] All documented setup steps completed successfully
- [ ] Piper Morgan reaches operational state
- [ ] Setup time measured and reasonable (<30 minutes)
- [ ] Any documentation gaps identified
- [ ] Terminal output evidence for every step

### Measurement Targets
- **Setup time**: Goal <20 minutes for new developer
- **Success rate**: 100% completion following only docs
- **Clarity**: All steps clear without external help
- **Completeness**: No missing dependencies or configuration

### Evidence Package to Provide
1. **Step-by-step execution log**: Every command and output
2. **Setup timing**: Total duration and major milestones
3. **Documentation gaps**: Any unclear or missing instructions  
4. **Final state verification**: Proof system is operational
5. **New developer assessment**: Clarity rating (1-5 scale)

## Cross-Validation with Code Agent
**Coordination points**:
- Confirm Code's environment preparation successful
- Report any issues with prepared environment
- Share setup experience and timing results
- Document any environmental dependencies Code missed

## STOP Conditions
- If Code agent's environment preparation incomplete
- If setup documentation missing or severely incomplete
- If setup fails despite following documentation
- If dependencies cannot be installed

## Success Definition
**Fresh clone reaches operational state following only docs**:
- New developer can complete setup in <30 minutes
- All commands documented work as described
- System functional for basic operations
- No external knowledge required beyond documentation

---

**Mission**: Execute setup documentation exactly as written, measuring new developer experience and documenting any gaps.

**Evidence Standard**: Complete terminal log, timing data, gap analysis, operational verification.

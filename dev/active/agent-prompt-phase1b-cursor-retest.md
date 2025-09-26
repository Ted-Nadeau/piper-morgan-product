# Cursor Agent Prompt: Fresh Clone Re-verification After Documentation Commit

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements  
- METHODOLOGY.md - Inchworm Protocol

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Code Agent's Documentation Commit FIRST
**Before doing ANYTHING else, verify Code successfully committed documentation**:

```bash
# Verify Code completed documentation commit
# Check for recent commits with documentation
git log --oneline -5 | grep -i doc

# Verify key documentation files now exist in repository
git ls-tree HEAD docs/guides/
git ls-tree HEAD docs/testing/
git ls-tree HEAD docs/architecture/
```

**Context**: Previous fresh clone test revealed documentation deployment gap. Code agent deployed to commit today's comprehensive documentation work to repository.

## Session Log Management (CRITICAL)

**Create new session log for re-verification**:
- Create one at: `dev/2025/09/25/2025-09-25-1750-prog-cursor-retest-log.md`
- Document this as "Phase 1B Re-test with Committed Documentation"
- Reference previous test results for comparison

## MANDATORY FIRST ACTIONS

### 1. Create New Fresh Clone Environment
```bash
# Create completely new test environment
cd /tmp
mkdir fresh-clone-retest-$(date +%Y%m%d-%H%M)
cd fresh-clone-retest-*

# Document new clean state  
pwd
ls -la  # Should show empty directory
echo $VIRTUAL_ENV  # Should show nothing
```

### 2. Fresh Clone with Updated Repository
```bash
# Clone repository with committed documentation
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# Verify documentation now accessible
ls -la docs/guides/orchestration-setup-guide.md
ls -la docs/testing/performance-enforcement.md
ls -la docs/architecture/initialization-sequence.md

# Check commit recency
git log --oneline -3
```

## Mission
**Re-test setup following comprehensive documentation committed by Code agent**

**Scope Boundaries**:
- This prompt covers: Fresh clone setup using proper comprehensive documentation
- Compare to previous test: Document improvements in setup experience
- Focus: docs/guides/orchestration-setup-guide.md (the comprehensive guide)

## Context
- **GitHub Issue**: GREAT-1C (#187) - Verification Phase Re-test
- **Previous Test**: 60% success rate, 4 critical gaps, 4 minute setup
- **Documentation Fix**: Code agent committed comprehensive setup guide
- **Target**: Measure improvement in new developer experience
- **Infrastructure Verified**: [Verify Code's commit work per above]

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"Documentation improved"** → Show before/after comparison
- **"Setup faster"** → Show timing comparison with previous test
- **"Issues resolved"** → Show specific problems now fixed
- **"New issues found"** → Document any remaining gaps
- **"Success rate"** → Calculate percentage of functional systems

### Comparison Requirements:
**Previous test baseline**:
- Setup time: 4 minutes, 8 seconds
- Success rate: ~60%
- Issues: Missing pytest, personality_integration module, Python version
- Documentation: docs/internal/development/tools/setup.md

### Shell Command Guidelines for Cursor
- Use single quotes for string literals: 'text' not "text"
- If stuck in quote prompt (>), type closing quote and press Enter
- For complex commands, use simpler syntax or break into steps
- Test shell commands in small increments

## Constraints & Requirements

### For This Agent
1. **New environment**: Don't reuse previous /tmp directory
2. **Comprehensive documentation**: Use docs/guides/orchestration-setup-guide.md
3. **Comparison focus**: Document improvements from previous test
4. **Time tracking**: Measure setup duration for comparison
5. **Gap analysis**: Identify any remaining issues

## Phase 1B Re-test Specific Instructions

### Step 1: Setup Documentation Comparison
```bash
# Compare available documentation
echo "=== DOCUMENTATION COMPARISON ==="
echo "Previous test used: docs/internal/development/tools/setup.md"
echo "Current test using: docs/guides/orchestration-setup-guide.md"

# Show new comprehensive guide structure
cat docs/guides/orchestration-setup-guide.md | head -20
wc -l docs/guides/orchestration-setup-guide.md
```

### Step 2: Execute Comprehensive Setup
```bash
# Start timing
SETUP_START_TIME=$(date +%s)
echo "Setup started at: $(date)"

# Follow comprehensive setup guide step-by-step
# Document every command and output
# Note any improvements from previous experience
```

### Step 3: Address Previous Issues
```bash
# Specifically test previous failure points:

echo "=== TESTING PREVIOUS ISSUE AREAS ==="

# 1. Test pytest installation
echo "Testing pytest installation..."
# Follow documentation for test setup

# 2. Test missing modules
echo "Testing module availability..."
python3 -c "import personality_integration" 2>/dev/null && echo "personality_integration: OK" || echo "personality_integration: MISSING"

# 3. Test Python version compatibility
echo "Testing Python version..."
python3 --version
python3 -c "import asyncio; print('asyncio.timeout available:', hasattr(asyncio, 'timeout'))"

# 4. Test web application startup
echo "Testing web application..."
# Follow documentation for web startup verification
```

### Step 4: Compare Results
```bash
# End timing
SETUP_END_TIME=$(date +%s)
SETUP_DURATION=$((SETUP_END_TIME - SETUP_START_TIME))

echo "=== COMPARISON RESULTS ==="
echo "Previous test: 248 seconds (4m 8s), 60% success"
echo "Current test: ${SETUP_DURATION} seconds, [calculate success %]"
echo "Time improvement: $((248 - SETUP_DURATION)) seconds"
```

## Expected Outcomes

### Success Criteria Comparison
**Previous Test Results**:
- Setup Time: 4m 8s  
- Success Rate: 60%
- Critical Issues: 4 major blocking problems

**Target Improvements**:
- [ ] Setup time reduced (target: <3 minutes)
- [ ] Success rate improved (target: >80%)
- [ ] Critical issues resolved (target: <2 remaining)
- [ ] Documentation clarity improved

### Evidence Package to Provide
1. **Setup timing comparison**: Before/after with improvement metrics
2. **Success rate calculation**: Functional systems percentage
3. **Issue resolution**: Which problems fixed, which remain
4. **Documentation assessment**: Clarity and completeness improvements
5. **New developer experience**: Updated rating and feedback

## Cross-Validation with Previous Test
**Direct comparison points**:
- Does pytest now install correctly?
- Are missing modules resolved?
- Is web application startup functional?
- How much did comprehensive documentation improve experience?

## STOP Conditions
- If fresh clone cannot access committed documentation
- If comprehensive setup guide missing from repository
- If new environment cannot be established
- If setup regresses significantly from previous test

## Success Definition
**Verification phase completion**: Fresh clone reaches higher operational state following committed comprehensive documentation, demonstrating documentation deployment success and improved new developer experience.

---

**Mission**: Re-test setup with committed comprehensive documentation, measuring improvements in new developer experience and identifying remaining gaps.

**Evidence Standard**: Complete before/after comparison, timing improvements, issue resolution status, enhanced documentation assessment.

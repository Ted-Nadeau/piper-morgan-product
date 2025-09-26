# Claude Code Agent Prompt: Fix YAML CI/CD Pipeline Issue

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements  
- METHODOLOGY.md - Inchworm Protocol

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check YAML Issue Scope FIRST
**Before doing ANYTHING else, verify the YAML syntax problem**:

```bash
# Verify the problematic file exists
ls -la .github/workflows/test.yml

# Check YAML validity
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))" 2>&1 || echo "YAML INVALID"

# Show the specific problem area (lines 93-206)
sed -n '90,210p' .github/workflows/test.yml
```

**Context**: CI/CD pipeline cannot parse workflow due to improper Python code indentation within YAML heredoc structure.

## Session Log Management (CRITICAL)

**Continue existing session log**: Use your existing session log from previous phases
- Update with infrastructure blocker resolution task
- Do NOT create new session log

## Mission
**Fix YAML syntax error in GitHub Actions workflow to restore CI/CD functionality**

**Scope Boundaries**:
- This prompt covers ONLY: YAML indentation fix for .github/workflows/test.yml
- NOT in scope: Modifying Python logic or workflow functionality
- Specific issue: Lines 93-206 Python code needs proper YAML indentation

## Context
- **GitHub Issue**: GREAT-1C (#187) - Verification Phase Infrastructure Blocker
- **Current State**: CI/CD pipeline cannot parse workflow file due to YAML syntax
- **Target State**: Valid YAML that CI/CD can process, performance/coverage systems functional
- **Verification requirement**: "All tests pass in CI/CD pipeline" blocked by this issue
- **Infrastructure Critical**: Performance regression and coverage enforcement systems non-functional
- **User Data Risk**: None - syntax fix only

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"YAML fixed"** → Show successful `python -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"`
- **"Indentation corrected"** → Show before/after of problematic lines
- **"Workflow parseable"** → Show GitHub Actions can validate the workflow
- **"CI functional"** → Show workflow runs without parse errors
- **"Committed fix"** → Show `git commit` output with fix

### YAML Structure Requirements:
- All Python code in heredoc must be indented 8 spaces from `run:` key
- Python internal indentation preserved within that 8-space base
- No lines at column 0 within the `run: |` block

## Constraints & Requirements

### For This Agent
1. **Syntax only**: Fix indentation, don't modify Python logic
2. **Preserve functionality**: Maintain all existing workflow behavior
3. **Test before commit**: Verify YAML validity before committing
4. **Evidence collection**: Before/after comparison with validation proof

## YAML Fix Instructions

### Step 1: Backup and Assess Current State
```bash
# Backup the problematic file
cp .github/workflows/test.yml .github/workflows/test.yml.backup

# Show current YAML validation failure
echo "=== CURRENT YAML VALIDATION ==="
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))" 2>&1 || echo "YAML parsing failed as expected"

# Identify the specific problem area
echo "=== PROBLEM AREA (lines 93-206) ==="
sed -n '90,210p' .github/workflows/test.yml
```

### Step 2: Fix Python Code Indentation
```bash
# The issue: Python code in heredoc not properly indented for YAML
# Required: All Python code needs 8-space indentation from 'run:' key

# Fix the indentation using sed or manual editing
# Pattern: Add 8 spaces to all Python lines between << 'PYTHON_SCRIPT' and PYTHON_SCRIPT

# Show the transformation needed:
echo "=== REQUIRED TRANSFORMATION ==="
echo "BEFORE (breaks YAML):"
echo "      - name: Run Performance Regression Tests"
echo "        run: |"
echo "          PYTHONPATH=. python3 << 'PYTHON_SCRIPT'"
echo "import asyncio  # ← NO indentation - breaks YAML"

echo "AFTER (valid YAML):"
echo "      - name: Run Performance Regression Tests"  
echo "        run: |"
echo "          PYTHONPATH=. python3 << 'PYTHON_SCRIPT'"
echo "          import asyncio  # ← 8 spaces - valid YAML"
```

### Step 3: Apply the Fix Systematically
```bash
# Apply indentation fix to all Python lines in the heredoc
# Lines 94-205 need 8-space prefix for YAML compliance

# Use sed to add proper indentation:
sed -i.bak '94,205s/^/        /' .github/workflows/test.yml

# Verify the fix applied correctly
echo "=== AFTER INDENTATION FIX ==="
sed -n '90,210p' .github/workflows/test.yml
```

### Step 4: Validate YAML Syntax
```bash
# Test YAML validity after fix
echo "=== YAML VALIDATION AFTER FIX ==="
python3 -c "import yaml; print('YAML Valid:', yaml.safe_load(open('.github/workflows/test.yml')) is not None)"

# Check for any remaining syntax issues
yamllint .github/workflows/test.yml 2>/dev/null || echo "yamllint not available, manual validation completed"
```

### Step 5: Test GitHub Actions Compatibility
```bash
# If GitHub CLI available, validate workflow
gh workflow list 2>/dev/null && echo "GitHub CLI available for workflow validation" || echo "Manual validation required"

# Show the corrected structure
echo "=== CORRECTED STRUCTURE SAMPLE ==="
sed -n '93,100p' .github/workflows/test.yml
```

### Step 6: Commit the Fix
```bash
# Commit the YAML fix
git add .github/workflows/test.yml
git status
git commit -m "fix: Correct YAML indentation in CI workflow

- Fix Python code indentation in .github/workflows/test.yml
- All Python code in heredoc now properly indented (8 spaces)
- Resolves CI/CD pipeline parse errors blocking verification
- Performance regression and coverage enforcement systems restored

Fixes lines 93-206 YAML syntax errors blocking GREAT-1C verification."

# Show commit evidence
git log --oneline -1
git show --stat HEAD
```

## Expected Outcomes

### Success Criteria
- [ ] YAML file passes syntax validation
- [ ] Python code properly indented within YAML structure  
- [ ] CI/CD pipeline can parse workflow file
- [ ] Performance/coverage enforcement systems accessible
- [ ] GitHub Actions workflow executable
- [ ] Fix committed with clear description

### Evidence Package to Provide
1. **Before/after validation**: YAML parse failure → success
2. **Indentation proof**: Show corrected Python code structure
3. **Commit evidence**: Show successful fix commit
4. **Functionality verification**: CI/CD pipeline operational

## Cross-Validation Preparation
Once YAML fixed, coordinate with Cursor's SSL certificate fix for complete infrastructure resolution.

## STOP Conditions
- If YAML structure more complex than indentation issue
- If Python logic needs modification (out of scope)
- If workflow functionality would be impacted
- If backup and recovery not feasible

## Success Definition
**CI/CD pipeline infrastructure restored**: GitHub Actions workflow parseable, performance regression detection and coverage enforcement systems accessible for verification phase completion.

---

**Mission**: Fix YAML indentation syntax error to restore CI/CD functionality, enabling completion of "All tests pass in CI/CD pipeline" verification requirement.

**Evidence Standard**: YAML validation success, before/after comparison, commit proof, CI/CD accessibility confirmation.

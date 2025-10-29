# Claude Code Prompt: TEST-SMOKE-HOOKS - Add Smoke Tests to Pre-commit Hooks

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

This is your FIRST task in the Haiku 4.5 testing protocol. This is a simple configuration task designed to build confidence in Haiku's capabilities.

## Essential Context
Read these briefing documents first in docs/briefing/:
- BRIEFING-PROJECT.md - What Piper Morgan is
- BRIEFING-CURRENT-STATE.md - Current sprint (A8 Alpha Preparation)
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-METHODOLOGY.md - Inchworm Protocol

---

## HAIKU 4.5 TEST PROTOCOL

**Model**: Use Haiku 4.5 for this task
```bash
claude --model haiku
```

**Why Haiku**: This is a simple configuration task (20-30 min estimate) perfect for testing Haiku's capabilities on straightforward work.

**STOP Conditions** (escalate to PM if triggered):
- ⚠️ 2 failures on same subtask
- ⚠️ Breaks existing tests
- ⚠️ 30 minutes with no meaningful progress
- ⚠️ Architectural confusion

**If STOP triggered**: Report to PM and await decision (continue with Haiku or escalate to Sonnet).

---

## SERENA MCP USAGE (MANDATORY)

Use Serena MCP for efficient code navigation:
- `find_symbol` for locating definitions
- `find_referencing_symbols` for usage tracking
- Avoid reading entire files when possible

**Why This Matters**: 70% context window reduction, critical for Haiku's efficiency.

**Example**:
```bash
# Instead of: cat .pre-commit-config.yaml
# Use: find_symbol for locating relevant sections
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
Before doing ANYTHING else, verify infrastructure:

```bash
# Gameplan assumes:
# - Pre-commit hooks exist (.pre-commit-config.yaml)
# - Smoke tests work (./scripts/run_tests.sh smoke)
# - Smoke tests execute in ~1 second

# Verify reality:
ls -la .pre-commit-config.yaml
ls -la scripts/run_tests.sh
./scripts/run_tests.sh smoke  # Test execution time

# Check execution time
time ./scripts/run_tests.sh smoke
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## Mission
Add smoke tests to pre-commit hooks to provide immediate feedback about basic functionality before commits.

**Scope**: Configuration only - no test modifications needed.

**Why**: Developers should know if basic functionality works before committing (catch import errors, basic issues early).

---

## Context
- **GitHub Issue**: #274 TEST-SMOKE-HOOKS
- **Current State**:
  - ✅ Smoke tests work: `./scripts/run_tests.sh smoke` executes in 1 second
  - ✅ Pre-commit hooks exist: `.pre-commit-config.yaml` has linting, formatting
  - ❌ No smoke test validation in pre-commit workflow
- **Target State**: Smoke tests run automatically before every commit
- **Dependencies**: None (independent of ChromaDB bus error issue)
- **User Data Risk**: None (configuration only)
- **Infrastructure Verified**: [To be confirmed by you]

---

## Evidence Requirements

### For EVERY Claim You Make:
- **"Added to config"** → Show `git diff .pre-commit-config.yaml`
- **"Pre-commit works"** → Show test commit attempt with output
- **"Execution time OK"** → Show `time` output showing <5 seconds
- **"Bypass works"** → Show `git commit --no-verify` succeeds
- **"Tests run"** → Show actual pre-commit output with smoke test results
- **"Committed changes"** → Show `git log --oneline -1` output

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- Show actual terminal output for every verification

---

## Constraints & Requirements

### Configuration Requirements
1. **Add smoke test hook** to `.pre-commit-config.yaml`
2. **Execution time**: Must stay under 5 seconds total for pre-commit
3. **Bypass option**: Allow `git commit --no-verify` for emergency commits
4. **Clear errors**: If smoke tests fail, provide clear error messages
5. **Reliability**: Should work without database/external dependencies

### Suggested Hook Configuration
```yaml
- repo: local
  hooks:
    - id: smoke-tests
      name: Smoke Tests
      entry: ./scripts/run_tests.sh smoke
      language: system
      pass_filenames: false
      stages: [commit]
```

### Testing Requirements
1. **Verify hook runs**: Make a test commit and show pre-commit output
2. **Verify execution time**: Show `time` output for full pre-commit
3. **Verify bypass**: Show `--no-verify` allows commit
4. **Verify failure handling**: Intentionally break import and show clear error

---

## Success Criteria (With Evidence)

- [ ] Infrastructure matches expectations (verified)
- [ ] Smoke test hook added to `.pre-commit-config.yaml` (show diff)
- [ ] Pre-commit executes in <5 seconds (show timing)
- [ ] Test commit succeeds with smoke tests passing (show output)
- [ ] Bypass with `--no-verify` works (show output)
- [ ] Clear error messages when tests fail (show example)
- [ ] All existing pre-commit hooks still work (show full run)
- [ ] Git commits clean (show `git log --oneline -1`)
- [ ] GitHub issue updated with completion checkbox

---

## Deliverables

1. **Modified File**: `.pre-commit-config.yaml` with smoke test hook
2. **Evidence Report**: Terminal outputs showing:
   - Infrastructure verification
   - Hook configuration added
   - Test commit with smoke tests passing
   - Execution time under 5 seconds
   - Bypass option working
   - Example failure message
3. **GitHub Update**: Issue #274 updated with completion
4. **Git Status**: Clean repository with commit

---

## Implementation Guidance

### Step 1: Verify Infrastructure (MANDATORY)
```bash
# Check pre-commit config exists
ls -la .pre-commit-config.yaml

# Check smoke tests work
./scripts/run_tests.sh smoke

# Time the execution
time ./scripts/run_tests.sh smoke
```

### Step 2: Add Hook Configuration
Edit `.pre-commit-config.yaml` to add smoke test hook.

### Step 3: Test Installation
```bash
# Re-install hooks
pre-commit install

# Verify hooks are installed
pre-commit run --all-files
```

### Step 4: Test Commit Workflow
```bash
# Make a trivial change for testing
echo "# test" >> README.md

# Try commit (should run smoke tests)
git add README.md
git commit -m "test: verify smoke tests in pre-commit"

# Show output demonstrating smoke tests ran
```

### Step 5: Test Bypass
```bash
# Verify bypass works
git commit --no-verify -m "test: bypass verification"
```

### Step 6: Test Failure Handling
```bash
# Intentionally break something to test error display
# (then revert)
```

---

## Cross-Validation Preparation

Leave clear markers for verification:
- `.pre-commit-config.yaml` diff showing exact changes
- Test commands to reproduce results
- Expected timing (should be <5 seconds)
- Example outputs for success and failure cases

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. Did I verify infrastructure matches gameplan?
2. Did I provide terminal evidence for configuration changes?
3. Did I test actual commit workflow (not just dry-run)?
4. Did I verify execution time is acceptable?
5. Did I test bypass option?
6. Did I show example failure message?
7. Did I verify git commits with log output?
8. Can another developer use this without issues?

### If Uncertain:
- Run actual test commits yourself
- Show real output, not expected output
- Acknowledge what's not verified yet

---

## Haiku Performance Tracking

**For the PM's Haiku testing analysis**, please note in your completion report:
- Actual time taken (vs 20-30 min estimate)
- Number of attempts required
- Any challenges encountered
- Quality of implementation
- Whether STOP conditions were triggered

This helps evaluate Haiku's viability for similar simple tasks.

---

## Example Evidence Format

```bash
# Infrastructure verification
$ ls -la .pre-commit-config.yaml
-rw-r--r-- 1 user group 1234 Oct 26 15:00 .pre-commit-config.yaml

$ time ./scripts/run_tests.sh smoke
===== test session starts =====
...
===== 5 passed in 0.89s =====
real    0m1.234s

# Configuration changes
$ git diff .pre-commit-config.yaml
+  - repo: local
+    hooks:
+      - id: smoke-tests
+        name: Smoke Tests
+        entry: ./scripts/run_tests.sh smoke
+        language: system
+        pass_filenames: false
+        stages: [commit]

# Test commit with smoke tests
$ git commit -m "test: verify smoke tests"
[INFO] Initializing environment for local.
[INFO] Running: Smoke Tests
===== test session starts =====
===== 5 passed in 0.89s =====
[smoke-tests] PASSED

# Execution timing
$ time pre-commit run --all-files
...
real    0m3.456s (under 5 second target ✓)

# Git commit
$ git log --oneline -1
abc1234 Add smoke tests to pre-commit hooks
```

---

## Related Documentation
- `architectural-guidelines.md` - Architecture principles
- `stop-conditions.md` - When to stop and ask for help
- `tdd-pragmatic-approach.md` - Test-driven development guidance
- `github-guide.md` - GitHub workflow requirements

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:
1. **Verifying infrastructure FIRST** (matches gameplan)
2. Following ALL verification requirements
3. Providing evidence for EVERY claim
4. Using Serena MCP for efficiency
5. Stopping when STOP conditions trigger
6. Tracking Haiku performance for analysis
7. **Never guessing - always verifying first!**

**This is a Haiku testing task. Success builds confidence for more complex work.**

---

*Prompt Version: 1.0*
*Sprint: A8 (Alpha Preparation)*
*Issue: #274 TEST-SMOKE-HOOKS*
*Model: Haiku 4.5*
*Estimated Time: 20-30 minutes*
*Created: October 26, 2025*

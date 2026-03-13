# Claude Code Prompt: CORE-KEYS-STORAGE-VALIDATION - Validate API Keys Before Storage

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

**IMPORTANT CONTEXT**: Issue #274 was completed with Sonnet 4.5 by accident (PM forgot to set model flag). THIS issue (#268) is where the Haiku 4.5 testing protocol actually begins. So while this says "SECOND task," it's really your FIRST Haiku test!

This is a straightforward validation integration task - perfect for testing Haiku's capabilities on simple integration work.

## Essential Context
Read these briefing documents first in docs/briefing/:
- BRIEFING-PROJECT.md - What Piper Morgan is
- BRIEFING-CURRENT-STATE.md - Current sprint (A8 Alpha Preparation)
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-METHODOLOGY.md - Inchworm Protocol

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

**This is critical**. After compaction, get your bearings first.

---

## HAIKU 4.5 TEST PROTOCOL

**Model**: Use Haiku 4.5 for this task
```bash
claude --model haiku
```

**Why Haiku**: Straightforward validation logic (20-30 min estimate). **This is your FIRST real Haiku test** (Issue #274 used Sonnet by accident when PM forgot to set the model flag!).

**Baseline to Beat**: Issue #274 took Sonnet ~10 minutes. Can Haiku match or beat this on similar integration work?

**STOP Conditions** (escalate to PM if triggered):
- ⚠️ 2 failures on same subtask
- ⚠️ Breaks existing tests
- ⚠️ 30 minutes with no meaningful progress
- ⚠️ Architectural confusion

**If STOP triggered**: Report to PM and await decision (continue with Haiku or escalate to Sonnet).

---

## SERENA MCP USAGE (MANDATORY)

Use Serena MCP for efficient code navigation:
- `find_symbol` for locating KeyValidator, UserAPIKeyService
- `find_referencing_symbols` for understanding key storage workflow
- Avoid reading entire files when possible

**Example**:
```bash
# Find where keys are currently stored
find_symbol "store_user_key"
find_referencing_symbols "UserAPIKeyService"
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
Before doing ANYTHING else, verify infrastructure:

```bash
# Gameplan assumes:
# - KeyValidator exists (from Sprint A7 #252)
# - UserAPIKeyService handles key storage
# - Key validation methods available

# Verify reality:
find . -name "*key_validator*" -type f
find . -name "*user_api_key*" -type f
grep -r "class KeyValidator" . --include="*.py"
grep -r "store_user_key" . --include="*.py"

# Check validation infrastructure from #252
ls -la services/security/key_validator.py
ls -la services/security/format_checker.py
ls -la services/security/strength_checker.py
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## Mission
Integrate the KeyValidator (from Sprint A7 #252) into the key storage workflow to prevent weak, invalid, or compromised keys from being stored.

**Scope**: Wire existing validation into storage flow - no new validation logic needed.

**Why**: Users could currently store weak/invalid keys. This prevents security issues by validating before storage.

---

## Context
- **GitHub Issue**: #268 CORE-KEYS-STORAGE-VALIDATION
- **Current State**:
  - ✅ KeyValidator exists (Sprint A7 #252) with 4-layer validation:
    - Format validation
    - Strength analysis
    - Leak detection
    - Provider validation
  - ❌ Validation not integrated into storage workflow
  - ❌ Users can store weak/invalid keys
- **Target State**: All keys validated before storage, with clear error messages
- **Dependencies**:
  - Issue #252 (KeyValidator implementation) - COMPLETE
  - UserAPIKeyService exists
- **User Data Risk**: Low (adds validation, doesn't change storage)
- **Infrastructure Verified**: [To be confirmed by you]

---

## Evidence Requirements

### For EVERY Claim You Make:
- **"Found validation code"** → Show `find_symbol` output and file locations
- **"Integrated validator"** → Show `git diff` of modified files
- **"Validation works"** → Show test output with valid and invalid keys
- **"Error messages clear"** → Show actual error output examples
- **"Tests pass"** → Show pytest output with pass counts
- **"Committed changes"** → Show `git log --oneline -1` output

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- Test with ACTUAL invalid keys, not assumptions

---

## Constraints & Requirements

### Integration Requirements
1. **Use existing KeyValidator** - Don't reimplement validation
2. **Call validation before storage** - In UserAPIKeyService.store_user_key()
3. **Clear error messages** - User should know why key rejected
4. **Don't break existing functionality** - All current tests must pass
5. **Handle all validation failures** - Format, strength, leak, provider

### Validation Flow
```python
async def store_user_key(user_id: str, provider: str, api_key: str):
    # NEW: Validate key before storage
    validator = KeyValidator()
    report = await validator.validate_key(api_key, provider)

    if not report.is_valid():
        # Raise clear exception with specific failure reason
        raise InvalidKeyError(report.get_failure_message())

    # EXISTING: Store key (unchanged)
    await self._store_key(user_id, provider, api_key)
```

### Error Message Requirements
- Format: "Key format invalid: must start with sk-"
- Strength: "Key too weak: entropy 35% (required: 70%)"
- Leak: "Key found in breach database (source: test_pattern)"
- Provider: "API rejected key (status: 401)"

---

## Success Criteria (With Evidence)

- [ ] Infrastructure matches expectations (KeyValidator exists)
- [ ] Found existing validation code (show file paths)
- [ ] Modified storage workflow (show git diff)
- [ ] Validation called before storage (show code)
- [ ] Invalid format rejected (show test with error)
- [ ] Weak key rejected (show test with error)
- [ ] Test/demo key rejected (show test with error)
- [ ] Valid key accepted (show test passing)
- [ ] Clear error messages (show examples)
- [ ] All existing tests pass (show pytest output)
- [ ] New tests added (show test file)
- [ ] Git commits clean (show `git log --oneline -1`)
- [ ] GitHub issue updated

---

## Deliverables

1. **Modified Files**:
   - `services/user/user_api_key_service.py` (add validation call)
   - Possibly: Error handling in calling code
2. **New Tests**:
   - `tests/services/test_key_storage_validation.py`
   - Test invalid format, weak key, test key, valid key
3. **Evidence Report**: Terminal outputs showing:
   - Infrastructure verification
   - Validation integration
   - Test scenarios (valid and invalid keys)
   - Error message examples
   - All tests passing
4. **GitHub Update**: Issue #268 updated with completion
5. **Git Status**: Clean repository with commits

---

## Implementation Guidance

### Step 1: Verify Infrastructure (MANDATORY)
```bash
# Find KeyValidator
find_symbol "KeyValidator"

# Check validation methods exist
grep -r "class KeyValidator" services/ --include="*.py"

# Find storage methods
find_symbol "store_user_key"

# Verify validation layers from #252
ls -la services/security/key_validator.py
ls -la services/security/format_checker.py
ls -la services/security/strength_checker.py
ls -la services/security/leak_detector.py
```

### Step 2: Understand Current Storage Flow
```bash
# Find where keys are stored
grep -r "store_user_key" services/ --include="*.py"

# Check existing tests
grep -r "test.*store.*key" tests/ --include="*.py"
```

### Step 3: Integrate Validation
Modify `UserAPIKeyService.store_user_key()` to call KeyValidator.

### Step 4: Add Error Handling
Ensure validation failures raise clear exceptions.

### Step 5: Write Tests
```python
# Test cases needed:
# 1. Invalid format (wrong prefix)
# 2. Weak key (low entropy)
# 3. Test/demo key (detected as leaked)
# 4. Valid key (passes all checks)
```

### Step 6: Verify All Tests Pass
```bash
# Run new tests
pytest tests/services/test_key_storage_validation.py -v

# Run all existing tests (ensure no regressions)
pytest tests/ -v
```

---

## Test Scenarios (REQUIRED)

### Scenario 1: Invalid Format
```python
# Key: "invalid-key-12345" (wrong prefix)
# Expected: Raise InvalidKeyError with format message
# Message: "Key format invalid: must start with sk-"
```

### Scenario 2: Weak Key
```python
# Key: "sk-" + "a" * 48 (low entropy)
# Expected: Raise InvalidKeyError with strength message
# Message: "Key too weak: entropy 35% (required: 70%)"
```

### Scenario 3: Test Key
```python
# Key: "sk-test-demo-key-12345"
# Expected: Raise InvalidKeyError with leak message
# Message: "Key found in breach database"
```

### Scenario 4: Valid Key
```python
# Key: "sk-" + secrets.token_urlsafe(48)
# Expected: Store successfully, return success
```

---

## Cross-Validation Preparation

Leave clear markers for verification:
- File paths modified with diffs
- Test commands to run
- Expected validation errors for each scenario
- All test outputs included

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. Did I verify KeyValidator exists from #252?
2. Did I integrate validation (not reimplement it)?
3. Did I test all 4 scenarios (format, strength, leak, valid)?
4. Did I show actual error messages?
5. Do all existing tests still pass?
6. Did I provide terminal evidence for claims?
7. Can another developer run my tests?

### If Uncertain:
- Run validation with real invalid keys
- Show actual error output
- Verify existing tests pass

---

## Haiku Performance Tracking

**For the PM's Haiku testing analysis**, please note:
- Actual time taken (vs 20-30 min estimate)
- Number of attempts required
- Any integration challenges
- Quality of error handling
- Whether STOP conditions triggered

---

## Example Evidence Format

```bash
# Infrastructure verification
$ find_symbol "KeyValidator"
Found in: services/security/key_validator.py

$ ls -la services/security/key_validator.py
-rw-r--r-- 1 user group 5678 Oct 23 16:12 services/security/key_validator.py

# Integration changes
$ git diff services/user/user_api_key_service.py
+from services.security.key_validator import KeyValidator
+
 async def store_user_key(self, user_id: str, provider: str, api_key: str):
+    # Validate before storage
+    validator = KeyValidator()
+    report = await validator.validate_key(api_key, provider)
+    if not report.is_valid():
+        raise InvalidKeyError(report.get_failure_message())

# Test with invalid format
$ pytest tests/services/test_key_storage_validation.py::test_invalid_format -v
===== test session starts =====
tests/services/test_key_storage_validation.py::test_invalid_format PASSED
  Error message: "Key format invalid: must start with sk-"

# All tests pass
$ pytest tests/ -v
===== 125 passed in 12.34s =====

# Git commit
$ git log --oneline -1
def4567 Integrate KeyValidator into key storage workflow
```

---

## Related Documentation
- Issue #252 (KeyValidator implementation)
- `services/security/key_validator.py` (validation logic)
- `architectural-guidelines.md` (architecture principles)
- `stop-conditions.md` (when to escalate)

---

## REMINDER: Methodology Cascade

You are responsible for:
1. **Verifying infrastructure FIRST** (KeyValidator exists)
2. **Using existing code** (don't reimplement)
3. Providing evidence for EVERY claim
4. Using Serena MCP for efficiency
5. Testing all scenarios thoroughly
6. Stopping when STOP conditions trigger
7. **Never guessing - always verifying first!**

**This builds on TEST-SMOKE-HOOKS success. Haiku should handle this integration well.**

---

*Prompt Version: 1.0*
*Sprint: A8 (Alpha Preparation)*
*Issue: #268 CORE-KEYS-STORAGE-VALIDATION*
*Model: Haiku 4.5*
*Estimated Time: 20-30 minutes*
*Created: October 26, 2025*

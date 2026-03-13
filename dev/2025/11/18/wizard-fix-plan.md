# Wizard & Status Fix Plan - Nov 18, 2025
## Time: 5:05 PM - Systematic Fix Plan
## Agent: Claude Code (Sonnet 4.5)

---

## Executive Summary

**Goal**: Fix all issues discovered during alfa-romeo (should be alfrick) alpha testing session

**Scope**: 12 distinct issues across wizard, status command, and documentation

**Approach**:
- Use Beads for tracking
- Use Serena for code analysis
- No plan deviations without PM approval
- 100% completion required

---

## Issues Inventory

### Category 1: Wizard - API Key Flow

**Issue #13: Keychain check not visible/working**
- **Symptom**: Code added but doesn't show "✓ Using existing key from keychain"
- **Root Cause**: Exception handling swallowing failures OR keychain empty
- **Priority**: HIGH
- **Files**: `scripts/setup_wizard.py` lines 616-626, 700-710, 769-779
- **Fix**: Add debug logging, verify keychain check actually runs

**Issue #11: Wizard doesn't check keychain before prompting** (CLAIMED FIXED but not working)
- **Symptom**: User has keys in keychain but wizard still asks
- **Root Cause**: Implementation may have bug
- **Priority**: HIGH
- **Files**: `scripts/setup_wizard.py`
- **Fix**: Verify keychain check logic, add visible confirmation

**Issue #8: Environment variable logic** (FIXED for OpenAI, need verify for Anthropic/GitHub)
- **Status**: Believed fixed in commit d81794be
- **Verification needed**: Confirm Anthropic/GitHub match OpenAI pattern
- **Priority**: MEDIUM (verify only)

### Category 2: Wizard - User Account Flow

**Issue #14: Can't reclaim username from incomplete setup**
- **Symptom**: Wizard shows "Found incomplete setup for: alfric" but forces new username
- **Root Cause**: Resume logic broken OR username validation prevents reuse
- **Priority**: MEDIUM
- **Files**: `scripts/setup_wizard.py` user creation section
- **Fix**: Allow resuming with same username OR clean up incomplete users

### Category 3: Wizard - Database Migrations

**Issue #2: Database migrations not running automatically** (CLAIMED FIXED but not verified)
- **Symptom**: user_api_keys.user_id still VARCHAR after wizard runs
- **Status**: Code added in commit d81794be but user still hit VARCHAR error
- **Priority**: CRITICAL
- **Files**: `scripts/setup_wizard.py` lines 990-1009
- **Fix**: Verify migration code actually executes, check for silent failures

### Category 4: Status Command Issues

**Issue #15: Duplicate key retrieval logs**
- **Symptom**: Each provider (openai/anthropic/github) logged twice
- **Evidence**:
  ```
  [debug] Retrieved API key for .../openai from keychain
  [debug] Retrieved API key for .../openai from keychain  # DUPLICATE
  ```
- **Priority**: LOW (cosmetic)
- **Files**: Status command implementation
- **Fix**: Find duplicate keychain call, remove

**Issue #16: 'dict' object has no attribute 'is_active' error**
- **Symptom**: `Failed to check key ages for user ...: 'dict' object has no attribute 'is_active'`
- **Root Cause**: Code expects object but gets dict
- **Priority**: MEDIUM
- **Files**: Status command, key age checking logic
- **Fix**: Handle dict return type OR fix upstream to return object

**Issue #17: Keychain service initialized twice**
- **Symptom**:
  ```
  [info] Keychain service initialized backend=Keyring service_name=piper-morgan
  [info] Keychain service initialized backend=Keyring service_name=piper-morgan  # DUPLICATE
  ```
- **Priority**: LOW (cosmetic, same as wizard)
- **Files**: Keychain service initialization
- **Fix**: Find duplicate initialization, remove

### Category 5: Wizard - Service Checks

**Issue #5: Temporal timeout** (FIXED in latest commit)
- **Status**: Fixed - reduced to 20s, made optional
- **Commit**: Latest (after d81794be)
- **Priority**: DONE ✅

**Issue #4: Port 8001 check TIME_WAIT bug** (FIXED)
- **Status**: Fixed in commit 58ff6269
- **Priority**: DONE ✅

### Category 6: Wizard - Dependencies

**Issue #3: No sqlalchemy dependency check**
- **Symptom**: ImportError if pip install not run
- **Priority**: MEDIUM
- **Files**: `scripts/setup_wizard.py` top of file
- **Fix**: Add try/except on import with helpful message

### Category 7: Documentation

**Issue #18: ALPHA_QUICKSTART.md - .md files not clickable links**
- **Symptom**: "see ALPHA_TESTING_GUIDE.md" renders as text not link
- **Priority**: LOW
- **Files**: `docs/ALPHA_QUICKSTART.md`
- **Fix**: Use proper markdown link syntax: `[ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md)`

### Previously Fixed (Verify Only)

**Issue #1: AlphaUser import** ✅ FIXED commit 7ce48ec4
**Issue #6: Directory name in docs** ✅ FIXED in alpha docs
**Issue #7: Python version in docs** ✅ FIXED in alpha docs

---

## Fix Plan - Prioritized

### Phase 1: CRITICAL - Database Migration (15 min)

**Why Critical**: User still hit VARCHAR error despite fix being in code

**Tasks**:
1. Read `scripts/setup_wizard.py` lines 990-1009
2. Verify migration code is actually reachable
3. Check if subprocess.run is failing silently
4. Add better error logging
5. Test migration actually runs

**Success Criteria**: Migration runs and is visible in wizard output

**Beads Issue**: TBD

---

### Phase 2: HIGH - Keychain Check (30 min)

**Why High**: Core UX issue - users shouldn't re-enter keys

**Tasks**:
1. Use Serena to find `retrieve_user_key` implementation
2. Verify my added code (lines 616-626, 700-710, 769-779) actually executes
3. Check if keychain is actually empty (explain why no keys found)
4. Add visible logging: "Checking keychain for existing keys..."
5. Fix exception handling - don't swallow all errors

**Success Criteria**:
- Wizard shows "Checking keychain..." message
- If key found: "✓ Using existing key from keychain"
- If not found: "No existing key found, checking environment variables..."

**Beads Issue**: TBD

---

### Phase 3: MEDIUM - Username Reclaim (20 min)

**Why Medium**: Annoying UX but not blocking

**Tasks**:
1. Find user account creation code
2. Check resume logic for incomplete setups
3. Determine why "alfric" couldn't be resumed as "alfric"
4. Fix to allow same username OR provide clear cleanup guidance

**Success Criteria**: User can resume with original username

**Beads Issue**: TBD

---

### Phase 4: MEDIUM - Status Command Fixes (30 min)

**Issue #16: 'dict' object has no attribute 'is_active'**

**Tasks**:
1. Use Serena to find "check key ages" code
2. Identify where dict is returned instead of object
3. Fix type handling

**Issue #15 & #17: Duplicate logging**

**Tasks**:
1. Find duplicate keychain initialization
2. Find duplicate key retrieval calls
3. Remove duplicates

**Success Criteria**:
- No 'dict' error
- Each log line appears once

**Beads Issues**: TBD

---

### Phase 5: LOW - Polish (20 min)

**Issue #3: SQLAlchemy import guard**
**Issue #18: Documentation link fix**

**Tasks**:
1. Add import guard with helpful message
2. Fix markdown link in ALPHA_QUICKSTART.md

**Success Criteria**: Better error messages, clickable links

**Beads Issues**: TBD

---

## Execution Protocol

### Before Starting Any Phase:
1. ✅ Create Beads issue for phase
2. ✅ Mark issue as in_progress
3. ✅ Use Serena for code analysis (not manual grep)

### During Phase:
1. ✅ Follow plan exactly - no deviations
2. ✅ If blocker found → STOP, update plan, get PM approval
3. ✅ Document findings in Beads issue

### After Phase:
1. ✅ Test fix manually if possible
2. ✅ Commit with descriptive message
3. ✅ Close Beads issue with evidence
4. ✅ Mark phase complete

### End of All Phases:
1. ✅ Run all tests
2. ✅ Push to origin/main
3. ✅ Update session log with summary
4. ✅ Report completion to PM

---

## Time Estimates

- Phase 1 (Migration): 15 min
- Phase 2 (Keychain): 30 min
- Phase 3 (Username): 20 min
- Phase 4 (Status): 30 min
- Phase 5 (Polish): 20 min
- **Total**: ~115 min (under 2 hours)

---

## Success Metrics

**All issues resolved**:
- [ ] Database migrations run automatically and visibly
- [ ] Keychain check shows visible output
- [ ] Username can be reclaimed from incomplete setup
- [ ] Status command has no duplicate logs
- [ ] Status command handles dict types correctly
- [ ] SQLAlchemy import has helpful error
- [ ] Documentation links are clickable

**Quality Gates**:
- [ ] All unit tests pass
- [ ] Pre-commit hooks pass
- [ ] Pre-push validation passes
- [ ] Manual wizard test passes

---

## Notes for PM

**Current alpha test user**: alfrick / alfrick@dinp.xyz (NOT alfa-romeo, that was Nov 6)

**Today's username progression**:
1. alfric (incomplete)
2. alfrith (incomplete after interim fix)
3. alfrick (successful ✅)

**What's working now**:
- Setup completes with env vars
- Preferences works
- Status shows valid keys
- Core functionality ready for e2e testing

**What needs fixing**: See phases above

---

**Status**: Plan ready for PM approval
**Next**: Await PM go-ahead to execute
**Time**: 5:05 PM

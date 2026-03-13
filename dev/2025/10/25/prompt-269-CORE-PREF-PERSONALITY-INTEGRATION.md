# Claude Code Prompt: CORE-PREF-PERSONALITY-INTEGRATION - Connect Preferences to PersonalityProfile

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

**Context from Previous Issues**:
- ✅ Issue #274: Complete with Sonnet in ~10 min (PM forgot model flag)
- ✅ Issue #268: Complete with Haiku in 19 min - **excellent work!**

This is your SECOND real Haiku test. Issue #268 showed Haiku handles straightforward integration well. Now we test MEDIUM complexity with cross-system integration.

**Complexity Level**: MEDIUM - This tests Haiku's limits. STOP conditions are MORE likely here than #268.

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

**Why Haiku**: Medium complexity integration. Tests if Haiku can handle cross-system integration.

**What We Learned from #268**:
- Haiku beat estimate (19 min on straightforward integration)
- Handled test infrastructure challenges independently
- Quality matched Sonnet
- ~75-80% cost savings

**⚠️ WATCH CLOSELY FOR STOP CONDITIONS** (medium complexity increases likelihood):
- ⚠️ 2 failures on same subtask
- ⚠️ Breaks existing tests
- ⚠️ No meaningful progress (you'll know when you're stuck)
- ⚠️ Architectural confusion (connects wrong systems)

**If STOP triggered**: Report to PM immediately. This is expected - medium complexity tests Haiku's limits. Escalating to Sonnet is fine!

---

## SERENA MCP USAGE (MANDATORY)

Use Serena MCP for efficient code navigation:
- `find_symbol` for locating PersonalityProfile, preference storage
- `find_referencing_symbols` for understanding usage patterns
- This is crucial - multiple files involved

**Example**:
```bash
# Find PersonalityProfile
find_symbol "PersonalityProfile"

# Find preference questionnaire code
find_symbol "run_preference_questionnaire"

# Find where preferences are stored
grep -r "alpha_users.preferences" . --include="*.py"
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
```bash
# Gameplan assumes:
# - PersonalityProfile system exists (Sprint A5)
# - Preference questionnaire works (Sprint A7 #267)
# - Preferences stored in alpha_users.preferences JSONB
# - PersonalityProfile used in response generation

# Verify reality:
find_symbol "PersonalityProfile"
find . -name "*personality*" -type f
grep -r "class PersonalityProfile" . --include="*.py"

# Check preference questionnaire from #267
find . -name "*preferences_questionnaire*" -type f
grep -r "run_preference_questionnaire" . --include="*.py"

# Check database schema
grep -r "alpha_users" models/ --include="*.py"
grep -r "preferences" models/ --include="*.py"
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## Mission
Connect the preference questionnaire (Sprint A7 #267) to the PersonalityProfile system (Sprint A5) so user preferences affect Piper's behavior.

**Scope**: Integration layer only - both systems exist, just need to be connected.

**Why**: Users set preferences via questionnaire, but Piper doesn't apply them yet. This makes preferences functional.

---

## Context
- **GitHub Issue**: #269 CORE-PREF-PERSONALITY-INTEGRATION
- **Current State**:
  - ✅ Preference questionnaire works (Sprint A7 #267)
  - ✅ Preferences stored in `alpha_users.preferences` JSONB
  - ✅ PersonalityProfile system exists (Sprint A5)
  - ❌ Preferences not read by PersonalityProfile
  - ❌ Preferences don't affect behavior
- **Target State**: PersonalityProfile loads and applies user preferences
- **Dependencies**:
  - Issue #267 (Preference questionnaire) - COMPLETE
  - Sprint A5 (PersonalityProfile) - COMPLETE
  - alpha_users table exists with preferences column
- **User Data Risk**: Low (reading existing data, not modifying)
- **Infrastructure Verified**: [To be confirmed by you]

---

## Evidence Requirements

### For EVERY Claim You Make:
- **"Found PersonalityProfile"** → Show file location and class definition
- **"Found preferences storage"** → Show database query/model code
- **"Integrated systems"** → Show git diff of changes
- **"Preferences apply"** → Show test output with different preference values
- **"Behavior changes"** → Show response differences based on preferences
- **"Tests pass"** → Show pytest output
- **"Committed changes"** → Show `git log --oneline -1`

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- Test with ACTUAL user preferences from database

---

## Constraints & Requirements

### Integration Requirements
1. **PersonalityProfile loads preferences** from database on initialization
2. **Applies 5 preference dimensions**:
   - communication_style (concise/balanced/detailed)
   - work_style (structured/flexible/exploratory)
   - decision_making (data-driven/intuitive/collaborative)
   - learning_style (examples/explanations/exploration)
   - feedback_level (minimal/moderate/detailed)
3. **Graceful defaults** if preferences not set (use 'balanced'/'moderate')
4. **Priority order**: Runtime > Database > Defaults
5. **Don't break existing functionality** - all tests must pass

### Expected Integration Points
```python
class PersonalityProfile:
    def __init__(self, user_id: str):
        # NEW: Load preferences from database
        self.preferences = await self._load_user_preferences(user_id)

        # Apply to personality traits
        self.communication_style = self.preferences.get(
            'communication_style',
            'balanced'  # default
        )
        self.work_style = self.preferences.get('work_style', 'flexible')
        # ... other dimensions

    async def _load_user_preferences(self, user_id: str):
        """Load preferences from alpha_users.preferences JSONB"""
        # Query database
        # Return preferences dict or empty dict
```

### Response Generation Integration
```python
def get_response_style_guidance(self) -> str:
    """Generate prompt guidance based on preferences"""
    if self.communication_style == 'concise':
        return "Keep responses brief and to-the-point."
    elif self.communication_style == 'detailed':
        return "Provide comprehensive explanations with examples."
    else:
        return "Balance detail with brevity."
```

---

## Success Criteria (With Evidence)

- [ ] Infrastructure verified (PersonalityProfile and preferences exist)
- [ ] Found PersonalityProfile code (show location)
- [ ] Found preferences storage (show database/model code)
- [ ] Modified PersonalityProfile (show git diff)
- [ ] Loads preferences from database (show code)
- [ ] Applies all 5 dimensions (show code)
- [ ] Graceful defaults work (test with no preferences set)
- [ ] Response guidance changes (test different communication_style values)
- [ ] All existing tests pass (show pytest output)
- [ ] New tests added (show test file)
- [ ] Git commits clean (show git log)
- [ ] GitHub issue updated

---

## Deliverables

1. **Modified Files**:
   - PersonalityProfile class (add preference loading)
   - Possibly: Response generation that uses PersonalityProfile
2. **New Tests**:
   - `tests/services/test_personality_preferences.py`
   - Test all 5 dimensions
   - Test defaults when no preferences
   - Test response guidance changes
3. **Evidence Report**: Terminal outputs showing:
   - Infrastructure verification
   - Preference loading from database
   - Different behaviors based on preferences
   - All tests passing
4. **GitHub Update**: Issue #269 updated
5. **Git Status**: Clean commits

---

## Implementation Guidance

### Step 1: Verify Infrastructure (MANDATORY)
```bash
# Find PersonalityProfile
find_symbol "PersonalityProfile"
ls -la services/personality/

# Find preference questionnaire from #267
find_symbol "run_preference_questionnaire"
ls -la scripts/preferences_questionnaire.py

# Check database model
grep -r "class AlphaUser" models/ --include="*.py"
grep -r "preferences" models/ --include="*.py"
```

### Step 2: Understand Current PersonalityProfile
```bash
# Read PersonalityProfile implementation
find_referencing_symbols "PersonalityProfile"

# See how it's currently used
grep -r "PersonalityProfile" services/ --include="*.py"
```

### Step 3: Add Preference Loading
Modify PersonalityProfile to load from database.

### Step 4: Apply Preferences
Use loaded preferences in response generation.

### Step 5: Write Tests
```python
# Test cases needed:
# 1. Load concise style → Brief responses
# 2. Load detailed style → Comprehensive responses
# 3. No preferences set → Use defaults
# 4. All 5 dimensions applied correctly
```

### Step 6: Verify Integration
```bash
# Test with actual preferences
# Show response differences based on preference changes
```

---

## Test Scenarios (REQUIRED)

### Scenario 1: Concise Communication
```python
# User preference: communication_style = 'concise'
# Expected: Response guidance = "Keep responses brief"
# Verify: Response is actually shorter
```

### Scenario 2: Detailed Communication
```python
# User preference: communication_style = 'detailed'
# Expected: Response guidance = "Provide comprehensive explanations"
# Verify: Response includes examples and detail
```

### Scenario 3: Default Behavior
```python
# User has no preferences set
# Expected: Falls back to 'balanced' defaults
# Verify: Moderate response length
```

### Scenario 4: All Dimensions
```python
# Test that all 5 dimensions are loaded and applied:
# - communication_style
# - work_style
# - decision_making
# - learning_style
# - feedback_level
```

---

## Cross-Validation Preparation

Leave clear markers:
- PersonalityProfile file path and changes
- Database query for preferences
- Test commands showing behavior differences
- Example responses with different preferences

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. Did I verify both systems exist?
2. Did I load preferences from database (not hardcode)?
3. Did I test all 5 dimensions?
4. Did I test defaults when no preferences?
5. Do responses actually change based on preferences?
6. Do all existing tests pass?
7. Am I claiming integration without proof?

### If Uncertain:
- Actually test with different preference values
- Show real response differences
- Verify database query works

---

## ⚠️ MEDIUM COMPLEXITY WARNING

**This is where Haiku might struggle**:
- Multiple systems to understand
- Database queries involved
- Behavioral changes to verify
- Integration points to identify

**Watch for STOP conditions**:
- If you attempt same fix twice → STOP
- If tests break → STOP
- If unclear how systems connect → STOP
- If 30 minutes with no progress → STOP

**It's OK to escalate** - this tests Haiku's limits!

---

## Haiku Performance Tracking

**Critical data point for Haiku analysis**:
- Time taken (vs 30-45 min estimate)
- Integration understanding (correct systems connected?)
- Number of attempts required
- STOP conditions triggered?
- Quality of implementation

**This task determines**: Can Haiku handle medium complexity integration?

---

## Example Evidence Format

```bash
# Infrastructure verification
$ find_symbol "PersonalityProfile"
Found: services/personality/personality_profile.py

$ ls -la services/personality/personality_profile.py
-rw-r--r-- 1 user group 3456 Oct 21 14:20 services/personality/personality_profile.py

# Integration changes
$ git diff services/personality/personality_profile.py
+    async def _load_user_preferences(self, user_id: str):
+        query = "SELECT preferences FROM alpha_users WHERE id = :user_id"
+        result = await session.execute(query, {"user_id": user_id})
+        return result.preferences or {}

# Test with concise preference
$ pytest tests/services/test_personality_preferences.py::test_concise -v
===== test session starts =====
test_concise PASSED
  Guidance: "Keep responses brief and to-the-point."

# Test with detailed preference
$ pytest tests/services/test_personality_preferences.py::test_detailed -v
test_detailed PASSED
  Guidance: "Provide comprehensive explanations with examples."

# All tests pass
$ pytest tests/ -v
===== 127 passed in 13.45s =====

# Git commit
$ git log --oneline -1
ghi7890 Connect preference questionnaire to PersonalityProfile
```

---

## Related Documentation
- Issue #267 (Preference questionnaire)
- Sprint A5 documentation (PersonalityProfile system)
- `services/personality/` directory
- `stop-conditions.md` (when to escalate)

---

## REMINDER: Methodology Cascade

You are responsible for:
1. **Verifying infrastructure FIRST**
2. **Understanding both systems** before connecting
3. Providing evidence for EVERY claim
4. Using Serena MCP for multi-file navigation
5. **Stopping immediately if confused**
6. Testing actual behavior changes
7. **Never guessing - always verifying first!**

**Medium complexity = higher STOP condition likelihood. That's expected and valuable data.**

---

*Prompt Version: 1.0*
*Sprint: A8 (Alpha Preparation)*
*Issue: #269 CORE-PREF-PERSONALITY-INTEGRATION*
*Model: Haiku 4.5*
*Estimated Time: 30-45 minutes*
*Complexity: MEDIUM (watch STOP conditions)*
*Created: October 26, 2025*

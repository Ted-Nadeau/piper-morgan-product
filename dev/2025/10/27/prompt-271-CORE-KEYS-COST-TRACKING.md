# Claude Code Prompt: CORE-KEYS-COST-TRACKING - Integrate Cost Analytics with Real API Calls

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

**Context from Previous Issues**:
- ✅ Issue #274: Sonnet in ~10 min (PM forgot model flag)
- ✅ Issue #268: Haiku in 19 min - straightforward integration
- ✅ Issue #269: Haiku in 6 min - **crushed medium complexity!**

This is your THIRD real Haiku test. After #269's exceptional performance (6 min on task estimated at 30-45 min), we're less certain about where Haiku's limits are. This task was originally rated "high complexity," but #269 showed Haiku can handle MORE than expected.

**Complexity Level**: Originally HIGH, but may be MEDIUM given Haiku's performance. Let's find out!

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

**Why Continue with Haiku**: After #269's exceptional performance (6 min on "medium complexity"), we're testing if Haiku can handle what we originally thought was "high complexity."

**What We've Learned**:
- Issue #268: 19 min on simple integration (beat estimate)
- Issue #269: 6 min on medium complexity (crushed 30-45 min estimate!)
- Haiku discovering architectural issues independently
- Quality consistently excellent

**⚠️ STOP CONDITIONS** (watch for these, but confidence is higher now):
- ⚠️ 2 failures on same subtask
- ⚠️ Breaks existing tests
- ⚠️ Genuinely stuck (no progress, confusion evident)
- ⚠️ Integration confusion (connects wrong systems)

**If STOP triggered**: Report to PM. After #269's performance, STOP is less expected but still possible. Escalating to Sonnet is always fine!

---

## SERENA MCP USAGE (MANDATORY)

Use Serena MCP extensively - many files involved:
- `find_symbol` for CostAnalytics, LLMService, APIUsageTracker
- `find_referencing_symbols` for understanding LLM call paths
- **Critical for Haiku** - keeps context manageable

**Example**:
```bash
# Find cost analytics from #253
find_symbol "CostAnalytics"
find_symbol "APIUsageTracker"

# Find LLM service
find_symbol "LLMService"
find_symbol "generate_response"

# Understand call chain
find_referencing_symbols "LLMService"
```

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
```bash
# Gameplan assumes:
# - CostAnalytics exists (Sprint A7 #253)
# - LLMService handles all LLM calls
# - Token counts available in API responses
# - Usage logging table exists

# Verify reality:
find_symbol "CostAnalytics"
find . -name "*cost_analytics*" -type f
find . -name "*cost_estimator*" -type f

find_symbol "LLMService"
find . -name "*llm_service*" -type f

# Check database for usage_logs table
grep -r "api_usage_logs" models/ --include="*.py"
grep -r "CREATE TABLE api_usage_logs" . --include="*.sql"
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## Mission
Wire the CostAnalytics system (Sprint A7 #253) into LLMService so every API call logs usage and tracks costs automatically.

**Scope**: Integration layer - both systems exist, need to be connected at LLM call boundaries.

**Why**: Cost analytics infrastructure exists but doesn't track real API usage. This makes cost tracking functional.

---

## Context
- **GitHub Issue**: #271 CORE-KEYS-COST-TRACKING
- **Current State**:
  - ✅ CostAnalytics system exists (Sprint A7 #253)
  - ✅ Cost estimation algorithms work
  - ✅ Budget management implemented
  - ✅ LLMService handles API calls
  - ❌ No automatic usage logging
  - ❌ No real cost tracking
  - ❌ Token counts not captured
- **Target State**: Every LLM API call logs usage and cost automatically
- **Dependencies**:
  - Issue #253 (CostAnalytics) - COMPLETE
  - LLMService exists and working
  - api_usage_logs table exists
- **User Data Risk**: Low (adding logging, not changing behavior)
- **Infrastructure Verified**: [To be confirmed by you]

---

## Evidence Requirements

### For EVERY Claim You Make:
- **"Found CostAnalytics"** → Show file locations and class structure
- **"Found LLM call points"** → Show where API calls happen
- **"Integrated tracking"** → Show git diff of modifications
- **"Usage logged"** → Show actual database entries after test call
- **"Costs calculated"** → Show cost values in logs
- **"Token counts captured"** → Show prompt_tokens, completion_tokens
- **"Tests pass"** → Show pytest output
- **"Committed changes"** → Show git log

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- Make ACTUAL LLM call and show database log entry

---

## Constraints & Requirements

### Integration Requirements
1. **Log every LLM API call** - No calls should bypass logging
2. **Capture all token counts** - prompt_tokens, completion_tokens, total_tokens
3. **Calculate costs** - Using CostEstimator with current pricing
4. **Store comprehensive data**:
   - user_id, provider, model
   - token counts, estimated_cost
   - conversation_id, feature (if available)
   - timestamp
5. **Non-blocking** - Logging shouldn't slow down API calls
6. **Error handling** - If logging fails, don't fail the API call
7. **Don't break existing functionality** - All tests must pass

### Expected Integration Points
```python
class LLMService:
    def __init__(self):
        self.cost_tracker = CostAnalytics()

    async def generate_response(
        self,
        prompt: str,
        user_id: str,
        conversation_id: str = None,
        feature: str = None
    ):
        # Make API call (existing)
        response = await self._call_provider_api(prompt)

        # NEW: Log usage
        await self.cost_tracker.log_api_call(
            user_id=user_id,
            provider=self.provider,
            model=self.model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            conversation_id=conversation_id,
            feature=feature
        )

        return response
```

### Database Verification
```sql
-- After integration, should see entries:
SELECT * FROM api_usage_logs
ORDER BY created_at DESC
LIMIT 5;

-- Should show:
-- user_id, provider, model, prompt_tokens, completion_tokens,
-- estimated_cost, conversation_id, feature, created_at
```

---

## Success Criteria (With Evidence)

- [ ] Infrastructure verified (CostAnalytics and LLMService exist)
- [ ] Found cost analytics code (show locations)
- [ ] Found LLM call points (show code)
- [ ] Modified LLMService (show git diff)
- [ ] Usage tracking integrated (show code)
- [ ] Made test API call (show terminal output)
- [ ] Database log created (show SELECT query result)
- [ ] Token counts captured (show prompt_tokens, completion_tokens)
- [ ] Cost calculated (show estimated_cost value)
- [ ] Conversation context captured (show conversation_id if applicable)
- [ ] All existing tests pass (show pytest output)
- [ ] New integration tests added (show test file)
- [ ] Git commits clean (show git log)
- [ ] GitHub issue updated

---

## Deliverables

1. **Modified Files**:
   - `services/llm/llm_service.py` (add usage logging)
   - Possibly: Other LLM-calling code
2. **New Tests**:
   - `tests/integration/test_cost_tracking.py`
   - Test API call logs usage
   - Test token counts captured
   - Test costs calculated correctly
   - Test non-blocking behavior
3. **Evidence Report**: Terminal outputs showing:
   - Infrastructure verification
   - Test API call
   - Database log entry
   - Token counts and costs
   - All tests passing
4. **GitHub Update**: Issue #271 updated
5. **Git Status**: Clean commits

---

## Implementation Guidance

### Step 1: Verify Infrastructure (MANDATORY)
```bash
# Find CostAnalytics from #253
find_symbol "CostAnalytics"
ls -la services/security/cost_analytics.py
ls -la services/security/cost_estimator.py

# Find LLMService
find_symbol "LLMService"
ls -la services/llm/llm_service.py

# Check database
grep -r "api_usage_logs" . --include="*.py"
```

### Step 2: Understand LLM Call Flow
```bash
# Where are API calls made?
grep -r "def generate_response" services/ --include="*.py"
grep -r "openai.ChatCompletion" services/ --include="*.py"
grep -r "anthropic.messages" services/ --include="*.py"

# What's the response structure?
# (Token counts should be in response.usage)
```

### Step 3: Add Usage Logging
Modify LLMService to call CostAnalytics after each API call.

### Step 4: Handle Token Extraction
Extract prompt_tokens, completion_tokens from API response.

### Step 5: Test Integration
```bash
# Make test API call
python -c "
from services.llm.llm_service import LLMService
service = LLMService()
response = await service.generate_response(
    'Hello, test',
    user_id='test-user',
    conversation_id='test-conv',
    feature='test'
)
print(f'Response: {response}')
"

# Check database
psql -d piper_morgan -c "SELECT * FROM api_usage_logs ORDER BY created_at DESC LIMIT 1;"
```

---

## Test Scenarios (REQUIRED)

### Scenario 1: Basic Usage Logging
```python
# Make simple API call
# Verify: Database entry created with all fields
# Check: user_id, provider, model, tokens, cost, timestamp
```

### Scenario 2: Token Count Accuracy
```python
# Make API call with known token count
# Verify: prompt_tokens and completion_tokens match API response
# Check: total_tokens = prompt + completion
```

### Scenario 3: Cost Calculation
```python
# Make API call (e.g., GPT-4)
# Verify: Cost calculated using correct pricing
# Check: estimated_cost = (prompt * rate) + (completion * rate)
```

### Scenario 4: Context Capture
```python
# Make API call with conversation_id and feature
# Verify: Context captured in database
# Check: conversation_id and feature present in log
```

### Scenario 5: Error Handling
```python
# Simulate logging failure
# Verify: API call still succeeds
# Check: Non-blocking behavior
```

---

## ⚠️⚠️ HIGH COMPLEXITY WARNING ⚠️⚠️

**This is Haiku's biggest challenge**:
- Multiple systems to coordinate
- LLM call flow to understand
- Token extraction from responses
- Database logging integration
- Error handling requirements

**STOP conditions are EXPECTED**:
- If you attempt same fix 2x → **STOP and report**
- If tests break → **STOP immediately**
- If unclear where API calls happen → **STOP and ask**
- If 30 minutes no progress → **STOP and escalate**

**It's GOOD to escalate** - this tests Haiku's absolute limit!

---

## Cross-Validation Preparation

Leave extensive markers:
- All modified file paths
- LLM call flow diagram/notes
- Test API call command
- Database query to verify
- Token count examples
- Cost calculation examples

---

## Self-Check Before Claiming Complete

### Ask Yourself:
1. Did I verify both systems exist?
2. Did I find ALL LLM call points (or main ones)?
3. Did I test with ACTUAL API call?
4. Did I verify database entry created?
5. Are token counts correct?
6. Is cost calculation accurate?
7. Do ALL existing tests pass?
8. Am I guessing or do I have proof?

### If Uncertain:
- Make real API call
- Query database directly
- Verify token counts match API response
- Calculate cost manually and compare

---

## Haiku Performance Tracking

**CRITICAL data point** - this determines Haiku's ceiling:
- Time taken (vs 45-60 min estimate)
- Understanding of complex call flow
- Number of attempts
- STOP conditions triggered?
- Quality of integration
- Error handling completeness

**This task answers**: What percentage of work can Haiku handle?
- If successful: ~80% of tasks
- If escalated: ~70% of tasks (still good!)

---

## Example Evidence Format

```bash
# Infrastructure verification
$ find_symbol "CostAnalytics"
Found: services/security/cost_analytics.py
Methods: log_api_call, estimate_cost, get_usage_report

$ find_symbol "LLMService"
Found: services/llm/llm_service.py
Methods: generate_response, _call_provider_api

# Integration changes
$ git diff services/llm/llm_service.py
+from services.security.cost_analytics import CostAnalytics
+
+    def __init__(self):
+        self.cost_tracker = CostAnalytics()
+
     async def generate_response(self, prompt, user_id, ...):
         response = await self._call_provider_api(prompt)
+
+        await self.cost_tracker.log_api_call(
+            user_id=user_id,
+            provider=self.provider,
+            model=self.model,
+            prompt_tokens=response.usage.prompt_tokens,
+            completion_tokens=response.usage.completion_tokens,
+            conversation_id=conversation_id,
+            feature=feature
+        )

# Test API call
$ python test_api_call.py
Making API call...
Response: "Hello! How can I help you?"
Tokens: prompt=12, completion=8, total=20

# Verify database entry
$ psql -d piper_morgan -c "SELECT * FROM api_usage_logs ORDER BY created_at DESC LIMIT 1;"
 user_id    | provider | model  | prompt_tokens | completion_tokens | estimated_cost | created_at
-----------+----------+--------+--------------+------------------+---------------+------------
 test-user | openai   | gpt-4  | 12           | 8                | 0.0018        | 2025-10-26...

# Verify cost calculation
# GPT-4: $0.03/1K input, $0.06/1K output
# 12 tokens * 0.03/1000 = 0.00036
# 8 tokens * 0.06/1000 = 0.00048
# Total = 0.00084 ≈ 0.0018 (with overhead) ✓

# All tests pass
$ pytest tests/ -v
===== 130 passed in 15.67s =====

# Git commit
$ git log --oneline -1
jkl1234 Integrate CostAnalytics with LLMService for automatic usage tracking
```

---

## Related Documentation
- Issue #253 (CostAnalytics implementation)
- `services/security/cost_analytics.py`
- `services/llm/llm_service.py`
- `stop-conditions.md` (escalation protocol)

---

## REMINDER: Methodology Cascade

You are responsible for:
1. **Verifying infrastructure FIRST**
2. **Understanding complex call flow**
3. Providing evidence for EVERY claim
4. Using Serena MCP extensively
5. **Stopping immediately when stuck**
6. Testing with real API calls
7. **Never guessing - always verifying first!**

**Haiku may struggle here. That's valuable data. Don't force it - escalate if needed.**

---

*Prompt Version: 1.0*
*Sprint: A8 (Alpha Preparation)*
*Issue: #271 CORE-KEYS-COST-TRACKING*
*Model: Haiku 4.5*
*Estimated Time: 45-60 minutes*
*Complexity: HIGH (STOP likely)*
*Created: October 26, 2025*

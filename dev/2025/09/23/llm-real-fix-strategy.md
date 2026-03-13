# Real LLM Regression Diagnosis and Fix

## What's Involved

### Phase 1: Understand the Integration (15 min)

**Find the LLM client code**:
```bash
# Locate actual LLM client implementation
cat services/llm/clients/llm_client.py
cat services/llm/config.py

# Find how responses are parsed
grep -A 20 "def.*classify\|def.*parse" services/intent_service/llm_classifier.py
```

**Questions to answer**:
1. Which API is being called? (Anthropic/OpenAI/both)
2. What's the expected response format?
3. How is JSON being parsed?
4. Where are API keys configured?

### Phase 2: Identify What Changed (10 min)

**Git archaeology**:
```bash
# When did it last work?
git log --all --oneline -- services/llm/ services/intent_service/llm_classifier.py

# What changed in that commit range?
git diff <last-working-commit> HEAD -- services/llm/ services/intent_service/llm_classifier.py

# Check for config changes
git diff <last-working-commit> HEAD -- config/ .env*
```

**Possible breaking changes**:
- API client library version updated
- Response format assumptions changed
- Prompt structure modified
- Environment variable renamed
- API endpoint changed

### Phase 3: Reproduce and Debug (10-15 min)

**Run failing test with debug output**:
```bash
# Add print statements or use debugger
PYTHONPATH=. python -m pytest tests/unit/services/intent_service/test_llm_intent_classifier.py::TestLLMIntentClassifier::test_successful_classification_with_high_confidence -v -s

# Check what the actual response is
# Modify llm_classifier.py temporarily to log raw response:
# print(f"Raw LLM response: {response}")
# print(f"Parsed JSON attempt: {json.loads(response)}")
```

**Identify exact failure point**:
- Is API being called at all?
- Is response received?
- What does raw response look like?
- Where does JSON parsing fail?

### Phase 4: Fix Options (15-30 min depending on root cause)

**Option A: API Key Issue** (5 min)
- Check if API keys are set
- Verify key permissions
- Test with explicit key

**Option B: Response Format Changed** (15 min)
- Update parsing logic to match new format
- Adjust JSON extraction
- Update response handler

**Option C: API Client Updated** (20 min)
- Check library version in requirements.txt
- Review migration guide for breaking changes
- Update client usage patterns

**Option D: Prompt Structure** (10 min)
- Review what's being sent to LLM
- Check if response schema specified
- Update prompt to request proper JSON format

## Total Time Estimate

**Best case** (API key or simple config): 30-40 min
**Typical case** (response format change): 45-60 min
**Worst case** (client library breaking change): 60-90 min

## What You Need

**To investigate**:
- Access to codebase (have)
- Git history (have)
- Test execution ability (have)

**To fix**:
- Understanding of what changed (investigation finds this)
- Ability to modify code (have)
- API key if testing live (may or may not have)
- Time to test fix (15-30 min after fix applied)

## Risk Assessment

**Low risk** if:
- It's just parsing logic adjustment
- Config file correction
- Prompt format update

**Medium risk** if:
- API client library needs updating
- Response handling needs rewrite
- Multiple integration points affected

**High risk** if:
- Fundamental API change requires architecture shift
- Multiple services depend on broken behavior
- External API deprecated the endpoint

## Recommendation for Tonight

Given you're near quitting time, here's the decision tree:

**If Code finishes CI fix in next 2 min**:
- Start Phase 1 investigation (15 min)
- If root cause is obvious and simple → fix it
- If root cause is complex → document and stop

**Timeline check at 10:20 PM**:
- Simple fix found? → Complete it (another 15 min)
- Complex issue? → Document thoroughly, fix tomorrow

**Absolute stop time**: 10:30 PM
- Ensures clean handoff regardless
- Prevents rushed fixes to complex issues

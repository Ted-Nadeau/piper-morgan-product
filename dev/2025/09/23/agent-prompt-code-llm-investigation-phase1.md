# Agent Prompt: LLM Regression Investigation - Phase 1

## Mission
Investigate LLM integration to understand root cause of JSON parsing regression. 15-minute time box to determine if this is a simple fix or complex issue.

## Context
- LLM JSON parsing worked previously (regression, not new bug)
- Constructor fix revealed underlying issue
- Error: "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
- 0.00 confidence scores resulting

## Investigation Tasks

### 1. Understand Current LLM Integration (5 min)
```bash
cd /Users/xian/Development/piper-morgan

# Find LLM client implementation
cat services/llm/clients/llm_client.py | head -100

# Check LLM config
cat services/llm/config.py

# See how classifier uses LLM
grep -A 30 "def classify" services/intent_service/llm_classifier.py

# Check response parsing logic
grep -A 20 "json.loads\|json.parse" services/intent_service/llm_classifier.py
```

**Capture**:
- Which API? (Anthropic/OpenAI/both)
- Expected response format?
- How is JSON extracted from response?

### 2. Find What Changed (5 min)
```bash
# Find commits affecting LLM between working and broken
git log --oneline --all -- services/llm/ services/intent_service/llm_classifier.py | head -20

# PM said it worked before - check recent changes
git diff HEAD~10 HEAD -- services/llm/clients/llm_client.py
git diff HEAD~10 HEAD -- services/intent_service/llm_classifier.py

# Check if response format changed
git log -p --all -- services/llm/ | grep -B 5 -A 5 "json\|parse\|response" | head -50
```

**Look for**:
- Response parsing logic changes
- JSON extraction method changes
- API client updates
- Prompt format modifications

### 3. Capture Actual Error (5 min)
```bash
# Run failing test with maximum verbosity
PYTHONPATH=. python -m pytest tests/unit/services/intent_service/test_llm_intent_classifier.py::TestLLMIntentClassifier::test_successful_classification_with_high_confidence -vv -s 2>&1 | tail -50

# Check what the raw response looks like (if possible)
# Look for any debug output or response logging
grep -r "print.*response\|logger.*response" services/intent_service/llm_classifier.py services/llm/
```

**Capture**:
- Exact error message
- Stack trace
- Any raw response data visible
- Line number where parsing fails

## Root Cause Categories

Based on investigation, classify as:

**SIMPLE (can fix tonight)**:
- [ ] JSON extraction logic bug (parsing wrong part of response)
- [ ] Response format assumption changed (need to adjust parser)
- [ ] Prompt needs schema specification (tell LLM to return JSON)

**MODERATE (could fix tonight if clear)**:
- [ ] API client method signature changed
- [ ] Response wrapper format different
- [ ] Missing response validation

**COMPLEX (fix tomorrow)**:
- [ ] API library breaking changes requiring migration
- [ ] Fundamental prompt/response architecture issue
- [ ] Multiple integration points affected

## Evidence Report Format

```
INTEGRATION ANALYSIS:
API Used: [Anthropic | OpenAI | both]
Client Location: [file path]
Response Parsing: [how it works]
Expected Format: [what JSON structure is expected]

WHAT CHANGED:
Last Working: [commit or approximate]
Breaking Change: [specific commit or change]
Change Type: [code | config | library]

ACTUAL ERROR:
Error Message: [exact error]
Failure Point: [file:line]
Raw Response (if visible): [what LLM actually returns]

ROOT CAUSE CLASSIFICATION:
Category: [SIMPLE | MODERATE | COMPLEX]
Specific Issue: [one-line description]

FIX APPROACH:
If SIMPLE: [exact change needed - file:line]
If MODERATE: [approach outline - 2-3 steps]
If COMPLEX: [why complex, what needs investigation tomorrow]

TIME ESTIMATE:
Fix Time: [X minutes]
Confidence: [HIGH | MEDIUM | LOW]
```

## Success Criteria
- Understand LLM integration architecture
- Identify what changed to break it
- Classify as SIMPLE/MODERATE/COMPLEX
- Clear fix approach if SIMPLE
- Clear investigation path if COMPLEX

## Time Box
15 minutes - stop at 10:35 PM regardless of completion

Report findings with classification and recommendation: fix tonight or tomorrow.

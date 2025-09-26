# Agent Prompt: LLM Classifier Failure Investigation

## Mission
Investigate why LLM classifier is producing JSON parsing errors and 0.00 confidence scores. This is blocking test execution independent of import issues.

## Context from Phase 2
**Cursor reported**:
- LLM Classifier failing with JSON parsing errors
- 0.00 confidence scores being returned
- Malformed JSON responses from classifier

**Likely blocking**: Error scenario tests, integration tests that use classification

## Investigation Tasks

### 1. Find LLM Classifier Test Failures
```bash
cd /Users/xian/Development/piper-morgan

# Find test files that use LLM classifier
grep -r "llm.*classif" tests/ --include="*.py" -l
grep -r "LLMClassifier" tests/ --include="*.py" -l

# Look for JSON parsing errors in test output
PYTHONPATH=. python -m pytest tests/ -k "llm or classif" -v 2>&1 | grep -A 5 "JSON\|parse\|confidence"
```

### 2. Examine LLM Classifier Implementation
```bash
# Find the classifier implementation
find services/ -name "*llm*classif*" -o -name "*classifier*" | grep -v __pycache__

# Look at the actual classifier code
cat services/intent_service/llm_classifier.py 2>/dev/null | head -100
cat services/intent_service/llm_classifier_factory.py 2>/dev/null | head -50

# Check for JSON response handling
grep -A 10 "json" services/intent_service/llm_classifier.py 2>/dev/null
grep -A 10 "confidence" services/intent_service/llm_classifier.py 2>/dev/null
```

### 3. Check Configuration
```bash
# Look for LLM configuration
grep -r "LLM.*config\|llm.*key\|openai\|anthropic" config/ --include="*.md" --include="*.yaml" --include="*.json"

# Check environment setup
grep -r "API.*KEY\|LLM" .env* 2>/dev/null

# Look for mock LLM setup in tests
grep -r "mock.*llm\|MockLLM" tests/ --include="*.py" -A 5
```

### 4. Identify Root Cause Pattern
```bash
# Find recent changes to classifier
git log --oneline --all -- "**/llm_classifier*" | head -10

# Check for TODO comments about JSON
grep -r "TODO.*json\|TODO.*parse\|TODO.*confidence" services/intent_service/ --include="*.py"
```

## Analysis Questions

### Root Cause Determination
1. **Is it a configuration issue?** (Missing API keys, wrong endpoints)
2. **Is it a parsing issue?** (LLM returns valid JSON but parser expects different format)
3. **Is it a mock issue?** (Tests expect real LLM but get mock with wrong interface)
4. **Is it incomplete implementation?** (Classifier partially built, TODO comments)

### Scope Assessment
1. **GREAT-1C scope?** (Simple fix like mock setup or config)
2. **Separate issue?** (Requires LLM integration work)
3. **Test-only issue?** (Real classifier works, test setup broken)

## Evidence Requirements

### Investigation Report
```
LLM Classifier Failure Analysis:

Root Cause: [configuration | parsing | mock | incomplete]

Evidence:
1. Failed Tests: [list test names and failure messages]
2. Implementation Status: [complete | partial | broken]
3. Configuration: [present | missing | incorrect]
4. Mock Setup: [exists | missing | wrong interface]

Specific Issues Found:
- [Issue 1 with file:line reference]
- [Issue 2 with file:line reference]
[etc.]

Code Snippets:
[paste relevant code showing the problem]

Recommendation: [fix now in GREAT-1C | create separate issue | needs architectural decision]
```

### Quick Fix Assessment
```
Can this be fixed in GREAT-1C scope?

IF YES:
- What needs to change: [specific files and changes]
- Estimated time: [minutes]
- Risk: [low | medium | high]

IF NO:
- Why out of scope: [requires X which is beyond testing]
- Separate issue needed: [title and description]
- Workaround available: [yes/no - what is it]
```

## Success Criteria
- ✅ Root cause identified with evidence
- ✅ Scope determination (GREAT-1C vs separate issue)
- ✅ If fixable now: specific changes needed
- ✅ If not fixable now: clear issue description for later

## STOP Conditions
- If LLM classifier requires live API access (external dependency)
- If issue is actually in Anthropic/OpenAI SDK integration (beyond our control)
- If fix requires architectural changes to intent system

## The Parallel Strategy
While Cursor fixes imports, you find out if we have ANOTHER blocker or if this is separate work. Either way, we need to know what we're dealing with.

Report findings with specific file references and failure evidence.

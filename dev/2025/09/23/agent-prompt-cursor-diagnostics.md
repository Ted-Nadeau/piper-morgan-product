# Agent Prompt: CI Failures and LLM Regression Diagnostics

## Mission
Quick diagnostic of two blockers: CI failures and LLM JSON parsing regression. Understand root causes before committing to fixes.

## Context
- CI failures blocking Verification Phase
- LLM JSON parsing worked previously (regression, not new bug)
- Need to understand complexity before fixing

## Diagnostic Tasks

### PART A: CI Failure Analysis

**1. Check Recent CI Runs**
```bash
cd /Users/xian/Development/piper-morgan

# Check GitHub Actions status
ls -la .github/workflows/
cat .github/workflows/*.yml | head -50

# Look for recent workflow runs (if gh CLI available)
gh run list --limit 5 2>/dev/null || echo "No gh CLI"

# Check git log for recent commits that might break CI
git log --oneline -10
```

**2. Identify Failure Pattern**
```bash
# What tests are failing in CI?
# Check workflow file for test commands
grep -A 5 "pytest\|python -m pytest" .github/workflows/*.yml

# Are there CI-specific configurations?
cat .github/workflows/*.yml | grep -i "env:\|secrets:\|matrix:"
```

**3. Quick Diagnosis**
```
CI Failure Type: [test failures | config issue | dependency | other]
Affected Tests: [list]
Root Cause: [hypothesis based on evidence]
Fix Complexity: [trivial | moderate | complex]
Estimated Fix Time: [minutes]
```

### PART B: LLM Regression Root Cause

**1. Find What Changed**
```bash
# When did LLM JSON parsing last work?
git log --all --oneline -- "**/llm_classifier.py" | head -10

# Recent changes to LLM-related files
git diff HEAD~5 services/intent_service/llm_classifier.py
git diff HEAD~5 services/llm/

# Check for config changes
git log --oneline -- "config/*" "*.env*" | head -10
```

**2. Check LLM Client Configuration**
```bash
# What LLM client is being used?
grep -r "import.*anthropic\|import.*openai\|from.*llm" services/intent_service/llm_classifier.py

# Check for response parsing code
grep -A 10 "json.loads\|json.parse" services/intent_service/llm_classifier.py

# Look for response format expectations
grep -r "response\|json\|parse" services/llm/config.py
```

**3. Compare Working vs Broken**
```bash
# Find test that shows the regression
PYTHONPATH=. python -m pytest tests/unit/services/intent_service/test_llm_intent_classifier.py -v 2>&1 | grep -A 5 "JSON\|parse"

# Capture actual error
PYTHONPATH=. python -m pytest tests/performance/test_llm_classifier_benchmarks.py::TestLLMClassifierBenchmarks::test_single_classification_latency -v 2>&1 | tail -20
```

**4. Root Cause Hypothesis**
```
What Changed: [code | config | dependency | API]
When: [commit hash or approximate date]
Why Breaking: [specific reason]
Fix Complexity: [trivial | moderate | complex]
Estimated Fix Time: [minutes]
```

## Evidence Format

### CI Diagnostic
```
CI Status: [failing | passing | unknown]
Failure Type: [specific issue]
Recent Changes: [commits that might cause it]
Fix Approach: [what needs to change]
Time Estimate: X minutes
Confidence: [high | medium | low]
```

### LLM Regression Diagnostic  
```
Last Working: [commit or date]
Breaking Change: [specific change]
Error Pattern: [exact error message]
Root Cause: [hypothesis]
Fix Approach: [what needs to change]
Time Estimate: X minutes
Confidence: [high | medium | low]
```

## Success Criteria
- Understand CI failure scope (quick fix or deep issue?)
- Understand LLM regression cause (config or code?)
- Time estimates for fixes
- Confidence level in diagnoses

## Time Box
15 minutes total (7-8 min per diagnostic)

Report findings with clear fix recommendations and time estimates.

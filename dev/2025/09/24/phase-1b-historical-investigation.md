# Agent Prompt: LLM Regression Phase 1B - Historical Investigation

**Mission**: Investigate when LLM JSON parsing last worked and identify what changed to break it.

## Context from Lead Developer
- **Timeline**: LLM JSON parsing worked ~3-4 months ago (July 2024, first month of project)
- **Use case**: Working during PM-011 (analyzing uploaded files)
- **Current failure**: Same JSON parsing now fails with malformed JSON errors
- **API keys**: Still present, so not a missing key issue - something changed in loading/usage

## Investigation Tasks

### 1. Git History Analysis - LLM Related Files
```bash
# Check recent changes to LLM classifier (last 3 months)
git log --oneline --since="3 months ago" services/intent_service/llm_classifier.py

# Check changes to LLM client infrastructure
git log --oneline --since="3 months ago" services/llm/

# Look for commits mentioning JSON parsing or LLM fixes
git log --grep="json\|JSON\|llm\|LLM" --oneline --since="3 months ago"

# Check for API key or configuration changes
git log --oneline --since="3 months ago" -- .env.example config/

# Look for dependency changes that might affect LLM clients
git log --oneline --since="3 months ago" -- requirements.txt pyproject.toml
```

### 2. Find When LLM Tests Last Passed
```bash
# Look for test additions or modifications
git log --oneline --since="3 months ago" tests/regression/test_queryrouter_lock.py
git log --oneline --since="3 months ago" tests/performance/

# Check for test configuration changes
git log --oneline --since="3 months ago" pytest.ini pyproject.toml

# Look for any test-specific LLM mocking changes
git log --oneline --since="3 months ago" tests/ | grep -i "llm\|mock"
```

### 3. Identify Breaking Changes Pattern
```bash
# Get detailed diff for key timeframe (July to now)
git log --pretty=format:"%h %ad %s" --date=short --since="2024-07-01" services/intent_service/llm_classifier.py

# Look at actual code changes in LLM classifier
git show --stat $(git log --oneline --since="3 months ago" services/intent_service/llm_classifier.py | head -5 | cut -d' ' -f1)

# Check if there were environment loading changes
git diff HEAD~50 HEAD -- .env.example

# Look for requirements.txt changes (API client version bumps?)
git diff HEAD~30 HEAD -- requirements.txt | grep -i "anthropic\|openai"
```

### 4. Search for Historical JSON Parsing Solutions
```bash
# Look for past JSON parsing fixes or workarounds
git log --grep="parse\|json.*error\|malformed" --oneline

# Search for confidence score related changes
git log --grep="confidence\|0.00" --oneline

# Check for past LLM integration fixes
git log --grep="llm.*fix\|llm.*error" --oneline

# Look for PM-011 related commits (when it was working)
git log --grep="PM-011" --oneline
```

### 5. Configuration Archaeology
```bash
# Check how .env loading has changed
git log -p --since="3 months ago" -- .env.example | head -100

# Look for configuration loading changes in main.py or app startup
git log --oneline --since="3 months ago" main.py web/app.py

# Check if there were changes to how tests load environment
git log --oneline --since="3 months ago" tests/conftest.py tests/fixtures/
```

## Evidence Collection Requirements

### Historical Timeline Report
```
=== LLM Component Change Timeline ===

LLM Classifier Changes (last 3 months):
[List commits with dates - most recent first]

LLM Client Infrastructure Changes:
[List commits with dates]

Key Configuration Changes:
[List commits affecting .env, requirements.txt, etc.]

Test Framework Changes:
[List commits affecting test setup/configuration]
```

### Breaking Change Analysis
```
=== Potential Breaking Changes Identified ===

API Client Version Changes:
- requirements.txt changes: [list any anthropic/openai version changes]
- New dependencies added: [list any new LLM-related deps]

Environment Loading Changes:
- .env.example changes: [any new patterns or removed variables]
- Configuration loading modifications: [changes to how env vars loaded]

Test Setup Changes:
- pytest configuration: [any changes to test environment setup]
- Mock/fixture changes: [changes affecting LLM mocking in tests]
```

### Working State Evidence
```
=== When It Last Worked ===

PM-011 Related Commits:
[List commits mentioning PM-011 when LLM parsing worked]

Last Known Working Timeframe:
- Approximate date: [based on git history]
- Last good commit: [if identifiable]
- Context: [what was being implemented when it worked]

Working Configuration Pattern:
[Any evidence of how LLM was configured when working]
```

### Prime Suspects for Investigation
```
=== Most Likely Breaking Changes ===

Top 3 Suspect Changes:
1. [Most recent significant change with evidence]
2. [Second most likely change with reasoning]
3. [Third candidate with rationale]

Recommended Investigation Priority:
[Which changes to investigate first based on evidence]
```

## Success Criteria
- [ ] Timeline of LLM-related changes established
- [ ] Potential breaking changes identified
- [ ] Last known working state approximated
- [ ] Investigation priorities ranked by likelihood

## Time Estimate
20-25 minutes for complete historical analysis

## Critical Questions to Answer
1. **When exactly** did the LLM parsing stop working? (commit range)
2. **What changed** around that time? (configuration, dependencies, code)
3. **How was it working** before? (what configuration enabled it)
4. **What broke** the working pattern? (specific change that caused regression)

**Report findings with specific commit hashes and change evidence - this will guide Phase 2 root cause identification.**

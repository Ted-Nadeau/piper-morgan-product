# Gameplan: LLM Regression Root Cause Analysis & Fix

**Date**: September 24, 2025  
**Issue**: LLM JSON parsing regression blocking GREAT-1C performance tests  
**Architect**: Claude Opus 4.1  
**Lead Developer**: [To be assigned]

---

## Critical Context: This is a REGRESSION, Not Incomplete Work

### What We Know
- **LLM JSON parsing WORKED months ago** (PM confirmation)
- **API keys WORKED in the past** (PM confirmation)
- **Performance tests ran successfully before**
- **Current state**: `LowConfidenceIntentError` due to malformed JSON
- **Quick fix rejected**: Mocking hides the problem, doesn't fix it

### The Mission
Find out WHAT changed and WHY it broke. Fix the root cause, not the symptom.

---

## Infrastructure Verification Checkpoint

### Expected Configuration Points
```yaml
API Keys Could Be In:
- Environment variables: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
- Config files: config/PIPER.user.md or config/api_keys.yaml
- Secrets management: .env file or cloud secrets
- Test config: tests/config/ or pytest fixtures

JSON Parsing Lives In:
- services/intent_service/llm_classifier.py
- services/intent_service/llm_classifier_factory.py
- Parsing utilities in services/utils/
```

### PM Verification Before Starting
```bash
# Check current API key configuration
grep -r "API.*KEY" config/ --include="*.md" --include="*.yaml" 2>/dev/null | head -10

# Check environment setup
cat .env.example 2>/dev/null
ls -la .env 2>/dev/null

# Check test configuration
ls -la tests/config/ tests/fixtures/ 2>/dev/null

# See if keys are in environment now
env | grep -i "api.*key" | wc -l  # Should be >0 if configured
```

---

## Phase 1: Current State Analysis (30 min)

### Both Agents Together

#### 1A. Verify the Regression
```bash
# Run the failing test to see exact error
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

# Capture the full error message
# Look for: LowConfidenceIntentError, JSON parsing errors, API errors
```

#### 1B. Check Current Key Loading
```python
# In Python, check how keys are loaded now:
from services.intent_service.llm_classifier_factory import LLMClassifierFactory
from services.intent_service.llm_classifier import LLMClassifier
import os

# How does it try to get keys?
print("Environment keys:", [k for k in os.environ if 'API' in k.upper()])

# Try to instantiate
try:
    classifier = LLMClassifierFactory.create_classifier("production")
    print("Classifier created successfully")
except Exception as e:
    print(f"Failed: {e}")
    print(f"Type: {type(e)}")
```

#### 1C. Document Current Failure Mode
Create a clear problem statement:
- Exact error message
- Where it fails (file:line)
- What it's trying to do
- What configuration it expects

---

## Phase 2: Historical Investigation (45 min)

### Deploy: Code for Git History, Cursor for File Analysis

#### Code Instructions - Find When It Broke
```markdown
Investigation: When did LLM tests last work?

1. Git history on key files:
   ```bash
   git log --oneline -20 services/intent_service/llm_classifier.py
   git log --oneline -20 services/intent_service/llm_classifier_factory.py
   git log --oneline -20 tests/regression/test_queryrouter_lock.py
   ```

2. Look for commits mentioning:
   - API keys
   - JSON parsing
   - LLM configuration
   - Test fixes or breaks

3. Find the last known working state:
   ```bash
   # Check commits from last 30 days
   git log --since="30 days ago" --grep="LLM\|API\|JSON" --oneline
   ```

4. Identify potential breaking changes:
   - Config file restructuring
   - Environment variable renames
   - API client upgrades
   - Test infrastructure changes
```

#### Cursor Instructions - Configuration Archaeology  
```markdown
Investigation: How SHOULD keys be configured?

1. Check configuration files:
   - config/PIPER.user.md - look for API key sections
   - config/*.yaml - any API configurations
   - .env.example - expected environment variables
   - tests/fixtures/config.py - test-specific config

2. Find key loading code:
   - Where are keys retrieved from environment?
   - Any fallback mechanisms?
   - Test vs production differences?

3. Check for configuration changes:
   ```bash
   git diff HEAD~30 config/
   git diff HEAD~30 .env.example
   ```

Document EXACT configuration expected vs what exists.
```

### Cross-Validation Point
- Do both agents agree on when it last worked?
- Is the configuration mechanism consistent?
- Any conflicting information about how keys should load?

---

## Phase 3: Root Cause Identification (30 min)

### Both Agents - Systematic Debugging

#### 3A. Test Key Loading Mechanism
```python
# Create minimal test script: test_api_keys.py
import os
from pathlib import Path

print("=== API Key Loading Test ===")

# Method 1: Environment variables
env_keys = {k: v[:10] + "..." for k, v in os.environ.items() if 'API' in k.upper()}
print(f"Environment keys found: {env_keys}")

# Method 2: Config files
config_path = Path("config/PIPER.user.md")
if config_path.exists():
    content = config_path.read_text()
    if "api" in content.lower():
        print("API references found in config")

# Method 3: .env file
env_file = Path(".env")
if env_file.exists():
    print(".env file exists")
    # Don't print contents for security

# Method 4: Test the actual loading
try:
    # Import the actual loading mechanism
    from config.api_config import load_api_keys  # or wherever it is
    keys = load_api_keys()
    print(f"Keys loaded: {list(keys.keys())}")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"Loading failed: {e}")
```

#### 3B. Test JSON Parsing Directly
```python
# Create minimal test: test_json_parsing.py
from services.intent_service.llm_classifier import LLMClassifier

# Mock response that should work
test_response = '{"intent": "CREATE_TASK", "confidence": 0.95}'

# Try parsing
try:
    parsed = LLMClassifier._parse_response(test_response)  # or appropriate method
    print(f"Parsing successful: {parsed}")
except Exception as e:
    print(f"Parsing failed: {e}")
    
# Now try with actual API if keys exist
if os.environ.get("OPENAI_API_KEY"):
    classifier = LLMClassifier()
    result = classifier.classify("Create a GitHub issue about the bug")
    print(f"Live test: {result}")
```

---

## Phase 4: Fix Implementation (45 min)

### Based on Root Cause Found

#### If Keys Not Loading:
```bash
# Option 1: Fix environment
export OPENAI_API_KEY="sk-..."  # Set properly
export ANTHROPIC_API_KEY="..."

# Option 2: Fix config file
echo "api_keys:" >> config/test_config.yaml
echo "  openai: ${OPENAI_API_KEY}" >> config/test_config.yaml

# Option 3: Fix .env file
echo "OPENAI_API_KEY=sk-..." >> .env
```

#### If JSON Parsing Changed:
```python
# Fix parsing logic in llm_classifier.py
# Update response format handling
# Ensure backward compatibility
```

#### If Dependencies Changed:
```bash
# Check and fix package versions
pip list | grep -E "openai|anthropic|json"
pip install openai==1.x.x  # Correct version
```

---

## Phase 5: Verification (15 min)

### Both Agents - Confirm Fix Works

1. **Run Original Failing Test**
   ```bash
   PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs
   ```
   **Must show**: PASSED

2. **Run All Performance Tests**
   ```bash
   PYTHONPATH=. python -m pytest tests/performance/ -v
   ```
   **Must show**: No JSON parsing errors

3. **Verify Production Unaffected**
   ```bash
   # Start the service
   python main.py
   
   # Test via API
   curl -X POST http://localhost:8001/api/intent \
       -d '{"message": "Create a task"}' \
       -H "Content-Type: application/json"
   ```
   **Must show**: Successful response

---

## Phase Z: Documentation & Handoff

### Document the Fix

1. **Create Fix Report**
   ```markdown
   ## LLM Regression Fix - Sept 24, 2025
   
   ### Root Cause
   [Exact cause found]
   
   ### What Changed
   [Specific change that broke it]
   
   ### Fix Applied
   [Exact fix implemented]
   
   ### Files Modified
   - [List all files changed]
   
   ### Tests Verified
   - [List all tests now passing]
   
   ### Prevention
   [How to prevent this regression in future]
   ```

2. **Update Documentation**
   - Add to troubleshooting guide if needed
   - Update config documentation
   - Add to test README if test-specific

3. **GitHub Update**
   ```bash
   gh issue comment 187 --body "LLM regression fixed. Root cause: [cause]. All performance tests now passing."
   ```

---

## Success Criteria

- [ ] Exact root cause identified (not just "keys missing")
- [ ] Historical breaking point found (when it stopped working)
- [ ] Fix addresses root cause (not bandaid/mock)
- [ ] Performance test passes (<500ms)
- [ ] All related tests pass
- [ ] Production unaffected or improved
- [ ] Documentation updated
- [ ] GitHub issue updated with evidence

---

## STOP Conditions

- If "fix" would break production
- If root cause indicates bigger architectural problem
- If regression is actually multiple regressions
- If fix would take >4 hours (reassess approach)

---

## Remember: No Shortcuts

The Lead Dev report showed Code wanted to "just mock it" - that's not acceptable. We need:
1. Real understanding of what broke
2. Real fix that restores functionality
3. Real tests with real API calls
4. Real evidence it works

This is the Inchworm way: complete, thorough, locked.

---

*Investigate thoroughly, fix properly, verify completely.*
# Agent Prompt: Phase 2A - Current Prompt Debugging and Fix Implementation

**Agent**: Code  
**Mission**: Debug current LLM classifier prompt construction, test API responses, and implement JSON formatting fix.

## Context from Phase 1
- **Root Cause**: Anthropic returning `{category: "value"}` instead of `{"category": "value"}`
- **Infrastructure Status**: All working (keys load, clients work, parsing works with valid JSON)
- **PM Direction**: Fix Anthropic API interaction properly, no shortcuts or fallbacks
- **Historical Context**: Worked in PM-011 (June 2025), broke sometime July-August 2025

## Phase 2A Investigation Tasks

### 1. Debug Current Prompt Construction
```python
# Examine how prompts are built for Anthropic API
from services.intent_service.llm_classifier import LLMClassifier
import inspect

print("=== Current LLM Classifier Analysis ===")

classifier = LLMClassifier()

# Get the classification method source
if hasattr(classifier, 'classify'):
    method_source = inspect.getsource(classifier.classify)
    print("Classification method source:")
    print(method_source)

# Look for prompt-building methods
prompt_methods = [attr for attr in dir(classifier) if 'prompt' in attr.lower() or 'template' in attr.lower() or 'format' in attr.lower()]
print(f"Prompt-related methods/attributes: {prompt_methods}")

# Examine each prompt-related attribute
for method_name in prompt_methods:
    try:
        method = getattr(classifier, method_name)
        if callable(method):
            print(f"\n{method_name} (method):")
            print(inspect.getsource(method))
        else:
            print(f"\n{method_name} (attribute): {method}")
    except Exception as e:
        print(f"Could not examine {method_name}: {e}")

# Look for system prompt or message construction
if hasattr(classifier, '_build_prompt') or hasattr(classifier, '_format_message'):
    print("Found prompt building methods")
```

### 2. Test Current API Interaction
```python
# Capture what's actually being sent to Anthropic API
import os
from services.intent_service.llm_classifier import LLMClassifier

print("=== API Interaction Test ===")

# Test with a simple message
test_message = "Create a GitHub issue about the login bug"
print(f"Testing classification of: '{test_message}'")

try:
    classifier = LLMClassifier()
    
    # Try to classify and capture detailed error
    result = classifier.classify(test_message)
    print(f"SUCCESS - Classification result: {result}")
    
except Exception as e:
    print(f"FAILED - Error: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # Try to get raw response if available
    if hasattr(e, 'response'):
        print(f"Raw API response: {e.response}")
    
    # Look at the full traceback
    import traceback
    print("Full traceback:")
    traceback.print_exc()
```

### 3. Examine LLM Client Configuration
```python
# Check how the LLM client is configured and called
from services.llm.clients import llm_client

print("=== LLM Client Configuration ===")

# Look at client structure
print(f"LLM client type: {type(llm_client)}")
print(f"LLM client attributes: {[attr for attr in dir(llm_client) if not attr.startswith('_')]}")

# Check if there's a complete() method or similar
if hasattr(llm_client, 'complete'):
    print("Found complete() method")
    print(inspect.getsource(llm_client.complete))

# Test direct API call with explicit JSON instruction
test_prompt = """You are an intent classifier. Classify this user message.

User message: "Create a GitHub issue about the login bug"

IMPORTANT: Respond with valid JSON only. All property names must be in double quotes.

Required format:
{
    "category": "task_management",
    "action": "create_issue", 
    "confidence": 0.95
}"""

print(f"\n=== Testing Enhanced Prompt ===")
print("Enhanced prompt:")
print(test_prompt)

try:
    # Make direct API call to test prompt fix
    response = llm_client.complete(test_prompt)
    print(f"API Response: {response}")
    
    # Test if it parses as valid JSON
    import json
    parsed = json.loads(response)
    print(f"JSON Parse Success: {parsed}")
    
except Exception as e:
    print(f"Enhanced prompt test failed: {e}")
```

### 4. Implement JSON Format Fix
```python
# Based on findings, implement the fix in the actual classifier

# First, create a backup of current method
import shutil
shutil.copy('services/intent_service/llm_classifier.py', 'services/intent_service/llm_classifier.py.backup')

print("=== Implementing JSON Format Fix ===")

# After examining the code structure, implement the specific fix needed
# This will depend on how prompts are constructed, but likely involves:

# Option A: Fix system prompt
# Option B: Fix user message formatting  
# Option C: Add JSON schema specification

print("Fix implementation will be based on findings from steps 1-3")
```

### 5. Verify Fix with Performance Test
```bash
# Run the failing performance test to verify fix
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

# Should show:
# - PASSED status
# - Timing under 500ms
# - No JSON parsing errors
```

## Evidence Collection Requirements

### Current State Analysis
```
=== Current Prompt Structure ===
Classification Method: [source code of classify method]
Prompt Building: [how prompts are constructed]
System Message: [current system prompt if any]
User Message Format: [how user input is formatted]

JSON Instructions Present: [yes/no with details]
API Client Used: [Anthropic client details]
```

### API Response Testing
```
=== API Response Analysis ===
Test Message: "Create a GitHub issue about the login bug"

Current Prompt Results:
- API Response: [actual raw response]
- JSON Valid: [yes/no]
- Parsing Error: [specific error if any]

Enhanced Prompt Results:
- Enhanced Prompt: [full prompt with JSON instructions]
- API Response: [response with enhanced prompt]
- JSON Valid: [yes/no]
- Parsing Success: [parsed result]
```

### Fix Implementation
```
=== Fix Applied ===
Root Cause Found: [specific missing JSON instruction]
File Modified: services/intent_service/llm_classifier.py
Method/Line Modified: [specific location]

Before (broken):
[current prompt structure]

After (fixed):
[enhanced prompt structure with JSON formatting]

Backup Created: services/intent_service/llm_classifier.py.backup
```

### Verification Results
```
=== Performance Test Results ===
Test Command: pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

Results:
- Status: [PASSED/FAILED]
- Timing: [actual ms] vs 500ms requirement
- JSON Parsing: [working/failing]
- Error Messages: [any remaining errors]
```

## Success Criteria
- [ ] Current prompt construction fully analyzed
- [ ] API response captured and malformed JSON confirmed
- [ ] Enhanced prompt tested with valid JSON response
- [ ] Fix implemented in LLM classifier
- [ ] Performance test passes with <500ms timing
- [ ] No JSON parsing errors remain

## Time Estimate
25-30 minutes for complete debugging, fix implementation, and verification

## Critical Requirements
- **No shortcuts**: Debug the actual Anthropic interaction thoroughly
- **Proper JSON**: Fix must ensure valid JSON responses from Anthropic
- **Evidence-based**: All changes must be based on actual API response testing
- **Verification**: Must pass the original failing performance test

**Focus on systematic debugging to understand exactly why Anthropic is returning malformed JSON, then fix it properly.**

# Agent Prompt: Phase 2 - JSON Prompt Investigation and Fix

**Mission**: Debug and fix Anthropic API interaction to return valid JSON instead of malformed JavaScript-style objects.

## Context from Phase 1
- **Root Cause Confirmed**: Anthropic returning `{category: "value"}` instead of `{"category": "value"}`
- **Infrastructure Status**: All components work (keys, clients, parsing) 
- **Historical Context**: Worked in PM-011 (June 2025) with proper JSON responses
- **PM Direction**: Fix the Anthropic API interaction properly, no shortcuts or fallbacks

## Phase 2 Investigation Tasks

### 1. Capture Current Prompt Structure
```python
# Find and examine the current LLM classification prompt
from services.intent_service.llm_classifier import LLMClassifier
import json

# Instantiate classifier to examine prompt structure
classifier = LLMClassifier()

# Look for prompt template or system message
print("=== Current LLM Classifier Analysis ===")

# Check for prompt/system message attributes
attributes = [attr for attr in dir(classifier) if 'prompt' in attr.lower() or 'system' in attr.lower() or 'template' in attr.lower()]
print(f"Prompt-related attributes: {attributes}")

# Check for classification method to understand prompt construction
if hasattr(classifier, 'classify'):
    import inspect
    method_source = inspect.getsource(classifier.classify)
    print("Classification method found - examining source structure")
    
# Look for where the prompt is built for Anthropic API
for attr in ['system_prompt', 'prompt_template', '_build_prompt', '_format_prompt']:
    if hasattr(classifier, attr):
        print(f"Found {attr} attribute")
        try:
            value = getattr(classifier, attr)
            if callable(value):
                print(f"{attr} is a method")
            else:
                print(f"{attr} content: {value[:200]}..." if len(str(value)) > 200 else f"{attr} content: {value}")
        except Exception as e:
            print(f"Could not access {attr}: {e}")
```

### 2. Test Current API Call with Debug Output
```python
# Make a test classification call with verbose output
import os
from services.intent_service.llm_classifier import LLMClassifier

# Enable any debug logging if available
test_message = "Create a GitHub issue about the login bug"

print("=== API Call Debug Test ===")
print(f"Testing with message: '{test_message}'")

try:
    classifier = LLMClassifier()
    
    # Try to intercept or log the raw API response
    # Check if there's a debug mode or way to capture raw response
    result = classifier.classify(test_message)
    print(f"Classification result: {result}")
    
except Exception as e:
    print(f"Classification failed: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # Try to get more details about the API response
    if hasattr(e, 'response') and e.response:
        print(f"Raw API response: {e.response}")
```

### 3. Compare with Historical Working Version (PM-011)
```bash
# Get the working PM-011 LLM classifier version
git show 6861995b:services/intent_service/llm_classifier.py > /tmp/working_llm_classifier.py

# Compare current vs working version for prompt differences
diff services/intent_service/llm_classifier.py /tmp/working_llm_classifier.py

# Look specifically for system prompt or JSON instruction changes
grep -A 10 -B 5 -i "json\|system.*prompt\|response.*format" /tmp/working_llm_classifier.py

# Check the working LLM client structure
git show 6861995b:services/llm/ --name-only
git show 6861995b:services/llm/clients.py
```

### 4. Examine Current vs Required JSON Instructions
```python
# Test if current prompts include JSON format instructions
sample_prompts = [
    # Check if any of these patterns exist in current code
    "respond with valid JSON",
    "return JSON format", 
    "output must be JSON",
    "response format: JSON",
    '"category":', 
    'confidence":',
    "structured response"
]

# Search for JSON formatting instructions in current classifier
from services.intent_service.llm_classifier import LLMClassifier
import inspect

classifier = LLMClassifier()
source_code = inspect.getsource(classifier.__class__)

print("=== JSON Instruction Analysis ===")
for pattern in sample_prompts:
    if pattern.lower() in source_code.lower():
        print(f"✅ Found pattern: '{pattern}'")
    else:
        print(f"❌ Missing pattern: '{pattern}'")

# Look for the actual system prompt or user prompt construction
lines = source_code.split('\n')
for i, line in enumerate(lines):
    if any(keyword in line.lower() for keyword in ['prompt', 'system', 'json', 'format']):
        context_start = max(0, i-2)
        context_end = min(len(lines), i+3)
        print(f"\nLines {context_start+1}-{context_end}: Context around JSON/prompt")
        for j in range(context_start, context_end):
            prefix = ">>> " if j == i else "    "
            print(f"{prefix}{lines[j]}")
```

### 5. Create and Test JSON Format Fix
```python
# Create test to validate JSON formatting instruction
test_prompts = [
    # Current style (likely missing proper JSON instruction)
    "Classify this message: 'Create a GitHub issue about the login bug'",
    
    # Enhanced with explicit JSON instruction
    """Classify this message: 'Create a GitHub issue about the login bug'

You must respond with valid JSON only. Use double quotes around all property names and string values.

Required format:
{
    "category": "task_management", 
    "action": "create_issue",
    "confidence": 0.95
}""",

    # Alternative explicit instruction
    """Classify the intent of this message: 'Create a GitHub issue about the login bug'

IMPORTANT: Your response must be valid JSON with properly quoted property names.

Expected JSON structure:
{"category": "string", "action": "string", "confidence": number}"""
]

print("=== JSON Format Fix Testing ===")
for i, prompt in enumerate(test_prompts):
    print(f"\n--- Test Prompt {i+1} ---")
    print(f"Prompt: {prompt[:100]}...")
    
    # Here we would test each prompt format
    # In actual implementation, this would call the Anthropic API directly
    print("(Would test with Anthropic API here)")
```

## Expected Findings and Fixes

### Most Likely Issues to Find

**Missing JSON Format Instruction**:
```python
# Current (broken):
system_prompt = "You are an intent classifier. Classify the user's message."

# Fixed:
system_prompt = """You are an intent classifier. Classify the user's message.

IMPORTANT: You must respond with valid JSON only. All property names must be enclosed in double quotes.

Required response format:
{
    "category": "intent_category_here",
    "action": "specific_action_here", 
    "confidence": 0.0_to_1.0_number_here
}"""
```

**Insufficient JSON Schema Specification**:
```python
# Current (broken):
user_prompt = f"Classify: {message}"

# Fixed:
user_prompt = f"""Classify this message: "{message}"

Respond with valid JSON using this exact structure:
{{"category": "category_name", "action": "action_name", "confidence": confidence_score}}

Ensure all property names are in double quotes. Do not include any text outside the JSON object."""
```

## Implementation Requirements

### Fix Application
1. **Locate exact prompt construction** in LLM classifier
2. **Compare with working PM-011 version** to see what changed
3. **Add explicit JSON formatting instructions** to system/user prompts
4. **Test fix** with the failing performance test
5. **Verify JSON compliance** with multiple test messages

### Verification Steps
```bash
# After implementing fix, verify it works:
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

# Should show: PASSED and <500ms timing
```

### Evidence Required
```
=== JSON Prompt Fix Results ===

Current Prompt Analysis:
- Prompt construction method: [location and current structure]
- JSON instruction presence: [yes/no with details]
- Comparison with PM-011: [key differences found]

Root Cause Identified:
- Specific missing instruction: [exact missing JSON format requirement]
- Location of fix needed: [file and method/line]

Fix Applied:
- Before: [current prompt structure]
- After: [enhanced prompt with JSON instruction]
- Files modified: [list with line numbers]

Verification Results:
- Performance test: [PASSED/FAILED]
- Test timing: [actual ms vs 500ms requirement]
- JSON parsing: [works correctly with API response]
```

## Success Criteria
- [ ] Current prompt structure analyzed and documented
- [ ] Comparison with working PM-011 version completed  
- [ ] Missing JSON formatting instructions identified
- [ ] Fix applied to prompt construction
- [ ] Performance test passes with <500ms timing
- [ ] JSON parsing works correctly with enhanced prompts

## Time Estimate
20-25 minutes for complete investigation, fix, and verification

**Remember: No shortcuts. Debug the Anthropic API interaction properly and ensure robust JSON formatting instructions.**

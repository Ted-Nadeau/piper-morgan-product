# Agent Prompt: Phase 3B - Implement Historical Response Format Fix

**Agent**: Code
**Mission**: Implement the `response_format={"type": "json_object"}` parameter fix that Cursor found in historical analysis, or report if it conflicts with your previous changes.

## Context from Historical Analysis
- **Cursor found**: TextAnalyzer (July 2025) used `response_format={"type": "json_object"}` successfully
- **Missing from current**: LLM classifier doesn't use this parameter
- **Your previous fix**: You reported fixing "API interface mismatch + test mock issues"
- **Verification needed**: Determine if both fixes are needed or if there's a conflict

## Implementation Tasks

### 1. Verify Current State After Your Changes
```python
# Check what your previous fix actually implemented
print("=== Current LLM Classifier State After Your Fix ===")

# Look at the current complete() call
from services.intent_service.llm_classifier import LLMClassifier
import inspect

classifier = LLMClassifier()
if hasattr(classifier, '_llm_classify'):
    source = inspect.getsource(classifier._llm_classify)
    print("Current _llm_classify method:")
    print(source)

# Check if response_format parameter is already present
if "response_format" in source:
    print("✅ response_format already implemented in your fix")
else:
    print("❌ response_format still missing - needs to be added")
```

### 2. Analyze TextAnalyzer Working Pattern
```python
# Find and examine the TextAnalyzer implementation
import os
from pathlib import Path

print("=== TextAnalyzer Working Pattern Analysis ===")

# Look for TextAnalyzer files
text_analyzer_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if 'analyzer' in file.lower() and file.endswith('.py'):
            text_analyzer_files.append(os.path.join(root, file))

for file in text_analyzer_files:
    print(f"Found: {file}")
    with open(file, 'r') as f:
        content = f.read()
        if 'response_format' in content:
            print(f"response_format found in {file}")
            # Extract the relevant section
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'response_format' in line:
                    start = max(0, i-5)
                    end = min(len(lines), i+10)
                    print(f"Context around line {i+1}:")
                    for j in range(start, end):
                        prefix = ">>> " if j == i else "    "
                        print(f"{prefix}{lines[j]}")
                    break
```

### 3. Implement Response Format Fix
```python
# Based on findings, implement the response_format parameter

print("=== Implementing Response Format Fix ===")

# First, backup the current file
import shutil
shutil.copy('services/intent_service/llm_classifier.py', 'services/intent_service/llm_classifier.py.phase3-backup')

# Read current implementation
with open('services/intent_service/llm_classifier.py', 'r') as f:
    content = f.read()

print("Current file backed up to .phase3-backup")

# Check if your previous fix conflicts with response_format addition
if 'complete(' in content:
    print("Found complete() call - analyzing structure")

    # Look for the exact location where response_format should be added
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'complete(' in line or '.complete(' in line:
            print(f"Line {i+1}: {line.strip()}")
            # Show context around the complete call
            start = max(0, i-3)
            end = min(len(lines), i+8)
            print("Context:")
            for j in range(start, end):
                print(f"  {j+1:3d}: {lines[j]}")
            break

# The fix should add response_format parameter like this:
suggested_fix = '''
# Add to the complete() call:
response = await self.llm.complete(
    prompt=enhanced_prompt,
    max_tokens=200,
    temperature=0.3,
    response_format={"type": "json_object"}  # ADD THIS LINE
)
'''

print("Suggested fix pattern:")
print(suggested_fix)
```

### 4. Apply the Response Format Parameter
```python
# Apply the actual fix to add response_format parameter

print("=== Applying Response Format Parameter Fix ===")

# Read the current file
with open('services/intent_service/llm_classifier.py', 'r') as f:
    lines = f.readlines()

# Find the complete() call and add response_format parameter
modified = False
new_lines = []

for i, line in enumerate(lines):
    new_lines.append(line)

    # Look for the complete() call parameters
    if ('complete(' in line or '.complete(' in line) and not modified:
        # Look ahead to find where parameters end
        j = i + 1
        while j < len(lines) and ')' not in lines[j]:
            new_lines.append(lines[j])
            j += 1

        # Add response_format parameter before the closing parenthesis
        if j < len(lines) and ')' in lines[j]:
            # Add the response_format parameter
            indent = len(lines[j]) - len(lines[j].lstrip())
            response_format_line = ' ' * indent + 'response_format={"type": "json_object"}\n'
            new_lines.append(response_format_line)
            new_lines.append(lines[j])  # Add the closing line
            modified = True
            j += 1

        # Skip the lines we already processed
        i = j - 1
        continue

print(f"Response format parameter {'added' if modified else 'not added - manual intervention needed'}")

if modified:
    # Write the modified content
    with open('services/intent_service/llm_classifier.py', 'w') as f:
        f.writelines(new_lines)
    print("✅ File updated with response_format parameter")
else:
    print("⚠️ Could not automatically add parameter - manual fix needed")
```

### 5. Test the Combined Fix
```python
# Test if the combined fix (your changes + response_format) works
print("=== Testing Combined Fix ===")

try:
    from services.intent_service.llm_classifier import LLMClassifier
    import asyncio
    import json

    async def test_combined_fix():
        classifier = LLMClassifier()
        test_message = "Create a GitHub issue about the login bug"

        print(f"Testing: '{test_message}'")
        result = await classifier.classify(test_message)

        print(f"✅ Classification successful: {result}")
        print(f"Type: {type(result)}")

        # Verify it's properly structured
        if hasattr(result, 'category') and hasattr(result, 'confidence'):
            print(f"Category: {result.category}")
            print(f"Confidence: {result.confidence}")
            print("✅ Proper structure confirmed")
        else:
            print("⚠️ Result structure may need verification")

        return result

    # Run the test
    result = asyncio.run(test_combined_fix())

except Exception as e:
    print(f"❌ Combined fix test failed: {e}")
    print(f"Error type: {type(e).__name__}")

    # If it fails, we need to understand why
    import traceback
    traceback.print_exc()
```

### 6. Verify Performance Test Still Passes
```bash
# Run the performance test to ensure both fixes work together
PYTHONPATH=. python -m pytest tests/regression/test_queryrouter_lock.py::test_performance_requirement_queryrouter_initialization_under_500ms -xvs

# Also run the LLM classifier benchmarks
PYTHONPATH=. python -m pytest tests/performance/test_llm_classifier_benchmarks.py -xvs
```

## Conflict Resolution Scenarios

### Scenario A: Your Fix Already Includes response_format
```
If your previous API interface fix already added response_format:
- Report: "response_format already implemented in previous fix"
- Explain: How the interface fix included this parameter
- Verify: Tests still pass with current implementation
```

### Scenario B: response_format Needed in Addition to Your Fix
```
If response_format is still missing:
- Implement: Add the parameter to existing complete() call
- Test: Verify both fixes work together
- Report: "Combined fix applied - interface fix + response_format"
```

### Scenario C: Conflict Between Fixes
```
If adding response_format breaks your interface fix:
- Report: "Conflict detected between fixes"
- Analyze: Why the two approaches conflict
- Recommend: Which approach should take precedence based on evidence
```

## Evidence Requirements

### Implementation Status
```
=== Response Format Implementation ===
Current State: [already present / needs to be added / conflicts with existing]

If already present:
- Location: [file:line where response_format is used]
- Implementation: [exact code showing parameter usage]

If added:
- Change made: [before and after code]
- Location: [file:line of modification]
- Backup created: [backup file location]

If conflict:
- Conflict description: [specific issue between fixes]
- Recommendation: [which approach to use and why]
```

### Testing Results
```
=== Combined Fix Testing ===
LLM Classification Test:
- Input: "Create a GitHub issue about the login bug"
- Output: [actual result object]
- Status: [SUCCESS/FAILURE]
- JSON Structure: [proper/improper]

Performance Test Results:
- QueryRouter test: [PASSED/FAILED - timing]
- LLM benchmark test: [PASSED/FAILED - performance]
- Any new errors: [list or none]
```

### Integration Assessment
```
=== Fix Integration Analysis ===
Your Previous Fix: [brief description of interface changes]
Cursor's Historical Fix: [response_format parameter addition]
Combined Result: [working together / conflicting / redundant]

Final Implementation:
- API interface: [current implementation approach]
- JSON formatting: [current parameter usage]
- Test compatibility: [all tests passing / some issues]

Recommendation:
[Is current combined implementation the optimal solution?]
```

## Success Criteria
- [ ] Current state after your previous fix analyzed
- [ ] TextAnalyzer working pattern examined
- [ ] response_format parameter implementation attempted
- [ ] Combined fix tested with actual LLM calls
- [ ] Performance tests verified still passing
- [ ] Clear report on fix integration success/conflicts

## Time Estimate
20-25 minutes for analysis, implementation, and testing

## Critical Questions
1. **Does your interface fix already include response_format?** (check actual implementation)
2. **Can both fixes work together?** (test combined implementation)
3. **Which approach is more robust?** (interface fix vs response_format vs both)

**Focus: Determine if Cursor's historical fix adds value to your solution or if your fix already addresses the root cause completely.**
